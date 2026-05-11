---
name: video-ingest
description: Watch folder for new raw video, register and kick off analysis pipeline
web_bundle: true
---

# Video Ingest

**Goal:** Detect new raw video files in the ingest folder, register metadata and proxy-raw mappings, and trigger the Audio Analysis pipeline after user confirmation.

**Your Role:** In addition to your name, communication_style, and persona, you are also a video pipeline operator and file system analyst. You bring expertise in video file detection, metadata extraction, and pipeline orchestration, while the user brings their video project context and confirmation to proceed.

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere too 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **Append-Only Building**: Build documents by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- `project_folder`, `content_output_folder`

### 2. Resolve Active Project and Ingest Path

Load the wiki session log from `{plugin-root}/video-plugin/wiki/index.md` and read the most recent session row to determine `last_active_project`.

**If `last_active_project` exists:**
- Set `{active_project}` to the slug value
- Set `{project_path}` to `{content_output_folder}/projects/{active_project}/`
- Set `{video_ingest_path}` to `{project_path}/video-ingest/`
- Confirm with user: "**Active project: "{active_project}". Scanning `{video_ingest_path}` for new video files. Continue?**"

**If `last_active_project` is empty or missing:**
- Check `{content_output_folder}/projects/_index.yaml` for available projects
- If projects exist: ask user to select one
- If no projects exist: ask if they want to work standalone
- **Standalone mode:** set `{video_ingest_path}` to `{content_output_folder}/standalone/{date}-{description}/video-ingest/`

### 3. First Step EXECUTION

Once the active project is confirmed and `{video_ingest_path}` is resolved, load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
