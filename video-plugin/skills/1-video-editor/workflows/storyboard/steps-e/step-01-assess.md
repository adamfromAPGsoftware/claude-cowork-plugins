---
name: 'step-01-assess'
description: 'Load existing storyboard, assess state, determine edit scope'

nextStepFile: './step-02-edit.md'
---

# Step 1: Assess Existing Storyboard

## STEP GOAL:

Load an existing storyboard document, assess its current state (completeness, approval status, pacing compliance), and determine the scope of edits needed.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR assessing an existing document
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Focus ONLY on assessment — do NOT apply any edits in this step
- Report what exists and what's missing
- Determine if storyboard is APPROVED, DRAFT, or incomplete

## EXECUTION PROTOCOLS:

- 🎯 Load existing storyboard, assess completeness and approval status, capture edit goals
- 💾 No output file written in this step — assessment only
- 🚫 Do NOT apply any edits in this step

## CONTEXT BOUNDARIES:

- Available context: Existing storyboard document in project folder
- Focus: State assessment only — report what exists and what is missing
- Limits: Do NOT edit the storyboard in this step
- Dependencies: An existing storyboard document must exist before assessment

## MANDATORY SEQUENCE

### 1. Load Storyboard

Ask user for the storyboard path if not provided:
- Search: `{project_folder}/{project-slug}/video-editor/storyboard/*-storyboard.md`

Read the complete storyboard document.

### 2. Assess State

Check frontmatter:
- `status`: APPROVED / DRAFT / missing
- `stepsCompleted`: Which steps have been completed
- `scope`: intro-only / full-video

Check document sections:
- Production Brief: present/missing
- Speaker Position Map: present/missing
- Visual Asset Source Map: present/missing
- Text Placement Strategy: present/missing
- Master Timeline: present/missing
- Pacing Validation Report: present/missing

### 3. Present Assessment

"**Storyboard Assessment — {video-id}**

**Status:** {status}
**Scope:** {scope}
**Steps Completed:** {steps_list}

**Section Status:**

| Section | Status | Notes |
|---------|--------|-------|
| Production Brief | {present/missing} | {notes} |
| Speaker Position Map | {present/missing} | {notes} |
| Visual Asset Source Map | {present/missing} | {notes} |
| Text Placement Strategy | {present/missing} | {notes} |
| Master Timeline | {present/missing} | {segments count} |
| Pacing Validation | {present/missing} | {pass/fail status} |

**What would you like to edit?**

[C] Continue** — Describe your edit goals and proceed"

#### Menu Handling Logic:
- IF C: Capture user's edit goals, then load, read entire file, then execute {nextStepFile}
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed when user selects 'C' and describes their edit goals

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Storyboard loaded and fully assessed
- All sections checked for presence/completeness
- Clear status report presented to user
- Edit goals captured before proceeding

### FAILURE:

- Making edits in this assessment step
- Not checking all sections
- Not reporting storyboard status
