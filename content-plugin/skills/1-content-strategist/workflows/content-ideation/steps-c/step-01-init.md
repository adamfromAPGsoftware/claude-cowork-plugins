---
name: 'step-01-init'
description: 'Initialize workflow, load brand/ICP context from sidecar, check for existing footage/transcript, discover research report, accept topic direction'

nextStepFile: './step-02-generate.md'
transcriptStepFile: './step-01b-transcript.md'
outputFile: '{output_folder}/content-concept-{concept_slug}-{date}.md'
templateFile: '../templates/concept-brief.md'
---

# Step 1: Load Context

## STEP GOAL:

To initialize the content ideation workflow by auto-loading brand guidelines and ICP profile from sidecar, checking whether the user has already filmed a video (transcript path), discovering any available competitive research reports, and accepting a topic direction from the user if no research is available.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Content Strategist guiding the user through content ideation
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You bring expertise in audience targeting, platform strategy, and content formats
- ✅ The user brings brand knowledge and creative direction

### Step-Specific Rules:

- 🎯 Focus only on loading and confirming context — do NOT generate ideas yet
- 🚫 FORBIDDEN to brainstorm or suggest content ideas in this step
- 💬 Present loaded context clearly so the user can confirm before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Create output document from {templateFile} once context is confirmed
- 📖 Update frontmatter with loaded context details
- 🚫 FORBIDDEN to proceed to idea generation without confirmed context

## CONTEXT BOUNDARIES:

- Available: Module config, sidecar files (brand guidelines, ICP profile)
- Focus: Loading and confirming all input context
- Limits: Do not generate ideas or evaluate content in this step
- Dependencies: None — this is the first step

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Welcome and Explain

"**Welcome to Content Ideation!**

I'll guide you through developing a content concept informed by your brand, audience, and research. By the end, you'll have a complete concept brief with a content tree mapped across your target platforms.

Let me start by loading your context..."

### 2. Auto-Load Required Sidecar Files

Load the following from sidecar automatically:
- **Brand Guidelines** — brand voice, values, positioning, visual identity
- **ICP Profile** — target audience demographics, pain points, aspirations, preferred platforms

Present a summary of what was loaded:

"**Context Loaded:**

**Brand Guidelines:**
- [Brief summary of key brand attributes loaded]

**ICP Profile:**
- [Brief summary of key ICP attributes loaded]"

If either file is missing or cannot be loaded, inform the user:
"**Missing:** [file name] could not be loaded from sidecar. Please provide the path or paste the relevant information."

Do not proceed until both required inputs are confirmed.

### 3. Check for Existing Footage

Ask the user whether they have already filmed the main video:

"**Have you already filmed the main video for this content piece?**

- **Yes — I have a transcript/footage** → Paste or provide your transcript and we'll build the content strategy around what you've already captured
- **No — I'm starting from scratch** → We'll develop the concept first, then plan the shoot

**Your answer:**"

Wait for user input.

**If user has existing footage/transcript:**
- Accept the transcript (pasted directly or as a file path)
- Store it as `{transcript}` in session context
- Set `has_transcript: true` in session context
- Note: the primary concept is already defined by the footage — ideation will focus on maximising platform value from existing material
- The workflow will route through {transcriptStepFile} after step-01 to analyse the transcript before idea generation

**If user is starting from scratch:**
- Set `has_transcript: false` in session context
- Continue to step 3 (research discovery) as normal

---

### 4. Discover Competitive Research Report

Search for any available competitive research reports. If found:

"**Research Report Found:**
- [Report name/path]

Would you like to use this research to inform our ideation? [Y/N]"

If no research report is found:

"**No competitive research report found.** That's fine — we can work from a topic direction instead.

**What topic or content direction would you like to explore?**

This could be:
- A specific subject area or theme
- A trend you've noticed in your industry
- A gap in your current content
- A question your audience frequently asks

**Your topic:**"

Wait for user input.

### 5. Optional Inputs

Check sidecar for optional inputs and present if available:

"**Additional Context (from sidecar):**
- **Platform Priorities:** [loaded priorities, or 'Not set — all platforms will be considered equally']
- **Content Format Preferences:** [loaded preferences, or 'Not set — all formats will be considered']"

### 6. Confirm Context Summary

Present the complete context summary for user approval:

"**Context Summary:**

| Input | Status |
|-------|--------|
| Brand Guidelines | ✅ Loaded |
| ICP Profile | ✅ Loaded |
| Research Report | [✅ Loaded / ❌ Not available] |
| Existing Footage | [✅ Transcript provided / ❌ Starting from scratch] |
| Topic Direction | [User's topic, if provided] |
| Platform Priorities | [Loaded / Default] |
| Format Preferences | [Loaded / Default] |

**Does this look correct? Ready to proceed?**"

### 7. Present MENU OPTIONS

Display: "**Select:** [C] Continue"

#### Menu Handling Logic:

- IF C AND has_transcript is true: Create {outputFile} from {templateFile}, populate frontmatter with context details (date, user_name, project_name, concept_slug, has_transcript: true), update stepsCompleted to ['step-01-init'], then load, read entire file, then execute {transcriptStepFile}
- IF C AND has_transcript is false: Create {outputFile} from {templateFile}, populate frontmatter with context details (date, user_name, project_name, concept_slug, has_transcript: false), update stepsCompleted to ['step-01-init'], then load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then [Redisplay Menu Options](#7-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- Route to {transcriptStepFile} when has_transcript is true, {nextStepFile} when false

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the output file has been created from the template with context details populated in frontmatter, will you then load and read fully the appropriate next step file — {transcriptStepFile} if transcript was provided, {nextStepFile} if starting from scratch.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Brand guidelines loaded from sidecar
- ICP profile loaded from sidecar
- Existing footage check completed — user answered and transcript stored if provided
- Research report discovered and offered (or topic direction gathered)
- Optional inputs checked and presented
- Complete context summary confirmed by user (including footage status)
- Output document created from template with frontmatter populated (including has_transcript flag)
- Correct next step routed based on has_transcript flag

### ❌ SYSTEM FAILURE:

- Proceeding without both brand guidelines and ICP profile
- Generating content ideas in this step
- Not presenting context summary for confirmation
- Not creating output document before loading next step
- Skipping research report discovery

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
