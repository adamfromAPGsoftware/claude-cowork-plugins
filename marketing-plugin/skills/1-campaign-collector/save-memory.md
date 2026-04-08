---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-collector-sidecar/index.md`

2. **Update with current session:**
   - Last sync date and entity counts (campaigns, ad sets, ads, insights)
   - Ad account ID in use
   - Any notable findings (new campaigns detected, API issues)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if sync was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
