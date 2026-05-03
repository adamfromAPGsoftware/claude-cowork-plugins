---
name: 'step-06-ctr-pre-validation'
description: 'Run 7-point CTR scorecard on each combo before generation to catch issues early'

nextStepFile: './step-07-write-plan.md'
ctrChecklistData: '../../visual-asset-creation/data/ctr-checklist.md'
---

# Step 6: CTR Pre-Validation

## STEP GOAL:

To run the 7-point CTR validation scorecard on each combo BEFORE generation — catching text length issues, composition gaps, weak curiosity gaps, and expression mismatches while changes are still free (no API credits spent yet).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a CTR analyst applying data-driven validation before generation
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring CTR psychology, mobile readability expertise, and thumbnail performance data
- ✅ The user brings their audience knowledge and creative judgement

### Step-Specific Rules:

- 🎯 Focus on scoring and identifying issues — not on generating thumbnails
- 🚫 FORBIDDEN to execute any generation scripts
- 💬 Be honest about scores — don't inflate to avoid uncomfortable feedback
- 📋 Every combo MUST be scored — no skipping

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load CTR Checklist

Load and read {ctrChecklistData} completely. Use the 7-point validation criteria and presentation template.

### 2. Score Each Combo

For each confirmed combo, run the 7-point checklist:

"**CTR Pre-Validation — Combo {N}: {title}**

| # | Check | Score | Notes |
|---|-------|-------|-------|
| 1 | Text character count | {PASS/WARN/FAIL} | {text overlay}: {count} characters |
| 2 | 3-element composition | {PASS/WARN/FAIL} | {what's present: face + object + text} |
| 3 | Curiosity gap | {PASS/WARN/FAIL} | {assessment of title + thumbnail gap} |
| 4 | Title-thumbnail coherence | {PASS/WARN/FAIL} | {complementary or redundant?} |
| 5 | Mobile readability | {PASS/WARN/FAIL} | {will text/elements be clear at 168x94px?} |
| 6 | Emotional trigger | {PASS/WARN/FAIL} | {does expression match content tone?} |
| 7 | ICP relevance | {PASS/WARN/FAIL} | {which ICPs targeted?} |

**Pre-Score:** {X}/7
{If any FAIL: '⚠️ Recommendations: [specific improvements]'}
{If all PASS: '✅ Strong combo — ready for generation.'}"

### 3. Present Summary Table

After scoring all combos:

"**CTR Pre-Validation Summary:**

| Combo | Title | Text Overlay | Pre-Score | Issues |
|-------|-------|-------------|-----------|--------|
| 1 | {title} | {text} | {X}/7 | {FAIL items or 'None'} |
| 2 | ... | ... | {X}/7 | ... |
| 3 | ... | ... | {X}/7 | ... |

**Recommendation:** {rank combos by score, flag any with FAIL items}

**Options:**
- `fix` — I'll suggest specific fixes for any FAIL/WARN items
- `drop {N}` — Remove a weak combo
- `approve` — Accept all scores and proceed to plan writing"

Wait for user decision.

### 3b. AUTO MODE — Auto Fix Loop

**Only execute this section if `{workflow_mode}` is `auto`. Skip entirely in collab mode.**

Score all combos using the same 7-point checklist (section 2). For any FAIL items, auto-fix using these rules:

- **Text >15 chars** → shorten to <12 using strongest words
- **Weak curiosity gap** → rewrite title to strengthen info gap (keep keywords)
- **Expression mismatch** → swap to matching expression per Expression Performance Ranking
- **Missing composition element** → add it and update Gemini prompt
- **Title-thumbnail redundancy** → rewrite overlay to complement, not duplicate
- **Mobile readability fail** → simplify/enlarge text
- **ICP relevance fail** → adjust visual direction

After fixes, re-score the affected combos and present the updated summary.

**One fix cycle maximum.** If any combo still has a FAIL after 1 fix cycle, drop that combo with a logged reason.

**Hard floor: minimum 2 combos must survive.** If fewer than 2 combos pass after fixing, HALT with diagnostic:
"**AUTO MODE HALTED:** Only {count} combo(s) survived CTR validation. Minimum 2 required.
{list each dropped combo and why}
Switch to collab mode (`DP collab`) to manually resolve."

If 2+ combos survive:
"**Auto CTR validation complete.**

| Combo | Title | Pre-Score | Fixed | Post-Fix Score |
|-------|-------|-----------|-------|----------------|
| 1 | {title} | {X}/7 | {Yes/No} | {X}/7 |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |

{If any dropped: '**Dropped:** Combo {N} ({title}) — {reason}'}

**Auto-proceeding to write plan...**"

Skip the [A]/[P]/[C] menu and auto-proceed to {nextStepFile}.

### 4. Fix Loop (If Requested)

If user requests fixes:

For each FAIL/WARN item, suggest a specific fix:
- Text too long → suggest shorter alternatives
- Weak curiosity gap → suggest title/text rewording
- Expression mismatch → suggest different expression
- Composition issue → suggest element repositioning

After fixes, re-score the affected combos and present the updated summary.

Repeat until user approves.

### 5. Lock Pre-Scores

After user approves:

"**Pre-validation scores locked.** These will be included in the package plan for comparison against post-generation CTR scores.

| Combo | Pre-Score |
|-------|-----------|
| 1 | {X}/7 |
| 2 | {X}/7 |
| 3 | {X}/7 |"

### 6. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Write Plan

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [all combos scored and approved], will you load and read fully `{nextStepFile}` to begin writing the package plan.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- CTR checklist loaded
- Every combo scored against all 7 checks
- Scores presented with specific notes (not vague)
- FAIL items flagged with actionable recommendations
- User approved scores (with or without fixes)
- Pre-scores stored for plan writing

### ❌ SYSTEM FAILURE:

- Skipping any combo during scoring
- Inflating scores to avoid feedback
- Vague notes ("looks good" instead of specific assessment)
- Executing generation scripts
- Proceeding without user approving scores

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
