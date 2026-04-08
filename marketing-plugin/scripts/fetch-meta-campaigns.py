#!/usr/bin/env python3
"""
fetch-meta-campaigns.py — Pull campaign data from Meta Marketing API (READ-ONLY).

Fetches campaigns, ad sets, ads, and daily insights from Meta Graph API v22.0.
Auto-discovers ad account ID from the access token.

Usage:
  python3 marketing-plugin/scripts/fetch-meta-campaigns.py --from-date 2026-03-01 --to-date 2026-04-01
  python3 marketing-plugin/scripts/fetch-meta-campaigns.py  # defaults to last 30 days
  python3 marketing-plugin/scripts/fetch-meta-campaigns.py --level adset  # insights at ad set level

Requires:
  pip install requests python-dotenv

SAFETY: This script ONLY uses GET endpoints.
        It NEVER creates, modifies, or deletes campaigns, ads, or any Meta resources.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
MARKETING_DATA_PATH = PLUGIN_ROOT / "data" / "marketing-data.json"
GRAPH_API_BASE = "https://graph.facebook.com/v22.0"

# Meta API page size (max 500 for most endpoints)
PAGE_SIZE = 200

# Rate limit: back off and retry on 429
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 60


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env (plugin dir first, then repo root)."""
    # Try plugin-local .env first, then fall back to repo root
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    access_token = os.environ.get("META_ACCESS_TOKEN")

    if not access_token:
        print("Error: META_ACCESS_TOKEN not set.", file=sys.stderr)
        print("  1. Copy .env.example to .env in the plugin directory", file=sys.stderr)
        print("  2. Add your Meta access token", file=sys.stderr)
        print("  3. Get a token from: https://developers.facebook.com/tools/explorer/", file=sys.stderr)
        print("  See SETUP.md for detailed instructions.", file=sys.stderr)
        sys.exit(1)

    return access_token


def api_get(token: str, path: str, params: dict = None) -> dict:
    """Make a GET request to Meta Graph API. GET only — no writes."""
    url = f"{GRAPH_API_BASE}{path}"
    all_params = {"access_token": token}
    if params:
        all_params.update(params)

    for attempt in range(MAX_RETRIES):
        resp = requests.get(url, params=all_params, timeout=30)

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 401:
            error_data = resp.json().get("error", {})
            print(f"Error: Authentication failed — {error_data.get('message', 'Invalid token')}", file=sys.stderr)
            print("  Your token may have expired. Get a new one from:", file=sys.stderr)
            print("  https://developers.facebook.com/tools/explorer/", file=sys.stderr)
            print("  Then update META_ACCESS_TOKEN in your .env file.", file=sys.stderr)
            sys.exit(1)

        if resp.status_code == 429 or (resp.status_code == 400 and "too many calls" in resp.text.lower()):
            if attempt < MAX_RETRIES - 1:
                print(f"  Rate limited. Waiting {RETRY_DELAY_SECONDS}s before retry {attempt + 2}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            print("Error: Meta API rate limit exceeded after retries.", file=sys.stderr)
            sys.exit(1)

        error_data = resp.json().get("error", {})
        print(f"Error: Meta API returned {resp.status_code} — {error_data.get('message', resp.text)}", file=sys.stderr)
        sys.exit(1)

    return {}


def paginate_get(token: str, path: str, params: dict = None, fields: str = None) -> list:
    """Fetch all pages from a Meta Graph API endpoint using cursor pagination."""
    all_items = []
    request_params = {"limit": PAGE_SIZE}
    if params:
        request_params.update(params)
    if fields:
        request_params["fields"] = fields

    next_url = None
    while True:
        if next_url is None:
            # First page: use api_get with the base path + params
            data = api_get(token, path, request_params)
        else:
            # Subsequent pages: follow the cursor URL directly (params already embedded)
            for attempt in range(MAX_RETRIES):
                resp = requests.get(next_url, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    break
                if resp.status_code == 429:
                    if attempt < MAX_RETRIES - 1:
                        print(f"  Rate limited. Waiting {RETRY_DELAY_SECONDS}s...")
                        time.sleep(RETRY_DELAY_SECONDS)
                        continue
                    print("Error: Rate limit exceeded during pagination.", file=sys.stderr)
                    sys.exit(1)
                error_data = resp.json().get("error", {})
                print(f"Error during pagination: {resp.status_code} — {error_data.get('message', resp.text)}", file=sys.stderr)
                sys.exit(1)

        items = data.get("data", [])
        all_items.extend(items)

        paging = data.get("paging", {})
        next_url = paging.get("next")
        if not next_url or not items:
            break

    return all_items


def load_existing_data() -> dict:
    """Load existing marketing-data.json or return empty scaffold."""
    if MARKETING_DATA_PATH.exists():
        with open(MARKETING_DATA_PATH) as f:
            return json.load(f)
    return {
        "last_sync": None,
        "meta_ad_account_id": None,
        "sync_status": "synced",
        "meta": {
            "last_sync": None,
            "campaigns": [],
            "ad_sets": [],
            "ads": [],
            "insights": [],
        },
        "ga4": None,
        "funnel_links": [],
    }


# ─── Account Discovery ──────────────────────────────────────────────────────

def discover_ad_accounts(token: str) -> list:
    """Discover ad accounts accessible with this token. GET only."""
    data = api_get(token, "/me/adaccounts", {
        "fields": "id,name,account_id,account_status,currency,business_name",
        "limit": 100,
    })
    accounts = data.get("data", [])
    return accounts


# ─── Data Fetchers ───────────────────────────────────────────────────────────

def fetch_campaigns(token: str, account_id: str) -> list:
    """Fetch all campaigns for an ad account. GET only."""
    fields = "id,name,objective,status,daily_budget,lifetime_budget,created_time,updated_time"
    items = paginate_get(token, f"/{account_id}/campaigns", fields=fields)
    return [
        {
            "campaign_id": c["id"],
            "name": c.get("name", ""),
            "objective": c.get("objective", ""),
            "status": c.get("status", ""),
            "daily_budget": float(c.get("daily_budget", 0)) / 100 if c.get("daily_budget") else 0.0,
            "lifetime_budget": float(c.get("lifetime_budget", 0)) / 100 if c.get("lifetime_budget") else 0.0,
            "currency": "AUD",
            "created_time": c.get("created_time", ""),
            "updated_time": c.get("updated_time", ""),
        }
        for c in items
    ]


def fetch_ad_sets(token: str, account_id: str) -> list:
    """Fetch all ad sets for an ad account. GET only."""
    fields = "id,campaign_id,name,status,targeting,optimization_goal,daily_budget,bid_strategy"
    items = paginate_get(token, f"/{account_id}/adsets", fields=fields)
    results = []
    for a in items:
        targeting = a.get("targeting", {})
        targeting_parts = []
        if targeting.get("age_min") or targeting.get("age_max"):
            targeting_parts.append(f"Age {targeting.get('age_min', '?')}-{targeting.get('age_max', '?')}")
        geo = targeting.get("geo_locations", {})
        countries = geo.get("countries", [])
        if countries:
            targeting_parts.append(f"Countries: {', '.join(countries)}")
        targeting_summary = "; ".join(targeting_parts) if targeting_parts else ""

        results.append({
            "ad_set_id": a["id"],
            "campaign_id": a.get("campaign_id", ""),
            "name": a.get("name", ""),
            "status": a.get("status", ""),
            "targeting_summary": targeting_summary,
            "optimization_goal": a.get("optimization_goal", ""),
            "daily_budget": float(a.get("daily_budget", 0)) / 100 if a.get("daily_budget") else 0.0,
            "bid_strategy": a.get("bid_strategy", ""),
        })
    return results


def fetch_ads(token: str, account_id: str) -> list:
    """Fetch all ads for an ad account. GET only."""
    fields = "id,adset_id,campaign_id,name,status,creative{id}"
    items = paginate_get(token, f"/{account_id}/ads", fields=fields)
    return [
        {
            "ad_id": a["id"],
            "ad_set_id": a.get("adset_id", ""),
            "campaign_id": a.get("campaign_id", ""),
            "name": a.get("name", ""),
            "status": a.get("status", ""),
            "creative_id": (a.get("creative") or {}).get("id", ""),
        }
        for a in items
    ]


def fetch_ad_creatives(token: str, ads: list) -> dict:
    """
    Fetch creative content (body, title, image URL) for each ad's creative_id. GET only.

    Returns a dict mapping creative_id → creative content fields.
    Batches requests with a small delay to respect rate limits.
    """
    creative_ids = list({a["creative_id"] for a in ads if a.get("creative_id")})
    if not creative_ids:
        return {}

    print(f"  Fetching creative content for {len(creative_ids)} creatives...")
    creatives = {}
    fields = "id,body,title,image_url,thumbnail_url,object_story_spec"

    for idx, cid in enumerate(creative_ids):
        try:
            data = api_get(token, f"/{cid}", {"fields": fields})
            creatives[cid] = {
                "creative_body": data.get("body", ""),
                "creative_title": data.get("title", ""),
                "creative_image_url": data.get("image_url", ""),
                "creative_thumbnail_url": data.get("thumbnail_url", ""),
            }
            # Extract additional fields from object_story_spec if available
            oss = data.get("object_story_spec", {})
            link_data = oss.get("link_data", {})
            if link_data:
                if not creatives[cid]["creative_body"] and link_data.get("message"):
                    creatives[cid]["creative_body"] = link_data["message"]
                if not creatives[cid]["creative_title"] and link_data.get("name"):
                    creatives[cid]["creative_title"] = link_data["name"]
                creatives[cid]["creative_link"] = link_data.get("link", "")
                creatives[cid]["creative_description"] = link_data.get("description", "")
                creatives[cid]["creative_cta_type"] = link_data.get("call_to_action", {}).get("type", "")
            video_data = oss.get("video_data", {})
            if video_data:
                if not creatives[cid]["creative_body"] and video_data.get("message"):
                    creatives[cid]["creative_body"] = video_data["message"]
                creatives[cid]["creative_video_id"] = video_data.get("video_id", "")

        except SystemExit:
            # api_get calls sys.exit on auth errors — re-raise
            raise
        except Exception as e:
            print(f"    Warning: Failed to fetch creative {cid}: {e}")
            creatives[cid] = {}

        # Rate limit: small delay every 10 requests
        if (idx + 1) % 10 == 0 and idx + 1 < len(creative_ids):
            time.sleep(1)

    print(f"  Fetched content for {len(creatives)} creatives")
    return creatives


def fetch_insights(token: str, account_id: str, from_date: str, to_date: str, level: str = "campaign") -> list:
    """
    Fetch daily insights for an ad account at the specified level. GET only.

    Level can be: campaign, adset, ad
    """
    params = {
        "fields": "campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,"
                  "impressions,clicks,spend,cpc,cpm,ctr,reach,frequency,"
                  "conversions,cost_per_conversion,actions",
        "time_range": json.dumps({"since": from_date, "until": to_date}),
        "time_increment": "1",
        "level": level,
        "limit": PAGE_SIZE,
    }
    items = paginate_get(token, f"/{account_id}/insights", params=params)

    results = []
    for i in items:
        # Determine entity type and ID based on level
        if level == "ad":
            entity_type = "ad"
            entity_id = i.get("ad_id", "")
        elif level == "adset":
            entity_type = "ad_set"
            entity_id = i.get("adset_id", "")
        else:
            entity_type = "campaign"
            entity_id = i.get("campaign_id", "")

        # Parse actions array
        actions = []
        for action in (i.get("actions") or []):
            actions.append({
                "action_type": action.get("action_type", ""),
                "value": int(action.get("value", 0)),
            })

        # Parse conversions — may be in actions or as a separate field
        conversions = 0
        cost_per_conversion = 0.0
        for action in actions:
            if action["action_type"] in ("lead", "offsite_conversion.fb_pixel_lead", "onsite_conversion.lead_grouped"):
                conversions += action["value"]
        conv_field = i.get("conversions")
        if conv_field:
            try:
                conversions = int(conv_field)
            except (ValueError, TypeError):
                pass
        cpc_field = i.get("cost_per_conversion")
        if cpc_field:
            try:
                cost_per_conversion = float(cpc_field)
            except (ValueError, TypeError):
                pass

        results.append({
            "entity_type": entity_type,
            "entity_id": entity_id,
            "date": i.get("date_start", ""),
            "impressions": int(i.get("impressions", 0)),
            "clicks": int(i.get("clicks", 0)),
            "spend": float(i.get("spend", 0)),
            "currency": "AUD",
            "cpc": float(i.get("cpc", 0)) if i.get("cpc") else 0.0,
            "cpm": float(i.get("cpm", 0)) if i.get("cpm") else 0.0,
            "ctr": float(i.get("ctr", 0)) if i.get("ctr") else 0.0,
            "reach": int(i.get("reach", 0)),
            "frequency": float(i.get("frequency", 0)) if i.get("frequency") else 0.0,
            "conversions": conversions,
            "cost_per_conversion": cost_per_conversion,
            "roas": 0.0,
            "actions": actions,
        })

    return results


# ─── Merge & Dedup ───────────────────────────────────────────────────────────

def merge_entities(existing: list, new: list, id_field: str) -> tuple:
    """Merge new entities into existing list, deduplicating by ID. Returns (merged, new_count)."""
    existing_ids = {e[id_field] for e in existing}
    added = 0
    merged = list(existing)
    for item in new:
        if item[id_field] not in existing_ids:
            merged.append(item)
            existing_ids.add(item[id_field])
            added += 1
        else:
            # Update existing entity with fresh data
            for idx, e in enumerate(merged):
                if e[id_field] == item[id_field]:
                    merged[idx] = item
                    break
    return merged, added


def merge_insights(existing: list, new: list) -> tuple:
    """Merge insights, deduplicating by entity_type + entity_id + date."""
    existing_keys = {
        (i["entity_type"], i["entity_id"], i["date"])
        for i in existing
    }
    added = 0
    merged = list(existing)
    for item in new:
        key = (item["entity_type"], item["entity_id"], item["date"])
        if key not in existing_keys:
            merged.append(item)
            existing_keys.add(key)
            added += 1
        else:
            # Update existing insight with fresh data
            for idx, e in enumerate(merged):
                if (e["entity_type"], e["entity_id"], e["date"]) == key:
                    merged[idx] = item
                    break
    return merged, added


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Meta ad campaign data (read-only).")
    parser.add_argument("--from-date", type=str, default=None,
                        help="Start date (YYYY-MM-DD). Default: 30 days ago.")
    parser.add_argument("--to-date", type=str, default=None,
                        help="End date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--level", type=str, default="all",
                        choices=["all", "campaign", "adset", "ad"],
                        help="Insights breakdown level. Default: all (campaign + adset + ad).")
    parser.add_argument("--skip-structure", action="store_true",
                        help="Skip fetching campaigns/adsets/ads (only fetch insights)")
    parser.add_argument("--skip-insights", action="store_true",
                        help="Skip fetching insights (only fetch structure)")
    args = parser.parse_args()

    # Defaults
    today = datetime.now(timezone.utc)
    from_date = args.from_date or (today - timedelta(days=30)).strftime("%Y-%m-%d")
    to_date = args.to_date or today.strftime("%Y-%m-%d")

    # Load env
    access_token = load_env()

    print(f"Date range: {from_date} → {to_date}")
    print(f"Insights level: {args.level}" + (" (campaign + adset + ad)" if args.level == "all" else ""))

    # Load existing data
    marketing_data = load_existing_data()

    # ── 1. Discover ad account ──
    cached_account = marketing_data.get("meta_ad_account_id")
    if cached_account:
        account_id = cached_account
        print(f"Using cached ad account: {account_id}")
    else:
        print("Discovering ad accounts...")
        accounts = discover_ad_accounts(access_token)
        if not accounts:
            print("Error: No ad accounts found for this token.", file=sys.stderr)
            print("  Make sure your token has ads_read permission.", file=sys.stderr)
            sys.exit(1)

        if len(accounts) == 1:
            account_id = accounts[0]["id"]
            print(f"  Found 1 ad account: {account_id} ({accounts[0].get('name', '')})")
        else:
            print(f"  Found {len(accounts)} ad accounts:")
            for idx, acc in enumerate(accounts):
                status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_REVIEW"}
                status = status_map.get(acc.get("account_status"), str(acc.get("account_status", "?")))
                print(f"    {idx + 1}. {acc['id']} — {acc.get('name', 'Unnamed')} ({status})")
            # Default to first active account
            account_id = accounts[0]["id"]
            print(f"  Using: {account_id}")

        marketing_data["meta_ad_account_id"] = account_id

    new_campaigns = 0
    new_ad_sets = 0
    new_ads = 0
    new_insights = 0

    # ── 2. Fetch campaign structure ──
    if not args.skip_structure:
        print("\nFetching campaigns...")
        campaigns = fetch_campaigns(access_token, account_id)
        marketing_data["meta"]["campaigns"], new_campaigns = merge_entities(
            marketing_data["meta"]["campaigns"], campaigns, "campaign_id"
        )
        print(f"  {len(campaigns)} campaigns fetched ({new_campaigns} new)")

        print("Fetching ad sets...")
        ad_sets = fetch_ad_sets(access_token, account_id)
        marketing_data["meta"]["ad_sets"], new_ad_sets = merge_entities(
            marketing_data["meta"]["ad_sets"], ad_sets, "ad_set_id"
        )
        print(f"  {len(ad_sets)} ad sets fetched ({new_ad_sets} new)")

        print("Fetching ads...")
        ads = fetch_ads(access_token, account_id)
        marketing_data["meta"]["ads"], new_ads = merge_entities(
            marketing_data["meta"]["ads"], ads, "ad_id"
        )
        print(f"  {len(ads)} ads fetched ({new_ads} new)")

        # Fetch creative content for each ad
        print("Fetching ad creative content...")
        creatives = fetch_ad_creatives(access_token, ads)
        if creatives:
            for ad_rec in marketing_data["meta"]["ads"]:
                cid = ad_rec.get("creative_id", "")
                if cid and cid in creatives:
                    ad_rec.update(creatives[cid])
    else:
        print("\nSkipping structure (--skip-structure)")

    # ── 3. Fetch insights ──
    if not args.skip_insights:
        if args.level == "all":
            # Fetch all three levels for complete data
            for level in ["campaign", "adset", "ad"]:
                print(f"\nFetching insights ({level} level, {from_date} → {to_date})...")
                insights = fetch_insights(access_token, account_id, from_date, to_date, level)
                marketing_data["meta"]["insights"], level_new = merge_insights(
                    marketing_data["meta"]["insights"], insights
                )
                new_insights += level_new
                print(f"  {len(insights)} {level} insight rows fetched ({level_new} new)")
        else:
            print(f"\nFetching insights ({args.level} level, {from_date} → {to_date})...")
            insights = fetch_insights(access_token, account_id, from_date, to_date, args.level)
            marketing_data["meta"]["insights"], new_insights = merge_insights(
                marketing_data["meta"]["insights"], insights
            )
            print(f"  {len(insights)} insight rows fetched ({new_insights} new)")
    else:
        print("\nSkipping insights (--skip-insights)")

    # Sort insights by date (newest first)
    marketing_data["meta"]["insights"].sort(key=lambda i: i.get("date", ""), reverse=True)

    # Update sync metadata
    marketing_data["last_sync"] = today.isoformat()
    marketing_data["meta"]["last_sync"] = today.isoformat()
    marketing_data["sync_status"] = "synced"

    # Ensure output directory exists
    MARKETING_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save
    with open(MARKETING_DATA_PATH, "w") as f:
        json.dump(marketing_data, f, indent=2)

    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Campaigns: {len(marketing_data['meta']['campaigns'])} total ({new_campaigns} new)")
    print(f"  Ad Sets:   {len(marketing_data['meta']['ad_sets'])} total ({new_ad_sets} new)")
    print(f"  Ads:       {len(marketing_data['meta']['ads'])} total ({new_ads} new)")
    print(f"  Insights:  {len(marketing_data['meta']['insights'])} rows ({new_insights} new)")
    print(f"  Saved to:  {MARKETING_DATA_PATH}")

    # Summary of spend by campaign
    if marketing_data["meta"]["insights"]:
        campaign_spend = {}
        for insight in marketing_data["meta"]["insights"]:
            if insight.get("date", "") >= from_date and insight["entity_type"] == "campaign":
                cid = insight["entity_id"]
                campaign_spend[cid] = campaign_spend.get(cid, 0) + insight.get("spend", 0)

        if campaign_spend:
            # Map campaign IDs to names
            campaign_names = {c["campaign_id"]: c["name"] for c in marketing_data["meta"]["campaigns"]}
            print(f"\n  Spend by campaign ({from_date} → {to_date}):")
            for cid, spend in sorted(campaign_spend.items(), key=lambda x: x[1], reverse=True):
                name = campaign_names.get(cid, cid)
                print(f"    {name}: ${spend:,.2f}")

            total_spend = sum(campaign_spend.values())
            total_clicks = sum(
                i.get("clicks", 0) for i in marketing_data["meta"]["insights"]
                if i.get("date", "") >= from_date and i["entity_type"] == "campaign"
            )
            total_impressions = sum(
                i.get("impressions", 0) for i in marketing_data["meta"]["insights"]
                if i.get("date", "") >= from_date and i["entity_type"] == "campaign"
            )
            print(f"\n  Totals: ${total_spend:,.2f} spend | {total_impressions:,} impressions | {total_clicks:,} clicks")
            if total_clicks > 0:
                print(f"  Avg CPC: ${total_spend / total_clicks:.2f}")
            if total_impressions > 0:
                print(f"  Avg CTR: {(total_clicks / total_impressions) * 100:.2f}%")


if __name__ == "__main__":
    main()
