---
name: 'step-03-audio-precision'
description: 'Refine content cut boundaries using audio analysis data for natural transitions, then perform pure audio cleanup — silence removal, breath trimming, noise cut, filler handling'

nextStepFile: './step-05-generate.md'
outputFile: '{project_folder}/{project-slug}/video-editor/clips/{video-id}-clip-plan.md'
---

# Step 3: Audio Precision & Cleanup

## STEP GOAL:

Two responsibilities: (A) Refine AUTO_APPROVED content cut boundaries from step 2 by snapping them to natural audio edges (silence/breath boundaries) for clean transitions, and (B) perform deterministic audio cleanup — extracting SPEECH regions, applying gap handling rules, and generating a unified keep segment list.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip classified region loading — `classified_regions` is the authoritative source
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step, ensure entire file is read
- 📋 This step is DETERMINISTIC — follow the exact algorithm
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video editing automation assistant executing audio precision refinement and deterministic audio cleanup
- ✅ Technical precision is critical — timestamps must be millisecond-exact
- ✅ No creative interpretation — follow the algorithm exactly

### Step-Specific Rules:

- 🎯 Focus ONLY on (A) refining content cut boundaries and (B) generating audio-based keep segments
- 🚫 FORBIDDEN to re-run FFmpeg silencedetect in this step — audio analysis is pre-computed
- 🚫 FORBIDDEN to modify content cut decisions from step 2 (only refine their boundaries)
- 🚫 FORBIDDEN to use FFmpeg `silenceremove` filter (known precision bugs)
- ✅ MUST derive cut points from `classified_regions` in audio-analysis.json
- ✅ MUST use `speech_boundary_detail` for millisecond-precise onset/offset at start and end
- ✅ MUST use `trim`/`atrim`/`concat` for cutting (not `silenceremove`)
- ✅ MUST use stream copy (`-c copy`) for final video cuts
- ✅ Audio analysis (classified_regions) is MANDATORY — no FFmpeg fallback

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Append audio precision & cleanup summary to {outputFile}
- 📖 Update frontmatter stepsCompleted when complete
- 🚫 This is an auto-proceed step — no user interaction

## CONTEXT BOUNDARIES:

- Step 1 provided: audio-analysis.json path, transcript JSON path, content_type (intro/main), buffer_ms
- Step 2 provided: AUTO_APPROVED content cuts with raw transcript timestamps (in clip plan)
- Visual analysis JSON provides visual events (distractions, obstructions, breaks) for smart distraction handling
- This step: (A) refines content cut boundaries using audio data, (B) produces speech boundary trim + gap-handled keep segments
- Output appended to clip plan document

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise.

### 1. Load Audio Analysis JSON

Load the audio analysis JSON file identified in step 1:
`{project_folder}/{project-slug}/video-editor/analysis/{content-type}/audio-analysis.json`

**Verify required fields exist:**
- `classified_regions` — array of `{startMs, endMs, durationMs, classification, confidence, avgDb, vadProb}`
- `speech_boundary_detail` — array of boundary onset/offset tables
- `audio_metadata.total_speech_ms` — total speech duration

**Optional fields:**
- `filler_regions` — array of `{startMs, endMs, durationMs, word}` (extracted from transcript by analyze-audio.ts)
- `denoised` — boolean indicating whether audio was denoised before analysis
- `content_type` — `intro` or `main` (may also come from step 1 init)

**If `classified_regions` is missing or empty:**
"**Error: audio-analysis.json does not contain `classified_regions`.**

The Audio Analysis workflow must be run first with the updated `analyze-audio.ts` script.
Run the Audio Analysis workflow (AA) before Video Clipping."
→ HALT. Do not proceed.

**Extract:**
- `classified_regions` array
- `speech_boundary_detail` array
- `audio_metadata` (total durations, RMS, etc.)
- `filler_regions` array (if available — used for filler word handling)
- `denoised` flag (log whether analysis used denoised audio)
- Total duration from `audio_metadata.duration_ms` or `total_speech_ms + total_silence_ms + total_breath_ms + total_noise_ms`

**Log denoising status:**
If `denoised` is true: "Audio analysis was performed on denoised audio (highpass + arnndn RNNoise). Classification accuracy is improved."
If `denoised` is false or missing: "Warning: Audio analysis was NOT denoised. Consider re-running Audio Analysis with denoising enabled for better results."

"**Loading audio analysis data...**"

### 1b. Load Visual Events from Visual Analysis

Load the visual analysis JSON:
`{project_folder}/{project-slug}/video-editor/analysis/{content-type}/visual-analysis.json`

Extract all `visualEvents` from segments classified as `talking-head` or `mixed-pip`. Build a flat list of visual events with their timestamps converted to milliseconds:

```
visual_events = []
for segment in visual_analysis.segments:
    if segment.details.visualEvents:
        for event in segment.details.visualEvents:
            visual_events.append({
                startMs: parse_mmss_to_ms(event.timestamp),
                endMs: parse_mmss_to_ms(event.endTimestamp),
                eventType: event.eventType,
                description: event.description
            })
```

If visual analysis JSON is missing or has no visual events:
"Visual events: none detected (visual analysis may not have flagged any presenter distractions)."

If visual events found:
"**Visual events loaded:** {count} events ({distraction_count} distractions, {obstruction_count} obstructions, {break_count} breaks)"

### 1c. Load Content Cuts from Step 2

Load the **Content Cleanup Findings** section from {outputFile}.

Extract all AUTO_APPROVED content cuts with their raw transcript timestamps:
- Cut ID, start timestamp, end timestamp, duration

"**Content cuts loaded:** {count} AUTO_APPROVED cuts ({total_seconds}s) from transcript analysis"

If no content cuts exist:
"**No content cuts from transcript analysis.** Proceeding with audio cleanup only."

### 2. Refine Content Cut Boundaries

**Primary responsibility of this step:** Snap content cut boundaries to natural audio edges for clean transitions.

For each AUTO_APPROVED content cut boundary (start AND end):

1. Search `classified_regions` and `speech_boundary_detail` within a **200ms tolerance window** around the boundary
2. Find the nearest SILENCE or BREATH edge (where dB drops / VAD drops)
3. Snap the cut boundary to that edge for natural-sounding transitions
4. If no silence/breath edge exists within 200ms: keep the raw transcript timestamp — it's in the middle of speech content
5. Log all adjustments:

```
Content Cut Boundary Refinement:
| Cut ID | Boundary | Original (ms) | Snapped (ms) | Aligned To | Delta (ms) |
|--------|----------|---------------|--------------|------------|------------|
| C1     | start    | 15234         | 15180        | SILENCE    | -54        |
| C1     | end      | 22456         | 22490        | BREATH     | +34        |
| C2     | start    | 22890         | 22890        | —          | 0 (no edge within 200ms) |
| ...    | ...      | ...           | ...          | ...        | ...        |
```

After snapping, recalculate the duration of each adjusted cut. If any adjusted cut duration becomes ≤ 0 after snapping (boundaries crossed), flag it for removal with a warning.

**Refinement Summary:**
```
**Content Cut Boundary Refinement:**
- Boundaries checked: {count}
- Boundaries snapped: {snapped_count}
- Boundaries unchanged: {unchanged_count}
- Max adjustment: {max_delta}ms
- Cuts invalidated (boundaries crossed): {invalidated_count}
```

### 3. Apply Speech Quality Filters

After loading `classified_regions`, apply these filters to discard false-positive SPEECH classifications BEFORE generating the keep/remove list:

1. **Minimum duration**: Discard SPEECH segments shorter than 200ms — noise bursts, not speech
2. **Minimum confidence**: Discard SPEECH segments with confidence < 0.75 — unreliable classification
3. **Energy floor**: Discard SPEECH segments with RMS energy below -35dB (`avgDb < -35`) — not genuine speech
4. **Isolated segment check**: SPEECH segment with no adjacent SPEECH within 500ms on either side AND duration < 300ms → treat as noise

Log all discarded segments with reason codes for debugging:

```
Discarded SPEECH segments:
| startMs | endMs | durationMs | confidence | avgDb | Reason |
|---------|-------|------------|------------|-------|--------|
| 38120   | 38240 | 120        | 0.62       | -28   | LOW_CONFIDENCE (0.62 < 0.75) |
| 52400   | 52520 | 120        | 0.81       | -38   | ENERGY_FLOOR (-38 < -35dB) |
```

### 3b. Content-Type-Specific Audio Cleanup

When processing intro content (`content_type = intro`):

- Use **150ms** silence buffer — the intro must be clipped tight for retention
- Zero tolerance for non-speech sounds: coughs, sneezes, breaths, background noise
- BREATH classifications adjacent to SPEECH are acceptable ONLY if < 100ms duration
- Any NOISE or unclassified region > 50ms between speech segments → remove
- Filler words (from `filler_regions` in audio-analysis.json, if available) → always CUT

When processing body/main content (`content_type = main`):
- Use **300ms** silence buffer — preserves natural speaking rhythm
- More conservative gap handling — prioritize natural pacing over tight cuts
- Short silences that create natural sentence/thought boundaries should be preserved
- Filler words → CUT only if isolated (surrounded by silence/breath ≥ 200ms on at least one side)

### 4. Extract Filtered SPEECH Regions

Filter `classified_regions` (after quality filters from step 3) to get only SPEECH entries that passed all filters — these define the authoritative keep list before gap handling:

```
speech_regions = [r for r in classified_regions if r.classification == 'SPEECH']
```

**Sort by startMs** (should already be ordered, but confirm).

Report:
"**Speech regions from classified_regions:** {count} regions, total {total_speech_ms}ms speech"

### 5. Apply Speech Boundary Precision (Start and End of Video)

Use `speech_boundary_detail` for ms-precise onset/offset at the **first** and **last** SPEECH regions.

**For the first SPEECH region (video start trim):**
- Look up `speech_boundary_detail[0].onset` — the 20ms-resolution waveform points ±150ms around the first speech onset
- Find the exact millisecond where speech starts (first onset point where VAD prob rises above 0.4 and RMS dBFS rises above -40)
- `speech_start_ms = onset detection result`
- `trim_in_ms = max(0, speech_start_ms - 150)` (apply 150ms pre-buffer)

**For the last SPEECH region (video end trim):**
- Look up `speech_boundary_detail[-1].offset` — the waveform points ±150ms around the last speech offset
- Find the exact millisecond where speech ends (last offset point where VAD prob drops below 0.4 and RMS dBFS drops below -40)
- `speech_end_ms = offset detection result`
- `trim_out_ms = min(total_duration_ms, speech_end_ms + 150)` (apply 150ms post-buffer)

**If boundary detail is unavailable or inconclusive** (e.g., sparse onset points):
- Fall back to `speech_regions[0].startMs - 150` for trim_in
- Fall back to `speech_regions[-1].endMs + 150` for trim_out

Report:
"**Speech Boundary Trim:**
- First speech onset: {speech_start_ms}ms → trim in: {trim_in_ms}ms
- Last speech offset: {speech_end_ms}ms → trim out: {trim_out_ms}ms
- Dead time removed: {trim_in_ms}ms from start, {total_duration_ms - trim_out_ms}ms from end"

### 6. Apply Gap Handling Rules to Non-SPEECH Regions

Walk the `classified_regions` array. For each non-SPEECH region between the first and last SPEECH boundaries, apply the gap handling rules:

**Gap Handling Rules (Intro — content_type = intro):**

| Region classification | Duration | Action |
|---|---|---|
| SILENCE | ≥ 1000ms (1s) | **CUT** — remove entirely |
| SILENCE | 300ms – 999ms | **COMPRESS** to 150ms |
| SILENCE | < 300ms | **KEEP** — preserve natural rhythm |
| BREATH | ≥ 100ms | **CUT** — remove entirely |
| BREATH | < 100ms (adjacent to SPEECH) | **KEEP** — natural breath |
| NOISE | any | **CUT** — remove entirely |
| FILLER | any | **CUT** — remove entirely |

**Gap Handling Rules (Main — content_type = main):**

| Region classification | Duration | Action |
|---|---|---|
| SILENCE | ≥ 2000ms (2s) | **CUT** — remove entirely |
| SILENCE | 500ms – 1999ms | **COMPRESS** to 300ms |
| SILENCE | < 500ms | **KEEP** — preserve natural rhythm |
| BREATH | any | **TRIM** to 150ms |
| NOISE | any | **CUT** — remove entirely |
| FILLER | isolated (silence/breath ≥ 200ms on at least one side) | **CUT** — remove filler |
| FILLER | mid-speech (no adjacent gap) | **KEEP** — part of natural flow |

**FILLER regions:** If `filler_regions` exists in audio-analysis.json, cross-reference each filler's timestamp range with the classified_regions. For each filler word:
1. Find the classified region(s) it falls within
2. If the filler is surrounded by SILENCE or BREATH (≥ 200ms gap on at least one side for main, any gap for intro): mark as CUT
3. Split the enclosing SPEECH region if needed to excise the filler

**Algorithm:**
For each non-SPEECH region with startMs ≥ trim_in_ms and endMs ≤ trim_out_ms, apply the rules for the current content_type (intro or main) as defined in the tables above.

Track:
- `silence_cut_count`, `silence_cut_ms` — regions fully removed
- `silence_compressed_count`, `silence_compressed_ms_saved` — ms saved by compression
- `breath_trimmed_count`, `breath_trimmed_ms_saved` — ms saved by breath trimming
- `noise_cut_count`, `noise_cut_ms` — noise regions removed

### 6b. Visual Distraction Handling

After gap handling, cross-reference the keep segments with `visual_events` from step 1b:

**For each visual event (distraction, obstruction, or break):**

1. Find the SPEECH region(s) that overlap with the event's timestamp range
2. Calculate the overlapping speech duration (how much speech falls within the event's time range)
3. Apply the distraction decision rules:

**Auto-CUT (remove without user review):**
- The speech overlapping with the visual event is **short** (< 2000ms / 2 seconds)
- AND the speech content is **throwaway** (single filler word, "alright", "okay", "right", "so", etc.)
- AND the event is a `distraction` or `obstruction` type

**FLAG for review (do NOT auto-cut):**
- The speech overlapping with the visual event is **substantive** (>= 2000ms)
- OR the speech contains valuable content (full sentences, explanations, key points)
- These are logged in the clip plan for user awareness but NOT removed

**Algorithm:**
```
for event in visual_events:
    overlapping_speech = find_speech_regions_in_range(event.startMs, event.endMs)
    total_speech_ms = sum(overlap duration for each region)

    if total_speech_ms < 2000:
        # Short speech — check if throwaway
        words_in_range = get_transcript_words_in_range(event.startMs, event.endMs)
        if is_throwaway(words_in_range):
            mark_for_cut(event.startMs, event.endMs, reason="VISUAL_DISTRACTION_SHORT")
        else:
            flag_for_review(event, words_in_range, reason="distraction with non-throwaway speech")
    else:
        flag_for_review(event, reason="distraction during substantive speech")
```

**Report:**
"**Visual distraction handling:**
- Events processed: {count}
- Auto-cut (short throwaway + distraction): {cut_count} ({cut_ms}ms)
- Flagged for review (valuable speech): {flag_count}
{for each flagged: '  - {timestamp}: {eventType} — "{speech_content}" ({duration}ms)'}
"

### 7. Generate Unified Keep Segments

Reconstruct the timeline into KEEP segments based on SPEECH regions + gap decisions + visual distraction cuts + content cut regions (with refined boundaries):

**Algorithm:**
1. Start with audio-derived keep segments (SPEECH regions after gap handling)
2. Start at `trim_in_ms`
3. Walk SPEECH regions in order
4. Between SPEECH regions: apply gap handling (CUT removes, COMPRESS inserts compressed duration, KEEP inserts full gap, BREATH inserts trimmed duration, NOISE removes)
5. End at `trim_out_ms`
6. **Subtract all content cut regions** (with refined boundaries from step 2 of this sequence) from the keep segments
7. Result: final ordered keep segment list

**Result:** ordered list of KEEP segments with ms-precise start/end:

```
KEEP segments:
[
  { startMs: {trim_in_ms}, endMs: {first_speech_end_ms}, durationMs: X },
  { startMs: {next_speech_start_ms}, endMs: {next_speech_end_ms}, durationMs: X },
  ...
  { startMs: {last_speech_start_ms}, endMs: {trim_out_ms}, durationMs: X }
]
```

Note: The compressed silence "keeps" are implicit in the timeline — they are represented as a gap between the previous KEEP segment's endMs and the next segment's startMs. The FFmpeg filter_complex in step 5 will include these naturally.

### 8. Calculate Summary Statistics

Compute:
- **Speech regions:** {count}
- **Total speech duration:** {ms}ms ({seconds}s)
- **Speech as % of original:** {percentage}%
- **Start dead air removed:** {trim_in_ms}ms
- **End dead air removed:** {total_duration_ms - trim_out_ms}ms
- **Silence cut (≥ threshold):** {count} regions, {ms}ms removed
- **Silence compressed (mid-range):** {count} regions, {ms}ms saved
- **Breath trimmed:** {count} regions, {ms}ms saved
- **Noise cut:** {count} regions, {ms}ms removed
- **Content cuts (boundary-refined):** {count} cuts, {ms}ms removed
- **Total removed:** {ms}ms
- **Original duration:** {ms}ms
- **Estimated cleaned duration:** {ms}ms
- **Reduction:** {percentage}%
- **Keep segments:** {count}

### 9. Append Audio Precision & Cleanup Summary to Clip Plan

Update the **Audio Precision & Cleanup Summary** section of {outputFile}:

```markdown
## Audio Precision & Cleanup Summary

**Source:** `classified_regions` from audio-analysis.json (analyze-audio.ts + Silero VAD)
**Denoised:** {yes/no} (highpass 80Hz + arnndn RNNoise mix=0.95)
**Silence Threshold:** -35 dBFS (Silero VAD + FFmpeg silencedetect)
**Content Type:** {intro/main}
**Buffer:** {150ms (intro) / 300ms (main)} pre/post SPEECH regions

**Content Cut Boundary Refinement:**
- Boundaries checked: {count}
- Boundaries snapped: {snapped_count}
- Boundaries unchanged: {unchanged_count}
- Max adjustment: {max_delta}ms
- Cuts invalidated: {invalidated_count}

| Cut ID | Boundary | Original (ms) | Snapped (ms) | Aligned To | Delta (ms) |
|--------|----------|---------------|--------------|------------|------------|
| ...    | ...      | ...           | ...          | ...        | ...        |

**Speech Boundary Trim:**
- First speech onset: {speech_start_ms}ms → trim in: {trim_in_ms}ms
- Last speech offset: {speech_end_ms}ms → trim out: {trim_out_ms}ms
- Start dead air removed: {trim_in_ms}ms
- End dead air removed: {end_dead_ms}ms

**Gap Handling Results:**

| Action | Count | Duration Removed/Saved |
|--------|-------|----------------------|
| Silence cut (≥ threshold) | {count} | {ms}ms |
| Silence compressed (mid-range → buffer) | {count} | {ms}ms saved |
| Silence kept (< threshold) | {count} | — |
| Breath trimmed/cut | {count} | {ms}ms saved |
| Noise cut | {count} | {ms}ms |
| Filler words cut | {count} | {ms}ms |

**Overall:**

| Metric | Value |
|--------|-------|
| Original duration | {ms}ms ({s}s) |
| Speech regions | {count} |
| Total speech | {ms}ms ({s}s, {%}%) |
| Content cuts (boundary-refined) | {count} ({ms}ms) |
| Total removed | {ms}ms |
| Estimated cleaned duration | {ms}ms ({s}s) |
| Reduction | {%}% |

**Keep Segments ({count}):**

| # | Start (ms) | End (ms) | Duration (ms) |
|---|-----------|---------|--------------|
| 1 | {trim_in_ms} | {end_ms} | {dur_ms} |
| 2 | {start_ms} | {end_ms} | {dur_ms} |
| ... | ... | ... | ... |
```

Update frontmatter: append `'step-03-audio-precision'` to `stepsCompleted`.

### 10. Auto-Proceed to Clip Plan Generation

"**Audio precision & cleanup complete. {count} SPEECH regions identified. {refined_count} content cut boundaries refined. {trim_in_ms}ms dead air removed from start, {end_dead_ms}ms from end. {total_removed_ms}ms total removed ({reduction}% reduction). {keep_count} keep segments generated.**

**Proceeding to clip plan generation (skipping review — all cuts auto-decided)...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- AUTO_APPROVED content cuts loaded from step 2
- Content cut boundaries refined by snapping to nearest SILENCE/BREATH edges within 200ms tolerance
- All boundary adjustments logged with cut ID, original, snapped, aligned-to, and delta
- `classified_regions` loaded from audio-analysis.json (no FFmpeg re-run)
- Audio analysis used denoised audio (arnndn + highpass) for cleaner classification
- Speech quality filters applied: min duration (200ms), min confidence (0.75), energy floor (-35dB), isolated segment check
- Discarded segments logged with reason codes
- Content-type-specific cleanup applied (intro: 150ms buffer, aggressive; main: 300ms buffer, conservative)
- Filler regions cross-referenced from `filler_regions` in audio-analysis.json (if available)
- Visual events loaded from visual-analysis.json and cross-referenced with speech regions
- Visual distractions with short throwaway speech auto-cut; substantive speech flagged for review only
- SPEECH regions extracted as authoritative keep list (post-filter)
- `speech_boundary_detail` used for ms-precise trim_in/trim_out
- Gap handling rules applied per content_type table (including FILLER handling)
- Content cut regions subtracted from keep segments to produce unified list
- Keep segments generated with ms-precise timestamps
- Summary statistics computed and appended to clip plan (including boundary refinement log)
- Frontmatter updated with step completion
- Auto-proceeded to clip plan generation

### ❌ SYSTEM FAILURE:

- Re-running FFmpeg silencedetect (audio analysis is pre-computed)
- Using `silenceremove` instead of `trim`/`concat`
- Missing `classified_regions` from JSON and proceeding without halting
- Incorrect buffer application (wrong direction or value)
- Modifying content cut decisions from step 2 (only boundaries are refined, not decisions)
- Not loading content cuts from step 2 before generating keep segments
- Asking user for input (this is an auto-proceed step)
- Using gap rules inconsistent with the table above

**Master Rule:** This step has two responsibilities: (A) refine content cut boundaries from step 2 by snapping to audio silence/breath edges within 200ms tolerance, and (B) perform deterministic audio cleanup using `classified_regions` as the ONLY source of truth. The unified keep segment list subtracts both audio gaps AND content cuts. No creative interpretation, no re-running FFmpeg, no user interaction.
