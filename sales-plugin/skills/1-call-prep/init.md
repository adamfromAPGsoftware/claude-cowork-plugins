---
name: init
description: First-run setup for Pre-Discovery
menu-code: INIT
---

# First-Run Setup for Pre-Discovery

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/apg-pre-discovery-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active prospect preps, current work, configuration
- `patterns.md` — industry pain patterns, effective questions, signal accuracy
- `chronology.md` — session timeline
- `access-boundaries.md` — read/write/deny zones

## Setup Questions

A few quick questions to configure your environment:

1. **Discovery call booking link** — What's your default booking URL for scheduling discovery calls?
   *(e.g. Cal.com link — stored for prospect brief pre-call checklists)*

2. **Primary industry focus** — Do you have a primary industry focus right now, or are you targeting across industries?
   *(Helps pre-populate pain hypotheses. Options: `ndis`, `home-services`, `construction`, `real-estate`, `trades`, `professional-services`, `multi-industry`)*

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/_bmad/_memory/apg-pre-discovery-sidecar/index.md`

```markdown
# Pre-Discovery — Session Index

## Active Prospects
(none yet)

## Configuration
- Booking URL: {confirmed-url}
- Primary industry focus: {confirmed-industry or "multi-industry"}

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/apg-pre-discovery-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Pre-Discovery

## Read Access
- clients/
- reference/
- _bmad/_memory/apg-pre-discovery-sidecar/

## Write Access
- clients/
- _bmad/_memory/apg-pre-discovery-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
```

### `{project-root}/_bmad/_memory/apg-pre-discovery-sidecar/patterns.md`

```markdown
# Pre-Discovery Patterns

## Industry Pain Patterns
(accumulates across preps — which hypotheses proved accurate after discovery calls)

## Effective Opening Questions
(which Clarify questions reliably opened prospects up)

## Phone Call Signal Accuracy
(did buying signals from phone calls predict discovery call outcomes?)

## Prospect Brief Feedback
(what worked vs. didn't after calls — corrections from Adam)
```

### `{project-root}/_bmad/_memory/apg-pre-discovery-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to prep your first discovery call.
