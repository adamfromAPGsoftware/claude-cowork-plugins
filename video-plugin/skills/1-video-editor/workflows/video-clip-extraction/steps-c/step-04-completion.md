---
name: 'step-04-completion'
description: 'Present extraction summary and confirm all files saved correctly'
---

# Step 4: Completion

## STEP GOAL:

To present a final summary of all extracted clips with their file paths and confirm the workflow completed successfully.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a systematic video extraction technician
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Present results clearly and concisely

### Step-Specific Rules:

- 🎯 Focus only on summarising results and confirming completion
- 🚫 FORBIDDEN to extract additional clips in this step
- 💬 Approach: Clear, concise summary of what was produced

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Present final summary
- 📖 Mark workflow as complete

## CONTEXT BOUNDARIES:

- Available context: All extraction results from Step 3
- Focus: Summary and confirmation
- Limits: No further extraction — this is the final step
- Dependencies: Requires completed Step 3

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Present Extraction Summary

"**Video Clip Extraction Complete**

---

**Source Video:** {video file path}

**Extracted Clips:**

| # | Type | Timestamp | Output File | Status |
|---|------|-----------|-------------|--------|
| 1 | {type} | {start} → {end} | {output filename} | ✅ |
| ... | ... | ... | ... | ... |

---

**Summary:**
- **B-Roll clips:** {count} extracted
- **Speed-Up clips:** {count} extracted
- **LinkedIn clips:** {count} extracted
- **Total:** {total count} clips

**Output Location:** {output path}"

### 2. Confirm Completion

"**All clips have been extracted and saved. Workflow complete.**

Is there anything else you need?"

### 3. End Workflow

This is the final step. No next step to load. Workflow is complete.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete summary presented with all clips listed
- File paths confirmed
- Counts accurate
- Workflow marked as complete

### ❌ SYSTEM FAILURE:

- Missing clips from summary
- Incorrect file paths or counts
- Attempting further extraction after completion

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
