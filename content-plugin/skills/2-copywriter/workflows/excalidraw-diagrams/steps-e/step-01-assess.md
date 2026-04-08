---
name: 'step-01-assess'
description: 'Load existing diagram and assess what needs editing'

nextStepFile: './step-02-edit.md'
diagramStandards: '../data/diagram-standards.md'
excalidrawFormatReference: '../data/excalidraw-format-reference.md'
---

# Step 1: Assess Existing Diagram

## STEP GOAL:

To load an existing `.excalidraw` diagram and its metadata, assess the current state, and determine what edits the user wants to make.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER make edits without user direction
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR assessing the current state
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual communication designer assessing an existing diagram
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue — understand before changing
- ✅ You bring layout analysis expertise, user brings their edit requirements

### Step-Specific Rules:

- 🎯 Focus on understanding the current diagram and gathering edit requirements
- 🚫 FORBIDDEN to make any edits in this step — that's step 2
- 💬 Approach: Present what exists, ask what should change

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Document the edit requirements for step 2
- 📖 Load diagram standards and format reference
- 🚫 This is the assessment step — understand first, edit later

## CONTEXT BOUNDARIES:

- Available: User-provided path to existing diagram
- Focus: Understanding current state and gathering requirements
- Limits: Do not make any changes yet
- Dependencies: User must provide path to existing `.excalidraw` file

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Existing Diagram

"**Please provide the path to the diagram you want to edit.**"

Load the `.excalidraw` file and its companion metadata plan (if it exists).

### 2. Analyse Current State

Parse the ExcaliDraw JSON and present a summary:

"**Current Diagram:**

| Element Type | Count |
|-------------|-------|
| Containers | {count} |
| Images | {count} |
| Text labels | {count} |
| Arrows | {count} |
| **Total** | {count} |

**Canvas:** {width} x {height}
**Layout:** {describe the visual structure}
**Concepts represented:** {list key concepts from text labels}

**Metadata plan:** {found/not found}"

### 3. Gather Edit Requirements

"**What would you like to change?**

Common edit types:
- **[I]mages** — Swap, regenerate, add, or remove images
- **[T]ext** — Update labels, headers, descriptions
- **[L]ayout** — Rearrange elements, change spacing, resize panels
- **[A]rrows** — Add, remove, or reroute connections
- **[C]olour** — Change colour coding
- **[E]lements** — Add or remove concept elements

**Describe the changes you want, or select a category.**"

Wait for user input. Gather specific edit requirements.

### 4. Confirm Edit Plan

"**Edit plan:**
1. {Edit 1 description}
2. {Edit 2 description}
3. ...

**Ready to apply these changes?**"

### 5. Present MENU OPTIONS

Display: "**Select:** [C] Continue to Edit"

#### Menu Handling Logic:

- IF C: Save edit requirements, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user refine requirements, then [Redisplay Menu Options](#5-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Existing diagram loaded and parsed
- Current state clearly presented to user
- Edit requirements gathered and confirmed
- No edits made in this step

### ❌ SYSTEM FAILURE:

- Making edits before step 2
- Not presenting current state
- Proceeding without clear edit requirements

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
