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

Read current `_bmad/_memory/apg-pre-discovery-sidecar/index.md` and update:

**Active Prospects section** — For the current `{client_slug}`, update or add:
```
- {client_slug}: {status} | Research: {done/pending} | Phone: {done/pending} | Prospect Brief: {done/pending}
```

**Last Session section** — Replace with:
```
## Last Session
- Date: {today}
- Client: {client_slug}
- Actions: {what was done this session — e.g. "Created client, ran research, generated prospect brief"}
- Notes: {any notable observations or pending items}
```

### Step 2: Update `patterns.md` (if applicable)

Only update if new patterns were learned this session:

- **Industry pain patterns** — If research revealed industry-specific insights worth remembering
- **Effective questions** — If Adam gave feedback on what worked
- **Signal accuracy** — If a discovery call happened and we know whether phone signals were accurate

### Step 3: Update `chronology.md`

Append a session entry:
```
## {today} — {client_slug}
- Created: {what was created — client folder, research, transcript analysis, prospect brief}
- Status: {current prospect status}
- Notes: {any notable context}
```

### Step 4: Confirm

```
Memory saved.
- index.md: updated with {client_slug} status
- chronology.md: session logged
{- patterns.md: updated with {what} (only if updated)}
```
