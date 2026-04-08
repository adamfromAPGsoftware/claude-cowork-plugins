---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/index.md`

2. **Update with current session:**
   - Accounts processed and response counts per account
   - DMs sent, comments replied, items skipped (with reasons)
   - Any errors encountered (send failures, API issues)
   - Conversation patterns noted (common question types, nurture stage distribution)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if responses were sent

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
