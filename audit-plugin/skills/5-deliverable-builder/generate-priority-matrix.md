---
name: generate-priority-matrix
description: Generate priority-matrix.html — interactive bubble chart with clickable modals and 3-horizon roadmap
menu-code: GM
---

# Generate Priority Matrix

## Purpose

Produce `priority-matrix.html` — a standalone interactive deliverable showing where to start implementing. Features an interactive bubble chart (weeks to implement vs annual value), clickable modals with 5-section content, and a 3-horizon implementation roadmap.

**Requires:** `proposed_changes[]` populated with `modal_content` and `value` (run Process Analyst [BR] first).

**For interactive mode:** Run Process Analyst [RI] then [BR] before generating. The interactive chart requires `modal_content`, `value`, and `implementation` on proposed_changes.

## Process

### Step 1: Pre-flight

Client slug is set from activation. Load `clients/{client_slug}/audit/audit-data.json`.

Check `proposed_changes[]`:
- If empty or missing: warn and stop.
  ```
  ✗ proposed_changes[] is empty. Run Process Mapper EI (Extract Improvements) first to populate it.
  ```
- If populated: note count.

Check for analyst enrichment:
- Count changes with `modal_content` and `value` sub-objects.
- If none have enrichment: warn that chart will use fallback SVG mode.
  ```
  ⚠ No analyst-enriched changes found. Priority matrix will use basic SVG scatter plot.
  Run Process Analyst [RI] then [BR] for the interactive bubble chart with modals.
  ```

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output priority-matrix
```

Output is saved to: `clients/{client_slug}/deliverables/priority-matrix.html`

### Step 3: Report

```
PRIORITY MATRIX GENERATED — {company_name}
File: clients/{client_slug}/deliverables/priority-matrix.html

Priority matrix:
  Mode: {INTERACTIVE — weeks vs value with modals | BASIC — payback vs saving SVG}
  {n} items plotted
  {n} with modal content (click-to-expand)
  {n} time_saving (green)  {n} productivity (blue)  {n} both (purple)

Roadmap: {n} items across 3 horizons
  Horizon 1 (QUICK_WIN): {n} items
  Horizon 2 (CORE_BUILD): {n} items
  Horizon 3 (FUTURE): {n} items

Next step: Run [GW] to update the client website with the Transformation Blueprint.
```
