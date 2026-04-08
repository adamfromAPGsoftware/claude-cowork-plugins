---
name: 'step-03-media'
description: 'Plan visual media assets for the selected hook — branches internally by format'

nextStepFile: './step-04-content.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 3: Media Planning

## STEP GOAL:

To plan the visual media assets that will accompany the LinkedIn post, with format-specific brainstorming for image, carousel, and video posts. Text posts skip this step entirely.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual content strategist who understands how media amplifies LinkedIn engagement
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring visual storytelling expertise and media production knowledge, user brings their available assets and brand preferences

### Step-Specific Rules:

- 🎯 Focus only on media planning — no post body text yet
- 🚫 FORBIDDEN to write post copy in this step
- 💬 Present media options with clear rationale for how they support the hook
- 📋 Text format auto-skips this step entirely
- 📋 All generated or prepared media assets MUST target the output folder

## EXECUTION PROTOCOLS:

- 🎯 Check format — if text, auto-proceed to next step immediately
- 💾 Store media plan as session variable for content generation step
- 📖 Reference media asset inventory for project-based mode
- 🚫 FORBIDDEN to proceed without confirmed media selection (except text format)

## CONTEXT BOUNDARIES:

- Source mode, format, content context, selected hook, and content category are all available from previous steps
- Media asset inventory available from content brief (project mode)
- Brand guidelines available from agent context
- Focus: Visual assets only — post body comes in step-04

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Format Check

**If `{post_format}` is text:**

"**Text posts don't need media. Proceeding to content generation...**"

Immediately load, read entire file, then execute {nextStepFile}. Do NOT continue with the rest of this sequence.

**If `{post_format}` is image, carousel, or video:** Continue to section 2.

### 2. Media Brainstorming — IMAGE Format

**If `{post_format}` is image:**

Propose **3-5 specific image options** for the selected hook, prioritised:

**Project-based mode:**

1. **Branded single slide** — Use carousel generator in `single-image` mode to create a branded 1080x1080 image with a bold headline statement. Provide single-slide JSON config
2. **Existing screenshots** — Reference screenshots from project assets that show relevant IDE views, terminal output, or UI states
3. **Existing logo canvases** — Composite images from project assets that combine tool logos. Good for comparison/vs posts
4. **Rendered poster frames** — Still frames from rendered video outputs
5. **Gemini-generated image** — If no existing asset fits, propose a Gemini image generation prompt

**Personal mode:**

1. **Branded single slide** (recommended) — Use carousel generator in `single-image` mode. Bold headline image matching the hook
2. **Gemini-generated image** — Custom image via Gemini generation

For each option, present:
```
IMAGE OPTION {n}: {brief description}
Source: {filename or "carousel generator (single-image)" or "Gemini generation"}
What viewer sees: {description}
Why it works: {how it supports the hook}
```

### 3. Media Brainstorming — CAROUSEL Format

**If `{post_format}` is carousel:**

Plan the narrative arc across slides. A carousel tells a story — each slide must earn the swipe to the next.

**Plan slide structure:**
- **Title slide (1):** Bold hook headline (3 lines max, one line highlighted) + supporting body text + "SWIPE >>>" prompt
- **Body slides (3-8):** Each slide makes ONE point. Headline (3 lines, one highlighted) + supporting body text. Numbered automatically
- **CTA slide (1):** Headline question + CTA button text (comment keyword) + supporting body text

**Check carousel templates first:** Before designing slides from scratch, check `carousel-templates.md` (in the creative-director visual-asset-creation data folder) for proven patterns like the "Saraev Alternating" template. If a template fits the content type, use it as the slide structure and fill in the text.

**Draft slide content and present the full slide plan:**

```
CAROUSEL PLAN ({total_slides} slides):

SLIDE 1 (title):
  Headline: "{line 1}" / "{line 2 — HIGHLIGHT}" / "{line 3}"
  Body: "{supporting text}"

SLIDE 2 (body):
  Headline: "{line 1}" / "{line 2 — HIGHLIGHT}" / "{line 3}"
  Body: "{supporting text}"

... (repeat for each body slide)

SLIDE {N} (cta):
  Headline: "{CTA question}"
  Button: "{Comment KEYWORD below}"
  Body: "{what they'll receive}"
```

**Slide writing rules:**
- Each headline is exactly 3 short lines (2-4 words per line). One line is the "highlight"
- Body text is 1-2 sentences max per slide — punchy, not paragraphs
- Title slide hook must complement the post text hook (different wording, same angle)
- Body slides build a logical sequence (problem → insight → proof → solution)
- CTA slide headline is a question. Button text includes the comment keyword
- Total slides: 5-12 (sweet spot is 6-8 for engagement)

**Generate the slides JSON config:**

```json
{
  "branding": {
    "company": "SOFTWARE",
    "author": "{YOUR_NAME}"
  },
  "slides": [
    {
      "type": "title",
      "headline": ["Line 1", "Line 2", "Line 3"],
      "highlightIndex": 1,
      "body": "Supporting text here."
    },
    {
      "type": "body",
      "headline": ["Line 1", "Line 2", "Line 3"],
      "highlightIndex": 1,
      "body": "Supporting text here."
    },
    {
      "type": "cta",
      "headline": "CTA Question Here?",
      "buttonText": "Comment KEYWORD below",
      "body": "Description of what they'll receive."
    }
  ]
}
```

### 4. Media Brainstorming — VIDEO Format

**If `{post_format}` is video:**

Review the media asset inventory from the content brief and propose **3-5 specific video options**, prioritised:

1. **Existing motion graphics** — Already short, high-quality, branded. Suggest speed adjustments if needed
2. **Existing b-roll clips** — Already extracted segments. Suggest speed multiplier and trim points
3. **Clip extraction candidates** — From media inventory or video analysis. Specify: timestamp range, what's on screen, suggested duration (15-30s), speed multiplier
4. **Composite approach** — Combine multiple short clips if a single clip doesn't tell the full story

For each option, present:
```
VIDEO OPTION {n}: {brief description}
Source: {filename or timestamp range}
Duration: {seconds} | Speed: {multiplier}
What viewer sees: {description of the visual}
Why it works: {how it supports the hook}
```

### 5. User Selection

Present all options to the user. User selects one, combines multiple, or proposes their own.

Store as `{media_plan}` with all details needed for the content generation step and final output.

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
- IF C: Confirm media selection stored, then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN media is selected and confirmed (or text format auto-skips) will you load and read fully `{nextStepFile}` to execute content generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Text format correctly auto-skips to content generation
- Format-specific media options presented with clear rationale
- Media selection supports the selected hook
- Carousel slide plan follows 3-line headline rules with highlights
- Carousel JSON config is valid
- Video options include duration, speed, and trim details
- User confirmed media selection
- Media plan stored for subsequent steps

### ❌ SYSTEM FAILURE:

- Not auto-skipping for text format
- Writing post body copy in this step
- Generic media suggestions without hook-specific rationale
- Carousel slides with incorrect headline structure
- Video options without actionable extraction instructions
- Proceeding without confirmed media selection

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
