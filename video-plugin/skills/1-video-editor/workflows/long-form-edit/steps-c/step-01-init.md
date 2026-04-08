---
name: 'step-01-init'
description: 'Discover video files, load script, detect recording mode (multi-file vs single-file), generate proxies, create output directories'

nextStepFile: './step-02-analysis.md'
---

# Step 1: Initialize — Discover Videos, Detect Recording Mode, Load Script

## STEP GOAL:

Discover raw video files in the project's `video-editor/raw/` folder, detect whether this is a multi-file recording (separate intro + body files) or a single-file recording (one continuous take), generate 720p proxies if missing, load the script, extract intro text, and create all output directories.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 AUTO-PROCEED: Minimal user interaction — auto-detect from file structure
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a long-form video production specialist
- ✅ Technical, concise, efficient communication
- ✅ Execute with precision — creative decisions already made by Copywriter

### Step-Specific Rules:

- 🎯 Focus ONLY on discovery, proxy generation, script loading, and recording mode detection
- 🚫 FORBIDDEN to run audio analysis, transcription, or clipping in this step
- 🎯 Proxies are generated programmatically — no user action needed
- 🎯 Recording mode detection is based on YAML `content_type` values, not file count alone

## MANDATORY SEQUENCE

### 1. Load CCS Config

Load and read full config from `{project-root}/_bmad/ccs/config.yaml` and resolve:
- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- Resolve `{project_folder}` and `{project-slug}` for the active project

### 1b. Auto-Ingest from Drop Folder

Scan `{project_folder}/{project-slug}/video-editor/video-ingest/` for raw video files (`.mp4`, `.mov`, `.mkv`).

**If raw video files found AND no registry YAMLs exist in `raw/`:**

1. For each video file, probe with ffprobe:
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration,codec_name \
  -show_entries format=duration,size,filename \
  -of json "{video_ingest_path}/{filename}"
```

2. Create a registry YAML in `{project_folder}/{project-slug}/video-editor/raw/`:
```yaml
video_id: "{project-slug}-full"
content_type: full
role: raw
status: registered
metadata:
  filename: "{original_filename}"
  source_path: "{video_ingest_path}/{filename}"
  resolution: "{W}x{H}"
  duration: {duration}
  codec: "{codec_name}"
  auto_ingested: true
```

3. Log: "**Auto-ingested:** {filename} → registered as `content_type: full` (single-file mode)"

**If registry YAMLs already exist in `raw/`:** Skip this section entirely (backward compatible — existing multi-file or pre-registered projects continue unchanged).

**If no files found in `video-ingest/` AND no YAMLs in `raw/`:** HALT — "No video files found. Either drop a raw video into `video-ingest/` or register files via `[VI] Video Ingest`."

### 2. Scan for Registry YAMLs

Scan `{project_folder}/{project-slug}/video-editor/raw/` for `.yaml` registry files.

For each YAML found, extract:
- `video_id`, `content_type`, `role`, `metadata.filename`, `metadata.source_path`

### 3. Detect Recording Mode

Determine recording mode from the discovered YAMLs:

**Multi-file mode** (separate intro + body recordings):
- 2+ YAMLs with different `content_type` values (e.g., `intro` and `main`)
- Each file is analysed independently with its own content_type thresholds

**Single-file mode** (one continuous recording):
- 1 YAML with `content_type: full`, OR only 1 YAML present regardless of content_type
- Requires boundary detection in step-02 to find where intro ends and body begins

Set session variable `{recording_mode}` to `multi-file` or `single-file`.

### 4. Probe All Videos with ffprobe

For each registered video file:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration \
  -show_entries format=duration,size \
  -of json "{video_path}"
```

"**Raw Videos Discovered:**

| # | Video ID | Content Type | Resolution | Duration | Size | File |
|---|----------|-------------|-----------|----------|------|------|
| 1 | {id} | {content_type} | {W}x{H} | {dur}s | {size}MB | {filename} |
| ... | ... | ... | ... | ... | ... | ... |

**Recording Mode:** {multi-file / single-file}"

### 5. Generate Proxies If Missing

For each raw video, check if a corresponding proxy exists (paired via `paired_with` in YAML, or by convention `{id}-proxy`).

If proxy is missing, generate a 480p proxy (small, fast — proxies are only used for API calls and analysis, not final output):

```bash
ffmpeg -i "{raw_video_path}" \
  -vf "scale=480:-2" \
  -c:v libx264 -preset ultrafast -crf 28 \
  -c:a aac -b:a 96k \
  -movflags +faststart \
  "{proxy_output_path}"
```

Verify each proxy:
- File exists and is playable (ffprobe succeeds)
- Resolution is 480px wide
- Duration matches raw file (within ±0.1s)
- Audio track present

### 6. Load Script

Load the script file from `{project_folder}/{project-slug}/copywriter/scripts/` — look for `script-*.md` or similar naming.

Extract from the script:
- **Intro text**: Everything in the intro section (Hook → Credibility → Value Promise → Barrier Removal → Bridge). This is the spoken text the presenter reads for the intro.
- **MG stage directions**: All `[MG-A]`..`[MG-G]` markers and their descriptions
- **Body structure**: Section headers and key content markers

Store the intro spoken text as `{script_intro_text}` — this is used for boundary detection in single-file mode.

### 7. Create Output Directories

Ensure these directories exist under `{project_folder}/{project-slug}/video-editor/`:

```bash
mkdir -p "{video_editor_path}/analysis/intro"
mkdir -p "{video_editor_path}/analysis/body"
mkdir -p "{video_editor_path}/clips"
mkdir -p "{video_editor_path}/storyboard"
mkdir -p "{video_editor_path}/broll"
mkdir -p "{video_editor_path}/motion-graphics"
mkdir -p "{video_editor_path}/remotion"
mkdir -p "{video_editor_path}/renders"
```

### 8. Summary and Proceed

**COLLAB mode:** Present discovery summary and wait for confirmation:

"**Initialization Complete**

| Setting | Value |
|---------|-------|
| Recording mode | {multi-file / single-file} |
| Videos found | {count} |
| Proxies ready | {count} |
| Script loaded | {script_filename} |
| Intro text extracted | {word_count} words |
| MG directions found | {count} ([MG-A] through [MG-{X}]) |

**Recording mode detected: {mode}**
{multi-file: Separate intro and body files — each will be analysed independently.}
{single-file: Single continuous recording — boundary detection will run in step 2 to split intro from body.}

[C] Continue to analysis | [A] Adjust recording mode"

**AUTO mode:** Log summary and auto-proceed.

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All registry YAMLs discovered and parsed
- Recording mode correctly detected (multi-file vs single-file)
- All raw videos probed with ffprobe
- 720p proxies generated or confirmed for all videos
- Script loaded with intro text extracted
- MG stage directions identified
- All output directories created
- Session variables set: `{recording_mode}`, `{execution_mode}`, `{video_files}`, `{script_intro_text}`

### ❌ SYSTEM FAILURE:

- Running audio analysis or transcription in this step
- Not detecting recording mode from YAML content_type values
- Proceeding without a loaded script
- Not generating proxies (trying to use 4K files for analysis)
- Proxy duration doesn't match raw duration
- Not extracting intro text from the script
