#!/usr/bin/env python3
"""
create-meta-campaign.py — Create a complete Meta campaign structure via the Marketing API.

Creates Campaign, Ad Set, and Ads — all in PAUSED state. Supports dry-run (default)
to preview what will be created before executing.

Also supports --activate to change an existing PAUSED campaign to ACTIVE.

Usage:
    # Dry run (default) — show what would be created
    python3 marketing-plugin/scripts/create-meta-campaign.py \
        --campaign-id camp-2026-04-07-001

    # Execute — actually create in Meta
    python3 marketing-plugin/scripts/create-meta-campaign.py \
        --campaign-id camp-2026-04-07-001 --execute

    # Activate — change PAUSED campaign to ACTIVE
    python3 marketing-plugin/scripts/create-meta-campaign.py \
        --campaign-id camp-2026-04-07-001 --activate

Requires:
    pip install requests python-dotenv
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
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

PLUGIN_ROOT = Path(__file__).parent.parent
REPO_ROOT = PLUGIN_ROOT.parent

CAMPAIGN_DATA_PATH = PLUGIN_ROOT / "data" / "campaign-data.json"
CREATIVE_DATA_PATH = PLUGIN_ROOT / "data" / "creative-data.json"

META_API_BASE = "https://graph.facebook.com/v22.0"
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # seconds


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables and return required Meta credentials."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = REPO_ROOT / ".env"
    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    access_token = os.environ.get("META_ACCESS_TOKEN")
    ad_account_id = os.environ.get("META_AD_ACCOUNT_ID")

    if not access_token:
        print("Error: META_ACCESS_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)
    if not ad_account_id:
        print("Error: META_AD_ACCOUNT_ID not set in .env", file=sys.stderr)
        sys.exit(1)

    # Ensure ad account ID has act_ prefix
    if not ad_account_id.startswith("act_"):
        ad_account_id = f"act_{ad_account_id}"

    return access_token, ad_account_id


def load_campaign_data():
    """Load campaign-data.json."""
    if not CAMPAIGN_DATA_PATH.exists():
        print(f"Error: Campaign data not found at {CAMPAIGN_DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CAMPAIGN_DATA_PATH, "r") as f:
        return json.load(f)


def save_campaign_data(data):
    """Write campaign-data.json."""
    with open(CAMPAIGN_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_creative_data():
    """Load creative-data.json."""
    if not CREATIVE_DATA_PATH.exists():
        return None
    with open(CREATIVE_DATA_PATH, "r") as f:
        return json.load(f)


def find_campaign(data, campaign_id):
    """Find campaign by ID."""
    for i, camp in enumerate(data.get("campaigns", [])):
        if camp.get("campaign_id") == campaign_id:
            return i, camp
    print(f"Error: Campaign '{campaign_id}' not found", file=sys.stderr)
    sys.exit(1)


def meta_api_call(method, endpoint, access_token, data=None, files=None):
    """Make a Meta API call with exponential backoff on rate limits."""
    url = f"{META_API_BASE}/{endpoint}"
    headers = {}

    for attempt in range(MAX_RETRIES):
        try:
            if method == "POST":
                if data:
                    data["access_token"] = access_token
                resp = requests.post(url, data=data, files=files, headers=headers, timeout=30)
            else:
                params = data or {}
                params["access_token"] = access_token
                resp = requests.get(url, params=params, headers=headers, timeout=30)

            if resp.status_code == 429:
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                print(f"  Rate limited. Waiting {backoff}s before retry...", file=sys.stderr)
                time.sleep(backoff)
                continue

            resp_json = resp.json()
            if "error" in resp_json:
                error = resp_json["error"]
                code = error.get("code", "unknown")
                msg = error.get("message", "Unknown error")

                # Transient errors — retry
                if code in (1, 2, 4, 17):
                    backoff = INITIAL_BACKOFF * (2 ** attempt)
                    print(f"  Transient error (code {code}). Waiting {backoff}s...", file=sys.stderr)
                    time.sleep(backoff)
                    continue

                print(f"  Meta API error (code {code}): {msg}", file=sys.stderr)
                return None

            return resp_json

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                print(f"  Request failed: {e}. Retrying in {backoff}s...", file=sys.stderr)
                time.sleep(backoff)
            else:
                print(f"  Request failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                return None

    print("  Max retries exceeded.", file=sys.stderr)
    return None


def dollars_to_cents(dollars):
    """Convert dollar amount to cents for Meta API."""
    return int(float(dollars) * 100)


# ─── Dry Run ──────────────────────────────────────────────────────────────────

def dry_run(campaign, creative_data):
    """Print what would be created without making API calls."""
    meta = campaign.get("meta_campaign", {})
    audience = campaign.get("audience", {})
    budget_dollars = campaign.get("daily_budget", 0)

    print("\n═══ Campaign Creation Preview (DRY RUN) ═══\n")

    print(f"Campaign:")
    print(f"  Name: {campaign.get('name', 'unnamed')}")
    print(f"  Objective: {meta.get('objective', 'OUTCOME_LEADS')}")
    print(f"  Special Ad Categories: []")
    print(f"  Status: PAUSED")

    print(f"\nAd Set:")
    print(f"  Name: {campaign.get('name', 'unnamed')} - Ad Set")
    print(f"  Targeting:")
    print(f"    Locations: {audience.get('locations', ['AU'])}")
    print(f"    Age: {audience.get('age_min', 25)}-{audience.get('age_max', 55)}")
    print(f"    Interests: {audience.get('interests', [])}")
    print(f"  Daily Budget: ${budget_dollars} ({dollars_to_cents(budget_dollars)} cents)")
    print(f"  Optimization Goal: {meta.get('optimization_goal', 'LEAD_GENERATION')}")
    print(f"  Billing Event: IMPRESSIONS")
    print(f"  Status: PAUSED")

    # Find creatives for this campaign
    ad_count = 0
    if creative_data:
        for batch in creative_data.get("batches", []):
            if batch.get("campaign_id") == campaign.get("campaign_id"):
                for angle in batch.get("angles", []):
                    for creative in angle.get("creatives", []):
                        if creative.get("meta_creative_id"):
                            ad_count += 1
                            print(f"\n  Ad: {creative.get('filename', 'unnamed')}")
                            print(f"    Creative ID: {creative['meta_creative_id']}")
                            print(f"    Status: PAUSED")

    if ad_count == 0:
        print(f"\n  Ads: No creatives with meta_creative_id found.")
        print(f"  Run [UC] to upload creatives first.")

    print(f"\n═══ Budget Breakdown ═══")
    print(f"  Daily:   ${budget_dollars}")
    print(f"  7-Day:   ${budget_dollars * 7}")
    print(f"  30-Day:  ${budget_dollars * 30}")
    print(f"\n  All entities created in PAUSED state — won't spend until [GO].\n")


# ─── Execute ──────────────────────────────────────────────────────────────────

def execute(campaign, creative_data, access_token, ad_account_id):
    """Create campaign structure in Meta."""
    meta_config = campaign.get("meta_campaign", {})
    audience = campaign.get("audience", {})
    budget_dollars = campaign.get("daily_budget", 0)
    campaign_name = campaign.get("name", "unnamed")

    created = {"campaign_id": None, "ad_set_ids": [], "ad_ids": []}

    # Step 1: Create Campaign
    print(f"\n1. Creating campaign: {campaign_name}")
    resp = meta_api_call("POST", f"{ad_account_id}/campaigns", access_token, {
        "name": campaign_name,
        "objective": meta_config.get("objective", "OUTCOME_LEADS"),
        "special_ad_categories": "[]",
        "status": "PAUSED",
    })
    if not resp or "id" not in resp:
        print(f"   FAILED to create campaign.", file=sys.stderr)
        print(f"   Already created: {json.dumps(created, indent=2)}")
        return None
    created["campaign_id"] = resp["id"]
    print(f"   Campaign ID: {resp['id']}")

    # Step 2: Create Ad Set
    print(f"\n2. Creating ad set...")
    targeting = build_targeting(audience)
    resp = meta_api_call("POST", f"{ad_account_id}/adsets", access_token, {
        "campaign_id": created["campaign_id"],
        "name": f"{campaign_name} - Ad Set",
        "targeting": json.dumps(targeting),
        "daily_budget": str(dollars_to_cents(budget_dollars)),
        "optimization_goal": meta_config.get("optimization_goal", "LEAD_GENERATION"),
        "billing_event": "IMPRESSIONS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "status": "PAUSED",
    })
    if not resp or "id" not in resp:
        print(f"   FAILED to create ad set.", file=sys.stderr)
        print(f"   Already created: {json.dumps(created, indent=2)}")
        return created
    created["ad_set_ids"].append(resp["id"])
    print(f"   Ad Set ID: {resp['id']}")

    # Step 3: Create Ads (one per creative with meta_creative_id)
    ad_num = 0
    if creative_data:
        for batch in creative_data.get("batches", []):
            if batch.get("campaign_id") == campaign.get("campaign_id"):
                for angle in batch.get("angles", []):
                    for creative in angle.get("creatives", []):
                        creative_id = creative.get("meta_creative_id")
                        if not creative_id:
                            continue
                        ad_num += 1
                        ad_name = f"{campaign_name} - {angle.get('name', 'angle')} - {creative.get('filename', f'ad-{ad_num}')}"
                        print(f"\n3.{ad_num}. Creating ad: {ad_name}")

                        ad_data = {
                            "adset_id": created["ad_set_ids"][0],
                            "name": ad_name,
                            "creative": json.dumps({"creative_id": creative_id}),
                            "status": "PAUSED",
                        }

                        # Add pixel tracking if configured
                        pixel_id = campaign.get("tracking", {}).get("meta_pixel_id")
                        if pixel_id:
                            ad_data["tracking_specs"] = json.dumps([{
                                "action.type": ["offsite_conversion"],
                                "fb_pixel": [pixel_id],
                            }])

                        resp = meta_api_call("POST", f"{ad_account_id}/ads", access_token, ad_data)
                        if not resp or "id" not in resp:
                            print(f"   FAILED to create ad.", file=sys.stderr)
                            continue
                        created["ad_ids"].append(resp["id"])
                        print(f"   Ad ID: {resp['id']}")

    if ad_num == 0:
        print(f"\n   No creatives with meta_creative_id found. No ads created.")
        print(f"   Run [UC] to upload creatives, then re-run [MC].")

    print(f"\n═══ Campaign Created (PAUSED) ═══")
    print(f"  Campaign ID: {created['campaign_id']}")
    print(f"  Ad Set IDs: {created['ad_set_ids']}")
    print(f"  Ad IDs: {created['ad_ids']}")
    print(f"  Status: PAUSED — run [GO] to activate.\n")

    return created


def activate(campaign, access_token):
    """Activate a PAUSED campaign (set campaign, ad sets, ads to ACTIVE)."""
    meta = campaign.get("meta_campaign", {})
    campaign_id = meta.get("campaign_id")
    ad_set_ids = meta.get("ad_set_ids", [])
    ad_ids = meta.get("ad_ids", [])

    if not campaign_id:
        print("Error: No Meta campaign ID found. Run [MC] first.", file=sys.stderr)
        sys.exit(1)

    print(f"\n═══ Activating Campaign ═══\n")

    # Activate campaign
    print(f"1. Activating campaign {campaign_id}...")
    resp = meta_api_call("POST", campaign_id, access_token, {"status": "ACTIVE"})
    if resp and resp.get("success"):
        print(f"   Campaign ACTIVE")
    else:
        print(f"   FAILED to activate campaign", file=sys.stderr)
        return False

    # Activate ad sets
    for i, adset_id in enumerate(ad_set_ids):
        print(f"2.{i+1}. Activating ad set {adset_id}...")
        resp = meta_api_call("POST", adset_id, access_token, {"status": "ACTIVE"})
        if resp and resp.get("success"):
            print(f"   Ad Set ACTIVE")
        else:
            print(f"   FAILED to activate ad set", file=sys.stderr)

    # Activate ads
    for i, ad_id in enumerate(ad_ids):
        print(f"3.{i+1}. Activating ad {ad_id}...")
        resp = meta_api_call("POST", ad_id, access_token, {"status": "ACTIVE"})
        if resp and resp.get("success"):
            print(f"   Ad ACTIVE")
        else:
            print(f"   FAILED to activate ad", file=sys.stderr)

    print(f"\n═══ Campaign LIVE ═══")
    print(f"  All entities activated. Budget is now spending.\n")
    return True


def build_targeting(audience):
    """Build Meta targeting spec from audience config."""
    targeting = {}

    # Geo locations
    locations = audience.get("locations", ["AU"])
    geo = {}
    if isinstance(locations, list) and all(isinstance(l, str) and len(l) == 2 for l in locations):
        geo["countries"] = locations
    elif isinstance(locations, dict):
        geo = locations
    else:
        geo["countries"] = ["AU"]
    targeting["geo_locations"] = geo

    # Age
    if "age_min" in audience:
        targeting["age_min"] = audience["age_min"]
    if "age_max" in audience:
        targeting["age_max"] = audience["age_max"]

    # Interests
    interests = audience.get("interests", [])
    if interests:
        if isinstance(interests[0], dict):
            targeting["flexible_spec"] = [{"interests": interests}]
        else:
            # Plain strings — pass as-is, Meta may need IDs in practice
            targeting["flexible_spec"] = [{"interests": [{"name": i} for i in interests]}]

    # Platforms
    targeting["publisher_platforms"] = audience.get("platforms", ["facebook", "instagram"])

    return targeting


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Create Meta campaign structure")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID from campaign-data.json")
    parser.add_argument("--execute", action="store_true", help="Execute (default is dry-run)")
    parser.add_argument("--activate", action="store_true", help="Activate a PAUSED campaign")
    args = parser.parse_args()

    data = load_campaign_data()
    idx, campaign = find_campaign(data, args.campaign_id)
    creative_data = load_creative_data()

    if args.activate:
        access_token, ad_account_id = load_env()
        success = activate(campaign, access_token)
        if success:
            campaign.setdefault("meta_campaign", {})["status"] = "active"
            campaign["meta_campaign"]["activated_at"] = datetime.now(timezone.utc).isoformat()
            campaign["status"] = "live"
            data["campaigns"][idx] = campaign
            save_campaign_data(data)
            print("campaign-data.json updated: status = live")
    elif args.execute:
        access_token, ad_account_id = load_env()
        created = execute(campaign, creative_data, access_token, ad_account_id)
        if created and created.get("campaign_id"):
            campaign.setdefault("meta_campaign", {}).update({
                "status": "created",
                "campaign_id": created["campaign_id"],
                "ad_set_ids": created["ad_set_ids"],
                "ad_ids": created["ad_ids"],
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            campaign.setdefault("approval_log", []).append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": "create_campaign",
                "meta_campaign_id": created["campaign_id"],
            })
            data["campaigns"][idx] = campaign
            save_campaign_data(data)
            print("campaign-data.json updated with Meta entity IDs.")
    else:
        dry_run(campaign, creative_data)


if __name__ == "__main__":
    main()
