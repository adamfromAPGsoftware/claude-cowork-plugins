---
name: 'step-01-init'
description: 'Resolve video file from ingest registry, prefer proxy over raw'

nextStepFile: './step-02-analyse.md'
---

# Step 1: Init & Resolve Video

## STEP GOAL:

To accept a video ID, look up its Video Ingest registry YAML, resolve the correct file path (preferring proxy over raw for cost efficiency), and validate the file exists before proceeding to audio analysis.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip scanning the registry — every field must be examined
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator and audio analyst
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Report findings clearly with structured data

### Step-Specific Rules:

- 🎯 Focus ONLY on resolving the correct video file — do NOT run any analysis yet
- 🚫 FORBIDDEN to proceed without a valid, accessible video file
- 💬 Report resolution results in structured format
- 📋 Always prefer proxy file over raw when available

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Track the resolved file path for the next step
- 📖 Report resolution status before proceeding
- 🚫 FORBIDDEN to proceed if video file does not exist on disk

## CONTEXT BOUNDARIES:

- Available context: CCS module config (project_folder, video_ingest_folder)
- Focus: Video file resolution only
- Limits: Do NOT extract audio or run any FFmpeg commands yet
- Dependencies: Video must be registered via Video Ingest workflow

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Accept Video ID

If video ID was not provided during workflow invocation, ask the user:

"**Which video should I analyse?**

Please provide the video ID (e.g., `project-alpha-body`)."

### 2. Locate Registry YAML

Search for the video's registry YAML file at:
`{project_folder}/{project-slug}/video-editor/raw/{video-id}.yaml`

**If YAML not found:**
"**Error: No registry entry found for video `{video-id}`.**

Expected location: `{project_folder}/{project-slug}/video-editor/raw/{video-id}.yaml`

To fix: Run the Video Ingest workflow first to register this video."
→ HALT. Do not proceed.

**If YAML found:**
Read the complete YAML file and extract all metadata fields.

### 3. Resolve File Path (Proxy Preference)

**Resolution logic:**

1. Read the `role` field from the YAML
2. Read the `paired_with` field from the YAML
3. **If this file IS a proxy** (`role: proxy`): use this file's `source_path` directly
4. **If this file IS raw AND has a `paired_with` value:**
   - Look up the paired file's YAML: `{project_folder}/{project-slug}/video-editor/raw/{paired_with}.yaml`
   - If paired file has `role: proxy` → use the paired proxy file's `source_path`
   - If paired file is not a proxy → use the original raw file's `source_path`
5. **If this file IS raw AND has no `paired_with`:** use this file's `source_path`

### 4. Validate File Exists

Check that the resolved file path exists on disk.

**If file does not exist:**
"**Error: Resolved file not found on disk.**

File: `{resolved_path}`
Role: `{proxy/raw}`

The registry points to a file that no longer exists. Please check the file location."
→ HALT. Do not proceed.

### 5. Report Resolution Results

"**Video Resolved.**

**Video ID:** `{video-id}`
**Project Group:** `{project_group}`
**Content Type:** `{content_type}`
**Resolved File:** `{resolved_filename}`
**File Role:** `{proxy/raw}`
**File Path:** `{resolved_path}`
**Resolution:** `{proxy preferred / raw fallback / raw only}`

**Proceeding to audio analysis...**"

### 6. Auto-Proceed to Analysis

Display: "**Proceeding to FFmpeg audio analysis...**"

#### Menu Handling Logic:

- After resolution results are reported and file is validated, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed init step with no user choices at this stage
- Proceed directly to next step after resolution report
- If file not found or YAML missing, HALT and wait for user guidance

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN a valid video file has been resolved and confirmed to exist on disk will you load and read fully `{nextStepFile}` to execute FFmpeg audio analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Video ID accepted
- Registry YAML located and read
- Proxy preference logic applied correctly
- Resolved file validated on disk
- Resolution results reported in structured format
- Auto-proceeded to step 2

### ❌ SYSTEM FAILURE:

- Skipping proxy preference logic
- Proceeding with a file that doesn't exist
- Not checking paired_with for proxy availability
- Running FFmpeg before file resolution
- Proceeding without reporting resolution results

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
