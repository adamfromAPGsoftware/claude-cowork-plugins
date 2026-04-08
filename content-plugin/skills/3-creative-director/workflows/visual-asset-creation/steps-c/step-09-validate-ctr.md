---
name: 'step-09-validate-ctr'
description: 'Run 7-point CTR checklist on any thumbnail + title pair — standalone validation'

ctrChecklistData: '../data/ctr-checklist.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 9: Validate CTR (Standalone)

## STEP GOAL:

To run the 7-point CTR validation scorecard on any thumbnail + title pair. This can be used on thumbnails from any source — generated, manually created, or competitor thumbnails for benchmarking.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a CTR analyst with data-driven validation expertise
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring CTR psychology, mobile readability expertise, and thumbnail performance data
- ✅ The user brings their thumbnails and titles for validation

### Step-Specific Rules:

- 🎯 Focus on honest, actionable CTR validation
- 🚫 FORBIDDEN to inflate scores to avoid feedback
- 💬 Be specific in notes — "looks good" is not acceptable
- 📋 Every check must have a score AND specific notes

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load CTR Checklist

Load and read {ctrChecklistData} completely.

### 2. Gather Inputs

"**What thumbnail + title pair do you want to validate?**

I need:
1. **Thumbnail** — file path to the image (I'll analyse the visual elements)
2. **Title** — the YouTube title paired with this thumbnail
3. **Text overlay** — what text appears on the thumbnail image

Provide all three, or point me to a project folder to find them."

If an active project is set, offer to scan the generated folder:
"I can also scan `{project_folder}/{project-slug}/creative-director/thumbnails/generated/` for recent thumbnails."

Wait for user input.

### 3. Analyse and Score

Read the thumbnail image to analyse visual elements.

Run the 7-point checklist using the presentation template from the CTR checklist:

"**CTR Validation Results:**

**Title:** {title}
**Text Overlay:** {text overlay}

| # | Check | Score | Notes |
|---|-------|-------|-------|
| 1 | Text character count | {PASS/WARN/FAIL} | {text}: {count} characters |
| 2 | 3-element composition | {PASS/WARN/FAIL} | {what's present — face, object, text positions} |
| 3 | Curiosity gap | {PASS/WARN/FAIL} | {specific assessment of title + thumbnail information gap} |
| 4 | Title-thumbnail coherence | {PASS/WARN/FAIL} | {complementary or redundant — be specific} |
| 5 | Mobile readability | {PASS/WARN/FAIL} | {assessment at 168x94px phone display} |
| 6 | Emotional trigger | {PASS/WARN/FAIL} | {expression assessment and match to content tone} |
| 7 | ICP relevance | {PASS/WARN/FAIL} | {which ICPs are targeted and how} |

**Overall:** {X}/7 checks passed

{If any FAIL: '⚠️ **Recommendations:**\n' + specific improvements for each FAIL item}
{If all PASS: '✅ **Strong thumbnail — ready to use.**'}
{If 5-6 PASS: '👍 **Good thumbnail with minor improvements possible.**'}"

### 4. Offer Next Steps

"**Options:**
- **[F] Fix** — I'll suggest specific fixes for FAIL/WARN items
- **[V] Validate another** — run validation on a different thumbnail
- **[C] Compare** — validate a second thumbnail to compare scores
- **[D] Done** — exit validation"

#### Menu Handling Logic:

- IF F: Present specific, actionable fix suggestions for each FAIL/WARN item. After presenting, redisplay the options menu.
- IF V: Return to section 2 (Gather Inputs) for a new thumbnail
- IF C: Gather a second thumbnail's inputs, score it, then present side-by-side comparison table
- IF D: End workflow session
- IF Any other: help user respond, then redisplay menu

### 5. Compare Mode (If Selected)

If user chose Compare:

"**CTR Comparison:**

| Check | Thumbnail A | Thumbnail B |
|-------|------------|------------|
| Text chars | {score} | {score} |
| Composition | {score} | {score} |
| Curiosity gap | {score} | {score} |
| Coherence | {score} | {score} |
| Mobile readability | {score} | {score} |
| Emotional trigger | {score} | {score} |
| ICP relevance | {score} | {score} |
| **Total** | **{X}/7** | **{Y}/7** |

**Recommendation:** {which thumbnail is stronger and why}"

Return to section 4 options.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- CTR checklist loaded
- All 3 inputs gathered (thumbnail, title, text overlay)
- All 7 checks scored with specific notes
- Actionable recommendations for FAIL items
- Compare mode works correctly when selected

### ❌ SYSTEM FAILURE:

- Scoring without specific notes per check
- Inflating scores
- Missing any of the 7 checks
- Vague recommendations ("make it better")

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
