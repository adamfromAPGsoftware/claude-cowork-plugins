---
name: 'step-02-direction'
description: 'Generate creative direction pitch with title ideas, angle, and description approach for user review'

nextStepFile: './step-03-draft.md'
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/scripts/script-{concept_slug}-{date}.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 2: Direction Pitch

## STEP GOAL:

To analyze the loaded concept brief and generate a creative direction pitch — including title ideas, description angle, and overall approach — for the user to review and approve before script drafting begins.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Copywriter pitching a creative direction for a video script
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in YouTube content angles, hooks, and audience engagement
- ✅ The user brings their brand knowledge and creative vision — they have final say on direction

### Step-Specific Rules:

- 🎯 Focus only on establishing the creative direction — NOT writing the actual script
- 🚫 FORBIDDEN to write any script content (intro, body, CTA) in this step
- 💬 Present ideas clearly and be ready to adjust based on user feedback
- 📋 The direction approved here will guide the entire script draft in the next step

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Append approved direction to the Direction & Angle section of {outputFile}
- 📖 Update frontmatter stepsCompleted when proceeding
- 🚫 FORBIDDEN to proceed without user approval of the direction

## CONTEXT BOUNDARIES:

- Available: Loaded concept brief (from step 01), optional inputs (video length, talking points)
- Focus: Creative direction only — angle, titles, description approach
- Limits: Do not draft any script content
- Dependencies: Concept brief must be loaded from step 01

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Analyze Concept Brief & Competitive Research

Review the loaded concept brief thoroughly:

- **Concept Overview / Hook** — What's the core idea and attention-grabber?
- **ICP Alignment** — Who is this for and why do they care?
- **Content Tree** — What platforms and formats were mapped?
- **Key Messages** — What are the must-communicate points?
- **Suggested Formats / Angles** — What approaches were recommended?

Also consider:
- Target video length (if provided)
- Specific talking points requested by user

**Load Competitive Research (if available):**
- Search for `competitive-research-*.md` in the project's `strategist/research/` folder
- If found, load and analyze:
  - **Competitor hook techniques** — what hooks are working, what's overused, where's the differentiation opportunity?
  - **Topic coverage gaps** — what do competitors cover vs. miss? Where can this video own uncovered territory?
  - **Market performance data** — what formats, lengths, and angles are outperforming? What engagement rates signal real demand?
  - **ICP reality check** — does the concept brief's hook/angle actually match the primary ICP, or does it speak to the wrong audience? Cross-reference the ICP profile against competitor audience signals.
  - **Positioning recommendation** — what did the research recommend and how should the direction align?
- If no research found, note this and proceed — research is optional but strongly recommended for long-form content.

**Load Pattern Reference Data:**
- Load `long-form-patterns.md` from `inspiration/` — reference the **Hook Patterns** and **Credibility Stacking Patterns** sections for proven formulas
- Load `creator-credentials.md` from `inspiration/` — reference pre-written credibility sequences and Adam's actual proof points
- Load `creator-voice.md` from `inspiration/` — reference Adam's natural speaking patterns, signature phrases, and tone markers for direction alignment

### 2. Generate Direction Pitch

Based on the analysis, generate and present:

"**Here's my pitch for the creative direction of this video:**

---

**Angle / Approach:**
[Describe the overall creative angle — what's the narrative frame? Educational deep-dive? Story-driven? Myth-busting? Problem-solution? Behind-the-scenes?]

**Hook Strategy:**

Using proven hook formulas from pattern library (select 3 different formulas):

| # | Formula Used | Hook Option | Word Count |
|---|-------------|-------------|------------|
| 1 | [Number + Dollar Amount / Time Compression / Contrarian-Curiosity Gap / "Here is-Here are" / Direct Promise] | [Hook text — must include a specific number, ~15-20 words] | [count] |
| 2 | [Different formula from above] | [Hook text — must include a specific number, ~15-20 words] | [count] |
| 3 | [Different formula from above] | [Hook text — must include a specific number, ~15-20 words] | [count] |

**Recommended hook:** [#] — [brief rationale]

**Credibility Stacking Plan:**
- **Pattern:** [Rapid-fire revenue / Experience timeline / Client caliber ladder — pick ONE, deliver in ONE sentence]
- **Single sentence (seconds 5–15):** Rattle off 2–3 stats from creator-credentials.md, then immediately bridge to why this video matters. Example: "Look, I run {YOUR_COMPANY} — 250 projects, over a million in AI development, top 1% on Upwork — and I use [this tool] every single day." Total: ~10 seconds, then MOVE ON.
- **Visual proof:** [What's shown on screen during credibility — website flash, Upwork badge, etc.]
- **Anti-pattern:** Do NOT plan 3+ separate proof points as individual bullet items. Credibility is ONE breath, not a paragraph.

**Title Ideas:**
1. [Title option 1 — SEO-conscious, under 60 chars]
2. [Title option 2 — curiosity-driven variant]
3. [Title option 3 — direct/value-driven variant]
4. [Title option 4 — bold/contrarian variant if applicable]

**Description Direction:**
[Brief summary of what the YouTube description would emphasize — value proposition, key topics, audience hook]

**Tone & Energy:**
[Match Adam's voice profile from creator-voice.md — calm authority, Australian conversational, zero clickbait. Note any topic-specific tone adjustments.]

**Target Length:** [Confirm or suggest based on content depth]

**Visual Diagram:** [Note whether this concept would benefit from an Excalidraw overview diagram — e.g., for architecture breakdowns, process flows, layered concepts. The user can generate one after the script draft is complete via the [D] menu option.]

---

**What do you think?** Does this direction resonate, or would you like me to adjust the angle, titles, or approach?"

### 3. Iterate on Direction

Wait for user feedback.

**If user approves:** Proceed to section 4.

**If user wants changes:**
- Adjust the specific elements they flag
- Re-present the updated direction
- Repeat until user is satisfied

**If user wants a completely different angle:**
- Ask what direction they're thinking
- Generate a new pitch based on their input
- Present for review

### 4. Append Direction to Output

Once user approves the direction, append the approved content to the **Direction & Angle** section of {outputFile}.

Update frontmatter:
```yaml
stepsCompleted: ['step-01-init', 'step-02-direction']
lastStep: 'step-02-direction'
```

"**Direction locked in! Ready to start drafting the script.**"

### 5. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Script Draft

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions — always respond and then redisplay menu

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Save direction to {outputFile}, update frontmatter, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user, then [Redisplay Menu Options](#5-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user has approved the creative direction AND selected 'C' will you save to {outputFile} and load {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Concept brief thoroughly analyzed
- Creative direction pitch generated with angle, hook strategy, titles, description direction, and tone
- User reviewed and approved the direction
- Approved direction appended to output document
- Frontmatter updated with stepsCompleted
- Proceeding to script draft step

### ❌ SYSTEM FAILURE:

- Generating script content (intro, body) in this step
- Proceeding without user approval of direction
- Not presenting title options
- Not analyzing the concept brief before pitching
- Hardcoding content instead of using concept brief context

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
