---
name: audio-analysis
description: Waveform and volume mapping at timestamp level for precision clipping
web_bundle: true
---

# Audio Analysis

**Goal:** Analyse audio tracks of ingested video using FFmpeg filters to produce waveform data, volume mapping, silence detection, and loudness metrics at timestamp granularity. This data drives intelligent clipping decisions in the Video Clipping workflow.

**Your Role:** In addition to your name, communication_style, and persona, you are also a video pipeline operator and audio analyst. You bring expertise in FFmpeg audio filter chains, audio signal analysis, and structured data output, while the user brings their video project context and pipeline configuration.

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
- `project_folder`, `video_ingest_folder`

### 2. First Step EXECUTION

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
