---
name: 'step-05-timeline-assembly'
description: 'Build master timeline with every segment: visual, speech, templates, B-roll, captions'

nextStepFile: './step-06-pacing-validation.md'
outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
---

# Step 5: Timeline Assembly

## STEP GOAL:

Build the master timeline — the core storyboard artifact. Every segment in the final video gets a row with: time range, visual type, Remotion template, props, B-roll reference, caption text, and caption position. This is the definitive build plan for Remotion Edit.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is a DETERMINISTIC step — assemble timeline from prior steps, no creative decisions
- No user interaction — auto-proceed after building
- ZERO frame gaps between segments — every millisecond must be accounted for
- Every segment must reference a specific Remotion template

## EXECUTION PROTOCOLS:

- 🎯 Assemble master timeline from all prior step outputs with ZERO gaps
- 💾 Append complete timeline to {outputFile}, auto-proceed to pacing validation
- 📖 Verify caption timing against word-level transcript data (within ±15 frame tolerance)
- 🚫 No user interaction — deterministic assembly only

## CONTEXT BOUNDARIES:

- Available context: Production brief, speaker position map, visual asset source map, text placement strategy
- Focus: Timeline assembly with ZERO gaps; transcript-verified captions
- Limits: No creative decisions — assemble only from existing plans in prior steps
- Dependencies: All prior steps (01–04) must be complete before assembly

## MANDATORY SEQUENCE

### 1. Gather All Inputs

From the storyboard document built so far, collect:
- Production brief (sections, durations, B-roll candidates)
- Speaker position map (where speaker is at each time)
- B-Roll source map (all B-roll with IDs and source info)
- Text placement strategy (templates per section, caption positions)

### 2. Build Timeline Rows

For each section, break into individual timeline segments. A segment is the smallest unit of visual change in the video.

**Segment types (exactly 7):**
- `speaker` — Speaker on camera (main video footage)
- `video-extract` — Extracted clip from the main video (screen recording, tool demo, etc.)
- `motion-graphic` — Hera Video API generated clip
- `branded-template` — Constant branded Remotion component (UpworkProfile, AgencyBrand)
- `chapter-card` — Full-screen text transition
- `cta` — Call-to-action overlay
- `transition` — Visual transition overlay (e.g., WhiteFlash at section boundaries)

**CRITICAL:** Every `video-extract` segment MUST reference an entry in the Visual Asset Source Map that was confirmed by the main video's visual analysis. Every `motion-graphic` segment MUST reference an entry in the Visual Asset Source Map. Every `branded-template` segment MUST reference a known branded template name. Every `transition` segment MUST specify a template (default: `WhiteFlash`).

**TWO-TIMELINE DISTINCTION:**
- The master timeline uses the **target segment's** timestamps (e.g., the intro's 00:00 → 02:30)
- The `source_file` for `video-extract` segments points to the **extracted B-roll clip** (once extracted via [BE]), NOT the main video directly
- The `asset_ref` links to the Visual Asset Source Map entry, which contains the **main video timestamps** for extraction

For each segment, populate:

| Field | Description |
|-------|-------------|
| `segment_id` | Sequential: `seg-001`, `seg-002`, etc. |
| `start_time` | Absolute start time in the **target segment's** timeline (HH:MM:SS.mmm) |
| `end_time` | Absolute end time in the **target segment's** timeline (HH:MM:SS.mmm) |
| `duration_frames` | Duration in frames at 30fps |
| `visual_type` | speaker / video-extract / motion-graphic / branded-template / chapter-card / cta / transition |
| `template` | Remotion template name (from template library) |
| `source_file` | Path to video/clip file for this segment (target video for `speaker`, extracted clip for `video-extract`, generated clip for `motion-graphic`, `branded-assets` for branded templates; `null` for `showcase-mg`) |
| `asset_ref` | Visual Asset Source Map ID (required for video-extract, motion-graphic, showcase-mg, branded-template) |
| `caption_text` | Caption/overlay text (if applicable) |
| `caption_position` | top-left / top-right / bottom-left / bottom-right / bottom-center |
| `section` | Which production brief section this belongs to |
| `template_category` | For `showcase-mg` and `motion-graphic` segments: the showcase component name (e.g., `NumberCountUp`) or `hera-interface`. Used by the Reuse Cap Validator. |
| `notes` | Special instructions for Remotion Edit. **For every `showcase-mg` and `motion-graphic` segment, `notes` MUST include a `symbolic_alignment:` line** — one sentence explaining how the visual depicted in this segment symbolically matches what the speaker is saying at this timestamp. |

### 3. Caption Timing — Two-Pass VAD Calibration (MANDATORY)

**CRITICAL:** Every caption segment MUST go through two-pass timing calibration before its frame values are written to the storyboard. Never derive `captionFrame` from the transcript alone — the transcript gives a rough window; the audio analysis VAD gives the precise acoustic onset. See `remotion-edit/data/caption-style-spec.md` for the canonical methodology.

**Required inputs:**
- Transcript word-level JSON (from [TR] Transcription workflow) — word timestamps to nearest ~10ms
- Audio analysis `classified_regions` JSON (from [AA] Audio Analysis workflow) — VAD boundaries at 20ms resolution
- Clipping offset from the video-clipping workflow (seconds trimmed from the source start)

**Two-Pass Process:**

**Pass 1 — Transcript lookup (rough window):**
1. Locate the caption phrase in the word-level transcript
2. Record `phrase_start` (first word start) and `phrase_end` (last word end)
3. Define a search window: `[phrase_start − 0.5s, phrase_end + 0.5s]`

**Pass 2 — Audio analysis VAD refinement (precise onset/offset):**
1. Load `classified_regions` from the audio analysis JSON
2. Within the search window, find the `SPEECH` region containing the key word
3. Set `vad_onset` = that region's `start` timestamp
4. Set `vad_offset` = that region's `end` timestamp
5. Compute: `captionFrame = round((vad_onset − clip_offset) × fps)`
6. Compute: `segment_end_frame = round((vad_offset − clip_offset) × fps) + 3`

**Conflict resolution:** If transcript and VAD disagree by >3 frames, always defer to VAD.

**Example:**
- Transcript: "workforce" at 10.48s; clip_offset = 0.484s → rough frame ≈ 300
- VAD `classified_regions` shows SPEECH onset at 10.44s in that window
- `captionFrame = round((10.44 − 0.484) × 30) = frame 299`
- Segment end = round((VAD_offset − 0.484) × 30) + 3

**If audio analysis is unavailable:** Fall back to transcript timestamps (±15 frame tolerance) AND mark the segment with `notes: 'timing: transcript-only, VAD not applied'` so it can be re-calibrated.

**Segment boundary rules:**
- The segment's `start_time` MUST be at or before `captionFrame`
- The segment's `end_time` MUST be at or after `segment_end_frame`
- If a boundary needs adjusting, adjust it — do not leave captions out of sync

This eliminates the failure where captions appear before the speaker says the words, or fade out mid-word.

### 4. Intro Visual Pacing Rule

The intro MUST maintain high visual energy to retain viewer attention.

**Timing constraints:**
- Maximum **6 seconds** between visual breaks (B-roll cut or motion graphic)
- Target **4 seconds** between visual breaks (preferred)
- A "visual break" is any non-speaker segment: `video-extract`, `motion-graphic`, or `branded-template`

**Minimum visual density (density-based formula):**
- `min_visual_breaks = ceil(intro_duration_seconds / 10)` — at least 1 visual break per 10s
- `min_mgs = ceil(min_visual_breaks * 0.6)` — at least 60% of visual breaks should be MGs
- Remaining visual breaks can be B-roll cuts
- Examples: 90s intro → min 9 visual breaks (≥6 MGs, ≥3 B-roll); 45s intro → min 5 visual breaks (≥3 MGs, ≥2 B-roll)
- These are MINIMUMS — more is better for pacing
- Total visual breaks should give approximately 1 every 4-6 seconds across intro duration

**MG brief requirements:**
- Each MG brief MUST include a clear, specific creative prompt
- If the MG requires logos (company, product, platform), note them in the brief as extraction prerequisites
- Reference the script/transcript section the MG supports

**B-roll cut selection:**
- B-roll cuts from main video should show relevant screen recordings, demos, or product shots
- Each cut should visually reinforce the speaker's point at that moment in the intro
- Prefer cuts that show action (typing, clicking, dashboards updating) over static screens

**Body sections:**
- Body sections have more flexibility — visual breaks every 10-20 seconds acceptable
- At least 2 MGs should appear in body sections for technical explanations

**PiP Decision Rules (Long-Form):**
When assembling timeline rows for long-form content with screen share segments:
- **Concept/agenda slides:** Include PiP speaker overlay (30–40% width, `position: right-center`)
- **Deep technical screen share:** Either no PiP or small PiP (≤16% width, `position: bottom-right`) — maximize UI legibility
- **Speaker delivering transition between sections:** Full-frame speaker (no PiP, no screen share)
- PiP position MUST NOT overlap caption text — if captions are bottom-center, place PiP bottom-right or top-right

**Motion Graphic Placement at Narration Triggers (Long-Form):**
When the storyboard includes `[MG-X]` stage directions from the script or identified narration trigger points:
- Map each trigger to the appropriate MG type (A–G) from the template library's MG Type mapping table
- Place the MG segment at the transcript timestamp where the trigger narration occurs
- Ensure MG duration matches the type's standard duration (e.g., Type A: 2–4s, Type B: 3–5s)
- The speaker's voiceover continues over the MG — audio never breaks

**MG Spacing Validation (P12):**
After placing all MG segments in the intro timeline:
1. Calculate gap between each MG segment's end time and the next MG segment's start time
2. **FAIL** if any intro MG gap > 8s — add an MG in the gap
3. **FAIL** if any consecutive MG gap < 2s — shift or merge MGs to create breathing room
4. **WARN** if > 50% of MGs are clustered in a single intro section (e.g., all 4 in the hook)
5. Target: 2–8s spacing between MGs, with 6s as the ideal average gap

**Validation:** After building intro timeline rows, count visual breaks and measure gaps. If any gap exceeds 6 seconds or asset counts are below minimums, redistribute segments before proceeding.

### 4a. Reuse Cap Validation

After the intro timeline rows are built, scan all `showcase-mg` and `motion-graphic` segments and tally `template_category` usage:

1. Build a count map: `{ ComponentName: count }` for intro segments only.
2. **FAIL** if any `template_category` appears more than **2 times** in the intro (exception: ROI running-total `NumberCountUp` / `ROICalculator` used for a continuous chapter-by-chapter counter).
3. **FAIL** if any `template_category` appears more than **3 times** across the full video (same exception applies).
4. **FAIL** if two MG segments separated only by one speaker segment share the same `template_category` — the viewer sees the same graphic twice in rapid succession.
5. **FAIL** if any `motion-graphic` segment does not have `hera: true` in its Visual Asset Source Map entry.
6. **FAIL** if total `hera: true` segments in the intro exceeds **3**.

For each FAIL: identify the over-used template, demote the lowest-priority instance to the next showcase candidate from the template library's mapping table, and update `template_category` and `template` accordingly.

### 4b. Symbolic Alignment Validation

For every `showcase-mg` and `motion-graphic` segment in the timeline:

1. Locate the narration text at that segment's `start_time` in the clipped transcript.
2. Check that the segment's `notes` field contains a `symbolic_alignment:` entry.
3. **FAIL** if `symbolic_alignment:` is absent or its value is blank.
4. **FAIL** if the alignment reads as generic (e.g., "shows relevant information") — require a specific claim like "speaker is saying '$600/month saved'; NumberCountUp animating to $600 directly represents that number."
5. Flag any case where the visual type does not match the speech content — for example, a `FlowchartAnimation` during a sentence about a single number, or a `ChecklistReveal` while the speaker describes a single tool. In these cases, note the mismatch and substitute the correct showcase template.

If symbolic alignment issues are found: update the `template` and `template_category` to better match the spoken claim, update `notes` with the corrected `symbolic_alignment:` entry, and re-run Reuse Cap Validation to ensure the substitution doesn't breach the cap.

### 4c. MG Description Quality Validation

Run after Reuse Cap and Symbolic Alignment validations. These are FAIL-level gates — resolve before proceeding.

For every MG segment in the assembled timeline:

**Check 1 — Hera Prompt Length (FAIL if under 100 words):**
If `hera: true`, count the words in the MG brief prompt in the storyboard. FAIL if the prompt is fewer than 100 words. Rewrite the prompt using the 5-part structure (subject / motion / style / color / duration hint) until it passes.

**Check 2 — Hera Reference Image (FAIL if missing):**
If `hera: true`, verify the Visual Asset Source Map entry has a non-empty `reference_image_url` (Supabase library URL) OR `image_source: frame-extract` with a resolved file path. FAIL if the field is empty, `null`, or set to `unknown`. If a reference cannot be obtained, demote this slot to a showcase template — NEVER submit a reference-less brief to Hera.

**Check 3 — Showcase Typed Props (FAIL if free-text only):**
If `visual_type: showcase-mg`, verify the segment has a `showcaseProps` object (not just a `notes` description). Each prop key must match the component's TypeScript Props type. FAIL if the only documentation is free-text. Rewrite as typed props before proceeding.

**Check 4 — Template Variety (FAIL if same template reused within 3 MG slots):**
Scan all MG segments in order. FAIL if any showcase template appears in two MG slots that are 3 or fewer MG positions apart (i.e., MG-1 and MG-4 or closer use the same template). This is stricter than the adjacent-only Reuse Cap check and prevents visual monotony across the intro. ROI running-total counters (`ROICalculator` / `NumberCountUp`) are exempt.

For each FAIL: identify the deficient MG, apply the fix (rewrite prompt, add reference image, select a different template, write typed props), then re-run Reuse Cap + Symbolic Alignment + MG Description Quality validations.

### 5. Transition Segments

When combining intro and body clips into a single composition:
- Insert a `transition` segment at the intro-to-body boundary
- Default: `WhiteFlash` template, 30 frames (1s at 30fps)
- Overlaps last 15 frames of intro's final segment + first 15 frames of body's first segment
- Visual type: `transition`, template: `WhiteFlash`
- The transition segment appears in the timeline as an overlay — it does not replace adjacent segments

### 6. Logo Extraction Prerequisites

Before Hera motion graphic generation can proceed:

1. **Scan MG briefs** for any logo references (company logos, platform icons, product marks)
2. **Check existing assets**: look in `video-editor/branded-assets/` and project `public/` for existing logo files
3. **Extract missing logos**: For each referenced logo not already available:
   - If visible in source video frames → extract frame, crop logo region, save as PNG
   - If available as project asset (e.g., uploaded brand kit) → reference directly
   - If neither → note as "MISSING — requires manual upload" in the Visual Asset Source Map
4. **List in Visual Asset Source Map** under a `logo-prerequisites` section with:
   - `logo_id`, `description`, `source` (frame-extract / brand-kit / missing), `file_path`

The [FP] Full Pipeline command must resolve all logo prerequisites BEFORE triggering Hera MG generation.

### 7. Validate Continuity

After building all rows:
1. Sort by `start_time`
2. Verify ZERO gaps: each segment's `end_time` equals the next segment's `start_time`
3. Verify no overlaps: no two segments claim the same time range
4. Verify total duration matches expected video length

**If gaps found:** Insert `speaker` segments to fill gaps (speaker is the default visual).
**If overlaps found:** Flag for manual resolution.

### 8. Build the Timeline Table

```markdown
## Master Timeline

**Total Duration:** {total_duration}
**Total Segments:** {segment_count}
**FPS:** 30

| Seg | Start | End | Frames | Visual | Template | Source | Asset Ref | Caption | Cap Pos | Section |
|-----|-------|-----|--------|--------|----------|--------|----------|---------|---------|---------|
| seg-001 | 00:00.000 | 00:02.500 | 75 | speaker | SubtleZoom | {path} | — | "Hook text" | bottom-left | hook |
| seg-002 | 00:02.500 | 00:05.000 | 75 | video-extract | BRollOverlay | {path} | broll-01 | — | — | hook |
| seg-003 | 00:05.000 | 00:08.000 | 90 | branded-template | UpworkProfile | branded-assets | bt-01 | — | — | intro |
...
```

### 9. Append and Auto-Proceed

Append the complete master timeline to {outputFile}.

"**Timeline Assembly Complete**

- Total segments: {segment_count}
- Total duration: {total_duration}
- Zero gaps: {verified/issues}
- Section breakdown: {section_counts}

Proceeding to pacing validation..."

Update {outputFile} frontmatter with `stepsCompleted` appended, then load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Every segment has all required fields populated, including `template_category` for all MG segments
- Zero frame gaps between segments
- Total duration matches expected video length
- Each segment references a valid Remotion template
- All caption segments verified via two-pass VAD calibration (±3 frame tolerance when audio analysis available; ±15 frame for transcript-only fallback, flagged in notes)
- Intro visual density validated: min_visual_breaks = ceil(intro_duration / 10), min_mgs = ceil(min_visual_breaks * 0.6), max 6s between visual breaks
- MG spacing validated: all intro MG gaps between 2–8s (P12), no clustering > 50% in single section
- Reuse Cap Validation passed: no showcase template > 2 in intro, no template > 3 in full video, no identical template in adjacent MG slots
- Symbolic Alignment Validation passed: every `showcase-mg` and `motion-graphic` segment has a specific, non-generic `symbolic_alignment:` in notes
- Total `hera: true` segments in intro ≤ 3
- Logo prerequisites identified and listed in Visual Asset Source Map
- Transition segment inserted at intro-to-body boundary
- Timeline appended to storyboard document
- MG Description Quality Validation passed: all Hera MGs have ≥100-word prompts + reference images; all showcase MGs have typed `showcaseProps`; no template reused within 3 MG slots

### FAILURE:

- Gaps in the timeline
- Missing template assignments
- Not validating continuity
- Deriving `captionFrame` from transcript alone without VAD refinement (single-pass is not acceptable when audio analysis is available)
- Caption text appearing outside of when the speaker says those words
- Skipping two-pass calibration and approximating frame values
- Intro with fewer MGs or visual breaks than the density formula requires
- Intro with visual gaps exceeding 6 seconds
- MG spacing violations: any intro gap > 8s or consecutive gap < 2s (P12)
- Reuse Cap violation: any showcase template > 2 in intro or > 3 in full video
- Same `template_category` in adjacent MG segments (MG-speaker-MG sandwich)
- Any `motion-graphic` segment without `hera: true` in Visual Asset Source Map
- More than 3 Hera-approved MGs in the intro
- Missing or blank `symbolic_alignment:` in notes for any `showcase-mg` or `motion-graphic` segment
- Generic symbolic_alignment text that does not describe the specific speech–visual match
- Missing `template_category` on MG segments
- Missing logo prerequisites in Visual Asset Source Map
- No transition segment at intro-to-body boundary
- Requiring user interaction (this is deterministic)
- Hera MG brief under 100 words (MG Description Quality Check 1)
- Hera MG missing reference image (MG Description Quality Check 2)
- Showcase MG with free-text notes instead of typed `showcaseProps` (MG Description Quality Check 3)
- Same showcase template appearing within 3 MG slots (MG Description Quality Check 4)
