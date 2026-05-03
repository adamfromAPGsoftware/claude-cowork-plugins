---
name: diagram-generation
description: Generate a treasure-map-style visual diagram from a video script — pan+zoom HTML canvas with concept nodes, code panels, real screenshots from the reference frame library, and connected paths
menu-code: DG
---

# [DG] Diagram Generation

## Purpose

Parse a video script into a treasure-map-style visual diagram. A navigable HTML canvas — cream paper, dotted grid, paths weaving across sections — that visually explains the content discussed in the video.

Each diagram includes:
- **ConceptNodes** — titled cards for key ideas
- **CodeNodes** — terminal panels for prompts, code, commands
- **ScreenshotNodes** — real screenshots pinned from the reference frame library (or Gemini-generated where no match exists)
- **PromptNodes** — short Claude prompt bubbles
- **SectionSigns** — chapter dividers marking the start of each section
- **DecisionNodes** — branching points
- **QuoteNodes** — pull quotes from the script

The output is a self-contained HTML file. Open it in any browser, drag to pan, scroll to zoom — ready to use as a visual backdrop while filming.

## Prerequisites

Load workflow on activation:
`{project-root}/content-plugin/skills/2-copywriter/workflows/diagram-generation/workflow.md`

---

## On Activation

1. Load and read the full workflow from `workflows/diagram-generation/workflow.md`
2. Follow the INITIALIZATION SEQUENCE in that file
3. Present mode selection (Create / Edit) and execution mode (Auto / Collab)

---

## Output

Saved to: `{project_path}/copywriter/diagrams/diagram-{slug}.html`

Open in browser — double-click the file. Pan by dragging, zoom with scroll wheel.

---

## Success Criteria

- 4–8 sections covering the full video arc
- At least 4 different node types used
- At least 2 ScreenshotNodes with real images (from catalog or generated)
- All connectors route between actual node edges
- Title block and legend present
- HTML opens without errors in Chrome/Safari
- Pan and zoom work
