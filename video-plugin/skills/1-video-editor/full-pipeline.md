---
name: full-pipeline
description: One-shot autonomous execution — clip through render with quality gates
menu-code: FP
---

# [FP] Full Pipeline Quick

**Goal:** Run the entire video post-production pipeline autonomously from clipping through final render, with quality gates at each phase boundary. One command, fully sequenced, with self-healing on gate failures.

**Prerequisite:** Video Ingest [VI], Audio Analysis [AA], Transcription [TR], and Visual Analysis [VA] must already be complete (their JSON outputs must exist).

> For the full end-to-end pipeline including auto-ingest and analysis, use [LF] Long-Form Edit instead.

---

## Pipeline Phases

```
PHASE 1: PREREQUISITES CHECK
  Verify AA, TR, VA JSON files exist (Gate G1)
PHASE 2: VIDEO CLIPPING [VC]
  Enhanced audio cleanup with speech quality filters (Gate G2)
  Intro-specific 150ms buffer (Gate G2b)
PHASE 3: STORYBOARD [SB]
  Intro visual pacing rule enforced (Gate G4)
PHASE 4: ASSET PREREQUISITES
  Logo extraction from source material (Gate G5)
PHASE 5: ASSET GENERATION (sequential)
  [BE] B-Roll Extraction + [HM] Hera Motion Graphics
  B-roll content verification (Gate G6)
PHASE 6: REMOTION EDIT [RE]
  Full Remotion pipeline: scaffold, theme, segments, QA, content verify, render
```

---

## Gate G1: Prerequisites Check

Verify 3 JSON files exist and are non-empty:
1. `analysis/{content-type}/audio-analysis.json`
2. `analysis/{content-type}/transcript.json`
3. `analysis/{content-type}/visual-analysis.json`

**If any missing:** HALT — "Gate G1 FAILED: Missing prerequisite files. Run [AA], [TR], and/or [VA] first."

---

## Phase 2: Video Clipping

Execute video-clipping capability.

**Gate G2 check after audio cleanup:**
- Verify speech quality filters applied (min duration, min confidence, energy floor, isolated segment check)
- Verify intro content used 150ms buffer (not 250ms)
- Self-heal: re-run with explicit filter instructions

---

## Phase 3: Storyboard

Execute storyboard capability.

**Gate G4 check after timeline assembly:**
- Intro MGs >= 4
- Intro B-roll cuts >= 4
- Max gap between intro visual breaks <= 6 seconds
- Self-heal: flag deficiency and re-run with explicit pacing instructions

---

## Phase 4: Logo Extraction (Gate G5)

1. Scan all MG briefs for logo references
2. Check `branded-assets/` and project `public/` for existing logos
3. Extract missing logos from source video frames
4. Flag logos not in video as "MISSING — requires manual upload"
5. **HALT if any logo flagged MISSING** — do not proceed to MG generation without logos

---

## Phase 5: Asset Generation

### 5a: B-Roll Extraction
Execute broll-extraction capability from Visual Asset Source Map.

### 5b: Hera Motion Graphics
Execute hera-motion-graphics capability from storyboard MG briefs + extracted logos.

### Gate G6: B-Roll Content Verification
- Verify each B-roll clip exists and is > 0 bytes
- Spot-check via Gemini if available
- Self-heal: check Visual Analysis JSON for alternative timestamps, re-extract
- **HALT if file missing after self-heal**

---

## Phase 6: Remotion Edit

Execute full remotion-edit capability (steps 01 through 07).

---

## Pipeline Complete

Report all phases with status, metrics, and gate results.

---

## Error Handling

### Self-Heal Protocol
1. Log failure with specifics (which gate, what failed, why)
2. Attempt ONE automatic correction
3. Re-check the gate
4. If still fails: HALT with full diagnostic report

### HALT Protocol
1. Report which phase and gate failed
2. Report self-heal attempt
3. Report current state of all outputs
4. Suggest specific manual action to unblock

**Master Rule:** Never silently continue past a gate failure. The pipeline must either self-heal or stop.
