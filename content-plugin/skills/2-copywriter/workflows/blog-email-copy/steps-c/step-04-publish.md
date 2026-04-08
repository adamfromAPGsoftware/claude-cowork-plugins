---
name: 'step-04-publish'
description: 'Generate SEO metadata, then publish the approved blog post to Supabase with media upload'

outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{format}-{content_slug}-{date}.md'
blogStandards: '../data/blog-standards.md'
publishScript: '{project-root}/scripts/publish-to-supabase.py'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 4: Publish

## STEP GOAL:

To generate final SEO metadata for the approved blog post, then upload all media to Supabase Storage and publish the blog to the lander resources table — all in one approval gate.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content strategist performing the final metadata pass and publishing
- ✅ This is the last step — one approval from the user, then it's live

### Step-Specific Rules:

- 🎯 Generate metadata, present it with the publish preview, get ONE confirmation, then publish
- 🚫 FORBIDDEN to rewrite the draft body — only add metadata
- 🚫 FORBIDDEN to publish without explicit user confirmation
- 📋 The output must be publication-ready before the publish confirmation prompt

## CONTEXT BOUNDARIES:

- Available: Approved draft from Step 3, format choice and inputs from Step 2 — all in {outputFile}
- Focus: Metadata generation + Supabase publishing
- Limits: Do not rewrite the draft — only add metadata and publish
- Dependencies: Approved draft from Step 3 must exist

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Context

Load {outputFile} completely — frontmatter and draft body.

Read format from frontmatter. If format is `email`, this step is not applicable — inform user that email publishing uses ConvertKit (handled separately) and return to agent menu.

Load {blogStandards} for metadata generation rules.

### 2. Generate SEO Metadata

Generate and present:

1. **Meta title** — 2 options, each ≤60 characters, primary keyword front-loaded
2. **Meta description** — 2 options, each ≤155 characters, includes CTA language

"**Quick SEO metadata before we publish:**

**Meta Title (select one):**
A) {option 1} ({character count} chars)
B) {option 2} ({character count} chars)

**Meta Description (select one):**
A) {option 1} ({character count} chars)
B) {option 2} ({character count} chars)

**Select your preferences (e.g., A/B or B/A).**"

Wait for user selection.

### 3. Prepare Publish Payload

With metadata selected, prepare the publishing payload:

- **title**: From the H1 heading of the draft
- **slug**: Use `{project_slug}` (already lowercase with hyphens)
- **description**: The selected meta_description
- **category**: From frontmatter `category` field (gathered in Step 2)
- **thumbnail**: Scan `{content_output_folder}/projects/{project_slug}/creative-director/thumbnails/` for thumbnail images. If multiple exist, ask user which to use. If none, skip (thumbnail is optional).
- **content**: The full markdown draft body
- **media files**: Scan the draft for all local image/media references (relative paths in `![alt](path)`, `<img src="path">`, `<video src="path">`). List how many local files will be uploaded.

### 4. Present Publish Preview and Confirm

Present everything in one view:

"**Ready to publish to Supabase.**

**SEO Metadata:**
- Meta Title: {selected meta title}
- Meta Description: {selected meta description}

**Publishing Payload:**
- Title: {extracted title}
- Slug: {slug}
- Description: {selected meta description}
- Category: {category}
- Thumbnail: {thumbnail path or 'none'}
- Content: {character count} characters of markdown
- Media: {count} local files will be uploaded to `resource-media/{slug}/`
- Published: true

**Target:** Lander — `resources` table + `resource-media` storage

This will upload images to Supabase Storage, rewrite local paths to public URLs, and upsert the resource (insert new or update existing if slug matches).

**Publish now? [Y/N]**"

Wait for user confirmation. This is the single approval gate.

- If N: Return to agent menu. Inform user the draft is saved and can be published later via [PB] Publish Blog.
- If Y: Continue to step 5.

### 5. Execute Publishing

**5a. Update output file frontmatter:**

```yaml
title: '{H1 text}'
meta_title: '{selected meta title}'
meta_description: '{selected meta description}'
primary_keyword: '{keyword}'
secondary_keywords: [{keywords from frontmatter}]
category: '{category}'
date: '{current date}'
status: complete
stepsCompleted: ['step-01-init', 'step-02-format', 'step-03-draft', 'step-04-publish']
format: blog
images_used: [{list of embedded image filenames from draft}]
```

**5b. Rename output file:**

Save as `blog-{content_slug}-{date}.md` in the same directory.

**5c. Run the publish script:**

```bash
python3 "{project-root}/scripts/publish-to-supabase.py" \
  --file "{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{blog_filename}" \
  --title "{extracted title}" \
  --slug "{slug}" \
  --description "{selected meta description}" \
  --category "{category}" \
  --thumbnail "{thumbnail path or URL}"
```

Omit `--thumbnail` if no thumbnail was selected.

The script reads `APG_LANDER_SUPABASE_URL` and `APG_LANDER_SUPABASE_SECRET_KEY` from environment variables.

**The script automatically handles:**
- Uploading all local media files (images, video) to Supabase Storage at `resource-media/{slug}/`
- Rewriting local paths in the markdown to public URLs
- Upserting the resource row in the `resources` table

### 6. Report Result

**On success:**

"**Published!**

- **URL:** `https://{YOUR_DOMAIN}/resources/{slug}`
- **Media uploaded:** {count} files to `resource-media/{slug}/`
- **Status:** Live

The blog post is now accessible on the lander."

**On error:**

Display the error from the script. Common issues:
- Missing env vars → tell user to set `APG_LANDER_SUPABASE_URL` and `APG_LANDER_SUPABASE_SECRET_KEY`
- Auth error → secret key may be invalid or expired
- Network error → check connectivity

### 7. Update Tracking

- Update `{project-root}/_bmad/_memory/copywriter-sidecar/memories.md` with blog publish status, timestamp, and URL
- Log: date, slug, title, status (published/failed)

### 8. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [D] Done

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF D: Workflow complete. Return control to the invoking agent.
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- This is the final step — no next step file to load
- User can use A/P for final refinements before exiting

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Meta title and meta description generated and user-selected
- Output file updated with final metadata in frontmatter
- Publish preview presented with full payload details
- User explicitly confirmed [Y] before any publishing action
- Publishing script executed successfully
- Media files uploaded to Supabase Storage
- Resource upserted in resources table
- Result reported to user with URL
- Tracking updated in copywriter sidecar memories

### SYSTEM FAILURE:

- Publishing without explicit user [Y] confirmation
- Not generating metadata before publishing
- Not presenting the publish preview payload
- Script errors not reported to user
- Not updating the output file frontmatter before publishing
- Not updating tracking after publish

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
