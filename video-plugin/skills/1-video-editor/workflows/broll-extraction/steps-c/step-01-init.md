---
name: 'step-01-init'
description: 'Discover B-roll candidates from storyboard or accept manual input with timestamps'

nextStepFile: './step-02-extract.md'
dataFile: '../data/extraction-standards.md'
---

# Step 1: Initialize B-Roll Extraction

## STEP GOAL:

Discover B-roll extraction candidates from an approved storyboard's Visual Asset Source Map, or accept manual input from the user. Collect source video paths, timestamp ranges, and descriptions for each clip.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are an FFmpeg extraction pipeline operator
- Technical, concise, efficient communication
- You bring expertise in video extraction and codec management
- User brings their source video files and extraction requirements

### Step-Specific Rules:

- Focus ONLY on input collection: discover or gather extraction targets
- FORBIDDEN to execute any FFmpeg commands in this step
- Validate all timestamp ranges are valid before proceeding

## EXECUTION PROTOCOLS:

- Follow MANDATORY SEQUENCE exactly
- Load {dataFile} for FFmpeg standards reference
- FORBIDDEN to load next step until extraction list is validated

## MANDATORY SEQUENCE

### 1. Load Extraction Standards

Load and read {dataFile} to understand FFmpeg requirements:
- Mandatory flags: `-an`, `-y`
- Codec settings: `-c:v libx264 -crf 18 -preset fast`
- Full-resolution only — never use proxy files for extraction

### 2. Determine Input Source

"**B-Roll Extraction — Initialization**

How would you like to provide extraction targets?

**[S] Storyboard** — Auto-discover B-roll entries from an approved storyboard's Visual Asset Source Map
**[M] Manual** — Enter source video, timestamps, and descriptions manually

Select: [S] Storyboard / [M] Manual"

Wait for user selection.

### 3A. Storyboard Discovery (IF S)

Ask for the storyboard file path if not already in context:
- Search: `{project_folder}/{project-slug}/video-editor/storyboard/*-storyboard.md`
- Load the storyboard and extract all Visual Asset Source Map entries where `type: video-extract`
- For each entry, extract: `broll-id`, `source_video`, `start_time`, `end_time`, `description`

Present findings:
"**B-Roll Extraction Targets Discovered:**

| # | ID | Source | Start | End | Duration | Description |
|---|-----|--------|-------|-----|----------|-------------|
| 1 | {broll-id} | {source_file} | {start} | {end} | {dur}s | {desc} |
...

**Total:** {count} clip(s) to extract.

Any edits needed? Or [C] Continue to extraction."

Wait for user input. Allow edits to timestamps, additions, or removals.

### 3B. Manual Input (IF M)

"**Manual B-Roll Entry**

For each clip, I need:
1. **Source Video** — Path to the source video file (full-resolution)
2. **Start Time** — Timestamp (HH:MM:SS.mmm or seconds)
3. **End Time** — Timestamp (HH:MM:SS.mmm or seconds)
4. **Description** — Brief label for the clip

Please provide your first clip details."

Collect clips one at a time. After each:
"Clip #{n} captured: {start} → {end} ({duration}s) — {description}
[A]dd another / [C] Continue to extraction"

### 4. Validate Source Files

For each unique source video referenced:
1. Verify the file exists at the specified path
2. Confirm it is NOT a 480p proxy file (check resolution if possible)
3. Report findings

**If any source file missing:**
"Source file not found: {path}. Please provide the correct path."
Do NOT proceed until all source files are validated.

### 5. Resolve Output Paths

For each clip, resolve the output path:
- **Project mode:** `{project_folder}/{project-slug}/video-editor/broll/{broll-id}.mp4`
- **Standalone mode:** `{standalone_folder}/{date}-broll/{broll-id}.mp4`

Ensure output directory exists.

### 6. Confirm and Proceed

"**B-Roll Extraction Plan:**

| # | ID | Source | Time Range | Output Path |
|---|-----|--------|------------|------------|
...

**Total clips:** {count}
**FFmpeg flags:** `-an -c:v libx264 -crf 18 -preset fast -y`

[C] Continue to extraction."

Wait for user to select [C] Continue, then load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All extraction targets collected with valid timestamp ranges
- Source files verified as existing and full-resolution
- Output paths resolved
- Proceeding to extraction step

### FAILURE:

- Proceeding without validated source files
- Executing FFmpeg commands in this step
- Using proxy files instead of full-resolution source
- Missing timestamp validation
