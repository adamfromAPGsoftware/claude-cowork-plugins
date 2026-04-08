---
name: init
description: First-run setup for Receipt Manager
menu-code: INIT
---

# First-Run Setup for Receipt Manager

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — session state, receipt processing history, coverage stats
- `patterns.md` — merchant name normalization patterns for receipt matching
- `chronology.md` — receipt processing session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/index.md`

```markdown
# Receipt Manager — Session Index

## Configuration
- Receipts directory: finance/receipts/
- Naming format: {YYYY-MM-DD}-{merchant-slug}.{ext}
- Match tolerance: amount ± $0.05, date ± 3 days

## Processing History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Receipt Manager

## Read Access
- finance/
- finance-plugin/
- _bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/

## Write Access
- finance/
- finance/receipts/
- _bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (finance plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/patterns.md`

```markdown
# Receipt Matching Patterns

## Merchant Name Variations
(accumulates as receipts are processed — receipt merchant text → normalized merchant name)

## Common GST Patterns
(merchants known to include/exclude GST on receipts)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/chronology.md`

```markdown
# Receipt Processing Chronology

(Processing sessions logged here as they accumulate)
```

## Receipts Directory

If `finance/receipts/` does not exist, create it.

## Ready

Setup complete! Share a receipt photo to get started.
