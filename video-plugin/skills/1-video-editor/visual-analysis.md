---
name: visual-analysis
description: Gemini Pro screen analysis at timestamps for scene types, tools, and B-roll opportunities
menu-code: VA
---

# [VA] Visual Analysis

**Goal:** Analyse video frames using Gemini Pro to understand what's happening visually at each timestamp — identifying scene types, tools being used, user activity, and B-roll extraction opportunities.

**Role:** Video analysis pipeline operator. Technical, precise, prescriptive. Minimal interaction after initial configuration.

---

## Correction Detection

When the user corrects your output at any step in this workflow:
1. Apply the fix immediately
2. Assess: Is this a reusable correction? (A visual analysis pattern, FPS setting, or scene classification rule that should apply in future)
3. If yes → prompt: **"That's a useful fix. Save it to the wiki so it doesn't recur? [Y/N]"**
4. If Y → run [WU] inline: most visual analysis corrections belong in `wiki/storyboard.md` or `wiki/motion-graphics.md`, append the entry, confirm
5. Continue the workflow from where you left off

## Phase 1: Init and Configuration

### 1.1 Discover Video File

Search Video Ingest registry for the target video. Present found video for confirmation. If not found, ask for path.

### 1.2 Configure Analysis Granularity

"**Analysis granularity — how many frames should Gemini analyse per second?**

[S] Standard — 0.2 FPS (1 frame every 5 seconds) — good for body/main content
[H] High — 1.0 FPS (1 frame per second) — good for short intros, fast-paced content
[C] Custom — Specify your own FPS"

Auto-configure based on content type if running within Pre-Storyboard Pipeline:
- Body/Main: 0.2 FPS
- Intro: 1.0 FPS
- Outro: 0.2 FPS

### 1.3 Assess Chunking Requirements

Based on video duration and FPS, calculate total frames and token budget. If frames exceed Gemini context limit, determine chunk count and boundaries.

---

## Phase 2: Gemini Analysis

### 2.1 Extract Frames

Use FFmpeg to extract frames at the configured FPS:
```bash
ffmpeg -i "{video_path}" -vf "fps={fps}" "{output_dir}/frame_%04d.jpg"
```

### 2.2 Submit to Gemini

Use Gemini 2.5 Pro with structured output. For each frame/chunk:
- Identify scene type (talking-head, screen-share, mixed, b-roll, transition)
- Identify tools/software visible on screen
- Describe user activity
- Flag B-roll extraction opportunities
- Detect visual events (transitions, zoom changes, new content appearing)

### 2.3 Handle Chunking

If chunked: process each chunk sequentially, merge results with overlap deduplication at chunk boundaries. Ensure timeline continuity across chunks.

---

## Phase 3: Output

### 3.1 Compile Results

Assemble all analysis results into a single timeline-ordered JSON:
```json
{
  "video_id": "{video-id}",
  "content_type": "{content_type}",
  "analysis_date": "{ISO timestamp}",
  "fps": {fps_used},
  "segments": [
    {
      "startMs": 0,
      "endMs": 5000,
      "scene_type": "talking-head",
      "tools_visible": [],
      "activity": "Speaker introducing topic",
      "broll_opportunity": false,
      "visual_events": []
    }
  ]
}
```

### 3.2 Validate Timeline

Ensure no gaps or overlaps in segment timeline. Verify all segments have required fields.

### 3.3 Write JSON

Write to: `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/visual-analysis.json`

Report: segment count, visual event count, scene type distribution, B-roll opportunity count.
