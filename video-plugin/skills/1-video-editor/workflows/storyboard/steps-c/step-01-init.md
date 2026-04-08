---
name: 'step-01-init'
description: 'Scope selection, discover input files, create storyboard output doc from template'

nextStepFile: './step-02-production-brief.md'
outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
templateFile: '../templates/storyboard-template.md'
---

# Step 1: Initialize Storyboard

## STEP GOAL:

Determine storyboard scope (intro-only or full-video), discover all required input files from the project, and create the storyboard output document from the template.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are a video production planner
- Technical, concise, efficient communication
- You bring expertise in visual pacing, segment design, and B-roll strategy
- User brings their creative vision and content goals

### Step-Specific Rules:

- Focus ONLY on initialization: scope, input discovery, output creation
- FORBIDDEN to perform any storyboarding in this step
- Auto-proceed to step 2 after setup

## EXECUTION PROTOCOLS:

- 🎯 Get scope selection, discover input files, create output document from template
- 💾 Create {outputFile} from {templateFile} with populated frontmatter
- 🚫 Do NOT storyboard in this step — initialization only

## CONTEXT BOUNDARIES:

- Available context: Module config, project folder structure, discovered input files
- Focus: Scope selection and input file discovery only
- Limits: Do NOT plan any visual segments in this step
- Dependencies: Requires transcript + visual analysis to be present before proceeding

## MANDATORY SEQUENCE

### 1. Scope Selection

"**Storyboard — Initialization**

What scope for this storyboard?

**[I] Intro Only** — Detailed storyboard for intro section (15+ visual events/min, high density)
**[F] Full Video** — Intro (detailed) + body sections (chapter transitions, selective B-roll, 7-10 events/min)

Select: [I] Intro Only / [F] Full Video"

#### Menu Handling Logic:
- IF I: Set `scope: intro-only`, then proceed to step 2
- IF F: Set `scope: full-video`, then proceed to step 2
- IF Any other: Help user understand scope options, then redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to step 2 after user selects [I] or [F]

### 2. Discover Input Files

"**Discovering project files...**"

Search in `{project_folder}/{project-slug}/` for:

**REQUIRED — HARD BLOCK (cannot proceed without these):**

The analysis folder structure is: `video-editor/analysis/{content-type}/` where `{content-type}` is `intro`, `body`, `outro`, etc. Each content-type subfolder contains its own `transcript.json`, `visual-analysis.json`, and `audio-analysis.json`.

**CRITICAL DISTINCTION — Target vs B-Roll Source:**
- The **target segment** is what we're storyboarding (e.g., `intro`) — its transcript provides speech timing and captions
- The **B-roll source** is the **main video** (typically `body`) — its visual analysis is where extractable B-roll lives (screen recordings, demos, tools, slides)
- These are usually DIFFERENT analysis folders. The intro is mostly speaker-to-camera; the B-roll comes from the full main recording

1. **Target transcript:** `video-editor/analysis/{target-content-type}/transcript.json` — MANDATORY. Provides word-level speech timing, captions, and section structure for the segment being storyboarded.
2. **Main video visual analysis:** `video-editor/analysis/{main-content-type}/visual-analysis.json` — MANDATORY. This is the visual analysis of the **full main video** (usually `body`), which identifies screen recordings, tool demos, slides, and other non-speaker content available for B-roll extraction. This is where extractable B-roll is discovered.
3. **Target visual analysis:** `video-editor/analysis/{target-content-type}/visual-analysis.json` — MANDATORY. Identifies speaker position in the target segment for the speaker position map and text placement decisions.

**Strongly recommended:**
4. **Audio analysis:** `video-editor/analysis/{target-content-type}/audio-analysis.json` — pacing calibration, silence detection
5. **Main video transcript:** `video-editor/analysis/{main-content-type}/transcript.json` — Context for what's being discussed during B-roll candidate segments
6. **Clip plan(s):** `video-editor/clips/*-clip-plan.md` — segment timing from clipping workflow
7. **Script:** `copywriter/scripts/script-*.md` — section structure and B-roll suggestions

**Optional:**
8. **Clipped video files:** `video-editor/clips/*.mp4` — source video references
9. **Existing B-roll:** `video-editor/broll/*.mp4` — already extracted B-roll
10. **Existing motion graphics:** `video-editor/motion-graphics/*.mp4` — already generated MG

**Branded assets (always available):**
11. **Branded assets folder:** `{project-root}/_bmad/_memory/video-editor-sidecar/branded-assets/` — Contains reusable brand images (Upwork profile, {YOUR_COMPANY} logo, etc.) used by branded Remotion templates. These are constant across all videos.

Discover all available analysis subfolders:
- Search: `{project_folder}/{project-slug}/video-editor/analysis/*/`
- List all content-types found (e.g., `intro`, `body`)

Ask user to confirm:
"**Which segment are you storyboarding, and where is the B-roll?**

Analysis folders found: {list of content-type subfolders}

- **Target segment** (what we're editing): {auto-suggest based on scope — `intro` if intro-only}
- **B-roll source** (main video to scan for B-roll): {auto-suggest `body` if it exists}

Confirm or adjust these assignments."

Present discovery results:
"**Input Files:**

| # | Type | Source | Status | File |
|---|------|--------|--------|------|
| 1 | Transcript (target) | {target-content-type} | {found/MISSING} | {path} |
| 2 | Visual Analysis (main — B-roll source) | {main-content-type} | {found/MISSING} | {path} |
| 3 | Visual Analysis (target — speaker map) | {target-content-type} | {found/MISSING} | {path} |
| 4 | Audio Analysis | {target-content-type} | {found/missing} | {path} |
| 5 | Transcript (main — B-roll context) | {main-content-type} | {found/missing} | {path} |
| 6 | Clip Plan | — | {found/missing} | {path} |
| 7 | Script | — | {found/missing} | {path} |
| 8 | Clipped Video | — | {found/count} | {paths} |
| 9 | Existing B-Roll | — | {found/count} | {paths} |
| 10 | Existing MG | — | {found/count} | {paths} |
| 11 | Branded Assets | — | {found/count} | {paths} |"

**If target transcript is missing:** "Target transcript is REQUIRED. Run **[TR] Transcription** on the {target-content-type} segment first." Do NOT proceed.
**If main video visual analysis is missing:** "Main video visual analysis is REQUIRED. Run **[VA] Visual Analysis** on the main video ({main-content-type}) first — this is where B-roll candidates are identified." Do NOT proceed.
**If target visual analysis is missing:** "Target visual analysis is REQUIRED. Run **[VA] Visual Analysis** on the {target-content-type} segment first — this is needed for the speaker position map." Do NOT proceed.
All three must be present to continue.

### 3. Create Output File

Create {outputFile} from {templateFile} with frontmatter populated:

```yaml
---
status: DRAFT
scope: '{scope}'
stepsCompleted: ['step-01-init']
lastStep: 'step-01-init'
date: '{current_date}'
user_name: '{user_name}'
video_id: '{video-id}'
project_slug: '{project-slug}'
target_content_type: '{target-content-type}'   # e.g., intro
main_content_type: '{main-content-type}'       # e.g., body
---
```

### 4. Auto-Proceed

"**Initialization Complete — Scope: {scope}**

Proceeding to production brief..."

Update {outputFile} frontmatter by appending 'step-01-init' to stepsCompleted, then load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Scope selected (intro-only or full-video)
- Transcript AND Visual Analysis both found and validated
- Branded assets folder checked
- Input files discovered and status reported
- Output file created from template
- Auto-proceeding to production brief

### FAILURE:

- Proceeding without Transcript (HARD BLOCK)
- Proceeding without Visual Analysis (HARD BLOCK)
- Not asking user for scope selection
- Performing storyboarding in this step
- Not reporting missing input files
