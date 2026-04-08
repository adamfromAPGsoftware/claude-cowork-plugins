---
name: generate-transformation-blueprint
description: Generate transformation-blueprint.html — side-by-side current vs future state process map with phase timeline and change details
menu-code: GT
---

# Generate Transformation Blueprint

## Purpose

Produce `transformation-blueprint.html` — a standalone interactive deliverable showing the client's current operations side-by-side with their optimised future state after implementing the recommended changes.

**Requires:** `transformation_blueprint` top-level object in audit data (run Process Analyst [TB] first).

## Process

### Step 1: Pre-flight

Client slug is set from activation. Load `clients/{client_slug}/audit/audit-data.json`.

Check `transformation_blueprint`:
- If missing: warn and stop.
  ```
  ✗ transformation_blueprint not found. Run Process Analyst [TB] first to build the blueprint.
  ```
- If present: note phase count and change count.

Check `proposed_changes[]` for `future_step_type` fields:
- Count changes with future-state data.
- If none have it: warn that blueprint will show current state only.

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output transformation-blueprint
```

Output is saved to: `clients/{client_slug}/deliverables/transformation-blueprint.html`

### Step 3: Report

```
TRANSFORMATION BLUEPRINT GENERATED — {company_name}
File: clients/{client_slug}/deliverables/transformation-blueprint.html

Blueprint:
  Phases: {n} ({phase labels})
  Changes visualised: {n}
  Steps: {current} current → {future} future
  Total annual value: ${total}/yr

Next step: Run [GW] to update the client website with the Transformation Blueprint summary.
```
