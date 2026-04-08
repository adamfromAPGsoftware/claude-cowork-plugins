#!/usr/bin/env python3
"""Tests for validate-audit-data-lite.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "validate-audit-data-lite.py"

VALID_AUDIT_DATA = {
    "client_slug": "test-client",
    "company_name": "Test Co",
    "industry_tag": "home-services",
    "discovery_date": "2026-03-19",
    "transcript_source": "meetings/discovery.md",
    "contact": {"name": "Jane Smith", "role": "Owner", "company_size": "10"},
    "business_stages_covered": ["acquisition", "fulfilment"],
    "tools": [],
    "pain_points": [{"description": "manual quoting", "stage": "quoting", "quote": "we do it all by hand", "speaker": "Jane", "confidence": "HIGH"}],
    "waste_items": [
        {
            "activity": "manual invoice entry",
            "hours_per_week": 5,
            "headcount_affected": 2,
            "annual_waste_aud": 26000,
            "waste_type": "manual_data_entry",
            "quote": "takes us about 5 hours every week",
            "confidence": "HIGH",
        }
    ],
    "top_waste_item": {
        "description": "manual invoice entry",
        "annual_waste_aud": 26000,
        "monthly_waste_aud": 2167,
        "quote": "takes us about 5 hours every week",
    },
    "objections": [],
    "positive_signals": [],
    "data_gaps": [],
}


def write_json(data: dict) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


def run(filepath: str, extra: list = None) -> tuple[int, dict]:
    args = [sys.executable, str(SCRIPT), "--file", filepath] + (extra or [])
    result = subprocess.run(args, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {"raw": result.stdout}
    return result.returncode, data


def test_valid_audit_data_passes():
    f = write_json(VALID_AUDIT_DATA)
    code, data = run(f)
    assert code == 0, f"Expected 0, got {code}: {data}"
    assert data["status"] == "pass"
    assert data["summary"]["critical"] == 0
    assert data["summary"]["high"] == 0
    print("PASS: test_valid_audit_data_passes")


def test_missing_required_field():
    bad = {**VALID_AUDIT_DATA}
    del bad["company_name"]
    f = write_json(bad)
    code, data = run(f)
    assert code == 1
    assert data["status"] == "fail"
    issues = [x["location"]["field"] for x in data["findings"] if x["severity"] == "critical"]
    assert "company_name" in issues
    print("PASS: test_missing_required_field")


def test_empty_waste_items():
    bad = {**VALID_AUDIT_DATA, "waste_items": []}
    f = write_json(bad)
    code, data = run(f)
    assert code == 1
    print("PASS: test_empty_waste_items")


def test_invalid_confidence_value():
    bad = {**VALID_AUDIT_DATA, "waste_items": [{**VALID_AUDIT_DATA["waste_items"][0], "confidence": "MAYBE"}]}
    f = write_json(bad)
    code, data = run(f)
    assert code == 1
    issues = [x["issue"] for x in data["findings"]]
    assert any("MAYBE" in i for i in issues)
    print("PASS: test_invalid_confidence_value")


def test_missing_top_waste_item_field():
    bad = {**VALID_AUDIT_DATA, "top_waste_item": {"description": "x", "quote": "y"}}  # missing annual_waste_aud
    f = write_json(bad)
    code, data = run(f)
    assert code == 1
    issues = [x["location"]["field"] for x in data["findings"] if x["severity"] == "critical"]
    assert "top_waste_item.annual_waste_aud" in issues
    print("PASS: test_missing_top_waste_item_field")


def test_no_high_confidence_items_is_high_severity():
    bad = {**VALID_AUDIT_DATA, "waste_items": [{**VALID_AUDIT_DATA["waste_items"][0], "confidence": "MEDIUM"}]}
    f = write_json(bad)
    code, data = run(f)
    assert code == 1
    severities = [x["severity"] for x in data["findings"]]
    assert "high" in severities
    print("PASS: test_no_high_confidence_items_is_high_severity")


def test_file_not_found():
    code, data = run("/nonexistent/path/audit-data-lite.json")
    assert code == 2
    assert data["status"] == "error"
    print("PASS: test_file_not_found")


def test_invalid_json():
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    f.write("not valid json {{{")
    f.close()
    code, data = run(f.name)
    assert code == 2
    assert data["status"] == "error"
    print("PASS: test_invalid_json")


def test_output_has_required_fields():
    f = write_json(VALID_AUDIT_DATA)
    code, data = run(f)
    assert code == 0
    required = ["script", "version", "file", "timestamp", "status", "findings", "summary"]
    for field in required:
        assert field in data, f"Missing: {field}"
    print("PASS: test_output_has_required_fields")


if __name__ == "__main__":
    tests = [
        test_valid_audit_data_passes,
        test_missing_required_field,
        test_empty_waste_items,
        test_invalid_confidence_value,
        test_missing_top_waste_item_field,
        test_no_high_confidence_items_is_high_severity,
        test_file_not_found,
        test_invalid_json,
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
