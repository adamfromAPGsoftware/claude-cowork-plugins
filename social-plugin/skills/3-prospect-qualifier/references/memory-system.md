# Memory System — Prospect Qualifier

## Location

`{project-root}/_bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Qualification history, configuration, current state | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Qualification session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next qualification session
- Condense to essence — no narrative
- Update index.md immediately after each qualification run
- Write-through on critical events:
  - New CRM-enabled account added to accounts/
  - High-confidence agency_services prospect identified
  - CRM sync failures (for retry tracking)
  - Classification edge cases (contacts that were hard to classify)
  - ICP or products.md changes that affect classification
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- CRM-enabled account keys and display names
- Qualification run frequency (how often each account is processed)
- Typical contact volume and tier distribution per account
- CRM sync success/failure patterns
- Classification edge cases and how they were resolved
- Contacts that repeatedly fall below confidence threshold

## What NOT to Remember

- Individual message content (that lives in social-data.json)
- Full conversation threads (read fresh each qualification run)
- CRM entity details beyond lead_id (CRM is source of truth for lead data)
- Anything derivable from the current social-data.json state
