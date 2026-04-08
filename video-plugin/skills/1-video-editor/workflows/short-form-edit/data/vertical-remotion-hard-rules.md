# Vertical Remotion Hard Rules — 6 Additional Rules for 9:16

These rules supplement the 19 base rules in `remotion-edit/data/remotion-hard-rules.md`. All 19 base rules still apply. These 6 additional rules are specific to vertical (1080×1920 / 2160×3840) short-form compositions.

---

## Rule V1: Vertical Composition Dimensions

**Composition MUST be 9:16 vertical aspect ratio, with dimensions probed from the raw source video via ffprobe.** Common resolutions: 1080×1920, 2160×3840 (4K). Never hardcode — always probe.

```tsx
// theme.ts — CORRECT (probed from source)
export const PROJECT = {
  width: 2160,   // probed via ffprobe
  height: 3840,  // probed via ffprobe
  fps: 30,       // probed via ffprobe
  // ...
};

// ALSO CORRECT (1080p source)
export const PROJECT = {
  width: 1080,
  height: 1920,
  fps: 30,
  // ...
};

// WRONG — landscape dimensions
export const PROJECT = {
  width: 1920,
  height: 1080,
  // ...
};

// WRONG — hardcoded without probing
export const PROJECT = {
  width: 1080,   // ← guessed, not probed
  height: 1920,  // ← guessed, not probed
  // ...
};
```

The composition ID should include "vertical" or "sf" to distinguish from landscape compositions.

**QA check:** Verify `PROJECT.width < PROJECT.height` (portrait orientation) AND `PROJECT.width / PROJECT.height` is approximately 9/16 (0.5625 ± 0.01).

Why: All target platforms (Instagram Reels, TikTok, YouTube Shorts) require 9:16 aspect ratio. Resolution must match source to preserve native quality (Rule 11).

---

## Rule V2: Text Safe Zone

**All text and captions must be within the center 80% of the screen (10% margin top and bottom).**

```tsx
// CORRECT — center-positioned with margins
style={{
  top: '10%',
  bottom: '10%',
  // text positioned within this safe zone
}}

// WRONG — text at the very top or bottom
style={{
  top: '2%',    // overlaps platform status bar
  bottom: '2%', // overlaps platform UI (comments, share, like)
}}
```

Why: Instagram, TikTok, and YouTube Shorts overlay UI elements (like/comment/share buttons, profile info, caption text) in the top and bottom ~10% of the screen. Text placed there is obscured.

---

## Rule V3: Max Segment Duration

**No segment may be longer than 4 seconds without a visual change.** Calculate the frame limit from the probed fps: `maxFrames = 4 * PROJECT.fps` (e.g., 120 frames at 30fps, 240 frames at 60fps).

```
// CORRECT — segments under 4s
Seg01: 60 frames (2s) — hook-text
Seg02: 90 frames (3s) — speaker-zoom
Seg03: 75 frames (2.5s) — broll

// WRONG — segment exceeds 4s
Seg04: 150 frames (5s) — speaker
```

If a speaker segment naturally exceeds 4s, split it by inserting an MG cut. The audio continues uninterrupted under the visual change.

Why: Short-form viewers scroll away within 3 seconds if the visual doesn't change. The 4-second limit provides a 1-second buffer above the critical 3-second threshold.

---

## Rule V4: Minimum Non-Speaker Coverage

**At least 65–70% of total frames must be non-speaker visual types (motion graphic, split-screen, or hook-text).** Punchy/Standard videos: 65% minimum. Deep videos (50–60s): 70% minimum. **Note:** Top performers hit 80–84%; 65% is the minimum floor, not the goal.

```
// For a 35s Standard video at 30fps = 1050 total frames
// Minimum non-speaker frames: 1050 × 0.65 = 683 frames

// CORRECT
Speaker frames: 315 (30%)
Non-speaker frames: 735 (70%) ✅

// WRONG
Speaker frames: 600 (57%)
Non-speaker frames: 450 (43%) ❌  ← too much talking head

// ALSO WRONG
Speaker frames: 800 (76%)
Non-speaker frames: 250 (24%) ❌
```

Non-speaker visual types: V4 (motion-graphic), V4b (motion-graphic-cutaway), V5 (split-screen with MG overlay), V6 (hook-text).
Speaker visual types: V1 (speaker), V2 (speaker-zoom), V7 (cta).

**Design principle:** The speaker's audio plays continuously under all visual types — motion graphics don't interrupt the script, they replace the visual. Think "MG with occasional speaker moments." Research shows viewers scroll within 3 seconds if visuals don't change; near-constant visual variety is the #1 retention driver.

---

## Rule V5: Speaker Cropping — Landscape 4K Source

**Speaker source video IS landscape 4K (3840×2160). This is the standard source format. `objectPosition` on speaker `<OffthreadVideo>` is ALLOWED for face framing. `objectFit: 'cover'` remains MANDATORY.**

```tsx
// CORRECT — landscape source, objectPosition for face framing
<OffthreadVideo
  src={seg.sourceFile}
  muted
  pauseWhenBuffering
  style={{
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    objectPosition: 'center 25%',  // ← frames face in upper portion
  }}
/>

// CORRECT — vertical source, no cropping needed
<OffthreadVideo
  src={seg.sourceFile}
  muted
  pauseWhenBuffering
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>

// WRONG — missing objectFit: 'cover'
<OffthreadVideo
  src={seg.sourceFile}
  muted
  pauseWhenBuffering
  style={{ width: '100%', height: '100%' }}
/>
```

**MANDATORY:** Source video is 4K landscape (3840×2160). This matches what top creators (@nateherkai, @nick_saraev) do:
- Split-screen overlay zone gets the full widescreen content (no black bars)
- Speaker-only segments: centre-crop 16:9 → 9:16 via `objectFit: 'cover'`, 4K gives 1080p+ after crop
- Use `objectPosition: 'center 25%'` to frame the speaker's face in the upper portion of the vertical frame

**Framing behaviour (automatic via objectFit: 'cover'):**
- **Full-frame speaker (V1/V2)**: Tight centre-crop — ~32% of landscape width visible. Shows face close-up. Use `objectPosition: 'center 25%'` for face framing.
- **Split-screen speaker (V5 bottom 35%)**: Wide framing — ~90% of landscape width visible. Shows head, shoulders, upper body. Use `objectPosition: 'center 25%'` to keep face in upper portion of zone.
- Both levels of framing come from the same source — no pre-cropping needed.

**Filming guidance:** Frame a medium shot (head to waist) so that:
- Full-frame centre-crop shows face + shoulders clearly
- Split-screen wide view shows full upper body with room to breathe

Why: 4K landscape source provides maximum flexibility — full-width content for split-screen overlays and high-resolution centre-crop for speaker-only segments.

---

---

## Rule V6: Asset Resolution Must Match Composition

**All source video assets (b-roll, motion graphics) in `public/` MUST match the composition resolution (`PROJECT.width × PROJECT.height`).** Verify with ffprobe before rendering. If mismatched, upscale with FFmpeg before copying to `public/`.

```bash
# Verify every asset in public/ matches the composition
TARGET="${PROJECT_WIDTH},${PROJECT_HEIGHT}"
for f in public/motion-graphics/*.mp4; do
  res=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f")
  [ "$res" != "$TARGET" ] && echo "FAIL: $f is $res, expected $TARGET"
done

# Fix mismatched assets — software encoding for intermediate quality (CRF 15 = near-lossless)
ffmpeg -y -i "mismatched.mp4" \
  -vf "scale=${PROJECT_WIDTH}:${PROJECT_HEIGHT}:flags=lanczos" \
  -c:v libx264 -crf 15 -preset medium \
  "fixed.mp4"
```

Why: Remotion's renderer produces horizontal line artifacts (banding) when source assets have different resolutions than the composition canvas. All assets must be pre-scaled to the exact composition dimensions before rendering.

---

## Rule V7: No Fade-In on First Segment

**The first segment (Seg01) MUST NOT fade in from black.** Pass `skipFadeIn` to the template component so the first frame renders at full opacity. Subsequent segments keep their default fade-in transition.

```tsx
// CORRECT — Seg01 skips fade-in
<VerticalSplitScreen
  speakerSrc={seg.sourceFile}
  overlaySrc={seg.overlayFile!}
  startFrame={0}
  durationInFrames={seg.durationInFrames}
  videoStartFrom={seg.startFrame}
  variant="split"
  dividerColor="transparent"
  speakerPosition="bottom"
  skipFadeIn
/>

// CORRECT — MotionGraphic as Seg01 skips fade-in
<MotionGraphic src={seg.sourceFile} startFrame={0} durationInFrames={seg.durationInFrames} skipFadeIn />

// WRONG — Seg01 without skipFadeIn (first frame = black)
<VerticalSplitScreen ... />
```

Why: The parent `<div>` has `backgroundColor: '#000'`. Templates fade in over 8 frames (opacity 0→1), so frame 0 is fully black. This creates a poor thumbnail and first impression on all platforms.

---

## QA Execution Summary (Vertical Rules)

| # | Rule | Check Method |
|---|------|-------------|
| V1 | 9:16 vertical (probed) | Parse theme.ts → verify `PROJECT.width < PROJECT.height` AND ratio ≈ 0.5625; ffprobe raw source → verify PROJECT matches |
| V2 | Text safe zone | Verify VerticalCaption uses 10% top/bottom margins |
| V3 | Max 4s segments | Parse theme.ts SEGMENTS → verify all `durationInFrames ≤ 4 * PROJECT.fps` |
| V4 | 65–70% non-speaker (top performers: 80–84%) | Sum non-speaker segment frames → verify ≥ 65% (Punchy/Standard) or ≥ 70% (Deep); check VerticalSplitScreen default is 50/50 |
| V5 | objectPosition only with objectFit:cover | Grep speaker Seg*.tsx — if `objectPosition` present, verify `objectFit: 'cover'` also present |
| V6 | Asset resolution match | ffprobe every file in `public/motion-graphics/` → must equal `PROJECT.width,PROJECT.height` |
| V7 | No fade-in on Seg01 | Verify Seg01.tsx passes `skipFadeIn` to its template component |
