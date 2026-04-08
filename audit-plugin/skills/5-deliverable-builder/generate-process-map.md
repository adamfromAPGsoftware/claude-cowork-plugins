---
name: generate-process-map
description: Generate process-map.html — HTML/CSS zone-based current-state process map with citation dropdowns and Fathom deep-links
menu-code: GP
---

# Generate Process Map

## Purpose

Produce `process-map.html` — a single-file, self-contained HTML/CSS process map showing the current-state business operations across all 5 stages. Every box is citation-locked to a transcript quote. A waste heatmap toggle shows relative waste intensity per step. No Mermaid — pure HTML/CSS zone-based layout.

## Process

### Step 1: Pre-flight Check

Client slug is set from activation. Load `clients/{client_slug}/audit/audit-data.json`.

Run:
```bash
python3 .claude/skills/bmad-apg-agent-analyst/scripts/validate_audit_data.py \
  --file clients/{client_slug}/audit/audit-data.json
```

If the validation fails with critical/high findings, show the findings and ask: "The audit data has issues that may affect the process map. Proceed anyway, or fix these first?"

Check which stages have data in `processes[]`. Note any stages with no steps — these zones will render as "Pending — data collection in progress."

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output process-map
```

Output is saved to: `clients/{client_slug}/deliverables/process-map.html`

### Step 3: Report

```
PROCESS MAP GENERATED — {company_name}
File: clients/{client_slug}/deliverables/process-map.html

Stages rendered:
  ✓ Acquisition   — {n} steps ({n} HIGH, {n} MEDIUM, {n} LOW confidence)
  ✓ Quoting       — {n} steps
  ✗ Onboarding    — No data (zone renders as "Pending")
  ✓ Fulfilment    — {n} steps
  ✗ Retention     — No data (zone renders as "Pending")

Step types:
  {n} standard steps
  {n} parallel groups (horizontal chip rows — sources/channels/tools)
  {n} decision nodes (diamond boxes)
  {n} pain points (red highlight)
  {n} opportunities (green highlight)

Waste heatmap: {enabled if any waste_items have hours_per_week}
Citations: {n} of {total} steps have source quotes
Fathom links: {n} of {total} steps have meeting_references with timestamp deep-links (always visible at 70% opacity, full on hover)
Tool recording links: {n} tools have meeting_references — ▶ badge shown on tool tag in People Bar
Tool tags: {n} of {total} steps have tool_ids mapped
Data flow arrows: {n} of {total} handoffs have labeled mechanisms ({n} manual, {n} automated, {n} unknown)
Pain points summary: {n} themes identified across {total} pain points

⚠ Warnings (if any):
  • {n} LOW confidence steps rendered with dashed border
  • Onboarding and Retention zones are empty — run more sessions
  • {n} steps imply tool usage but have empty tool_ids — run CC to identify
  • {n} handoffs have mechanism: "unknown" — probe in next session
```

Open the file in a browser to review. Ask: "Ready to generate the audit report [GR] or client website [GW]?"
