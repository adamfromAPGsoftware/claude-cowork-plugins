---
name: 'step-01-init'
description: 'Discover filmed landscape videos, generate 720p proxies, load scripts and creative plans, validate all inputs'

nextStepFile: './step-02-batch-analysis.md'
---

# Step 1: Initialize — Discover Videos, Generate Proxies, Load Plans

## STEP GOAL:

Discover the 5 user-filmed 4K landscape (16:9) videos in the short-form folder, generate 720p proxy versions for analysis, match each to its corresponding script/creative plan from the Copywriter SS workflow, and validate all inputs before proceeding to analysis.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 AUTO-PROCEED: Minimal user interaction — auto-detect from file structure
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video editing automation specialist
- ✅ Technical, concise, efficient communication
- ✅ Execute with precision — creative decisions already made by Copywriter SS

### Step-Specific Rules:

- 🎯 Focus ONLY on input discovery, proxy generation, matching, and validation
- 🎯 Combined Recording Flow REQUIRES audio analysis + transcription for precise splitting — this is the ONE exception to "no analysis in init"
- 🚫 FORBIDDEN to proceed without all 5 video-script pairs validated
- 🎯 Proxies are generated programmatically — no user action needed

## MANDATORY SEQUENCE

### 1. Discover Filmed Videos

"**Short-Form Pipeline — Initialization**"

Scan `{project_folder}/{project-slug}/video-editor/short-form/` for raw video files.

**First, check for combined recording:** Look for `sf-all-raw.mp4` in the short-form folder root.

- **If `sf-all-raw.mp4` exists** → enter **Combined Recording Flow** (sections 1b–1d below), which will split it into 5 individual files in `raw/`, then continue from section 2 onwards.
- **If `sf-all-raw.mp4` does NOT exist** → proceed with **Individual Recording Flow** (existing behavior below).

#### Individual Recording Flow

Expected naming: `sf-01.mp4`, `sf-02.mp4`, ... `sf-05.mp4` (in the short-form root, where the user drops them)

Also check for alternate naming patterns: `sf-01-raw.mp4`, `SF01.mp4`, `sf_01.mp4`, etc.

If files use different naming, attempt to match by order or ask user to confirm mapping.

Once discovered, move (or copy) the raw files into the `raw/` subdirectory:
```bash
mkdir -p "{project_folder}/{project-slug}/video-editor/short-form/raw"
mv "{project_folder}/{project-slug}/video-editor/short-form/sf-{NN}.mp4" \
   "{project_folder}/{project-slug}/video-editor/short-form/raw/sf-{NN}.mp4"
```

**For each video found, probe with ffprobe:**

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration \
  -show_entries format=duration,size \
  -of json "{video_path}"
```

"**Filmed Videos Found:**

| # | File | Resolution | Duration | Size | Orientation |
|---|------|-----------|----------|------|-------------|
| SF-01 | sf-01.mp4 | {W}x{H} | {X}s | {Y}MB | {portrait/landscape} |
| SF-02 | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |"

**Validation:**
- ✅ If landscape (width > height), confirmed. Expected format.
- ⚠️ If any video is vertical (height > width):
  - **COLLAB mode:** Warn: "SF-{NN} appears to be vertical. Source should be landscape (16:9) for split-screen support. Confirm?"
  - **AUTO mode:** Warn but continue with centre-crop assumption.

Skip to section 2.

### 1b. Generate Combined Proxy (Combined Recording Flow only)

Probe the combined recording with ffprobe:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration \
  -show_entries format=duration,size \
  -of json "{project_folder}/{project-slug}/video-editor/short-form/sf-all-raw.mp4"
```

Generate a 720p proxy of the combined recording:

```bash
mkdir -p "{project_folder}/{project-slug}/video-editor/short-form/proxies"
ffmpeg -i "{project_folder}/{project-slug}/video-editor/short-form/sf-all-raw.mp4" \
  -vf "scale=720:-2" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-all-proxy.mp4"
```

Validate the proxy with ffprobe (file exists, 720px wide, duration matches raw).

"**Combined recording detected:** `sf-all-raw.mp4`
**Duration:** {X}s | **Resolution:** {W}x{H} | **Proxy:** proxies/sf-all-proxy.mp4 generated ✅"

### 1c. Analyse & Transcribe Combined Recording (Combined Recording Flow only)

Run the full audio analysis pipeline on the combined proxy — the same approach used for main/intro videos. This gives precise classified regions (SPEECH, SILENCE, BREATH, NOISE) with millisecond boundaries, which are far more reliable than transcript-only silence detection for finding the inter-script pauses.

Ensure the `analysis/` directory exists before proceeding.

#### Audio Analysis

```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
npx tsx analyze-audio.ts \
  --video "{project_folder}/{project-slug}/video-editor/short-form/sf-all-proxy.mp4" \
  --output "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-all-audio-analysis.md" \
  --content-type short
```

This produces:
- `sf-all-audio-analysis.md` — human-readable analysis
- `sf-all-audio-analysis.json` — machine-readable classified regions (auto-generated sidecar)

#### Transcription

Transcribe the combined proxy using DeepGram Nova-3 API for word-level timestamps. The API key is in `.env` as `DEEPGRAM_API_KEY`.

```bash
curl -X POST "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&utterances=true&punctuate=true&diarize=false&detect_language=false&language=en" \
  --header "Authorization: Token ${DEEPGRAM_API_KEY}" \
  --header "Content-Type: audio/mp4" \
  --data-binary @"{project_folder}/{project-slug}/video-editor/short-form/sf-all-proxy.mp4"
```

Save the full transcript response to:
`{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-all-transcript.json`

### 1d. Match & Split (Combined Recording Flow only)

Split the combined recording into 5 individual video files using audio analysis classified regions + transcript validation. This uses the same precision approach as the main/intro clipping pipeline.

**Step 1 — Load scripts:**
Load all 5 script files from `short-form/scripts/sf-{NN}-script.md` (NN = 01–05).
Extract the spoken text only (Hook + Body + CTA words) from each script.

**Step 2 — Detect inter-script boundaries using audio analysis:**
From `sf-all-audio-analysis.json`, find all SILENCE regions ≥ 2000ms in the `classified_regions` array. These correspond to the ~3-second pauses Adam left between scripts.

Sort these long silence regions by start time. Select exactly 4 boundaries — if more than 4 silences ≥ 2s exist, select the 4 longest (these are the deliberate inter-script pauses, not mid-sentence hesitations).

For each boundary silence region, the split point is the **midpoint** of the silence: `splitMs = (startMs + endMs) / 2`.

This gives 5 segments:
- Segment 1: 0 → split₁
- Segment 2: split₁ → split₂
- Segment 3: split₂ → split₃
- Segment 4: split₃ → split₄
- Segment 5: split₄ → end

**Step 3 — Cross-reference with transcript for precise speech boundaries:**
Within each segment, use the transcript word-level timestamps to find:
- **First spoken word** timestamp → segment speech start
- **Last spoken word** timestamp → segment speech end

Apply a 300ms buffer before first word and after last word. This handles any leading/trailing breath or mouth noise within each segment.

**Step 4 — Detect and exclude false starts within segments:**
Within each segment's transcript words, check for **false starts** — short bursts of speech followed by a restart of the same phrase. Indicators:
- A word or short phrase (1–3 words) followed by a silence ≥ 500ms, then the same or very similar words repeated
- Isolated noise/cough regions (NOISE classification in audio analysis) within the segment
- BREATH regions > 300ms mid-sentence (indicates a restart point)

When a false start is detected, trim the segment start to begin AFTER the false start (at the restart point). Log the false start for the summary report.

**Step 5 — Validate segments against scripts:**
For each of the 5 segments, compare the transcript text to the expected script text using token overlap:
1. Tokenize both the transcript segment and the script text (lowercase, strip punctuation)
2. Calculate overlap ratio: `|intersection| / |script_tokens|`
3. Threshold: overlap ratio must be > 0.6 for a valid match

If validation fails for any segment:
- **COLLAB mode:** Warn and present the segment boundaries for user confirmation: "Segment {N} has low match confidence ({ratio}). Expected: '{first 10 words of script}...'. Got: '{first 10 words of transcript}...'. [C] Confirm | [A] Adjust boundaries"
- **AUTO mode:** Warn but proceed: "⚠️ Segment {N} match confidence is {ratio} — proceeding with best-effort split."

**Step 6 — Split the raw recording:**
For each validated segment, split using FFmpeg with lossless copy. Use the refined boundaries from steps 3–4 (after false start exclusion):

```bash
mkdir -p "{project_folder}/{project-slug}/video-editor/short-form/raw"
ffmpeg -i "{project_folder}/{project-slug}/video-editor/short-form/sf-all-raw.mp4" \
  -ss {start} -to {end} -c copy \
  "{project_folder}/{project-slug}/video-editor/short-form/raw/sf-{NN}.mp4"
```

**Important:** These are coarse splits at the inter-script boundaries. Each individual `sf-{NN}.mp4` still contains its full take including any mid-script hesitations, breaths, and fillers. The precision cleanup (cutting fillers, compressing silences, trimming breaths) happens in step-02 when each video goes through the full AA → TR → VC pipeline with `short` content type thresholds.

"**Combined recording split into 5 videos:**

| # | Start | End | Duration | Match | False Starts | File |
|---|-------|-----|----------|-------|-------------|------|
| SF-01 | {start}s | {end}s | {dur}s | {ratio} | {count} excluded | raw/sf-01.mp4 ✅ |
| SF-02 | ... | ... | ... | ... | ... | raw/sf-02.mp4 ✅ |
| SF-03 | ... | ... | ... | ... | ... | raw/sf-03.mp4 ✅ |
| SF-04 | ... | ... | ... | ... | ... | raw/sf-04.mp4 ✅ |
| SF-05 | ... | ... | ... | ... | ... | raw/sf-05.mp4 ✅ |

**Analysis files saved:** `analysis/sf-all-audio-analysis.json`, `analysis/sf-all-transcript.json`
**Split method:** Audio analysis classified regions (SILENCE ≥ 2s) + transcript validation"

After splitting, the 5 individual files exist and the rest of the pipeline continues as normal from section 2 onwards.

### 2. Generate 720p Proxies

For each raw video, generate a 720p proxy for use in analysis, transcription, and clipping. The raw 4K files are preserved for final Remotion render.

**FFmpeg proxy generation command (per video):**

```bash
mkdir -p "{project_folder}/{project-slug}/video-editor/short-form/proxies"
ffmpeg -i "{project_folder}/{project-slug}/video-editor/short-form/raw/sf-{NN}.mp4" \
  -vf "scale=720:-2" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-{NN}-proxy.mp4"
```

**`scale=720:-2` explained:** Sets width to 720px, calculates height to maintain aspect ratio (rounded to nearest even number). For a 3840×2160 (4K landscape) source, this produces 720×405. For 1920×1080 (HD landscape), this produces 720×405.

Run all 5 proxies sequentially and report:

"**Proxies Generated:**

| # | Raw | Proxy | Raw Size | Proxy Size | Reduction |
|---|-----|-------|----------|------------|-----------|
| SF-01 | raw/sf-01.mp4 (2160×3840) | proxies/sf-01-proxy.mp4 (720×1280) | {X}MB | {Y}MB | {Z}% |
| SF-02 | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |"

**Verify each proxy:**
- File exists and is playable (ffprobe succeeds)
- Resolution is 720px wide
- Duration matches raw file (within ±0.1s)
- Audio track present

### 3. Load Script / Creative Plans

For each video, load its corresponding script from:
`{project_folder}/{project-slug}/video-editor/short-form/scripts/sf-{NN}-script.md`

Extract from each script:
- Script text (Hook → Body → CTA)
- Duration category (Punchy / Standard / Deep) and target duration
- B-roll extraction plan (timestamps + descriptions)
- MG prompts (Hera prompts + references)
- Conceptual storyboard (beat-by-beat visual plan)
- Word count and validation results

### 4. Validate All Pairs

For each of the 5 videos:
- ✅ Raw video file exists and is playable (ffprobe succeeds)
- ✅ Proxy video generated and verified
- ✅ Script file exists and has all 4 sections (script, B-roll plan, MG prompts, storyboard)
- ✅ Duration category assigned

"**Video-Script Pairs:**

| # | Video | Proxy | Duration | Category | Script | B-Roll | MG | Status |
|---|-------|-------|----------|----------|--------|--------|-----|--------|
| SF-01 | raw/sf-01.mp4 | proxies/sf-01-proxy.mp4 | {X}s | {Punchy} | sf-01-script.md | {count} | {count} | ✅ |
| SF-02 | ... | ... | ... | ... | ... | ... | ... | ✅ |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |"

### 5. Create Registry YAMLs

For each video, create **two** registry YAMLs:

**Raw registry:** `{project_folder}/{project-slug}/video-editor/short-form/raw/sf-{NN}-raw.yaml`

```yaml
video_id: sf-{NN}-raw
content_type: short
role: raw
paired_with: sf-{NN}-proxy
format: landscape
metadata:
  filename: sf-{NN}.mp4
  resolution: '{W}x{H}'
  duration: '{duration}'
  frame_rate: '{fps}fps'
  file_size: '{size}'
  source_path: '{absolute_path_to_raw}'
registered_at: '{current_date}'
```

**Proxy registry:** `{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-{NN}-proxy.yaml`

```yaml
video_id: sf-{NN}-proxy
content_type: short
role: proxy
paired_with: sf-{NN}-raw
format: landscape
metadata:
  filename: sf-{NN}-proxy.mp4
  resolution: '720x{H}'
  duration: '{duration}'
  frame_rate: '{fps}fps'
  file_size: '{size}'
  encoder: 'FFmpeg libx264 crf23'
  source_path: '{absolute_path_to_proxy}'
registered_at: '{current_date}'
```

### 6. Create Output Directories

Ensure these directories exist:
- `short-form/raw/` (individual raw video files + raw registry YAMLs)
- `short-form/proxies/` (720p proxy files + proxy registry YAMLs)
- `short-form/analysis/sf-{NN}/` (for each video)
- `short-form/clips/`
- `short-form/storyboard/`
- `short-form/motion-graphics/`
- `short-form/remotion/sf-{NN}/` (for each video)
- `short-form/renders/` (final rendered MP4s)

### 7. Summary and Proceed

"**Initialization Complete**

| Setting | Value |
|---------|-------|
| Recording mode | {Combined / Individual} |
| Videos found | {count}/5 |
| Proxies generated | {count}/5 |
| Scripts loaded | {count}/5 |
| Content type | short |
| Raw resolution | {W}x{H} (4K landscape) |
| Proxy resolution | 720x{H} |
| Processing order | SF-01 → SF-05 (sequential) |
| Duration mix | {X} Punchy + {Y} Standard + {Z} Deep |

**Pipeline path:**
- **Proxy** (720p, in `proxies/`) → used for audio analysis, transcription, clipping
- **Raw** (4K, in `raw/`) → used for final Remotion render
- **Renders** → final MP4s output to `renders/`

**Proceeding to batch analysis...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Combined recording detected and split into 5 individual files (if `sf-all-raw.mp4` present), OR all 5 individual files discovered
- Combined split used full audio analysis pipeline (`analyze-audio.ts`) + transcript for precision boundary detection
- False starts detected and excluded from split boundaries
- All 5 raw video files validated via ffprobe
- All 5 proxies generated at 720p with matching duration in `proxies/`
- Raw files organized in `raw/`, proxies in `proxies/`
- All 5 scripts loaded with complete sections
- Raw and proxy registry YAMLs created alongside their videos
- Output directories created (including `renders/`)
- All pairs validated

### ❌ SYSTEM FAILURE:

- Proceeding with fewer than 5 video-script pairs
- Not generating proxies (trying to use 4K files for analysis)
- Proxy duration doesn't match raw duration
- Not validating video files with ffprobe
- Using transcript-only silence gap detection for combined split (must use audio analysis classified regions)
- Not creating both raw and proxy registry YAMLs
- Combined recording found but not split (skipping sections 1b–1d)
