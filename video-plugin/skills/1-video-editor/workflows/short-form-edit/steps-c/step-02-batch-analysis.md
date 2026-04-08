---
name: 'step-02-batch-analysis'
description: 'Run audio analysis, transcription, and video clipping per video using 720p proxies with short content-type thresholds'

nextStepFile: './step-03-storyboard.md'
---

# Step 2: Batch Analysis — AA → TR → VC per Video (Using Proxies)

## STEP GOAL:

Run the audio analysis, transcription, and video clipping pipelines for each of the 5 short-form videos using the **720p proxy** files and the `short` content type thresholds (100ms buffer, zero silence tolerance, always cut fillers).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 Process all 5 videos in parallel — each is independent (separate proxy, separate output dir)
- 🎯 Use **proxy files** (`proxies/sf-{NN}-proxy.mp4`) for all analysis — NOT the raw 4K files
- 🚫 FORBIDDEN to use raw 4K files for analysis (wastes time, identical results)
- 🚫 Visual analysis is intentionally excluded (not needed for short-form speaker-to-camera)
- 📋 Use `--content-type short` for all audio analysis and clipping commands
- 🎯 Each video gets: Audio Analysis → Transcription → Video Clipping

## MANDATORY SEQUENCE

### 1. Process All Videos in Parallel (5 Sub-Agents)

Spawn **5 sub-agents in parallel** using the Agent tool — one per video. Each sub-agent runs the full AA → TR → Refine → VC → C2 chain for its video independently.

**Sub-agent spawn pattern:**
```
Use the Agent tool to spawn 5 sub-agents in a SINGLE message (all parallel):

Sub-agent SF-01: "Run the full analysis chain for SF-01..."
Sub-agent SF-02: "Run the full analysis chain for SF-02..."
Sub-agent SF-03: "Run the full analysis chain for SF-03..."
Sub-agent SF-04: "Run the full analysis chain for SF-04..."
Sub-agent SF-05: "Run the full analysis chain for SF-05..."
```

Each sub-agent receives the full per-video pipeline instructions (sections A through C2 below) and executes them autonomously. Each sub-agent reports back:
- Success/failure status
- Original duration, cleaned duration, reduction %
- Keep segment count, fillers cut count
- Any errors or warnings encountered

**Why sub-agents over bash background jobs:** Each analysis chain involves multiple sequential commands with error handling (AA → TR → Refine → VC → C2). A sub-agent can check intermediate outputs, retry on failure, verify `ffprobe` durations, and report structured results. Background bash jobs would need complex error propagation.

The main agent collects all 5 sub-agent results and presents the summary table (section 2).

#### Per-Video Pipeline (run for SF-01 through SF-05 in parallel)

For each video `sf-{NN}`, use the **proxy** path:
`{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-{NN}-proxy.mp4`

#### A. Audio Analysis

Run the audio analysis script with `short` content type on the **proxy**:

```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
npx tsx analyze-audio.ts \
  --video "{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-{NN}-proxy.mp4" \
  --output "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/audio-analysis.md" \
  --content-type short
```

This produces:
- `audio-analysis.md` — human-readable analysis
- `audio-analysis.json` — machine-readable analysis (auto-generated sidecar)

**Why proxy is fine for audio analysis:** Audio analysis only needs the audio track, which is identical between proxy and raw. The proxy's smaller file size means faster FFmpeg extraction.

#### B. Transcription

Run the existing transcription workflow (DeepGram) on the **proxy**:
- Use the same DeepGram pipeline as the long-form transcription workflow
- Input: `sf-{NN}-proxy.mp4` (proxy — audio track is identical to raw)
- Output to: `{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/transcript.json`

**Why proxy is fine for transcription:** DeepGram only processes the audio stream. Proxy and raw have identical audio.

#### B2. Refine Transcript Timing

Run the transcript refinement script to calibrate DeepGram word timestamps against the audio waveform:

```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
npx tsx refine-transcript.ts \
  --transcript "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/transcript.json" \
  --sidecar "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/audio-analysis-sidecar.json" \
  --output "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/refined-transcript.json"
```

This cross-references each word's DeepGram timestamp with the 20ms-granularity VAD probability curve to find actual speech onset/offset, correcting drift up to +/-300ms.

This produces:
- `refined-transcript.json` — same format as `transcript.json` with corrected word start/end times and `originalStart`/`originalEnd` fields for debugging

**Why this matters:** DeepGram word timestamps can drift up to ~500ms. The refined transcript ensures caption bursts in step 3 align with actual speech rhythm rather than equal-time distribution.

#### C. Video Clipping

Run the clip plan generator with `short` content type:

```bash
cd {project-root}/video-plugin/skills/1-video-editor/workflows/video-clipping
npx tsx generate-clip-plan.ts \
  --analysis "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/audio-analysis.json" \
  --video "{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-{NN}-proxy.mp4" \
  --type short \
  --output "{project_folder}/{project-slug}/video-editor/short-form/clips/sf-{NN}-clip-plan.md"
```

Or use the wrapper script:

```bash
./clip-video.sh \
  --video "{project_folder}/{project-slug}/video-editor/short-form/proxies/sf-{NN}-proxy.mp4" \
  --type short \
  --output-dir "{project_folder}/{project-slug}/video-editor/short-form/clips/"
```

This produces:
- `sf-{NN}-clip-plan.md` — clip plan with FFmpeg commands
- `sf-{NN}-keep-segments.json` — segments to keep (timestamps apply to both proxy and raw)
- `sf-{NN}-content-cuts.json` — what was cut

**Important:** The timestamps in keep-segments.json and content-cuts.json are time-based (milliseconds), not resolution-dependent. They apply equally to both the proxy and the raw 4K file. The Remotion render (step 05) will use these same timestamps against the raw 4K source.

#### C2. Post-Clip Transcription (Clipped Timeline)

After video clipping produces a cleaned proxy, re-run the transcription pipeline on the **clipped** video to get word timestamps that are **native to the clipped video timeline** — no offset math needed downstream.

**Why this is needed:** The pre-clip `refined-transcript.json` uses timestamps from the original unclipped video. Converting those to the clipped timeline requires accumulating offsets across every removed gap, which causes drift (e.g., SF-01 showed ~40-frame drift by later segments). Running transcription on the clipped proxy gives timestamps that directly correspond to the clipped video's timeline.

**Cost:** ~$0.002 per clip (DeepGram Nova-3 on 15-25s audio) + ~5s local processing.

1. **Run DeepGram on the clipped proxy:**
   - Input: `{project_folder}/{project-slug}/video-editor/short-form/clips/sf-{NN}-cleaned.mp4`
   - Output: `{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/clipped-transcript.json`
   - Use the same DeepGram pipeline as section B above

2. **Run audio analysis on the clipped proxy:**
   ```bash
   cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
   npx tsx analyze-audio.ts \
     --video "{project_folder}/{project-slug}/video-editor/short-form/clips/sf-{NN}-cleaned.mp4" \
     --output "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/clipped-audio-analysis.md" \
     --content-type short
   ```
   This produces:
   - `clipped-audio-analysis.md` — human-readable analysis of the clipped audio
   - `clipped-audio-analysis-sidecar.json` — VAD curve for the clipped timeline

3. **Run refine-transcript on the clipped transcript:**
   ```bash
   cd {project-root}/video-plugin/skills/1-video-editor/workflows/audio-analysis
   npx tsx refine-transcript.ts \
     --transcript "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/clipped-transcript.json" \
     --sidecar "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/clipped-audio-analysis-sidecar.json" \
     --output "{project_folder}/{project-slug}/video-editor/short-form/analysis/sf-{NN}/clipped-refined-transcript.json"
   ```
   This produces:
   - `clipped-refined-transcript.json` — VAD-calibrated word timestamps native to the clipped video timeline

**Verification:** Compare the last word's end time in `clipped-refined-transcript.json` against the clipped proxy duration (via `ffprobe -v error -show_entries format=duration -of csv=p=0 clips/sf-{NN}-cleaned.mp4`). They should be within 0.5s of each other.

### 2. Summary Report

After all 5 videos are processed:

"**Batch Analysis Complete**

| # | Category | Original | Cleaned | Reduction | Keep Segments | Fillers Cut |
|---|----------|----------|---------|-----------|---------------|-------------|
| SF-01 | {Punchy} | {X}s | {Y}s | {Z}% | {count} | {count} |
| SF-02 | {Standard} | {X}s | {Y}s | {Z}% | {count} | {count} |
| ... | ... | ... | ... | ... | ... | ... |

**Content type:** short (100ms buffer, zero silence tolerance)
**Analysis source:** 720p proxies (timestamps apply to raw 4K for render)
**Visual analysis:** Skipped (not needed for speaker-to-camera)

**Proceeding to storyboard generation...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 5 videos processed through AA → TR → VC
- **Proxy files** used for all analysis (not raw 4K)
- `short` content type used for all analysis
- Refined transcript generated for each video (B2)
- Audio analysis, transcript, refined transcript, and clip plan generated for each video
- `clipped-refined-transcript.json` generated for each video (C2) with timestamps native to clipped timeline
- Summary report presented with metrics

### ❌ SYSTEM FAILURE:

- Using raw 4K files for analysis instead of proxies
- Using `intro` or `main` content type instead of `short`
- Running visual analysis (intentionally excluded)
- Skipping any video
- Skipping transcript refinement (B2) before video clipping
- Not generating all 4 outputs per video (audio-analysis, transcript, refined-transcript, clip-plan)
- Not generating `clipped-refined-transcript.json` for each video after clipping (C2)
- Missing any of the 3 clipped-timeline outputs per video (clipped-transcript, clipped-audio-analysis, clipped-refined-transcript)
