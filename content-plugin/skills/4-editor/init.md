---
name: init
description: First-run setup for CCS Editor
menu-code: INIT
---

# First-Run Setup for CCS Editor

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/content-plugin/data/memory/4-editor-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active reviews, quality gate results, current work
- `patterns.md` — recurring quality issues, voice drift patterns, common feedback
- `chronology.md` — session timeline

## Setup Questions

1. **Brand guidelines** — Confirm brand guidelines accessible at `{project-root}/references/brand-voice.md`
2. **ICP profile** — Confirm ICP profile accessible at `{project-root}/references/content-icp.md`
3. **Pass threshold** — Confirm quality gate pass threshold is 7/10 for all three gates

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/content-plugin/data/memory/4-editor-sidecar/index.md`

```markdown
# CCS Editor — Session Index

## Active Reviews
(none yet)

## Configuration
- Brand guidelines: confirmed
- ICP profile: confirmed
- Pass threshold: 7/10 (all gates)

## Last Session
(none)
```

### `{project-root}/content-plugin/data/memory/4-editor-sidecar/patterns.md`

```markdown
# Editor Patterns

## Recurring Quality Issues
(common problems across reviews)

## Voice Drift Patterns
(where and how brand voice tends to drift)

## Effective Feedback Patterns
(feedback approaches that led to best revisions)
```

### `{project-root}/content-plugin/data/memory/4-editor-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to review content.
