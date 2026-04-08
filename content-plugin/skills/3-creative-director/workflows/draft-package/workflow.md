---
name: draft-package
description: Draft a reviewable thumbnail/title package plan with keyword research, CTR pre-validation, and YouTube description
web_bundle: true
---

# Draft Package

**Goal:** Plan and draft a complete title/thumbnail package before spending API credits on generation. Produces a `package-plan.md` file that the Visual Asset Creation thumbnail step consumes in plan-mode — titles, prompts, compositions, CTR pre-scores, YouTube description, and generation config, all reviewable and editable before generation.

**Your Role:** In addition to your name, communication_style, and persona, you are also a thumbnail strategist and title copywriter collaborating with a content creator. You combine CTR psychology, keyword data, and visual composition expertise to draft the strongest possible title/thumbnail combinations. This is the planning phase — no API credits are spent here.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file
6. **CHECK MODE**: If `{workflow_mode}` is `auto`, execute AUTO MODE blocks instead of halting at user input gates

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input — **UNLESS `{workflow_mode}` is `auto`**, in which case skip all menus and user input gates; use autonomous decision criteria defined in each step's AUTO MODE sections
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `content_output_folder`, `project_folder`, `standalone_folder`, `env_file`, `reference_photos_folder`

### 1b. Mode Detection

Detect the workflow mode from the user's invocation:

- `DP auto` → set `{workflow_mode}` = `auto`
- `DP` or `DP collab` → set `{workflow_mode}` = `collab`
- Ambiguous → ask once: "**Run in auto mode (full autonomous pipeline) or collab mode (interactive)?** [auto / collab]"

Store `{workflow_mode}` as a session variable. In **auto** mode, all menus and user input gates are skipped — the agent uses autonomous decision criteria defined in each step's AUTO MODE sections. In **collab** mode, behavior is unchanged from the standard interactive workflow.

### 2. First Step Execution

Load, read the full file and then execute `./steps-c/step-01-init.md` to begin the workflow.
