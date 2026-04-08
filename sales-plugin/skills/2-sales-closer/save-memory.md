---
name: save-memory
description: Explicitly save current session context to memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/apg-close-sidecar/index.md`

2. **Update with current session:**
   - Active engagements and their current status
   - Client slug being worked on and what was produced
   - Any configuration changes
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new close patterns or social proof observations discovered this session
   - `chronology.md` — Add session summary if a close asset was generated

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
