---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/index.md`

2. **Update with current session:**
   - CRM-enabled accounts processed and their qualification counts
   - Tier breakdown per account
   - CRM sync results (contacts synced, leads created, errors)
   - Any notable findings (high-confidence agency_services prospects, classification edge cases)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if qualification or CRM sync was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
