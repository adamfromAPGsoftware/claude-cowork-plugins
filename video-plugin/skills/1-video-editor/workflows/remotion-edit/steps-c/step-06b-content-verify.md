---
name: 'step-06b-content-verify'
description: 'Post-QA content verification + final audio re-analysis before render'

nextStepFile: './step-07-render.md'
---

# Step 06b: Content Verification & Final Audio Re-Analysis

## STEP GOAL:

Post-QA automated checks + final audio verification before rendering. Self-healing: attempt automatic correction on failure. This is the last gate before the video goes to render.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction unless a gate fails
- Intro checks are BLOCKING — body checks are WARNINGS
- Self-heal once on failure; if still fails, stop and report

## MANDATORY SEQUENCE

### 1. Intro Visual Pacing Verification

- Count all non-speaker segments in intro sections of the master timeline
- Verify minimum 4 motion-graphic segments in intro
- Verify minimum 4 video-extract (B-roll) segments in intro
- Calculate time gaps between visual breaks — flag any gap > 6 seconds
- **Self-heal**: If insufficient visuals in intro, abort and flag: "Storyboard needs re-run with intro pacing rules applied"

Report:
```
Intro Visual Pacing:
- MGs in intro: {count} (min 4)
- B-roll cuts in intro: {count} (min 4)
- Max gap between visuals: {seconds}s (max 6s)
- Status: PASS / FAIL
```

### 2. Motion Graphic Source Files

For each segment with `visualType: motion-graphic`:
- Verify `sourceFile` exists in `public/` and is > 0 bytes
- Check MG clip duration >= segment `durationInFrames` at project fps
- **Self-heal**: If MG file missing, flag: "Hera MG generation needed for {asset_ref}"

### 3. Segment Pacing Check

- Flag speaker segments > 20 seconds without visual break (body sections) → WARN
- Flag speaker segments > 6 seconds without visual break (intro sections) → BLOCK
- A "visual break" is any non-speaker segment adjacent in the timeline

### 4. Audio Duration Match

- Verify `theme.ts` `totalDurationInFrames` matches actual audio file duration ±30 frames
- **Self-heal**: If mismatch, update `totalDurationInFrames` in theme.ts and adjust final segment's `durationInFrames` accordingly

### 5. Post-Clip Audio Verification (Critical for Intro)

Run audio analysis (VAD classification) on the FINAL concatenated audio file:

**For intro portion** (0 to intro end timestamp):
- Flag any non-speech region > 150ms that wasn't removed
- Flag any low-confidence (< 0.75) speech region that was kept
- Flag any breath/cough/noise > 100ms between speech segments
- Tolerance: 150ms for intro

**For body portion** (intro end to audio end):
- Flag any non-speech region > 500ms (more lenient)
- Tolerance: 250ms for body

**Self-heal**: If intro audio artifacts found:
1. Re-run audio cleanup with intro-specific filters
2. Re-concatenate audio
3. Update theme.ts with new audio duration
4. Re-verify

### 6. Transcript Spot-Check

- Compare transcript word count against audio duration — flag if ratio is outside 2-4 words/second
- Verify no silence gaps > 1 second exist within the final audio that weren't in the clip plan
- This is a sanity check — WARN only, do not block

### 7. Generate Content Verification Report

Append all results to qa-report.md:

```markdown
## Content Verification

### Intro Visual Pacing
- MGs in intro: {count}/4 minimum — {PASS/FAIL}
- B-roll in intro: {count}/4 minimum — {PASS/FAIL}
- Max visual gap: {seconds}s — {PASS/FAIL} (max 6s)

### Motion Graphic Files
- {count}/{total} MG files verified — {PASS/FAIL}
- Missing: {list or 'none'}

### Segment Pacing
- Intro max speaker run: {seconds}s — {PASS/FAIL} (max 6s)
- Body max speaker run: {seconds}s — {PASS/WARN} (max 20s)

### Audio Duration
- theme.ts: {frames} frames | Audio: {frames} frames — {PASS/FAIL} (±30 tolerance)

### Post-Clip Audio (Intro)
- Non-speech regions > 150ms: {count} — {PASS/FAIL}
- Low-confidence speech kept: {count} — {PASS/FAIL}
- Breath/noise > 100ms: {count} — {PASS/FAIL}

### Post-Clip Audio (Body)
- Non-speech regions > 500ms: {count} — {PASS/WARN}

### Transcript Spot-Check
- Words/second ratio: {ratio} — {PASS/WARN} (expected 2-4)
- Silence gaps > 1s: {count} — {PASS/WARN}
```

### 8. Gate Decision

- **All intro checks PASS** (or self-healed) → auto-proceed to render
- **Any intro check FAIL after self-heal** → HALT and report: "Content verification failed. Fix required before render."
- **Body warnings only** → WARN and proceed

"**Content Verification Complete**

- Intro pacing: {PASS/FAIL}
- MG files: {PASS/FAIL}
- Audio quality: {PASS/FAIL}
- Body pacing: {PASS/WARN}

{Proceeding to render... | BLOCKED — see report above}"

If PASS: Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All 6 verification checks executed
- Self-heal attempted on fixable failures
- Report appended to qa-report.md with specific pass/fail per check
- Intro checks block render on failure; body checks warn only
- Auto-proceeded to render on all-pass

### FAILURE:

- Skipping any verification check
- Proceeding to render with a failing intro check
- Not attempting self-heal before blocking
- Not logging results to qa-report.md
- Treating body warnings as blockers (too conservative)
- Treating intro failures as warnings (too permissive)
