---
name: 'step-04-publish'
description: 'Generate SEO metadata then save the approved blog post as a complete markdown file ready for any CMS'

outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{format}-{content_slug}-{date}.md'
blogStandards: '../data/blog-standards.md'
---

# Step 4: Publish

## STEP GOAL:

To generate final SEO metadata for the approved blog post then save it as a complete, CMS-ready markdown file. Images stay as local relative paths — the user deploys to their platform of choice (Ghost, WordPress, Astro, Notion, etc.).

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
- Focus: Metadata generation + local file save
- Limits: Do not rewrite the draft — only add metadata and save
- Dependencies: Approved draft from Step 3 must exist

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Context

Load {outputFile} completely — frontmatter and draft body.

Read format from frontmatter. If format is `email`, this step is not applicable — inform user that email publishing is handled separately via your email platform (see step-04-polish.md) and return to agent menu.

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

### 3. Prepare Export Summary

With metadata selected:

- **title**: From the H1 heading of the draft
- **slug**: Use `{project_slug}` (already lowercase with hyphens)
- **description**: The selected meta_description
- **category**: From frontmatter `category` field (gathered in Step 2)
- **images**: Note any local image paths in the draft — they stay as relative paths

### 4. Update Output File Frontmatter

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

Save as `blog-{content_slug}-{date}.md` in the same directory.

### 5. Report Result

"**Blog post saved and ready to deploy.**

- **File:** `{file path}`
- **Meta title:** {selected meta title}
- **Meta description:** {selected meta description}
- **Images:** {count local image references — stay as relative paths}

**Deploy your blog:**
- **Ghost / WordPress:** Import the markdown file directly
- **Astro / Hugo / Next.js:** Drop into your `content/` directory (frontmatter is pre-structured)
- **Notion:** Paste body or use Notion API import
- **Beehiiv / Kit:** Copy body into your email editor

Images are referenced as relative paths — upload them to your CMS media library when publishing."

### 6. Update Tracking

- Update `{project-root}/context/memory/2-copywriter-sidecar/memories.md` with blog save status and timestamp
- Log: date, slug, title, status (saved)

### 7. Present MENU OPTIONS

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
- File saved as `blog-{slug}-{date}.md`
- Deploy instructions presented with CMS options
- Tracking updated in copywriter sidecar memories

### SYSTEM FAILURE:

- Not generating metadata before saving
- Not updating the output file frontmatter before saving
- Not presenting deploy instructions
- Not updating tracking after save

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
