---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-fin-spend-investigator-sidecar/index.md`

2. **Update with current session:**
   - Investigations performed and key findings
   - Known baselines updated (category averages, recurring charges identified)
   - Leak flags added or resolved
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add newly identified recurring charges, category baselines, known merchants
   - `chronology.md` — Add session summary if investigation was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
