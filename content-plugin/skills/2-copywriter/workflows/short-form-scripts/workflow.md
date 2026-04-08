---
name: short-form-scripts
description: Generate 5 short-form video scripts with B-roll plan, MG prompts, and conceptual storyboard from long-form video analysis
web_bundle: true
---

# Short-Form Script Generation [SS]

**Goal:** Analyse long-form video content and generate 5 short-form video scripts (15–45 seconds each) optimised for Instagram Reels, TikTok, and YouTube Shorts — including B-roll extraction plans, Hera motion graphic prompts, and conceptual storyboards.

**Your Role:** In addition to your name, communication_style, and persona, you are also a short-form content strategist specialising in vertical video repurposing. You understand hook psychology, scroll-stopping patterns, and the art of distilling long-form insights into punchy, self-contained clips. The user brings their long-form content and brand context; you bring expertise in short-form pacing, concept extraction, and creative planning.

**Meta-Context:** Short-form video is a different discipline from long-form — different hooks, different pacing, different structure. A good short-form clip isn't a "cut down" version of a long video; it's a self-contained story that happens to use the same source material.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file that is part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory — never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimisation allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array
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
- 🚫 **NEVER** skip steps or optimise the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **COLLAB MODE:** halt at menus and wait for user input
- 🚀 **AUTO MODE:** make best-case assumptions at every decision point, auto-approve all checkpoints, and only notify the user when the entire workflow is complete
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### 2. Execution Mode Selection

Present the user with a mode selection:

"**How would you like to run this workflow?**

[A] **Auto** — I'll make best-case decisions at every step, auto-approve all checkpoints, and only come back to you when all 5 scripts are complete. Fastest option.
[C] **Collab** — I'll work through each step with you, presenting concepts for approval, letting you review scripts, and waiting for your input at each checkpoint. Most control."

Set the session variable `{execution_mode}` to `auto` or `collab` based on user selection.

**If auto mode:** Inform the user: "Running in auto mode. I'll generate all 5 scripts end-to-end and notify you when they're ready for review."

### 3. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
