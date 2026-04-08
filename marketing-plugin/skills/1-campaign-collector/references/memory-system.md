# Memory System — Campaign Collector

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Sync history, configuration, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Sync session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next sync session
- Condense to essence — no narrative
- Update index.md immediately after each sync
- Write-through on critical events:
  - Ad account selection changed
  - New campaign detected that wasn't in previous sync
  - Unusual sync result (errors, rate limits, permission issues, data gaps)
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Ad account IDs and names in use
- Campaign naming patterns (e.g., "Brand - AU - Conversions")
- Sync patterns (typical data volume per pull)
- Any recurring issues with Meta API responses (rate limits, permission errors)
- Date range gaps (periods where data may be incomplete)

## What NOT to Remember

- Individual insight metrics (that lives in marketing-data.json)
- Campaign performance judgments (that's the Performance Analyst's job)
- Anything derivable from the current marketing-data.json state
