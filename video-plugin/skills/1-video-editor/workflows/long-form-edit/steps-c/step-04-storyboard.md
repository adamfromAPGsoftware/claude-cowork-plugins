---
name: 'step-04-storyboard'
description: 'Decompose intro into detailed segments with full visual treatment, plan body as single passthrough clip'

nextStepFile: './step-05-assets.md'
---

# Step 4: Storyboard — Intro Decomposition + Body Passthrough

## STEP GOAL:

Decompose the intro into detailed Remotion segments with full visual treatment (motion graphics, captions, jump-cut zooms, B-roll, branded templates). Plan the body as a single passthrough clip (Pattern 8) with no decomposition. Write the unified storyboard document for the remotion-edit workflow to consume.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a long-form video production specialist
- ✅ Apply proven YouTube tutorial intro patterns (from inspiration analyses)
- ✅ The body is ALWAYS passthrough — never decompose body footage into segments

### Step-Specific Rules:

- 🎯 Intro gets FULL treatment: segment decomposition, MGs, captions, jump-cut zooms, B-roll, branded templates
- 🎯 Body stays as one continuous clip (Pattern 8 base) — no segment decomposition into Seg files
- 🎯 Body gets light overlay treatment: chapter cards, PiP speaker toggles, digital zoom keyframes
- 🎯 WhiteFlash transition (30 frames) between last intro segment and body
- 🎯 All timestamps reference the CLIPPED transcript (from step-03), NOT original timestamps
- 🚫 FORBIDDEN to decompose body into multiple Seg files — overlays only
- 🚫 FORBIDDEN to use original (pre-clip) timestamps — always use clipped transcript

## MANDATORY SEQUENCE

### 1. Load Reference Data

Load all required reference files:

- `{project-root}/video-plugin/skills/1-video-editor/workflows/long-form-edit/data/long-form-pacing-rules.md` — P1-P18 pacing rules (canonical version)
- `{project-root}/video-plugin/skills/1-video-editor/workflows/long-form-edit/data/inspiration-compliance-checklist.md` — non-pacing inspiration gates
- `{project-root}/video-plugin/skills/1-video-editor/workflows/long-form-edit/data/inspiration/mg-style-guide.md` — long-form MG style guide (aggregated from 5 inspiration analyses)
- `{project-root}/video-plugin/skills/1-video-editor/workflows/remotion-edit/data/segment-patterns.md` — Patterns 1-9
- `{project-root}/video-plugin/skills/1-video-editor/workflows/storyboard/data/template-library.md` — available Remotion templates
- `{project-root}/video-plugin/skills/1-video-editor/workflows/storyboard/data/pacing-rules.md` — shared pacing rules
- `{project-root}/video-plugin/skills/1-video-editor/workflows/remotion-edit/data/caption-style-spec.md` — caption styling

Also load from the current project:
- `{clips_dir}/intro-clipped-transcript.json` — intro word timestamps on clipped timeline
- `{clips_dir}/body-clipped-transcript.json` — body word timestamps on clipped timeline
- `{analysis_dir}/intro/visual-analysis.json` — intro visual scene data
- `{analysis_dir}/body/visual-analysis.json` — body visual scene data
- The loaded script (from step-01) with `[MG-A]`..`[MG-G]` stage directions

### 2. Parse Intro Structure

Break the intro script into its structural sections:

| Section | Purpose | Typical Duration |
|---------|---------|-----------------|
| Hook | Grab attention via authority/FOMO/curiosity/social-proof (P23) — no CTA, no screen share, ≥1 MG | 3–7s |
| Credibility | Why you should listen to me | 5-15s |
| Value Promise | What you'll learn/achieve | 5-10s |
| Barrier Removal | Why it's easier than you think | 3-8s |
| Bridge | Transition to body content | 2-5s |

Map each section boundary to the **clipped transcript** by finding the matching words and their timestamps.

### 3. Map MG Stage Directions

**MG Style Guide Reference:** When planning MG events, consult the long-form MG style guide (`mg-style-guide.md`) for:
- MG category frequency benchmarks (what types appear most often in successful tutorials)
- Entry/exit animation type distribution (most common: cut-in, fade-in, pop-in)
- Duration targets per MG type (from aggregated inspiration data)
- MG spacing constraints (intro: max 8s gap; body: see P18)
- Color palette patterns (background, text, accent hex codes)
- Motion-to-speech correlation rules (what narration triggers which MG type)

For each `[MG-X]` marker in the script:

1. Find the surrounding spoken text in the clipped transcript
2. Identify the exact timestamp range where the MG should appear
3. Determine the MG type (A-G) from the marker and its description in the script
4. Create an MG brief with: type, prompt description, duration, timestamp range, reference requirements
   - **Duration:** Use P24 duration clustering bands — ultra-short (0.8–3s) for logos/text, short (3–8s) for UI/concepts, medium (8–15s) for pan-zooms/partial reveals, long (15–30s) for sequential lists. Cross-reference style guide avg ±50%.
   - **Entry/exit animation:** Prefer the most common animation types from the style guide for this category
   - **Transcript correlation:** Quote the exact spoken words (mandatory — null is a system failure)
5. **Tool identification gate (Type B/C/D only — M10/M11 HARD gate):** If the MG references a named tool or platform:
   - **MANDATORY: Check the central reference frame library FIRST** at `{project-root}/_bmad/ccs/data/brand-assets/reference-frames/catalog.yaml`. Browse for the tool name and aliases. If a matching frame exists, set `image_source: library` and record the `supabase_url` from the catalog — no logo fetch or frame extraction needed. The library contains real interface screenshots from all past projects (21 tools indexed).
   - **Resolution waterfall (if NOT in library):**
     1. **Frame-extract:** If the tool appears in body footage (check `visual-analysis.json`), extract a frame using `resolve-reference-image.ts --tool "{tool}" --visual-analysis "{analysis_dir}/body/visual-analysis.json" --source-video "{clips_dir}/body-clipped-raw.mp4" --output "{mg_dir}/ref-{slug}.png"`
     2. **Ask user:** If tool is NOT in library AND NOT in body footage: **STOP and ask user** to capture a screenshot and add it to `{project-root}/_bmad/ccs/data/brand-assets/reference-frames/{tool-slug}/`, then run `npx tsx scripts/analyze-library-images.ts --tool {tool}` to index it. Present: "The reference library doesn't have a screenshot for {tool}. Please capture one and drop it into the reference-frames folder."
   - **No logo-only fallback for Type C** (UI mockup MGs) — logos give Hera zero context about interface layout (M10)
   - Look up the tool in `{project-root}/video-plugin/skills/1-video-editor/workflows/hera-motion-graphics/data/tool-visual-reference.md`
   - Include the tool's primary hex colors, UI layout description, and key visual elements in the MG brief prompt
   - Set `tool_name` and `tool_visual_details` fields on the MG entry
   - For Type B: include the tool's primary color for logo glow/accent effect (e.g., `#D97757` terracotta glow for Claude)
   - For Type D: style diagram elements using the tool's visual language (e.g., n8n-style nodes for workflow concepts, chat bubbles for Claude-related concepts)

### 4. Assign Segment Patterns

For each intro section, assign appropriate segment patterns from the template library:

| Visual Scenario | Pattern | Template |
|----------------|---------|----------|
| Speaker talking (hook, bridge) | Pattern 1: Speaker Full | SubtleZoom |
| Speaker with MG overlay | Pattern 2: Speaker + MG | MotionGraphic + SubtleZoom |
| Full-screen MG | Pattern 3: MG Only | MotionGraphic |
| Speaker with B-roll overlay | Pattern 4: Speaker + B-roll | BRollOverlay + SubtleZoom |
| Branded screen (agency site) | Pattern 6: Branded Template | AgencyBrand |
| Social proof (Upwork profile) | Pattern 7: Social Proof | UpworkProfile / SocialProofStack |

**Jump-cut zoom alternation** on consecutive speaker segments:
- Odd speaker segments: `objectPosition: '50% 25%'` (standard framing)
- Even speaker segments: `objectPosition: '50% 15%'` (slight zoom, tighter crop)

### 5. Plan Visual Assets

Compile all asset requests from the intro storyboard:

**B-roll requests:** Identify moments in the BODY footage that illustrate concepts mentioned in the intro (e.g., demo of the product being discussed). Note body raw video timestamps for extraction in step-05.

**⚡ Logo pre-fetch (optional optimization):** If the MG briefs below reference multiple tools needing logos, launch logo fetching as background processes now. The script already contains `[MG-B]`, `[MG-C]` markers that reference specific tools — the tool names are known at this point. By pre-fetching logos during storyboard writing, they'll be ready when step 5 starts.

```bash
# Pre-fetch logos in background (if tool names are known from script MG markers)
rm -f "{logos_dir}/{slug}.png"
npx tsx {project-root}/scripts/fetch-logo.ts --name "{tool}" \
  --output "{logos_dir}/{slug}.png" \
  --color ffffff &
```

**MG requests:** For each `[MG-X]` direction:
- MG type (A-G)
- Hera prompt template (from `hera-motion-graphics/steps-c/step-02-generate.md`)
- Duration (typically 2-4 seconds)
- Reference image requirements (logo, screenshot, etc.)
- Tool name and visual identity (if referencing a named tool — from `tool-visual-reference.md`)
- Explicit hex codes for tool brand colors (e.g., Claude: `#D97757`, n8n: `#FF6D5A`)
- UI layout description for Type C recreations (e.g., "dark sidebar left, warm cream chat area, terracotta icon")
- `image_source` recommendation based on whether the tool appears in body footage (`frame-extract`) or needs to be composed (`canvas-build`)

**Logo requests:** Any tool/brand names mentioned that need logos fetched via `fetch-logo.ts`.

**Branded template assets:** Screenshots of agency website, Upwork profile, etc. — check if already in `public/branded-assets/`.

### 6. Generate Caption Burst Plan

From the intro clipped transcript, generate the caption burst plan:

- Group words into display phrases (2-5 words per burst, break at natural pauses)
- Each burst has: `startFrame`, `endFrame`, `text`, `highlightWord` (the emphasized word)
- Apply caption style spec rules (font, size, position, animation)
- Bursts must cover 100% of spoken words in the intro

### 7. Body Entry — Pattern 8 with Light Overlays

Create a single body entry using **Pattern 8: Video Passthrough** as the base, with overlay Sequences planned on top:

```
## BODY — Pattern 8: Video Passthrough + Light Overlays

sourceFile: body-clipped.mp4 (raw: body-clipped-raw.mp4)
duration: {body_clipped_duration}s ({body_clipped_frames} frames at {fps}fps)
pattern: 8 — Video Passthrough (base clip, NOT decomposed into Seg files)
audio: included in full-audio.m4a concatenation
captions: none (body does not get caption overlays)

### Overlay Plan:
- Chapter cards: {count} planned at section boundaries
- PiP toggle points: {count} identified for screen share sections
- Digital zoom keyframes: {count} planned for static screen share > 30s
- Speaker return points: {count} planned at natural break points
```

### 7b. Body Treatment — Chapter Cards + Light MGs

The body is a raw video passthrough. Overlays are limited to chapter cards and **light body MGs** at concept explanation and speaker return points. No PiP overlays, no digital zoom keyframes — the source footage already contains any PiP or screen share composition from the original recording.

**Chapter Cards (Remotion-native — NEVER Hera):**

🚫 **HARD RULE:** Chapter cards are ALWAYS rendered as native Remotion components using the `ChapterCard` template from `template-library.md`. They must NEVER be submitted to Hera — chapter cards are simple, consistent black/white title cards that Hera would be wasteful (cost + time) for. This applies to ALL long-form edits.

- Identify chapter boundaries by searching the body transcript for when each section actually begins:
  1. For each script section header (e.g., "Part 2: The Architecture"), identify 2-3 **concept anchor keywords** that uniquely mark the start of that section — these should be distinctive topic words (e.g., "architecture", "module structure") rather than generic words. Also extract a longer context phrase (10-15 words) from the script's opening sentence for that section.
  2. Search `body-clipped-transcript.json` for the anchor keywords. Strategy:
     - First pass: search the `transcript` full-text field for the concept keywords to get an approximate region
     - Second pass: in the `words[]` array near that region (±120s), find the first occurrence of the anchor keywords appearing together within a 30-word window
     - If multiple matches: use the one closest to the script-planned estimate
  3. The chapter card `startFrame` = `BODY.startFrame + Math.round((matched_word.start - 3) * fps)` — place the card 3s BEFORE the trigger so it appears as a visual separator before the new section
  4. **Validation:** If the transcript-derived timestamp differs from the script estimate by >90s, flag it with `⚠️ TIMING DELTA` and log both values — large deltas indicate the recording order may differ from the script
  5. **Fallback:** If anchor keywords are not found (speaker skipped or significantly rephrased), use the script estimate and mark as `[ESTIMATED — keywords not found: "{keywords}"]`
- Each chapter card: 2–3s, black bg (#000000), white text (#FFFFFF), hard cut in/out (P9)
- **First chapter card pre-roll (mandatory):** The FIRST chapter card MUST start 0.5s (0.5 * fps frames) BEFORE `BODY.startFrame` so its fade-in completes before body content appears. Extend its duration by the same amount. Formula: `startFrame = BODY.startFrame - Math.round(0.5 * fps)`, `durationInFrames = standard_duration + Math.round(0.5 * fps)`.
- Place as overlay Sequences at chapter transition timestamps

**Body MGs (light treatment — guided by P18 and mg-style-guide.md):**
- Consult the MG style guide's "MG Spacing Rules by Video Length" section for body MG density targets
- Body MGs are placed at **speaker return points** and **concept explanation moments** only (M1 still applies — no MGs during deep screen share execution)
- Typical body MG types: Type A (text overlay at numbers/metrics), Type E (sequential bullets at list moments), Type D (concept graphic at definition/explanation moments)
- Body MG density targets (P22): shorter-form ≥1.0 MG/min, course-length ≥0.15 MG/min. MGs cluster at explanation/speaker-return points only — never in screen share execution (M1).
- Each body MG uses the same VDB format and reference image rules as intro MGs
- P18 (body visual monotony) is a WARN gate — flag but don't block if body has sparse MGs

**Body MG timestamp derivation (mandatory — do NOT use script-planned estimates):**

The body recording will diverge from the script. Speakers ad-lib, reorder sections, expand explanations, and condense others. Script-planned timestamps are unreliable for the body.

For each body MG, derive the actual timestamp:

1. **Extract concept anchor keywords** from the MG's transcript trigger — pick 2-3 distinctive topic words that uniquely identify when this concept is being discussed (e.g., for a "permission modes" MG, anchors might be: "permission", "modes", "ask", "auto"). Avoid generic words like "going", "actually", "really".

2. **Search the body transcript:**
   - Search the `transcript` full-text field for the anchor keywords to find the approximate region
   - In the `words[]` array near that region, find where the anchor keywords cluster within a 30-word sliding window
   - Extract the `start` timestamp of the first anchor keyword in the cluster

3. **Set body MG timing:**
   - `startFrame` = `BODY.startFrame + Math.round(matched_word.start * fps)`
   - Place the MG at or slightly after (0-2s) the point where the speaker introduces the concept — the MG should illustrate what's being explained, not pre-empt it

4. **Multiple occurrences:** If a concept appears multiple times (e.g., "MCP" mentioned in several sections), use the occurrence where it's being **explained or introduced** (usually the first substantial mention, not a passing reference). Check surrounding words for explanation indicators: "what X is", "how X works", "let me show you X", "this is called X".

5. **Delta check:** If derived time differs from script estimate by >90s, log `⚠️ TIMING DELTA` with both values

6. **Fallback:** If keywords not found within ±180s of estimate, use script estimate and mark as `[ESTIMATED]`

The storyboard body MG table must use **derived timestamps** (e.g., `1423s`) not approximates (e.g., `~1400s`). The column header should be "Body Timestamp" not "Approx Body Time".

**Note:** All body timestamps above are derived from word-level timestamps in `body-clipped-transcript.json`. Any entries marked `[ESTIMATED]` had keywords not found in the transcript and should be manually verified during Remotion preview.

**DO NOT plan any of the following for the body:**
- ~~PiP Speaker Toggle~~ — source footage already has PiP baked in
- ~~Digital Zoom Keyframes~~ — not used in long-form body

### 8. Transition Planning

Between the last intro segment and the body passthrough:
- **WhiteFlash** transition: 30 frames duration
- Placed as a Sequence immediately after the last intro segment
- Body Sequence starts immediately after WhiteFlash ends (zero gap)

**Note:** All 5 inspiration videos use black title cards (not white flashes) at chapter transitions. The WhiteFlash is a deliberate brand differentiation — it matches our short-form visual identity. If a project requires strict inspiration compliance, replace WhiteFlash with a black chapter card (P9 spec: #000000 bg, #FFFFFF text, 2–4s, hard cut).

### 8b. Background Music Decision

Decide whether background music enhances this video:

**Default: No music** (4/5 inspiration creators use zero background music)

**When to add music:**
- High-energy intro with rapid cuts (music adds momentum)
- Storytelling/narrative sections (music adds emotion)
- CTA/outro (music adds energy to the final push)

**When NOT to add music:**
- Deep technical screen share (music is distracting)
- Body tutorial content (clean VO is standard)

**If music is added:**
- Volume: 8-12% of voiceover (barely audible)
- Sections: intro + CTA only (never body)
- Source: royalty-free from Pixabay Music, Uppbeat, or Artlist
- Style: subtle ambient/electronic, no lyrics, no strong beat
- Fade: in over 2s at intro start, out over 2s before body transition
- Implementation: single `<Audio>` element in Root.tsx with volume={0.08-0.12}

**Background Music Plan (storyboard entry):**
```
## Background Music
- **Decision:** Yes/No (user choice — do NOT default to "no" based on inspiration data alone)
- **Track source:** Pre-curated library at `{project-root}/_bmad/ccs/data/brand-assets/background-music/` OR Pixabay Music (royalty-free, no attribution required)
- **Search terms:** `corporate ambient`, `lo-fi chill`, `tech background` — match video energy
- **Volume:** ≤10% of voiceover volume (at least -20dB below dialogue)
- **Sections:**
  - Intro (talking head): music at target volume, subtle energy driver
  - Transition (WhiteFlash): music fades out over 3-5s (90-150 frames at 30fps / 180-300 at 60fps)
  - Body (screen share): either silent OR barely-audible (~5% volume) for noise masking
- **Fade rules:**
  - Fade in: first 2s of video (gentle ramp from 0 to target volume)
  - Fade out: 3-5s centered on intro-to-body transition
  - If music continues into body: drop to ~5% at transition, maintain until outro
```

### 9. Pacing Validation (Hard Blocker)

Validate the storyboard against all P1–P18 rules and the MG style guide benchmarks. **FAIL on any FAIL-level gate blocks progression** — remediate and re-validate before proceeding.

#### 9a. Intro Pacing Validation (FAIL = hard blocker)

| Rule | Check | Target | Actual | Status |
|------|-------|--------|--------|--------|
| P1 | Hook cut density | 12–17.5 cuts/min | {measured} | ✅/❌ |
| P2 | Credibility/value prop pacing | 5–12 cuts/min | {measured} | ✅/❌ |
| P3 | Agenda walkthrough pacing | 0–5 cuts/min | {measured} | ✅/❌ |
| P5 | Max speaker hold | ≤ 15s | {longest} | ✅/❌ |
| P8 | Jump-cut zoom alternation | 1.05–1.15x, alternating | {pattern} | ✅/❌ |
| P9 | Chapter card duration & style | 2–4s, hard cut, #000/#FFF | {check} | ✅/❌ |
| P19 | Intro MG density | ≥ ceil(intro_s / 9) [shorter-form] or ceil(intro_s / 15) [course-length] | {actual} | ✅/❌ |
| P12 | MG spacing — max gap | ≤ 8s between MGs | {max_gap} | ✅/❌ |
| P12 | MG spacing — min gap | ≥ 2s between MGs | {min_gap} | ✅/❌ |
| P13 | Layout change frequency | ≥ 3 changes/min | {measured} | ✅/❌ |
| P14 | Hook timing | Hook ≤ 7s | {hook_end} | ✅/❌ |
| P16 | MG type compliance — numbers | Type A at every number | {count} | ✅/❌ |
| P16 | MG type compliance — tools | Type B at first tool mention | {count} | ✅/❌ |
| P21 | Intro layout variation | ≥3 distinct layouts, no 3+ consecutive same | {measured} | ✅/⚠️ |
| P23 | Hook content pattern | Authority/relevance in ≤7s, no CTA, ≥1 MG | {check} | ✅/❌ |
| P25 | CTA placement | Zero CTAs in first 90s | {check} | ✅/❌ |

#### 9b. Intro Timing Validation (WARN = flag, not block)

| Rule | Check | Target | Actual | Status |
|------|-------|--------|--------|--------|
| P10 | B-roll clip duration | 3–6s each | {range} | ✅/⚠️ |
| P15 | Credibility timing | Completes ≤ 25s | {cred_end} | ✅/⚠️ |

#### 9c. Body Overlay Validation (WARN = flag, not block)

| Rule | Check | Target | Actual | Status |
|------|-------|--------|--------|--------|
| P16 | No MGs during deep screen share execution | 0 MGs in active screen share | {count} | ✅/⚠️ |
| P18 | Body visual monotony | No >60s without visual change | {max_gap} | ✅/⚠️ |
| — | First chapter card pre-roll | startFrame ≤ BODY.startFrame - 0.5*fps | {actual} | ✅/❌ |
| — | Chapter cards at section boundaries | ≥ 1 per body section | {count} | ✅/⚠️ |
| P22 | Body MG density | ≥1.0 MG/min [shorter-form] or ≥0.15 MG/min [course-length] | {measured} | ✅/⚠️ |
| M10 | Tool MG reference images | All tool-referencing MGs have library/frame-extract reference | {count} | ✅/❌ |

#### 9d. MG Style Compliance (WARN = flag, not block)

| Check | Target | Actual | Status |
|-------|--------|--------|--------|
| Intro MG type distribution (P20) | ≥3 categories, none >40%, UI-mockup ≥15%, text-overlay ≥12% | {distribution} | ✅/⚠️ |
| Entry animation distribution | Majority are cut-in/fade-in/pop-in | {distribution} | ✅/⚠️ |
| MG duration clustering (P24) | Matches type-specific band, no >30s non-agenda MGs, ≤50% in same band | {range} | ✅/⚠️ |

#### 9d. Remediation Loop

If any FAIL-level gate triggers:
1. Identify the failing rule and the specific segment(s) causing the failure
2. Apply the remediation strategy from the pacing rules document
3. Re-run the full validation table
4. Repeat until all FAIL-level gates pass
5. Log WARN-level issues in the storyboard but do not block progression

### 10. Write Storyboard Document

Write the complete storyboard to: `{storyboard_dir}/full-storyboard.md`

Structure:
```markdown
# Full Video Storyboard — {project_name}

## Production Summary
- Total estimated duration: {intro + transition + body}s
- Intro segments: {count}
- Body: passthrough (1 clip)
- Transition: WhiteFlash (30 frames)

## Intro Master Timeline
[Detailed segment-by-segment breakdown with patterns, templates, timestamps, MG briefs]

## Transition
WhiteFlash — 30 frames after last intro segment

## Body — Pattern 8 Passthrough + Chapter Cards Only
Pattern 8 base — body-clipped.mp4, {duration}s
### Chapter Cards
[List with timestamps and titles]

## Asset Requests
### B-Roll Extraction
[List with body raw timestamps]

### Motion Graphics
[List with MG type, prompt, duration, reference needs]

### Logos
[List with tool names]

### Branded Assets
[List with asset names and status]

## Caption Burst Plan
Not used — long-form videos have no caption overlays.

## Pacing Validation
[P1-P16 validation tables with Target | Actual | Status columns]
[Body overlay validation results]
```

### 11. Storyboard Review

**COLLAB mode:** Present the storyboard in stages:

1. "**Production Brief** — {summary}" → wait for acknowledgment
2. "**Intro Timeline** — {segment count} segments across {sections}" → present segment table, wait for `[C]`
3. "**Asset Requests** — {MG count} MGs, {broll count} B-roll clips, {logo count} logos" → wait for `[C]`
4. "**Pacing Validation** — {pass/fail count}" → wait for `[C] Continue to assets`

**AUTO mode:** Generate full storyboard, validate pacing, auto-approve.

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Intro decomposed into segments with appropriate patterns (1-7, 9)
- Body is a SINGLE Pattern 8 base clip — no decomposition into Seg files
- Body chapter cards planned at all script section boundaries
- Body PiP toggle points identified for all screen share sections
- Body digital zoom keyframes planned for screen share > 30s
- All timestamps reference clipped transcript (not original)
- MG stage directions mapped to transcript timestamps with briefs
- Jump-cut zoom alternation applied to consecutive speaker segments
- WhiteFlash transition (30 frames) between intro and body
- Caption burst plan covers 100% of intro spoken words
- P1-P16 pacing rules validated — all FAIL-level gates pass
- WARN-level issues logged but do not block progression
- Complete storyboard written to `full-storyboard.md`
- B-roll, MG, logo, branded asset requests clearly listed

### ❌ SYSTEM FAILURE:

- Decomposing body into multiple Seg files (body stays as one continuous clip with overlays only)
- Using original (pre-clip) timestamps instead of clipped transcript timestamps
- Missing MG stage directions — all `[MG-X]` markers must be mapped
- No caption burst plan for intro
- No pacing validation or skipping P1-P16 validation
- Any FAIL-level gate unresolved (must remediate and re-validate)
- Missing WhiteFlash transition between intro and body
- Zero body overlays planned (body must have at least chapter cards)
