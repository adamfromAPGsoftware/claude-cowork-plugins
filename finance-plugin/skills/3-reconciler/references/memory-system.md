# Memory System — Reconciler

## Location

`{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Import history, reconciliation state, CRM sync status | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `patterns.md` | Merchant aliases, CRM reference formats, confirmed dupe/non-dupe pairs | When running IA, DD, AR, or MM |
| `chronology.md` | Reconciliation session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next reconciliation session
- Condense to essence — no narrative
- Update index.md immediately after each import or reconciliation pass
- Write-through on critical events:
  - New Amex-to-Airwallex merchant alias confirmed by user
  - Duplicate pair confirmed or rejected by user
  - CRM reference format pattern discovered
  - CRM sync failure requiring retry
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Amex merchant name -> Airwallex merchant name aliases (e.g., "AMZN MKTP US" -> "Amazon")
- Confirmed duplicate transaction pairs (Amex ID <-> Airwallex ID)
- Confirmed non-duplicate pairs (to avoid re-flagging)
- CRM reference number patterns (e.g., invoice format "INV-{number}")
- CRM entity mappings (which merchants map to which CRM contacts)
- Recurring reconciliation patterns (e.g., "Anthropic invoice always arrives 2 days after Airwallex charge")

## What NOT to Remember

- Individual transaction details (that lives in finance-data.json)
- Full CRM invoice/bill records (fetch fresh via MCP each session)
- Anything derivable from the current finance-data.json state
- Amex CSV raw data (processed into finance-data.json)
