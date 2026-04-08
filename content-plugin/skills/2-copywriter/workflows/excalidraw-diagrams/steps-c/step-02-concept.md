---
name: 'step-02-concept'
description: 'Parse intro script into segments, propose hero illustration prompts, and present approval table'

nextStepFile: './step-03-images.md'
diagramStandards: '../data/diagram-standards.md'
imagePromptTemplates: '../data/image-prompt-templates.md'
---

# Step 2: Segment Parsing & Storyboard Planning

## STEP GOAL:

To parse the intro script into video segments, define the storyboard structure for each segment (heading, subtitle, hero illustration, supporting text), generate Nanobanana prompts for each hero illustration, and present a complete segment approval table for user sign-off before image generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR working autonomously with approval checkpoints (collab mode) or fully autonomously (auto mode)
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual storyboard designer specialising in segment composition and illustration direction
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ This step is AUTONOMOUS — you analyse and propose, user approves
- ✅ You bring visual storytelling expertise, user brings creative direction and domain knowledge

### Step-Specific Rules:

- 🎯 Focus on parsing segments, defining storyboard structure, and crafting illustration prompts
- 🚫 FORBIDDEN to generate any images or ExcaliDraw JSON — that's step 3 and 4
- 💬 Approach: Present your analysis confidently, then ask for approval/adjustments
- 📋 The output of this step is a segment plan that drives everything that follows

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write segment plan to the storyboard plan metadata file
- 📖 Load diagram standards and image prompt templates for reference
- 🚫 FORBIDDEN to proceed to image generation without user approval of segment plan

## CONTEXT BOUNDARIES:

- Available: Script content from step 1, output path
- Focus: Analysing script structure and proposing visual storyboard per segment
- Limits: Do not generate images or ExcaliDraw JSON
- Dependencies: Step 1 must have provided the script

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load References

Load `{diagramStandards}` and `{imagePromptTemplates}` for reference during analysis.

### 2. Parse Script into Segments

**Autonomously** analyse the intro script to identify distinct video segments/sections:

1. **Identify segment boundaries** — Look for natural topic shifts, section markers, or narrative transitions in the script
2. **For each segment, extract:**
   - **Segment number** (sequential: 01, 02, 03...)
   - **Heading** — A short, punchy title (like "Your Claude Code, In Your Pocket" or "The Problem Everyone Has")
   - **Subtitle** — A one-line description that adds context (like "A thin bridge between your phone and your entire Claude Code ecosystem")
   - **Core visual concept** — What should the hero illustration depict?
   - **Supporting text** — A bold takeaway line for below the illustration (like "Everything you already use. One thin bridge. Access from your pocket.")

### 3. Craft Hero Illustration Prompts

For each segment, craft a detailed Nanobanana prompt using templates from `{imagePromptTemplates}`:

- Each prompt should produce a **rich, detailed scene illustration** — NOT a small icon
- The illustration should visually tell the story of that segment
- Style: Hand-drawn sketch with black ink on white/transparent background, ExcaliDraw aesthetic
- Complexity: Full compositions with multiple visual elements, labels, sub-scenes — like the reference examples
- Size: Large enough to be the hero visual (~400-600px wide in the final storyboard)

### 4. Present Segment Approval Table

Present the complete storyboard plan as a table:

"**Storyboard Plan — {segment_count} Segments:**

| # | Heading | Subtitle | Hero Illustration Prompt | Supporting Text |
|---|---------|----------|--------------------------|-----------------|
| 01 | {heading} | {subtitle} | {full Nanobanana prompt} | {takeaway text} |
| 02 | {heading} | {subtitle} | {full Nanobanana prompt} | {takeaway text} |
| ... | ... | ... | ... | ... |

**Storyboard Layout:**
- Wide horizontal canvas flowing left-to-right
- Each segment: Numbered heading → subtitle → hero illustration → supporting text → arrow to next
- Arrows connect segments in sequence
- Final segment has no trailing arrow

---

**Does this storyboard plan look right? You can:**
- Adjust any heading or subtitle
- Modify illustration prompts
- Add/remove segments
- Change supporting text

**What would you like to adjust, or shall we proceed?**"

**Auto mode:** Auto-approve the segment plan and proceed directly to step 5 (write metadata) then step 6 (continue).

**Collab mode:** Wait for user feedback. Incorporate any adjustments and re-present if needed.

### 5. Write Segment Plan to Metadata File

Once approved, write the storyboard plan to the metadata file at the output path established in step 1.

Include:
- Segment count
- Each segment's heading, subtitle, illustration prompt, and supporting text
- Canvas layout description
- Source script reference

### 6. Present MENU OPTIONS

**Auto mode:** Auto-proceed to {nextStepFile} immediately — no menu.

**Collab mode:**

Display: "**Storyboard plan approved. Select:** [C] Continue to Image Generation"

#### Menu Handling Logic:

- IF C: Update storyboard plan metadata with segment plan, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user adjust the plan, then [Redisplay Menu Options](#6-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the segment plan has been written to the metadata file will you then load and read fully `{nextStepFile}` to execute image generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Script parsed into distinct video segments
- Each segment has heading, subtitle, illustration prompt, and supporting text
- Hero illustration prompts are detailed enough to produce rich scene compositions (not small icons)
- Complete segment table presented for user approval
- User approved the storyboard plan
- Segment plan written to metadata file

### ❌ SYSTEM FAILURE:

- Generating images or ExcaliDraw JSON in this step
- Not presenting the full segment table for approval
- Producing icon-level prompts instead of rich scene illustration prompts
- Missing segments from the script
- Proceeding without user approval
- Not writing the segment plan to the metadata file

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
