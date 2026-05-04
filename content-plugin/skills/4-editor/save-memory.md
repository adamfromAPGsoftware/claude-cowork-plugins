---
name: save-memory
description: Save current session context to memory
menu-code: SM
---

# [SM] Save Memory

## Purpose

Persist current session progress to sidecar memory so the next session picks up where this one left off.

## Execution

### Step 1: Update `index.md`

Read current `memory/4-editor-sidecar/index.md` and update:

**Active Reviews section** — Update review status and gate results.

**Last Session section** — Replace with:
```
## Last Session
- Date: {today}
- Content reviewed: {what was reviewed}
- Results: Brand Voice {score}/10, ICP {score}/10, Value {score}/10 — {PASS/FAIL}
- Notes: {observations}
```

### Step 2: Update `patterns.md` (if applicable)

- **Recurring issues** — Common problems found across reviews
- **Voice drift patterns** — Where brand voice tends to drift
- **Feedback effectiveness** — Which feedback approaches led to best revisions

### Step 3: Update `chronology.md`

Append session entry.

### Step 4: Confirm

```
Memory saved.
- index.md: updated with review results
- chronology.md: session logged
{- patterns.md: updated with {what} (only if updated)}
```
