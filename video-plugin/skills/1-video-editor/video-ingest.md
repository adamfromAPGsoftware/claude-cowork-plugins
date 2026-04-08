---
name: video-ingest
description: Detect raw video in watch folder, register and kick off pipeline
menu-code: VI
---

# [VI] Video Ingest

**Goal:** Detect new raw video files in the ingest folder, register metadata and proxy-raw mappings, and trigger the analysis pipeline after user confirmation.

**Role:** Video pipeline operator and file system analyst. Concise, status-report communication.

---

## Phase 1: Detect New Video Files

### 1.1 Resolve Ingest Path

Load Video Editor sidecar memories, read `last_active_project`.

- **If project exists:** Set `{video_ingest_path}` to `{project_path}/video-ingest/`. Confirm: "Active project: {active_project}. Scanning for new video files. Continue?"
- **If no project:** Check `_index.yaml` for available projects. If none, offer standalone mode.

### 1.2 Scan Folder

List all files in ingest folder. Identify video files by extension: `.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`, `.mxf`. Ignore non-video files.

### 1.3 Classify Each File

- **Role:** proxy (contains "proxy" in filename or subfolder) vs raw (default)
- **Content type:** body (default), intro (contains "intro"), outro (contains "outro")
- **Detect pairs:** Match proxy/raw files by naming convention

Report: structured table of detected files with role, content type, size, and detected pairs.

---

## Phase 2: Register Videos

### 2.1 Probe Metadata

For each detected video, run FFprobe:
```bash
ffprobe -v quiet -print_format json -show_format -show_streams "{file_path}"
```

Extract: duration, resolution, codec, frame rate, file size.

### 2.2 Generate Proxy (if raw only)

If a raw file has no paired proxy, generate one:
```bash
ffmpeg -i "{raw_path}" -vf "scale=-2:720" -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k "{proxy_path}" -y
```

### 2.3 Create Registry YAMLs

For each file, write a registry YAML to `{project_folder}/{project-slug}/video-editor/raw/{video-id}.yaml`:

```yaml
video_id: "{video-id}"
role: "{proxy|raw}"
content_type: "{body|intro|outro}"
paired_with: "{paired-video-id or null}"
processing_order: {1-N}
status: "ingested"
ingested_at: "{ISO timestamp}"
metadata:
  source_path: "{absolute file path}"
  duration_s: {duration}
  resolution: "{WxH}"
  codec: "{codec}"
  frame_rate: {fps}
  file_size_bytes: {size}
```

---

## Phase 3: Confirm and Trigger

### 3.1 Present Summary

"**Video Ingest Complete**

| # | Video ID | Role | Content Type | Duration | Resolution | Size | Pair |
|---|----------|------|-------------|----------|-----------|------|------|
...

**Total:** {count} video(s) registered."

### 3.2 Offer Next Steps

"**What next?**
[AA] Run Audio Analysis on a specific video
[PSB] Run full Pre-Storyboard Pipeline (AA + TR + VA + VC for all)
[X] Done — ingest only"
