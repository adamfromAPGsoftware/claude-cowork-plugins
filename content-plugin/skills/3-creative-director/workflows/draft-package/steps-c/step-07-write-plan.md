---
name: 'step-07-write-plan'
description: 'Compile everything into package-plan.md — titles, prompts, compositions, CTR pre-scores, YouTube description, and generation config'

packagePlanTemplate: '../data/package-plan-template.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 7: Write Package Plan

## STEP GOAL:

To compile all outputs from steps 02-06 into a single `package-plan.md` file — the reviewable, editable source of truth that the Visual Asset Creation thumbnail step consumes in plan-mode. This file contains titles, prompts, compositions, CTR pre-scores, YouTube description, and generation config.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a production coordinator compiling the final package plan
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring structured documentation expertise and attention to detail
- ✅ The user brings final approval on the complete package

### Step-Specific Rules:

- 🎯 Focus on compiling and writing the plan file — not on generating images
- 🚫 FORBIDDEN to execute any generation scripts
- 💬 Present the complete plan for user review before writing
- 📋 The plan must be comprehensive enough for the thumbnail generation step to run in plan-mode without any additional input

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Package Plan Template

Load and read {packagePlanTemplate} completely.

### 2. Draft YouTube Description

Before writing the plan, draft the YouTube description that accompanies the chosen title:

**Source timestamps from the storyboard (DO NOT invent):**

1. **Primary — storyboard.json:** load `{project_folder}/{project-slug}/video-editor/storyboard/storyboard.json`.
   - Chapter titles: `chapter_cards[].title` (use `.subtitle` as the brief descriptor after an em dash)
   - Chapter times: `chapter_cards[].trigger_seconds` — these are relative to the **body** video
   - **Final-video offset:** add `durations.intro_seconds + durations.transition_seconds` to every body-relative chapter time (e.g. 73.3 + 1.0 = 74.3s offset). The first chapter card at body 0.0s becomes `(0 + 74.3)` = 1:14. ALWAYS compute this offset from the storyboard's own `durations` block — never hardcode.
   - Prepend a `0:00 — Hook` chapter that covers the intro segment (use `intro_segments[0].name` or the intro hook content)
   - Format as `M:SS` (pad seconds to 2 digits; truncate fractional seconds)

2. **Fallback — script sections:** if storyboard.json is missing, load `{project_folder}/{project-slug}/copywriter/scripts/*.md` and extract section headers with their timecodes.

3. **Last resort — transcript:** parse topic transitions from `video-editor/clips/body/transcript.json`.

4. **None found:** omit chapters entirely, note "Timestamp Source: none".

Store which source was used as `{timestamp_source}` (storyboard | script | transcript | none). Include this as a `**Timestamp Source:**` line directly above the description code block in the plan.

"**YouTube Description Draft:**

I've drafted a description using the selected keywords, the winning title, and timestamps sourced from the {timestamp_source}. The description follows this structure:
- Hook line (first 2 lines visible before 'Show more')
- Value proposition / what the viewer will learn
- Chapter markers (real section names + computed final-video timestamps, first chapter at 0:00)
- Relevant links
- SEO tags from keyword research

---
{draft description}
---

**Edit or approve this description.**"

Wait for user input. Once approved, proceed to section 2c.

### 2b. AUTO MODE — YouTube Description with Timestamps

**Only execute this section if `{workflow_mode}` is `auto`. Skip entirely in collab mode (use section 2 above instead).**

Draft the YouTube description autonomously with chapter timestamps and tool links.

**Timestamp extraction priority (same as collab mode — see section 2):**
1. **Storyboard** (primary): load `{project_folder}/{project-slug}/video-editor/storyboard/storyboard.json`, read `chapter_cards[]` for titles/subtitles/trigger_seconds, and add the final-video offset (`durations.intro_seconds + durations.transition_seconds`) to every body-relative `trigger_seconds` value. Prepend a `0:00 — Hook` chapter for the intro. Format as `M:SS`.
2. **Script sections** (fallback): load `{project_folder}/{project-slug}/copywriter/scripts/*.md`, parse section headers with timecodes
3. **Transcript** (last resort): identify topic transitions from `video-editor/clips/body/transcript.json`
4. **None found**: omit chapters, note "Timestamp Source: none"

Store which source was used as `{timestamp_source}` (storyboard | script | transcript | none).

**Auto description structure (kept short, with tool links):**
```
{Hook line — rephrased value statement from winning angle}

{1-2 sentence value proposition}

Chapters:
0:00 - {section name}
{MM:SS} - {section name}
...

Tools & Links:
{tool/brand name} - {URL}
...

{SEO tags from keyword research}
```

**Tool links:** Extract tools/brands mentioned in the content (script, content brief, transcript). For each, include a link if a URL is known or can be derived from the content. Keep it to the tools actually featured in the video — don't pad with unrelated links.

Log the description for audit trail but do NOT wait for user input. Auto-proceed to section 2c.

### 2c. Draft Skool Classroom Lesson

Draft a Skool classroom title and description for the lesson page.

**Skool title:** Rephrase the winning YouTube title to feel more course/community-oriented.
- Shorter is fine (no character limit pressure)
- Drop SEO keywords if they make it feel unnatural
- Frame it as a lesson the viewer is about to learn

**Skool description format:**
- Hook line (1-2 sentences, community tone)
- Emoji-led sections with → sub-bullets for tools, steps, or takeaways
- Bold section headers (e.g. **The 3 Skills to Dabble In**, **4-Step Strategy**)
- Key links section: tools/brands featured in the video + any community links (e.g. community URL)
- No timestamps
- ~300–400 words max, heavy white space, scannable on mobile

**Source:** Pull key points, tools, and structure from the content brief, script, or storyboard.

**COLLAB MODE:** Present draft and wait for user approval before proceeding to section 3.

**AUTO MODE:** Generate autonomously and log for audit trail. Proceed to section 3 immediately.

### 3. Compile Package Plan

Using the template from {packagePlanTemplate}, compile the complete plan with all data from previous steps:

**Data sources:**
- **Step 02** — Selected angles with hooks, expressions, visual direction
- **Step 03** — Selected keywords, keyword research results
- **Step 04** — Final title/text overlay combos
- **Step 05** — Composition tables, expression directions, full Gemini prompts
- **Step 06** — CTR pre-validation scores per combo

**Generation config section must include:**
- Reference photos folder path and file list
- Inspiration thumbnails path (if available)
- Output path pattern: `{project_folder}/{project-slug}/creative-director/thumbnails/generated/`
- Sequential execution (never parallel)
- Maximum 5 combos per batch

### 4. Present Plan for Review

Present the complete compiled plan:

"**Package Plan — Final Review:**

{complete plan content}

**This plan will be saved to:**
`{project_folder}/{project-slug}/creative-director/thumbnails/package-plan.md`

**Review the complete plan.** You can:
- Edit any section (titles, prompts, compositions, description)
- Reorder combos by priority
- Remove a combo
- Type `write` to save the plan"

Wait for user review and approval.

**AUTO MODE:** Output the plan for audit trail, then write immediately — do not wait for user review or the `write` command.

### 5. Write the Plan File

When user types `write` or approves (or immediately in auto mode):

Write the package-plan.md file to:
`{project_folder}/{project-slug}/creative-director/thumbnails/package-plan.md`

Confirm:

"**Package plan written!**

📄 **File:** `{project_folder}/{project-slug}/creative-director/thumbnails/package-plan.md`
📊 **Combos:** {count}
🎯 **Average CTR Pre-Score:** {average}/7

**Next Steps:**
- Run **[VA] Visual Assets → [TH] Thumbnail** to generate from this plan (plan-mode auto-detected)
- Or edit the plan file directly and regenerate
- The plan is your source of truth — any manual edits will be honoured during generation

**Draft Package complete.**"

### 6. Present MENU OPTIONS

**Collab mode:**

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [D] Done

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF D: End workflow session
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- Workflow ends when user selects 'D'

**AUTO MODE — Chain to Thumbnail Generation:**

Skip the menu entirely. Chain directly to thumbnail generation:

1. Load `{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/steps-c/step-03-thumbnail.md`
2. The step has plan-mode detection (section 0) that will auto-load the package-plan.md just written
3. Pass `{workflow_mode}` = `auto` forward — the thumbnail step's auto-mode blocks will handle skipping user gates:
   - Skip the [G]/[R]/[S]/[X] file check menu → auto-select [G] Generate all (or generate missing only if some exist)
   - Skip section 6 pre-execution menu → auto-proceed to generation
   - Execute section 7 (generate thumbnails) sequentially for all combos using exact prompts from the plan
   - Execute section 8 (CTR validation) comparing pre-scores to post-scores
   - Skip section 9 completion menu → output final summary and end

"**Auto mode — chaining to thumbnail generation...**"

## CRITICAL STEP COMPLETION NOTE

In **collab mode**, this is the final step of the Draft Package workflow. The workflow is complete when the package-plan.md file is written and the user acknowledges completion.

In **auto mode**, this step chains directly to thumbnail generation. The workflow is complete when all thumbnails are generated and CTR-validated.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Template loaded
- YouTube description drafted and approved
- All step outputs compiled into a single plan
- Generation config is complete (paths, photo list, output pattern)
- Plan presented for user review
- Plan file written to correct project location
- User informed of next steps (VA → TH for plan-mode generation)

### ❌ SYSTEM FAILURE:

- Missing any data from previous steps in the plan
- Writing plan without user review
- Incomplete generation config (missing paths or photo list)
- Executing generation scripts in this step
- Writing plan to wrong location
- Not informing user that VA → TH will auto-detect the plan

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
