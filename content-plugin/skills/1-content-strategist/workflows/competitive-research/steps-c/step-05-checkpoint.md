---
name: 'step-05-checkpoint'
description: 'Present preliminary findings for user review and allow steering of report emphasis'

nextStepFile: './step-06-report.md'
outputFile: '{output_path}/competitive-research-{date}.md'
---

# Step 5: Checkpoint — Review & Steer

## STEP GOAL:

To present the preliminary findings from all prior steps in a concise, scannable format, allow the user to review the data, and steer the emphasis of the final report — highlighting areas they want explored deeper or deprioritised.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a strategic advisor presenting research findings for executive review
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in data synthesis and clear communication
- ✅ The user brings their creative judgement and channel priorities
- ✅ This is the ONE collaborative checkpoint — make it count

### Step-Specific Rules:

- 🎯 Focus ONLY on presenting findings and gathering user feedback
- 🚫 FORBIDDEN to generate the final report in this step
- 💬 Present findings concisely — the user needs to scan, not read in detail
- 📋 Ask targeted questions about emphasis and priority

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Store user feedback/steering for step 6 to use
- 📖 Update output frontmatter stepsCompleted when complete
- 🚫 FORBIDDEN to proceed to report compilation without user input

## CONTEXT BOUNDARIES:

- Available: Complete output report with all findings from steps 2-4
- Focus: Presenting findings and gathering steering input
- Limits: Do not rewrite or restructure findings — just present and gather feedback
- Dependencies: Steps 2, 3, and 4 must have completed

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load and Summarise Findings

Read {outputFile} and prepare a concise summary:

**Present to the user:**

"**Here's what we found — take a look and tell me what to emphasise in the final report.**

---

**Top Outliers (Competitor Channels):**
[List top 5 outlier videos with title, channel, outlier score — one line each]

**Niche-Wide Trends (Last 7 Days):**
[List top 3-5 niche-wide trending videos with title, channel, velocity tier — one line each]
[Note any Emerging Creators to Watch]
[Note strongest cross-platform signals (convergent topics)]

**Trending Topics:**
[List top 3-5 trending topics/keywords with brief context — combining both competitor and niche-wide data]

**Transcript Patterns:**
[2-3 bullet points on key patterns: dominant hooks, content structures, engagement drivers]

**Top Opportunities:**
[List top 3-5 opportunities with scores and one-line rationale]

**[Validation mode only] Your Idea Assessment:**
[2-3 bullet points: competition density, positioning, key risks/advantages]

---"

### 2. Gather User Steering

Ask the user:

"**Three questions to shape the final report:**

1. **Any of these opportunities jump out?** Which topics or gaps are most interesting to you?

2. **Anything to deprioritise?** Topics or findings that aren't relevant to your current focus?

3. **Anything to dig deeper on?** Want me to expand on any particular finding in the final report?"

**Wait for user response.**

### 3. Process Feedback

Based on user input:

1. **Note priority topics** — these get expanded coverage in the final report
2. **Note deprioritised areas** — these get summarised briefly or omitted
3. **Note deep-dive requests** — these get additional analysis in the final report
4. **If user has no specific steering** — proceed with balanced coverage

Store the steering decisions in the output frontmatter:
- `priority_topics`: [list]
- `deprioritised`: [list]
- `deep_dive_requests`: [list]

Update frontmatter: append `'step-05-checkpoint'` to `stepsCompleted`.

### 4. Present MENU OPTIONS

Display: **Select an Option:** [C] Continue to Final Report

#### Menu Handling Logic:

- IF C: Update output frontmatter with steering decisions and stepsCompleted, then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Findings presented concisely and scannably
- User feedback gathered on priorities, deprioritisation, and deep-dives
- Steering decisions stored in output frontmatter
- User explicitly confirms readiness to proceed
- Frontmatter updated with step completion

### ❌ SYSTEM FAILURE:

- Presenting raw data instead of synthesised summaries
- Proceeding to report compilation without user input
- Not asking about priorities and emphasis
- Generating the final report in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
