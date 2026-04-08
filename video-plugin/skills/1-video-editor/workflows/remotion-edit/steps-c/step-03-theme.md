---
name: 'step-03-theme'
description: 'Generate theme.ts with SEGMENTS, OVERLAYS, CAPTIONS, colors, FPS'

nextStepFile: './step-04-segments.md'
---

# Step 3: Generate Theme Configuration

## STEP GOAL:

Generate the `theme.ts` file that defines all constants for the Remotion project: segment definitions, overlay timing, caption configuration, color palette, FPS, and total duration.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction
- ALL timing values must be in frames (not seconds)
- **Resolution and FPS MUST be probed from the source video** — never hardcode defaults
- Every segment from the master timeline gets an entry in SEGMENTS

## MANDATORY SEQUENCE

### 1. Probe Source Video Properties

**CRITICAL:** The Remotion composition MUST match the source video's native resolution and frame rate. Never hardcode defaults — always probe.

Run ffprobe on the main source video (the clipped speaker video in `public/`):

```bash
ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name -of json {source_video_path}
```

Extract:
- **width** and **height** — use these as `PROJECT.width` and `PROJECT.height`
- **r_frame_rate** — parse the fraction (e.g., `30/1` → 30, `60/1` → 60, `30000/1001` → 29.97 → round to 30). Use this as `PROJECT.fps`
- Confirm codec is h264/h265 (expected)

If the source video is 3840x2160 at 30fps, the composition is 3840x2160 at 30fps. If it's 1920x1080 at 60fps, the composition is 1920x1080 at 60fps. The output always matches the input.

### 2. Extract Constants from Storyboard

From the master timeline, extract:
- Total duration in frames (using the probed FPS from step 1)
- Number of segments
- All unique templates used
- Color references from the storyboard

### 3. Generate SEGMENTS Array

**CRITICAL:** When translating the master timeline to SEGMENTS entries, preserve the exact `startFrame` and `durationInFrames` values from the storyboard. These values were calibrated against the transcript's word-level timestamps during storyboard timeline assembly. Do NOT round, adjust, or "clean up" frame values — they are precise.

For caption segments (those with `captionText`), the segment boundaries ensure the caption is on screen when the speaker says those words. Any drift in these values will cause visible caption/audio desync.

For each row in the master timeline, create a segment definition:

**VideoRenderer mode:** When using the VideoRenderer (recommended), the SEGMENTS array is the ONLY data the AI needs to produce — no per-segment SegXX.tsx files are generated. The Segment type includes all rendering props (captions, styles, branded template data, PiP config). See `VideoRenderer.tsx` for the complete `Segment` type definition.

```typescript
import { staticFile } from 'remotion';

export const SEGMENTS = [
  {
    id: 'seg-001',
    startFrame: 0,
    durationInFrames: 75,
    visualType: 'speaker',
    template: 'SubtleZoom',
    sourceFile: staticFile('intro-clipped.mp4'),
    startFrom: 0,
    bounceIn: true,              // First segment bounce-in
    captionText: 'Hook text here',
    captionHighlight: 'Hook',
    captionPosition: 'bottom-left',
    section: 'hook',
    brollRef: null,
  },
  // ... one entry per timeline segment
] as const;
```

### 4. Generate OVERLAYS Configuration

Font sizes MUST be scaled for the target composition height. The base sizes assume 1080p (height=1080). Scale proportionally: `fontSize = Math.round(baseSize * height / 1080)`.

| Composition | defaultFontSize (base 36) | kineticFontSize (base 48) |
|------------|--------------------------|--------------------------|
| 1080p | 36 | 48 |
| 1440p | 48 | 64 |
| 4K (2160p) | 72 | 96 |

```typescript
// --- FIXED CONSTANTS (do not modify — only height changes per video) ---
// CAPTION STYLE: PowerCaption only — no background, no box, no pill. See caption-style-spec.md.
export const OVERLAYS = {
  captions: {
    defaultPosition: 'bottom-center',
    defaultColor: '#FFFFFF',
    // NO defaultBackgroundColor — spec mandates no background on captions
    defaultFontSize: Math.round(36 * height / 1080),   // resolution-scaled
    kineticFontSize: Math.round(48 * height / 1080),    // resolution-scaled
  },
  broll: {
    defaultStyle: 'fullscreen',
    transitionFrames: 8,
  },
} as const;
```

**OVERLAYS is a fixed constant** — the only variable is `height` (from ffprobe). The AI computes the font sizes from `height` and copies everything else exactly. Never modify the structure or base values.

### 5. Generate Project Constants

**Use the values probed from the source video in Step 1 — never hardcode resolution or FPS.**

```typescript
export const PROJECT = {
  fps: {probed_fps},              // From ffprobe r_frame_rate
  width: {probed_width},          // From ffprobe width
  height: {probed_height},        // From ffprobe height
  totalDurationInFrames: {calculated_total},
  compositionId: '{composition-name}',
  audioSource: staticFile('{clipped-source}.mp4'),
  sourceFile: staticFile('{clipped-source}.mp4'),
  audioOffsetMs: 0, // Adjustable in Remotion Studio sidebar — tweak for lip sync
} as const;

// --- FIXED CONSTANTS (do not modify) ---
export const COLORS = {
  primary: '#FFFFFF',
  secondary: '#000000',
  accent: '#FF6B35',      // Canonical PowerCaption orange — never change this
  brand: '#2D6A4F',       // green — chapter cards, branded accents
  background: '#0A0A0A',  // Dark background for chapter cards, branded overlays
} as const;
```

**COLORS is a fixed constant** — identical across all videos. The AI should copy-paste it exactly. Never modify these values.

### 6. Wrap All Paths with staticFile()

**CRITICAL:** theme.ts MUST `import { staticFile } from 'remotion'` at the top. ALL file path values that reference files in the `public/` directory MUST be wrapped in `staticFile()` as an **actual function call**, not a string representation.

This applies to:
- `sourceFile` on every segment
- `audioSource` in PROJECT
- **`imageSrc` on branded-template segments** (AgencyBrand, UpworkProfile custom images)

```typescript
// CORRECT — actual staticFile() call, resolves at runtime
imageSrc: staticFile('branded-assets/agency-homepage.png'),

// WRONG — string containing the text "staticFile(...)" — image will NOT load
imageSrc: "staticFile('branded-assets/agency-homepage.png')",
```

```typescript
import { staticFile } from 'remotion';

// CORRECT — every path uses staticFile()
sourceFile: staticFile('intro-clipped.mp4'),
audioSource: staticFile('intro-clipped.mp4'),

// WRONG — bare path strings cause DEMUXER_ERROR_COULD_NOT_OPEN during render
sourceFile: '/intro-clipped.mp4',
audioSource: '/intro-clipped.mp4',
```

This applies to EVERY path in SEGMENTS[].sourceFile and PROJECT.audioSource. Never use bare string paths.

### 7. Write theme.ts

Write the complete `theme.ts` file to `{project_path}/src/theme.ts`.

### 8. Auto-Proceed

"**Theme Generated**

- Source video: {width}x{height} @ {fps}fps (probed from source)
- Segments defined: {count}
- Total duration: {frames} frames ({seconds}s at {fps}fps)
- Audio source: {path}

Proceeding to segment generation..."

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Source video probed with ffprobe — resolution and FPS extracted
- PROJECT.width, PROJECT.height, and PROJECT.fps match the source video exactly
- Every master timeline segment has a corresponding SEGMENTS entry
- All timing in frames, not seconds
- Audio source path specified
- All sourceFile and audioSource values use `staticFile()` (no bare path strings)
- theme.ts written to project src/

### FAILURE:

- Hardcoding resolution (1920x1080) or FPS (30) without probing the source video
- PROJECT dimensions not matching the source video
- Missing segments from the master timeline
- Timing in seconds instead of frames
- Not specifying audio source
