---
name: tiktok-comment-processor
description: Playwright harness for running the TikTok comment processor userscript
---

# TikTok Comment Processor Workflow

Run and debug a userscript that automates "comment X for Y" lead magnet responses on TikTok videos. The script scans comments for a keyword, DMs followers the Skool link, and replies publicly to non-followers asking them to follow + DM you.

## How It Works

- **Followers:** Opens their profile in a new tab, sends a DM with the Skool community link (`https://{YOUR_COMMUNITY_URL}`), then posts a randomly-selected follow-up comment (e.g. "Sent!")
- **Non-followers:** Posts a randomly-selected public reply asking them to follow and DM you (e.g. "Follow me and shoot me a DM and I'll send you the link!") — the Skool link is never shared publicly
- **Message variations:** Both follow-up comments and non-follower replies support up to 3 message templates. A random template is chosen each time, making responses feel more natural. All variations are auto-detected for skip logic.
- **Already-handled threads:** Automatically skipped if any of your configured reply message variations are detected in the thread
- **Cross-tab coordination:** Uses `localStorage` keys (`tiktok_cp_dmTask` / `tiktok_cp_dmTaskResult`) to pass DM instructions between the main tab and profile tabs
- **Activity Log:** A dark terminal-style panel at the bottom of the Comment Processor card shows real-time actions, warnings, and errors — including logs from DM tabs
- **Rate limiting:** 45s-2min between replies, 10/hour, 25/session, with 5-10min cooldowns every 5 replies

## Funnel Strategy

| Commenter Status | Action |
|-----------------|--------|
| **Follows you** | DM them the Skool link directly (cross-tab: open profile → send DM) |
| **Doesn't follow you** | Public reply: "Follow me and send me a DM and I'll send you the link!" (variations) |
| **Already handled** | Skip (detected via skip logic) |

## Actions

Present the user with these actions:

1. **[TC] Launch TikTok Comment Processor** — Configure and run the comment processor on a single TikTok video
2. **[PA] Process All Videos** — Auto-iterate all your TikTok videos (newest first), auto-detecting the keyword per video
3. **[DB] Debug from Snapshot** — Read exported HTML/screenshots to diagnose and fix issues

---

### [TC] Launch TikTok Comment Processor

#### Steps

1. **Validate prerequisites**

   Confirm Playwright is installed:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/tiktok-comment-processor && npx playwright --version
   ```
   If not found, run:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/tiktok-comment-processor && pnpm install && npx playwright install chromium
   ```

2. **Get the TikTok session cookie**

   Ask: "Paste your TikTok `sessionid` cookie. Here's how to get it:"

   ```
   1. Open TikTok in your regular browser (Chrome/Edge/Firefox)
   2. Press F12 to open Developer Tools
   3. Go to the Application tab (Chrome/Edge) or Storage tab (Firefox)
   4. In the left sidebar, expand Cookies > https://www.tiktok.com
   5. Find the cookie named "sessionid"
   6. Copy the full Value
   ```

   Optionally also ask for `sid_tt` and `tt_csrf_token` cookies for better session stability.

3. **Get the TikTok video URL**

   Ask: "What TikTok video URL do you want to process?"

   - Format: `https://www.tiktok.com/@username/video/1234567890`
   - If user just provides a username, ask for the specific video URL

4. **Choose browser mode**

   Ask: "Do you want to run this in a visible Chromium window or headless?"

   - **Visible (headed)** — You can watch the automation in real time, interact with the UI card (Analyze / Process / Stop & Export), and manually intervene. Recommended for first runs and debugging.
   - **Headless** — Runs in the background without opening a browser window. The script auto-clicks Process on page load. Useful once config is stable and you don't need to watch.

5. **Configure the comment processor**

   **If headed mode:** Skip detailed configuration. Tell the user:
   - "You can configure everything in the browser UI — keyword, DM message, reply templates, and follow-up tags are all editable in the Comment Processor card that appears at the bottom-left of the page. Settings persist in localStorage between runs."

   **If headless mode:** The user can't interact with the UI, so walk through each setting here.

   Read the current CONFIG object from `content-plugin/skills/5-publisher/workflows/tiktok-comment-processor/userscript.js` (near the top of the file) to show current defaults.

   Walk through each setting, presenting the current value and asking the user to confirm or change it:

   **a. Search Keyword** (CONFIG.keyword)
   - "What keyword should trigger processing? Current: `{current_value}`"

   **b. DM Message for Followers** (CONFIG.msgFollower)
   - "What DM message should be sent to followers? Current: `{current_value}`"

   **c. Comment Replies for Non-Followers** (CONFIG.msgsNonFollower)
   - "What public replies should be posted for non-followers? You can provide up to 3 variations (a random one is chosen each time). Current: `{current_values}`"
   - All variations are auto-detected as author follow-up comments for skip logic

   **d. Follow-up Comments After DM** (CONFIG.msgsAfterDM + CONFIG.enableMsgAfterDM)
   - "What follow-up comments should be posted after a successful DM? You can provide up to 3 variations (a random one is chosen each time). Current: `{current_values}` (enabled: {enabled})"
   - Say "disable" to skip follow-up comments
   - All variations are auto-detected as author follow-up comments for skip logic

   **e. Author Follow-up Keywords** (CONFIG.followUpTags)
   - "Any extra keywords to detect already-handled threads? Current: `{current_value}`"
   - Comma-separated list, or "skip" for none
   - Note: All configured reply message variations (msgsAfterDM, msgsNonFollower) are auto-checked — you only need keywords here for custom replies you've posted manually

   After collecting all inputs, update ONLY the CONFIG values in `content-plugin/skills/5-publisher/workflows/tiktok-comment-processor/userscript.js`. Do not modify any other code.

6. **Present launch summary**

   **If headed mode:**
   ```
   TikTok Comment Processor — Ready to Launch

   Video URL: {url}
   Browser:   Headed (visible Chromium)
   Session:   sessionid cookie provided
   Config:    Set via browser UI
   ```
   - A Chromium browser will open, already authenticated via your sessionid cookie.
   - The Comment Processor card appears at the bottom-left of the video page.
   - Configure keyword, messages, and tags in the UI, then click **Process**.
   - Click **Stop & Export** or press **Ctrl+C** to stop and export a debug snapshot.
   - The Activity Log panel shows real-time progress including DM tab logs.
   - Rate limit display shows session/hourly counts and cooldown timers.

   **If headless mode:**
   ```
   TikTok Comment Processor — Ready to Launch

   Video URL:      {url}
   Browser:        Headless
   Keyword:        {keyword}
   DM Message:     {msgFollower (truncated to 50 chars)}
   Non-Follower:   {msgsNonFollower count}x variations
   Follow-up:      {msgsAfterDM count}x variations ({enabled/disabled})
   Skip Keywords:  {followUpTags or "auto (all reply variations)"}
   Session:        sessionid cookie provided
   ```

   Ask: "Ready to launch? (yes/no)"

7. **Launch the browser**

   For headed mode:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/tiktok-comment-processor && npx tsx run.ts --url "<url>" --cookie "<sessionid>"
   ```

   For headless mode:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/tiktok-comment-processor && npx tsx run.ts --url "<url>" --cookie "<sessionid>" --headless
   ```

   If additional cookies were provided:
   ```bash
   cd content-plugin/skills/5-publisher/workflows/tiktok-comment-processor && npx tsx run.ts --url "<url>" --cookie "<sessionid>" --sid "<sid_tt>" --csrf "<tt_csrf_token>"
   ```

   Run this as a background task. The browser stays open until the user clicks Stop & Export or presses Ctrl+C.

8. **After exit**

   When the process completes, check the output and the latest snapshot:
   ```bash
   ls content-plugin/skills/5-publisher/workflows/tiktok-comment-processor/debug/
   ```

   Ask: "How did it go? Would you like to:"
   - **[DB]** Debug from the snapshot
   - **[TC]** Re-run with different settings
   - **[X]** Done

---

### [PA] Process All Videos (Profile Mode)

Automatically iterate through all your TikTok videos (newest first), auto-detecting the CTA keyword per video from the most commonly repeated short comment.

#### Steps

1. **Validate prerequisites** (same as [TC] step 1)

2. **Get the TikTok session cookie** (same as [TC] step 2)

3. **Get your TikTok profile URL**

   Ask: "What's your TikTok profile URL?"
   - Format: `https://www.tiktok.com/@username`

4. **Configure messages**

   The keyword is auto-detected per video, but you still need to set the DM message and reply templates:
   - "What DM message should be sent to followers?" (default: Skool community link)
   - "What public replies for non-followers?" (up to 3 variations)

   These can also be configured in the browser UI before clicking "Scan & Process All".

5. **Launch**

   ```bash
   cd content-plugin/skills/5-publisher/workflows/tiktok-comment-processor && npx tsx run.ts --url "https://www.tiktok.com/@username" --cookie "<sessionid>"
   ```

   The Profile Mode UI card will appear on the profile page. It will:
   - Scroll the profile to discover all videos
   - Navigate to each video (newest first)
   - Auto-detect the keyword from comment patterns
   - Process each video using the standard comment processor
   - Skip videos with no clear keyword pattern
   - Show progress (processed / skipped / total)

6. **After completion**

   Ask: "How did it go? Would you like to:"
   - **[DB]** Debug from snapshot
   - **[PA]** Re-run profile mode
   - **[TC]** Process a specific video
   - **[X]** Done

---

### [DB] Debug from Snapshot

Read exported HTML/screenshots to diagnose issues, then fix the userscript.

#### Steps

1. **Identify the latest snapshot**

   ```bash
   ls -lt content-plugin/skills/5-publisher/workflows/tiktok-comment-processor/debug/ | head -5
   ```

   If multiple snapshots exist, ask which one to examine.

2. **Read the Activity Log from the HTML**

   The Activity Log is inside `#tt-cp-devlog` in the DOM export. Search for it:
   ```
   content-plugin/skills/5-publisher/workflows/tiktok-comment-processor/debug/{timestamp}/tab-0.html
   ```

   The log entries use color coding:
   - Green (`rgb(74, 222, 128)`) = actions taken (e.g. "Liked comment", "Reply posted", "DM result: SUCCESS")
   - Yellow (`rgb(250, 204, 21)`) = warnings (e.g. "Reply button not found", "Skipping — already handled")
   - Red (`rgb(248, 113, 113)`) = errors (e.g. "replyPublicly error", "Read comments error")
   - Grey = info/debug messages

3. **Inspect the DOM for selector issues**

   Key selectors to check against the actual HTML:
   - Comment list: `div[data-e2e="comment-list"]`
   - Comment item: `div[data-e2e="comment-item"]`
   - Comment text: `span[data-e2e="comment-level-1"]`
   - Username: `a[data-e2e="comment-username-1"]`
   - Author badge: `span[data-e2e="comment-author-tag"]`
   - Reply button: `span[data-e2e="comment-reply-1"]`, `p[class*="PReplyLabel"]`
   - Reply input: `div[data-e2e="comment-input"] div[contenteditable="true"]`
   - Submit: `div[data-e2e="comment-post"]`, `button[data-e2e="comment-post"]`
   - Follow button: `button[data-e2e="follow-button"]`
   - Follow back button: `button[data-e2e="follow-back-button"]`
   - Friends button: `button[data-e2e="friends-button"]`
   - DM button: `a[data-e2e="message-icon"]`, `button[data-e2e="profile-message"]`
   - Chat composer: `div[contenteditable="true"]` inside message container
   - Send button: `button[data-e2e="message-send"]`

4. **Read the screenshot** (supplementary)

   View the screenshot to understand the visual state.

5. **Diagnose and fix**

   Common failure patterns:
   - **"Read comments error: X is not defined"** — Variable name typo in the userscript. Check the error message for the exact variable.
   - **"Reply button not found"** — TikTok changed a selector. Check the DOM for the actual element.
   - **"Reply textbox not found after N attempts"** — The reply editor didn't open. Check if the reply button click is registering.
   - **"commentReply execCommand: FAILED"** — The text insertion method failed. Check if the editor is a `contenteditable` div.
   - **DM not sending** — Check the cross-tab logs (replayed in the Activity Log with `[DM]` prefix). Common: message button selector changed, chat not opening, composer not receiving text.
   - **Bot detection / CAPTCHA** — Delete `.browser-data/` and re-authenticate with a fresh cookie.
   - **Processing complete with 0 comments** — Check keyword match (case-insensitive in the UI input), and check that comments are loaded (scroll count in the log).
   - **"Follower check failed"** — Profile page may not have loaded. Check for CAPTCHA or rate limiting on profile visits.
   - **Rate limit hit** — The script enforces its own limits. If TikTok is rate limiting, increase `replyIntervalMs` and `perActionDelayMs` in CONFIG.

   Edit `content-plugin/skills/5-publisher/workflows/tiktok-comment-processor/userscript.js` to update selectors or logic.

   After fixing, ask: "Want to re-run with [TC]?"

---

## Architecture

```
run.ts                  — Playwright launcher (persistent context, cookie auth, anti-detection, debug export)
userscript.js           — The comment processor (~1400 lines, injected into every TikTok page)
.browser-data/          — Chromium profile with session cookies (gitignored)
debug/{timestamp}/      — DOM + screenshot snapshots (gitignored)
```

### CLI flags

| Flag | Description |
|------|-------------|
| `--url <url>` | TikTok video URL to navigate to (default: tiktok.com) |
| `--cookie <sessionid>` | TikTok session cookie for authentication |
| `--sid <sid_tt>` | Optional additional session cookie for stability |
| `--csrf <tt_csrf_token>` | Optional CSRF token cookie |
| `--headless` | Run without visible browser window |

### Skip logic (already-handled threads)

The script automatically skips threads where you've already replied. No manual configuration needed — all message variations are auto-checked:

- **Followers:** Skipped if your reply ends with any `msgsAfterDM` variation or matches a `followUpTag`
- **Non-followers:** Skipped if your reply ends with any `msgsNonFollower` or `msgsAfterDM` variation or matches a `followUpTag`
- **Upgraded followers:** If a user was previously a non-follower (has any `msgsNonFollower` reply) but now follows you, they are NOT skipped — they get processed for DM

### Timing & Rate Limits

Action delays use randomised intervals to appear human-like and respect TikTok's stricter bot detection:
- Between actions: 3–8 seconds (`perActionDelayMs`)
- Typing speed: 15–40ms per character (`typingDelayMsPerChar`)
- Between replies: 45s–2min (`replyIntervalMs`)
- Per session: 25 replies max (`maxRepliesPerSession`)
- Per hour: 10 replies max (`maxRepliesPerHour`)
- Cooldown: 5–10min every 5 replies (`sessionCooldownAfter`, `sessionCooldownMs`)

### Cross-tab DM coordination

1. Main tab saves `tiktok_cp_dmTask` to localStorage (profile URL + message)
2. Profile tab opens, reads `tiktok_cp_dmTask`, clicks DM button, sends message
3. Profile tab writes `tiktok_cp_dmTaskResult` to localStorage (success/fail + logs)
4. Main tab polls `tiktok_cp_dmTaskResult`, replays DM logs into Activity Log, closes profile tab

### Text insertion

Both DM and comment reply use `document.execCommand('insertText')` to trigger React/TikTok state updates. Fallback chain: execCommand → clipboard paste simulation → direct value set with input event.

### Follower detection

For each keyword commenter, the script opens their profile in a new tab and checks the follow button:
- "Follow back" → they follow you (one-way: them → you)
- "Friends" → mutual followers
- "Follow" → they don't follow you

Both "Follow back" and "Friends" are treated as followers eligible for DM.
