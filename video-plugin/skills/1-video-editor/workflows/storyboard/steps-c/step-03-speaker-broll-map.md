---
name: 'step-03-speaker-broll-map'
description: 'Build speaker position map from visual analysis and B-roll source map'

nextStepFile: './step-04-text-placement.md'
outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
---

# Step 3: Speaker & B-Roll Map

## STEP GOAL:

Build two deterministic maps from the analysis data: (1) Speaker Position Map — where the speaker appears on screen at each timestamp, and (2) Visual Asset Source Map — the definitive list of all visual assets (video-extracts, motion graphics, branded templates) with IDs, sources, and status.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is a DETERMINISTIC step — build maps from data, no creative decisions
- No user interaction required — auto-proceed after building
- The Visual Asset Source Map becomes the contract for downstream workflows (B-Roll Extraction, Hera MG)

## EXECUTION PROTOCOLS:

- 🎯 Build speaker position map and visual asset source map from data — no creative decisions
- 💾 Append both maps to {outputFile}, update stepsCompleted, auto-proceed
- 🚫 No user interaction — deterministic data mapping only

## CONTEXT BOUNDARIES:

- Available context: Production brief from step 2, target + main video visual analysis
- Focus: Data extraction only — map what exists, do not invent
- Limits: Do NOT invent B-roll from timestamps where speaker is on screen; do NOT confuse target vs main video timelines
- Dependencies: Production brief must exist before building maps

## MANDATORY SEQUENCE

### 1. Build Speaker Position Map

From the **target segment's visual analysis** (e.g., `analysis/intro/visual-analysis.json`), for each analysed timestamp segment:
- Determine if speaker is visible
- If visible: note position (left/center/right), size (close-up/medium/wide), looking direction
- If not visible: note what's on screen (screen recording, slides, etc.)

This map uses the **target segment's** timestamps because it describes what the viewer sees in the base footage being edited.

Build a speaker position table:

```markdown
## Speaker Position Map

Source: {target-content-type} visual analysis

| Time Range | Speaker Visible | Position | Shot Type | Notes |
|-----------|----------------|----------|-----------|-------|
| 00:00-00:05 | Yes | Center | Medium | Direct to camera |
| 00:05-00:15 | No | — | — | Screen recording: VS Code |
...
```

**If target visual analysis unavailable:** Note that speaker position map is unavailable and text placement (step 4) will use default positions.

### 2. Build Visual Asset Source Map

Consolidate ALL visual assets from the production brief into the definitive source map. There are exactly 3 asset types:

**Type 1: `video-extract` — Segments extracted from the MAIN video via FFmpeg**

These come from the **main video's visual analysis** (e.g., `analysis/body/visual-analysis.json`) — NOT the target segment's analysis. The main video contains screen recordings, demos, tools, and other non-speaker content that can be extracted and overlaid onto the target segment.

- `broll-id`: Unique identifier (e.g., `broll-01-vscode-demo`)
- `type`: `video-extract`
- `source_video`: Path to the full-resolution **main** source video (raw, not proxy)
- `start_time`: Extraction start timestamp **in the main video's timeline** (from main video visual analysis)
- `end_time`: Extraction end timestamp **in the main video's timeline** (from main video visual analysis)
- `description`: What's shown in this clip (from main video visual analysis classification)
- `context`: What's being discussed at this point in the main video (from main video transcript, if available)
- `status`: `pending-extraction` or `extracted` (if file already exists in broll/ folder)

**CRITICAL:** The `start_time` and `end_time` reference the **main video's** timeline, not the target segment's timeline. These are the timestamps [BE] B-Roll Extraction will use to extract the clip from the main video.

**Type 2: `motion-graphic` — Generated via Hera Video API**
- `mg-id`: Unique identifier (e.g., `mg-01-stats-overlay`)
- `type`: `motion-graphic`
- `prompt`: Production-ready Hera Video prompt (see prompt rules below)
- `duration`: 1-5 seconds
- `aspect_ratio`: 16:9 / 9:16 / 1:1
- `reference_image`: Path to reference image, or null if not needed
- `image_source`: Where the reference image comes from — `branded-assets` | `frame-extract` | `canvas-build` | `none`
- `description`: What this MG conveys
- `status`: `pending-generation` or `generated` (if file already exists in motion-graphics/ folder)

**Prompt Rules — Write production-ready prompts using this structure:**
1. **Subject** — What is shown (logo, text, counter, data, shape)
2. **Motion** — How it moves (slides in, fades up, scales, counts up, bounces)
3. **Style** — Visual treatment (clean, minimal, corporate, energetic)
4. **Color** — Specific colors if brand-relevant (dark gradient, brand blue, white text)
5. **Duration hint** — Pacing guidance (quick reveal, slow build, snappy bounce)

Use motion design vocabulary (reveal, slide-in, animate, counter, overlay, glow, bounce) — Hera is a motion graphics tool, not a cinematic video generator.

Good: "Animated counter showing '500+ Projects Delivered' with the number counting up rapidly from 0. White text on a dark blue gradient background. Clean sans-serif font. The number lands with a subtle bounce effect."
Bad: "Something showing project stats" — too vague, will produce unreliable results.

**Reference Image Rules:**
- **REQUIRED** when the MG involves a brand, logo, person's image, or specific visual branding
- **NOT needed** for abstract animations, text-only animations, counters, or generic visual effects
- Set `image_source` to indicate where to get it: `branded-assets` (from sidecar), `frame-extract` (FFmpeg frame from video), `canvas-build` (composite from multiple sources), or `none`

### Logo Fetching Rule (Before Finalising MG Entries)

When a motion graphic's subject involves a named tool, platform, or brand logo:

1. Set `image_source: canvas-build`
2. Set `reference_image` to the target path: `broll/logos/{tool-name}.svg`
3. Note in `description`: `"Fetch logo via: npx tsx scripts/fetch-logo.ts --name '{tool}' --output broll/logos/{tool-name}.svg"`
4. Use the logo's official brand color in the Hera prompt (e.g., "Claude orange #CF4100", "GitHub dark #181717")

**Logo color waterfall:** Simple Icons (simpleicons.org) → SVG Logos → Logotypes.dev → Logo.dev

Simple Icons also provides official brand hex colors — always use them in the Hera prompt for color-accurate motion graphics.

**Type 3: `branded-template` — Constant reusable Remotion components**
- `bt-id`: Unique identifier (e.g., `bt-01-upwork-profile`)
- `type`: `branded-template`
- `template_name`: Remotion component name (e.g., `UpworkProfile`, `AgencyBrand`)
- `description`: What this template displays
- `status`: `ready` (branded templates are always available — no generation needed)

Build the Visual Asset Source Map:

```markdown
## Visual Asset Source Map

### Video Extracts (Extract via [BE] B-Roll Extraction)

Source: {main-content-type} visual analysis — timestamps reference the MAIN video

| ID | Source Video | Start (main) | End (main) | Description | Context | Status |
|----|-------------|--------------|------------|-------------|---------|--------|
| broll-01 | {main video path} | {start} | {end} | {desc} | {context} | {status} |
...

### Motion Graphics (Generate via [HM] Hera Motion Graphics)

| ID | Prompt | Duration | Aspect | Ref Image | Status |
|----|--------|----------|--------|-----------|--------|
| mg-01 | {prompt} | {dur}s | {ratio} | {ref} | {status} |
...

### Branded Templates (Always Ready)

| ID | Template | Description | Status |
|----|----------|-------------|--------|
| bt-01 | UpworkProfile | Animated Upwork profile card | ready |
| bt-02 | AgencyBrand | {YOUR_COMPANY} logo animation | ready |
...
```

**CRITICAL:** Every video-extract entry MUST be backed by a timestamp range that the **main video's** visual analysis confirmed contains non-speaker content. Do NOT invent extractions from timestamps where the speaker is on camera. Do NOT confuse the target segment's timeline with the main video's timeline.

### 2b. Visual Asset Density Self-Check

Before proceeding, verify minimum asset counts against storyboard standards Category 6:

- **Talking head intro sections:** Count total B-roll + MG entries. If combined count < (section_duration_seconds / 8), flag: "WARNING: Visual asset density below minimum for talking head intro. Review main video visual analysis for additional B-roll extraction opportunities — screen recordings, tool UIs, and demonstrations are high-value B-roll sources."
- **B-roll count for intros > 45s:** If B-roll extraction count < 2, flag: "WARNING: Intro > 45s with < 2 B-roll extracts. Check main video for additional extraction candidates."
- **Body sections:** If any body section has > 15s gap between visual breaks, flag for review.

This is an early warning — full density validation happens in step-01-validate, but catching gaps here prevents rework.

### 3. Check Existing Assets

Scan project folders for already-extracted B-roll and generated MG:
- `{project_folder}/{project-slug}/video-editor/broll/*.mp4`
- `{project_folder}/{project-slug}/video-editor/motion-graphics/*.mp4`

Update status for any matching entries to `extracted` or `generated`.

### 4. Append to Storyboard and Auto-Proceed

Append both maps to {outputFile}.

"**Speaker & B-Roll Maps Built**

- Speaker positions mapped: {count} segments
- Visual assets: {extract_count} video extracts, {mg_count} motion graphics, {bt_count} branded templates
- Existing assets found: {existing_count}

Proceeding to text placement..."

Update {outputFile} frontmatter with `stepsCompleted` appended, then load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Speaker position map built from visual analysis (or noted as unavailable)
- Visual asset source map built with all entries typed (video-extract, motion-graphic, branded-template)
- Existing assets checked and statuses updated
- Both maps appended to storyboard document

### FAILURE:

- Making creative decisions (this is deterministic data mapping)
- Not checking for existing B-roll/MG assets
- Requiring user interaction (this step auto-proceeds)
