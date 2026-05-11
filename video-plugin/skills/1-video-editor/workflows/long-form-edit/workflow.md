---
name: long-form-edit
description: Full production editing pipeline for long-form tutorial videos (16:9 landscape)
web_bundle: true
---

# Long-Form Edit Workflow

**Goal:** Take raw filmed footage (talking-head + screen recordings) and produce a fully edited long-form tutorial video with motion graphics, captions, jump-cut zooms, B-roll, and polished transitions — rendered via Remotion. The intro gets full segment decomposition; the body gets dead air removal only and plays as a single passthrough clip.

**Your Role:** In addition to your name, communication_style, and persona, you are a long-form video production specialist. You combine talking-head footage with screen share recordings, apply proven YouTube tutorial editing patterns (studied from top-performing inspiration videos), and produce professional tutorial content. The user provides raw footage and a script — you execute the edit with technical precision.

**Meta-Context:** This workflow handles everything specific to long-form editing — analysis, clipping, storyboard decomposition, and asset preparation. When all assets are ready, it hands off to the **Remotion Edit** workflow for scaffolding, code generation, QA, and rendering. This workflow does NOT duplicate any Remotion build logic.

**Status:** 5 steps: Init → Analysis → Clipping (+ VA) → Storyboard → Assets, then hands off to remotion-edit (11 steps: preflight → render).

---

## DROP AND GO

Put your 4K video in the project's `video-ingest/` folder and run `[FP]`. That's it.

**Path:** `{project_folder}/{project-slug}/video-editor/video-ingest/`

Step-01 will auto-detect the file, probe it, create a registry YAML with `content_type: full`, generate a 720p proxy, and proceed through the full pipeline. In AUTO mode, the entire chain runs without questions — from raw file to rendered MP4.

If you've already registered files via `[VI] Video Ingest` or have existing registry YAMLs in `raw/`, the auto-ingest is skipped and the pipeline works exactly as before.

---

## COLLAB MODE CHECKPOINTS

When running in Collab mode, the pipeline pauses at 3 checkpoints for review. Analysis, boundary detection, false start removal, and clipping are fully autonomous — the agent makes all decisions based on rules and only pauses when you need to see results.

| # | Checkpoint | Step | What You Can Review |
|---|-----------|------|-------------------|
| 1 | After clipping complete | step-03 section 8 | Clipped video files, durations, removal stats |
| 2 | After storyboard | step-04 end | Segment breakdown, MG briefs, pacing validation |
| 3 | After Remotion preview, before render | remotion step-07 | Remotion Studio preview of assembled video |

In AUTO mode, all checkpoints are auto-approved and you're notified only when the rendered MP4 is ready.

---

## RELATED WORKFLOWS

Understanding how the three editing workflows relate:

| Workflow | Scope | What It Owns |
|----------|-------|-------------|
| **long-form-edit** (this) | Long-form tutorials (16:9, 5-60+ min) | Inspiration analysis, long-form pacing rules, PiP patterns, section transition strategy, screen share editing, intro structure |
| **short-form-edit** | Short-form vertical (9:16, 15-60s) | Inspiration analysis, vertical pacing rules, vertical patterns (V1-V7), hook/CTA strategy, MG-first editing |
| **remotion-edit** | Remotion build engine (shared) | Project scaffolding, segment code generation (Patterns 1-9), theme.ts, Root.tsx composition, QA checklist, rendering, hard rules |

**Data flow:**
- `long-form-edit` produces an approved storyboard + asset list → feeds into `remotion-edit` for Remotion build
- `short-form-edit` produces an approved storyboard + asset list → feeds into `remotion-edit` for Remotion build
- `remotion-edit` consumes storyboards from either workflow and produces rendered `.mp4` files
- Both `long-form-edit` and `short-form-edit` have their own inspiration data, pacing rules, and format-specific patterns
- Shared templates (SubtleZoom, Caption, MotionGraphic, etc.) and shared patterns (Patterns 1-8) live in `remotion-edit`
- Long-form-specific templates (PiPSpeaker) live in the shared template library but are primarily used by this workflow
- The storyboard workflow (`storyboard/`) is shared and has guidance for both formats

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Pipeline Overview

```
step-01-init       → Discover files, auto-ingest from drop folder, load script, detect recording mode
step-02-analysis   → Audio analysis + Transcription + boundary VA + boundary detection
step-03-clipping   → Split (single-file) → Clip intro (150ms) + body (300ms) → Remap transcripts → Visual analysis on clipped videos
step-04-storyboard → Decompose intro into segments, body as passthrough
step-05-assets     → B-roll extraction, logo fetch, Hera MG generation, audio concat → remotion-edit handoff
    ↓
    Hand off to remotion-edit workflow (11 existing steps: preflight → render)
```

### Recording Mode Support

**Multi-file** (current pattern): Separate intro + body recordings → separate proxy YAMLs with `content_type: intro` and `content_type: main`. Each file analysed independently.

**Single-file** (new): One continuous recording → boundary detected by visual analysis (talking-head → screen-share transition), with transcript overlap as fallback. After detection, pipeline converges to same flow (two clipped files from step 3 onwards).

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file that is part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory — never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimisation allowed
- **State Tracking**: Document progress using session variables for tracking
- **Handoff Model**: Long-form-edit prepares storyboard + assets → remotion-edit builds and renders

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimise the sequence
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **COLLAB MODE:** halt at menus and wait for user input
- 🚀 **AUTO MODE:** make best-case assumptions at every decision point, auto-approve all checkpoints, and only notify the user when the entire workflow is complete
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Parallelization Model

The pipeline uses targeted parallelism where operations are provably independent. This reduces total pipeline time by ~26-45 minutes without changing outputs.

**Step 2 — Analysis (multi-file):** Intro and body branches run in parallel. Within each branch, audio analysis and transcription run concurrently, then refinement runs after both complete.

**Step 2 — Analysis (single-file):** Boundary VA runs in parallel with audio analysis + transcription. All three must complete before boundary detection.

**Step 3 — Clipping:** All 4 FFmpeg clip commands (intro-proxy, intro-raw, body-proxy, body-raw) run as parallel background processes. Both transcript remaps run in parallel. Per-clip audio extraction launches as background processes after clips complete (runs during VA + storyboard). Both Gemini VA calls (intro + body) run simultaneously.

**Step 4 — Storyboard:** Optional logo pre-fetch in background when tool names are known from MG markers.

**Step 5 — Assets:** Three-phase parallel execution:
- Phase 1: B-roll extractions + logo fetches + no-reference Hera MGs (all concurrent)
- Phase 2: Logo-dependent Hera MGs (after logos ready)
- Phase 3: Unified Hera polling loop for all submitted jobs
- Audio concat: verify-only (already done in step 3), fallback regenerate if missing

All background processes use `wait` with exit code checks. No orphaned processes on failure.

### Editing Intensity Split

- **Intro**: Full Remotion segment decomposition — MGs, captions, jump-cut zooms, B-roll, branded templates (Patterns 1-7, 9)
- **Body**: Clipping (dead air removal), played as single OffthreadVideo (Pattern 8) with light overlays — chapter cards + concept MGs at speaker return/explanation points (P18). No segment decomposition, no B-roll.

---

## KEY DATA FILES

### Long-Form Specific (this workflow)

| File | Purpose |
|------|---------|
| `data/long-form-pacing-rules.md` | 18 pacing rules for long-form tutorials (P1-P18) |
| `data/inspiration-compliance-checklist.md` | Non-pacing inspiration gates (transitions, MG usage, captions, PiP, audio) |
| `data/inspiration/videos.yaml` | 5 inspiration video manifest with categories + sample windows |
| `data/inspiration/mg-style-guide.md` | Long-form MG style guide — aggregated from all 5 per-video analyses |
| `data/inspiration/mg-analysis-schema.json` | JSON schema for per-video mg-analysis.json files |
| `data/inspiration/long-form-mg-analysis-prompt.md` | 3-pass Gemini MG analysis prompt (intro + body samples + density) |
| `data/inspiration/long-form-production-analysis-prompt.md` | 10-section Gemini production analysis prompt (two-pass: intro + full) |
| `data/inspiration/run-long-form-analysis.py` | Gemini analysis runner (production + MG passes) |
| `data/inspiration/generate-lf-mg-style-guide.py` | Script to aggregate mg-analysis.json files into mg-style-guide.md |
| `data/inspiration/extract-transcripts.py` | DeepGram Nova-3 transcript extraction |
| `data/inspiration/long-form-patterns.md` | Synthesized patterns across all 5 analyses (MG types, pacing, intro structure) |
| `data/inspiration/{folder}/mg-analysis.md` | Per-video MG analysis (merged from 3 passes) |
| `data/inspiration/{folder}/mg-analysis.json` | Per-video MG analysis (structured JSON) |
| `data/inspiration/{folder}/production-analysis.md` | Per-video production analysis (generated) |
| `data/inspiration/{folder}/transcript.json` | Per-video word-level transcript (generated) |

### Shared (in remotion-edit)

| File | Purpose |
|------|---------|
| `remotion-edit/data/segment-patterns.md` | Patterns 1-9 (incl. Pattern 9: PiP Speaker) |
| `remotion-edit/data/remotion-hard-rules.md` | 8 hard rules for all Remotion projects |
| `remotion-edit/data/caption-style-spec.md` | Caption burst styling and animation spec |
| `storyboard/data/template-library.md` | All Remotion templates (incl. PiPSpeaker) |
| `storyboard/data/pacing-rules.md` | Shared pacing validation rules |

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `output_folder`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### 2. Load Reference Data

Load the following data files (read completely before proceeding):
- `./data/long-form-pacing-rules.md` — long-form pacing enforcement rules
- `./data/inspiration/long-form-patterns.md` — synthesized inspiration patterns (if populated)
- `../hera-motion-graphics/steps-c/step-02-generate.md` — MG brief templates by type (Types A-G)

Also load shared reference data from sibling workflows:
- `../remotion-edit/data/segment-patterns.md` — segment code patterns (Patterns 1-9)
- `../remotion-edit/data/remotion-hard-rules.md` — Remotion hard rules
- `../storyboard/data/template-library.md` — available Remotion templates

### 3. Execution Mode Selection

Present the user with a mode selection:

"**How would you like to run this workflow?**

[A] **Auto** — I'll process the full pipeline end-to-end without stopping, making best-case decisions at every checkpoint. You'll be notified when all assets are ready and the remotion-edit handoff is complete. Fastest option.
[C] **Collab** — I'll work through each step with you, presenting results for review and waiting for your input at each checkpoint. Most control."

Set the session variable `{execution_mode}` to `auto` or `collab` based on user selection.

**If auto mode:** Inform the user: "Running in auto mode. I'll process the full long-form pipeline (init → analysis → clipping → storyboard → assets) and then hand off to remotion-edit. I'll notify you when the rendered MP4 is ready."

### 4. Runtime Pipeline Order

The long-form production pipeline runs in this order — the storyboard works with **actual clipped footage**, not script predictions:

1. **Script** — Copywriter writes script with MG stage directions `[MG-A]`..`[MG-G]`
2. **Film** — Record the video (actual delivery differs from script in timing and wording)
3. **Audio analysis + Transcription** — Extract word-level transcript and VAD data from filmed footage
4. **Clip** — Remove dead air, filler, gaps → produce clipped A-roll with precise timestamps
5. **Transcript remap** — Deterministically remap word timestamps to clipped timeline (pure math using keep-segments). Outputs `{content_type}-clipped-transcript.json`
6. **Storyboard** — Plan visual overlays (MGs, B-roll, PiP, captions) on top of the clipped footage using the **remapped** transcript
7. **Hera MG generation** — Generate motion graphics from storyboard briefs
8. **Remotion build** — Assemble everything using clipped transcript timestamps for caption sync

### 5. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
