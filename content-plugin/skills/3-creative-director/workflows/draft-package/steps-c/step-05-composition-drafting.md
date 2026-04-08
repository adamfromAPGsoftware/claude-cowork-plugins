---
name: 'step-05-composition-drafting'
description: 'Draft 3-element composition tables, expression directions, and full Gemini prompts for each combo'

nextStepFile: './step-06-ctr-pre-validation.md'
promptTemplateData: '../../visual-asset-creation/data/thumbnail-prompt-template.md'
shortFormGuideData: '../../visual-asset-creation/data/short-form-style-guide.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 5: Composition Drafting

## STEP GOAL:

To build a full composition breakdown for each confirmed combo — 3-element layout, expression direction, background description, and a complete Gemini prompt — so the user can review and edit everything before generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a visual composition expert designing thumbnail layouts
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring 3-element composition expertise, expression psychology, and prompt engineering for Gemini image generation
- ✅ The user brings their creative preferences and content knowledge

### Step-Specific Rules:

- 🎯 Focus on composition tables and Gemini prompt construction
- 🚫 FORBIDDEN to execute any generation scripts — that happens via [VA] Visual Assets after the plan is written
- 💬 Present each combo's composition clearly for user review
- 📋 Use the loaded prompt template ({promptTemplateData}) to construct prompts — do NOT freestyle
- 🚫 FORBIDDEN to describe the user's face in the text prompt — reference photos handle identity preservation

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Prompt Template

Load and read {promptTemplateData} completely.

Also confirm the reference photos folder from CCS config: `{reference_photos_folder}`

### 2. Draft Composition for Each Combo

For each confirmed combo from step 04, build a composition table:

**Present each combo as:**

"**Combo {N}: {title}**

**Text Overlay:** {text overlay} ({char count} chars)
**Expression:** {expression from step 02 angle}

| Element | Position | Description |
|---------|----------|-------------|
| Face | {left third / right third / centre} | {expression direction — specific facial cues} |
| Object/Context | {centre / background / opposite side} | {what the viewer sees besides the face — tools, screens, logos, etc.} |
| Text | {opposite third from face / top / bottom} | "{EXACT TEXT}" in {colour} {font style} |

**Background:** {specific background description — not just 'dark' but e.g., 'dark gradient with subtle code editor lines'}

**Full Gemini Prompt:**
```
{complete prompt following the loaded template structure}
```
"

### 3. Present All Combos Together

After building all compositions, present them together for comparison:

"**Composition Drafts — All Combos:**

{Combo 1 table + prompt}

---

{Combo 2 table + prompt}

---

{Combo 3 table + prompt}

**Review these compositions and prompts. You can:**
- Modify any element (expression, position, background, text)
- Swap elements between combos
- Add or remove a combo
- Edit the prompt text directly

**Type your changes, or `approve` to lock these compositions.**"

Wait for user review. Apply any modifications.

### 3b. AUTO MODE — Composition Approval

**Only execute this section if `{workflow_mode}` is `auto`. Skip entirely in collab mode.**

Draft all compositions using the exact same process as collab mode (template, 3-element tables, Gemini prompts). Output everything for the audit trail.

Auto-approve all compositions without waiting for user review:
"**All {count} compositions drafted and auto-approved.**

**Auto-proceeding to CTR pre-validation...**"

Skip the [A]/[P]/[C] menu and auto-proceed to {nextStepFile}.

### 4. Confirm Final Compositions

After user approves (with or without modifications):

"**Compositions locked for CTR pre-validation.**

| Combo | Title | Text Overlay | Expression | Elements |
|-------|-------|-------------|-----------|----------|
| 1 | {title} | {text} | {expression} | {face position} + {object} + {text position} |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |

Proceeding to CTR pre-validation..."

### 5. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to CTR Pre-Validation

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [all compositions approved by user], will you load and read fully `{nextStepFile}` to begin CTR pre-validation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Prompt template loaded and followed
- 3-element composition table built for each combo
- Expression direction specific and actionable
- Background descriptions specific (not generic)
- Full Gemini prompts constructed using the template structure
- User reviewed and approved all compositions
- No face descriptions in prompts (reference photos handle identity)

### ❌ SYSTEM FAILURE:

- Executing generation scripts in this step
- Describing the user's face in prompt text
- Generic backgrounds ("dark background" without detail)
- Not using the loaded prompt template structure
- Not presenting compositions for user review
- Proceeding without user approval

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
