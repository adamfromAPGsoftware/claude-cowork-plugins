#!/usr/bin/env python3
"""
deploy-landing-page.py — Deploy a landing page to Cloudflare Pages.

Reads campaign-data.json for the specified campaign, copies the generated landing
page to a staging directory, and deploys to the 'apg-landing-pages' Cloudflare
Pages project via the Cloudflare API (Direct Upload).

Usage:
    # Dry run (default) — show what would be deployed
    python3 marketing-plugin/scripts/deploy-landing-page.py \
        --campaign-id camp-2026-04-07-001

    # Execute deployment
    python3 marketing-plugin/scripts/deploy-landing-page.py \
        --campaign-id camp-2026-04-07-001 --execute

Requires:
    pip install requests python-dotenv
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
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

PLUGIN_ROOT = Path(__file__).parent.parent
REPO_ROOT = PLUGIN_ROOT.parent

CAMPAIGN_DATA_PATH = PLUGIN_ROOT / "data" / "campaign-data.json"
OUTPUT_DIR = PLUGIN_ROOT / "data" / "landing-pages"

PAGES_PROJECT_NAME = "apg-landing-pages"
CF_API_BASE = "https://api.cloudflare.com/client/v4"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables and return required Cloudflare credentials."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = REPO_ROOT / ".env"
    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")

    if not api_token:
        print("Error: CLOUDFLARE_API_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)
    if not account_id:
        print("Error: CLOUDFLARE_ACCOUNT_ID not set in .env", file=sys.stderr)
        sys.exit(1)

    return api_token, account_id


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


def cf_headers(api_token):
    """Cloudflare API headers."""
    return {
        "Authorization": f"Bearer {api_token}",
    }


def create_deployment(api_token, account_id, project_name, deploy_dir):
    """
    Deploy files to Cloudflare Pages via Direct Upload API.

    1. Create a deployment to get an upload URL
    2. Upload files as a multipart form
    """
    # Step 1: Create deployment
    url = f"{CF_API_BASE}/accounts/{account_id}/pages/projects/{project_name}/deployments"

    # Collect files to upload
    files_to_upload = []
    for file_path in sorted(deploy_dir.rglob("*")):
        if file_path.is_file():
            rel_path = file_path.relative_to(deploy_dir)
            files_to_upload.append((str(rel_path), file_path))

    if not files_to_upload:
        print("Error: No files to deploy", file=sys.stderr)
        sys.exit(1)

    # Build multipart form data
    multipart_files = []
    for rel_path, abs_path in files_to_upload:
        content_type = "text/html" if abs_path.suffix == ".html" else "application/octet-stream"
        multipart_files.append(
            (rel_path, (rel_path, abs_path.read_bytes(), content_type))
        )

    print(f"  Uploading {len(files_to_upload)} file(s) to Cloudflare Pages...")
    resp = requests.post(
        url,
        headers=cf_headers(api_token),
        files=multipart_files,
        timeout=120,
    )

    if resp.status_code not in (200, 201):
        print(f"  ERROR: Deployment failed ({resp.status_code})", file=sys.stderr)
        print(f"  Response: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    if not result.get("success"):
        errors = result.get("errors", [])
        print(f"  ERROR: {errors}", file=sys.stderr)
        sys.exit(1)

    deployment = result.get("result", {})
    deploy_url = deployment.get("url", "")
    deploy_id = deployment.get("id", "")

    return deploy_url, deploy_id


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deploy landing page to Cloudflare Pages")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview what would be deployed (default)")
    parser.add_argument("--execute", action="store_true",
                        help="Actually deploy to Cloudflare Pages")
    args = parser.parse_args()

    # If --execute is passed, disable dry-run
    is_dry_run = not args.execute

    api_token, account_id = load_env()

    # Load campaign
    data = load_campaign_data()
    idx, campaign = find_campaign(data, args.campaign_id)
    landing_page = campaign.get("landing_page", {})

    # Verify landing page exists
    deploy_path = landing_page.get("deploy_path")
    if not deploy_path:
        print("Error: No deploy_path set. Run generate-landing-page.py first.", file=sys.stderr)
        sys.exit(1)

    source_dir = PLUGIN_ROOT / deploy_path
    index_html = source_dir / "index.html"

    if not index_html.exists():
        print(f"Error: Landing page not found at {index_html}", file=sys.stderr)
        sys.exit(1)

    # Collect files
    files = list(source_dir.rglob("*"))
    files = [f for f in files if f.is_file()]

    domain = landing_page.get("domain", "(not configured)")
    full_url = landing_page.get("full_url", f"https://{PAGES_PROJECT_NAME}.pages.dev/{args.campaign_id}/")

    print(f"\n{'DRY RUN' if is_dry_run else 'DEPLOYING'} — {campaign.get('name', args.campaign_id)}")
    print(f"\n  Files to deploy:")
    for f in files:
        rel = f.relative_to(source_dir)
        size_kb = f.stat().st_size / 1024
        print(f"    - {rel} ({size_kb:.1f}KB)")

    print(f"\n  Target: {PAGES_PROJECT_NAME} (Cloudflare Pages)")
    print(f"  Domain: {domain}")
    print(f"  URL: {full_url}")

    if is_dry_run:
        print(f"\n  Dry run complete. Use --execute to deploy.")
        return

    # Stage files — copy to temp directory with campaign_id as subdirectory
    with tempfile.TemporaryDirectory() as staging:
        staging_path = Path(staging)
        for f in files:
            rel = f.relative_to(source_dir)
            dest = staging_path / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)

        # Deploy
        deploy_url, deploy_id = create_deployment(
            api_token, account_id, PAGES_PROJECT_NAME, staging_path
        )

    # Update campaign-data.json
    now = datetime.now(timezone.utc).isoformat()
    campaign["landing_page"]["status"] = "deployed"
    campaign["landing_page"]["deployed_at"] = now
    campaign["updated_at"] = now

    # Add approval log entry
    if "approval_log" not in campaign:
        campaign["approval_log"] = []
    campaign["approval_log"].append({
        "gate": "landing_page",
        "status": "approved",
        "timestamp": now,
        "notes": f"Deployed to Cloudflare Pages. Deployment ID: {deploy_id}"
    })

    data["campaigns"][idx] = campaign
    save_campaign_data(data)

    print(f"\n  Deployment successful!")
    print(f"  URL: {deploy_url}")
    print(f"  Deployment ID: {deploy_id}")
    print(f"  Status: deployed")


if __name__ == "__main__":
    main()
