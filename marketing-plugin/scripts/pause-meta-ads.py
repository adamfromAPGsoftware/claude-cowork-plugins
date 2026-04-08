#!/usr/bin/env python3
"""
pause-meta-ads.py — Pause specific ads in Meta Ads Manager.

Takes a list of ad IDs and sets their status to PAUSED. Supports dry-run
(default) to preview which ads will be paused.

Usage:
    # Dry run (default)
    python3 marketing-plugin/scripts/pause-meta-ads.py \
        --ad-ids 120212345678903456,120212345678903457

    # Execute
    python3 marketing-plugin/scripts/pause-meta-ads.py \
        --ad-ids 120212345678903456,120212345678903457 --execute

Requires:
    pip install requests python-dotenv
"""

import argparse
import json
import os
import sys
import time
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

META_API_BASE = "https://graph.facebook.com/v22.0"
MAX_RETRIES = 3
INITIAL_BACKOFF = 2


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables and return Meta access token."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = REPO_ROOT / ".env"
    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    access_token = os.environ.get("META_ACCESS_TOKEN")
    if not access_token:
        print("Error: META_ACCESS_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    return access_token


def meta_api_call(method, endpoint, access_token, data=None):
    """Make a Meta API call with exponential backoff on rate limits."""
    url = f"{META_API_BASE}/{endpoint}"

    for attempt in range(MAX_RETRIES):
        try:
            if data:
                data["access_token"] = access_token
            else:
                data = {"access_token": access_token}

            resp = requests.post(url, data=data, timeout=30)

            if resp.status_code == 429:
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                print(f"  Rate limited. Waiting {backoff}s...", file=sys.stderr)
                time.sleep(backoff)
                continue

            resp_json = resp.json()
            if "error" in resp_json:
                error = resp_json["error"]
                code = error.get("code", "unknown")
                msg = error.get("message", "Unknown error")
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

    return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Pause specific ads in Meta")
    parser.add_argument("--ad-ids", required=True, help="Comma-separated list of Meta ad IDs to pause")
    parser.add_argument("--execute", action="store_true", help="Execute (default is dry-run)")
    args = parser.parse_args()

    ad_ids = [aid.strip() for aid in args.ad_ids.split(",") if aid.strip()]

    if not ad_ids:
        print("Error: No ad IDs provided.", file=sys.stderr)
        sys.exit(1)

    if not args.execute:
        # Dry run
        print(f"\n═══ Pause Ads Preview (DRY RUN) ═══\n")
        print(f"Ads to pause ({len(ad_ids)}):")
        for ad_id in ad_ids:
            print(f"  - {ad_id} -> would be set to PAUSED")
        print(f"\nRun with --execute to pause these ads.\n")
        return

    # Execute
    access_token = load_env()
    paused = 0
    failed = 0

    print(f"\n═══ Pausing {len(ad_ids)} Ads ═══\n")

    for ad_id in ad_ids:
        print(f"  Pausing ad {ad_id}...", end=" ")
        resp = meta_api_call("POST", ad_id, access_token, {"status": "PAUSED"})
        if resp and resp.get("success"):
            print("PAUSED")
            paused += 1
        else:
            print("FAILED")
            failed += 1

    print(f"\n═══ Results ═══")
    print(f"  Paused: {paused}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(ad_ids)}\n")


if __name__ == "__main__":
    main()
