#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
audit-data-lite Structure Validator — {YOUR_AUDIT_SERVICE}

Validates that an audit-data-lite JSON file has required fields, valid confidence
scores, and a quantified top_waste_item before close page generation proceeds.

Usage:
    python3 validate-audit-data-lite.py --file clients/slug/audit/audit-data-lite.json
    python3 validate-audit-data-lite.py --file audit-data-lite.json --verbose
    python3 validate-audit-data-lite.py --help

Output: JSON to stdout. Diagnostics to stderr (with --verbose).
Exit codes: 0=pass, 1=fail (critical/high issues found), 2=error (file problem)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "client_slug",
    "company_name",
    "industry_tag",
    "contact",
    "pain_points",
    "waste_items",
    "top_waste_item",
]
REQUIRED_CONTACT_FIELDS = ["name"]
REQUIRED_WASTE_FIELDS = ["activity", "confidence"]
REQUIRED_TOP_WASTE_FIELDS = ["description", "annual_waste_aud", "quote"]
VALID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


def validate(data: dict) -> list:
    findings = []

    # Required top-level fields
    for field in REQUIRED_TOP_LEVEL:
        if field not in data or data[field] is None:
            findings.append({
                "severity": "critical",
                "category": "structure",
                "location": {"field": field},
                "issue": f"Required field '{field}' is missing or null",
                "fix": f"Add '{field}' to audit-data-lite",
            })

    # Contact name
    contact = data.get("contact")
    if isinstance(contact, dict):
        for field in REQUIRED_CONTACT_FIELDS:
            if not contact.get(field):
                findings.append({
                    "severity": "high",
                    "category": "structure",
                    "location": {"field": f"contact.{field}"},
                    "issue": f"Contact field '{field}' is missing",
                    "fix": "Add client contact name from transcript",
                })

    # Waste items
    waste_items = data.get("waste_items", [])
    if not waste_items:
        findings.append({
            "severity": "high",
            "category": "structure",
            "location": {"field": "waste_items"},
            "issue": "No waste items found — close page requires at least one quantified waste item",
            "fix": "Extract at least one waste item with hours_per_week from transcript analysis",
        })
    else:
        for i, item in enumerate(waste_items):
            # Required fields
            for field in REQUIRED_WASTE_FIELDS:
                if not item.get(field):
                    findings.append({
                        "severity": "high",
                        "category": "structure",
                        "location": {"field": f"waste_items[{i}].{field}"},
                        "issue": f"Waste item {i} missing required field '{field}'",
                        "fix": f"Add '{field}' to waste_items[{i}]",
                    })
            # Confidence validity
            conf = item.get("confidence", "")
            if conf not in VALID_CONFIDENCE:
                findings.append({
                    "severity": "high",
                    "category": "structure",
                    "location": {"field": f"waste_items[{i}].confidence"},
                    "issue": f"Waste item {i} has invalid confidence '{conf}'",
                    "fix": "Set confidence to HIGH, MEDIUM, or LOW",
                })
            # Warn on items missing annual_waste_aud
            if item.get("confidence") in ("HIGH", "MEDIUM") and not item.get("annual_waste_aud"):
                findings.append({
                    "severity": "medium",
                    "category": "completeness",
                    "location": {"field": f"waste_items[{i}].annual_waste_aud"},
                    "issue": f"Waste item {i} has no annual_waste_aud — run waste-calculator.py",
                    "fix": "python3 scripts/waste-calculator.py --hours-per-week X --headcount Y",
                })

        # At least one HIGH confidence item
        high_items = [w for w in waste_items if w.get("confidence") == "HIGH"]
        if not high_items:
            findings.append({
                "severity": "high",
                "category": "consistency",
                "location": {"field": "waste_items"},
                "issue": "No HIGH confidence waste items — close page should only feature verified figures",
                "fix": "Confirm waste figures with client before generating close assets, or upgrade confidence if explicitly stated",
            })

    # top_waste_item
    top = data.get("top_waste_item")
    if isinstance(top, dict):
        for field in REQUIRED_TOP_WASTE_FIELDS:
            if not top.get(field):
                findings.append({
                    "severity": "critical",
                    "category": "structure",
                    "location": {"field": f"top_waste_item.{field}"},
                    "issue": f"top_waste_item.{field} is missing — this drives the close page hero section",
                    "fix": f"Set top_waste_item.{field} from the highest-confidence waste item",
                })

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Validate audit-data-lite JSON structure before close page generation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 validate-audit-data-lite.py --file clients/mark-one-agency/audit/audit-data-lite.json
  python3 validate-audit-data-lite.py --file audit-data-lite.json --verbose

Exit codes: 0=pass, 1=fail (critical/high issues), 2=error (file not found/invalid JSON)
        """,
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the audit-data-lite JSON file to validate",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print diagnostics to stderr",
    )

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(json.dumps({
            "script": "validate-audit-data-lite",
            "version": "1.0.0",
            "status": "error",
            "error": f"File not found: {args.file}",
        }))
        sys.exit(2)

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "script": "validate-audit-data-lite",
            "version": "1.0.0",
            "status": "error",
            "error": f"Invalid JSON: {e}",
        }))
        sys.exit(2)

    findings = validate(data)

    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f.get("severity", "info")
        counts[sev] = counts.get(sev, 0) + 1

    if counts["critical"] + counts["high"] > 0:
        status = "fail"
    elif counts["medium"] > 0:
        status = "warning"
    else:
        status = "pass"

    output = {
        "script": "validate-audit-data-lite",
        "version": "1.0.0",
        "file": args.file,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": status,
        "findings": findings,
        "summary": {
            "total": len(findings),
            **counts,
        },
    }

    if args.verbose:
        print(f"Validated: {args.file} → {status.upper()}", file=sys.stderr)
        for f in findings:
            print(f"  [{f['severity'].upper()}] {f['issue']}", file=sys.stderr)

    print(json.dumps(output, indent=2))
    sys.exit(0 if status in ("pass", "warning") else 1)


if __name__ == "__main__":
    main()
