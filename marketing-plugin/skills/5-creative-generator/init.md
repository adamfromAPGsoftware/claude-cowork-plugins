---
name: init
description: First-run setup for Creative Generator
menu-code: INIT
---

# First-Run Setup for Creative Generator

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — batch history, configuration, current state
- `chronology.md` — generation session timeline
- `access-boundaries.md` — read/write/deny zones
- `angles.md` — proven angle patterns and performance notes

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/index.md`

```markdown
# Creative Generator — Session Index

## Configuration
- Default image formats: 1:1, 9:16, 16:9
- Default video formats: 9:16, 1:1
- Video duration: 5s

## Batch History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Creative Generator

## Read Access
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/
- .env (for API credentials)

## Write Access
- marketing-plugin/data/creative-data.json
- marketing-plugin/data/creatives/
- _bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/chronology.md`

```markdown
# Generation Chronology

(Generation sessions logged here as they accumulate)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/angles.md`

```markdown
# Angle Patterns

Proven angle patterns and performance notes accumulated across batches.

## Winner Patterns
(none yet — updated after performance data flows back from the Performance Analyst)

## Angle Templates
(accumulated as batches are generated)
```

## Environment Check

Verify these are set in `.env`:
- `OPENROUTER_API_KEY` — Required for LLM calls (angle generation reasoning)
- `FAL_API_KEY` — Required for fal.ai video generation (Kling image-to-video)

If missing, prompt the user to add them.

## Creative Data Bootstrap

If `marketing-plugin/data/creative-data.json` does not exist, create it with this scaffold:

```json
{
  "meta": {
    "last_generation": null,
    "total_batches": 0,
    "total_creatives": 0
  },
  "batches": []
}
```

Also create the creatives directory if it doesn't exist:
- `marketing-plugin/data/creatives/`

## Ready

Setup complete! Ready to build angles from competitor intelligence and generate creatives.
