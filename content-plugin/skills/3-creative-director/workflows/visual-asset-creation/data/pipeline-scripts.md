# Pipeline Script CLI Reference

> **MANDATORY MODEL + TOOL RULE:**
> - **Text-only generation** (no reference photo): use `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"`
> - **Identity-preserving generation** (reference photo provided): use `mcp__fal-ai__edit_image` with `model: "fal-ai/nano-banana-2/edit"` and `strength: 0.92`
> - **NEVER use `generate_image_from_image`** with nano-banana-2 — it sends `image_url` as a singular string but the model API expects `image_urls` as an array. `edit_image` wraps the URL correctly internally.
> - Never use Flux, Gemini, SDXL, or any other model.

## 1. YouTube Thumbnail — fal-ai MCP

**Tool (text-only):** `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"`
**Tool (identity-preserving):** `mcp__fal-ai__edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`
**Auth:** Platform-level MCP — no API key needed

**Call pattern (text-only):**
```
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="YouTube thumbnail: ...",
  image_size="landscape_16_9"
)
```

**Call pattern (identity-preserving, with reference photo):**
```
1. mcp__fal-ai__upload_file(file_path="reference-photos/creator-hero-front.jpg")
   → returns reference_url

2. mcp__fal-ai__edit_image(
     model="fal-ai/nano-banana-2/edit",
     image_url=reference_url,
     prompt="YouTube thumbnail showing {creator} ...",
     strength=0.92
   )
```

**Why `edit_image` not `generate_image_from_image`:** `generate_image_from_image` sends `image_url` as a singular string, but `fal-ai/nano-banana-2/edit` expects `image_urls` as an array. `edit_image` wraps the URL into an array before calling the API, making it compatible.

**Orchestration Rules:**
- Run combos sequentially — NEVER parallelise (rate limiting)
- If a combo fails, report the error and continue to the next
- Maximum 5 combinations per batch
- Always pair a thumbnail with its title — never present one without the other
- Run CTR validation on every generated combo

**Key Mechanics:**
- Upload reference photo first with `mcp__fal-ai__upload_file`, then pass the URL to `edit_image`
- Use 1-3 creator reference photos for best identity consistency
- `strength: 0.92` = high transformation while preserving the reference identity
- `edit_image` does not take `image_size` — output dimensions match the input reference photo

---

## 2. General Image — fal-ai MCP

**Tool (text-only):** `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"`
**Tool (with input images):** `mcp__fal-ai__edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`
**Auth:** Platform-level MCP — no API key needed

**Call pattern (text-only):**
```
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="A dark comparison graphic showing Tool A vs Tool B logos",
  image_size="landscape_4_3"
)
```

**Call pattern (with input images — logos, screenshots, existing images as reference):**
```
1. mcp__fal-ai__upload_file(file_path="logos/tool-a.png")  → url_a
2. mcp__fal-ai__edit_image(
     model="fal-ai/nano-banana-2/edit",
     image_url=url_a,
     prompt="Combine these logos into a horizontal comparison",
     strength=0.92
   )
```

**Available image_size presets:** `square`, `square_hd`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_4_5`

**Key Mechanics:**
- Upload local files first with `mcp__fal-ai__upload_file`, then pass the returned URL
- To resize for platform specs: use `mcp__fal-ai__resize_image` with target_format presets (e.g., `instagram_post`, `youtube_thumbnail`, `linkedin_post`)

---

## 3. LinkedIn Carousel — generate-carousel.js

**Script:** `scripts/generate-carousel.js`
**Runtime:** Node.js 20+ | Puppeteer, pdf-lib

```bash
# Carousel mode (multi-page PDF)
node scripts/generate-carousel.js --input slides.json --output output/carousels/carousel.pdf --mode carousel

# Single image mode (PNG)
node scripts/generate-carousel.js --input slides.json --output output/images/post.png --mode single-image
```

| Flag | Required | Description |
|------|----------|-------------|
| `--input` / `-i` | Yes | Path to JSON slides config |
| `--output` / `-o` | Yes | Output file path (PDF or PNG) |
| `--mode` / `-m` | No | `carousel` (default) or `single-image` |

**JSON Slides Schema:**
```json
{
  "branding": { "company": "SOFTWARE", "author": "{YOUR_NAME}" },
  "slides": [
    { "type": "title", "headline": ["LINE ONE", "LINE TWO", "LINE THREE"], "highlightIndex": 1, "body": "Supporting text" },
    { "type": "body", "headline": ["POINT", "HEADLINE", "HERE"], "highlightIndex": 0, "body": "Detailed explanation" },
    { "type": "cta", "headline": "Ready to get started?", "buttonText": "Comment KEYWORD", "body": "What happens next" }
  ]
}
```

**Slide types:**
- `title` — First slide hook with headline, body, and "SWIPE >>>" prompt
- `body` — Content slides with headline + body + SWIPE. Optional `"label"` field renders a small green uppercase label above the headline (e.g., `"label": "STEP 1"`)
- `photo-title` — Full-bleed photo as bg with gradient overlay, headline at bottom-left. When last slide: green "Follow" pill bubble instead of SWIPE. Requires `"photoPath"`. Optional `"ctaText"` for the bubble (default: "Follow for more")
- `text-only` — Dark bg, white body text + SWIPE. Optional `"imagePath"` renders a rounded screenshot in the upper portion with text directly below. Without image, text is vertically centered
- `cta` — Centered CTA with headline, button, and body text

**Additional fields:**
```json
{ "type": "photo-title", "photoPath": "/path/to/photo.png", "headline": ["LINE 1", "LINE 2"], "highlightIndex": 0, "body": "optional", "ctaText": "Follow + ♻️" }
{ "type": "text-only", "body": "White text content.", "imagePath": "/optional/path/to/image.png" }
{ "type": "body", "label": "STEP 1", "headline": [...], "highlightIndex": 0, "body": "..." }
```

**SWIPE behaviour:** "SWIPE >>>" appears automatically on all slides except the last. The last `photo-title` slide gets a green pill-shaped CTA bubble instead.

---

## 4. Instagram Carousel — fal-ai MCP (per-slide)

**Tool (content slides, text-only):** `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"`
**Tool (hook slide with reference photo):** `mcp__fal-ai__edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`
**Auth:** Platform-level MCP — no API key needed

**Slide generation pattern:**

For each slide in `slides.json`, make a separate MCP call:

```
# Content slides (text-only — no photo_path):
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="Portrait Instagram slide 1080x1350. ...",
  image_size="portrait_4_5"
)

# Hook slide (photo_path set — use edit_image, NOT generate_image_from_image):
1. mcp__fal-ai__upload_file(file_path=slide.photo_path)  → photo_url
2. mcp__fal-ai__edit_image(
     model="fal-ai/nano-banana-2/edit",
     image_url=photo_url,
     prompt="Portrait Instagram slide 1080x1350. Using the attached photo as the hero background...",
     strength=0.92
   )
```

**Why `edit_image` for hook slides:** `generate_image_from_image` sends `image_url` as a singular string; `fal-ai/nano-banana-2/edit` expects `image_urls` as an array. `edit_image` handles the wrapping internally.

**Slides JSON schema** (same format, read by the agent):
```json
{
  "slides": [
    {
      "slide_number": 1,
      "prompt": "Portrait Instagram slide 1080x1350. ...",
      "photo_path": "/path/to/real-photo.png",
      "embed_images": []
    },
    {
      "slide_number": 2,
      "prompt": "Portrait Instagram slide 1080x1350. ...",
      "embed_images": ["./screenshots/terminal.png"]
    }
  ]
}
```

**Key Mechanics:**
- Hook slide (`photo_path` set): upload with `upload_file` → pass URL to `edit_image`
- Content slides (no `photo_path`): use `generate_image` with `image_size: "portrait_4_5"` (1080×1350)
- 2s delay between calls (rate limiting) — NEVER parallelise
- Maximum 10 slides per carousel
- Save each output as `slide-01.png`, `slide-02.png`, etc.
- To regenerate a specific slide: re-call the MCP tool with that slide's prompt only

---

## 5. Instagram Scheduling — Buffer MCP

**Tool:** `mcp__buffer__use_buffer_api`
**Auth:** Platform-level MCP — no API key needed

**Call pattern:**
```
# First: discover your channel IDs
mcp__buffer__buffer_api_help(action="listChannels")
→ then call mcp__buffer__use_buffer_api with action "listChannels"

# Then: create the post
mcp__buffer__use_buffer_api(
  action="createPost",
  payload={
    "profileIds": ["<instagram-channel-id>"],
    "text": "Your caption...",
    "scheduledAt": "2026-03-10T09:00:00+11:00",
    "media": ["<slide-01-url>", "<slide-02-url>", ...]
  }
)
```

**Key Mechanics:**
- Use `mcp__buffer__buffer_api_help` first to discover exact action names and payload schema
- Media files can be passed as URLs (upload via `mcp__fal-ai__upload_file` first if local)
- `scheduledAt` is ISO 8601. Omit for immediate posting.
- For carousel: pass all slide image URLs in the `media` array

---

## 6. Logo Fetch — fetch-logo.ts

**Script:** `scripts/fetch-logo.ts`
**Runtime:** Node.js 20+ | TypeScript (tsx), Sharp
**Dependency:** `sharp` (add to `scripts/package.json`) — handles SVG→PNG via libvips

**Output is always PNG (512×512, transparent background).** SVGs are fetched internally and converted before saving — the fal-ai MCP requires raster image inputs, not SVG.

```bash
# Automatic waterfall — outputs PNG
npx tsx scripts/fetch-logo.ts --name "Claude Code" --output logos/claude-code.png

# With explicit fill colour for dark backgrounds (default: ffffff)
npx tsx scripts/fetch-logo.ts --name "Anthropic" --output logos/anthropic.png --color ffffff

# Direct URL override (skips waterfall)
npx tsx scripts/fetch-logo.ts --name "Custom Tool" --output logos/custom.png --url "https://example.com/logo.svg"
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--name` | Yes | — | Brand/tool name |
| `--output` | Yes | — | Output PNG path |
| `--color` | No | `ffffff` | Fill hex for unfilled SVG logos (white = dark bg) |
| `--url` | No | — | Direct URL override (skips waterfall) |

**4-Tier Waterfall:**

| Tier | Source | Auth | Notes |
|------|--------|------|-------|
| 1 | Simple Icons CDN (jsdelivr) | None | SVG — fill injected via `--color` |
| 2 | SVG Logos (gilbarbara) | None | SVG — already coloured |
| 3 | Logotypes.dev | None | SVG or raster fallback |
| 4 | Logo.dev | `LOGO_DEV_TOKEN` env var | PNG, 256px |

All tiers save as PNG — SVG conversion happens automatically via Sharp.

**Finding slugs for manual reference:**
- Simple Icons: search simpleicons.org — slug = icon title, lowercase, no spaces/hyphens (e.g., `claudecode`)
- Gilbarbara: lowercase, spaces→hyphens (e.g., `claude-code`)
- Full slug list: github.com/simple-icons/simple-icons/blob/develop/slugs.md

---

## 7. Logo Canvas Composition — compose-canvas.ts

**Script:** `scripts/compose-canvas.ts`
**Runtime:** Node.js 20+ | TypeScript (tsx), Sharp

```bash
npx tsx scripts/compose-canvas.ts \
    --logos logos/claude-code.svg,logos/remotion.svg \
    --width 1920 --height 1080 \
    --output output/images/logo-canvas.png \
    [--bg "#1a1a2e"] [--padding 10]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--logos` | Yes | Comma-separated logo file paths |
| `--width` | Yes | Canvas width in pixels |
| `--height` | Yes | Canvas height in pixels |
| `--output` | Yes | Output PNG file path |
| `--bg` | No | Background colour hex (default: `#1a1a2e`) |
| `--padding` | No | Padding percentage 0-50 (default: `10`) |

**Composition:** Single logo = 40% of canvas, centered. Multiple = side-by-side with 5% gap.

---

## 8. Web Page Capture — screenshot.ts

**Script:** `scripts/screenshot.ts`
**Runtime:** Node.js 20+ | TypeScript (tsx), Playwright

```bash
npx tsx scripts/screenshot.ts \
    --url "https://example.com" \
    --output output/captures/example.png \
    [--viewport landscape] [--selector ".main-content"] [--dark-mode]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--url` | Yes | URL to capture |
| `--output` | No | Output path (default: `screenshot.png`) |
| `--viewport` | No | `landscape` (1920x1080), `portrait` (1080x1920), `square` (1080x1080) |
| `--selector` | No | CSS selector to capture specific element |
| `--dark-mode` | No | Enable dark colour scheme |

**Features:** 2x device scale factor, auto-hides cookie banners/chat widgets, 1500ms content load wait, 60s page timeout.

---

## 9. YouTube Keyword Research — keyword-research.py

**Script:** `scripts/keyword-research.py`
**Runtime:** Python 3.10+ | pytrends, requests
**Auth:** Layer 3 uses YouTube MCP (`mcp__youtube__*`) — platform-level, no API key needed

```bash
python scripts/keyword-research.py \
    --seeds "AI agents, Claude Code, automation" \
    --output output/keyword-research.md \
    [--brief content-brief.md] \
    [--format markdown|json]
```

| Flag | Required | Description |
|------|----------|-------------|
| `--seeds` | Yes | Comma-separated seed keywords |
| `--output` | Yes | Output file path for the keyword report |
| `--brief` | No | Path to content brief for additional context |
| `--format` | No | Output format: `markdown` (default) or `json` |

**3-Layer Waterfall:**

| Layer | Source | Auth | Data |
|-------|--------|------|------|
| 1 | YouTube Autocomplete | None | Related search suggestions |
| 2 | Google Trends (pytrends) | None | Interest over time, rising queries, related topics |
| 3 | YouTube MCP (`mcp__youtube__searchVideos`, `mcp__youtube__getVideoDetails`) | Platform-level MCP | Competitor tags, video metadata |

**Output Sections:**
- **HIGH-SIGNAL Keywords** — appearing in 2+ layers (priority for title wording)
- **RISING / BREAKOUT Terms** — trending opportunities from Google Trends
- **Competitor Tags** — tags from top-performing videos in the niche
- **Suggested SEO Tags** — curated list for YouTube description

**Key Mechanics:**
- Layers are independent — if one fails, others still run
- Layer 3 is optional (requires YouTube MCP connection) — script works fine with just Layers 1-2
- Cross-references results across layers to identify high-signal keywords
- Non-blocking in workflow context — script failure should never gate the workflow
