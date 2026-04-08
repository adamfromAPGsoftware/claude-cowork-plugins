---
name: save-memory
description: Save current session progress to memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/apg-process-mapper-sidecar/index.md`

2. **Update with current session:**
   - Active engagements and their current status (sessions completed, audit data state, open follow-up questions, next session date if known)
   - Client slug being worked on and what was extracted this session
   - Any new patterns or industry observations
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new industry patterns, effective follow-up questions, or tool stack observations discovered this session
   - `chronology.md` — Add session summary if a session was analyzed or the audit data was materially updated

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
