---
name: save-memory
description: Save current session progress to sidecar memory
menu-code: SM
---

# Save Memory

Save the current session state to sidecar memory for continuity across sessions.

## Process

1. **Read current memory** — Load `{project-root}/_bmad/_memory/bmad-apg-mkt-campaign-planner-sidecar/index.md`

2. **Update with current session:**
   - Campaigns created or modified this session
   - Market reports generated
   - Strategies built
   - Performance reviews completed
   - Key decisions made

3. **Write updated index.md** with current state.

4. **Append to chronology.md** — Add session entry:
   ```
   ## {timestamp}
   - Action: {what was done}
   - Campaigns: {which campaigns were touched}
   - Outcome: {result}
   ```

5. **Confirm:** "Session progress saved to memory."
