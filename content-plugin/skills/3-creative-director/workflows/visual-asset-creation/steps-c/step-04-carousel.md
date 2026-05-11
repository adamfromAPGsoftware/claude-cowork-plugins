---
name: 'step-04-carousel'
description: 'Create LinkedIn carousels or single post images from structured slide content'

brandConfigData: '../data/brand-config.md'
pipelineScriptsData: '../data/pipeline-scripts.md'
carouselTemplatesData: '../data/carousel-templates.md'
---

# Step 4: Carousel Creation

## STEP GOAL:

To collaboratively create LinkedIn carousel PDFs or single post images by designing slide content, building a JSON config with brand tokens, and executing the carousel generator.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Creative Director with expertise in LinkedIn content design and carousel engagement patterns
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring knowledge of slide composition, hook writing, and LinkedIn best practices
- ✅ The user brings their content, key points, and target audience

### Step-Specific Rules:

- 🎯 Focus on carousel/single-image design and generation
- 🚫 FORBIDDEN to execute the script before user approves the slide content
- 💬 Help craft punchy headlines — 3 lines max per slide, one highlighted in brand green
- 📋 Title slide must hook — it's the scroll-stopper
- 📋 CTA slide must have a clear call to action with button text

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Build JSON slides config from user content and brand tokens
- 📖 Execute script via bash tool call
- 🚫 FORBIDDEN to skip slide content review

## CONTEXT BOUNDARIES:

- Available: CCS config, brand tokens (from {brandConfigData}), project context
- Focus: LinkedIn carousel/image creation only
- Limits: Do not create other asset types in this step
- Dependencies: Step 01 init, step 02 selection (CA)

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Mode Selection

"**What type of LinkedIn visual do you need?**

**[C] Carousel** — Multi-slide PDF (swipeable). Best for educational content, lists, frameworks. Typically 5-8 slides.

**[S] Single Image** — One branded 1080x1080 PNG. Best for announcements, quotes, single points.

**Select:** [C] Carousel / [S] Single Image"

Wait for selection. Store the mode.

### 1b. Load Carousel Inspiration

Check the global carousel inspiration folder:

```bash
ls "{workspace}/context/inspiration/carousels/" 2>/dev/null | wc -l
```

**If images are found:**
- Load `{workspace}/context/references/visual-inspiration.md` and extract the "Carousel Patterns" section.
- If the file does not exist, read up to 3 images from the folder directly using the Read tool (multimodal) and extract dominant patterns inline: slide structure, text density, colour treatment, typography weight.
- Store as `carousel_inspiration_notes`.
- Inform user inline: "**Brand inspiration loaded:** {N} carousel examples from your workspace — I'll apply these design patterns to your slides."

**If the folder is empty:**
- Continue without blocking. Use brand tokens from {brandConfigData} only.

### 2. Check Carousel Templates

**For Carousel mode only:**

Load {carouselTemplatesData} and check if an existing template matches the content type (lead magnet, educational breakdown, nurture content). If a template applies, present it to the user:

"**I found a matching carousel template: {template name}.**
{brief description of the pattern}

Would you like to use this template? It handles the slide structure — you just need to fill in the text.

**[Y] Use template** / **[N] Design from scratch**"

If user selects Y, skip to section 3 with the template's slide structure pre-filled. If N, continue to section 3 with freeform design.

### 3. Gather Slide Content

**For Carousel mode:**

"**Let's design your carousel. I need:**

1. **Topic/theme** — what is this carousel about?
2. **Key points** — the 3-5 main points you want to convey (these become body slides)
3. **Hook headline** — what makes someone stop scrolling? (this becomes the title slide)
4. **CTA** — what should the reader do? (comment, follow, share, link?)

Give me the raw content and I'll shape it into slides."

**For Single Image mode:**

"**Let's design your post image. I need:**

1. **Headline** — the main message (3 lines, one will be highlighted in green)
2. **Supporting text** — brief body text below the headline
3. **Highlight line** — which of the 3 headline lines should be green?"

Wait for user input. Work collaboratively to refine the content.

### 4. Build Slide Structure

Load {brandConfigData} for branding values.

**If `carousel_inspiration_notes` were extracted in section 1b**, use them to inform layout decisions: text density per slide, typography weight, composition tendencies, colour accents. If inspiration shows a pattern that differs from the brand tokens, call it out to the user: "Your inspiration examples tend to use {pattern} — want to try that here, or stick with the standard brand style?"

Shape the user's content into the JSON slides structure:

**Title slide:**
- 3 headline lines (short, punchy, ALL CAPS works well)
- One highlighted in brand green (highlightIndex)
- Brief body text
- SWIPE prompt auto-added for carousel mode

**Body slides (carousel only):**
- Numbered automatically
- 3 headline lines each with one highlighted
- Body text explaining the point

**CTA slide:**
- Centered headline (question format works best)
- Button text (e.g., "Comment KEYWORD", "Follow for more")
- Brief supporting body text

Present the complete slide breakdown:

"**Here's your slide structure:**

**Slide 1 (Title):**
> {LINE 1}
> **{LINE 2 — highlighted}**
> {LINE 3}
> _{body text}_

**Slide 2:**
> {POINT 1 HEADLINE}
> _{body text}_

... {continue for all slides}

**Slide {N} (CTA):**
> {CTA headline}
> [{button text}]
> _{body text}_

**Total slides:** {count}
**Mode:** {carousel PDF / single image PNG}"

### 5. Present MENU OPTIONS (Pre-Execution)

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Generate

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Proceed to execution (section 5)
- IF user wants to modify slides: Make adjustments and redisplay the structure, then redisplay menu
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY execute the script when user selects 'C'
- After other menu items execution, return to this menu

### 6. Build JSON and Execute

Load {pipelineScriptsData} for the generate-carousel.js CLI reference.

Build the JSON slides config file:
```json
{
  "branding": { "company": "SOFTWARE", "author": "{YOUR_NAME}" },
  "slides": [ ... ]
}
```

Write the JSON to a temporary file, then execute:
```bash
node scripts/generate-carousel.js \
    --input [temp slides json path] \
    --output [project carousels path]/[slug]-carousel-[date].{pdf|png} \
    --mode {carousel|single-image}
```

Report the result:
- If success: "**{Carousel PDF / Single image} generated!** Saved to: {output path} ({slide count} slides)"
- If failure: Report error, ask if user wants to adjust and retry

### 7. Schedule to LinkedIn (Optional)

After carousel generation, offer to schedule the post:

"**Would you like to schedule this carousel to LinkedIn?**

**[Y] Schedule** / **[N] Skip**"

If Y:
1. Ask for the post text — can be from a file or collaboratively written
2. Ask for the schedule date/time (default timezone: AEST/AEDT)
3. Preview the payload and get confirmation
4. Execute the scheduling script:

```bash
python3 scripts/schedule-linkedin-post.py \
  --file "{post-text-file}" \
  --scheduled-at "{ISO 8601 datetime}" \
  --media "{carousel-pdf-path}"
```

See `{project-root}/content-plugin/skills/2-copywriter/workflows/linkedin-content/data/schedule-linkedin.md` for full workflow details.

### 8. Completion

"**Carousel complete.**

**File:** {output path}
**Mode:** {carousel PDF / single image}
**Slides:** {count}

Session complete."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Mode selected (carousel or single-image)
- Slide content collaboratively designed with user
- JSON config built with correct brand tokens
- User approved slide structure before execution
- Script executed successfully
- Output saved to correct project location

### ❌ SYSTEM FAILURE:

- Executing script before user approves slide content
- Missing branding in JSON config
- Title slide without a hook headline
- CTA slide without a clear call to action
- Not presenting slide structure for review

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
