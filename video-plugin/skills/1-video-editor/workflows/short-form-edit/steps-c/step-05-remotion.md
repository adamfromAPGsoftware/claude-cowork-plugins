---
name: 'step-05-remotion'
description: 'Scaffold, build, QA, and render each vertical Remotion project at source-matched 4K resolution'

templateLibraryData: '../data/vertical-template-library.md'
segmentPatternsData: '../data/vertical-segment-patterns.md'
hardRulesData: '../data/vertical-remotion-hard-rules.md'
sfThumbnailStyleGuide: '{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/data/short-form-style-guide.md'
---

# Step 5: Remotion — Scaffold, Build, QA, Render

## STEP GOAL:

For each of the 5 short-form videos, scaffold a 9:16 vertical Remotion project at source-matched resolution (e.g. 2160×3840 for 4K source), generate all segment files from the storyboard, run QA against all 25 rules (19 base + 6 vertical), and render the final MP4 at near-lossless quality.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 **Phase A (scaffold + codegen):** Spawn sub-agents to scaffold all 5 videos in parallel — scaffolding only needs the storyboard, NOT the MG video files
- 🎯 **Phase B (asset copy + render):** Sequential per video — copy MGs to `public/`, QA, then render. Renders are CPU-bound and must be sequential.
- 📖 Load {templateLibraryData}, {segmentPatternsData}, and {hardRulesData} before starting
- 🎯 Every project MUST pass QA before rendering
- 🚫 FORBIDDEN to render without passing QA
- 🎯 Use **cleaned 4K files** (not raw or proxies) for Remotion — raw files have a different timeline than the cleaned audio used for composition timing. Generate cleaned 4K clips from raw sources using the clip plan FFmpeg commands before scaffolding.
- 🎯 Probe cleaned 4K file with ffprobe to get actual fps/resolution for PROJECT config — do NOT hardcode
- 🎯 **Intermediate encoding quality**: ALL FFmpeg operations on source video (cleaning, trimming, concat) MUST use near-lossless quality settings. See "Intermediate Encoding Quality" section below.
- 🎯 **Render must include `--crf 15`** — never omit CRF from the render command

## MANDATORY SEQUENCE

### 1. Load Reference Data

Load and read:
- {templateLibraryData} — vertical template catalog
- {segmentPatternsData} — V1–V7 code generation patterns
- {hardRulesData} — 5 vertical hard rules (supplements 19 base rules)
- Also load: `{project-root}/video-plugin/skills/1-video-editor/workflows/remotion-edit/data/remotion-hard-rules.md` — 19 base rules
- {sfThumbnailStyleGuide} — short-form thumbnail composition, typography, and prompt template (used in Section G2b)

### 1b. Pre-Scaffold: Generate Cleaned 4K Clips

Before scaffolding, generate cleaned 4K clips from the raw sources using the clip plan FFmpeg commands. This ensures the Remotion source files have the same timeline as the composition timing (which was derived from cleaned audio analysis).

**Why:** Raw source files have silences and gaps that were removed during analysis. The composition frame counts, segment boundaries, and `videoStartFrom` values are all based on the cleaned timeline. Using raw files causes audio/video desync, audio cutoff at the end, and MG timing mismatches.

**For each SF-01 through SF-05:**

```bash
# Adapt the clip plan's FFmpeg command to use the raw 4K source
# Input: raw/sf-{NN}.mp4 (3840x2160 @ 60fps)
# Quality: -c:v libx264 -crf 15 -preset medium -c:a aac -b:a 256k
# Output: clips/sf-{NN}-cleaned-4k.mp4

ffmpeg -y -i "raw/sf-{NN}.mp4" -filter_complex "
  {filter_complex from clips/sf-{NN}-clip-plan.md}
" -map "[outv]" -map "[outa]" \
  -c:v libx264 -crf 15 -preset medium \
  -c:a aac -b:a 256k \
  "clips/sf-{NN}-cleaned-4k.mp4"
```

**Run all 5 in parallel** (they read different source files). Verify each output duration matches the clip plan's expected final duration via ffprobe.

**Critical:** All speaker segments in theme.ts must use `videoStartFrom = startFrame` since the cleaned source shares the same timeline as the composition.

### 2. Phase A: Scaffold All 5 Videos (Deterministic Script)

Run `remotion-scaffold.ts` for each video. This replaces the previous 5-sub-agent manual codegen approach with a single deterministic script call per video. No LLM reasoning needed — the script reads the storyboard JSON and generates all Remotion code.

**Prerequisites:** Storyboard JSON files must exist from step 03 (section 3a).

```bash
# Run all 5 scaffolds (can be parallelised — they write to separate directories)
for NN in 01 02 03 04 05; do
  npx tsx {project-root}/scripts/remotion-scaffold.ts \
    --storyboard "{project_folder}/{project-slug}/video-editor/short-form/storyboard/sf-${NN}-storyboard.json" \
    --source "{project_folder}/{project-slug}/video-editor/short-form/clips/sf-${NN}-cleaned-4k.mp4" \
    --output "{project_folder}/{project-slug}/video-editor/short-form/remotion/sf-${NN}" \
    --probe
done
```

**What the script generates per video:**

The scaffold now handles FlashTransition wiring, correct audio volume (pre-baked levels, volume=1.0 with fade-only envelope), STUDIO_PREVIEW toggle, transitionSfx propagation to SEGMENTS, continuation segment overlay continuity, and copies FlashTransition.tsx + Caption.tsx from sidecar templates. **No manual post-scaffold fixes needed.**

```
sf-{NN}/
  package.json            — Remotion 4.0.261 + React 19 (name from video title)
  tsconfig.json           — ES2022, bundler resolution, react-jsx
  src/
    index.ts              — registerRoot boilerplate
    theme.ts              — PROJECT config + SEGMENTS array (with transitionSfx, STUDIO_PREVIEW toggle, speakerSource conditional)
    Root.tsx               — Composition + Audio + Sequence mapping + FlashTransition overlay (auto-generated from transitionSfx)
    FlashTransition.tsx    — 4-frame white flash (0→0.5→0 opacity) on click boundaries (copied from sidecar)
    Caption.tsx            — No-op stub (captions are platform-native, not burned in) (copied from sidecar)
    Seg01.tsx ... Seg{XX}.tsx  — Pattern-matched V1-V7 → TSX (deterministic lookup)
    SubtleZoom.tsx         — copied from sidecar templates
    MotionGraphic.tsx      — copied from sidecar templates
    SocialProofStack.tsx   — copied from sidecar templates
    VerticalSplitScreen.tsx — copied from sidecar vertical templates
    VerticalHookText.tsx   — copied from sidecar vertical templates
  public/
    motion-graphics/       — empty, ready for MG files (Phase B)
```

**Pattern → code mapping (built into the script):**

| Pattern | Template Component | Key Props |
|---------|-------------------|-----------|
| V1 | SubtleZoom | zoom=1.03, videoStartFrom, objectPosition |
| V2 | SubtleZoom | zoom=1.08, videoStartFrom, objectPosition |
| V4 | MotionGraphic | zoom=1.15 |
| V4b | MotionGraphic | zoom=1.1 |
| V5 | VerticalSplitScreen | variant="split", speakerPosition="bottom", overlayPadding, skipFadeIn; **continuation pairs auto-get overlayStartFrom + skipFadeOut/skipFadeIn** |
| V6 | VerticalHookText | text, highlight |
| V7 | SubtleZoom | zoom=1.05, videoStartFrom, objectPosition |

**Built-in validation** (runs automatically before code generation):
- Rule 6: Zero frame gaps between segments
- Rule V1: 9:16 vertical composition
- Rule V3: Max 4s per segment
- Rule V4/P3: Non-speaker coverage ≥65%
- P4: First segment is V5 hook
- P5: ≥3 distinct patterns
- Rule 14: Speaker segments have videoStartFrom
- Rule V7: First segment skipFadeIn
- `--probe` cross-checks dimensions/fps against source video via ffprobe

**V5 continuation segment handling (auto, no manual action needed):**

When the V3 4s rule forces a long V5 split-screen to split across two consecutive segments with the same `overlayFile`, the scaffold automatically:
1. Emits `overlayStartFrom: prevSeg.durationInFrames` in `theme.ts` so the overlay continues from where the previous segment left off (not restart from frame 0)
2. Adds `skipFadeOut` to the ending segment so it holds full opacity at the boundary
3. Adds `skipFadeIn` to the continuation segment so it starts at full opacity

Without these three, the overlay MG replays from the beginning and a visible flash appears at the 2-second mark. The scaffold handles this entirely — **never manually omit these props on continuation pairs.**

**After all 5 scaffolds complete**, proceed to Phase B (section 3).

#### A2. Pre-Render Asset Resolution Verification

Before copying assets to `public/`, ffprobe every source file and confirm it matches `PROJECT.width × PROJECT.height`:

```bash
TARGET="${PROJECT_WIDTH},${PROJECT_HEIGHT}"  # e.g., "2160,3840"

for f in motion-graphics/sf-*-mg-*.mp4; do
  res=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f")
  if [ "$res" != "$TARGET" ]; then
    echo "MISMATCH: $f is $res — upscaling to $TARGET"
    # Software encoding for intermediate quality (CRF 15 = near-lossless)
    ffmpeg -y -i "$f" -vf "scale=${PROJECT_WIDTH}:${PROJECT_HEIGHT}:flags=lanczos" \
      -c:v libx264 -crf 15 -preset medium "${f%.mp4}-scaled.mp4" \
      && mv "${f%.mp4}-scaled.mp4" "$f"
  fi
done
```

**Critical:** Use real file copies (not symlinks) when placing assets in `public/`. Remotion's webpack bundler does not reliably follow symlinks.

### 3. Phase B: Asset Copy, QA, and Render (Sequential Per Video)

Process each video sequentially: SF-01 through SF-05. Each video must have its MG files downloaded and upscaled (from Step 4) before proceeding.

**Pipeline overlap:** While SF-01 renders (30-60 min), Phase A sub-agents for SF-02–05 should already be complete. When SF-01's render finishes, SF-02 is immediately ready for asset copy + QA + render.

For each video SF-{NN}:

#### E0. Copy MG Assets to public/

Copy all MG video files referenced in the storyboard from `motion-graphics/` to the Remotion project's `public/motion-graphics/`:

```bash
# For each MG in the storyboard's MG Requests table:
cp "{project_folder}/{project-slug}/video-editor/short-form/motion-graphics/{mg_filename}" \
   "{remotion_project_path}/public/motion-graphics/{mg_filename}"
```

For shared MGs (from `mg-dispatch-tracker.json` `shared_by`), the source file may be named after a different video — copy it with the filename expected by this video's storyboard.

#### E. QA — 24 Rules

Run all 19 base rules + 6 vertical rules:

**Base rules (1–19):** As defined in `remotion-hard-rules.md`
**Vertical rules (V1–V6):** As defined in `vertical-remotion-hard-rules.md`

Present results:

"**QA Report — SF-{NN}**

| # | Rule | Status |
|---|------|--------|
| 1 | OffthreadVideo muted | ✅ PASS |
| 2 | OffthreadVideo style | ✅ PASS |
| ... | ... | ... |
| V1 | source-matched 9:16 | ✅ PASS |
| V2 | Text safe zone | ✅ PASS |
| V3 | Max 4s segments | ✅ PASS |
| V4 | 65-70% non-speaker | ✅ PASS |
| V5 | objectPosition with cover | ✅ PASS |
| V6 | Asset resolution match | ✅ PASS |

**Result: {PASS/FAIL}**"

If any rule fails, fix the issue and re-run QA until all pass.

#### F. Render

> **Hardware Acceleration Notes (Mac Studio 2025 — M4 Max, 64GB RAM):**
> - `--gl=angle` — enables GPU for CSS effects (shadows, blurs, gradients, transforms) in headless Chromium
> - `--hardware-acceleration if-possible` — uses Apple VideoToolbox for H.264 encoding instead of software libx264 (3-5x faster)
> - `--concurrency=8` — optimised for M4 Max (14-16 CPU cores). Run `npx remotion benchmark` to fine-tune.
> - If rendering on a different machine, adjust `--concurrency` and remove `--hardware-acceleration` if not on macOS.

First, create the renders output folder if it doesn't exist:

```bash
mkdir -p {project_folder}/{project-slug}/video-editor/short-form/renders
```

Then render into it:

```bash
cd {remotion_project_path}
npx remotion render src/index.ts {composition_id} \
  --output ../../renders/sf-{NN}-final.mp4 \
  --codec h264 \
  --crf 15 \
  --image-format jpeg \
  --concurrency=8 \
  --gl=angle \
  --hardware-acceleration if-possible
```

Verify output:
- File exists and size is reasonable (see expected size table in `step-07-render.md`)
- Resolution matches `PROJECT.width × PROJECT.height` (ffprobe)
- FPS matches `PROJECT.fps`
- Duration matches expected
- Audio is present and synced

#### G. Generate SRT File (Post-Render)

After each successful render, generate an SRT subtitle file from the transcript for YouTube API upload:

1. **Read** `clipped-refined-transcript.json` for the video
2. **Group words into 3-4 word phrases** (similar to caption page logic but simpler — just group sequential words)
3. **Write SRT format:**
   ```
   1
   00:00:00,000 --> 00:00:01,500
   You don't need n8n

   2
   00:00:01,500 --> 00:00:03,200
   or Zapier to build
   ```
4. **Save to:** `{project_folder}/{project-slug}/video-editor/short-form/renders/sf-{NN}-final.srt`

**SRT timing rules:**
- Use word-level `start` and `end` times from `clipped-refined-transcript.json`
- Each subtitle entry = 3-4 words grouped sequentially
- Entry start = first word's `start` time, entry end = last word's `end` time
- Format timestamps as `HH:MM:SS,mmm` (SRT standard)
- No styling tags — plain text only (YouTube handles styling)

**Verification:** Open the SRT in a text editor and spot-check 3-4 entries against the transcript timestamps.

#### G2. Generate Short-Form Thumbnails (Post-Render)

After all 5 videos are rendered and SRT files generated, create 1 thumbnail per video.

**G2a. Fetch Tool/Brand Logos**

Before generating thumbnails, identify tools/brands mentioned in each script and fetch their logos using the existing `fetch-logo.ts` waterfall. Logos make thumbnails more clickable — viewers recognise brand icons instantly.

```bash
# For each tool/brand mentioned in the scripts:
npx tsx {project-root}/scripts/fetch-logo.ts \
  --name "{tool_name}" \
  --output "{project_folder}/{project-slug}/video-editor/logos/{tool-slug}.png"
```

Re-use logos already fetched in `logos/` from earlier pipeline steps (long-form edit, MG generation) — only fetch missing ones.

**G2b. Generate Thumbnails**

> **CRITICAL:** Read {sfThumbnailStyleGuide} before drafting any prompt. Every thumbnail MUST follow the composition blueprint, typography rules, and prompt template defined in that style guide.

**For each SF-01 through SF-05:**

1. **Read the script** at `short-form/scripts/sf-{NN}-script.md` to extract the topic, hook, key message, and **tools/brands mentioned**
2. **Auto-draft a thumbnail prompt** using the **exact prompt template** from {sfThumbnailStyleGuide}. Key requirements:
   - **2-line bottom text (MANDATORY):**
     - **Line 1** — Descriptive context: white, regular/medium weight, ALL CAPS (e.g., "AI VALIDATES YOUR")
     - **Line 2** — Hook/payoff on GREEN banner: white bold on bright green (#39FF14) rectangle banner, ALL CAPS (e.g., "CONTENT TOPICS")
   - **Bottom safe zone padding:** 150-190px dark empty space below the green banner (platform UI overlay zone)
   - **Top zone:** Main topic brand logo centered, 10-15% from top
   - **Floating icons:** 2 icons/logos flanking person's head, rounded-square app-icon style with slight 3D tilt
   - **Person:** Centered, chest-up crop, head in upper-center area
   - **Background:** Themed texture (NOT flat black) at low opacity behind person
   - 9:16 aspect ratio (1080x1920)
3. **Execute `generate-thumbnail.py`** with `--logo` flags for each relevant tool:

```bash
python scripts/generate-thumbnail.py \
  --ref-dir "{reference_photos_folder}" \
  --inspo-dir "_bmad/_memory/creative-director-sidecar/short-form-inspiration" \
  --output "{project_folder}/{project-slug}/video-editor/short-form/thumbnails/sf-{NN}-thumbnail.png" \
  --prompt "{prompt built from style guide template — MUST include 2-line text + green banner + bottom padding}" \
  --logo "{project_folder}/{project-slug}/video-editor/logos/{tool-a}.png" \
  --logo "{project_folder}/{project-slug}/video-editor/logos/{tool-b}.png"
```

4. **Sequential generation** — 1 at a time, 5 total (API rate limits)
5. **Verify** each PNG exists and is non-zero size
6. **Visually verify** all 5 PNGs show: logos, 2-line text at bottom with green banner on Line 2, bottom padding, person centred

**Logo selection per video:** Include up to 2-3 logos per thumbnail — the primary tool featured in that video's script. Don't overload; pick the most recognisable brands that viewers will click on.

**Output folder:** `{project_folder}/{project-slug}/video-editor/short-form/thumbnails/`

Create the output folder before generating:

```bash
mkdir -p {project_folder}/{project-slug}/video-editor/short-form/thumbnails
```

### Intermediate Encoding Quality

**CRITICAL: Any FFmpeg operation on source video (cleaning, trimming, gap removal, concat) MUST preserve near-lossless quality.** The cleaning step produces an intermediate file that feeds into Remotion — if quality is lost here, the final render cannot recover it.

**Required encoding settings for intermediate clips (cleaning/concat):**

Always use software libx264 with CRF 15 for intermediate files. Hardware encoding (VideoToolbox) is reserved for the final Remotion render only — its quality control is less precise than CRF for intermediates.

| Stage | Codec | Quality Setting | Notes |
|-------|-------|----------------|-------|
| Cleaning/concat (intermediate) | `libx264` | `-crf 15 -preset medium` | Near-lossless. Slower but guaranteed quality match to source. |
| MG upscaling (intermediate) | `libx264` | `-crf 15 -preset medium` | Same — preserve MG quality through the pipeline. |
| Final Remotion render | `h264` | `--crf 15 --hardware-acceleration if-possible` | VideoToolbox for speed, CRF 15 for quality. |

**Example — cleaning/concat step:**
```bash
ffmpeg -y -i input.mp4 -filter_complex "..." \
  -c:v libx264 -crf 15 -preset medium \
  -c:a aac -b:a 256k \
  output-cleaned.mp4
```

**Expected intermediate file sizes (CRF 15, approximate):**

| Resolution | FPS | Duration | Expected Size |
|-----------|-----|----------|--------------|
| 3840×2160 | 60 | 25s | 200-350 MB |
| 3840×2160 | 30 | 25s | 100-200 MB |
| 1920×1080 | 30 | 25s | 30-60 MB |

The intermediate should be a similar order of magnitude to the raw source. If it's dramatically smaller (e.g., 8 MB for a 25s 4K clip when the raw is 174 MB), the quality settings are wrong and MUST be corrected before proceeding.

### 3. Final Summary

"**All 5 Short-Form Videos Rendered**

| # | Title | Duration | Resolution | File Size | Status |
|---|-------|----------|------------|-----------|--------|
| SF-01 | {title} | {X}s | source-matched 9:16 | {size} | ✅ |
| SF-02 | ... | ... | ... | ... | ✅ |
| ... | ... | ... | ... | ... | ... |

**Output directory:** `{project_folder}/{project-slug}/video-editor/short-form/renders/`
**Thumbnails:** `{project_folder}/{project-slug}/video-editor/short-form/thumbnails/`

**Workflow complete.** 5 vertical videos + 5 thumbnails ready for upload to Instagram Reels, TikTok, and YouTube Shorts."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Phase A: 5 Remotion projects scaffolded via `remotion-scaffold.ts` (deterministic, no LLM codegen)
- All vertical templates copied into each project (NO VerticalCaptionV2.tsx — captions are platform-native)
- SRT files generated for each video from `clipped-refined-transcript.json`
- Seg{NN}.tsx files generated from storyboard using correct patterns
- Phase B: MG assets copied to each project's `public/motion-graphics/`
- Shared MGs (from `mg-dispatch-tracker.json`) correctly copied with expected filenames
- All 25 QA rules pass for every project (including V6 asset resolution match)
- 5 final MP4s rendered and verified
- 5 thumbnails generated in `short-form/thumbnails/`

### ❌ SYSTEM FAILURE:

- Manually writing Remotion code instead of using `remotion-scaffold.ts` (Phase A)
- Composition not source-matched 9:16
- Rendering without passing QA
- Rendering before MG assets are copied to `public/`
- Using landscape templates instead of vertical
- Including VerticalCaptionV2 or CAPTION_PAGES in any Remotion project
- Missing SRT file after render
- Missing vertical template files in scaffold
- Output not verified via ffprobe
