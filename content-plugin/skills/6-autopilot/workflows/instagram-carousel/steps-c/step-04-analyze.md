---
name: step-04-analyze
description: Analyze top scraped inspiration posts for style patterns and psychology
nextStep: ./step-05-ideate.md
---

# Step 4: Analyze Inspiration

## Goal

Extract the structural and psychological patterns that make the top scraped posts perform. Build a style brief that informs our carousel design — not what to say, but HOW to say it.

## Sequence

### 1. Load Top Posts

Read `meta.json` files from `{inspirationDir}` across all handles.

Sort by engagement rate: `(likes + comments * 3) / slide_count` — comments weighted higher as a stronger signal.

Select the top 5 posts by engagement rate.

**Static inspiration library (always load this):** Read the 5 pre-analyzed outlier posts from `{existingInspiration}`. These are confirmed viral Claude-niche carousels (8K–14K comments) from @itstylergermain and @aifornontechies. Each post directory contains slide JPGs and a `meta.json` with engagement data. Treat these as ground truth for what works in our exact niche — weight them heavily even when fresh scraped posts are available. The `instagram-carousel-inspiration.md` file in `{existingInspiration}/../` contains a full written breakdown of all 5 posts.

If the Apify-scraped library has fewer than 3 posts, use the static inspiration library exclusively.

### 2. Visually Analyze Slides

For each of the top 5 posts, read its slide images (the Read tool can display PNGs as Claude is multimodal).

For each carousel, analyze and record:
- **Slide count** — total slides (common patterns: 5, 7, 9, 10)
- **Hook technique** — what the first slide does (bold claim, shocking stat, question, visual contrast)
- **Text density** — words per slide (minimal: <10, medium: 10-20, dense: 20-30)
- **Text placement** — top-aligned, centered, bottom-aligned, layered over image
- **Visual style** — dark background, bright accent color, photo background, flat design
- **Color palette** — dominant colors and accent
- **Typography weight** — bold headlines only, mixed weight, all caps vs sentence case
- **Transition feel** — does each slide clearly lead to the next? How?
- **CTA slide** — what does the final slide ask for? (comment keyword, follow, link in bio)
- **Caption length** — approximate word count

### 3. Identify Dominant Patterns

Across all 5 posts, identify the 2-3 patterns that appear most consistently in the highest-performing posts.

Examples:
- "All top posts use 7 slides with a single bold stat per slide (under 12 words)"
- "Hook slide always uses a polarizing claim — no questions"
- "Dark background with single neon accent, minimal text"
- "Slides 2-6 each answer one sub-question raised by the hook"

### 4. Cross-Reference Our Guidelines

Compare the dominant patterns against our dark-mode carousel guidelines at `{carouselGuidelines}`.

Note any patterns from inspiration that our guidelines already capture vs. new insights to incorporate.

### 5. Build Style Brief

```
STYLE BRIEF — for step-07 visual generation

Slide count target: {N} slides
Hook slide:        {technique description}
Content slides:    {text density, placement, pattern per slide}
Visual style:      {description matching our brand + inspiration patterns}
CTA slide:         {format description}
Typography:        {weight, case, max words per slide}
Key insight:       {1-2 sentences on WHY these posts perform}
```

Then immediately load and execute step-05.
