---
name: step-07-generate
description: Generate carousel slide images via fal-ai nano-banana-2 using existing Creative Director pipeline
nextStep: ./step-08-quality.md
---

# Step 7: Generate Visuals

## Goal

Plan the hook slide composition, build the slides.json input, and run the carousel generator to produce all slide PNGs at 1080×1350 in the design system style defined in `{carouselGuidelines}`.

> **MANDATORY TOOL + MODEL RULE:**
> - **Hook slide (reference photo):** `mcp__fal-ai__edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`
> - **Content slides (text-only):** `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"`
> - **NEVER use `generate_image_from_image`** — it sends `image_url` as a string but `fal-ai/nano-banana-2/edit` expects `image_urls` as an array. `edit_image` handles this correctly.
> - Never use Flux, Gemini, SDXL, or any other model.

## Sequence

### 1. Set Output Directory

```
slides_dir = {project-root}/context/draft-queue/carousels/YYYY-MM-DD-instagram/
```

Create the directory if it doesn't exist. Derive the date from today's date.

---

### 2. Select Theme

**Always use `paper` theme** for all content slides. The warm cream (#f5f0e8) background with dotted grid is the standard for all Instagram carousels regardless of topic angle.

The hook slide is **always** `hero` theme (creator photo full-bleed with gradient) regardless of the content theme. Record the theme as `paper` — it applies to all non-hook slides.

---

### 3. Hook Slide Planning Gate

This is a deliberate planning step that runs **before** building slides.json. Work through each sub-step in order.

#### 3a. Select hook image source

**Primary source: Asset Catalog.** Read `{project-root}/context/context/brand-assets/asset-catalog.yaml` and filter for all assets where `subject_in_frame: true`. This gives you every photo and video frame of the creator available — including Instagram reference photos, headshots, mirror selfies, and B-roll frames.

Each asset has rich metadata: `subject_description` (where the creator is, what they're doing), `setting`, `emotion`, `mood`, `camera_angle`, and `use_cases`. Use this to pick the photo that best matches the carousel's topic and energy.

**Rotation rule — never reuse the same photo in consecutive carousels.** Check the `ic_history` in `{stateFile}` for the last 5 carousel entries. If a `hook_photo` field exists, exclude those files from selection. Pick a different photo each time. If all photos have been used recently, restart the rotation from the least recently used.

Record the chosen source and filename. When updating state in step-09, save the selected filename as `hook_photo` in the history entry.

**Fallback sources (if asset catalog is unavailable):**
- `{instagramReferencePhotos}` directory listing (IMG_7883–7887.jpg)
- `{hookInspirationDir}` for drop-in hero images
- Generated scene — last resort

#### 3a-ii. Claude branding on hook slide (conditional)

If the carousel topic mentions **Claude, Anthropic, Claude Code, Claude Design, or any Claude product**, the hook slide **must** include Claude visual identity.

**Claude brand assets (canonical paths):**
- Orange sunburst logo: `{project-root}/context/context/brand-assets/logos/claude.png`
- Black sunburst logo: `{project-root}/content/projects/{active_project_slug}/creative-director/logos/claude-sunburst.png`

**Placement rules:**
- Use the **orange sunburst** on dark/hero backgrounds (matches the `#d97757` accent palette)
- Include the logo as an `embed_images` entry on the hook slide
- In the image prompt, describe placement: position the Claude sunburst icon at ~120px size, placed in a visible area that does NOT overlap the headline text or the creator's face. Typical placements: near the "NEW" tab, beside the headline, or floating in the clear zone of the hero gradient.
- The logo should feel like part of the composition, not a watermark — visible and intentional

**When NOT to include:** If the topic is about general AI tools, AI business, or community topics that don't specifically mention Claude products, omit the Claude logo.

#### 3b. Analyse photo composition (if using a creator photo)

Read the selected photo using the Read tool. Claude is multimodal and can see the image directly.

Determine:
1. **Subject position** — Where is the creator in the frame? (left side, right side, center; upper half, lower half)
2. **Background content** — What fills the space around them? (desk, monitors, office, plain wall, etc.)

From this, select the `anchor` prop for `HookSlide`:

| Creator's position | Recommended anchor | Rationale |
|----------------|--------------------|-----------|
| Bottom-right of frame | `top-left` | Headline sits in upper-left dark gradient zone — most readable, most common |
| Bottom-left of frame | `top-right` | Headline sits in upper-right dark gradient zone |
| Center-left | `bottom-right` | Headline uses lower-right dark gradient zone |
| Center / full-width | `top-left` or `bottom-left` | Either dark gradient zone works — pick whichever avoids the creator's face |

The `hero` background in `SlideFrame` applies a gradient: `rgba(10,7,6,0.35)` at top → transparent at 45% → `rgba(10,7,6,0.9)` at bottom. Text is most readable in these darkened zones. The headline **must not overlap the creator's face or body**.

#### 3c. Plan headline layout

Map the carousel hook copy from step-06 onto `HookSlide` props:

- **`tab`** — Optional. Large orange number or short keyword (e.g., `"5"`, `"NEW"`). 96px, bold. Use when the carousel has a numbered list angle or a strong recency hook. Omit if it adds clutter.
- **`head1`** — First line of the headline. White, bold sans-serif, 92px.
- **`accent`** — Single orange italic serif word (renders via `SerifAccent` — italic, not underlined). Use for the emotional or conceptual pivot word.
- **`head2`** — Continuation of the headline after the accent word. White, bold sans-serif.
- **`sub`** — Optional. Short italic serif subtext (32px, 92% opacity). Good for a "…here's how" or teaser line. Omit if the headline is punchy enough on its own.

All text must be positioned to avoid overlapping the creator's face/body given the chosen `anchor`.

#### 3d. Output hook plan summary

Before proceeding to step 4, print this block:

```
Hook Plan:
  Photo:  {filename or "inspiration: {filename}" or "generated scene"}
  Anchor: {anchor}
  Tab:    {tab value or "none"}
  Head:   {head1} + accent({accent}) + {head2}
  Sub:    {sub text or "none"}
  Claude branding: {yes — orange sunburst | no — topic not Claude-specific}
```

---

### 4. Select Reference Screenshots

Reference frames directory:
```
{project-root}/context/context/brand-assets/reference-frames/
```

Pick the most topically relevant screenshot for slides that call for a UI embed. Use the mapping below:

| Topic | Screenshot path (relative to reference-frames/) |
|-------|--------------------------------------------------|
| Claude Code / agents | `claude-code/claude-code-claude-code-initial-state-with-prompt.png` |
| Claude chat / prompting | `claude-chat/claude-chat-claude-chat-main-interface.png` |
| Task management / automation | `claude-desktop/claude-desktop-cowork-task-management-interface.png` |
| Dispatching agents / workflows | `claude-dispatch/claude-dispatch-cowork-dispatch-tab.png` |
| Terminal / CLI work | `terminal/terminal-zsh-terminal-prompt.png` |
| n8n / workflow canvas | `n8n/n8n-workflow-canvas-with-nodes.png` |

Only `screenshot`-type slides need an `embed_images` entry. Content and code slides do not embed screenshots unless the copy specifically references a UI.

---

### 5. Build slides.json

Construct the full slides array. Reference `{carouselGuidelines}` for the image prompt templates for each slide type — the style guide contains the full wording for backgrounds, typography, border treatments, and syntax highlight colours.

The script expects this top-level shape:

```json
{
  "slides": [
    {
      "slide_number": 1,
      "prompt": "...",
      "photo_path": "optional — absolute path to creator's photo for hero slides",
      "embed_images": ["optional — absolute paths to screenshots or logos to embed"]
    }
  ]
}
```

**Slide type → JSON mapping:**

**`hook` (slide 1 — always hero theme)**
- Set `photo_path` to the absolute path of the selected creator photo (or omit if using a generated scene).
- The `prompt` must describe: full-bleed hero photo, gradient overlay (top ~35% dark, bottom ~45% dark), headline text placed at the `anchor` position from the hook plan, `tab` if planned, `head1` + italic serif `accent` + `head2`, optional `sub` line. Reference `{carouselGuidelines}` for the full hero prompt template.
- No `embed_images` unless using an inspiration image as the hero.

**`code` slide**
- Prompt describes: `▶ SEND THIS TO CLAUDE` eyebrow in orange monospace, headline with serif italic accent word, dark terminal card with orange syntax highlights on key terms.
- Apply the selected carousel theme (dark or paper) for the background.
- No `embed_images`.

**`content` slide**
- Prompt describes: badge eyebrow (e.g., `skill · 01`), ghost word at ~6% opacity in background, headline with orange `Accent` underlined word (blocky rectangular bar underline — NOT brushstroke), body copy in light grey, monospace chip at bottom.
- Apply the selected carousel theme.
- No `embed_images` unless the slide references a specific UI.

**`screenshot` slide**
- **Do NOT embed static screenshots.** When a slide claims Claude generated something (a dashboard, an app, a UI), use `fal-ai/nano-banana-2` to **generate a realistic representation** of that output directly in the slide image.
- In the image prompt, describe the generated UI in detail: layout structure, color scheme, component types (sidebar nav, analytics cards, charts, tables), and any specific content. The generated UI should look like a real, polished application — not a placeholder.
- The generated UI sits inside the ScreenshotSlide frame (title bar with dots, path label, framed area).
- Prompt describes: eyebrow label, headline with accent, the framed area containing the generated UI (described in natural language), caption text below.
- Apply the selected carousel theme.
- Only use `embed_images` with real screenshots when the slide is showing an actual tool interface (Claude Code terminal, Claude Desktop, etc.) — not when demonstrating what Claude built.

**`cta` (last slide)**
- Prompt describes: eyebrow, headline + CTA keyword in large orange, subtext, CTA button pill with keyword.
- **Do NOT include "save for later" in the footer** — the CTA slide uses `showNextHint: false` in the design system.
- Apply the selected carousel theme.

**Theme colour reference:**

| Element | Dark theme | Paper theme |
|---------|-----------|-------------|
| Background | `#0f0d0b` with orange radial glows | `#f5f0e8` with dotted grid (`#d8cfc0` 1.4px dots, 28px spacing) |
| Body text | `#fafaf8` | `#1a1614` |
| Orange accent | `#d97757` | `#d97757` |
| Terminal cards | Dark `#141210` with orange glow border | Same dark card — provides contrast on paper bg |
| Grain overlay | Yes (35% opacity, overlay blend) | No |

---

### 6. Run Generator

Save the completed slides array as `slides.json` inside `{slides_dir}`, then for each slide call fal-ai MCP:

```
# Hook slide (with photo reference) — use edit_image, NOT generate_image_from_image:
mcp__fal-ai__upload_file(file_path="{hook photo path}")  → photo_url
mcp__fal-ai__edit_image(
  model="fal-ai/nano-banana-2/edit",
  image_url=photo_url,
  prompt="{slide 1 prompt}",
  strength=0.92
)

# Content slides (text-only):
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="{slide N prompt}",
  image_size="portrait_4_5"
)
```

> **TOOL RULE:** Hook slide with photo → `edit_image` (wraps URL into array correctly). Content slides → `generate_image`. Never use `generate_image_from_image`.

Save each slide as `slide-01.png`, `slide-02.png`, etc. in `{slides_dir}`.

**Critical:** Generate one slide at a time with a 2-second pause between calls. Never parallelise.

---

### 7. Verify Output

List files in `{slides_dir}`. Verify:
- PNG count matches the slide count in slides.json.
- Each PNG is non-zero in size.

Retry any missing or zero-byte slides by re-calling the MCP tool for that specific slide's prompt.

---

### 8. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Visual Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Theme:         {paper|dark}
Hook photo:    {filename} (anchor: {anchor})
Slides:        {N}/{total} generated
Output dir:    {slides_dir}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If any slides are missing: append `⚠ Missing: slide-{N}.png — will need manual regeneration` per missing file.

Then immediately load and execute step-08.
