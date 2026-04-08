---
name: init
description: First-run setup for Video Editor
menu-code: INIT
---

# First-Run Setup for Video Editor

Welcome! Setting up your video production workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-vid-1-video-editor-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `memories.md` — session history, user preferences, pipeline notes
- `instructions.md` — operational protocols and boundaries
- `editing-preferences.md` — pacing rules, transition preferences, visual style per format
- `branded-assets/` — logos, profile images, brand graphics

## Setup Questions

1. **Primary content format** — What do you primarily edit? (e.g. `talking-head`, `screen-recording`, `podcast`, `mixed`)
2. **Proxy workflow** — Do you film in 4K and want automatic 720p proxy generation? (yes/no, default: yes)
3. **Default output folder** — Where should rendered videos be saved?

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-vid-1-video-editor-sidecar/memories.md`

```markdown
# Video Editor — Memories

## User Profile
- Primary user: {user_name}
- Primary format: {confirmed-format}
- Skill level: Understands video production concepts, expects autonomous execution

## Session History
_No sessions recorded yet._

## Patterns & Preferences
_No patterns identified yet._

## Pipeline Notes
_No pipeline observations recorded yet._
```

### `{project-root}/_bmad/_memory/bmad-apg-vid-1-video-editor-sidecar/instructions.md`

```markdown
# Video Editor — Instructions

## Protocols
- Always load editing-preferences.md before any editing or analysis task
- Use proxy files for ALL API requests, transcription, audio analysis, and visual analysis — never the raw file
- Track proxy-to-raw file mapping for every ingested video
- Process main video body FIRST, then intro (intro may depend on B-roll extracted from body)
- Reference memories.md for user preferences and session continuity

## Boundaries
- Only read/write files within this sidecar folder
- Do not modify editing-preferences.md without explicit user approval
- Pipeline outputs go to the active project folder or standalone output folder, not the sidecar

## Startup Behavior
1. Load memories.md for user context
2. Load editing-preferences.md for format-specific rules
3. Check for any in-progress pipeline work
4. Greet user with pipeline status if applicable
5. Present menu
```

### `{project-root}/_bmad/_memory/bmad-apg-vid-1-video-editor-sidecar/editing-preferences.md`

```markdown
# Video Editor — Editing Preferences

## Proxy Workflow
- Always use proxy files for API calls (DeepGram, Gemini Pro)
- Apply final cuts to raw (full-resolution) files
- Track proxy <-> raw file mapping per project

## Multi-File Ingest
- Projects may contain multiple video files (body + intro)
- Process main body first — it's the primary content and B-roll source
- Process intro after body — intro may incorporate extracted B-roll
- Final assembly combines all files in correct order

## Pacing Rules
_No pacing preferences configured yet._

## Transition Preferences
_No transition preferences configured yet._

## Visual Style
_No visual style preferences configured yet._

## Format-Specific Approaches
_Populated as editing sessions establish patterns._
```

## Ready

Setup complete! Ready to process your first video.
