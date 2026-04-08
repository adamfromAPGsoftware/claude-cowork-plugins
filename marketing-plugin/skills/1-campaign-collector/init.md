---
name: init
description: First-run setup for Campaign Collector
menu-code: INIT
---

# First-Run Setup for Campaign Collector

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — sync history, configuration, current state
- `chronology.md` — sync session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/index.md`

```markdown
# Campaign Collector — Session Index

## Configuration
- Meta ad account ID: (set via DA — discover accounts)
- Default date range: last 30 days

## Sync History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Campaign Collector

## Read Access
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/
- .env (for API credentials)

## Write Access
- marketing-plugin/data/
- _bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/chronology.md`

```markdown
# Sync Chronology

(Sync sessions logged here as they accumulate)
```

## Environment Check

Verify these are set in `.env`:
- `META_ACCESS_TOKEN` — Meta Marketing API access token (read-only permissions)

If missing, prompt the user to add it. The token requires `ads_read` and `ads_management` (read-only) permissions on the target ad account.

## Marketing Data Bootstrap

If `marketing-plugin/data/marketing-data.json` does not exist, create it with this scaffold:

```json
{
  "meta": {
    "last_sync": null,
    "sync_status": "never_synced",
    "meta_ad_account_id": null
  },
  "campaigns": [],
  "ad_sets": [],
  "ads": [],
  "insights": []
}
```

## Ready

Setup complete! Ready to discover your ad accounts and pull your first campaign data.
