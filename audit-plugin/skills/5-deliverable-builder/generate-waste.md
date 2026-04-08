---
name: generate-waste
description: "Generate waste.html — quantified waste breakdown with hours and annual costs per item."
menu-code: GV
---

# Generate Waste

## Purpose

Produce `waste.html` from audit-data.json using `generate.py --output waste`. Shows waste_items with hours/week, annual cost, and confidence levels.

## Process

### Step 1: Pre-flight Check

Client slug is set from activation. Load `clients/{client_slug}/audit/audit-data.json`.

Check that `waste_items[]` is non-empty with at least one item that has `annual_waste_aud` calculated.

```
✗ waste_items[] is empty or no items have annual_waste_aud calculated. Run more mapping sessions to identify waste.
```

If the check passes, note the count of waste items and total annual waste.

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output waste
```

Output is saved to: `clients/{client_slug}/deliverables/waste.html`

### Step 3: Post-generation

Confirm the file was created. Report the file path and size.

```
WASTE GENERATED — {company_name}
File: clients/{client_slug}/deliverables/waste.html
Size: {size}

Waste items: {n}
Total annual waste: ${total_annual_waste_aud}
Confidence breakdown: {n} HIGH, {n} MEDIUM, {n} LOW
```

Suggest opening in browser to review.
