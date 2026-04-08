#!/usr/bin/env python3
"""
fetch-instagram-comments.py — Poll Instagram for new comments on recent posts/Reels (READ-ONLY).

Fetches recent media and their comments from the Instagram Graph API, deduplicates
by comment ID, creates/updates contact entries, and maintains social-data.json.

Usage:
  python3 social-plugin/scripts/fetch-instagram-comments.py --account example-account
  python3 social-plugin/scripts/fetch-instagram-comments.py --account example-account --days 7
  python3 social-plugin/scripts/fetch-instagram-comments.py  # processes all accounts

Requires:
  pip install requests python-dotenv

SAFETY: This script ONLY uses GET endpoints. It NEVER posts replies.
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

# Default lookback for recent posts
DEFAULT_DAYS = 7


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


# ─── Comment Fetching ─────────────────────────────────────────────────────────

def fetch_recent_media(token: str, ig_user_id: str) -> list:
    """Fetch recent media posts from Instagram. GET only."""
    fields = "id,caption,media_type,timestamp,permalink"
    media = paginate_get(token, f"/{ig_user_id}/media", fields=fields)
    return media


def fetch_comments_for_media(token: str, media_id: str) -> list:
    """Fetch comments for a single media post. GET only."""
    fields = "id,text,username,timestamp,from"
    comments = paginate_get(token, f"/{media_id}/comments", fields=fields)
    return comments


def process_comments(media_list: list, social_data: dict, token: str, ig_user_id: str, cutoff_dt: datetime) -> tuple:
    """
    Fetch comments for recent media and merge into social_data.
    Returns (new_comments_count, posts_scanned).
    """
    new_comments = 0
    posts_scanned = 0
    existing_comment_ids = set(social_data.get("comments", {}).keys())

    for media in media_list:
        media_id = media.get("id", "")
        media_timestamp = media.get("timestamp", "")
        if not media_id:
            continue

        # Filter by cutoff date
        try:
            media_dt = datetime.fromisoformat(media_timestamp.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            media_dt = datetime.now(timezone.utc)

        if media_dt < cutoff_dt:
            continue

        posts_scanned += 1
        caption = media.get("caption", "")
        # Truncate caption for storage
        caption_short = caption[:100] + "..." if len(caption) > 100 else caption

        print(f"  Scanning: {media.get('media_type', 'POST')} — {caption_short[:60]}...")

        comments = fetch_comments_for_media(token, media_id)

        for comment in comments:
            comment_id = comment.get("id", "")
            if not comment_id or comment_id in existing_comment_ids:
                continue

            # Skip our own comments (replies we posted)
            commenter = comment.get("from", {})
            commenter_id = commenter.get("id", "")
            commenter_username = comment.get("username", commenter.get("username", ""))

            if commenter_id == ig_user_id:
                continue

            # Add comment
            social_data["comments"][comment_id] = {
                "contact_id": commenter_id,
                "post_id": media_id,
                "post_caption": caption_short,
                "text": comment.get("text", ""),
                "timestamp": comment.get("timestamp", ""),
                "reply": None,
            }
            existing_comment_ids.add(comment_id)
            new_comments += 1

            # Create/update contact
            comment_timestamp = comment.get("timestamp", "")
            if commenter_id and commenter_id not in social_data["contacts"]:
                social_data["contacts"][commenter_id] = {
                    "username": commenter_username,
                    "name": commenter.get("name", commenter_username),
                    "first_seen": comment_timestamp,
                    "last_interaction": comment_timestamp,
                    "interaction_count": 0,
                    "channels": [],
                    "qualification": {
                        "status": "unclassified",
                        "tier": None,
                        "signals": [],
                        "qualified_at": None,
                        "crm_lead_id": None,
                    },
                }

            if commenter_id:
                contact = social_data["contacts"][commenter_id]
                if comment_timestamp > contact.get("last_interaction", ""):
                    contact["last_interaction"] = comment_timestamp
                contact["interaction_count"] = contact.get("interaction_count", 0) + 1
                if "comment" not in contact.get("channels", []):
                    contact.setdefault("channels", []).append("comment")

        # Small delay between posts to respect rate limits
        if posts_scanned % 10 == 0:
            time.sleep(1)

    return new_comments, posts_scanned


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Instagram comments (read-only).")
    parser.add_argument("--account", type=str, default=None,
                        help="Account key to process (default: all accounts).")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS,
                        help=f"Scan posts from last N days (default: {DEFAULT_DAYS}).")
    args = parser.parse_args()

    # Load env
    load_env()

    # Calculate cutoff
    now = datetime.now(timezone.utc)
    cutoff_dt = now - timedelta(days=args.days)

    # Discover accounts
    accounts = discover_accounts(args.account)
    print(f"Processing {len(accounts)} account(s)...")
    print(f"Scanning posts from last {args.days} days (since {cutoff_dt.strftime('%Y-%m-%d')})")

    total_new_comments = 0
    total_posts_scanned = 0

    for config in accounts:
        account_key = config["account_key"]
        print(f"\n{'─' * 50}")
        print(f"Account: {config.get('display_name', account_key)} ({account_key})")

        # Get credentials
        token, page_id, ig_user_id = get_credentials(config)

        # Load existing data
        social_data = load_social_data(account_key)

        # Fetch recent media
        print("  Fetching recent media...")
        media_list = fetch_recent_media(token, ig_user_id)
        print(f"  {len(media_list)} total media posts found")

        # Process comments
        new_comments, posts_scanned = process_comments(
            media_list, social_data, token, ig_user_id, cutoff_dt
        )
        total_new_comments += new_comments
        total_posts_scanned += posts_scanned

        # Update poll timestamp
        social_data["meta"]["last_poll_comments"] = now.isoformat().replace("+00:00", "Z")

        # Save
        saved_path = save_social_data(account_key, social_data)
        print(f"  {posts_scanned} posts scanned, {new_comments} new comments")
        print(f"  Saved to: {saved_path}")

    # Summary
    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Accounts processed: {len(accounts)}")
    print(f"  Posts scanned:      {total_posts_scanned}")
    print(f"  New comments:       {total_new_comments}")
    print(f"  Total contacts:     (see per-account social-data.json)")


if __name__ == "__main__":
    main()
