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

Read current `context/memory/2-copywriter-sidecar/index.md` and update:

**Active Projects section** — Update project status.

**Derivative Tracking section** — For each piece of content produced this session, add:
```
| {date} | {platform} | {format} | {category} | {hook summary} | {keyword} | {status} |
```

**Last Session section** — Replace with:
```
## Last Session
- Date: {today}
- Project: {project_slug or 'standalone'}
- Actions: {what was written — e.g. "Generated 5 short-form scripts, LinkedIn post"}
- Notes: {any notable observations}
```

### Step 2: Update `patterns.md` (if applicable)

Only update if new patterns were learned:
- **Hook effectiveness** — Which hooks got strong reactions or approvals
- **Voice calibration** — Any corrections to voice matching from user feedback
- **Platform performance** — What worked vs didn't per platform

### Step 3: Update `chronology.md`

Append a session entry:
```
## {today} — {project_slug or 'standalone'}
- Created: {what was produced — scripts, posts, blog drafts}
- Status: {current status}
- Notes: {context}
```

### Step 4: Confirm

```
Memory saved.
- index.md: updated with derivative tracking
- chronology.md: session logged
{- patterns.md: updated with {what} (only if updated)}
```
