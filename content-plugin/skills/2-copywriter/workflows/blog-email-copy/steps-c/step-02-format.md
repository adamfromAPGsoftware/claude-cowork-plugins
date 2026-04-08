---
name: 'step-02-format'
description: 'Select content format (blog or email) and gather format-specific inputs'

nextStepFile: './step-03-draft.md'
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{format}-{content_slug}-{date}.md'
---

# Step 2: Format Selection

## STEP GOAL:

To determine whether the user wants a blog post or an email campaign, then gather the format-specific inputs needed for content generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content strategist helping the user choose the right format and gather inputs
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in SEO blogging and email marketing, user brings their content goals
- ✅ Help the user make an informed format choice based on their source material

### Step-Specific Rules:

- 🎯 Focus ONLY on format selection and input gathering — do not draft content yet
- 🚫 FORBIDDEN to generate blog or email content in this step
- 💬 Present format options clearly with descriptions of what each produces
- 📋 Gather ALL format-specific inputs before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Update output file frontmatter with format choice and inputs
- 📖 Track format selection and all gathered inputs
- 🚫 Do not proceed without a confirmed format choice and inputs

## CONTEXT BOUNDARIES:

- Available: Source material summary and image catalog from Step 1 (in output file frontmatter)
- Focus: Format selection and format-specific input gathering
- Limits: Do not generate any content — only collect the inputs needed for Step 3
- Dependencies: Source material and image catalog must be loaded from Step 1

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Read Source Context

Load {outputFile} and read the source material summary and image catalog from frontmatter. Briefly reference the key concepts and available images to inform the format recommendation.

### 2. Determine Format

**Check the agent menu entry point that triggered this workflow:**
- If the user entered via **[BL] Blog Content** → format is **blog**. Skip the format question entirely and proceed to step 3.
- If the user entered via **[EM] Email Copy** → format is **email**. Skip the format question entirely and proceed to step 3.
- If the format cannot be determined from context (e.g., workflow launched directly), present the format options:

"**What format would you like to create?**

**[B] Blog Post**
SEO-optimised lead magnet with dual-funnel targeting. Produces a long-form markdown blog post with meta tags, keyword-rich headings, and a prominent video CTA. Project images (diagrams, B-roll stills, thumbnails) will be embedded throughout.

**[E] Email Campaign**
Brand-compliant nurture or announcement email. Produces subject line, preview text, and full email body following proven Format A (Story-Driven) or Format B (Announcement) structures. Includes a hero image from your project assets.

**Select:** [B] Blog Post / [E] Email Campaign"

Wait for user selection only if format was not already determined.

### 3. Gather Format-Specific Inputs and Confirm

**IF Blog Post:**

"**Blog post — let me gather a few inputs to sharpen the output:**

1. **Primary SEO keyword** — What keyword should this post target?
{IF keyword_data exists in frontmatter from Step 1:}
   Based on your source material and keyword research, here are my suggestions:
   {For each primary candidate: **{keyword}** — {volume} monthly searches, {competition} competition. Rationale: {why this fits the content}}
   Pick one, or provide your own.
{ELSE:}
   (optional — I can suggest based on your content)

2. **YouTube video URL** — Do you have a video URL for the CTA? (optional — I'll use a placeholder if not)

3. **Category** — What category does this fall under? (e.g., ai-engineering, automation, tutorial, case-study)

**Images:** I found **{count}** visual assets in your project (diagrams, B-roll, thumbnails). I'll select the best ones to embed in the post during drafting. You can guide image selection in the next step if you want.

Provide what you have — none of these are blockers."

Wait for user input. Accept partial answers.

**IF Email Campaign:**

Auto-derive as much as possible from ingested project context before asking the user:

**Auto-source from project context:**
- **Email goal/topic** — Derive from the content concept brief (key messages, hook, positioning), competitive research (opportunity framing), and any existing blog post or script in the project. Summarise in one sentence.
- **CTA landing page URL** — Check for `youtube_url` in any existing blog post frontmatter within the project, or in the content concept brief. If a YouTube URL exists, use it. If not, check for other landing page references.
- **Specific details** — Extract key numbers, credentials, dates, and proof points from the content concept brief, competitive research, and transcripts (e.g., "250+ projects", "$1M+ revenue", "Top 1% Upwork", project-specific metrics).

**Only ask the user for the email structure choice** — this is the one genuinely subjective decision:

"**Email campaign — I've pulled the goal, CTA, and details from your project context. One choice for you:**

**Email format** — Which structure?
- **[A] Story-Driven** — Personal narrative, lesson, soft CTA. Best for nurture sequences.
- **[B] Announcement** — Bold, direct, social proof, hard CTA. Best for launches and video drops.

**Auto-sourced from project:**
- **Goal:** {derived email goal from content concept/blog/research}
- **CTA URL:** {youtube_url or landing page from project context, or 'none found — please provide'}
- **Key details:** {extracted proof points and specifics}
- **Hero image:** I found **{count}** visual assets in your project — I'll select the strongest one during drafting.

**Select [A] or [B]** — or override any of the auto-sourced inputs above."

Wait for user input. Accept format choice and any overrides.

### 4. Confirm Inputs and Continue

Present a summary of the format choice and all gathered inputs with the continue option:

"**Here's what we're working with:**

**Format:** {Blog Post / Email Campaign}
{Format-specific inputs listed}
**Image assets available:** {count} from project catalog
**Source material:** {Brief reference to key concepts from Step 1}

**[C] Continue to Content Draft** — or tell me what to change."

Wait for user input.

#### Menu Handling Logic:

- IF C (or confirmation like "looks good", "yes", "continue"): Update output file (see step 5), then load, read entire file, then execute {nextStepFile}
- IF user provides changes: Accommodate changes, re-present summary with [C] Continue option
- IF Any other: help user, then redisplay summary with [C] Continue option

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting the summary
- ONLY proceed to next step when user confirms or selects 'C'

### 5. Update Output File (on confirmation)

When the user confirms in step 4, update {outputFile} frontmatter with format choice and inputs:

**For Blog:**
```yaml
format: blog
primary_keyword: '{user input or empty}'
youtube_url: '{user input or YOUTUBE_URL}'
category: '{user input}'
```

**For Email:**
```yaml
format: email
email_format: '{A or B}'
email_goal: '{auto-derived from project context, or user override}'
landing_page_url: '{auto-derived youtube_url or landing page from project, or user override}'
specific_details: '{auto-derived proof points and metrics from project context, or user override}'
```

Update `stepsCompleted` to include `step-02-format`. Then immediately proceed to load and execute {nextStepFile}.

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user confirms (C or affirmative response) and the output file has been updated with format choice and all inputs will you then load and read fully `./step-03-draft.md` to execute content generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- User selected format (blog or email)
- Format-specific inputs gathered (required + available optional)
- Image availability acknowledged and referenced
- Inputs confirmed by user
- Output file updated with format choice and inputs in frontmatter
- stepsCompleted updated

### ❌ SYSTEM FAILURE:

- Generating blog or email content in this step
- Proceeding without format selection
- Not gathering format-specific inputs
- Not confirming inputs with user
- Not updating output file frontmatter

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
