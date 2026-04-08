#!/usr/bin/env python3
"""
fetch-balances.py — Pull current account balances from Airwallex (READ-ONLY).

Reads AIRWALLEX_CLIENT_ID, AIRWALLEX_API_KEY, and AIRWALLEX_ENVIRONMENT from .env,
authenticates with Airwallex, fetches current balances, and saves to finance/balances.json.

Usage:
  python3 finance-plugin/scripts/fetch-balances.py

Requires:
  pip install requests python-dotenv

SAFETY: This script ONLY uses GET endpoints (plus one POST for auth token).
"""

import json
import os
import sys
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

BALANCES_PATH = Path("finance/balances.json")
FINANCE_DATA_PATH = Path("finance/finance-data.json")

API_BASES = {
    "demo": "https://api-demo.airwallex.com",
    "prod": "https://api.airwallex.com",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env at repo root."""
    repo_root = Path(__file__).parent.parent.parent
    load_dotenv(repo_root / ".env")

    client_id = os.environ.get("AIRWALLEX_CLIENT_ID")
    api_key = os.environ.get("AIRWALLEX_API_KEY")
    environment = os.environ.get("AIRWALLEX_ENVIRONMENT", "demo")

    if not client_id:
        print("Error: AIRWALLEX_CLIENT_ID not set. Add it to .env at the repo root.", file=sys.stderr)
        sys.exit(1)
    if not api_key:
        print("Error: AIRWALLEX_API_KEY not set. Add it to .env at the repo root.", file=sys.stderr)
        sys.exit(1)
    if environment not in API_BASES:
        print(f"Error: AIRWALLEX_ENVIRONMENT must be 'demo' or 'prod', got '{environment}'", file=sys.stderr)
        sys.exit(1)

    return client_id, api_key, environment


def authenticate(base_url: str, client_id: str, api_key: str) -> str:
    """Authenticate with Airwallex and return a Bearer token."""
    resp = requests.post(
        f"{base_url}/api/v1/authentication/login",
        headers={
            "x-client-id": client_id,
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    if resp.status_code == 401:
        print("Error: Invalid Airwallex credentials.", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    token = resp.json().get("token")
    if not token:
        print("Error: No token in authentication response.", file=sys.stderr)
        sys.exit(1)
    return token


def api_get(base_url: str, token: str, path: str, params: dict = None) -> dict:
    """GET request to Airwallex. Read-only."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    resp = requests.get(f"{base_url}{path}", headers=headers, params=params or {}, timeout=30)
    if resp.status_code == 401:
        print("Error: Token expired or invalid.", file=sys.stderr)
        sys.exit(1)
    if resp.status_code == 429:
        print("Error: Airwallex rate limit hit.", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    client_id, api_key, environment = load_env()
    base_url = API_BASES[environment]

    print(f"Environment: {environment}")
    print("Authenticating with Airwallex...")

    token = authenticate(base_url, client_id, api_key)
    print("Authenticated. Fetching balances...")

    # Fetch current balances
    data = api_get(base_url, token, "/api/v1/balances/current")
    # API returns a list directly, or a dict with items key
    items = data if isinstance(data, list) else data.get("items", [])

    now = datetime.now(timezone.utc).isoformat()

    # Build balances snapshot
    balances = {
        "snapshot_date": now,
        "accounts": [
            {
                "currency": item.get("currency", ""),
                "available_amount": item.get("available_amount", 0),
                "pending_amount": item.get("pending_amount", 0),
                "total_amount": item.get("total_amount", 0),
            }
            for item in items
        ],
    }

    # Save to balances.json
    BALANCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(BALANCES_PATH, "w") as f:
        json.dump(balances, f, indent=2)

    # Also update finance-data.json balances section if it exists
    if FINANCE_DATA_PATH.exists():
        with open(FINANCE_DATA_PATH) as f:
            finance_data = json.load(f)
        finance_data["balances"] = balances
        with open(FINANCE_DATA_PATH, "w") as f:
            json.dump(finance_data, f, indent=2)
        print("Updated finance-data.json balances section.")

    # Report
    print(f"\nBalances as of {now}:")
    for account in balances["accounts"]:
        currency = account["currency"]
        available = account["available_amount"]
        pending = account["pending_amount"]
        total = account["total_amount"]
        print(f"  {currency}: ${available:,.2f} available | ${pending:,.2f} pending | ${total:,.2f} total")

    print(f"\nSaved to: {BALANCES_PATH}")


if __name__ == "__main__":
    main()
