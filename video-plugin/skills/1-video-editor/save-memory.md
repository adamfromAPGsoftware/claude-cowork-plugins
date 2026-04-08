---
name: save-memory
description: Save current session context to memory
menu-code: SM
---

# [SM] Save Memory

## Purpose

Persist current session progress to sidecar memory so the next session picks up where this one left off.

## Execution

### Step 1: Update `memories.md`

Read current `_bmad/_memory/bmad-apg-vid-1-video-editor-sidecar/memories.md` and update:

**Session History section** — Append:
```
### {today} — {project_slug or "standalone"}
- Pipeline stages completed: {list — e.g. "AA, TR, VA, VC for intro + body"}
- Output files: {key outputs — e.g. "audio-analysis.json, transcript.json, clipped-intro.mp4"}
- Status: {current state — e.g. "Ready for storyboard"}
- Notes: {any notable observations}
```

**Patterns & Preferences section** — Update only if new patterns were identified:
- Pacing observations (e.g. "intro needed 150ms buffer, body needed 300ms")
- Quality gate results (e.g. "Gate G2 passed on first attempt")
- Editing style feedback from user

**Pipeline Notes section** — Update only if pipeline behavior was notable:
- Performance observations (e.g. "Gemini VA at 1.0 FPS took 4 minutes for 30s intro")
- Tool-specific notes (e.g. "DeepGram filler_words=true caught 12 'um's in body")

### Step 2: Update `editing-preferences.md` (if applicable)

Only update with explicit user approval:
- New pacing rules discovered during editing
- Transition preferences established
- Format-specific approaches identified

### Step 3: Confirm

```
Memory saved.
- memories.md: session logged for {project_slug}
- Pipeline stage: {current stage}
{- editing-preferences.md: updated with {what} (only if updated)}
```
