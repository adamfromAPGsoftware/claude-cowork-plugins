---
name: 'step-03-images'
description: 'Batch-generate hero illustrations per segment via fal-ai MCP with review and revision loop'

nextStepFile: './step-04-compose.md'
imagePromptTemplates: '../data/image-prompt-templates.md'
diagramStandards: '../data/diagram-standards.md'
---

# Step 3: Hero Illustration Generation

## STEP GOAL:

To batch-generate one rich, detailed hero illustration per segment using fal-ai MCP, present them for review, and iterate on specific images until the user is satisfied with the full set.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR executing prescriptive image generation
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual storyboard designer generating hero illustration assets
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ This step is PRESCRIPTIVE — follow the prompt templates precisely for consistency
- ✅ You bring illustration direction expertise, user brings quality judgement

### Step-Specific Rules:

- 🎯 Focus on generating ONE hero illustration per segment from the approved storyboard plan
- 🚫 FORBIDDEN to compose the ExcaliDraw storyboard — that's step 4
- 💬 Approach: Batch-generate all, then review as a set for visual consistency
- 🎯 Use subprocess optimization (Pattern 4) for parallel image generation when available
- ⚙️ TOOL/SUBPROCESS FALLBACK: If subprocess unavailable, perform in main thread

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Save all generated images to the output images/ directory
- 📖 Use prompt templates from data/image-prompt-templates.md for consistency
- 🚫 FORBIDDEN to proceed until user approves the full image set

## CONTEXT BOUNDARIES:

- Available: Storyboard plan from step 2 (segment table with illustration prompts), output path
- Focus: Generating and refining hero illustrations only
- Limits: Do not compose the storyboard or create ExcaliDraw JSON
- Dependencies: Step 2 must have provided approved segment plan with illustration prompts

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load References and Segment Plan

Load `{imagePromptTemplates}` and `{diagramStandards}` for reference.

Read the storyboard plan metadata file from the output path to retrieve:
- The segment table (heading, subtitle, illustration prompt, supporting text)
- The visual style requirements

### 2. Prepare Image Prompts

For each segment in the storyboard plan:

1. Take the approved illustration prompt from the segment table
2. Wrap it with the base style foundation from `{imagePromptTemplates}` — ensuring consistent sketch style
3. Ensure each prompt targets a rich, detailed scene illustration (NOT a small icon)

Present the prepared prompts for final confirmation:

"**Prepared {count} hero illustration prompts (one per segment):**

| Segment | Heading | Key Visual Elements |
|---------|---------|---------------------|
| 01 | {heading} | {brief summary of what the illustration will show} |
| 02 | {heading} | {brief summary} |
| ... | ... | ... |

**Style consistency:** All prompts use the same base style — hand-drawn sketch aesthetic, black ink on white/transparent, detailed scene compositions.

**Ready to generate?** [G] Generate all hero illustrations"

**Auto mode:** Auto-proceed to generation immediately — no confirmation needed.

**Collab mode:** Wait for user confirmation.

### 3. Batch Generate Hero Illustrations

**With subprocess capability (Pattern 4 — Parallel Execution):**

Launch sub-processes in parallel to generate multiple images simultaneously:
- Each sub-process handles one hero illustration generation request
- Each returns the generated image file path and generation metadata
- Parent aggregates all results when complete

**Without subprocess capability (Fallback):**

Generate images sequentially in main thread:
- Process each prompt one at a time
- Save each image to the output images/ directory
- Track progress and report as each completes

For each segment:
1. Call `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"` (REQUIRED — never use any other model), the prepared prompt, and `image_size: "landscape_4_3"`. The fal-ai MCP is platform-level — no API key needed.
2. Save the returned image to `{output_path}/images/segment-{NN}-{heading-slug}.png`
3. Record: filename, prompt used, generation timestamp

"**Generation complete: {count}/{total} hero illustrations generated successfully.**"

If any failed:
"**{failed_count} illustrations failed to generate:**
- Segment {NN} ({heading}): {error reason}

**Options:** [R] Retry failed images [S] Skip and continue"

### 4. Present Batch for Review

Present all generated hero illustrations for user review:

"**Generated Hero Illustrations ({count} images — one per segment):**

| Segment | Heading | File | Status |
|---------|---------|------|--------|
| 01 | {heading} | {filename} | ✅ Generated |
| 02 | {heading} | {filename} | ✅ Generated |
| ... | ... | ... | ... |

**Review the illustrations for:**
- Visual consistency across the set (same sketch style)
- Correct representation of each segment's concept
- Rich detail level (full scene compositions, not icons)
- Clear visual storytelling that supports the segment narrative

**Which illustrations need revision? Enter segment numbers (comma-separated) or 'all good' to proceed.**"

**Auto mode:** Auto-approve all illustrations and proceed directly to step 6 (metadata) then step 7 (continue).

**Collab mode:** Wait for user feedback.

### 5. Revision Loop

**If user flags illustrations for revision:**

For each flagged illustration:
1. Ask: "**Segment {NN} ({heading})** — What should change? (e.g., different composition, more/less detail, different metaphor, wrong concept)"
2. Prepare a revision prompt using the revision template from `{imagePromptTemplates}`
3. Regenerate the specific illustration
4. Save to the same path (overwrite)

After revisions complete, re-present the updated set:

"**Updated illustrations:**
| Segment | Heading | Status |
|---------|---------|--------|
| {NN} | {heading} | 🔄 Revised |
| ... | ... | ... |

**Review again? Enter segment numbers for more revisions or 'all good' to proceed.**"

**Repeat this loop until user confirms 'all good' or selects C.**

### 6. Update Metadata

Once all illustrations are approved, update the storyboard plan metadata file:
- Record all image file paths per segment
- Record prompts used for each (for reproducibility)
- Record any revision notes

### 7. Present MENU OPTIONS

**Auto mode:** Auto-proceed to {nextStepFile} immediately — no menu.

**Collab mode:**

Display: "**All hero illustrations approved. Select:** [R] Revise more illustrations [C] Continue to Composition"

#### Menu Handling Logic:

- IF R: Return to revision loop (section 5), then [Redisplay Menu Options](#7-present-menu-options)
- IF C: Update storyboard plan metadata with image generation results, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user, then [Redisplay Menu Options](#7-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and all illustrations are approved and metadata updated will you then load and read fully `{nextStepFile}` to execute storyboard composition.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- One hero illustration prompt prepared per segment
- Consistent sketch style across all prompts (same base template)
- All illustrations generated (batch or sequential)
- Full set presented for user review
- Revision loop executed for any flagged illustrations
- User approved the complete illustration set
- All image paths and prompts recorded in metadata

### ❌ SYSTEM FAILURE:

- Composing the ExcaliDraw storyboard in this step
- Generating small icons instead of rich hero illustrations
- Not presenting the full set for review
- Skipping the revision loop when user flags illustrations
- Proceeding without user approval of all illustrations
- Inconsistent style across generated illustrations
- Not recording prompts used (breaks reproducibility)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
