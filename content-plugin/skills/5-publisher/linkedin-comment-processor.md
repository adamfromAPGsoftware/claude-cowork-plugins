---
name: linkedin-comment-processor
description: Automate "comment X for Y" lead magnet DMs and replies on LinkedIn posts
menu-code: LC
---

# [LC] LinkedIn Comment Processor

## Purpose

Run and debug a userscript that automates "comment X for Y" lead magnet responses on LinkedIn posts. The script scans comments for a keyword, DMs connected users, and replies publicly to non-connections.

## How It Works

- **Connected users (1st degree):** Opens their profile in a new tab, sends a DM via the chat bubble, then posts a randomly-selected follow-up comment reply (e.g. "Sent!")
- **Non-connected users (2nd/3rd):** Likes the comment and posts a randomly-selected public reply (e.g. "Thanks! Please connect so I can DM you the details.")
- **Message variations:** Both follow-up comments and non-connection replies support up to 3 message templates. Random selection makes responses feel natural.
- **Already-handled threads:** Automatically skipped if any configured reply variations are detected.
- **Cross-tab coordination:** Uses localStorage keys for DM instructions between main tab and profile tabs.

---

## Actions

**[LC] Launch Comment Processor** — Configure and run on a LinkedIn post
**[DB] Debug from Snapshot** — Read exported HTML/screenshots to diagnose issues

---

## Launch Comment Processor

### Step 1: Validate Prerequisites

Confirm Playwright installed:
```bash
cd _bmad/custom/workflows/linkedin-comment-processor && npx playwright --version
```

### Step 2: Get LinkedIn Session Cookie

Ask for `li_at` session cookie. Explain how to find it (Developer Tools > Application > Cookies > linkedin.com > li_at).

### Step 3: Get Post URL

Accept the LinkedIn post URL to process.

### Step 4: Choose Browser Mode

- **Headed (visible)** — Watch automation in real time, interact with UI card, recommended for first runs
- **Headless** — Background execution, auto-clicks Process on load

### Step 5: Configure (Headless only)

For headless mode, walk through settings:
- **Search keyword** — trigger word for processing
- **DM message** — message sent to 1st-degree connections
- **Non-connection replies** — up to 3 variations
- **Follow-up comments** — up to 3 variations after DM
- **Author follow-up keywords** — extra skip detection keywords

Update CONFIG in `userscript.js`.

### Step 6: Launch

```bash
# Headed:
cd _bmad/custom/workflows/linkedin-comment-processor && npx tsx run.ts --url "<url>" --cookie "<li_at>"

# Headless:
cd _bmad/custom/workflows/linkedin-comment-processor && npx tsx run.ts --url "<url>" --cookie "<li_at>" --headless
```

Run as background task.

### Step 7: After Exit

Check debug output. Offer: [DB] Debug, [LC] Re-run, [X] Done.

---

## Debug from Snapshot

1. Identify latest snapshot in `debug/` directory
2. Read Activity Log from `#li-cp-devlog` in DOM export (color-coded: green=actions, yellow=warnings, red=errors)
3. Inspect DOM for selector issues against known selectors
4. View screenshot for visual state
5. Diagnose and fix common patterns:
   - Variable name typos
   - LinkedIn selector changes
   - Reply editor not opening
   - DM coordination failures
   - Bot detection/CAPTCHA
6. Edit `userscript.js` to fix issues
7. Offer to re-run

---

## Architecture

```
run.ts              — Playwright launcher (persistent context, cookie auth, debug export)
userscript.js       — Comment processor (~1900 lines, injected into every LinkedIn page)
.browser-data/      — Chromium profile with session cookies (gitignored)
debug/{timestamp}/  — DOM + screenshot snapshots (gitignored)
```

## Timing

Action delays use randomised intervals: 1-2.5s between actions, 3-10ms per character typing.
