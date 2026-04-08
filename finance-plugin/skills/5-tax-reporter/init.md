---
name: init
description: First-run setup for Tax & Compliance Reporter
menu-code: INIT
---

# First-Run Setup for Tax & Compliance Reporter

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — session state, reports generated, coverage stats
- `patterns.md` — tax classification patterns and R&D tagging rules
- `chronology.md` — report generation timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/index.md`

```markdown
# Tax & Compliance Reporter — Session Index

## Configuration
- Tax output directory: finance/tax/
- Australian FY: Jul 1 → Jun 30
- BAS quarters: Q1 Jul-Sep, Q2 Oct-Dec, Q3 Jan-Mar, Q4 Apr-Jun
- GST rate: 10% (1/11th of inclusive amount)

## Reports Generated
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Tax & Compliance Reporter

## Read Access
- finance/
- finance-plugin/
- _bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/

## Write Access
- finance/tax/
- _bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (finance plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/patterns.md`

```markdown
# Tax Classification Patterns

## R&D Eligible Categories
- software (development tools, APIs)
- hosting (cloud infrastructure for R&D projects)
- contractors (development and research contractors)

## GST-Free Categories
(categories known to be GST-free: e.g., international services, certain financial services)

## Depreciation Thresholds
- Items > $300 in office or equipment categories may be depreciation-eligible
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/chronology.md`

```markdown
# Report Generation Chronology

(Report sessions logged here as they accumulate)
```

## Tax Directory

If `finance/tax/` does not exist, create it.

## Ready

Setup complete! Ready to generate your first tax report.
