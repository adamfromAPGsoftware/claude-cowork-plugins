#!/usr/bin/env python3
"""Tests for waste-calculator.py"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "waste-calculator.py"


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


def test_basic_calculation():
    code, data = run(["--hours-per-week", "5", "--headcount", "3"])
    assert code == 0, f"Expected exit 0, got {code}"
    assert data["status"] == "pass"
    assert data["annual_waste_aud"] == 39000.0  # 5 * 3 * 50 * 52
    assert data["monthly_waste_aud"] == 3250.0
    assert data["weekly_waste_aud"] == 750.0
    print("PASS: test_basic_calculation")


def test_custom_hourly_rate():
    code, data = run(["--hours-per-week", "10", "--headcount", "2", "--hourly-rate", "65"])
    assert code == 0
    assert data["annual_waste_aud"] == 67600.0  # 10 * 2 * 65 * 52
    print("PASS: test_custom_hourly_rate")


def test_activity_label():
    code, data = run(["--hours-per-week", "1", "--headcount", "1", "--activity", "test task"])
    assert code == 0
    assert data["activity"] == "test task"
    print("PASS: test_activity_label")


def test_formula_string():
    code, data = run(["--hours-per-week", "5", "--headcount", "3"])
    assert code == 0
    assert "5" in data["formula"]
    assert "3 staff" in data["formula"]
    assert "$50" in data["formula"]
    print("PASS: test_formula_string")


def test_invalid_zero_hours():
    code, data = run(["--hours-per-week", "0", "--headcount", "3"])
    assert code == 1
    assert data["status"] == "fail"
    print("PASS: test_invalid_zero_hours")


def test_invalid_negative_headcount():
    code, data = run(["--hours-per-week", "5", "--headcount", "-1"])
    assert code == 1
    assert data["status"] == "fail"
    print("PASS: test_invalid_negative_headcount")


def test_output_has_required_fields():
    code, data = run(["--hours-per-week", "5", "--headcount", "3"])
    assert code == 0
    required = ["script", "version", "timestamp", "status", "annual_waste_aud", "monthly_waste_aud", "formula"]
    for field in required:
        assert field in data, f"Missing field: {field}"
    print("PASS: test_output_has_required_fields")


if __name__ == "__main__":
    tests = [
        test_basic_calculation,
        test_custom_hourly_rate,
        test_activity_label,
        test_formula_string,
        test_invalid_zero_hours,
        test_invalid_negative_headcount,
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
