---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/index.md`

2. **Update with current session:**
   - Accounts polled and their last poll timestamps
   - DM and comment counts per account
   - Any notable findings (new conversations, expiring windows, API issues)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if polling was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
