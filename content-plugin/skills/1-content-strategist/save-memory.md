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

Read current `_bmad/_memory/bmad-apg-ccs-1-content-strategist-sidecar/index.md` and update:

**Active Projects section** — For the current project, update or add:
```
- {project_slug}: {status} | Research: {done/pending} | Ideation: {done/pending} | Content Tree: {done/pending}
```

**Last Session section** — Replace with:
```
## Last Session
- Date: {today}
- Project: {project_slug or 'standalone'}
- Actions: {what was done — e.g. "Ran competitive research, generated 5 content concepts"}
- Notes: {any notable observations or pending items}
```

### Step 2: Update `patterns.md` (if applicable)

Only update if new patterns were learned this session:

- **Research patterns** — Which search strategies, API queries, or data sources yielded best results
- **Topic clusters** — Recurring high-signal topics discovered across research runs
- **Ideation success** — Which concept types scored highest in evaluation

### Step 3: Update `chronology.md`

Append a session entry:
```
## {today} — {project_slug or 'standalone'}
- Created: {what was produced — research report, content concepts, content tree}
- Status: {current project status}
- Notes: {any notable context}
```

### Step 4: Confirm

```
Memory saved.
- index.md: updated with project status
- chronology.md: session logged
{- patterns.md: updated with {what} (only if updated)}
```
