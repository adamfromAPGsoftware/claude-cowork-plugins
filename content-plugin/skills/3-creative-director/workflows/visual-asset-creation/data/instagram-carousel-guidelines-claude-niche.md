# Instagram Carousel — Style Guide ({YOUR_NAME} / Claude-Niche)

fal-ai/nano-banana-2 image generation prompt reference for @{YOUR_HANDLE_PERSONAL} Instagram carousels.
This file is the **translation layer** between the JSX design system and fal-ai/nano-banana-2 — it doesn't read JSX components, it reads natural language. Every prompt template here describes what the components render without naming font families (Gemini will render them as literal text).

**Design system source:** `content-plugin/skills/6-autopilot/references/design-system/`
Canonical components: `carousels/SlideFrame.jsx`, `HookSlide.jsx`, `ContentSlide.jsx`, `CodeSlide.jsx`, `ScreenshotSlide.jsx`, `CTASlide.jsx`

---

## 1. Color Tokens

All hex values are sourced directly from `colors_and_type.css`.

### Paper theme (warm cream)

| Token | Hex | Role |
|---|---|---|
| Slide background | `#f5f0e8` | Warm cream canvas |
| Dotted grid dots | `#d8cfc0` | 1.4px dots at 28px cadence |
| Primary ink | `#1a1614` | Headlines, key borders |
| Body text | `#3d3833` | Body copy on paper |
| Muted text | `#9a928c` | Captions, labels at low opacity |
| Panel inset | `#f2ede8` | Slightly darker cream for mono chip bg (on paper the chip is inverted dark) |

### Dark theme

| Token | Hex | Role |
|---|---|---|
| Slide background | `#0f0d0b` | Near-black warm base |
| Gradient terminus | `#0a0706` | Darkest point at bottom of linear gradient |
| Radial glow 1 (top-left) | `#d97757` at 12% opacity | Warm orange bloom, 20% from left, 10% from top |
| Radial glow 2 (bottom-right) | `#d97757` at 8% opacity | Second bloom, 90% from left, 90% from top |
| Grain overlay | `#fafaf8` at 0.5px dots, 35% opacity | Fine noise, 3px cadence, overlay blend mode |
| Headline text | `#fafaf8` | Near-white |
| Body text | `#c9c0b3` | Warm mid-grey |
| Terminal headline | `#f0e6d3` | Warm cream on dark terminal card |

### Accent scale

| Token | Hex | Usage |
|---|---|---|
| `--orange-500` | `#d97757` | THE accent — Accent underlines, eyebrows, borders, CTA bg |
| `--orange-100` | `#f4a387` | Soft/hover — secondary code highlights, soft orange in code |
| `--orange-700` | `#c05f2a` | Orange-as-text on light surfaces |
| `--orange-900` | `#6a3820` | Deep accent for heavy emphasis on cream |
| SerifAccent on dark/hero | `#ffb089` | Lighter warm orange — use instead of `#d97757` when bg is dark or hero so contrast holds |

---

## 2. Typography (model-safe descriptions)

**CRITICAL RULE:** Never name a specific font family in image prompts. The model will render the font name as visible text on the slide. Use the style descriptions below instead.

| Design system role | Font + weight | Model-safe description |
|---|---|---|
| Headline / display | Inter 900 | "bold black-weight sans-serif headline" |
| Heavy heading | Inter 800 | "extra-bold sans-serif heading" |
| Body | Inter 400 | "regular-weight sans-serif body text" |
| Eyebrow / badge label | JetBrains Mono 700, uppercase, 0.22em tracking | "clean monospace uppercase label with wide letter-spacing (0.22em)" |
| Code / terminal text | JetBrains Mono 400–700 | "clean monospace code text" |
| Footer handle | JetBrains Mono 400 | "small monospace handle text" |
| Accent word (SerifAccent) | Instrument Serif italic 400 | "italic serif accent word" |
| Ghost word (GhostWord) | Instrument Serif italic 400 | "massive italic serif ghost word" |

### Size reference (for spatial descriptions)

These are actual pixel sizes from the JSX — describe them as relative proportions:

- Headline on HookSlide: 92px — "very large display headline"
- Headline on ContentSlide: 112px — "massive display headline, the largest text block"
- Headline on CTASlide: 108px — "very large display headline"
- Headline on CodeSlide: 88px — "large bold headline"
- Headline on ScreenshotSlide: 72px — "large heading"
- Eyebrow/badge: 18px monospace — "small uppercase monospace label"
- Body text: 36px — "medium body text"
- Footer: 18px — "small footer text"
- Slide counter: 11px at 35% opacity — "tiny monospace counter, barely visible"

---

## 3. Accent System

Three accent types are used across slides. Each has a precise visual description for the model.

### Accent — block underline word

Used for bold, geometric emphasis. The orange word sits above a solid rectangular bar.

**Model prompt:** "The word '[WORD]' in orange (#d97757), with a solid rectangular orange block directly beneath it — a thick flat 8px horizontal bar, sharp geometric edges, borderRadius 2px. The bar sits flush below the word's baseline. Blocky and technical, NOT a brushstroke or curved line."

On ContentSlide and CTASlide the bar is 12px tall. On HookSlide-derived and ScreenshotSlide it is 8px.

### SerifAccent — italic serif word in orange

Used for softer, editorial emphasis — a single keyword rendered in an italic serif style within an otherwise sans-serif headline.

**Model prompt on paper bg:** "The word '[WORD]' in italic serif style, orange (#d97757). The surrounding headline text remains bold sans-serif upright."

**Model prompt on dark or hero bg:** "The word '[WORD]' in italic serif style, warm orange (#ffb089). The surrounding headline text remains bold sans-serif upright." (Use #ffb089 on dark/hero for contrast — the JSX explicitly uses this value.)

### GhostWord — massive background watermark

A huge italic serif word positioned at bottom-right, partially bleeding off the canvas edge. It is not a design element the reader consciously notices — it is atmosphere.

**Model prompt:** "Behind all content, at the bottom-right corner bleeding off the edge: a massive italic serif word '[WORD]' at roughly 540px — so large it bleeds off canvas. Very low opacity (6-7%). Color: #fafaf8 on dark theme, #1a1614 on paper theme. Line height 0.85, tight tracking. The word should feel like a watermark or shadow, not a readable element."

---

## 4. Slide Type Prompt Templates

### Template: HookSlide (bg: hero — always)

HookSlide always uses the hero background: a real photo of the creator as full-bleed, overlaid with a gradient. The `anchor` prop controls where the text block sits relative to the creator's position in the frame — pick the corner/area where the creator is NOT standing to keep text readable.

**Gradient spec from SlideFrame.jsx:**
```
linear-gradient(180deg,
  rgba(10,7,6,0.35) 0%,    ← top: semi-dark, text readable
  rgba(10,7,6,0.15) 45%,   ← middle: almost clear, shows photo
  rgba(10,7,6,0.90) 100%   ← bottom: dense dark, footer legible
)
```

**Image prompt template (fal-ai/nano-banana-2):**

```
Generate a 1080x1350 portrait Instagram slide. The background is [PHOTO DESCRIPTION] as a full-bleed photo. Over the photo, apply a gradient overlay: top 35% semi-dark (rgba 10,7,6 at 35% opacity), middle zone almost transparent (rgba 10,7,6 at 15% opacity), bottom 45% dense dark (rgba 10,7,6 at 90% opacity).

[IF tab exists] At [ANCHOR POSITION], a large bold black-weight sans-serif number or word "[TAB]" in orange (#d97757), 96px, tight tracking (-0.04em), with text shadow (4px blur, black, 40% opacity).

Directly below [or at] [ANCHOR POSITION]: a bold black-weight sans-serif headline, very large (92px, line-height 0.98, tracking -0.035em), in near-white (#fafaf8), with text shadow (4px blur, black, 45% opacity):
Line 1: "[HEAD1]"
[IF accent] Line 2: "[ACCENT]" — rendered as italic serif accent word in warm orange (#ffb089) with text shadow
[IF head2] Line 3: "[HEAD2]" in near-white

[IF sub] Below the headline (24px gap): italic serif text "[SUB]" at 32px, near-white at 92% opacity, max-width 820px, text shadow (2px blur, black, 50% opacity).

Footer (always visible on every slide):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" in small monospace uppercase text, near-white (#fafaf8) at 75% opacity, 18px, 0.04em tracking
- Bottom-right: "send to a friend" in small monospace, near-white at 85% opacity, followed by a paper plane send icon "✈" inside a 34x34px square outline (1.5px border, borderRadius 4)
- Top-right: a bookmark icon — a geometric flag/bookmark shape (36x40px rectangle with no bottom border and a V-notch cut from the bottom, 2px line, near-white at 80% opacity)
- Centered above footer line: "[INDEX] / [TOTAL]" in tiny monospace (11px), near-white at 35% opacity, very wide tracking (0.25em)

1080x1350 pixels.
```

**Anchor position guidance:**
- Creator bottom-right → use `top-left` anchor (text upper-left)
- Creator bottom-left → use `top-right` anchor (text upper-right)
- Creator center → use `bottom-left` anchor (text lower-left)
- Creator top → use `bottom-left` or `bottom-right` anchor

---

### Template: ContentSlide (bg: paper or dark)

ContentSlide is the workhorse educational slide. It carries a badge eyebrow, massive headline with one accent, body text, an optional mono chip, and the GhostWord watermark at bottom-right.

**Image prompt template — PAPER variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: warm cream (#f5f0e8) with a dotted grid pattern — small dots (#d8cfc0, 1.4px radius) arranged in a 28px × 28px repeating grid, offset 14px from each edge.

Behind all content at the bottom-right corner, bleeding off the canvas edge: a massive italic serif word "[GHOST]" at approximately 540px tall. Very low opacity (6%). Color: #1a1614 (near-black). The word bleeds off the right and bottom edges. Line-height 0.85, tight tracking.

Content block centered vertically on the slide (padding: 64px top, 72px sides, 104px bottom):

1. Badge eyebrow: a small clean monospace uppercase label with wide letter-spacing (0.22em). Color: orange (#d97757). Text: "▶ [BADGE TEXT]". 18px. Margin-bottom 28px.

2. Headline: bold black-weight sans-serif, 112px, line-height 0.94, tracking -0.04em, color #1a1614. Max-width 940px.
   "[TITLE]" — then the word "[ACCENT]" in orange (#d97757) with a solid rectangular orange block beneath it (12px tall, sharp geometric edges, no curve, flush to baseline, borderRadius 2). The bar underlines only that one word.
   [OR if serifAccent:] the word "[SERIFACCENT]" in italic serif style, orange (#d97757). Surrounding text remains bold sans-serif upright.

3. Body text (44px below headline): regular-weight sans-serif, 36px, color #3d3833, line-height 1.35, tracking -0.008em, max-width 900px.
   "[BODY TEXT]"

4. Mono chip (44px below body, optional): a small pill/chip with dark background (#1a1614), 1px solid dark border (#1a1614), borderRadius 8, padding 22px × 28px. Inside: clean monospace text, 24px, color near-white (#f5f0e8).
   "[MONO TEXT]"

Footer (always):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #1a1614 at 60% opacity
- Bottom-right: "send to a friend" small monospace, #1a1614 at 70% opacity, followed by boxed "→" (34x34px, 1.5px border borderRadius 4)
- Top-right: geometric bookmark icon, 2px border, #1a1614 at 80% opacity
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace, #1a1614 at 35% opacity

1080x1350 pixels.
```

**Image prompt template — DARK variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: near-black warm (#0f0d0b) with two soft orange radial glows — one at top-left (20% from left, 10% from top, #d97757 at 12% opacity fading to transparent over 45% radius) and one at bottom-right (90% from left, 90% from top, #d97757 at 8% opacity fading to transparent over 50% radius). Over everything: a fine grain noise overlay — tiny dots (#fafaf8, 0.5px) at 3px cadence, 35% opacity, overlay blend mode.

Behind all content at bottom-right corner, bleeding off the canvas: a massive italic serif word "[GHOST]" at approximately 540px tall. Very low opacity (7%). Color: #fafaf8. Bleeds off right and bottom edges. Line-height 0.85, tight tracking.

Content block centered vertically (padding: 64px top, 72px sides, 104px bottom):

1. Badge eyebrow: small clean monospace uppercase label, wide letter-spacing (0.22em), orange (#d97757). Text: "▶ [BADGE TEXT]". 18px. Margin-bottom 28px.

2. Headline: bold black-weight sans-serif, 112px, line-height 0.94, tracking -0.04em, color #fafaf8. Max-width 940px.
   "[TITLE]" — then the word "[ACCENT]" in orange (#d97757) with solid rectangular orange block beneath (12px, sharp geometric, flush to baseline, borderRadius 2).
   [OR if serifAccent:] the word "[SERIFACCENT]" in italic serif style, warm orange (#ffb089). Surrounding text remains bold sans-serif upright.

3. Body text (44px below headline): regular-weight sans-serif, 36px, color #c9c0b3 (warm mid-grey), line-height 1.35, tracking -0.008em, max-width 900px.
   "[BODY TEXT]"

4. Mono chip (44px below body, optional): pill/chip with subtle orange-tinted dark background (rgba 217,119,87 at 8%), 1px solid border (rgba 217,119,87 at 40%), borderRadius 8, padding 22px × 28px. Inside: clean monospace text, 24px, soft orange (#f4a387).
   "[MONO TEXT]"

Footer (always):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #fafaf8 at 75% opacity
- Bottom-right: "send to a friend" small monospace, #fafaf8 at 85% opacity, followed by boxed "→" (34x34px, 1.5px border borderRadius 4, near-white)
- Top-right: geometric bookmark icon, 2px border, #fafaf8 at 80% opacity
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace, #fafaf8 at 35% opacity

1080x1350 pixels.
```

---

### Template: CodeSlide (bg: dark or paper)

CodeSlide shows a Claude prompt in a terminal-style card. The terminal card is ALWAYS dark — even on the paper variant. On paper the dark card appears inverted (dark on cream), which is intentional and striking.

**Key specs from CodeSlide.jsx:**
- Eyebrow: `▶ SEND THIS TO CLAUDE` (or custom eyebrow text) — monospace, 18px, uppercase, 0.22em tracking, orange
- Headline: bold black-weight sans-serif, 88px, line-height 0.98, tracking -0.035em
- Terminal card: `background rgba(10,7,6,0.6)` on dark, `#1a1614` solid on paper. Border: `2px solid #d97757`. borderRadius 20. Padding 44px × 48px.
- Terminal shadow on dark: `0 0 50px rgba(217,119,87,0.18)` (glow). On paper: `0 20px 50px rgba(26,22,20,0.18)` (blocky drop shadow).
- Code text base color: `#e8ddc8` (warm cream)
- Orange keywords: `#d97757`
- Soft orange secondary highlights: `#f4a387`

**Image prompt template — DARK variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: near-black warm (#0f0d0b) with soft orange radial glows (top-left: #d97757 at 12% opacity; bottom-right: #d97757 at 8% opacity) and fine grain noise overlay (tiny dots at 35% opacity, overlay blend).

Padding: 64px top, 72px sides, 104px bottom.

1. Eyebrow (top): small clean monospace uppercase label, wide letter-spacing (0.22em), orange (#d97757), 18px. A play symbol "▶" followed by "[EYEBROW TEXT — default: SEND THIS TO CLAUDE]". Inline, left-aligned.

2. Headline (below eyebrow, 20px gap): bold black-weight sans-serif, 88px, line-height 0.98, tracking -0.035em, color #fafaf8. Max-width 940px.
   "[HEAD1]" — then "[ACCENT]" in orange (#d97757) with solid rectangular orange block underline (10px, geometric, flush, borderRadius 2).
   [OR serifAccent:] "[SERIFACCENT]" in italic serif style, warm orange (#ffb089), surrounded by upright bold sans-serif.
   [IF head2:] new line "[HEAD2]" in #fafaf8.

3. Terminal card (36px below headline, fills remaining vertical space): a large rounded rectangle. Background: very dark near-black (rgba 10,7,6 at 60%), 2px solid orange border (#d97757), borderRadius 20, padding 44px × 48px, soft orange glow shadow (0 0 50px rgba 217,119,87 at 18%). Content centered vertically inside.

   Inside the terminal: clean monospace text, 30px, line-height 1.5. Base text color warm cream (#e8ddc8). Key terms in orange (#d97757). Secondary highlights in soft orange (#f4a387). Empty lines are real line breaks (spacing). Render exactly:
   [CODE LINES — list each line, specifying color for each segment]

Footer (always):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #fafaf8 at 75% opacity
- Bottom-right: "send to a friend" small monospace, #fafaf8 at 85% opacity, boxed "→"
- Top-right: geometric bookmark icon, #fafaf8
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35% opacity

1080x1350 pixels.
```

**Image prompt template — PAPER variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: warm cream (#f5f0e8) with dotted grid (dots #d8cfc0, 1.4px radius, 28px cadence, 14px offset).

Padding: 64px top, 72px sides, 104px bottom.

1. Eyebrow: small clean monospace uppercase label, wide letter-spacing (0.22em), orange (#d97757), 18px. "▶ [EYEBROW TEXT]". Left-aligned.

2. Headline: bold black-weight sans-serif, 88px, line-height 0.98, tracking -0.035em, color #1a1614. Max-width 940px.
   "[HEAD1]" — "[ACCENT]" in orange (#d97757) with solid rectangular orange block underline (10px, geometric, flush, borderRadius 2).
   [OR serifAccent:] "[SERIFACCENT]" in italic serif style, orange (#d97757), surrounded by upright bold sans-serif.
   [IF head2:] new line "[HEAD2]" in #1a1614.

3. Terminal card (36px below headline, fills remaining space): DARK card on cream background (inverted). Background: solid dark near-black (#1a1614), 2px solid orange border (#d97757), borderRadius 20, padding 44px × 48px, blocky drop shadow (0 20px 50px rgba 26,22,20 at 18%). Content centered vertically.

   Inside: clean monospace text, 30px, line-height 1.5. Base color warm cream (#e8ddc8). Key terms orange (#d97757). Secondary highlights soft orange (#f4a387).
   [CODE LINES]

Footer (always):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #1a1614 at 60% opacity
- Bottom-right: "send to a friend" small monospace, #1a1614 at 70% opacity, boxed "→"
- Top-right: geometric bookmark icon, #1a1614 at 80% opacity
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35% opacity

1080x1350 pixels.
```

---

### Template: ScreenshotSlide (bg: dark or paper)

ScreenshotSlide shows a tool screenshot or UI inside a framed area with a macOS-style fake title bar. The frame has three colored dot buttons (orange, soft orange, muted) and a monospace path label.

**Key specs from ScreenshotSlide.jsx:**
- Headline: bold black-weight sans-serif, 72px, line-height 1.0, tracking -0.03em
- Frame on dark: background `#15110e`, border `2px solid rgba(217,119,87,0.4)`, borderRadius 14, padding 14, shadow `0 0 40px rgba(217,119,87,0.15)` (glow)
- Frame on paper: background `#fafaf8`, border `2px solid #1a1614`, borderRadius 14, padding 14, shadow `8px 8px 0 #1a1614` (blocky offset shadow)
- Title bar dots: orange `#d97757`, soft orange `#f4a387`, muted (dark: `#2a1f18`, paper: `#d8d2cc`). Each 12px circle.
- Path label in title bar: small monospace, `~/claude-code · preview` style
- Screenshot fill area: diagonal stripe pattern background + dashed border (placeholder for real screenshot image)
- Caption: 26px regular sans-serif, below the frame

**Image prompt template — DARK variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: near-black warm (#0f0d0b) with soft orange radial glows and fine grain noise overlay (as per dark theme spec).

Padding: 64px top, 72px sides, 104px bottom.

1. Eyebrow: small clean monospace uppercase label, wide letter-spacing (0.22em), orange (#d97757). "▶ [EYEBROW TEXT]". 18px, left-aligned.

2. Headline (16px below eyebrow): bold black-weight sans-serif, 72px, line-height 1.0, tracking -0.03em, color #fafaf8.
   "[TITLE]" — "[ACCENT]" in orange (#d97757) with solid rectangular orange block underline (8px, geometric, flush, borderRadius 2).

3. Screenshot frame (32px below headline, fills remaining vertical space): a large framed area.
   - Outer container: background #15110e, 2px solid border (rgba 217,119,87 at 40%), borderRadius 14, padding 14, outer glow shadow (0 0 40px rgba 217,119,87 at 15%).
   - Fake title bar inside top of frame: three small circles (12px each) — first circle orange (#d97757), second soft orange (#f4a387), third muted dark (#2a1f18). 8px gap between circles. To the right of dots: small monospace label "[PATH LABEL — e.g. ~/claude-code · preview]" in dim warm brown (#7a6b5a).
   - Below title bar: fill with the actual screenshot image [INSERT SCREENSHOT]. The screenshot fills the remaining frame area. If no screenshot yet: diagonal stripe placeholder in very dark warm tones with a dashed orange border and centered monospace label "[SCREENSHOT PLACEHOLDER LABEL]" in orange.

4. Caption (24px below frame, optional): regular-weight sans-serif, 26px, color #c9c0b3, line-height 1.4, max-width 900px.
   "[CAPTION]"

Footer (always):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #fafaf8 at 75% opacity
- Bottom-right: "send to a friend" small monospace, #fafaf8 at 85% opacity, boxed "→"
- Top-right: geometric bookmark icon, #fafaf8 at 80%
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35%

1080x1350 pixels.
```

**Image prompt template — PAPER variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: warm cream (#f5f0e8) with dotted grid (dots #d8cfc0, 1.4px, 28px cadence).

Padding: 64px top, 72px sides, 104px bottom.

1. Eyebrow: small clean monospace uppercase label, 0.22em tracking, orange (#d97757). "▶ [EYEBROW TEXT]". 18px, left-aligned.

2. Headline: bold black-weight sans-serif, 72px, line-height 1.0, tracking -0.03em, color #1a1614.
   "[TITLE]" — "[ACCENT]" in orange (#d97757) with solid rectangular orange block underline (8px, geometric, borderRadius 2).

3. Screenshot frame (fills remaining space): 
   - Outer container: background #fafaf8, 2px solid border #1a1614, borderRadius 14, padding 14, blocky offset shadow (8px 8px 0 #1a1614 — hard shadow, no blur).
   - Title bar: three circles — orange (#d97757), soft orange (#f4a387), muted (#d8d2cc). Monospace path label (#7a726b): "[PATH LABEL]".
   - Below: screenshot image [INSERT SCREENSHOT], or diagonal stripe placeholder with dashed border (#b9b2ab) and centered monospace label in warm brown.

4. Caption: regular-weight sans-serif, 26px, color #3d3833, line-height 1.4, max-width 900px.
   "[CAPTION]"

Footer (always):
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #1a1614 at 60% opacity
- Bottom-right: "send to a friend" small monospace, #1a1614 at 70% opacity, boxed "→"
- Top-right: geometric bookmark icon, #1a1614 at 80%
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35%

1080x1350 pixels.
```

---

### Template: CTASlide (bg: dark, paper, or hero)

CTASlide is always the last slide. It uses `showNextHint={false}` — the "send to a friend" box-arrow is NOT shown, but @{YOUR_HANDLE_PERSONAL} still appears. The GhostWord appears on dark and paper variants (not on hero — the photo does that job).

**Key specs from CTASlide.jsx:**
- Eyebrow: same monospace uppercase label as other slides, typically "▶ YOUR TURN" or custom
- Headline: 108px, line-height 1.02, tracking -0.04em
- Sub text: italic serif, 34px, line-height 1.3
- CTA button: background #d97757, text #0a0706 (very dark), padding 26px × 34px, borderRadius 12, monospace bold 28px with "→" appended, box-shadow `0 12px 32px rgba(217,119,87,0.4)`

**Image prompt template — DARK variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: near-black warm (#0f0d0b) with soft orange radial glows and grain overlay.

Behind all content at bottom-right, bleeding off canvas: a massive italic serif word "[GHOST]" at ~540px, near-white (#fafaf8) at 7% opacity, bleeding off right and bottom edges.

Content block centered vertically (padding: 64px top, 72px sides, 104px bottom):

1. Eyebrow: small clean monospace uppercase label, 0.22em tracking, orange (#d97757). "▶ [EYEBROW TEXT — e.g. YOUR TURN]". 18px. Margin-bottom 24px.

2. Headline: bold black-weight sans-serif, 108px, line-height 1.02, tracking -0.04em, color #fafaf8. Max-width 940px.
   "[HEAD1]"
   New line: "[ACCENT]" — in orange (#d97757) with solid rectangular block underline (12px, geometric, flush, borderRadius 2).
   [OR serifAccent:] "[SERIFACCENT]" in italic serif style, warm orange (#ffb089).
   [IF head2:] new line "[HEAD2]" in #fafaf8.

3. Sub text (64px below headline): italic serif style, 34px, color #fafaf8 at 92% opacity, line-height 1.3, max-width 880px.
   "[SUB TEXT]"

4. CTA button (48px below sub text): an inline button element — background orange (#d97757), very dark text (#0a0706), padding 26px top/bottom × 34px left/right, borderRadius 12, soft drop shadow (0 12px 32px rgba 217,119,87 at 40%). Inside: bold monospace text, 28px, wide tracking, "[CTA TEXT] →"

Footer — NOTE: NO "send to a friend" box on CTA slide:
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #fafaf8 at 75% opacity
- Bottom-right: [EMPTY — no save-for-later on CTA slide]
- Top-right: geometric bookmark icon, #fafaf8 at 80%
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35%

1080x1350 pixels.
```

**Image prompt template — PAPER variant:**

```
Generate a 1080x1350 portrait Instagram slide.

Background: warm cream (#f5f0e8) with dotted grid (dots #d8cfc0, 28px cadence).

Behind all content at bottom-right, bleeding off canvas: massive italic serif word "[GHOST]" at ~540px, color #1a1614 at 5% opacity, bleeding off right and bottom edges.

Content block centered vertically (padding: 64px top, 72px sides, 104px bottom):

1. Eyebrow: small monospace uppercase label, 0.22em tracking, orange (#d97757). "▶ [EYEBROW TEXT]". 18px.

2. Headline: bold black-weight sans-serif, 108px, line-height 1.02, tracking -0.04em, color #1a1614. Max-width 940px.
   "[HEAD1]" — new line — "[ACCENT]" in orange (#d97757) with 12px geometric block underline.
   [OR serifAccent:] "[SERIFACCENT]" in italic serif style, orange (#d97757), upright bold sans-serif surrounding text.

3. Sub text: italic serif, 34px, color #3d3833, line-height 1.3, max-width 880px.
   "[SUB TEXT]"

4. CTA button: orange bg (#d97757), very dark text (#0a0706), padding 26px × 34px, borderRadius 12, drop shadow. Bold monospace 28px. "[CTA TEXT] →"

Footer — NO save-for-later:
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #1a1614 at 60% opacity
- Bottom-right: [EMPTY]
- Top-right: geometric bookmark icon, #1a1614 at 80%
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35%

1080x1350 pixels.
```

**Image prompt template — HERO variant (photo CTA):**

```
Generate a 1080x1350 portrait Instagram slide. Background: [PHOTO] as full-bleed with gradient overlay (rgba 10,7,6 at 35% top, 15% at 45%, 90% at 100% — dense dark at bottom).

[NO ghost word — photo is sufficient]

Content block anchored to bottom of canvas (before footer zone):

1. Eyebrow: small monospace uppercase label, orange (#d97757). "▶ [EYEBROW TEXT]".

2. Headline: bold black-weight sans-serif, 108px, line-height 1.02, tracking -0.04em, near-white (#fafaf8), text-shadow (4px blur, black, 50%). Max-width 940px.
   [HEAD1 / ACCENT / SERIFACCENT / HEAD2 as needed]

3. Sub text: italic serif, 34px, near-white at 92% opacity, line-height 1.3, text-shadow (2px blur, black, 50%). "[SUB TEXT]"

4. CTA button: orange bg (#d97757), very dark text (#0a0706), bold monospace 28px, borderRadius 12, drop shadow. "[CTA TEXT] →"

Footer — NO save-for-later:
- Bottom-left: "@{YOUR_HANDLE_PERSONAL}" small monospace, #fafaf8 at 75%
- Bottom-right: [EMPTY]
- Top-right: geometric bookmark icon, #fafaf8
- Centered above footer: "[INDEX] / [TOTAL]" tiny monospace at 35%

1080x1350 pixels.
```

---

## 5. Theme Selection

| Theme | Background | Use for |
|---|---|---|
| **Paper** | Warm cream `#f5f0e8` + dotted grid | Educational, step-by-step, beginner-friendly, skill tutorials |
| **Dark** | `#0f0d0b` + orange radial glows + grain | Technical, code-heavy, agentic, agency/OS content |
| **Hero** | Photo full-bleed + dark gradient overlay | Hook slides only. Never use hero for content or code slides. |

**Mixing themes across a carousel is allowed.** CAROUSEL_1 (from content.jsx) uses paper throughout. CAROUSEL_2 uses dark throughout. Mixing (e.g. hero hook → dark content slides) is valid.

---

## 6. Structural Patterns

Two canonical carousel structures from `content.jsx`:

### CAROUSEL_1 — Skill tutorial (paper theme throughout)

| Slide | Type | Key elements |
|---|---|---|
| 1 | HookSlide (hero) | Photo bg, `anchor: "top-left"`, orange number tab, headline with SerifAccent |
| 2 | ContentSlide (paper) | badge "skill · 01", ghost word, headline + Accent, body, mono chip |
| 3 | CodeSlide (paper) | eyebrow "Send this to Claude", headline + SerifAccent, dark terminal card on cream |
| 4 | ContentSlide (paper) | badge "skill · 02", ghost word, headline + Accent, body, mono chip |
| 5 | ContentSlide (paper) | badge "skill · 03", ghost word, headline + Accent, body, mono chip |
| 6 | CodeSlide (paper) | eyebrow "Send this to Claude", headline + SerifAccent, dark terminal card |
| 7 | ContentSlide (paper) | badge "skill · 04", ghost word, headline + Accent, body, mono chip |
| 8 | ScreenshotSlide (paper) | eyebrow, headline + Accent, framed screenshot, caption |
| 9 | CTASlide (paper) | eyebrow "your turn", headline + SerifAccent, ghost word, sub, CTA button |

### CAROUSEL_2 — Perspective shift (dark theme throughout)

| Slide | Type | Key elements |
|---|---|---|
| 1 | HookSlide (hero) | Photo bg, `anchor: "bottom-right"`, tab "NEW", headline + SerifAccent |
| 2 | ContentSlide (dark) | badge "the problem", ghost word, headline + Accent, body, mono chip |
| 3 | ContentSlide (dark) | badge "the shift", ghost word, headline + Accent, body, mono chip |
| 4 | CodeSlide (dark) | eyebrow "Send this to Claude", headline + SerifAccent, terminal card with glow |
| 5 | ScreenshotSlide (dark) | eyebrow, headline + Accent, framed screenshot with glow, caption |
| 6–7 | ContentSlide (dark) | badge, ghost word, headline + Accent/SerifAccent, body, mono chip |
| 8 | CTASlide (dark) | eyebrow "get the stack", headline + SerifAccent, ghost word, sub, CTA button |

---

## 7. Footer Chrome (Every Slide)

All slides share the same footer chrome from SlideFrame.jsx. Describe it consistently in every image prompt.

**@{YOUR_HANDLE_PERSONAL} handle:**
- Bottom-left, 18px, small monospace uppercase text, wide tracking (0.04em)
- Paper: `#1a1614` at 60% opacity
- Dark/hero: `#fafaf8` at 75% opacity

**"send to a friend" send icon (ALL slides EXCEPT CTASlide):**
- Bottom-right: text "send to a friend" in same monospace style, then a paper plane send icon "✈" inside a boxed square
- Box: 34×34px, 1.5px border, borderRadius 4, same color as handle
- Paper: `#1a1614` at 70% opacity
- Dark/hero: `#fafaf8` at 85% opacity
- **CTASlide: omit entirely — the right side of the footer is empty**

**Bookmark icon (top-right, every slide):**
- A geometric bookmark/flag shape: 36×40px rectangle with no bottom border + a rotated square (18×18px) at the bottom center creating a V-notch point. 2px border, borderRadius 0.
- Paper: `#1a1614` at 80% opacity
- Dark/hero: `#fafaf8` at 80% opacity

**Slide counter (centered above footer):**
- Positioned above the footer line (not overlapping @{YOUR_HANDLE_PERSONAL})
- Format: `01 / 07` — both padded to 2 digits
- 11px, monospace, 0.25em tracking, near-white or near-black at 35% opacity

---

## 8. What NOT to Do

**Typography:**
- Never name Inter, JetBrains Mono, or Instrument Serif in an image prompt — they render as visible text
- Never use all-caps for headlines — always sentence case or mixed-case
- Never use a brushstroke, curved, or hand-drawn underline — the Accent is a solid rectangular bar

**Colors:**
- Never use cold blue-black as a background — always the warm near-black (#0f0d0b / #0a0706)
- Never use `{brand.colors.primary}` (set in config.yaml) on Claude-niche slides — that is the company brand, not the personal carousel brand
- Never make all code text the same color — orange syntax highlighting on key terms is mandatory

**Accents:**
- Never use SerifAccent color `#d97757` on a dark or hero background — use `#ffb089` for contrast
- Never use a thin hairline border on the terminal card — it must be 2px solid orange
- Never add a glow to the paper-theme screenshot frame — use the blocky hard offset shadow instead (`8px 8px 0 #1a1614`)

**Layout:**
- Never omit the GhostWord on ContentSlide and CTASlide (dark/paper variants) — it is always present
- Never show "send to a friend" on the CTASlide — `showNextHint={false}` on the last slide
- Never put the Accent block underline on the wrong word — it underlines ONE word only, the accent word
- Never use a swipe cue arrow separate from the footer "send to a friend" box — the send icon lives inside the box
- Never mix hero theme with ContentSlide or CodeSlide — hero is hook-only

**Content:**
- No emoji anywhere — only typographic glyphs: `→`, `▶`, `·`
- No open questions as CTAs — use keyword comment triggers ("comment 'CLAUDE'") or mic-drop closers
- No gear logo — this is personal brand content, no company logo

---

## 9. Hook Slide Photo Planning

When using a real photo of the creator as the hero background:

**Step 1 — Choose the photo.**
Available photos: `context/brand-assets/reference-photos/`
Current files: `IMG_7883.jpg`, `IMG_7884.jpg`, `IMG_7885.jpg`, `IMG_7886.jpg`, `IMG_7887.jpg`
View each photo and assess where the creator is positioned in the frame.

**Step 2 — Select the anchor.**
The text block must NOT cover the creator's face. Place text where the creator is NOT.

| Creator's position in frame | Use anchor |
|---|---|
| Bottom-right | `top-left` |
| Bottom-left | `top-right` |
| Bottom-center | `top-left` or `top-right` |
| Top-right | `bottom-left` |
| Top-left | `bottom-right` |
| Center | `bottom-left` |

**Step 3 — Describe the gradient.**
Always use the exact gradient from SlideFrame.jsx:
- Top (0%): rgba(10,7,6,0.35) — semi-dark
- Mid (45%): rgba(10,7,6,0.15) — almost clear, creator's face visible
- Bottom (100%): rgba(10,7,6,0.90) — dense dark for footer legibility

**Step 4 — Apply text shadows.**
Every text element on a hero slide needs text shadow: `0 4px 24px rgba(0,0,0,0.45)` on the headline, `0 2px 12px rgba(0,0,0,0.50)` on sub text. This is what keeps text readable over any photo.

**Step 5 — If no creator photo is available:**
Check `content-plugin/skills/6-autopilot/references/hook-slide-inspiration/` for inspiration frames, or use a Claude interface screenshot as the hero visual (screenshot-forward hook variant from the old guide). In that case, use a dark theme ContentSlide-style background instead of hero.

---

## 10. Reference Screenshots

Available at `context/brand-assets/reference-frames/`. Use as inputs for ScreenshotSlide frames and HookSlide screenshot-forward hooks.

| Topic | Directory | Best for |
|---|---|---|
| Claude Code terminal interface | `claude-code/` | Hook slides showing Claude Code; CodeSlide references |
| Claude chat (web) | `claude-chat/` | Content about prompting Claude; skill demo slides |
| Claude desktop / Cowork | `claude-desktop/` | Agent automation, task management, Cowork slides |
| Claude Dispatch | `claude-dispatch/` | Multi-agent, dispatch, orchestration content |
| Terminal / zsh | `terminal/` | Code-heavy, technical command slides |
| Client Portal | `your-client-portal/` | Agency delivery, audit portal content |
| Marketing Report | `your-marketing-report/` | Analytics, reporting, dashboard content |
| Cursor IDE | `cursor/` | Code editor, dev workflow content |
| VS Code | `vs-code/` | Development environment content |
| n8n | `n8n/` | Automation workflow content |
| Google Meet / Calendar | `google-meet/`, `google-calendar/` | Client calls, scheduling content |
| LinkedIn | `linkedin/` | LinkedIn content, social strategy slides |
| Fathom | `fathom/` | Meeting transcript, call analysis content |
| Exa | `exa/` | Research, web search agent content |

**How to pick:** Match the screenshot to the slide's prompt topic. A slide about Claude Code skills → `claude-code/`. A slide about automating research → `exa/` or `claude-desktop/`. A slide about agency delivery → `your-client-portal/`.

Check the catalog file at `context/brand-assets/reference-frames/catalog.yaml` for the full annotated list with analysis of each frame.
