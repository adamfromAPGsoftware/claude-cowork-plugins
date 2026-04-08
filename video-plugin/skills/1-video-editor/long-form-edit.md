---
name: long-form-edit
description: Full production editing pipeline for long-form tutorial videos (16:9 landscape)
menu-code: LF
---

# [LF] Long-Form Edit

**Goal:** Take raw filmed footage (talking-head + screen recordings) and produce a fully edited long-form tutorial video with motion graphics, captions, jump-cut zooms, B-roll, and polished transitions — rendered via Remotion. The intro gets full segment decomposition; the body gets dead air removal only and plays as a single passthrough clip.

**Role:** Long-form video production specialist. Combines talking-head footage with screen share recordings, applies proven YouTube tutorial editing patterns.

---

## Drop and Go

Put your 4K video in `{project_folder}/{project-slug}/video-editor/video-ingest/` and run [LF]. Step 01 auto-detects the file, probes it, creates a registry YAML, generates a 720p proxy, and proceeds through the full pipeline.

---

## Execution Mode Selection

[A] **Auto** — Full pipeline end-to-end without stopping. Notified when rendered MP4 is ready.
[C] **Collab** — Review results at 3 checkpoints (after clipping, after storyboard, before render).

---

## Recording Mode Support

**Multi-file:** Separate intro + body recordings -> separate proxy YAMLs with content_type: intro and content_type: main.

**Single-file:** One continuous recording -> boundary detected by visual analysis (talking-head to screen-share transition), with transcript overlap as fallback.

---

## Pipeline Steps

### Step 1: Init
Discover files, auto-ingest from drop folder, load script, detect recording mode (multi-file or single-file).

### Step 2: Analysis
**Multi-file:** Intro and body branches run in parallel. Within each branch, audio analysis and transcription run concurrently, then refinement.

**Single-file:** Boundary VA runs in parallel with AA + TR. All three must complete before boundary detection.

### Step 3: Clipping
Split (single-file) -> Clip intro (150ms buffer) + body (300ms buffer) -> Remap transcripts -> Visual analysis on clipped videos.

All 4 FFmpeg clip commands (intro-proxy, intro-raw, body-proxy, body-raw) run as parallel background processes. Both transcript remaps run in parallel. Audio concatenation launches as background process. Both Gemini VA calls run simultaneously.

**Collab Checkpoint 1:** Review clipped video files, durations, removal stats.

### Step 4: Storyboard
Decompose intro into full Remotion segments. Body as single passthrough. Plan MGs, B-roll, captions, PiP. Validate pacing rules (P1-P18).

**Collab Checkpoint 2:** Review segment breakdown, MG briefs, pacing validation.

### Step 5: Assets
Three-phase parallel execution:
1. B-roll extractions + logo fetches + no-reference Hera MGs (concurrent)
2. Logo-dependent Hera MGs (after logos ready)
3. Unified Hera polling loop for all submitted jobs

Audio concat: verify-only (already done in step 3), fallback regenerate if missing.

---

## Editing Intensity Split

- **Intro:** Single continuous OffthreadVideo passthrough with jump-cut zoom segments (CSS scale alternation) + full-screen MG/B-roll/branded template overlays via Sequences. No per-segment video clipping.
- **Body:** Single continuous OffthreadVideo passthrough (Pattern 8) with light overlays — chapter cards (Remotion-native, never Hera) + concept MGs at speaker return/explanation points (P18). No segment decomposition.

---

## Remotion Architecture (MANDATORY — Passthrough + Overlay Pattern)

**HARD RULE:** The intro and body are ALWAYS rendered as continuous OffthreadVideo passthroughs with overlays on top. Never decompose the source video into per-segment clip files. This is critical for Remotion performance — loading many short video clips causes buffering, decode stalls, and timeline corruption. One long video + overlay Sequences is dramatically more stable.

**Pattern:**
```
<Sequence from={0} durationInFrames={introFrames}>
  <OffthreadVideo src="intro-clipped-raw.mp4" />  {/* continuous passthrough */}
</Sequence>
{MG_OVERLAYS.map(mg => (
  <Sequence from={mg.startFrame} durationInFrames={mg.dur}>
    {mg.type === 'broll' ? <BRollOverlay src={mg.src} /> : <FullScreenMG src={mg.src} />}
  </Sequence>
))}
```

**MG overlay types:**
- `hera-mg` → `FullScreenMG` (full-screen Hera-generated motion graphic, fade in/out)
- `broll` → `BRollOverlay` (retro VHS camera effect with "LATER IN VIDEO" badge, desaturation, scanlines, REC indicator)
- Branded templates (UpworkProfile, AgencyBrand) → rendered as dedicated Sequences

**Jump-cut zooms** are applied via CSS `transform: scale()` + `objectPosition` on the passthrough OffthreadVideo element, alternating per intro section (odd: 1.05x, even: 1.10x). No video re-encoding needed.

---

## Handoff to Remotion Edit

After all assets are ready, hands off to the Remotion Edit capability for scaffolding, code generation, QA, and rendering (steps 01-08).

---

## Key Reference Data

- Long-form pacing rules (P1-P18)
- Inspiration compliance checklist
- Inspiration video analyses and patterns
- MG style guide (aggregated from inspiration analyses)
- Segment patterns (Patterns 1-9, including Pattern 9: PiP Speaker)
- Remotion hard rules
- Caption style spec
- Template library (all Remotion templates including PiPSpeaker)
