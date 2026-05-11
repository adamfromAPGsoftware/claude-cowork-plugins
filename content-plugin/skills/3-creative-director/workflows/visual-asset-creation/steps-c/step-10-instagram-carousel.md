---
name: 'step-10-instagram-carousel'
description: 'Create Instagram carousels with nano-banana-2-generated slides, embedded screenshots, and brand styling'

instagramGuidelinesDark: '../data/instagram-carousel-guidelines-dark.md'
instagramGuidelinesLight: '../data/instagram-carousel-guidelines-light.md'
brandConfigData: '../data/brand-config.md'
pipelineScriptsData: '../data/pipeline-scripts.md'
instagramInspirationDir: '../data/instagram-carousel-inspiration'
scheduleInstagramData: '{project-root}/content-plugin/skills/2-copywriter/workflows/linkedin-content/data/schedule-instagram.md'
brandLogoDark: '{project-root}/context/context/brand-assets/brand-logo-dark.png'
brandLogoLight: '{project-root}/context/context/brand-assets/brand-logo-light.png'
---

# Step 10: Instagram Carousel Creation

## STEP GOAL:

To collaboratively create Instagram carousel slides using fal-ai MCP (`fal-ai/nano-banana-2` model), with embedded screenshots, custom per-slide prompts, and consistent brand styling. Each slide is uniquely crafted — not templated.

> **MANDATORY TOOL + MODEL RULE:**
> - Hook slides (reference photo) → `edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`
> - Content slides (text-only) → `generate_image` with `model_id: "fal-ai/nano-banana-2"`
> - Never use `generate_image_from_image` — model expects `image_urls` array, not `image_url` string. `edit_image` handles this correctly.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Creative Director with expertise in Instagram visual content and carousel engagement patterns
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring knowledge of scroll-stopping design, platform-specific visual psychology, and brand consistency
- ✅ The user brings their content, screenshots, and creative direction

### Step-Specific Rules:

- 🎯 Focus on Instagram carousel design and generation
- 🚫 FORBIDDEN to execute the script before user approves ALL slide prompts
- 💬 Each slide prompt must be unique but anchored to the brand constants from guidelines
- 📋 Hook slide must stop scrolling — it's the first impression
- 📋 CTA slide must have a clear "Comment [KEYWORD]" call to action

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Build JSON slides config from crafted prompts
- 📖 Execute script via bash tool call
- 🚫 FORBIDDEN to skip prompt review

## CONTEXT BOUNDARIES:

- Available: CCS config, brand tokens (from {brandConfigData}), Instagram guidelines (dark: {instagramGuidelinesDark}, light: {instagramGuidelinesLight}), project context
- Focus: Instagram carousel creation only
- Limits: Maximum 10 slides per carousel
- Dependencies: Step 01 init, step 02 selection (IC)

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Guidelines & Inspiration

Read {brandConfigData} for branding values, reference photo details, and Brand Modes configuration.

**ALWAYS** load and review all images from {instagramInspirationDir}. These are the style reference for every carousel. Study the layouts, typography, backgrounds, visual elements, photo treatments, and flow patterns. Use these to inform every prompt you craft. Do NOT ask the user whether to review them — this is automatic.

**Additionally, check global inspiration folders:**

1. Check `{workspace}/context/inspiration/carousels/` for any user-provided carousel inspiration.
2. Check `{workspace}/context/inspiration/instagram/` for autopilot-scraped Instagram posts.

If images are found in either folder:
- Load `{workspace}/context/references/visual-inspiration.md` and extract the "Carousel Patterns" section.
- Merge these patterns with the static inspiration from {instagramInspirationDir}: the static library remains the baseline, but global user-provided inspiration may surface brand-specific design preferences to apply.
- Note any patterns that are particularly relevant to this brand's identity (e.g., a preference for minimal text, specific composition tendencies, unique colour usage).

### 2. Brand & Mode Selection

**First, select the brand(s):**

"**Which brand(s) are we generating for?**

**[B] Both** — Generate {YOUR_COMPANY} (dark + logo) + {YOUR_NAME} (dark, no logo) from the same content (Recommended)
**[A] {YOUR_COMPANY}** — Dark mode with logo (@{YOUR_HANDLE}, SME founders)
**[P] Personal** — Dark mode, no logo (@{YOUR_HANDLE_PERSONAL}, builders)

Select: [B] / [A] / [P]"

Wait for selection. Store the brand mode.

- IF B (Both): Load BOTH {instagramGuidelinesDark} and {instagramGuidelinesLight}. Pipeline will run twice.
- IF A ({YOUR_COMPANY}): Load {instagramGuidelinesDark} only.
- IF P (Personal): Load {instagramGuidelinesLight} only.

**Then, select the creation mode:**

"**How would you like to build this carousel?**

**[AUTO] Autonomous** — I'll extract the topic from the video, decide everything, fetch logos, craft prompts, generate all slides, write the caption, and save. You'll be notified when it's done — zero questions.

**[COLLAB] Collaborative** — We'll work through each decision together — topic, points, slide count, layouts, and prompts.

**Select:** [AUTO] / [COLLAB]"

Wait for selection. Store the mode.

### 3. Extract Content & Execute

#### AUTO Mode — FULL AUTONOMOUS PIPELINE:

**🛑 CRITICAL: In AUTO mode, do NOT stop for user input at ANY point. Execute steps 3 through 10 as one continuous run. Only notify the user at the very end with the final output summary.**

**3a. Extract content** — Read the active project's video content files:
- Transcript (`transcript.json`)
- Audio analysis (`audio-analysis.json`, `audio-analysis.md`)
- Visual analysis (`visual-analysis.json`)
- Storyboard (if available)
- B-roll folder (check for screenshots/images that can be embedded)

From these, autonomously determine:
1. **Topic** — the most carousel-worthy angle from the video
2. **Key points** — 3-6 educational or insight-driven points
3. **Slide count** — based on content density (typically 5-8)
4. **CTA keyword** — derived from the topic
5. **B-roll/screenshots for inspiration** — review project B-roll to understand what tools and settings appear in the video. Use as prompt inspiration only — do NOT embed video frames. Tool UI screenshots (e.g., Claude Code interface) CAN be embedded.
6. **Hook slide photo** — the hook slide (slide 1) features the creator using a real photo. **PAUSE AUTO MODE HERE** and prompt the user to provide a photo. List available photos from `context/brand-assets/reference-photos/` as quick-select options. The user can select one or provide a custom file path. Store the selected path as `photo_path` in the slide JSON. The CTA slide (last slide) is text-only — "Comment [KEYWORD]" design, no photo of the creator.

**3b. Fetch logos** — Identify all tools/brands mentioned. For each, run `fetch-logo.ts` fresh (delete existing first). Verify each logo visually. If a logo fails or looks wrong, skip it silently — do not embed a wrong logo.

**3c. Craft prompts & generate (per brand)** — For each selected brand, run the full generation pass:

**When "Both" or single brand selected, execute for each brand in sequence:**

**Pass 1 (if or Both): Dark Mode (@{YOUR_HANDLE})**
1. Load dark guidelines from {instagramGuidelinesDark}
2. Craft prompts with dark palette, @{YOUR_HANDLE} handle, logo ({brandLogoDark}) top-right on every slide
3. Include logo in every slide's `embed_images` array
4. Logos fetched with `--color ffffff` (white-on-transparent for dark backgrounds)
5. Hook slide (slide 1): set `photo_path` to the user's selected photo. CTA slide (last slide): text-only "Comment [KEYWORD]" design, no `photo_path`.
6. Write `slides.json`, generate slides via `mcp__fal-ai__generate_image` per slide → output to `{output}/instagram/{brand_account}/`
7. Write caption with tone (professional, ROI-focused, "we built this" energy) + 3-5 business-focused hashtags

**Pass 2 (if Personal or Both): Dark Mode (@{YOUR_HANDLE_PERSONAL})**
1. Load personal dark guidelines from {instagramGuidelinesLight}
2. Craft prompts with dark palette (black/#111111 backgrounds), @{YOUR_HANDLE_PERSONAL} handle with YouTube icon, NO company logo (no logo)
3. Logos fetched with `--color ffffff` (white-on-transparent for dark backgrounds)
4. Hook slide (slide 1): set `photo_path` to the user's selected photo. CTA slide (last slide): text-only, no `photo_path`.
5. Write `slides.json`, generate slides via `mcp__fal-ai__generate_image` per slide → output to `{output}/instagram/{creator_account}/`
5. Write caption with personal tone (casual, builder-to-builder, anti-guru) + 3-5 builder-focused hashtags

**3d. Save** — Save captions as markdown with YAML frontmatter alongside the slide PNGs in each brand's output folder.

**3e. Notify user** — Present the FINAL summary only:

"**Instagram carousel(s) generated.**

**Topic:** {topic}
**CTA:** Comment "{KEYWORD}"

{IF generated:}
**{YOUR_COMPANY} (Dark) — @{YOUR_HANDLE}**
- **Slides:** {count} slides
- **Output:** `{output}/instagram/{brand_account}/`
- **Caption:** `{output}/instagram/{brand_account}/instagram-caption.md`
- **logo:** On every slide ✅

{IF Personal generated:}
**{YOUR_NAME} (Light) — @{YOUR_HANDLE_PERSONAL}**
- **Slides:** {count} slides
- **Output:** `{output}/instagram/{creator_account}/`
- **Caption:** `{output}/instagram/{creator_account}/instagram-caption.md`

**Logos fetched:** {list of tools with ✅/❌}
**Creator appears on:** Slide {N}, Slide {N}

Review the slides and let me know if you want to adjust anything, or schedule them."

Then proceed to step 11 (Schedule) — this is the ONLY point where AUTO mode halts for user input.

**SKIP steps 4–10 below when in AUTO mode — they are handled inline above.**

---

#### COLLAB Mode:

"**Let's design your Instagram carousel. I need:**

1. **Topic** — what is this carousel about?
2. **Key points** — the 3-6 main points (these become content slides)
3. **CTA keyword** — what should people comment to get the lead magnet? (e.g., "AGENT", "TOOLS", "GUIDE")
4. **Screenshots to embed** — do you have any screenshots/images to incorporate into slides? Provide file paths.
5. **Photo for hook slide** — provide a photo of yourself for the first slide. Available headshots in `context/brand-assets/reference-photos/` — or provide a custom file path.

I'll decide the slide count and which slides should feature you based on the inspiration patterns. Give me the raw content and I'll shape it."

Wait for user input.

After receiving content, autonomously decide:
- Slide count based on number of key points + hook + CTA
- Which slides feature the creator (following inspiration patterns and authenticity rules)
- Present these decisions to the user alongside the content summary (same format as AUTO mode)

### 4. Logos (COLLAB only — AUTO handles this in step 3b)

**4a. Fetch logos** — After content is confirmed, identify ALL tools, platforms, or brands mentioned in the carousel content. For each one, fetch the logo using `fetch-logo.ts` so it can be embedded into the relevant slide.

**Automatic logo detection:** Scan the key points and topic for tool/brand names (e.g., "Claude Code", "Cursor", "Notion", "Slack"). Every tool mentioned should have its logo fetched.

**For each detected tool/brand, run:**

```bash
npx tsx scripts/fetch-logo.ts \
    --name "{tool name}" \
    --output "{project logos folder}/{slug}.png" \
    --color ffffff
```

**Logo storage:** Save to the project's logo cache at `{project_folder}/{project-slug}/creative-director/logos/`.

**🛑 ALWAYS FETCH FRESH — NEVER reuse cached logos.** Delete any existing file at the output path before fetching. Stale/incorrect logos are worse than no logo. Every carousel run must pull fresh logos via the waterfall.

**After each fetch, VERIFY the logo:**
1. Read the output PNG to visually confirm it is the correct logo for that brand
2. If it looks wrong (generic icon, wrong brand, placeholder), treat it as a failed fetch

**If a fetch fails OR the logo looks wrong:**
1. Report which logo failed or looked incorrect
2. Ask the user: "The logo for **{tool name}** didn't come through correctly. Can you provide a direct URL to the official SVG/PNG, or should I skip the logo for this slide?"
3. If URL provided, re-run with `--url "{provided URL}"`
4. If skip, proceed without the logo on that slide — do NOT use an incorrect logo

**Present the logo fetch results:**

"**Logos fetched:**
- ✅ {tool 1} — {tier found} → `{output path}`
- ✅ {tool 2} — {tier found} → `{output path}`
- ❌ {tool 3} — not found (skipped / URL needed)

These will be embedded into the relevant slides."

Do NOT proceed to prompt crafting until all needed logos are resolved (fetched or explicitly skipped).

### 5. Craft Per-Slide Prompts (COLLAB only — AUTO handles this in step 3c)

**NOTE:** The hook slide (slide 1) uses the user's real photo — use the "Photo Hook Slide" prompt pattern from the guidelines. The CTA slide (last slide) is text-only — use the "CTA Slide" prompt pattern. Content slides are generated via `fal-ai/nano-banana-2`.

Using the guidelines from {instagramGuidelinesData} AND the inspiration images reviewed in step 1, craft a detailed image prompt for EACH slide. Each prompt must:

- Start with "Generate a 1080x1350 portrait Instagram slide."
- Include the brand anchors (green accent, font styles, dark palette)
- Be unique in layout and visual treatment (vary backgrounds, visual elements per inspiration)
- Reference any embedded screenshots with instructions on how to display them
- **Include fetched logos as `embed_images`** when a slide discusses a specific tool/brand — describe logo placement in the image prompt (e.g., "Show the attached logo in the top-right corner at roughly 80px", "Display the attached tool logo inside a rounded dark card alongside the headline")
- Include `@{YOUR_HANDLE_PERSONAL}` and bookmark on content slides (not hook)
- For the hook slide: include `photo_path` pointing to the user's selected photo. For the CTA slide: text-only, no `photo_path`.

**Present ALL prompts to the user for review:**

"**Here are your slide prompts:**

**Slide 1 (Hook):**
> {full prompt text}
> Embed images: {list or "none"}
> Photo: {path or "none"}

**Slide 2:**
> {full prompt text}
> Embed images: {list or "none"}
> Photo: none

... {continue for all slides}

**Slide {N} (CTA):**
> {full prompt text}
> Embed images: {list or "none"}
> Photo: none

**Total slides:** {count}"

### 6. Present MENU OPTIONS (COLLAB only — AUTO skips this)

Display: **Select an Option:** [A] Adjust prompts [E] Advanced Elicitation [P] Party Mode [G] Generate

#### Menu Handling Logic:

- IF A: Ask which slide(s) to adjust, make changes, redisplay all prompts, then redisplay menu
- IF E: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF G: Proceed to generation (section 7)
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY execute the script when user selects 'G'
- After other menu items execution, return to this menu

### 7. Build JSON & Execute (COLLAB only — AUTO handles this in step 3d)

Load {pipelineScriptsData} for the fal-ai MCP reference.

Build the `slides.json` file from the approved prompts. Then for each slide, call fal-ai MCP:

```
# Hook slide (with reference photo) — use edit_image, NOT generate_image_from_image:
mcp__fal-ai__upload_file(file_path="/path/to/real-photo.png")  → photo_url
mcp__fal-ai__edit_image(
  model="fal-ai/nano-banana-2/edit",
  image_url=photo_url,
  prompt="Using the attached photo of this person as the hero background, ...",
  strength=0.92
)

# Content slides (text-only):
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="Generate a 1080x1350 portrait Instagram slide. ...",
  image_size="portrait_4_5"
)
```

> **TOOL + MODEL RULE:** Hook slides with reference photos → `edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`. Content slides (text-only) → `generate_image` with `model_id: "fal-ai/nano-banana-2"`. Never use `generate_image_from_image` — it sends `image_url` as a string but nano-banana-2 expects an array.

Save each slide as `slide-01.png`, `slide-02.png`, etc. in `{project output}/instagram/`.

**Critical:** Generate slides sequentially — 2s pause between calls, NEVER parallelise.

Report the result:
- If success: "**Carousel generated!** {count} slides saved to: {output path}"
- If failure: Report error, ask if user wants to adjust prompts and retry

### 8. Review Output (COLLAB only — AUTO skips this)

"**Review the generated slides.** Check each one for:
- Text readability and accuracy
- Screenshot embedding quality
- Brand consistency (green accent, dark palette)
- Overall visual impact

**Options:**
- **[R] Regenerate slide(s)** — specify which slide number(s) to redo (I can adjust the prompt first)
- **[C] Continue** — slides look good, move to caption"

If R: Ask which slide(s) and whether to adjust the prompt. Regenerate only those slides (update JSON with just the target slides, re-run script). Then redisplay review menu.

If C: Proceed to caption.

### 9. Caption Writing (COLLAB only — AUTO handles this in step 3e)

"**Let's write the Instagram caption.** Based on the carousel content:

**Draft caption:**

{agent drafts caption following the caption rules from guidelines — hook line, context, CTA with keyword, hashtags}

**Options:**
- **[A] Adjust** — modify the caption
- **[C] Confirm** — caption looks good"

Work collaboratively until user approves.

### 10. Save (COLLAB only — AUTO handles this in step 3f)

Save the caption as a markdown file with YAML frontmatter:

```yaml
---
platform: instagram
type: carousel
slides: {count}
cta_keyword: "{KEYWORD}"
created: "{date}"
---
```

Followed by the caption text.

Save to the project output directory alongside the slide PNGs.

Report: "**Saved:**
- Slides: {output dir}/slide-01.png through slide-{NN}.png
- Caption: {output dir}/instagram-caption.md"

### 11. Schedule (Optional)

**If both brands were generated, offer scheduling for each separately:**

"**Would you like to schedule these carousels to Instagram?**

{For each generated brand:}

**{Brand Name} (@{handle}):**
**[N] Schedule now** — post immediately
**[T] Schedule for a time** — specify date/time (AEST default)
**[S] Skip** — don't schedule, just keep the files"

IF N or T:
1. Load {scheduleInstagramData} for scheduling workflow details
2. Preview the scheduling payload
3. Get explicit confirmation
4. Execute with the correct `--account` flag:
```bash
# {YOUR_COMPANY} carousel
python3 scripts/schedule-instagram-post.py \
  --file "{brand-caption-file-path}" \
  --media-dir "{output}/instagram/{brand_account}/" \
  --account {brand_account} \
  --scheduled-at "{ISO 8601 datetime}"  # omit for immediate

# {YOUR_NAME} carousel
python3 scripts/schedule-instagram-post.py \
  --file "{creator-caption-file-path}" \
  --media-dir "{output}/instagram/{creator_account}/" \
  --account {creator_account} \
  --scheduled-at "{ISO 8601 datetime}"  # omit for immediate
```
5. Report result for each brand

IF S: Skip scheduling.

### 12. Completion

"**Instagram carousel complete.**

**Slides:** {count} slides at {output path}
**Caption:** {caption path}
**Scheduled:** {scheduled status or 'not scheduled'}

Session complete."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Guidelines AND inspiration images loaded automatically before any prompt crafting
- Content extracted from video (AUTO) or gathered collaboratively (COLLAB)
- AI autonomously decided slide count, creator placement, and layouts (user approved)
- Unique per-slide prompts crafted following brand anchors and authenticity rules
- ALL prompts presented for user review before generation
- Script executed successfully with correct flags
- Output reviewed by user
- Caption written following Instagram caption rules
- Files saved to correct project location

### ❌ SYSTEM FAILURE:

- Executing script before user approves all prompts
- Using generic/identical prompts across slides
- Missing brand anchors (green accent, dark palette, font styles)
- Hook slide without scroll-stopping energy
- CTA slide without "Comment [KEYWORD]" call to action
- Not presenting prompts for review
- Skipping caption collaboration

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
