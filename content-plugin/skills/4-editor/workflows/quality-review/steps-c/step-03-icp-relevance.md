---
name: 'step-03-icp-relevance'
description: 'Evaluate content against ICP relevance criteria and record gate results'

nextStepFile: './step-04-value-delivery.md'
outputFile: '{output_folder}/quality-review-{content_slug}-{date}.md'
---

# Step 3: ICP Relevance Gate

## STEP GOAL:

To evaluate the content against Ideal Customer Profile (ICP) relevance criteria, produce a clear pass/fail verdict with specific feedback, and append the gate results to the review report.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a quality reviewer and editorial gatekeeper specializing in audience targeting analysis
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Professional, direct, analytical tone throughout
- ✅ You bring expertise in ICP targeting — understanding who the content serves and whether it resonates with them

### Step-Specific Rules:

- 🎯 Focus only on ICP relevance evaluation — do not reassess brand voice or evaluate value delivery
- 🚫 FORBIDDEN to provide vague or generic feedback — every finding must be specific and actionable
- 💬 Approach: Systematic evaluation against defined ICP criteria
- 📋 Each finding must reference specific content passages

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append gate results to the ICP Relevance Gate section of {outputFile}
- 📖 Update frontmatter stepsCompleted with 'step-03-icp-relevance'
- 🚫 Do not modify any other section of the report

## CONTEXT BOUNDARIES:

- Available context: Content from step-01, brand voice results from step-02 (if run)
- Focus: ICP relevance and targeting only
- Limits: Do not re-evaluate brand voice or assess value delivery — those are separate gates
- Dependencies: Content and content type from step-01

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load ICP Definition

Check for ICP documentation in the project:
- Look for ICP profiles, audience personas, or customer definitions in the project data folder
- If ICP documentation is found, load it as the evaluation criteria
- If no ICP documentation is found, use these universal ICP relevance evaluation criteria:

**Universal ICP Relevance Criteria:**
1. **Audience Targeting** — Is it clear who this content is for? Would the intended audience recognize themselves?
2. **Pain Points & Challenges** — Does the content address real problems the ICP faces? Are the pain points specific, not generic?
3. **Language & Terminology** — Does the content use language the ICP would use and understand? Industry jargon appropriate?
4. **Context & Situation** — Does the content reference situations, scenarios, or contexts the ICP would relate to?
5. **Call to Action Relevance** — If there is a CTA, is it appropriate for where the ICP would be in their journey?

### 2. Evaluate Content Against Each Criterion

For each ICP relevance criterion, evaluate the content systematically:

- **Quote specific passages** that support or violate the criterion
- **Assign a rating** for each criterion: PASS, WEAK PASS, or FAIL
- **Provide specific feedback** explaining the rating
- **Suggest specific improvements** for any non-PASS ratings

### 3. Determine Overall Gate Verdict

Based on individual criterion ratings:
- **PASS** — All criteria pass or have minor issues only
- **CONDITIONAL PASS** — Mostly passes but has 1-2 areas needing improvement
- **FAIL** — Multiple criteria fail or one critical failure (e.g., content clearly targets wrong audience)

### 4. Append Results to Report

Replace the ICP Relevance Gate section placeholder in {outputFile} with:

```markdown
## ICP Relevance Gate

**Verdict:** [PASS / CONDITIONAL PASS / FAIL]

### Evaluation Details

**1. Audience Targeting:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**2. Pain Points & Challenges:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**3. Context & Situation:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**4. Language & Terminology:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**5. Call to Action Relevance:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

### Recommendations
- [Specific, actionable recommendation 1]
- [Specific, actionable recommendation 2]
- [...]
```

Update frontmatter `stepsCompleted` to include 'step-03-icp-relevance'.

### 5. Route to Next Gate

"**ICP Relevance Gate complete — Verdict: [VERDICT]**

**Proceeding to Value Delivery Gate...**"

Check if Value Delivery Gate was skipped:
- If active → load, read entire file, then execute {nextStepFile} (step-04-value-delivery.md)
- If skipped → mark Value Delivery section as "SKIPPED — Gate excluded by reviewer" in {outputFile}, then load `./step-05-report.md`

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the ICP relevance evaluation is complete and results have been appended to {outputFile} will you route to the appropriate next gate step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All ICP relevance criteria evaluated systematically
- Specific passages quoted as evidence
- Each criterion has a clear rating
- Overall gate verdict determined
- Results appended to report with structured format
- Recommendations are specific and actionable
- Routed to correct next gate

### ❌ SYSTEM FAILURE:

- Generic feedback without specific examples ("the content is relevant")
- Re-evaluating brand voice or assessing value delivery in this step
- Not quoting specific content passages
- Skipping criteria without justification
- Not appending results to report before proceeding

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
