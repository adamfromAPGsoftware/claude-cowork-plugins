---
name: draft-package
description: Keyword research, title/thumbnail combos, CTR pre-validation, and package plan
menu-code: DP
---

# [DP] Draft Package

## Purpose

Plan and draft a complete title/thumbnail package before spending API credits on generation. Produces a `package-plan.md` file with titles, prompts, compositions, CTR pre-scores, YouTube description, and generation config — all reviewable and editable before generation.

## Role Context

You are a thumbnail strategist and title copywriter. You combine CTR psychology, keyword data, and visual composition expertise. This is the planning phase — no API credits are spent here.

## Mode Detection

- `DP auto` -> workflow_mode = auto (skip all menus, use autonomous criteria)
- `DP` or `DP collab` -> workflow_mode = collab (interactive)

---

## Phase 1: Initialization

### 1.1 Load Config

Resolve: user_name, communication_language, content_output_folder, project_folder, standalone_folder, env_file, reference_photos_folder.

### 1.2 Project Context

Verify active project. Set output path: `{project_folder}/{project-slug}/creative-director/thumbnails/`

### 1.3 Check Existing Content Analysis

Look for `content-analysis.md` in the thumbnails folder. If found, load the selected angles as starting context.

---

## Phase 2: Inspiration Thumbnail Fetch

**Automatic step — runs before any creative work begins.**

Check `{project_folder}/{project-slug}/creative-director/thumbnails/inspiration/` for existing inspiration thumbnails.

**If the folder is empty or doesn't exist:**
1. Create the folder if needed
2. Build search queries from the project's content topic and keywords (use script title, concept brief angle, and competitive research terms)
3. Build primary keywords from the core topic terms (e.g. "claude code", "marketing agency", "meta ads", "cowork", "dashboard")
4. Build secondary keywords from related/supporting terms (e.g. "automation", "ROAS", "AI agent", "plugin")
5. Run the inspiration fetch algorithm:
```bash
python3 scripts/fetch-inspiration-thumbnails.py \
    --queries "{query1},{query2},{query3},{query4}" \
    --primary-keywords "{primary1},{primary2},{primary3}" \
    --secondary-keywords "{secondary1},{secondary2},{secondary3}" \
    --output {project_folder}/{project-slug}/creative-director/thumbnails/inspiration \
    --top 3 \
    --min-views 10000
```
6. Read the downloaded thumbnails (view the images) and `metadata.md` to extract the visual language

**If inspiration thumbnails already exist:**
1. Read the images and `metadata.md`
2. Skip the fetch — use what's there

**Visual Language Extraction (mandatory):**
After loading inspiration thumbnails, analyse and document:
- Background style and colour palette (light/dark, gradients, textures)
- Face position and expression style
- Text placement, font weight, colour treatment
- Brand mark placement and style
- Overall energy (educational, bold, minimal, etc.)

This extracted visual language becomes the **binding style reference** for all compositions in Phase 5.

---

## Phase 2b: Content Analysis

If no content-analysis.md exists, perform inline content analysis:
1. Scan project for script, concept brief, storyboard
2. Extract the core topic, key transformation, and emotional hooks
3. Identify 3-5 thumbnail angles

## Phase 3: Keyword Research

Run 3-layer YouTube keyword research waterfall:

**Layer 1: YouTube Autocomplete**
- Use seed keywords from content topic
- Extract autocomplete suggestions

**Layer 2: Google Trends**
- Query pytrends for related queries and interest over time
- Flag rising/breakout terms

**Layer 3: YouTube Data API**
- Search competitor videos on the topic
- Extract tags from top performers

Present keyword results: high-signal (2+ layers), rising terms, competitor tags.
Save keyword report to project folder.

## Phase 4: Title Generation

Generate 3-5 title options informed by keyword research:
- Each title under 60 characters
- Incorporate high-signal keywords naturally
- Mix angles: curiosity, tutorial, contrarian, result-led
- Title and thumbnail are ONE unit — design together

Present titles for user selection (Collab) or auto-select top 3 (Auto).

## Phase 5: Composition Drafting

For each selected title, draft a thumbnail composition **sourced from the inspiration thumbnails' visual language** (extracted in Phase 2):

- **Scene description** — what the viewer sees
- **Expression** — from the expression performance ranking
- **3-element layout** — face position, object/context, text overlay (mirror the layout patterns observed in inspiration)
- **Text overlay** — under 12 characters, high contrast
- **Background treatment** — MUST match one of the palettes extracted from inspiration (e.g. if inspiration uses cream/warm backgrounds, compositions should default to cream/warm; if dark, default to dark). Do NOT invent a palette that doesn't appear in the inspiration set.
- **Colour palette** — explicitly reference the hex codes and colour relationships observed in inspiration thumbnails
- **Composition pattern** — mirror the face position, text placement, and object layout from the highest-performing inspiration thumbnails
- **Full image prompt (fal-ai/nano-banana-2)** — exact text ready for API, no placeholders. Every prompt MUST:
  1. Open with: "YouTube thumbnail matching the style of the provided inspiration thumbnails."
  2. Reference the specific colour palette extracted from inspiration (not generic defaults)
  3. Match the background treatment observed in inspiration (light/dark/gradient/texture)
  4. Include the identity preservation paragraph
  5. Reference composition layout from inspiration (e.g. "face right third matching inspo layout")

**Palette mixing rule:** If the inspiration set contains both light and dark styles, compositions may use either — but each combo must clearly state which inspiration thumbnail it's drawing from and why. Never invent a third palette that doesn't exist in the inspiration.

Follow the thumbnail prompt template for 16:9 wide thumbnails.

## Phase 6: CTR Pre-Validation

Run the 7-point CTR checklist on each title/thumbnail combination:
1. Human face with clear emotional expression
2. Text under 12 characters
3. Readable at 168x94px (mobile)
4. Curiosity gap between title and thumbnail
5. 3-element composition (face + object + text)
6. High contrast and visual clarity
7. Title/thumbnail unity (one visual story)

Score each combo. Flag anything below 5/7 for revision.

## Phase 7: YouTube Description

Draft complete YouTube description:
- Hook line (mirrors video intro)
- Video summary (2-3 sentences)
- Chapter markers (from transcript — see rules below)
- Links mentioned
- Free resources
- CTA section
- Tags

### Chapter Timestamps — Source Priority

**CRITICAL: Chapter timestamps MUST come from the actual recorded video, NOT the pre-written script.** Scripts contain estimated timings that are almost always wrong — the real video will have different pacing, cuts, and total duration.

**Source priority (use the first one that exists):**
1. **Storyboard chapters** — `{project_folder}/{project-slug}/video-editor/storyboard/chapters.json` — definitive chapter timestamps with absolute times derived from the clipped transcript
2. **Full storyboard** — `{project_folder}/{project-slug}/video-editor/storyboard/full-storyboard.md` — chapter card table with body offsets and absolute timestamps
3. **Clipped transcript** — `{project_folder}/{project-slug}/video-editor/clips/body-clipped-transcript.json` — word-level timestamps from the actual recording (requires manual chapter detection)

**If none of these exist** (video not yet recorded/edited): use placeholder timestamps from the script with a clear `[PLACEHOLDER — update from transcript after edit]` warning. Do NOT present script timestamps as final.

**Format:** Convert absolute seconds to `M:SS` or `MM:SS` format. Include an "0:00 — Intro" entry for the intro segment that precedes the first body chapter.

## Phase 8: Write Package Plan

Save `package-plan.md` to `{project_folder}/{project-slug}/creative-director/thumbnails/` with:
- All title/thumbnail combos with prompts
- CTR pre-scores
- Keyword research summary
- YouTube description
- Generation config (reference photos, inspiration folder, output paths)

Present completion summary. This package plan is the input for [VA] Visual Asset Creation in plan-mode.

---

## Success Criteria

- Keyword research performed (3-layer waterfall)
- 3-5 title/thumbnail combos drafted with full image prompt (fal-ai/nano-banana-2)s
- CTR pre-validated (7-point checklist)
- YouTube description complete
- Package plan saved for downstream consumption
- No API credits spent (planning only)
