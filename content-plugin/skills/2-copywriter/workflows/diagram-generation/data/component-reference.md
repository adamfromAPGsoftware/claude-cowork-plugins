# Component Reference — Diagram UI Kit

All components are React, rendered via Babel standalone. Each is absolutely positioned within the MapCanvas world (3000×2000px by default).

---

## MapCanvas

Pan+zoom viewport. Wraps everything. Children are world-coordinate divs.

```jsx
<MapCanvas worldW={3000} worldH={2000}>
  {/* ConnectorLayer must be first child */}
  {/* then all nodes */}
</MapCanvas>
```

**Props:**
- `worldW` (default 3000) — world width in px
- `worldH` (default 2000) — world height in px
- `initialX`, `initialY`, `initialZoom` — override initial view (rarely needed; auto-fit is smarter)

**Behavior:** Saves/restores pan+zoom state in localStorage under key `ag_map_view`. Top-left chrome shows `@{YOUR_HANDLE_PERSONAL} / map · drag to pan · scroll to zoom`. Bottom-right: zoom controls (+ / − / ⟲ reset).

---

## ConnectorLayer

SVG layer drawn beneath all nodes. Must be the first child of MapCanvas.

```jsx
<ConnectorLayer worldW={3000} worldH={2000}>
  <Connector from={{x:470, y:590}} to={{x:740, y:640}} kind="curve" label="compile" />
  <Connector from={{x:1660, y:660}} to={{x:1880, y:760}} kind="straight" dashed />
</ConnectorLayer>
```

---

## Connector

Individual arrow drawn inside ConnectorLayer.

```jsx
<Connector
  from={{x: 470, y: 590}}
  to={{x: 740, y: 640}}
  kind="curve"
  curvature={0.35}
  label="compile"
  dashed={false}
  stroke="#d97757"
  strokeWidth={3}
/>
```

**Props:**
- `from` / `to` — `{x, y}` world coordinates (arrow start and tip)
- `kind` — `"straight"` | `"elbow"` | `"curve"` (default `"curve"`)
- `curvature` — 0..1, how pronounced the curve is (default `0.35`)
- `label` — optional mono uppercase text pill at the midpoint
- `dashed` — boolean (default false)
- `stroke` — color (default `"#d97757"` orange)
- `strokeWidth` — (default `3`; use `2` for secondary/branch connectors)

**Anchor point guidance:**
- Right edge of a node at `x, y, w`: anchor at `{x: x+w, y: y+height/2}`
- Bottom edge: `{x: x+w/2, y: y+height}`
- Top edge: `{x: x+w/2, y: y}`
- For ConceptNode (w=340, typical h=160): right-center ≈ `{x: x+340, y: y+80}`

---

## ConceptNode

Titled card — the main explanation node.

```jsx
<ConceptNode
  x={140} y={570} w={340}
  tag="step · 01"
  title="Write the"
  accent="brief"
  body="Problem, audience, constraints, success criteria. Always markdown. Lives next to the code."
/>
```

**Props:**
- `x`, `y` — top-left world coordinates
- `w` (default 360) — width in px
- `tag` — mono eyebrow above title (optional; e.g., `"step · 01"`, `"key concept"`)
- `title` — bold display heading
- `accent` — orange accent word appended to title (optional)
- `body` — body text below heading (optional)

**Size estimation:** Height ≈ 120px (no body) to 180px (with body). Width is explicit via `w`.

**Style:** Cream background (#fafaf8), 1.5px ink border, 10px radius, 4px 4px offset shadow.

---

## CodeNode

Terminal panel for code, prompts, file contents, commands.

```jsx
<CodeNode
  x={2320} y={1280} w={400}
  title="review-command.sh"
  lines={[
    { parts: [{ t: "$ ", c: "#7a726b" }, { t: "claude review ", c: "#c9d1d9" }, { t: "--diff HEAD", c: "#f4a387" }] },
    "",
    { parts: [{ t: "→ checks against ", c: "#c9d1d9" }, { t: "CLAUDE.md", c: "#d97757" }] },
    { parts: [{ t: "→ flags ", c: "#c9d1d9" }, { t: "naming, tests, smells", c: "#f4a387" }] },
  ]}
/>
```

**Props:**
- `x`, `y` — top-left world coordinates
- `w` (default 460) — width in px
- `title` — file/command name shown in the terminal title bar (optional)
- `lines` — array of line definitions:
  - `""` — empty line (spacer)
  - `"plain string"` — plain text line (cream color)
  - `{ parts: [{t: "text", c: "hex"}] }` — multi-color line; `c` defaults to `#c9d1d9` (cream on dark)

**Color palette for syntax highlighting:**
- `#c9d1d9` — default (body on terminal)
- `#d97757` — orange accent (keywords, important values)
- `#f4a387` — soft orange (parameters, highlighted segments)
- `#7a726b` — muted (comments, prompts like `$`)

**Size estimation:** Height ≈ 80px header + (24px × number of lines) + 36px padding. Plan ~200-260px for 4-6 lines.

---

## ScreenshotNode

Pinned photo with tape/pin — for real screenshots or placeholder.

```jsx
<ScreenshotNode
  x={1300} y={100} w={420} h={280}
  src="../../../content-plugin/data/brand-assets/reference-frames/claude-code/claude-code-initial-state-with-prompt.png"
  caption="claude code — initial setup"
  label="CLAUDE CODE"
  rotate={-2.5}
  pin="pin"
/>
```

**Props:**
- `x`, `y` — top-left world coordinates (note: tape/pin extends ~12px above `y`)
- `w` (default 420) — width in px
- `h` (default 280) — image/placeholder height in px
- `src` — file path to image (relative from the HTML output file) OR empty for placeholder
- `label` — mono uppercase label shown in placeholder box (ignored when `src` provided)
- `caption` — italic caption below the image/placeholder
- `rotate` — degrees of tilt (-3 to +3, alternating)
- `pin` — `"tape"` (default, orange translucent strip) | `"pin"` (orange dot)

**When `src` is provided:** Renders `<img>` with `objectFit: cover`. Use the actual file path relative to where the HTML will be saved.

**When `src` is omitted:** Shows dashed placeholder box with label text and "drop image into assets/" hint.

**Size estimation:** Total height ≈ `h + 50px` (for tape/pin + caption padding).

**Relative path from output dir:** The HTML is saved to `{project}/copywriter/diagrams/diagram-{slug}.html`. To reference a catalog image at `content-plugin/data/brand-assets/reference-frames/claude-code/...`, the relative path is:
`../../../../content-plugin/data/brand-assets/reference-frames/claude-code/...`
(4 levels up: diagrams → copywriter → {project-slug} → content/projects → repo root is 5 levels from content, but content sits at repo root + content/projects/{slug}/copywriter/diagrams)

**Exact relative path calculation:**
- Output HTML: `content/projects/{slug}/copywriter/diagrams/diagram-{slug}.html`
- Reference frames: `content-plugin/data/brand-assets/reference-frames/{tool}/{file}.png`
- Relative: `../../../../../content-plugin/data/brand-assets/reference-frames/{tool}/{file}.png`
  (5 levels up: diagrams/ → copywriter/ → {slug}/ → projects/ → content/ → [repo root])

---

## PromptNode

Dark mono bubble for short Claude prompts or key commands.

```jsx
<PromptNode
  x={120} y={900} w={280}
  label="Prompt · 01"
  text="You are my chief of staff. Read these notes and return a one-page brief. Be concise. Ask before you invent."
/>
```

**Props:**
- `x`, `y` — top-left world coordinates
- `w` (default 260) — width in px
- `label` — small orange uppercase tag (e.g., `"Prompt · 01"`, `"SEND THIS TO CLAUDE"`)
- `text` — the prompt or command content

**Size estimation:** Height ≈ 60px + (~20px per line of text at w=260). Plan 100-150px for short prompts.

---

## SectionSign

Chapter divider — numbered block + heading. Place at the top of each section's area.

```jsx
<SectionSign x={140} y={440} number="1" label="Brief" />
```

**Props:**
- `x`, `y` — top-left world coordinates
- `number` — section number (string or number)
- `label` — section heading text (e.g., `"Brief"`, `"Context"`, `"The Hook"`)
- `w` (default 320) — total width

**Size estimation:** 72px tall (the numbered box), 34px font for label. Total height ~72px.

---

## DecisionNode

Diamond shape for branching decisions.

```jsx
<DecisionNode
  x={1880} y={760} w={220} h={160}
  question="Does it feel right?"
  yes="ship"
  no="iterate"
/>
```

**Props:**
- `x`, `y` — top-left world coordinates
- `w` (default 200) — width
- `h` (default 140) — height
- `question` — text inside the diamond
- `yes` — label for the "yes" branch (right side)
- `no` — label for the "no" branch (bottom)

---

## StepMarker

Numbered circular waypoint — marks a step along the main path.

```jsx
<StepMarker x={600} y={660} number={1} label="brief.md" />
```

**Props:**
- `x`, `y` — CENTER of the circle (not top-left)
- `number` — step number (renders as `01`, `02`, etc.)
- `label` — mono chip below the circle (optional)

**Size:** 64×64px circle. Total height with label chip ~90px. Account for centering: the circle is drawn at `x-32, y-32`.

---

## QuoteNode

Pull quote with orange left border.

```jsx
<QuoteNode
  x={160} y={1380} w={420}
  quote="The brief, the system, and the ADR are the product. The code is just the exhaust."
  attribution="context compounds"
/>
```

**Props:**
- `x`, `y` — top-left world coordinates
- `w` (default 360) — width
- `quote` — the quote text (rendered with orange curly quotes)
- `attribution` — mono uppercase attribution below (optional)

**Size estimation:** Height ≈ 30px per line of quote text + 40px attribution padding. Plan 100-180px.

---

## Footer (standalone)

Thin @{YOUR_HANDLE_PERSONAL} signature — used when embedding a map in a slide, not on the standalone map (which has it baked into the canvas chrome).

```jsx
<Footer />
```

Rarely needed in diagram context since MapCanvas already shows the handle.

---

## Bounding Box Estimation

**Canonical reference for overlap detection in Step 2 and Step 5.** Use these formulas to compute each node's occupied rectangle `(left, top, right, bottom)` in world coordinates.

| Node Type | left | top | right | bottom |
|-----------|------|-----|-------|--------|
| ConceptNode(x,y,w) | x | y | x + w | y + 180 (with body) / y + 120 (no body) |
| CodeNode(x,y,w,lines[]) | x | y | x + w | y + 80 + (len(lines) × 24) + 36 |
| ScreenshotNode(x,y,w,h) | x | y − 12 | x + w | y + h + 50 |
| PromptNode(x,y,w,text) | x | y | x + w | y + 60 + (ceil(len(text)/30) × 20) |
| QuoteNode(x,y,w,quote) | x | y | x + w | y + (ceil(len(quote)/40) × 30) + 40 |
| DecisionNode(x,y,w,h) | x | y | x + w | y + h + 22 |
| StepMarker(x,y) | x − 32 | y − 32 | x + 32 | y + 58 |
| SectionSign(x,y) | x | y | x + 300 | y + 72 |
| TitleBlock | 140 | 100 | 900 | 380 |

**Notes:**
- ScreenshotNode `top` is `y − 12` because the tape/pin extends 12px above the declared y coordinate.
- PromptNode and QuoteNode heights are estimated from text length; assume ~30 chars/line for PromptNode at w=260 and ~40 chars/line for QuoteNode at w=360. Scale proportionally for other widths.
- CodeNode: count each entry in `lines[]`, including empty-string spacer lines.

**Overlap test:** Two nodes A and B overlap when ALL of the following are true:
```
left_A  < right_B
right_A > left_B
top_A   < bottom_B
bottom_A > top_B
```

**Canvas edge constraints** (every node must satisfy):
- `left ≥ 20`
- `top ≥ 20`
- `right ≤ worldW − 40`
- `bottom ≤ worldH − 200` (reserve space for legend)
