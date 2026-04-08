---
name: short-form-edit
description: Platform-specific short-form vertical cuts (9:16)
menu-code: SF
---

# [SF] Short-Form Edit

**Goal:** Take 5 user-filmed landscape (16:9) videos and produce 5 fully edited vertical (9:16) short-form videos with motion graphics, captions, and visual effects — ready for Instagram Reels, TikTok, and YouTube Shorts.

**Source format:** All source videos filmed in landscape (16:9) at 4K. Speaker-only segments are centre-cropped from 16:9 to 9:16 via `objectFit: 'cover'` with `objectPosition` for face framing.

**Role:** Short-form video editing automation specialist. Executes the technical pipeline with precision. Creative decisions come from the Copywriter SS workflow output.

---

## Execution Mode Selection

[A] **Auto** — Process all 5 videos end-to-end. Notified when all 5 rendered MP4s are ready.
[C] **Collab** — Review at each checkpoint with full control.

---

## Pipeline Execution Model

```
Step 1 (init, all 5)
  |
Step 2 — 5 parallel sub-agents (one per video: AA -> TR -> Refine -> VC -> C2)
  | all 5 complete
Steps 3-5 PIPELINE:
  Main agent builds storyboards sequentially
  Background sub-agents handle asset prep per video as storyboard completes
  MG REVIEW GATE — consolidated Tier C MG prompt review
  Step 4: Poll all MG IDs, download, upscale
  Step 5: Scaffold all 5 (parallel) -> Render sequentially
```

---

## Step 1: Init

Discover all 5 source video files. Create registry YAMLs. Generate 720p proxies.

## Step 2: Batch Analysis (Parallel)

For each of the 5 videos, run in parallel:
- Audio Analysis (AA) with denoising
- Transcription (TR) with DeepGram Nova-3
- Transcript refinement
- Video Clipping (VC) with content-type-appropriate buffers
- Clipped transcript remap (C2)

Gate: all 5 must complete before proceeding.

## Step 3: Storyboard (Sequential with Background Prep)

For each video sequentially:
- Build storyboard using vertical segment patterns (V1-V7)
- Apply short-form pacing rules (P1-P11)
- Plan MG-first visual coverage (target 80%+ non-speaker coverage)
- Background sub-agent handles logo/screenshot prep per video

**MG Review Gate:** After all 5 storyboards complete, present consolidated Tier C MG table for user review before any Hera dispatch.

## Step 4: Assets

After MG prompt approval:
- Dispatch all Tier C MGs to Hera Video API
- Poll all MG IDs in unified loop
- Download, verify, upscale completed MGs

## Step 5: Remotion

Scaffold all 5 Remotion projects (parallel). Render each sequentially:
- Apply vertical-specific Remotion hard rules
- 9:16 format, centre-crop speaker segments
- MG overlay positioning for vertical layout

---

## Key Reference Data

- Short-form pacing rules (P1-P11)
- Vertical segment patterns (V1-V7)
- Vertical template library
- Vertical Remotion hard rules (5 additional rules)
- Production style guide
