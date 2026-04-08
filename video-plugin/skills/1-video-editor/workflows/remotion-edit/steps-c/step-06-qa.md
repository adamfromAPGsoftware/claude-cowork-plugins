---
name: 'step-06-qa'
description: 'Run 18-point QA checklist and generate qa-report.md'

nextStepFile: './step-06b-content-verify.md'
dataFile: '../data/remotion-hard-rules.md'
---

# Step 6: QA — 18-Point Checklist

## STEP GOAL:

Run the complete 17-point QA checklist from the hard rules against all generated code files. Generate a `qa-report.md` documenting every check with pass/fail status and specific file/line references for any failures.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction unless failures found
- Load hard rules from {dataFile} for the 18-point checklist
- Check EVERY file in the project, not just Root.tsx
- Generate qa-report.md regardless of pass/fail

## MANDATORY SEQUENCE

### 1. Load Hard Rules

Load and read {dataFile} for the 16-point checklist.

### 2. Scan All Project Files

Read every `.tsx` and `.ts` file in the project `src/` directory.

### 3. Execute 16-Point QA Checklist

For each rule, scan ALL relevant files:

**Rule 1: OffthreadVideo muted**
- Scan every file for `<OffthreadVideo`
- Check each instance has `muted` prop
- Report: file, line number, pass/fail

**Rule 2: OffthreadVideo style**
- Every `<OffthreadVideo>` must have `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`
- Report: file, line number, pass/fail

**Rule 3: OffthreadVideo and Audio pauseWhenBuffering**
- Every `<OffthreadVideo>` and `<Audio>` must have `pauseWhenBuffering`
- Report: file, line number, pass/fail

**Rule 4: Single Audio element**
- Count ALL `<Audio` occurrences across ALL files
- Must be exactly 1 (in Root.tsx only)
- Report: count, files found in

**Rule 5: No Img tags**
- Scan all files for `<Img` or `<img`
- Must be zero occurrences
- Report: any occurrences found

**Rule 6: Zero frame gaps**
- Validate sequence chain: each segment's end frame = next segment's start frame
- Report: any gaps found with frame numbers

**Rule 7: Sequence premountFor**
- Every `<Sequence` must have `premountFor={30}`
- Report: file, line number, pass/fail

**Rule 8: Sequence name prop**
- Every `<Sequence` must have a descriptive `name` prop
- Report: file, line number, pass/fail

**Rule 9: No Audio in segments**
- Seg{NN}.tsx files must NOT contain `<Audio`
- Report: any violations

**Rule 10: All imports valid**
- Every imported component must exist as a file
- Report: any missing imports

**Rule 11: Theme completeness + source video match**
- SEGMENTS array count matches number of Seg{NN}.tsx files
- PROJECT constants all present (fps, width, height, totalDurationInFrames, compositionId, audioSource)
- Run ffprobe on the main source video in `public/` and verify PROJECT.width, PROJECT.height, and PROJECT.fps match exactly
- Report: any missing entries, any resolution/FPS mismatches

**Rule 12: B-roll video only + correct template assignment**
- No `<Img>`, no KenBurns patterns, no static image references in B-roll segments
- All video-extract and motion-graphic segments use `<OffthreadVideo>` with video files
- `video-extract` segments MUST use `BRollOverlay` (VHS effect for real b-roll)
- `motion-graphic` segments MUST use `MotionGraphic` (clean playback — NO VHS effect)
- Motion graphics should never have the BRollOverlay treatment
- Report: any violations (wrong template assignment, Img usage)

**Rule 13: staticFile() for all public asset paths**
- Parse theme.ts for `sourceFile:` and `audioSource:` values
- Every value must be wrapped in `staticFile()` — no bare path strings like `'/file.mp4'`
- Report: any bare path strings found

**Rule 14: startFrom on speaker OffthreadVideo**
- For every speaker/CTA segment (Seg{NN}.tsx) that uses the main video source, check `<OffthreadVideo>` has `startFrom={seg.startFrame}`
- B-roll and motion-graphic segments are exempt
- Report: file, line number, pass/fail

**Rule 15: OffthreadVideo import source**
- Grep all `.tsx` files for `from '@remotion/media-utils'`
- Must be zero occurrences of OffthreadVideo imported from `@remotion/media-utils`
- Report: any violations with file/line

**Rule 16: No require() in branded templates**
- Grep all branded template files for `require(`
- Must be zero occurrences — all brand asset paths must use `staticFile()`
- Report: any violations with file/line

**Rule 18: Transitions only between visual type changes**
**Note:** If the user reports Remotion Studio preview FPS drops or freezing at segment boundaries, suggest running with `logLevel="trace"` on the `<Composition>` element to diagnose buffering events. Also verify `@remotion/preload` is installed and `preloadVideo(PROJECT.sourceFile)` is called in the Main component's `useEffect`.


- Walk through the SEGMENTS array in theme.ts sequentially
- For each pair of adjacent segments, check their `visualType`
- If both are `speaker` (regardless of template — SubtleZoom, KineticCaption, bare), verify neither segment component has any fade/opacity transition logic
- Speaker segments should render the OffthreadVideo at full opacity with no animated opacity wrapper
- Report: any consecutive speaker pairs that have unintended transitions

**Rule 17: Caption timing vs transcript word timestamps**
- Load the transcript word-level timestamps (from audio analysis output)
- Load the clipping offset (from video clipping output)
- For each segment with `captionText` in theme.ts:
  1. Look up the first word of `captionText` in the transcript
  2. Convert transcript time to frame: `frame = Math.round((word_time - clip_offset) * fps)`
  3. Verify segment `startFrame` is within ±15 frames of the first spoken word
  4. Verify segment `startFrame + durationInFrames` extends past the last spoken word
- Report: segment ID, expected frame from transcript, actual startFrame, delta

### 4. Generate QA Report

Write `qa-report.md` to the project directory:

```markdown
# QA Report — {composition-name}

**Date:** {date}
**Overall Status:** {PASS / FAIL}

## 16-Point Checklist

| # | Rule | Status | Details |
|---|------|--------|---------|
| 1 | OffthreadVideo muted | {PASS/FAIL} | {count checked, failures} |
| 2 | OffthreadVideo style | {PASS/FAIL} | {count checked, failures} |
| 3 | pauseWhenBuffering | {PASS/FAIL} | {count checked, failures} |
| 4 | Single Audio | {PASS/FAIL} | {count found} |
| 5 | No Img tags | {PASS/FAIL} | {count found} |
| 6 | Zero frame gaps | {PASS/FAIL} | {gaps found} |
| 7 | Sequence premountFor | {PASS/FAIL} | {count checked, failures} |
| 8 | Sequence name prop | {PASS/FAIL} | {count checked, failures} |
| 9 | No Audio in segments | {PASS/FAIL} | {violations} |
| 10 | All imports valid | {PASS/FAIL} | {missing imports} |
| 11 | Theme completeness | {PASS/FAIL} | {missing entries} |
| 12 | B-roll video only | {PASS/FAIL} | {violations} |
| 13 | staticFile() paths | {PASS/FAIL} | {bare paths found} |
| 14 | startFrom on speaker | {PASS/FAIL} | {count checked, failures} |
| 15 | OffthreadVideo import | {PASS/FAIL} | {violations} |
| 16 | No require() in branded | {PASS/FAIL} | {violations} |
| 17 | Caption timing vs transcript | {PASS/FAIL} | {segments checked, delta details} |
| 18 | Transitions only on type change | {PASS/FAIL} | {consecutive speaker pairs checked} |

## Failures

{Detailed findings for each failure with file path and line number}

## Summary

- Checks passed: {pass_count}/18
- Checks failed: {fail_count}/18
```

### 5. Handle Results

**If all 16 checks PASS:**
"**QA PASSED — All 18 rules verified**

qa-report.md saved to {project_path}/

Proceeding to render..."

Auto-proceed: load, read entire file, then execute {nextStepFile}.

**If any checks FAIL:**
"**QA FAILED — {fail_count} rule(s) violated**

{List each failure with file:line reference}

**[F]ix** — Auto-fix all violations
**[X] Exit** — Save QA report and stop

#### Menu Handling Logic:
- IF F: Fix all violations, re-run QA, if all pass then proceed to {nextStepFile}
- IF X: Save report and end workflow

#### EXECUTION RULES:
- ALWAYS halt and wait for user input if failures found"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All 18 rules checked across ALL project files
- qa-report.md generated with specific findings
- All failures identified with file/line references
- Violations fixed before proceeding to render

### FAILURE:

- Skipping any of the 18 checks
- Not scanning ALL files (only checking Root.tsx)
- Proceeding to render with unresolved failures
- Not generating qa-report.md
