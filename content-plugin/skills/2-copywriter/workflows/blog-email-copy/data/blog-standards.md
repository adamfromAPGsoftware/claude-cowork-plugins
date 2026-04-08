# Blog Post Standards

## SEO Structure Rules

### Meta Tags
- **Meta title:** ≤60 characters, primary keyword front-loaded
- **Meta description:** ≤155 characters, includes CTA language

### Heading Hierarchy
- **H1:** Single, benefit-driven headline incorporating primary keyword — targets both ICPs
- **H2 sections:** 3-6 core content sections, each with a keyword-rich H2 header
- **H3 sub-headers:** Use within longer sections to aid scannability
- **Primary keyword placement:** H1, meta title, first 100 words, and at least 2 H2 headers
- **Secondary/trending keywords:** Distributed naturally across sections (no stuffing)

### Introduction
- Hook paragraph: 2-3 sentences max creating curiosity + stating what the reader will gain
- Include primary keyword naturally within the first 100 words

---

## Readability Rules

- **Flesch reading ease target:** 60-70
- **Paragraphs:** 2-4 sentences max — no walls of text
- **Formatting:** Bold key phrases, use bullet lists and numbered steps liberally
- **Hook-driven sections:** Every H2 section opens with something that earns the next sentence
- **Conversational tone:** Write like explaining to a smart colleague, not lecturing
- **White space:** Generous spacing between sections — the post should breathe
- **Pattern interrupts:** Mix prose with lists, bold callouts, and image breaks to maintain attention
- **Front-load value:** Put the most useful insight in each section first, context second
- **Active voice:** Default to active voice throughout. Passive voice only when it reads more naturally

---

## Dual-Funnel Check

Every section must pass the dual-funnel test:

- **Builder angle:** Does this section teach something actionable? What skill or knowledge do they gain?
- **SME angle:** Does this section demonstrate ROI or business value? What outcome is shown?
- **If a section only speaks to one audience:** Sharpen it or add a bridging sentence
- **ICP reference:** Reference ICP profiles from the copywriter agent sidecar (`_bmad/_memory/copywriter-sidecar/`) for specific audience pain points, language patterns, and resonance triggers when sharpening sections

---

## CTA Formatting

The YouTube/video CTA MUST be a visually prominent callout block:

- Wrap in a blockquote or visually distinct container (e.g., `> **heading**`)
- Include a compelling one-line hook above the link (e.g., "Want to see this built from scratch?")
- The link uses bold anchor text with an arrow: **[Watch the full build process →](YouTube-URL)**
- Separate from surrounding content with horizontal rules (`---`) above and below
- The CTA block should feel like a standalone visual element — not buried in a paragraph
- **NEVER** display the raw URL. If YouTube URL is not available, use placeholder: **[Watch the full build →](YOUTUBE_URL)**

---

## Image Embedding

### Source Priority
Images come from the project image catalog (built in Step 1). Use this priority:

1. **Diagrams** (`type: diagram`) — Excalidraw exports from `copywriter/diagrams/images/`. Best for illustrating concepts, frameworks, and architectures. Embed inline where the concept is discussed.
2. **B-roll stills** (`type: broll`) — Extracted from `video-editor/broll/`. Best for visual breaks showing real examples, screen recordings, or demonstrations. Embed between major sections.
3. **Thumbnails** (`type: thumbnail`) — From `creative-director/thumbnails/`. Best as the hero/header image at the top of the post.
4. **Motion graphics** (`type: motion-graphic`) — From `video-editor/motion-graphics/`. Reference with "see the animation in the video" + CTA link, or extract a still frame if appropriate.

### Embedding Rules
- Aim for **3-6 images** per post depending on length and available assets
- Use relative paths for project images: `![alt text](../relative/path/to/image.ext)`
- **Alt text:** Descriptive, containing target keywords: `![Building an AI agent workforce with Claude Code](path/to/diagram.png)`
- Place images at natural breakpoints — after introducing a concept, between sections, or to illustrate a key point
- Cap at contextually appropriate number — don't over-embed
- Every image should earn its place by adding visual value the text alone can't deliver
- If the image catalog is empty, the post still works — images are enhancement, not requirement

### Complex Image Layouts

When single-column markdown image syntax isn't sufficient, use inline HTML for richer layouts. Prefer markdown for single images — only use HTML when the layout requires it.

**Side-by-side images:**
```html
<div style="display: flex; gap: 16px; margin: 24px 0;">
  <div style="flex: 1;">
    <img src="../relative/path/image-1.png" alt="Description 1" style="width: 100%; border-radius: 8px;" />
  </div>
  <div style="flex: 1;">
    <img src="../relative/path/image-2.png" alt="Description 2" style="width: 100%; border-radius: 8px;" />
  </div>
</div>
```

**Image with caption:**
```html
<figure style="margin: 24px 0; text-align: center;">
  <img src="../relative/path/image.png" alt="Description" style="max-width: 100%; border-radius: 8px;" />
  <figcaption style="margin-top: 8px; font-size: 14px; color: #666; font-style: italic;">Caption text here</figcaption>
</figure>
```

**When to use HTML layouts:**
- Two related images that should be compared side-by-side (e.g., before/after, two architecture diagrams)
- An image that needs a caption for additional context (e.g., crediting a source, explaining what's shown)
- Three-column layouts for feature comparisons

**Rule:** Prefer standard markdown `![alt](path)` for single images. Only reach for HTML when the layout adds meaning that a single image can't deliver.

### Style References

If `inspiration/blog.md` exists in the copywriter memory sidecar (`_bmad/_memory/copywriter-sidecar/inspiration/blog.md`), load it during drafting for style pattern guidance — sentence rhythms, opening hooks, section transitions, and formatting preferences observed from approved content.

---

## Key Takeaways Section

- Numbered list, scannable, immediately useful
- 5-7 bullet points
- Each takeaway should stand alone as valuable

---

## Blog Output Frontmatter Schema

This schema is required for downstream publish compatibility:

```yaml
---
title: ""
meta_title: ""
meta_description: ""
primary_keyword: ""
secondary_keywords: []
category: ""
date: ""
status: draft
stepsCompleted: []
format: blog
images_used: []
---
```

---

## Quality Checklist

Before presenting a blog draft, verify:

- [ ] Primary keyword in H1, meta title, first 100 words, and 2+ H2 headers
- [ ] Meta title ≤60 characters with keyword front-loaded
- [ ] Meta description ≤155 characters with CTA language
- [ ] All sections pass dual-funnel check
- [ ] Flesch readability 60-70 range
- [ ] Short paragraphs (2-4 sentences max)
- [ ] YouTube CTA formatted as prominent callout block
- [ ] Project images embedded from catalog (3-6 when assets available)
- [ ] All images have keyword-rich alt text
- [ ] Key takeaways section with 5-7 items
- [ ] Active voice throughout
- [ ] No keyword stuffing
