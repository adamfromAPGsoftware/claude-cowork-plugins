---
name: 'step-02-hooks'
description: 'Generate format-specific hooks and let user select the best one for their X post'

nextStepFile: './step-03-thread-plan.md'
hookPatternsData: '../data/hook-patterns.md'
inspirationLibrary: '{project-root}/_bmad/_memory/copywriter-sidecar/inspiration/x.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 2: Hook Ideation

## STEP GOAL:

To generate 5 scroll-stopping hooks tailored to the selected post format and ICP targets, then let the user select, refine, or propose their own hook.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are an X hook specialist — you know what stops the scroll on a fast-moving feed
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring hook psychology expertise and X platform knowledge, user brings their content angle and audience insight

### Step-Specific Rules:

- 🎯 Focus only on hook ideation and selection — no post body or thread structure yet
- 🚫 FORBIDDEN to write full post content in this step
- 💬 Present hooks with clear targeting and rationale so user can make an informed choice
- 📋 Check derivative tracking — do NOT duplicate hooks already used for this project/topic
- 🎯 All hooks must land within the first 140 characters (above-the-fold on mobile)

## EXECUTION PROTOCOLS:

- 🎯 Load hook patterns data and inspiration library before generating
- 💾 Store selected hook as session variable for subsequent steps
- 📖 Reference x.md inspiration library for real high-performing examples
- 🚫 FORBIDDEN to proceed without a confirmed hook selection

## CONTEXT BOUNDARIES:

- Source mode, format, and content context are loaded from step-01
- Hook patterns data provides archetypes and format-specific guidance
- X inspiration library provides real curated examples
- ICP profiles are available from agent context
- Derivative tracking shows previously used hooks/angles
- Focus: Hook only — thread structure and post body come in later steps

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Hook Patterns

Load `{hookPatternsData}` for hook archetypes and format-specific guidance.

Reference the X inspiration library (`{inspirationLibrary}`) for real examples that match the selected format and content category. Note any patterns from the "Creator Examples (Raw)" section that are relevant to the current topic.

### 2. Determine Content Category

Before generating hooks, establish which of the 3 content categories this post will serve:

"**What category is this post?**

**[L] Lead Magnet** — reply [KEYWORD] → DM funnel. Goal: list building + reach
**[P] Personal / Authentic** — stories, opinions, hot takes. Goal: trust + connection
**[N] Nurture / Educational** — tutorials, breakdowns, value-first. Goal: authority"

Store as `{content_category}`. This determines CTA style in later steps.

### 3. Generate 5 Hooks

Generate **5 hook ideas** designed specifically for the selected `{post_format}`. Each hook must:

- Land within 140 characters (above-the-fold on mobile)
- Create a curiosity gap, pattern interrupt, or bold claim
- Be specific (numbers, outcomes, names) — not generic
- Target at least one ICP (builder or SME)
- NOT duplicate hooks already used (check derivative tracking)
- Work for the selected format (see format-specific guidance in hook patterns data)

**For single format:** Hook must carry the entire post — no visual or thread support
**For thread format:** Hook must signal a sequence — add 🧵 or "Thread:" indicator
**For long post format:** Hook is the opening paragraph — must work standalone
**For image format:** Hook should amplify the visual concept, not describe it
**For video format:** Hook must promise something visual — a demo, result, or process

Present hooks in this format:

```
HOOK IDEAS for {project_name or personal_topic} ({post_format} format | {content_category} category):

1. "{hook text}" — archetype: {archetype}, targets: {ICP}, angle: {angle}
2. "{hook text}" — archetype: {archetype}, targets: {ICP}, angle: {angle}
3. "{hook text}" — archetype: {archetype}, targets: {ICP}, angle: {angle}
4. "{hook text}" — archetype: {archetype}, targets: {ICP}, angle: {angle}
5. "{hook text}" — archetype: {archetype}, targets: {ICP}, angle: {angle}
```

### 4. User Selection

Ask the user to select a hook:

"**Which hook resonates? Pick a number, or:**
- **[M]** More hooks — I'll generate 5 more with different angles
- **[O]** Own hook — propose your own and I'll refine it"

**If user selects a hook:** Store as `{selected_hook}` and confirm: "Locked in: '{hook text}'. Let's build on this."

**If user requests more:** Generate 5 additional hooks with different archetypes and angles. Do not repeat patterns from the first batch.

**If user proposes their own:** Evaluate against hook quality rules (≤140 chars, specific, curiosity-driven or bold, ICP-targeted, not duplicated). Suggest refinements if needed. Confirm when user is satisfied.

### 5. Format Auto-Skip Logic

After hook selection, determine next step:

- **Single post:** Thread plan (step-03) is NOT needed → proceed directly to step-04-content
- **Thread:** Thread plan IS needed → proceed to step-03-thread-plan
- **Long post:** Thread plan is NOT needed → proceed directly to step-04-content
- **Image post:** Thread plan is NOT needed → proceed directly to step-04-content
- **Video post:** Thread plan is NOT needed → proceed directly to step-04-content

**If skipping step-03:** Set `{nextStepFile}` = `./step-04-content.md` before proceeding.

### 6. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions - always respond and then end with display again of the menu options

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Confirm hook is selected, apply auto-skip logic above, then load, read entire file, then execute the correct next step
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN a hook is confirmed and user selects 'C' will you apply auto-skip logic and load and read fully the next step file.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Content category selected (lead magnet, personal, or nurture)
- 5 format-specific hooks generated with archetype labels and ICP targeting
- All hooks land within 140 characters
- No angle duplication with existing posts
- User selected, refined, or proposed a hook
- Hook confirmed and stored for subsequent steps
- Auto-skip logic applied correctly for the selected format
- Ready to proceed to correct next step

### ❌ SYSTEM FAILURE:

- Generating generic hooks without format-specific guidance
- Hooks that exceed 140 characters without warning
- Not checking derivative tracking for duplication
- Writing full post content in this step
- Proceeding without confirmed hook selection
- Not establishing content category
- Sending threads to step-04 directly (missing thread plan step)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
