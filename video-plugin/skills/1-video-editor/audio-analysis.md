---
name: audio-analysis
description: Waveform and volume mapping at timestamp level for precision clipping
menu-code: AA
---

# [AA] Audio Analysis

**Goal:** Analyse audio tracks of ingested video using FFmpeg filters to produce waveform data, volume mapping, silence detection, and loudness metrics at timestamp granularity. This data drives intelligent clipping decisions in the Video Clipping workflow.

**Role:** Video pipeline operator and audio analyst. Concise, status-report, mechanical and factual communication.

---

## Phase 1: Init and Resolve Video

### 1.1 Accept Video ID

If video ID was not provided during workflow invocation, ask:

"**Which video should I analyse?** Please provide the video ID (e.g., `project-alpha-body`)."

### 1.2 Locate Registry YAML

Search for: `{project_folder}/{project-slug}/video-editor/raw/{video-id}.yaml`

- **If not found:** HALT — "No registry entry found. Run Video Ingest first."
- **If found:** Read complete YAML and extract all metadata fields.

### 1.3 Resolve File Path (Proxy Preference)

1. Read the `role` and `paired_with` fields
2. If this file IS a proxy (`role: proxy`): use its `source_path` directly
3. If raw AND has `paired_with`: look up paired YAML — if paired is proxy, use its path
4. If raw AND no pair: use this file's `source_path`

### 1.4 Validate and Report

Verify file exists on disk. Report resolution results:

"**Video Resolved.** Video ID: `{video-id}` | Content Type: `{content_type}` | File: `{resolved_filename}` ({proxy/raw})"

---

## Phase 2: Run Audio Analysis

### 2.1 Check Dependencies

Verify: ffmpeg (with arnndn filter), python3, silero-vad, npx/tsx, curl. If `node_modules/` absent in script directory, run `npm install`.

### 2.2 Determine Output Path

**Project mode:** `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/audio-analysis.md`

Create directory if needed.

### 2.3 Construct and Execute Command

```bash
npx tsx "{script_dir}/analyze-audio.ts" \
  --video "{resolved_file_path}" \
  --output "{analysis_md_path}" \
  --content-type "{content_type}" \
  [--transcript "{transcript_json_path}"]  # if transcript.json exists
```

The script runs FFmpeg silencedetect + dB waveform + Silero VAD with automatic audio denoising (highpass 80Hz + RNNoise arnndn). It writes both a 5-section markdown and `audio-analysis.json` directly.

### 2.4 Validate Execution

- Exit code 0: proceed
- Non-zero: HALT with error details (check ffmpeg, silero-vad, npx, disk space)

---

## Phase 3: Parse Output and Write JSON

### 3.1 Direct JSON Path

The script writes `audio-analysis.json` directly. If it exists, read it, merge project metadata (video_id, project_group, content_type), and write to the final path.

### 3.2 Fallback: Parse 5-Section Markdown

If direct JSON missing, parse the markdown's 5 sections:

1. **Audio Metadata** — overall_rms_dbfs, peak_dbfs, noise_floor_dbfs, dynamic_range_db, speech/silence/breath/noise totals
2. **Silence Regions** — array of {startMs, endMs, durationMs}
3. **VAD Speech Regions** — array of {startMs, endMs, durationMs, avgProbability}
4. **Speech Boundary Detail** — per-region onset/offset tables at 20ms resolution
5. **Classified Regions** — array of {startMs, endMs, durationMs, classification, confidence, avgDb, vadProb}

Valid classifications: `SPEECH`, `SILENCE`, `BREATH`, `NOISE`

Preserve `filler_regions` if present (from `--transcript` flag).

### 3.3 Assemble and Write JSON

Write to: `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/audio-analysis.json`

Schema includes: video_id, project_group, content_type, source_file, analysis_date, audio_metadata, volume (legacy), loudness (legacy), silence_regions, speech_regions, speech_boundary_detail, classified_regions, filler_regions.

### 3.4 Report Completion

Report key metrics: Overall RMS, Peak Level, Noise Floor, Dynamic Range, region counts by classification.

Recommend next: **Video Clipping** workflow (classified_regions populated).
