---
name: storyboard
description: Plan video production — segments, B-roll, motion graphics, captions, pacing
menu-code: SB
---

# [SB] Storyboard

**Goal:** Build a complete video production storyboard that plans every visual segment, B-roll placement, motion graphic brief, caption strategy, and pacing target — producing the single source of truth that the Remotion Edit workflow consumes.

**Role:** Video production planner. Expertise in visual pacing, segment design, B-roll strategy, and Remotion template selection. Collaborative partnership with the user.

---

## Mode Selection

"**Storyboard Workflow. How would you like to proceed?**

[C]reate — Build a new video production storyboard
[E]dit — Edit an existing storyboard
[V]alidate — Validate a storyboard against production standards"

---

## Create Flow

### Phase 1: Initialize

**Scope selection:** [I] Intro Only (15+ visual events/min, high density) | [F] Full Video (intro detailed + body selective)

**Discover input files (REQUIRED):**
- Clipped transcript (JSON with word-level timestamps)
- Visual analysis (JSON with scene types and B-roll opportunities)
- Audio analysis (JSON with classified regions)
- Script (from copywriter workflow)

**Load reference data (for long-form):**
- Long-form pacing rules (P1-P18)
- Inspiration compliance checklist
- Segment patterns (Patterns 1-9)
- Remotion hard rules
- Template library
- Caption style spec

### Phase 2: Production Brief

Summarize project context: format (long-form/short-form), duration, content type, visual style targets. Map script sections to transcript timestamps. Identify MG trigger points from script stage directions `[MG-A]`..`[MG-G]`.

### Phase 3: Speaker and B-Roll Map

Map speaker segments to A-roll (talking head, screen share, PiP). Identify B-roll insertion points from visual analysis. Build Visual Asset Source Map: for each visual overlay, specify type (video-extract, motion-graphic), source, timestamps, and description.

### Phase 4: Text Placement

Plan caption strategy: word-level sync from clipped transcript, burst styling, PiP-aware positioning. Plan chapter cards (long-form body only) at section transitions.

### Phase 5: Timeline Assembly

Assemble complete segment-by-segment timeline. Each segment specifies: timing, Remotion template, visual content, transitions, captions. Apply editing intensity split:
- **Intro:** Full decomposition — MGs, captions, jump-cut zooms, B-roll, branded templates (Patterns 1-7, 9)
- **Body:** Single passthrough clip (Pattern 8) with light overlays — chapter cards + concept MGs

### Phase 6: Pacing Validation

Validate against pacing rules:
- Intro: >= 4 MGs, >= 4 B-roll cuts, <= 6s max gap between visual breaks
- Overall visual event density targets
- Long-form body: 4-8 events/min
- Short-form: 7-10 events/min

### Phase 7: Review

Present storyboard for user review with segment count, MG count, B-roll count, pacing validation results. Allow edits, then mark as approved.

---

## Edit Flow

Load existing storyboard. Assess what needs changing. Apply edits while preserving timeline integrity. Re-validate pacing.

---

## Validate Flow

Load storyboard. Run full pacing validation. Check all MG briefs are complete. Verify Visual Asset Source Map completeness. Report pass/fail with specifics.
