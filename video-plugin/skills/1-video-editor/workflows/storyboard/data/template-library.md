# Remotion Template Library

## Overview

These are the available Remotion templates that can be assigned to storyboard segments. Each template lives in `_bmad/_memory/video-editor-sidecar/remotion-templates/` and is copied into the Remotion project during scaffold (Remotion Edit step 02).

---

## KineticCaption

**File:** `KineticCaption.tsx`
**Purpose:** Animated word-by-word caption display with emphasis effects
**Best for:** Hook phrases, key statements, high-energy intro sections

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| text | string | Yes | The caption text to animate |
| startFrame | number | Yes | Frame to begin animation |
| durationInFrames | number | Yes | Total animation duration |
| position | enum | No | top-left / top-right / bottom-left / bottom-right / bottom-center (default: bottom-center) |
| emphasisWords | string[] | No | Words to emphasize with larger size/color |
| color | string | No | Text color (default: white) |
| fontSize | number | No | Base font size (default: 48) |

### Visual Event Contribution

- 1 event per word animated (high density)
- Counts as multiple visual events per caption instance

### Recommended Sections

- Hook (primary)
- Intro sections (primary)
- Body key statements (selective use)

---

## Caption

**File:** `Caption.tsx`
**Purpose:** Standard subtitle-style caption display
**Best for:** Body sections, standard dialogue, supplementary text

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| text | string | Yes | The caption text |
| startFrame | number | Yes | Frame to appear |
| durationInFrames | number | Yes | Display duration |
| position | enum | No | Caption position (default: bottom-center) |
| color | string | No | Text color (default: white) |
| backgroundColor | string | No | Background color (default: rgba(0,0,0,0.7)) |
| fontSize | number | No | Font size (default: 36) |

### Visual Event Contribution

- 1 event per caption appearance

### Recommended Sections

- Body sections (primary)
- Intro sections (secondary, alongside KineticCaption)

---

## PowerCaption

**File:** `PowerCaption.tsx`
**Purpose:** Word-by-word keyword burst captions — each burst pops in letter-by-letter with one highlighted orange word
**Best for:** ALL speaker segments — replaces KineticCaption and Caption as the single caption system

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| bursts | CaptionBurst[] | Yes | Array of caption burst objects (see schema below) |

**CaptionBurst schema:**

| Field | Type | Description |
|-------|------|-------------|
| text | string | Full burst text (ALL CAPS, 2–4 words) |
| highlight | string | The one word to render in orange |
| startFrame | number | Frame at which this burst appears |
| durationInFrames | number | How long the burst stays on screen |
| wordOffsets | number[] | Per-word frame offset within the burst (word-by-word reveal) |

### Visual Event Contribution

- 1 event per burst appearance
- 1 event per individual word reveal within the burst

### Recommended Sections

- Hook (primary)
- Intro sections (primary)
- Body speaker segments (primary)
- **Replaces KineticCaption and Caption for ALL speaker caption segments**

**Long-form intro exception:** PowerCaption is NOT used on speaker segments in long-form intros. The rapid-fire visual pacing (MGs, B-roll, branded templates) provides sufficient visual density without caption overlays.

### Word-by-Word Timing

`wordOffsets` and `startFrame` are sourced from transcript word-level timestamps (audio analysis output), with the clipping offset subtracted. Actual timing is computed in step 5 (timeline assembly / caption timing verification). The burst plan (which phrases, which highlight word) is decided in step 4 and recorded in the segment's `notes` field.

---

## BRollOverlay

**File:** `BRollOverlay.tsx`
**Purpose:** B-roll video clip displayed as an overlay or full-frame replacement
**Best for:** Screen recordings, demonstrations, visual evidence

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| src | string | Yes | Path to B-roll video file |
| startFrame | number | Yes | Frame to begin |
| durationInFrames | number | Yes | Overlay duration |
| style | enum | No | fullscreen / pip-top-right / pip-top-left / pip-bottom-right / pip-bottom-left (default: fullscreen) |
| captionText | string | No | Optional caption over the B-roll |
| captionPosition | enum | No | Caption position (default: bottom-center) |

### Visual Event Contribution

- 1 event for B-roll appearing
- 1 event for B-roll disappearing
- +1 if captionText is provided

### Recommended Sections

- Body sections (screen recordings)
- Intro sections (visual demonstrations)
- Any section needing visual evidence

### Critical Rules

- The `src` B-roll video MUST have no audio track (`-an` in extraction)
- MUST include `muted` prop on internal `<OffthreadVideo>`
- MUST include `pauseWhenBuffering` prop

---

## SubtleZoom

**File:** `SubtleZoom.tsx`
**Purpose:** Slow zoom-in on the speaker with optional caption overlay
**Best for:** Emphasis moments, important statements, transitions between points

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| src | string | Yes | Path to speaker video |
| startFrame | number | Yes | Frame to begin zoom |
| durationInFrames | number | Yes | Zoom duration |
| zoomFactor | number | No | End zoom level (default: 1.15 = 15% zoom) |
| captionText | string | No | Optional caption during zoom |
| captionPosition | enum | No | Caption position (default: bottom-center) |

### Visual Event Contribution

- 1 event for zoom start
- +1 if captionText is provided

### Recommended Sections

- Hook (emphasis on speaker)
- Body transitions (subtle visual change)
- CTA (focus on speaker)

### Critical Rules

- MUST include `muted` prop on internal `<OffthreadVideo>`
- MUST include `pauseWhenBuffering` prop
- MUST include `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`

---

## SocialProofStack

**File:** `SocialProofStack.tsx`
**Purpose:** Display statistics, testimonials, or social proof as animated text cards
**Best for:** Authority building, data presentation, testimonial sections

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| items | object[] | Yes | Array of {label, value} pairs to display |
| startFrame | number | Yes | Frame to begin animation |
| durationInFrames | number | Yes | Total display duration |
| style | enum | No | stack / grid / sequential (default: sequential) |
| color | string | No | Text color (default: white) |
| accentColor | string | No | Highlight color (default: brand primary) |

### Visual Event Contribution

- 1 event per item animated in
- High density when items appear sequentially

### Recommended Sections

- Intro (authority building)
- Body (data presentation)
- CTA (social proof before ask)

---

---

## PiPSpeaker

**File:** `PiPSpeaker.tsx`
**Purpose:** Picture-in-Picture speaker overlay on screen share content — the defining long-form tutorial pattern
**Best for:** Screen share tutorial segments where speaker should remain visible in a corner

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| speakerSrc | string | Yes | Path to speaker video file |
| speakerStartFrom | number | Yes | Frame to seek speaker video to |
| durationInFrames | number | Yes | Segment duration |
| position | enum | No | bottom-right / bottom-left / top-right / top-left (default: bottom-right) |
| size | number | No | PiP width as % of composition (default: 15) |
| shape | enum | No | circle / rounded-rect / rect (default: circle) |
| borderColor | string | No | Border colour (default: #FFFFFF) |
| borderWidth | number | No | Border width in px (default: 3) |
| shadowEnabled | boolean | No | Drop shadow on PiP (default: true) |
| animateIn | number | No | Scale-in entrance frames (default: 12, 0 = no animation) |
| children | ReactNode | Yes | Screen share content rendered full-frame underneath |

### Visual Event Contribution

- 1 event for PiP appearing
- 1 event for PiP disappearing (if animated)

### Recommended Sections

- Body screen share segments (primary — long-form tutorials)
- Any segment where speaker + screen content must coexist

### Critical Rules

- Speaker `<OffthreadVideo>` inside PiPSpeaker MUST have `muted`, `pauseWhenBuffering`
- Children screen share `<OffthreadVideo>` MUST have `muted`, `pauseWhenBuffering`
- Position PiP to avoid overlapping captions (e.g., PiP bottom-right, captions bottom-center)

---

## ChapterCard

**File:** `ChapterCard.tsx`
**Purpose:** Branded chapter transition card with dark background, green accent bar, chapter number, and slide-up animation
**Best for:** Chapter transitions between body sections — replaces the old inline Caption-based chapter card

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| title | string | Yes | Chapter title text |
| chapterNumber | number | No | Chapter number (displays as "CHAPTER 02") |
| durationInFrames | number | Yes | Total display duration |

### Visual Design

- Background: dark gradient (#0A0A0A → #141414)
- Left accent bar: green (#2D6A4F), vertical
- Chapter number: green (#2D6A4F), Inter 600, letter-spaced
- Title: white (#FFFFFF), Inter 700, large
- Animation: fade in (10 frames) + slide up from 20px, hold, fade out (10 frames)
- Resolution-scaled via `useVideoConfig()` (same pattern as Caption.tsx)

### Visual Event Contribution

- 1 event for card appearance

### Recommended Sections

- Body chapter transitions (primary)
- Any section divider between major content blocks

### Critical Rules

- This is a CONSTANT template — same branded design every time
- Zero AI decisions needed beyond title text and chapter number
- Duration: 2–4s (60–120 frames at 30fps)

---

## Branded Templates (Constant — Same Animation Every Time)

Branded templates use fixed image assets from `_bmad/_memory/video-editor-sidecar/branded-assets/` and produce identical animations across all videos where they're used. No generation or API calls needed — they are always ready.

### UpworkProfile

**File:** `UpworkProfile.tsx`
**Purpose:** Animated Upwork profile card showing profile image, rating, and key stats
**Best for:** Authority building, social proof, credibility moments
**Assets:** `branded-assets/upwork-profile.png`

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| startFrame | number | Yes | Frame to begin animation |
| durationInFrames | number | Yes | Total display duration |
| position | enum | No | overlay position (default: center) |

**Visual Event Contribution:** 1 event for card appearance + 1 per stat animated in

**Recommended Sections:** Intro (authority), CTA (credibility), Body (when referencing freelancing)

### AgencyBrand

**File:** `AgencyBrand.tsx`
**Purpose:** {YOUR_COMPANY} logo animation with brand colors
**Best for:** Intro branding, CTA sign-off, transitions
**Assets:** `branded-assets/apg-logo.png`

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| startFrame | number | Yes | Frame to begin animation |
| durationInFrames | number | Yes | Total display duration |
| style | enum | No | full-screen / corner-watermark / lower-third (default: full-screen) |

**Visual Event Contribution:** 1 event for logo appearance

**Recommended Sections:** Intro (branding), CTA (sign-off), Chapter transitions

**AgencyBrand Style Selection Rule:**
When the speaker discusses agency credentials (project count, team size, revenue, "250 projects worldwide"), assign AgencyBrand in `full-screen` mode with the homepage screenshot — NOT `lower-third`. Lower-third is for passive branding only.

---

## Template Selection Guide

| Section Type | Primary Template | Secondary | Density Target |
|-------------|-----------------|-----------|---------------|
| Hook | PowerCaption | SubtleZoom | 15+ events/min |
| Intro | PowerCaption | BRollOverlay, SocialProofStack, UpworkProfile | 12-15 events/min |
| Body | PowerCaption | BRollOverlay | 7-10 events/min |
| Chapter Transition | ChapterCard | AgencyBrand | N/A (2-4s card) |
| CTA | SubtleZoom | SocialProofStack, UpworkProfile, AgencyBrand | Match intro density |
| Screen Share + Speaker (long-form) | PiPSpeaker | — | 2-4 events/min |

## Visual Asset Types → Template Mapping

| Visual Type | Available Templates |
|------------|-------------------|
| speaker | SubtleZoom, PowerCaption |
| video-extract | BRollOverlay (with B-roll video from main video) |
| motion-graphic | MotionGraphic (clean, full-color playback of Hera-generated video) |
| branded-template | UpworkProfile, AgencyBrand |
| chapter-card | ChapterCard |
| cta | SubtleZoom, SocialProofStack, UpworkProfile |
| pip-speaker | PiPSpeaker (with screen share children) |

---

## Social Proof Priority Rule

**CRITICAL: Branded templates ALWAYS take priority over Hera motion graphics for social proof content.**

When the script at a given moment references any of the following, assign `UpworkProfile` (or another branded template) instead of generating a Hera motion graphic:

- Upwork profile stats (ratings, earnings, project count, Top Rated / Expert Vetted status)
- Agency revenue, client count, or project numbers
- Platform credentials, certifications, or recognition
- Any personal credibility or authority signal tied to an existing branded asset

### Reasoning

Branded templates use real screenshots/assets that viewers recognise as authentic. Hera-generated graphics look polished but fictional for social proof — they reduce credibility rather than build it. The `UpworkProfile` template shows the actual profile screenshot and is always available without any generation cost.

### How to Apply

1. Scan the script section for social proof signals (numbers, credentials, platform references).
2. If found → assign `branded-template` visual type + `UpworkProfile` template.
3. Set `sourceFile: null` (branded assets are embedded in the component).
4. Use the `headline` prop to surface the key stat from that moment of the speech.
5. Only fall back to a Hera motion graphic for social proof if NO suitable branded asset exists.

---

## Branded Asset Selection Rule

**Which image does UpworkProfile display?**

The `UpworkProfile` component accepts an optional `imageSrc` prop. The correct image depends on what the script is claiming at that moment:

| Script Claim | Image to Use | imageSrc prop |
|-------------|-------------|---------------|
| Upwork credentials — ratings, reviews, earnings, Top Rated / Expert Vetted status, freelancing history | `upwork-profile.png` | omit prop (default) |
| Agency identity — team, project count as a business, "AI Agency", client portfolio | `agency-homepage.png` | `staticFile('branded-assets/agency-homepage.png')` |

**Rule:** The image MUST match the claim. Showing the agency homepage while the speaker says "Top Rated Plus on Upwork" is incoherent, and vice versa. Never swap these assets.

**Import required when using `staticFile`:**
```tsx
import { staticFile } from 'remotion';
```

---

## Motion Graphic Type → Template/Generation Mapping

Maps the 7 motion graphic types (from inspiration analysis) to available Remotion templates and Hera generation strategies.

| MG Type | Description | Template / Generation | Notes |
|---------|-------------|----------------------|-------|
| A: Text/Number Overlay | Bold number/metric on speaker | PowerCaption (pop-in variant) or Hera MG | See Type A Decision Tree below |
| B: Logo Graphic | Tool/platform logo beside speaker | Hera MG with `reference_image_url` (logo) | Fetch logo via `fetch-logo.ts` waterfall, use as Hera reference image |
| C: UI Mockup | Recreated social proof UI | Hera MG (custom prompt) | Full-screen recreations of YouTube search, comments, chat UIs |
| D: Concept Graphic | Abstract concept diagram | Hera MG (custom prompt) | Minimalist diagrams with animated connecting lines |
| E: Sequential Reveals | Bullet list with PiP | Hera MG or custom Remotion component | Bullets reveal synced to transcript word timestamps; speaker in PiP |
| F: Stylized B-Roll | Real footage with creative post-processing | BRollOverlay with CSS filter overlays | Film grain, 8mm matte, or cinematic grade applied via Remotion filters |
| G: Digital Pan/Zoom | Smooth movements across static content | SubtleZoom (extended with translate) | Use `interpolate()` for both `scale()` and `translate()` transforms |

**Type A Decision Tree:**
- Static number/metric display (e.g., "$1M+" appearing) → PowerCaption pop-in burst (default)
- Animated counter (e.g., 0 counting up to $1M) → Hera MG
- Default: PowerCaption (free, reliable, sufficient for 90% of cases)
- Use Hera only when script explicitly calls for counting animation or number morph

### Resolved Gap Decisions

| Type | Gap | Decision |
|------|-----|----------|
| A | PowerCaption lacks animated counter | PowerCaption for static pop-in (default); Hera only for counting animations |
| E | SocialProofStack lacks slide-style PiP | Use Hera MG for agenda/bullet slides; SocialProofStack for data cards only |
| F | BRollOverlay lacks film grain | Use Hera MG for stylized B-roll with film effects; BRollOverlay for clean screen recordings |
| G | SubtleZoom lacks pan (translate) | Use Hera MG for pan+zoom across documents; SubtleZoom for zoom-to-detail only |

---

## VideoRenderer (Generic Segment Dispatcher)

**File:** `VideoRenderer.tsx`
**Purpose:** Data-driven segment renderer that eliminates per-segment SegXX.tsx files. Maps `visualType` → component automatically.

### How It Works

The VideoRenderer reads segment data from the `SEGMENTS` array in `theme.ts` and dispatches each segment to the correct template component based on `visualType`:

| visualType | Component Used |
|-----------|---------------|
| `speaker` / `cta` | SubtleZoom |
| `video-extract` | BRollOverlay |
| `motion-graphic` | MotionGraphic |
| `branded-template` | UpworkProfile or AgencyBrand (based on `template` field) |
| `chapter-card` | ChapterCard (branded dark bg + green accent) |
| `pip-speaker` | PiPSpeaker |
| `transition` | WhiteFlash |

### Extended Segment Type

When using VideoRenderer, the `Segment` type in theme.ts carries ALL rendering props. No separate component files needed. Key additional fields:

| Field | Used By | Description |
|-------|---------|-------------|
| `bounceIn` | speaker | First-segment bounce-in effect |
| `zoomFactor` | speaker, motion-graphic | End zoom level |
| `skipFadeIn` | motion-graphic | Skip fade-in transition |
| `style` | video-extract, branded-template | Display style variant |
| `headline` / `subheadline` | branded-template | Text for branded cards |
| `imageSrc` | branded-template | Custom image source |
| `screenShareFile` | pip-speaker | Screen share video underneath PiP |
| `pipPosition` / `pipSize` / `pipShape` | pip-speaker | PiP overlay configuration |
| `bursts` | speaker (PowerCaption) | Caption burst data |

### Benefits

- **Zero per-segment files** — eliminates 15–40 SegXX.tsx files per composition
- **AI produces data only** — SEGMENTS array in theme.ts, not code
- **Deterministic rendering** — same data = same output, no generation errors
- **Works for all video types** — intro, body, full-video, short-form
- **Template components shared** — via sidecar, consistent across projects

### When NOT to Use

- If a segment needs truly custom rendering logic not covered by any template
- In that case, create a single custom component and add it as a special case in the VideoRenderer switch
