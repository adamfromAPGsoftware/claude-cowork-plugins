# Memory System — Competitor Intelligence

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Watchlist state, scrape history, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Scrape session timeline | When saving memory (SM) |
| `patterns.md` | Recurring competitor strategy observations | When saving memory (SM) |

## Discipline

- Only remember what matters for the next scrape session
- Condense to essence — no narrative
- Update index.md immediately after each scrape
- Write-through on critical events:
  - Competitor added or removed from watchlist
  - New winner detected (ad crossed 30+ day threshold)
  - Scrape failures or Apify issues
  - Significant strategy shift observed across a competitor's ads
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Watchlist changes (competitors added/removed and why)
- Scrape patterns (typical volume per competitor, frequency)
- Notable winners and their characteristics (hook type, visual style, longevity)
- Competitor strategy shifts (e.g., switched from UGC to polished, changed CTA approach)
- Any recurring issues with Apify scraping (rate limits, Page ID changes)

## What NOT to Remember

- Individual ad details (that lives in competitor-data.json)
- Raw creative analysis results (stored per-ad in competitor-data.json)
- Anything derivable from the current competitor-data.json state
