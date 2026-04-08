---
name: 'step-02-production-brief'
description: 'Parse script into sections, extract B-roll candidates, classify types, timing calibration'

nextStepFile: './step-03-speaker-broll-map.md'
outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
dataFile: '../data/pacing-rules.md'
---

# Step 2: Production Brief

## STEP GOAL:

Build the production brief section of the storyboard: parse the script into sections, extract B-roll candidates from script and visual analysis, classify B-roll types, and calibrate timing against audio analysis data.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are a video production planner
- Collaborative dialogue — present analysis, get user refinement
- You bring expertise in pacing analysis and B-roll identification
- User brings their creative vision for the final video

### Step-Specific Rules:

- Focus on analysis and brief building — NOT timeline assembly (that's step 5)
- Present findings for review before appending to storyboard
- Load pacing rules from {dataFile} for section targets

## EXECUTION PROTOCOLS:

- 🎯 Parse script into sections, identify visual assets from exactly 3 sources, calibrate timing
- 💾 Append production brief to {outputFile} on [C] Continue — update stepsCompleted
- 📖 Load {dataFile} before any pacing decisions
- 🚫 Do NOT build the timeline in this step — plan and brief only

## CONTEXT BOUNDARIES:

- Available context: Script, transcript, visual analysis, audio analysis (discovered in step 1)
- Focus: Section structure, B-roll identification, timing calibration
- Limits: Do NOT assemble the timeline — plan only
- Dependencies: Requires input files confirmed in step 1

## MANDATORY SEQUENCE

### 1. Load Pacing Rules

Load and read {dataFile} for target pacing by section type:
- Hook: 15+ visual events/min
- Intro: 12-15 visual events/min
- Body: 7-10 visual events/min

### 2. Parse Script into Sections

If script was discovered in step 1, parse it into sections:
- Hook / Opening
- Intro sections (high energy, establish topic)
- Body sections (main content, chapters)
- CTA / Outro

For each section, extract:
- Section name and type (hook/intro/body/cta)
- Estimated duration (from transcript word timings or script word count)
- Key talking points
- B-roll suggestions mentioned in script

**If no script available:** Build sections from transcript structure and clip plan segments.

### 2b. Identify Intro Section Boundaries

**Critical:** Distinguish between the **talking head intro** and the **screen share/agenda section**. These have drastically different MG density requirements.

**Talking Head Intro** (high MG density zone):
- Speaker is full-frame on camera, no screen share
- Contains: hook, authority/credibility, value proposition
- Target duration: **30–90s** (sweet spot based on inspiration data)
- Density: ≥ 1 visual per 8s, ≥ 2 MGs in first 15s

**Screen Share / Agenda Section** (lower density):
- Speaker transitions to PiP on slides, Excalidraw, or screen recording
- Contains: agenda walkthrough, topic preview, syllabus
- Duration: variable (20s–3min depending on content)
- Density: ≥ 1 visual change per 15s (pan/zoom/highlight counts)

**How to identify the boundary:**
1. **Primary signal — Visual analysis:** Look for the frame where speaker transitions from full-frame to screen share/slides. The Gemini visual classification identifies frame types (speaker, screen-recording, slides, etc.)
2. **Secondary signal — Transcript:** Look for transitional phrases: "let me show you", "let's jump into", "here's what we'll cover", "let me walk you through"
3. **Tertiary signal — Audio analysis:** Pacing/energy shift (intro speech is typically faster, more energetic)

**Do NOT rely solely on the script** — the speaker may diverge from script. Cross-reference with visual analysis timestamps.

Mark each section in the Production Brief with:
- Section type: `talking-head-intro` | `screen-share-agenda` | `body` | `cta`
- Start/end timestamps (from visual analysis)
- Density target (from storyboard standards D1–D9)

### 3. Identify Available Visual Assets

The storyboard can ONLY use visuals that actually exist or can be created. There are exactly 3 sources:

**Source 1: Video Extracts** (from the MAIN video — not the target segment)
Scan the **main video's visual analysis** (loaded in step 1 as the "B-roll source") to identify segments where non-speaker content appears — these are extractable B-roll. The main video (typically `body`) is the raw full recording that contains screen recordings, demos, and other visual content that can be clipped out and overlaid onto the target segment (e.g., `intro`).

Common extractable content:
- Screen recordings (VS Code, terminal, browser)
- Tool demonstrations
- Slide presentations
- Any non-speaker visual content

Also load the **main video's transcript** (if available) for context — knowing what's being discussed during a screen recording helps decide when to use that B-roll in the target segment's storyboard.

For each, classify as `video-extract` — will be extracted from the main video via [BE] B-Roll Extraction. The `source_video` path must point to the main video file (raw, not proxy).

**CRITICAL:** B-roll extraction timestamps reference the **main video's** timeline, not the target segment's timeline. The storyboard timeline uses the target segment's timestamps, but the extraction commands will use the main video timestamps.

**Source 2: Motion Graphics** (generated via Hera Video API)
Motion graphics add energy and polish — but maintain a healthy balance with video-extracts (Source 1). Video-extracts from the source footage should be the primary B-roll, with motion graphics complementing them rather than replacing them. Plan a motion graphic when:
- The concept benefits from a generated visual (statistics, data visualizations, animated counters)
- A logo reveal or branded animation adds energy and professionalism
- An abstract concept illustration would reinforce the point better than source footage
- A visual transition between sections needs a generated element

**Budget:** 2-5 motion graphics per video. Ensure there's a healthy balance — if the video has plenty of strong B-roll from the source footage, lean toward the lower end. If source B-roll is limited, motion graphics can fill more of the visual variety.

Suitable motion graphic use cases:
- Statistics or data visualizations (animated counters, chart reveals)
- Logo reveals and branded animations (these add real energy)
- Abstract concept illustrations that don't exist in source footage
- Section transition animations

For each, classify as `motion-graphic` — will be generated via [HM] Hera Motion Graphics.

**Source 3: Branded Templates** (constant, reusable Remotion components)
These are pre-built Remotion templates that use fixed brand assets (Upwork profile image, {YOUR_COMPANY} logo, etc.) from `{project-root}/_bmad/_memory/video-editor-sidecar/branded-assets/`. They produce the SAME animation and effects every time — no generation needed:
- `UpworkProfile` — Animated Upwork profile card with rating and stats
- `AgencyBrand` — {YOUR_COMPANY} logo animation

Identify sections where branded templates are relevant (authority building, CTA, social proof moments).

**CRITICAL:** Do NOT invent B-roll sources that don't exist. Every video-extract must be backed by actual non-speaker content confirmed in the main video's visual analysis. If the visual analysis doesn't show a screen recording at a timestamp, you cannot plan a video-extract there.

### 3b. Motion Graphic Trigger Rules (Long-Form)

When building the production brief for long-form content, identify narration trigger points and map them to motion graphic types A–G:

| Narration Context | Graphic Type | Duration | Priority |
|-------------------|-------------|----------|----------|
| Speaker states a number/metric | A: Text overlay | 2–4s | HIGH |
| Speaker names a tool/platform (first mention) | B: Logo graphic | 3–5s | MEDIUM |
| Speaker references social proof / audience demand | C: UI mockup | 4–8s | HIGH |
| Speaker explains an abstract concept | D: Concept graphic | 5–15s | HIGH |
| Speaker walks through a list | E: Sequential bullets | 3–5s per item | HIGH |
| Speaker shifts to storytelling/context | F: Stylized B-roll | 3–6s | MEDIUM |
| Speaker guides attention through a document | G: Digital pan/zoom | Continuous | HIGH |

**When NOT to use motion graphics:**
- During deep technical screen share execution (all 5 inspiration creators remove graphics during step-by-step tutorials)
- When speaker is delivering an emotional/personal moment (stay on full-frame speaker)
- Within 2s of a previous graphic ending (avoid visual overload)

### 3c. Identify MG Reference Screenshots

For every Type B (logo) and Type C (UI mockup) motion graphic identified above, cross-reference the main video's visual analysis to find timestamps where that tool's UI is visible:

1. Search visual analysis frame classifications for frames showing the tool (e.g., "Claude chat interface", "n8n workflow canvas", "VS Code editor")
2. Select the timestamp where the tool is most clearly visible (full screen, sharp focus, no overlays)
3. Record this as `reference_frame_timestamp` in the MG brief entry

**MG brief entry additions for tool-referencing MGs:**

| Field | Description |
|-------|-------------|
| `reference_frame_timestamp` | Timestamp in the main video where this tool is visible (for frame extraction) |
| `reference_source` | `body-footage` if found in visual analysis, `branded-assets` if in sidecar, `none` if not available |

**If the tool is NOT visible in the main video:** Set `reference_source: none` and note in the MG brief that no reference frame is available. The Hera generation step will fall back to `fetch-logo` (Type B) or enhanced text prompt with `tool-visual-reference.md` details (Type C).

If the script includes `[MG-X]` stage directions, use those as starting points for placement. If no script is available, identify trigger points from the transcript narration context.

### 3d. Mandatory Reference Image Resolution

For every Type B, C, or D MG that references a named tool or platform:

1. If tool appears in visual analysis (screen-share or mixed-pip segments):
   - `image_source: frame-extract`
   - Record `reference_frame_timestamp` from visual analysis

2. If tool NOT in visual analysis:
   - `image_source: web-screenshot`
   - The resolver script handles acquisition in the Hera generation step

3. Type B logo-only MGs (no UI needed):
   - `image_source: fetch-logo`

4. `image_source: none` is ONLY valid for:
   - Type A (text/number overlays)
   - Type E (sequential reveals)
   - Type F (stylized B-roll)
   - MGs depicting abstract concepts with no named tool

Record `reference_resolution_note` explaining the decision for each MG.

**Reference image resolution uses the unified resolver script:**
```bash
npx tsx scripts/resolve-reference-image.ts \
  --tool "{tool_name}" \
  --project-slug "{project-slug}" \
  --visual-analysis "{project_folder}/{project-slug}/video-editor/analysis/body/visual-analysis.json" \
  --source-video "{main_source_video}" \
  --output "{output_dir}/{mg_id}-reference.png"
```

The resolver handles the 3-tier waterfall (frame-extract → web-screenshot → logo) automatically and uploads to Supabase Storage for a persistent public URL.

**Validation gate:** Before proceeding to step 4, count tool-referencing MGs with `image_source: none`. If any exist, flag a warning and reconsider.

### 4. Timing Calibration

Cross-reference script sections with audio analysis data:
- Map section boundaries to actual audio timestamps
- Note silence gaps and speech density per section
- Flag sections where pacing targets may be difficult to hit

### 5. Present Production Brief

"**Production Brief**

**Video Overview:**
- Total Duration: {estimated_duration}
- Scope: {scope}
- Sections: {section_count}

**Section Breakdown:**

| # | Section | Type | Section Class | Est. Duration | Pacing Target | B-Roll Candidates |
|---|---------|------|---------------|---------------|---------------|-------------------|
| 1 | {name} | {type} | {class} | {dur} | {events/min} | {count} |
...

**Visual Assets: {total_count}**

| # | Description | Type | Source | Section |
|---|-------------|------|--------|---------|
| 1 | {desc} | {video-extract/motion-graphic/branded-template} | {source ref} | {section} |
...

Review this brief. Any adjustments?

**[E]dit** — Modify sections or B-roll candidates
**[T]une** — Discuss pacing targets
**[C] Continue** — Accept and proceed

#### Menu Handling Logic:
- IF E: Discuss adjustments, apply changes, redisplay menu
- IF T: Discuss pacing concerns, adjust targets if needed, redisplay menu
- IF C: Append production brief to {outputFile}, update frontmatter `stepsCompleted`, then load, read entire file, then execute {nextStepFile}
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Script parsed into sections with timing estimates
- Visual assets identified from exactly 3 sources: video-extract, motion-graphic, branded-template
- Timing calibrated against audio analysis
- User reviewed and accepted production brief
- Brief appended to storyboard document

### FAILURE:

- Skipping section parsing
- Using B-roll types other than video-extract, motion-graphic, or branded-template
- Planning visuals that don't actually exist in the source video
- Not presenting for user review
- Building timeline in this step (that's step 5)
