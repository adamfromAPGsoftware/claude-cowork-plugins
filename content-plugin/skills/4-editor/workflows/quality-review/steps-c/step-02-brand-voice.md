---
name: 'step-02-brand-voice'
description: 'Evaluate content against brand voice standards and record gate results'

nextStepFile: './step-03-icp-relevance.md'
outputFile: '{output_folder}/quality-review-{content_slug}-{date}.md'
---

# Step 2: Brand Voice Gate

## STEP GOAL:

To evaluate the content against brand voice standards, produce a clear pass/fail verdict with specific feedback, and append the gate results to the review report.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a quality reviewer and editorial gatekeeper specializing in brand voice analysis
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Professional, direct, analytical tone throughout
- ✅ You bring expertise in brand voice evaluation — tone, vocabulary, personality, consistency

### Step-Specific Rules:

- 🎯 Focus only on brand voice evaluation — do not assess ICP relevance or value delivery
- 🚫 FORBIDDEN to provide vague or generic feedback — every finding must be specific and actionable
- 💬 Approach: Systematic evaluation against defined brand voice criteria
- 📋 Each finding must reference specific content passages

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append gate results to the Brand Voice Gate section of {outputFile}
- 📖 Update frontmatter stepsCompleted with 'step-02-brand-voice'
- 🚫 Do not modify any other section of the report

## CONTEXT BOUNDARIES:

- Available context: Content loaded in step-01, report file created
- Focus: Brand voice consistency only
- Limits: Do not evaluate ICP relevance or value delivery — those are separate gates
- Dependencies: Content and content type from step-01

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Brand Voice Standards

Check for brand voice documentation in the project:
- Look for brand voice rules, tone guidelines, or voice documentation in the project data folder
- If brand voice standards are found, load them as the evaluation criteria
- If no brand voice standards are found, use these universal brand voice evaluation criteria:

**Universal Brand Voice Criteria:**
1. **Tone Consistency** — Is the tone consistent throughout? Does it match the expected tone for this content type?
2. **Vocabulary & Language** — Does the word choice align with the brand's communication style? Any off-brand terminology?
3. **Personality** — Does the content reflect the brand's personality traits? Is it authentic to the brand?
4. **Audience Appropriateness** — Is the language level and style appropriate for the brand's audience?
5. **Emotional Register** — Does the emotional tone match brand guidelines? Too formal? Too casual?

### 2. Evaluate Content Against Each Criterion

For each brand voice criterion, evaluate the content systematically:

- **Quote specific passages** that support or violate the criterion
- **Assign a rating** for each criterion: PASS, WEAK PASS, or FAIL
- **Provide specific feedback** explaining the rating
- **Suggest specific improvements** for any non-PASS ratings

### 3. Determine Overall Gate Verdict

Based on individual criterion ratings:
- **PASS** — All criteria pass or have minor issues only
- **CONDITIONAL PASS** — Mostly passes but has 1-2 areas needing improvement
- **FAIL** — Multiple criteria fail or one critical failure

### 4. Append Results to Report

Replace the Brand Voice Gate section placeholder in {outputFile} with:

```markdown
## Brand Voice Gate

**Verdict:** [PASS / CONDITIONAL PASS / FAIL]

### Evaluation Details

**1. Tone Consistency:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**2. Vocabulary & Language:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**3. Personality:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**4. Audience Appropriateness:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

**5. Emotional Register:** [PASS/WEAK PASS/FAIL]
[Specific findings with quoted passages]

### Recommendations
- [Specific, actionable recommendation 1]
- [Specific, actionable recommendation 2]
- [...]
```

Update frontmatter `stepsCompleted` to include 'step-02-brand-voice'.

### 5. Route to Next Gate

"**Brand Voice Gate complete — Verdict: [VERDICT]**

**Proceeding to ICP Relevance Gate...**"

Check if ICP Relevance Gate was skipped:
- If active → load, read entire file, then execute {nextStepFile} (step-03-icp-relevance.md)
- If skipped → mark ICP Relevance section as "SKIPPED — Gate excluded by reviewer" in {outputFile}, then check Value Delivery Gate:
  - If active → load `./step-04-value-delivery.md`
  - If skipped → load `./step-05-report.md`

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the brand voice evaluation is complete and results have been appended to {outputFile} will you route to the appropriate next gate step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All brand voice criteria evaluated systematically
- Specific passages quoted as evidence
- Each criterion has a clear rating
- Overall gate verdict determined
- Results appended to report with structured format
- Recommendations are specific and actionable
- Routed to correct next gate

### ❌ SYSTEM FAILURE:

- Generic feedback without specific examples ("the tone is good")
- Evaluating ICP relevance or value delivery in this step
- Not quoting specific content passages
- Skipping criteria without justification
- Not appending results to report before proceeding

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
