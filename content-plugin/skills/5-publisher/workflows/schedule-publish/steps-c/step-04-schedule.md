---
name: 'step-04-schedule'
description: 'Present final summary, get user confirmation, then submit scheduled posts to Late.dev API'

nextStepFile: './step-05-confirm.md'
---

# Step 4: Schedule via Late.dev

## STEP GOAL:

To present a final summary of everything that will be scheduled, get explicit user confirmation, then call the Late.dev API to schedule the post(s) across the selected platforms. Handle success and failure per platform.

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

- 🎯 Focus ONLY on confirmation and API scheduling
- 🚫 FORBIDDEN to call the Late.dev API without explicit user confirmation
- 🚫 FORBIDDEN to modify calendar files in this step — that's step 05
- 💬 Present clear summary, wait for explicit go-ahead
- 🔄 Handle partial failures gracefully — report per-platform status

## EXECUTION PROTOCOLS:

- 🎯 Present final summary for user review
- 💾 Call Late.dev API only after user confirms
- 📖 Track success/failure per platform
- 🚫 Never proceed without explicit confirmation

## CONTEXT BOUNDARIES:

- Available: Formatted content per platform, selected accounts, publish date/time from steps 1-3
- This step SENDS — calls the Late.dev API to schedule posts
- Calendar updates happen in step 05, not here
- Must handle API errors and partial failures

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Present Final Summary

"**Final scheduling summary — please review before I send:**

| # | Platform | Account | Scheduled Date/Time | Content Preview | First Comment |
|---|----------|---------|---------------------|-----------------|:-------------:|
| 1 | {platform} | @{handle} | {date} {time} | {first 60 chars of formatted content}... | {yes/no} |

**Total posts to schedule:** {count}
**API endpoint:** `POST https://getlate.dev/api/v1/posts`

This action will submit the above to Late.dev for scheduling. Once scheduled, posts will go live at the specified times.

**Confirm scheduling?**
**[Y]** Yes — schedule all
**[X]** Cancel — abort scheduling"

Wait for user input.

**IF X (Cancel):**
"**Scheduling cancelled. No posts were submitted.**"
End workflow.

**IF Any other (not Y):** Help user, redisplay confirmation.

### 2. Upload Media (if applicable)

**Only execute this section after user confirms with Y.**

If the post includes media (images, videos, or documents like PDF carousels), upload them FIRST before creating the post.

**Media Upload:**
```bash
POST https://getlate.dev/api/v1/media
Authorization: Bearer {LATE_API_KEY}
Content-Type: multipart/form-data

# Field name MUST be "files" (not "file", "media", or "upload")
-F "files=@/path/to/file.pdf;type=application/pdf"
```

**Response:**
```json
{
  "files": [
    {
      "type": "document",
      "url": "https://media.getlate.dev/...",
      "filename": "file.pdf",
      "size": 403362,
      "mimeType": "application/pdf"
    }
  ]
}
```

Store the returned `url` — this is the publicly accessible URL to reference in `mediaItems` when creating the post.

### 2b. Discover and Upload Thumbnails (short-form content)

**Only for short-form video posts (Reels, Shorts, TikTok).**

Before creating the post, check if generated thumbnails exist for this video:

**Thumbnail Discovery Waterfall (check in order, use first match):**
```
1. {project_folder}/video-editor/short-form/thumbnails/sf-{NN}-thumbnail.png  ← PRIMARY (video editor output)
2. {project_folder}/creative-director/short-form/{video-title-slug}/sf-{NN}.png  ← FALLBACK (creative director output)
3. No thumbnail found → platform auto-generates cover frame
```

**If a thumbnail is found:**

1. **Upload via Late.dev media endpoint:**
```bash
POST https://getlate.dev/api/v1/media
Authorization: Bearer {LATE_API_KEY}
Content-Type: multipart/form-data

-F "files=@/path/to/sf-01.png;type=image/png"
```

2. **Store the returned `url`** — this becomes the thumbnail URL for platform-specific fields.

**Per-platform thumbnail attachment:**

| Platform | Field | How to attach | Custom image supported? |
|----------|-------|---------------|:----------------------:|
| **Instagram Reels** | `thumbnail` on `mediaItems` | Set `thumbnail` field on the mediaItems entry: `{"type":"video","url":"...mp4","thumbnail":"...jpg"}`. NOT in platformSpecificData — `instagramThumbnail` in pSD is silently dropped by the API. | YES (via mediaItems) |
| **TikTok** | `video_cover_timestamp_ms` | Set to `0` (first frame) — TikTok API does NOT support custom thumbnail images | NO |
| **YouTube** | `thumbnail` on `mediaItems` | Set `thumbnail` field on the mediaItems entry: `{"type":"video","url":"...mp4","thumbnail":"...jpg"}`. NOT in platformSpecificData. Shorts support is inconsistent but Late.dev passes it through. | YES (via mediaItems) |

**YouTube first comment:** Always include `firstComment` inside YouTube's `platformSpecificData`. Use for lead magnet CTAs and hashtags. Up to ~10,000 chars. For scheduled posts, the comment posts when the video goes live.

**Example — Instagram Reel with custom thumbnail:**
```json
{
  "platformSpecificData": {
    "contentType": "reels",
    "instagramThumbnail": "https://media.getlate.dev/media/..._sf-01.png"
  }
}
```

**If no thumbnail is found:** Proceed without — platforms will auto-generate a cover frame.

### 3. Call Late.dev API

"**Submitting to Late.dev...**"

**API Call:**
```
POST https://getlate.dev/api/v1/posts
Authorization: Bearer {LATE_API_KEY}
Content-Type: application/json

{
  "platforms": [
    {
      "platform": "linkedin",
      "accountId": "{accountId from GET /accounts response — the _id field}",
      "platformSpecificData": {
        "documentTitle": "{title for document posts}",
        "firstComment": "{first comment text — MUST go here, inside platformSpecificData}"
      }
    }
  ],
  "profileId": "{profileId from GET /accounts response — the profileId._id field}",
  "content": "{main post text — optional if all platforms have customContent}",
  "customContent": {
    "linkedin": "{linkedin-formatted text}",
    "twitter": "{twitter-formatted text}"
  },
  "mediaItems": [
    {"type": "document", "url": "{url from media upload response}"}
  ],
  "scheduledFor": "{ISO 8601 datetime — omit if using publishNow}",
  "publishNow": true,
  "title": "{content title/identifier}"
}
```

**CRITICAL FORMAT NOTES:**
- `platforms` is an ARRAY OF OBJECTS, not strings. Each must have `platform` and `accountId`.
- `platformSpecificData` goes INSIDE each platform object, not at the root level.
- `mediaItems` replaces the old `mediaUrls` — each item needs `type` and `url`.
- For document posts (LinkedIn PDF carousels): use `type: "document"` and include `documentTitle` in `platformSpecificData`.
- Documents CANNOT be mixed with images/videos in the same post.
- `firstComment` goes INSIDE `platformSpecificData` for each platform, NOT at the root level. Root-level `firstComment` is silently ignored.
- First comment is supported on LinkedIn, Instagram, Facebook, YouTube.
- Published posts CANNOT be deleted via API — only draft/scheduled posts can be deleted.
- Platform-specific required fields (TikTok, Pinterest, Reddit) go inside each platform's `platformSpecificData` object.

**Platform-specific data examples:**
```json
// TikTok (all 3 are REQUIRED)
{"privacy_level": "PUBLIC_TO_EVERYONE", "content_preview_confirmed": true, "express_consent_given": true}

// Pinterest (boardId is REQUIRED)
{"boardId": "{board ID from GET /accounts/{accountId}/pinterest-boards}"}

// Reddit (subreddit is REQUIRED)
{"subreddit": "{subreddit name without r/ prefix}"}

// LinkedIn document post
{"documentTitle": "{display title for the carousel}"}
```

For each selected platform/account:
1. Call the Late.dev API to schedule the formatted post at the specified date/time
2. Capture the API response — success or failure
3. Store any scheduling IDs, URLs, or confirmation details returned (especially `platformPostUrl` and post IDs)

### 3. Report Results

**If all platforms succeeded:**

"**All posts scheduled successfully.**

| # | Platform | Account | Status | Late.dev ID |
|---|----------|---------|--------|-------------|
| 1 | {platform} | @{handle} | Scheduled | {id or reference} |

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

**IF R (Retry):** Re-call API for failed platforms only, then re-report.
**IF S (Skip):** Proceed with successful posts only.
**IF X (Cancel all):** "**All scheduling cancelled.**" End workflow.
**IF Any other:** Help user, redisplay options.

**If all platforms failed:**

"**Scheduling failed — no posts were submitted.**

| # | Platform | Account | Status | Error |
|---|----------|---------|--------|-------|
| 1 | {platform} | @{handle} | FAILED | {error message} |

**Possible causes:**
- Late.dev API may be experiencing issues
- API key permissions may be insufficient
- Account connection may have expired

**Options:**
**[R]** Retry all — attempt again
**[X]** Cancel — abort scheduling"

Wait for user input.

**IF R:** Re-call API for all platforms, then re-report.
**IF X:** "**Scheduling cancelled.**" End workflow.

### 4. Proceed to Calendar Update

Once at least one platform has been successfully scheduled:

Display: **[C]** Continue to Calendar Update & Confirmation

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN at least one post has been successfully scheduled via Late.dev API and user selects 'C' will you load and read fully `step-05-confirm.md` to execute the calendar update and confirmation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Final summary presented clearly before any API call
- User explicitly confirmed before scheduling
- Late.dev API called for each selected platform
- Per-platform success/failure tracked and reported
- Retry offered for failed platforms
- Partial success handled gracefully
- Proceeded only with at least one successful schedule

### ❌ SYSTEM FAILURE:

- Calling Late.dev API without user confirmation
- Not reporting per-platform status
- Ignoring API failures silently
- Updating calendar in this step (that's step 05)
- Proceeding with zero successful schedules

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
