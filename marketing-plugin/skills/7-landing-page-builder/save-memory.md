---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-landing-page-builder-sidecar/index.md`

2. **Update with current session:**
   - Last deployment date and campaign summary (campaign ID, domain, template used)
   - Any notable findings (template issues, tracking verification results, Cloudflare API notes)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if generation or deployment was performed

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
