---
name: broll-extraction
description: Extract B-roll clips from source video via FFmpeg
menu-code: BE
---

# [BE] B-Roll Extraction

**Goal:** Extract B-roll video clips from source video files using FFmpeg — from storyboard Visual Asset Source Map entries or manual timestamp input — delivering silent `.mp4` clips ready for Remotion integration.

**Role:** FFmpeg extraction pipeline operator. Technical precision with timestamps, codecs, and audio stripping.

---

## HARD RULES (NO EXCEPTIONS)

- ALL FFmpeg commands MUST include `-an` flag (strip audio)
- ALWAYS use full-resolution source files, NEVER 480p proxies
- ALWAYS include `-y` flag to overwrite without prompting

---

## Phase 1: Initialize

### 1.1 Determine Input Source

"**B-Roll Extraction — Initialization**

[S] Storyboard — Auto-discover from approved storyboard's Visual Asset Source Map
[M] Manual — Enter source video, timestamps, and descriptions manually"

### 1.2 Storyboard Discovery (if S)

Search `{project_folder}/{project-slug}/video-editor/storyboard/*-storyboard.md`. Extract all Visual Asset Source Map entries where `type: video-extract`. For each: broll-id, source_video, start_time, end_time, description.

### 1.3 Manual Input (if M)

Collect per clip: source video path, start time, end time, description.

### 1.4 Validate Source Files

Verify each source file exists. Confirm NOT a 480p proxy. Resolve output paths:
- **Project mode:** `{project_folder}/{project-slug}/video-editor/broll/{broll-id}.mp4`

---

## Phase 2: Extract

### 2.1 Generate FFmpeg Commands

```bash
ffmpeg -y -ss {start_time} -to {end_time} -i "{source_video}" -c:v libx264 -crf 18 -preset fast -an "{output_path}"
```

**Validation before presenting:** Confirm `-an` and `-y` in EVERY command. Confirm full-resolution source.

### 2.2 Execute

Present commands, then: [E] Execute All | [O] One-by-One | [X] Cancel

Process sequentially. Report after each: "Extracted: {broll-id}.mp4 ({file_size})"

### 2.3 Verify No Audio

For each extracted clip:
```bash
ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "{output_path}"
```
Expected: empty output. If audio detected, re-extract with explicit `-an`.

---

## Phase 3: Completion

### 3.1 Final Verification

Verify all `.mp4` files exist, non-zero size, no audio streams, full resolution.

### 3.2 Summary

"**B-Roll Extraction Complete**

| # | ID | Duration | Resolution | Size | Path |
...

**Total:** {success} extracted | {skip} skipped | {fail} failed
**Audio Streams:** None (all clips verified silent)

Ready for Storyboard and Remotion Edit workflows."
