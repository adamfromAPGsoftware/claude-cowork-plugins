---
name: 'step-02-register'
description: 'Extract metadata, map proxy-raw pairs, group multi-file projects, create YAML files'

nextStepFile: './step-03-confirm.md'
---

# Step 2: Register and Map Video Files

## STEP GOAL:

To extract metadata from each detected video file, map proxy-raw file pairs, group multi-file projects (body + intro), set processing order, and create video metadata YAML files.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip any detected file — every file must be registered
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator and file system analyst
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Report registration results clearly with structured data

### Step-Specific Rules:

- 🎯 Focus on metadata extraction, pair mapping, and project grouping
- 🚫 FORBIDDEN to trigger any pipeline — that comes after user confirmation
- 💬 Report all mappings and groupings in structured format
- 📋 Create YAML files for each registered video

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Create video metadata YAML files in the project output folder
- 📖 Track all mappings and groupings for confirmation step
- 🚫 FORBIDDEN to proceed without completing all registrations

## CONTEXT BOUNDARIES:

- Available context: File manifest from step 1 (detected files with classifications)
- Focus: Metadata extraction, pair mapping, project grouping, YAML creation
- Limits: Do NOT trigger any downstream workflows yet
- Dependencies: Step 1 must have completed with detected files

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Extract Metadata for Each File

For each detected video file, extract:

- **Duration** (hours:minutes:seconds)
- **Resolution** (width x height)
- **Format/Codec** (H.264, ProRes, etc.)
- **File size**
- **Creation date**

Use file system tools to read file properties. If metadata extraction tools are unavailable, extract what is available from file properties and note any limitations.

### 2. Map Proxy-Raw File Pairs

Match proxy files to their raw counterparts using:

**Matching rules (in priority order):**
1. **Identical base name** — `video-001-proxy.mp4` ↔ `video-001.mp4`
2. **Same name, different folder** — `proxy/video-001.mp4` ↔ `raw/video-001.mp4`
3. **Same name, different extension** — `video-001.mp4` (proxy) ↔ `video-001.mov` (raw)

**If a proxy has no matching raw (or vice versa):**
- Flag as unmatched
- Register as standalone file
- Note in the mapping report

### 3. Group Multi-File Projects

Identify files that belong to the same project:

**Grouping rules:**
1. **Shared base name** — `project-alpha-body.mp4` + `project-alpha-intro.mp4` = Project "project-alpha"
2. **Shared folder** — Files in the same subfolder form a project group
3. **Single file** — Standalone files become single-file projects

**For each project group, set processing order:**
1. Body (main content) — processed FIRST
2. Intro — processed SECOND
3. Outro — processed THIRD (if present)

### 4. Create Video Metadata YAML Files

For each registered video, create a YAML file at:
`{project_folder}/{project-slug}/video-editor/raw/{video-id}.yaml`

**YAML structure:**
```yaml
video_id: '{video-id}'
project_group: '{project-name}'
content_type: '{body/intro/outro}'
processing_order: {1/2/3}
role: '{proxy/raw}'
paired_with: '{paired-file-id or null}'
metadata:
  filename: '{original-filename}'
  duration: '{HH:MM:SS}'
  resolution: '{width}x{height}'
  format: '{codec}'
  file_size: '{size}'
  creation_date: '{date}'
  source_path: '{full-path-to-file}'
status: 'registered'
registered_at: '{timestamp}'
```

### 5. Report Registration Results

"**Registration Complete.**

**Files registered:** {count}
**Proxy-raw pairs mapped:** {pair-count}
**Projects identified:** {project-count}

**Project Groups:**

**Project: {project-name}**
| # | File | Role | Type | Order | Paired With |
|---|------|------|------|-------|-------------|
| 1 | {filename} | Raw | Body | 1 | {proxy-file} |
| 2 | {filename} | Proxy | Body | 1 | {raw-file} |
| 3 | {filename} | Raw | Intro | 2 | — |

{Repeat for each project group}

**Unmatched files:** {count or 'None'}

**YAML files created:** {count} at `{output-path}`

**Proceeding to confirmation...**"

### 6. Auto-Proceed to Confirmation

Display: "**Proceeding to user confirmation...**"

#### Menu Handling Logic:

- After registration results are reported, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step — registration results flow directly to confirmation
- Proceed directly to next step after registration report

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN all files have been registered, pairs mapped, projects grouped, and YAML files created will you load and read fully `{nextStepFile}` to execute user confirmation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All detected files have metadata extracted
- Proxy-raw pairs correctly mapped
- Multi-file projects correctly grouped with processing order
- YAML metadata files created for each video
- Registration results reported in structured format
- Auto-proceeded to confirmation step

### ❌ SYSTEM FAILURE:

- Skipping files during registration
- Incorrect proxy-raw pair matching
- Wrong processing order (body must be first)
- Missing YAML files for registered videos
- Triggering pipeline before user confirmation

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
