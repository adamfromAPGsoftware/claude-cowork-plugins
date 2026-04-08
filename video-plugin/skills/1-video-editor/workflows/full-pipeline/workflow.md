---
name: full-pipeline
description: One-shot autonomous execution — clip through render with quality gates
web_bundle: true
---

# Full Pipeline Quick — One-Shot Autonomous Execution

> **Note:** For the full end-to-end pipeline including auto-ingest, analysis, and boundary detection, use `[FP]` (long-form-edit). This workflow is the quick-mode shortcut (`[FPQ]`) when AA/TR are already complete and you want to skip straight to clipping.

**Goal:** Run the entire video post-production pipeline autonomously from clipping through final render, with quality gates at each phase boundary. One command, fully sequenced, with self-healing on gate failures.

**Your Role:** In addition to your name, communication_style, and persona, you are the pipeline orchestrator. You chain each sub-workflow in sequence, passing outputs forward, and enforce quality gates between phases. On any gate failure, attempt self-heal once; if still fails, stop and report.

**Meta-Context:** This workflow replaces manual step-by-step execution. It assumes Video Ingest [VI], Audio Analysis [AA], Transcription [TR], and Visual Analysis [VA] have already completed (their JSON outputs must exist).

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Sequential Chaining**: Each phase completes before the next begins
- **Gate Enforcement**: Quality gates between phases — no silent continuation past failures
- **Self-Heal Once**: On gate failure, attempt automatic correction once; if still fails, HALT
- **Output Forwarding**: Each phase's output becomes the next phase's input

### Pipeline Phases

```
PHASE 1: PREREQUISITES CHECK
  Verify AA, TR, VA JSON files exist (Gate G1)
  │
PHASE 2: VIDEO CLIPPING [VC]
  Execute video-clipping/workflow.md
  Enhanced audio cleanup with speech quality filters (Gate G2)
  Intro-specific 150ms buffer (Gate G2b)
  │
PHASE 3: STORYBOARD [SB]
  Execute storyboard/workflow.md
  Intro visual pacing rule enforced (Gate G4)
  │
PHASE 4: ASSET PREREQUISITES
  Logo extraction from source material (Gate G5)
  │
PHASE 5: ASSET GENERATION (sequential)
  [BE] B-Roll Extraction — from storyboard Visual Asset Source Map
  [HM] Hera Motion Graphics — from storyboard MG briefs, using extracted logos
  B-roll content verification (Gate G6)
  │
PHASE 6: REMOTION EDIT [RE]
  Execute remotion-edit/workflow.md (all steps through render)
  Includes: scaffold → theme → segments → QA → content verify → render
```

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `output_folder`

### 2. Prerequisites Check (Gate G1)

Verify these 3 JSON files exist and are non-empty:

1. `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/audio-analysis.json`
2. `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/transcript.json`
3. `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/visual-analysis.json`

**If any missing:** HALT — "Gate G1 FAILED: Missing prerequisite files. Run [AA], [TR], and/or [VA] first."

### 3. Execute Pipeline

Run each phase sequentially. Between phases, report progress:

"**[FP] Phase {N}/{total}: {phase_name}**"

#### Phase 2 — Video Clipping

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping/workflow.md`

**Gate G2 check after step-02 (audio cleanup):**
- Verify speech quality filters were applied (min duration, min confidence, energy floor, isolated segment check)
- Verify intro content used 150ms buffer (not 250ms)
- If filters not applied → self-heal: re-run step-02 with explicit filter instructions

#### Phase 3 — Storyboard

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/storyboard/workflow.md`

**Gate G4 check after step-05 (timeline assembly):**
- Count intro MGs — require >= 4
- Count intro B-roll cuts — require >= 4
- Check max gap between intro visual breaks — require <= 6 seconds
- If fails → self-heal: flag specific deficiency and re-run step-05 with explicit pacing instructions

#### Phase 4 — Logo Extraction (Gate G5)

After storyboard approval, before asset generation:

1. Scan all MG briefs in the storyboard for logo references
2. Check `video-editor/branded-assets/` and project `public/` for existing logo files
3. For missing logos visible in source video → extract frame, crop logo, save as PNG
4. For missing logos not in video → flag as "MISSING — requires manual upload"
5. **If any logo flagged MISSING** → HALT and report. Do not proceed to MG generation without logos.

#### Phase 5a — B-Roll Extraction

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/broll-extraction/workflow.md`

Uses the Visual Asset Source Map from the approved storyboard.

#### Phase 5b — Hera Motion Graphics

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/hera-motion-graphics/workflow.md`

Uses MG briefs from the approved storyboard + extracted logos from Phase 4.

#### Gate G6 — B-Roll Content Verification

After both asset generation phases complete:
- Verify each B-roll clip file exists and is > 0 bytes
- If Gemini available: spot-check 1 frame per clip against storyboard description
- **Self-heal on mismatch**: check Visual Analysis JSON for alternative timestamps, re-extract
- **If file missing after self-heal** → HALT

#### Phase 6 — Remotion Edit

Execute `{project-root}/video-plugin/skills/1-video-editor/workflows/remotion-edit/workflow.md`

This runs the full Remotion pipeline including the new gates:
- step-01: preflight
- step-01b: B-roll verification
- step-02: scaffold
- step-03: theme
- step-04: segments (with transition template support)
- step-05: composition
- step-06: QA (18-point checklist)
- step-06b: content verification + final audio re-analysis
- step-07: render (user preview)

### 4. Pipeline Complete

"**[FP] Full Pipeline Complete**

Pipeline executed {phase_count} phases with {gate_count} quality gates.

Summary:
- Video Clipping: {status} — {keep_segments} keep segments, {reduction}% reduction
- Storyboard: {status} — {segment_count} segments, {mg_count} MGs, {broll_count} B-roll
- Logo Extraction: {status} — {logo_count} logos resolved
- B-Roll Extraction: {status} — {clip_count} clips extracted
- Hera Motion Graphics: {status} — {mg_count} MGs generated
- Remotion Edit: {status} — QA {qa_status}, Content Verify {cv_status}
- Render: {render_status}

Preview available in Remotion Studio."

---

## ERROR HANDLING

### Self-Heal Protocol

On any gate failure:
1. Log the failure with specifics (which gate, what failed, why)
2. Attempt ONE automatic correction based on the gate's self-heal instructions
3. Re-check the gate
4. If still fails → HALT with full diagnostic report

### HALT Protocol

When halting:
1. Report which phase and gate failed
2. Report what was attempted for self-heal
3. Report the current state of all outputs (what succeeded before the failure)
4. Suggest the specific manual action needed to unblock

**Master Rule:** Never silently continue past a gate failure. The pipeline must either self-heal or stop. Half-built videos waste more time than clear error reports.
