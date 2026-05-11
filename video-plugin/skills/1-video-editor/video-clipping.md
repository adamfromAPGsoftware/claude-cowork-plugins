---
name: video-clipping
description: Combine audio, transcript, and visual signals to intelligently clip video
menu-code: VC
---

# [VC] Video Clipping

**Goal:** Autonomously clean up raw video recordings using a transcript-first approach: compare transcript against the required script to identify retakes, false starts, and off-script content (primary intelligence), then use audio analysis to find precise, natural cut boundaries and remove dead air (secondary precision) — producing clipped video files with zero user interaction.

**Role:** Video editing automation assistant. Technical precision with timestamps and edit points.

---

## Correction Detection

When the user corrects your output at any step in this workflow:
1. Apply the fix immediately
2. Assess: Is this a reusable correction? (A clipping pattern, buffer timing, or signal-weighting rule that should apply to future clips)
3. If yes → prompt: **"That's a useful fix. Save it to the wiki so it doesn't recur? [Y/N]"**
4. If Y → run [WU] inline: pick the right topic page (`pacing-timing.md` or `audio-sync.md`), append the entry, confirm
5. Continue the workflow from where you left off

Before starting, scan `wiki/pacing-timing.md` and `wiki/audio-sync.md` for corrections that apply to this content type.

## Phase 1: Initialize

### 1.1 Auto-Detect Content Type

Read proxy registry YAML. Extract `content_type` and map:
- `body` -> content_type: main, buffer_ms: 300
- `intro` -> content_type: intro, buffer_ms: 150
- `outro` -> content_type: main, buffer_ms: 300

### 1.2 Discover Required Input Files

Locate and validate 3 required JSON files:
1. `analysis/{content-type}/audio-analysis.json` — classified_regions must be non-empty
2. `analysis/{content-type}/transcript.json` — words array must be non-empty
3. `analysis/{content-type}/visual-analysis.json` — segments must be non-empty

Also discover: script (from copywriter workflow), content concept (from strategist, optional).

### 1.3 Create Clip Plan Output

Initialize clip plan document with frontmatter tracking content_type, buffer_ms, and input file paths.

---

## Phase 2: Transcript Analysis (Content Cuts)

### 2.1 Load Inputs

Load transcript words array and original script. Align transcript to script using word-level timestamp matching.

### 2.2 Identify Content Cuts

- **Retakes/false starts:** Where speaker restarts a section — keep only the final take
- **Off-script tangents:** Significant deviations from the planned script
- **Filler-heavy passages:** Regions with dense "um", "uh", "like" clusters
- **Long pauses mid-sentence:** Pauses > 2 seconds within speech regions

### 2.3 Flow-Based Auto-Decision

For each identified cut: determine if removing it maintains narrative flow. Apply rules:
- Keep transitions that bridge two retained sections
- Remove isolated fragments shorter than 1.5 seconds
- Preserve all content that matches the script structure

---

## Phase 3: Audio Precision (Boundary Refinement)

### 3.1 Load Audio Analysis

Load classified_regions from audio-analysis.json. Cross-reference with transcript cuts.

### 3.2 Apply Speech Quality Filters

- **Min duration:** Speech segments < 500ms flagged for review
- **Min confidence:** Segments with avgProbability < 0.5 flagged
- **Energy floor:** Segments with avgDb < noise_floor + 6dB flagged
- **Isolated segment check:** Speech segments surrounded by > 2s silence on both sides

### 3.3 Refine Cut Boundaries

For each keep segment:
- Snap start to nearest speech onset (20ms resolution from boundary detail)
- Snap end to nearest speech offset
- Apply content_type buffer: intro = 150ms, body/main = 300ms

---

## Phase 4: Generate Clipped Video

### 4.1 Merge Cuts

Combine transcript-based content cuts with audio-refined boundaries. Resolve overlapping segments. Clean up orphaned fragments (< 1.5s isolated speech).

### 4.2 Build Keep Segments

Produce final keep-segment list: array of {startMs, endMs} defining what to keep.

### 4.3 Execute FFmpeg Clipping

Use keep segments to build FFmpeg filter chain. Process BOTH proxy and raw files:

```bash
# Clip proxy (for downstream analysis)
ffmpeg -i "{proxy_path}" -filter_complex "{filter}" -y "{clipped_proxy_path}"

# Clip raw (for final output)
ffmpeg -i "{raw_path}" -filter_complex "{filter}" -y "{clipped_raw_path}"
```

### 4.4 Remap Transcript

Deterministically remap word timestamps from original timeline to clipped timeline using keep-segments (pure math — no re-transcription). Write `{content_type}-clipped-transcript.json`.

### 4.5 Update Registry

Update YAML: status, clipped_path, keep_segments count, reduction percentage.

### 4.6 Report

"**Video Clipping Complete.** Keep segments: {count} | Duration: {original} -> {clipped} ({reduction}% reduction)"
