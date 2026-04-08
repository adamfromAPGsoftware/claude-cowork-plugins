# Memory System — Spend Investigator

## Location

`{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Investigation history, known baselines, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `patterns.md` | Known recurring charges, category baselines, spend patterns | When investigating (SS, LD, TA) |
| `chronology.md` | Investigation session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next investigation
- Condense to essence — no narrative
- Update index.md immediately after each investigation session
- Write-through on critical events:
  - New recurring charge identified (merchant + amount + frequency)
  - Category baseline established or significantly changed
  - Leak confirmed or new pattern discovered
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Known recurring charges (merchant, expected amount, frequency)
- Category baselines (typical monthly spend per category)
- Dismissed leak flags (to avoid re-flagging)
- Effective query patterns for common financial questions
- Notable one-time events that might confuse future trend analysis

## What NOT to Remember

- Individual transaction details (that lives in finance-data.json)
- Leak flags (those live in finance-data.json leak_flags[])
- Anything derivable from the current finance-data.json state
