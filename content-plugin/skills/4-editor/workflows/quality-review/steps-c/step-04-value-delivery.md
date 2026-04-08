---
name: 'step-04-value-delivery'
description: 'Evaluate content against value delivery benchmarks and record gate results'

nextStepFile: './step-05-report.md'
outputFile: '{output_folder}/quality-review-{content_slug}-{date}.md'
---

# Step 4: Value Delivery Gate

## STEP GOAL:

To evaluate whether the content delivers genuine value to the audience, produce a clear pass/fail verdict with specific feedback, and append the gate results to the review report.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a quality reviewer and editorial gatekeeper specializing in content value assessment
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Professional, direct, analytical tone throughout
- ✅ You bring expertise in value delivery evaluation — substance, originality, usefulness, and audience benefit

### Step-Specific Rules:

- 🎯 Focus only on value delivery evaluation — do not reassess brand voice or ICP relevance
- 🚫 FORBIDDEN to provide vague or generic feedback — every finding must be specific and actionable
- 💬 Approach: Systematic evaluation against defined value delivery criteria
- 📋 Each finding must reference specific content passages

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append gate results to the Value Delivery Gate section of {outputFile}
- 📖 Update frontmatter stepsCompleted with 'step-04-value-delivery'
- 🚫 Do not modify any other section of the report

## CONTEXT BOUNDARIES:

- Available context: Content from step-01, previous gate results (if run)
- Focus: Value delivery and content substance only
- Limits: Do not re-evaluate brand voice or ICP relevance — those are separate gates
- Dependencies: Content and content type from step-01

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Value Delivery Standards

Check for value delivery documentation in the project:
- Look for content quality standards, value criteria, or editorial guidelines in the project data folder
- If value delivery standards are found, load them as the evaluation criteria
- If no value delivery standards are found, use these universal value delivery evaluation criteria:

**Universal Value Delivery Criteria:**
1. **Substance & Depth** — Does the content go beyond surface-level? Does it provide meaningful insight, not just filler?
2. **Originality** — Does the content offer a unique perspective, original thinking, or fresh angle? Or is it generic and interchangeable?
3. **Actionability** — Can the audience DO something with this content? Does it provide practical takeaways, not just theory?
4. **Clarity of Message** — Is the core message clear and easy to grasp? Does the content deliver on what it promises (headline, hook, intro)?
5. **Engagement Quality** — Does the content earn attention through substance, not just tricks? Would the audience share or reference it?

### 2. Evaluate Content Against Each Criterion

For each value delivery criterion, evaluate the content systematically:

- **Quote specific passages** that support or violate the criterion
- **Assign a rating** for each criterion: PASS, WEAK PASS, or FAIL
- **Provide specific feedback** explaining the rating
- **Suggest specific improvements** for any non-PASS ratings

### 3. Determine Overall Gate Verdict

Based on individual criterion ratings:
- **PASS** — All criteria pass or have minor issues only
- **CONDITIONAL PASS** — Mostly passes but has 1-2 areas needing improvement
- **FAIL** — Multiple criteria fail or one critical failure (e.g., content is pure filler with no substance)

### 4. Append Results to Report

Replace the Value Delivery Gate section placeholder in {outputFile} with:

```markdown
## Value Delivery Gate

**Verdict:** [PASS / CONDITIONAL PASS / FAIL]

### Evaluation Details

**1. Substance & Depth:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**2. Originality:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**3. Actionability:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**4. Clarity of Message:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**5. Engagement Quality:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

### Recommendations
- [Specific, actionable recommendation 1]
- [Specific, actionable recommendation 2]
- [...]
```

Update frontmatter `stepsCompleted` to include 'step-04-value-delivery'.

### 5. Proceed to Report

"**Value Delivery Gate complete — Verdict: [VERDICT]**

**All gates evaluated. Proceeding to compile final report...**"

Load, read entire file, then execute {nextStepFile} (step-05-report.md).

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the value delivery evaluation is complete and results have been appended to {outputFile} will you proceed to the report compilation step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All value delivery criteria evaluated systematically
- Specific passages quoted as evidence
- Each criterion has a clear rating
- Overall gate verdict determined
- Results appended to report with structured format
- Recommendations are specific and actionable
- Proceeded to report compilation step

### ❌ SYSTEM FAILURE:

- Generic feedback without specific examples ("the content provides value")
- Re-evaluating brand voice or ICP relevance in this step
- Not quoting specific content passages
- Skipping criteria without justification
- Not appending results to report before proceeding

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
