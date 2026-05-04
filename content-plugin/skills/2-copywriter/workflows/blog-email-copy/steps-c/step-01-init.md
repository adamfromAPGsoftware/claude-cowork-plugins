---
name: 'step-01-init'
description: 'Initialize workflow, select project, and auto-ingest all project context'

nextStepFile: './step-02-format.md'
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{format}-{content_slug}-{date}.md'
standaloneOutputFile: '{standalone_folder}/{date}-blog-email-{content_slug}/{format}-{content_slug}.md'
---

# Step 1: Load Concept

## STEP GOAL:

To select the content project (or standalone source), auto-ingest all existing project artifacts, and build a complete content brief with an image catalog for downstream blog and email generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a content strategist discovering source material for content creation
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring content strategy expertise, user brings their content concepts and project knowledge
- ✅ Together we identify the best source material for downstream content generation

### Step-Specific Rules:

- 🎯 Focus ONLY on discovering, loading, and cataloguing source material — do not draft any content yet
- 🚫 FORBIDDEN to generate blog or email content in this step
- 💬 Present findings clearly and let the user confirm which sources to use
- 📋 Flag any content gaps that might limit downstream quality
- 🖼️ Build an image catalog from all available project visual assets

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Create output file with source material summary and image catalog in frontmatter
- 📖 Track which sources were discovered and selected
- 🚫 Do not proceed without user confirmation of source material

## CONTEXT BOUNDARIES:

- Available: Project folder structure, content briefs, transcripts, analysis files, visual assets
- Focus: Finding and loading all relevant source content + cataloguing images
- Limits: Do not generate any blog or email content — only discover sources
- Dependencies: None — this is the first step

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 0. Load Voice Library (before anything else)

Load `{project-root}/context/references/brand-voice.md` immediately. Apply the Written Content Adaptations and Anti-AI Red Flags sections to all blog and email drafts generated in this workflow. Run anti-AI scan before presenting any output to the user.

### 1. Greet and Determine Mode

"**Welcome to Blog & Email Copy generation.**

I'll help you create an SEO-optimised blog post or a brand-compliant email campaign from your content.

**How would you like to work?**

**[P]roject mode** — Select an existing project. I'll auto-ingest all your concept docs, scripts, transcripts, visual analysis, and images.
**[S]tandalone mode** — Provide source material manually for a one-off piece.

Select: [P]roject / [S]tandalone"

Wait for user selection.

### 2. Load Source Material

**IF Project Mode:**

Ask for the project slug or scan `{content_output_folder}/projects/` and present available projects as a numbered list. Wait for user to select.

Once a project is selected, **auto-scan the entire project folder** and ingest all available artifacts:

**Strategist outputs:**
- `strategist/ideation/content-concept-*.md` — Content concepts, hooks, ICP alignment, content tree
- `strategist/research/competitive-research-*.md` — Market gaps, positioning

**Copywriter outputs:**
- `copywriter/scripts/script-*.md` — Video scripts (primary content source)
- `copywriter/linkedin/*.md` — LinkedIn copy (for cross-format consistency)
- `copywriter/diagrams/images/*.png` — Excalidraw diagram exports

**Creative Director outputs:**
- `creative-director/thumbnails/*.png` — Video thumbnails
- `creative-director/thumbnails/logos/*` — Brand logos and wordmarks

**Video Editor outputs:**
- `video-editor/analysis/*/transcript.json` — Word-level transcripts
- `video-editor/analysis/*/visual-analysis.json` — Frame-by-frame visual classification
- `video-editor/analysis/*/audio-analysis.json` — Audio analysis data
- `video-editor/storyboard/*-storyboard.md` — Approved storyboards
- `video-editor/broll/*.mp4` — Extracted B-roll clips (note filenames for description)
- `video-editor/motion-graphics/*.mp4` — Motion graphic clips

**Project metadata:**
- `project.yaml` — Project title, slug, status, platforms

**Strategist keyword/trend data:**
- `strategist/research/keyword-research-*.md` — Keyword research, search volume, competition data
- `strategist/research/trend-analysis-*.md` — Trending topics and content gap analysis

Read each discovered file and extract key information. For image/video assets, catalogue the filename and infer the content from the filename or parent context.

**IF Standalone Mode:**

"**What content should we work from?**

You can provide:
- A **specific file path** — point me to a content brief, transcript, or document
- A **content concept** — describe the topic and I'll work from that

**What have you got?**"

Wait for user input. Load and extract key information from provided sources.

### 3. Build Image Catalog

**Project mode only** — Build an image catalog from all visual assets found in the project:

| # | Asset | Source | Type | Description |
|---|-------|--------|------|-------------|
| 1 | `diagram-name.png` | `copywriter/diagrams/images/` | diagram | {inferred from filename} |
| 2 | `broll-01-description.mp4` | `video-editor/broll/` | broll | {inferred from filename} |
| 3 | `thumbnail-name.png` | `creative-director/thumbnails/` | thumbnail | {inferred from filename} |
| 4 | `mg-01-description.mp4` | `video-editor/motion-graphics/` | motion-graphic | {inferred from filename} |
| 5 | `logo-name.png` | `creative-director/thumbnails/logos/` | logo | {inferred from filename} |

For B-roll and motion graphics (.mp4 files), note these as **frame-extractable** — the blog can use a still frame exported from the clip, and emails can use them as hero images.

**Storyboard cross-reference:** If a storyboard exists (`video-editor/storyboard/*-storyboard.md`), cross-reference B-roll and motion graphic assets with the storyboard entries. Annotate each visual asset with:
- What it shows (scene description from storyboard)
- Which speech segment / section it accompanies
- Whether it's a demonstration, proof point, or conceptual illustration

This context helps downstream steps embed images at the right points in the content.

**Standalone mode** — If the user provides image paths, catalogue those. Otherwise, note that no project images are available.

### 4. Present Source Summary and Confirm

"**Here's what I found in your project:**

**Project:** {project title from project.yaml}

**Content sources loaded:** {count} files
{For each source: filename — one-line summary of what it contains}

**Key concepts identified:**
- {Bullet list of main topics, arguments, and angles from the source material}

**ICP Targeting Analysis:**
- **Builder angle:** {How this content speaks to builders — skills taught, tools demonstrated, actionable takeaways}
- **SME angle:** {How this content speaks to SMEs/business owners — ROI shown, business outcomes, efficiency gains}
- **Dual-funnel opportunities:** {Where both audiences can be served in the same section, bridging language}

**Visual Analysis Summary:** *(if visual-analysis.json exists)*
- **Key visual moments:** {Significant screen recordings, demonstrations, or visual proof points from the visual analysis}
- **Proof points:** {Frames showing results, dashboards, outputs — useful for blog image embedding}
- **Demo sequences:** {Multi-frame sequences showing a process — candidates for side-by-side image layouts}

**Keyword Data:** *(if keyword research files exist)*
- **Primary keyword candidates:** {Top keywords by relevance + search volume from strategist research}
- **Secondary/trending keywords:** {Supporting keywords and trending terms to weave naturally}
- **Content gaps in SERPs:** {Topics competitors aren't covering well — angles to exploit}

**Image catalog:** {count} visual assets available
{Table from step 3}

**Content gaps:**
- {Any missing material that might limit quality — flag but don't block}

**[C] Continue to Format Selection** — or tell me what to change."

Wait for user input.

#### Menu Handling Logic:

- IF C (or confirmation like "looks good", "yes", "continue"): Create the output file (see step 5), save source summary, update frontmatter stepsCompleted, then load, read entire file, then execute {nextStepFile}
- IF user provides changes: Accommodate changes, re-present source summary with updated [C] Continue option
- IF Any other: help user, then redisplay the source summary with the [C] Continue option

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting the source summary
- ONLY proceed to next step when user confirms or selects 'C'

### 5. Create Output File (on confirmation)

When the user confirms in step 4, create the output file at the confirmed path with source summary and image catalog in frontmatter:

```yaml
---
stepsCompleted: ['step-01-init']
date: '{current date}'
user_name: '{user_name}'
output_mode: '{project or standalone}'
project_slug: '{project_slug or empty}'
content_slug: '{content_slug}'
format: ''
sources_loaded: [{list of source file paths or 'concept-input'}]
key_concepts: [{bullet list of extracted concepts}]
content_gaps: [{any identified gaps}]
icp_targeting:
  builder_angle: '{how content speaks to builders}'
  sme_angle: '{how content speaks to SMEs}'
  dual_funnel_opportunities: '{bridging points}'
visual_analysis_summary: '{key visual moments, proof points, demo sequences — or empty}'
keyword_data:
  primary_candidates: [{keyword, volume, competition}]
  secondary_keywords: [{supporting and trending keywords}]
  serp_gaps: [{uncovered content angles}]
image_catalog:
  - asset: '{filename}'
    source_path: '{relative path from project root}'
    type: '{diagram|broll|thumbnail|motion-graphic|logo}'
    description: '{inferred description}'
    storyboard_context: '{what it shows and which segment it accompanies — if storyboard exists}'
---
```

Then immediately proceed to load and execute {nextStepFile}.

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user confirms (C or affirmative response) and the output file has been created with source material summary and image catalog will you then load and read fully `./step-02-format.md` to execute format selection.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Output mode selected (project or standalone)
- Source material discovered and loaded (auto-scanned in project mode)
- Image catalog built from all available visual assets including logos (project mode)
- Storyboard cross-referenced with visual assets (if storyboard exists)
- ICP targeting analysis completed (builder angle, SME angle, dual-funnel opportunities)
- Visual analysis summary extracted (if visual-analysis.json exists)
- Keyword data extracted from strategist research (if keyword research files exist)
- User confirmed which sources to use
- Content gaps flagged (if any)
- Output file created with source summary, image catalog, ICP targeting, and keyword data in frontmatter
- Key concepts extracted and documented

### ❌ SYSTEM FAILURE:

- Generating blog or email content in this step
- Not auto-scanning the project folder in project mode (asking user to provide file paths manually)
- Skipping image cataloguing
- Not presenting findings to user
- Proceeding without user confirmation
- Not creating the output file

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
