---
name: storyboard
description: Plan video production — segments, B-roll, motion graphics, captions, pacing
web_bundle: true
createWorkflow: './steps-c/step-01-init.md'
editWorkflow: './steps-e/step-01-assess.md'
validateWorkflow: './steps-v/step-01-validate.md'
---

# Storyboard

**Goal:** Build a complete video production storyboard that plans every visual segment, B-roll placement, motion graphic brief, caption strategy, and pacing target — producing the single source of truth that the Remotion Edit workflow consumes to compile the final video.

**Your Role:** In addition to your name, communication_style, and persona, you are also a video production planner collaborating with a content creator. This is a partnership, not a client-vendor relationship. You bring expertise in visual pacing, segment design, B-roll strategy, and Remotion template selection, while the user brings their creative vision, brand knowledge, and content goals. Work together as equals.

**Meta-Context:** This workflow sits between the analysis/clipping pipeline (upstream) and the Remotion Edit workflow (downstream). It consumes transcripts, audio analysis, visual analysis, clip plans, and scripts. It produces a storyboard document that the Remotion Edit workflow's preflight step validates and compiles.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere to 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array
- **Append-Only Building**: Build the storyboard document by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps
- **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `output_folder`

### 1b. Long-Form Reference Data Loading

When processing long-form content (detected from project config or user input):
- Load `../long-form-edit/data/inspiration/long-form-patterns.md` — synthesized production patterns (MG types A-G, pacing rules, PiP strategies, transition rules)
- Load `../long-form-edit/data/long-form-pacing-rules.md` — P1-P16 pacing enforcement rules
- Load `../long-form-edit/data/inspiration-compliance-checklist.md` — non-pacing inspiration gates
- Load `../remotion-edit/data/caption-style-spec.md` — caption style (long-form mode: phrase-level reveals, PiP-aware positioning)

This data informs:
- Step 02 (Production Brief): MG trigger rules, visual asset type selection
- Step 05 (Timeline Assembly): Intro visual pacing, PiP decision rules, MG placement at narration triggers
- Step 06 (Pacing Validation): Long-form body target (4-8 events/min vs 7-10 short-form)

### 2. Mode Selection

"**Storyboard Workflow. How would you like to proceed?**

**[C]reate** — Build a new video production storyboard
**[E]dit** — Edit an existing storyboard
**[V]alidate** — Validate a storyboard against production standards

Please select: [C]reate / [E]dit / [V]alidate"

Wait for user selection.

### 3. Route to First Step

- **IF C:** Load, read completely, then execute {createWorkflow} (steps-c/step-01-init.md)
- **IF E:** Ask for storyboard path, then load, read completely, then execute {editWorkflow} (steps-e/step-01-assess.md)
- **IF V:** Ask for storyboard path, then load, read completely, then execute {validateWorkflow} (steps-v/step-01-validate.md)
- **IF Any other:** Help user respond, then redisplay mode selection menu
