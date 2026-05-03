---
name: linkedin-comment-processor
description: Playwright harness for running the LinkedIn comment processor userscript
---

# LinkedIn Comment Processor Workflow

Run and debug a userscript that automates "comment X for Y" lead magnet responses on LinkedIn posts. The script scans comments for a keyword, DMs connected users, and replies publicly to non-connections.

## How It Works

- **Connected users (1st degree):** Opens their profile in a new tab, sends a DM via the chat bubble, then posts a randomly-selected follow-up comment reply (e.g. "Sent!")
- **Non-connected users (2nd/3rd):** Likes the comment and posts a randomly-selected public reply (e.g. "Thanks! Please connect so I can DM you the details.")
- **Message variations:** Both follow-up comments and non-connection replies support up to 3 message templates. A random template is chosen each time, making responses feel more natural. All variations are auto-detected as author follow-up comments for skip logic.
- **Already-handled threads:** Automatically skipped if any of your configured reply message variations are detected in the thread. If a previously non-connected user is now connected, they get processed for DM.
- **Cross-tab coordination:** Uses `localStorage` keys (`dmTask` / `dmTaskResult`) to pass DM instructions between the main tab and profile tabs
- **Activity Log:** A dark terminal-style panel at the bottom of the Comment Processor card shows real-time actions, warnings, and errors — including logs from DM tabs

## Actions

Present the user with these actions:

1. **[LC] Launch Comment Processor** — Configure and run the comment processor on a LinkedIn post
2. **[DB] Debug from Snapshot** — Read exported HTML/screenshots to diagnose and fix issues

---

### [LC] Launch Comment Processor

#### Steps

1. **Validate prerequisites**

   Confirm Playwright is installed:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/linkedin-comment-processor && npx playwright --version
   ```
   If not found, run:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/linkedin-comment-processor && npm install && npx playwright install chromium
   ```

2. **Get the LinkedIn session cookie**

   Ask: "Paste your LinkedIn `li_at` session cookie. Here's how to get it:"

   ```
   1. Open LinkedIn in your regular browser (Chrome/Edge/Firefox)
   2. Press F12 to open Developer Tools
   3. Go to the Application tab (Chrome/Edge) or Storage tab (Firefox)
   4. In the left sidebar, expand Cookies > https://www.linkedin.com
   5. Find the cookie named "li_at"
   6. Copy the full Value (it's a long string starting with "AQ...")
   ```

3. **Get the LinkedIn post URL**

   Ask: "What LinkedIn post URL do you want to process?"

   - If user says "feed" or similar, use `https://www.linkedin.com/feed/`
   - Otherwise use the URL they provide

4. **Choose browser mode**

   Ask: "Do you want to run this in a visible Chromium window or headless?"

   - **Visible (headed)** — You can watch the automation in real time, interact with the UI card (Analyze / Process / Stop & Export), and manually intervene. Recommended for first runs and debugging.
   - **Headless** — Runs in the background without opening a browser window. The script auto-clicks Process on page load. Useful once config is stable and you don't need to watch.

5. **Configure the comment processor**

   **If headed mode:** Skip detailed configuration. Tell the user:
   - "You can configure everything in the browser UI — keyword, DM message, reply templates, and follow-up tags are all editable in the Comment Processor card that appears at the bottom-left of the page. Settings persist in localStorage between runs."

   **If headless mode:** The user can't interact with the UI, so walk through each setting here.

   Read the current CONFIG object from `content-plugin/skills/5-publisher/workflows/linkedin-comment-processor/userscript.js` (near the top of the file) to show current defaults.

   Walk through each setting, presenting the current value and asking the user to confirm or change it:

   **a. Search Keyword** (CONFIG.keyword)
   - "What keyword should trigger processing? Current: `{current_value}`"

   **b. DM Message for Connected Users** (CONFIG.msgConnected)
   - "What DM message should be sent to 1st-degree connections? Current: `{current_value}`"

   **c. Comment Replies for Non-Connections** (CONFIG.msgsNotConnected + CONFIG.enableMsgNotConnected)
   - "What public replies should be posted for non-connections? You can provide up to 3 variations (a random one is chosen each time). Current: `{current_values}` (enabled: {enabled})"
   - Say "disable" to skip non-connection replies
   - All variations are auto-detected as author follow-up comments for skip logic

   **d. Follow-up Comments After DM** (CONFIG.msgsAfterDM + CONFIG.enableMsgAfterDM)
   - "What follow-up comments should be posted after a successful DM? You can provide up to 3 variations (a random one is chosen each time). Current: `{current_values}` (enabled: {enabled})"
   - Say "disable" to skip follow-up comments
   - All variations are auto-detected as author follow-up comments for skip logic

   **e. Author Follow-up Keywords** (CONFIG.followUpTags)
   - "Any extra keywords to detect already-handled threads? Current: `{current_value}`"
   - Comma-separated list, or "skip" for none
   - Note: All configured reply message variations (msgsAfterDM, msgsNotConnected) are auto-checked — you only need keywords here for custom replies you've posted manually

   After collecting all inputs, update ONLY the CONFIG values in `content-plugin/skills/5-publisher/workflows/linkedin-comment-processor/userscript.js`. Do not modify any other code.

6. **Present launch summary**

   **If headed mode:**
   ```
   LinkedIn Comment Processor — Ready to Launch

   Post URL:  {url}
   Browser:   Headed (visible Chromium)
   Session:   li_at cookie provided
   Config:    Set via browser UI
   ```
   - A Chromium browser will open, already authenticated via your li_at cookie.
   - The Comment Processor card appears at the bottom-left of the post page.
   - Configure keyword, messages, and tags in the UI, then click **Process**.
   - Click **Stop & Export** or press **Ctrl+C** to stop and export a debug snapshot.
   - The Activity Log panel shows real-time progress including DM tab logs.

   **If headless mode:**
   ```
   LinkedIn Comment Processor — Ready to Launch

   Post URL:       {url}
   Browser:        Headless
   Keyword:        {keyword}
   DM Message:     {msgConnected (truncated to 50 chars)}
   Non-Connection: {msgsNotConnected count}x variations ({enabled/disabled})
   Follow-up:      {msgsAfterDM count}x variations ({enabled/disabled})
   Skip Keywords:  {followUpTags or "auto (all reply variations)"}
   Session:        li_at cookie provided
   ```

   Ask: "Ready to launch? (yes/no)"

7. **Launch the browser**

   For headed mode:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/linkedin-comment-processor && npx tsx run.ts --url "<url>" --cookie "<li_at>"
   ```

   For headless mode:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/linkedin-comment-processor && npx tsx run.ts --url "<url>" --cookie "<li_at>" --headless
   ```

   Run this as a background task. The browser stays open until the user clicks Stop & Export or presses Ctrl+C.

8. **After exit**

   When the process completes, check the output and the latest snapshot:
   ```bash
   ls content-plugin/skills/5-publisher/workflows/linkedin-comment-processor/debug/
   ```

   Ask: "How did it go? Would you like to:"
   - **[DB]** Debug from the snapshot
   - **[LC]** Re-run with different settings
   - **[X]** Done

---

### [DB] Debug from Snapshot

Read exported HTML/screenshots to diagnose issues, then fix the userscript.

#### Steps

1. **Identify the latest snapshot**

   ```bash
   ls -lt content-plugin/skills/5-publisher/workflows/linkedin-comment-processor/debug/ | head -5
   ```

   If multiple snapshots exist, ask which one to examine.

2. **Read the Activity Log from the HTML**

   The Activity Log is inside `#li-cp-devlog` in the DOM export. Search for it:
   ```
   content-plugin/skills/5-publisher/workflows/linkedin-comment-processor/debug/{timestamp}/tab-0.html
   ```

   The log entries use color coding:
   - Green (`rgb(74, 222, 128)`) = actions taken (e.g. "Liked comment", "Reply posted", "DM result: SUCCESS")
   - Yellow (`rgb(250, 204, 21)`) = warnings (e.g. "Reply button not found", "Skipping — already handled")
   - Red (`rgb(248, 113, 113)`) = errors (e.g. "replyPublicly error", "Read comments error")
   - Grey = info/debug messages

3. **Inspect the DOM for selector issues**

   Key selectors to check against the actual HTML:
   - Comment elements: `article.comments-comment-entity`
   - Reply button: `button.comments-comment-social-bar__reply-action-button--cr` or `button[aria-label*="Reply"]`
   - Like button: `button.social-actions-button.react-button__trigger[aria-pressed="false"]`
   - Reply editor: `.ql-editor[contenteditable="true"]`
   - Submit button: `button.comments-comment-box__submit-button--cr`
   - Author badge: `.comments-comment-meta__badge` (text: "Author")
   - Profile link: `a[data-view-name="comment-actor-description"]`
   - Connection degree: `.comments-comment-meta__description-title`
   - DM message button: `a[data-view-name="profile-primary-message"]`
   - Chat bubble composer: `.msg-form__contenteditable`

4. **Read the screenshot** (supplementary)

   View the screenshot to understand the visual state.

5. **Diagnose and fix**

   Common failure patterns:
   - **"Read comments error: X is not defined"** — Variable name typo in the userscript. Check the error message for the exact variable.
   - **"Reply button not found"** — LinkedIn changed the reply button class. Check the DOM for the actual selector.
   - **"Reply textbox not found after 8 attempts"** — The reply editor didn't open. Check if the reply button click is registering and if the editor has a different container structure.
   - **"commentReply execCommand: FAILED"** — The text insertion method failed. Check if the editor is a `contenteditable` div.
   - **DM not sending** — Check the cross-tab logs (replayed in the Activity Log with `[DM]` prefix). Common: message button selector changed, chat bubble not found, composer not receiving text.
   - **Bot detection / CAPTCHA** — Delete `.browser-data/` and re-authenticate with a fresh cookie.
   - **Processing complete with 0 comments** — Check keyword match (case-sensitive in the UI input), and check that comments are loaded (scroll count in the log).

   Edit `content-plugin/skills/5-publisher/workflows/linkedin-comment-processor/userscript.js` to update selectors or logic.

   After fixing, ask: "Want to re-run with [LC]?"

---

## Architecture

```
run.ts                  — Playwright launcher (persistent context, cookie auth, debug export)
userscript.js           — The comment processor (~1900 lines, injected into every LinkedIn page)
.browser-data/          — Chromium profile with session cookies (gitignored)
debug/{timestamp}/      — DOM + screenshot snapshots (gitignored)
```

### CLI flags

| Flag | Description |
|------|-------------|
| `--url <url>` | LinkedIn post URL to navigate to (default: feed) |
| `--cookie <li_at>` | LinkedIn session cookie for authentication |
| `--headless` | Run without visible browser window |

### Skip logic (already-handled threads)

The script automatically skips threads where you've already replied. No manual configuration needed — all message variations are auto-checked:

- **Connected users:** Skipped if your reply ends with any `msgsAfterDM` variation or matches a `followUpTag`
- **Non-connected users:** Skipped if your reply ends with any `msgsNotConnected` or `msgsAfterDM` variation or matches a `followUpTag`
- **Upgraded connections:** If a user was previously non-connected (has any `msgsNotConnected` reply) but is now 1st degree, they are NOT skipped — they get processed for DM

### Timing

Action delays use randomised intervals to appear human-like:
- Between actions: 1–2.5 seconds (`perActionDelayMs`)
- Typing speed: 3–10ms per character (`typingDelayMsPerChar`)
- All intermediate waits use `randBetween()` for natural variation

### Cross-tab DM coordination

1. Main tab saves `dmTask` to localStorage (profile URL + message)
2. Profile tab opens, reads `dmTask`, sends DM via chat bubble
3. Profile tab writes `dmTaskResult` to localStorage (success/fail + logs)
4. Main tab polls `dmTaskResult`, replays DM logs into Activity Log, closes profile tab

### Text insertion

Both DM and comment reply use `document.execCommand('insertText')` to trigger React/LinkedIn state updates. Fallback chain: execCommand → clipboard paste simulation → innerHTML.
