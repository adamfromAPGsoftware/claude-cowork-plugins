#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Payback Threshold Gate — {YOUR_AUDIT_SERVICE}

Tags opportunities as QUICK_WIN, CORE_BUILD, or FUTURE based on payback period.
Formula: (build_cost / annual_saving) × 12 = payback months

Tier Prices (AUD):
  micro:    $1,800  (5–10 hrs dev)
  standard: $3,800  (12–25 hrs dev)
  complex:  $6,500  (28–45 hrs dev)
  sprint:   $15,000

Thresholds:
  QUICK_WIN:  payback < 12 months
  CORE_BUILD: payback 12–24 months
  FUTURE:     payback > 24 months

Usage:
    python3 payback-gate.py --annual-saving 24000 --tier standard
    python3 payback-gate.py --annual-saving 52000 --tier complex --activity "quoting automation"
    python3 payback-gate.py --annual-saving 12000 --build-cost 1800
    python3 payback-gate.py --help

Output: JSON to stdout. Diagnostics to stderr (with --verbose).
Exit codes: 0=pass, 1=fail (invalid inputs), 2=error
"""

import argparse
import json
import sys
from datetime import datetime

TIER_PRICES = {
    "micro": 1800,
    "standard": 3800,
    "complex": 6500,
    "sprint": 15000,
}

QUICK_WIN_MONTHS = 12
CORE_BUILD_MONTHS = 24


def tag_opportunity(annual_saving: float, build_cost: float) -> dict:
    if annual_saving <= 0:
        return {
            "tag": "UNQUALIFIED",
            "reason": "annual_saving must be greater than 0",
            "payback_months": None,
        }

    payback_months = (build_cost / annual_saving) * 12

    if payback_months < QUICK_WIN_MONTHS:
        tag = "QUICK_WIN"
    elif payback_months <= CORE_BUILD_MONTHS:
        tag = "CORE_BUILD"
    else:
        tag = "FUTURE"

    return {
        "tag": tag,
        "payback_months": round(payback_months, 1),
        "annual_saving_aud": round(annual_saving, 2),
        "monthly_saving_aud": round(annual_saving / 12, 2),
        "build_cost_aud": round(build_cost, 2),
        "roi_12mo_aud": round(annual_saving - build_cost, 2),
        "formula": (
            f"${build_cost:,.0f} build ÷ ${annual_saving:,.0f}/yr × 12 "
            f"= {payback_months:.1f} months → {tag}"
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Tag opportunities as QUICK_WIN, CORE_BUILD, or FUTURE based on payback period.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 payback-gate.py --annual-saving 24000 --tier standard
  python3 payback-gate.py --annual-saving 52000 --tier complex --activity "quoting automation"
  python3 payback-gate.py --annual-saving 12000 --build-cost 1800

Tiers:  micro=$1,800 | standard=$3,800 | complex=$6,500 | sprint=$15,000 AUD
Tags:   QUICK_WIN (<12mo) | CORE_BUILD (12-24mo) | FUTURE (>24mo)
        """,
    )
    parser.add_argument(
        "--annual-saving",
        type=float,
        required=True,
        help="Estimated annual saving in AUD",
    )

    build_group = parser.add_mutually_exclusive_group(required=True)
    build_group.add_argument(
        "--tier",
        choices=list(TIER_PRICES.keys()),
        help="pricing tier (auto-resolves build cost)",
    )
    build_group.add_argument(
        "--build-cost",
        type=float,
        help="Custom build cost in AUD",
    )

    parser.add_argument(
        "--activity",
        type=str,
        default="",
        help="Description of the opportunity (included in output for labelling)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print diagnostics to stderr",
    )

    args = parser.parse_args()

    if args.annual_saving <= 0:
        output = {
            "script": "payback-gate",
            "version": "1.0.0",
            "status": "fail",
            "errors": ["--annual-saving must be greater than 0"],
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)

    build_cost = TIER_PRICES[args.tier] if args.tier else args.build_cost

    if build_cost <= 0:
        output = {
            "script": "payback-gate",
            "version": "1.0.0",
            "status": "fail",
            "errors": ["--build-cost must be greater than 0"],
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)

    result = tag_opportunity(args.annual_saving, build_cost)

    output = {
        "script": "payback-gate",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "pass",
        "activity": args.activity,
        "tier_used": args.tier or "custom",
        **result,
    }

    if args.verbose:
        print(f"Result: {result['formula']}", file=sys.stderr)

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
