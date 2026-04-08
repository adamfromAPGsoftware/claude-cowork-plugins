---
name: 'step-04-segments'
description: 'Generate Seg{NN}.tsx per timeline row, verify muted and pauseWhenBuffering props'

nextStepFile: './step-05-composition.md'
dataFile: '../data/segment-patterns.md'
captionStyleFile: '../data/caption-style-spec.md'
---

# Step 4: Generate Segment Components

## STEP GOAL:

Generate one React component file (`Seg{NN}.tsx`) for each segment in the master timeline, using the segment patterns from the data file. Every `<OffthreadVideo>` MUST have `muted` and `pauseWhenBuffering` props.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction
- Load segment patterns from {dataFile} for code generation templates
- Load caption style spec from {captionStyleFile} — this is the ONLY caption style permitted
- EVERY `<OffthreadVideo>` must have: `muted`, `pauseWhenBuffering`, `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`
- ALL B-roll is video — NEVER use `<Img>` or static images
- Component names follow: `Seg01`, `Seg02`, etc.
- CAPTION RULE: NEVER add Caption to motion-graphic segments (visualType: 'motion-graphic'). Only speaker and b-roll segments may have captions.
- CAPTION RULE: Always pass `highlight={seg.captionHighlight}` alongside `text={seg.captionText!}` — this drives the orange accent word.
- CAPTION TIMING RULE: Before writing any segment with `captionText`, verify the `captionFrame` value in theme.ts was derived from VAD two-pass calibration (see {captionStyleFile} Timing Methodology). If the storyboard notes say 'transcript-only, VAD not applied', flag this segment in a WARNING comment in the generated TSX and do not silently accept the approximate value.

## MANDATORY SEQUENCE

### 0. Check for VideoRenderer Mode

If `VideoRenderer.tsx` exists in `{project_path}/src/` (copied during scaffold):
- **Skip SegXX.tsx generation entirely** — the VideoRenderer reads SEGMENTS from theme.ts and dispatches to the correct template component automatically
- Verify that all SEGMENTS entries in theme.ts have the required fields for their `visualType` (see VideoRenderer.tsx Segment type)
- Auto-proceed to step 05

If VideoRenderer.tsx is NOT present, proceed with legacy per-segment generation below.

### 1. Load Segment Patterns

Load and read {dataFile} for the 6 segment generation patterns:
1. Speaker segment (main video)
2. B-roll overlay segment
3. Motion graphic segment
4. Chapter card segment
5. CTA segment
6. Speaker with SubtleZoom segment

### 2. Generate Components

For each segment in the SEGMENTS array from theme.ts:

1. Determine the visual type → select the matching pattern from {dataFile}
2. Import the appropriate template component — **critical distinction:**
   - `video-extract` → `BRollOverlay` (VHS desaturation + retro overlay)
   - `motion-graphic` → `MotionGraphic` (clean, full-color playback — NO VHS effect)
   - `speaker` → `SubtleZoom` or `KineticCaption`
   - `branded-template` → `UpworkProfile`, `AgencyBrand`, etc.
   - `transition` → `WhiteFlash` (full-screen overlay at section boundaries)
3. Generate the component code

**Transition Segments:**

For segments with `visualType: transition`:
- Import and use the `WhiteFlash` template from `./WhiteFlash.tsx`
- The WhiteFlash renders as an `AbsoluteFill` overlay ABOVE adjacent visual segments
- Implement as a separate `<Sequence>` that overlaps the boundary segments (last 15 frames of previous + first 15 frames of next)
- The transition segment does NOT replace adjacent segments — it layers on top
- No `<OffthreadVideo>` in transition segments — they are pure React animation
- No captions on transition segments
4. **VALIDATE** before writing:
   - Every `<OffthreadVideo>` has `muted` prop
   - Every `<OffthreadVideo>` has `pauseWhenBuffering` prop
   - Every `<OffthreadVideo>` has `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`
   - No `<Img>` tags anywhere
   - No `<Audio>` tags (audio lives in Root.tsx only)

5. Write to `{project_path}/src/Seg{NN}.tsx`

### 3. Self-Validate Generated Code

After generating ALL segment files, scan each one:

**Mandatory checks per file:**
- [ ] `muted` prop on every `<OffthreadVideo>`
- [ ] `pauseWhenBuffering` prop on every `<OffthreadVideo>`
- [ ] Correct `style` prop on every `<OffthreadVideo>`
- [ ] No `<Img>` tags
- [ ] No `<Audio>` tags
- [ ] Imports are correct
- [ ] Props match SEGMENTS entry
- [ ] Caption segments: `captionFrame` is VAD-calibrated (storyboard notes do NOT say 'transcript-only'); if they do, insert `{/* WARNING: captionFrame is transcript-only — re-calibrate with VAD */}` above the Caption component
- [ ] No `backgroundColor` or `background` prop passed to any Caption component — spec mandates no background

**If any violation found:** Fix immediately before proceeding.

### 4. Auto-Proceed

"**Segment Components Generated**

- Total segments: {count}
- Files created: Seg01.tsx through Seg{NN}.tsx
- Validation: All {count} segments pass hard rules

**Segment Breakdown:**
| Type | Count |
|------|-------|
| speaker | {count} |
| broll | {count} |
| motion-graphic | {count} |
| chapter-card | {count} |
| cta | {count} |

Proceeding to composition assembly..."

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- One Seg{NN}.tsx file per master timeline segment
- All `<OffthreadVideo>` have muted + pauseWhenBuffering + correct style
- No `<Img>` tags anywhere
- No `<Audio>` tags in segment files
- All imports and props correct

### FAILURE:

- Missing `muted` prop on any `<OffthreadVideo>`
- Missing `pauseWhenBuffering` on any `<OffthreadVideo>`
- Using `<Img>` instead of `<OffthreadVideo>` for visual assets
- Including `<Audio>` in a segment file
- Not self-validating generated code

**Master Rule:** EVERY `<OffthreadVideo>` MUST have `muted` and `pauseWhenBuffering`. No exceptions.
