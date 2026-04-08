#!/usr/bin/env python3
"""
setup-cloudflare-domain.py — Configure a subdomain on Cloudflare DNS for a Pages project.

Creates a CNAME record pointing a subdomain (e.g., audit.{YOUR_DOMAIN}) to the
apg-landing-pages Cloudflare Pages project, and adds it as a custom domain on the project.

Usage:
    # Dry run (default) — show what would be configured
    python3 marketing-plugin/scripts/setup-cloudflare-domain.py \
        --domain audit.{YOUR_DOMAIN}

    # Execute
    python3 marketing-plugin/scripts/setup-cloudflare-domain.py \
        --domain audit.{YOUR_DOMAIN} --execute

Requires:
    pip install requests python-dotenv
"""

import argparse
import json
import os
import sys
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

CF_API_BASE = "https://api.cloudflare.com/client/v4"
DEFAULT_PAGES_PROJECT = "apg-landing-pages"
BASE_DOMAIN = "{YOUR_DOMAIN}"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables and return Cloudflare credentials."""
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


def cf_headers(api_token):
    """Standard Cloudflare API headers."""
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }


def get_zone_id(api_token, domain):
    """Look up the Cloudflare zone ID for a domain."""
    # Extract the base domain (last two parts)
    parts = domain.split(".")
    if len(parts) < 2:
        print(f"Error: Invalid domain: {domain}", file=sys.stderr)
        sys.exit(1)
    base = ".".join(parts[-2:])

    url = f"{CF_API_BASE}/zones"
    params = {"name": base, "status": "active"}

    resp = requests.get(url, headers=cf_headers(api_token), params=params, timeout=30)
    if resp.status_code != 200:
        print(f"Error: Failed to list zones ({resp.status_code}): {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    zones = result.get("result", [])
    if not zones:
        print(f"Error: Zone not found for '{base}'. Is it in your Cloudflare account?", file=sys.stderr)
        sys.exit(1)

    return zones[0]["id"], base


def check_existing_record(api_token, zone_id, record_name):
    """Check if a DNS record already exists. Returns record ID or None."""
    url = f"{CF_API_BASE}/zones/{zone_id}/dns_records"
    params = {"type": "CNAME", "name": record_name}

    resp = requests.get(url, headers=cf_headers(api_token), params=params, timeout=30)
    if resp.status_code != 200:
        return None

    records = resp.json().get("result", [])
    for r in records:
        if r.get("name") == record_name:
            return r["id"]
    return None


def create_cname_record(api_token, zone_id, subdomain, target, proxied=True):
    """Create a CNAME DNS record."""
    url = f"{CF_API_BASE}/zones/{zone_id}/dns_records"
    payload = {
        "type": "CNAME",
        "name": subdomain,
        "content": target,
        "proxied": proxied,
        "ttl": 1,  # Auto TTL when proxied
    }

    resp = requests.post(url, headers=cf_headers(api_token), json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"Error: Failed to create CNAME ({resp.status_code}): {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    if not result.get("success"):
        errors = result.get("errors", [])
        print(f"Error: {errors}", file=sys.stderr)
        sys.exit(1)

    return result.get("result", {}).get("id")


def update_cname_record(api_token, zone_id, record_id, subdomain, target, proxied=True):
    """Update an existing CNAME DNS record."""
    url = f"{CF_API_BASE}/zones/{zone_id}/dns_records/{record_id}"
    payload = {
        "type": "CNAME",
        "name": subdomain,
        "content": target,
        "proxied": proxied,
        "ttl": 1,
    }

    resp = requests.put(url, headers=cf_headers(api_token), json=payload, timeout=30)
    if resp.status_code != 200:
        print(f"Error: Failed to update CNAME ({resp.status_code}): {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)

    return resp.json().get("result", {}).get("id")


def add_custom_domain_to_pages(api_token, account_id, project_name, domain):
    """Add a custom domain to a Cloudflare Pages project."""
    url = f"{CF_API_BASE}/accounts/{account_id}/pages/projects/{project_name}/domains"
    payload = {"name": domain}

    resp = requests.post(url, headers=cf_headers(api_token), json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        # 409 means domain already exists on project — that's fine
        if resp.status_code == 409:
            print(f"  Custom domain already configured on {project_name}")
            return True
        print(f"Error: Failed to add custom domain ({resp.status_code}): {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    if not result.get("success"):
        errors = result.get("errors", [])
        print(f"Error: {errors}", file=sys.stderr)
        sys.exit(1)

    return True


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Setup Cloudflare subdomain for Pages project")
    parser.add_argument("--domain", required=True,
                        help="Full subdomain (e.g., audit.{YOUR_DOMAIN})")
    parser.add_argument("--pages-project", default=DEFAULT_PAGES_PROJECT,
                        help=f"Pages project name (default: {DEFAULT_PAGES_PROJECT})")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Show what would be configured (default)")
    parser.add_argument("--execute", action="store_true",
                        help="Actually create DNS records and configure domain")
    args = parser.parse_args()

    is_dry_run = not args.execute
    domain = args.domain.lower().strip()
    pages_project = args.pages_project
    pages_target = f"{pages_project}.pages.dev"

    # Extract subdomain part
    parts = domain.split(".")
    if len(parts) < 3:
        print(f"Error: Expected a subdomain (e.g., audit.{YOUR_DOMAIN}), got: {domain}", file=sys.stderr)
        sys.exit(1)
    subdomain_part = parts[0]
    base_domain_parts = ".".join(parts[-2:])

    api_token, account_id = load_env()

    print(f"\n{'DRY RUN' if is_dry_run else 'CONFIGURING'} — {domain}")

    # Look up zone
    zone_id, base_domain = get_zone_id(api_token, domain)
    print(f"\n  Zone: {base_domain} ({zone_id})")

    # Check for existing record
    existing_id = check_existing_record(api_token, zone_id, domain)
    if existing_id:
        print(f"  Existing CNAME found: {domain} (record: {existing_id})")
        action = "update"
    else:
        action = "create"

    # Plan
    print(f"\n  DNS Record:")
    print(f"    Action: {action}")
    print(f"    Type: CNAME")
    print(f"    Name: {subdomain_part}")
    print(f"    Target: {pages_target}")
    print(f"    Proxied: Yes")

    print(f"\n  Pages Custom Domain:")
    print(f"    Project: {pages_project}")
    print(f"    Domain: {domain}")

    print(f"\n  SSL: Auto-provisioned by Cloudflare (Universal SSL)")

    if is_dry_run:
        print(f"\n  Dry run complete. Use --execute to configure.")
        return

    # Execute
    print(f"\n  Creating DNS record...")
    if action == "update":
        record_id = update_cname_record(api_token, zone_id, existing_id, domain, pages_target)
        print(f"  CNAME updated: {record_id}")
    else:
        record_id = create_cname_record(api_token, zone_id, domain, pages_target)
        print(f"  CNAME created: {record_id}")

    print(f"  Adding custom domain to Pages project...")
    add_custom_domain_to_pages(api_token, account_id, pages_project, domain)
    print(f"  Custom domain added: {domain}")

    print(f"\n  Domain configured successfully!")
    print(f"  URL: https://{domain}/")
    print(f"  SSL will be active within a few minutes.")


if __name__ == "__main__":
    main()
