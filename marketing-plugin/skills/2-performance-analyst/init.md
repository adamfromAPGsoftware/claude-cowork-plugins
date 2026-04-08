---
name: init
description: First-run setup for Performance Analyst
menu-code: INIT
---

# First-Run Setup for Performance Analyst

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — analysis history, known baselines, current state
- `patterns.md` — campaign naming conventions, performance benchmarks, user focus areas
- `chronology.md` — analysis session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/index.md`

```markdown
# Performance Analyst — Session Index

## Known Baselines
(accumulates as analyses establish normal performance levels per campaign)

## Active Focus Areas
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Performance Analyst

## Read Access
- marketing/
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/

## Write Access
- _bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
- finance/ (marketing plugin does not touch finance data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/patterns.md`

```markdown
# Performance Patterns

## Campaign Naming Conventions
(naming patterns observed across campaigns — helps identify campaign purpose)

## Performance Benchmarks
(typical CTR, CPC, CPM ranges per campaign objective — establishes what's "normal")

## User Focus Areas
(campaigns or metrics the user frequently asks about)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/chronology.md`

```markdown
# Analysis Chronology

(Analysis sessions logged here as they accumulate)
```

## Marketing Data Check

If `marketing/marketing-data.json` does not exist, warn the user and suggest running Campaign Collector [PC] first to bootstrap the file.

If it exists, verify it has a `meta.campaigns` array and note the current campaign count and insight date range.

## Ready

Setup complete! Ready to analyze your campaign performance data.
