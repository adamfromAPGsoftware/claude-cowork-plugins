---
name: 'step-01-init'
description: 'Receive source mode, select post format, and load context for LinkedIn content generation'

nextStepFile: './step-02-hooks.md'
writingRulesData: '../data/writing-rules.md'
---

# Step 1: Initialize

## STEP GOAL:

To establish the content source (project-based or personal), select the LinkedIn post format, and load all context needed for content generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a LinkedIn content strategist and distribution specialist
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring LinkedIn algorithm expertise and format-specific knowledge, user brings their content and audience context

### Step-Specific Rules:

- 🎯 Focus only on source mode, format selection, and context loading
- 🚫 FORBIDDEN to generate hooks or content in this step
- 💬 Present format options clearly with performance context
- 📋 Video format is project-based only — if personal mode, do not offer video

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

### 0. Load Voice Library (before anything else)

Load `{project-root}/references/brand-voice.md` immediately. Apply the Written Content Adaptations and Anti-AI Red Flags sections to all LinkedIn drafts generated in this workflow. Run anti-AI scan before presenting any output to the user.

### 1. Source Mode Selection

Ask the user which content source mode to use:

"**How are we sourcing this LinkedIn post?**

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

Present format options with performance context:

"**What format are we creating?**

**[T] Text post** — pure copy, no media. Best for: thought leadership, hot takes, personal stories
**[I] Image post** — text + single image (1080x1080). Best for: data points, bold statements, architecture diagrams
**[C] Carousel** — text + multi-slide PDF (5-12 slides). Best for: step-by-step breakdowns, listicles. Highest engagement — 1.6x reach vs text
**[V] Video post** — text + short clip (15-30s). Best for: demos, build processes, showing results"

**If source_mode is personal:** Do not present Video option — inform user video requires project assets.

Store selected format as `{post_format}`.

### 3. Load Context

**Load format-specific writing rules:**
- Load `{writingRulesData}` to understand format constraints

**Project-based mode — load:**
- Content brief from project folder
- Lead magnet information (if exists)
- Media asset inventory (for image/carousel/video formats)
- Check derivative tracking in memories for angle duplication

**Personal mode — load:**
- Reference brand guidelines for voice
- Check derivative tracking in memories for angle duplication
- Use `{personal_topic}` as the content source

### 4. Context Summary

Present a brief summary of loaded context:

"**Context loaded. Ready to create a {post_format} post.**

**Source:** {project name or personal topic}
**Format:** {format with key constraint — e.g., '800-1300 chars' or '5-12 slides'}
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
- Format selected (text, image, carousel, or video)
- Video gated to project-mode only
- All relevant context loaded (writing rules, content brief/topic, derivative tracking)
- Context summary presented to user
- Ready to proceed to hook ideation

### ❌ SYSTEM FAILURE:

- Generating hooks or content in this step
- Offering video format in personal mode
- Proceeding without confirmed source mode and format
- Not loading writing rules or context
- Skipping derivative tracking check

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
