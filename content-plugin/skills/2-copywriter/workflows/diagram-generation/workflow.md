---
name: diagram-generation
description: Generate treasure-map-style visual diagrams from video scripts — pan+zoom HTML canvas with concept nodes, code panels, real screenshots, and connected paths
createWorkflow: './steps-c/step-01-init.md'
editWorkflow: './steps-e/step-01-assess.md'
---

# Diagram Generation Workflow

**Goal:** Parse a video script into a treasure-map-style visual diagram — a pan+zoom HTML canvas with concept nodes, code panels, pinned screenshots, prompt bubbles, and connected paths. The output is a self-contained HTML file opened in any browser.

**Your Role:** You are a visual explainer who transforms dense video scripts into navigable concept maps. Think engineering notebook crossed with treasure map — cream paper, dotted grid, paths that weave across the canvas. The diagram should make the content visually compelling to look at while explaining it on camera.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file. Load only the current step.
- **Just-In-Time Loading**: Never load future step files until directed.
- **Sequential Enforcement**: Execute all numbered sections in order, no skipping.
- **State Tracking**: Write the diagram plan to `diagram-plan-{slug}.md` after step 2 and update it through the workflow.
- **Append-Only Building**: Build the HTML file in step 4 as a complete write — not incremental.
- **Bi-Modal Structure**: Separate step folders for Create (steps-c/) and Edit (steps-e/).

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: Only proceed when user selects Continue (collab mode) or automatically (auto mode)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** write/update the diagram plan file at the end of each step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **COLLAB MODE:** halt at checkpoints and wait for user input
- 🚀 **AUTO MODE:** make best-case assumptions, auto-approve all checkpoints, notify user only when complete
- 📋 **NEVER** create mental todo lists from future steps

---

## INITIALIZATION SEQUENCE

### 1. Load Module Configuration

Load and read `{project-root}/config.yaml`. Resolve:
- `user_name`, `communication_language`
- `content_output_folder` (e.g., `content/projects/`)
- `standalone_folder`
- `output_folder`

Also load the active project from `{project-root}/content-plugin/data/active-project.yaml`.

### 2. Mode Selection

Present:

> **Diagram Generation. How would you like to proceed?**
>
> **[C]reate** — Generate a new diagram from a script
> **[E]dit** — Edit an existing diagram
>
> Select: [C]reate / [E]dit

Wait for user selection.

### 3. Execution Mode (Create only)

If Create was selected:

> **How would you like to run this workflow?**
>
> **[A] Auto** — I'll discover the script, plan the diagram, match screenshots, and compose the full HTML end-to-end. Only notified when complete.
> **[C] Collab** — I'll work through each step with you, presenting the map plan for approval before building.

Set `{execution_mode}` to `auto` or `collab`.

If auto: "Running in auto mode. I'll generate the full diagram and notify you when it's ready."

### 4. Route to First Step

- **IF C (Create):** Load, read completely, then execute `steps-c/step-01-init.md`
- **IF E (Edit):** Ask for diagram file path, then load, read completely, then execute `steps-e/step-01-assess.md`
- **IF Other:** Help user respond, redisplay mode selection
