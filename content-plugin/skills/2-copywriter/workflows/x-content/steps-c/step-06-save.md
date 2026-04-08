---
name: 'step-06-save'
description: 'Save approved X post with frontmatter and optionally schedule via Late.dev'

nextStepFile: './step-07-more.md'
---

# Step 6: Save & Schedule

## STEP GOAL:

To save the approved X post as a markdown file with structured YAML frontmatter, save any companion media files, and optionally schedule the post via the Late.dev API for the X account.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content operations specialist handling delivery and distribution for X
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring file management and API integration expertise, user brings scheduling preferences

### Step-Specific Rules:

- 🎯 Focus only on saving output and scheduling — content is already approved
- 🚫 FORBIDDEN to modify approved content without user request
- 💬 Confirm all file paths before saving
- 📋 All X deliverables live in one folder — post markdown and media assets

## EXECUTION PROTOCOLS:

- 🎯 Save files to correct output paths under `x/` subfolder
- 💾 Update derivative tracking in agent memories
- 📖 Update project status if project-based mode
- 🚫 FORBIDDEN to overwrite existing files without confirmation

## CONTEXT BOUNDARIES:

- Approved post content, thread tweets (if thread), hook, CTA all available from previous steps
- Media file is ALREADY confirmed on disk by step-05b — do not re-check or re-produce it
- Output paths use `x/` subfolder (not `linkedin/`)
- Late.dev API available for scheduling — use X account (not LinkedIn)
- Focus: File output and distribution — no content changes

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Determine Output Path

**Project mode:**
- Output folder: `{project_folder}/x/`
- Create directory if it doesn't exist

**Personal mode:**
- Ask user for output path or default to `{output_folder}/x/`
- Create directory if it doesn't exist

Generate post slug from hook text (lowercase, hyphens, max 50 chars).

### 2. Save Post Markdown

Save the approved post to `{output_path}/{post-slug}.md` with frontmatter:

```yaml
---
hook: "{selected_hook}"
format: {post_format}
content_category: {content_category}
source_mode: {source_mode}
target_icp: {target_icp}
cta_style: "{cta_style}"
cta_keyword: "{cta_keyword or null}"
lead_magnet: "{lead_magnet_path or null}"
media_path: "{media file path or none}"
thread_tweet_count: {tweet count or null}
status: draft
scheduled_at: null
created: {current_date}
---

{approved post body text}
```

**For thread format:** Include all tweets in the body, clearly numbered and separated:

```
Tweet 1:
{tweet 1 text}

---

Tweet 2:
{tweet 2 text}

...

Tweet N:
{final CTA tweet text}
```

### 3. Reference Companion Media

Media has already been produced and confirmed by step-05b. Simply resolve the confirmed media path from session context and record it in the post frontmatter `media_path` field:

- **Image:** `{x_path}{post_slug}-image.{ext}`
- **Video (existing):** path as confirmed in step-05b
- **Video (trimmed):** `{x_path}{post_slug}-video.mp4`
- **Text-only (single/thread/long post):** `media_path: none`

### 4. Update Derivative Tracking

Update the agent's memories with derivative tracking:
- Source project/topic → hook → format → content category → status
- This prevents angle duplication in future posts

If project mode: update `{project_folder}/project.md` with X content status.

### 5. Late.dev Scheduling (Optional)

Ask the user:

"**When should this post go live?**

**[N] Now** — publish immediately via Late.dev
**[T] Time** — schedule for a specific date and time
**[S] Skip** — save as draft only"

**If Skip:** Keep `status: draft`. Display: "Saved as draft." Proceed to section 6.

**If Now or Time:**

#### 5a. Read API key from .env

```bash
LATE_API_KEY=$(grep '^LATE_API_KEY=' "{project-root}/.env" | cut -d'=' -f2)
```

Verify `LATE_API_KEY` is non-empty. If empty, report the error and ask the user to check the `.env` file. Do NOT proceed with scheduling.

#### 5b. If Time — get schedule datetime

Ask: "**What date and time? (e.g. 2026-03-10 09:00 AEST)**"
Convert to ISO 8601 UTC. Store as `{scheduled_for}`.
If Now: set `"publishNow": true` and omit `scheduledFor`.

#### 5c. Fetch X accountId and confirm account

```bash
curl -s -X GET "https://getlate.dev/api/v1/accounts" \
  -H "Authorization: Bearer $LATE_API_KEY"
```

Filter the response to X/Twitter accounts only (`platform === "twitter"` or `platform === "x"` and `isActive === true`).

**If one X account found:** Present it for confirmation:

"**Posting to X:** {displayName} (@{username})
Is this the right account? **[Y]** Yes / **[N]** No"

- If Y: store `{accountId}` and `{profileId}`, proceed.
- If N: list all available X accounts and ask user to select by number.

**If multiple X accounts found:** List them and ask user to select:

"**Which X account should this post to?**

1. {displayName} (@{username})
2. {displayName} (@{username})
...

Select a number."

Store selected account's `_id` as `{accountId}` and `profileId._id` as `{profileId}`.

**If no active X account found:** Report the error and halt — do NOT proceed. Remind user to connect X account in Late.dev.

#### 5d. Upload media (if post has media)

**For image or video formats:**

```bash
curl -s -X POST "https://getlate.dev/api/v1/media" \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -F "files=@{confirmed_media_path}"
```

Store the returned `url` from the response as `{media_url}`.
Store the returned `type` as `{media_type}` (e.g. `video`, `image`).

If upload fails, report the error and halt — do NOT proceed to post creation.

**For single, thread, or long post format:** skip this section, no media to upload.

#### 5e. Create and schedule the post

Build the JSON payload. For **Now**:
```json
{
  "platforms": [
    {
      "platform": "twitter",
      "accountId": "{accountId}"
    }
  ],
  "profileId": "{profileId}",
  "content": "{approved post body text}",
  "mediaItems": [{"type": "{media_type}", "url": "{media_url}"}],
  "publishNow": true,
  "title": "{post_slug}"
}
```

For **Time** (omit `publishNow`, include `scheduledFor`):
```json
{
  "platforms": [
    {
      "platform": "twitter",
      "accountId": "{accountId}"
    }
  ],
  "profileId": "{profileId}",
  "content": "{approved post body text}",
  "mediaItems": [{"type": "{media_type}", "url": "{media_url}"}],
  "scheduledFor": "{scheduled_for}",
  "title": "{post_slug}"
}
```

For **text-only posts** (single, thread, long post): omit the `mediaItems` field entirely.

**For THREAD format:** If Late.dev supports thread scheduling, pass tweets as an array. Otherwise, note for user:

"**Thread note:** If Late.dev doesn't support thread scheduling for X, the thread tweets will be saved as draft in the markdown file. You can post them manually or use X's native thread composer."

```bash
curl -s -X POST "https://getlate.dev/api/v1/posts" \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{payload}'
```

#### 5f. Handle response

**Success:** Update frontmatter `status: scheduled` (or `published` if Now), `scheduled_at: {datetime or "now"}`.
Display: "**Post scheduled via Late.dev for X.** ID: {response id}"

**Failure:** Display the full error response. Offer:
- **[R]** Retry
- **[S]** Skip scheduling — save as draft instead

### 6. Save Confirmation

Present a summary of everything saved:

```
SAVED:
  Post: {output_path}/{post-slug}.md
  Media: {companion files list or "none"}
  Status: {draft or scheduled}
  Scheduled: {datetime or "Not scheduled"}
  Platform: X/Twitter
```

### 7. Proceed

Display: "**Proceeding to check if you want to generate more posts...**"

#### Menu Handling Logic:

- After save confirmation, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is a save step with auto-proceed after completion
- Proceed directly to next step after all files saved

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN all files are saved, derivative tracking is updated, and scheduling decision is made will you load and read fully `{nextStepFile}` to check if user wants more posts.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Post markdown saved with complete YAML frontmatter to `x/` subfolder
- Thread tweets clearly formatted in the markdown body (if thread format)
- Output path uses `x/` not `linkedin/`
- Derivative tracking updated
- Late.dev API key auto-read from .env — never asked from user
- X account fetched (not LinkedIn account)
- Media uploaded to Late.dev before post creation (if media format)
- Post scheduled or published via API without manual curl from user
- Save confirmation presented with file paths and Late.dev post ID

### ❌ SYSTEM FAILURE:

- Saving to `linkedin/` subfolder instead of `x/`
- Using LinkedIn account instead of X account in Late.dev
- Missing frontmatter fields
- Not formatting thread tweets in the markdown body
- Overwriting existing files without confirmation
- Not updating derivative tracking
- Skipping Late.dev scheduling option

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
