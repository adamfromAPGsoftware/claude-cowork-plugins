#!/usr/bin/env python3
"""
send-instagram-dm.py — Send a DM reply via Instagram Messaging API.

Sends a message to a recipient, enforcing the 24-hour messaging window
and hourly rate limits. Updates social-data.json on success.

Usage:
  python3 social-plugin/scripts/send-instagram-dm.py --account example-account --recipient-id 12345 --message "Hey!"
  python3 social-plugin/scripts/send-instagram-dm.py --account example-account --conversation-id ig-conv-abc --message "Hey!"

Requires:
  pip install requests python-dotenv

NOTE: This script SENDS messages. It should be called by the Engagement
      Responder agent after generating a response.
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

PLUGIN_ROOT = Path(__file__).parent.parent  # social-plugin/
GRAPH_API_BASE = "https://graph.instagram.com/v21.0"

# Rate limit: back off and retry on 429
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 60

# Instagram hourly DM limit
HOURLY_DM_LIMIT = 200


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env (plugin dir first, then repo root)."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)


def get_account_credentials(account_key: str) -> tuple:
    """Load config.json and resolve credentials from env vars.
    page_id is optional (only needed for future webhook subscriptions)."""
    config_path = PLUGIN_ROOT / "accounts" / account_key / "config.json"
    if not config_path.exists():
        print(f"Error: Account '{account_key}' not found at {config_path}", file=sys.stderr)
        available = [p.parent.name for p in (PLUGIN_ROOT / "accounts").glob("*/config.json")]
        print(f"  Available accounts: {', '.join(available)}", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    token = os.environ.get(config["env_token_key"])
    page_id = os.environ.get(config.get("env_page_id_key", ""))  # Optional — not used in API calls
    ig_user_id = os.environ.get(config["env_ig_user_id_key"])

    if not all([token, ig_user_id]):
        missing = []
        if not token:
            missing.append(config["env_token_key"])
        if not ig_user_id:
            missing.append(config["env_ig_user_id_key"])
        print(f"Error: Missing credentials for account '{account_key}': {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return token, page_id, ig_user_id


def api_post(token: str, path: str, body: dict):
    """Make a POST request to Instagram Graph API with retry on rate limit."""
    url = f"{GRAPH_API_BASE}{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for attempt in range(MAX_RETRIES):
        resp = requests.post(url, json=body, headers=headers, timeout=30)

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code == 429:
            if attempt < MAX_RETRIES - 1:
                print(f"  Rate limited. Waiting {RETRY_DELAY_SECONDS}s...", file=sys.stderr)
                time.sleep(RETRY_DELAY_SECONDS)
                continue

        error = resp.json().get("error", {})
        print(f"Error: {resp.status_code} — {error.get('message', resp.text)}", file=sys.stderr)
        return None

    return None


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


def save_social_data(account_key: str, data: dict) -> Path:
    """Save social-data.json, creating directories as needed."""
    data_path = PLUGIN_ROOT / "data" / account_key / "social-data.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)
    return data_path


# ─── Rate Limit Tracking ─────────────────────────────────────────────────────

def load_rate_limit(account_key: str) -> dict:
    """Load rate-limit.json or return fresh counter."""
    rate_path = PLUGIN_ROOT / "data" / account_key / "rate-limit.json"
    if rate_path.exists():
        with open(rate_path) as f:
            return json.load(f)
    return {"hour": None, "count": 0}


def save_rate_limit(account_key: str, data: dict):
    """Save rate-limit.json."""
    rate_path = PLUGIN_ROOT / "data" / account_key / "rate-limit.json"
    rate_path.parent.mkdir(parents=True, exist_ok=True)
    with open(rate_path, "w") as f:
        json.dump(data, f, indent=2)


def check_rate_limit(account_key: str) -> bool:
    """Check if we're under the hourly DM limit. Returns True if OK to send."""
    now = datetime.now(timezone.utc)
    current_hour = now.strftime("%Y-%m-%dT%H")

    rate_data = load_rate_limit(account_key)

    # Reset counter if we're in a new hour
    if rate_data.get("hour") != current_hour:
        return True

    if rate_data.get("count", 0) >= HOURLY_DM_LIMIT:
        return False

    return True


def increment_rate_limit(account_key: str):
    """Increment the hourly rate limit counter."""
    now = datetime.now(timezone.utc)
    current_hour = now.strftime("%Y-%m-%dT%H")

    rate_data = load_rate_limit(account_key)

    if rate_data.get("hour") != current_hour:
        rate_data = {"hour": current_hour, "count": 1}
    else:
        rate_data["count"] = rate_data.get("count", 0) + 1

    save_rate_limit(account_key, rate_data)


# ─── Safety Checks ───────────────────────────────────────────────────────────

def check_24h_window(social_data: dict, conversation_id: str) -> tuple:
    """
    Check if the 24-hour messaging window is still open for a conversation.
    Returns (is_open, reason_string).
    """
    conv = social_data.get("conversations", {}).get(conversation_id)
    if not conv:
        return False, f"Conversation '{conversation_id}' not found in social-data.json"

    window_expires = conv.get("window_expires")
    if not window_expires:
        return False, f"No window_expires set for conversation '{conversation_id}' — no inbound message recorded"

    try:
        expires_dt = datetime.fromisoformat(window_expires.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return False, f"Invalid window_expires value: {window_expires}"

    now = datetime.now(timezone.utc)
    if expires_dt <= now:
        return False, f"24-hour window expired at {window_expires}"

    return True, f"Window open until {window_expires}"


def resolve_recipient_from_conversation(social_data: dict, conversation_id: str):
    """Look up the contact_id (recipient) from a conversation in social-data.json."""
    conv = social_data.get("conversations", {}).get(conversation_id)
    if not conv:
        return None
    return conv.get("contact_id")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Send an Instagram DM.")
    parser.add_argument("--account", type=str, required=True,
                        help="Account key (matches accounts/{key}/).")
    parser.add_argument("--recipient-id", type=str, default=None,
                        help="Instagram user ID of the recipient.")
    parser.add_argument("--conversation-id", type=str, default=None,
                        help="Conversation ID — will look up recipient from social-data.json.")
    parser.add_argument("--message", type=str, required=True,
                        help="Message text to send.")
    args = parser.parse_args()

    # Validate: need either --recipient-id or --conversation-id
    if not args.recipient_id and not args.conversation_id:
        print("Error: Provide either --recipient-id or --conversation-id.", file=sys.stderr)
        sys.exit(1)

    # Load env + credentials
    load_env()
    token, page_id, ig_user_id = get_account_credentials(args.account)

    # Load social data
    social_data = load_social_data(args.account)

    # ── Resolve recipient ──

    recipient_id = args.recipient_id
    conversation_id = args.conversation_id

    if conversation_id and not recipient_id:
        recipient_id = resolve_recipient_from_conversation(social_data, conversation_id)
        if not recipient_id:
            print(f"Error: Could not resolve recipient from conversation '{conversation_id}'.", file=sys.stderr)
            print("  The conversation may not exist or has no contact_id set.", file=sys.stderr)
            sys.exit(1)
        print(f"  Resolved recipient {recipient_id} from conversation {conversation_id}")

    # If we have a recipient but no conversation_id, find the matching conversation
    if recipient_id and not conversation_id:
        for conv_id, conv in social_data.get("conversations", {}).items():
            if conv.get("contact_id") == recipient_id:
                conversation_id = conv_id
                break

    # ── Safety check 1: 24-hour window ──

    if conversation_id:
        window_ok, window_reason = check_24h_window(social_data, conversation_id)
        if not window_ok:
            print(f"REFUSED: {window_reason}", file=sys.stderr)
            print("  Cannot send DM outside the 24-hour messaging window.", file=sys.stderr)
            print("  The recipient must send a message first to re-open the window.", file=sys.stderr)
            sys.exit(1)
        print(f"  Window check: {window_reason}")
    else:
        print("  Warning: No conversation found — cannot verify 24-hour window.", file=sys.stderr)
        print("  Proceeding with send (API will enforce window server-side).", file=sys.stderr)

    # ── Safety check 2: Rate limit ──

    if not check_rate_limit(args.account):
        rate_data = load_rate_limit(args.account)
        print(f"REFUSED: Hourly rate limit reached ({rate_data.get('count', 0)}/{HOURLY_DM_LIMIT} DMs this hour).", file=sys.stderr)
        print("  Wait until the next hour before sending more DMs.", file=sys.stderr)
        sys.exit(1)

    # ── Send the DM ──

    print(f"  Sending DM to {recipient_id} via @{args.account}...")

    body = {
        "recipient": {"id": recipient_id},
        "message": {"text": args.message},
    }
    result = api_post(token, f"/{ig_user_id}/messages", body)

    if not result:
        print("FAILED: DM was not sent. social-data.json has NOT been updated.", file=sys.stderr)
        sys.exit(1)

    # ── Success: update social-data.json ──

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat().replace("+00:00", "Z")
    message_id = result.get("message_id", f"sent-{now_iso}")

    # Ensure conversation exists
    if conversation_id and conversation_id in social_data["conversations"]:
        social_data["conversations"][conversation_id]["messages"].append({
            "id": message_id,
            "direction": "outbound",
            "text": args.message,
            "timestamp": now_iso,
        })
    elif conversation_id:
        # Conversation ID was provided but didn't exist yet
        social_data["conversations"][conversation_id] = {
            "contact_id": recipient_id,
            "window_expires": None,
            "messages": [{
                "id": message_id,
                "direction": "outbound",
                "text": args.message,
                "timestamp": now_iso,
            }],
        }

    # Increment rate limit
    increment_rate_limit(args.account)

    # Save
    saved_path = save_social_data(args.account, social_data)

    # Resolve username for display
    contact = social_data.get("contacts", {}).get(recipient_id, {})
    username = contact.get("username", recipient_id)

    print(f"Sent DM to {username} via @{args.account}")
    print(f"  Message ID: {message_id}")
    print(f"  Saved to: {saved_path}")


if __name__ == "__main__":
    main()
