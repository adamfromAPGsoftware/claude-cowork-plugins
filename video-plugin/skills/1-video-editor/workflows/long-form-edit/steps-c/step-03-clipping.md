---
name: 'step-03-clipping'
description: 'Remove dead air from intro and body with content-type-appropriate thresholds, remap transcripts to clipped timelines, run visual analysis on clipped videos'

nextStepFile: './step-04-storyboard.md'
---

# Step 3: Clipping — Dead Air Removal + Transcript Remap + Visual Analysis

## STEP GOAL:

Remove dead air (silence, breaths, filler words) from each content section using content-type-appropriate buffer thresholds. For single-file recordings, first split the raw and proxy files at the detected boundary. Then remap transcripts to the clipped timelines using deterministic math.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a long-form video production specialist
- ✅ Technical, concise, efficient communication
- ✅ Content-type thresholds are critical: intro=150ms (aggressive), body=300ms (conservative)

### Step-Specific Rules:

- 🎯 Intro clipping: `--content-type intro` → 150ms buffer, aggressive dead air removal
- 🎯 Body clipping: `--content-type main` → 300ms buffer, conservative dead air removal
- 🎯 Transcript remap is DETERMINISTIC — pure math using keep-segments, no re-transcription
- 🚫 FORBIDDEN to re-run transcription after clipping — remap existing transcripts only

### ⚡ Parallelization Rules:

- **FFmpeg execution (section 5):** After false start detection, run ALL FFmpeg clip commands simultaneously as background processes (`&` + `wait`): intro-proxy, intro-raw, body-proxy, body-raw. Also run both transcript remaps in parallel (pure math, instant).
- **Per-clip audio extraction (section 7):** Immediately after all FFmpeg clips complete, extract audio from each clipped video as background processes (`ffmpeg -vn -acodec copy`). They run during VA + storyboard instead of waiting until step 5.
- **Visual Analysis (section 8b):** Launch BOTH Gemini VA calls simultaneously (intro @ 1fps and body @ 0.2fps) — they are independent API calls.
- All background processes must be `wait`-ed with exit code checks before proceeding past their dependent step.

## MANDATORY SEQUENCE

### 1. Single-File Split (single-file only)

**Skip this section entirely for multi-file recordings.**

For single-file recordings, split the raw and proxy files at `{boundary_timestamp_ms}`:

```bash
# Split proxy into intro and body
ffmpeg -i "{proxy_path}" -to {boundary_seconds} -c copy "{clips_dir}/intro-proxy-split.mp4"
ffmpeg -i "{proxy_path}" -ss {boundary_seconds} -c copy "{clips_dir}/body-proxy-split.mp4"

# Split raw into intro and body
ffmpeg -i "{raw_path}" -to {boundary_seconds} -c copy "{clips_dir}/intro-raw-split.mp4"
ffmpeg -i "{raw_path}" -ss {boundary_seconds} -c copy "{clips_dir}/body-raw-split.mp4"
```

Probe split files to verify durations sum to original (within ±0.5s).

**Split reliability:** `-c copy` (stream copy) is fast but can produce corrupted first frames if the boundary doesn't fall on a keyframe. After probing, check the first frame of each split file is decodable:
```bash
ffmpeg -i "{split_file}" -frames:v 1 -f null - 2>&1
```
If the first frame fails to decode (error or black frame), re-split with re-encode for precision:
```bash
ffmpeg -i "{proxy_path}" -to {boundary_seconds} -c:v libx264 -preset fast -crf 18 -c:a aac "{clips_dir}/intro-proxy-split.mp4"
ffmpeg -i "{proxy_path}" -ss {boundary_seconds} -c:v libx264 -preset fast -crf 18 -c:a aac "{clips_dir}/body-proxy-split.mp4"
```

From this point onwards, the pipeline is identical for both recording modes — two separate files (intro + body) are processed independently.

### 2. Run Audio-Only Clip Plan

For each content section, run the deterministic audio cleanup tool to generate keep-segments. This handles silence, breaths, fillers, and noise — but NOT false starts (that requires language understanding, handled in step 3).

**Intro clipping:**
```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping
npx tsx generate-clip-plan.ts \
  --analysis "{analysis_dir}/intro/audio-analysis.json" \
  --video "{clips_dir}/intro-proxy-split.mp4" \
  --type intro \
  --output "{clips_dir}/intro-keep-segments.json"
```

**Body clipping:**
```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping
npx tsx generate-clip-plan.ts \
  --analysis "{analysis_dir}/body/audio-analysis.json" \
  --video "{clips_dir}/body-proxy-split.mp4" \
  --type main \
  --output "{clips_dir}/body-keep-segments.json"
```

### 3. Transcript Content Analysis (Common Sense False Start Check)

**Why this step exists:** False start detection requires language understanding — distinguishing intentional rhetorical repetition (e.g., anaphora like "you don't need to X... you don't need to Y...") from genuine retakes where the speaker stumbled and restarted. No heuristic can do this reliably. You (the agent) can.

**For each content section (intro, body):**

1. **Read the transcript JSON** (`{analysis_dir}/{content_type}/refined-transcript.json`) and the **script** (`{script_path}`)
2. **Read the keep-segments** from the clip plan generated in step 2
3. **Compare transcript against script** — understand what was said vs what was scripted
4. **Identify genuine false starts** — look for passages where the speaker:
   - Starts a sentence or phrase
   - Stops or pauses (visible as a silence/breath gap in the audio)
   - Restarts the **same thought** from the beginning

5. **Critical distinction — what is NOT a false start:**
   - **Intentional rhetorical repetition (anaphora):** Phrases that share the same opening but have **different completions** and flow naturally (e.g., "you don't need to be a developer... you don't need to know what an API is"). These are deliberate emphasis — do NOT cut.
   - **Callbacks/references:** Speaker revisiting a phrase from earlier for emphasis or structure
   - **Lists with repeated structure:** "First you do X... then you do Y... then you do Z..."

6. **For each genuine false start identified:**
   - Note the timestamp range (startMs → endMs)
   - Modify the keep-segments JSON to exclude it (split or trim the affected segment)
   - Keep the **clean take** (the second, completed version)

7. **Log findings concisely and proceed:**

Log any false starts found: "**False starts cut:** {count} ({total_duration}s removed)"
Log any preserved anaphora: "**Anaphora preserved:** {count} instances"

Auto-apply all modifications to keep-segments and proceed directly to FFmpeg execution — no checkpoint needed. False start detection is autonomous; the agent makes the call.

### 4. Proceed to FFmpeg Execution

No review checkpoint. The clip plan is generated and false starts are handled — proceed directly to executing the clips.

### 5. Execute FFmpeg Clipping (⚡ all 4 clips in parallel)

**Run ALL 4 FFmpeg clip commands simultaneously as background processes.** These are independent operations on different input/output files:

```bash
# Launch all 4 clips in parallel
bash {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping/clip-video.sh \
  --keep-segments "{clips_dir}/intro-keep-segments.json" \
  --input "{intro_proxy_path}" \
  --output "{clips_dir}/intro-clipped.mp4" &
PID_INTRO_PROXY=$!

bash {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping/clip-video.sh \
  --keep-segments "{clips_dir}/intro-keep-segments.json" \
  --input "{intro_raw_path}" \
  --output "{clips_dir}/intro-clipped-raw.mp4" &
PID_INTRO_RAW=$!

bash {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping/clip-video.sh \
  --keep-segments "{clips_dir}/body-keep-segments.json" \
  --input "{body_proxy_path}" \
  --output "{clips_dir}/body-clipped.mp4" &
PID_BODY_PROXY=$!

bash {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping/clip-video.sh \
  --keep-segments "{clips_dir}/body-keep-segments.json" \
  --input "{body_raw_path}" \
  --output "{clips_dir}/body-clipped-raw.mp4" &
PID_BODY_RAW=$!

# Wait for all and check exit codes
wait $PID_INTRO_PROXY || echo "FAILED: intro-proxy clip"
wait $PID_INTRO_RAW || echo "FAILED: intro-raw clip"
wait $PID_BODY_PROXY || echo "FAILED: body-proxy clip"
wait $PID_BODY_RAW || echo "FAILED: body-raw clip"
```

If any clip fails, report the failure and halt — do not proceed with partial clips.

### 6. Remap Transcripts to Clipped Timeline (⚡ both remaps in parallel)

Deterministically remap word timestamps from the original timeline to the clipped timeline using keep-segments. This is pure math — no re-transcription needed. **⚡ Run both intro and body remaps in parallel** (they are independent, pure-math operations).

**Algorithm (per word):**
1. Find which keep-segment contains the word's original timestamp
2. Calculate the cumulative duration of all previous keep-segments
3. New timestamp = cumulative_previous_duration + (word_original_timestamp - segment_start)

For each content type, produce:
- `{clips_dir}/intro-clipped-transcript.json`
- `{clips_dir}/body-clipped-transcript.json`

Each clipped transcript has the same word entries as the original but with remapped `start` and `end` timestamps.

### 7. Probe Clipped Videos + Launch Early Audio Concat

Probe all clipped files for duration and frame count:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,nb_frames,duration \
  -of json "{clips_dir}/{content_type}-clipped.mp4"
```

Store `{intro_clipped_duration}`, `{body_clipped_duration}`, `{intro_clipped_frames}`, `{body_clipped_frames}`.

**⚡ Per-Clip Audio Extraction:** Immediately after probing confirms all clips are valid, extract audio from each clipped video as **background processes**. This removes them from the critical path — they run during VA + storyboard instead of blocking step 5. Stream copy preserves the exact audio timeline from each clipped video with no re-encode and no drift.

```bash
ffmpeg -i "{clips_dir}/intro-clipped.mp4" -vn -acodec copy \
  "{remotion_dir}/public/intro-audio.m4a" &
PID_INTRO_AUDIO=$!
ffmpeg -i "{clips_dir}/body-clipped.mp4" -vn -acodec copy \
  "{remotion_dir}/public/body-audio.m4a" &
PID_BODY_AUDIO=$!
```

NEVER concatenate these into a single file — concatenation includes dead-air already removed from the video, causing 500ms+ sync drift (see `wiki/audio-sync.md`). The extractions will be verified in section 8c.

### 8. Clipping Complete — FIRST COLLAB CHECKPOINT

This is the first point where the pipeline pauses in Collab mode. Everything before this (boundary detection, false start removal, clip plan generation, FFmpeg execution, transcript remap) runs autonomously.

"**Clipping Complete**

| Content | Original | Clipped | Removed | Frames | File |
|---------|----------|---------|---------|--------|------|
| Intro | {orig}s | {clip}s | {rem}s ({pct}%) | {frames} | intro-clipped.mp4 |
| Body | {orig}s | {clip}s | {rem}s ({pct}%) | {frames} | body-clipped.mp4 |
| **Total** | — | **{intro+body}s** | — | — | — |

{If false starts were found: **False starts removed:** {count} ({duration}s)}
{If anaphora preserved: **Anaphora preserved:** {count} instances}

**Clipped files ready for review:**
- `{clips_dir}/intro-clipped.mp4`
- `{clips_dir}/body-clipped.mp4`

[C] Continue to visual analysis + storyboard | [P] Play clipped files (show paths for manual review)"

**AUTO mode:** Auto-proceed to visual analysis.

### 8b. Visual Analysis on Clipped Videos (⚡ both VA calls in parallel)

Run Gemini visual analysis on the **clipped proxy** videos (not the originals). Because VA runs on clipped footage, the timestamps directly match the clipped timeline — no remap needed for storyboarding.

**⚡ Launch BOTH Gemini VA calls simultaneously** — they are independent API calls that just need their respective clipped proxy files. This saves ~5 min (one ~5min call instead of two ~5min calls sequentially).

**Frame extraction rates by content type:**
- `{clips_dir}/intro-clipped.mp4` at **1 fps** — intro is short, captures rapid visual changes, MG timing, speaker energy shifts
- `{clips_dir}/body-clipped.mp4` at **0.2 fps** (1 frame every 5 seconds) — body is long, captures screen share transitions, section changes

Use the Gemini prompt from `{project-root}/video-plugin/skills/1-video-editor/workflows/visual-analysis/data/gemini-prompt.md`.

Save output to:
- `{analysis_dir}/intro/visual-analysis.json`
- `{analysis_dir}/body/visual-analysis.json`

Wait for both VA calls to complete before proceeding.

Log VA summary and auto-proceed — no checkpoint for VA results.

### 8c. Verify Per-Clip Audio Extraction

Before proceeding to the next step, verify the per-clip audio extractions launched in section 7 have completed:

```bash
wait $PID_INTRO_AUDIO || echo "FAILED: intro audio extraction"
wait $PID_BODY_AUDIO || echo "FAILED: body audio extraction"
```

Verify each file:
- `{remotion_dir}/public/intro-audio.m4a`: exists, is playable, duration matches `intro_clipped_duration` (within ±0.1s)
- `{remotion_dir}/public/body-audio.m4a`: exists, is playable, duration matches `body_clipped_duration` (within ±0.1s)

If either extraction failed, re-run that extraction in the foreground before proceeding. Store verification result so step 5 knows per-clip audio is already extracted.

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Single-file: raw and proxy split at boundary before clipping
- Single-file: split verified for first-frame decodability (re-encode fallback if needed)
- Intro clipped with 150ms buffer (aggressive — content_type intro)
- Body clipped with 300ms buffer (conservative — content_type main)
- Keep-segments generated for both content sections (audio-only cleanup)
- Transcript analysed for false starts using common sense (not heuristics)
- Intentional rhetorical repetition (anaphora) correctly preserved — NOT flagged as false starts
- Genuine false starts (stumbles/retakes) identified and keep-segments modified
- FFmpeg executed to produce clipped proxy and raw files
- Transcripts deterministically remapped to clipped timelines (no re-transcription)
- Clipped videos probed for duration and frame count
- Visual analysis run on **clipped** videos (intro @ 1fps, body @ 0.2fps)
- VA timestamps directly match clipped timeline (no remap needed)
- From step 3 onwards, pipeline is identical regardless of recording mode

### ❌ SYSTEM FAILURE:

- Using same buffer threshold for both intro and body
- Re-running DeepGram transcription after clipping instead of remapping
- Not splitting single-file recordings before clipping
- Not clipping both proxy AND raw files
- Skipping transcript remap
- Non-deterministic transcript adjustment (e.g., re-transcribing clipped audio)
- Running visual analysis on original/unclipped videos instead of clipped versions
- Skipping visual analysis entirely (it must run in this step, not step-02)
- Using programmatic/heuristic false start detection instead of common sense transcript analysis
- Cutting intentional rhetorical repetition (anaphora) as if it were a false start
