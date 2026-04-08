# Brand Design Tokens

## Company

| Field | Value |
|-------|-------|
| Company | SOFTWARE |
| Author | {YOUR_NAME} |

## Colour Palette

| Role | Hex | Usage |
|------|-----|-------|
| Background | `#000000` | Slide/thumbnail base |
| Surface | `#111111` | Card/panel backgrounds (elevated from pure black) |
| Border subtle | `#1A1A1A` | Card borders, dividers |
| Brand green | `#90F23C` | Headlines, accents, SWIPE text |
| Glow accent | `#90F23C` at 8-12% opacity | Subtle background glow effects |
| Headline text | `#ffffff` | White |
| Body text | `#999999` | Muted grey |
| CTA button | `#90F23C` | Neon lime |
| CTA button text | `#000000` | Black on button |
| Author text | `#ffffff` | White |
| Page counter | `#666666` | Dark grey |
| Canvas background | `#1a1a2e` | Dark navy (logo canvas default) |
| Short-form background | `#0D0D0D` | Near-black (vertical thumbnails) |
| Short-form banner | `#90F23C` | Neon lime (scroll-stopper text) |
| Gradient start | `#90F23C` | 100% opacity end of brand gradients |
| Gradient end | `#90F23C00` | 0% opacity fade |

## Typography

| Field | Value |
|-------|-------|
| Primary font | DM Sans |
| Weights | 400, 500, 700 |
| Source | `https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap` |

## Standard Dimensions

| Asset Type | Width | Height | Aspect |
|-----------|-------|--------|--------|
| YouTube Thumbnail (wide) | 1280 | 720 | 16:9 |
| Short-form Thumbnail (vertical) | 1080 | 1920 | 9:16 |
| LinkedIn Carousel / Single Image | 1080 | 1080 | 1:1 |
| Instagram Carousel | 1080 | 1350 | 4:5 |
| Landscape Capture | 1920 | 1080 | 16:9 |

## Reference Photos (Identity Preservation)

| Field | Value |
|-------|-------|
| Location | `{reference_photos_folder}` (from CCS config) |
| Subject | {YOUR_NAME} |
| Usage | Load as input images for Gemini identity preservation — thumbnails, general images with people |
| Default | **Always use these** when generating images that include a person, unless user specifies otherwise |

**Photos (load in this exact order):**

| # | File | Purpose |
|---|------|---------|
| 1 | `adam-hero-front.jpg` | Foundation — ALWAYS load first |
| 2 | `adam-3quarter-left.jpg` | Left angle identity |
| 3 | `adam-3quarter-right.jpg` | Right angle identity |
| 4 | `adam-smiling.jpg` | Smiling expression reference |
| 5 | `adam-talking.jpg` | Speaking expression reference |

**Rules:**
- 3-5 photos is the sweet spot — all 5 recommended
- Foundation image (hero-front) MUST be first
- Never describe Adam's face in the text prompt — reference photos handle identity
- If generating any image with a person, assume it should be Adam unless explicitly told otherwise

## Brand Modes (Instagram Carousel)

### {YOUR_COMPANY} (Dark Mode)

| Role | Value |
|------|-------|
| Account | @{YOUR_HANDLE} |
| ICP | SME founders & decision-makers (30-55, $500K-$10M revenue) |
| Background | #000000 (pure black) |
| Surface | #111111 |
| Border | #1A1A1A |
| Headline text | #FFFFFF |
| Body text | #CCCCCC |
| Accent | #90F23C |
| Logo | `{brand_assets}/apg-logo-dark.png` — top-right on every slide |
| Handle | @{YOUR_HANDLE} (bottom-left, content slides) |
| Caption tone | Professional but accessible. ROI-focused. "We built this" energy. |
| Logos colour | White-on-transparent (--color ffffff) |

### {YOUR_NAME} (Light Mode)

| Role | Value |
|------|-------|
| Account | @{YOUR_HANDLE_PERSONAL} |
| ICP | Aspiring AI builders (20-35, developers, career-switchers) |
| Background | #F5F5F5 (off-white) |
| Surface | #FFFFFF (white cards) |
| Border | #E5E5E5 (light grey) |
| Headline text | #111111 (near-black) |
| Body text | #444444 (dark grey) |
| Accent | #90F23C |
| Logo | None (personal brand — no company logo) |
| Handle | @{YOUR_HANDLE_PERSONAL} (bottom-left, content slides) |
| Caption tone | Casual, direct, builder-to-builder. "I just built this" energy. Anti-guru. |
| Logos colour | Dark-on-transparent (no --color flag, or --color 111111) |

## Brand Placement Rules

### Carousel / Single Image

- **Company name** (`SOFTWARE`): Top-right, green (#90F23C), 20px, 700 weight
- **Author name** (`{YOUR_NAME}`): Bottom-left, white, 22px, 400 weight
- **Green accent bar**: Left edge, 4px wide, 100px tall (body/title slides)

### JSON Config Schema (for generate-carousel.js)

```json
{
  "branding": {
    "company": "SOFTWARE",
    "author": "{YOUR_NAME}"
  }
}
```
