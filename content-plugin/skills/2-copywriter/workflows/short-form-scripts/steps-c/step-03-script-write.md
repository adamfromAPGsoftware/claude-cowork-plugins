---
name: 'step-03-script-write'
description: 'Write 5 short-form scripts with B-roll plan, MG prompts, conceptual storyboard, platform copy, and combined teleprompter file'

nextStepFile: './step-04-review.md'
scriptRulesData: '../data/script-rules.md'
---

# Step 3: Script Writing — Full Creative Plan for Each Video

## STEP GOAL:

Write 5 complete short-form video scripts with B-roll extraction plans, detailed Hera motion graphic prompts, and conceptual storyboards. Each script is a self-contained creative brief for the Video Editor SF workflow. A combined teleprompter file is generated for single-session recording.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 Write ALL 5 scripts in this step — do not split across steps
- 📖 Re-read {scriptRulesData} before writing — especially Speaking Rate Guidelines, Duration Variations, and Teleprompter Section rules
- 🎯 Each script MUST follow the Hook → Body → CTA structure from script rules
- 🎯 WORD COUNT VALIDATION: After writing each section, count words and verify against speaking rate (3.5 wps normal, 4.0 wps hook, 3.0 wps CTA). Calculated duration must be within ±1 second of time allocation.
- 🎯 DURATION MIX: Apply the 1-3-1 distribution: 1 Punchy (15–20s), 3 Standard (22–30s), 1 Deep (35–45s)
- 🎯 MG DENSITY: Near-constant MG is the standard (MG-first approach — "MG with occasional speaker moments"). Minimum clips per duration category enforced (Punchy: 4, Standard: 7, Deep: 10). Target 80%+ non-speaker coverage. Plan V4b cutaways at least 1 per 10–12 seconds.
- 🎯 MG PROMPT QUALITY: Every MG prompt must follow the 6-part structure (format+orientation → subject → motion → style → colors → timing). Vague prompts = system failure.
- 🚫 FORBIDDEN to generate B-roll or MG assets — only write the plan

## MANDATORY SEQUENCE

### 1. Re-Read Script Rules

Load and read {scriptRulesData}. Pay special attention to:
- **Speaking Rate Guidelines** — word count validation formula
- **Duration Variations** — 1-3-1 mix rule
- **B-Roll Density Guidelines** — minimum clips per category
- **MG Prompt Structure** — 6-part mandatory format
- **Teleprompter Section** — formatting rules (used for combined teleprompter file)

**Load Voice Reference Data:**
- Load `creator-voice.md` from `{project-root}/content-plugin/skills/2-copywriter/workflows/script-generation/data/inspiration/` — match the creator's sentence structure, contractions, and signature phrases in all scripted hooks and CTAs
- Load `creator-credentials.md` from `{project-root}/content-plugin/skills/2-copywriter/workflows/script-generation/data/inspiration/` — reference for any credibility mentions in hooks
- Load `{project-root}/content-plugin/data/lead-magnet-keywords.yaml` — select keywords for CTA integration
- Load `../data/icp-profiles.md` — ICP profiles, angle/ICP matrix, language register guide
- Load `../data/example-hooks.md` — 6 annotated inspiration examples for hook pattern matching

### 2. Assign Duration Categories

From the 5 approved concepts, assign each to a duration category based on complexity:

- **Simple insights, hot takes, one-liners** → Punchy (15–20s)
- **Tool demos, pain point + solution, mini-stories** → Standard (22–30s)
- **Step-by-step, frameworks, detailed case studies** → Deep (35–45s)

Distribution MUST be: 1 Punchy + 3 Standard + 1 Deep.

**If `{execution_mode}` = `collab`:**
Present assignments to confirm before writing:

"**Duration Assignments:**
| # | Concept | Category | Target Duration | Word Budget |
|---|---------|----------|----------------|-------------|
| SF-01 | {title} | Punchy | 18s | ~45 words |
| SF-02 | {title} | Standard | 35s | ~90 words |
| ... | ... | ... | ... | ... |

[C] Confirm and proceed | [R] Revise assignments"

Wait for user confirmation before writing scripts.

**If `{execution_mode}` = `auto`:**
Assign categories based on concept complexity and proceed immediately. Log the assignments but do not wait for confirmation.

### 2b. Angle-Specific Writing Guidance

> **Note:** After completing 2b, proceed to 2c before writing any script.

Before writing, check each concept's `angle_type` from step 02. Apply the matching guidance:

**Story scripts:**
- Tell a mini-journey — the hook teases the outcome or problem, the body walks through 2–4 stages from the body video in chronological order
- MGs are predominantly **Tier B/C with body video reference frames** (the viewer should see what was actually on screen)
- Use first-person journey narration: "I opened...", "The agents started...", "Here's what came back..."
- Recommended hooks: Journey Tease, Result Reveal, Pain Interrupt
- Include `[BODY-MOMENT]` markers (see script-rules.md) linking each beat to a real body video timestamp

**Tool-Focus scripts:**
- Spotlight one specific capability — the hook names the tool, the body shows 2–3 of its capabilities
- Mix of reference-based MGs (Tier B/C for the tool UI) and prompt-only MGs (Tier C for abstract concepts)
- Include `[BODY-MOMENT]` markers where applicable (tool demo timestamps from body video)
- Recommended hooks: Product Drop, Result Reveal, Step-by-Step Tease

**Concept / Value-Drop scripts:**
- Current default approach — no special guidance needed
- MGs are predominantly prompt-only (Tier C) with occasional reference frames if relevant

### 2c. ICP-Aware Writing Setup

Before writing each script, declare the ICP context. This step ensures language register, hook choice, and CTA keyword are all aligned before the first word is written.

**For each script, identify and state:**

1. **Target ICP** — from the approved concept card (`target_icp` field)
2. **Emotional register** — from the approved concept card (`emotional_register` field)
3. **Style reference** — find the best match in `example-hooks.md` by matching `angle_type` + `hook_pattern`. Use the Quick-Match Reference table.

**State this at the top of each script section (before writing the hook):**

```
Target ICP: {Primary (TOFU) / Secondary (BOFU)}
Emotional register: {Curious / Energised / Pragmatic / Relieved / Challenged}
Style reference: example-hooks.md Example {N} — {label}
```

**If Primary ICP:**
- Use builder language markers from `icp-profiles.md` (build, ship, deploy, tool names, etc.)
- Match hook structure to the identified example-hooks.md style model
- Default MG visual style: coding interface, workflow diagram, or tool UI
- CTA keyword: select from TOFU list (AGENT, BUILD, CLAUDE, CURSOR, TEMPLATE, WORKFLOW, AUTOMATE, STACK, DEPLOY, SHIP)

**If Secondary ICP (Before/After):**
- No direct example-hooks.md match — Secondary ICP creators not in dataset
- Use Language Register Guide from `icp-profiles.md` to translate every insight to ROI/outcome language
- Default MG visual style: cost counter, side-by-side comparison, or before/after dashboard
- CTA keyword: select from BOFU list ONLY (AUDIT, AI, RESULTS, ROI, SYSTEM)
- Apply the ROI-framing test to every body sentence: "Would a 45-year-old SME owner care about this?"

### 3. Write Scripts (Per Video)

For each of the 5 approved concepts (SF-01 through SF-05), produce a complete script file with these sections:

#### A. Script (with word count validation)

```
## Script

**Duration category:** {Punchy / Standard / Deep}
**Duration target:** {X}s
**Word budget:** {Y} words (at {Z} wps average)
**Hook type:** {from concept extraction}

### Hook (0:00–0:{HH}) — {W} words @ 4.0 wps = {T}s
{Exact words the speaker will say. Energetic, confident pace.}

### Body (0:{HH}–0:{BB}) — {W} words @ 3.5 wps = {T}s
{Exact words for the body. Break into beats.}

**Beat 1 (0:{HH}–0:{B1})** — {W} words @ 3.5 wps = {T}s
{Speaker words for this beat.}
[B-ROLL: source="{segment}" timestamp="{start}-{end}" description="{specific visual}" duration="{X}s"]

**Beat 2 (0:{B1}–0:{B2})** — {W} words @ 3.5 wps = {T}s
{Speaker words for this beat.}
[MG: prompt="{detailed 6-part Hera prompt}" reference="{asset path or 'none'}" duration="{X}s"]

{Continue beats...}

### CTA (0:{BB}–0:{CC}) — {W} words @ 3.0 wps = {T}s
{Exact words for the call-to-action. Deliberate, clear pace.}

### Word Count Validation
| Section | Words | WPS | Calculated Duration | Allocated Duration | Delta |
|---------|-------|-----|--------------------|--------------------|-------|
| Hook | {W} | 4.0 | {T}s | {A}s | {±D}s |
| Body | {W} | 3.5 | {T}s | {A}s | {±D}s |
| CTA | {W} | 3.0 | {T}s | {A}s | {±D}s |
| **Total** | **{W}** | — | **{T}s** | **{A}s** | **{±D}s** |
```

**CRITICAL:** If any section's delta exceeds ±1 second, rewrite the section to match before proceeding.

#### B. Reference Frame Plan (for Hera MG Generation)

Reference frames are single keyframe extracts from long-form B-roll — they are NOT used directly in the final video. Each frame feeds a Hera MG prompt that generates the animated visual. Be generous — plan more frames than the minimum.

```
## Reference Frame Plan

| # | Source | Timestamp | Description | Feeds MG | Image Source Intent |
|---|--------|-----------|-------------|----------|-------------------|
| 1 | {long-form segment} | {single timestamp} | {specific visual — what exactly is on screen} | MG-{NN} | {frame-extract (Tier B candidate) / frame-extract for Hera reference (Tier C) / prompt-only (no reference needed)} |
| 2 | ... | ... | ... | MG-{NN} | ... |

**Total reference frames:** {count}
**Note:** These frames are NOT used directly. Each feeds a Hera MG prompt (see Motion Graphics section).
```

#### C. Motion Graphic Prompts (Detailed Hera Prompts)

Each MG prompt MUST follow the 6-part structure from script-rules.md. Include specific tool names with brand hex colors. Include reference image paths when MG features recognisable brands/tools.

```
## Motion Graphics

### MG-01: {Descriptor}

**Hera Prompt:**
> A sleek 9:16 vertical motion graphic showing {SUBJECT with specific brand names and hex colors}. {MOTION — how elements appear, move, and transition}. {STYLE — clean/minimal/corporate/energetic, dark or light theme}. Background: {hex color, default #0a0a0a}. {TIMING — element pacing relative to the duration}.

**Reference Image:** {path to branded-asset, frame-extract, canvas-build, or "none — prompt-only"}
**Aspect Ratio:** 9:16
**Duration:** {X}s
**In Script At:** {timestamp where this MG appears}

### MG-02: {Descriptor}
...

**Total MG clips:** {count}
**Total MG duration:** {X}s
```

#### D. Conceptual Storyboard

Plan V4b MG cutaways: at least 1 per 10–12 seconds. Each V4b has no caption — voiceover continues from adjacent speaker segment. Use content rules from script-rules.md (tool→logo, build→typing, stat→counter, default→abstract tech).

```
## Conceptual Storyboard

| # | Beat | Time | Duration | Visual Type | Layout | Caption Highlight | Notes |
|---|------|------|----------|-------------|--------|-------------------|-------|
| 1 | Hook | 0:00–0:02 | 2s | split-screen | V5 | {keyword} | Stop the scroll — recognizable visual top, speaker bottom |
| 2 | Hook | 0:02–0:04 | 2s | speaker-zoom | V2 | {keyword} | Deliver hook line |
| 3 | Body 1 | 0:04–0:07 | 3s | split-screen | V5 | {keyword} | Demo in top half |
| 4 | Body 1 | 0:07–0:08 | 1s | motion-graphic-cutaway | V4b | — | Tool logo MG cutaway (no caption) |
| 5 | Body 2 | 0:08–0:11 | 3s | motion-graphic | V4 | {keyword} | Full-frame Hera MG |
| ... | ... | ... | ... | ... | ... | ... | ... |
| N | CTA | 0:{X}–0:{Y} | {Z}s | cta | V7 | {keyword} | Comment CTA — abrupt ending |

**Total segments:** {count}
**V4b cutaways:** {count} (minimum: 1 per 10–12 seconds)
**Non-speaker coverage:** {X}% (target: 80%+; minimum floor: {65% Punchy / 65% Standard / 70% Deep})
**Visual types used:** {list} ({count} unique — minimum 3)
**V3 segments:** 0 (V3 broll is FORBIDDEN in short-form — use V4/V4b/V5 with MG)
```

#### D2. Body Video Moments (Story & Tool-Focus Scripts Only)

For **Story** and **Tool-Focus** scripts, add a table mapping each body beat to a specific body video timestamp. This feeds the Video Editor SF storyboard step with pre-curated frame extraction targets.

```
## Body Video Moments

| Beat | Script Words | Body Video Timestamp | What's Visible On Screen | MG Intent |
|------|-------------|---------------------|--------------------------|-----------|
| Beat 1 | "{first few words of the beat}..." | {MM:SS}–{MM:SS} | {specific description of what's on screen} | Tier {B/C} → MG-{NN} |
| Beat 2 | ... | ... | ... | ... |

**Total mapped moments:** {count}
**Note:** These timestamps are from the body/long-form video, not the short-form timeline.
```

For **Concept** and **Value-Drop** scripts: "N/A — concept-driven MGs."

#### E. Platform Copy

Adapt the video's hook angle to each platform's native style. Follow the Platform Copy Rules from script-rules.md. Never copy-paste the same text across platforms.

```
## Platform Copy

### Instagram Reel
**Caption:**
{Hook line — under 125 chars, keyword-rich, matches hook angle}

{1-2 sentence value line + comment-gated CTA}

{0-3 niche hashtags OR none}

### TikTok
**Caption:**
{Casual/raw hook — can use self-diagnosis or chaotic style, up to 300 chars}

{Comment-first CTA: "Comment '{KEYWORD}' below and then DM me '{KEYWORD}' — I'll send you [resource]!" Make the comment action crystal clear.}

{3-5 topic hashtags}

### YouTube Shorts
**Title:** {Under 40 chars, front-loaded keyword, curiosity gap}
**Description:**
🎁 Grab this free resource in my free community → {YOUR_COMMUNITY_URL}

{2-3 keyword-rich sentences summarizing the value}

Subscribe for more → @handle

{3-5 hashtags including #Shorts}
```

### 4. Apply Pacing Rules to Storyboard

For each conceptual storyboard, verify:
- **Hook opens with V5 split-screen (NOT V6)** — P4 rule
- No beat exceeds 4 seconds (120 frames) — P1 rule
- MG coverage meets the minimum for that duration category (65–70% floor, target 80%+) — P3 rule
- At least 3 different layout types (V1–V7) used — P5 rule
- **V4b cutaway frequency:** at least 1 per 10–12 seconds — P3 sub-rule
- **No V3 (broll) segments** — V3 is deprecated for short-form; use V4/V4b/V5 with MG
- **Min cut density:** at least 6 visual changes per 15 seconds — P10 rule
- No chapter cards (forbidden in short-form) — P6 rule
- Word count validation passes for all sections (delta within ±1s)

If any rule is violated, adjust the storyboard and rewrite script sections to fit.

### 5. Save Script Files

Save each script to `{project_folder}/{project-slug}/video-editor/short-form/scripts/sf-{NN}-script.md` where NN is 01–05.

Each file should have frontmatter:

```yaml
---
title: '{concept title}'
concept_id: 'SF-{NN}'
duration_category: '{Punchy / Standard / Deep}'
duration_target_s: {15-60}
word_count: {total words}
hook_type: '{hook type}'
broll_clips: {count}
mg_clips: {count}
source_segment: '{long-form segment name}'
source_timestamps: '{start}–{end}'
angle_type: '{Story / Tool-Focus / Concept / Value-Drop / Before/After}'
target_icp: '{Primary (TOFU) / Secondary (BOFU)}'
emotional_register: '{Curious / Energised / Pragmatic / Relieved / Challenged}'
style_reference: 'example-hooks.md Example {N} — {shortcode}'
date: '{current_date}'
stepsCompleted: ['script-write']
---
```

### 5b. Generate Combined Teleprompter File

After saving all 5 individual scripts, generate a single combined teleprompter file at:
`{project_folder}/{project-slug}/video-editor/short-form/scripts/sf-all-teleprompter.md`

This file allows the creator to read all 5 scripts back-to-back in a single recording session instead of starting/stopping 5 times.

**Format:**

```markdown
# Short-Form Teleprompter — All Scripts

Record all 5 scripts in one take. Leave a 3-second pause between each script.

---

## SF-01: {title}

{Teleprompter text — one sentence per line, max 8-10 words per line, ALL CAPS for emphasis words, no markers, double line breaks between sections, ... for pauses}

[PAUSE — 3 SECONDS]

---

## SF-02: {title}

{Teleprompter text}

[PAUSE — 3 SECONDS]

---

## SF-03: {title}

{Teleprompter text}

[PAUSE — 3 SECONDS]

---

## SF-04: {title}

{Teleprompter text}

[PAUSE — 3 SECONDS]

---

## SF-05: {title}

{Teleprompter text}
```

Follow the teleprompter formatting rules from script-rules.md for each script's text (one sentence per line, max 8-10 words per line, ALL CAPS for emphasis, double line breaks between sections, `...` for pauses).

### 6. Reference Image Coverage Check (MANDATORY)

Before marking scripts as complete, verify that every tool/platform mentioned in MG prompts has a matching screenshot in the central reference frame library. This prevents the video editor from hitting missing references during storyboarding.

1. **Scan all 5 scripts** for `[MG:` and `[REF-FRAME:` markers — extract every tool/platform name referenced in prompts and reference fields
2. **Read the library catalog** at `{project-root}/brand-assets/reference-frames/catalog.yaml`
3. **Match each tool** against the catalog's tool entries (check `display_name` and `aliases`)
4. **Report coverage:**

"**Reference Image Coverage:**

Tools with library coverage:
- {tool} ({count} frames) — used in {SF-NN list}
- ...

⚠️ Tools MISSING from library (need screenshots before video editing):
- {tool} (0 frames) — needed for {SF-NN list}

Please capture screenshots and drop them into:
`brand-assets/reference-frames/{tool-slug}/`
Then run: `npx tsx scripts/analyze-library-images.ts`"

5. **If all tools are covered** → proceed to summary
6. **If any tools are missing** → present the list and WAIT for user confirmation that screenshots have been added (or that they want to proceed without them)

### 7. Summary

"**5 Short-Form Scripts Written**

| # | Title | Category | Duration | Words | B-Roll | MG | Storyboard Beats | WC Valid | ICP | Register |
|---|-------|----------|----------|-------|--------|-----|-----------------|----------|-----|---------|
| SF-01 | {title} | Punchy | {X}s | {W} | {count} | {count} | {count} | ✅ | {Primary/Secondary} | {register} |
| SF-02 | {title} | Standard | {X}s | {W} | {count} | {count} | {count} | ✅ | {Primary/Secondary} | {register} |
| SF-03 | {title} | Standard | {X}s | {W} | {count} | {count} | {count} | ✅ | {Primary/Secondary} | {register} |
| SF-04 | {title} | Standard | {X}s | {W} | {count} | {count} | {count} | ✅ | {Primary/Secondary} | {register} |
| SF-05 | {title} | Deep | {X}s | {W} | {count} | {count} | {count} | ✅ | {Primary/Secondary} | {register} |

**Duration mix:** 1 Punchy + 3 Standard + 1 Deep ✅
**ICP coverage:** {N} Primary + {N} Secondary (≥1 Secondary required) ✅
**Emotional registers:** {list of distinct registers} (≥2 required) ✅
**Pacing rules:** All 5 pass ✅
**Word count validation:** All 5 within ±1s ✅
**Combined teleprompter:** `sf-all-teleprompter.md` generated ✅

**Proceeding to review...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- 5 complete scripts written with all 5 sections (script, B-roll plan, MG prompts, storyboard, platform copy)
- Duration mix: 1 Punchy + 3 Standard + 1 Deep
- All scripts follow Hook → Body → CTA structure
- Word count validation passes for all sections (within ±1s of allocation)
- MG density meets minimum per duration category (65% floor, 80%+ target)
- V4b cutaways planned at least 1 per 10–12 seconds
- No V3 (broll) segments in any storyboard — V4/V4b/V5 with MG only
- Hook opens with V5 split-screen (NOT V6) in every storyboard
- MG prompts follow 6-part structure with specific brand names, hex colors, motion, and timing
- Combined teleprompter file (`sf-all-teleprompter.md`) generated with all 5 scripts and 3-second pause markers
- Platform copy present and adapted per-platform (Instagram, TikTok, YouTube Shorts) for all 5 scripts
- Pacing rules verified for all storyboards (all P1–P11 rules)
- Files saved to correct output path
- Batch includes ≥1 Secondary ICP script (Before/After angle)
- Batch includes ≥2 distinct emotional registers across the 5 scripts
- Each script header (section 2c block) declares `target_icp` + `style_reference` before the hook is written
- Secondary ICP script uses BOFU CTA keyword (AUDIT / AI / RESULTS / ROI / SYSTEM) — not TOFU keywords

### ❌ SYSTEM FAILURE:

- Fewer than 5 scripts written
- Wrong duration mix (not 1-3-1)
- Word count delta exceeds ±1 second for any section
- Missing B-roll plan or MG prompts section in individual scripts
- Vague MG prompts (missing brand names, hex colors, motion description, or timing)
- MG density below minimum for duration category
- V3 (broll) segments present in any storyboard
- V6 (hook text) used as opening segment in any storyboard
- Missing V4b cutaways (fewer than 1 per 10–12 seconds)
- Storyboard violates pacing rules (P1–P11)
- Scripts don't include [REF-FRAME], [MG], and [V4b] markers with full detail
- Missing platform copy or identical copy across platforms
- Combined teleprompter file not generated or missing pause markers
- All 5 scripts are Primary ICP — no Secondary ICP (Before/After) script present
- TOFU keywords (BUILD, AGENT, TEMPLATE, etc.) used in the Secondary ICP script's CTA
