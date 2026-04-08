---
name: generate-report
description: Generate audit-report.html — full audit report with ROI model, priority matrix, and 3-horizon roadmap
menu-code: GR
---

# Generate Audit Report

## Purpose

Produce `audit-report.html` — the full audit report. Contains: executive summary, ROI model (waste items with calculations), priority matrix (QUICK_WIN / CORE_BUILD / FUTURE tagged by payback threshold), and a 3-horizon roadmap. All figures trace to audit data which traces to transcripts.

## Readiness Requirements

The audit report is most useful after at least 2 sessions with HIGH confidence waste items. Check before generating:

- `waste_items[]` has at least 1 HIGH confidence item with `annual_waste_aud` calculated
- `roi_items[]` has items with `payback_tag` set (run payback-gate.py if needed)
- If neither requirement is met, warn and ask whether to proceed with partial data

### Run Payback Gate if roi_items Empty

If `roi_items[]` is empty but `waste_items[]` has HIGH confidence items, run the payback gate for each:

```bash
python3 .claude/skills/bmad-apg-agent-close/scripts/payback-gate.py \
  --annual-saving {annual_waste_aud} \
  --tier standard \
  --activity "{activity}"
```

Update audit data `roi_items[]` with the results before generating.

## Process

### Step 1: Pre-flight

```bash
python3 .claude/skills/bmad-apg-agent-analyst/scripts/validate_audit_data.py \
  --file clients/{client_slug}/audit/audit-data.json
```

Note any unresolved contradictions or pending HIGH priority follow-up questions — these appear as callouts in the report.

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output audit-report
```

Output: `clients/{client_slug}/deliverables/audit-report.html`

### Step 3: Report

```
AUDIT REPORT GENERATED — {company_name}
File: clients/{client_slug}/deliverables/audit-report.html

Sections:
  ✓ Executive Summary
  ✓ ROI Model — {n} waste items, total annual waste: ${total_annual_waste_aud}
  ✓ Priority Matrix
    QUICK_WIN:  {n} items (payback < 12 months)
    CORE_BUILD: {n} items (12–24 months)
    FUTURE:     {n} items (>24 months)
  ✓ 3-Horizon Roadmap
  {✓/✗} Stage Findings — {n} of 5 stages with data

⚠ Warnings (if any):
  • {n} unresolved contradictions noted in report
  • {n} HIGH priority follow-up questions flagged as data gaps
  • Onboarding findings not available — stage not yet covered
```
