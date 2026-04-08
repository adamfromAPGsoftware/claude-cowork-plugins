#!/usr/bin/env python3
"""
Setup GA4 key events and custom dimensions via GA4 Admin API.

Creates the funnel event taxonomy for go-enhance:
  Key events: generate_lead, quiz_complete, quiz_open, booking_complete
  Custom dimensions: cta_location, quiz_step, qualified, saas_spend,
                     team_size, revenue_band

Idempotent — existing events/dimensions are skipped.

Requires:
  GOOGLE_APPLICATION_CREDENTIALS env var pointing to a service account
  JSON with Editor role on the GA4 property.

Usage:
  python3 setup-ga4-events.py --property-id 469971846 [--dry-run]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1beta.types import (
    CustomDimension,
    KeyEvent,
)
from google.api_core.exceptions import AlreadyExists, PermissionDenied, GoogleAPIError


# ---- Target configuration ----------------------------------------------------

KEY_EVENTS = [
    "generate_lead",    # fires when qualified lead qualifies (SaaS + revenue)
    "quiz_complete",    # fires when user finishes all 5 quiz questions
    "quiz_open",        # fires when quiz modal opens (top of funnel)
    "booking_complete", # fires on ThankYou page (?booked=true)
]

CUSTOM_DIMENSIONS = [
    # (param_name, display_name, description)
    ("cta_location",  "CTA Location",
     "Which CTA button was clicked (hero, header, mid_page, footer, nav)"),
    ("quiz_step",     "Quiz Step",
     "Step number of the quiz (1-5) where the event fired"),
    ("qualified",     "Qualified",
     "Whether the lead qualified (true/false)"),
    ("saas_spend",    "SaaS Spend Band",
     "Monthly SaaS spend reported in quiz"),
    ("team_size",     "Team Size Band",
     "Team size reported in quiz"),
    ("revenue_band",  "Revenue Band",
     "Annual revenue band reported in quiz"),
]


def ensure_key_events(client, property_path, dry_run=False):
    """Create missing key events. Returns (created, skipped)."""
    existing = {}
    try:
        for ke in client.list_key_events(parent=property_path):
            # resource name: properties/{id}/keyEvents/{id}
            existing[ke.event_name] = ke.name
    except PermissionDenied as e:
        raise SystemExit(f"  PermissionDenied listing key events: {e.message}")

    created, skipped = [], []
    for name in KEY_EVENTS:
        if name in existing:
            skipped.append(name)
            continue
        if dry_run:
            created.append(name + " (dry-run)")
            continue
        ke = KeyEvent(
            event_name=name,
            counting_method=KeyEvent.CountingMethod.ONCE_PER_SESSION,
        )
        try:
            result = client.create_key_event(parent=property_path, key_event=ke)
            created.append(name)
        except AlreadyExists:
            skipped.append(name)
        except GoogleAPIError as e:
            print(f"  ! failed {name}: {e}")
    return created, skipped


def ensure_custom_dimensions(client, property_path, dry_run=False):
    """Create missing event-scoped custom dimensions."""
    existing = {}
    try:
        for cd in client.list_custom_dimensions(parent=property_path):
            existing[cd.parameter_name] = cd.name
    except PermissionDenied as e:
        raise SystemExit(f"  PermissionDenied listing dimensions: {e.message}")

    created, skipped = [], []
    for param, display, desc in CUSTOM_DIMENSIONS:
        if param in existing:
            skipped.append(param)
            continue
        if dry_run:
            created.append(param + " (dry-run)")
            continue
        cd = CustomDimension(
            parameter_name=param,
            display_name=display,
            description=desc,
            scope=CustomDimension.DimensionScope.EVENT,
        )
        try:
            client.create_custom_dimension(parent=property_path, custom_dimension=cd)
            created.append(param)
        except AlreadyExists:
            skipped.append(param)
        except GoogleAPIError as e:
            print(f"  ! failed {param}: {e}")
    return created, skipped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--property-id", required=True,
                        help="GA4 property ID, e.g. 469971846")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would be created without writing")
    args = parser.parse_args()

    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds or not Path(creds).exists():
        print("  GOOGLE_APPLICATION_CREDENTIALS not set or file missing")
        sys.exit(1)

    property_path = f"properties/{args.property_id}"
    client = AnalyticsAdminServiceClient()

    print(f"GA4 property: {property_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'APPLY'}")
    print()

    print("Key events:")
    created, skipped = ensure_key_events(client, property_path, args.dry_run)
    for n in created: print(f"  + {n}")
    for n in skipped: print(f"  = {n} (exists)")
    print(f"  → {len(created)} created, {len(skipped)} existed")
    print()

    print("Custom dimensions:")
    created, skipped = ensure_custom_dimensions(client, property_path, args.dry_run)
    for n in created: print(f"  + {n}")
    for n in skipped: print(f"  = {n} (exists)")
    print(f"  → {len(created)} created, {len(skipped)} existed")
    print()

    print("Done. In GA4, new key events may take ~24h to appear in reports.")


if __name__ == "__main__":
    main()
