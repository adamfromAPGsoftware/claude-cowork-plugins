---
name: init
description: First-run setup for Transaction Analyst
menu-code: INIT
---

# First-Run Setup for Transaction Analyst

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — sync history, configuration, current state
- `patterns.md` — merchant categorization patterns learned over time
- `chronology.md` — sync session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/index.md`

```markdown
# Transaction Analyst — Session Index

## Configuration
- Airwallex environment: (check AIRWALLEX_ENVIRONMENT in .env)
- Default date range: last 30 days

## Sync History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Transaction Analyst

## Read Access
- finance/
- finance-plugin/
- _bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/
- .env (for API credentials)

## Write Access
- finance/
- _bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (finance plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/patterns.md`

```markdown
# Merchant Categorization Patterns

## Known Merchants
(accumulates as transactions are categorized — merchant name → category_id mappings)

## MCC Code Mappings
(MCC codes that reliably map to specific categories)

## Normalization Rules
(merchant name cleanup rules: "STRIPE* ANTHROPIC" → "Anthropic", etc.)
```

### `{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/chronology.md`

```markdown
# Sync Chronology

(Sync sessions logged here as they accumulate)
```

## Environment Check

Verify these are set in `.env`:
- `AIRWALLEX_CLIENT_ID` — Airwallex client ID
- `AIRWALLEX_API_KEY` — Airwallex API key (read-only permissions)
- `AIRWALLEX_ENVIRONMENT` — `demo` or `prod`

If any are missing, prompt the user to add them.

## Finance Data Bootstrap

If `finance/finance-data.json` does not exist, create it with the scaffold from `references/finance-data-schema.md` — empty transactions array, default categories, null balances.

## Ready

Setup complete! Ready to pull your first transactions.
