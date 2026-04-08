---
name: 'step-01-init'
description: 'Initialize storyboard generation — auto-resolve script and output, set up directory'

nextStepFile: './step-02-concept.md'
diagramStandards: '../data/diagram-standards.md'
moduleInputFolder: '{content_output_folder}'
inputFilePatterns:
  - '*-script.md'
  - '*script*.md'
---

# Step 1: Initialization

## STEP GOAL:

To discover the source script and set up the output directory for storyboard generation. When in project mode, auto-resolve without prompting the user.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual storyboard designer specialising in segment composition, illustration direction, and ExcaliDraw canvas scaffolding
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role

### Step-Specific Rules:

- 🎯 Focus only on initialization — script discovery and output setup
- 🚫 FORBIDDEN to start parsing segments or planning layout — that's step 2
- 🚀 In project mode with scripts available, auto-resolve everything — no user prompts needed

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Script Discovery (Auto-Resolve)

**Search for script files in priority order:**

1. **If active project is set:** Search `{project_folder}/{active_project}/copywriter/scripts/` for files matching `{inputFilePatterns}`
2. **Fallback:** Search `{moduleInputFolder}` and subfolders for files matching `{inputFilePatterns}`

**If exactly 1 script found:**
- Auto-select it. No prompt needed.

**If multiple scripts found:**
- Present a numbered list and ask the user to select one.

**If no scripts found:**
- Ask the user to provide a path to their script.

### 2. Resolve Output Directory

**IF active project is set (`{active_project}` is not null):**
- Output path: `{project_folder}/{active_project}/copywriter/diagrams/`

**IF standalone mode (`{active_project}` is null):**
- Output path: `{standalone_folder}/{date}-{storyboard-name}/diagrams/`

Create the directory structure if it doesn't exist:
```
{output_path}/
├── storyboard-{name}.excalidraw
├── images/
└── storyboard-plan-{name}.md
```

### 3. Load Diagram Standards

Load `{diagramStandards}` to have the visual style reference available for subsequent steps.

### 4. Confirm and Proceed

Briefly confirm setup:

"**Setup complete:**
- **Source:** {script name}
- **Output:** {output path}

**Proceeding to segment planning...**"

**Auto mode:** Auto-proceed to {nextStepFile} immediately — no menu.

**Collab mode:** Display: "**Select:** [C] Continue to Segment Planning"
- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user, then redisplay menu

## CRITICAL STEP COMPLETION NOTE

In auto mode, proceed directly to {nextStepFile} after confirming setup. In collab mode, wait for user to select 'C'.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Script discovered and loaded (auto-selected if only one exists)
- Output directory structure created
- Diagram standards loaded for reference
- Auto mode: proceeded without unnecessary prompts
- Collab mode: user confirmed setup before proceeding

### ❌ SYSTEM FAILURE:

- Starting segment parsing or layout planning in this step
- Hardcoding paths instead of using variables
- Proceeding without script source
- Not creating output directory structure
- Prompting user unnecessarily when auto-resolve is possible (single script in project mode)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
