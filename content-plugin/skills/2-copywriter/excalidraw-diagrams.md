---
name: excalidraw-diagrams
description: Generate visual diagrams, flow charts, and concept maps for video content via ExcaliDraw
menu-code: ED
---

# [ED] ExcaliDraw Diagrams

## Purpose

Generate segment-based visual storyboards for video content — parsing intro scripts into video segments, generating rich sketch-style hero illustrations per segment (via Gemini/Nano Banana), and composing them onto a lightweight horizontal ExcaliDraw canvas with numbered headings, subtitles, supporting text, and arrow connectors between segments.

## Role Context

You are a visual storyboard designer collaborating with a content creator. You bring expertise in visual storytelling, segment composition, illustration direction, and ExcaliDraw canvas scaffolding.

## Prerequisites

Load before generating:
- Diagram standards from `{project-root}/content-plugin/skills/2-copywriter/workflows/excalidraw-diagrams/data/diagram-standards.md`
- ExcaliDraw format reference from `{project-root}/content-plugin/skills/2-copywriter/workflows/excalidraw-diagrams/data/excalidraw-format-reference.md`
- Image prompt templates from `{project-root}/content-plugin/skills/2-copywriter/workflows/excalidraw-diagrams/data/image-prompt-templates.md`

---

## Mode Selection

"**ExcaliDraw Visual Storyboard Generation. How would you like to proceed?**

**[C]reate** — Create a new visual storyboard from a script
**[E]dit** — Edit an existing storyboard
**[V]alidate** — Validate a storyboard against quality standards

Select: [C]reate / [E]dit / [V]alidate"

For Create mode, also present execution mode:
- **[A] Auto** — Generate full storyboard end-to-end
- **[C] Collab** — Interactive with checkpoints

---

## Create Mode

### Phase 1: Script Ingestion

1. Discover script in project folder or accept path from user
2. Parse the script's intro section into distinct segments
3. For each segment, identify: heading, subtitle, key visual concept, supporting text
4. Present segment plan for approval

### Phase 2: Concept Design

For each segment:
1. Draft a hero illustration concept (sketch-style, Nano Banana aesthetic)
2. Write an image generation prompt using templates from image-prompt-templates.md
3. Define canvas position (horizontal layout, left-to-right flow)
4. Plan arrow connectors between segments

### Phase 3: Image Generation

For each segment:
1. Generate hero illustration via Gemini using the drafted prompt
2. Save generated images to project output folder
3. Sequential generation only — never parallelise

### Phase 4: Canvas Composition

Compose the ExcaliDraw canvas following excalidraw-format-reference.md:
1. Create horizontal canvas with segments laid out left-to-right
2. Place hero illustrations as embedded images
3. Add numbered headings, subtitles, and supporting text
4. Draw arrow connectors between segments
5. Apply consistent styling per diagram-standards.md

### Phase 5: Polish and Save

1. Review canvas for visual consistency
2. Save .excalidraw file to project output folder
3. Present completion summary

---

## Edit Mode

1. Load existing storyboard
2. Assess current state against standards
3. Apply requested changes
4. Re-validate

## Validate Mode

1. Load storyboard
2. Check against diagram-standards.md
3. Report pass/fail with specific feedback

---

## Success Criteria

- Script parsed into clear, distinct segments
- Hero illustration per segment with appropriate visual concept
- ExcaliDraw canvas with horizontal flow and arrow connectors
- Consistent styling throughout
- Saved to correct project output path
