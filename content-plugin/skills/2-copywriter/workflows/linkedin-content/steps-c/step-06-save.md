---
name: 'step-06-save'
description: 'Save approved LinkedIn post with frontmatter and optionally schedule via Buffer'

nextStepFile: './step-07-more.md'
---

# Step 6: Save & Schedule

## STEP GOAL:

To save the approved LinkedIn post as a markdown file with structured YAML frontmatter, save any companion media files, and optionally schedule the post via the Buffer API.

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
- Buffer API available for scheduling
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
media_source: "{carousel-generator|existing-asset|nano-banana-generated|none}"
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

### 5. Buffer Scheduling (Optional)

Ask the user:

"**When should this post go live?**

**[N] Now** — publish immediately via Buffer
**[T] Time** — schedule for a specific date and time
**[S] Skip** — save as draft only"

**If Skip:** Keep `status: draft`. Display: "Saved as draft." Proceed to section 6.

**If Now or Time:**

#### 5a. If Time — get schedule datetime

Ask: "**What date and time? (e.g. 2026-03-05 09:00 AEST)**"
Convert to ISO 8601 UTC. Store as `{scheduled_for}`.

#### 5b. List channels via Buffer MCP

Call `mcp__buffer__use_buffer_api(action: "listChannels")` to retrieve connected accounts.

Filter to LinkedIn channels only. Present for confirmation:

"**Posting to:** {displayName} — LinkedIn
Is this the right account? **[Y]** Yes / **[N]** No"

If multiple LinkedIn channels found, list them and ask user to select.

Store the selected channel's profile ID as `{channel_id}`.

**If no LinkedIn channel found:** Halt — user must connect LinkedIn in Buffer at buffer.com/manage/channels.

#### 5c. Upload media (if post has media)

Use the Buffer MCP tool for media upload if available. If the Buffer MCP does not expose a direct media upload tool, note to user: "Upload your media file manually in Buffer's compose window, or use Buffer's web uploader."

#### 5d. Schedule the post via Buffer MCP

Call:
```
mcp__buffer__use_buffer_api(
  action: "createPost",
  profileIds: [selected LinkedIn channel ID],
  text: approved post body,
  scheduledAt: ISO 8601 UTC datetime,
  media: [media file path if applicable]
)
```

#### 5e. Handle response

**Success:** Update frontmatter `status: scheduled` (or `published` if Now), `scheduled_at: {datetime or "now"}`.
Display: "**Post scheduled via Buffer.** ID: {response id}"

**Failure:** Display the full error. Offer:
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
- Buffer MCP used to list channels (`listChannels`) and create post (`createPost`)
- LinkedIn channel fetched automatically via MCP call
- Post scheduled or published via Buffer MCP without manual API calls from user
- Save confirmation presented with file paths and Buffer post ID

### ❌ SYSTEM FAILURE:

- Modifying approved content during save
- Missing frontmatter fields
- Saving to wrong output path
- Overwriting existing files without confirmation
- Not updating derivative tracking
- Skipping Buffer scheduling option

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
