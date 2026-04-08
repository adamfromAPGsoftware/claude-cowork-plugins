---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/index.md`

2. **Update with current session:**
   - Last import date and file(s) processed
   - Reconciliation progress (reconciled / ambiguous / unmatched counts)
   - CRM sync status (synced count, pending count)
   - Any notable findings (new merchant aliases, recurring match patterns)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new merchant alias mappings, confirmed duplicate pairs, CRM reference patterns
   - `chronology.md` — Add session summary if import or reconciliation was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
