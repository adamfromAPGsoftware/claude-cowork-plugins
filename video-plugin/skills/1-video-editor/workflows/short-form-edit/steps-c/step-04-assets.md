---
name: 'step-04-assets'
description: 'Poll dispatched Hera MGs, download completed videos, upscale to target resolution, build audio mix, and verify all assets'

nextStepFile: './step-05-remotion.md'
audioLibraryData: '../../data/brand-assets/audio-library.yaml'
---

# Step 4: Asset Completion — Poll, Download, Upscale, Verify

## STEP GOAL:

By the time this step runs, background sub-agents from Step 3 have already dispatched all Hera MG requests and resolved reference images (frame-extract, screenshot, or logo per the priority hierarchy established in step-03 D3). This step completes the asset pipeline: poll for MG completion, download results, upscale to target resolution, and verify everything is ready for Remotion rendering.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 MG requests were already dispatched by Step 3 background sub-agents — do NOT re-dispatch
- 📋 Read `mg-dispatch-tracker.json` as the source of truth for dispatched MG IDs
- 🎯 All Hera MGs MUST be upscaled to match the target resolution after download
- 🎯 If any Step 3 sub-agent failed or is still running, complete its work here
- 🎯 Non-speaker visuals are produced via two tiers only: A (Remotion-native), C (Hera MG with library reference image). There is NO Tier B.

## MANDATORY SEQUENCE

### 0. Probe Target Resolution

Before verifying any assets, probe the raw speaker video to determine the **target resolution**:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0 \
  "{project_folder}/{project-slug}/video-editor/short-form/raw/sf-01.mp4"
# Example output: 2160,3840
```

Store as `TARGET_W` and `TARGET_H`. Every asset MUST match this resolution exactly.

"**Target resolution probed from speaker raw: {TARGET_W}×{TARGET_H}**"

### 1. Check Step 3 Sub-Agent Status

Read `motion-graphics/mg-dispatch-tracker.json` and assess the state of all dispatched MGs:

```json
// Expected structure from Step 3 sub-agents:
{
  "dispatched": [
    {
      "prompt_hash": "abc123",
      "prompt_summary": "Claude logo reveal on dark bg",
      "hera_id": "vid_xxx",
      "status": "pending",
      "output": "sf-01-mg-01.mp4",
      "shared_by": ["sf-01", "sf-03"]
    }
  ]
}
```

**Tier distribution sanity check:** Count entries by tier. If ALL dispatched MGs are Tier C with zero Tier A, flag a likely misclassification from step 3. Re-scan the storyboard MG Requests tables and reclassify any that match Tier A patterns (logo animations, counter animations, comment cards, text emphasis, badge/bubble reveals) before proceeding.

**Reference image check:** For each tool-referencing Tier C entry, verify it has a `reference_image_url`. Also check `short-form/reference-frames/` for `.meta.json` sidecars — if logos exist in `short-form/logos/` but no `.meta.json` sidecars exist anywhere, the resolver was bypassed in step 3 (only `fetch-logo.ts` was called). Re-run the resolver for each tool to recover.

**If any entries are missing `hera_id`** (sub-agent failed mid-dispatch), complete the dispatch now:
- Fire the missing `POST /v1/videos` requests
- Update the tracker with the returned video IDs

**If `mg-dispatch-tracker.json` doesn't exist** (all sub-agents failed or Step 3 was run without sub-agent support), fall back to the full asset generation flow:
1. Read all 5 storyboards and collect MG requests
2. Deduplicate by prompt similarity
3. Fetch logos and screenshots (sections 5b and 3d from the legacy Step 4)
4. Fire all Hera requests in parallel
5. Create and populate `mg-dispatch-tracker.json`

### 1b. Tier C Prompt Quality Validation Gate (Mandatory)

**Before verifying reference images or dispatching to Hera, validate every Tier C MG prompt against minimum quality requirements. This gate catches shallow prompts that slipped through storyboarding.**

Read each Tier C prompt in `mg-dispatch-tracker.json` and check ALL of the following:

| # | Check | Requirement | Failure Action |
|---|-------|-------------|----------------|
| 1 | **Length** | At least 3 sentences of visual description | Reject — prompt is too shallow |
| 2 | **Colour codes** | At least 2 hex colour codes (#XXXXXX) | Reject — missing visual specificity |
| 3 | **Motion choreography** | At least 2 numbered steps OR timing references (e.g., "over 0.3s", "0.2s stagger") | Reject — underspecified motion |
| 4 | **Transcript context** | `transcriptContext` is non-null, non-empty, contains actual transcript words | Reject — missing transcript sync |
| 5 | **Specificity** | Prompt does NOT contain banned vague phrases without detail: "animating", "with effects", "modern design", "sleek interface" used alone | Reject — too vague |
| 6 | **Reference description** | If `referenceFrameFile` is set, prompt describes what is IN the reference image (layout, colours, content) — not just "matching reference image" | Reject — reference image underutilised |
| 7 | **Text economy** | Prompt does not request more than 5 distinct text strings to appear in the MG | Flag warning — excessive text degrades Hera output quality |
| 8 | **No logo generation** | Prompt does NOT ask Hera to draw, create, or generate any logo | Reject — Hera renders logos incorrectly. Use reference image with fidelity instruction instead |

**If any Tier C prompt fails validation:**
1. Log the failing prompt with the specific check(s) that failed
2. Rewrite the prompt using the Visual Description Brief (VDB) format from step-03 D3b
3. Cross-reference the transcript and visual-analysis.json to enrich the prompt
4. Update `mg-dispatch-tracker.json` with the improved prompt
5. Re-validate until all checks pass

**This gate exists because every project run to date has produced prompts below the required quality standard — particularly with all `transcriptContext` fields set to N/A and single-sentence prompts.**

### 2. Verify Reference Images

For each MG request with a `referenceImageUrl`:
1. HEAD request to verify URL is reachable
2. If unreachable → re-run the resolver to obtain a fresh URL:
   ```bash
   npx tsx scripts/resolve-reference-image.ts \
     --tool "{tool}" \
     --project-slug "{project-slug}" \
     --visual-analysis "{project_folder}/{project-slug}/video-editor/analysis/body/visual-analysis.json" \
     --source-video "{long-form source video path}" \
     --output "{project_folder}/{project-slug}/video-editor/short-form/reference-frames/ref-{tool-slug}.png"
   ```
3. Update `mg-dispatch-tracker.json` with the fresh URL

For each MG request WITHOUT `referenceImageUrl` that references a named tool:
1. Flag as missing — run the resolver to obtain one (catches any MGs that slipped through storyboarding without a reference plan)
2. The resolver implements a 4-tier waterfall: (0) central library lookup via `catalog.yaml`, (1) frame-extract from body video via visual-analysis.json, (2) web-screenshot, (3) logo fallback. Library frames already have stable Supabase URLs — no re-upload needed.
3. Update the MG dispatch tracker with the new reference URL

**Library tier handling:** MGs resolved via the central library (tier: `library` in `.meta.json`) have stable, pre-uploaded Supabase URLs. These only need a HEAD request to verify reachability — no re-upload. The library should satisfy ~80% of tool reference needs across all projects.

### 2b. Reference Image Verification Gate (Mandatory)

**Every tool-referencing MG MUST have a verified reference image. This is a hard gate — do not proceed to polling without passing.**

**Reference image priority (established in step-03 D3):**
- **Priority 1 — Frame-extract** from body video (preferred for Tier C MGs depicting tool interfaces)
- **Priority 2 — Web screenshot** (fallback when tool not in body video)
- **Priority 3 — Logo** (last resort, only appropriate for Tier A logo-animation MGs)

1. **Scan all storyboards** for reference image requests (frame-extracts, screenshots, and logos)
2. **Check each expected file exists** — frame-extracts and screenshots in `reference-frames/`, logos in `logos/`
3. **If any are missing** (sub-agent failed), recover using the priority hierarchy:
   - First: Re-run `resolve-reference-image.ts` (attempts frame-extract → screenshot → logo waterfall)
   - Only if resolver fails entirely: `npx tsx scripts/fetch-logo.ts --name "{tool}" --output "short-form/logos/{slug}.png"`
   - Upload to Supabase: `bash scripts/upload-to-supabase-storage.sh "{ref_image_path}" "{project-slug}"`
4. **Verify frame-extract cleanup** — for every frame-extracted reference image, confirm:
   - No speaker PiP overlay (face/person visible in the frame) — if present, paint over with surrounding bg color (see step-03 D3 section 2b)
   - The image shows the correct tool interface for the MG concept
   - For IDE/editor frames: the focal content area is clearly visible (terminal output, specific panel, code block)
5. **Visually verify logos** (when logos ARE the correct source, i.e. Tier A MGs) — confirm correct **product-specific** brand identity:
   - Claude Desktop/Code → Claude speech bubble icon (NOT the Anthropic "A" wordmark)
   - VS Code → VS Code icon (NOT the Microsoft logo)
   - Use `--name "Claude"` not `--name "Anthropic"` (see product mapping in `hera-api-reference.md`)
   - Use `--color {brand_hex}` to ensure visible colors (not white-on-white)
6. **For multi-tool MGs** (e.g. connectors grid with 6 logos), verify the canvas composite exists. If missing, build via FFmpeg overlay filter.
7. **Pre-dispatch visual check of hosted URLs:** For each reference image URL that will be passed to Hera, HEAD request to confirm it loads (200), then visually read the image to confirm it's the right asset.
8. **🛑 HARD GATE — BLOCKS ALL HERA DISPATCH:** Count tool-referencing Tier C MGs vs. Tier C MGs with verified `reference_image_url`. They MUST match. **If ANY tool-referencing Tier C MG lacks a verified reference_image_url, DO NOT proceed to section 3 (polling). Instead:**
   - List every MG missing a reference image with its tool name and output filename
   - Run the resolver waterfall for each: `resolve-reference-image.ts` → upload to Supabase → update tracker
   - Re-check the gate. Only proceed when count matches.
   - **This gate has historically been bypassed by sub-agents — the main agent MUST personally verify the gate after sub-agent dispatch.** Read `mg-dispatch-tracker.json`, count entries with `tier: "C"` that mention a tool in their `prompt_summary` but have `reference_image_url: null`. If count > 0, the gate fails.

   **How to identify tool-referencing MGs:** Scan the `prompt_summary` or full `prompt` for named tools/platforms: Claude, YouTube, VS Code, terminal, IDE, editor, report, dashboard, config, workflow, pipeline. If the prompt describes a specific tool's interface (not an abstract concept), it needs a reference image.

### 2c. Process Tier A MGs (Remotion-Native Rendering)

For each entry in `mg-dispatch-tracker.json` with `"tier": "A"`:

1. **Scaffold a single shared Remotion project** at `short-form/tier-a-renders/` with one composition per Tier A MG:
   - `package.json` with `remotion`, `@remotion/cli`, `react`, `react-dom`
   - `src/index.ts` registering all compositions
   - One TSX component per Tier A MG

2. **Generate each TSX component** using the `remotion_desc` field from the tracker as the creative brief. Each component is self-contained and uses:
   - Remotion primitives: `interpolate`, `spring`, `useCurrentFrame`, `useVideoConfig`
   - HTML/CSS for layout, `staticFile()` for logos (copy needed logos into `public/`)
   - brand palette: light bg `#F5F5F5`, dark text `#1A1A1A`, green accents `#2D6A4F`, coral `#D97757`
   - Animation style matching the description (scale-up, pulse, stagger entrance, etc.)

3. **Render each composition SEQUENTIALLY (CRITICAL — no parallel renders):**
   ```bash
   # ⚠️ MUST render one at a time — parallel remotion render processes
   # cause SIGTERM kills, producing blank white frames (20KB output).
   for COMP in mg-01-name mg-02-name mg-03-name; do
     npx remotion render src/index.ts "$COMP" \
       --output "../motion-graphics/${OUTPUT_FILE}" \
       --codec h264 --crf 15 --gl=angle --hardware-acceleration if-possible

     # Verify render succeeded — blank renders are <50KB
     SIZE=$(stat -f%z "../motion-graphics/${OUTPUT_FILE}" 2>/dev/null || echo 0)
     if [ "$SIZE" -lt 51200 ]; then
       echo "RENDER FAILED: $COMP output is only ${SIZE} bytes — re-rendering..."
       npx remotion render src/index.ts "$COMP" \
         --output "../motion-graphics/${OUTPUT_FILE}" \
         --codec h264 --crf 15
     fi
   done
   ```

   **Why sequential:** Remotion spawns a headless Chrome instance per render. Multiple concurrent instances compete for memory and Chrome IPC, causing SIGTERM kills. On a 4-render batch, only 1 of 4 survived parallel execution — the rest produced blank white frames that weren't caught until preview.

   **Validation gate:** Every rendered MP4 must be >100KB. Files under 50KB are almost certainly blank frames on the background color. Re-render any that fail this check.

4. **Upscale if needed** — if the rendered output doesn't match the target resolution, upscale with FFmpeg lanczos (same as section 5).

5. **Update tracker** status to `"downloaded"`.

6. **Clean up** the `tier-a-renders/` project after all renders complete (or preserve for debugging if any failed).

### 3. Poll All Pending MG IDs

Collect all entries from `mg-dispatch-tracker.json` with `"tier": "C"` and status `"pending"` and poll until all reach `"success"`. Tier A MGs should already be `"downloaded"` by this point (section 2c).

```
Poll loop:
1. For each pending hera_id: GET /v1/videos/{hera_id}
2. If status = "success" → update tracker, proceed to download
3. If status = "failed" → log error, retry dispatch if possible
4. If still pending → wait 15s, re-poll
5. Repeat until all are "success" or permanently failed
```

**Timeout:** If any MG hasn't completed after 10 minutes of polling, flag it to the user.

"**MG Generation Status**

| # | Prompt Summary | Hera ID | Status | Duration | Shared By |
|---|----------------|---------|--------|----------|-----------|
| 1 | {summary} | {id} | ✅ success | {X}s | sf-01, sf-03 |
| 2 | {summary} | {id} | ✅ success | {X}s | sf-02 |
..."

### 4. Download All Completed MGs

For each MG with status `"success"`:
1. Get the download URL from the poll response — **the field is `outputs[0].file_url`** (NOT `url`):
   ```bash
   URL=$(curl -s "https://api.hera.video/v1/videos/{video_id}" \
     -H "x-api-key: $HERA_API_KEY" \
     | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['outputs'][0]['file_url'])")
   curl -sL "$URL" -o "{output_path}"
   ```
2. Save to: `{project_folder}/{project-slug}/video-editor/short-form/motion-graphics/{output_filename}`
3. Update tracker status to `"downloaded"`

### 5. Upscale All MGs to Target Resolution

Hera MGs are generated at native resolution (1080×1920 for 9:16, or 1920×1080 for 16:9). Use the deterministic upscaling script which handles aspect ratio routing automatically:

```bash
npx tsx {project-root}/scripts/upscale-mgs.ts \
  --tracker "{project_folder}/{project-slug}/video-editor/short-form/motion-graphics/mg-dispatch-tracker.json" \
  --target-width {TARGET_W} --target-height {TARGET_H}
```

The script handles:
- **Mixed aspect ratio routing:** 9:16 MGs → `{TARGET_W}×{TARGET_H}` (vertical 4K), 16:9 MGs → `{TARGET_H}×{TARGET_W}` (landscape 4K)
- **Skip already-correct:** MGs at target resolution are skipped
- **Verification:** All outputs probed to confirm resolution match
- **Lanczos upscaling** with CRF 15 quality
- **Note:** `v5Padding` is deprecated — all MGs get standard lanczos upscale. V5 overlay padding is handled exclusively by Remotion's `overlayPadding` prop (85% with `objectFit: contain`).

No manual FFmpeg commands needed — the script reads the tracker and processes all MGs.

### 6. Verify All Assets

For each generated MG asset (all three tiers produce MP4s in `motion-graphics/`):
- Verify file exists and is playable (ffprobe)
- Verify resolution matches target exactly (aspect-ratio aware)

```bash
# Verification — must output exactly "{TARGET_W},{TARGET_H}" for every MG asset
for f in motion-graphics/sf-*.mp4; do
  res=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f")
  if [ "$res" != "{TARGET_W},{TARGET_H}" ]; then
    echo "MISMATCH: $f is $res (expected {TARGET_W},{TARGET_H})"
  fi
done
```

For shared MGs (multiple entries in `shared_by`), verify the output file exists — downstream steps will copy it to each Remotion project that needs it.

"**Asset Completion Summary**

| Type | Expected | Present | Verified |
|------|----------|---------|----------|
| Tier A MGs (Remotion) | {count} | {present} | ✅ |
| Tier C MGs (Hera) | {count} | {present} | ✅ |
| Logos | {total} | {present} | ✅ |
| Tool screenshots | {total} | {present} | ✅ |

**All assets verified. Proceeding to Remotion rendering...**"

**Directory structure:**
```
short-form/
  raw/                # Individual raw 4K source videos + raw registry YAMLs
  proxies/            # 720p proxy files + proxy registry YAMLs
  analysis/sf-{NN}/   # Audio analysis, transcripts, refined transcripts per video (incl. clipped-* variants)
  clips/              # Clip plans, keep-segments, content-cuts
  scripts/            # Copywriter SS scripts (sf-{NN}-script.md)
  storyboard/         # Technical storyboards per video
  broll/              # Intermediate — reference sources only (NOT for Remotion)
  reference-frames/   # Keyframes for Hera reference_image_url
  logos/              # Tool/brand logos fetched via fetch-logo.ts
  motion-graphics/    # ALL MGs (pure prompt + reference-based) — these go into Remotion
    mg-dispatch-tracker.json  # Dedup registry + Hera video ID tracking
  remotion/sf-{NN}/   # Remotion project per video
  renders/            # Final rendered MP4s — easy to find and upload
```

### 7. Audio Mix (Music + Snap SFX)

Every short-form video gets a pre-mixed audio file containing background music + snap click SFX. This single file is referenced by `PROJECT.backgroundMusic` in Remotion, keeping the project within the 2-element `<Audio>` limit (Rule 4).

**CRITICAL — Snap + Flash pairing:** The audio snap and visual `FlashTransition` are a paired system. The snap peak must land exactly on the visual cut frame where the flash fires. See production style guide for the full spec.

#### 7a. Select Background Music

1. Read the storyboard metadata `mood` field (e.g., "techy", "inspiring", "chill")
2. Load `{project-root}/_bmad/ccs/data/brand-assets/audio-library.yaml`
3. Match `mood` against the `mood` tags in the catalog — pick the best match
4. If multiple tracks match, prefer variety across the 5 videos (cycle through tracks, avoid repeating the same track for consecutive videos)
5. Copy selected track to a working directory for mixing

#### 7b. Build Audio Mix

Use the deterministic audio mix script for each video SF-{NN}:

```bash
npx tsx {project-root}/scripts/mix-audio.ts \
  --storyboard "{project_folder}/{project-slug}/video-editor/short-form/storyboard/sf-{NN}-storyboard.json" \
  --music-track "{selected_track_path}" \
  --source-video "{project_folder}/{project-slug}/video-editor/short-form/clips/sf-{NN}-cleaned.mp4" \
  --output "{project_folder}/{project-slug}/video-editor/short-form/motion-graphics/sf-{NN}-audio-mix.mp3"
```

The script handles the entire 2-stage mix pipeline:
- **Stage 1:** Builds a click track by overlaying all `transitionSfx: "click"` timestamps onto silence (asplit + adelay + amix with `normalize=0`)
- **Stage 2:** Mixes click track (volume=6.0) + looped background music (volume=0.08) as 2 inputs
- **Snap peak alignment:** Each click's adelay is offset by -60ms so the snap peak lands exactly on the visual cut frame
- **Built-in verification:** Checks output duration (±0.5s) and click audibility (peak > -15dB at first click)
- **Hardcoded calibrated volumes:** MUSIC=0.08, CLICKS=6.0 (tested and confirmed in SF-02)

No manual FFmpeg filter_complex construction needed.

**Volume calibration notes (why these exact values — DO NOT override in the script):**
- Voiceover from source video peaks at **~-4.5dB**
- Clicks at `volume=6.0` produce peaks at **~-10dB** → clearly audible alongside voice
- Music at `volume=0.08` produces **~-47dB RMS** → gentle background hum
- Previous value of `volume=0.6` for clicks produced -30dB peaks → completely inaudible under voice (26dB gap)

**Remotion playback:** The mix is played at `volume=1.0` with only a fade envelope (0.5s fade-in, 1.0s fade-out). Do NOT apply `backgroundMusicVolume` attenuation — levels are pre-baked. The scaffold now generates this correct volume logic automatically.

**Output location:** Save to `motion-graphics/sf-{NN}-audio-mix.mp3`, then copy to `remotion/sf-{NN}/public/sf-{NN}-audio-mix.mp3` during Phase B asset copy.

**6. Record the selected track and click count in the asset summary:**
```
SF-{NN}: bg-corporate-tech-01.mp3 (122 BPM, techy) + 12 clicks (volume=6.0, peak ~-10dB)
```

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- `mg-dispatch-tracker.json` read and all dispatched MGs accounted for
- All Tier C MGs dispatched with reference images from central library
- Tier A MGs rendered via Remotion with brand styling
- All pending Tier C MGs polled to completion (status `"success"`)
- All MGs downloaded/rendered and upscaled to target resolution (9:16 → vertical 4K, 16:9 → landscape 4K)
- All reference images present and verified (reference image verification gate passed)
- Every tool-referencing Tier C MG confirmed to have `reference_image_url` with a verified reference image (frame-extract preferred, screenshot or logo as fallback)
- Frame-extracted reference images cleaned — no speaker PiP overlay, no faces/people
- Cross-video dedup honored — shared MGs generated once, output file exists
- All assets verified via ffprobe (resolution match)
- Audio mix file generated for each video (background music + swoosh SFX pre-mixed)
- Swoosh SFX placed at correct timestamps matching storyboard visual-type family transitions
- Audio mix duration matches video duration (within ±0.5s)
- Background music track varied across videos (no consecutive repeats)

### ❌ SYSTEM FAILURE:

- Re-dispatching MGs that were already dispatched by Step 3 sub-agents
- Not reading `mg-dispatch-tracker.json` as the source of truth
- MGs not upscaled to target resolution after download/render
- Missing reference images that sub-agents should have resolved (without attempting recovery via the frame-extract → screenshot → logo waterfall)
- Generating Hera MGs sequentially instead of in parallel (when falling back to full generation)
- **Using Hera for Tier A MGs** (Tier A = Remotion-native, must be rendered locally)
- **Any non-speaker visual that is not a verified MP4 from the appropriate tier**
- Tool-referencing Tier C MGs missing `reference_image_url` (must fail the reference image verification gate)
- **Using a logo as `reference_image_url` for a Tier C MG depicting a tool interface** when frame-extract is available in the body video (logos are last resort for Tier C, preferred only for Tier A logo animations)
- **Frame-extracted reference images still containing speaker PiP overlay** (faces/people must be removed before upload)
- Upscaling 16:9 landscape MGs to vertical dimensions (landscape MGs upscale to landscape 4K)
- Missing audio mix file for any video (every short-form video MUST have a pre-mixed audio file)
- Swoosh SFX placed at wrong timestamps (not matching storyboard Transition SFX column)
- Audio mix duration significantly different from video duration (>0.5s mismatch)
- Using `PROJECT.backgroundMusic: null` for short-form videos (always set to pre-mixed file path)
