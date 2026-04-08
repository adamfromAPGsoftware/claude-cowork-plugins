---
name: pre-storyboard
description: One command — AA, TR, VA, VC for all project videos
menu-code: PSB
---

# [PSB] Pre-Storyboard Pipeline

**Goal:** Run the complete analysis-to-clipping pipeline for all videos in a project with a single command. This is Step 1 of a two-step approach: (1) Pre-Storyboard produces clipped videos ready for editorial review, then (2) Full Pipeline or Storyboard produces the final edit.

**Role:** Pre-storyboard pipeline orchestrator. Chains AA -> TR -> VA -> VC for each video with quality gates between phases.

---

## Architecture

- **Per-Video Sequential:** Each video goes through all 4 workflows before the next starts
- **Video Ordering:** Process body first, then intro, then outro (if exists)
- **Gate Enforcement:** Quality gates between workflows — no silent continuation past failures
- **Fresh Run:** Delete existing analysis/clips data before starting (user confirms)
- **Proxy for Analysis, Raw for Output:** API calls use proxy files; final clipped output uses raw files

---

## Initialization

### 1. Project Discovery

Load active project from `_bmad/ccs/active-project.yaml`. Discover all video registry YAMLs. Filter to `role: proxy` entries. Sort by processing_order, then content_type priority: body -> intro -> outro.

### 2. Confirm Fresh Run

"**This will delete all existing analysis and clips data and re-run from scratch.**
Folders to clear: `analysis/` and `clips/`. Proceed? [Y/N]"

### 3. Visual Analysis FPS Auto-Configuration

- Body/Main: 0.2 FPS (Standard)
- Intro: 1.0 FPS (High — short content needs more detail)
- Outro: 0.2 FPS (Standard)

---

## Per-Video Pipeline

For each video:

### Phase 1 — Audio Analysis [AA]
Execute audio-analysis capability. **Gate AA:** Verify `audio-analysis.json` exists and `classified_regions` is non-empty.

### Phase 2 — Transcription [TR]
Execute transcription capability. **Gate TR:** Verify `transcript.json` exists and words array is non-empty.

### Phase 3 — Visual Analysis [VA]
Execute visual-analysis capability with auto-configured FPS. **Gate VA:** Verify `visual-analysis.json` exists and segments array is non-empty.

### Phase 4 — Video Clipping [VC]
Execute video-clipping capability. **Gate VC:** Verify clipped video file exists and duration > 0.

---

## Pipeline Complete

"**Pre-Storyboard Pipeline Complete**

| Video | Content Type | Original | Clipped | Reduction | Segments |
...

**All {count} videos analysed and clipped.**

**Next step:** Review clipped videos, then run [FP] Full Pipeline or [SB] Storyboard."

---

## Error Handling

On any gate failure:
1. Log which video and phase failed
2. Report current state (which videos completed, which failed)
3. HALT — do not continue
4. Suggest specific action to unblock

**Resume:** Already-completed videos can be skipped on re-run. Failed video re-processes from Phase 1.
