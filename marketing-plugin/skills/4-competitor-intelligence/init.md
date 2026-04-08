---
name: init
description: First-run setup for Competitor Intelligence
menu-code: INIT
---

# First-Run Setup for Competitor Intelligence

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — watchlist, scrape history, current state
- `chronology.md` — scrape session timeline
- `access-boundaries.md` — read/write/deny zones
- `patterns.md` — recurring observations about competitor ad strategies

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/index.md`

```markdown
# Competitor Intelligence — Session Index

## Watchlist
(none yet — use MC to add competitors)

## Scrape History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Competitor Intelligence

## Read Access
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/
- .env (for API credentials)

## Write Access
- marketing-plugin/data/competitor-data.json
- marketing-plugin/data/competitor-assets/
- _bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/chronology.md`

```markdown
# Scrape Chronology

(Scrape sessions logged here as they accumulate)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/patterns.md`

```markdown
# Competitor Intelligence Patterns

(Recurring observations about competitor ad strategies logged here)
```

## Environment Check

Verify these are set in `.env`:
- `APIFY_API_TOKEN` — Apify API token for Meta Ad Library scraping

If missing, prompt the user to add it. The token is required for running the scrape-competitor-ads.py script.

## Competitor Data Bootstrap

If `marketing-plugin/data/competitor-data.json` does not exist, create it with this scaffold:

```json
{
  "meta": {
    "last_scrape": null,
    "scrape_status": "never_scraped",
    "total_ads_tracked": 0,
    "winner_count": 0
  },
  "watchlist": [],
  "ads": []
}
```

Also create the `marketing-plugin/data/competitor-assets/` directory if it does not exist.

## Ready

Setup complete! Add competitors to your watchlist with [MC] and run your first scrape with [SC].
