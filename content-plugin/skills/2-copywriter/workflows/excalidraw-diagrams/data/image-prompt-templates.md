# Image Prompt Templates

## Model Configuration

**Tool:** `mcp__fal-ai__generate_image` (fal-ai MCP — platform-level)
**Model:** `fal-ai/nano-banana-2` (REQUIRED — always specify explicitly, never use any other model)
**Auth:** No API key needed — connected at the Claude Code platform level

**Call Pattern:**

```
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="PROMPT_HERE",
  image_size="landscape_4_3"
)
```

The tool returns the generated image directly. Save to disk at the appropriate path.

## Hero Illustration Generation

### Base Style Prompt

Use this as the foundation for ALL hero illustration requests. Append the segment-specific details after this base:

```
Generate a detailed hand-drawn sketch illustration for a video storyboard segment.
Style: Black ink sketch on white/transparent background, ExcaliDraw hand-drawn aesthetic.
Line weight: Medium, slightly uneven (hand-drawn feel).
Complexity: Rich and detailed — this is a HERO illustration, not a small icon.
The illustration should be a full scene composition with multiple visual elements that tell a story.
Include hand-drawn labels, annotations, and visual metaphors within the illustration.
No colour fills — line art only with optional light shading and cross-hatching for depth.
Think: whiteboard sketch that a designer drew to explain a concept, with detail and visual storytelling.
```

### Reference Style Description

The target style is inspired by high-quality tech explainer storyboards:

- **Rich compositions:** Each illustration contains multiple sub-elements (devices, icons, text labels, arrows, containers) arranged as a coherent visual scene
- **Hand-drawn labels:** Text within illustrations uses a hand-drawn style (e.g., "CLAUDE CODE" in rough block letters, "~200 lines" as a casual annotation)
- **Visual metaphors:** Abstract concepts shown through concrete imagery (bridges connecting systems, walls crumbling, scissors cutting between old/new approaches)
- **Sub-panels within illustrations:** Some hero images contain their own internal structure — split panels (old way vs new way), grids of components, timelines with bullet points
- **Sketch-style icons embedded in scenes:** Small recognisable icons (padlocks, gears, stars, warning triangles, checkmarks) support the main visual narrative
- **Scale and emphasis:** Important elements are drawn larger; supporting details are smaller but still detailed enough to read

### Segment Hero Illustration Prompt

For each segment's hero illustration, combine the base style with segment-specific direction:

```
[BASE STYLE PROMPT]

Segment concept: [SEGMENT HEADING]
Context: [SUBTITLE / NARRATIVE CONTEXT]

The illustration should depict:
[DETAILED SCENE DESCRIPTION — what specific visual elements to include, how they relate to each other, what story the image tells]

Key visual elements to include:
- [ELEMENT 1 — e.g., "A hand-drawn phone screen showing chat bubbles"]
- [ELEMENT 2 — e.g., "A bridge connecting the phone to a computer"]
- [ELEMENT 3 — e.g., "Small icons representing skills, memory, web search"]

Composition: [LAYOUT DIRECTION — e.g., "Left-to-right flow showing phone connecting to ecosystem" or "Split panel: top shows old way, bottom shows new way with scissors cutting between"]

Labels to include in the sketch: [LIST — e.g., "Your Phone", "The Bridge", "~200 lines"]
```

### Split-Panel Illustration Prompt

For segments that compare two approaches (old vs new, problem vs solution):

```
[BASE STYLE PROMPT]

Create a split-panel illustration:

**Top/Left Panel — [PANEL A TITLE]:**
[Description of what this panel shows]

**Bottom/Right Panel — [PANEL B TITLE]:**
[Description of what this panel shows]

Visual separator: [e.g., "scissors cutting a dashed line", "bold horizontal divider", "arrow showing transformation"]

Include hand-drawn labels for each panel title in rough block letters.
```

### Grid/Component Illustration Prompt

For segments that list multiple components, features, or options:

```
[BASE STYLE PROMPT]

Create a grid-style illustration showing [COUNT] components:

| Component | Icon/Visual | Label |
|-----------|-------------|-------|
| [NAME] | [DESCRIPTION] | [LABEL TEXT] |
| ... | ... | ... |

Arrange in a [2x3 / 3x2 / 2x2] grid layout.
Each cell should have: a sketch-style icon at top, the component name below, and a brief description line.
Include a title header above the grid: "[GRID TITLE]"
```

## Prompt Customisation Variables

| Variable | Description | Example |
|----------|-------------|---------|
| [SEGMENT HEADING] | The segment's title | "Your Claude Code, In Your Pocket" |
| [SUBTITLE / NARRATIVE CONTEXT] | What this segment is about | "A thin bridge between your phone and your entire Claude Code ecosystem" |
| [DETAILED SCENE DESCRIPTION] | Full visual direction | "Show a phone on the left with chat bubbles, a small bridge in the middle with a walking character, and a large screen showing Claude Code interface on the right" |
| [ELEMENT N] | Specific visual element to include | "A hand-drawn padlock with a red X through it" |
| [COMPOSITION] | Layout/flow direction | "Left-to-right: problem → solution → outcome" |
| [LABELS] | Text annotations within the sketch | "Your Phone", "The Bridge", "Everything you already use" |

## Batch Generation Guidelines

When generating hero illustrations for a storyboard:

1. Use the **same base style prompt** for all illustrations in the storyboard
2. Maintain consistent line weight and level of detail across all segments
3. Each illustration should be rich enough to be the dominant visual for its segment
4. Review the batch as a whole for visual consistency before composing the storyboard
5. Flag any illustrations that look stylistically different for regeneration
6. All illustrations should work at 400-600px width in the final ExcaliDraw canvas

## Revision Prompts

When revising a specific hero illustration:

```
Regenerate the hero illustration for segment [NN]: "[HEADING]".
Keep the same hand-drawn sketch style as the other illustrations in this storyboard.
Change: [SPECIFIC CHANGE — e.g., "add more detail to the bridge metaphor", "simplify the right panel", "make the labels more readable"]
Maintain: Black ink line art, hand-drawn aesthetic, same level of detail as the rest of the set.
The illustration should remain a rich, detailed scene composition — not simplified to an icon.
```
