---
name: pre-storyboard
description: Unified analysis + clipping pipeline — chains Audio Analysis, Transcription, Visual Analysis, and Video Clipping for all project videos in one command
web_bundle: true
---

# Pre-Storyboard Pipeline — Analysis + Clipping

**Goal:** Run the complete analysis-to-clipping pipeline for all videos in a project with a single command. This is Step 1 of a two-step approach: (1) Pre-Storyboard (this workflow) produces clipped videos ready for editorial review, then (2) Full Pipeline (storyboard + Remotion) produces the final edit.

**Your Role:** In addition to your name, communication_style, and persona, you are the pre-storyboard pipeline orchestrator. You chain AA → TR → VA → VC for each video in the project, with quality gates between phases.

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Per-Video Sequential**: Each video goes through all 4 workflows before the next video starts
- **Video Ordering**: Process `body` content first, then `intro`, then `outro` (if exists)
- **Gate Enforcement**: Quality gates between workflows — no silent continuation past failures
- **Fresh Run**: Delete existing analysis/clips data for the project before starting (user must confirm)
- **Proxy for Analysis, Raw for Output**: API calls use proxy files; final clipped output uses raw files

### Pipeline Per Video

```
VIDEO N:
  │
  PHASE 1: AUDIO ANALYSIS [AA]
    Execute audio-analysis workflow (steps 1-3)
    Gate: audio-analysis.json exists, classified_regions non-empty
    │
  PHASE 2: TRANSCRIPTION [TR]
    Execute transcription workflow (steps 1-4)
    Gate: transcript.json exists, words array non-empty
    │
  PHASE 3: VISUAL ANALYSIS [VA]
    Execute visual-analysis workflow (steps 1-3)
    Gate: visual-analysis.json exists, segments array non-empty
    │
  PHASE 4: VIDEO CLIPPING [VC]
    Execute video-clipping workflow (steps 1-5)
    Gate: clipped video file exists, duration > 0
    │
  ✓ VIDEO N COMPLETE
```

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `output_folder`
- `env_file` (for API keys)

### 2. Project Discovery

Load active project from `{project-root}/_bmad/ccs/active-project.yaml`.

Discover all video registry YAML files:
`{project_folder}/{project-slug}/video-editor/raw/*.yaml`

**Build video processing list:**
1. Filter to `role: proxy` entries only (these are the analysis sources)
2. For each proxy, resolve its paired raw file (find YAML where `video_id` matches `paired_with`)
3. Sort by `processing_order` (ascending), then by content_type priority: body → intro → outro

**Present discovery:**
"**Pre-Storyboard Pipeline — Project: {project_title}**

Videos to process:
| # | Video ID | Content Type | Proxy | Raw | Duration |
|---|----------|-------------|-------|-----|----------|
| 1 | {video_id} | {content_type} | {proxy_filename} | {raw_filename} | {duration} |
| ... | ... | ... | ... | ... | ... |

**Total videos:** {count}
**Estimated pipeline:** AA → TR → VA → VC × {count} videos"

### 3. Confirm Fresh Run

"**This will delete all existing analysis and clips data for this project and re-run from scratch.**

Folders to clear:
- `{project_folder}/{project-slug}/video-editor/analysis/`
- `{project_folder}/{project-slug}/video-editor/clips/`

**Proceed? [Y] Yes / [N] Cancel**"

Wait for user confirmation. If N → HALT.

If Y → delete the analysis/ and clips/ directories, then proceed.

### 4. Visual Analysis Granularity — Auto-Configuration

Auto-configure Gemini frame sampling rate based on content type (no user prompt):

- **Body/Main videos:** Standard — 0.2 FPS (1 frame/5 seconds)
- **Intro videos:** High — 1.0 FPS (1 frame/second, short content needs more detail)
- **Outro videos:** Standard — 0.2 FPS

"**Visual Analysis FPS auto-configured:**
- Body/Main: 0.2 FPS (Standard)
- Intro: 1.0 FPS (High)"

Store the FPS values for use in Phase 3 of each video.

---

## PIPELINE EXECUTION

### Per-Video Loop

For each video in the processing list:

"**[PSB] Processing video {N}/{total}: {video_id} ({content_type})**"

#### Phase 1 — Audio Analysis [AA]

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis/` workflow:
- Step 01 (init): Use the proxy video file, set content_type from registry
- Step 02 (analyse): Run analyze-audio.ts with `--content-type {content_type}` and `--no-denoise` off (denoising enabled)
- Step 03 (output): Validate and write audio-analysis.json

**Gate AA:** Verify `audio-analysis.json` exists and `classified_regions` is non-empty.
- If fails → HALT: "Gate AA FAILED for {video_id}: audio-analysis.json missing or empty."

"**[PSB] {video_id} — Audio Analysis complete. {speech_regions} speech regions, {total_speech}s speech.**"

#### Phase 2 — Transcription [TR]

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/transcription/` workflow:
- Step 01 (init): Load audio file from analysis folder
- Step 02 (prepare): Validate audio format
- Step 03 (transcribe): DeepGram Nova-3 with `filler_words=true`, `smart_format=true`, `utterances=true`
- Step 04 (output): Write transcript.json

**Gate TR:** Verify `transcript.json` exists and words array is non-empty.
- If fails → HALT: "Gate TR FAILED for {video_id}: transcript.json missing or empty."

"**[PSB] {video_id} — Transcription complete. {word_count} words, {confidence}% avg confidence.**"

#### Phase 3 — Visual Analysis [VA]

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/visual-analysis/` workflow:
- Step 01 (init): Use proxy video, set FPS from the granularity selection in step 4
- Step 02 (analyse): Gemini 2.5 Pro with structured output, visual events enabled
- Step 03 (output): Compile, validate timeline, write visual-analysis.json

**Gate VA:** Verify `visual-analysis.json` exists and segments array is non-empty.
- If fails → HALT: "Gate VA FAILED for {video_id}: visual-analysis.json missing or empty."

"**[PSB] {video_id} — Visual Analysis complete. {segment_count} segments, {visual_events} visual events.**"

#### Phase 4 — Video Clipping [VC]

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping/` workflow:
- Step 01 (init): Auto-detect content_type from registry, discover proxy + raw paths
- Step 02 (audio cleanup): Deterministic speech extraction with visual distraction handling
- Step 03 (transcript analysis): Content cut identification with flow-based auto-decision
- Step 04 (review): Skipped — cuts auto-decided in step 03
- Step 05 (generate): Merge cuts, orphaned fragment cleanup, execute FFmpeg with raw source, update registry

**Gate VC:** Verify clipped video file exists and has duration > 0.
- If fails → HALT: "Gate VC FAILED for {video_id}: clipped video missing or zero-length."

"**[PSB] {video_id} — Video Clipping complete. {keep_segments} segments, {reduction}% reduction, output: {clipped_file}.**"

---

## PIPELINE COMPLETE

After all videos are processed:

"**Pre-Storyboard Pipeline — Complete**

| Video | Content Type | Original | Clipped | Reduction | Segments |
|-------|-------------|----------|---------|-----------|----------|
| {video_id} | {type} | {orig_duration} | {clip_duration} | {reduction}% | {segments} |
| ... | ... | ... | ... | ... | ... |

**All {count} videos analysed and clipped.**

**Output files:**
- Analysis: `{project_folder}/{project-slug}/video-editor/analysis/`
- Clips: `{project_folder}/{project-slug}/video-editor/clips/`

**Next step:** Review clipped videos, then run [FP] Full Pipeline or [SB] Storyboard workflow."

---

## ERROR HANDLING

### Gate Failure Protocol

On any gate failure:
1. Log which video and which phase failed
2. Report the current state (which videos completed, which failed)
3. HALT — do not continue to the next video or phase
4. Suggest the specific action needed to unblock

### Resume After Failure

If the pipeline was halted mid-way:
- Already-completed videos (with valid output files) can be skipped on re-run
- The failed video must be re-processed from Phase 1 (AA) for that video

**Master Rule:** Every phase must complete with valid output before the next phase begins. Never silently skip a failed analysis step — incomplete data produces bad clips.
