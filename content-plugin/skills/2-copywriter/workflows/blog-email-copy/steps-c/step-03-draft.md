---
name: 'step-03-draft'
description: 'Generate the full content draft based on format choice — blog post or email campaign'

nextStepFile: './step-04-publish.md'  # blog → step-04-publish.md | email → step-04-polish.md (resolved at runtime)
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{format}-{content_slug}-{date}.md'
blogStandards: '../data/blog-standards.md'
emailStandards: '../data/email-standards.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 3: Content Draft

## STEP GOAL:

To generate the full content draft — either an SEO-optimised blog post with embedded project images, or a brand-compliant email campaign with a hero image — based on the format choice, inputs, and image catalog from previous steps.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator — but in this step you DO generate the draft based on gathered inputs and standards
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content strategist and skilled copywriter generating high-quality content
- ✅ We engage in collaborative dialogue — present the draft, accept feedback, revise
- ✅ You bring SEO expertise (blog) or email marketing expertise (email), user brings brand knowledge and approval authority
- ✅ The draft must follow the standards exactly — no shortcuts on SEO rules or email format structures

### Step-Specific Rules:

- 🎯 Focus ONLY on generating the content draft — do not generate SEO metadata or subject line variants (that's Step 4)
- 🚫 FORBIDDEN to skip loading the appropriate standards data file
- 🖼️ MUST use the image catalog from frontmatter to embed images (blog) or select a hero image (email)
- 💬 Present the complete draft for user review before proceeding
- 📋 Follow the quality checklist from the standards file before presenting

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append the full draft to {outputFile}
- 📖 Update stepsCompleted after user approves the draft
- 🚫 Do not proceed without user approval of the draft

## CONTEXT BOUNDARIES:

- Available: Source material + image catalog (Step 1), format choice and inputs (Step 2) — all in {outputFile} frontmatter
- Focus: Generating the content draft following the appropriate standards, with images from the catalog
- Limits: Do not generate final SEO metadata or subject line variants — that's Step 4
- Dependencies: Format choice, inputs, and image catalog from Steps 1-2 must be present

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Context and Standards

Load {outputFile} and read:
- Source material summary (key concepts, sources loaded)
- Image catalog (all available visual assets with types and descriptions)
- ICP targeting analysis (builder angle, SME angle, dual-funnel opportunities)
- Format choice (blog or email)
- Format-specific inputs (keywords, URLs, format A/B, etc.)

**Load brand context from the copywriter agent's sidecar memory:**
- `_bmad/_memory/copywriter-sidecar/brand-guidelines.md` — Brand voice, tone, positioning
- `_bmad/_memory/copywriter-sidecar/icp-profiles.md` — ICP pain points, language, resonance triggers (if exists)

**IF format is blog:**
- Load {blogStandards} completely. These are your generation rules.
- Load `_bmad/_memory/copywriter-sidecar/inspiration/blog.md` if it exists — for style pattern guidance

**IF format is email:**
- Load {emailStandards} completely. These are your generation rules.
- Load `_bmad/_memory/copywriter-sidecar/inspiration/email.md` if it exists — for style pattern guidance

### 1b. Pre-Generation Checks (Email Only)

Before generating the email draft, resolve these requirements:

**Hero Image Extraction:**
- Review the image catalog from frontmatter
- Email hero images MUST be actual image files (.png, .jpg) — NOT .mp4 video files
- **If only .mp4 assets exist in the catalog** (B-roll, motion graphics), extract a still frame:
  - Select the best .mp4 for the hero (priority: thumbnail-like content > key demonstration > B-roll)
  - Run: `ffmpeg -i "{mp4_path}" -ss 00:00:01 -frames:v 1 -q:v 2 "{output_path}/{asset_name}-frame.png"`
  - Save the extracted .png in the same directory as the source .mp4
  - Use the extracted .png as the hero image path going forward
- **If .png/.jpg assets exist** (thumbnails, diagrams), use those directly — no extraction needed
- Store the resolved hero image path for use in the draft

**YouTube URL Verification:**
- Check if `landing_page_url` or `youtube_url` exists in the output file frontmatter (auto-sourced in Step 2)
- If a YouTube URL is present, confirm it and use it as the CTA link
- **If NO YouTube URL is present**, ask the user: "I need the YouTube video URL for the email CTA. What's the link?"
- Do NOT proceed to draft generation without a confirmed CTA URL

### 2. Generate Draft

**IF Blog Post:**

Generate a complete blog post following ALL rules from {blogStandards}:

1. **H1 headline:** Benefit-driven, incorporates primary keyword, targets both ICPs
2. **Introduction:** Hook paragraph (2-3 sentences), primary keyword in first 100 words
3. **H2 sections (3-6):** Each with keyword-rich header, opens with hook sentence, delivers actionable content, uses H3 sub-headers for longer sections
4. **Embedded images:** Select the most relevant images from the image catalog and embed them throughout the post at contextually appropriate points. Use diagrams to illustrate concepts, B-roll stills for visual breaks, thumbnails for hero/header positioning. Follow the image embedding rules in {blogStandards}
5. **Key takeaways:** 5-7 numbered, scannable, immediately useful bullet points
6. **YouTube CTA:** Visually prominent callout block — blockquote with bold text, horizontal rules above and below, bold anchor text with arrow. NEVER a raw URL
7. **Throughout:** Short paragraphs (2-4 sentences), scannable formatting, active voice, conversational tone, front-loaded value, generous white space

**Image embedding guidance from catalog:**
- **Diagrams** (`type: diagram`) → embed inline where the concept they illustrate is discussed
- **B-roll stills** (`type: broll`) → embed as visual breaks between major sections or to show real examples
- **Thumbnails** (`type: thumbnail`) → use as the post's hero image at the top or in the introduction
- **Motion graphics** (`type: motion-graphic`) → reference as "see the animation in the video" with CTA link, or extract a still frame
- Aim for 3-6 images per post depending on length and available assets
- Every image gets keyword-rich alt text per {blogStandards}

**Dual-funnel check on every section:**
- Builder angle: teaches something actionable
- SME angle: demonstrates ROI or business value
- If a section only speaks to one audience, sharpen it

**IF Email Campaign:**

Generate a complete email following ALL rules from {emailStandards}:

**Hero image selection:** Review the image catalog and select the strongest visual as the hero image. Priority order: thumbnail > key diagram > B-roll still. The hero image sits at the top of the email body, before the opening text.

**For Format A (Story-Driven / Nick Saraev Style):**
1. Hero image (selected from catalog) — flag with `<!-- REQUIRES HOSTING: {local-path} -->` if local path
2. Cold open (1-2 sentences) — NO greeting. Drop straight into the story or hook mid-conversation
3. Story body (2-3 short paragraphs) — the experience, the mistake, the discovery. Specific details, real timelines
4. Insight / lesson (1 paragraph) — the takeaway, what changed
5. Natural bridge (1-2 sentences) — connect the story to something the reader can act on
6. Single bold CTA — soft sell, conversational. Bold the CTA link text
7. Sign-off — "Talk soon," line break, "Adam"
8. PS section (ALWAYS) — prime real estate. Italicized. Format: `**P.S.** *{content}*`
9. Persistent footer elements (exact approved copy from email-standards)

**Format A constraints:** 400-500 words. NEVER use bullet points — prose only. No greeting — cold opens only.

**For Format B (Announcement / Liam Ottley Style):**
1. Hero image (selected from catalog) — flag with `<!-- REQUIRES HOSTING: {local-path} -->` if local path
2. Greeting — "Hey –" line break, "Adam here."
3. Hook (1-2 sentences) — what's new, why now. Lead with the result or number
4. Context with bold figures (1-2 sentences) — social proof, specific numbers in **bold**
5. "What's inside" bullets (3-5) — each starts with bold label: "**The exact prompt** I use to..."
6. Direct CTA — action-oriented, clear. Bold the link text
7. Sign-off — "Keep going," line break, "Adam"
8. PS (optional) — secondary hook or teaser. Same italicized format
9. Persistent footer elements (exact approved copy from email-standards)

**Format B constraints:** 150-250 words. Bullets ENCOURAGED — they're the core value delivery.

**For both formats:**
- Write to ONE person, not a list
- Use specifics — real numbers, timelines, project names
- One clear CTA only (PS may contain secondary)
- Generate initial subject line (lowercase/sentence case, under 50 chars, curiosity-driven)
- Generate initial preview text (1-2 sentences, builds on subject)
- **Image hosting flag:** When hero image uses a local path, include `<!-- REQUIRES HOSTING: {local-path} -->` comment. The ConvertKit push step (Step 4) will resolve this by uploading to Supabase Storage

### 3. Internal Quality Check

Before presenting the draft, verify against the quality checklist in the loaded standards file.

**Blog:** Keyword placement, readability, dual-funnel, CTA formatting, image alt text, images embedded from catalog, all image paths relative
**Email:** Subject line rules (<50 chars), format structure (A or B followed exactly), brand voice, one CTA, specifics over vague, hero image present, sign-off present, PS present (required for A), word count in range, no bullets in Format A, persistent footer with exact approved copy

If any checks fail, fix before presenting.

### 4. Present Draft for Review

"**Here's your {blog post / email campaign} draft:**"

Present the complete draft.

"**Quality checks passed:**
{List which checks were verified}

**Images used:** {List which images from the catalog were embedded and where}

**What do you think?** You can:
- Request specific changes (tone, length, angle, sections)
- Ask me to swap images or add/remove embedded visuals
- Ask me to rework specific parts
- Approve as-is to move to the polish step

**Or use Advanced Elicitation [A] for alternative approaches, or Party Mode [P] for multi-perspective feedback.**"

Wait for user response.

### 5. Revision Loop

If the user requests changes:
1. Understand the WHY behind the revision
2. Make the requested changes (including image swaps if requested)
3. Re-verify quality checks
4. Re-present the updated draft
5. Repeat until user approves

### 6. Save Draft to Output

On user approval, append the full draft content to {outputFile} below the frontmatter.

Update frontmatter:
- `stepsCompleted` to include `step-03-draft`
- `draft_status: approved`
- `images_used: [{list of embedded image filenames}]`

### 7. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Publish

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Save draft to {outputFile}, update frontmatter stepsCompleted, then determine next step:
  - **IF format is blog:** load, read entire file, then execute `./step-04-publish.md`
  - **IF format is email:** load, read entire file, then execute `./step-04-polish.md`
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#7-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions — always respond and then redisplay the menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the draft has been saved to {outputFile} with user approval will you then:
- **Blog:** load and read fully `./step-04-publish.md` to execute metadata generation and publishing
- **Email:** load and read fully `./step-04-polish.md` to execute subject line selection and ConvertKit push

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Appropriate standards file loaded (blog-standards.md or email-standards.md)
- Image catalog read from frontmatter and used in draft generation
- Complete draft generated following ALL rules from the standards
- Blog: project images embedded at contextually appropriate points with keyword-rich alt text
- Email: hero image selected from catalog and placed at top of email body
- Internal quality checks passed before presenting
- Draft presented to user for review with image usage summary
- User approved the draft (possibly after revisions)
- Draft saved to output file with images_used tracking

### ❌ SYSTEM FAILURE:

- Not loading the standards data file
- Generating a blog post with no embedded images when the image catalog has assets
- Generating an email with no hero image when the image catalog has assets
- Generating content that violates the standards (wrong CTA format, keyword stuffing, etc.)
- Presenting draft without internal quality check
- Proceeding without user approval
- Not saving draft to output file

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
