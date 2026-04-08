---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-funnel-mapper-sidecar/index.md`

2. **Update with current session:**
   - Funnel analyses performed and key findings
   - Bottlenecks identified (which campaigns, which funnel stage)
   - Campaigns flagged for wasted budget
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add newly identified conversion issues, UTM conventions, funnel stage benchmarks
   - `chronology.md` — Add session summary if funnel analysis was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
