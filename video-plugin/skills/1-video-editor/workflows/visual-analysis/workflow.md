---
name: visual-analysis
description: Gemini Pro screen analysis at timestamp level for visual understanding and B-roll extraction
web_bundle: true
---

# Visual Analysis

**Goal:** Analyse video frames using Gemini Pro to understand what's happening visually at each timestamp — identifying scene types, tools being used, user activity, and B-roll extraction opportunities.

**Your Role:** In addition to your name, communication_style, and persona, you are also a video analysis pipeline operator executing a prescriptive visual analysis workflow. You bring technical precision in video processing and visual classification, while the user brings their video content and analysis preferences. This is an automated pipeline with minimal interaction after initial configuration.

**Meta-Context:** This workflow is part of the CCS video pipeline. It receives video files from Video Ingest and produces structured JSON analysis data that downstream workflows (B-roll extraction, clip generation) consume. Accuracy and completeness of visual analysis directly impacts downstream content quality.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere to 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`, `video_ingest_folder`
- `env_file` (for OPENROUTER_API_KEY)

### 2. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
