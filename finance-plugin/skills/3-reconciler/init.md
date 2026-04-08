---
name: init
description: First-run setup for Reconciler
menu-code: INIT
---

# First-Run Setup for Reconciler

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — import history, reconciliation state, CRM entity mappings
- `patterns.md` — merchant matching patterns, CRM reference formats
- `chronology.md` — reconciliation session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/index.md`

```markdown
# Reconciler — Session Index

## Configuration
- Amex CSV source: finance/amex/
- Dedup window: +/- 3 days
- CRM MCP tools: list_invoices, list_bills, create_document

## Import History
(none yet)

## Reconciliation State
- Reconciled: 0
- Unmatched: 0
- Ambiguous: 0

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Reconciler

## Read Access
- finance/
- finance-plugin/
- _bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/

## Write Access
- finance/
- _bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (finance plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/patterns.md`

```markdown
# Reconciliation Patterns

## Known Merchant Aliases
(Amex merchant name -> Airwallex merchant name mappings discovered during dedup)

## CRM Reference Formats
(invoice/bill reference patterns that help matching — e.g., "INV-{number}" format)

## Confirmed Duplicates
(pairs of transaction IDs confirmed as duplicates by user)

## Confirmed Non-Duplicates
(pairs flagged as potential dupes but confirmed distinct by user)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/chronology.md`

```markdown
# Reconciliation Chronology

(Reconciliation sessions logged here as they accumulate)
```

## Directory Check

Verify `finance/amex/` directory exists. If not, create it and inform the user this is where Amex CSV exports should be placed.

## Finance Data Check

If `finance/finance-data.json` does not exist, warn the user and suggest running Transaction Analyst [PT] first to bootstrap the file.

If it exists, verify it has a `transactions` array and note the current count by `account_source`.

## Ready

Setup complete! Ready to import Amex transactions and start reconciling.
