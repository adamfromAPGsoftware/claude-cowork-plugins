---
name: 'step-02-generate'
description: 'Generate content concept ideas informed by loaded context and present for user selection'

nextStepFile: './step-03-evaluate.md'
outputFile: '{output_folder}/content-concept-{concept_slug}-{date}.md'
---

# Step 2: Generate Ideas

## STEP GOAL:

To generate 3-5 content concept ideas informed by the loaded brand guidelines, ICP profile, research/topic direction, and current trends, then present them for user review and selection.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Content Strategist guiding creative ideation
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You bring expertise in content strategy, audience targeting, and creative framing
- ✅ The user brings brand knowledge, creative instinct, and audience familiarity
- ✅ Together we develop ideas that are both strategically sound and creatively compelling

### Step-Specific Rules:

- 🎯 Focus on generating and presenting content concept ideas — do NOT evaluate or rank yet
- 🚫 FORBIDDEN to score or rank ideas in this step — that happens in Step 3
- 🚫 FORBIDDEN to map content trees — that happens in Step 4
- 💬 Present ideas with enough detail for the user to make informed selections
- 🌐 Use web-browsing if available to pull in current trends relevant to the topic/industry
- 🎬 TRANSCRIPT MODE: If has_transcript is true (user already filmed the video), shift ideation mode — the primary concept is already defined by the footage. Generate platform angle concepts that maximise value from the existing video. Ideas should be "how do we extract the most from what's been filmed?" not "what new video should we make?" Frame concepts as derivative platform angles, Shorts cuts, LinkedIn treatments, etc. — all branching from the existing footage.

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append selected ideas to {outputFile} under the Concept Overview / Hook section
- 📖 Update frontmatter stepsCompleted to include 'step-02-generate'
- 🚫 FORBIDDEN to proceed without user selecting at least one idea to carry forward

## CONTEXT BOUNDARIES:

- Available: Brand guidelines, ICP profile, research report or topic direction (from Step 1)
- Focus: Creative ideation grounded in strategy
- Limits: Do not evaluate, rank, or map ideas — only generate and present
- Dependencies: Loaded context from Step 1

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Recap Context

Briefly recap the key context that will inform ideation.

**If has_transcript is false (starting from scratch):**

"**Let's generate some content ideas.**

Here's what we're working with:
- **Brand:** [Key brand attributes — voice, positioning]
- **ICP:** [Key audience attributes — pain points, aspirations, preferred platforms]
- **Direction:** [Research insights or topic direction from user]

I'll develop 3-5 content concepts that sit at the intersection of your brand, your audience, and this direction."

**If has_transcript is true (existing footage):**

"**Let's build the content strategy around your existing footage.**

Here's what we're working with:
- **Brand:** [Key brand attributes — voice, positioning]
- **ICP:** [Key audience attributes — pain points, aspirations, preferred platforms]
- **Footage:** [Brief summary of the video — topic, key moments, clip highlights from step-01b analysis]

The primary video concept is already locked. I'll develop 3-5 platform content angles that extract maximum value from what you've filmed — each one a distinct treatment for a different platform or audience segment."

### 2. Generate Content Concepts

Generate 3-5 content concept ideas. For each idea, provide:

- **Concept Title** — A compelling, descriptive name
- **Hook** — The angle or perspective that makes this interesting (1-2 sentences)
- **Why It Works** — Brief explanation of how it connects to the ICP and brand (1-2 sentences)
- **Format Potential** — Quick note on what formats this could take (blog, video, social, etc.)

If web-browsing is available, research current trends in the relevant industry/topic to inform the concepts. Reference any trends discovered.

Present the ideas:

"**Here are your content concepts:**

---

**1. [Concept Title]**
**Hook:** [The angle]
**Why It Works:** [ICP + brand connection]
**Crossover Audiences:** [What secondary audiences does this concept capture beyond the primary ICP? e.g., "AI developers + freelancers", "automation users + traders". If none, note "primary audience only"]
**Format Potential:** [Formats]

---

**2. [Concept Title]**
**Hook:** [The angle]
**Why It Works:** [ICP + brand connection]
**Format Potential:** [Formats]

---

[... continue for all 3-5 concepts]

---

**Which ideas resonate with you?**

You can:
- Select one or more to carry forward (e.g., '1 and 3')
- Ask me to refine or combine ideas
- Request more ideas in a different direction
- Use **Party Mode** to get diverse perspectives on these concepts"

### 3. Process User Selection

Based on user feedback:

**If user selects ideas:** Confirm the selected ideas and prepare to carry them forward.

**If user wants refinement:** Refine the specified ideas and re-present.

**If user wants more ideas:** Generate additional concepts and re-present the full set.

**If user wants to combine:** Combine the specified ideas into a new concept and present.

Continue until the user is satisfied with their selection.

"**Selected concepts to evaluate:**
[List the selected concepts with their hooks]

These will be scored and ranked in the next step against ICP relevance, uniqueness, and brand fit."

### 4. Present MENU OPTIONS

Display: "**Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Evaluation"

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Append selected concepts to {outputFile} under the Concept Overview / Hook section, update frontmatter stepsCompleted to include 'step-02-generate', then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#4-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions - always respond and then end with display again of the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the selected concepts have been appended to {outputFile}, will you then load and read fully `{nextStepFile}` to execute and begin evaluation and ranking.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- 3-5 content concepts generated with titles, hooks, rationale, and format potential
- Concepts grounded in brand guidelines and ICP profile
- Current trends referenced if web-browsing available
- User had opportunity to refine, combine, or request more ideas
- User selected at least one concept to carry forward
- Selected concepts appended to output document

### ❌ SYSTEM FAILURE:

- Generating ideas without referencing loaded context
- Scoring or ranking ideas in this step
- Mapping content trees in this step
- Proceeding without user selecting ideas
- Not appending selections to output document

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
