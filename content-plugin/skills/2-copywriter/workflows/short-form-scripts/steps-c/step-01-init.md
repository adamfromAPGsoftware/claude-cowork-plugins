---
name: 'step-01-init'
description: 'Load long-form analysis outputs and validate all required inputs for short-form script generation'

nextStepFile: './step-02-concept-extract.md'
scriptRulesData: '../data/script-rules.md'
---

# Step 1: Initialize — Load Long-Form Analysis

## STEP GOAL:

Load the long-form video's analysis outputs (transcript, visual analysis, audio analysis) and validate that all required inputs exist for concept extraction.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 AUTO-PROCEED: Minimal user interaction — auto-detect inputs from project folder
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a short-form content strategist specialising in vertical video repurposing
- ✅ You bring expertise in hook psychology, pacing, and concept extraction
- ✅ Collaborative partnership with the user

### Step-Specific Rules:

- 🎯 Focus ONLY on initialization: input discovery and validation
- 🚫 FORBIDDEN to extract concepts or write scripts in this step
- 🚫 FORBIDDEN to proceed without all 3 required analysis files validated

## MANDATORY SEQUENCE

### 1. Discover Long-Form Analysis Files

"**Short-Form Script Generation — Initialization**"

Search the active project's video-editor output folder for long-form analysis files:

**Required files (from long-form video pipeline):**
1. **Transcript:** `{project_folder}/{project-slug}/video-editor/analysis/*/transcript.json` — word-level timestamped transcript
2. **Visual analysis:** `{project_folder}/{project-slug}/video-editor/analysis/*/visual-analysis.json` — scene-by-scene visual descriptions
3. **Audio analysis:** `{project_folder}/{project-slug}/video-editor/analysis/*/audio-analysis.json` — energy levels, silence, speech patterns

Search across all sub-folders (intro/, body/, etc.) and consolidate.

**For each file found:**
- Validate it exists and is valid JSON
- Note which video segment it belongs to (intro, body, etc.)

"**Long-Form Analysis Files Found:**
- [1] ✅ Transcript: {filename} ({segment})
- [2] ✅ Visual Analysis: {filename} ({segment})
- [3] ✅ Audio Analysis: {filename} ({segment})"

**If any required file is missing:**
"❌ Missing: {filename}. Run the long-form video pipeline first (Audio Analysis → Transcription → Visual Analysis)."
Do NOT proceed until all files are available.

### 2. Load Script Rules

Load `{scriptRulesData}` — the short-form script structure, hook patterns, and CTA patterns.

### 3. Load Brand Context

Load brand guidelines from `{project-root}/references/brand-voice.md` for voice consistency.

### 4. Check for Existing Short-Form Scripts

Search `{project_folder}/{project-slug}/video-editor/short-form/scripts/` for any existing `sf-*-script.md` files.

- If found: "⚠️ Found {count} existing short-form scripts. These will NOT be overwritten — new scripts will be generated alongside them."
- If not found: "ℹ️ No existing short-form scripts found. Starting fresh."

### 5. Create Output Directory

Ensure `{project_folder}/{project-slug}/video-editor/short-form/scripts/` exists.

### 6. Summary and Proceed

"**Initialization Complete**

| Setting | Value |
|---------|-------|
| Project | {project_name} |
| Long-form segments | {list of segments found} |
| Transcript words | {total word count across all transcripts} |
| Visual scenes | {total scene count} |
| Brand voice | ✅ Loaded |
| Script rules | ✅ Loaded |

**Proceeding to concept extraction...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 3 required analysis files discovered and validated
- Script rules loaded
- Brand context loaded
- Output directory created
- Proceeding to concept extraction

### ❌ SYSTEM FAILURE:

- Proceeding without all 3 analysis files
- Extracting concepts or writing scripts in this step
- Not loading script rules or brand context

**Master Rule:** All required analysis files MUST be validated before proceeding.
