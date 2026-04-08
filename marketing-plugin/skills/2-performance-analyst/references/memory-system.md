# Memory System — Performance Analyst

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Analysis history, known baselines, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `patterns.md` | Campaign naming conventions, performance benchmarks, user focus areas | When analyzing (CS, AS) |
| `chronology.md` | Analysis session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next analysis session
- Condense to essence — no narrative
- Update index.md immediately after each analysis session
- Write-through on critical events:
  - New campaign naming pattern identified
  - Performance benchmark established or significantly changed
  - Campaign flagged for user attention (zero conversions, anomalous CPC)
  - User's recurring focus area noted
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Campaign naming conventions (patterns that indicate campaign purpose)
- Performance benchmarks (typical CTR, CPC, CPM per campaign objective)
- User's focus areas (campaigns or metrics they frequently ask about)
- Notable anomalies that might confuse future analysis
- Dismissed flags (to avoid re-flagging)

## What NOT to Remember

- Individual metric values (those live in marketing-data.json insights[])
- Campaign structure details (those live in marketing-data.json meta.campaigns[])
- Anything derivable from the current marketing-data.json state
