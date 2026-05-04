---
name: 'step-03-script-write'
description: 'Write 5 agency short-form scripts with MG prompts, conceptual storyboard, platform copy, and combined teleprompter file'

nextStepFile: './step-04-review.md'
baseScriptRulesData: '{project-root}/content-plugin/skills/2-copywriter/workflows/short-form-scripts/data/script-rules.md'
agencyScriptRulesData: '../data/agency-script-rules.md'
---

# Step 3: Script Writing — Full Creative Plan for Each Video

## STEP GOAL:

Write 5 complete agency short-form video scripts with detailed Hera motion graphic prompts, conceptual storyboards, platform copy, and a combined teleprompter file. Each script is a self-contained creative brief for the Video Editor SF workflow. A combined teleprompter file is generated for single-session recording.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Write ALL 5 scripts in this step — do not split across steps
- Re-read BOTH {baseScriptRulesData} AND {agencyScriptRulesData} before writing — the agency rules OVERRIDE specific sections of the base rules
- Each script MUST follow the Hook -> Body -> CTA structure
- WORD COUNT VALIDATION: After writing each section, count words and verify against speaking rate (3.5 wps normal, 4.0 wps hook, 3.0 wps CTA). Calculated duration must be within +/-1 second of time allocation
- DURATION MIX: Apply the 2-2-1 distribution: 2 Punchy (15-20s), 2 Standard (22-30s), 1 Deep (35-45s)
- MG DENSITY: Near-constant MG is the standard (MG-first approach). Minimum clips per duration category enforced (Punchy: 4, Standard: 7, Deep: 10). Target 80%+ non-speaker coverage
- MG PROMPT QUALITY: Every MG prompt must follow the 6-part structure. Vague prompts = system failure
- FORBIDDEN to generate MG assets — only write the plan

## MANDATORY SEQUENCE

### 1. Re-Read Script Rules

Load and read both:
1. {baseScriptRulesData} — base speaking rates, structure, pacing, MG format, caption rules, teleprompter rules, platform copy rules
2. {agencyScriptRulesData} — agency overrides for duration mix, hooks, CTAs, brand voice, reference frames, content pillars

**Load Voice Reference Data:**
- Load `creator-voice.md` from `{project-root}/content-plugin/skills/2-copywriter/workflows/script-generation/data/inspiration/` — match the creator's sentence structure, contractions, and signature phrases
- Load `creator-credentials.md` from `{project-root}/content-plugin/skills/2-copywriter/workflows/script-generation/data/inspiration/` — reference for credibility mentions

**Key override reminders:**
- Duration mix is 2-2-1 (not 1-3-1)
- Default CTA is "Comment AUDIT" (not follow/community)
- Reference frames come from branded assets or prompt-only (not long-form video)
- Brand voice is 60% Business Value / 40% Technical Proof
- Credibility signals reference "300+ projects", "Top 1%", case study metrics (not community/YouTube)

### 2. Assign Duration Categories

From the 5 approved concepts, assign each to a duration category:

- **Hot takes, single metrics, waste reveals** -> Punchy (15-20s)
- **Pain point + solution, case study snapshot, tool comparison** -> Standard (22-30s)
- **Framework, step-by-step, detailed case study** -> Deep (35-45s)

Distribution MUST be: 2 Punchy + 2 Standard + 1 Deep.

**If `{execution_mode}` = `collab`:**
Present assignments to confirm before writing:

"**Duration Assignments:**
| # | Concept | Category | Target Duration | Word Budget |
|---|---------|----------|----------------|-------------|
| SF-01 | {title} | Punchy | 18s | ~60 words |
| SF-02 | {title} | Standard | 25s | ~88 words |
| ... | ... | ... | ... | ... |

[C] Confirm and proceed | [R] Revise assignments"

Wait for user confirmation before writing scripts.

**If `{execution_mode}` = `auto`:**
Assign categories based on concept complexity and proceed immediately.

### 3. Write Scripts (Per Video)

For each of the 5 approved concepts (SF-01 through SF-05), produce a complete script file with these sections:

#### A. Script (with word count validation)

```
## Script

**Duration category:** {Punchy / Standard / Deep}
**Duration target:** {X}s
**Word budget:** {Y} words (at {Z} wps average)
**Hook type:** {from concept generation}
**Value pillar:** {pillar}
**News source:** {headline or "Evergreen"}

### Hook (0:00-0:{HH}) — {W} words @ 4.0 wps = {T}s
{Exact words the speaker will say. Energetic, confident, business-operator tone.}

### Body (0:{HH}-0:{BB}) — {W} words @ 3.5 wps = {T}s
{Exact words for the body. Break into beats.}

**Beat 1 (0:{HH}-0:{B1})** — {W} words @ 3.5 wps = {T}s
{Speaker words for this beat.}
[MG: prompt="{detailed 6-part Hera prompt}" reference="{branded-asset path or 'none -- prompt-only'}" duration="{X}s"]

**Beat 2 (0:{B1}-0:{B2})** — {W} words @ 3.5 wps = {T}s
{Speaker words for this beat.}
[V4b: content_rule="{tool|build|stat|default}" mg_prompt_ref="MG-{NN}" duration="1-2s"]

{Continue beats...}

### CTA (0:{BB}-0:{CC}) — {W} words @ 3.0 wps = {T}s
{Exact words — default: "Comment AUDIT and I'll send you the checklist."}

### Word Count Validation
| Section | Words | WPS | Calculated Duration | Allocated Duration | Delta |
|---------|-------|-----|--------------------|--------------------|-------|
| Hook | {W} | 4.0 | {T}s | {A}s | {+/-D}s |
| Body | {W} | 3.5 | {T}s | {A}s | {+/-D}s |
| CTA | {W} | 3.0 | {T}s | {A}s | {+/-D}s |
| **Total** | **{W}** | — | **{T}s** | **{A}s** | **{+/-D}s** |
```

**CRITICAL:** If any section's delta exceeds +/-1 second, rewrite the section to match before proceeding.

#### B. Reference Frame Plan (for Hera MG Generation)

**No long-form video source.** Reference frames come from branded assets, tool screenshots, or prompt-only generation.

```
## Reference Frame Plan

| # | Source Type | Asset/Tool | Description | Feeds MG |
|---|------------|-----------|-------------|----------|
| 1 | branded-asset | brand-logo.png | {YOUR_COMPANY} logo on dark background | MG-{NN} |
| 2 | tool-screenshot | hubspot | HubSpot pricing page showing per-user fees | MG-{NN} |
| 3 | prompt-only | — | Abstract data flow showing scattered vs unified | MG-{NN} |

**Total reference frames:** {count}
**Note:** No long-form video source. Frames are branded assets, tool screenshots, or prompt-only MG generation.
```

#### C. Motion Graphic Prompts (Detailed Hera Prompts)

Each MG prompt MUST follow the 6-part structure. Include specific tool names with brand hex colors. Reference branded assets when MG features recognisable brands/tools.

```
## Motion Graphics

### MG-01: {Descriptor}

**Hera Prompt:**
> A sleek 9:16 vertical motion graphic showing {SUBJECT with specific brand names and hex colors}. {MOTION — how elements appear, move, and transition}. {STYLE — clean/minimal/corporate/energetic, dark or light theme}. Background: {hex color, default #0a0a0a}. {TIMING — element pacing relative to the duration}.

**Reference Image:** {path to branded-asset, tool screenshot, or "none -- prompt-only"}
**Aspect Ratio:** 9:16
**Duration:** {X}s
**In Script At:** {timestamp where this MG appears}

### MG-02: {Descriptor}
...

**Total MG clips:** {count}
**Total MG duration:** {X}s
```

#### D. Conceptual Storyboard

Same format as base script rules. Plan V4b MG cutaways at least 1 per 10-12 seconds.

```
## Conceptual Storyboard

| # | Beat | Time | Duration | Visual Type | Layout | Caption Highlight | Notes |
|---|------|------|----------|-------------|--------|-------------------|-------|
| 1 | Hook | 0:00-0:02 | 2s | split-screen | V5 | {keyword} | Stop the scroll — branded visual top, speaker bottom |
| 2 | Hook | 0:02-0:04 | 2s | speaker-zoom | V2 | {keyword} | Deliver hook line |
| ... | ... | ... | ... | ... | ... | ... | ... |
| N | CTA | 0:{X}-0:{Y} | {Z}s | cta | V7 | {keyword} | Comment AUDIT CTA — abrupt ending |

**Total segments:** {count}
**V4b cutaways:** {count} (minimum: 1 per 10-12 seconds)
**Non-speaker coverage:** {X}% (target: 80%+; minimum floor: {65% Punchy / 65% Standard / 70% Deep})
**Visual types used:** {list} ({count} unique — minimum 3)
**V3 segments:** 0 (V3 broll is FORBIDDEN in short-form — use V4/V4b/V5 with MG)
```

#### E. Platform Copy

Follow agency script rules platform copy overrides. Instagram Reel is PRIMARY for @{YOUR_HANDLE}.

```
## Platform Copy

### Instagram Reel (PRIMARY)
**Caption:**
{Hook line — under 125 chars, keyword-rich, business-outcome focused}

{1-2 sentence value line + comment-gated CTA matching video CTA keyword}

### TikTok
**Caption:**
{Casual/raw hook — self-diagnosis or direct business pain, up to 300 chars}

{Comment-gated CTA}

#BusinessAutomation #SME #AIForBusiness #OperationalEfficiency #SaaS

### YouTube Shorts
**Title:** {Under 40 chars, front-loaded keyword, business-outcome focus}
**Description:**
{2-3 keyword-rich sentences}

{Audit CTA + website link}

#Shorts #BusinessAutomation #AIForBusiness
```

### 4. Apply Pacing Rules to Storyboard

For each conceptual storyboard, verify:
- **Hook opens with V5 split-screen (NOT V6)** — P4 rule
- No beat exceeds 4 seconds (120 frames) — P1 rule
- MG coverage meets the minimum for that duration category (65-70% floor, target 80%+) — P3 rule
- At least 3 different layout types (V1-V7) used — P5 rule
- **V4b cutaway frequency:** at least 1 per 10-12 seconds — P3 sub-rule
- **No V3 (broll) segments** — V3 is deprecated for short-form; use V4/V4b/V5 with MG
- **Min cut density:** at least 6 visual changes per 15 seconds — P10 rule
- No chapter cards (forbidden in short-form) — P6 rule
- Word count validation passes for all sections (delta within +/-1s)

If any rule is violated, adjust the storyboard and rewrite script sections to fit.

### 5. Save Script Files

Save each script to `{agency_folder}/{project-slug}/copywriter/agency-sf/scripts/sf-{NN}-script.md` where NN is 01-05.

Each file should have frontmatter:

```yaml
---
title: '{concept title}'
concept_id: 'SF-{NN}'
channel: {YOUR_HANDLE}
content_type: agency-bofu
duration_category: '{Punchy / Standard / Deep}'
duration_target_s: {15-45}
word_count: {total words}
hook_type: '{hook type}'
value_pillar: '{pillar}'
news_source: '{headline or "Evergreen"}'
cta_keyword: '{AUDIT / WASTE / AI / RESULTS}'
mg_clips: {count}
date: '{current_date}'
stepsCompleted: ['script-write']
---
```

### 5b. Generate Combined Teleprompter File

After saving all 5 individual scripts, generate a single combined teleprompter file at:
`{agency_folder}/{project-slug}/copywriter/agency-sf/scripts/sf-all-teleprompter.md`

This file allows the creator to read all 5 scripts back-to-back in a single recording session.

**Format:**

```markdown
# Agency Short-Form Teleprompter — All Scripts (@{YOUR_HANDLE})

Record all 5 scripts in one take. Leave a 3-second pause between each script.
Film in LANDSCAPE (16:9) 4K. The pipeline handles proxy generation and centre-crop to 9:16.

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

Follow the teleprompter formatting rules from script-rules.md for each script's text.

### 6. Reference Image Coverage Check (MANDATORY)

Before marking scripts as complete, verify that every tool/platform mentioned in MG prompts has a matching screenshot in the central reference frame library. This prevents the video editor from hitting missing references during storyboarding.

1. **Scan all 5 scripts** for `[MG:` and `[REF-FRAME:` markers — extract every tool/platform name referenced in prompts and reference fields
2. **Read the library catalog** at `{project-root}/context/context/brand-assets/reference-frames/catalog.yaml`
3. **Match each tool** against the catalog's tool entries (check `display_name` and `aliases`)
4. **Report coverage:**

"**Reference Image Coverage:**

Tools with library coverage:
- {tool} ({count} frames) — used in {SF-NN list}
- ...

⚠️ Tools MISSING from library (need screenshots before video editing):
- {tool} (0 frames) — needed for {SF-NN list}

Please capture screenshots and drop them into:
`context/brand-assets/reference-frames/{tool-slug}/`
Then run: `npx tsx scripts/analyze-library-images.ts`"

5. **If all tools are covered** → proceed to summary
6. **If any tools are missing** → present the list and WAIT for user confirmation that screenshots have been added (or that they want to proceed without them)

### 7. Summary

"**5 Agency Short-Form Scripts Written**

| # | Title | Category | Duration | Words | MG | Storyboard Beats | WC Valid | Pillar |
|---|-------|----------|----------|-------|----|-----------------|----------|--------|
| SF-01 | {title} | Punchy | {X}s | {W} | {count} | {count} | {check} | {pillar} |
| SF-02 | {title} | Punchy | {X}s | {W} | {count} | {count} | {check} | {pillar} |
| SF-03 | {title} | Standard | {X}s | {W} | {count} | {count} | {check} | {pillar} |
| SF-04 | {title} | Standard | {X}s | {W} | {count} | {count} | {check} | {pillar} |
| SF-05 | {title} | Deep | {X}s | {W} | {count} | {count} | {check} | {pillar} |

**Duration mix:** 2 Punchy + 2 Standard + 1 Deep
**Pacing rules:** All 5 pass
**Word count validation:** All 5 within +/-1s
**Combined teleprompter:** `sf-all-teleprompter.md` generated
**Channel:** @{YOUR_HANDLE}
**Default CTA:** Comment AUDIT

**Proceeding to review...**"

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- 5 complete scripts written with all 5 sections (script, reference frame plan, MG prompts, storyboard, platform copy)
- Duration mix: 2 Punchy + 2 Standard + 1 Deep
- All scripts follow Hook -> Body -> CTA structure
- Word count validation passes for all sections (within +/-1s of allocation)
- MG density meets minimum per duration category (65% floor, 80%+ target)
- V4b cutaways planned at least 1 per 10-12 seconds
- No V3 (broll) segments in any storyboard
- Hook opens with V5 split-screen (NOT V6) in every storyboard
- MG prompts follow 6-part structure with specific brand names, hex colors, motion, and timing
- Reference frames use branded-asset/tool-screenshot/prompt-only sources (NO long-form video references)
- Combined teleprompter file generated with all 5 scripts and 3-second pause markers
- Platform copy present with Instagram Reel as PRIMARY and adapted per-platform
- CTA defaults to "Comment AUDIT" pattern (not follow/community)
- Frontmatter includes channel: {YOUR_HANDLE}, content_type: agency-bofu
- Files saved to agency-sf/ output path (NOT short-form/)

### FAILURE:

- Fewer than 5 scripts written
- Wrong duration mix (not 2-2-1)
- Word count delta exceeds +/-1 second for any section
- Vague MG prompts (missing brand names, hex colors, motion, or timing)
- Reference frames pointing to long-form video source/timestamps
- Using @{YOUR_HANDLE_PERSONAL} CTAs (follow, community, Skool)
- MG density below minimum for duration category
- V3 (broll) segments present in any storyboard
- V6 (hook text) used as opening segment
- Scripts saved to short-form/ instead of agency-sf/
- Missing platform copy or identical copy across platforms
- Combined teleprompter file not generated
