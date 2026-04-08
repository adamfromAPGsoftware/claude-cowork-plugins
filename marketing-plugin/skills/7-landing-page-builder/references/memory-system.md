# Memory System — Landing Page Builder

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Deployed page history, domain configs, current state | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Deployment session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next landing page session
- Condense to essence — no narrative
- Update index.md immediately after each deployment
- Write-through on critical events:
  - New landing page generated with template and campaign ID
  - Landing page deployed with domain and URL
  - Domain configured with DNS details
  - Tracking codes injected with GA4 and Meta Pixel IDs
  - Deployment failures or Cloudflare API issues
  - Template customisations that deviated from defaults
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Campaign IDs and their deployed domains/URLs
- Domain configurations (which subdomains point where)
- Template customisations applied per campaign
- Tracking ID assignments (which GA4/Pixel IDs map to which campaigns)
- Deployment success/failure patterns
- Any Cloudflare API quirks or rate limit issues

## What NOT to Remember

- Full landing page HTML (that lives in data/landing-pages/)
- Campaign product/audience details (that lives in campaign-data.json)
- Creative assets or copy variants (that's the Creative Generator's domain)
- Ad performance metrics (that's the Performance Analyst's job)
- Anything derivable from the current campaign-data.json state
