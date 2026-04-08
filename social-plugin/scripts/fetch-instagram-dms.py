#!/usr/bin/env python3
"""
fetch-instagram-dms.py — Poll Instagram Messaging API for new DMs (READ-ONLY).

Fetches conversations and messages from the Instagram Graph API, deduplicates
by message ID, tracks 24-hour response windows, and maintains social-data.json.

Usage:
  python3 social-plugin/scripts/fetch-instagram-dms.py --account example-account
  python3 social-plugin/scripts/fetch-instagram-dms.py --account example-account --since 2026-04-01
  python3 social-plugin/scripts/fetch-instagram-dms.py  # processes all accounts

Requires:
  pip install requests python-dotenv

SAFETY: This script ONLY uses GET endpoints. It NEVER sends messages.
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

PLUGIN_ROOT = Path(__file__).parent.parent  # social-plugin/
GRAPH_API_BASE = "https://graph.instagram.com/v21.0"

# Meta API page size
PAGE_SIZE = 200

# Rate limit: back off and retry on 429
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 60

# 24-hour messaging window
DM_WINDOW_HOURS = 24


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env (plugin dir first, then repo root)."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)


def api_get(token: str, path: str, params: dict = None) -> dict:
    """Make a GET request to Instagram Graph API. GET only — no writes."""
    url = f"{GRAPH_API_BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    all_params = {}
    if params:
        all_params.update(params)

    for attempt in range(MAX_RETRIES):
        resp = requests.get(url, params=all_params, headers=headers, timeout=30)

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 401:
            error_data = resp.json().get("error", {})
            print(f"Error: Authentication failed — {error_data.get('message', 'Invalid token')}", file=sys.stderr)
            print("  Your token may have expired. Get a new one from:", file=sys.stderr)
            print("  https://developers.facebook.com/tools/explorer/", file=sys.stderr)
            print("  Then update the relevant token in your .env file.", file=sys.stderr)
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
            data = api_get(token, path, request_params)
        else:
            headers = {"Authorization": f"Bearer {token}"}
            for attempt in range(MAX_RETRIES):
                resp = requests.get(next_url, headers=headers, timeout=30)
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


# ─── Account Discovery ────────────────────────────────────────────────────────

def discover_accounts(filter_account: str = None) -> list:
    """Scan accounts/ directory for config.json files. Optionally filter by account key."""
    accounts_dir = PLUGIN_ROOT / "accounts"
    if not accounts_dir.exists():
        print("Error: accounts/ directory not found.", file=sys.stderr)
        sys.exit(1)

    configs = []
    for config_path in sorted(accounts_dir.glob("*/config.json")):
        with open(config_path) as f:
            config = json.load(f)
        account_key = config.get("account_key", config_path.parent.name)
        if filter_account and account_key != filter_account:
            continue
        configs.append(config)

    if filter_account and not configs:
        print(f"Error: Account '{filter_account}' not found in accounts/.", file=sys.stderr)
        available = [p.parent.name for p in accounts_dir.glob("*/config.json")]
        print(f"  Available accounts: {', '.join(available)}", file=sys.stderr)
        sys.exit(1)

    return configs


def get_credentials(config: dict) -> tuple:
    """Read token and IG user ID from env vars using config key names.
    page_id is optional (only needed for future webhook subscriptions)."""
    token_key = config.get("env_token_key", "")
    page_id_key = config.get("env_page_id_key", "")
    ig_user_id_key = config.get("env_ig_user_id_key", "")

    token = os.environ.get(token_key)
    page_id = os.environ.get(page_id_key)  # Optional — not used in API calls
    ig_user_id = os.environ.get(ig_user_id_key)

    account_key = config.get("account_key", "unknown")

    if not token:
        print(f"Error: {token_key} not set for account '{account_key}'.", file=sys.stderr)
        sys.exit(1)
    if not ig_user_id:
        print(f"Error: {ig_user_id_key} not set for account '{account_key}'.", file=sys.stderr)
        sys.exit(1)

    return token, page_id, ig_user_id


# ─── Data Loading ─────────────────────────────────────────────────────────────

def load_social_data(account_key: str) -> dict:
    """Load existing social-data.json or return empty scaffold."""
    data_path = PLUGIN_ROOT / "data" / account_key / "social-data.json"
    if data_path.exists():
        with open(data_path) as f:
            return json.load(f)
    return {
        "meta": {
            "account_key": account_key,
            "platform": "instagram",
            "last_poll_dms": None,
            "last_poll_comments": None,
        },
        "contacts": {},
        "conversations": {},
        "comments": {},
    }


def save_social_data(account_key: str, data: dict):
    """Save social-data.json, creating directories as needed."""
    data_path = PLUGIN_ROOT / "data" / account_key / "social-data.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)
    return data_path


# ─── DM Fetching ──────────────────────────────────────────────────────────────

def fetch_conversations(token: str, ig_user_id: str) -> list:
    """Fetch conversations with messages from Instagram Messaging API. GET only."""
    fields = "participants,messages{id,message,from,to,created_time},updated_time"
    conversations = paginate_get(token, f"/{ig_user_id}/conversations", fields=fields)
    return conversations


def process_conversations(conversations: list, social_data: dict, ig_user_id: str, since_dt: datetime = None) -> tuple:
    """
    Process conversations and extract new messages.
    Returns (new_conversations_count, new_messages_count, window_warnings).
    """
    new_conversations = 0
    new_messages = 0
    window_warnings = []
    now = datetime.now(timezone.utc)

    for conv in conversations:
        conv_id = conv.get("id", "")
        if not conv_id:
            continue

        messages_data = conv.get("messages", {}).get("data", [])
        if not messages_data:
            continue

        # Check if this is a new conversation for us
        is_new_conv = conv_id not in social_data["conversations"]
        if is_new_conv:
            social_data["conversations"][conv_id] = {
                "contact_id": None,
                "window_expires": None,
                "messages": [],
            }
            new_conversations += 1

        existing_msg_ids = {
            m["id"] for m in social_data["conversations"][conv_id]["messages"]
        }

        for msg in messages_data:
            msg_id = msg.get("id", "")
            if not msg_id or msg_id in existing_msg_ids:
                continue

            # Parse timestamp
            created_time = msg.get("created_time", "")
            try:
                msg_dt = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                msg_dt = now

            # Apply --since filter
            if since_dt and msg_dt < since_dt:
                continue

            # Determine direction
            sender = msg.get("from", {})
            sender_id = sender.get("id", "")
            direction = "outbound" if sender_id == ig_user_id else "inbound"

            # Add message
            message_entry = {
                "id": msg_id,
                "direction": direction,
                "text": msg.get("message", ""),
                "timestamp": created_time,
            }
            social_data["conversations"][conv_id]["messages"].append(message_entry)
            new_messages += 1

            # For inbound messages: update contact, set window, check expiry
            if direction == "inbound":
                sender_name = sender.get("name", sender.get("username", ""))

                # Calculate 24h window
                window_expires = msg_dt + timedelta(hours=DM_WINDOW_HOURS)
                window_iso = window_expires.isoformat().replace("+00:00", "Z")

                # Update conversation window (latest inbound sets the window)
                current_window = social_data["conversations"][conv_id].get("window_expires")
                if not current_window or window_iso > current_window:
                    social_data["conversations"][conv_id]["window_expires"] = window_iso

                # Set contact ID on conversation
                social_data["conversations"][conv_id]["contact_id"] = sender_id

                # Create/update contact
                if sender_id not in social_data["contacts"]:
                    # Check follow relationship
                    follows_them = False
                    they_follow_us = False
                    try:
                        profile = api_get(token, f"/{sender_id}", {
                            "fields": "is_business_follow_user,is_user_follow_business"
                        })
                        follows_them = profile.get("is_business_follow_user", False)
                        they_follow_us = profile.get("is_user_follow_business", False)
                    except Exception:
                        pass  # Non-blocking — default to False

                    social_data["contacts"][sender_id] = {
                        "username": sender.get("username", sender_name),
                        "name": sender_name,
                        "first_seen": created_time,
                        "last_interaction": created_time,
                        "interaction_count": 0,
                        "channels": [],
                        "we_follow_them": follows_them,
                        "they_follow_us": they_follow_us,
                        "qualification": {
                            "status": "unclassified",
                            "tier": None,
                            "signals": [],
                            "qualified_at": None,
                            "crm_lead_id": None,
                        },
                    }

                contact = social_data["contacts"][sender_id]
                contact["last_interaction"] = max(contact["last_interaction"], created_time)
                contact["interaction_count"] = contact.get("interaction_count", 0) + 1
                if "dm" not in contact.get("channels", []):
                    contact.setdefault("channels", []).append("dm")

                # Window warning
                if window_expires < now:
                    window_warnings.append(
                        f"  ! Window EXPIRED for {sender_name or sender_id} "
                        f"(expired {window_iso})"
                    )
                elif window_expires < now + timedelta(hours=4):
                    remaining = window_expires - now
                    hours_left = remaining.total_seconds() / 3600
                    window_warnings.append(
                        f"  ! Window closing soon for {sender_name or sender_id} "
                        f"({hours_left:.1f}h remaining)"
                    )

        # Sort messages by timestamp
        social_data["conversations"][conv_id]["messages"].sort(
            key=lambda m: m.get("timestamp", "")
        )

    return new_conversations, new_messages, window_warnings


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Instagram DMs (read-only).")
    parser.add_argument("--account", type=str, default=None,
                        help="Account key to process (default: all accounts).")
    parser.add_argument("--since", type=str, default=None,
                        help="Only include messages after this date (YYYY-MM-DD).")
    args = parser.parse_args()

    # Parse --since
    since_dt = None
    if args.since:
        try:
            since_dt = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Error: Invalid date format '{args.since}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)

    # Load env
    load_env()

    # Discover accounts
    accounts = discover_accounts(args.account)
    print(f"Processing {len(accounts)} account(s)...")

    now = datetime.now(timezone.utc)
    total_new_convs = 0
    total_new_msgs = 0
    all_window_warnings = []

    for config in accounts:
        account_key = config["account_key"]
        print(f"\n{'─' * 50}")
        print(f"Account: {config.get('display_name', account_key)} ({account_key})")

        # Get credentials
        token, page_id, ig_user_id = get_credentials(config)

        # Load existing data
        social_data = load_social_data(account_key)

        # Fetch conversations
        print("  Fetching conversations...")
        conversations = fetch_conversations(token, ig_user_id)
        print(f"  {len(conversations)} conversations found")

        # Process and merge
        new_convs, new_msgs, warnings = process_conversations(
            conversations, social_data, ig_user_id, since_dt
        )
        total_new_convs += new_convs
        total_new_msgs += new_msgs
        all_window_warnings.extend(warnings)

        # Update poll timestamp
        social_data["meta"]["last_poll_dms"] = now.isoformat().replace("+00:00", "Z")

        # Save
        saved_path = save_social_data(account_key, social_data)
        print(f"  {new_convs} new conversations, {new_msgs} new messages")
        print(f"  Saved to: {saved_path}")

        # Print window warnings for this account
        for w in warnings:
            print(w)

    # Summary
    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Accounts processed: {len(accounts)}")
    print(f"  New conversations:  {total_new_convs}")
    print(f"  New messages:       {total_new_msgs}")
    if all_window_warnings:
        print(f"  Window warnings:    {len(all_window_warnings)}")
        for w in all_window_warnings:
            print(w)


if __name__ == "__main__":
    main()
