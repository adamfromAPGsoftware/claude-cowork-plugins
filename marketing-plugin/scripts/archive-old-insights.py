#!/usr/bin/env python3
"""
archive-old-insights.py — Archive old insight data from marketing-data.json.

Separates insights into "hot" (recent) and "cold" (older than retention period),
aggregates cold insights from daily to weekly summaries, and writes them to
yearly archive files. Keeps marketing-data.json small and fast.

Usage:
  python3 marketing-plugin/scripts/archive-old-insights.py
  python3 marketing-plugin/scripts/archive-old-insights.py --retention-days 60
  python3 marketing-plugin/scripts/archive-old-insights.py --dry-run
  python3 marketing-plugin/scripts/archive-old-insights.py --dry-run --retention-days 30
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/
MARKETING_DATA_PATH = PLUGIN_ROOT / "data" / "marketing-data.json"
ARCHIVE_DIR = PLUGIN_ROOT / "data" / "archive"

DEFAULT_RETENTION_DAYS = 90


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_marketing_data() -> dict:
    """Load existing marketing-data.json or exit if missing."""
    if not MARKETING_DATA_PATH.exists():
        print(f"Error: {MARKETING_DATA_PATH} not found.", file=sys.stderr)
        print("  Run fetch-meta-campaigns.py first to populate marketing data.", file=sys.stderr)
        sys.exit(1)

    with open(MARKETING_DATA_PATH) as f:
        return json.load(f)


def save_marketing_data(data: dict):
    """Save marketing-data.json."""
    MARKETING_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MARKETING_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_archive(year: str) -> list:
    """Load existing archive file for a year, or return empty list."""
    path = ARCHIVE_DIR / f"marketing-insights-{year}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


def save_archive(year: str, data: list):
    """Save archive file for a year."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    path = ARCHIVE_DIR / f"marketing-insights-{year}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def iso_week_monday(date_str: str) -> str:
    """Return the Monday of the ISO week for a given date string (YYYY-MM-DD)."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    monday = dt - timedelta(days=dt.weekday())
    return monday.strftime("%Y-%m-%d")


def file_size_str(path: Path) -> str:
    """Return human-readable file size."""
    if not path.exists():
        return "0 B"
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.1f} MB"


# ─── Aggregation ─────────────────────────────────────────────────────────────

def aggregate_weekly(insights: list) -> list:
    """
    Aggregate daily insights into weekly summaries.

    Groups by entity_type + entity_id + ISO week.
    Sums: spend, impressions, clicks, reach, conversions
    Averages: cpc, cpm, ctr, frequency
    Uses the Monday of the ISO week as the date field.
    """
    groups = defaultdict(list)

    for insight in insights:
        week_monday = iso_week_monday(insight["date"])
        key = (insight["entity_type"], insight["entity_id"], week_monday)
        groups[key].append(insight)

    aggregated = []
    for (entity_type, entity_id, week_monday), records in groups.items():
        count = len(records)

        # Sum fields
        total_spend = sum(r.get("spend", 0) for r in records)
        total_impressions = sum(r.get("impressions", 0) for r in records)
        total_clicks = sum(r.get("clicks", 0) for r in records)
        total_reach = sum(r.get("reach", 0) for r in records)
        total_conversions = sum(r.get("conversions", 0) for r in records)

        # Average fields
        avg_cpc = sum(r.get("cpc", 0) for r in records) / count if count else 0
        avg_cpm = sum(r.get("cpm", 0) for r in records) / count if count else 0
        avg_ctr = sum(r.get("ctr", 0) for r in records) / count if count else 0
        avg_frequency = sum(r.get("frequency", 0) for r in records) / count if count else 0

        # Cost per conversion: recalculate from totals
        cost_per_conversion = total_spend / total_conversions if total_conversions else 0.0

        aggregated.append({
            "entity_type": entity_type,
            "entity_id": entity_id,
            "date": week_monday,
            "granularity": "weekly",
            "days_in_period": count,
            "impressions": total_impressions,
            "clicks": total_clicks,
            "spend": round(total_spend, 2),
            "currency": records[0].get("currency", "AUD"),
            "cpc": round(avg_cpc, 4),
            "cpm": round(avg_cpm, 4),
            "ctr": round(avg_ctr, 4),
            "reach": total_reach,
            "frequency": round(avg_frequency, 4),
            "conversions": total_conversions,
            "cost_per_conversion": round(cost_per_conversion, 2),
            "roas": 0.0,
        })

    return aggregated


def merge_archive(existing: list, new: list) -> list:
    """Merge new weekly insights into existing archive, deduping by entity_type + entity_id + date."""
    existing_keys = {}
    for idx, item in enumerate(existing):
        key = (item["entity_type"], item["entity_id"], item["date"])
        existing_keys[key] = idx

    merged = list(existing)
    for item in new:
        key = (item["entity_type"], item["entity_id"], item["date"])
        if key in existing_keys:
            # Replace existing with updated aggregation
            merged[existing_keys[key]] = item
        else:
            existing_keys[key] = len(merged)
            merged.append(item)

    return merged


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Archive old insights from marketing-data.json.")
    parser.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS,
                        help=f"Keep insights newer than this many days (default: {DEFAULT_RETENTION_DAYS}).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be archived without writing any files.")
    args = parser.parse_args()

    # Load data
    marketing_data = load_marketing_data()
    insights = marketing_data.get("meta", {}).get("insights", [])

    if not insights:
        print("No insights found in marketing-data.json. Nothing to archive.")
        return

    # Calculate cutoff date
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=args.retention_days)).strftime("%Y-%m-%d")

    print(f"Retention: {args.retention_days} days (cutoff: {cutoff})")
    print(f"Total insights: {len(insights)}")

    # ── 1. Separate hot and cold ──
    hot = []
    cold = []
    for insight in insights:
        date = insight.get("date", "")
        if date >= cutoff:
            hot.append(insight)
        else:
            cold.append(insight)

    print(f"  Hot (keeping):  {len(hot)} records")
    print(f"  Cold (archiving): {len(cold)} records")

    if not cold:
        print("\nNo insights older than the retention period. Nothing to archive.")
        return

    # ── 2. Aggregate cold insights to weekly ──
    print("\nAggregating cold insights to weekly summaries...")
    weekly = aggregate_weekly(cold)
    print(f"  {len(cold)} daily records → {len(weekly)} weekly summaries")

    # ── 3. Group by year for archive files ──
    by_year = defaultdict(list)
    for record in weekly:
        year = record["date"][:4]
        by_year[year].append(record)

    archived_years = sorted(by_year.keys())
    print(f"  Archive years: {', '.join(archived_years)}")

    if args.dry_run:
        print(f"\n{'─' * 50}")
        print("DRY RUN — no files written.")
        print(f"  Would archive {len(cold)} daily records as {len(weekly)} weekly summaries")
        print(f"  Would keep {len(hot)} records in marketing-data.json")
        for year, records in sorted(by_year.items()):
            archive_path = ARCHIVE_DIR / f"marketing-insights-{year}.json"
            existing = load_archive(year)
            merged = merge_archive(existing, records)
            print(f"  Archive {year}: {len(records)} new weekly records → {len(merged)} total")
        return

    # ── 4. Write archive files ──
    print("\nWriting archive files...")
    for year, records in sorted(by_year.items()):
        existing = load_archive(year)
        merged = merge_archive(existing, records)
        save_archive(year, merged)
        archive_path = ARCHIVE_DIR / f"marketing-insights-{year}.json"
        print(f"  {year}: {len(records)} new weekly records → {len(merged)} total ({file_size_str(archive_path)})")

    # ── 5. Update marketing-data.json ──
    print("\nUpdating marketing-data.json...")

    # Keep only hot insights
    marketing_data["meta"]["insights"] = hot

    # Sort hot insights by date (newest first)
    marketing_data["meta"]["insights"].sort(key=lambda i: i.get("date", ""), reverse=True)

    # Add _meta field
    hot_dates = [i["date"] for i in hot if i.get("date")]
    marketing_data["_meta"] = {
        "version": "1.0",
        "record_count": len(hot),
        "earliest_date": min(hot_dates) if hot_dates else None,
        "latest_date": max(hot_dates) if hot_dates else None,
        "last_archival": now.isoformat(),
        "archived_years": archived_years,
    }

    save_marketing_data(marketing_data)

    # ── 6. Print summary ──
    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Records archived:   {len(cold)} daily → {len(weekly)} weekly")
    print(f"  Records remaining:  {len(hot)}")
    print(f"  marketing-data.json: {file_size_str(MARKETING_DATA_PATH)}")
    for year in archived_years:
        archive_path = ARCHIVE_DIR / f"marketing-insights-{year}.json"
        print(f"  marketing-insights-{year}.json: {file_size_str(archive_path)}")


if __name__ == "__main__":
    main()
