---
name: 'step-03-evaluate'
description: 'Score and rank selected content ideas against ICP relevance, uniqueness, and brand fit'

nextStepFile: './step-04-tree.md'
outputFile: '{output_folder}/content-concept-{concept_slug}-{date}.md'
scoringCriteria: '../data/scoring-criteria.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 3: Evaluate & Rank

## STEP GOAL:

To score the selected content concepts from Step 2 against a consistent framework of ICP relevance, uniqueness, brand fit, and platform potential, then present ranked results so the user can select the top idea for content tree mapping.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Content Strategist applying analytical rigor to creative ideas
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You bring expertise in audience analysis, competitive positioning, and brand alignment
- ✅ The user brings their intuitive sense of what resonates with their audience
- ✅ Together we balance data-driven evaluation with creative instinct

### Step-Specific Rules:

- 🎯 Focus only on evaluating and ranking — do NOT generate new ideas
- 🚫 FORBIDDEN to map content trees in this step — that happens in Step 4
- 🚫 FORBIDDEN to skip any scoring criterion
- 💬 Explain scoring rationale transparently so the user understands each rating
- 📊 Use the scoring framework from {scoringCriteria} consistently across all ideas

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append evaluation results and selected top idea to {outputFile} under the ICP Alignment Rationale section
- 📖 Update frontmatter stepsCompleted to include 'step-03-evaluate'
- 🚫 FORBIDDEN to proceed without user selecting a top idea

## CONTEXT BOUNDARIES:

- Available: Selected concepts from Step 2 (in output document), brand guidelines, ICP profile
- Focus: Objective evaluation using consistent scoring framework
- Limits: Do not generate new ideas or map content trees
- Dependencies: Selected concepts from Step 2

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Scoring Framework

Load {scoringCriteria} to understand the evaluation criteria:

"**Time to evaluate your selected concepts.**

I'll score each idea against four criteria:

| Criterion | Weight | What It Measures |
|-----------|--------|-----------------|
| ICP Relevance | High (x2) | How directly it addresses your audience's needs |
| Uniqueness | Medium (x1) | How differentiated it is from competitor content |
| Brand Fit | High (x2) | How well it aligns with your brand voice and values |
| Platform Potential | Medium (x1) | How naturally it maps across multiple platforms |

**Max Score: 30**

Let me evaluate each concept..."

### 2. Score Each Concept

For each selected concept from Step 2, apply the scoring framework:

"**Concept: [Title]**

| Criterion | Score (1-5) | Rationale |
|-----------|:-----------:|-----------|
| ICP Relevance | [score] | [Why this score — reference specific ICP attributes] |
| Uniqueness | [score] | [Why this score — reference competitive landscape] |
| Brand Fit | [score] | [Why this score — reference brand guidelines] |
| Platform Potential | [score] | [Why this score — reference platform suitability] |

**Total: [weighted total] / 30** — [Rating: Excellent/Good/Fair/Weak]

---"

Repeat for each concept.

### 3. Present Ranked Results

Present all concepts ranked by total score:

"**Ranked Results:**

| Rank | Concept | Score | Rating |
|:----:|---------|:-----:|--------|
| 1 | [Title] | [score]/30 | [Rating] |
| 2 | [Title] | [score]/30 | [Rating] |
| 3 | [Title] | [score]/30 | [Rating] |

**Top Recommendation:** [Title] scored highest because [brief explanation of key strengths].

**Key Insight:** [Any notable observation — e.g., close scores, surprising results, trade-offs between ideas]"

### 4. User Selection

"**Which concept would you like to develop into a full content tree?**

You can:
- **Select the top-ranked concept** — Go with the data
- **Select a different concept** — Trust your instinct
- **Request re-evaluation** — If you disagree with any scores, I'll adjust
- Use **Advanced Elicitation** to stress-test the top idea before committing

**Your choice:**"

Wait for user input.

**If user selects a concept:** Confirm the selection.

**If user disagrees with scores:** Discuss specific criteria, adjust scores with rationale, re-rank if needed.

**If user wants to combine concepts:** Discuss feasibility, create a combined concept with new scores if agreed.

"**Selected for content tree mapping:**

**[Concept Title]**
- Score: [score]/30
- Key Strengths: [top 2 scoring criteria]
- Hook: [The angle from Step 2]

This concept will be mapped across your target platforms in the next step."

### 5. Present MENU OPTIONS

Display: "**Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Content Tree Mapping"

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Append evaluation results and selected concept to {outputFile} under the ICP Alignment Rationale section, update frontmatter stepsCompleted to include 'step-03-evaluate', then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#5-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions - always respond and then end with display again of the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the evaluation results with the selected top concept have been appended to {outputFile}, will you then load and read fully `{nextStepFile}` to execute and begin content tree mapping.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Scoring framework loaded and explained to user
- Every selected concept scored across all four criteria with transparent rationale
- Scores reference specific ICP attributes, brand guidelines, and competitive landscape
- Ranked results presented clearly
- User selected a top concept (or adjusted scores with discussion)
- Evaluation results and selection appended to output document

### ❌ SYSTEM FAILURE:

- Skipping any scoring criterion
- Not explaining score rationale
- Generating new ideas in this step
- Mapping content trees in this step
- Proceeding without user selecting a top concept
- Not using the scoring framework from {scoringCriteria}

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
