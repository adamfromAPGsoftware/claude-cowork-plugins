---
name: init
description: First-run setup for VSL Generator
menu-code: INIT
---

# First-Run Setup for VSL Generator

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — project history, configuration, current state
- `chronology.md` — generation session timeline
- `access-boundaries.md` — read/write/deny zones
- `frameworks.md` — notes on which VSL frameworks work well

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/index.md`

```markdown
# VSL Generator — Session Index

## Configuration
- Default frameworks: Hormozi, Mosing, PAS-Long
- Pricing source: _bmad/apg-pricing.md
- Proven template: content/standalone/2026-03-08-operational-audit-vsl/vsl-script.md

## Project History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for VSL Generator

## Read Access
- marketing-plugin/
- video-plugin/skills/1-video-editor/workflows/vsl-edit/data/ (pacing rules, compliance checklist)
- content/standalone/ (proven VSL template, generated scripts)
- _bmad/apg-pricing.md
- _bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/
- .env (for API credentials)

## Write Access
- marketing-plugin/data/vsl-data.json
- content/standalone/{date}-{slug}/ (generated scripts and edit instructions)
- _bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
- video-plugin/ (read-only reference only — never write to video plugin)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/chronology.md`

```markdown
# VSL Generation Chronology

(Generation sessions logged here as they accumulate)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/frameworks.md`

```markdown
# VSL Framework Notes

Notes on which frameworks have worked well, user preferences, and lessons learned.

## Framework Preferences
(updated after user feedback on generated scripts)

## Proven Patterns
- Hormozi structure validated with $3,000 Operational Audit VSL (4:00-4:30 runtime)
```

## Environment Check

Verify these are set in `.env`:
- `OPENROUTER_API_KEY` — Required for LLM reasoning during angle generation

No additional env vars needed — MG generation happens in the video editor, not here.

## VSL Data Bootstrap

If `marketing-plugin/data/vsl-data.json` does not exist, create it:

```json
{
  "meta": {
    "last_generation": null,
    "total_projects": 0
  },
  "projects": []
}
```

## Ready

Setup complete! Ready to generate VSL angles and scripts.
