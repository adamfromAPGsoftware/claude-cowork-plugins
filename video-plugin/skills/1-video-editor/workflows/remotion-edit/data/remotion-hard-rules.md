# Remotion Hard Rules — 19 Non-Negotiable Rules

These rules are enforced during QA (step 06). Every single rule must PASS for the project to proceed to render.

---

## Rendering Environment

> **Target Machine:** Mac Studio 2025 — Apple M4 Max, 64GB RAM
> **Remotion Version:** ≥4.0.432
>
> All render commands in this workflow are optimised for this hardware:
> - `--gl=angle` — GPU-accelerated frame rendering (CSS effects, canvas, WebGL)
> - `--hardware-acceleration if-possible` — Apple VideoToolbox H.264 encoding (3-5x faster than software libx264)
> - `--concurrency=8` — tuned for M4 Max CPU cores. Adjust with `npx remotion benchmark` if running on different hardware.
> - Standalone FFmpeg commands use `h264_videotoolbox -q:v 80` for hardware encoding (scale 0-100, higher = better; never use < 65 for intermediate files).
>
> **If running on non-Mac hardware:** Replace `--hardware-acceleration if-possible` with `--hardware-acceleration disabled`, and FFmpeg `h264_videotoolbox` with `libx264 -preset medium -crf 18`.

---

## Rule 1: OffthreadVideo muted

**ALL `<OffthreadVideo>` components MUST have the `muted` prop.**

```tsx
// CORRECT
<OffthreadVideo src={videoPath} muted />

// WRONG — missing muted
<OffthreadVideo src={videoPath} />
```

Why: B-roll clips should never play their own audio. The single Audio element in Root.tsx handles all audio.

---

## Rule 2: OffthreadVideo style

**ALL `<OffthreadVideo>` components MUST have `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`.**

```tsx
// CORRECT
<OffthreadVideo
  src={videoPath}
  muted
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>

// WRONG — missing style or partial style
<OffthreadVideo src={videoPath} muted />
<OffthreadVideo src={videoPath} muted style={{ width: '100%' }} />
```

Why: Ensures all video fills the frame without letterboxing or stretching.

---

## Rule 3: pauseWhenBuffering

**ALL `<OffthreadVideo>` AND `<Audio>` components MUST have `pauseWhenBuffering` prop.**

```tsx
// CORRECT
<OffthreadVideo src={videoPath} muted pauseWhenBuffering style={...} />
<Audio src={audioPath} pauseWhenBuffering />

// WRONG — missing pauseWhenBuffering
<OffthreadVideo src={videoPath} muted style={...} />
<Audio src={audioPath} />
```

Why: Prevents audio/video desync when media files are loading.

---

## Rule 4: Single Audio Element

**There must be exactly ONE `<Audio>` element in the ENTIRE project. It lives in Root.tsx only.**

No segment file (Seg{NN}.tsx) may contain an `<Audio>` element.

**Multi-clip compositions:** When the composition includes both intro segments and a body video clip, concatenate all audio sources into a single file (e.g., `full-audio.m4a`) BEFORE building the composition. Use FFmpeg concat filter: `[intro:a][silence:a][body:a]concat=n=3:v=0:a=1`. The single Audio element plays this concatenated file.

**Short-form exception:** Short-form compositions (9:16 vertical) may have a SECOND `<Audio>` element for background music (or a pre-mixed file containing background music + transition SFX). Whether the file is a raw music track or a pre-mixed music+SFX file, it counts as one element. This second Audio must use a volume callback for ducking and include `pauseWhenBuffering`. Both Audio elements must be in Root.tsx only — no Audio in segment files (Rule 9 still applies).

**Long-form exception:** Long-form compositions (16:9 landscape) MAY have a SECOND `<Audio>` element for background music when the storyboard's Background Music section specifies a track. This second Audio must:
- Use a volume callback that keeps music at ≤10% volume (≤ -20dB relative to voiceover)
- Include `pauseWhenBuffering`
- Fade out over 3-5 seconds at the intro-to-body transition (unless storyboard specifies music continues into body)
- Live in Root.tsx only (Rule 9 still applies)

Why: Multiple audio sources cause overlap and desync. A single Audio element ensures consistent audio playback. Background music is the one exception because it is ducked (low volume) and does not conflict with the voiceover.

---

## Rule 5: No Img Tags for B-Roll

**No `<Img>` or `<img>` tags for B-roll content. All visual overlay segments (video-extract and motion-graphic) MUST use `<OffthreadVideo>`.**

```tsx
// WRONG — never do this for B-roll
<Img src="/screenshot.png" />
<img src="/broll-image.png" />

// CORRECT — use OffthreadVideo for all B-roll media
<OffthreadVideo src="/broll-clip.mp4" muted pauseWhenBuffering style={...} />
```

**ONE EXCEPTION:** Branded template components (UpworkProfile, AgencyBrand) may use `<Img>` internally for static brand assets (profile photos, logos). These are NOT B-roll — they are fixed brand images. The QA check for this rule should only flag `<Img>` in Seg{NN}.tsx files, not in branded template source files.

Why: B-roll content must always be video for consistency. Brand images in branded templates are a distinct category.

---

## Rule 6: Zero Frame Gaps

**There must be ZERO frame gaps between segments in the composition.**

For adjacent sequences:
- `Sequence[N].from + Sequence[N].durationInFrames === Sequence[N+1].from`

The total of all sequence durations must equal `PROJECT.totalDurationInFrames`.

**Multi-clip compositions:** The transition and body segments must also chain with zero gaps. Example: 4699 (intro segments) + 30 (transition) + 42125 (body) = 46854 totalDurationInFrames. The `BODY.startFrame` must equal `TRANSITION.startFrame + TRANSITION.durationInFrames`.

Why: Frame gaps cause black flashes in the rendered video.

---

## Rule 7: Sequence premountFor

**ALL `<Sequence>` elements MUST have `premountFor={30}`.**

```tsx
// CORRECT
<Sequence from={0} durationInFrames={75} premountFor={30} name="Hook">

// WRONG — missing premountFor
<Sequence from={0} durationInFrames={75} name="Hook">
```

Why: Premounting ensures video files start buffering 30 frames before they're visible, preventing loading delays.

---

## Rule 8: Sequence Name Prop

**ALL `<Sequence>` elements MUST have a descriptive `name` prop.**

```tsx
// CORRECT
<Sequence from={0} durationInFrames={75} premountFor={30} name="Hook - Speaker SubtleZoom">

// WRONG — missing name or generic name
<Sequence from={0} durationInFrames={75} premountFor={30}>
<Sequence from={0} durationInFrames={75} premountFor={30} name="Segment 1">
```

Good names include the section + visual type: "Hook - Speaker SubtleZoom", "Body Ch1 - Screen Rec VS Code", "CTA - Social Proof Stack".

Why: Names appear in Remotion Studio's timeline, making debugging and preview navigation much easier.

---

## Rule 9: No Audio in Segments

**Segment files (Seg{NN}.tsx) must NOT contain any `<Audio>` elements.**

Audio is exclusively managed in Root.tsx.

---

## Rule 10: All Imports Valid

**Every `import` statement must reference a file that exists.**

Check: imported file path → file exists on disk.

---

## Rule 11: Theme Completeness + Source Video Match

**The SEGMENTS array in theme.ts must have exactly one entry per Seg{NN}.tsx file.**

Required PROJECT constants:
- `fps` (number — **must match source video frame rate**, probed via ffprobe)
- `width` (number — **must match source video width**, probed via ffprobe)
- `height` (number — **must match source video height**, probed via ffprobe)
- `totalDurationInFrames` (number)
- `compositionId` (string)
- `audioSource` (string — path to audio file)

**Resolution and FPS are NEVER hardcoded.** They are always probed from the main source video using ffprobe during theme generation. If the source is 4K 60fps, the composition is 4K 60fps. If it's 1080p 30fps, the composition is 1080p 30fps. The output always matches the input.

Why: Hardcoding resolution causes either upscaling artifacts (rendering 1080p from 4K source) or wasted quality (rendering 4K from 1080p source). The composition must match the source to preserve native quality.

---

## Rule 12: B-Roll Video Only + Template Assignment

**All visual overlay segments (video-extract and motion-graphic) are video. No static images, no KenBurns effects on images, no screenshots as images.**

**Critical template distinction:**
- `video-extract` segments → **BRollOverlay** (VHS desaturation + retro overlay — signals "this is pulled from later in the video")
- `motion-graphic` segments → **MotionGraphic** (clean, full-color playback — AI-generated content should look polished, not retro)

Motion graphics must NEVER use BRollOverlay. The VHS effect is exclusively for video-extracts (real b-roll pulled from the main recording).

If a storyboard segment references a static screenshot as B-roll, it must be:
1. Converted to a short video (e.g., via FFmpeg with `-loop 1 -t 3`)
2. Or replaced with a screen recording clip
3. Or replaced with a motion graphic

**Exception:** Branded template segments (UpworkProfile, AgencyBrand) may use static images for brand assets internally. This is by design — they are not B-roll.

---

## Rule 13: staticFile() for All Public Asset Paths

**All public asset paths in theme.ts MUST use `staticFile()` from remotion. Never use bare path strings like `'/file.mp4'`.**

```tsx
import { staticFile } from 'remotion';

// CORRECT
sourceFile: staticFile('intro-clipped.mp4'),
audioSource: staticFile('intro-clipped.mp4'),

// WRONG — bare path strings cause DEMUXER_ERROR_COULD_NOT_OPEN
sourceFile: '/intro-clipped.mp4',
audioSource: '/intro-clipped.mp4',
```

Why: Bare path strings like `'/intro-clipped.mp4'` cause `DEMUXER_ERROR_COULD_NOT_OPEN` errors during render. `staticFile()` resolves the path correctly relative to the `public/` directory.

**This also applies to `imageSrc` on branded-template segments.** The `imageSrc` prop must be an actual `staticFile()` function call, NOT a string containing the text "staticFile(...)":

```tsx
// CORRECT — actual function call
imageSrc: staticFile('branded-assets/agency-homepage.png'),

// WRONG — string representation, image will not load (renders as empty/broken)
imageSrc: "staticFile('branded-assets/agency-homepage.png')",
```

---

## Rule 14: startFrom on Speaker OffthreadVideo

**Speaker segments using the main video source MUST include `startFrom={seg.startFrame}` on `<OffthreadVideo>` to maintain audio sync.**

```tsx
// CORRECT — video seeks to the correct frame matching the audio
<OffthreadVideo
  src={seg.sourceFile}
  startFrom={seg.startFrame}
  muted
  pauseWhenBuffering
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>

// WRONG — video replays from 0:00 for every segment, out of sync with audio
<OffthreadVideo
  src={seg.sourceFile}
  muted
  pauseWhenBuffering
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>
```

Why: The single `<Audio>` element in Root.tsx plays continuously. Each speaker segment's `<OffthreadVideo>` must seek to the matching frame position using `startFrom` so the speaker's mouth movements match the audio. Without this, every speaker segment shows the video starting from frame 0.

**Note:** B-roll and motion-graphic segments do NOT need `startFrom` — they play their own clip from the beginning. Only speaker/CTA segments that reference the main recorded video need this.

---

## Rule 15: OffthreadVideo Import Source

**`OffthreadVideo` MUST be imported from `'remotion'`, NOT from `'@remotion/media-utils'`.**

```tsx
// CORRECT
import { OffthreadVideo } from 'remotion';

// WRONG — OffthreadVideo is not exported from @remotion/media-utils
import { OffthreadVideo } from '@remotion/media-utils';
```

Why: `OffthreadVideo` is exported from the core `remotion` package. Importing from `@remotion/media-utils` causes build errors or undefined component errors.

---

## Rule 16: Branded Templates Use staticFile(), Not require()

**Branded template components (AgencyBrand, UpworkProfile) MUST use `staticFile()` + `<Img>` for brand asset images. Never use `require()`.**

```tsx
import { Img, staticFile } from 'remotion';

// CORRECT
<Img src={staticFile('branded-assets/apg-logo.png')} style={{ ... }} />

// WRONG — require() does not work in Remotion's rendering pipeline
<Img src={require('../public/branded-assets/apg-logo.png')} style={{ ... }} />
```

Why: `require()` is a Node.js/Webpack pattern that does not resolve correctly during Remotion's rendering. `staticFile()` is Remotion's official method for referencing files in the `public/` directory.

---

## Rule 17: Caption Timing Matches Transcript Word Timestamps

**Every caption segment's frame boundaries MUST be verified against the transcript's word-level timestamps (from audio analysis).**

For each segment with `captionText`:
1. Look up the first word of `captionText` in the transcript word-level data
2. Convert the transcript word start time to a frame number: `frame = Math.round(time_seconds * fps)`
3. Apply the clipping offset if the source video was trimmed: `frame = Math.round((time_seconds - clip_offset) * fps)`
4. The segment's `startFrame` must be **≤** the first word's frame (the caption must be on screen when the word is spoken)
5. The segment's `startFrame + durationInFrames` must be **≥** the last word's frame (the caption must still be on screen when the last word is spoken)

```
// Example: transcript says "That's" at 9.76s, "workforce" at 10.48s
// Clipping offset: 0.484s
// First word frame: Math.round((9.76 - 0.484) * 30) = 278
// Last word frame: Math.round((10.48 - 0.484) * 30) = 300
// Segment: startFrame=288, durationInFrames=43, endFrame=331
// Check: 288 ≤ 278? NO → shift startFrame earlier or accept 10-frame tolerance
// In practice: allow ±15 frame tolerance for natural pacing
```

**Tolerance:** A ±15 frame (0.5s) tolerance is allowed for creative pacing. Beyond that, the segment boundaries MUST be adjusted.

Why: Caption text that appears before or after the speaker says those words breaks the viewing experience. The transcript's word-level timestamps are the single source of truth for when words are spoken.

---

## Rule 18: Transitions Only Between Visual Type Changes

**Fade/flash transitions MUST only occur when the visual type changes between segments. Consecutive speaker segments MUST be seamless hard cuts with NO transition effect.**

Transitions are built into the overlay/branded components (BRollOverlay fade in/out, AgencyBrand/UpworkProfile fade in/out). These are correct — they create a natural transition when cutting from speaker to b-roll and back.

**What must NOT happen:** Any fade, flash, or opacity transition between two consecutive speaker segments (whether using SubtleZoom, KineticCaption, or bare OffthreadVideo). Since both segments show the same source video at sequential `startFrom` positions, the viewer should see a seamless continuous shot.

| From → To | Expected Transition |
|-----------|-------------------|
| speaker → speaker | Hard cut (seamless) |
| speaker → b-roll/MG | B-roll fades in over speaker |
| b-roll/MG → speaker | B-roll fades out, revealing speaker |
| speaker → branded-template | Branded template fades in |
| branded-template → speaker | Branded template fades out |

Why: Flash transitions between two consecutive speaker shots create a jarring "camera flash" effect that breaks immersion. The speaker footage is continuous — viewers should not perceive segment boundaries between speaker shots.

---

## Rule 20: Resolution-Proportional UI Sizing

**All hardcoded pixel values in overlay UI components (BRollOverlay, branded templates) MUST scale proportionally with the composition resolution.**

Use `useVideoConfig()` from `'remotion'` to get the runtime `height`, then compute a `scale` factor against a 720p design baseline:

```tsx
import { useVideoConfig } from 'remotion';

// Inside the component:
const { height } = useVideoConfig();
const scale = height / 720; // baseline: 720p
// At 720p  → scale = 1   (original sizes)
// At 1080p → scale = 1.5
// At 4K    → scale = 3

const s = (n: number) => Math.round(n * scale);
// Then use s(38) instead of 38, s(16) instead of 16, etc.
```

**This applies to ALL pixel values within overlay UI elements:**
- Font sizes
- Border widths (triangles, outlines)
- Gap / padding / margin
- Icon / dot sizes
- Border radius
- Box shadow blur radius

**Percentage-based values (top: '4%', left: '3.5%', width: '100%') do NOT need scaling** — they are already relative to the composition dimensions.

This rule ensures the "LATER IN VIDEO", "REC", timecode, and any other overlay text remain visible and correctly proportioned at any output resolution (720p, 1080p, 4K).

---

## Rule 19: Audio Offset Input Prop

**The `audioOffsetMs` input prop MUST be passed through to the `<Audio>` wrapper `<Sequence>` for lip sync correction.**

When `audioOffsetMs > 0`, the single `<Audio>` element must be wrapped in a `<Sequence>`:

```tsx
const audioOffsetFrames = Math.round((audioOffsetMs / 1000) * PROJECT.fps);

// When offset is active
<Sequence from={audioOffsetFrames} name="Audio Offset">
  <Audio src={PROJECT.audioSource} pauseWhenBuffering />
</Sequence>

// When offset is 0 (default)
<Audio src={PROJECT.audioSource} pauseWhenBuffering />
```

- `audioOffsetMs` is exposed as a Remotion Studio sidebar input prop via `defaultProps` on the Composition
- User adjusts live in preview until lip sync matches, then renders with that value
- Positive value = delay audio (audio plays too early)
- Conversion: `offsetFrames = Math.round((audioOffsetMs / 1000) * fps)`
- The render command must include `--props='{"audioOffsetMs": {value}}'`

Why: Remotion's browser playback vs frame extraction can introduce a few ms of audio drift. This gives a single knob to correct it without touching composition logic.

---

## Rule 21: Jump-Cut Zoom Alternation (Long-Form)

**Consecutive speaker segments in long-form intros SHOULD alternate scale between 1.0x and 1.05–1.15x to create a jump-cut zoom effect.**

```tsx
// Even-indexed speaker segment (base scale)
<div style={{ transform: 'scale(1.0)', transformOrigin: 'center center', width: '100%', height: '100%' }}>
  <OffthreadVideo ... />
</div>

// Odd-indexed speaker segment (punched-in scale)
<div style={{ transform: 'scale(1.1)', transformOrigin: 'center center', width: '100%', height: '100%' }}>
  <OffthreadVideo ... />
</div>
```

This is a SHOULD rule (not MUST) — it applies to long-form intro speaker segments. Body speaker segments and short-form content do not require zoom alternation.

**Confirmed pattern:** 4 of 5 inspiration creators use this technique. Zoom factor range: 1.05–1.15x.

---

## Rule 22: Audio Continuity Across Transitions

**Audio MUST be continuous across all visual transitions. The voiceover bridges every visual cut — there are no audio gaps at visual boundaries.**

This is already enforced by Rule 4 (Single Audio Element), but this rule makes the intent explicit: the viewer should never experience an audio gap or glitch when the visual type changes. The single Audio element in Root.tsx plays continuously while visual segments change underneath it.

**Confirmed pattern:** Universal across all 5 inspiration creators — audio is 100% continuous.

---

## Rule 23: Maximum Quality Render Output

**The render command MUST produce output that exactly matches the source video resolution and frame rate, at near-lossless quality.**

Required render flags:
- `--codec h264` — universal compatibility
- `--crf 15` — near-lossless quality (never use CRF > 18)
- `--gl=angle` — GPU-accelerated CSS rendering
- `--hardware-acceleration if-possible` — Apple VideoToolbox encoding (macOS)
- `--concurrency=8` — tuned for M4 Max

**Prohibited render flags:**
- `--scale` — NEVER include. Downscales the output resolution.
- `--height` / `--width` — NEVER include. Overrides composition dimensions.
- `--quality` with low values — NEVER reduce below default.

**Post-render verification:** Run `ffprobe` on the output and confirm:
1. Width × Height matches `PROJECT.width` × `PROJECT.height`
2. Frame rate matches `PROJECT.fps`
3. File size is reasonable for the resolution/duration (see step-07-render.md size table)

If any verification fails, the render is invalid and must be re-done.

Why: The entire pipeline preserves source quality — from ffprobe-probed resolution in theme.ts to the final render. Any downscaling or quality reduction at render time wastes all that effort.

---

## QA Execution Summary

| # | Rule | Check Method |
|---|------|-------------|
| 1 | muted prop | Grep `<OffthreadVideo` → verify `muted` present |
| 2 | style prop | Grep `<OffthreadVideo` → verify full style object |
| 3 | pauseWhenBuffering | Grep `<OffthreadVideo` + `<Audio` → verify prop |
| 4 | Single Audio (or 2 for bg music/mix) | Count `<Audio` across all files → must be 1, or 2 if background music is used (short-form: always 2, with pre-mixed music+SFX file; long-form: 2 when storyboard specifies music), both in Root.tsx |
| 5 | No Img | Grep `<Img` + `<img` → must be 0 |
| 6 | Zero gaps | Parse Sequence from/duration → validate chain |
| 7 | premountFor | Grep `<Sequence` → verify `premountFor={30}` |
| 8 | name prop | Grep `<Sequence` → verify `name=` present |
| 9 | No Audio in segs | Grep `<Audio` in Seg*.tsx → must be 0 |
| 10 | Valid imports | Parse imports → verify files exist |
| 11 | Theme complete + source match | Parse theme.ts → verify all fields; ffprobe source video → verify PROJECT.width/height/fps match |
| 12 | Video-only + template assignment | Grep `<Img` → must be 0; verify video-extract uses BRollOverlay, motion-graphic uses MotionGraphic |
| 13 | staticFile() paths | Parse theme.ts → verify all sourceFile/audioSource use `staticFile()` |
| 14 | startFrom on speaker | Grep speaker Seg*.tsx `<OffthreadVideo` → verify `startFrom={seg.startFrame}` |
| 15 | OffthreadVideo import | Grep `from '@remotion/media-utils'` → must be 0 |
| 16 | No require() in branded | Grep `require(` in branded templates → must be 0 |
| 17 | Caption timing vs transcript | Cross-ref captionText segments against transcript word timestamps → within ±15 frame tolerance |
| 18 | Transitions only on type change | Verify no fade/flash between consecutive speaker segments → must be hard cuts |
| 21 | Jump-cut zoom (long-form) | Verify alternating scale on consecutive intro speaker segments |
| 22 | Audio continuity | Verify single Audio element plays continuously (covered by Rule 4 check) |
| 23 | Max quality render | Verify render uses `--crf 15`, no `--scale`/`--height`/`--width`; ffprobe output matches PROJECT dimensions |
