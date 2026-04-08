---
name: 'step-01-init'
description: 'Initialize video clipping workflow, auto-detect content type from registry, discover and load input files'

nextStepFile: './step-02-transcript-analysis.md'
outputFile: '{project_folder}/{project-slug}/video-editor/clips/{video-id}-clip-plan.md'
templateFile: '../data/clip-plan-template.md'
---

# Step 1: Initialize Video Clipping

## STEP GOAL:

Auto-detect content type from the proxy registry YAML, discover and validate all required input files, optionally load reference documents, and create the clip plan output file.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 AUTO-PROCEED: No user interaction in this step — all values resolved from registry
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video editing automation assistant
- ✅ Technical, concise, efficient communication
- ✅ You bring expertise in audio analysis and video editing automation
- ✅ User brings their content goals and video files

### Step-Specific Rules:

- 🎯 Focus ONLY on initialization: content type auto-detection, input discovery, validation
- 🚫 FORBIDDEN to perform any analysis or clipping in this step
- 🚫 FORBIDDEN to ask the user any questions — all values come from the registry
- 🚫 FORBIDDEN to proceed without all 3 required JSON files validated

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Create output file from {templateFile}
- 📖 Update frontmatter with content type and input paths
- 🚫 FORBIDDEN to load next step until inputs are validated

## CONTEXT BOUNDARIES:

- This is the first step — no prior context
- CCS module config provides folder paths
- Required: 3 JSON analysis files from upstream workflows
- Required: Script from copywriter workflow
- Optional: Content concept from strategist
- Focus: Setup only, no analysis

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Resolve Content Type from Registry

"**Video Clipping Workflow — Initialization**"

Read the proxy registry YAML file for the current video from `{video_ingest_folder}` or `{project_folder}/{project-slug}/video-editor/raw/`.

Extract `content_type` from the registry YAML and map:
- `body` → Set `content_type: main`, `buffer_ms: 300`
- `intro` → Set `content_type: intro`, `buffer_ms: 150`
- `outro` → Set `content_type: main`, `buffer_ms: 300`

**Fallback (no registry found):** Infer from the video filename:
- Filename contains `intro` → `content_type: intro`, `buffer_ms: 150`
- Otherwise → `content_type: main`, `buffer_ms: 300`

"**Auto-detected content type: {content_type} (buffer: {buffer_ms}ms)**"

### 2. Discover Required Input Files

"**Discovering analysis files...**"

Search for the 3 required JSON files in `{video_ingest_folder}` and current project folder:

**Required files:**
1. Audio analysis: `{video-id}-audio.json`
2. Transcript: `{video-id}-transcript.json`
3. Visual analysis: `{video-id}-visual.json`

**If user hasn't specified a video ID:**
"Please provide the video ID or the path to the analysis files."

**For each file found:**
- Validate it exists
- Validate it is valid JSON
- Confirm the video ID matches across all 3 files

**Present findings:**
"**Input Files Found:**
- [1] ✅ Audio: {filename} ({size})
- [2] ✅ Transcript: {filename} ({size})
- [3] ✅ Visual: {filename} ({size})

**Video ID:** {video-id}"

**If any required file is missing:**
"❌ Missing required file: {filename}. Please provide the path or run the upstream analysis workflow first."
Do NOT proceed until all 3 files are available.

### 3. Discover Required Script and Optional References

"**Checking for script and reference documents...**"

**Script — REQUIRED (location depends on content type):**

**Long-form** (body, intro, outro):
- Search: `{project_folder}/{project-slug}/copywriter/scripts/script-*.md`
- These are produced by the Copywriter workflow

**Short-form** (sf-NN videos):
- Search: `{project_folder}/{project-slug}/video-editor/short-form/scripts/sf-{NN}-script.md`
- These are produced by the Copywriter SS (short-form script) workflow and live alongside the short-form video assets

**Resolution:**
- If the video ID matches pattern `sf-{NN}` → search the short-form scripts path
- Otherwise → search the copywriter scripts path
- If found: "✅ Found script: {filename}. Will use for transcript-vs-script analysis."
- If NOT found: "❌ **Script is required for transcript-vs-script analysis.** Provide the script path or run the Copywriter workflow first."
  → HALT. Do not proceed without a script.

**Content Concept / ICP (from strategist):**
- Search: `{project_folder}/{project-slug}/strategist/ideation/content-concept-*.md`
- If found: "✅ Found content concept: {filename}. Will use for ICP relevance scoring."
- If not found: "ℹ️ No content concept found. Transcript analysis will skip ICP relevance check."

### 4. Create Output File

Create {outputFile} from {templateFile} with frontmatter populated:

```yaml
---
stepsCompleted: ['step-01-init']
lastStep: 'step-01-init'
date: '{current_date}'
user_name: '{user_name}'
video_id: '{video-id}'
source_file: '{proxy_video_path}'
raw_source_file: '{raw_video_path}'
content_type: '{content_type}'
buffer_ms: {buffer_ms}
script_path: '{script_path}'
---
```

**Proxy vs Raw resolution:**
- `source_file` — proxy video (720p, used for API calls and analysis throughout the pipeline)
- `raw_source_file` — raw/full-resolution video (used ONLY for final FFmpeg output in step 5)
- Resolve raw path from the registry: find the YAML where `role: raw` and `paired_with` matches the proxy's `video_id`, then use its `source_path`
- If no raw file found: fall back to proxy for output and log a warning

Fill in the Metadata section of the clip plan with the resolved values.

### 5. Summary and Proceed

"**Initialization Complete**

| Setting | Value |
|---------|-------|
| Content Type | {content_type} |
| Buffer | {buffer_ms}ms |
| Video ID | {video-id} |
| Proxy Source | {proxy_video_path} |
| Raw Source | {raw_video_path or 'N/A — using proxy'} |
| Audio Analysis | ✅ Loaded |
| Transcript | ✅ Loaded |
| Visual Analysis | ✅ Loaded |
| Script Reference | ✅ Loaded |
| ICP Reference | {✅ Loaded / ℹ️ Not available} |

**Proceeding to transcript analysis...**"

Update {outputFile} frontmatter with `stepsCompleted: ['step-01-init']`, then load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Content type auto-detected from registry (intro/main) with correct buffer
- All 3 required JSON files discovered and validated
- Required script discovered and validated
- Optional reference documents discovered (if available)
- Output file created from template with correct metadata
- Proceeding to transcript analysis step with no user interaction

### ❌ SYSTEM FAILURE:

- Proceeding without all 3 required JSON files
- Not validating JSON file integrity
- Asking the user for content type (must auto-detect from registry)
- Proceeding without a script (script is REQUIRED for transcript-vs-script analysis)
- Performing analysis in this step (that's step 2+)
- Hardcoded paths instead of variables

**Master Rule:** All 3 required input files MUST be validated before proceeding. Content type MUST be auto-detected from registry — no user interaction.
