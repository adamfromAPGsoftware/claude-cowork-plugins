---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-competitor-intelligence-sidecar/index.md`

2. **Update with current session:**
   - Watchlist count and competitor names
   - Total ads tracked, winner count (30+ days active)
   - Last scrape date and result summary
   - Any notable findings (new winners detected, competitors added/removed, scrape issues)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if scrape was performed
   - `patterns.md` — Add any new observations about competitor strategies

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
