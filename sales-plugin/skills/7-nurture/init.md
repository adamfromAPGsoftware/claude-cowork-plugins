---
name: init
description: First-run setup for Nurture Sequencer
menu-code: INIT
---

# First-Run Setup for Nurture Sequencer

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/apg-nurture-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active nurture sequences, configuration, last run summary
- `patterns.md` — nurture patterns learned from successful conversions
- `chronology.md` — session timeline
- `access-boundaries.md` — read/write/deny zones

## Setup Confirmation

Confirm the following defaults:

1. **Strategy document location:** `references/nurture-sequence-strategy.md` (within this skill folder)
2. **Email voice reference:** `shared-references/adam-email-voice.md`
3. **Post-discovery stages to nurture:** Discovery Call - Completed, Qualified, Proposal, Initial Follow-Up Phone Call, Not Showing up to Discovery Call (Need Harassment), Need Re-Activation
4. **Schedule:** Weekday mornings at 8:47am AEST

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/_bmad/_memory/apg-nurture-sidecar/index.md`

```markdown
# Nurture Sequencer — Session Index

## Active Sequences
(none yet)

## Configuration
- Strategy doc: references/nurture-sequence-strategy.md
- Email voice: shared-references/adam-email-voice.md
- Schedule: Weekday mornings, 8:47am AEST
- Max emails per lead per day: 1
- Sequence length: 5 emails over 21 days

## Last Run
(none)
```

### `{project-root}/_bmad/_memory/apg-nurture-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Nurture Sequencer

## Read Access
- clients/
- references/nurture-sequence-strategy.md
- _bmad/apg-pipeline.md
- shared-references/
- _bmad/_memory/apg-nurture-sidecar/

## Write Access
- _bmad/_memory/apg-nurture-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/

## MCP Access
- mcp__claude_ai_APG_CRM__* (leads, contacts, comments, activities)
- mcp__claude_ai_Gmail__* (search, read, create drafts)
```

### `{project-root}/_bmad/_memory/apg-nurture-sidecar/patterns.md`

```markdown
# Nurture Patterns

## Effective Email Angles by Industry
(accumulates from successful conversions)

## Scenario Detection Accuracy
(track which scenario classifications led to conversions vs. dead ends)

## Timing Observations
(which day gaps work best — shorter? longer?)

## Reply Triggers
(which email step generates the most replies)
```

### `{project-root}/_bmad/_memory/apg-nurture-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Run [NDR] to process your first daily nurture batch, or [NSL] to test with a single lead.
