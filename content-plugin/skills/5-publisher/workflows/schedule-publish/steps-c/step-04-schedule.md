---
name: 'step-04-schedule'
description: 'Present final summary, get user confirmation, then submit scheduled posts via Buffer MCP'

nextStepFile: './step-05-confirm.md'
---

# Step 4: Schedule via Buffer

## STEP GOAL:

To present a final summary of everything that will be scheduled, get explicit user confirmation, then use the Buffer MCP to schedule the post(s) across the selected platforms. Handle success and failure per platform.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a distribution logistics specialist — meticulous about confirmation before action
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Nothing goes live without explicit user approval

### Step-Specific Rules:

- 🎯 Focus ONLY on confirmation and scheduling via Buffer MCP
- 🚫 FORBIDDEN to call Buffer MCP without explicit user confirmation
- 🚫 FORBIDDEN to modify calendar files in this step — that's step 05
- 💬 Present clear summary, wait for explicit go-ahead
- 🔄 Handle partial failures gracefully — report per-platform status

## EXECUTION PROTOCOLS:

- 🎯 Present final summary for user review
- 💾 Call Buffer MCP only after user confirms
- 📖 Track success/failure per platform
- 🚫 Never proceed without explicit confirmation

## CONTEXT BOUNDARIES:

- Available: Formatted content per platform, selected accounts, publish date/time from steps 1-3
- This step SENDS — calls the Buffer MCP to schedule posts
- Calendar updates happen in step 05, not here
- Must handle API errors and partial failures

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Present Final Summary

"**Final scheduling summary — please review before I send:**

| # | Platform | Account | Scheduled Date/Time | Content Preview |
|---|----------|---------|---------------------|-----------------|
| 1 | {platform} | @{handle} | {date} {time} | {first 60 chars of formatted content}... |

**Total posts to schedule:** {count}
**Scheduling via:** Buffer MCP

This action will submit the above to Buffer for scheduling. Once scheduled, posts will go live at the specified times.

**Confirm scheduling?**
**[Y]** Yes — schedule all
**[X]** Cancel — abort scheduling"

Wait for user input.

**IF X (Cancel):**
"**Scheduling cancelled. No posts were submitted.**"
End workflow.

**IF Any other (not Y):** Help user, redisplay confirmation.

### 2. Attach Media (if applicable)

**Only execute this section after user confirms with Y.**

If the post includes media (images, videos, or documents like PDF carousels), attach them to the post creation call via the Buffer MCP media fields.

For thumbnail discovery on short-form content, check:
1. `{project_folder}/video-editor/short-form/thumbnails/sf-{NN}-thumbnail.png` (primary)
2. `{project_folder}/creative-director/short-form/{video-title-slug}/sf-{NN}.png` (fallback)
3. No thumbnail found → platform auto-generates cover frame

### 3. Call Buffer MCP

"**Submitting to Buffer...**"

Use the Buffer MCP to schedule each post:

```
mcp__buffer__use_buffer_api(
  action: "createPost",
  profileIds: [channel_ids for selected platforms],
  text: main post text,
  scheduledAt: ISO 8601 UTC datetime,
  media: [file paths or URLs for attachments]
)
```

For each platform, format content appropriately per the specs loaded in Phase 1 (platform-specs.md). Key platform rules:
- LinkedIn: 3,000 chars max, external links in first comment
- X/Twitter: 280 chars (free) / 25,000 chars (X Premium)
- Instagram: 2,200 chars, first comment for hashtags
- TikTok: privacy_level, content_preview_confirmed, express_consent_given required
- Threads: 500 chars — hard limit
- Bluesky: 300 chars — hard limit

For each selected platform/channel:
1. Call the Buffer MCP to schedule the formatted post
2. Capture the result — success or failure
3. Store any post IDs or confirmation details returned

### 4. Report Results

**If all platforms succeeded:**

"**All posts scheduled successfully.**

| # | Platform | Account | Status | Buffer Post ID |
|---|----------|---------|--------|----------------|
| 1 | {platform} | @{handle} | Scheduled | {id} |

**Proceeding to calendar update and confirmation...**"

**If some platforms failed (partial failure):**

"**Partial scheduling result — some posts failed.**

| # | Platform | Account | Status | Detail |
|---|----------|---------|--------|--------|
| 1 | {platform_a} | @{handle_a} | Scheduled | ID: {id} |
| 2 | {platform_b} | @{handle_b} | FAILED | {error message} |

**Options for failed platform(s):**
**[R]** Retry failed — attempt again
**[S]** Skip failed — proceed with successful posts only
**[X]** Cancel all — abort entire scheduling"

Wait for user input.

**IF R:** Retry via Buffer MCP for failed platforms only, then re-report.
**IF S:** Proceed with successful posts only.
**IF X:** "**All scheduling cancelled.**" End workflow.

**If all platforms failed:**

"**Scheduling failed — no posts were submitted.**

**Possible causes:**
- Buffer API token may be invalid or expired
- Social account may have been disconnected from Buffer
- Content may violate platform character limits

**Options:**
**[R]** Retry all
**[X]** Cancel — abort scheduling"

### 5. Proceed to Calendar Update

Once at least one platform has been successfully scheduled:

Display: **[C]** Continue to Calendar Update & Confirmation

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: Help user, then redisplay menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN at least one post has been successfully scheduled via Buffer MCP and user selects 'C' will you load and read fully `step-05-confirm.md` to execute the calendar update and confirmation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Final summary presented clearly before any MCP call
- User explicitly confirmed before scheduling
- Buffer MCP called for each selected platform
- Per-platform success/failure tracked and reported
- Retry offered for failed platforms
- Partial success handled gracefully
- Proceeded only with at least one successful schedule

### ❌ SYSTEM FAILURE:

- Calling Buffer MCP without user confirmation
- Not reporting per-platform status
- Ignoring MCP failures silently
- Updating calendar in this step (that's step 05)
- Proceeding with zero successful schedules

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
