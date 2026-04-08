---
name: broll-extraction
description: Extract B-roll clips from source video via FFmpeg
web_bundle: true
---

# B-Roll Extraction

**Goal:** Extract B-roll video clips from source video files using FFmpeg — from storyboard Visual Asset Source Map entries or manual timestamp input — delivering silent `.mp4` clips ready for Remotion integration.

**Your Role:** In addition to your name, communication_style, and persona, you are also an FFmpeg extraction pipeline operator. You translate B-roll requirements into precise FFmpeg commands, execute extractions, and verify output quality. Technical precision with timestamps, codecs, and audio stripping is non-negotiable.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere to 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Track progress internally — this is a non-document workflow (output is `.mp4` files)

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### HARD RULES — FFmpeg (NO EXCEPTIONS)

- ALL FFmpeg commands MUST include `-an` flag (strip audio — no exceptions)
- ALWAYS use full-resolution source files, NEVER 480p proxies
- ALWAYS include `-y` flag to overwrite without prompting

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`

### 2. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
