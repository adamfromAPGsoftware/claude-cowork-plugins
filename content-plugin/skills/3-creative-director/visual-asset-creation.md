---
name: visual-asset-creation
description: Create thumbnails, carousels, images, logos, and web captures
menu-code: VA
---

# [VA] Visual Asset Creation

## Purpose

Generate production-ready visual assets across the content pipeline — thumbnails (wide 16:9 + vertical 9:16) via Gemini with identity preservation, LinkedIn carousels/images via Puppeteer, Instagram carousels via Gemini per-slide generation, general image generation, logo fetching and canvas composition, and web page captures. All with brand consistency, CTR validation, and Creative Director visual expertise.

## Role Context

You are a visual asset architect and creative technologist. You bring expertise in visual design, composition, platform-specific visual psychology, and production pipeline orchestration.

---

## Phase 1: Initialization and Asset Type Selection

### 1.1 Load Config

Resolve: user_name, communication_language, content_output_folder, project_folder, standalone_folder, env_file.

### 1.2 Asset Type Menu

"**Visual Asset Creation. What are we building?**

**[TH]** YouTube Thumbnail (wide 16:9) — with identity preservation via Gemini
**[IC]** Instagram Carousel — per-slide generation with embedded screenshots
**[IM]** General Image — standalone image generation
**[LG]** Logo Fetch — source and compose brand logos
**[WC]** Web Capture — screenshot web pages for content
**[ET]** Edit Thumbnail — image-to-image refinement with identity preservation
**[VC]** Validate CTR — run 7-point checklist on any thumbnail/title pair

Select your asset type."

---

## Thumbnail Pipeline (TH)

### Plan Mode Detection

Check for `package-plan.md` in project thumbnails folder. If found:
- Auto-enable plan mode
- Use prompts EXACTLY as written in the plan (single source of truth)
- Do not modify, rephrase, or "improve" prompts

### From-Scratch Mode (No Plan)

1. Check for content-analysis.md for angle guidance
2. Ask user for topic, angle, desired expression
3. Draft 3 thumbnail compositions using the prompt template
4. Present for user approval

### Generation

For each approved composition:
```bash
python scripts/generate-thumbnail.py \
    --ref-dir {reference_photos_folder} \
    --inspo-dir {inspiration_folder} \
    --output {output_path}/{slugified-title}.png \
    --logo {logo_paths} \
    --prompt "{full_prompt_text}"
```

**Execution rules:**
- Attach creator reference photos (foundation image FIRST) for identity preservation
- Attach per-project inspiration thumbnails as style references
- Include `--logo` flags for any resolved brand PNGs
- Sequential generation only
- Maximum 5 combinations per batch
- NEVER describe the user's face in the text prompt

### Post-Generation

Run CTR validation on every generated thumbnail. Present results with scores.

---

## Instagram Carousel Pipeline (IC)

1. Load carousel template from `{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/data/instagram-carousel-guidelines-dark.md`
2. Plan slide-by-slide content (hook slide uses real photo, not reference photos)
3. Generate each slide via Gemini or compose via template
4. Sequential generation
5. Save to project output folder

## General Image Pipeline (IM)

1. Gather image requirements from user
2. Draft prompt
3. Generate via Gemini
4. Save to project output folder

## Logo Fetch Pipeline (LG)

Follow the logo sourcing waterfall:
1. Simple Icons (check first)
2. SVG Repo (fallback)
3. CompanyEnrich (last resort)

```bash
npx tsx scripts/fetch-logo.ts --name "{brand}" --output "{path}" --color "{brand-color}"
```

## Web Capture Pipeline (WC)

Use Puppeteer to screenshot web pages for content assets.

## Edit Thumbnail (ET)

Image-to-image refinement with identity preservation:
1. Load existing thumbnail
2. Gather change request
3. Build edit prompt with source image + reference photos
4. Generate refined version
5. Save as `-v2.png`
6. Re-run CTR validation

## Validate CTR (VC)

Run 7-point CTR checklist on any thumbnail/title pair:
1. Human face with clear emotional expression
2. Text under 12 characters
3. Readable at 168x94px (mobile)
4. Curiosity gap between title and thumbnail
5. 3-element composition
6. High contrast and visual clarity
7. Title/thumbnail unity

---

## Success Criteria

- Correct asset pipeline selected and executed
- Identity preservation via reference photos (thumbnails)
- Brand consistency maintained
- CTR validation on all thumbnails
- Plan mode honours package-plan.md exactly
- Sequential generation (never parallel)
- All assets saved to correct output paths
