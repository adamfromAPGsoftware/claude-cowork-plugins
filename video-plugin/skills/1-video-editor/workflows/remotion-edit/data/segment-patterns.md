# Segment Generation Patterns

## Overview

**VideoRenderer mode is the default.** When `VideoRenderer.tsx` is present (copied from sidecar by step-02-scaffold), the AI produces ONLY the `SEGMENTS` array in `theme.ts` — no per-segment `SegXX.tsx` files are needed. The VideoRenderer dispatches each segment to the correct template component based on `visualType` and props in the segment data.

**Legacy SegXX patterns below are for reference only and should NOT be used unless VideoRenderer.tsx is missing.** They document the rendering logic that VideoRenderer handles automatically.

The following patterns describe how each `visual_type` maps to a Remotion component. When using VideoRenderer, these patterns are handled internally — the AI's job is to populate the correct fields in each SEGMENTS entry.

---

## Pattern 1: Speaker Segment

**Visual Type:** `speaker`
**Template:** Main video footage of speaker on camera

```tsx
import React from 'react';
import { OffthreadVideo } from 'remotion';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <OffthreadVideo
        src={seg.sourceFile}
        startFrom={seg.startFrame}
        muted
        pauseWhenBuffering
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
    </div>
  );
};
```

**When to use:** Speaker visible on camera, standard footage.

**Long-form intro exception:** Speaker segments in long-form intros do NOT include any caption, PowerCaption, or KineticCaption text overlays. The rapid-fire visual pacing (motion graphics, B-roll, branded templates) provides sufficient visual density without caption overlays on speaker segments.

**Critical:** Speaker segments MUST include `startFrom={seg.startFrame}` on `<OffthreadVideo>` so the video seeks to the correct position matching the continuous audio track.

**Long-Form Intro Guidance — Jump-Cut Zoom:**
For consecutive speaker segments in long-form intros, alternate the scale between cuts to create a jump-cut zoom effect (confirmed across 4/5 inspiration creators):
- Even-indexed speaker segments: `transform: scale(1.0)` (base)
- Odd-indexed speaker segments: `transform: scale(1.05)` to `scale(1.15)` (punched in)
- Always use `transformOrigin: 'center center'` for consistency
- This is a subtle zoom alternation — not a dramatic zoom effect

---

## Pattern 2: B-Roll Overlay Segment

**Visual Type:** `broll`
**Template:** B-roll video clip (screen recording or extracted clip)

```tsx
import React from 'react';
import { BRollOverlay } from './BRollOverlay';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <BRollOverlay
      src={seg.sourceFile}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
      style="fullscreen"
      captionText={seg.captionText}
      captionPosition={seg.captionPosition}
    />
  );
};
```

**When to use:** Screen recordings, tool demonstrations, visual evidence clips.

**Critical:** The BRollOverlay component's internal `<OffthreadVideo>` MUST have `muted`, `pauseWhenBuffering`, and the correct style.

---

## Pattern 3: Motion Graphic Segment

**Visual Type:** `motion-graphic`
**Template:** Hera-generated motion graphic clip — uses `MotionGraphic` component (NOT BRollOverlay)

```tsx
import React from 'react';
import { MotionGraphic } from './MotionGraphic';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <MotionGraphic
      src={seg.sourceFile}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
      captionText={seg.captionText}
      captionPosition={seg.captionPosition}
    />
  );
};
```

**When to use:** Hera-generated title cards, transitions, abstract visualizations.

**Critical:** Motion graphics MUST use `MotionGraphic` (clean, full-color playback with fade in/out). NEVER use `BRollOverlay` for motion graphics — the VHS desaturation effect is exclusively for video-extract segments (real b-roll pulled from the main recording). AI-generated motion graphics should look polished, not retro.

**MG Duration Matching Rule:**
- The Hera MG clip duration MUST match the storyboard segment duration (±0.5s)
- Set `duration_seconds` in the Hera API request to `durationInFrames / fps`
- If clip is shorter than segment: MotionGraphic shows last frame frozen then fades out — looks bad
- If clip is longer: truncated at segment end — acceptable but wasteful
- CRITICAL: Always match durations to avoid frozen frames

---

## Pattern 4: Chapter Card Segment

**Visual Type:** `chapter-card`
**Template:** Branded chapter transition card — uses `ChapterCard` sidecar template

```tsx
import React from 'react';
import { ChapterCard } from './ChapterCard';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <ChapterCard
      title={seg.captionText ?? ''}
      chapterNumber={seg.chapterNumber}
      durationInFrames={seg.durationInFrames}
    />
  );
};
```

**When to use:** Chapter transitions between body sections. 2–4 seconds duration.

**Design:** Dark gradient background (#0A0A0A), green (#2D6A4F) vertical accent bar, chapter number in green, title in white Inter 700. Fade-in + slide-up animation (10 frames in/out). Consistent across ALL videos — zero AI decisions needed beyond title text and chapter number.

**VideoRenderer mode:** The `VideoRenderer.tsx` dispatches chapter-card segments to `ChapterCard` automatically. The SEGMENTS entry needs `captionText` (title), optional `chapterNumber`, and `durationInFrames`.

---

## Pattern 5: CTA Segment

**Visual Type:** `cta`
**Template:** Call-to-action with optional speaker + social proof

```tsx
import React from 'react';
import { OffthreadVideo } from 'remotion';
import { SocialProofStack } from './SocialProofStack';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <OffthreadVideo
        src={seg.sourceFile}
        startFrom={seg.startFrame}
        muted
        pauseWhenBuffering
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
      {seg.notes && seg.notes.includes('social-proof') && (
        <SocialProofStack
          items={JSON.parse(seg.notes.split('items:')[1] || '[]')}
          startFrame={0}
          durationInFrames={seg.durationInFrames}
          style="sequential"
        />
      )}
    </div>
  );
};
```

**When to use:** Final call-to-action section. Speaker on camera with optional social proof overlay.

**Critical:** CTA segments using the main speaker video MUST include `startFrom={seg.startFrame}` on `<OffthreadVideo>` to maintain audio sync.

---

## Pattern 6: Speaker with SubtleZoom Segment

**Visual Type:** `speaker` with `template: SubtleZoom`
**Template:** Slow zoom in on speaker for emphasis

```tsx
import React from 'react';
import { SubtleZoom } from './SubtleZoom';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <SubtleZoom
      src={seg.sourceFile}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
      zoomFactor={1.15}
      videoStartFrom={seg.startFrame}
    />
  );
};
```

**When to use:** Key statements, emotional moments, hook emphasis. The SubtleZoom component's internal `<OffthreadVideo>` MUST have `muted`, `pauseWhenBuffering`, and the correct style.

**Critical:** Speaker segments using SubtleZoom MUST pass `videoStartFrom={seg.startFrame}` so the internal OffthreadVideo seeks to the correct position matching the continuous audio track.

---

## Logo Acquisition for Custom Components

When a segment requires tool or brand logos (e.g., a FourToolStack or comparison graphic), use the **Creative Director's logo fetch pipeline** — do not guess URLs or manually search.

### Primary source: Simple Icons (Tier 1)

Simple Icons (simpleicons.org) provides 3300+ free brand SVGs under CC0. The jsDelivr CDN URL format is:

```
https://cdn.jsdelivr.net/npm/simple-icons@v16/icons/{slug}.svg
```

Find the correct slug by searching simpleicons.org. Common slugs: `anthropic`, `cursor`, `openai`, `github`, `notion`, `slack`, `vercel`, `supabase`, `docker`, `python`, `nodejs`.

**Downloaded SVGs have no fill by default** — add `fill="white"` (or the brand hex) to the `<svg>` tag for dark backgrounds:

```bash
# Download and make white
curl -s "https://cdn.jsdelivr.net/npm/simple-icons@v16/icons/anthropic.svg" \
  -o "public/branded-assets/logos/anthropic.svg"
sed -i '' 's/<svg /<svg fill="white" /' "public/branded-assets/logos/anthropic.svg"
```

**Brand colors** are available at `https://simpleicons.org/?q={name}` — shown as the hex beneath each icon. Apply with `fill="#HEX"` for colored versions.

### Full 4-tier waterfall

For brands not in Simple Icons, use the Creative Director's `fetch-logo.ts` waterfall:
`Simple Icons → SVG Logos → Logotypes.dev → Logo.dev`

```bash
npx tsx scripts/fetch-logo.ts --name "ToolName" --output public/branded-assets/logos/tool.svg
```

See: `content-plugin/skills/3-creative-director/workflows/visual-asset-creation/steps-c/step-06-logo.md`

### Remotion usage

In Remotion, reference downloaded logos with `staticFile()` and render with `<Img>`:

```tsx
import { Img, staticFile } from 'remotion';

<Img
  src={staticFile('branded-assets/logos/anthropic.svg')}
  style={{ width: 100, height: 100, objectFit: 'contain' }}
/>
```

**Note:** `<Img>` is permitted in custom branded components (FourToolStack, AgencyBrand, etc.) — the "no Img" hard rule applies only to B-roll Seg files.

---

## Pattern 7: Branded Template Segment

**Visual Type:** `branded-template`
**Template:** Constant branded Remotion component (UpworkProfile or AgencyBrand)

```tsx
import React from 'react';
import { UpworkProfile } from './UpworkProfile';
// OR: import { AgencyBrand } from './AgencyBrand';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', backgroundColor: '#0a0a0a' }}>
      <UpworkProfile
        startFrame={0}
        durationInFrames={seg.durationInFrames}
        position="center"
      />
    </div>
  );
};
```

**When to use:** Authority building, social proof, branding moments. These are CONSTANT templates — same animation every time, using fixed brand assets from `public/branded-assets/`.

**CRITICAL — Consistent branded template style:** Both `UpworkProfile` and `AgencyBrand` MUST use the same full-screen social proof card layout when displaying credentials. NEVER use `lower-third` for AgencyBrand during credibility segments — it renders as a tiny bar in the bottom-left that is barely visible. Always use `style="full-screen"` so the agency homepage screenshot fills the frame with the stat headline above it, matching the UpworkProfile card's visual weight.

**Note:** Branded templates use `<Img>` internally for static brand assets (not video). This is the ONE exception to the "no Img" rule — branded templates display static images (logos, profile photos), not B-roll.

---

## Pattern 8: Body Video Segment (Multi-Clip Composition)

**Visual Type:** `body-video`
**Template:** Single OffthreadVideo for the full clipped body recording

This pattern is NOT a Seg{NN}.tsx file — it is added directly to Root.tsx as a Sequence after all intro segments and a WhiteFlash transition.

```tsx
// In Root.tsx — after the intro segment map:

{/* White Flash Transition */}
<Sequence
  from={TRANSITION.startFrame}
  durationInFrames={TRANSITION.durationInFrames}
  premountFor={30}
  name="Transition - White Flash Intro to Body"
>
  <div style={{ width: '100%', height: '100%', backgroundColor: '#000' }}>
    <WhiteFlash durationInFrames={TRANSITION.durationInFrames} />
  </div>
</Sequence>

{/* Body Video — base continuous clip */}
<Sequence
  from={BODY.startFrame}
  durationInFrames={BODY.durationInFrames}
  premountFor={30}
  name="Body - Full Clipped Video"
>
  <OffthreadVideo
    src={BODY.sourceFile}
    muted
    pauseWhenBuffering
    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
  />
</Sequence>

{/* Body Overlays — Chapter Cards */}
{BODY_CHAPTERS.map((ch, i) => (
  <Sequence
    key={i}
    from={ch.startFrame}
    durationInFrames={ch.durationInFrames}
    premountFor={30}
    name={`Chapter Card - ${ch.title}`}
  >
    <ChapterCard title={ch.title} />
  </Sequence>
))}

{/* Body Overlays — PiP Speaker */}
{BODY_PIP_SECTIONS.map((pip, i) => (
  <Sequence
    key={i}
    from={pip.startFrame}
    durationInFrames={pip.durationInFrames}
    premountFor={30}
    name={`PiP Speaker - Section ${i + 1}`}
  >
    <PiPSpeaker
      speakerSrc={pip.speakerSrc}
      speakerStartFrom={pip.speakerStartFrom}
      durationInFrames={pip.durationInFrames}
      position="bottom-right"
      size={15}
      shape="rounded-rect"
    />
  </Sequence>
))}

{/* Body Overlays — Digital Zoom (applied via style on body OffthreadVideo wrapper) */}
{/* Zoom keyframes are defined in BODY_ZOOMS and applied as CSS transform overrides */}
```

**When to use:** Multi-clip compositions where both intro and body are rendered as one video. The body clip plays as a single continuous OffthreadVideo — no segment decomposition into Seg files. Overlays (chapter cards, PiP speaker, digital zoom) are layered as separate Sequences on top of the base clip.

**Theme constants required:**
- `BODY.sourceFile` — path to body-clipped.mp4
- `BODY.durationInFrames` — probed via ffprobe
- `BODY.startFrame` — intro totalFrames + transition duration
- `TRANSITION.startFrame` — intro totalFrames (where intro segments end)
- `TRANSITION.durationInFrames` — **18 frames (0.3s at 60fps / 0.6s at 30fps).** The flash should be a quick, snappy transition — not a pause. The viewer should barely register the flash as it bridges the visual cut between intro and body. Avoid long transition holds that break the flow.
- `BODY_CHAPTERS` — array of `{ startFrame, durationInFrames, title }` for chapter card overlays
- `BODY_PIP_SECTIONS` — array of `{ startFrame, durationInFrames, speakerSrc, speakerStartFrom }` for PiP overlays
- `BODY_ZOOMS` — array of `{ startFrame, durationInFrames, scale, targetX, targetY }` for digital zoom keyframes

**Audio:** Concatenate intro + 0.3s silence (matching 18-frame WhiteFlash duration at 60fps) + body audio into a single `full-audio.m4a` file to preserve the single Audio element rule (Rule 4).

---

## Pattern 9: PiP Speaker Over Screen Share

**Visual Type:** `pip-speaker`
**Template:** Speaker in corner PiP overlay on top of full-frame screen share content

```tsx
import React from 'react';
import { OffthreadVideo } from 'remotion';
import { PiPSpeaker } from './PiPSpeaker';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <PiPSpeaker
      speakerSrc={seg.sourceFile}
      speakerStartFrom={seg.startFrame}
      durationInFrames={seg.durationInFrames}
      position="bottom-right"
      size={15}
      shape="circle"
      borderColor="#FFFFFF"
      borderWidth={3}
    >
      <OffthreadVideo
        src={seg.screenShareFile}
        muted
        pauseWhenBuffering
        style={{ width: '100%', height: '100%', objectFit: 'contain' }}
      />
    </PiPSpeaker>
  );
};
```

**When to use:** Screen share tutorial content with speaker visible in corner. The defining pattern of long-form tutorial editing. Speaker maintains personal connection while demonstrating on-screen content.

**Critical:**
- Speaker `<OffthreadVideo>` inside PiPSpeaker MUST have `muted`, `pauseWhenBuffering`, and `startFrom`
- Screen share `<OffthreadVideo>` (children) MUST also have `muted` and `pauseWhenBuffering`
- Screen share typically uses `objectFit: 'contain'` (not `'cover'`) to preserve UI layout
- PiP position should avoid overlapping caption text (default: bottom-right, captions: bottom-center or bottom-left)

**Props reference:**
- `position`: `bottom-right` | `bottom-left` | `top-right` | `top-left`
- `size`: % of frame width (default: 15%)
- `shape`: `circle` | `rounded-rect` | `rect`
- `borderColor`, `borderWidth`, `shadowEnabled`: visual styling
- `animateIn`: frames for scale-in entrance (default: 12, set 0 to disable)

---

## Pattern Selection Rules

| visual_type | template | Pattern |
|------------|----------|---------|
| speaker | (no overlay) | Pattern 1 |
| speaker | SubtleZoom | Pattern 6 |
| video-extract | BRollOverlay | Pattern 2 |
| motion-graphic | MotionGraphic | Pattern 3 |
| chapter-card | — | Pattern 4 |
| cta | — | Pattern 5 |
| branded-template | UpworkProfile / AgencyBrand | Pattern 7 |
| pip-speaker | PiPSpeaker | Pattern 9 |

## Hard Rule Compliance

Every generated segment MUST comply with ALL hard rules. Double-check:
- `muted` on every `<OffthreadVideo>`
- `pauseWhenBuffering` on every `<OffthreadVideo>`
- `style={{ width: '100%', height: '100%', objectFit: 'cover' }}` on every `<OffthreadVideo>`
- No `<Audio>` elements
- No `<Img>` or `<img>` tags
- All public asset paths use `staticFile()` (never bare path strings)
- Speaker segments include `startFrom={seg.startFrame}` on `<OffthreadVideo>`
- `OffthreadVideo` imported from `'remotion'`, NOT `'@remotion/media-utils'`
- Branded templates use `staticFile()` + `<Img>`, never `require()`
