# Memory System — Campaign Launcher

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Deployment history, configuration, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Deployment session timeline | When saving memory (SM) |
| `api-log.md` | Audit trail of all API write operations | After any API write, when saving memory (SM) |

## Discipline

- Only remember what matters for the next deployment session
- Condense to essence — no narrative
- Update index.md immediately after each deployment operation
- Write-through on critical events:
  - Campaign created in Meta (campaign ID, ad set IDs, ad IDs)
  - Creatives uploaded (creative IDs mapped to local paths)
  - GA4 property created or configured (property ID, measurement ID)
  - Lead capture Worker deployed (Worker URL, campaign ID)
  - Ads paused or activated (ad IDs, status change)
  - API failures (endpoint, error code, what was already created)
- Log ALL API write operations to api-log.md with timestamp, endpoint, entity IDs, and result
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Campaign IDs created and their current status (PAUSED/ACTIVE)
- Mapping of campaign IDs to Meta entity IDs (campaign, ad set, ad)
- Creative upload status (which batches are uploaded, which creative IDs)
- GA4 property and measurement IDs per campaign domain
- Lead capture Worker URLs per campaign
- Approval gate outcomes (who approved, when)
- Any API errors or rate limit encounters

## What NOT to Remember

- Full API payloads (too verbose — store entity IDs only)
- Creative asset content (that lives in creative-data.json)
- Campaign planning details (that's the Campaign Planner's job)
- Performance metrics (that's the Performance Analyst's job)
- Anything derivable from the current campaign-data.json state
