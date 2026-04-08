---
name: 'step-01-init'
description: 'Receive source mode, select post format, and load context for X content generation'

nextStepFile: './step-02-hooks.md'
writingRulesData: '../data/writing-rules.md'
---

# Step 1: Initialize

## STEP GOAL:

To establish the content source (project-based or personal), select the X post format, and load all context needed for content generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are an X content strategist and platform specialist
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring X algorithm expertise and format-specific knowledge, user brings their content and audience context

### Step-Specific Rules:

- 🎯 Focus only on source mode, format selection, and context loading
- 🚫 FORBIDDEN to generate hooks or content in this step
- 💬 Present format options clearly with character limits and performance context
- 📋 Video and Long Post formats are project-based only — if personal mode, do not offer these

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Store source mode and format selection as session variables
- 📖 Load all required context before proceeding
- 🚫 FORBIDDEN to proceed without both source mode and format confirmed

## CONTEXT BOUNDARIES:

- This is the first step — no prior workflow state exists
- Agent context provides: ICP profiles, brand guidelines, inspiration library, creator credentials
- Workflow provides: writing rules, CTA patterns, quality checklist, hook patterns in data/
- Focus: Setup only — no content generation yet

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Source Mode Selection

Ask the user which content source mode to use:

"**How are we sourcing this X post?**

**[P] Project-based** — pull from an existing project's content brief and assets
**[C] Custom / Personal** — standalone content, provide the topic directly"

**If Project-based:**
- Set `{source_mode}` = `project`
- Validate that an active project is set and content brief exists
- If content brief doesn't exist, halt and tell user to run the scan project command first

**If Custom / Personal:**
- Set `{source_mode}` = `personal`
- Ask user: "What's the topic or angle for this post?" — get a brief description
- Store as `{personal_topic}`

### 2. Format Selection

Present format options with character limits and performance context:

"**What format are we creating?**

**[S] Single post** — ≤280 chars. Best for: hot takes, bold claims, punchy opinions, quick insights
**[T] Thread** — 2–20 tweets, 280 chars each (sweet spot: 5–12). Best for: breakdowns, how-tos, story threads. Equivalent to LinkedIn carousel for depth
**[L] Long post** — ≤25,000 chars (X Premium+ only). Best for: deep dives, article-style essays, comprehensive guides
**[I] Image post** — caption + single image. Best for: data points, architecture diagrams, screenshots with commentary
**[V] Video post** — caption + video clip. Best for: demos, build processes, result reveals"

**If source_mode is personal:** Do not present Long Post or Video options — inform user these require project assets.

Store selected format as `{post_format}`.

### 3. Load Context

**Load format-specific writing rules:**
- Load `{writingRulesData}` to understand format constraints

**Project-based mode — load:**
- Content brief from project folder
- Lead magnet information (if exists)
- Media asset inventory (for image/video formats)
- Check derivative tracking in memories for angle duplication

**Personal mode — load:**
- Reference brand guidelines for voice
- Check derivative tracking in memories for angle duplication
- Use `{personal_topic}` as the content source

### 4. Context Summary

Present a brief summary of loaded context:

"**Context loaded. Ready to create a {post_format} post.**

**Source:** {project name or personal topic}
**Format:** {format with key constraint — e.g., '≤280 chars' or '5–12 tweets' or '≤25,000 chars'}
**ICP targets:** {relevant ICPs}
**Existing posts:** {count of existing posts for this project/topic, if any — flag potential duplication}"

### 5. Proceed to Hook Ideation

Display: "**Proceeding to hook ideation...**"

#### Menu Handling Logic:

- After context is loaded and summary confirmed, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an init step with auto-proceed after setup
- Proceed directly to next step after context loading

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN source mode and format are confirmed and all context is loaded will you load and read fully `{nextStepFile}` to execute hook ideation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Source mode selected (project or personal)
- Format selected (single, thread, long post, image, or video)
- Long Post and Video gated to project-mode only
- All relevant context loaded (writing rules, content brief/topic, derivative tracking)
- Context summary presented to user
- Ready to proceed to hook ideation

### ❌ SYSTEM FAILURE:

- Generating hooks or content in this step
- Offering Long Post or Video format in personal mode
- Proceeding without confirmed source mode and format
- Not loading writing rules or context
- Skipping derivative tracking check

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
