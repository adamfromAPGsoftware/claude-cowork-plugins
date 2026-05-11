---
name: save-memory
description: Save current session context to the wiki
menu-code: SM
---

# [SM] Save Memory

## Purpose

Log the current session in the wiki index and surface any uncaptured corrections before closing out.

## Execution

### Step 1: Append session row to `wiki/index.md`

Read `{plugin-root}/video-plugin/wiki/index.md`. Append a row to the Session Log table:

```markdown
| {today} | {project_slug or "standalone"} | {skills used — e.g. "4-short-form [SF][SB][RE]"} | {n — corrections captured this session} |
```

### Step 2: Surface uncaptured corrections

Prompt:
```
Any corrections from this session not yet in the wiki?
If anything needed fixing that should be prevented next time, run [WU] now before closing out.
```

Wait for response. If user says yes or names a correction → run [WU] inline for each one.

### Step 3: Confirm

```
Session saved.
- wiki/index.md: session row added for {project_slug}
- Corrections captured this session: {n}
{- [WU] run: "{correction summary}" → {page} (only if WU was triggered)}
```
