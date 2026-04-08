---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/index.md`

2. **Update with current session:**
   - Last generation date and batch summary (batch ID, angles count, creatives generated)
   - Any notable findings (effective angle patterns, generation issues, format observations)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if generation was performed
   - `angles.md` — Update with any newly proven angle patterns

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
