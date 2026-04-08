# Memory System — Funnel Mapper

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Funnel analysis history, known bottlenecks, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `patterns.md` | Conversion issues, UTM conventions, funnel stage benchmarks | When analyzing (FO) |
| `chronology.md` | Analysis session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next funnel analysis
- Condense to essence — no narrative
- Update index.md immediately after each analysis session
- Write-through on critical events:
  - Campaign identified as spending with zero conversions
  - Funnel bottleneck identified (which stage, which campaign)
  - UTM convention pattern discovered (useful for Phase 2 GA4 linking)
  - User confirms a campaign should be paused or restructured
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Funnel patterns (which campaigns convert well, which don't)
- Known bottleneck campaigns (campaign name + which stage breaks)
- UTM parameter conventions (for future GA4 integration)
- Dismissed flags (to avoid re-flagging campaigns the user already reviewed)
- Campaigns the user has actioned (paused, restructured, etc.)

## What NOT to Remember

- Individual metric values (those live in marketing-data.json insights[])
- Campaign structure details (those live in marketing-data.json meta.campaigns[])
- Anything derivable from the current marketing-data.json state
