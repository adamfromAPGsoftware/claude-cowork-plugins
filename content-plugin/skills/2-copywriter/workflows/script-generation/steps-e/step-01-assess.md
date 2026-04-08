---
name: 'step-01-assess'
description: 'Load existing script document, assess current state, and determine what to edit'

nextStepFile: './step-02-edit.md'
scriptStandards: '../data/script-standards.md'
---

# Step 1: Assess Script

## STEP GOAL:

To load an existing video script document, assess its current state and completeness, and determine which sections the user wants to edit.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Copywriter reviewing an existing script for edits
- ✅ The user knows what they want to change — help them navigate

### Step-Specific Rules:

- 🎯 Focus only on loading and assessing the document
- 🚫 FORBIDDEN to make any edits in this step
- 💬 Present the current state clearly so the user can decide what to edit

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 📖 Load and analyze the existing script document
- 🚫 FORBIDDEN to modify any content in this step

## CONTEXT BOUNDARIES:

- Available: User-provided path to existing script document
- Focus: Assessment only
- Limits: No editing
- Dependencies: Script document must exist

## MANDATORY SEQUENCE

### 1. Load Script Document

**Search scope depends on the active mode (already resolved during agent startup):**

- **If in project mode:** Search ONLY within `{project_path}/copywriter/scripts/` for existing script files (`script-*.md`). Do NOT search other projects.
- **If in standalone mode:** Search `{standalone_folder}/*/` for script files (`script-*.md`).

**If exactly 1 script found:** Auto-select it and proceed.

**If multiple scripts found:**

"**Found these scripts:**

[1] {filename} — {concept title from frontmatter} ({date})
[2] {filename} — {concept title from frontmatter} ({date})
...

**Which script would you like to edit?** Enter the number, or provide a path to a different script."

**If no scripts found:**

"**No scripts found** in the active project. You can provide a path to a script file, or run the Create workflow first.

**Path or action:**"

Wait for user selection (unless auto-selected). Load the document and read all sections.

### 2. Assess Current State

Load {scriptStandards} and check completeness:

"**Script Assessment:**

**Document:** [filename]
**Concept:** [concept title from frontmatter]
**Status:** [complete/incomplete from frontmatter]
**Last Step:** [lastStep from frontmatter]

**Sections:**
1. Script Overview — [present/missing/incomplete]
2. Direction & Angle — [present/missing/incomplete]
3. Scripted Intro — [present/missing/incomplete]
4. Body Segments — [present/missing/incomplete] ([N] segments)
5. CTA / Outro — [present/missing/incomplete]
6. YouTube Metadata — [present/missing/incomplete]
7. Thumbnail Concepts — [present/missing/incomplete]
8. B-Roll Suggestions — [present/missing/incomplete]
9. Teleprompter Section — [present/missing/incomplete]

---

**What would you like to edit?** You can:
- Name specific sections (e.g., 'intro', 'titles', 'body segment 2')
- Describe the change (e.g., 'make the intro shorter', 'add a talking point about X')
- Request a full refresh of a section"

Wait for user input.

### 3. Confirm Edit Scope

Summarize what the user wants to edit:

"**Planned edits:**
- [Edit 1 description]
- [Edit 2 description]

**Ready to proceed with these edits?**"

### 4. Present MENU OPTIONS

Display: **Select:** [C] Continue to Edit

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user, then redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:
- Document loaded and assessed
- User has identified what to edit
- Edit scope confirmed

### ❌ SYSTEM FAILURE:
- Making edits in the assessment step
- Not presenting current state before asking what to edit

**Master Rule:** Skipping steps is FORBIDDEN.
