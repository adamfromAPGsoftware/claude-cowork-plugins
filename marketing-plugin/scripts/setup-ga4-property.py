#!/usr/bin/env python3
"""
setup-ga4-property.py — Create/configure a GA4 property and web data stream.

Creates a GA4 property for the campaign's landing page URL, sets up a web data
stream, retrieves the measurement ID, and creates key events for conversion tracking.

Usage:
    # Dry run (default)
    python3 marketing-plugin/scripts/setup-ga4-property.py \
        --campaign-id ai-scoping-engine-for-agencies

    # Execute
    python3 marketing-plugin/scripts/setup-ga4-property.py \
        --campaign-id ai-scoping-engine-for-agencies --execute

    # Use existing property
    python3 marketing-plugin/scripts/setup-ga4-property.py \
        --campaign-id ai-scoping-engine-for-agencies --property-id 469971846 --execute

Requires:
    pip install google-analytics-admin python-dotenv
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent
REPO_ROOT = PLUGIN_ROOT.parent

CAMPAIGN_DATA_PATH = PLUGIN_ROOT / "data" / "campaign-data.json"

KEY_EVENTS = ["generate_lead", "form_submit", "page_view"]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = REPO_ROOT / ".env"
    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS not set in .env", file=sys.stderr)
        sys.exit(1)

    if not Path(creds).exists():
        print(f"Error: Service account file not found: {creds}", file=sys.stderr)
        sys.exit(1)

    return creds


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


def find_campaign(data, campaign_id):
    """Find campaign by ID."""
    for i, camp in enumerate(data.get("campaigns", [])):
        if camp.get("campaign_id") == campaign_id:
            return i, camp
    print(f"Error: Campaign '{campaign_id}' not found", file=sys.stderr)
    sys.exit(1)


# ─── Dry Run ──────────────────────────────────────────────────────────────────

def dry_run(campaign, property_id=None):
    """Show what would be created."""
    landing_url = campaign.get("landing_page_url", "")
    parsed = urlparse(landing_url)
    domain = parsed.netloc or parsed.path
    campaign_name = campaign.get("name", "unnamed")

    print(f"\n═══ GA4 Property Setup Preview (DRY RUN) ═══\n")

    if property_id:
        print(f"  Using existing property: {property_id}")
    else:
        print(f"  Property Name: {campaign_name} - GA4")
        print(f"  Time Zone: Australia/Brisbane")
        print(f"  Currency: AUD")

    print(f"\n  Data Stream:")
    print(f"    URL: {landing_url}")
    print(f"    Name: {domain} - Web Stream")
    print(f"    Measurement ID: (will be generated)")

    print(f"\n  Key Events to Create:")
    for event in KEY_EVENTS:
        print(f"    - {event}")

    print(f"\n  Run with --execute to create.\n")


# ─── Execute ──────────────────────────────────────────────────────────────────

def execute(campaign, property_id=None):
    """Create/configure GA4 property."""
    try:
        from google.analytics.admin import AnalyticsAdminServiceClient
        from google.analytics.admin_v1beta.types import (
            Property,
            DataStream,
            KeyEvent,
        )
        from google.api_core.exceptions import AlreadyExists, GoogleAPIError
    except ImportError:
        print("Error: google-analytics-admin not installed.", file=sys.stderr)
        print("Run: pip install google-analytics-admin", file=sys.stderr)
        sys.exit(1)

    landing_url = campaign.get("landing_page_url", "")
    parsed = urlparse(landing_url)
    domain = parsed.netloc or parsed.path
    campaign_name = campaign.get("name", "unnamed")

    client = AnalyticsAdminServiceClient()

    # Step 1: Create or use existing property
    if property_id:
        print(f"\n1. Using existing property: {property_id}")
        property_name = f"properties/{property_id}"
    else:
        print(f"\n1. Creating GA4 property: {campaign_name} - GA4")
        try:
            prop = client.create_property(
                property=Property(
                    display_name=f"{campaign_name} - GA4",
                    time_zone="Australia/Brisbane",
                    currency_code="AUD",
                )
            )
            property_name = prop.name
            property_id = prop.name.split("/")[-1]
            print(f"   Property ID: {property_id}")
        except GoogleAPIError as e:
            print(f"   Failed to create property: {e}", file=sys.stderr)
            return None, None

    # Step 2: Create web data stream
    print(f"\n2. Creating web data stream for {domain}...")
    try:
        stream = client.create_data_stream(
            parent=property_name,
            data_stream=DataStream(
                type_=DataStream.DataStreamType.WEB_DATA_STREAM,
                display_name=f"{domain} - Web Stream",
                web_stream_data=DataStream.WebStreamData(
                    default_uri=landing_url,
                ),
            ),
        )
        measurement_id = stream.web_stream_data.measurement_id
        print(f"   Measurement ID: {measurement_id}")
    except AlreadyExists:
        print(f"   Data stream already exists for this property.")
        # List existing streams to get measurement ID
        streams = client.list_data_streams(parent=property_name)
        measurement_id = None
        for s in streams:
            if s.web_stream_data:
                measurement_id = s.web_stream_data.measurement_id
                print(f"   Existing Measurement ID: {measurement_id}")
                break
        if not measurement_id:
            print(f"   Could not find measurement ID.", file=sys.stderr)
            return property_id, None
    except GoogleAPIError as e:
        print(f"   Failed to create data stream: {e}", file=sys.stderr)
        return property_id, None

    # Step 3: Create key events
    print(f"\n3. Creating key events...")
    for event_name in KEY_EVENTS:
        try:
            client.create_key_event(
                parent=property_name,
                key_event=KeyEvent(
                    event_name=event_name,
                    counting_method=KeyEvent.CountingMethod.ONCE_PER_EVENT,
                ),
            )
            print(f"   Created: {event_name}")
        except AlreadyExists:
            print(f"   Exists: {event_name}")
        except GoogleAPIError as e:
            print(f"   Failed: {event_name} — {e}", file=sys.stderr)

    print(f"\n═══ GA4 Setup Complete ═══")
    print(f"  Property ID: {property_id}")
    print(f"  Measurement ID: {measurement_id}")
    print(f"  Key Events: {', '.join(KEY_EVENTS)}\n")

    return property_id, measurement_id


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Create/configure GA4 property")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID from campaign-data.json")
    parser.add_argument("--property-id", help="Existing GA4 property ID (optional)")
    parser.add_argument("--execute", action="store_true", help="Execute (default is dry-run)")
    args = parser.parse_args()

    load_env()
    data = load_campaign_data()
    idx, campaign = find_campaign(data, args.campaign_id)

    if not args.execute:
        dry_run(campaign, args.property_id)
        return

    property_id, measurement_id = execute(campaign, args.property_id)

    if property_id or measurement_id:
        tracking = campaign.setdefault("tracking", {})
        if property_id:
            tracking["ga4_property_id"] = property_id
        if measurement_id:
            tracking["ga4_measurement_id"] = measurement_id
        data["campaigns"][idx] = campaign
        save_campaign_data(data)
        print("campaign-data.json updated with GA4 tracking config.")


if __name__ == "__main__":
    main()
