#!/usr/bin/env python3
"""
deploy-landing-page.py — Deploy a landing page to Cloudflare Pages via wrangler CLI.

Each campaign deploys to its own isolated Cloudflare Pages project, derived from
campaign.landing_page.pages_project (explicit) or auto-generated as
"apg-lp-{campaign_id}" (fallback). Campaigns never overwrite each other.

Wrangler is used for the actual upload — it handles the two-step signed-URL
upload process that the raw Cloudflare API requires. The raw API approach
silently accepts uploads but fails to serve files correctly.

Usage:
    # Dry run — show what would be deployed
    python3 marketing-plugin/scripts/deploy-landing-page.py \
        --campaign-id marketing-plugin

    # Execute deployment
    python3 marketing-plugin/scripts/deploy-landing-page.py \
        --campaign-id marketing-plugin --execute

Requires:
    npx wrangler (bundled with Node.js / npx — no separate install needed)
    CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in .env
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)

from _config import load_config


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent
REPO_ROOT = PLUGIN_ROOT.parent
CAMPAIGN_DATA_PATH: Path = None

_config = load_config()
CF_API_BASE = "https://api.cloudflare.com/client/v4"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load .env and return (api_token, account_id)."""
    for env_path in [PLUGIN_ROOT / ".env", REPO_ROOT / ".env"]:
        if env_path.exists():
            load_dotenv(env_path)
            break

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
    if not CAMPAIGN_DATA_PATH.exists():
        print(f"Error: Campaign data not found at {CAMPAIGN_DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CAMPAIGN_DATA_PATH) as f:
        return json.load(f)


def save_campaign_data(campaign):
    with open(CAMPAIGN_DATA_PATH, "w") as f:
        json.dump(campaign, f, indent=2)
    registry_path = PLUGIN_ROOT / "data" / "campaigns.json"
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
        for entry in registry.get("campaigns", []):
            if entry.get("campaign_id") == campaign.get("campaign_id"):
                entry["status"] = campaign.get("status", entry["status"])
                entry["updated_at"] = campaign.get("updated_at", entry["updated_at"])
                break
        with open(registry_path, "w") as f:
            json.dump(registry, f, indent=2)


def derive_project_name(campaign_id: str) -> str:
    """Derive a Cloudflare Pages project name from campaign_id (max 28 chars)."""
    return f"apg-lp-{campaign_id}"[:28].rstrip("-")


# ─── Wrangler Deploy ──────────────────────────────────────────────────────────

def deploy_via_wrangler(api_token, account_id, project_name, source_dir):
    """
    Deploy source_dir to Cloudflare Pages using wrangler CLI.
    Returns the deployment preview URL.
    """
    env = {**os.environ, "CLOUDFLARE_API_TOKEN": api_token, "CLOUDFLARE_ACCOUNT_ID": account_id}

    result = subprocess.run(
        [
            "npx", "wrangler", "pages", "deploy", ".",
            "--project-name", project_name,
            "--branch", "main",
            "--commit-dirty=true",
        ],
        cwd=str(source_dir),
        env=env,
        capture_output=True,
        text=True,
    )

    # Print wrangler output (strip noisy warning lines)
    for line in result.stdout.splitlines():
        if line.strip():
            print(f"  {line}")

    if result.returncode != 0:
        print(f"  ERROR: wrangler deploy failed", file=sys.stderr)
        for line in result.stderr.splitlines():
            if line.strip() and "WARNING" not in line and "update available" not in line:
                print(f"  {line}", file=sys.stderr)
        sys.exit(1)

    # Extract the deployment URL from wrangler output
    deploy_url = ""
    for line in result.stdout.splitlines():
        if "pages.dev" in line:
            parts = line.split()
            for part in parts:
                if "pages.dev" in part:
                    deploy_url = part.strip()
                    break

    return deploy_url


# ─── Custom Domain ────────────────────────────────────────────────────────────

def ensure_custom_domain(api_token, account_id, project_name, domain):
    """Add the custom domain to the project if not already configured."""
    try:
        import requests
    except ImportError:
        print("  WARNING: 'requests' not installed — skipping custom domain setup", file=sys.stderr)
        print(f"  Add manually in Cloudflare: {domain} → {project_name}.pages.dev", file=sys.stderr)
        return

    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}

    # Check existing domains
    resp = requests.get(
        f"{CF_API_BASE}/accounts/{account_id}/pages/projects/{project_name}/domains",
        headers=headers, timeout=30,
    )
    if resp.status_code == 200:
        existing = [d.get("name") for d in resp.json().get("result", [])]
        if domain in existing:
            print(f"  Custom domain already configured: {domain}")
            return

    # Add domain
    resp = requests.post(
        f"{CF_API_BASE}/accounts/{account_id}/pages/projects/{project_name}/domains",
        headers=headers, json={"name": domain}, timeout=30,
    )
    if resp.status_code in (200, 201) and resp.json().get("success"):
        print(f"  Custom domain added: {domain}")
    else:
        print(f"  WARNING: Could not auto-add custom domain ({resp.status_code})", file=sys.stderr)
        print(f"  Add a CNAME manually: {domain} → {project_name}.pages.dev", file=sys.stderr)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deploy landing page to Cloudflare Pages via wrangler")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    global CAMPAIGN_DATA_PATH
    CAMPAIGN_DATA_PATH = PLUGIN_ROOT / "data" / "campaigns" / args.campaign_id / "campaign.json"

    is_dry_run = not args.execute
    api_token, account_id = load_env()

    campaign = load_campaign_data()
    landing_page = campaign.get("landing_page", {})

    project_name = landing_page.get("pages_project") or derive_project_name(args.campaign_id)

    deploy_path = landing_page.get("deploy_path")
    if not deploy_path:
        print("Error: No deploy_path set in campaign.json", file=sys.stderr)
        sys.exit(1)

    source_dir = PLUGIN_ROOT / deploy_path
    if not (source_dir / "index.html").exists():
        print(f"Error: index.html not found at {source_dir}", file=sys.stderr)
        sys.exit(1)

    files = [f for f in source_dir.rglob("*") if f.is_file()]
    domain = landing_page.get("domain", "")
    full_url = f"https://{domain}/" if domain else f"https://{project_name}.pages.dev/"

    print(f"\n{'DRY RUN' if is_dry_run else 'DEPLOYING'} — {campaign.get('name', args.campaign_id)}")
    print(f"\n  Files to deploy:")
    for f in sorted(files):
        print(f"    - {f.relative_to(source_dir)} ({f.stat().st_size / 1024:.1f}KB)")
    print(f"\n  Pages project: {project_name}")
    print(f"  Custom domain: {domain or '(none)'}")
    print(f"  URL: {full_url}")

    if is_dry_run:
        print(f"\n  Dry run complete. Use --execute to deploy.")
        return

    # Deploy via wrangler
    print(f"\n  Deploying via wrangler...")
    deploy_url = deploy_via_wrangler(api_token, account_id, project_name, source_dir)

    # Add custom domain if configured
    if domain:
        ensure_custom_domain(api_token, account_id, project_name, domain)

    # Update campaign.json
    now = datetime.now(timezone.utc).isoformat()
    campaign["landing_page"]["status"] = "deployed"
    campaign["landing_page"]["pages_project"] = project_name
    campaign["landing_page"]["pages_dev_url"] = deploy_url
    campaign["landing_page"]["deployed_at"] = now
    campaign["updated_at"] = now

    if "approval_log" not in campaign:
        campaign["approval_log"] = []
    campaign["approval_log"].append({
        "gate": "landing_page",
        "status": "approved",
        "timestamp": now,
        "notes": f"Deployed via wrangler to '{project_name}'. Domain: {domain or 'pages.dev only'}."
    })

    save_campaign_data(campaign)

    print(f"\n  Deployment successful!")
    print(f"  Pages dev URL: {deploy_url}")
    if domain:
        print(f"  Custom domain: https://{domain}/")
    print(f"  Project: {project_name}")


if __name__ == "__main__":
    main()
