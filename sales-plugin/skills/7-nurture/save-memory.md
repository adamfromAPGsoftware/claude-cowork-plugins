---
name: save-memory
description: Explicitly save current session context to memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/apg-nurture-sidecar/index.md`

2. **Update with current session:**
   - Active nurture sequences and their current steps
   - Last run date and summary (leads processed, drafts created, replies detected)
   - Any configuration changes
   - Next steps or issues to flag

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new observations about which emails/angles generate replies or conversions
   - `chronology.md` — Add session summary with date, leads processed, and outcomes

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
