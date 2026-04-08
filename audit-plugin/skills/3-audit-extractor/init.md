---
name: init
description: First-run setup for Analyst
menu-code: INIT
---

# First-Run Setup for Analyst ⚡

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/apg-analyst-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active audit engagements, current work, configuration
- `patterns.md` — audit patterns learned across clients and industries
- `chronology.md` — session timeline
- `access-boundaries.md` — read/write/deny zones

## Setup Questions

One quick confirmation to get started:

1. **Completeness checklist** — The analyst uses a per-stage checklist to track audit coverage across whatever business areas are discovered during transcript analysis. Industry-specific variants exist for NDIS, home-services, construction, and real estate. Confirm you want these defaults, or provide overrides.

   *(Default: use per-stage checklist + industry variants)*

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/_bmad/_memory/apg-analyst-sidecar/index.md`

```markdown
# Analyst — Session Index

## Active Engagements
(none yet)

## Configuration
- Completeness checklist: standard 5-stage + NDIS/home-services/construction variants
- Note: Blended hourly rates are extracted per client from transcripts (fallback: $50/hr LOW confidence)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/apg-analyst-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Analyst ⚡

## Read Access
- clients/
- assets/
- _bmad/_memory/apg-analyst-sidecar/

## Write Access
- clients/
- _bmad/_memory/apg-analyst-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
```

### `{project-root}/_bmad/_memory/apg-analyst-sidecar/patterns.md`

```markdown
# Audit Patterns

## Industry Patterns
(accumulates across audits — NDIS, home services, construction, real estate)

## Common Tool Stacks by Industry
(which tools appear together, typical integration gaps)

## Frequent Pain Point Patterns
(which pain points repeat across similar businesses)

## Follow-Up Question Effectiveness
(which questions reliably surface the deepest waste data)
```

### `{project-root}/_bmad/_memory/apg-analyst-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to analyze your first audit session.
