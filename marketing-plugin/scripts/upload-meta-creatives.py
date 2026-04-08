#!/usr/bin/env python3
"""
upload-meta-creatives.py — Upload creative assets to Meta Ads Manager.

Reads creative-data.json for batches linked to a campaign, uploads images and
videos to Meta, creates Ad Creatives, and stores the returned creative IDs back
in creative-data.json.

Usage:
    # Upload all batches for a campaign
    python3 marketing-plugin/scripts/upload-meta-creatives.py \
        --campaign-id camp-2026-04-07-001

    # Upload a specific batch
    python3 marketing-plugin/scripts/upload-meta-creatives.py \
        --campaign-id camp-2026-04-07-001 --batch-id batch-2026-04-07-001

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

CAMPAIGN_DATA_PATH = PLUGIN_ROOT / "data" / "campaign-data.json"
CREATIVE_DATA_PATH = PLUGIN_ROOT / "data" / "creative-data.json"
CREATIVES_DIR = PLUGIN_ROOT / "data" / "creatives"

META_API_BASE = "https://graph.facebook.com/v22.0"
MAX_RETRIES = 3
INITIAL_BACKOFF = 2
VIDEO_POLL_INTERVAL = 5  # seconds
VIDEO_POLL_MAX = 60  # max polls (5 minutes)


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
    page_id = os.environ.get("META_PAGE_ID", "")

    if not access_token:
        print("Error: META_ACCESS_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)
    if not ad_account_id:
        print("Error: META_AD_ACCOUNT_ID not set in .env", file=sys.stderr)
        sys.exit(1)

    if not ad_account_id.startswith("act_"):
        ad_account_id = f"act_{ad_account_id}"

    return access_token, ad_account_id, page_id


def load_creative_data():
    """Load creative-data.json."""
    if not CREATIVE_DATA_PATH.exists():
        print(f"Error: Creative data not found at {CREATIVE_DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CREATIVE_DATA_PATH, "r") as f:
        return json.load(f)


def save_creative_data(data):
    """Write creative-data.json."""
    with open(CREATIVE_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def meta_api_call(method, endpoint, access_token, data=None, files=None):
    """Make a Meta API call with exponential backoff on rate limits."""
    url = f"{META_API_BASE}/{endpoint}"

    for attempt in range(MAX_RETRIES):
        try:
            if method == "POST":
                if files:
                    params = {"access_token": access_token}
                    resp = requests.post(url, params=params, data=data or {}, files=files, timeout=120)
                else:
                    if data:
                        data["access_token"] = access_token
                    resp = requests.post(url, data=data, timeout=30)
            else:
                params = data or {}
                params["access_token"] = access_token
                resp = requests.get(url, params=params, timeout=30)

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


def upload_image(file_path, access_token, ad_account_id):
    """Upload an image to Meta and return the image hash."""
    print(f"  Uploading image: {file_path.name}")
    with open(file_path, "rb") as f:
        resp = meta_api_call("POST", f"{ad_account_id}/adimages", access_token,
                             files={"filename": (file_path.name, f, "image/png")})
    if not resp:
        return None

    images = resp.get("images", {})
    for name, info in images.items():
        return info.get("hash")
    return None


def upload_video(file_path, access_token, ad_account_id):
    """Upload a video to Meta and return the video ID (async upload with polling)."""
    print(f"  Uploading video: {file_path.name}")
    with open(file_path, "rb") as f:
        resp = meta_api_call("POST", f"{ad_account_id}/advideos", access_token,
                             data={"title": file_path.stem},
                             files={"source": (file_path.name, f, "video/mp4")})
    if not resp or "id" not in resp:
        return None

    video_id = resp["id"]
    print(f"    Video ID: {video_id} — polling for processing...")

    # Poll until ready
    for poll in range(VIDEO_POLL_MAX):
        time.sleep(VIDEO_POLL_INTERVAL)
        status_resp = meta_api_call("GET", video_id, access_token, {"fields": "status"})
        if not status_resp:
            continue
        status = status_resp.get("status", {})
        video_status = status.get("video_status", "processing")
        if video_status == "ready":
            print(f"    Video ready.")
            return video_id
        elif video_status == "error":
            print(f"    Video processing failed.", file=sys.stderr)
            return None
        else:
            if poll % 6 == 0:  # Every 30s
                print(f"    Still processing... ({poll * VIDEO_POLL_INTERVAL}s)")

    print(f"    Video processing timed out.", file=sys.stderr)
    return video_id  # Return anyway — may still be processing


def create_ad_creative(name, image_hash, page_id, copy_data, landing_url, access_token, ad_account_id):
    """Create an Ad Creative for an image."""
    link_data = {
        "image_hash": image_hash,
        "link": landing_url,
        "message": copy_data.get("primary_text", ""),
        "name": copy_data.get("headline", ""),
        "description": copy_data.get("description", ""),
        "call_to_action": {
            "type": copy_data.get("cta", "LEARN_MORE"),
            "value": {"link": landing_url},
        },
    }

    object_story_spec = {"page_id": page_id, "link_data": link_data}

    resp = meta_api_call("POST", f"{ad_account_id}/adcreatives", access_token, {
        "name": name,
        "object_story_spec": json.dumps(object_story_spec),
    })

    if resp and "id" in resp:
        return resp["id"]
    return None


def create_video_ad_creative(name, video_id, thumbnail_hash, page_id, copy_data, landing_url, access_token, ad_account_id):
    """Create an Ad Creative for a video."""
    video_data = {
        "video_id": video_id,
        "message": copy_data.get("primary_text", ""),
        "title": copy_data.get("headline", ""),
        "link_description": copy_data.get("description", ""),
        "call_to_action": {
            "type": copy_data.get("cta", "LEARN_MORE"),
            "value": {"link": landing_url},
        },
    }
    if thumbnail_hash:
        video_data["image_hash"] = thumbnail_hash

    object_story_spec = {"page_id": page_id, "video_data": video_data}

    resp = meta_api_call("POST", f"{ad_account_id}/adcreatives", access_token, {
        "name": name,
        "object_story_spec": json.dumps(object_story_spec),
    })

    if resp and "id" in resp:
        return resp["id"]
    return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Upload creative assets to Meta")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID from campaign-data.json")
    parser.add_argument("--batch-id", help="Specific batch ID (default: all campaign batches)")
    args = parser.parse_args()

    access_token, ad_account_id, page_id = load_env()

    # Load campaign data for landing page URL and page ID
    campaign_data = None
    if CAMPAIGN_DATA_PATH.exists():
        with open(CAMPAIGN_DATA_PATH, "r") as f:
            campaign_data = json.load(f)

    landing_url = ""
    if campaign_data:
        for camp in campaign_data.get("campaigns", []):
            if camp.get("campaign_id") == args.campaign_id:
                landing_url = camp.get("landing_page_url", "")
                page_id = page_id or camp.get("meta_page_id", "")
                break

    if not page_id:
        print("Warning: META_PAGE_ID not set. Ad creatives may fail without a page ID.", file=sys.stderr)

    creative_data = load_creative_data()
    uploaded_count = 0
    skipped_count = 0

    for batch in creative_data.get("batches", []):
        if batch.get("campaign_id") != args.campaign_id:
            continue
        if args.batch_id and batch.get("batch_id") != args.batch_id:
            continue

        print(f"\nProcessing batch: {batch.get('batch_id', 'unknown')}")

        for angle in batch.get("angles", []):
            copy_data = angle.get("copy", {})

            for creative in angle.get("creatives", []):
                # Skip already uploaded
                if creative.get("meta_creative_id"):
                    skipped_count += 1
                    continue

                file_path = PLUGIN_ROOT / creative.get("path", "")
                if not file_path.exists():
                    # Try relative to creatives dir
                    file_path = CREATIVES_DIR / creative.get("filename", "")
                if not file_path.exists():
                    print(f"  Skipping {creative.get('filename', 'unknown')} — file not found", file=sys.stderr)
                    continue

                asset_type = creative.get("type", "image")
                creative_name = f"{batch.get('batch_id', 'batch')} - {angle.get('name', 'angle')} - {creative.get('filename', 'asset')}"

                if asset_type == "video":
                    video_id = upload_video(file_path, access_token, ad_account_id)
                    if video_id:
                        # Use first image in angle as thumbnail if available
                        thumbnail_hash = None
                        creative_id = create_video_ad_creative(
                            creative_name, video_id, thumbnail_hash,
                            page_id, copy_data, landing_url,
                            access_token, ad_account_id
                        )
                        if creative_id:
                            creative["meta_creative_id"] = creative_id
                            creative["meta_video_id"] = video_id
                            uploaded_count += 1
                            print(f"    Creative ID: {creative_id}")
                else:
                    image_hash = upload_image(file_path, access_token, ad_account_id)
                    if image_hash:
                        creative_id = create_ad_creative(
                            creative_name, image_hash,
                            page_id, copy_data, landing_url,
                            access_token, ad_account_id
                        )
                        if creative_id:
                            creative["meta_creative_id"] = creative_id
                            creative["meta_image_hash"] = image_hash
                            uploaded_count += 1
                            print(f"    Creative ID: {creative_id}")

    save_creative_data(creative_data)

    print(f"\n═══ Upload Complete ═══")
    print(f"  Uploaded: {uploaded_count}")
    print(f"  Skipped (already uploaded): {skipped_count}")
    print(f"  Creative IDs stored in creative-data.json.\n")


if __name__ == "__main__":
    main()
