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
| Intro | PowerCaption | BRollOverlay, showcase-mg (NumberCountUp, ChecklistReveal, etc.), UpworkProfile | 12-15 events/min |
| Body | PowerCaption | BRollOverlay, showcase-mg (ROICalculator for running totals) | 7-10 events/min |
| Chapter Transition | ChapterCard | AgencyBrand | N/A (2-4s card) |
| CTA | SubtleZoom | SocialProofStack, UpworkProfile, AgencyBrand | Match intro density |
| Screen Share + Speaker (long-form) | PiPSpeaker | — | 2-4 events/min |

## Visual Asset Types → Template Mapping

| Visual Type | Available Templates |
|------------|-------------------|
| speaker | SubtleZoom, PowerCaption |
| video-extract | BRollOverlay (with B-roll video from main video) |
| motion-graphic | MotionGraphic (Hera-generated `.mp4` — only used when `hera: true` in Visual Asset Source Map) |
| showcase-mg | Any showcase component from `src/components/showcase/` — named in `template` field |
| branded-template | UpworkProfile, AgencyBrand |
| chapter-card | ChapterCard |
| cta | SubtleZoom, SocialProofStack, UpworkProfile |
| pip-speaker | PiPSpeaker (with screen share children) |

---

## Social Proof Priority Rule

**CRITICAL: Video scrollovers take priority over static screenshots for Upwork and agency social proof. Static branded templates are the fallback only.**

**Scrollover priority order:**
1. **Video scrollover** (preferred — most authentic): Check these locations for existing scrollover recordings:
   - `example-account-brand-plugin/context/brand/broll/footage/` — brand-level scrollover library (`adam_upwork.mp4`, `apg-website.mp4`, etc.)
   - Most recent working Remotion project's `public/` folder (`broll-upwork-scrollover.mp4`, `apg-website-scrollover.mp4`)
   - Render as `BRollOverlay` with `showVHSOverlay: false` and 8-frame cross-dissolve overlaps between clips
   - Combine as a 3–4 clip montage: Upwork scroll → stage/conference footage → agency website scroll
2. **Static branded template** (fallback — only when no scrollover exists): `UpworkProfile` / `AgencyBrand` component with real screenshot

**Speaking/stage footage:** Include `broll-stage-1.mp4` and `broll-stage-2.mp4` (conference/presentation clips) as part of the social proof montage. These add authority and energy between the Upwork and agency scrollovers.

When the script at a given moment references any of the following, apply the scrollover montage:

- Upwork profile stats (ratings, earnings, project count, Top Rated / Expert Vetted status)
- Agency revenue, client count, or project numbers
- Platform credentials, certifications, or recognition
- Any personal credibility or authority signal tied to an existing branded asset

### Reasoning

Video scrollovers of the real Upwork profile and agency website are more authentic than static screenshots — viewers see the real thing in motion. Conference/stage footage adds authority. Static templates are a cost-free fallback but rank below video for credibility.

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

## Showcase Templates (Long-Form, Non-Hera)

These components live in `video-plugin/skills/2-remotion/references/template-showcase/src/components/` and are copied to `src/components/showcase/` during Remotion Edit scaffold (Step 02). They are the **default choice** for all non-interface MG slots in long-form videos. Use Hera only when none of these fit — see [Hera Eligibility Rules](#hera-eligibility-rules-long-form) below.

Visual type for all showcase segments: `showcase-mg`. VideoRenderer renders them full-screen inside a `<Sequence>`.

### Number / Metric

| Component | File | Best for |
|-----------|------|---------|
| `NumberCountUp` | `NumberCountUp.tsx` | Animated counter — single value counting up from 0. Use for "7.5 HRS", "$2,800/month" hero numbers, ROI totals. Prop: `end`, `prefix`, `suffix`, `duration`. |
| `MetricCard` | `MetricCard.tsx` | Single large stat with label and sub-text. Static or spring-in. Use for authority flash ("250+ PROJECTS"). |
| `StatSplitCard` | `StatSplitCard.tsx` | Two side-by-side stats with labels. Use for dual-stat reveals ("$2,800+/MO + 7.5 HRS/WK"). |
| `ProgressRing` | `ProgressRing.tsx` | Circular progress indicator filling to a target %. Use for completion or capacity metrics. |
| `ROICalculator` | `ROICalculator.tsx` | Running total with line items adding sequentially. Use for multi-chapter ROI accumulator (replaces MG-BODY-01..06). |

### Text / Statement

| Component | File | Best for |
|-----------|------|---------|
| `BoldStatement` | `BoldStatement.tsx` | Large single-line or two-line text reveal. Use for bold directional text ("LET'S BUILD IT"), authority claims. |
| `CinematicReveal` | `CinematicReveal.tsx` | Slow cinematic fade/slide reveal on dark background. Use for mood-setting section openers. |
| `FullscreenTitleCard` | `FullscreenTitleCard.tsx` | Title + subtitle on solid or gradient background. Use for chapter intro moments in the intro segment. |
| `TextRevealMask` | `TextRevealMask.tsx` | Text masked behind a wipe animation — word reveals from a horizontal slide. High-impact for single key phrases. |
| `ParagraphReveal` | `ParagraphReveal.tsx` | Multi-line text fading in line by line. Use for short explanatory callouts. |

### List / Sequential Reveals

| Component | File | Best for |
|-----------|------|---------|
| `ChecklistReveal` | `ChecklistReveal.tsx` | Bullet list with items revealing one-by-one, optional check icons. Use for agendas, feature lists, "5 things you'll learn". |
| `SequentialPillBuild` | `SequentialPillBuild.tsx` | Pill/tag items popping in sequentially. Use for tool lists or tag-style feature bullets. |
| `StackedPillsReveal` | `StackedPillsReveal.tsx` | Stacked horizontal pill rows building from top. Use for agenda lists or categorised groupings. |

### Concept / Diagram

| Component | File | Best for |
|-----------|------|---------|
| `FlowchartAnimation` | `FlowchartAnimation.tsx` | Nodes and connecting arrows animating in sequence. Use for tool/workflow flows (e.g., "Gmail → Claude → structured output"). |
| `TransformationArrow` | `TransformationArrow.tsx` | Before → After split with animated arrow. Use for problem→solution transitions, directional "bridge" moments. |
| `SVGLineTimeline` | `SVGLineTimeline.tsx` | Horizontal or vertical timeline with steps drawing in. Use for process sequences. |
| `TimelineStep` | `TimelineStep.tsx` | Single step card with number, title, and description. Use within a sequence of steps. |

### Logo / Tool Callout (Non-Interface)

| Component | File | Best for |
|-----------|------|---------|
| `ToolLogoGrid` | `ToolLogoGrid.tsx` | Grid of tool logos with names. Use for "connected tools" reveals, integration showcases (Gmail + Calendar CONNECTED). |
| `AIPulseIcon` | `AIPulseIcon.tsx` | Pulsing AI/tool icon with animated aura. Use for single-tool spotlight moments. |
| `GlowingIconPop` | `GlowingIconPop.tsx` | Icon pops in with colour glow matching tool brand. Use for single-tool callout with brand colour. |

### Comparison / Proof

| Component | File | Best for |
|-----------|------|---------|
| `ComparisonTable` | `ComparisonTable.tsx` | Two-column feature comparison. Use for "before AI vs after AI" contrasts. |
| `BeforeAfterSplit` | `BeforeAfterSplit.tsx` | Screen-split before/after with wipe. Use for visible transformations (messy inbox vs organised output). |
| `SplitScreenReveal` | `SplitScreenReveal.tsx` | Two content panels sliding in from sides. Use for dual contrast or side-by-side demos. |
| `ProofQuote` | `ProofQuote.tsx` | Large blockquote with attribution. Use for testimonial or client result moments. |

---

## MG Slot Classification → Template Mapping

For each MG trigger point `[MG-X]` in the script, classify intent, select the primary showcase template, and only reach for Hera if the eligibility rules are satisfied.

| Intent | Showcase candidates (in preference order) | Hera allowed? |
|--------|------------------------------------------|--------------|
| `number` — animated counter | `NumberCountUp`, `ROICalculator`, `StatSplitCard` | No — these handle all counter cases |
| `number` — static flash | `MetricCard`, `BoldStatement` | No |
| `list` — agenda / features | `ChecklistReveal`, `StackedPillsReveal`, `SequentialPillBuild` | No |
| `statement` — bold directional | `BoldStatement`, `TextRevealMask`, `CinematicReveal` | No |
| `concept` — flow / diagram | `FlowchartAnimation`, `TransformationArrow`, `SVGLineTimeline` | No |
| `logo` — tool callout (logo only) | `ToolLogoGrid`, `AIPulseIcon`, `GlowingIconPop` | No |
| `comparison` | `ComparisonTable`, `BeforeAfterSplit` | No |
| `interface` — live tool UI in motion | — | **Yes, if eligibility passes** |

**Type F (Stylized B-Roll):** `BRollOverlay` with CSS filter overlays. Not Hera.
**Type G (Digital Pan/Zoom on a document/screenshot):** `SubtleZoom` extended with `interpolate()` translate. Use Hera only when the pan is over a live interface (eligibility required).

---

## Hera Eligibility Rules (Long-Form)

A storyboard segment may be assigned to Hera only if **all three** of the following are true:

1. **Subject is a named coding tool or AI interface** — Claude, ChatGPT, Cursor, n8n, Gmail, VS Code, Warp, Airtable, Notion, a terminal, a code editor, a browser dashboard, etc. Generic concepts, numbers, lists, or diagrams are NOT eligible.
2. **The motion requires a live interface** — zoom-into-UI, text typing in a field, logs filling a terminal, a button being clicked, an agent running. The showcase library cannot replicate this. If a static logo + "CONNECTED" label suffices, use `ToolLogoGrid` instead.
3. **A usable reference image exists or can be fetched** — frame-extract from the source video where the tool is visible, or a web-screenshot via the logo waterfall resolver. Hera without a reference image produces generic chrome that looks fabricated. If no reference image is obtainable, fall back to the showcase template.

If any condition fails → **must use a showcase template**.

**Maximum Hera MGs per video:** ≤ 3 in the intro, ≤ 1 per body section. If the video contains no screen-share footage of a specific tool (only the speaker talking about it), Hera count is 0 — use showcase templates throughout.

**Storyboard flag:** Segments approved for Hera must carry `hera: true` in the Visual Asset Source Map row. The [HM] Hera Motion Graphics workflow will reject any brief without this flag.

---

## Template Reuse Cap

To prevent visual monotony, the following caps apply across the whole storyboard:

| Scope | Rule |
|-------|------|
| Intro | No single showcase template may appear more than **2 times** |
| Full video | No single showcase template may appear more than **3 times** |
| Adjacent MGs | Two MG segments separated only by a speaker segment must not use the same template |
| Body ROI counters | `ROICalculator` or `NumberCountUp` used for a running-total narrative is a **named exception** — the same template may repeat once per chapter to build continuity, but each instance must have a distinct `startValue`/`endValue` pair |

**Application in step 4:** Before assigning a showcase template, tally how many times it has already been assigned. If the intro cap (2) or full-video cap (3) would be exceeded, move to the next candidate in the preference order. Document the cap-trigger and final choice in the Visual Asset Source Map `notes` field.

---

## Motion Graphic Type Reference (Legacy Labels)

The A–G labels from inspiration analysis still appear in script stage directions. This table maps them to the new showcase-first approach.

| Legacy Type | Description | Primary approach | Hera? |
|-------------|-------------|-----------------|-------|
| A: Text/Number | Bold number/metric | `NumberCountUp` (counter) or `MetricCard` / `BoldStatement` (flash) | No |
| B: Logo Graphic | Tool logo callout | `ToolLogoGrid` / `GlowingIconPop` (logo only); Hera `interface-zoom` (if live interface needed + eligibility) | Conditional |
| C: UI Mockup | Live interface in motion | Hera `interface-ui-mockup` (if eligibility passes) | Conditional |
| D: Concept Graphic | Abstract diagram | `FlowchartAnimation` / `TransformationArrow` | No |
| E: Sequential Reveals | Bullet list | `ChecklistReveal` / `StackedPillsReveal` | No |
| F: Stylized B-Roll | Footage + post-processing | `BRollOverlay` (clean); Hera only for film-grain effects on source footage | No (usually) |
| G: Digital Pan/Zoom | Pan across static content | `SubtleZoom` (zoom-only); Hera `interface-pan` (pan over live interface, eligibility required) | Conditional |

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
| `motion-graphic` | MotionGraphic (wraps Hera-generated `.mp4`) |
| `showcase-mg` | Showcase component named in `template` field (e.g. `NumberCountUp`, `ChecklistReveal`) |
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
| `showcaseProps` | showcase-mg | Full props object passed to the named showcase component |

### Benefits

- **Zero per-segment files** — eliminates 15–40 SegXX.tsx files per composition
- **AI produces data only** — SEGMENTS array in theme.ts, not code
- **Deterministic rendering** — same data = same output, no generation errors
- **Works for all video types** — intro, body, full-video, short-form
- **Template components shared** — via sidecar, consistent across projects

### When NOT to Use

- If a segment needs truly custom rendering logic not covered by any template
- In that case, create a single custom component and add it as a special case in the VideoRenderer switch
