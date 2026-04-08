---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-vsl-generator-sidecar/index.md`

2. **Update with current session:**
   - Last generation date and project summary (project ID, offer, angles count, script status)
   - Any notable findings (effective frameworks, script patterns, user preferences)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if generation was performed
   - `frameworks.md` — Update with any framework preference feedback

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
