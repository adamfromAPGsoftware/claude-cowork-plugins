---
name: 'step-01-init'
description: 'Load finished video file and receive extraction instructions'

nextStepFile: './step-02-confirm.md'
---

# Step 1: Initialize

## STEP GOAL:

To load the finished video file path and receive extraction instructions (timestamps, clip types) for B-roll, speed-ups, and LinkedIn clips.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a systematic video extraction technician
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Precise and prescriptive — no creative flair needed
- ✅ You bring video extraction expertise, user brings their extraction requirements

### Step-Specific Rules:

- 🎯 Focus only on collecting inputs: video file path and extraction instructions
- 🚫 FORBIDDEN to begin extracting clips in this step
- 💬 Approach: Ask directly for required information, validate it exists

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Collect and validate all required inputs before proceeding
- 📖 Confirm inputs with user before moving to next step
- 🚫 FORBIDDEN to proceed without a video file path and at least one extraction instruction

## CONTEXT BOUNDARIES:

- Available context: This is the first step — no prior context
- Focus: Gathering inputs only
- Limits: Do not analyse or process the video yet
- Dependencies: None — this is the entry point

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Welcome and Explain

"**Video Clip Extraction**

This workflow extracts reusable video assets from finished/edited footage:
- **B-roll clips** — for future video projects
- **Speed-up clips** — for social content
- **LinkedIn clips** — short video attachments for LinkedIn posts

I'll need two things from you:
1. The path to your finished video file
2. Extraction instructions (what to extract and where)"

### 2. Request Video File Path

"**Please provide the path to your finished video file.**"

Wait for user to provide the video file path. Validate the path is provided.

### 3. Request Extraction Instructions

"**Now provide your extraction instructions.**

For each clip you want extracted, I need:
- **Clip type:** B-roll, speed-up, or LinkedIn
- **Timestamp range:** Start time → End time (e.g., 02:15 → 02:45)
- **Notes (optional):** Any specific requirements (e.g., target duration, speed factor for speed-ups)

You can provide these as a list, a table, or paste from another document."

Wait for user to provide extraction instructions.

### 4. Validate and Confirm Inputs

Confirm all inputs are present:

"**Inputs received:**

**Video file:** {video file path}

**Extraction instructions:**
{summarise the extraction instructions in a clear table format}

| # | Type | Start | End | Notes |
|---|------|-------|-----|-------|
| 1 | {type} | {start} | {end} | {notes} |
| ... | ... | ... | ... | ... |

**Does this look correct?**"

Wait for user confirmation. If they want to adjust, collect corrections and re-confirm.

### 5. Proceed to Confirmation

"**Proceeding to extraction plan confirmation...**"

#### Menu Handling Logic:

- After user confirms inputs are correct, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step — once inputs are validated and confirmed, move directly to step 2
- If user has not confirmed, do not proceed

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user has confirmed their inputs (video file path and extraction instructions) are correct will you load and read fully `step-02-confirm.md` to begin extraction plan confirmation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Video file path collected
- Extraction instructions collected with clip types and timestamps
- Inputs summarised and confirmed by user
- Proceeding to step 2

### ❌ SYSTEM FAILURE:

- Proceeding without a video file path
- Proceeding without extraction instructions
- Not confirming inputs with user
- Beginning clip extraction in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
