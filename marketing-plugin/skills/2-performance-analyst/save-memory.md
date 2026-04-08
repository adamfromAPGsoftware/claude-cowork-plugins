---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-performance-analyst-sidecar/index.md`

2. **Update with current session:**
   - Analyses performed and key findings
   - Performance baselines updated (typical CTR, CPC, CPM per campaign)
   - Campaigns flagged for attention (zero conversions, high CPC, etc.)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add newly identified campaign naming conventions, performance benchmarks, user focus areas
   - `chronology.md` — Add session summary if analysis was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
