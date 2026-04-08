---
name: 'step-01-init'
description: 'Detect ingest folder, scan for new video files, identify file types'

nextStepFile: './step-02-register.md'
---

# Step 1: Detect New Video Files

## STEP GOAL:

To detect the video ingest folder, scan it for new video files, and identify each file's type (proxy vs raw, body vs intro).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip scanning — every file in the ingest folder must be examined
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator and file system analyst
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Report findings clearly with counts and file details

### Step-Specific Rules:

- 🎯 Focus ONLY on detecting and classifying files — do NOT extract metadata yet
- 🚫 FORBIDDEN to modify any files during detection
- 💬 Report all findings in a structured format
- 📋 Supported video formats: MP4, MOV, MKV, AVI, WEBM, ProRes

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Build an internal file manifest for the next step
- 📖 Report detection results before proceeding
- 🚫 FORBIDDEN to proceed if no video files are detected

## CONTEXT BOUNDARIES:

- Available context: `{video_ingest_path}` — resolved during workflow initialization from the active project or standalone context
- Focus: File detection and type classification only
- Limits: Do NOT extract metadata or create YAML files yet
- Dependencies: File System access required, `{video_ingest_path}` must be resolved before this step

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Locate Ingest Folder

Use `{video_ingest_path}` — already resolved during workflow initialization (step 2 of workflow.md) from the active project's sidecar memory or user selection.

Verify the folder exists and is accessible. If the folder is empty or missing, inform the user to drop their video files there and provide the resolved path so they know exactly where to put them.

### 2. Scan Folder for Video Files

List all files in the ingest folder and its immediate subfolders.

**Identify video files by extension:**
- `.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`, `.mxf`

**Ignore non-video files** (thumbnails, .DS_Store, temp files, etc.)

### 3. Classify Each File

For each detected video file, determine:

**File role:**
- **Proxy** — Lower resolution version (typically contains "proxy" in filename or is in a proxy subfolder)
- **Raw** — Full resolution original (typically larger file size, in raw subfolder, or no proxy indicator)

**Content type:**
- **Body** — Main video content (default if no indicator)
- **Intro** — Intro segment (typically contains "intro" in filename)
- **Outro** — Outro segment (if applicable)

**Classification rules:**
1. Check filename for keywords: `proxy`, `raw`, `intro`, `outro`, `body`
2. Check parent folder name for classification hints
3. If ambiguous, default to: Raw + Body

### 4. Report Detection Results

"**Detection Complete.**

**Ingest folder:** `{path}`
**Video files found:** {count}

| # | Filename | Role | Content Type |
|---|----------|------|-------------|
| 1 | {filename} | {proxy/raw} | {body/intro/outro} |
| 2 | ... | ... | ... |

**Proceeding to registration...**"

**If no video files found:**
"**No video files detected in `{path}`.** Please check the folder and try again."
→ HALT. Do not proceed.

### 5. Auto-Proceed to Registration

Display: "**Proceeding to registration and mapping...**"

#### Menu Handling Logic:

- After detection results are reported and files are found, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed init step with no user choices at this stage
- Proceed directly to next step after detection report
- If no files found, HALT and wait for user guidance

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN video files have been detected and classified will you load and read fully `{nextStepFile}` to execute registration and mapping.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Ingest folder located and scanned
- All video files detected and classified (role + content type)
- Detection results reported in structured format
- Auto-proceeded to step 2

### ❌ SYSTEM FAILURE:

- Skipping file classification
- Modifying files during detection
- Proceeding with zero files detected
- Not reporting detection results before proceeding

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
