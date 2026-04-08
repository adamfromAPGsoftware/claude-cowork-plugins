# Memory System — Campaign Planner

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Campaign history, configuration, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Planning session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next planning session
- Condense to essence — no narrative
- Update index.md immediately after each campaign creation or strategy build
- Write-through on critical events:
  - New campaign created with product and audience summary
  - Market intelligence report generated with key themes
  - Creative strategy approved with angle count
  - Performance review completed with winner/loser counts
  - Campaign status change (draft → planning → creatives → live → completed)
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Campaign IDs and their current pipeline status
- Market intelligence themes that led to winning angles
- Audience insights that proved accurate (validated by performance data)
- Creative strategy patterns that produced high-performing campaigns
- Performance review outcomes — which iteration cycles improved CPA/ROAS
- Approval gate decisions and any modifications requested

## What NOT to Remember

- Full landing page copy (that lives in campaign-data.json)
- Individual ad performance metrics (that's the Performance Analyst's job)
- Creative asset details (that's the Creative Generator's job)
- Anything derivable from the current campaign-data.json state
