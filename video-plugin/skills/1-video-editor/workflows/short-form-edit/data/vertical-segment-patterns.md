# Vertical Segment Patterns (9:16)

## Overview

These are the 7 code generation patterns for vertical (1080×1920) short-form Seg{NN}.tsx files. Each pattern maps to a visual type in the storyboard. Select the matching pattern and fill in props from the SEGMENTS array in theme.ts.

---

## Pattern V1: Speaker

**Visual Type:** `speaker`
**Template:** `SubtleZoom` (standard slow zoom)
**Production params:** zoom 1.03, no burned-in captions (platform-native)

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
      zoomFactor={1.03}
      videoStartFrom={seg.startFrame}
    />
  );
};
```

**When to use:** Standard speaker shot. Source may be landscape 4K or vertical 9:16.
**Critical:** `videoStartFrom={seg.startFrame}` maintains audio sync.
**Production note:** Zoom factor 1.03 (not 1.08) — inspiration videos use barely perceptible zoom.
**Source framing:** Source is landscape 16:9. Pass `objectPosition="center 25%"` to SubtleZoom for face framing (tight centre-crop, ~32% of frame width visible).

---

## Pattern V2: Speaker Zoom (Emphasis)

**Visual Type:** `speaker-zoom`
**Template:** `SubtleZoom` with moderate zoom for emphasis
**Production params:** zoom 1.08, no burned-in captions (platform-native)

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
      zoomFactor={1.08}
      videoStartFrom={seg.startFrame}
    />
  );
};
```

**When to use:** Hook moments, emphasis, emotional peaks. Zoom 1.08 (not 1.25) — inspiration videos never exceed 1.08.
**Production note:** Old value was 1.25 which looked amateur. Real top creators use subtle zoom only.
**Source framing:** Source is landscape 16:9. Pass `objectPosition="center 25%"` to SubtleZoom for face framing (tight centre-crop, ~32% of frame width visible).

---

## Pattern V3: B-Roll

**⚠️ DEPRECATED FOR SHORT-FORM** — use V4/V4b with Hera MG instead. B-roll extracts serve only as reference frames for Hera prompts. V3 remains available for full-length landscape videos only.

**Visual Type:** `broll`
**Template:** `VerticalBRollOverlay`

```tsx
import React from 'react';
import { VerticalBRollOverlay } from './VerticalBRollOverlay';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <VerticalBRollOverlay
      src={seg.sourceFile}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
      style="fullscreen"
    />
  );
};
```

**When to use:** Full-length landscape videos only. NOT for short-form — use V4/V4b/V5 with Hera MG instead.

---

## Pattern V4: Motion Graphic

**Visual Type:** `motion-graphic`
**Template:** `MotionGraphic`

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
      zoomFactor={1.15}
    />
  );
};
```

**When to use:** Motion graphics (any tier) at 9:16 aspect ratio.
**Production note:** `zoomFactor={1.15}` applies mandatory Ken Burns zoom (1.0→1.15 over segment duration). Static MG display is FORBIDDEN. Use `1.3` for aggressive UI highlight zoom.
**Minimum duration:** 60 frames (2 seconds). If segment is shorter than 2s, simplify the Hera prompt to a single motion (e.g., one logo reveal, one counter tick) so the animation completes within the time.

---

## Pattern V4b: MG Cutaway (Interstitial)

**Visual Type:** `motion-graphic-cutaway`
**Template:** `MotionGraphic`
**Production params:** 2-3 seconds (60-90 frames @ 30fps), NO caption overlay — voiceover continues from adjacent speaker segment

```tsx
import React from 'react';
import { MotionGraphic } from './MotionGraphic';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <MotionGraphic
      src={seg.sourceFile!}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
      zoomFactor={1.1}
    />
  );
};
```

**When to use:** Brief 2-3 second MG cutaway (any tier) interleaved between speaker segments. Provides visual variety without interrupting flow. No caption needed — the speaker's voiceover plays through from the adjacent segment.
**Content rules:**
- Tool/platform mentioned → tool logo MG
- Build/creation action → typing/coding animation
- Statistic cited → animated counter
- Default → abstract tech/data flow
**Duration:** 60-90 frames (2-3s at 30fps). Never shorter than 60 frames. Never longer than 90 frames.
**Frequency:** At least 1 per 10-12 seconds. For a 30s video, minimum 2 MG cutaways.
**Prompt simplification for 2s MGs:** When duration is 2 seconds (60 frames), limit the Hera prompt to ONE primary motion (e.g., "logo fades in and settles" not "logo fades in, rotates, glows, and settles with particles"). Longer MGs (3s+) can include 2-3 motion stages.
**Tier A logo coloring (CRITICAL):** Logos fetched via `fetch-logo.ts` (Simple Icons) are black silhouettes. When rendering Tier A logo MGs in Remotion, apply the brand color using CSS mask technique — NOT by relying on the PNG color:
```tsx
// CORRECT — CSS mask applies brand color to black logo PNG
<div style={{
  width: '40%', aspectRatio: '1',
  backgroundColor: '#D97757',  // Claude brand orange
  WebkitMaskImage: `url(${staticFile('logos/claude-logo.png')})`,
  WebkitMaskSize: 'contain', WebkitMaskRepeat: 'no-repeat', WebkitMaskPosition: 'center',
  maskImage: `url(${staticFile('logos/claude-logo.png')})`,
  maskSize: 'contain', maskRepeat: 'no-repeat', maskPosition: 'center',
}} />
// WRONG — renders black logo (Simple Icons default)
<Img src={staticFile('logos/claude-logo.png')} />
```
Common brand colors: Claude `#D97757`, YouTube `#FF0000`, VS Code `#007ACC`, Slack `#4A154B`, GitHub `#181717`.

---

## Pattern V5: Split Screen

**Visual Type:** `split-screen`
**Template:** `VerticalSplitScreen`
**Production params:** 50/50 ratio (content top, speaker bottom), hard-cut transitions only, no visible divider, no burned-in captions (platform-native)

```tsx
import React from 'react';
import { VerticalSplitScreen } from './VerticalSplitScreen';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <VerticalSplitScreen
      speakerSrc={seg.sourceFile}
      overlaySrc={seg.overlayFile!}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
      videoStartFrom={seg.startFrame}
      variant="split"
      dividerColor="transparent"
      speakerPosition="bottom"
      overlayPadding
    />
  );
};
```

**When to use:** Content/screen-recording top (50%) + speaker bottom (50%). This is the dominant layout in top-performing reels — 4/5 inspiration videos use 50/50 split.
**Production note:** Speaker goes BOTTOM (not top). 50/50 gives the speaker more presence than 65/35.
**Overlay source:** `overlaySrc` must point to an MG file (`motion-graphics/...`) from any tier, never raw B-roll.
**Overlay padding:** ALWAYS pass `overlayPadding` — the overlay zone renders the MG at 96% size with light (#F5F5F5) background and `objectFit: cover`, providing a minimal safe margin while filling the zone. This is the **sole padding mechanism** — FFmpeg pre-padding (`v5Padding`) is deprecated. The MG should fill nearly the entire overlay zone with just a thin 2% border on each side.
**Overlay aspect ratio:** V5 overlay MGs MUST be **16:9 landscape** (not 9:16). The top zone is ~2160×1920 (~9:8), so 9:16 MGs lose ~50% content to cropping. 16:9 landscape MGs lose only ~13% side crop via `objectFit: cover`, preserving the visual content. Upscale landscape MGs to 3840×2160 (landscape 4K).
**V5 overlay safe margin:** When creating V5 overlay MGs (all tiers), key content MUST be centered with 15% safe margin on left/right edges to account for the ~13% side crop from `objectFit: cover`.
**Divider:** `dividerColor="transparent"` — 5/5 analyses show NO visible divider.
**Hook usage:** V5 is the PRIMARY hook pattern (4/5 top performers). The top half MUST show the video's **hero keyword visual** (tool logo, UI, or code interface MG) — never text. See P4a in pacing rules. Bottom half shows speaker face.

---

## Pattern V6: Hook Text

**Visual Type:** `hook-text`
**Template:** `VerticalHookText`

```tsx
import React from 'react';
import { VerticalHookText } from './VerticalHookText';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <VerticalHookText
      text={seg.captionText!}
      highlight={seg.captionHighlight}
      startFrame={0}
      durationInFrames={seg.durationInFrames}
    />
  );
};
```

**⚠️ DEPRECATED AS DEFAULT HOOK OPENER.** Real top-performing shorts open with V5 (split-screen with hero keyword visual) — not text cards. V6 may still be used mid-video for emphasis text cards only.

**When to use:** Mid-video emphasis text cards only. NOT for hook openings — use V5 (split-screen with hero keyword visual) as the hook instead. V6 may be used mid-video for emphasis text cards only.

---

## Pattern V7: CTA

**Visual Type:** `cta`
**Template:** `SubtleZoom` + `SocialProofStack`, no burned-in captions (platform-native)

```tsx
import React from 'react';
import { SubtleZoom } from './SubtleZoom';
import { SocialProofStack } from './SocialProofStack';
import { SEGMENTS } from './theme';

const seg = SEGMENTS[{INDEX}];

export const Seg{NN}: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <SubtleZoom
        src={seg.sourceFile}
        startFrame={0}
        durationInFrames={seg.durationInFrames}
        zoomFactor={1.05}
        videoStartFrom={seg.startFrame}
      />
      {seg.notes?.includes('social-proof') && (
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

**When to use:** Final CTA section with optional social proof overlay.
**Production note:** Zoom 1.05 (not 1.08) — distinct from V2, subtle emphasis for closing. **Abrupt ending** — zero dead frames, no end card, loop-encouraging. Comment-based CTA pattern (4/5 videos).

---

## Pattern Selection Rules

| visual_type | Pattern | Template |
|------------|---------|----------|
| speaker | V1 | SubtleZoom (1.03) |
| speaker-zoom | V2 | SubtleZoom (1.08) |
| broll | V3 (DEPRECATED for short-form) | VerticalBRollOverlay |
| motion-graphic | V4 | MotionGraphic |
| motion-graphic-cutaway | V4b | MotionGraphic (no caption, 60-90 frames) |
| split-screen | V5 | VerticalSplitScreen (overlay MGs must be 16:9 landscape) |
| hook-text | V6 | VerticalHookText |
| cta | V7 | SubtleZoom (1.05) + SocialProofStack |

**Hook pattern:** V5 split-screen is the PRIMARY hook pattern (4/5 top performers). V2 speaker-zoom is acceptable but NOT primary.

## Hard Rule Compliance

**For short-form:** All non-speaker visuals use V4, V4b, or V5 with MG overlays (Tier A: Remotion-native, Tier C: Hera with library reference image). V3 and Tier B are deprecated. All MG visuals MUST have zoom (zoomFactor prop) — static display is FORBIDDEN.

Every generated segment MUST comply with ALL hard rules (19 base + 5 vertical). Double-check:
- `muted` on every `<OffthreadVideo>`
- `pauseWhenBuffering` on every `<OffthreadVideo>`
- `style={{ width: '100%', height: '100%', objectFit: 'cover' }}` on every `<OffthreadVideo>`
- No `<Audio>` elements in segment files
- No `<Img>` or `<img>` tags in segment files
- Speaker segments include `videoStartFrom={seg.startFrame}`
- `objectPosition` on speaker video only when source is landscape AND `objectFit: 'cover'` present (Rule V5)
- No segment longer than 120 frames (Rule V3 — 4 seconds @ 30fps)
