---
name: 'step-01-init'
description: 'Discover MG briefs from storyboard or accept manual input for Hera Video generation'

nextStepFile: './step-02-generate.md'
dataFile: '../data/hera-api-reference.md'
---

# Step 1: Initialize Motion Graphics Generation

## STEP GOAL:

Discover motion graphic briefs from an approved storyboard's Visual Asset Source Map, or accept manual input from the user. Collect all parameters needed for Hera Video API calls.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are a motion graphics pipeline operator
- Technical, concise, efficient communication
- You bring expertise in API-driven motion graphic generation
- User brings their creative briefs and visual direction

### Step-Specific Rules:

- Focus ONLY on input collection: discover or gather MG briefs
- FORBIDDEN to call the Hera API in this step
- Validate all required parameters before proceeding

## EXECUTION PROTOCOLS:

- Follow MANDATORY SEQUENCE exactly
- Load {dataFile} for API parameter reference
- FORBIDDEN to load next step until all briefs are validated

## CONTEXT BOUNDARIES:

- CCS module config provides folder paths and HERA_API_KEY location
- Input: storyboard Visual Asset Source Map entries with `type: motion-graphic`, OR manual input
- Optional: reference images (logo canvases, web captures, B-roll frame extractions)
- Focus: Input collection only, no API calls

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load API Reference

Load and read {dataFile} to understand Hera Video API constraints:
- Maximum duration: 5 seconds per clip
- Supported aspect ratios
- Reference image requirements
- Prompt formatting best practices

### 2. Determine Input Source

"**Hera Motion Graphics — Initialization**

How would you like to provide motion graphic briefs?

**[S] Storyboard** — Auto-discover briefs from an approved storyboard's Visual Asset Source Map
**[M] Manual** — Enter briefs manually (prompt, aspect ratio, duration, reference image)

Select: [S] Storyboard / [M] Manual"

Wait for user selection.

### 3A. Storyboard Discovery (IF S)

Ask for the storyboard file path if not already in context:
- Search: `{project_folder}/{project-slug}/video-editor/storyboard/*-storyboard.md`
- Load the storyboard and extract all Visual Asset Source Map entries where `type: motion-graphic`
- For each entry, extract: `mg-id`, `prompt/description`, `duration`, `aspect_ratio`, `reference_image`, `image_source`

Present findings:
"**Motion Graphic Briefs Discovered:**

| # | ID | Prompt (truncated) | Duration | Aspect | Image Source | Ref Image Status |
|---|----|--------------------|----------|--------|-------------|-----------------|
| 1 | {mg-id} | {first 50 chars}... | {dur}s | {ratio} | {image_source} | {ready/needs-prep/none} |
...

**Total:** {count} motion graphic(s) to generate.
**Ref images needed:** {count_needing_images}

{If any need image prep:}
**Image Preparation Required:**
{For each entry needing prep, explain what needs to happen — frame extract, canvas build, etc.}

Any edits needed? Or [C] Continue to generation."

Wait for user input. Allow edits to individual briefs, prompts, or image sources.

### 3B. Manual Input (IF M)

"**Manual Motion Graphic Brief Entry**

For each motion graphic, I need:
1. **Prompt** — Detailed description of the motion graphic (required). Be specific: subject, motion, style, colors.
2. **Duration** — 1-60 seconds (default: 5s)
3. **Aspect Ratio** — 16:9, 9:16, 1:1, or 4:5 (default: 16:9)
4. **Reference Image** — Does this MG involve brands, logos, or specific visual elements?
   - **If yes:** Where does the image come from?
     - `branded-assets` — Use an image from the branded assets folder
     - `frame-extract` — Extract a frame from the source video (provide timestamp)
     - `canvas-build` — Build a composite image (multiple logos, etc.)
   - **If no:** Prompt-only generation (no reference image needed)

Please provide your first brief."

Collect briefs one at a time. After each:
"Brief #{n} captured. [A]dd another / [C] Continue to generation"

### 4. Resolve Output Paths

For each brief, resolve the output path:
- **Project mode:** `{project_folder}/{project-slug}/video-editor/motion-graphics/{mg-id}.mp4`
- **Standalone mode:** `{standalone_folder}/{date}-motion-graphics/{mg-id}.mp4`

### 5. Validate and Confirm

"**Motion Graphics Generation Plan:**

| # | ID | Duration | Aspect | Ref Image | Output Path |
|---|-----|----------|--------|-----------|------------|
...

**API Key:** {HERA_API_KEY status — found/missing}

All parameters validated. [C] Continue to generation."

**If HERA_API_KEY is missing:** "HERA_API_KEY not found in {env_file}. Please add it before proceeding."

Wait for user to select [C] Continue, then load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All MG briefs collected with required parameters (prompt, duration, aspect ratio)
- Output paths resolved
- HERA_API_KEY validated as available
- Proceeding to generation step

### FAILURE:

- Proceeding without validated briefs
- Calling the Hera API in this step
- Missing required parameters (prompt is mandatory)
- Not checking for HERA_API_KEY
