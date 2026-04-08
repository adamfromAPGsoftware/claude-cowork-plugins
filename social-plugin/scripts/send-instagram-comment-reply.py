#!/usr/bin/env python3
"""
send-instagram-comment-reply.py — Reply to an Instagram comment.

Posts a reply to a specific comment and updates social-data.json on success.

Usage:
  python3 social-plugin/scripts/send-instagram-comment-reply.py --account example-account --comment-id 12345 --message "Thanks!"

Requires:
  pip install requests python-dotenv

NOTE: This script POSTS replies. Called by Engagement Responder after
      generating a response.
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


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Reply to an Instagram comment.")
    parser.add_argument("--account", type=str, required=True,
                        help="Account key (matches accounts/{key}/).")
    parser.add_argument("--comment-id", type=str, required=True,
                        help="ID of the comment to reply to.")
    parser.add_argument("--message", type=str, required=True,
                        help="Reply text.")
    args = parser.parse_args()

    # Load env + credentials
    load_env()
    token, page_id, ig_user_id = get_account_credentials(args.account)

    # Load social data
    social_data = load_social_data(args.account)

    # Check if comment exists in our data
    comment = social_data.get("comments", {}).get(args.comment_id)
    if comment:
        username = comment.get("username", args.comment_id)
        print(f"  Replying to comment by {username}")
        if comment.get("reply"):
            print(f"  Warning: Comment already has a reply (sent_at: {comment['reply'].get('sent_at', '?')})")
    else:
        username = args.comment_id
        print(f"  Comment {args.comment_id} not found in social-data.json — posting reply anyway")

    # ── Post the reply ──

    print(f"  Posting reply to comment {args.comment_id} via @{args.account}...")

    body = {"message": args.message}
    result = api_post(token, f"/{args.comment_id}/replies", body)

    if not result:
        print("FAILED: Reply was not posted. social-data.json has NOT been updated.", file=sys.stderr)
        sys.exit(1)

    # ── Success: update social-data.json ──

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat().replace("+00:00", "Z")
    reply_id = result.get("id", f"reply-{now_iso}")

    if args.comment_id in social_data.get("comments", {}):
        social_data["comments"][args.comment_id]["reply"] = {
            "id": reply_id,
            "text": args.message,
            "sent_at": now_iso,
        }

    # Save
    saved_path = save_social_data(args.account, social_data)

    print(f"Sent reply to {username} via @{args.account}")
    print(f"  Reply ID: {reply_id}")
    print(f"  Saved to: {saved_path}")


if __name__ == "__main__":
    main()
