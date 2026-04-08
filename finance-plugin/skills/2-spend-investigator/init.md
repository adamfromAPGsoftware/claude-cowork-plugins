---
name: init
description: First-run setup for Spend Investigator
menu-code: INIT
---

# First-Run Setup for Spend Investigator

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — investigation history, known baselines, current state
- `patterns.md` — spend patterns, known recurring charges, investigation findings
- `chronology.md` — investigation session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/index.md`

```markdown
# Spend Investigator — Session Index

## Known Baselines
(accumulates as investigations establish normal spend levels per category)

## Active Investigations
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Spend Investigator

## Read Access
- finance/
- finance-plugin/
- _bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/

## Write Access
- finance/finance-data.json (leak_flags[] only)
- _bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (finance plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/patterns.md`

```markdown
# Spend Patterns

## Known Recurring Charges
(expected monthly/annual subscriptions and their amounts)

## Category Baselines
(typical monthly spend per category — establishes what's "normal")

## Investigation Templates
(effective query patterns for common financial questions)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/chronology.md`

```markdown
# Investigation Chronology

(Investigation sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to investigate your financial data.
