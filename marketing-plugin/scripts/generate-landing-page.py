#!/usr/bin/env python3
"""
generate-landing-page.py — Generate landing page HTML from campaign config and templates.

Reads campaign-data.json for a specified campaign, loads the appropriate template,
performs {{variable}} substitution, injects form fields and benefits HTML,
and writes the output to data/landing-pages/{campaign_id}/index.html.

Usage:
    python3 marketing-plugin/scripts/generate-landing-page.py \
        --campaign-id camp-2026-04-07-001

Requires:
    pip install python-dotenv
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/
REPO_ROOT = PLUGIN_ROOT.parent

CAMPAIGN_DATA_PATH = PLUGIN_ROOT / "data" / "campaign-data.json"
TEMPLATES_DIR = PLUGIN_ROOT / "templates" / "landing-pages"
COMPONENTS_DIR = TEMPLATES_DIR / "components"
OUTPUT_DIR = PLUGIN_ROOT / "data" / "landing-pages"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = REPO_ROOT / ".env"
    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)


def load_campaign_data():
    """Load and return campaign-data.json."""
    if not CAMPAIGN_DATA_PATH.exists():
        print(f"Error: Campaign data not found at {CAMPAIGN_DATA_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(CAMPAIGN_DATA_PATH, "r") as f:
        return json.load(f)


def save_campaign_data(data):
    """Write campaign-data.json back to disk."""
    with open(CAMPAIGN_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Updated: {CAMPAIGN_DATA_PATH}")


def find_campaign(data, campaign_id):
    """Find a campaign by ID. Returns (index, campaign) or exits."""
    for i, camp in enumerate(data.get("campaigns", [])):
        if camp.get("campaign_id") == campaign_id:
            return i, camp
    print(f"Error: Campaign '{campaign_id}' not found in campaign-data.json", file=sys.stderr)
    sys.exit(1)


def build_form_fields_html(form_fields):
    """Generate HTML for form fields from a list of field names."""
    if not form_fields:
        return ""

    field_map = {
        "name": ("text", "Your full name"),
        "first_name": ("text", "First name"),
        "last_name": ("text", "Last name"),
        "email": ("email", "Email address"),
        "phone": ("tel", "Phone number"),
        "company": ("text", "Company name"),
        "business_name": ("text", "Business name"),
        "website": ("url", "Website URL"),
        "role": ("text", "Your role"),
        "message": ("textarea", "Tell us about your situation..."),
        "revenue": ("text", "Annual revenue"),
        "team_size": ("text", "Team size"),
    }

    parts = []
    for field in form_fields:
        field_lower = field.lower().replace(" ", "_")
        input_type, placeholder = field_map.get(field_lower, ("text", field.replace("_", " ").title()))

        if input_type == "textarea":
            parts.append(
                f'<div class="form-group">\n'
                f'  <textarea name="{field_lower}" placeholder="{placeholder}" required></textarea>\n'
                f'</div>'
            )
        else:
            parts.append(
                f'<div class="form-group">\n'
                f'  <input type="{input_type}" name="{field_lower}" placeholder="{placeholder}" required>\n'
                f'</div>'
            )

    return "\n".join(parts)


def build_benefits_html(benefits):
    """Generate HTML for benefits grid from a list of benefit strings or objects."""
    if not benefits:
        return ""

    icons = ["&#x2713;", "&#x26A1;", "&#x1F4CA;", "&#x1F680;", "&#x1F3AF;", "&#x2B50;",
             "&#x1F4A1;", "&#x1F512;", "&#x2764;", "&#x1F4B0;"]

    parts = []
    for i, benefit in enumerate(benefits):
        icon = icons[i % len(icons)]

        if isinstance(benefit, dict):
            title = benefit.get("title", "")
            desc = benefit.get("description", "")
        else:
            # Simple string — use as both title and description
            title = str(benefit)
            desc = ""

        card = (
            f'<div class="benefit-card">\n'
            f'  <div class="benefit-icon">{icon}</div>\n'
            f'  <h3>{title}</h3>\n'
        )
        if desc:
            card += f'  <p>{desc}</p>\n'
        card += '</div>'
        parts.append(card)

    return "\n".join(parts)


def build_social_proof_html(social_proof):
    """Generate HTML for social proof from a list of strings or objects."""
    if not social_proof:
        return ""

    parts = []
    for item in social_proof:
        if isinstance(item, dict):
            quote = item.get("quote", item.get("text", ""))
            author = item.get("author", item.get("name", ""))
            parts.append(
                f'<div class="testimonial">\n'
                f'  <blockquote>"{quote}"</blockquote>\n'
                f'  <div class="attribution">— {author}</div>\n'
                f'</div>'
            )
        else:
            # Simple string — treat as a testimonial quote
            parts.append(
                f'<div class="testimonial">\n'
                f'  <blockquote>"{item}"</blockquote>\n'
                f'</div>'
            )

    return "\n".join(parts)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate landing page HTML from campaign config")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID (e.g., camp-2026-04-07-001)")
    args = parser.parse_args()

    load_env()

    # Load campaign data
    data = load_campaign_data()
    idx, campaign = find_campaign(data, args.campaign_id)

    print(f"\nGenerating landing page for: {campaign.get('name', args.campaign_id)}")

    # Extract config sections
    product = campaign.get("product", {})
    audience = campaign.get("audience", {})
    creatives = campaign.get("creatives", {})
    tracking = campaign.get("tracking", {})
    landing_page = campaign.get("landing_page", {})
    lead_capture = campaign.get("lead_capture", {})
    lp_copy = creatives.get("landing_page_copy", {})

    if not lp_copy:
        print("Error: No landing_page_copy found in campaign creatives section.", file=sys.stderr)
        print("  Populate creatives.landing_page_copy first (via Campaign Planner).", file=sys.stderr)
        sys.exit(1)

    # Determine template
    template_name = landing_page.get("template", "lead-gen")
    template_path = TEMPLATES_DIR / f"{template_name}.html"

    if not template_path.exists():
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
        print(f"  Available templates: {[f.stem for f in TEMPLATES_DIR.glob('*.html')]}", file=sys.stderr)
        sys.exit(1)

    print(f"  Template: {template_name}")

    # Load template
    template_html = template_path.read_text()

    # Build component HTML
    form_fields = lp_copy.get("form_fields", ["name", "email", "phone"])
    form_fields_html = build_form_fields_html(form_fields)
    benefits_html = build_benefits_html(lp_copy.get("benefits", []))
    social_proof_html = build_social_proof_html(lp_copy.get("social_proof", []))

    # Determine form action
    form_action = lead_capture.get("form_webhook_url") or "#"

    # Perform substitutions
    substitutions = {
        "{{headline}}": lp_copy.get("headline", ""),
        "{{subheadline}}": lp_copy.get("subheadline", ""),
        "{{benefits_html}}": benefits_html,
        "{{social_proof_html}}": social_proof_html,
        "{{cta_text}}": lp_copy.get("cta_text", "Get Started"),
        "{{form_action}}": form_action,
        "{{form_fields_html}}": form_fields_html,
        "{{campaign_name}}": campaign.get("name", args.campaign_id),
        "{{utm_source}}": tracking.get("utm_source", "meta"),
        "{{utm_medium}}": tracking.get("utm_medium", "paid"),
        "{{utm_campaign}}": tracking.get("utm_campaign", args.campaign_id),
    }

    output_html = template_html
    for placeholder, value in substitutions.items():
        output_html = output_html.replace(placeholder, value)

    # Check for tracking template — inject if tracking IDs are present
    tracking_template_path = COMPONENTS_DIR / "tracking.html"
    ga4_id = tracking.get("ga4_measurement_id")
    pixel_id = tracking.get("meta_pixel_id")

    if tracking_template_path.exists() and (ga4_id or pixel_id):
        tracking_html = tracking_template_path.read_text()
        if ga4_id:
            tracking_html = tracking_html.replace("{{ga4_measurement_id}}", ga4_id)
        else:
            # Remove GA4 block if no ID
            tracking_html = re.sub(
                r'<!-- ─── GA4.*?</script>\n', '', tracking_html, flags=re.DOTALL
            )
        if pixel_id:
            tracking_html = tracking_html.replace("{{meta_pixel_id}}", pixel_id)
        else:
            # Remove Meta Pixel block if no ID
            tracking_html = re.sub(
                r'<!-- ─── Meta Pixel.*?</noscript>\n', '', tracking_html, flags=re.DOTALL
            )
        output_html = output_html.replace("<!-- TRACKING_SCRIPTS -->", tracking_html)
        print(f"  Tracking injected: GA4={'yes' if ga4_id else 'no'}, Pixel={'yes' if pixel_id else 'no'}")
    else:
        print("  Tracking: placeholder preserved (no IDs configured or template missing)")

    # Write output
    campaign_dir = OUTPUT_DIR / args.campaign_id
    campaign_dir.mkdir(parents=True, exist_ok=True)
    output_path = campaign_dir / "index.html"
    output_path.write_text(output_html)

    print(f"  Output: {output_path}")

    # Check for remaining unsubstituted variables
    remaining = re.findall(r'\{\{[a-z_]+\}\}', output_html)
    if remaining:
        unique = list(set(remaining))
        print(f"  WARNING: Unsubstituted variables found: {unique}", file=sys.stderr)

    # Update campaign-data.json
    now = datetime.now(timezone.utc).isoformat()
    if "landing_page" not in campaign:
        campaign["landing_page"] = {}
    campaign["landing_page"]["status"] = "generated"
    campaign["landing_page"]["deploy_path"] = f"data/landing-pages/{args.campaign_id}"
    campaign["landing_page"]["generated_at"] = now
    campaign["updated_at"] = now

    data["campaigns"][idx] = campaign
    save_campaign_data(data)

    # Summary
    print(f"\n  Landing page generated successfully.")
    print(f"  Headline: {lp_copy.get('headline', '(empty)')[:60]}")
    print(f"  Benefits: {len(lp_copy.get('benefits', []))} items")
    print(f"  Social proof: {len(lp_copy.get('social_proof', []))} items")
    print(f"  Form fields: {len(form_fields)} fields")
    print(f"  Form action: {form_action}")


if __name__ == "__main__":
    main()
