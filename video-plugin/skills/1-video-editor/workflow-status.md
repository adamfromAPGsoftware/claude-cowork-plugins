---
name: workflow-status
description: Check status of in-progress video content
menu-code: WS
---

# [WS] Workflow Status

**Goal:** Check status of in-progress video content across the pipeline. Show which stage each video is at and surface any issues.

---

## Execution

### 1. Load Active Project

Load active project from `_bmad/ccs/active-project.yaml`. If no active project, list available projects.

### 2. Scan Video Registry

Read all YAML files in `{project_folder}/{project-slug}/video-editor/raw/`. For each registered video, check:

- **Ingest:** Registry YAML exists?
- **Audio Analysis:** `analysis/{content-type}/audio-analysis.json` exists?
- **Transcription:** `analysis/{content-type}/transcript.json` exists?
- **Visual Analysis:** `analysis/{content-type}/visual-analysis.json` exists?
- **Clipping:** Clipped video file exists in `clips/`?
- **Storyboard:** `storyboard/*-storyboard.md` exists?
- **B-Roll:** Files in `broll/`?
- **Motion Graphics:** Files in `motion-graphics/`?
- **Remotion Project:** Remotion project directory exists?
- **Render:** Rendered MP4 exists?

### 3. Present Status

"**Pipeline Status — Project: {project_title}**

| Video ID | Type | Ingest | AA | TR | VA | VC | SB | BE | HM | RE | Render |
|----------|------|--------|----|----|----|----|----|----|----|----|--------|
| {id} | {type} | {ok/--} | {ok/--} | ... | ... | ... | ... | ... | ... | ... | ... |

**Summary:**
- Videos registered: {count}
- Fully rendered: {count}
- In progress: {count} (next step: {suggestion})
- Blocked: {count} ({reason})"

### 4. Suggest Next Action

Based on pipeline state, recommend the most productive next action (e.g., "Run [AA] for intro-001" or "Run [PSB] to process all remaining videos").
