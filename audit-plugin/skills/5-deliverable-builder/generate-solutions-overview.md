---
name: generate-solutions-overview
description: "Generate solutions-overview.html — researched automation and integration options for each pain point and optimisation."
menu-code: GS
---

# Generate Solutions Overview

## Purpose

Produce `solutions-overview.html` showing all researched solutions per pain point/optimisation. Grouped by stage, showing tool options with pricing, API availability, integration notes, and confidence. This is the visual output of the analyst's [RI] research work.

**Requires:** `proposed_changes[]` with research sub-objects populated (run Analyst [RI] first).

## Process

### Step 1: Pre-flight Check

Client slug is set from activation. Load `clients/{client_slug}/audit/audit-data.json`.

Check that at least some `proposed_changes` have `research.status` != `"not_started"`.

```
✗ proposed_changes[] has no research data. Run Analyst [RI] first.
```

If the check passes, note the count of changes with research data and how many are still pending.

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output solutions-overview
```

> Note: The `generate_solutions_overview()` function in generate.py needs to be implemented. This capability file is ready for it.

Output is saved to: `clients/{client_slug}/deliverables/solutions-overview.html`

### Step 3: Content Structure

The generated HTML should contain:

- **Header** with branding
- **Summary stats:** total opportunities, tools evaluated, gaps remaining
- **For each stage** (grouped):
  - Stage header
  - For each proposed_change in this stage:
    - Pain point / problem description with source quote
    - Solution options table (from `research.tools_researched[]`):
      - Tool name, category, pricing, API available, integration notes, confidence
      - **Pricing source badge** next to each tool's pricing (green OFFICIAL, blue AGGREGATOR, yellow BLOG, red ESTIMATED) — from `pricing_source_type`
      - **"(estimated)" note** next to annual cost when `pricing_is_estimated` is true
      - **Hidden costs collapsible section** when `hidden_costs[]` is non-empty — shows type, description, annual cost, trigger, and likelihood tag per item
      - **"True annual cost" line** when `total_cost_with_hidden_aud > annual_cost_aud` — dashed red border to distinguish from headline pricing
      - **Custom build option card** when `tools_researched[]` contains an "Custom Build" entry — uses `.so-opt-custom` CSS class with green border, shows scope badge (`scope_level`) and build-weeks badge from `custom_build_option`
    - **Detailed value formulas** in the value bar — shows individual `time_saving.formula` and `productivity_enhancement.formula` breakdowns with labelled rows, not just the summary total. Falls back to `formula_summary` if sub-formulas are not available.
    - Feasibility notes and risks
    - Estimated effort (`weeks_label`) if BR has run
- **Design tokens:** lime `#7DFF00`, Inter font, card-based layout, self-contained HTML

### Step 4: Post-generation

Confirm the file was created. Report the file path and size.

```
SOLUTIONS OVERVIEW GENERATED — {company_name}
File: clients/{client_slug}/deliverables/solutions-overview.html
Size: {size}

Proposed changes with research: {n} of {total}
Tools evaluated: {n}
Stages covered: {list}
Gaps remaining: {n} changes with no research
```

Suggest opening in browser to review.
