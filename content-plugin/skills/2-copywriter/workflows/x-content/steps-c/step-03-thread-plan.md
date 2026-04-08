---
name: 'step-03-thread-plan'
description: 'Plan the thread structure: tweet count, tweet-by-tweet outline, bookmark and CTA placement'

nextStepFile: './step-04-content.md'
writingRulesData: '../data/writing-rules.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 3: Thread Plan

## STEP GOAL:

To build a tweet-by-tweet thread outline before writing content — establishing tweet count, key point per tweet, bookmark hook placement, and CTA tweet position.

## AUTO-SKIP RULE:

⚠️ **This step applies to THREAD format ONLY.**

If `{post_format}` is **Single**, **Long Post**, **Image**, or **Video** — this step should NOT have been loaded. If it was loaded in error, immediately load and execute `./step-04-content.md`.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are an X thread architect — you understand how to structure multi-tweet narratives
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring thread structure expertise and reader retention knowledge, user brings the content and insights

### Step-Specific Rules:

- 🎯 Focus only on thread structure — no content writing yet
- 🚫 FORBIDDEN to write the full tweet text in this step
- 💬 Each tweet outline is one key point or idea — not full prose
- 📋 Sweet spot: 5–12 tweets. Flag if outside this range.

## EXECUTION PROTOCOLS:

- 🎯 Load writing rules before building the outline
- 💾 Store thread plan as session variable for step-04
- 📖 Reference hook patterns for thread-specific guidance
- 🚫 FORBIDDEN to proceed without a confirmed thread outline

## CONTEXT BOUNDARIES:

- Source mode, format (Thread), content context, selected hook, and content category are loaded from previous steps
- Writing rules provide thread-specific constraints
- Focus: Outline only — actual tweet writing happens in step-04

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Writing Rules

Load `{writingRulesData}` — focus on the Thread section for constraints and structure guidance.

### 2. Suggest Tweet Count

Based on the content context and selected hook, recommend a tweet count:

"**Thread size for this content:**

My recommendation: **[N] tweets** — [brief reason, e.g., '3 key steps each deserve a tweet, plus hook and CTA']

This fits within the sweet spot (5–12 tweets) for maximum engagement without reader fatigue.

**[A] Accept this count**
**[C] Choose a different count** — tell me how many tweets you want (2–20)"

Store confirmed count as `{thread_tweet_count}`.

### 3. Build Tweet-by-Tweet Outline

Draft a tweet-by-tweet outline. For each tweet, specify:
- Tweet number
- Key point or purpose (not the full text — just the idea)
- Special role: hook, bookmark prompt, CTA, story beat, numbered step

"**Proposed thread outline:**

Tweet 1 (Hook): {selected_hook} + thread signal 🧵
Tweet 2 (Bookmark prompt + first insight): Save this. [Key point 1]
Tweet 3: [Key point 2]
...
Tweet {N-1}: [Key point N]
Tweet {N} (CTA): Summary + follow hook + RT/bookmark prompt

Does this structure work? Any tweets to add, remove, or reorder?"

Wait for user feedback and adjust the outline until confirmed.

Store confirmed outline as `{thread_outline}`.

### 4. Determine Bookmark Hook Placement

If not already in the outline, confirm where the bookmark hook goes:

"**Bookmark hook placement:**

Bookmark hooks ('Save this thread. You'll need it.') work best in tweet 1 or tweet 2 — before readers scroll past.

**Current placement:** {placement from outline or 'not yet placed'}

Confirm or adjust?"

Update `{thread_outline}` with confirmed bookmark hook placement.

### 5. Confirm CTA Tweet Position

Verify the final tweet is the CTA tweet:

"**CTA tweet:** Tweet {N} — {CTA summary from outline}

This will include:
- 1-line thread summary or punchline
- Follow hook: 'Follow @[handle] for more [topic]'
- RT or bookmark prompt

Confirmed? Or adjust the CTA approach?"

Wait for confirmation. Update `{thread_outline}` if needed.

### 6. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Content Generation

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions - always respond and then end with display again of the menu options

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Confirm thread outline, then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN thread outline is confirmed and user selects 'C' will you load and read fully `{nextStepFile}` to execute content generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Tweet count confirmed within 2–20 range (5–12 preferred)
- Tweet-by-tweet outline created with one key point per tweet
- Each tweet's role identified (hook, insight, bookmark, CTA)
- Bookmark hook placed in tweet 1 or 2
- Final tweet designated as CTA tweet
- User confirmed the outline before proceeding
- Thread outline stored for step-04

### ❌ SYSTEM FAILURE:

- Building outline for a non-thread format
- Writing full tweet text in this step
- Outline with multiple ideas per tweet
- No bookmark hook in the outline
- No CTA tweet at the end
- Proceeding without user confirmation of the outline

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
