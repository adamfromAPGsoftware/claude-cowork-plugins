# Production Style Guide — Short-Form Vertical (9:16)

Synthesized from frame-level analysis of 5 top-performing Instagram Reels (53K–252K engagement). These are **binding specifications** for storyboard and Remotion steps — not suggestions.

**Source videos:**
- DRXZJeHiAES (@nateherkai, 252K eng, 28s)
- DSdZtG7k80v (@nateherkai, 113K eng, 22s)
- DTXqGz2Evxq (@nateherkai, 70K eng, 31s)
- DSm-QQ_Dxh3 (@nick_saraev, 57K eng, 48s)
- DSu3h2Fj1oM (@nick_saraev, 53K eng, 37s)

Raw analysis data: `./inspiration/{shortCode}-production-analysis.json`

---

## Section 1: Caption Strategy — Platform-Native (No Burned-In Text)

**All captions are delivered via platform-native systems. Zero text overlays are burned into the Remotion render.**

| Platform | Caption Method | Implementation |
|----------|---------------|----------------|
| YouTube | SRT file uploaded via API | Generated from `clipped-refined-transcript.json` after render |
| Instagram Reels | Platform auto-captions | Toggled on per post in the app |
| TikTok | Platform auto-captions | Toggled on per post in the app |

**Why platform-native:**
- Multilingual translation support (platform auto-translate)
- Cleanest visual aesthetic — no burned-in text competing with MGs
- Each platform styles captions to match its current UI conventions
- No VerticalCaptionV2, VerticalCaption, or any caption component in Remotion projects

**What NOT to do:**
- Do NOT add any text overlay components to Remotion segment files
- Do NOT import or use VerticalCaptionV2 or VerticalCaption
- Do NOT generate CAPTION_PAGES in theme.ts
- Do NOT plan caption page timing in storyboards

---

## Section 2: Transition Spec

### Hard Rule: Hard-cuts only

All 5 inspiration videos use **exclusively hard-cuts** (instant scene changes). Zero dissolves, wipes, slides, or any blended transitions were detected across 167 total seconds analysed.

| Boundary | Transition | Implementation |
|----------|-----------|----------------|
| Hook → body | Hard-cut | Adjacent `<Sequence>` blocks, no overlap |
| Body → body | Hard-cut | Adjacent `<Sequence>` blocks |
| Body → CTA | Hard-cut | Adjacent `<Sequence>` blocks |
| All others | Hard-cut | No transition components needed |

**Implication for Remotion:** No transition components required. Segments are simply sequential `<Sequence>` blocks in Root.tsx with no frame overlap. This is already how the current templates work — do NOT add transition effects.

---

## Section 3: Split-Screen Spec

### Layout Distribution (observed averages)

| Layout | % of runtime | When used |
|--------|-------------|-----------|
| Split-screen (50/50) | 35–89% | Opening hook, demo narration, majority of video |
| Full-frame screen (MG) | 30–50% | Solo MG demos replacing static screen recordings |
| Full-frame speaker | 10–20% | CTA/closing, emotional emphasis |
| Graphic-only | 0–5% | Mid-video emphasis text only — NOT for hook opening |

### Split-Screen Configuration

| Property | Value | Remotion Prop |
|----------|-------|---------------|
| Primary ratio | 50% content (top) / 50% speaker (bottom) | `variant: 'split'` |
| Secondary ratio | 65/35 (available but NOT default) | `variant: 'split-65-35'` |
| Speaker position | Bottom (4/5 videos) | `speakerPosition: 'bottom'` |
| Content position | Top (MG overlay — full widescreen content) | `overlayZone: 'top'` |
| Divider | No visible divider (transparent default) | `dividerColor: 'transparent'` |

**Production note:** 0/5 inspiration videos use 65/35; 4/5 use 50/50. The 50/50 split gives the speaker more presence and creates a balanced composition.

### Layout Sequencing Rules

1. **Start with V5 split-screen (50/50)** — Recognizable visual (brand logo, authority figure, complex technical visual) in top half + speaker face in bottom half. Split-screen hooks outperform face-only hooks in 4/5 top performers.
2. **Alternate between split and full-frame** — Never more than 8s in the same layout
3. **End with full-frame speaker** — CTA section uses full-frame speaker (last 3–5s)
4. **No text card openers** — V6 hook text is forbidden as the opening segment. Text cards may be used mid-video for emphasis only.

### Hook Pattern Detail

The opening V5 split-screen should feature:
- **Top half:** **Hero keyword visual** — the video's primary subject visualized. Priority: (1) tool/platform logo fetched via `fetch-logo.ts` waterfall, (2) tool UI or code interface MG, (3) side-by-side comparison logos. **Text-only MGs are FORBIDDEN for the hook visual.**
- **Bottom half:** Speaker face with natural expression (not posed)
- **Duration:** 1-2 seconds before first visual change

**Hero keyword identification:** The hero keyword is identified during storyboard step C2 and its logo (if applicable) is fetched and verified during asset step 5b using `scripts/fetch-logo.ts`.

### PiP Style (rare — only 1 video)

| Property | Value |
|----------|-------|
| Speaker position | Bottom-left |
| Speaker size | ~25% of frame |
| Shape | Circular or rounded-rect |
| Usage | Brief overlay during screen demos (3s max) |

---

## Section 4: Zoom/Motion Spec

### Zoom — MANDATORY on Speaker Returns

| Property | Value | When |
|----------|-------|------|
| Type | `slow-in` only | Speaker full-frame shots only |
| Factor | 1.02–1.05 (2–5% zoom) | Never exceeds 1.05 |
| Speed | Slow (over 2+ seconds) | Gradual, barely perceptible |
| Usage | **MANDATORY on every speaker-return segment (V1/V7)** | Every time visual cuts back to speaker after non-speaker, must use SubtleZoom |

**Updated values:**
- V1 (speaker): `zoomFactor: 1.03` (was 1.08)
- V2 (speaker-zoom/emphasis): `zoomFactor: 1.08` (was 1.25)
- V7 (CTA): `zoomFactor: 1.05` — distinct from V2, subtle emphasis for closing

### MG/B-roll Motion (Ken Burns) — MANDATORY

**All non-speaker visuals (V4, V4b, V5 overlay zone) MUST have Ken Burns zoom/pan. Static MG display is FORBIDDEN.**

All 5 inspiration videos apply Ken Burns zoom+pan on every screen-content and MG segment. Static display looks flat and amateur.

| Motion Type | Zoom Range | When |
|------------|-----------|------|
| Default zoom | `1.0 → 1.15` over segment duration | All MG/screen content |
| Aggressive zoom (UI highlight) | `1.0 → 1.3` over segment duration | Close-up on specific UI element |
| Digital pan | Horizontal/vertical pan | Scrolling through content, navigating UI |

**Remotion implementation:** `MotionGraphic` component accepts `zoomFactor` prop (default: `1.15`). The zoom is applied as a `scale()` transform that interpolates from `1.0` to `zoomFactor` over the segment duration with `overflow: hidden` on the parent container.

### Pan

| Property | Value |
|----------|-------|
| Usage | 1/5 videos only (DSm-QQ_Dxh3) |
| Direction | Down (scrolling through content) |
| Speed | Medium |
| Duration | 3 consecutive seconds |

Pan is acceptable for scrolling/navigating content but not the primary motion style.

### Shake

Zero shake effects detected. **Never add shake.**

---

## Section 5: Cut Rhythm Spec

### Cut Frequency

| Metric | Value | Source |
|--------|-------|--------|
| Avg cuts per 30s | 13–15 | 4/5 videos |
| Avg cut interval | 2.0–2.2 seconds | Consistent across creators |
| Hook section (first 3s) | 1–3 cuts | Fast opener |
| Demo sections | 0.2–0.5 cuts/second | Slower during demos |
| CTA section (last 3s) | 0–1 cuts | Usually single shot |

### Cut Pattern

3/5 videos follow `hook-fast-then-regular`:
- **First 3 seconds:** 2–3 rapid cuts (one per second)
- **Middle 80%:** Regular ~2s intervals
- **Last 3–5 seconds:** Single shot or 1 cut

### Segment Duration Targets

| Segment type | Target duration | Max |
|-------------|----------------|-----|
| Hook text / graphic | 45–60 frames (1.5–2s) | 60 frames |
| Speaker (full-frame) | 60–90 frames (2–3s) | 120 frames |
| Screen recording | 60–120 frames (2–4s) | 120 frames |
| Split-screen | 60–90 frames (2–3s) | 120 frames |
| CTA speaker | 90–120 frames (3–4s) | 120 frames |

### Visual Change Frequency

| Metric | Target |
|--------|--------|
| Minimum changes per 30s | 13 |
| Maximum same-shot duration | 4 seconds (120 frames) |
| Typical same-shot duration | 2 seconds (60 frames) |

---

## Section 6: Colour Treatment Spec

All 5 videos use neutral, ungraded footage:

| Property | Value |
|----------|-------|
| Temperature | Neutral |
| Contrast | Normal |
| Saturation | Normal |
| Grade/LUT | None |

**Do not apply colour grading.** The production quality comes from cut rhythm and composition, not colour treatment.

---

## Section 7: Audio Spec

| Property | Value |
|----------|-------|
| Background music | **Mandatory** — every short-form video gets background music |
| Audio strategy | **Music + SFX** (always) |
| Music energy changes | None — constant throughout |
| SFX at transitions | Camera click on visual-type family changes |
| Voiceover | Continuous throughout entire video |

**Single mandatory audio strategy:**

| Strategy | Description |
|----------|-------------|
| **Music + SFX** (always) | Voiceover + background music at 0.08–0.12 volume + click SFX on visual-type family transitions |

Every short-form video gets background music AND transition swooshes. No opt-out.

### Background Music Spec

| Property | Value |
|----------|-------|
| Source | Pre-curated library at `example-account-brand-plugin/context/brand/brand-assets/background-music/` — see `audio-library.yaml` for catalog |
| Volume | 0.08–0.12 (ducked under voiceover) |
| Fade in | 0.5 seconds |
| Fade out | 1.0 seconds |
| Genre | Corporate/tech, 90–136 BPM, no lyrics |
| Energy | Matched to video mood via `audio-library.yaml` mood tags |
| Track selection | Match storyboard metadata `mood` field against `audio-library.yaml` mood tags |

### Transition SFX Spec

| Property | Value |
|----------|-------|
| Sound | Trimmed snap click (`sfx/click-snap-01.wav`), **170ms** — no dead air |
| Trigger | Visual-type FAMILY change only |
| FFmpeg volume | **`volume=6.0`** in the click track (pre-mix stage 1). This produces clicks at ~-10dB which cuts through voiceover at ~-4.5dB. |
| Timing offset | **-60ms** — snap peaks at 60ms into the clip, so `adelay = cut_time_ms - 60` places the peak exactly on the visual cut |
| Paired visual | **FlashTransition** — 4-frame white flash (opacity 0→0.5→0) centered on the cut frame. The snap peak and flash peak hit simultaneously. |

**Snap + Flash pairing (MANDATORY for all short-form):**
The click SFX and visual flash are a paired system — never use one without the other. The snap peak (60ms) and flash peak (cut frame) must be synchronized:
- **Audio:** `adelay = (startFrame / fps * 1000) - 60` in the FFmpeg audio mix
- **Visual:** `<FlashTransition atFrame={startFrame} />` in Root.tsx for each click boundary
- **Flash spec:** White (#FFFFFF) overlay, opacity ramps 0→0.5→0 over 4 frames (2 before cut, 2 after), z-index above all segments

**Visual-type families (no click within same family):**
- Speaker family: V1 (speaker), V2 (speaker-zoom), V7 (CTA)
- MG family: V4 (motion-graphic), V4b (MG cutaway)
- Split-screen: V5
- Hook-text: V6

A click fires only when the visual-type family changes between adjacent segments (e.g., speaker → MG, MG → split-screen). Transitions within the same family (e.g., V1 → V2, V4 → V4b) get no click.

### Audio Mix Pipeline

Background music and swoosh SFX are pre-mixed into a single audio file via FFmpeg in step-04 (Section 7: Audio Mix). This keeps Remotion within the 2-element `<Audio>` limit (Rule 4): one for voiceover, one for the pre-mixed music+SFX file.

**Remotion implementation:** The pre-mixed audio file is referenced via `PROJECT.backgroundMusic`. It is always set (never null) for short-form videos.

**CRITICAL — Volume levels are PRE-BAKED in the FFmpeg mix.** The mix contains music at `volume=0.08` and clicks at `volume=6.0` (relative to full scale). Remotion plays the mix at `volume=1.0` and ONLY applies a fade-in/fade-out envelope. These values are calibrated so clicks peak at ~-10dB, cutting through voiceover at ~-4.5dB.

**Three rules that MUST be followed (violations cause inaudible audio):**
1. **No double-attenuation** — Do NOT apply `backgroundMusicVolume` (0.08) on top of the pre-mixed file. The mix is already leveled. Remotion volume = 1.0.
2. **2-stage FFmpeg mix** — Build a click track first (all clicks onto silence), THEN mix with music as 2 inputs. Never mix N clicks + music as N+1 inputs — `amix` normalizes by 1/N, crushing the clicks.
3. **Click volume = 6.0** — This is the calibrated value. Music at 0.08 + clicks at 6.0 produces the right relative levels where clicks punch through speech.

```tsx
// Root.tsx — background music + SFX pre-mix (always present for short-form)
// Levels pre-baked in FFmpeg mix. Remotion only handles fade envelope.
{PROJECT.backgroundMusic && (
  <Audio
    src={PROJECT.backgroundMusic}
    volume={(f) => {
      const fadeInEnd = Math.round(0.5 * PROJECT.fps);
      const fadeOutStart = PROJECT.totalDurationInFrames - Math.round(1.0 * PROJECT.fps);
      if (f < fadeInEnd) return interpolate(f, [0, fadeInEnd], [0, 1]);
      if (f > fadeOutStart) return interpolate(f, [fadeOutStart, PROJECT.totalDurationInFrames], [1, 0]);
      return 1;
    }}
    pauseWhenBuffering
  />
)}
```

---

## Section 8: Motion Graphics Strategy (MG-First)

### Hard Rule: No Raw B-Roll in Final Video

All non-speaker visuals in short-form content are motion graphics (Tier A: Remotion-native, Tier B: reference-frame Ken Burns, Tier C: Hera AI-generated). Raw B-roll (screen recordings, website captures, terminal screenshots) is **never** used directly in the final video.

### Rationale

All 5 inspiration videos (@nateherkai, @nick_saraev) use animated visuals for non-speaker segments — not static screen captures. Static B-roll looks flat and amateur compared to motion graphics with cursor movement, loading animations, and UI interactions.

### Pipeline Flow

1. **Extract B-roll** from long-form source (as reference material only)
2. **Extract keyframe** from B-roll clip: `ffmpeg -i "broll/sf-broll-{NN}.mp4" -vf "select=eq(n\,0)" -frames:v 1 "reference-frames/sf-broll-{NN}-keyframe.png"`
3. **Generate Hera MG** with `reference_image_url` pointing to the keyframe — prompt describes animated version of the static content
4. **Upscale** Hera output from 1080×1920 → target resolution (e.g., 2160×3840)
5. **Use in Remotion** — `staticFile('motion-graphics/...')` in theme.ts

### Split-Screen Overlay Zone

For V5 (split-screen) segments, the overlay zone receives MG files, never raw B-roll clips:
- `overlaySrc: staticFile('motion-graphics/sf-{NN}-mg-broll-{XX}.mp4')` — correct
- `overlaySrc: staticFile('broll/sf-broll-{XX}.mp4')` — **FORBIDDEN** for short-form

### Reference Frame Prompting

When generating Hera MGs from B-roll reference frames, the prompt should describe an **animated version** of the static content:
- Static website screenshot → "Animated dashboard with elements sliding in, cursor hovering, subtle glow pulse"
- Terminal output → "Dark terminal with text appearing line by line, typewriter effect, cursor blinking"
- IDE file structure → "File explorer with folders expanding, files highlighting in sequence, code preview sliding in"

---

## Section 9: Structural Overlays (Optional — Tutorial Content)

These overlays are used in tutorial-style reels to add visual structure. They are optional and should be used when the content has distinct steps or sections.

### Step Labels

| Property | Value |
|----------|-------|
| Font weight | 800 |
| Size | 7% of frame height |
| Color | `#FFFFFF` |
| Text case | ALL CAPS |
| Position | 12% from top |
| Background | Semi-transparent dark pill (`rgba(0,0,0,0.5)`, 16px padding, 24px border-radius) |

### B-Roll Title Overlays

| Property | Value |
|----------|-------|
| Font style | Serif italic bold |
| Size | 6% of frame height |
| Color | `#222222` (dark on light backgrounds) or `#FFFFFF` (on dark) |
| Position | 15% from top |

### Red Indicator Arrows

| Property | Value |
|----------|-------|
| Color | `#EF4444` |
| Animation | Pop-in `0 → 1.0` over 4 frames with spring bounce |
| Usage | Point to specific UI elements during tutorial demos |

---

## Section 10: CTA Pattern Spec

Derived from 4/5 videos that end with a comment-based CTA.

### CTA Structure

| Property | Value |
|----------|-------|
| Layout | Full-frame speaker |
| Zoom | 1.04–1.06x (V7 uses `zoomFactor: 1.05`) |
| Duration | 3–5 seconds (last segment) |
| CTA type | Comment-based ("Comment X and I'll send you Y") — 4/5 videos |
| CTA highlight | Optional green `#4ADE80` on the CTA keyword |
| Ending | **Abrupt** — zero dead frames, no end card, no fade-out. Loop-encouraging. |

### CTA Rules

1. **No end cards** — the video ends mid-energy, encouraging Instagram's auto-loop
2. **No fade-to-black** — hard cut to nothing (loop point)
3. **Comment CTA pattern** is primary — direct response ask
4. **CTA keyword** may be highlighted in `#4ADE80` teal (e.g., "Comment **CLAUDE** below")

---

## Quick Reference: Remotion Parameter Map

For use by storyboard step and Remotion scaffolding:

```
CAPTIONS:
  strategy: platform-native (zero burned-in text in Remotion)
  youtube: SRT file from clipped-refined-transcript.json, uploaded via API
  instagram: platform auto-captions toggled per post
  tiktok: platform auto-captions toggled per post
  remotion: NO VerticalCaptionV2, NO VerticalCaption, NO CAPTION_PAGES

ZOOM:
  V1_speaker: 1.03
  V2_emphasis: 1.08
  V7_cta: 1.05
  speed: slow (full segment duration)

MG_MOTION (Ken Burns — MANDATORY):
  default_zoom: 1.0 → 1.15 (MotionGraphic zoomFactor: 1.15)
  aggressive_zoom: 1.0 → 1.3
  static_display: FORBIDDEN

SPLIT_SCREEN:
  primaryRatio: '50/50' (content top, speaker bottom)
  secondaryRatio: '65/35' (available, NOT default)
  speakerPosition: bottom
  divider: transparent (no visible divider)

AUDIO:
  strategy: 'music-sfx' (always — every short-form video)
  backgroundMusic: staticFile('audio/sf-{NN}-audio-mix.mp3') (pre-mixed music + swoosh SFX)
  backgroundMusicVolume: 0.08
  transitionSfx: click on visual-type family changes only

CTA:
  zoom: 1.05
  ending: abrupt (zero dead frames, no end card)
  ctaHighlightColor: '#4ADE80'

TRANSITIONS:
  type: hard-cut only (no effects)

CUT_RHYTHM:
  hookCuts: 2-3 in first 3s
  bodyInterval: ~60 frames (2s)
  ctaDuration: 90-120 frames (single shot)
```
