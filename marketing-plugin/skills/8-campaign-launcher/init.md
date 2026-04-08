---
name: init
description: First-run setup for Campaign Launcher
menu-code: INIT
---

# First-Run Setup for Campaign Launcher

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — campaign deployment history, configuration, current state
- `chronology.md` — deployment session timeline
- `access-boundaries.md` — read/write/deny zones
- `api-log.md` — audit trail of all API write operations

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/index.md`

```markdown
# Campaign Launcher — Session Index

## Configuration
- Default campaign status: PAUSED
- Dry-run default: true
- Approval gates: all enabled

## Deployment History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Campaign Launcher

## Read Access
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/
- .env (for API credentials)

## Write Access
- marketing-plugin/data/campaign-data.json
- marketing-plugin/data/creative-data.json (creative ID updates only)
- marketing-plugin/data/marketing-data.json (ad ID updates only)
- _bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/chronology.md`

```markdown
# Deployment Chronology

(Deployment sessions logged here as they accumulate)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/api-log.md`

```markdown
# API Write Operations Log

All Meta, GA4, and Cloudflare write operations are logged here for audit trail.

| Date | Operation | Endpoint | Entity IDs | Result |
|------|-----------|----------|------------|--------|
```

## Environment Check

Verify these are set in `.env`:
- `META_ACCESS_TOKEN` — Required for Meta Marketing API write operations
- `META_AD_ACCOUNT_ID` — Required for creating campaigns and uploading creatives
- `CLOUDFLARE_API_TOKEN` — Required for deploying lead capture Workers
- `CLOUDFLARE_ACCOUNT_ID` — Required for Cloudflare Workers deployment
- `GOOGLE_APPLICATION_CREDENTIALS` — Required for GA4 property setup (service account JSON path)
- `META_PIXEL_ID` — Required for conversion tracking verification

If any are missing, list which are absent and prompt the user to add them. The agent can still operate for capabilities that don't need the missing tokens.

## Ready

Setup complete! Ready to launch campaigns to Meta with full tracking infrastructure.
