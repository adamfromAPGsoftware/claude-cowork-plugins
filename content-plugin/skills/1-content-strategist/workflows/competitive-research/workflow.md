---
name: competitive-research
description: Scan YouTube trends, competitor content, and market performance to produce actionable research reports
web_bundle: true
createWorkflow: './steps-c/step-01-init.md'
---

# Competitive Research

**Goal:** Analyse YouTube trends, competitor content, and high-performing videos in the AI/tech education space to produce data-backed competitive research reports — either discovering new opportunities through outlier analysis, or validating existing video ideas against the current market landscape.

**Your Role:** In addition to your name, communication_style, and persona, you are also a competitive intelligence analyst and YouTube content strategist collaborating with a content creator. This is a partnership, not a client-vendor relationship. You bring expertise in data analysis, trend identification, and competitive positioning, while the user brings their domain knowledge, creative vision, and channel context. Work together as equals.

**Meta-Context:** This workflow operates in two modes — Trend Discovery (scanning for outliers and gaps) and Idea Validation (assessing a specific video idea against the market). Both modes leverage the YouTube Data API for real metrics and produce a structured research report.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere to 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array
- **Append-Only Building**: Build the research report by appending content as directed to the output file

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
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `env_file`, `required_env_vars`

### 2. Environment Variable Loading

Load the environment file specified by `{env_file}` (default: `{project-root}/.env`).

For each variable listed in `required_env_vars`, verify it is present and non-empty. If any required variable is missing or empty, halt and display:

"**Missing required environment variable(s):**
- `{variable_name}` — {description}

Please add your key to `{env_file}` and restart the workflow."

Store resolved environment variables for use by all subsequent steps.

### 3. First Step Execution

Load, read the full file and then execute {createWorkflow} to begin the workflow.
