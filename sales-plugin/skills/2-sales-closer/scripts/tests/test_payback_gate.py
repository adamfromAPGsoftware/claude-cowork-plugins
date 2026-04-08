#!/usr/bin/env python3
"""Tests for payback-gate.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "payback-gate.py"


def run(args: list) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {"raw": result.stdout}
    return result.returncode, data


def test_quick_win_via_tier():
    # $24,000/yr saving ÷ $3,800 (standard) = 1.9 months → QUICK_WIN
    code, data = run(["--annual-saving", "24000", "--tier", "standard"])
    assert code == 0
    assert data["status"] == "pass"
    assert data["tag"] == "QUICK_WIN"
    assert data["payback_months"] == 1.9
    print("PASS: test_quick_win_via_tier")


def test_core_build():
    # $6,000/yr saving ÷ $6,500 (complex) = 13 months → CORE_BUILD
    code, data = run(["--annual-saving", "6000", "--tier", "complex"])
    assert code == 0
    assert data["tag"] == "CORE_BUILD"
    print("PASS: test_core_build")


def test_future():
    # $5,000/yr saving ÷ $15,000 (sprint) = 36 months → FUTURE
    code, data = run(["--annual-saving", "5000", "--tier", "sprint"])
    assert code == 0
    assert data["tag"] == "FUTURE"
    print("PASS: test_future")


def test_custom_build_cost():
    # $12,000/yr ÷ $1,800 = 1.8 months → QUICK_WIN
    code, data = run(["--annual-saving", "12000", "--build-cost", "1800"])
    assert code == 0
    assert data["tag"] == "QUICK_WIN"
    assert data["tier_used"] == "custom"
    print("PASS: test_custom_build_cost")


def test_boundary_exactly_12_months():
    # $3,800/yr ÷ $3,800 = 12 months exactly → CORE_BUILD (not QUICK_WIN, threshold is <12)
    code, data = run(["--annual-saving", "3800", "--tier", "standard"])
    assert code == 0
    assert data["tag"] == "CORE_BUILD"
    print("PASS: test_boundary_exactly_12_months")


def test_boundary_exactly_24_months():
    # $1,900/yr ÷ $3,800 = 24 months → CORE_BUILD (threshold is <=24)
    code, data = run(["--annual-saving", "1900", "--tier", "standard"])
    assert code == 0
    assert data["tag"] == "CORE_BUILD"
    print("PASS: test_boundary_exactly_24_months")


def test_roi_12mo_calculation():
    code, data = run(["--annual-saving", "24000", "--tier", "standard"])
    assert code == 0
    assert data["roi_12mo_aud"] == 24000 - 3800
    print("PASS: test_roi_12mo_calculation")


def test_monthly_saving():
    code, data = run(["--annual-saving", "12000", "--tier", "micro"])
    assert code == 0
    assert data["monthly_saving_aud"] == 1000.0
    print("PASS: test_monthly_saving")


def test_invalid_zero_saving():
    code, data = run(["--annual-saving", "0", "--tier", "standard"])
    assert code == 1
    assert data["status"] == "fail"
    print("PASS: test_invalid_zero_saving")


def test_output_has_required_fields():
    code, data = run(["--annual-saving", "24000", "--tier", "standard"])
    assert code == 0
    required = ["script", "version", "timestamp", "status", "tag", "payback_months", "formula"]
    for field in required:
        assert field in data, f"Missing field: {field}"
    print("PASS: test_output_has_required_fields")


if __name__ == "__main__":
    tests = [
        test_quick_win_via_tier,
        test_core_build,
        test_future,
        test_custom_build_cost,
        test_boundary_exactly_12_months,
        test_boundary_exactly_24_months,
        test_roi_12mo_calculation,
        test_monthly_saving,
        test_invalid_zero_saving,
        test_output_has_required_fields,
    ]
    failed = []
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"FAIL: {t.__name__} — {e}")
            failed.append(t.__name__)

    if failed:
        print(f"\n{len(failed)} test(s) failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"\nAll {len(tests)} tests passed.")
        sys.exit(0)
