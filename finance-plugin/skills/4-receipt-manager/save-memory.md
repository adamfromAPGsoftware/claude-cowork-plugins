---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-fin-receipt-manager-sidecar/index.md`

2. **Update with current session:**
   - Receipts processed this session (count and details)
   - Receipt coverage stats (total, receipted, unreceipted above $50)
   - Any new merchant name patterns learned
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new merchant name variations confirmed this session
   - `chronology.md` — Add session summary if receipts were processed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
