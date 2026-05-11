#!/usr/bin/env python3
"""
scrape-competitor-ads.py — Scrape competitor Meta ads via Apify Facebook Ads Scraper.

Fetches competitor ad creatives, copy, and metadata from Meta Ad Library.
Normalizes results into competitor-data.json with merge/dedup and activity tracking.

Usage:
  python3 marketing-plugin/scripts/scrape-competitor-ads.py --campaign-id marketing-plugin --pages 12345678,87654321
  python3 marketing-plugin/scripts/scrape-competitor-ads.py --campaign-id marketing-plugin --all  # load watchlist from competitor-data.json
  python3 marketing-plugin/scripts/scrape-competitor-ads.py --campaign-id marketing-plugin --all --country US
  python3 marketing-plugin/scripts/scrape-competitor-ads.py --campaign-id marketing-plugin --search "business automation" --country AU
  python3 marketing-plugin/scripts/scrape-competitor-ads.py --campaign-id marketing-plugin --search "CRM software" --country AU --max-items 100

Requires:
  pip install requests python-dotenv
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/
COMPETITOR_DATA_PATH: Path = None  # Set in main() after --campaign-id is parsed
APIFY_API_BASE = "https://api.apify.com/v2"
ACTOR_ID = "apify~facebook-ads-scraper"

# Meta Ad Library base URL — the actor takes these as startUrls
AD_LIBRARY_BASE = "https://www.facebook.com/ads/library/"

# Polling interval for Apify run completion
POLL_INTERVAL_SECONDS = 5
MAX_POLL_ATTEMPTS = 120  # 10 minutes max

# Rate limit: back off and retry on transient errors
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 10


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env (plugin dir first, then repo root)."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    token = os.environ.get("APIFY_API_TOKEN")

    if not token:
        print("Error: APIFY_API_TOKEN not set.", file=sys.stderr)
        print("  1. Add APIFY_API_TOKEN to your .env file", file=sys.stderr)
        print("  2. Get a token from: https://console.apify.com/account/integrations", file=sys.stderr)
        sys.exit(1)

    return token


def load_competitor_data() -> dict:
    """Load existing competitor-data.json or return empty scaffold."""
    if COMPETITOR_DATA_PATH.exists():
        with open(COMPETITOR_DATA_PATH) as f:
            return json.load(f)
    return {
        "meta": {
            "last_scrape": None,
            "scrape_status": "never_scraped",
            "total_ads_tracked": 0,
            "winner_count": 0,
        },
        "watchlist": [],
        "ads": [],
    }


def save_competitor_data(data: dict):
    """Save competitor-data.json, ensuring directory exists."""
    COMPETITOR_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPETITOR_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def build_ad_library_url(country_code: str, search_terms: str = None, page_id: str = None) -> str:
    """Build a Meta Ad Library URL for the Apify actor's startUrls input."""
    params = f"active_status=active&ad_type=all&country={country_code}"
    if search_terms:
        params += f"&q={quote(search_terms)}&search_type=keyword_unordered"
    if page_id:
        params += f"&view_all_page_id={page_id}&search_type=page"
    return f"{AD_LIBRARY_BASE}?{params}"


# ─── Apify API ────────────────────────────────────────────────────────────────

def submit_apify_run(token: str, start_urls: list, max_items: int = 500) -> str:
    """Submit an Apify actor run with startUrls and return the run ID."""
    url = f"{APIFY_API_BASE}/acts/{ACTOR_ID}/runs?token={token}"
    payload = {
        "startUrls": [{"url": u} for u in start_urls],
        "maxItems": max_items,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, json=payload, timeout=30)

            if resp.status_code in (200, 201):
                run_data = resp.json().get("data", {})
                run_id = run_data.get("id")
                if not run_id:
                    print(f"Error: Apify returned success but no run ID.", file=sys.stderr)
                    print(f"  Response: {resp.text[:500]}", file=sys.stderr)
                    sys.exit(1)
                return run_id

            if resp.status_code == 401:
                print("Error: Authentication failed — invalid APIFY_API_TOKEN.", file=sys.stderr)
                print("  Check your token at: https://console.apify.com/account/integrations", file=sys.stderr)
                sys.exit(1)

            if resp.status_code == 429:
                if attempt < MAX_RETRIES - 1:
                    print(f"  Rate limited. Waiting {RETRY_DELAY_SECONDS}s before retry {attempt + 2}/{MAX_RETRIES}...")
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
                print("Error: Apify rate limit exceeded after retries.", file=sys.stderr)
                sys.exit(1)

            print(f"Error: Apify returned {resp.status_code} — {resp.text[:500]}", file=sys.stderr)
            sys.exit(1)

        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                print(f"  Request timed out. Retrying {attempt + 2}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            print("Error: Apify request timed out after retries.", file=sys.stderr)
            sys.exit(1)

    return ""


def poll_apify_run(token: str, run_id: str) -> bool:
    """Poll Apify run until completion. Returns True if succeeded."""
    url = f"{APIFY_API_BASE}/acts/{ACTOR_ID}/runs/{run_id}?token={token}"

    for attempt in range(MAX_POLL_ATTEMPTS):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code != 200:
                print(f"  Warning: Poll returned {resp.status_code}, retrying...")
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            run_data = resp.json().get("data", {})
            status = run_data.get("status", "UNKNOWN")

            if status == "SUCCEEDED":
                return True
            elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                print(f"Error: Apify run {status}.", file=sys.stderr)
                return False
            else:
                if attempt % 6 == 0:  # Print status every 30s
                    print(f"  Run status: {status} (polling {attempt * POLL_INTERVAL_SECONDS}s)...")
                time.sleep(POLL_INTERVAL_SECONDS)

        except requests.exceptions.Timeout:
            time.sleep(POLL_INTERVAL_SECONDS)

    print("Error: Apify run timed out after maximum poll attempts.", file=sys.stderr)
    return False


def fetch_apify_results(token: str, run_id: str) -> list:
    """Fetch dataset items from a completed Apify run via the dataset endpoint."""
    # First get the dataset ID from the run
    run_url = f"{APIFY_API_BASE}/acts/{ACTOR_ID}/runs/{run_id}?token={token}"
    try:
        resp = requests.get(run_url, timeout=30)
        if resp.status_code == 200:
            dataset_id = resp.json().get("data", {}).get("defaultDatasetId")
            if dataset_id:
                return _fetch_dataset(token, dataset_id)
    except requests.exceptions.Timeout:
        pass

    print("Warning: Could not get dataset ID from run, trying direct endpoint...", file=sys.stderr)
    return _fetch_dataset_from_run(token, run_id)


def _fetch_dataset(token: str, dataset_id: str) -> list:
    """Fetch items from a dataset by ID."""
    url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items?token={token}"
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=60)
            if resp.status_code == 200:
                return resp.json()
            if attempt < MAX_RETRIES - 1:
                print(f"  Fetch failed ({resp.status_code}). Retrying {attempt + 2}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            print(f"Error: Failed to fetch results — {resp.status_code}", file=sys.stderr)
            return []
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                print(f"  Fetch timed out. Retrying {attempt + 2}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            print("Error: Fetch timed out after retries.", file=sys.stderr)
            return []
    return []


def _fetch_dataset_from_run(token: str, run_id: str) -> list:
    """Fallback: fetch dataset items directly from run endpoint."""
    url = f"{APIFY_API_BASE}/acts/{ACTOR_ID}/runs/{run_id}/dataset/items?token={token}"
    try:
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200:
            return resp.json()
    except requests.exceptions.Timeout:
        pass
    return []


# ─── Normalization ────────────────────────────────────────────────────────────

def normalize_ad(result: dict, today_str: str) -> dict:
    """Normalize an Apify ad result into our schema.

    The actor returns a different schema than the old one:
    - adArchiveID (not id)
    - snapshot.body.text (not body)
    - snapshot.title (not title)
    - snapshot.images[].originalImageUrl / snapshot.videos[].videoHdUrl
    - snapshot.cards[].originalImageUrl / .videoHdUrl
    - snapshot.linkUrl, snapshot.ctaType, snapshot.ctaText
    - publisherPlatform (not platforms)
    - startDate is a unix timestamp (not ISO string)
    """
    snapshot = result.get("snapshot") or {}
    body_obj = snapshot.get("body")
    body_text = ""
    if isinstance(body_obj, dict):
        body_text = body_obj.get("text", "") or body_obj.get("markup", {}).get("__html", "")
    elif isinstance(body_obj, str):
        body_text = body_obj

    # Extract creative URLs — check cards first, then top-level images/videos
    creative_url = None
    creative_type = None

    images = snapshot.get("images") or []
    videos = snapshot.get("videos") or []
    cards = snapshot.get("cards") or []

    # Try top-level videos first (most valuable)
    for v in videos:
        if isinstance(v, dict):
            url = v.get("videoHdUrl") or v.get("videoSdUrl")
            if url:
                creative_url = url
                creative_type = "video"
                break

    # Then top-level images
    if not creative_url:
        for img in images:
            if isinstance(img, dict):
                url = img.get("originalImageUrl") or img.get("resizedImageUrl")
                if url:
                    creative_url = url
                    creative_type = "image"
                    break

    # Then cards
    if not creative_url:
        for card in cards:
            url = card.get("videoHdUrl") or card.get("videoSdUrl")
            if url:
                creative_url = url
                creative_type = "video"
                break
            url = card.get("originalImageUrl") or card.get("resizedImageUrl")
            if url:
                creative_url = url
                creative_type = "image"
                break

    # Parse startDate — could be unix timestamp or ISO string
    start_date = result.get("startDate", "")
    if isinstance(start_date, (int, float)) and start_date > 0:
        start_date = datetime.fromtimestamp(start_date, tz=timezone.utc).strftime("%Y-%m-%d")

    return {
        "ad_id": str(result.get("adArchiveID") or result.get("adId") or result.get("id", "")),
        "page_id": str(result.get("pageId") or result.get("pageID", "")),
        "page_name": result.get("pageName", ""),
        "ad_copy": body_text,
        "headline": snapshot.get("title", ""),
        "cta_type": snapshot.get("ctaType", ""),
        "cta_text": snapshot.get("ctaText", ""),
        "creative_url": creative_url,
        "creative_type": creative_type,
        "local_path": None,
        "landing_page_url": snapshot.get("linkUrl", ""),
        "link_description": snapshot.get("linkDescription", ""),
        "platforms": result.get("publisherPlatform", []),
        "display_format": snapshot.get("displayFormat", ""),
        "started_running": start_date,
        "first_seen": today_str,
        "last_seen": today_str,
        "days_active": 0,
        "status": "active" if result.get("isActive") else "inactive",
        "ad_library_url": f"https://www.facebook.com/ads/library/?id={result.get('adArchiveID', '')}",
        "analysis": None,
    }


def calculate_days_active(ad: dict, today_str: str) -> dict:
    """Calculate days_active and status for an ad."""
    try:
        first = datetime.strptime(ad["first_seen"], "%Y-%m-%d")
        last = datetime.strptime(ad["last_seen"], "%Y-%m-%d")
        today = datetime.strptime(today_str, "%Y-%m-%d")

        ad["days_active"] = (last - first).days + 1

        # If we haven't seen it in over 7 days, mark as inactive
        if (today - last).days > 7:
            ad["status"] = "inactive"
        else:
            ad["status"] = "active"
    except (ValueError, KeyError):
        pass

    return ad


# ─── Merge & Dedup ───────────────────────────────────────────────────────────

def merge_ads(existing: list, new: list, today_str: str) -> tuple:
    """Merge new ads into existing list, deduplicating by ad_id. Returns (merged, new_count, updated_count)."""
    existing_map = {ad["ad_id"]: ad for ad in existing}
    new_count = 0
    updated_count = 0

    for ad in new:
        ad_id = ad["ad_id"]
        if ad_id in existing_map:
            # Update existing: refresh last_seen, preserve first_seen, local_path, analysis
            old = existing_map[ad_id]
            ad["first_seen"] = old.get("first_seen", ad["first_seen"])
            ad["local_path"] = old.get("local_path")
            ad["analysis"] = old.get("analysis")
            ad["last_seen"] = today_str
            existing_map[ad_id] = calculate_days_active(ad, today_str)
            updated_count += 1
        else:
            existing_map[ad_id] = calculate_days_active(ad, today_str)
            new_count += 1

    merged = list(existing_map.values())
    return merged, new_count, updated_count


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scrape competitor Meta ads via Apify.")
    parser.add_argument("--campaign-id", type=str, required=True,
                        help="Campaign ID (e.g. marketing-plugin). Competitor data is scoped per campaign.")
    parser.add_argument("--pages", type=str, default=None,
                        help="Comma-separated Meta Page IDs to scrape.")
    parser.add_argument("--all", action="store_true",
                        help="Scrape all pages from the watchlist in competitor-data.json.")
    parser.add_argument("--search", type=str, default=None,
                        help="Keyword search to discover competitors (e.g. 'business automation').")
    parser.add_argument("--country", type=str, default="AU",
                        help="Country code for ad library search (default: AU).")
    parser.add_argument("--max-items", type=int, default=500,
                        help="Maximum ads to return (default: 500). Lower = cheaper.")
    args = parser.parse_args()

    global COMPETITOR_DATA_PATH
    COMPETITOR_DATA_PATH = PLUGIN_ROOT / "data" / "campaigns" / args.campaign_id / "competitor-data.json"

    if not args.pages and not args.all and not args.search:
        print("Error: Provide --pages, --all, or --search.", file=sys.stderr)
        print("  --pages 12345678,87654321   Scrape specific page IDs", file=sys.stderr)
        print("  --all                       Scrape all watchlist pages from competitor-data.json", file=sys.stderr)
        print("  --search 'keyword'          Discover competitors by keyword search", file=sys.stderr)
        sys.exit(1)

    # Load env
    token = load_env()

    # Load existing data
    data = load_competitor_data()

    # ── Search / discovery mode ──
    if args.search:
        print(f"Discovery search: \"{args.search}\"")
        print(f"Country: {args.country} | Max items: {args.max_items}")

        url = build_ad_library_url(args.country, search_terms=args.search)
        print(f"Ad Library URL: {url}")

        print("\nSubmitting Apify run...")
        run_id = submit_apify_run(token, [url], max_items=args.max_items)
        print(f"  Run ID: {run_id}")

        print("\nWaiting for completion...")
        success = poll_apify_run(token, run_id)
        if not success:
            print("Search failed.", file=sys.stderr)
            sys.exit(1)
        print("  Search completed.")

        print("\nFetching results...")
        results = fetch_apify_results(token, run_id)
        print(f"  {len(results)} ads found.\n")

        if not results:
            print("No ads found for this search term.")
            return

        # Group by page to produce a discovery report
        pages = {}
        for r in results:
            pid = str(r.get("pageId") or r.get("pageID", "unknown"))
            if pid not in pages:
                pages[pid] = {
                    "page_name": r.get("pageName", ""),
                    "page_id": pid,
                    "ad_count": 0,
                    "sample_ads": [],
                }
            pages[pid]["ad_count"] += 1
            if len(pages[pid]["sample_ads"]) < 3:
                ad_id = r.get("adArchiveID") or r.get("adId") or r.get("id", "")
                snap = r.get("snapshot", {})
                body_obj = snap.get("body", {})
                body = body_obj.get("text", "") if isinstance(body_obj, dict) else str(body_obj or "")
                pages[pid]["sample_ads"].append({
                    "ad_id": str(ad_id),
                    "headline": snap.get("title", ""),
                    "body": (body or "")[:120],
                    "link": f"https://www.facebook.com/ads/library/?id={ad_id}",
                })

        # Sort by ad count descending
        sorted_pages = sorted(pages.values(), key=lambda p: p["ad_count"], reverse=True)

        # Output as JSON for easy parsing
        output = {
            "search_term": args.search,
            "country": args.country,
            "total_ads": len(results),
            "unique_pages": len(sorted_pages),
            "pages": sorted_pages,
        }
        # Write discovery results to a file
        discovery_path = PLUGIN_ROOT / "data" / "discovery-results.json"
        with open(discovery_path, "w") as f:
            json.dump(output, f, indent=2)

        print(f"{'─' * 60}")
        print(f"Discovery complete: {len(results)} ads from {len(sorted_pages)} pages")
        print(f"Results saved to: {discovery_path}")
        print(f"\nTop pages by ad count:")
        for p in sorted_pages[:20]:
            print(f"  {p['page_name']:<40} | Page ID: {p['page_id']:<15} | {p['ad_count']} ads")
            for s in p["sample_ads"][:1]:
                print(f"    └─ {s['link']}")
        return

    # ── Page scrape mode ──
    if args.pages:
        page_ids = [p.strip() for p in args.pages.split(",") if p.strip()]
    else:
        page_ids = [str(w.get("page_id")) for w in data.get("watchlist", []) if w.get("page_id")]
        if not page_ids:
            print("Error: No pages in watchlist. Add competitors to competitor-data.json first,", file=sys.stderr)
            print("  or use --pages to specify Page IDs directly.", file=sys.stderr)
            sys.exit(1)

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Scraping {len(page_ids)} page(s): {', '.join(page_ids)}")
    print(f"Country: {args.country} | Max items: {args.max_items}")

    # Build startUrls — one per page
    start_urls = [build_ad_library_url(args.country, page_id=pid) for pid in page_ids]
    for u in start_urls:
        print(f"  {u}")

    # ── 1. Submit Apify run ──
    print("\nSubmitting Apify run...")
    run_id = submit_apify_run(token, start_urls, max_items=args.max_items)
    print(f"  Run ID: {run_id}")

    # ── 2. Poll for completion ──
    print("\nWaiting for completion...")
    success = poll_apify_run(token, run_id)
    if not success:
        data.setdefault("meta", {})["scrape_status"] = "failed"
        save_competitor_data(data)
        sys.exit(1)

    print("  Run completed successfully.")

    # ── 3. Fetch results ──
    print("\nFetching results...")
    results = fetch_apify_results(token, run_id)
    print(f"  {len(results)} raw ad results returned.")

    if not results:
        print("  No ads found for these pages.")
        data.setdefault("meta", {})["last_scrape"] = today_str
        data["meta"]["scrape_status"] = "no_results"
        save_competitor_data(data)
        return

    # ── 4. Normalize results ──
    print("\nNormalizing ad data...")
    normalized = []
    for result in results:
        ad = normalize_ad(result, today_str)
        if ad["ad_id"]:
            normalized.append(ad)

    print(f"  {len(normalized)} ads normalized.")

    # ── 5. Merge with existing data ──
    existing_ads = data.get("ads", [])
    merged_ads, new_count, updated_count = merge_ads(existing_ads, normalized, today_str)

    # Recalculate days_active for all existing ads not in this batch
    scraped_ids = {ad["ad_id"] for ad in normalized}
    for ad in merged_ads:
        if ad["ad_id"] not in scraped_ids:
            calculate_days_active(ad, today_str)

    # ── 6. Variant deduplication ──
    variant_groups = {}
    for ad in merged_ads:
        key = (
            (ad.get("page_id") or "").strip().lower()
            + "|" + (ad.get("ad_copy") or "").strip().lower()
            + "|" + (ad.get("headline") or "").strip().lower()
        )
        group_hash = hashlib.sha256(key.encode()).hexdigest()[:12]
        variant_groups.setdefault(group_hash, []).append(ad)
        ad["variant_group"] = group_hash

    multi_variant_groups = sum(1 for g in variant_groups.values() if len(g) > 1)
    multi_variant_ads = sum(len(g) for g in variant_groups.values() if len(g) > 1)
    print(f"\n  {multi_variant_groups} variant groups detected across {multi_variant_ads} ads")

    # ── 7. Archive stale ads ──
    archive_cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
    newly_archived = 0
    for ad in merged_ads:
        if ad.get("status") != "archived" and ad.get("last_seen", "") < archive_cutoff:
            ad["status"] = "archived"
            newly_archived += 1

    data["ads"] = merged_ads
    data.setdefault("meta", {})
    data["meta"]["last_scrape"] = today_str
    data["meta"]["scrape_status"] = "success"
    data["meta"]["total_ads_tracked"] = len(merged_ads)
    data["meta"]["winner_count"] = sum(1 for a in merged_ads if a.get("days_active", 0) >= 30)

    # ── 8. Save ──
    save_competitor_data(data)

    # ── 9. Print summary ──
    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  New ads found:      {new_count}")
    print(f"  Existing updated:   {updated_count}")
    print(f"  Newly archived:     {newly_archived}")
    print(f"  Total ads tracked:  {len(merged_ads)}")

    # Per-competitor breakdown
    competitor_counts = {}
    for ad in merged_ads:
        name = ad.get("page_name") or ad.get("page_id", "unknown")
        if name not in competitor_counts:
            competitor_counts[name] = {"total": 0, "active": 0}
        competitor_counts[name]["total"] += 1
        if ad.get("status") == "active":
            competitor_counts[name]["active"] += 1

    if competitor_counts:
        print(f"\n  Per-competitor breakdown:")
        for name, counts in sorted(competitor_counts.items()):
            print(f"    {name}: {counts['total']} total ({counts['active']} active)")

    print(f"\n  Saved to: {COMPETITOR_DATA_PATH}")


if __name__ == "__main__":
    main()
