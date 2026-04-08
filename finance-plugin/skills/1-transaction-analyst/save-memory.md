---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/index.md`

2. **Update with current session:**
   - Last sync date and transaction count
   - Categorization progress (auto vs manual vs unset)
   - Any notable findings (new merchants, unusual patterns)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new merchant → category mappings confirmed this session
   - `chronology.md` — Add session summary if sync was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
