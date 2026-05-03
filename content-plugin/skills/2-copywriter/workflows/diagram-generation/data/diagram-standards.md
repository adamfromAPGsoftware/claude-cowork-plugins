# Diagram Standards — Treasure-Map Style

## Philosophy

These diagrams are visual concept maps for video content — not org charts, not flowcharts. Think **engineering notebook crossed with treasure map**: cream paper, dotted grid, paths that weave across the canvas, secondary material branching off like annotations. The goal is something interesting to look at and navigate while explaining concepts on camera.

---

## Canvas Dimensions

- **World size:** 3000×2000px (default), scale up for longer scripts
- **For 4-5 sections:** 3000×2000 is fine
- **For 6-8 sections:** 3600×2200
- **Title block:** Always top-left, world coords roughly (140, 140)
- **Content area:** Starts ~450px from top (below title), spans to ~1800px wide, ~1700px tall

---

## Layout Principles

### Do not do this:
- Linear left-to-right grid (that's what [CD] was — boring)
- All nodes at the same Y coordinate
- Perfectly symmetric layouts

### Do this:
- **Weave the path:** Main flow moves roughly left-to-right but steps up and down (Y varies ±100-200px between sections)
- **Branch secondary material:** Prompts, quotes, screenshots sit above or below the main nodes they relate to, connected with lighter connectors
- **Cluster related nodes:** A section's ConceptNode + its CodeNode/ScreenshotNode sit close together (within 200px), not spread out
- **Use the bottom half:** The lower canvas area (y > 1000) is valuable — use it for secondary nodes, loopbacks, and the legend

### World coordinate planning
Start with a rough grid, then offset each section:

| Section | Approx X | Approx Y (main) |
|---------|----------|-----------------|
| §1 | 140 | 440–600 |
| §2 | 680 | 480–620 |
| §3 | 1200 | 400–580 |
| §4 | 1700 | 500–640 |
| §5 | 2300 | 440–580 |
| §6 | 2600 | 800–1000 |
| §7 | 1900 | 1200–1400 |
| §8 | 1200 | 1500–1700 |

Secondary nodes (prompts, screenshots, quotes): offset ±200-300px from their parent section's X, place above or below (Y ±200-300px from parent)

---

## Section Anatomy

Each section of the map typically has:

1. **SectionSign** — §N block + chapter heading (e.g., "§1 Brief")
2. **StepMarker** — numbered waypoint on the main path (slightly to the right of the SectionSign)
3. **ConceptNode** — main explanation card (below SectionSign)
4. **0-1 secondary nodes:** CodeNode, ScreenshotNode, PromptNode, or QuoteNode (branching off)

Not every section needs every node type. Keep the density interesting but not cluttered.

---

## Node Usage Guide

| Node | When to use |
|------|-------------|
| `ConceptNode` | Explaining a key idea, process step, or principle |
| `CodeNode` | Showing a Claude prompt, file contents, terminal commands, or code snippets |
| `ScreenshotNode` | Visual evidence — a specific tool's interface, a result, a before/after |
| `PromptNode` | Short snippets of Claude prompts or key commands (smaller, more casual than CodeNode) |
| `SectionSign` | Chapter divider — marks the start of each major section |
| `DecisionNode` | Branching point — yes/no, if/else, "does it work?" |
| `StepMarker` | Waypoints along the main path — numbered, with a label chip |
| `QuoteNode` | Pull quotes from the script — key insights, memorable lines |

**Minimum node types per diagram:** Use at least 4 different node types. A diagram with only ConceptNodes is boring.

**Maximum per type:** Cap at 8 ConceptNodes, 4 CodeNodes, 4 ScreenshotNodes, 4 PromptNodes, 2 DecisionNodes, 4 QuoteNodes.

---

## Connector Routing

### Main path connectors (solid, orange)
- `kind="curve"` with moderate `curvature` (0.25–0.4) for the treasure-map feel
- `kind="straight"` for mandatory sequential steps
- `strokeWidth={3}` (default)
- Always label the main path connectors (`label="compile"`, `label="brief"`, `label="ship"`, etc.)

### Secondary connectors (lighter, grey)
- Connecting branch nodes (screenshots, prompts) back to their parent section
- `stroke="#7a726b"` (neutral-700), `strokeWidth={2}`
- `kind="curve"` with `curvature=0.3`
- No label (or very short label)

### Loopbacks and alternatives (dashed)
- `dashed={true}`
- For: iteration loops, "try again" paths, compounding memory connections
- `kind="curve"` with higher `curvature` (0.45–0.6) to arc over the main path

### Connector planning tips
- Anchor connectors to the visual edges of nodes, not their centers
- For a ConceptNode at (x=140, y=570, w=340): right edge is at x=480, center-right is y=570+half_height
- For a ScreenshotNode, account for the tape/pin height (~12px above top)
- Aim for 10-20 total connectors per diagram — fewer is better

---

## Screenshot Placement

`ScreenshotNode` settings for the best scrapbook feel:
- **Rotation:** Alternate between negative and positive: `rotate={-2}`, `rotate={2.5}`, `rotate={-1.5}`
- **Pin style:** Alternate between `pin="tape"` and `pin="pin"`
- **Caption:** Always add a caption — make it descriptive (what the screenshot shows, not just the tool name)
- **Size:** Default `w=420 h=280` is good. For wider content: `w=500 h=300`

---

## Screenshot Sourcing Strategy

Screenshots are sourced using a 4-tier priority system. Always attempt higher tiers first.

### Tier 1: Playwright Live Capture
For URLs mentioned directly in the video script (GitHub repos/gists, documentation pages, tool interfaces), capture a live screenshot using the Playwright MCP integration. This produces the most authentic, current screenshots.

**When to use:** A specific URL is mentioned in the script and the page is publicly accessible without authentication.
**How:** `mcp__playwright__browser_navigate` → wait 2–3s → `mcp__playwright__browser_take_screenshot`
**Output path:** `./images/{descriptive-name}.png` (sibling of the HTML file)
**Error handling:** If Playwright is unavailable or the page fails (timeout, auth wall, 404), fall to Tier 2 or 3.

### Tier 2: Catalog Reference Frame
Match the tool/platform mention against the reference frame catalog (`catalog.yaml`). Use the frame whose `description` and `tags[]` best match how the tool is being used in the section.

**When to use:** The script mentions a tool by name, a relevant reference frame exists, and Tier 1 didn't apply.
**Output path:** `{ref_path_prefix}{tool}/{frame-file}.png`

### Tier 3: FLUX-Generated Concept Image
Generate an image via `mcp__fal-ai__generate_image` (fal-ai MCP). Use the **concept-on-backdrop** approach: describe the concept being illustrated and specify a relevant tool's visual aesthetic as the backdrop. This is better than using a generic tool screenshot that doesn't match the content.

**When to use:** No URL to capture, no catalog match — but a visual would help explain the concept.
**How:** Pick the template from `data/image-prompt-templates.md` that best fits, using the concept-on-backdrop template for sections that discuss abstract architecture or layers.
**Output path:** `./images/{descriptive-name}.png`

### Tier 4: Placeholder
Omit the `src` prop on the ScreenshotNode, which renders the dashed-box placeholder with a label.

**When to use:** Both capture and generation failed, or the concept is too abstract for any visual. Always label with a descriptive string so it's clear what the image should show.

---

## Content Density Targets

| Metric | Target |
|--------|--------|
| Sections | 4–8 |
| Total nodes | 15–30 |
| Connectors | 10–20 |
| ScreenshotNodes | 2–5 |
| CodeNodes | 1–4 |
| PromptNodes | 1–4 |
| QuoteNodes | 0–3 |

---

## The Title Block

Always include a `TitleBlock` component at `x={140} y={140}`. Structure:
- Mono eyebrow: `The Map · 01` (small, orange, uppercase, JetBrains Mono)
- H1 display title: Video title, 68px, Inter 900, `-0.035em` tracking
- Orange accent word: The key phrase gets `color: "#d97757"` + an orange underline bar below it
- Subtitle: 20px, `#3d3833`, up to 2 lines, explains what the map covers

---

## Legend

Always include a legend block in the bottom-left area (around `x=160, y=1720`):
```
LEGEND
—— solid : the flow (happy path)
- - dashed : iteration · loopback · compounding memory
● numbered circle : a waypoint · something on disk
◆ diamond : a decision
```
Style: JetBrains Mono, 12px, `#3d3833`, cream background, 1px border, `borderRadius: 8`
