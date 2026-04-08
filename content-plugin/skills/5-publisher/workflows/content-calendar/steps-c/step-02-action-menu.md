---
name: 'step-02-action-menu'
description: 'Present action selection menu and route to the selected operation'

viewStepFile: './step-03-view.md'
duplicateCheckStepFile: './step-04-duplicate-check.md'
updateStepFile: './step-05-update.md'
---

# Step 2: Action Menu

## STEP GOAL:

Present the content calendar action menu and route the user to the selected operation: View/Query, Duplicate Check, Update Entry, or Exit.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a calendar operations manager — precise, systematic
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Present clear, unambiguous menu options

### Step-Specific Rules:

- 🎯 Focus ONLY on presenting the menu and routing
- 🚫 FORBIDDEN to execute any calendar operations in this step
- 💬 Display the menu clearly and wait for selection
- 🚫 FORBIDDEN to proceed without a valid selection

## EXECUTION PROTOCOLS:

- 🎯 Present action menu
- 💾 Route to correct step file based on selection
- 📖 This step is the hub — all action steps loop back here
- 🚫 FORBIDDEN to auto-select an action

## CONTEXT BOUNDARIES:

- Calendar has been loaded in step-01
- Calendar data is in memory from the init step
- This step only routes — does not process
- All action steps (03, 04, 05) return to this step after completion

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Present Action Menu

"**Content Calendar — Select an Action:**

**[V]** View/Query — display calendar entries with optional filters
**[D]** Duplicate Check — scan for overlapping or duplicate content
**[U]** Update Entry — add, modify, or remove calendar entries
**[X]** Exit — close the content calendar workflow

**Select:** [V] View | [D] Duplicate Check | [U] Update | [X] Exit"

### 2. Route to Selected Action

#### Menu Handling Logic:

- IF V: Load, read entire file, then execute {viewStepFile}
- IF D: Load, read entire file, then execute {duplicateCheckStepFile}
- IF U: Load, read entire file, then execute {updateStepFile}
- IF X: "**Content calendar closed. Returning to agent menu.**" — End workflow
- IF Any other: "**Not recognised.** Please select V, D, U, or X." — Redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- Branching options load different steps based on user choice
- After each action step completes, it will reload this step for the next action

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Menu displayed clearly with all 4 options
- User selection routed to correct step file
- Invalid selections handled gracefully
- Exit option ends workflow cleanly

### ❌ SYSTEM FAILURE:

- Auto-selecting an action without user input
- Routing to wrong step file
- Not handling invalid selections
- Not waiting for user input

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
