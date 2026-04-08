# Caption Style Specification — Canonical PowerCaption

This file defines the one and only caption style used across all Remotion video projects.
**Do not deviate from this spec.** The Caption.tsx sidecar template implements it exactly.

---

## Visual Design

| Property | Value |
|----------|-------|
| Font | `'Arial Black', 'Arial Bold', Arial, sans-serif` |
| Weight | `900` |
| Case | ALL CAPS (`.toUpperCase()` in code) |
| Color — body words | White `#FFFFFF` |
| Color — highlight word | Orange `#FF6B35` |
| Text shadow | `0 4px 24px rgba(0,0,0,0.95), 0 2px 8px rgba(0,0,0,0.85)` |
| Letter spacing | `2px` (scaled) |
| Line height | `1` |
| Background | **None** — no box, no pill, no semi-transparent bg |
| Position | `bottom: 10%`, `left: 50%`, centered |

## Animation

| Property | Value |
|----------|-------|
| Entry | Per-word reveal: each word snaps in at its staggered frame |
| Scale in | `0.82 → 1.0` over 8 frames, `Easing.out(Easing.cubic)` |
| Opacity in | `0 → 1` over 8 frames per word |
| Exit | Burst-level fade: `1 → 0` over last 6 frames |
| Word stagger | `Math.floor(durationInFrames / wordCount)` frames per word |

## Resolution Scaling

All pixel values use `useVideoConfig()` to scale relative to 1080p baseline:
```typescript
const { height } = useVideoConfig();
const scale = height / 1080;
const s = (n: number) => Math.round(n * scale);
// At 1080p: scale = 1 (original)
// At 4K:   scale = 2 (all sizes double)
```

## Font Size Conventions

Defined in `OVERLAYS.captions` in `theme.ts`:
```typescript
captions: {
  defaultFontSize: Math.round(36 * height / 1080),  // secondary captions
  kineticFontSize: Math.round(48 * height / 1080),  // primary PowerCaption bursts
}
```

Pass `fontSize={OVERLAYS.captions.kineticFontSize}` for PowerCaption bursts.

## Theme Integration

The `SEGMENTS` array in `theme.ts` must include per-segment caption fields:
```typescript
captionText: 'JUST OVER AN HOUR',    // 2–4 word ALL CAPS burst
captionHighlight: 'HOUR',            // the orange accent word
captionFrame: 1757,                  // absolute frame when key word is spoken
captionPosition: 'bottom-center',
```

The `captionHighlight` value is passed as the `highlight` prop to Caption:
```tsx
<Caption
  text={seg.captionText!}
  highlight={seg.captionHighlight}   // → renders 'HOUR' in orange #FF6B35
  startFrame={captionOffset}
  durationInFrames={captionDuration}
  position={seg.captionPosition}
  fontSize={OVERLAYS.captions.kineticFontSize}
/>
```

## Rules

1. **Speaker segments** (`visualType: 'speaker'`) — MAY have a Caption if a key word is worth emphasising
2. **B-roll segments** (`visualType: 'video-extract'`) — MAY have a Caption overlaid on the VHS footage
3. **Motion-graphic segments** (`visualType: 'motion-graphic'`) — **MUST NOT** have a Caption. Motion graphics have their own visual language. Adding a caption clutters the frame.
4. **Branded-template segments** (`visualType: 'branded-template'`) — MAY have a Caption for social proof stats

## Accent Color

Orange `#FF6B35` is the canonical accent. It must be consistent across all projects.
Do not use gold (`#FFD700`), yellow, or any other colour.
The accent color matches the `COLORS.accent` constant in `theme.ts`.

---

## Long-Form Caption Mode

Long-form tutorials use a distinct caption style optimised for instructional pacing — phrase-level reveals instead of per-word kinetic bursts.

### Visual Design (Long-Form)

| Property | Value | Difference from Short-Form |
|----------|-------|---------------------------|
| Font | `'Inter', 'Roboto', 'Arial', sans-serif` | Not Arial Black 900 |
| Weight | `700` (Bold) | Not 900 |
| Case | Sentence case | Not ALL CAPS |
| Color — body words | White `#FFFFFF` | Same |
| Color — highlight word | Orange `#FF6B35` | Same accent, but applied less frequently (1 per phrase max) |
| Text shadow | `0px 4px 8px rgba(0,0,0,0.8)` | Slightly lighter shadow |
| Position | `bottom: 8%`, `left: 50%`, centered | Slightly higher |
| Width constraint | `maxWidth: 60%` | Narrower to avoid PiP overlap |
| PiP-aware offset | Left-offset when PiP present in bottom-right | New for long-form |

### Animation (Long-Form)

| Property | Value |
|----------|-------|
| Reveal style | Phrase-level: 2–4 words appear together |
| Entry | Opacity 0→1 over 6 frames for the whole phrase |
| Exit | Opacity 1→0 over 6 frames |
| No per-word stagger | Words in a phrase appear simultaneously |

### Theme Integration (Long-Form)

Add `captionMode` field to theme.ts to select between styles:

```typescript
captionMode: 'long-form' | 'short-form',
// 'short-form' = existing PowerCaption (per-word kinetic bursts, ALL CAPS, Arial Black 900)
// 'long-form'  = phrase-level reveals (sentence case, Inter Bold 700, wider phrases)
```

### Caption Source

- **Source:** DeepGram Nova-3 word timestamps → VAD refinement (existing two-pass process — no changes needed)
- **Timing methodology:** NO CHANGES — the existing two-pass calibration (transcript lookup → VAD refinement) is correct and well-documented
- **Gap we fill:** All 5 inspiration videos lack burned-in captions — this is a retention gap we address in Remotion

### Long-Form Body Caption Frequency

**CRITICAL:** Long-form body captions appear ONLY at "power moments" — not on every speaker segment. Inspiration videos show keyword captions at roughly 1 burst per 10–15 seconds of body speaker footage.

**Caption selection criteria (in priority order):**
1. **Numbers/metrics** — statistics, revenue figures, quantities, percentages
2. **Tool names on first mention** — when a new tool/platform is introduced in the body
3. **Key takeaway phrases** — the "headline" of a section or argument
4. **Emotional hooks** — surprising statements, counterintuitive claims, calls to action

**Storyboard rule:** Most body speaker segments should have `captionText: null`. Reserve captions for high-impact moments that benefit from visual reinforcement. A body section with 60s of speaker footage should have roughly 4–6 caption bursts total, NOT a caption on every segment.

**Anti-pattern:** Captioning every speaker segment in the body creates visual noise and dilutes the impact of captions at truly important moments. If the viewer always sees captions, none of them feel special.

### When to Use Long-Form Mode

- Any video longer than 3 minutes
- Any tutorial or instructional content
- Any content with PiP speaker overlays (needs PiP-aware positioning)

---

## Caption Timing Methodology

`captionFrame` MUST be derived from a two-pass calibration using both the transcript and audio analysis. Never approximate from script alone.

### Two-Pass Process

**Pass 1 — Transcript lookup (rough window):**
1. Find the caption phrase in the word-level transcript JSON
2. Record the `start` timestamp of the first word and the `end` timestamp of the last word
3. This gives a rough window: `[phrase_start - 0.5s, phrase_end + 0.5s]`

**Pass 2 — Audio analysis VAD refinement (precise boundary):**
1. Load the `classified_regions` array from the audio analysis JSON
2. Within the rough window from Pass 1, find the `SPEECH` region that contains the key word
3. Use the VAD region's `start` as the precise speech onset
4. `captionFrame = round((vad_onset - clip_offset) × fps)`
5. Segment end frame = `round((vad_offset - clip_offset) × fps) + 3` (3-frame tail after last word)

**When both sources disagree by >3 frames:** Always defer to the audio analysis VAD. Transcript timestamps reflect decoding confidence; VAD timestamps reflect actual acoustic energy onset.

### captionFrame in theme.ts

The `captionFrame` field is the absolute frame in the **clipped video's** timeline (clip_offset already subtracted) at which the highlight word is spoken. It drives `startFrame` inside the Caption component.

```typescript
// CORRECT — VAD-calibrated
captionFrame: 1757,   // frame when VAD onset detected "WORKFORCE" in audio analysis

// WRONG — transcript-only approximation
captionFrame: 1770,   // transcript timestamp without VAD refinement
```

### Tolerance

| Source available | Max acceptable error |
|-----------------|---------------------|
| Audio analysis VAD + transcript | ±3 frames (0.1s) |
| Transcript only (no audio analysis) | ±15 frames (0.5s) — flag as low-confidence |

Caption segments where audio analysis was unavailable MUST be marked with `notes: 'timing: transcript-only, VAD not applied'` in the storyboard and theme.ts so they can be re-calibrated later.
