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

Read current `context/memory/3-creative-director-sidecar/index.md` and update:

**Active Projects section** — Update project and visual asset status.

**Last Session section** — Replace with:
```
## Last Session
- Date: {today}
- Project: {project_slug or 'standalone'}
- Actions: {what was created — e.g. "Generated 3 thumbnail combos, CTR validated"}
- Notes: {observations}
```

### Step 2: Update `patterns.md` (if applicable)

- **Visual preferences** — Style choices that worked well
- **Thumbnail performance** — CTR scores and user feedback
- **Prompt patterns** — Gemini prompts that produced strong results

### Step 3: Update `chronology.md`

Append session entry.

### Step 4: Confirm

```
Memory saved.
- index.md: updated with project status
- chronology.md: session logged
{- patterns.md: updated with {what} (only if updated)}
```
