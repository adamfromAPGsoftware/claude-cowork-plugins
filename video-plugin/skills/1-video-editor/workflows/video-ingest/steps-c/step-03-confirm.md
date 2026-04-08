---
name: 'step-03-confirm'
description: 'Present detection and registration results to user for confirmation before triggering pipeline'

nextStepFile: './step-04-trigger.md'
---

# Step 3: Confirm Before Pipeline Trigger

## STEP GOAL:

To present the complete detection and registration results to the user — files detected, proxy-raw mappings, project groupings, and processing order — and obtain explicit confirmation before triggering the Audio Analysis pipeline.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed without explicit user confirmation
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator presenting results for review
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Present data clearly so the user can make an informed decision

### Step-Specific Rules:

- 🎯 Focus ONLY on presenting results and obtaining confirmation
- 🚫 FORBIDDEN to trigger any pipeline in this step
- 🚫 FORBIDDEN to modify any YAML files or mappings without user request
- 💬 Allow user to request adjustments before confirming

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Apply any user-requested adjustments to YAML files
- 📖 User must explicitly select 'C' to proceed to pipeline trigger
- 🚫 FORBIDDEN to auto-proceed — this is the confirmation gate

## CONTEXT BOUNDARIES:

- Available context: Registration results from step 2 (files, mappings, groupings, YAML files)
- Focus: User review and confirmation only
- Limits: Do NOT trigger pipeline or modify data unless user requests changes
- Dependencies: Step 2 must have completed with all registrations

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Present Summary for Review

"**Ready for your review before triggering the pipeline.**

---

**Ingest Summary:**
- **Total files detected:** {count}
- **Proxy-raw pairs:** {pair-count}
- **Projects:** {project-count}

---

**Processing Order:**

{For each project group, list in processing order:}

**Project: {project-name}**

| Order | File | Role | Type | Duration | Resolution | Paired With |
|-------|------|------|------|----------|------------|-------------|
| 1 | {filename} | Raw | Body | {duration} | {resolution} | {proxy-file} |
| 2 | {filename} | Raw | Intro | {duration} | {resolution} | — |

{Repeat for each project}

---

**Unmatched files:** {list or 'None'}
**YAML files created:** {count}

---"

### 2. Ask for Confirmation or Adjustments

"**Please review the above. You can:**

- **Adjust** — Request changes to mappings, groupings, or processing order
- **Confirm** — Approve and proceed to trigger the Audio Analysis pipeline

**Any adjustments needed, or ready to proceed?**"

**If user requests adjustments:**
1. Apply the requested changes to the relevant YAML files
2. Re-display the updated summary
3. Ask for confirmation again

**If user confirms or has no adjustments:**
Proceed to menu.

### 3. Present MENU OPTIONS

Display: **Select:** [C] Confirm and Trigger Pipeline

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: Apply adjustments if requested, re-display summary, then [Redisplay Menu Options](#3-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- User can request adjustments — apply them and redisplay menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user has explicitly confirmed by selecting 'C' will you load and read fully `{nextStepFile}` to execute the pipeline trigger.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete summary presented with all files, mappings, groupings, and processing order
- User had opportunity to review and request adjustments
- Any adjustments applied and re-confirmed
- User explicitly confirmed before proceeding
- Proceeded to pipeline trigger step

### ❌ SYSTEM FAILURE:

- Auto-proceeding without user confirmation
- Not presenting complete summary
- Ignoring user adjustment requests
- Triggering pipeline in this step
- Proceeding without explicit 'C' selection

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
