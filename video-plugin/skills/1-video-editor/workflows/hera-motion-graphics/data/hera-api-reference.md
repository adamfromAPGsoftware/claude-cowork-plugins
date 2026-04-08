# Hera Video API Reference

## Overview

Hera Video is an AI motion graphics generation API. It takes a text prompt and an optional reference image URL, and produces animated motion graphic video clips.

## Endpoint

```
POST https://api.hera.video/v1/videos
```

## Authentication

```
x-api-key: {HERA_API_KEY}
```

The API key is stored in the project `.env` file. Load via `{env_file}` from CCS config.

## Request Format

```json
{
  "prompt": "Detailed motion graphic description here",
  "reference_image_url": "https://publicly-accessible-url/image.png",
  "duration_seconds": 5,
  "outputs": [
    {
      "format": "mp4",
      "aspect_ratio": "16:9",
      "fps": "30",
      "resolution": "1080p"
    }
  ]
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text prompt describing the motion graphic to generate |
| `outputs` | array | Yes | Export configurations (max 10 items) |
| `reference_image_url` | string | No | URL of a publicly accessible reference image |
| `reference_image_urls` | array of strings | No | Multiple reference image URLs (max 5). Use instead of `reference_image_url` for multi-reference MGs (e.g., tool comparisons) |
| `reference_video_url` | string | No | URL of a reference video |
| `duration_seconds` | number | No | Duration in seconds (1-60) |
| `style_id` | string | No | Style identifier for video styling |
| `parent_video_id` | string | No | Previously generated video ID or template ID |

### Output Configuration (each item in `outputs` array)

| Field | Required | Allowed Values |
|-------|----------|---------------|
| `format` | Yes | mp4, prores, webm, gif |
| `aspect_ratio` | Yes | 16:9, 9:16, 1:1, 4:5 |
| `fps` | Yes | "24", "25", "30", "60" — **MUST be passed as a string, not an integer** (live API rejects integer values despite documentation showing numbers) |
| `resolution` | Yes | 360p, 480p, 720p, 1080p, 4k |

### Constraints

- **Duration range:** 1-60 seconds
- **Max outputs per request:** 10
- **Reference image:** Must be a publicly accessible URL (not base64)

## Response Format

### Success (200) — Create Response

```json
{
  "video_id": "331a1e75-2b9a-43c8-a5b1-d1b3e3c77005",
  "project_url": "https://app.hera.video/motions/bb235249-96d3-4dde-a7d9-e3b6807ad76f?v=331a1e75-2b9a-43c8-a5b1-d1b3e3c77005"
}
```

The `video_id` is used to poll for completion and retrieve the rendered output.

### Retrieving Status & Output

```
GET https://api.hera.video/v1/videos/{video_id}
x-api-key: {HERA_API_KEY}
```

Poll this endpoint every 15 seconds until status is `"success"` or `"failed"`. **Note: the live API returns `"success"` not `"completed"` as the terminal success status.** Typical generation time is 2-4 minutes.

### Poll Response — In Progress

```json
{
  "video_id": "331a1e75-2b9a-43c8-a5b1-d1b3e3c77005",
  "project_url": "https://app.hera.video/motions/...",
  "status": "in-progress",
  "outputs": []
}
```

### Poll Response — Success (with download URL)

```json
{
  "video_id": "331a1e75-2b9a-43c8-a5b1-d1b3e3c77005",
  "project_url": "https://app.hera.video/motions/...",
  "status": "success",
  "outputs": [
    {
      "status": "success",
      "file_url": "https://hera-video.s3-accelerate.amazonaws.com/...mp4?X-Amz-...",
      "config": {
        "format": "mp4",
        "aspect_ratio": "9:16",
        "fps": "30",
        "resolution": "1080p"
      }
    }
  ]
}
```

**CRITICAL: The download URL field is `outputs[0].file_url` — NOT `url`.** This is a common mistake. Always access the download URL as:
```python
response["outputs"][0]["file_url"]
```

### Download Command

```bash
# Extract file_url and download
URL=$(curl -s "https://api.hera.video/v1/videos/{video_id}" \
  -H "x-api-key: $HERA_API_KEY" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['outputs'][0]['file_url'])")
curl -sL "$URL" -o "{output_path}"
```

## Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| 16:9 | YouTube, standard landscape video |
| 9:16 | YouTube Shorts, TikTok, Instagram Reels |
| 1:1 | Instagram feed, LinkedIn |
| 4:5 | Instagram feed, Facebook |

## Standard Output Config (for our pipeline)

Always use this output configuration unless the storyboard specifies otherwise:

```json
{
  "format": "mp4",
  "aspect_ratio": "16:9",
  "fps": "30",
  "resolution": "1080p"
}
```

---

## Reference Image Strategy

Reference images are CRITICAL for brand-related motion graphics and optional for abstract/descriptive ones.

### When a Reference Image is REQUIRED

- Motion graphic mentions a brand, logo, or company (e.g., "Upwork", "{YOUR_COMPANY}")
- Motion graphic features a person's image or profile
- Motion graphic needs to match specific visual branding
- **Type B (logo) and Type C (UI mockup) motion graphics** — always provide a reference image. For Type C, frame-extract from body footage is the preferred source (see Auto-Extract Strategy below)

### Reference Image Priority for Tool-Referencing MGs

**Frame-extracts from the body video are ALWAYS preferred over logos for Tier C MGs.** A frame-extract shows Hera the actual tool interface (panel layout, terminal output, data visible) which produces dramatically better results than a logo that gives zero interface context.

| MG Type | Reference Image Source | Why |
|---------|----------------------|-----|
| Tier C depicting tool UI | Frame-extract from body video | Shows actual interface layout, panels, data |
| Tier C depicting tool UI (tool not in body video) | Web screenshot via resolver | Shows real interface even if not in the video |
| Tier C abstract (no tool) | None — prompt-only | No visual reference needed |
| Tier A logo animation | Logo via fetch-logo.ts | Logo IS the subject — correct source |
| Tier B Ken Burns | Frame-extract from body video | Frame IS the output — correct source |

**Anti-pattern:** Passing a logo as `reference_image_url` for a Tier C MG prompt that says "terminal with command execution" or "UI with cards sliding in". The logo tells Hera nothing about the terminal layout or card design. Either use a real frame-extract/screenshot or omit the reference and write a highly detailed prompt.

### When a Reference Image is NOT Needed

- Abstract animations (e.g., "flowing particles", "gradient wave")
- Text-only animations (e.g., "statistic counter: 500+ projects")
- Generic visual effects (e.g., "smooth transition swoosh")

### Auto-Extract Reference Frames from Body Footage

**Default for all tool-referencing MGs:** When the visual analysis identifies a screen recording showing a specific tool (e.g., Claude UI, n8n canvas, VS Code), and a Type B or Type C MG is planned for that tool, extract a reference frame from the main video at the moment that tool is clearly visible.

**Extraction command:**
```bash
ffmpeg -ss {timestamp} -i "{source_video}" -frames:v 1 "{output_dir}/{tool_slug}-reference.png"
```

**Strategy:**
1. Cross-reference the MG's `tool_name` with the visual analysis frame classification
2. Find the timestamp where that tool's UI is most clearly visible (full screen, no overlays, sharp focus)
3. Extract a single frame at that timestamp
4. Use this as `reference_image_url` for the Hera API call

**This replaces the previous approach** where `frame-extract` was only used when explicitly marked in the MG brief. Now frame-extract is the **default** for all tool-referencing MGs when the tool is visible in the body footage.

**Reference frame cleanup (MANDATORY before upload):**
Raw frame-extracts often contain elements that hurt Hera output quality:
1. **Speaker PiP overlay** — Most screen recordings have the creator's face in a bottom-right picture-in-picture. Paint over or crop this out. Hera will try to reproduce faces, which looks wrong in an MG.
2. **Busy IDE chrome** — The reference image gives Hera the general layout and colour scheme. The PROMPT directs what to focus on. Don't worry about perfectly cleaning up every sidebar icon — just remove faces/people.
3. **No people or faces** — If the frame contains any person after cleanup, add "Do not include any people or faces." to the prompt.

**Prompt simplification for IDE/editor frames:**
IDE screenshots contain dozens of UI elements (sidebars, tab bars, minimaps, breadcrumbs, status bars). Don't try to describe all of them in the prompt — Hera picks up the general layout from the reference image. Instead, identify the **2-3 focal elements** that relate to what the viewer is hearing and describe those in detail. Let the reference image handle the rest.

**Zoom-to-focal-content (STRONGLY RECOMMENDED for IDE/tool MGs):**
Rather than trying to animate an entire busy IDE frame, direct Hera to zoom into the specific area where the key action happens — terminal logs scrolling, text being typed, code being highlighted. This naturally cuts visual noise and focuses viewer attention on what matters.

Example zoom prompts:
- "Camera slowly zooms into the terminal panel, focusing on green execution logs: 'Scanning 10 channels...', 'Scoring outliers...'"
- "Zooming into the chat input where 'Run competitive research' is being typed character by character"
- "Starting wide on the editor, then smoothly zooming into the output panel where results scroll in"

Zoom patterns: **type-and-zoom** (wide → zoom to typing area), **zoom-to-result** (start on action area, data appears), **static zoom** (already focused, for short 2s MGs).

**Fallback chain (when tool is NOT visible in body footage):**
1. `fetch-logo` waterfall (for Type B logo graphics)
2. `canvas-build` composite (for Type C UI mockups — combine logos + layout hints)
3. Enhanced text prompt with `tool-visual-reference.md` details (last resort — no image)

### Reference Image Sources

The `image_source` field in the storyboard's Visual Asset Source Map tells us where to get the reference image:

| image_source | Description | Workflow |
|-------------|-------------|----------|
| `branded-assets` | Pre-existing brand images in sidecar | Copy from `{project-root}/_bmad/_memory/video-editor-sidecar/branded-assets/` |
| `frame-extract` | Single frame extracted from the main video | Extract via FFmpeg: `ffmpeg -ss {timestamp} -i "{source}" -frames:v 1 "{output}.png"` |
| `canvas-build` | Composite image built from multiple sources | Build using ImageMagick or similar: combine logos, resize, create canvas |
| `fetch-logo` | Tool/brand logo fetched via waterfall script | Run `scripts/fetch-logo.ts` → visually verify → host at public URL |
| `none` | No reference image needed | Prompt-only generation |

### Canvas Building — DEPRECATED for Multi-Logo MGs

**Do NOT build multi-logo canvas composites for Hera.** Hera cannot faithfully reproduce multiple logos from a composite image — the results are garbled and off-brand.

**Instead:** Use text labels with brand colors for multi-tool MGs (see "Multi-Tool MGs" section above).

**Canvas composites are still valid for:**
- Single-tool comparison layouts (e.g., before/after with ONE tool's logo)
- Non-logo composites (e.g., combining screenshots, UI mockups)

### Hosting Reference Images

Reference images MUST be at a publicly accessible URL that does not expire.

**Primary: Supabase Storage (persistent)**
```bash
bash scripts/upload-to-supabase-storage.sh "{local_image}" "mg-refs/{project-slug}"
```
Returns: `https://{supabase-url}/storage/v1/object/public/resource-media/mg-refs/{project-slug}/{filename}`

**Automated: resolve-reference-image.ts**
The unified resolver handles upload automatically — returns a persistent URL directly:
```bash
npx tsx scripts/resolve-reference-image.ts \
  --tool "{tool_name}" \
  --project-slug "{project-slug}" \
  --visual-analysis "{visual_analysis_path}" \
  --source-video "{source_video_path}" \
  --output "{output_path}"
```

**DEPRECATED: tmpfiles.org**
Do NOT use tmpfiles.org. URLs expire within hours, breaking re-runs and debugging. Always use Supabase Storage for persistent hosting.

---

## Prompt Best Practices

### Structure

Write prompts with this structure:
1. **Subject** — What is being shown (logo, text, data, etc.)
2. **Motion** — How it moves (slides in, fades up, rotates, scales)
3. **Style** — Visual treatment (clean, minimal, corporate, energetic)
4. **Color** — Specific colors if brand-relevant
5. **Duration hint** — Pacing guidance (quick reveal, slow build)

### Good Prompt Examples

**Brand logo animation:**
"A clean corporate logo reveal: the {YOUR_COMPANY} logo fades in from center with a subtle glow effect, then settles with a thin underline animation sliding in from left. Dark gradient background. Professional and minimal."

**Statistics display:**
"Animated counter showing '500+ Projects Delivered' with the number counting up rapidly from 0. White text on a dark blue gradient background. Clean sans-serif font. The number lands with a subtle bounce effect."

**Profile card:**
"A floating profile card slides in from the right side: circular profile photo on the left, name '{YOUR_NAME}' and title 'Freelance Developer' on the right, with a 5-star rating beneath. Subtle shadow and rounded corners. Modern, professional style."

**Abstract transition:**
"Smooth flowing gradient transition from deep blue to teal, with subtle particle effects moving left to right. Clean and professional, suitable as a section divider."

### Context-Driven Prompts (MANDATORY for Short-Form MGs)

Short-form MG prompts MUST be enriched with two context sources. The goal is that every MG visually reinforces what the viewer is hearing AND accurately depicts the tool/concept as it appears in the creator's video.

**1. Transcript context** — What words are being spoken during this MG segment? The visual must reinforce the audio. If the speaker says "scans 10 channels and ranks every video", the MG should show channel data being scanned and ranked — not a generic abstract animation.

**2. Visual analysis context** — If the MG depicts a tool that appears in the body video, read the `description` field from `visual-analysis.json` to understand what the interface actually looks like. Use those details in the prompt: specific panel names, tab labels, terminal output text, file names visible, data shown.

**Prompt structure:**
```
[SPECIFIC UI ELEMENTS — what panels, tabs, text, data are visible, drawn from visual-analysis descriptions and reference frame]
[ANIMATION — how elements move, appear, transition]
[TRANSCRIPT CONNECTION — how the visual relates to what the viewer hears at this moment]
[STYLE SUFFIX — light bg, brand colors, minimal aesthetic]
```

**Example — VS Code terminal MG while speaker says "one command, full research report":**
> "A VS Code split-pane view: left side shows a file tree with 'competitive-research/' folder expanded revealing workflow YAML files. Right side shows an integrated terminal with the command 'npx tsx run-workflow competitive-research' in white text, followed by green agent logs: '→ Scanning 10 channels...', '→ 461 videos analyzed', '→ Scoring outliers...'. A progress indicator fills from left to right. Dark terminal inset on light background (#F5F5F5). The reference image shows the exact VS Code layout to match."

**Example — Claude Desktop MG while speaker says "AI system that validates every topic":**
> "Claude Desktop application showing the Customize panel. Left sidebar with navigation icons. Main area shows 'Skills' tab active with two installed skill cards: 'competitive-research' and 'content-planning', each with a green (#4ADE80) active badge. 'Connectors' and 'Agents' tabs visible but inactive on the right. Cards slide in from the right with a subtle spring animation. Clean light UI chrome matching the reference image."

### Bad Prompt Examples (avoid these)

- "Make a cool logo thing" — too vague
- "Animate" — no subject or motion described
- "Something with the brand" — no specific visual description
- "Claude Code terminal with command text animating line-by-line" — no specific commands, output, or connection to transcript
- "Claude Desktop Skills UI, cards slide in" — doesn't describe what's on the cards, what tabs are visible, what the layout looks like

### Motion Graphic Generation Rules

- **Hera API is the ONLY supported MG method** — never fall back to Python/PIL, ImageMagick, or any other static image generator. These produce garbage-quality results that degrade the video.
- **Failure recovery:** If Hera fails, retry (3× with 10s backoff) → simplify the prompt → substitute with a video-extract as last resort. Never generate a static image fallback.
- **Tool/platform specificity:** When the script mentions specific tools or platforms, MG prompts MUST name them explicitly with brand colors (e.g., "WhatsApp green #25D366 chat bubble", "Gmail red #EA4335 envelope icon", "Slack purple #4A154B workspace"). Generic descriptions like "messaging app icons" produce unrecognisable results.
- **Logo inclusion:** When a MG should feature tool logos, fetch them via `scripts/fetch-logo.ts` (see Logo Acquisition Pipeline below), visually verify, then include as `reference_image_url` (single logo) or build a canvas composite for multi-logo MGs. Hera produces significantly better results with visual references than text-only prompts for branded content.

---

## Tool Logo Inclusion Rule

### Single-Tool MGs (one tool referenced)

**When a MG features ONE tool, fetch its logo and pass as `reference_image_url`. The prompt MUST instruct Hera to reproduce the logo exactly.**

**Logo fidelity instruction — append to ALL single-logo prompts:**
```
The reference image contains the exact logo to use. Reproduce this logo precisely as shown — do not redraw, reinterpret, or stylize it. The logo must be pixel-accurate to the reference image.
```

**Acquisition:**
1. Fetch logo via `scripts/fetch-logo.ts` waterfall
2. Host at a publicly accessible URL (Supabase Storage)
3. Pass as `reference_image_url` in the Hera API request
4. Prompt must include the fidelity instruction above

**Example:**
- **Prompt:** "A clean motion graphic showing the Slack logo centered with a subtle pulse animation. The reference image contains the exact logo to use. Reproduce this logo precisely as shown — do not redraw, reinterpret, or stylize it. The logo must be pixel-accurate to the reference image. Clean modern design on a light off-white background (#F5F5F5)."
- **reference_image_url:** URL to fetched Slack logo PNG

### Multi-Tool MGs (2+ tools referenced)

**CRITICAL: When a MG features MULTIPLE tools, do NOT use logos. Use tool names as text labels instead.**

Hera cannot reliably reproduce multiple logos from a composite reference image — the results are garbled, unrecognizable, and off-brand. Text labels are clean, readable, and unmistakable.

**Rules for multi-tool MGs:**
- **NO `reference_image_url`** — do not pass any logo reference
- **NO canvas composites** — do not build multi-logo images
- **Use text labels** — show tool names as styled text (e.g., "Slack", "Gmail", "Notion")
- **Use iconic shapes** — pair each name with a simple geometric icon or colored dot/badge (NOT the actual brand logo)
- **Use brand colors** — color each tool's text or badge in its brand color for recognition

**Example — connectors grid with 6 tools:**
- **BAD:** "Grid of Slack, Gmail, Notion, HubSpot logos" + composite reference image → garbled logos
- **GOOD:** "A grid of 6 SaaS connector cards, each showing the tool name in bold black sans-serif text with a colored accent badge: 'Slack' (purple #4A154B), 'Gmail' (red #EA4335), 'Notion' (black #000000), 'HubSpot' (orange #FF7A59), 'Google Calendar' (blue #4285F4), 'Figma' (orange-red #F24E1E). Each card slides in with a green (#2D6A4F) checkmark. Clean modern design on light off-white background (#F5F5F5)."
- **reference_image_url:** NONE

### When to Use Which Strategy

| Scenario | Strategy | reference_image_url |
|----------|----------|---------------------|
| MG features 1 tool | Single-logo with fidelity instruction | YES — tool's logo |
| MG features 2+ tools | Text labels with brand colors | NO — none |
| MG is abstract (no tools) | Prompt-only | NO — none |
| MG features tool UI | Frame-extract or screenshot reference | YES — UI screenshot |

---

## Motion Graphic Visual Theme

**All motion graphics MUST follow the brand visual theme for consistency across all videos.**

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Light/Clean White | #F5F5F5 or #FAFAFA | Primary MG background — clean, modern tech aesthetic |
| Primary Text | Black | #1A1A1A | Headlines, numbers, labels |
| Accent | Dark Green | #2D6A4F | Highlighted words, accent elements, brand identity |
| Secondary | White | #FFFFFF | Card backgrounds, contrast elements |
| Shadow | Soft Black | rgba(0,0,0,0.1) | Depth, card shadows, text shadows |

### Style Rules

1. **Light backgrounds** — NOT dark gradients. Clean, bright, modern tech aesthetic
2. **Black text with green accents** — Primary text in #1A1A1A, key words/numbers in #2D6A4F
3. **Subtle shadows** — Soft drop shadows for depth, not heavy glows
4. **Sans-serif typography** — Inter, Helvetica Neue, or system sans-serif
5. **Minimal design** — Clean lines, generous whitespace, no visual clutter
6. **Consistent across all MGs** — Every MG in a video should feel like part of the same design system

### Prompt Template

**CRITICAL: Always append this style suffix to EVERY MG prompt. Dark backgrounds (#0a0a0a, #111, black) are FORBIDDEN unless explicitly overridden by the user.**

```
Clean modern design on a light off-white background (#F5F5F5). Black sans-serif text with dark green (#2D6A4F) accent highlights. Subtle soft shadows for depth. Professional, minimal tech aesthetic.
```

### Before (Old Style — FORBIDDEN)
"Bold white text on dark gradient background. Background: #0a0a0a." — generic, dark mode, inconsistent between MGs

### After (Style — REQUIRED)
"Bold black sans-serif text on clean light background (#F5F5F5), with dark green (#2D6A4F) accent on the key number. Subtle shadow beneath text. Professional, minimal tech aesthetic." — branded, consistent, light mode

### Common Mistakes to Avoid
- Using `Background: #0a0a0a` or any dark background in prompts
- Describing white/light text (use black #1A1A1A text instead)
- Using "dark theme" or "dark code-editor theme" (use light theme)
- Describing "glow" effects (use subtle shadows instead — glows imply dark backgrounds)

---

## Logo Acquisition Pipeline

When any MG brief references a named tool or brand, logos must be fetched and verified before use as `reference_image_url`.

### Pipeline Flow

1. **Fetch via `scripts/fetch-logo.ts`** — 4-tier waterfall:
   - Tier 1: Simple Icons (SVG → PNG conversion, fill color injected)
   - Tier 2: SVG Logos (community SVG repository — often has brand colors)
   - Tier 3: Logotypes.dev (logo API)
   - Tier 4: Logo.dev (fallback logo API)

2. **Command:**
   ```bash
   rm -f "{output_path}"  # Always fetch fresh
   npx tsx scripts/fetch-logo.ts --name "{tool}" \
     --output "{project_folder}/video-editor/short-form/logos/{slug}.png" \
     --color {brand_hex}
   ```

   **CRITICAL — `--color` flag:** Simple Icons (Tier 1) renders SVGs as a solid fill color. The default is white (`ffffff`), which is **invisible on white/light backgrounds**. Always pass the tool's brand color:

   | Tool | `--color` value | Notes |
   |------|----------------|-------|
   | Slack | _(omit — Tier 2 SVG Logos has brand colors)_ | Tier 2 has the multi-color logo with wordmark |
   | Gmail | `EA4335` | Google red |
   | Notion | `000000` | Black |
   | HubSpot | `FF7A59` | Orange |
   | Google Calendar | `4285F4` | Google blue |
   | Figma | `F24E1E` | Orange-red |
   | Anthropic | `D97757` | Coral |
   | Cursor | `000000` | Black |
   | Jira | `0052CC` | Blue |
   | Trello | `0052CC` | Blue |
   | Asana | `F06A6A` | Coral |
   | Zoom | `0B5CFF` | Blue |
   | Google Drive | `4285F4` | Google blue |

3. **Product-specific logo mapping (CRITICAL):**

   Some tools are sub-products of a parent company. `fetch-logo.ts` searches by name, so using the parent company name returns the WRONG logo.

   | Script Mentions | fetch-logo `--name` | WRONG name | Notes |
   |----------------|--------------------|-----------| ------|
   | Claude Desktop | `"Claude"` | ~~"Anthropic"~~ | Claude has its own icon (speech bubble), Anthropic is the "A" wordmark |
   | Claude Code | `"Claude"` | ~~"Anthropic"~~ | Same Claude icon — the product logos are the same |
   | Claude Chat | `"Claude"` | ~~"Anthropic"~~ | Same |
   | VS Code | `"Visual Studio Code"` | ~~"Microsoft"~~ | VS Code has its own icon |
   | Google Calendar | `"Google Calendar"` | ~~"Google"~~ | Product-specific icon |

   **If `fetch-logo.ts` cannot find the product-specific logo** (e.g., "Claude" not in Simple Icons), use `--url` to provide a direct URL:
   ```bash
   npx tsx scripts/fetch-logo.ts --name "Claude" \
     --output "logos/claude.png" \
     --url "https://claude.ai/favicon.ico"
   ```

   **Rule:** Always verify the fetched logo matches the SPECIFIC product mentioned in the script, not just the parent company.

4. **Visual verification gate (MANDATORY):** Read the output PNG and confirm:
   - Correct brand — matches the SPECIFIC product (Claude icon, not Anthropic "A")
   - Visible colors — not white-on-white or invisible on the expected background
   - Correct proportions — not stretched, cropped, or placeholder
   - If wrong → retry with `--url` override, try a different `--name` variant, or ask user

5. **Store in project logos directory:** `{project}/video-editor/short-form/logos/{slug}.png`

6. **Optional canvas composition** (for multi-logo MGs like comparison videos):
   - Fetch each logo individually via steps 1-5
   - Compose onto a single canvas via FFmpeg overlay filter
   - Use dark background (`#0a0a0a`) for the composite canvas since logos will be colorful
   - Store composite as `logos/{descriptor}-composite.png`
   - Visually verify the composite before upload

7. **Host at public URL** for `reference_image_url` parameter:
   ```bash
   export $(grep -E '^APG_LANDER_SUPABASE' .env | xargs)
   bash scripts/upload-to-supabase-storage.sh "{logo_path}" "{project-slug}"
   ```

8. **Pre-dispatch reference image verification (MANDATORY):**
   Before including any URL as `reference_image_url` in a Hera dispatch, visually verify the hosted image by reading/viewing it. Confirm:
   - The image loads (not 404)
   - It shows the correct brand/tool
   - It will be recognizable to Hera as a reference
   - Log the verification in the dispatch tracker

### Integration Points

- **Short-form storyboard (step 03, section C2):** Identifies hero keyword and records `heroLogoName` for fetch
- **Short-form assets (step 04, section 5b):** Executes fetch + verification for all logo MGs
- **Hera generation (step 02):** Uses verified logo as `reference_image_url` with `image_source: fetch-logo`

---

## Naming Convention for Output Files

Motion graphic IDs follow the pattern: `mg-{sequence}-{descriptor}`

Examples:
- `mg-01-apg-logo-reveal.mp4`
- `mg-02-upwork-profile-card.mp4`
- `mg-03-stats-counter.mp4`
- `mg-04-section-transition.mp4`
