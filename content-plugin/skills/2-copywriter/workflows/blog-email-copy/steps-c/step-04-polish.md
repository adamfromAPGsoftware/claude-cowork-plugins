---
name: 'step-04-polish'
description: 'Generate SEO metadata or subject line variants, verify compliance, push to ConvertKit (email), and save final output'

outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{format}-{content_slug}-{date}.md'
blogStandards: '../data/blog-standards.md'
emailStandards: '../data/email-standards.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
convertKitScript: '{project-root}/scripts/create-convertkit-draft.sh'
imageHostScript: '{project-root}/scripts/upload-to-supabase-storage.sh'
---

# Step 4: Polish & Metadata

## STEP GOAL:

To generate final metadata (SEO tags for blog, subject line variants for email), perform a final compliance verification, and save the completed output file.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator — but in this step you DO generate metadata and verify compliance
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content strategist performing the final quality pass
- ✅ We engage in collaborative dialogue — present metadata options, user selects
- ✅ You bring SEO expertise (blog) or email marketing expertise (email), user makes final decisions
- ✅ This is the last step — output must be publication-ready

### Step-Specific Rules:

- 🎯 Focus ONLY on metadata generation, compliance verification, and final save
- 🚫 FORBIDDEN to rewrite the draft body — only add metadata and make minor compliance fixes
- 💬 Present metadata options for user selection
- 📋 The final output file must be complete and ready for downstream workflows

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Update {outputFile} with final metadata and mark as complete
- 📖 Update stepsCompleted to mark workflow complete
- 🚫 Do not save final output without user approval

## CONTEXT BOUNDARIES:

- Available: Approved draft from Step 3, format choice and inputs from Step 2 — all in {outputFile}
- Focus: Metadata generation and final compliance verification
- Limits: Do not rewrite the draft — only add metadata and fix compliance issues
- Dependencies: Approved draft from Step 3 must exist

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Context and Standards

Load {outputFile} completely — frontmatter and draft body.

Read format from frontmatter.

**IF format is blog:** Load {blogStandards} completely.
**IF format is email:** Load {emailStandards} completely.

### 2. Generate Metadata

**IF Blog Post:**

Generate and present:

1. **Meta title** — ≤60 characters, primary keyword front-loaded
   - Present 2 options for user to choose from

2. **Meta description** — ≤155 characters, includes CTA language
   - Present 2 options for user to choose from

3. **Keyword verification report:**
   - Primary keyword in H1: ✅/❌
   - Primary keyword in first 100 words: ✅/❌
   - Primary keyword in 2+ H2 headers: ✅/❌
   - Secondary keywords distributed naturally: ✅/❌

4. **CTA verification:**
   - YouTube CTA formatted as prominent callout block: ✅/❌
   - No raw URLs exposed: ✅/❌
   - If YouTube URL was a placeholder, remind user to replace before publishing

5. **Readability pass:**
   - Paragraphs ≤4 sentences: ✅/❌
   - Active voice predominant: ✅/❌
   - Scannable formatting (bullets, bold, headers): ✅/❌

"**Meta options:**

**Meta Title (select one):**
A) {option 1} ({character count} chars)
B) {option 2} ({character count} chars)

**Meta Description (select one):**
A) {option 1} ({character count} chars)
B) {option 2} ({character count} chars)

**Compliance Report:**
{verification results}

**Please select your preferred meta title and description.**"

Wait for user selection. Fix any compliance failures before proceeding.

**IF Email Campaign:**

Generate and present everything in one view — subject lines, preview text, compliance check, and publish confirmation combined into a single prompt:

1. **Subject line variants** — 3 options following the rules from {emailStandards}:
   - Variant 1: Curiosity-driven (open a loop)
   - Variant 2: Benefit-driven (what they get)
   - Variant 3: Pattern interrupt (unexpected angle)

2. **Preview text variants** — 2 options, each complementing the subject line

3. **Brand voice compliance check:**
   - Written to one person: ✅/❌
   - Specifics used (not vague): ✅/❌
   - One CTA only: ✅/❌
   - Format A/B structure followed: ✅/❌
   - Word count in range: ✅/❌
   - Persistent footer elements present: ✅/❌

"**Final review before ConvertKit push:**

**Subject Line (select one):**
1) {variant 1} — Curiosity-driven
2) {variant 2} — Benefit-driven
3) {variant 3} — Pattern interrupt

**Preview Text (select one):**
A) {option 1}
B) {option 2}

**Compliance:** {all checks passing summary}
**Hero image:** {resolved .png path — ready for hosting}
**CTA:** {YouTube URL or landing page}

**Select your subject line + preview text, then I'll push to ConvertKit as a draft.**
(e.g., "1A" or "2B" — or tell me what to change)"

Wait for user selection. This is the single interaction before publishing — subject line choice + preview text choice + implicit publish confirmation in one response.

### 3. Update Output File with Final Metadata

**IF Blog Post:**

Update {outputFile} frontmatter:
```yaml
title: '{H1 text}'
meta_title: '{selected meta title}'
meta_description: '{selected meta description}'
primary_keyword: '{keyword}'
secondary_keywords: [{keywords}]
category: '{category}'
date: '{current date}'
status: complete
stepsCompleted: ['step-01-init', 'step-02-format', 'step-03-draft', 'step-04-polish']
format: blog
images_used: [{list of embedded image filenames from draft}]
```

**IF Email Campaign:**

Update {outputFile} frontmatter:
```yaml
subject: '{selected subject line}'
preview_text: '{selected preview text}'
format: '{A or B}'
hero_image: '{path to selected hero image}'
date: '{current date}'
status: complete
stepsCompleted: ['step-01-init', 'step-02-format', 'step-03-draft', 'step-04-polish']
```

### 4. Save Final Output

Save the completed file to its final output location.

**Blog:** Rename/save as `blog-{slug}-{date}.md`
**Email:** Rename/save as `email-{slug}-{date}.md`

**Blog compliance check:** Verify all image paths are relative (e.g., `../relative/path/to/image.png`). The publish workflow will upload images and rewrite paths to hosted URLs. Flag any absolute or external URLs that shouldn't be there.

### 5. ConvertKit Draft Push (Email Only — Automatic After Subject Line Selection)

**Skip this section entirely for blog posts.**

When the user selects their subject line and preview text in step 2, proceed directly to ConvertKit push — no additional Y/N confirmation needed. The subject line selection IS the publish confirmation.

1. **Upload hero image** (if local path):
   - Check if hero image path is a local path or contains `<!-- REQUIRES HOSTING:` comment
   - If local: execute `{imageHostScript} "{local-path}" "{project_slug}"` to upload to Supabase Storage
   - Capture the returned public URL
   - Replace the local path in the email body with the hosted URL

2. **Convert markdown to HTML:**
   - Follow the HTML Conversion Rules from {emailStandards}
   - Apply inline styles to every element per the Element Style Table
   - Convert hero image to `<img>` tag with hosted URL
   - Convert persistent footer to the exact HTML block from email-standards
   - Ensure all `<p>`, `<ul>`, `<li>`, `<hr>`, `<a>`, `<strong>`, `<em>` tags have inline styles

3. **Build ConvertKit payload:**
   ```json
   {
     "subject": "{selected subject line}",
     "preview_text": "{selected preview text}",
     "content": "{HTML email body}",
     "description": "Draft from CCS blog-email-copy workflow",
     "email_template_id": 4965521,
     "send_at": null,
     "public": false
   }
   ```
   - Write payload to a temp file: `/tmp/convertkit-payload-{slug}-{date}.json`
   - **Safety:** `send_at` is ALWAYS null, `public` is ALWAYS false — this creates a draft only

4. **Execute ConvertKit script:**
   - Run: `{convertKitScript} /tmp/convertkit-payload-{slug}-{date}.json`
   - On success: capture broadcast ID from output
   - On failure: report error, suggest user check `CONVERTKIT_API_KEY` env var

5. **Update frontmatter:**
   - Set `broadcast_id: {captured broadcast ID}`
   - Set `status: pushed`

6. **Clean up:**
   - Remove temp payload file

### 6. Present Completion Summary

"**Content generation complete!**

**Format:** {Blog Post / Email Campaign}
**Output saved:** {final file path}
**Status:** Complete

{IF Blog:}
**Next steps:**
- Run [PB] Publish Blog to push to Supabase
- Or review/edit the output file directly
- All image paths are relative — the publish workflow will upload and rewrite them

{IF Email:}
**ConvertKit draft created!**
- Broadcast ID: {broadcast_id}
- Subject: {selected subject line}
- Status: DRAFT (will not send until you review and schedule in ConvertKit)
- Hero image: hosted at {public URL}
**Next step:** Review the draft in ConvertKit and schedule when ready. It will NOT send automatically.

**Done.**"

### 7. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [D] Done

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF D: Workflow complete. Return control to the invoking agent.
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#7-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- This is the final step — no next step file to load
- User can use A/P for final refinements before exiting

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Appropriate standards file loaded for final verification
- Metadata options generated and presented (meta title/description for blog, subject line/preview text variants for email)
- User selected preferred metadata options
- Compliance verification completed with all checks passing
- Output file updated with final metadata in frontmatter
- Final output saved to correct location with proper filename
- Blog: all image paths verified as relative (ready for publish workflow)
- Email: ConvertKit push offered to user with clear safety messaging
- Email (if pushed): hero image uploaded to Supabase, HTML converted with inline styles, draft created with send_at: null, broadcast_id captured
- Completion summary presented with next steps (including ConvertKit status for emails)
- stepsCompleted reflects all 4 steps

### ❌ SYSTEM FAILURE:

- Not loading standards for final verification
- Not presenting metadata options for user selection
- Saving with compliance failures unfixed
- Not updating frontmatter with final metadata
- Missing stepsCompleted in final output
- Not presenting completion summary
- Email: pushing to ConvertKit without user confirmation
- Email: creating a broadcast with send_at set to anything other than null
- Email: not uploading hero image before ConvertKit push (local paths won't render)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
