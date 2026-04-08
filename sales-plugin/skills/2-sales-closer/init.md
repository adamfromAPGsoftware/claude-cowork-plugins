---
name: init
description: First-run setup for Close
menu-code: INIT
---

# First-Run Setup for Close ⚡

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/apg-close-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active close engagements, current work, configuration
- `patterns.md` — close patterns learned from successful deals
- `chronology.md` — session timeline
- `access-boundaries.md` — read/write/deny zones

## Setup Questions

A few quick questions to configure your environment:

1. **Social proof folder** — Where are your social proof assets stored?
   *(Default: `assets/social-proof/`)*

2. **Pricing tiers** — Confirm current tier pricing (AUD):
   - Micro (5–10hrs dev): $1,800
   - Standard (12–25hrs dev): $3,800
   - Complex (28–45hrs dev): $6,500
   - Sprint: $15,000
   *(Confirm, or provide updated figures)*

   Note: Blended hourly rates are extracted per client from their transcripts — not configured globally.

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/_bmad/_memory/apg-close-sidecar/index.md`

```markdown
# Close — Session Index

## Active Engagements
(none yet)

## Configuration
- Social proof folder: {confirmed-path}
- Pricing tiers: Micro $1,800 / Standard $3,800 / Complex $6,500 / Sprint $15,000 AUD
- Note: Blended hourly rates are extracted per client from transcripts (fallback: $50/hr LOW confidence)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/apg-close-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Close ⚡

## Read Access
- clients/
- assets/social-proof/
- _bmad/_memory/apg-close-sidecar/

## Write Access
- clients/
- _bmad/_memory/apg-close-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
```

### `{project-root}/_bmad/_memory/apg-close-sidecar/patterns.md`

```markdown
# Close Patterns

## Successful Close Language
(accumulates from successful deals — Mark, Dale, etc.)

## Effective Waste Framings
(which waste types land hardest by industry)

## Social Proof Performance
(which assets land by industry tag)
```

### `{project-root}/_bmad/_memory/apg-close-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to process your first discovery call.
