#!/usr/bin/env python3
"""
download-competitor-assets.py — Download competitor ad creative images/videos to local storage.

Reads competitor-data.json, finds ads with creative_url but no local_path,
and downloads them to data/competitor-assets/{page_id}/{ad_id}.{ext}.

Usage:
  python3 marketing-plugin/scripts/download-competitor-assets.py
  python3 marketing-plugin/scripts/download-competitor-assets.py --competitor 12345678
  python3 marketing-plugin/scripts/download-competitor-assets.py --limit 20

Requires:
  pip install requests python-dotenv
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

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

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/
COMPETITOR_DATA_PATH = PLUGIN_ROOT / "data" / "competitor-data.json"
ASSETS_DIR = PLUGIN_ROOT / "data" / "competitor-assets"

DOWNLOAD_TIMEOUT = 60
CHUNK_SIZE = 8192

# Content-type to extension mapping
CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
}

# Fallback extension mapping from URL
URL_EXT_MAP = {
    ".jpg": ".jpg",
    ".jpeg": ".jpg",
    ".png": ".png",
    ".webp": ".webp",
    ".gif": ".gif",
    ".mp4": ".mp4",
    ".mov": ".mov",
    ".webm": ".webm",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env (plugin dir first, then repo root)."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)


def load_competitor_data() -> dict:
    """Load competitor-data.json."""
    if not COMPETITOR_DATA_PATH.exists():
        print("Error: competitor-data.json not found.", file=sys.stderr)
        print(f"  Expected at: {COMPETITOR_DATA_PATH}", file=sys.stderr)
        print("  Run scrape-competitor-ads.py first to populate competitor data.", file=sys.stderr)
        sys.exit(1)

    with open(COMPETITOR_DATA_PATH) as f:
        return json.load(f)


def save_competitor_data(data: dict):
    """Save competitor-data.json."""
    with open(COMPETITOR_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def determine_extension(url: str, content_type: str = None) -> str:
    """Determine file extension from content-type header or URL."""
    # Try content-type first
    if content_type:
        ct = content_type.split(";")[0].strip().lower()
        ext = CONTENT_TYPE_EXT.get(ct)
        if ext:
            return ext

    # Fall back to URL extension
    parsed = urlparse(url)
    path = parsed.path.lower()
    for url_ext, file_ext in URL_EXT_MAP.items():
        if path.endswith(url_ext):
            return file_ext

    # Default based on creative type hint
    return ".jpg"


def download_file(url: str, dest: Path) -> tuple:
    """Download a file with streaming. Returns (success, file_size_bytes)."""
    try:
        resp = requests.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "")
        ext = determine_extension(url, content_type)

        # Update destination with correct extension if needed
        if dest.suffix != ext:
            dest = dest.with_suffix(ext)

        dest.parent.mkdir(parents=True, exist_ok=True)

        total_bytes = 0
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
                total_bytes += len(chunk)

        return True, total_bytes, dest

    except requests.exceptions.Timeout:
        print(f"    Download timed out ({DOWNLOAD_TIMEOUT}s)")
        return False, 0, dest

    except requests.exceptions.HTTPError as e:
        print(f"    HTTP error: {e}")
        return False, 0, dest

    except Exception as e:
        print(f"    Download failed: {e}")
        return False, 0, dest


def format_size(size_bytes: int) -> str:
    """Format byte count as human-readable string."""
    if size_bytes >= 1_048_576:
        return f"{size_bytes / 1_048_576:.1f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f} KB"
    return f"{size_bytes} B"


# ─── Main ─────────────────────────────────────────────────────────────────────

def check_url_alive(url: str) -> tuple:
    """HEAD-check a URL. Returns (alive: bool, status_code: int)."""
    try:
        resp = requests.head(url, timeout=15, allow_redirects=True)
        return resp.status_code == 200, resp.status_code
    except Exception:
        return False, 0


def main():
    parser = argparse.ArgumentParser(description="Download competitor ad creative assets.")
    parser.add_argument("--competitor", type=str, default=None,
                        help="Filter by Page ID (download only this competitor's assets).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum number of assets to download per run.")
    parser.add_argument("--force", action="store_true",
                        help="Re-download assets even if already downloaded (still skips expired URLs).")
    args = parser.parse_args()

    # Load env (may need proxy settings etc.)
    load_env()

    # Load data
    data = load_competitor_data()
    ads = data.get("ads", [])

    if not ads:
        print("No ads in competitor-data.json. Run scrape-competitor-ads.py first.")
        sys.exit(0)

    # Filter to ads needing download
    pending = []
    for i, ad in enumerate(ads):
        creative_url = ad.get("creative_url")
        download_status = ad.get("download_status")

        if not creative_url:
            continue

        # Always skip expired URLs — even with --force
        if download_status == "expired":
            continue

        # Skip already-downloaded unless --force
        if download_status == "downloaded" and not args.force:
            continue

        # Legacy check: skip ads with local_path already set (unless --force)
        if ad.get("local_path") and not args.force:
            continue

        if args.competitor and ad.get("page_id") != args.competitor:
            continue

        pending.append((i, ad))

    if not pending:
        print("No pending downloads.")
        if args.competitor:
            print(f"  (Filtered to page_id: {args.competitor})")
        print("  All ads either downloaded or expired.")
        sys.exit(0)

    # Apply limit
    if args.limit and args.limit < len(pending):
        pending = pending[:args.limit]

    print(f"Downloading {len(pending)} creative assets...")
    if args.competitor:
        print(f"  Filtered to competitor: {args.competitor}")
    if args.force:
        print(f"  --force: re-downloading previously downloaded assets")
    print(f"  Assets directory: {ASSETS_DIR}")

    downloaded_count = 0
    skipped_count = 0
    expired_count = 0
    failed_count = 0
    total_bytes = 0

    for idx, (ad_index, ad) in enumerate(pending, 1):
        ad_id = ad.get("ad_id", "unknown")
        page_id = ad.get("page_id", "unknown")
        page_name = ad.get("page_name", page_id)
        creative_url = ad["creative_url"]
        creative_type = ad.get("creative_type", "image")

        # Determine initial extension
        ext = determine_extension(creative_url)
        dest_dir = ASSETS_DIR / page_id
        dest_path = dest_dir / f"{ad_id}{ext}"

        print(f"\n  [{idx}/{len(pending)}] {page_name} — {ad_id} ({creative_type})")

        # HEAD check — detect expired URLs before downloading
        alive, status_code = check_url_alive(creative_url)
        if not alive and status_code in (403, 404):
            print(f"    URL expired (HTTP {status_code}). Skipping.")
            ads[ad_index]["download_status"] = "expired"
            expired_count += 1
            continue

        # Check if file already exists (idempotent, unless --force)
        if not args.force:
            if dest_path.exists():
                size = dest_path.stat().st_size
                print(f"    Already exists: {dest_path.name} ({format_size(size)})")
                rel_path = str(dest_path.relative_to(PLUGIN_ROOT))
                ads[ad_index]["local_path"] = rel_path
                ads[ad_index]["download_status"] = "downloaded"
                skipped_count += 1
                continue

            # Also check with other common extensions
            existing = None
            for alt_ext in URL_EXT_MAP.values():
                alt_path = dest_dir / f"{ad_id}{alt_ext}"
                if alt_path.exists():
                    existing = alt_path
                    break

            if existing:
                size = existing.stat().st_size
                print(f"    Already exists: {existing.name} ({format_size(size)})")
                rel_path = str(existing.relative_to(PLUGIN_ROOT))
                ads[ad_index]["local_path"] = rel_path
                ads[ad_index]["download_status"] = "downloaded"
                skipped_count += 1
                continue

        # Download
        success, file_size, actual_dest = download_file(creative_url, dest_path)

        if success:
            rel_path = str(actual_dest.relative_to(PLUGIN_ROOT))
            ads[ad_index]["local_path"] = rel_path
            ads[ad_index]["download_status"] = "downloaded"
            downloaded_count += 1
            total_bytes += file_size
            print(f"    Saved: {actual_dest.name} ({format_size(file_size)})")
        else:
            ads[ad_index]["download_status"] = f"failed"
            failed_count += 1

    # Save updated data
    data["ads"] = ads
    save_competitor_data(data)

    # Print summary
    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Downloaded:   {downloaded_count}")
    print(f"  Expired:      {expired_count}")
    print(f"  Failed:       {failed_count}")
    print(f"  Skipped:      {skipped_count} (already done)")
    print(f"  Total size:   {format_size(total_bytes)}")
    print(f"  Saved to:     {COMPETITOR_DATA_PATH}")


if __name__ == "__main__":
    main()
