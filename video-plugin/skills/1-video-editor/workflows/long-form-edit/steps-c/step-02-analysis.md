---
name: 'step-02-analysis'
description: 'Run audio analysis, transcription, and lightweight boundary visual analysis on all files. Detect intro/body boundary using visual analysis (talking-head → screen-share transition) for single-file recordings, with transcript overlap as fallback.'

nextStepFile: './step-03-clipping.md'
---

# Step 2: Analysis — Audio, Transcription, Boundary Detection

## STEP GOAL:

Run audio analysis, transcription, and transcript refinement on all video files. For single-file recordings, detect the intro/body boundary using lightweight visual analysis (talking-head → screen-share transition), with transcript overlap as fallback. The full storyboard visual analysis is deferred to step-03 where it runs on the clipped videos (so timestamps match the clipped timeline directly).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a long-form video production specialist
- ✅ Technical, concise, efficient communication
- ✅ Execute with precision — run all analysis tools sequentially per file

### Step-Specific Rules:

- 🎯 Multi-file: use `content_type` from each YAML for audio analysis thresholds
- 🎯 Single-file: use `main` (conservative) for audio analysis, then detect boundary using visual analysis
- 🎯 Boundary VA: Gemini call on first 3min of proxy (1fps) — NOT the full storyboard VA (which runs in step-03 on clipped videos)
- 🚫 FORBIDDEN to clip or modify video files in this step — analysis only
- 🚫 FORBIDDEN to run full storyboard VA in this step — only boundary VA is allowed here

### ⚡ Parallelization Rules:

- **Multi-file mode:** Process intro and body content types in PARALLEL (two independent branches). Within each branch, run audio analysis (`analyze-audio.ts`) and transcription (DeepGram API call) concurrently as background processes, then wait for both before running `refine-transcript.ts`.
- **Single-file mode:** Launch boundary VA concurrently with audio analysis + transcription. All three must complete before refinement + boundary detection.
- Use background bash processes (`&` + `wait`) or the Agent tool to run independent operations concurrently.

## MANDATORY SEQUENCE

### 1. Determine Analysis Plan

Based on `{recording_mode}`:

**Multi-file:** Each file is analysed independently with its own content_type:
- Intro YAML → analyse with `--content-type intro`
- Body/Main YAML → analyse with `--content-type main`

**Single-file:** The single file gets analysed as `main` (conservative thresholds), then boundary detection splits the transcript into intro/body portions.

### 2. Audio Analysis + Transcription (per file — parallelized)

**⚡ Multi-file parallel execution:** For multi-file recordings, process BOTH content types (intro and body) simultaneously. Launch two parallel branches — each branch runs its audio analysis and transcription concurrently, then waits for both to complete before proceeding to refinement.

**Within each content type**, run audio analysis and transcription concurrently:
- Launch `analyze-audio.ts` as a background process
- Launch the DeepGram API call concurrently
- Wait for both to complete
- Then run `refine-transcript.ts` (which depends on both outputs)

**Single-file mode:** Launch audio analysis, transcription, and boundary VA concurrently. Wait for all three before refinement and boundary detection.

#### 2a. Audio Analysis

For each video file, run `analyze-audio.ts` with the appropriate content_type:

```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
npx tsx analyze-audio.ts \
  --video "{proxy_path}" \
  --output "{analysis_dir}/{content_type}/audio-analysis.md" \
  --content-type {intro|main}
```

This produces:
- `audio-analysis.md` — human-readable analysis
- `audio-analysis.json` — machine-readable classified regions (auto-generated sidecar)
- `audio-analysis-sidecar.json` — additional analysis data

#### 2b. Transcription (per file — runs concurrently with audio analysis and boundary VA)

Transcribe each proxy using DeepGram Nova-3 API for word-level timestamps. The API key is in `.env` as `DEEPGRAM_API_KEY`. **This runs concurrently with the audio analysis above — do not wait for audio analysis to complete before starting transcription.**

```bash
curl -X POST "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&utterances=true&diarize=false&detect_language=false&language=en" \
  --header "Authorization: Token ${DEEPGRAM_API_KEY}" \
  --header "Content-Type: audio/mp4" \
  --data-binary @"{proxy_path}"
```

Save the full transcript response to:
`{analysis_dir}/{content_type}/transcript.json`

#### 2c. Boundary Visual Analysis (single-file only — runs concurrently with 2a + 2b)

**Skip this section entirely for multi-file recordings.**

Run a lightweight Gemini visual analysis on the first 3 minutes of the proxy video to detect where talking-head transitions to screen-share. This gives the rough boundary second — the transcript + audio analysis will refine it to an exact clip point in section 3.

**This runs in parallel with audio analysis and transcription — launch it concurrently.**

1. Upload the proxy video to the Gemini Files API
2. Query the first 3 minutes at 1fps using the standard Gemini VA prompt and `VisualAnalysisSegments` schema (~180 frames)
3. Model: `gemini-2.5-pro`, temperature 0.2
4. Use `start_offset="0s"`, `end_offset="180s"` in `videoMetadata` (string format required by SDK)
5. Save the response to `{analysis_dir}/boundary-va.json`

#### 2d. Transcript Refinement (per file — after both AA and TR complete)

**Wait for both audio analysis AND transcription to complete before running refinement.**

**Transcript flattening:** DeepGram returns a nested response (`results.channels[0].alternatives[0].words`). Before refinement, flatten it to the format `refine-transcript.ts` expects — a top-level `words` array, `utterances` array, and `transcript` string. Save the original DeepGram response to `deepgram-raw.json` for reference.

Run `refine-transcript.ts` to calibrate word timestamps against VAD boundaries:

```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
npx tsx refine-transcript.ts \
  --transcript "{analysis_dir}/{content_type}/transcript.json" \
  --sidecar "{analysis_dir}/{content_type}/audio-analysis-sidecar.json" \
  --output "{analysis_dir}/{content_type}/refined-transcript.json"
```

### 3. Boundary Detection (single-file only)

**Skip this section entirely for multi-file recordings.**

**Wait for boundary VA (2c), audio analysis (2a), transcription (2b), and refinement (2d) to ALL complete before proceeding.**

For single-file recordings, detect where the intro ends and the body begins using visual analysis as the primary method, with transcript overlap as fallback.

#### 3a. Primary Method — Visual Transition Detection

Walk the boundary VA segments (`boundary-va.json`) chronologically:

1. Find the first non-talking-head segment (`screen-share`, `diagram-slides`, `mixed-pip`) lasting ≥ 10 seconds
2. **Brief cutaway check:** if that segment is followed by a return to talking-head within 5 seconds, skip it and continue searching
3. Boundary = start timestamp of the first sustained non-talking-head segment
4. If a `transition` segment (< 3s) immediately precedes it, use the transition's start timestamp instead

**If a visual transition is found, proceed to 3c (Precision Clip).**

#### 3b. Fallback — Extended VA + Transcript Overlap

If no visual transition is found in the first 3 minutes:

1. **Extend VA window:** Re-query Gemini at 1fps for minutes 3-6 (`start_offset="180s"`, `end_offset="360s"`). Save to `{analysis_dir}/boundary-va-extended.json`
2. Walk the extended segments using the same rules as 3a
3. **If still no visual transition:** Fall back to transcript token overlap matching:
   1. Extract all words from `{script_intro_text}` (from step-01) — tokenize: lowercase, strip punctuation
   2. Extract all words from the transcript with their timestamps
   3. Use a sliding window of `len(script_intro_tokens)` words across the transcript
   4. For each window position, calculate overlap ratio: `|intersection with script_intro_tokens| / |script_intro_tokens|`
   5. The intro region is where overlap is consistently high (> 0.3)
   6. Find the transition point: where overlap drops below 0.3 for 5+ consecutive words after a high-overlap region
4. Log: "**Fallback:** No visual transition detected — using transcript overlap boundary"

#### 3c. Precision Clip — Transcript + Audio Refinement

The visual analysis (or transcript overlap) gives a rough boundary second. Refine it to an exact clip point:

1. Find the nearest sentence boundary in the transcript at or before the rough timestamp — the last word before a period/question mark, or the last word of the nearest utterance boundary
2. Snap to the nearest SILENCE region ≥ 1000ms near that sentence boundary. The boundary is the **midpoint** of this silence region
3. **Silence fallback cascade:** ≥ 500ms → ≥ 300ms → raw sentence-end timestamp

#### 3d. Timing Validation (I4)

Validate the detected boundary against inspiration timing data:

- < 30s → ⚠️ WARNING: "Unusually short intro ({boundary}s) — expected 30-120s"
- 30-120s → ✅ Normal (no warning)
- \> 120s → ⚠️ WARNING: "Unusually long intro ({boundary}s) — expected 30-120s"

**Visual boundary is always used regardless of warnings** — timing warnings are informational only.

#### 3e. Store Boundary

Set session variables:
- `{boundary_timestamp_ms}` — the millisecond position where intro ends and body begins
- `{boundary_method}` — `visual` or `transcript-fallback`

Log boundary concisely: "**Boundary detected ({boundary_method}):** {boundary}s — '...{last 5 words}...' | '...{first 5 words}...'"

### 4. Auto-Proceed to Clipping

Analysis decisions (boundary detection, silence snapping) are fully autonomous — no checkpoint needed. Log a one-line summary and proceed immediately:

"**Analysis done:** {words} words transcribed, boundary at {boundary}s. Proceeding to clipping."

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Audio analysis completed for all files with correct content_type thresholds
- Transcripts generated with word-level timestamps via DeepGram Nova-3
- Transcripts refined against VAD boundaries
- Single-file: boundary VA completed on first 3min of proxy (`boundary-va.json` saved)
- Single-file: boundary detected using visual transition (or transcript-fallback if no transition found)
- Single-file: boundary precision-refined via sentence boundary + silence snap
- All analysis files saved to correct `{content_type}/` subdirectories
- Session variables updated with analysis results (including `{boundary_method}`)
- Full storyboard VA NOT run in this step (deferred to step-03 on clipped videos)

### ❌ SYSTEM FAILURE:

- Using wrong content_type for audio analysis (e.g., `intro` thresholds on body footage)
- Skipping transcript refinement
- Running full storyboard VA in this step (only boundary VA is allowed — full VA runs on clipped videos in step-03)
- Single-file: skipping boundary VA and going straight to transcript overlap
- Single-file: not snapping boundary to a silence region
- Clipping or modifying video files in this step
