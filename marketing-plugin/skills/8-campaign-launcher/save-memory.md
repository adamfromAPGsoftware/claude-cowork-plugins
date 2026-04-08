---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Immediately persist the current session context to memory.

## Process

1. **Read current index.md** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-launcher-sidecar/index.md`

2. **Update with current session:**
   - Last deployment date and summary (campaign ID, entities created, status)
   - Any API operations performed (uploads, creates, activations, pauses)
   - Any errors encountered (API failures, rate limits)
   - Next steps to continue

3. **Write updated index.md** — Replace content with condensed, current version

4. **Checkpoint other files if needed:**
   - `chronology.md` — Add session summary if deployments were performed
   - `api-log.md` — Append any API write operations not yet logged

## Output

Confirm save with brief summary: "Memory saved. {brief-summary-of-what-was-updated}"
