#!/usr/bin/env python3
"""
fetch-ga4-analytics.py — Pull landing page and conversion data from GA4 (READ-ONLY).

Fetches session, pageview, conversion, and source/medium data from the GA4 Data API.
Uses a service account for authentication.

Usage:
  python3 marketing-plugin/scripts/fetch-ga4-analytics.py --from-date 2026-03-01 --to-date 2026-04-01
  python3 marketing-plugin/scripts/fetch-ga4-analytics.py  # defaults to last 30 days

Requires:
  pip install google-analytics-data python-dotenv

SAFETY: This script ONLY reads analytics data. It never modifies GA4 configuration.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
        FilterExpression,
        Filter,
    )
except ImportError:
    print("Error: 'google-analytics-data' not installed. Run: pip install google-analytics-data", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/
MARKETING_DATA_PATH = PLUGIN_ROOT / "data" / "marketing-data.json"
ROW_LIMIT = 100000


# ─── Helpers ──────────────────────────────────────────────────────────────────

PROPERTY_ALIASES = {
    "landing": "GA4_PROPERTY_ID",       # {YOUR_LANDING_DOMAIN} — Meta ads funnel
    "home": "GA4_PROPERTY_ID_HOME",     # {YOUR_DOMAIN} — main website
}


def load_env(property_alias: str = None):
    """Load environment variables from .env (plugin dir first, then repo root)."""
    # Try plugin-local .env first, then fall back to repo root
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    # Determine which property to use
    if property_alias and property_alias in PROPERTY_ALIASES:
        env_key = PROPERTY_ALIASES[property_alias]
    else:
        env_key = "GA4_PROPERTY_ID"

    property_id = os.environ.get(env_key)
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if not property_id:
        print(f"Error: {env_key} not set.", file=sys.stderr)
        print("  1. Copy .env.example to .env in the plugin directory", file=sys.stderr)
        print("  2. Add your GA4 Property ID", file=sys.stderr)
        print("  See SETUP.md for detailed instructions.", file=sys.stderr)
        sys.exit(1)

    if credentials_path:
        # Resolve relative paths against plugin root first, then repo root
        creds_file = Path(credentials_path)
        if not creds_file.is_absolute():
            if (PLUGIN_ROOT / creds_file).exists():
                creds_file = PLUGIN_ROOT / creds_file
            elif (PLUGIN_ROOT.parent / creds_file).exists():
                creds_file = PLUGIN_ROOT.parent / creds_file
            else:
                print(f"Error: Service account key not found at {creds_file}", file=sys.stderr)
                print(f"  Searched: {PLUGIN_ROOT / creds_file}", file=sys.stderr)
                print(f"  Searched: {PLUGIN_ROOT.parent / creds_file}", file=sys.stderr)
                print("  Place the JSON key file in the plugin directory.", file=sys.stderr)
                sys.exit(1)
        elif not creds_file.exists():
            print(f"Error: Service account key not found at {creds_file}", file=sys.stderr)
            sys.exit(1)
        # Set for the Google client library
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(creds_file)
    else:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS not set.", file=sys.stderr)
        print("  Add path to your service account JSON in .env", file=sys.stderr)
        print("  See SETUP.md for instructions on creating a service account.", file=sys.stderr)
        sys.exit(1)

    return property_id


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


def create_ga4_scaffold():
    """Return empty GA4 data structure."""
    return {
        "last_sync": None,
        "property_id": None,
        "landing_pages": [],
        "conversions": [],
    }


# ─── GA4 Reports ─────────────────────────────────────────────────────────────

def fetch_landing_page_report(client, property_id: str, from_date: str, to_date: str) -> list:
    """
    Fetch landing page performance by source/medium/campaign.
    READ-ONLY — only calls runReport.
    """
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="landingPage"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
            Dimension(name="sessionCampaignName"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="screenPageViews"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="conversions"),
        ],
        date_ranges=[DateRange(start_date=from_date, end_date=to_date)],
        limit=ROW_LIMIT,
    )

    response = client.run_report(request)
    results = []

    for row in response.rows:
        dims = row.dimension_values
        mets = row.metric_values

        # Parse date from YYYYMMDD to YYYY-MM-DD
        raw_date = dims[0].value
        date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}" if len(raw_date) == 8 else raw_date

        sessions = int(mets[0].value)
        if sessions == 0:
            continue

        results.append({
            "date": date_str,
            "landing_page": dims[1].value,
            "source": dims[2].value,
            "medium": dims[3].value,
            "campaign": dims[4].value if dims[4].value != "(not set)" else "",
            "sessions": sessions,
            "total_users": int(mets[1].value),
            "new_users": int(mets[2].value),
            "pageviews": int(mets[3].value),
            "bounce_rate": round(float(mets[4].value), 4),
            "avg_session_duration": round(float(mets[5].value), 2),
            "conversions": int(float(mets[6].value)),
        })

    return results


def fetch_conversion_report(client, property_id: str, from_date: str, to_date: str) -> list:
    """
    Fetch conversion events by source/medium/campaign.
    READ-ONLY — only calls runReport.
    """
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="eventName"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
            Dimension(name="sessionCampaignName"),
        ],
        metrics=[
            Metric(name="eventCount"),
            Metric(name="eventValue"),
        ],
        date_ranges=[DateRange(start_date=from_date, end_date=to_date)],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="isConversionEvent",
                string_filter=Filter.StringFilter(value="true"),
            )
        ),
        limit=ROW_LIMIT,
    )

    try:
        response = client.run_report(request)
    except Exception as e:
        # isConversionEvent filter may not work on all properties — fall back to unfiltered
        if "isConversionEvent" in str(e):
            print("  Note: isConversionEvent filter not available, fetching key events instead...")
            request = RunReportRequest(
                property=f"properties/{property_id}",
                dimensions=[
                    Dimension(name="date"),
                    Dimension(name="eventName"),
                    Dimension(name="sessionSource"),
                    Dimension(name="sessionMedium"),
                    Dimension(name="sessionCampaignName"),
                ],
                metrics=[
                    Metric(name="eventCount"),
                    Metric(name="eventValue"),
                ],
                date_ranges=[DateRange(start_date=from_date, end_date=to_date)],
                limit=ROW_LIMIT,
            )
            response = client.run_report(request)
        else:
            raise

    results = []
    for row in response.rows:
        dims = row.dimension_values
        mets = row.metric_values

        count = int(mets[0].value)
        if count == 0:
            continue

        raw_date = dims[0].value
        date_str = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}" if len(raw_date) == 8 else raw_date

        results.append({
            "date": date_str,
            "event_name": dims[1].value,
            "source": dims[2].value,
            "medium": dims[3].value,
            "campaign": dims[4].value if dims[4].value != "(not set)" else "",
            "count": count,
            "value": round(float(mets[1].value), 2),
        })

    return results


# ─── Merge & Dedup ───────────────────────────────────────────────────────────

def merge_landing_pages(existing: list, new: list) -> tuple:
    """Merge landing page data, dedup by date+page+source+medium+campaign."""
    existing_keys = {
        (r["date"], r["landing_page"], r["source"], r["medium"], r["campaign"])
        for r in existing
    }
    added = 0
    merged = list(existing)
    for item in new:
        key = (item["date"], item["landing_page"], item["source"], item["medium"], item["campaign"])
        if key not in existing_keys:
            merged.append(item)
            existing_keys.add(key)
            added += 1
        else:
            # Update existing with fresh data
            for idx, e in enumerate(merged):
                if (e["date"], e["landing_page"], e["source"], e["medium"], e["campaign"]) == key:
                    merged[idx] = item
                    break
    return merged, added


def merge_conversions(existing: list, new: list) -> tuple:
    """Merge conversion data, dedup by date+event+source+medium+campaign."""
    existing_keys = {
        (r["date"], r["event_name"], r["source"], r["medium"], r["campaign"])
        for r in existing
    }
    added = 0
    merged = list(existing)
    for item in new:
        key = (item["date"], item["event_name"], item["source"], item["medium"], item["campaign"])
        if key not in existing_keys:
            merged.append(item)
            existing_keys.add(key)
            added += 1
        else:
            for idx, e in enumerate(merged):
                if (e["date"], e["event_name"], e["source"], e["medium"], e["campaign"]) == key:
                    merged[idx] = item
                    break
    return merged, added


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch GA4 analytics data (read-only).")
    parser.add_argument("--from-date", type=str, default=None,
                        help="Start date (YYYY-MM-DD). Default: 30 days ago.")
    parser.add_argument("--to-date", type=str, default=None,
                        help="End date (YYYY-MM-DD). Default: yesterday.")
    parser.add_argument("--property", type=str, default=None,
                        choices=["landing", "home", "all"],
                        help="Which GA4 property: 'landing' ({YOUR_LANDING_DOMAIN}), "
                             "'home' ({YOUR_DOMAIN}), or 'all' (both). Default: landing.")
    parser.add_argument("--skip-landing-pages", action="store_true",
                        help="Skip landing page report")
    parser.add_argument("--skip-conversions", action="store_true",
                        help="Skip conversion report")
    args = parser.parse_args()

    # Defaults — GA4 data has ~24-48h latency, so default end is yesterday
    today = datetime.now(timezone.utc)
    yesterday = today - timedelta(days=1)
    from_date = args.from_date or (today - timedelta(days=30)).strftime("%Y-%m-%d")
    to_date = args.to_date or yesterday.strftime("%Y-%m-%d")

    # Determine properties to fetch
    prop_arg = args.property or "landing"
    if prop_arg == "all":
        properties_to_fetch = ["landing", "home"]
    else:
        properties_to_fetch = [prop_arg]

    # Load env for first property (also sets up credentials)
    property_id = load_env(properties_to_fetch[0])

    property_names = {"landing": "{YOUR_LANDING_DOMAIN}", "home": "{YOUR_DOMAIN}"}

    print(f"Date range: {from_date} → {to_date}")
    print(f"Properties: {', '.join(f'{p} ({property_names.get(p, p)})' for p in properties_to_fetch)}")

    # Create client
    print("Authenticating with Google Analytics...")
    try:
        client = BetaAnalyticsDataClient()
    except Exception as e:
        print(f"Error: Failed to authenticate — {e}", file=sys.stderr)
        print("  Check that GOOGLE_APPLICATION_CREDENTIALS points to a valid service account JSON.", file=sys.stderr)
        sys.exit(1)
    print("Authenticated.\n")

    # Load existing data
    marketing_data = load_existing_data()
    if marketing_data.get("ga4") is None:
        marketing_data["ga4"] = create_ga4_scaffold()

    new_pages = 0
    new_conversions = 0

    for prop_alias in properties_to_fetch:
        pid = load_env(prop_alias)
        site_name = property_names.get(prop_alias, prop_alias)
        print(f"── {site_name} (property {pid}) ──")
        marketing_data["ga4"]["property_id"] = pid

        # ── 1. Landing page report ──
        if not args.skip_landing_pages:
            print("  Fetching landing page report...")
            try:
                pages = fetch_landing_page_report(client, pid, from_date, to_date)
                # Tag each row with the property for multi-property tracking
                for p in pages:
                    p["property_id"] = pid
                    p["site"] = site_name
                marketing_data["ga4"]["landing_pages"], added = merge_landing_pages(
                    marketing_data["ga4"].get("landing_pages", []), pages
                )
                new_pages += added
                print(f"    {len(pages)} rows fetched ({added} new)")
            except Exception as e:
                print(f"    Error fetching landing pages: {e}", file=sys.stderr)
                marketing_data["sync_status"] = "partial"

        # ── 2. Conversion report ──
        if not args.skip_conversions:
            print("  Fetching conversion report...")
            try:
                conversions = fetch_conversion_report(client, pid, from_date, to_date)
                for c in conversions:
                    c["property_id"] = pid
                    c["site"] = site_name
                marketing_data["ga4"]["conversions"], added = merge_conversions(
                    marketing_data["ga4"].get("conversions", []), conversions
                )
                new_conversions += added
                print(f"    {len(conversions)} rows fetched ({added} new)")
            except Exception as e:
                print(f"    Error fetching conversions: {e}", file=sys.stderr)
                marketing_data["sync_status"] = "partial"

        print()

    # Sort by date (newest first)
    marketing_data["ga4"]["landing_pages"].sort(key=lambda r: r.get("date", ""), reverse=True)
    marketing_data["ga4"]["conversions"].sort(key=lambda r: r.get("date", ""), reverse=True)

    # Update sync metadata
    marketing_data["last_sync"] = today.isoformat()
    marketing_data["ga4"]["last_sync"] = today.isoformat()
    if marketing_data["sync_status"] != "partial":
        marketing_data["sync_status"] = "synced"

    # Save
    MARKETING_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MARKETING_DATA_PATH, "w") as f:
        json.dump(marketing_data, f, indent=2)

    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Landing pages: {len(marketing_data['ga4']['landing_pages'])} rows ({new_pages} new)")
    print(f"  Conversions:   {len(marketing_data['ga4']['conversions'])} rows ({new_conversions} new)")
    print(f"  Saved to:      {MARKETING_DATA_PATH}")

    # Summary
    if marketing_data["ga4"]["landing_pages"]:
        total_sessions = sum(
            r["sessions"] for r in marketing_data["ga4"]["landing_pages"]
            if r.get("date", "") >= from_date
        )
        total_users = sum(
            r["total_users"] for r in marketing_data["ga4"]["landing_pages"]
            if r.get("date", "") >= from_date
        )

        # Top sources
        source_sessions = {}
        for r in marketing_data["ga4"]["landing_pages"]:
            if r.get("date", "") >= from_date:
                key = f"{r['source']} / {r['medium']}"
                source_sessions[key] = source_sessions.get(key, 0) + r["sessions"]

        print(f"\n  Totals ({from_date} → {to_date}): {total_sessions:,} sessions | {total_users:,} users")

        if source_sessions:
            print(f"\n  Top sources:")
            for source, sessions in sorted(source_sessions.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"    {source}: {sessions:,} sessions")

        # Top landing pages
        page_sessions = {}
        for r in marketing_data["ga4"]["landing_pages"]:
            if r.get("date", "") >= from_date:
                page_sessions[r["landing_page"]] = page_sessions.get(r["landing_page"], 0) + r["sessions"]

        if page_sessions:
            print(f"\n  Top landing pages:")
            for page, sessions in sorted(page_sessions.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"    {page}: {sessions:,} sessions")

    if marketing_data["ga4"]["conversions"]:
        # Top conversion events
        event_counts = {}
        for r in marketing_data["ga4"]["conversions"]:
            if r.get("date", "") >= from_date:
                event_counts[r["event_name"]] = event_counts.get(r["event_name"], 0) + r["count"]

        if event_counts:
            print(f"\n  Conversion events:")
            for event, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"    {event}: {count:,}")


if __name__ == "__main__":
    main()
