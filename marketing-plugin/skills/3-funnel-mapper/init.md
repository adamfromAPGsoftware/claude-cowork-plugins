---
name: init
description: First-run setup for Funnel Mapper
menu-code: INIT
---

# First-Run Setup for Funnel Mapper

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — funnel analysis history, known bottlenecks, current state
- `patterns.md` — funnel patterns, campaigns with conversion issues, UTM conventions
- `chronology.md` — analysis session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/index.md`

```markdown
# Funnel Mapper — Session Index

## Known Bottlenecks
(accumulates as analyses identify funnel stage failures)

## Active Investigations
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Funnel Mapper

## Read Access
- marketing/
- marketing-plugin/
- _bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/

## Write Access
- _bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (marketing plugin does not touch audit data)
- finance/ (marketing plugin does not touch finance data)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/patterns.md`

```markdown
# Funnel Patterns

## Known Conversion Issues
(campaigns consistently producing zero conversions despite spend)

## UTM Conventions
(UTM parameter patterns observed in campaign data — helps link to GA4 in Phase 2)

## Funnel Stage Benchmarks
(typical conversion rates at each funnel stage per campaign objective)
```

### `{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/chronology.md`

```markdown
# Funnel Analysis Chronology

(Analysis sessions logged here as they accumulate)
```

## Marketing Data Check

If `marketing/marketing-data.json` does not exist, warn the user and suggest running Campaign Collector [PC] first to bootstrap the file.

If it exists, verify it has a `meta.campaigns` array and note the current campaign count and whether conversion data exists in insights.

## Ready

Setup complete! Ready to map your ad-to-conversion funnels.
