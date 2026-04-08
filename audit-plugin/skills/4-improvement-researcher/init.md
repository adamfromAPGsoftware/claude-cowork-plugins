---
name: init
description: First-run setup for Process Analyst
menu-code: INIT
---

# First-Run Setup for Process Analyst

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-process-analyst-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active research engagements, current work, configuration
- `patterns.md` — research patterns learned across clients and industries
- `chronology.md` — research session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-process-analyst-sidecar/index.md`

```markdown
# Process Analyst — Session Index

## Active Engagements
(none yet)

## Configuration
- Default dev rate: ${YOUR_DEV_RATE}/hr (internal, not shown to client)
- Default PM rate: ${YOUR_PM_RATE}/hr (internal, not shown to client)
- Value calculation: time_saving (hrs × rate × 52) + productivity_enhancement (metric × improvement %)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-process-analyst-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Process Analyst

## Read Access
- clients/
- assets/
- _bmad/_memory/bmad-apg-process-analyst-sidecar/

## Write Access
- clients/
- _bmad/_memory/bmad-apg-process-analyst-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
```

### `{project-root}/_bmad/_memory/bmad-apg-process-analyst-sidecar/patterns.md`

```markdown
# Research Patterns

## Industry Patterns
(accumulates across audits — tool recommendations, integration paths, common automation opportunities)

## Common Tool Stacks by Industry
(which tools appear together, typical API integration opportunities)

## Effective Research Strategies
(which search queries, tool categories, and comparison approaches produce the best results)

## Value Estimation Patterns
(typical time savings by automation type, typical productivity improvements by AI use case)
```

### `{project-root}/_bmad/_memory/bmad-apg-process-analyst-sidecar/chronology.md`

```markdown
# Research Chronology

(Research sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to analyze your first completed audit.
