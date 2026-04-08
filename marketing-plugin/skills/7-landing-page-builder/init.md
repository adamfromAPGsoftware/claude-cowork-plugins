---
name: init
description: First-run setup for Landing Page Builder
menu-code: INIT
---

# First-Run Setup for Landing Page Builder

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — deployed page history, configuration, current state
- `chronology.md` — deployment session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/index.md`

```markdown
# Landing Page Builder — Session Index

## Configuration
- Default template: lead-gen
- Cloudflare Pages project: apg-landing-pages
- Domain pattern: *.{YOUR_DOMAIN}

## Deployed Pages
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Landing Page Builder

## Read Access
- marketing-plugin/data/campaign-data.json
- marketing-plugin/templates/landing-pages/
- marketing-plugin/references/
- _bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/
- .env (for Cloudflare credentials)

## Write Access
- marketing-plugin/data/campaign-data.json (landing_page and tracking sections only)
- marketing-plugin/data/landing-pages/
- _bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/chronology.md`

```markdown
# Deployment Chronology

(Deployment sessions logged here as they accumulate)
```

## Environment Check

Verify these are set in `.env`:
- `CLOUDFLARE_API_TOKEN` — Required for Cloudflare Pages deployment and DNS management
- `CLOUDFLARE_ACCOUNT_ID` — Required for Cloudflare API calls

If missing, prompt the user to add them.

## Data Directory Bootstrap

Create the landing pages output directory if it doesn't exist:
- `marketing-plugin/data/landing-pages/`

Verify templates exist:
- `marketing-plugin/templates/landing-pages/lead-gen.html`
- `marketing-plugin/templates/landing-pages/components/tracking.html`
- `marketing-plugin/templates/landing-pages/components/form.html`

If templates are missing, warn the user — generation will fail without them.

## Ready

Setup complete! Ready to generate and deploy landing pages from campaign configurations.
