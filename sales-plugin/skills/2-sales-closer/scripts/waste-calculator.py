#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Waste Calculator — {YOUR_AUDIT_SERVICE}

Calculates annual operational waste from manual process inputs.
Formula: hours_per_week × headcount × hourly_rate × 52

Usage:
    python3 waste-calculator.py --hours-per-week 5 --headcount 3
    python3 waste-calculator.py --hours-per-week 5 --headcount 3 --hourly-rate 65
    python3 waste-calculator.py --hours-per-week 10 --headcount 2 --activity "manual invoice entry"
    python3 waste-calculator.py --help

Output: JSON to stdout. Diagnostics to stderr (with --verbose).
Exit codes: 0=pass, 1=fail (invalid inputs), 2=error
"""

import argparse
import json
import sys
from datetime import datetime

DEFAULT_HOURLY_RATE = 50.0
WEEKS_PER_YEAR = 52


def calculate_waste(hours_per_week: float, headcount: int, hourly_rate: float) -> dict:
    weekly_cost = hours_per_week * headcount * hourly_rate
    annual_cost = weekly_cost * WEEKS_PER_YEAR
    monthly_cost = annual_cost / 12

    return {
        "hours_per_week": hours_per_week,
        "headcount": headcount,
        "hourly_rate_aud": hourly_rate,
        "weekly_waste_aud": round(weekly_cost, 2),
        "monthly_waste_aud": round(monthly_cost, 2),
        "annual_waste_aud": round(annual_cost, 2),
        "formula": f"{hours_per_week} hrs/wk × {headcount} staff × ${hourly_rate}/hr × {WEEKS_PER_YEAR} weeks",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate annual operational waste from manual process inputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 waste-calculator.py --hours-per-week 5 --headcount 3
  python3 waste-calculator.py --hours-per-week 10 --headcount 2 --hourly-rate 65
  python3 waste-calculator.py --hours-per-week 5 --headcount 3 --activity "manual invoice entry"

Output JSON fields:
  annual_waste_aud   Total annual waste in AUD
  monthly_waste_aud  Monthly equivalent
  formula            Human-readable calculation string
        """,
    )
    parser.add_argument(
        "--hours-per-week",
        type=float,
        required=True,
        help="Hours per week spent on this manual activity",
    )
    parser.add_argument(
        "--headcount",
        type=int,
        required=True,
        help="Number of staff performing this activity",
    )
    parser.add_argument(
        "--hourly-rate",
        type=float,
        default=DEFAULT_HOURLY_RATE,
        help=f"Blended hourly rate in AUD (default: ${DEFAULT_HOURLY_RATE})",
    )
    parser.add_argument(
        "--activity",
        type=str,
        default="",
        help="Description of the manual activity (included in output for labelling)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print diagnostics to stderr",
    )

    args = parser.parse_args()

    # Validate inputs
    errors = []
    if args.hours_per_week <= 0:
        errors.append("--hours-per-week must be greater than 0")
    if args.headcount <= 0:
        errors.append("--headcount must be greater than 0")
    if args.hourly_rate <= 0:
        errors.append("--hourly-rate must be greater than 0")

    if errors:
        output = {
            "script": "waste-calculator",
            "version": "1.0.0",
            "status": "fail",
            "errors": errors,
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)

    result = calculate_waste(args.hours_per_week, args.headcount, args.hourly_rate)

    output = {
        "script": "waste-calculator",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "pass",
        "activity": args.activity,
        **result,
    }

    if args.verbose:
        print(f"Calculating: {result['formula']}", file=sys.stderr)
        print(f"Annual waste: ${result['annual_waste_aud']:,.2f} AUD", file=sys.stderr)

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
