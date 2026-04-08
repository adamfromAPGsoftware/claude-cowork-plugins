---
name: 'step-04-title-generation'
description: 'Generate title options for each angle with keyword integration and ICP scoring'

nextStepFile: './step-05-composition-drafting.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 4: Title Generation

## STEP GOAL:

To generate 3-5 title options per selected angle, integrating high-signal keywords naturally, and have the user select the final title/text-overlay combinations to develop into full thumbnail combos.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a title copywriter who understands YouTube CTR psychology
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring hook pattern expertise, keyword integration, and character-count discipline
- ✅ The user brings their voice and creative preferences

### Step-Specific Rules:

- 🎯 Focus on generating titles and thumbnail text overlays
- 🚫 FORBIDDEN to write Gemini prompts or composition details — that's step 05
- 💬 Present titles in a clear table with character counts and keyword notes
- 📋 Character counts must be ACCURATE — count the actual characters, do not estimate

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Generate Title Options

For each selected angle from step 02, generate 3-5 title options:

**Hook patterns to apply:**
- Curiosity gap ("I tried X and...")
- Number/stat lead ("5 tools that...")
- Transformation claim ("From X to Y in...")
- Contrarian take ("Stop using X for...")
- How-to with twist ("How to X (without Y)")

**For each title:**
- Incorporate HIGH-SIGNAL keywords from step 03 where they fit naturally — do NOT force keywords that break the hook
- Target under 60 characters
- Calculate exact character count

**For each title, also draft a thumbnail text overlay:**
- Under 12 characters (this appears ON the thumbnail image)
- Must complement the title, not duplicate it
- Calculate exact character count

### 2. Present Title Options

Present all titles in a structured format:

"**Title Options:**

**Angle 1: {angle name}**

| # | Title | Chars | Text Overlay | Chars | Keywords Used |
|---|-------|-------|-------------|-------|--------------|
| 1a | {title} | {count} | {text} | {count} | {keywords} |
| 1b | {title} | {count} | {text} | {count} | {keywords} |
| 1c | {title} | {count} | {text} | {count} | {keywords} |

**Angle 2: {angle name}**

| # | Title | Chars | Text Overlay | Chars | Keywords Used |
|---|-------|-------|-------------|-------|--------------|
| 2a | ... | ... | ... | ... | ... |

..."

### 3. User Selection

"**Select the title/text combos to develop into full thumbnail compositions.**

Pick one title per angle (e.g., `1a, 2c, 3b`) or modify any title before selecting.

Aim for 3-5 final combos total."

Wait for user selection. Allow modifications.

### 3b. AUTO MODE — Title Selection

**Only execute this section if `{workflow_mode}` is `auto`. Skip entirely in collab mode.**

Auto-select **1 best title per angle** using the following priority criteria:

1. **Curiosity gap strength** — strongest information gap between title + thumbnail
2. **Keyword integration** — natural incorporation of high-signal keywords
3. **Character count** — prefer <55 chars, penalize >60
4. **Proven hook pattern** — prefer patterns matching outlier data (default ranking: curiosity gap > number/stat > transformation > contrarian > how-to)
5. **Text overlay complementarity** — title + overlay form coherent unit, not duplicate

Log selection rationale per angle:
"**Auto-selected titles:**

| Combo | Angle | Title | Chars | Text Overlay | Rationale |
|-------|-------|-------|-------|-------------|-----------|
| 1 | {angle} | {title} | {count} | {text} | {why this title won — which criteria} |
| 2 | {angle} | {title} | {count} | {text} | {rationale} |
| 3 | {angle} | {title} | {count} | {text} | {rationale} |

**Auto-proceeding to composition drafting...**"

Skip user confirmation and the [A]/[P]/[C] menu. Auto-proceed to {nextStepFile}.

### 4. Confirm Final Combo List

Present the selected combos clearly:

"**Final Combos for Composition Drafting:**

| Combo | Angle | Title | Text Overlay | Expression |
|-------|-------|-------|-------------|-----------|
| 1 | {angle} | {title} | {text} | {expression from step 02} |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |

Confirm these are the combos to draft compositions for?"

Wait for confirmation.

### 5. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Composition Drafting

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [3-5 combos confirmed by user], will you load and read fully `{nextStepFile}` to begin composition drafting.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- 3-5 title options generated per angle with keyword integration
- Character counts accurate for both titles and text overlays
- User selected final combos
- Combos confirmed and stored for step 05

### ❌ SYSTEM FAILURE:

- Inaccurate character counts
- Forcing keywords that break the hook
- Writing Gemini prompts in this step
- Not presenting titles for user selection
- Proceeding without user confirming final combo list

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
