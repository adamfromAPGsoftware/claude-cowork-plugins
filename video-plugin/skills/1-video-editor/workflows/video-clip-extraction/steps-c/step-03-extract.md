---
name: 'step-03-extract'
description: 'Execute clip extraction for all clip types sequentially'

nextStepFile: './step-04-completion.md'
---

# Step 3: Extract Clips

## STEP GOAL:

To execute the extraction of all requested clips from the finished video — B-roll, speed-ups, and LinkedIn clips — saving each with the correct naming convention to the correct output paths.

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
- ✅ Execute extraction precisely — follow the confirmed plan exactly
- ✅ Report progress clearly as each clip is processed

### Step-Specific Rules:

- 🎯 Focus only on extracting clips as specified in the confirmed plan
- 🚫 FORBIDDEN to extract clips not in the confirmed plan
- 🚫 FORBIDDEN to modify timestamps or clip types without user approval
- 💬 Approach: Execute systematically, report progress for each clip

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Extract clips using file I/O operations
- 📖 Report progress after each clip type is processed
- 🚫 FORBIDDEN to skip any clips in the confirmed plan

## CONTEXT BOUNDARIES:

- Available context: Confirmed extraction plan from Step 2 (clip types, timestamps, output filenames)
- Focus: Executing extraction operations
- Limits: Only extract what was confirmed — no additions or modifications
- Dependencies: Requires confirmed extraction plan from Step 2

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Begin Extraction

"**Beginning clip extraction...**"

### 2. Extract B-Roll Clips

If B-roll clips are in the plan:

"**Extracting B-Roll clips...**"

For each B-roll clip in the plan:
- Extract the clip from the source video at the specified timestamp range
- Save as `{video-id}-broll-{n}.mp4` to the output path
- Report: "✅ B-Roll {n}: {start} → {end} — saved as {output filename}"

If no B-roll clips requested:
"*No B-roll clips requested — skipping.*"

### 3. Extract Speed-Up Clips

If speed-up clips are in the plan:

"**Extracting Speed-Up clips...**"

For each speed-up clip in the plan:
- Extract the clip from the source video at the specified timestamp range
- Apply the specified speed factor
- Save as `{video-id}-speedup-{n}.mp4` to the output path
- Report: "✅ Speed-Up {n}: {start} → {end} (×{speed factor}) — saved as {output filename}"

If no speed-up clips requested:
"*No speed-up clips requested — skipping.*"

### 4. Extract LinkedIn Clips

If LinkedIn clips are in the plan:

"**Extracting LinkedIn clips...**"

For each LinkedIn clip in the plan:
- Extract the clip from the source video at the specified timestamp range
- Save as `{video-id}-linkedin-{n}.mp4` to the output path
- Report: "✅ LinkedIn {n}: {start} → {end} — saved as {output filename}"

If no LinkedIn clips requested:
"*No LinkedIn clips requested — skipping.*"

### 5. Proceed to Completion

"**All clips extracted. Proceeding to completion summary...**"

#### Menu Handling Logic:

- After all clips have been extracted, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step — once all clips are extracted, move directly to step 4
- If extraction fails for any clip, report the error and ask user how to proceed

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN all clips from the confirmed plan have been extracted (or user has acknowledged any failures) will you load and read fully `step-04-completion.md` to present the completion summary.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All B-roll clips extracted and saved with correct naming
- All speed-up clips extracted with correct speed factors and saved
- All LinkedIn clips extracted and saved with correct naming
- Progress reported for each clip
- All files saved to correct output paths
- Proceeding to step 4

### ❌ SYSTEM FAILURE:

- Skipping clips from the confirmed plan
- Extracting clips not in the plan
- Wrong naming convention on output files
- Not reporting progress for each clip
- Modifying timestamps without user approval

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
