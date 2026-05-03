# Short-Form Thumbnail Style Guide (9:16)

## Format

- **Aspect ratio:** 9:16 (1080x1920) — vertical short-form
- **Use case:** YouTube Shorts, TikTok, Instagram Reels covers

## Composition Blueprint

```
+-------------------------+
|   [TOPIC ICON/LOGO]     |  <- Top zone: main topic brand/icon (10-15% from top)
|                         |
|     +---+   +---+      |
|     | A |   | B |      |  <- Floating icons: 2 icons/logos
|     +---+   +---+      |     flanking face, slight 3D tilt
|                         |
|      +-----------+      |
|      |           |      |  <- Person: centered, chest-up crop
|      |   FACE    |      |     head in upper-center area
|      |           |      |
|      +-----------+      |
|                         |
|  DESCRIPTIVE LINE       |  <- Text line 1: white, regular weight, ALL CAPS
|  #### HOOK TEXT ####    |  <- Text line 2: white bold on GREEN banner
|                         |
|   ### SAFE ZONE ###     |  <- Bottom padding: ~8-10% dark space (150-190px)
+-------------------------+
```

## Zone Breakdown

| Zone | Content | Position | Notes |
|------|---------|----------|-------|
| Top | Main topic brand logo | Top center, ~10-15% from top | Largest icon — establishes topic instantly |
| Mid-flanks | 2 floating icons/logos | Left and right of head | Slight 3D tilt, app-icon rounded-square style |
| Center | Person | Centered, chest/shoulders up | Head in upper third of frame |
| Bottom text | Text block | Bottom 20-25% of frame | 2 lines |
| Bottom padding | Dark empty space | Below text, bottom ~8-10% | CRITICAL: platforms overlay UI here. 150-190px dark space. |

## Typography

**Line 1 — Descriptive context:**
- Content: Short topic descriptor (e.g., "FREE AI AGENT TO")
- Style: White, regular/medium weight, ALL CAPS, sans-serif
- Size: Secondary — smaller than Line 2

**Line 2 — Hook/payoff (scroll-stopper):**
- Content: The punchy payoff (e.g., "AUTOMATE ANY TASK")
- Style: White bold on green/lime rectangle banner
- Size: Primary — largest text on the thumbnail
- ALL CAPS, sans-serif, heavy weight

## Colour Palette

| Role | Hex | Notes |
|------|-----|-------|
| Background | `#0D0D0D` - `#1A1A1A` | Subtle themed texture — NOT flat black |
| Banner | `{brand.colors.primary}` (set in config.yaml) | Bright, saturated — must pop at phone size |
| Banner text | `#FFFFFF` | Bold, high contrast on green |
| Line 1 text | `#FFFFFF` | Regular weight |
| Icons/logos | **Original brand colours ONLY** | YouTube = red (#FF0000), Claude = orange (#E07A3A). NEVER monochrome, greyscale, or white-on-dark. Generic icons white or green. |

## Background Treatment

- Coding topics: Subtle code editor / terminal lines behind person
- AI/agent topics: Neural network nodes, abstract AI geometry
- Tool topics: Faint UI screenshots or tool interfaces
- General: Dark gradient with subtle geometric pattern
- Always **low opacity / blurred** — face and text must pop

## Floating Icons Rules

- **Exactly 2 icons** flanking person's head (left and right)
- **CRITICAL: Logos MUST use their real brand colours** — YouTube red (#FF0000), Claude orange (#E07A3A), etc. Never render brand logos in greyscale, monochrome, or white-on-dark.
- Style: Rounded-square app-icon format, slight 3D perspective tilt
- Size: ~15-20% of frame width each
- Shadow: Subtle drop shadow

## Prompt Template (9:16)

```
Vertical YouTube Shorts thumbnail (9:16, 1080x1920): the person from the reference photos centered, chest-up crop, head in upper-center area.
Expression: [specific expression direction].
Top zone: [main topic logo/icon] centered, 10-15% from top.
Floating icons: [Icon A] on left and [Icon B] on right of head, rounded-square app-icon style with slight 3D tilt. IMPORTANT: all brand logos must use their real brand colours (YouTube = red, Claude = orange) — NEVER monochrome or greyscale.
Text line 1: "[DESCRIPTIVE TEXT]" in white regular weight ALL CAPS, positioned in bottom 20-25%.
Text line 2: "[HOOK TEXT]" in white bold on bright accent-colour (`{brand.colors.primary}` from config.yaml) rectangle banner, below line 1.
Background: [themed texture — NOT flat black] at low opacity behind person.
Bottom padding: 150-190px of dark empty space below green banner (platform UI safe zone).
Style reference: match the composition and colour palette of the provided inspiration thumbnails.
High contrast, bold, mobile-optimised.
```

## Generation Checklist

- [ ] 9:16 aspect ratio specified (1080x1920)
- [ ] Person centered, chest-up, head in upper third
- [ ] Exactly 2 floating icons specified with 3D tilt, using real brand colours (not monochrome)
- [ ] Top brand/topic icon specified
- [ ] Background themed to topic (not flat black)
- [ ] Line 1: white, regular, ALL CAPS — descriptive
- [ ] Line 2: white bold on GREEN/LIME banner — hook
- [ ] Bottom padding: ~8-10% dark space below green banner
- [ ] Expression direction included in prompt
- [ ] Reference photos attached for identity preservation
