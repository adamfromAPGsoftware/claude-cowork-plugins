# Vertical Remotion Template Library (9:16)

## Overview

Templates available for vertical short-form Remotion projects (1080×1920). Templates live in `_bmad/_memory/video-editor-sidecar/remotion-templates/vertical/` and are copied into each Remotion project during scaffold.

---

## Vertical-Specific Templates

### VerticalCaptionV2 (Karaoke Highlight — PRIMARY)

**File:** `vertical/VerticalCaptionV2.tsx`
**Purpose:** Karaoke highlight captions — full phrase visible, active word highlighted as spoken
**Status:** **PRIMARY** — used for all continuous speech captions

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| pages | CaptionPage[] | Yes | Pre-computed pages with per-word timing from `clipped-refined-transcript.json` |
| durationInFrames | number | Yes | Segment display duration |
| position | enum | No | `'lower-center'` (default) / `'center'` / `'upper-center'` |
| fontSize | number | No | Base font size (default: 96 — 5% of 1920h) |
| color | string | No | Inactive word color (default: #FFFFFF) |
| activeColor | string | No | Active word color at 100% opacity (default: #FFFFFF) |
| accentColor | string | No | Highlight color for accent words when active (default: #4ADE80) |
| highlightWords | string[] | No | Words to render in `accentColor` when active |
| layoutContext | enum | No | `'full-speaker'` / `'split-screen'` / `'full-screen'` — adjusts vertical position |
| textTransform | enum | No | `'sentence-case'` (default) / `'uppercase'` |

**Data types (exported from component, also in theme.ts):**
```typescript
interface CaptionToken { word: string; startFrame: number; endFrame: number; }
interface CaptionPage { tokens: CaptionToken[]; startFrame: number; endFrame: number; }
```

**Caption behaviour (karaoke highlight):**
- Shows a full page of 5-7 words on ONE horizontal line — all words visible simultaneously
- Active word (being spoken): 100% opacity + 1.08x scale pulse (spring: damping 15, stiffness 300, mass 0.4)
- Unspoken words: 50% opacity, scale 1.0
- Already-spoken words: 70% opacity, scale 1.0 (shows reading progress)
- Accent words (in `highlightWords`): render in `accentColor` (#4ADE80) when active
- Page transition: 3-frame cross-fade between pages
- Final page exit: 6-frame opacity fade at segment end
- Word timing from `CAPTION_PAGES` in theme.ts (sourced from transcript word timestamps)

**Layout-dependent positioning:** full-speaker 72%, split-screen 90%, full-screen 82%, fallback 75%

---

### VerticalCaption (Callout Only — LEGACY)

**File:** `vertical/VerticalCaption.tsx`
**Purpose:** Brief 1-2 word emphasis callout flashes — **NOT for continuous speech**
**Status:** **Callout-only** — retained for `style: 'callout'` emphasis overlays (max 2-3 per video)

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| text | string | Yes | Callout text (1-2 words only) |
| startFrame | number | Yes | Frame to begin animation |
| durationInFrames | number | Yes | Display duration (30-60 frames) |
| highlight | string | No | Word(s) to render in accent color |
| position | enum | No | `'upper-center'` for callout style |
| fontSize | number | No | Base font size (default: 134 for callout) |
| color | string | No | Text color (default: #FFFFFF) |
| accentColor | string | No | Highlight color (default: #4ADE80) |
| style | enum | No | `'callout'` — black box background, upper-center position |
| layoutContext | enum | No | `'full-speaker'` / `'split-screen'` / `'full-screen'` |
| textTransform | enum | No | `'sentence-case'` (default) / `'uppercase'` |

**When to use:** Product names, key features, numbers — brief flash over screen content. NOT for continuous speech captions (use VerticalCaptionV2 instead).

---

### VerticalBRollOverlay

**⚠️ DEPRECATED FOR SHORT-FORM.** Not included in scaffold for vertical projects. Use MotionGraphic (V4/V4b) or VerticalSplitScreen (V5) with Hera MG overlays instead.

**File:** `vertical/VerticalBRollOverlay.tsx`
**Purpose:** VHS-style B-roll overlay repositioned for 9:16 format
**Adapted from:** `BRollOverlay.tsx`

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| src | string | Yes | Path to B-roll video file |
| startFrame | number | Yes | Frame to begin |
| durationInFrames | number | Yes | Overlay duration |
| style | enum | No | fullscreen / pip-top / pip-bottom (default: fullscreen) |

**Key differences from BRollOverlay.tsx:**
- PiP sizes: 40% width (vs 35%) for mobile visibility
- "LATER IN VIDEO" indicator repositioned for portrait (smaller font, badge style)
- Simplified PiP positions: top/bottom only (no left/right — too narrow in portrait)
- Timecode repositioned to bottom-right (avoids platform UI overlap bottom-left)

---

### VerticalSplitScreen

**File:** `vertical/VerticalSplitScreen.tsx`
**Purpose:** Speaker top half + B-roll/MG bottom half with animated divider
**NEW template — no landscape equivalent**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| speakerSrc | string | Yes | Path to speaker video |
| overlaySrc | string | Yes | Path to B-roll or MG video |
| startFrame | number | Yes | Frame to begin |
| durationInFrames | number | Yes | Display duration |
| videoStartFrom | number | No | Speaker video seek position for audio sync |
| variant | enum | No | `'split'` (default, 50/50) / `'split-65-35'` / `'pip'` |
| dividerColor | string | No | Divider line color (default: `'transparent'` — no visible divider) |

**Variants:**
- `split` (default) — Content fills top 50%, speaker fills bottom 50%, no visible divider. **4/5 top performers use this.**
- `split-65-35` — Content fills top 65%, speaker fills bottom 35%. Available but NOT default.
- `pip` — B-roll fills full screen, speaker in circular PiP overlay (top-right, 30% diameter)

---

### VerticalHookText

**File:** `vertical/VerticalHookText.tsx`
**Purpose:** Large kinetic text animation for hook openings — words slam in from sides
**NEW template — no landscape equivalent**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| text | string | Yes | Hook text (rendered ALL CAPS) |
| highlight | string | No | Word(s) to render in accent color |
| startFrame | number | Yes | Frame to begin animation |
| durationInFrames | number | Yes | Total animation duration |
| backgroundColor | string | No | Background color (default: #0a0a0a) |
| accentColor | string | No | Highlight color (default: #4ADE80) |

**Animation:**
- Each word slams in from alternating sides (left, right, left...)
- Scale overshoot: 1.3 → 1.0 with bounce easing
- Words stack vertically, centered on screen
- Fade out in last 6 frames

---

## Reused Templates (Already Vertical-Compatible)

These existing templates use `useVideoConfig()` for scaling and work at any resolution:

| Template | File | Notes |
|----------|------|-------|
| SubtleZoom | `SubtleZoom.tsx` | Works as-is — zoom scales relative to composition |
| MotionGraphic | `MotionGraphic.tsx` | Works as-is — full-frame video playback |
| SocialProofStack | `SocialProofStack.tsx` | Works as-is — uses `useVideoConfig()` scaling |

---

## Template Selection Guide (Short-Form)

| Section | Primary Template | Secondary | Max Duration |
|---------|-----------------|-----------|-------------|
| Hook (0–2s) | VerticalSplitScreen (V5) split-screen | SubtleZoom (V2) | 1-2s split-screen then snap to V1/V4 |
| Body (5–40s) | SubtleZoom (V1) | MotionGraphic, VerticalSplitScreen (with MG overlay) | 4s max per segment |
| CTA (last 5s) | SubtleZoom (V1) | SocialProofStack | 5s max |

## Visual Type → Template Mapping

| Visual Type | Template | Pattern |
|------------|----------|---------|
| speaker | SubtleZoom (1.03 zoom) + VerticalCaptionV2 | V1 |
| speaker-zoom | SubtleZoom (1.08 zoom) + VerticalCaptionV2 | V2 |
| motion-graphic-cutaway | MotionGraphic (no caption, 60-90 frames) | V4b |
| broll | VerticalBRollOverlay (DEPRECATED for short-form) | V3 |
| motion-graphic | MotionGraphic | V4 |
| split-screen | VerticalSplitScreen + VerticalCaptionV2 | V5 |
| hook-text | VerticalHookText | V6 |
| cta | SubtleZoom + SocialProofStack + VerticalCaptionV2 | V7 |
