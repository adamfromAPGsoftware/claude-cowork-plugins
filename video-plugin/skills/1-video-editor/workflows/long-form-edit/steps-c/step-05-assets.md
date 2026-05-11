---
name: 'step-05-assets'
description: 'Extract B-roll, fetch logos, generate Hera MGs, verify per-clip audio, then hand off to remotion-edit workflow'

nextStepFile: null
---

# Step 5: Assets + Handoff — Prepare All Visual Assets, Then Launch Remotion Edit

## STEP GOAL:

Prepare all visual assets needed by the intro storyboard: extract B-roll clips from body footage, fetch tool/brand logos, generate Hera motion graphics, verify per-clip audio files extracted in step 3. Verify all assets, then hand off to the remotion-edit workflow for the Remotion build and render phase.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the FINAL step of long-form-edit — after completion, hand off to remotion-edit
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a long-form video production specialist
- ✅ Asset preparation is the bridge between storyboard and Remotion build
- ✅ All assets must be verified before handoff — remotion-edit should not encounter missing files

### Step-Specific Rules:

- 🎯 B-roll is extracted from BODY raw footage at timestamps identified in storyboard
- 🎯 Per-clip audio: verify `intro-audio.m4a` and `body-audio.m4a` already exist from step 3 extraction — only re-extract as fallback
- 🎯 All MGs generated via Hera API using type-specific prompt templates
- 🚫 **FORBIDDEN to submit chapter cards to Hera** — chapter cards are ALWAYS native Remotion (black/white title cards, simple + consistent, handled by the `ChapterCard` template in remotion-edit)
- 🚫 FORBIDDEN to start Remotion scaffolding — that belongs to remotion-edit workflow
- 🎯 Handoff provides all inputs remotion-edit needs: storyboard, assets, audio, video files

### ⚡ Parallelization Rules:

Asset generation runs in THREE phases to maximize parallelism while respecting dependencies:

- **Phase 1 (all parallel):** Launch simultaneously:
  - All B-roll FFmpeg extractions (multiple background processes)
  - All logo fetches (multiple background processes)
  - Hera MGs that need NO reference image (Types A, D, E) — submit immediately via batch API calls
  - **Hera MGs with `image_source: library`** — these have pre-existing Supabase URLs from the central reference frame library. Submit immediately in Phase 1 (no logo dependency). Pass the catalog's `supabase_url` directly to `dispatch-hera.ts --reference-image`.
- **Phase 2 (after logos ready):** Submit remaining Hera MGs that need logo reference images (Types B, C — only those WITHOUT library references)
- **Phase 3 (poll all):** Poll ALL submitted Hera jobs in a single loop (every 10s) until all reach `"success"`
- Per-clip audio: verify `intro-audio.m4a` + `body-audio.m4a` exist (extracted in step 3), re-extract only as fallback
- Asset verification: run all probes

## MANDATORY SEQUENCE

### 1. Load Storyboard Asset Requests

Read `{storyboard_dir}/full-storyboard.md` and extract all asset requests from **both intro and body sections**:

- **B-roll clips**: body raw timestamps, descriptions, output filenames
- **Motion graphics (intro)**: MG type (A-G), Hera prompts, durations, reference needs
- **Motion graphics (body)**: Body MGs at speaker return and concept explanation points (same format as intro MGs)
- **Logos**: tool/brand names to fetch
- **Branded assets**: screenshots/images needed (check if already available)

**Classify MGs by reference dependency** (applies to both intro and body MGs):
- **No-ref MGs** (Types A, E — no reference image needed): can submit immediately
- **Library-ref MGs** (any type with `image_source: library`): can submit immediately — URL from `catalog.yaml` pre-exists. Check the central library at `{project-root}/example-account-brand-plugin/context/brand/brand-assets/reference-frames/catalog.yaml` for the tool name. This should cover ~80% of tool-referencing MGs.
- **Frame-extract MGs** (any type with `image_source: frame-extract`): resolved during storyboard step via `resolve-reference-image.ts` — verify the output file exists and has a valid `supabase_url` in its `.meta.json` sidecar
- **Logo-ref MGs** (Types B — need logo reference image AND not in library): must wait for logo fetch to complete

**⚠️ HARD GATE — Reference Image Verification (M10/M11):**

Before ANY Hera dispatch, verify that every tool-referencing MG (Types B, C, D) has a verified reference image:

1. Count tool-referencing MGs in the storyboard
2. Count MGs with verified `reference_image_url` or `supabase_url` (from library or frame-extract)
3. **These counts MUST match** — if ANY tool-referencing MG lacks a verified reference URL, DO NOT proceed to Hera dispatch
4. For each missing reference: run `npx tsx scripts/resolve-reference-image.ts --tool "{tool}" --output "{mg_dir}/ref-{slug}.png"` with the full waterfall
5. If waterfall fails: **STOP and ask user** — "The reference library doesn't have a screenshot for {tool}. Please capture one and drop it into `example-account-brand-plugin/context/brand/brand-assets/reference-frames/{tool-slug}/`, then run `npx tsx scripts/analyze-library-images.ts --tool {tool}`."
6. **No logo-only fallback for Type C** (UI mockup MGs) — logos give Hera zero context about interface layout

### 2. Phase 1 — Parallel Launch (⚡ B-roll + Logos + No-Ref MGs simultaneously)

Launch ALL of the following concurrently:

#### 2a. B-Roll Extraction (background processes)

For each B-roll request, launch FFmpeg extraction as a background process:

```bash
# Launch all B-roll extractions in parallel
ffmpeg -i "{body_raw_path}" \
  -ss {start_seconds} -t {duration_seconds} \
  -c:v libx264 -preset fast -crf 18 \
  -c:a aac -b:a 128k \
  "{broll_dir}/broll-{NN}.mp4" &
```

These clips show product demos, screen shares, or other body footage that illustrates concepts discussed in the intro.

#### 2b. Logo Acquisition (concurrent fetches)

For each tool/brand referenced in MG briefs, launch logo fetch concurrently:

```bash
# Launch all logo fetches in parallel
rm -f "{broll_dir}/../logos/{slug}.png"
npx tsx {project-root}/scripts/fetch-logo.ts --name "{tool}" \
  --output "{broll_dir}/../logos/{slug}.png" \
  --color ffffff &
```

#### 2c. No-Reference Hera MGs (batch submit — Types A, D, E)

For each MG brief that needs NO reference image, submit the Hera API call immediately. **Do not wait for completion** — just capture the `video_id` from each response. These run on Hera's servers in parallel with the local B-roll and logo operations.

**COLLAB mode:** Before generation, present MG request table:

"**Motion Graphic Generation Plan**

| # | Type | Prompt Summary | Duration | Reference | Phase |
|---|------|---------------|----------|-----------|-------|
| 1 | {A-G} | {first 50 chars}... | {dur}s | none | Phase 1 (submitted) |
| 2 | {A-G} | {first 50 chars}... | {dur}s | logo | Phase 2 (after logos) |
| ... | ... | ... | ... | ... | ... |

**Total MGs: {count} | No-ref: {phase1_count} | Logo-ref: {phase2_count}**

[C] Continue — generate all | [S] Skip a specific MG | [A] Adjust prompts"

**AUTO mode:** Submit all no-ref MGs immediately, skip cost confirmation.

### 3. Phase 2 — Logo-Dependent MGs (after logos ready)

Wait for all logo fetches from Phase 1 to complete.

**Visual verification gate:** Read each output PNG to visually confirm it is the correct logo. Check for:
- Wrong brand (generic icon instead of specific tool)
- Wrong colors (inverted, wrong variant)
- Placeholder or error image

**If wrong:** Report to user and ask for a direct URL override or skip. Do NOT proceed with an incorrect logo.

"**Logo Acquisition Summary**

| # | Tool | Logo File | Status | Verified |
|---|------|-----------|--------|----------|
| 1 | {tool} | logos/{slug}.png | fetched | ✅ correct / ❌ wrong |
| ... | ... | ... | ... | ... |"

Now submit remaining Hera MGs (Types B, C) that need logo reference images. Capture their `video_id`s.

### 4. Phase 3 — Poll ALL Hera Jobs (single unified loop)

**Poll all submitted Hera jobs** (from both Phase 1 and Phase 2) **in a single loop.** Check `GET /v1/videos/{video_id}` for each job every 10 seconds until ALL reach `"success"` or `"failed"`.

```
while any job is still pending:
  for each pending job:
    GET /v1/videos/{video_id}
    if status == "success": download MP4, mark complete
    if status == "failed": mark failed, offer retry
  sleep 10s
```

This replaces the old sequential pattern (submit → poll → download → repeat) with a batch approach that processes all MGs concurrently on Hera's servers.

After all downloads complete, verify each MG:
- File exists and is playable (ffprobe)
- Duration matches request
- Aspect ratio is 16:9

Also wait for all background B-roll extractions to complete. Probe each extracted clip:
- File exists and is playable
- Duration matches request (within ±0.5s)
- Resolution matches raw source

"**B-Roll Extracted: {count} clips from body footage**

| # | Description | Timestamp | Duration | File | Status |
|---|------------|-----------|----------|------|--------|
| 1 | {desc} | {start}-{end}s | {dur}s | broll-01.mp4 | ✅ |
| ... | ... | ... | ... | ... | ... |"

### 5. Per-Clip Audio Verification (verify or fallback)

**Check if per-clip audio files already exist** from the extraction launched in step 3 (section 7).

**If both exist:** Verify only:
- `{remotion_dir}/public/intro-audio.m4a`: playable, duration matches `intro_clipped_duration` (within ±0.1s)
- `{remotion_dir}/public/body-audio.m4a`: playable, duration matches `body_clipped_duration` (within ±0.1s)

**If either does NOT exist** (step 3 extraction failed or was skipped): Extract now as a fallback using stream copy:

```bash
ffmpeg -i "{clips_dir}/intro-clipped.mp4" -vn -acodec copy \
  "{remotion_dir}/public/intro-audio.m4a"
ffmpeg -i "{clips_dir}/body-clipped.mp4" -vn -acodec copy \
  "{remotion_dir}/public/body-audio.m4a"
```

Verify both files exist and are playable. NEVER concatenate audio into a single file — concatenation causes 500ms+ sync drift (see `wiki/audio-sync.md`).

### 6. Asset Verification

Comprehensive verification of all assets:

```bash
# Probe all B-roll clips
for f in {broll_dir}/broll-*.mp4; do
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 "$f"
done

# Probe all MG clips
for f in {mg_dir}/mg-*.mp4; do
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 "$f"
done

# Probe per-clip audio
ffprobe -v error -show_entries format=duration -of csv=p=0 "{remotion_dir}/public/intro-audio.m4a"
ffprobe -v error -show_entries format=duration -of csv=p=0 "{remotion_dir}/public/body-audio.m4a"
```

"**Asset Verification Complete**

| Asset Type | Count | All Verified |
|-----------|-------|-------------|
| B-roll clips | {count} | ✅ |
| Motion graphics | {count} | ✅ |
| Logos | {count} | ✅ |
| Branded assets | {count} | ✅ |
| Per-clip audio | 2 | ✅ (intro: {intro_dur}s · body: {body_dur}s) |

**All assets ready for Remotion build.**"

### 7. Select Background Music (if storyboard specifies)

If the storyboard's Background Music section has `Decision: Yes`:

1. Check pre-curated library at `{project-root}/example-account-brand-plugin/context/brand/brand-assets/background-music/`
2. Select a track matching the video energy: corporate ambient, 90–120 BPM, no lyrics
3. If no pre-curated match, use Pixabay Music (royalty-free, no attribution required): search `corporate ambient`, `lo-fi chill`, `tech background`
4. Copy selected track to: `{remotion_dir}/public/music/background-music.mp3`
5. Verify track duration ≥ intro duration + 5s (enough for fade-out to complete)
6. If track is shorter than needed, loop with FFmpeg:

```bash
ffmpeg -stream_loop -1 -i track.mp3 -t {required_duration_seconds} -c copy looped.mp3
mv looped.mp3 background-music.mp3
```

### 8. Handoff to Remotion Edit Workflow

The long-form-edit pipeline is complete. Everything needed by the remotion-edit workflow is now in place:

**What remotion-edit expects:**
- ✅ Approved storyboard: `{storyboard_dir}/full-storyboard.md`
- ✅ Clipped proxy videos: `{clips_dir}/intro-clipped.mp4`, `{clips_dir}/body-clipped.mp4`
- ✅ Clipped raw videos: `{clips_dir}/intro-clipped-raw.mp4`, `{clips_dir}/body-clipped-raw.mp4`
- ✅ Clipped transcripts: `{clips_dir}/intro-clipped-transcript.json`, `{clips_dir}/body-clipped-transcript.json`
- ✅ B-roll clips: `{broll_dir}/broll-*.mp4`
- ✅ Motion graphics: `{mg_dir}/mg-*.mp4`
- ✅ Logos: `logos/*.png`
- ✅ Branded assets: `public/branded-assets/*` (if applicable)
- ✅ Per-clip audio: `{remotion_dir}/public/intro-audio.m4a` + `{remotion_dir}/public/body-audio.m4a`
- ✅ Raw video registry YAMLs: `raw/*.yaml`

**Remotion-edit will run its 11 steps:**
1. `step-01-preflight` — Load storyboard, validate prerequisites
2. `step-01b-broll-verify` — Verify B-roll clips match storyboard intent
3. `step-02-scaffold` — Create Remotion project structure
4. `step-03-theme` — Generate theme.ts configuration
5. `step-04-segments` — Generate segment components (intro Seg01-SegNN + body passthrough)
6. `step-05-composition` — Assemble Root.tsx (intro segments → WhiteFlash → body OffthreadVideo → per-clip Audio elements)
7. `step-06-qa` — 18-point QA checklist
8. `step-06b-content-verify` — Content verification
9. `step-07-render` — Preview & render final MP4
10. `step-07b-studio-preflight` — Studio preflight (optional)
11. `step-08-audio-enhance` — Audio enhancement (optional)

**COLLAB mode:**

"**Long-Form Edit Pipeline Complete!**

All analysis, clipping, storyboard, and assets are ready. The next phase is the Remotion build.

**To continue:** Launch the **remotion-edit** workflow, which will pick up from the approved storyboard and build the Remotion project.

You can start it with: `/bmad-agent-ccs-video-editor` → select the **remotion-edit** workflow."

**AUTO mode:**

"**Long-Form Edit Pipeline Complete — auto-proceeding to remotion-edit workflow.**

All assets verified. Launching remotion-edit workflow to build and render the final video."

Instruct the system to load and execute the remotion-edit workflow:
`{project-root}/video-plugin/skills/1-video-editor/workflows/remotion-edit/workflow.md`

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All B-roll clips extracted from body raw footage at storyboard-specified timestamps
- All logos fetched and visually verified as correct
- All Hera MGs generated with correct type, duration, and aspect ratio (16:9)
- Per-clip audio extracted via stream copy: `intro-audio.m4a` + `body-audio.m4a` (never concatenated)
- All assets verified via ffprobe (exist, playable, correct resolution/duration)
- Complete handoff checklist satisfied — remotion-edit has everything it needs
- Clear instruction to launch remotion-edit workflow

### ❌ SYSTEM FAILURE:

- Starting Remotion scaffolding or code generation (belongs to remotion-edit)
- Missing per-clip audio files (remotion-edit requires `intro-audio.m4a` + `body-audio.m4a`)
- Concatenating audio into a single file (causes 500ms+ sync drift)
- Generating MGs at wrong aspect ratio (must be 16:9 for long-form)
- Proceeding with incorrect/unverified logos
- Not verifying all assets before handoff
- Missing any file that remotion-edit expects
