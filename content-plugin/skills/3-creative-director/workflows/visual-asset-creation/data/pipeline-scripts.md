# Pipeline Script CLI Reference

## 1. YouTube Thumbnail — generate-thumbnail.py

**Script:** `scripts/generate-thumbnail.py`
**Runtime:** Python 3.10+ | Gemini API
**Model:** `gemini-3-pro-image-preview`

```bash
python scripts/generate-thumbnail.py \
    --ref-dir reference-photos \
    --inspo-dir inspiration \
    --output output/thumbnails/combo-01.png \
    --prompt "YouTube thumbnail: ..."
```

| Flag | Required | Description |
|------|----------|-------------|
| `--ref-dir` | Yes | Directory containing creator reference photos |
| `--inspo-dir` | Yes | Directory containing inspiration thumbnails |
| `--output` | Yes | Output file path for the generated thumbnail |
| `--prompt` | Yes | Full text prompt for thumbnail generation |

**Orchestration Rules:**
- Run combos sequentially — NEVER parallelise (rate limiting)
- If a combo fails, report the error and continue to the next
- Maximum 5 combinations per batch
- Always pair a thumbnail with its title — never present one without the other
- Run CTR validation on every generated combo

**Key Mechanics:**
- Reference photos loaded in strict order (foundation image first)
- Up to 14 images total per call, up to 5 human faces
- 3-5 reference photos is the sweet spot
- Typical output: single PNG, 500-650 KB

---

## 2. General Image — generate-image.py

**Script:** `scripts/generate-image.py`
**Runtime:** Python 3.10+ | Gemini API
**Model:** `gemini-3-pro-image-preview`

```bash
# Text-only generation
python scripts/generate-image.py \
    --prompt "A dark comparison graphic showing N8N vs BMAD logos" \
    --output output/images/comparison.png

# With input images
python scripts/generate-image.py \
    --prompt "Combine these logos into a horizontal comparison" \
    --input logos/n8n.svg \
    --input logos/bmad.png \
    --output output/images/comparison.png
```

| Flag | Required | Description |
|------|----------|-------------|
| `--prompt` | Yes | Text prompt for image generation |
| `--output` | Yes | Output file path |
| `--input` | No | Input image path (repeatable — use multiple `--input` flags) |

**Supported MIME types:** JPEG, PNG, GIF, WebP, SVG

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
- `photo-title` — Gemini-generated photo as full-bleed bg with gradient overlay, headline at bottom-left. When last slide: green "Follow" pill bubble instead of SWIPE. Requires `"photoPath"`. Optional `"ctaText"` for the bubble (default: "Follow for more")
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

## 4. Instagram Carousel — generate-instagram-carousel.py

**Script:** `scripts/generate-instagram-carousel.py`
**Runtime:** Python 3.10+ | OpenRouter API
**Model:** `google/gemini-3-pro-image-preview` (nano banana pro, routed via OpenRouter)
**Auth:** `OPENROUTER_API_KEY` in `.env`

```bash
python3 scripts/generate-instagram-carousel.py \
    --input slides.json \
    --output-dir ./output/instagram/
```

| Flag | Required | Description |
|------|----------|-------------|
| `--input` | Yes | Path to JSON file with per-slide definitions |
| `--output-dir` | Yes | Output directory for generated slide PNGs |
| `--slides` | No | Comma-separated slide numbers to regenerate (e.g., '1,7') |

**JSON Input Schema:**
```json
{
  "slides": [
    {
      "slide_number": 1,
      "prompt": "Using the attached photo of this person as the base image, ...",
      "photo_path": "/path/to/real-photo.png",
      "embed_images": []
    },
    {
      "slide_number": 2,
      "prompt": "Generate a 1080x1350 portrait Instagram slide. ...",
      "embed_images": ["./screenshots/terminal.png"]
    },
    {
      "slide_number": 7,
      "prompt": "Generate a 1080x1350 portrait Instagram slide. ...",
      "embed_images": []
    }
  ]
}
```

**Slide fields:**
- `slide_number` — sequential number (1-10)
- `prompt` — full Gemini text prompt for this slide
- `photo_path` — (optional) path to a real photo for Gemini to composite text around (used on hook slide)
- `embed_images` — array of file paths for screenshots/images to incorporate into the slide

**Key Mechanics:**
- Each slide is a separate OpenRouter chat-completions call (routed to Google's nano banana pro) with its own unique prompt
- Embedded images are loaded as base64 data-URIs and sent alongside the prompt — the model composes them into the design
- For slides with `photo_path`, the real photo is sent as the first content part — the model analyses it and composites text around the person
- 2s delay between API calls (rate limiting)
- Maximum 10 slides per carousel
- Output: `slide-01.png`, `slide-02.png`, etc.

---

## 5. Instagram Scheduling — schedule-instagram-post.py

**Script:** `scripts/schedule-instagram-post.py`
**Runtime:** Python 3.10+
**Auth:** `INTERNAL_CRM_SUPABASE_URL` + `INTERNAL_CRM_APG_API_KEY` in `.env`

```bash
# Carousel from directory of PNGs
python3 scripts/schedule-instagram-post.py \
    --caption "Your caption..." \
    --media-dir ./output/instagram/ \
    --scheduled-at "2026-03-10T09:00:00+11:00"

# Single image
python3 scripts/schedule-instagram-post.py \
    --file path/to/caption.md \
    --media path/to/image.png
```

| Flag | Required | Description |
|------|----------|-------------|
| `--file` | No* | Path to caption markdown file (strips frontmatter) |
| `--caption` | No* | Inline caption text (*one of `--file` or `--caption` required) |
| `--scheduled-at` | No | ISO 8601 datetime. Omit for immediate posting |
| `--media` | No | Path to single media file |
| `--media-dir` | No | Directory of numbered slide PNGs (carousel mode) |

**Instagram account_id:** `a2867c79-f288-4a16-898b-5f12ed71513c`

---

## 6. Logo Fetch — fetch-logo.ts

**Script:** `scripts/fetch-logo.ts`
**Runtime:** Node.js 20+ | TypeScript (tsx), Sharp
**Dependency:** `sharp` (add to `scripts/package.json`) — handles SVG→PNG via libvips

**Output is always PNG (512×512, transparent background).** SVGs are fetched internally and converted before saving — Gemini does not accept SVG input.

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
**Auth:** Optional `YOUTUBE_API_KEY` in `.env` for Layer 3

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
| 3 | YouTube Data API v3 | `YOUTUBE_API_KEY` | Competitor tags, video metadata |

**Output Sections:**
- **HIGH-SIGNAL Keywords** — appearing in 2+ layers (priority for title wording)
- **RISING / BREAKOUT Terms** — trending opportunities from Google Trends
- **Competitor Tags** — tags from top-performing videos in the niche
- **Suggested SEO Tags** — curated list for YouTube description

**Key Mechanics:**
- Layers are independent — if one fails, others still run
- Layer 3 is optional (requires API key) — script works fine with just Layers 1-2
- Cross-references results across layers to identify high-signal keywords
- Non-blocking in workflow context — script failure should never gate the workflow
