---
name: short-form-thumbnail
description: Generate vertical 9:16 short-form thumbnails using the style guide and sidecar inspiration images
web_bundle: true
shortFormGuideData: '../visual-asset-creation/data/short-form-style-guide.md'
ctrChecklistData: '../visual-asset-creation/data/ctr-checklist.md'
pipelineScriptsData: '../visual-asset-creation/data/pipeline-scripts.md'
brandConfigData: '../visual-asset-creation/data/brand-config.md'
sidecarInspirationFolder: '{project-root}/memory/3-creative-director-sidecar/short-form-inspiration'
---

# Short-Form Thumbnail Generation

**Goal:** Generate vertical 9:16 thumbnails for YouTube Shorts, TikTok, and Instagram Reels using the short-form style guide and pre-loaded inspiration images.

**Your Role:** You are a short-form visual strategist who knows the composition blueprint, colour system (green/lime, not red), and typography rules for vertical thumbnails. You draft 1 concept per short-form video for user approval before spending API credits.

**Meta-Context:** This is a dedicated workflow for vertical short-form thumbnails. It auto-loads the style guide and 3 sidecar inspiration images — no need for the user to provide inspiration. When a project has short-form scripts, those scripts are the primary source of truth for what thumbnails to generate. For wide 16:9 thumbnails, use [VA] Visual Assets instead.

---

## WORKFLOW ARCHITECTURE

This is a single-file workflow. Follow the mandatory sequence below.

### Critical Rules (NO EXCEPTIONS)

- 🛑 NEVER generate thumbnails before user approves concepts
- 📖 Load the style guide and ALL 3 inspiration images before drafting concepts
- 📋 Every prompt must be FULLY RESOLVED — no placeholders, no brackets
- ✅ Communicate in your Agent communication style with `{communication_language}`
- 🚫 Banner colour is `{brand.colors.primary}` (set in config.yaml) — NEVER red
- 📋 Sequential generation only — NEVER parallelise
- 🎭 Expressions must be SUBTLE and NATURAL — see Expression Rules below
- 1️⃣ ONE thumbnail per short-form video — not multiple concepts per video

### Expression Rules

Allowed expressions (subtle, natural, positive range only):
- **Slight smile** — warm, approachable
- **Thoughtful** — hand on chin, contemplative
- **Curious** — slight head tilt, interested
- **Neutral/confident** — default professional

NEVER use: frowning, shocked, surprised, jaw-drop, wide-eyed, overly excited, unhappy, serious/stern, or exaggerated expressions of any kind. Keep it real, approachable, and positive.

### Icon/Logo Rules

- **All 3 icon positions (top, left, right) MUST be visually distinct** — never use the same brand logo twice, even in different variants (e.g. Claude logo + Claude Code terminal logo counts as a duplicate)
- **Claude ≠ Anthropic** — Claude has its own logo (the terracotta/orange "C" swirl shape), which is different from the Anthropic corporate logo. When the video features Claude or Claude Code, use the **Claude logo**, not the Anthropic logo.
- **Claude Code** has a terminal-style icon variant — use this when the topic is specifically about Claude Code (the CLI tool) rather than Claude (the model/chat product)
- **When Claude/Claude Code is the top icon**, the two floating icons must be different brands or generic icons (e.g. YouTube + a topic-relevant icon like magnifying glass, document, chart, etc.)
- **Prefer real brand logos over generic icons** — but never duplicate a brand to fill a slot

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from `{project-root}/config.yaml`:
- `user_name`, `communication_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `reference_photos_folder`

### 2. Load Style Guide and Inspiration

1. Load and read {shortFormGuideData} completely — this is the structural blueprint for ALL short-form thumbnails
2. Load ALL inspiration images from {sidecarInspirationFolder}:
   - `inspo-01.png`
   - `inspo-02.png`
   - `inspo-03.png`
3. Verify inspiration images exist (minimum 2). If missing, STOP: "Short-form inspiration images are missing from the sidecar. Add 2-3 example short-form thumbnails to `{sidecarInspirationFolder}/`."
4. Load {brandConfigData} for reference photo registry and colour palette

### 3. Load Keyword Research (Project Mode)

If `{active_project}` is set, scan for keyword research in the project's creative-director folder:

**Search path:** `{project_folder}/{active_project}/creative-director/thumbnails/`

1. Look for `keyword-research*.md` files (e.g. `keyword-research.md`, `keyword-research-v2.md`, `keyword-research-v3.md`)
2. Load the **latest version** (highest version number, or the one without a version suffix if only one exists)
3. Extract high-signal keywords and trending terms — focus on:
   - YouTube Autocomplete suggestions (Layer 1) — these reflect real search behaviour
   - Rising/breakout terms from Google Trends (Layer 2) if available
   - High-performing competitor keywords (Layer 3) if available
4. Store as `{keyword_pool}` — a ranked list of keywords to draw from when drafting text lines

**Keyword-to-Thumbnail Rules:**
- **Text lines MUST incorporate high-signal keywords** — the banner text (line 2) and descriptive text (line 1) should use actual search terms people type, not generic marketing copy
- **Floating icons and top icon MUST reflect keyword brands** — if "Claude Code" is a top keyword, use the Claude Code logo. If "YouTube" is trending, use the YouTube logo. Brand logos > generic icons.
- **Prioritise compound keywords** — "Claude Code skill" > "AI tool", "AI agents" > "automation", "agentic workflow" > "pipeline"
- **Every concept should hit at least 1-2 keywords** from the pool in either the text or the icon selection
- **Keep text lines short** — work keywords in naturally, don't stuff. Under 12 characters on line 2 is ideal, up to 25 is acceptable.

**IF no keyword research found:**
- Proceed without keyword data — draft concepts based on script content and general best practices
- Note to user: "No keyword research found for this project. Consider running [KR] Keyword Research first for better keyword-optimised thumbnails."

---

## MANDATORY SEQUENCE

### 1. Auto-Detect Scripts (Project Mode)

If `{active_project}` is set, check for existing short-form scripts:

**Scripts path:** `{project_folder}/{active_project}/video-editor/short-form/scripts/`

1. Scan for files matching `sf-*-script.md`
2. For each script found, read the frontmatter to extract:
   - `title` — the video title (used for thumbnail text and concept)
   - `concept_id` — e.g. SF-01, SF-02 (used for file naming: `sf-01.png`, `sf-02.png`)
   - `hook_type` — informs the vibe/angle
   - `status` — only process scripts with `status: approved`
3. Read the script body (Hook section) to understand the opening line and topic

**IF scripts found:**
- Present a summary table of detected scripts:

"**Auto-detected {N} short-form scripts in this project:**

| # | ID | Title | Hook Type | Status |
|---|-----|-------|-----------|--------|
| 1 | SF-01 | {title} | {hook_type} | {status} |
| ... | ... | ... | ... | ... |

I'll generate 1 thumbnail for each approved script. Shall I proceed with drafting concepts for all {N} approved scripts, or select specific ones?"

- Wait for user input (e.g. "all", "1,3,5", specific IDs)
- Skip to **Step 3** (Draft Concepts) using script data as context — do NOT ask for video description or slug

**IF no scripts found (or standalone mode):**
- Proceed to **Step 2** (Manual Input)

### 2. Manual Input (Fallback)

Only reached if no scripts were auto-detected.

"**Let's create a short-form thumbnail.** I need to know about your video:

1. **What is the video about?** (topic, key message)
2. **What is the vibe?** (educational, entertaining, shocking, motivational, etc.)
3. **What tools/brands are featured?** (determines top icon and floating icons)
4. **Any specific visual elements to include or avoid?**"

Wait for user input.

Then ask:

"**What's the video title slug?** (lowercase, hyphens — used for folder naming and file output)

Example: `ai-agent-automation`, `claude-code-tutorial`"

Wait for user input. Store as `{video-title-slug}`.

### 3. Draft Thumbnail Concepts

Draft **1 concept per short-form video**. Use script data (title, hook, topic) when available, or user-provided description for manual mode.

**Keyword Integration (when `{keyword_pool}` is available):**
- Cross-reference each script's topic against `{keyword_pool}`
- Select the 1-2 most relevant keywords for each concept's text lines
- Choose icon logos that match keyword brands (e.g. "Claude Code" keyword → Claude Code logo as floating icon or top icon)
- Present which keywords were used in the concept table so the user can see the SEO reasoning

**For each video, present the concept as:**

"**{concept_id}: {video title}**

| Field | Value |
|-------|-------|
| Top icon | {main topic brand/icon at top of frame — prefer brand logos matching keywords} |
| Floating icon (L) | {left icon — brand logo matching keyword, rounded-square, 3D tilt} |
| Floating icon (R) | {right icon — brand logo matching keyword, rounded-square, 3D tilt} |
| Expression | {subtle expression from allowed list — see Expression Rules} |
| Background | {themed background treatment — coded to topic per style guide} |
| Text line 1 | {white medium-weight ALL CAPS, modern geometric sans-serif — noticeably smaller than line 2 (~60-70% of line 2 font size), dark stroke outline for readability — incorporate keyword naturally} |
| Text line 2 | {white ultra-bold ALL CAPS, same sans-serif — larger than line 1, dark stroke outline (~3-4px black) so white reads clearly, thick bright green (#90F23C) underline bar (~8px) flush beneath letters only — NO filled rectangle} |
| Char count (line 2) | {count} |
| Keywords used | {which keywords from the pool informed this concept's text and icons} |

**Full Gemini Prompt:**
```
{EXACT text ready to send to the API — no placeholders, no brackets, fully resolved. Must specify: 9:16 aspect ratio (1080x1920), person centered chest-up, 2 floating icons with 3D tilt flanking head, top brand icon, themed background, bottom padding (160px dark empty space below the text block — platform UI safe zone), "match the composition and colour palette of the provided inspiration thumbnails". Expression MUST be from the subtle/natural allowed list. Icon logos MUST use real brand colours. When a logo is provided via --logo, the prompt MUST reference it explicitly by brand name so the model uses the provided image rather than hallucinating the shape — e.g. "use the provided [brand] logo image exactly as the [top/floating] icon".

TYPOGRAPHY — MANDATORY in every prompt (exact language):
- Line 1: "[TEXT]" in white medium-weight ALL CAPS, modern geometric sans-serif with clean rounded terminals and balanced proportions, moderate letter-spacing — NOTICEABLY SMALLER than line 2 (approximately 60-70% of line 2's font size), with a dark black stroke outline (~3px) so the white text reads clearly against the background.
- Line 2: "[TEXT]" in white ultra-bold ALL CAPS, same modern geometric sans-serif — LARGER than line 1, with a dark black stroke outline (~4px) so the white reads clearly. NO filled background rectangle. A thick bright green (#90F23C) horizontal underline bar (~8px) sits flush beneath the text letters only.
- Size contrast between lines is critical — the two lines must have a clear visual hierarchy, not appear the same size.}
```
"

### 4. Present for Approval

**If multiple thumbnails (from scripts):**

"**{N} Short-Form Concepts Ready:**

{All concepts listed with --- separators}

**Select which to generate:**
- **[A]** Approve all
- **[1]** / **[2]** / **[3]** etc. — Approve specific concept(s)
- **[R]** Request revisions"

**If single thumbnail (manual mode):**

"**Concept Ready:**

{Concept}

- **[Y]** Approve and generate
- **[R]** Request revisions"

Wait for user selection.

#### Menu Handling Logic:
- IF A or Y: Generate all approved
- IF specific numbers: Generate selected concepts only
- IF R: Ask what to change, apply modifications, re-present

### 4.5. Logo Sourcing (Auto)

No gate question. Run automatically after concept approval, before generation.

**Logos folder:** `{project_folder}/{active_project}/video-editor/short-form/logos/`

1. For each approved concept, extract all brand names from icon fields (top icon, floating left, floating right)
2. For each brand, check whether a PNG already exists in the logos folder — if yes, skip the fetch
3. For any brand **not** already present as a PNG, load {pipelineScriptsData} and run:
   ```bash
   npx tsx scripts/fetch-logo.ts \
       --name "{brand}" \
       --output "{project_folder}/{active_project}/video-editor/short-form/logos/{slug}.png" \
       --color "{brand-color}"
   ```

   **Known Brand Colors:**
   | Brand | `--name` value | `--color` |
   |-------|---------------|-----------|
   | Claude / Claude Code | `Claude` | `CC785C` |
   | Anthropic | `Anthropic` | `CC785C` |
   | OpenAI / ChatGPT | `OpenAI` | `ffffff` |
   | Google / Google Meet | `Google Meet` | `ffffff` |
   | Chrome | `Chrome` | `ffffff` |
   | DeepGram | `Deepgram` | `13EF93` |
   | OpenRouter | `OpenRouter` | `ffffff` |
   | GitHub | `GitHub` | `ffffff` |
   | YouTube | `YouTube` | `FF0000` |

   For any brand NOT in this table, default to `--color ffffff`.

4. Report inline: `Logos fetched: Claude ✓ (Tier 1), YouTube ✓ (Tier 1)`
   - If a fetch fails: "**{brand} logo fetch failed.** Provide a direct URL (`--url https://...`) or type **skip** to omit it."
5. Store all confirmed logo paths as `{logo_paths}` for use in Step 5

### 5. Generate Approved Thumbnails

For each approved concept, execute generation via fal-ai MCP:

```
# 1. Upload creator reference photo first (identity preservation)
mcp__fal-ai__upload_file(file_path="{reference_photos_folder}/creator-hero-front.jpg")
  → returns ref_url

# 2. Upload each logo PNG and capture URLs for prompt inclusion
mcp__fal-ai__upload_file(file_path="{logo_paths[0]}")  → logo_url_1
mcp__fal-ai__upload_file(file_path="{logo_paths[1]}")  → logo_url_2

# 3. Generate thumbnail (logos are described in the prompt — reference their URLs)
mcp__fal-ai__generate_image_from_image(
  image_url=ref_url,
  prompt="{exact prompt from the approved concept, with logo URLs referenced}",
  image_size="portrait_4_5"
)
```

Omit logo upload steps if no logos were resolved for this concept.

**Execution rules:**
- Attach creator reference photos (foundation image FIRST) for identity preservation
- Attach ALL 3 sidecar inspiration images as style references
- Include one `--logo {path}` per resolved PNG from Step 4.5
- Use the EXACT prompt from the approved concept — do NOT modify
- Sequential generation (never parallel)
- Report per-concept status: `Generating {concept_id}: {title}... [success/failed]`

### 6. Determine Output Location

Resolve the output folder — thumbnails live alongside the scripts they were generated from:
- If `{active_project}` is NOT NONE: `{project_folder}/{active_project}/video-editor/short-form/thumbnails/`
  - This places thumbnails next to the `scripts/` folder in the same short-form pipeline directory
- If `{active_project}` is NONE: `{standalone_folder}/short-form/{video-title-slug}/thumbnails/`

Ensure the output folder exists, create if not.

Save:
- Generated thumbnails as `sf-01.png`, `sf-02.png`, etc. (matching concept_id numbering)
- The concept prompts as `short-form-prompts.md` in the same thumbnails folder — include the logo paths used per concept so future re-generations can skip the waterfall for already-fetched logos

### 7. CTR Validation

Load {ctrChecklistData} and run the 7-point validation on each generated thumbnail.

Present results with scores.

### 8. Completion

"**Short-Form Thumbnails Complete.**

| # | Title | File | CTR Score |
|---|-------|------|-----------|
| 1 | {title} | sf-01.png | {X}/7 |
| ... | ... | ... | ... |

**Output folder:** `{output_folder}/`

**What would you like to do?**
- **[E]** Edit a specific thumbnail (image-to-image refinement)
- **[D]** Done — exit this workflow"

Wait for user selection.

#### Menu Handling Logic:
- IF E: Ask which thumbnail and what changes. Build an edit prompt, execute with source image + reference photos. Save as `sf-{NN}-v2.png`. Re-run CTR validation. Return to this menu.
- IF D: End workflow session

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:
- Style guide loaded from data file
- ALL 3 sidecar inspiration images loaded
- Keyword research loaded when available (project mode)
- Scripts auto-detected when available (project mode)
- 1 concept drafted per short-form video (not 3)
- Text lines incorporate high-signal keywords from keyword research
- Icon/logo choices reflect keyword brands (Claude Code, YouTube, etc.)
- Expressions are subtle and natural (no shocked/exaggerated)
- User approved concepts before generation
- Logo sourcing (Step 4.5) ran after approval and before generation
- Correct brand logos fetched via fetch-logo.ts waterfall (not hallucinated)
- Logo PNGs uploaded via `mcp__fal-ai__upload_file` and referenced by URL in the prompt for each resolved PNG
- Prompts reference provided logo images by brand name explicitly
- Reference photos attached for identity preservation
- Inspiration images attached as style reference
- Green/lime banner colour used (not red)
- Bottom padding specified in prompts
- Thumbnails saved to correct output folder
- CTR validation run on every generated thumbnail

### FAILURE:
- Generating before user approves concepts
- Not loading sidecar inspiration images
- Not loading keyword research when it exists in the project
- Using generic text when keyword research is available
- Using generic icons when brand logos match keywords
- Using red banners instead of green/lime
- Prompts with placeholders or brackets
- Parallelising generation
- Not specifying bottom padding in prompts
- Skipping logo sourcing step or hallucinating logo shapes in prompts
- Skipping CTR validation
- Using shocked/surprised/exaggerated expressions
- Generating 3 concepts per video instead of 1
- Not checking scripts folder when in project mode
