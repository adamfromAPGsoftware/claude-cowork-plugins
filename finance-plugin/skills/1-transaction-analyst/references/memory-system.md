# Memory System — Transaction Analyst

## Location

`{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Sync history, configuration, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `patterns.md` | Merchant categorization patterns, normalization rules | When categorizing (CT) |
| `chronology.md` | Sync session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next sync/categorization session
- Condense to essence — no narrative
- Update index.md immediately after each sync
- Write-through on critical events:
  - New merchant → category mapping confirmed by user
  - Merchant normalization rule discovered (e.g., "STRIPE* ANTHROPIC" → "Anthropic")
  - Unusual sync result (errors, rate limits, data gaps)
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Merchant name → category mappings (e.g., "AWS" → hosting, "ANTHROPIC" → software)
- Merchant normalization rules (raw name → clean name)
- MCC codes that reliably map to categories
- Sync patterns (typical transaction volume per day/week)
- Any recurring issues with Airwallex API responses

## What NOT to Remember

- Individual transaction details (that lives in finance-data.json)
- Balance amounts (that lives in balances.json)
- Anything derivable from the current finance-data.json state
