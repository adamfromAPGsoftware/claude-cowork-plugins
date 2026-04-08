---
name: 'step-06-save'
description: 'Save approved LinkedIn post with frontmatter and optionally schedule via Late.dev'

nextStepFile: './step-07-more.md'
---

# Step 6: Save & Schedule

## STEP GOAL:

To save the approved LinkedIn post as a markdown file with structured YAML frontmatter, save any companion media files, and optionally schedule the post via the Late.dev API.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content operations specialist handling delivery and distribution
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring file management and API integration expertise, user brings scheduling preferences

### Step-Specific Rules:

- 🎯 Focus only on saving output and scheduling — content is already approved
- 🚫 FORBIDDEN to modify approved content without user request
- 💬 Confirm all file paths before saving
- 📋 All LinkedIn deliverables live in one folder — post markdown, media assets, companion files

## EXECUTION PROTOCOLS:

- 🎯 Save files to correct output paths
- 💾 Update derivative tracking in agent memories
- 📖 Update project status if project-based mode
- 🚫 FORBIDDEN to overwrite existing files without confirmation

## CONTEXT BOUNDARIES:

- Approved post content, media plan, hook, CTA all available from previous steps
- Media file is ALREADY confirmed on disk by step-05b — do not re-check or re-produce it
- Output paths depend on source mode (project vs personal)
- Late.dev API available for scheduling
- Focus: File output and distribution — no content changes

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Determine Output Path

**Project mode:**
- Output folder: `{project_folder}/linkedin/`
- Create directory if it doesn't exist

**Personal mode:**
- Ask user for output path or default to `{output_folder}/linkedin/`
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
media_source: "{carousel-generator|existing-asset|gemini-generated|none}"
slides_json: "{path to slides JSON if carousel, else null}"
hashtags: []  # Never include hashtags — they are an AI-generated tell
status: draft
scheduled_at: null
created: {current_date}
---

{approved post body text}
```

### 3. Reference Companion Media

Media has already been produced and confirmed by step-05b. Simply resolve the confirmed media path from session context and record it in the post frontmatter `media_path` field:

- **Video:** `{linkedin_path}{post_slug}-video.mp4`
- **Carousel:** `{linkedin_path}{post_slug}-carousel.pdf`
- **Image (branded):** `{linkedin_path}{post_slug}-image.png`
- **Image (existing asset):** path as confirmed in step-05b

### 4. Update Derivative Tracking

Update the agent's memories with derivative tracking:
- Source project/topic → hook → format → content category → status
- This prevents angle duplication in future posts

If project mode: update `{project_folder}/project.md` with LinkedIn content status.

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

Ask: "**What date and time? (e.g. 2026-03-05 09:00 AEST)**"
Convert to ISO 8601 UTC. Store as `{scheduled_for}`.
If Now: set `"publishNow": true` and omit `scheduledFor`.

#### 5c. Fetch LinkedIn accountId and confirm account

```bash
curl -s -X GET "https://getlate.dev/api/v1/accounts" \
  -H "Authorization: Bearer $LATE_API_KEY"
```

Filter the response to LinkedIn accounts only (`platform === "linkedin"` and `isActive === true`).

**If one LinkedIn account found:** Present it for confirmation:

"**Posting to:** {displayName} (@{username}) — {profileUrl}
Is this the right account? **[Y]** Yes / **[N]** No"

- If Y: store `{accountId}` and `{profileId}`, proceed.
- If N: list all available LinkedIn accounts and ask user to select by number.

**If multiple LinkedIn accounts found:** List them and ask user to select:

"**Which LinkedIn account should this post to?**

1. {displayName} (@{username}) — {profileUrl}
2. {displayName} (@{username}) — {profileUrl}
...

Select a number."

Store selected account's `_id` as `{accountId}` and `profileId._id` as `{profileId}`.

**If no active LinkedIn account found:** Report the error and halt — do NOT proceed.

#### 5d. Upload media (if post has media)

**For video, image, or carousel formats:**

```bash
curl -s -X POST "https://getlate.dev/api/v1/media" \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -F "files=@{confirmed_media_path}"
```

Store the returned `url` from the response as `{media_url}`.
Store the returned `type` as `{media_type}` (e.g. `video`, `image`, `document`).

If upload fails, report the error and halt — do NOT proceed to post creation.

**For text format:** skip this section, no media to upload.

#### 5e. Create and schedule the post

Build the JSON payload. For **Now**:
```json
{
  "platforms": [
    {
      "platform": "linkedin",
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
      "platform": "linkedin",
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

For **text posts** omit the `mediaItems` field entirely.

```bash
curl -s -X POST "https://getlate.dev/api/v1/posts" \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{payload}'
```

#### 5f. Handle response

**Success:** Update frontmatter `status: scheduled` (or `published` if Now), `scheduled_at: {datetime or "now"}`.
Display: "**Post scheduled via Late.dev.** ID: {response id}"

**Failure:** Display the full error response. Offer:
- **[R]** Retry
- **[S]** Skip scheduling — save as draft instead

### 6. Save Confirmation

Present a summary of everything saved:

```
SAVED:
  Post: {output_path}/{post-slug}.md
  Media: {companion files list}
  Status: {draft or scheduled}
  Scheduled: {datetime or "Not scheduled"}
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

- Post markdown saved with complete YAML frontmatter
- Companion files saved (carousel JSON, image JSON, video instructions)
- Output paths correct for source mode
- Derivative tracking updated
- Late.dev API key auto-read from .env — never asked from user
- Media uploaded to Late.dev before post creation
- LinkedIn accountId fetched automatically from GET /accounts
- Post scheduled or published via API without manual curl from user
- Save confirmation presented with file paths and Late.dev post ID

### ❌ SYSTEM FAILURE:

- Modifying approved content during save
- Missing frontmatter fields
- Saving to wrong output path
- Overwriting existing files without confirmation
- Not updating derivative tracking
- Skipping Late.dev scheduling option

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
