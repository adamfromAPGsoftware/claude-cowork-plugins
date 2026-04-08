---
name: 'step-01-init'
description: 'Discover video from registry, resolve proxy/raw file path, gather optional transcription parameters'

nextStepFile: './step-02-extract-audio.md'
---

# Step 1: Initialize & Resolve Video

## STEP GOAL:

To discover the target video from the Video Ingest registry, resolve the optimal file path (proxy preferred over raw for cost efficiency), and gather any optional transcription parameters before proceeding to audio extraction.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed without confirming the target video
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a transcription pipeline operator
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You execute prescriptive instructions precisely
- ✅ You bring API integration expertise

### Step-Specific Rules:

- 🎯 Focus ONLY on discovering the video and resolving the file path
- 🚫 FORBIDDEN to start audio extraction or API calls in this step
- 💬 Present findings clearly and confirm before proceeding
- 📋 Always prefer proxy file over raw file when a proxy pair exists

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Track resolved file path and parameters for next steps
- 📖 Validate registry YAML exists and contains required fields
- 🚫 FORBIDDEN to proceed without a valid source file path

## CONTEXT BOUNDARIES:

- Available: Video Ingest registry YAMLs at `{project_folder}/{project-slug}/video-editor/raw/`
- Focus: File discovery and path resolution only
- Limits: Do not extract audio or call APIs in this step
- Dependencies: Video Ingest workflow must have registered the video

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Receive Video Target

Ask the user for the video to transcribe:

"**Which video should I transcribe?**

Please provide one of:
- A video ID (e.g., `body-001`)
- A path to the video's registry YAML
- A project slug and I'll list available videos"

### 2. Discover Video Registry YAML

**If video ID provided:**
- Search for `{video-id}.yaml` in `{project_folder}/{project-slug}/video-editor/raw/`

**If project slug provided:**
- List all YAML files in `{project_folder}/{project-slug}/video-editor/raw/`
- Present available videos for selection

**If direct path provided:**
- Load the YAML at the provided path

**Validation:**
- Confirm the YAML file exists
- Confirm it contains: `video_id`, `role`, `metadata.source_path`
- If missing or invalid: "Registry YAML not found or incomplete. Has Video Ingest been run for this video?"

### 3. Resolve Optimal File Path (Proxy Preferred)

**Read the registry YAML and apply proxy resolution logic:**

**IF `role: 'raw'` AND `paired_with` is not null:**
- Load the paired proxy YAML: `{paired_with}.yaml` from the same directory
- Use the proxy's `metadata.source_path` as the target file
- Report: "Found proxy file for {video_id}. Using proxy for cost-efficient transcription."

**IF `role: 'proxy'`:**
- Use this file's `metadata.source_path` directly
- Report: "Using proxy file directly."

**IF `role: 'raw'` AND `paired_with` is null:**
- Use this file's `metadata.source_path` (no proxy available)
- Report: "No proxy available for {video_id}. Using raw file."

**Validate the resolved file path exists on disk.**

### 4. Gather Optional Parameters

"**Optional transcription settings** (press Enter to skip any):

1. **Language:** Default is `en`. Override? (e.g., `es`, `fr`, `de`, `multi`)
2. **Speaker diarisation:** Identify different speakers? (yes/no, default: no)
3. **DeepGram model:** Default is `nova-3`. Override? (e.g., `nova-3-medical`)
4. **Keyterm prompting:** Any domain-specific terms to boost recognition? (comma-separated list or skip)
   - Nova-3 uses the `keyterm` API parameter (NOT `keywords` — that parameter is incompatible with Nova-3)
   - Each term gets a boost value of 1-5 (default: 2)"

### 5. Confirm and Proceed

Present a summary:

"**Transcription Configuration:**

| Setting | Value |
|---------|-------|
| Video ID | {video_id} |
| Source file | {resolved source_path} |
| File type | {proxy/raw} |
| Language | {language or 'en'} |
| Diarisation | {yes/no} |
| Model | {model or 'nova-3'} |
| Keyterms | {keyterms or 'none'} |

**Proceeding to audio extraction...**"

### 6. Auto-Proceed

Display: "**Proceeding to audio extraction...**"

#### Menu Handling Logic:

- After configuration is confirmed, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed init step — proceed directly after confirmation
- If user wants to change settings, allow modifications and re-confirm

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the video registry YAML is loaded, the optimal file path is resolved, and optional parameters are gathered, will you then load and read fully `{nextStepFile}` to execute audio extraction.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Video registry YAML discovered and loaded
- Proxy file used when available (cost optimisation)
- File path validated (exists on disk)
- Optional parameters gathered
- Configuration summary presented
- Proceeding to audio extraction

### ❌ SYSTEM FAILURE:

- Not checking for proxy file pair
- Using raw file when proxy is available
- Proceeding without validating file path exists
- Not presenting configuration summary
- Skipping optional parameter gathering

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
