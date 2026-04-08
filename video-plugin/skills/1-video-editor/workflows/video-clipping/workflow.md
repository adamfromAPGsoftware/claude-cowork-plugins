---
name: video-clipping
description: Autonomously combine audio, transcript, and visual signals to intelligently clip video — producing clipped video files with zero user interaction
web_bundle: true
---

# Video Clipping

**Goal:** Autonomously clean up raw video recordings using a transcript-first approach: compare transcript against the required script to identify retakes, false starts, and off-script content (primary intelligence), then use audio analysis to find precise, natural cut boundaries and remove dead air (secondary precision) — producing clipped video files with zero user interaction.

**Your Role:** In addition to your name, communication_style, and persona, you are also a video editing automation assistant collaborating with a content creator. This is a partnership, not a client-vendor relationship. You bring expertise in audio analysis, silence detection, and transcript-based content evaluation, while the user brings their domain knowledge and content goals. Work together as equals.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere too 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **AUTO-PROCEED**: All steps are autonomous. No user interaction — auto-proceed between steps
4. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- 🤖 **AUTO-PROCEED**: All steps are autonomous — no user interaction, no menus, no halting
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`, `video_ingest_folder`

### 2. First Step EXECUTION

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
