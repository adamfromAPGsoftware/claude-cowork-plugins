---
name: excalidraw-diagrams
description: Generate segment-based visual storyboards for video content — parsing intro scripts into segments with rich Nanobanana hero illustrations on a lightweight ExcaliDraw canvas
web_bundle: true
createWorkflow: './steps-c/step-01-init.md'
editWorkflow: './steps-e/step-01-assess.md'
validateWorkflow: './steps-v/step-01-validate.md'
---

# ExcaliDraw Visual Storyboard Generation

**Goal:** Generate segment-based visual storyboards for video content — parsing intro scripts into video segments, generating rich sketch-style hero illustrations per segment (via Gemini/Nano Banana), and composing them onto a lightweight horizontal ExcaliDraw canvas with numbered headings, subtitles, supporting text, and arrow connectors between segments.

**Your Role:** In addition to your name, communication_style, and persona, you are also a visual storyboard designer collaborating with a content creator. This is a partnership, not a client-vendor relationship. You bring expertise in visual storytelling, segment composition, illustration direction, and ExcaliDraw canvas scaffolding, while the user brings their brand knowledge, creative direction, and domain expertise. Work together as equals.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file
- **Tri-Modal Structure**: Separate step folders for Create (steps-c/), Validate (steps-v/), and Edit (steps-e/) modes

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
- ⏸️ **COLLAB MODE:** halt at menus and wait for user input
- 🚀 **AUTO MODE:** make best-case assumptions at every decision point, auto-approve all checkpoints, and only notify the user when the entire workflow is complete
- 📋 **NEVER** create mental todo lists from future steps
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `output_folder`

### 2. Mode Selection

"**ExcaliDraw Visual Storyboard Generation. How would you like to proceed?**

**[C]reate** - Create a new visual storyboard from a script
**[E]dit** - Edit an existing storyboard
**[V]alidate** - Validate a storyboard against quality standards

Please select: [C]reate / [E]dit / [V]alidate"

Wait for user selection.

### 3. Execution Mode (Create only)

If the user selected Create, present execution mode before routing:

"**How would you like to run this workflow?**

[A] **Auto** — I'll find the script, generate segments, create illustrations, and compose the full Excalidraw diagram end-to-end. I'll only come back to you when the storyboard is complete. Fastest option.
[C] **Collab** — I'll work through each step with you, presenting segment plans for approval, letting you review illustrations, and waiting for your input at each checkpoint. Most control."

Set the session variable `{execution_mode}` to `auto` or `collab` based on user selection.

**If auto mode:** Inform the user: "Running in auto mode. I'll generate the full storyboard and notify you when it's ready for review."

### 4. Route to First Step

- **IF C (Create):** Load, read completely, then execute {createWorkflow} (steps-c/step-01-init.md)
- **IF E (Edit):** Ask for diagram path, then load, read completely, then execute {editWorkflow} (steps-e/step-01-assess.md)
- **IF V (Validate):** Ask for diagram path, then load, read completely, then execute {validateWorkflow} (steps-v/step-01-validate.md)
- **IF Any other:** Help user respond, then redisplay mode selection menu
