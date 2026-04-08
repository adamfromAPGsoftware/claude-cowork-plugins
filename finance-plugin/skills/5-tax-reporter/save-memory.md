---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-fin-tax-reporter-sidecar/index.md`

2. **Update with current session:**
   - Reports generated this session (type, period, output path)
   - Data quality observations (GST coverage, receipt coverage)
   - Any tax classification patterns confirmed
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `patterns.md` — Add new R&D tagging rules or GST classification patterns confirmed this session
   - `chronology.md` — Add session summary if reports were generated

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
