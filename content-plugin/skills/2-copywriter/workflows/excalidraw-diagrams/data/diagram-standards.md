# Storyboard Standards

## Visual Style Requirements

### ExcaliDraw Canvas Settings
- **Background:** `#FAFAFA` (warm off-white — set via `appState.viewBackgroundColor`)
- **Roughness:** 0 (clean architect style — polished, not hand-drawn)
- **Fill Style:** solid
- **Stroke Width:** 2 for standard elements, 3 for emphasis
- **Font Family:** 1 (Virgil/hand-drawn) for headings, 5 (default) for body text

### Colour Palette — Cold Orange

| Role | Hex | Fill | Usage |
|------|-----|------|-------|
| Primary | `#E8590C` | `#FFF4E6` | Main flow boxes, primary concepts |
| Amber | `#F08C00` | `#FFF9DB` | Tool/service boxes, secondary concepts |
| Green | `#2F9E44` | `#EBFBEE` | Success, highlights, Opus 4.7/new elements |
| Purple | `#7048e8` | `#F3F0FF` | External services, analysis steps |
| Heading | `#1A1A1A` | — | Primary text (near-black on light bg) |
| Body | `#495057` | — | Secondary text, annotations |
| Arrow | `#E8590C` | — | Flow arrows (orange = momentum) |
| Dimmed | `#CED4DA` | `#F8F9FA` | Inactive/background elements in variant diagrams |
| Canvas | `#FAFAFA` | — | Background |

### Typography Hierarchy

| Level | fontSize | Font | Color | Usage |
|-------|----------|------|-------|-------|
| Diagram Title | 28-32 | Virgil (1), bold | `#1A1A1A` | Top-level heading |
| Box Label | 16-18 | Virgil (1) | Stroke color | Centered inside boxes |
| Subtitle | 14-16 | Default (5) | `#495057` | Descriptive line below box |
| Annotation | 12-13 | Default (5) | `#495057` | Small callout text |
| Badge | 13 | Default (5) | Stroke color | Highlighted callout badges |

## Segment Anatomy (storyboard / horizontal flow)

Each segment in the storyboard follows this horizontal structure:

```
  ┌─────────────────────┐      ──────→      ┌─────────────────────┐
  │  Stage Name         │                   │  Next Stage         │
  │  [Logo if relevant] │                   │  [Logo if relevant] │
  └─────────────────────┘                   └─────────────────────┘
       annotation                                annotation
```

### Pipeline Box Dimensions
- **Single-stage box:** ~220-250px wide × 70px tall
- **Cluster box (parallel stages):** ~200px wide × 62px tall, 20-30px gaps
- **Arrow gap (between stages):** 60-100px for straight arrows

### Logo Placement
- Size: 36-44px inside or directly beside the box
- Position: right-aligned inside the box, vertically centered OR to the right of box label
- Only add logos where they add information (tool identity, brand recognition)
- Missing logos degrade gracefully — use a text badge instead

## Layout Patterns

### Horizontal Pipeline (primary pattern)
- **Direction:** left → right
- Canvas scales with stage count: `(stages × ~320px)` + padding
- Canvas height: ~700-800px
- Vertical center for single-stage boxes: ~350px
- Parallel/cluster stages centered around the same vertical midpoint
- Final output: single `.excalidraw` file (no variants unless specifically needed)

### Fan-out / Fan-in
For parallel stages (e.g., multiple analysis steps running simultaneously):
- Draw diagonal arrows from the preceding single box to each parallel box (fan out)
- Draw diagonal arrows from each parallel box back to the next single box (fan in)
- Add an annotation: "runs simultaneously"

### Fork (LF / SF split)
- Two diagonal arrows from the preceding box — one going up-right, one down-right
- Fork boxes stacked vertically, centered around the pipeline midpoint

### Vision / Feedback Loop
- Curved arc arrow drawn BELOW the pipeline
- Arcs from the final output box back to the relevant earlier stage
- Uses green (`#2F9E44`) to distinguish from primary flow

## Logo Integration

Use `scripts/fetch-logo.ts` to source logos before generating diagrams:

```bash
# Standard brand-color logo (works on light background)
npx tsx scripts/fetch-logo.ts --name "Anthropic" --output logos/anthropic.png

# Force specific fill color (only if brand colors don't render well)
npx tsx scripts/fetch-logo.ts --name "ToolName" --output logos/tool.png --color 000000
```

The `cold_orange_builder.py` `Builder` class handles logo embedding:
```python
b.logo("stage_logo", "logos/anthropic.png", x=box_x + 4, y=box_y + 14, size=42)
```

Missing logos are silently skipped — the box still renders without the logo.

## Hero Illustration Integration (storyboard mode)

### Image Requirements
- Rich, detailed scene compositions
- Match ExcaliDraw hand-drawn sketch aesthetic
- Transparent or white background
- Consistent style across all segments
- Large enough to be the hero visual (400-600px wide)

### Image Placement Rules
- Centred horizontally within the segment block
- Below subtitle, above supporting text
- Minimum 20px padding from surrounding text
- All hero illustrations consistently sized within a storyboard

## Shared Builder

All diagrams import from the shared Cold Orange Builder:
```python
from cold_orange_builder import Builder, ORANGE, AMBER, GREEN, BODY, DIM
```

Located at: `content-plugin/skills/2-copywriter/workflows/excalidraw-diagrams/data/cold_orange_builder.py`

Never copy-paste the Builder class into per-project files. Import it.
