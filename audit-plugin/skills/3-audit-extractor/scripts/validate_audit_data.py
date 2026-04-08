#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
validate-audit-data.py — Validates the audit data JSON file.

Usage:
  python3 validate_audit_data.py --file clients/slug/audit/audit-data.json [--verbose]

Exit codes:
  0 — pass (no critical or high severity findings)
  1 — fail (critical or high severity findings present)
  2 — error (file not found, invalid JSON, etc.)
"""

import argparse
import json
import re
import sys
from pathlib import Path


def load_audit_data(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        print(json.dumps({"status": "error", "message": f"File not found: {file_path}"}))
        sys.exit(2)
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON: {e}"}))
        sys.exit(2)


def validate(ssad: dict) -> list[dict]:
    findings = []

    def add(severity, field, message):
        findings.append({"severity": severity, "field": field, "message": message})

    # --- Required top-level fields ---
    required_fields = [
        "client_slug", "company_name", "industry_tag", "audit_status",
        "contact", "blended_hourly_rate_aud", "blended_rate_confidence",
        "processes", "waste_items", "completeness_checklist", "sessions"
    ]
    for field in required_fields:
        if field not in ssad:
            add("critical", field, f"Required field '{field}' is missing")

    # --- Contact block ---
    contact = ssad.get("contact", {})
    if not contact.get("name"):
        add("high", "contact.name", "Contact name is empty")
    if not contact.get("role"):
        add("medium", "contact.role", "Contact role is empty")

    # --- Blended hourly rate ---
    rate = ssad.get("blended_hourly_rate_aud")
    rate_conf = ssad.get("blended_rate_confidence", "")
    if rate is None:
        add("high", "blended_hourly_rate_aud", "Blended hourly rate is null — waste calculations cannot be verified")
    elif not isinstance(rate, (int, float)) or rate <= 0:
        add("high", "blended_hourly_rate_aud", f"Blended hourly rate must be a positive number, got: {rate}")
    if rate_conf not in ("HIGH", "MEDIUM", "LOW"):
        add("medium", "blended_rate_confidence", f"blended_rate_confidence must be HIGH, MEDIUM, or LOW — got: '{rate_conf}'")

    # --- Audit status ---
    valid_statuses = ("discovery", "session-1", "session-2", "session-3", "process_map_complete")
    audit_status = ssad.get("audit_status", "")
    if audit_status not in valid_statuses:
        add("medium", "audit_status", f"audit_status must be one of {valid_statuses}, got: '{audit_status}'")

    # --- Processes ---
    processes = ssad.get("processes", [])
    valid_step_types = ("step", "decision", "pain", "optimisation", "automation")
    valid_confidence = ("HIGH", "MEDIUM", "LOW")

    if not isinstance(processes, list):
        add("critical", "processes", "processes must be an array")
    else:
        seen_stages = set()
        for i, process in enumerate(processes):
            stage = process.get("stage", "")
            if not stage:
                add("critical", f"processes[{i}].stage", "Stage key is empty")
            elif not re.match(r'^[a-z][a-z0-9_]*$', stage):
                add("medium", f"processes[{i}].stage", f"Stage key '{stage}' should be snake_case")
            elif stage in seen_stages:
                add("high", f"processes[{i}].stage", f"Duplicate stage '{stage}'")
            else:
                seen_stages.add(stage)
            if not process.get("name"):
                add("low", f"processes[{i}].name", f"Missing display name for stage '{stage}'")
            steps = process.get("steps", [])
            if not isinstance(steps, list):
                add("high", f"processes[{i}].steps", "steps must be an array")
                continue
            for j, step in enumerate(steps):
                if not step.get("description"):
                    add("high", f"processes[{i}].steps[{j}].description", "Step description is empty")
                step_type = step.get("type", "")
                if step_type not in valid_step_types:
                    add("medium", f"processes[{i}].steps[{j}].type", f"Invalid step type '{step_type}'")
                if step.get("confidence", "") not in valid_confidence:
                    add("medium", f"processes[{i}].steps[{j}].confidence", "confidence must be HIGH, MEDIUM, or LOW")
                if not step.get("source_quote"):
                    add("medium", f"processes[{i}].steps[{j}].source_quote", "No source quote — citation missing")

    # --- Waste items ---
    waste_items = ssad.get("waste_items", [])
    valid_waste_types = ("manual_data_entry", "duplicate_work", "no_followup", "communication_gap", "missing_automation")

    if not isinstance(waste_items, list):
        add("critical", "waste_items", "waste_items must be an array")
    else:
        for i, item in enumerate(waste_items):
            if not item.get("activity"):
                add("high", f"waste_items[{i}].activity", "Waste item activity description is empty")
            conf = item.get("confidence", "")
            if conf not in valid_confidence:
                add("medium", f"waste_items[{i}].confidence", "confidence must be HIGH, MEDIUM, or LOW")
            if conf in ("HIGH", "MEDIUM"):
                if item.get("annual_waste_aud") is None:
                    add("high", f"waste_items[{i}].annual_waste_aud",
                        f"HIGH/MEDIUM confidence waste item '{item.get('activity', 'unknown')}' has no annual_waste_aud — run waste calculator")
                if item.get("hours_per_week") is None:
                    add("medium", f"waste_items[{i}].hours_per_week",
                        f"Waste item '{item.get('activity', 'unknown')}' has no hours_per_week — calculation unverifiable")
            if not item.get("quote"):
                add("medium", f"waste_items[{i}].quote", "No source quote — citation missing")
            waste_type = item.get("waste_type", "")
            if waste_type and waste_type not in valid_waste_types:
                add("low", f"waste_items[{i}].waste_type", f"Invalid waste_type '{waste_type}'")

    # --- Must have at least one HIGH confidence waste item if audit is beyond session-1 ---
    if audit_status not in ("discovery", "session-1"):
        high_waste = [w for w in waste_items if w.get("confidence") == "HIGH"]
        if not high_waste:
            add("high", "waste_items", "No HIGH confidence waste items — audit report cannot proceed without verified waste data")

    # --- Decision nodes ---
    decision_nodes = ssad.get("decision_nodes", [])
    for i, node in enumerate(decision_nodes):
        if not node.get("condition"):
            add("medium", f"decision_nodes[{i}].condition", "Decision node has no condition")
        if not node.get("source_quote"):
            add("low", f"decision_nodes[{i}].source_quote", "Decision node has no source quote")

    # --- Contradictions ---
    contradictions = ssad.get("contradictions", [])
    unresolved = [c for c in contradictions if c.get("status") == "unresolved"]
    if unresolved:
        add("medium", "contradictions",
            f"{len(unresolved)} unresolved contradiction(s) — consultant must review before final deliverables")

    # --- Follow-up questions ---
    follow_ups = ssad.get("follow_up_questions", [])
    high_pending = [q for q in follow_ups if q.get("priority") == "HIGH" and q.get("status") == "pending"]
    if high_pending:
        add("medium", "follow_up_questions",
            f"{len(high_pending)} HIGH priority follow-up question(s) still pending — audit data may be incomplete")

    # --- Proposed changes (analyst enrichment) ---
    proposed_changes = ssad.get("proposed_changes", [])
    valid_sources = ("client", "analyst")
    valid_value_types = ("time_saving", "productivity_enhancement", "both")
    valid_research_statuses = ("not_started", "in_progress", "complete", "needs_review")
    valid_weeks_labels = ("<1 week", "1-2 weeks", "2-4 weeks", "4+ weeks")

    for i, change in enumerate(proposed_changes):
        prefix = f"proposed_changes[{i}]"
        # Optional analyst fields — validate if present
        source = change.get("source")
        if source is not None and source not in valid_sources:
            add("low", f"{prefix}.source", f"source must be 'client' or 'analyst', got: '{source}'")

        value_type = change.get("value_type")
        if value_type is not None and value_type not in valid_value_types:
            add("low", f"{prefix}.value_type", f"value_type must be one of {valid_value_types}, got: '{value_type}'")

        research = change.get("research")
        if research is not None:
            rs = research.get("status", "")
            if rs not in valid_research_statuses:
                add("low", f"{prefix}.research.status", f"research.status must be one of {valid_research_statuses}, got: '{rs}'")

        impl = change.get("implementation")
        if impl is not None:
            we = impl.get("weeks_estimate")
            if we is not None and (not isinstance(we, (int, float)) or we <= 0):
                add("low", f"{prefix}.implementation.weeks_estimate", f"weeks_estimate must be a positive number, got: {we}")
            wl = impl.get("weeks_label")
            if wl is not None and wl not in valid_weeks_labels:
                add("low", f"{prefix}.implementation.weeks_label", f"weeks_label must be one of {valid_weeks_labels}, got: '{wl}'")

        value = change.get("value")
        if value is not None:
            cav = value.get("combined_annual_value_aud")
            if cav is not None and (not isinstance(cav, (int, float)) or cav < 0):
                add("low", f"{prefix}.value.combined_annual_value_aud", f"combined_annual_value_aud must be non-negative, got: {cav}")

    # --- Sessions ---
    sessions = ssad.get("sessions", [])
    unanalyzed = [s for s in sessions if not s.get("analyzed", False)]
    if unanalyzed:
        add("low", "sessions",
            f"{len(unanalyzed)} session(s) recorded but not analyzed: {[s.get('transcript_file') for s in unanalyzed]}")

    # --- Completeness checklist ---
    checklist = ssad.get("completeness_checklist", {})
    process_stages = {p.get("stage") for p in ssad.get("processes", []) if p.get("stage")}
    uncovered_stages = [stage for stage in process_stages
                        if not checklist.get(stage, {}).get("covered", False)]
    if process_stages and len(uncovered_stages) == len(process_stages):
        add("high", "completeness_checklist", "All stages show covered: false — completeness checklist not populated")
    elif uncovered_stages and audit_status not in ("discovery", "session-1"):
        add("medium", "completeness_checklist",
            f"Stages not yet covered: {', '.join(uncovered_stages)}")

    return findings


def main():
    parser = argparse.ArgumentParser(description="Validate an audit data JSON file")
    parser.add_argument("--file", required=True, help="Path to audit-data.json")
    parser.add_argument("--verbose", action="store_true", help="Show all findings")
    args = parser.parse_args()

    ssad = load_audit_data(args.file)
    findings = validate(ssad)

    critical = [f for f in findings if f["severity"] == "critical"]
    high = [f for f in findings if f["severity"] == "high"]
    medium = [f for f in findings if f["severity"] == "medium"]
    low = [f for f in findings if f["severity"] == "low"]

    status = "pass" if not critical and not high else "fail"

    result = {
        "status": status,
        "file": args.file,
        "client_slug": ssad.get("client_slug", "unknown"),
        "summary": {
            "critical": len(critical),
            "high": len(high),
            "medium": len(medium),
            "low": len(low),
            "total": len(findings)
        }
    }

    if args.verbose or status == "fail":
        result["findings"] = findings if args.verbose else critical + high

    print(json.dumps(result, indent=2))
    sys.exit(0 if status == "pass" else 1)


if __name__ == "__main__":
    main()
