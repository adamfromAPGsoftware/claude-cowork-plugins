---
name: short-form-thumbnail
description: Generate vertical 9:16 thumbnails with style guide and inspiration images
menu-code: SF
---

# [SF] Short-Form Thumbnail

## Purpose

Generate vertical 9:16 thumbnails for YouTube Shorts, TikTok, and Instagram Reels using the short-form style guide and pre-loaded inspiration images.

## Role Context

You are a short-form visual strategist who knows the composition blueprint, colour system (green/lime, not red), and typography rules for vertical thumbnails. Draft 1 concept per short-form video for user approval before spending API credits.

---

## Critical Rules

- NEVER generate thumbnails before user approves concepts
- Load the style guide and ALL 3 inspiration images before drafting concepts
- Every prompt must be FULLY RESOLVED — no placeholders, no brackets
- Brand uses GREEN/LIME banners (#39FF14 or #00E676) — NEVER red
- Sequential generation only — NEVER parallelise
- ONE thumbnail per short-form video — not multiple concepts per video

### Expression Rules (Subtle and Natural Only)

Allowed: Slight smile, Thoughtful (hand on chin), Curious (slight head tilt), Neutral/confident.
NEVER: frowning, shocked, surprised, jaw-drop, wide-eyed, overly excited, unhappy, serious/stern, exaggerated.

### Icon/Logo Rules

- All 3 icon positions (top, left, right) MUST be visually distinct
- Claude has its own logo (terracotta/orange "C" swirl), different from Anthropic corporate logo
- Claude Code has a terminal-style icon variant
- Prefer real brand logos over generic icons — never duplicate a brand to fill a slot

---

## Phase 1: Load Style Guide and Inspiration

1. Load short-form style guide from `{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/data/short-form-style-guide.md`
2. Load ALL inspiration images from `{project-root}/_bmad/_memory/creative-director-sidecar/short-form-inspiration/` (inspo-01.png, inspo-02.png, inspo-03.png)
3. Verify minimum 2 inspiration images exist
4. Load brand config for reference photo registry and colour palette
5. If active project, load keyword research (latest version) and build `{keyword_pool}`

## Phase 2: Auto-Detect Scripts (Project Mode)

Scan `{project_folder}/{active_project}/video-editor/short-form/scripts/` for `sf-*-script.md`. For each, read frontmatter (title, concept_id, hook_type, status). Only process approved scripts.

Present detection summary. User selects which to generate.

If no scripts found: fall back to manual input (video description, vibe, tools/brands, visual elements, title slug).

## Phase 3: Draft Thumbnail Concepts

Draft 1 concept per video. For each:

| Field | Value |
|-------|-------|
| Top icon | Main topic brand/icon |
| Floating icon (L) | Brand logo, rounded-square, 3D tilt |
| Floating icon (R) | Brand logo, rounded-square, 3D tilt |
| Expression | Subtle expression from allowed list |
| Background | Themed background treatment |
| Text line 1 | White medium-weight ALL CAPS, modern geometric sans-serif, ~60-70% of line 2 size, dark stroke |
| Text line 2 | White ultra-bold ALL CAPS, same sans-serif, dark stroke, thick green (#90F23C) underline bar |
| Char count (line 2) | {count} |
| Keywords used | Which keywords from pool informed this concept |

Include **Full Gemini Prompt** — exact text ready to send, no placeholders. Must specify: 9:16 (1080x1920), person centered chest-up, 2 floating icons with 3D tilt, top brand icon, themed background, bottom padding (160px dark safe zone), match inspiration thumbnails.

Typography must be specified exactly with font sizes, weights, stroke widths, and the green underline bar.

## Phase 4: Approval

Present concepts for user approval. Options: Approve all, select specific, request revisions.

## Phase 5: Logo Sourcing (Auto)

After approval, before generation:
1. Extract all brand names from approved concepts
2. Check if PNGs already exist in logos folder
3. Fetch missing logos via `npx tsx scripts/fetch-logo.ts`
4. Report results

## Phase 6: Generate Thumbnails

Load pipeline scripts reference. For each approved concept:
```bash
python scripts/generate-thumbnail.py \
    --ref-dir {reference_photos_folder} \
    --inspo-dir {sidecarInspirationFolder} \
    --output {output_folder}/sf-{NN}.png \
    --logo {logo_paths} \
    --prompt "{exact prompt}"
```

Sequential generation. Reference photos first (foundation image FIRST). Include all 3 inspiration images.

## Phase 7: CTR Validation

Load CTR checklist. Run 7-point validation on each generated thumbnail.

## Phase 8: Save and Complete

Save thumbnails as sf-01.png through sf-05.png. Save prompts as short-form-prompts.md. Present completion table with CTR scores. Offer: [E] Edit a thumbnail, [D] Done.

---

## Success Criteria

- Style guide and all 3 inspiration images loaded
- Keyword research loaded when available
- Scripts auto-detected when available
- 1 concept per video (not 3)
- Text lines incorporate keywords
- Icons reflect keyword brands
- Expressions subtle and natural
- User approved before generation
- Logos fetched correctly
- Green/lime banner colour used
- Bottom padding specified
- CTR validation run on every thumbnail
