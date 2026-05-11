# Instagram Carousel — Prompt Guidelines ({YOUR_NAME} / Dark Mode)

Reference for crafting fal-ai/nano-banana-2 image-generation prompts for **@{YOUR_HANDLE_PERSONAL}** Instagram carousel slides. Every prompt MUST include the brand anchors. The personal brand is casual, builder-focused, and tech-forward — DM Sans typography, neon lime (#90F23C) accents on dark backgrounds. Direct, anti-guru energy targeting aspiring AI builders and developers.

---

## 1. Brand Anchors (REQUIRED in every slide prompt)

These constants must appear in every prompt:

| Element | Specification |
|---------|---------------|
| Dimensions | 1080x1350 portrait (4:5 ratio) |
| Green accent | `#90F23C` — highlighted keyword in headline is ALWAYS this neon lime |
| Headline font | DM Sans Bold, all-caps, tight letter-spacing |
| Body font | Clean sans-serif (DM Sans Regular or Medium), white, centered |
| Handle | `@{YOUR_HANDLE_PERSONAL}` bottom-left on content slides, with a small YouTube icon to the left of the handle |
| Repost | Instagram repost icon + "repost" bottom-right on content slides |
| Palette | Dark-dominant — pure black, near-black surfaces (#111111), neon lime accents |
| Logo | No company logo — YouTube icon next to @{YOUR_HANDLE_PERSONAL} handle only |
| Density | One idea per slide — clean, not cluttered |

**Prompt prefix for every slide:**
> "Generate a 1080x1350 portrait Instagram slide."

**🛑 CRITICAL — Font Names in Prompts:**
NEVER include font names (e.g., "DM Sans", "Inter", "Helvetica") in image prompts. The model will render font names as visible text on the slide. Instead, describe the STYLE you want: "bold all-caps headline", "clean sans-serif body text", "regular weight text". Describe appearance, not font names.

---

## 2. Slide Prompt Patterns

### Hook Slide (Slide 1)

Bold, eye-catching first slide. Stops the scroll.

```
Generate a 1080x1350 portrait Instagram slide. Bold eye-catching design.
Large DM Sans Bold all-caps headline with tight tracking at top: "[HEADLINE]"
with the word "[KEYWORD]" rendered in neon lime (#90F23C), remaining text in
white. [BACKGROUND TREATMENT — see variation guidance].
The design should feel high-energy and stop scrolling. [Optional: product
image, screenshot, or visual element in center]. Clean, modern, dark
aesthetic. No @handle or bookmark on hook slide.
```

**SWIPE CUE (MANDATORY on hook slide):** The hook slide MUST include a clear visual indicator to swipe/go to the next slide. Common patterns:
- Clean arrow or chevron pointing right (neon lime #90F23C or white)
- "SWIPE →" or "→" text in clean sans-serif near the right edge
- A visual element (screenshot, card, text block) that is deliberately cut off at the right edge, implying continuation
- Chevron or arrow icon at the mid-right edge

Pick whichever feels most natural for the slide's layout. The goal is that viewers instinctively know there's more content to the right.

**NOTE:** When the hook slide features the creator, it uses a real photo — see the "Photo Hook Slide" pattern above. The generic hook pattern here is for hook slides that do NOT feature the creator.

### Screenshot Feature Slide

Content slide with an embedded screenshot or app UI.

```
Generate a 1080x1350 portrait Instagram slide. Dark black or near-black
(#111111) background. Large DM Sans Bold all-caps headline with tight
tracking at top: "[HEADLINE]" with "[KEYWORD]" in neon lime (#90F23C),
rest in white. In the center, show the attached screenshot inside [a rounded
card with subtle shadow / a laptop frame / floating with drop shadow /
a card with subtle neon lime (#90F23C) border glow]. Below the screenshot,
clean sans-serif (DM Sans Regular) white text centered: "[description]".
Bottom-left: small YouTube icon followed by "@{YOUR_HANDLE_PERSONAL}" in small white text.
Bottom-right: Instagram repost icon with "repost" in small text.
```

### Text-Only Slide

Content slide with headline + explanation, no embedded image.

```
Generate a 1080x1350 portrait Instagram slide. Dark [black / near-black /
subtle geometric grid] background. Large DM Sans Bold all-caps headline
centered: "[HEADLINE]" with "[KEYWORD]" in neon lime (#90F23C), rest in
white. Below, clean sans-serif (DM Sans Regular) white body text centered:
"[explanation]". [Optional: clean accent line, subtle glow, or clean
arrow/chevron for emphasis].
Bottom-left: small YouTube icon followed by "@{YOUR_HANDLE_PERSONAL}" in small white text.
Bottom-right: Instagram repost icon with "repost" in small text.
```

### Photo Hook Slide (Slide 1) — Real Photo Composite

The hook slide uses a **real photo** of the creator (not AI-generated). The model analyses the photo to determine where the creator is positioned and places text in available space around them.

```
Using the attached photo of this person as the base image, generate a
1080x1350 portrait Instagram slide. Analyse where the person is positioned
and what space is available for text. Keep the person EXACTLY as they
appear — do not modify their face, body, pose, or clothing. Extend or
adapt the existing background to fill the frame using dark tones consistent
with the brand palette. Overlay large bold all-caps text in available
space around the person: "[HEADLINE]" with "[KEYWORD]" in neon lime
(#90F23C), remaining text in white. Place text where it does not cover
the person. Include a swipe cue (arrow or chevron). No @handle or bookmark
on hook slide.
```

### CTA Slide (Last Slide) — Text Only

The CTA slide is a text-based "Comment [KEYWORD]" design. No photo of the creator.

```
Generate a 1080x1350 portrait Instagram slide. Dark background [black /
subtle geometric grid / radial glow]. Large bold all-caps centered
headline: "[HEADLINE]" with "[KEYWORD]" in neon lime (#90F23C), rest in
white. Below, prominent neon lime (#90F23C) text: "Comment [KEYWORD]"
with a clean geometric arrow pointing down. [Optional: tool logos or
brand icon]. Clean, bold, high-contrast. No photo of the creator — text and
branding only.
Bottom-left: small YouTube icon followed by "@{YOUR_HANDLE_PERSONAL}" in small white text.
Bottom-right: Instagram repost icon with "repost" in small text.
```

---

## 3. Variation Guidance

Each carousel should feel unique. Vary these elements BETWEEN carousels:

### Backgrounds
- Pure black (#000000)
- Near-black with very subtle noise/grain texture (adds warmth, not sterile)
- Dark gradient (black → very dark green, or black → charcoal)
- Subtle geometric grid (thin #1A1A1A lines on black — tech feel, not overpowering)
- Dark photo with black gradient overlay (hook/CTA slides — keeps it real and personal)
- Radial gradient glow (#90F23C at 5-10% opacity, corner-positioned, fading to black)

### Visual Elements (mix and match)
- Code cards (dark rounded rectangles, monospace text, subtle #1A1A1A border)
- Rounded screenshot frames with subtle shadow or neon lime border glow
- Laptop / MacBook Pro mockup frames
- Clean accent lines (thin, #90F23C, horizontal/vertical — used sparingly as emphasis)
- Subtle gradient glow spots (neon lime, low opacity, background atmosphere)
- Pill-shaped tags/labels (dark #111111 surface with lime border or lime text)
- Terminal-style text blocks (monospace on dark surface)
- Minimal line-style icons (white or lime)
- Card/panel layouts (#111111 surfaces on black, subtle #1A1A1A borders)
- Clean arrows and directional cues (white or lime — personality without sketch feel)

### Color Pops
- Neon lime (#90F23C) is the PRIMARY and ONLY accent
- White for contrast and hierarchy
- No yellow, no orange, no multi-color pops
- Monochrome + single-accent = the brand

### Personality & Warmth
- Keep the conversational, builder-to-builder energy in all slides
- Creator photo slides should still feel candid and real (not corporate headshot energy)
- Body text tone stays casual and direct — "I just built this" anti-guru energy
- Dark backgrounds with subtle texture > flat sterile black (texture adds human touch)

### Layout Composition
- Full-text (headline + body, centered)
- Text + embedded screenshot (upper or center)
- Big headline + description box below
- Photo background + text overlay (hook/CTA)
- Split layout (text left, visual right)

---

## 4. Carousel Flow Pattern

1. **Hook slide** — bold, eye-catching, different energy. Often has a product image, screenshot, or strong visual. No @handle or bookmark. **MUST have a swipe cue** (arrow, "SWIPE →", or cut-off element) so viewers know to swipe right.
2. **Content slides** (3-6) — each makes ONE point. Vary layouts between slides. Include @{YOUR_HANDLE_PERSONAL} (with YouTube icon) and repost icon.
3. **CTA slide** — "Comment [KEYWORD]" for lead magnet. Text-only design — no photo of the creator. Bold, high-contrast, clear call to action.

---

## 5. Caption Rules

Instagram-specific caption formatting:

- **Tone:** Casual, direct, builder-to-builder. Lowercase-friendly, authentic. Anti-guru.
- **Hashtags:** 3-5 targeted, niche-specific hashtags per post. Treat them like SEO keywords.
  - NEVER use generic tags (#instagood, #ai, #tech)
  - NEVER copy-paste the same hashtags across posts (triggers spam detection)
  - Each carousel gets unique hashtags matching its specific content
  - Place hashtags at the end of the caption, not inline
  - {YOUR_NAME} focus: builder tools, dev tutorials, AI coding (e.g. `#claudecode` `#aibuilder` `#buildwithAI`)
- **Structure:**
  - Hook line (first line visible before "...more")
  - Line breaks for readability
  - Key points or context
  - CTA: "Comment [KEYWORD] and I'll send you..." — NEVER mention YouTube or any specific platform in the CTA. Keep it generic: "the full resource", "the full breakdown", "the comparison guide", etc.

**Example format:**
```
this changed everything about how i use ai for [topic] 👇

[2-3 lines of context]

here's what most people get wrong:
→ [point 1]
→ [point 2]
→ [point 3]

comment "[KEYWORD]" and i'll send you the full resource

#tag1 #tag2 #tag3
```

---

## 6. Screenshot Guidance

When embedding screenshots into slides:

- **Dark mode preferred** — matches the dark carousel aesthetic
- **Crop tight** — show only the relevant part of the UI
- **Terminal / code screenshots** work great as embedded elements
- **Browser screenshots** — crop out the URL bar unless it's relevant
- **App UIs** — focus on the feature being discussed

The prompt should specify HOW to embed the screenshot:
- "inside a rounded card with subtle shadow"
- "inside a MacBook Pro frame"
- "floating with a drop shadow"
- "card with subtle neon lime (#90F23C) border glow"

---

## 7. Real Photo Usage

The hook slide (slide 1) uses a **real photo** of the creator — not AI-generated. The photo is provided by the user and sent to fal-ai/nano-banana-2 as-is.

### Rules

- Set `photo_path` in the slide JSON pointing to the real photo file
- The photo is sent as the first content part — the model analyses where the person is positioned and composites text/branding around them
- The model must NOT alter the person's face, body, pose, or clothing — the person must appear exactly as in the source photo
- The prompt describes only: text content, text placement strategy, background treatment, and brand elements
- The CTA slide (last slide) does NOT feature the creator — it's a text-based "Comment [KEYWORD]" design
- Only the hook slide uses a real photo; content slides (text-only, screenshot features) remain fully nano-banana-2-generated

---

## 8. Logo Integration

### No Company Logo (Personal Brand)

The {YOUR_NAME} personal brand does NOT use a company logo. Instead, a small YouTube icon is placed to the left of the @{YOUR_HANDLE_PERSONAL} handle (bottom-left) on content slides. Do NOT add any company logos (or otherwise) to personal brand slides.

### Tool & Brand Logos

When carousel slides mention tools, platforms, or brands, their logos should be embedded into the slide for visual credibility.

### Logo Fetching

Use `fetch-logo.ts` (4-tier waterfall: Simple Icons → SVG Logos → Logotypes.dev → Logo.dev) to fetch logos as 512x512 PNGs into the project's `creative-director/logos/` folder.

**🛑 ALWAYS fetch fresh logos — NEVER reuse previously cached files.** Stale logos are a common source of incorrect/wrong-brand images. Delete existing files and re-fetch every time. After fetching, visually verify the PNG is the correct logo before using it in a slide.

### Embedding Logos in Slide Prompts

Include the fetched logo PNG in the slide's `embed_images` array. The prompt should describe how to display it:

- **Single tool slide:** "Show the attached logo centered above the headline at roughly 120px, with a subtle glow or shadow"
- **Tool comparison/list slide:** "Display the attached logos in a horizontal row, each roughly 80px, evenly spaced below the headline"
- **Screenshot + logo:** "Place the attached logo in the top-right corner at roughly 60px as a badge"
- **Hook slide with tool:** "Show the attached logo large (200px) in the center with the headline text wrapping around it"

### Rules

- **Every tool mentioned by name MUST have its real logo fetched and embedded** — never let the model guess/generate a logo from the text prompt alone — the model will get logos wrong if you don't provide the actual image.
- Logos are white-on-transparent (fetched with `--color ffffff`) — they work on dark backgrounds
- If a tool has a coloured logo that should stay coloured, fetch WITHOUT `--color` flag so Tier 2 (gilbarbara) preserves original brand colours
- Don't overcrowd slides — if 3+ tools are mentioned on one slide, show logos smaller or pick the most important ones
- If a logo fetch fails and user skips, do NOT reference any logo in the prompt — the model must not attempt to draw logos from text description

---

## 9. Slide Generation Approach

### Hook Slide — Real Photo + nano-banana-2 Text Composite

The hook slide (slide 1) uses a **real photo** of the creator provided by the user. The model receives the photo and composites text/branding around the person without modifying their appearance. Set `photo_path` in the slide JSON pointing to the photo file.

### CTA Slide — Text Only

The CTA slide (last slide) is fully generated by fal-ai/nano-banana-2 from a text prompt — no photo of the creator. It's a bold "Comment [KEYWORD]" design with brand styling. See the CTA Slide prompt pattern in Section 2.

### Content Slides — Fully nano-banana-2-Generated

Content slides (text-only, screenshot features) are fully nano-banana-2-generated from text prompts and optional `embed_images`. No photos of the creator on content slides.

### B-Roll & Screenshots

1. **Review B-roll/screenshots** from the project folder to understand what the video covers visually — tools shown, interfaces demonstrated, settings used.
2. **Use these observations to write better prompts** — describe the scenes, tools, and settings you saw in the video so nano-banana-2 generates contextually accurate slides.
3. **NEVER add B-roll images or extracted video frames to `embed_images`** — they are reference material for the prompt author (you), not input images for the model.
4. **Screenshots of tool UIs** (e.g., Claude Code interface, IDE windows) are an EXCEPTION — these are product screenshots, not video frames of the creator. Tool UI screenshots CAN be embedded via `embed_images` when a slide discusses that specific tool.

### Rules

- **Hook slide uses a real photo** — set `photo_path` in the slide JSON, the model composites text around the person
- **CTA slide is text-only** — no photo of the creator, bold "Comment [KEYWORD]" design
- **Content slides are fully nano-banana-2-generated** — text prompts + optional embedded screenshots/logos
- **B-roll/extracts = prompt inspiration only** — study them, describe what you see, but never embed them
- **Tool UI screenshots are allowed** as `embed_images` (product screenshots ≠ video frames of the creator)

---

## 10. Content Extraction from Video

When creating carousels from video content (the primary use case):

1. **Source material:** Read the project's video analysis files — transcript, audio analysis, visual analysis, storyboard
2. **Extract carousel-worthy topics:** Look for educational moments, step-by-step processes, tool showcases, tips/tricks, surprising insights
3. **Map to slides:** Each key point from the video becomes one content slide
4. **Screenshots/B-roll:** Check the project's B-roll folder and video screenshots for images that can be embedded into slides
5. **CTA keyword:** Derive from the video topic (e.g., video about Claude Code → keyword "CLAUDE")
6. **Slide count:** AI determines the optimal count based on content density (typically 5-8 slides)
