---
name: 'step-05-report'
description: 'Compile overall verdict, add recommendations, and finalize the quality review report'

outputFile: '{output_folder}/quality-review-{content_slug}-{date}.md'
---

# Step 5: Review Report

## STEP GOAL:

To compile all gate results into an overall verdict, add prioritized recommendations, and finalize the quality review report as a complete deliverable.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a quality reviewer and editorial gatekeeper delivering a final assessment
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Professional, direct, analytical tone throughout
- ✅ You bring expertise in synthesizing quality findings into clear, actionable reports

### Step-Specific Rules:

- 🎯 Focus only on compiling the overall verdict and finalizing the report
- 🚫 FORBIDDEN to re-evaluate any gate — use the results already recorded
- 💬 Approach: Synthesize findings into a clear overall assessment
- 📋 Prioritize recommendations by impact

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Replace the Overall Verdict section placeholder in {outputFile}
- 📖 Update frontmatter stepsCompleted with 'step-05-report' and mark workflow complete
- 🚫 Do not modify individual gate result sections

## CONTEXT BOUNDARIES:

- Available context: Complete report with all gate results appended
- Focus: Overall synthesis and final verdict only
- Limits: Do not re-run or modify individual gate evaluations
- Dependencies: All active gates must have been evaluated and recorded

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Complete Report

Load {outputFile} and read all gate results that have been recorded.

Identify:
- Which gates were run and their individual verdicts
- Which gates were skipped
- Key findings across all gates
- Common themes or patterns in the feedback

### 2. Determine Overall Verdict

Based on individual gate verdicts:

- **PASS** — All active gates passed. Content is ready for publication/use.
- **CONDITIONAL PASS** — No gate failed outright, but one or more gates have a conditional pass. Content needs minor revisions before publication.
- **FAIL** — One or more gates failed. Content requires significant revision before it meets quality standards.

**Verdict logic:**
- Any gate FAIL → Overall FAIL
- Any gate CONDITIONAL PASS (and no FAILs) → Overall CONDITIONAL PASS
- All gates PASS → Overall PASS
- If gates were skipped, note this as a caveat in the verdict

### 3. Compile Prioritized Recommendations

Gather all recommendations from individual gates and prioritize them:

**Priority 1 — Must Fix (from FAIL ratings):**
- Issues that caused gate failures
- Critical problems that must be addressed

**Priority 2 — Should Fix (from WEAK PASS/CONDITIONAL PASS ratings):**
- Issues that weakened the content
- Improvements that would meaningfully strengthen quality

**Priority 3 — Consider (from PASS ratings with minor notes):**
- Optional refinements
- Polish items that could elevate the content further

### 4. Identify Feedback Routing

Based on the content type and findings, identify who should receive this report:

- **Copywriter** — If brand voice or messaging issues dominate
- **Creative Director** — If strategic direction or originality issues dominate
- **Video Editor** — If the content is video-related and structural issues found
- **Content Creator (general)** — If issues span multiple areas

### 5. Append Overall Verdict to Report

Replace the Overall Verdict section placeholder in {outputFile} with:

```markdown
## Overall Verdict

**Result:** [PASS / CONDITIONAL PASS / FAIL]

**Gates Summary:**
| Gate | Verdict |
|------|---------|
| Brand Voice | [PASS/CONDITIONAL PASS/FAIL/SKIPPED] |
| ICP Relevance | [PASS/CONDITIONAL PASS/FAIL/SKIPPED] |
| Value Delivery | [PASS/CONDITIONAL PASS/FAIL/SKIPPED] |

### Priority 1 — Must Fix
- [Issue from failed criteria with specific reference]
- [...]

### Priority 2 — Should Fix
- [Issue from weak pass criteria with specific reference]
- [...]

### Priority 3 — Consider
- [Optional refinement]
- [...]

### Feedback Routing
**Send this report to:** [Agent/role recommendation]
**Reason:** [Brief explanation of why this agent should handle revisions]

---

*Quality review completed on {{date}} by {{user_name}}*
```

### 6. Finalize Report

Update {outputFile} frontmatter:
- Add 'step-05-report' to `stepsCompleted`
- Set `lastStep` to 'step-05-report'
- Set status to 'COMPLETE'

### 7. Present Final Summary

"**Quality Review Complete**

**Overall Verdict: [VERDICT]**

**Gate Results:**
- Brand Voice: [verdict or SKIPPED]
- ICP Relevance: [verdict or SKIPPED]
- Value Delivery: [verdict or SKIPPED]

**Top Recommendations:**
1. [Highest priority recommendation]
2. [Second priority recommendation]
3. [Third priority recommendation]

**Report saved to:** {outputFile}

**Feedback routing:** Send to [recommended agent/role] for revisions.

---

This workflow is now complete."

## CRITICAL STEP COMPLETION NOTE

This is the FINAL step. No next step file exists. The workflow ends after the report is finalized and presented to the user.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All gate results read and synthesized
- Overall verdict correctly determined from individual gate verdicts
- Recommendations prioritized by impact (must fix, should fix, consider)
- Feedback routing identified based on content type and findings
- Report finalized with complete Overall Verdict section
- Frontmatter updated to mark workflow complete
- Final summary presented to user

### ❌ SYSTEM FAILURE:

- Re-evaluating individual gates instead of using recorded results
- Overall verdict contradicts individual gate verdicts
- Generic recommendations not tied to specific findings
- Not prioritizing recommendations
- Not finalizing the report file
- Not marking the workflow as complete

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
