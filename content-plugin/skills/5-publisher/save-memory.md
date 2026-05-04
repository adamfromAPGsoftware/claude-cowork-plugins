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

Read current `memory/5-publisher-sidecar/index.md` and update:

**Lead Magnet Keyword Registry** — Add any new keywords assigned this session.

**Last Session section** — Replace with:
```
## Last Session
- Date: {today}
- Actions: {what was scheduled/published — e.g. "Scheduled 5 short-form videos to TikTok + YouTube"}
- Posts created: {count and platform summary}
- Notes: {observations}
```

### Step 2: Update `patterns.md` (if applicable)

- **Scheduling patterns** — Optimal times confirmed by engagement data
- **Platform quirks** — New API gotchas or format issues discovered
- **Calendar history** — Significant scheduling events

### Step 3: Update `chronology.md`

Append session entry with post IDs and scheduling details.

### Step 4: Confirm

```
Memory saved.
- index.md: updated with scheduling status
- chronology.md: session logged
{- patterns.md: updated with {what} (only if updated)}
```
