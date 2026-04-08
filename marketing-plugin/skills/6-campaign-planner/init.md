---
name: init
description: First-run setup for Campaign Planner
menu-code: INIT
---

# First-Run Setup for Campaign Planner

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — campaign history, configuration, current state
- `chronology.md` — planning session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/index.md`

```markdown
# Campaign Planner — Session Index

## Configuration
- Default campaign objective: leads
- Default landing page template: lead-gen
- Review cadence: 7 days

## Campaign History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Campaign Planner

## Read Access
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/
- .env (for API credentials)

## Write Access
- marketing-plugin/data/campaign-data.json
- marketing-plugin/data/reports/campaigns/
- _bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/chronology.md`

```markdown
# Planning Chronology

(Planning sessions logged here as they accumulate)
```

## Reports Directory

Create the reports directory structure if it doesn't exist:
- `marketing-plugin/data/reports/campaigns/`

This directory holds per-campaign market intelligence reports and strategy documents.

## Campaign Data Bootstrap

If `marketing-plugin/data/campaign-data.json` does not exist, create it with this scaffold:

```json
{
  "meta": {
    "last_created": null,
    "total_campaigns": 0,
    "active_campaigns": 0
  },
  "campaigns": []
}
```

## Ready

Setup complete! Ready to plan campaigns, generate market intelligence, and build creative strategies.
