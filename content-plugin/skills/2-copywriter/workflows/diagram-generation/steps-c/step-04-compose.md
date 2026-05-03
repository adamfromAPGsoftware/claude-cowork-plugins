---
step: 4
name: compose
description: Build the complete self-contained HTML diagram
---

# Step 4 — Compose

## 1. Load the template and plan

Read:
- `{project-root}/content-plugin/skills/2-copywriter/workflows/diagram-generation/data/html-template.md` — the full HTML template
- `{plan_file}` — the diagram plan with all node specs, connectors, and image paths

---

## 2. Prepare substitution values

From the plan:
- `{WORLD_W}` and `{WORLD_H}` — world dimensions
- `{VIDEO_TITLE}` — the video title for the `<title>` tag
- The title block: map label, H1 title with accent word, subtitle
- All section nodes with their exact props
- All connectors with their from/to coordinates, kind, label, etc.
- All ScreenshotNode `src` values (either `{ref_path_prefix}{frame_file}` for catalog matches, or `./images/{name}.png` for generated images)

---

## 3. Build the TitleBlock component

Based on the video title and script theme, write the `TitleBlock` function:

```jsx
function TitleBlock({ x, y }) {
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: 760,
      fontFamily: "Inter, sans-serif",
    }}>
      <div style={{
        fontFamily: "JetBrains Mono, monospace", fontSize: 14, color: "#d97757",
        fontWeight: 700, letterSpacing: "0.22em", textTransform: "uppercase", marginBottom: 14,
      }}>The Map · 01</div>
      <h1 style={{
        fontSize: 68, fontWeight: 900, lineHeight: 0.95,
        letterSpacing: "-0.035em", color: "#1a1614", margin: 0,
      }}>
        {/* Put the main title here, with one accent word in orange */}
        {/* Example: */}
        How I build <span style={{ position: "relative", display: "inline-block" }}>
          <span style={{ color: "#d97757" }}>{ACCENT_WORD}</span>
          <span style={{
            position: "absolute", left: 0, right: 0, bottom: -4,
            height: 8, background: "#d97757", borderRadius: 2,
          }}/>
        </span>
        <br/>with Claude.
      </h1>
      <div style={{
        marginTop: 20, fontSize: 20, color: "#3d3833", maxWidth: 640, lineHeight: 1.45,
      }}>
        {SUBTITLE_HERE}
      </div>
    </div>
  );
}
```

**Title guidance:**
- Keep the accent word to 1-2 words — the key verb or noun in the title
- Subtitle should be 1 sentence that explains what the map covers (e.g., "Six steps from brief to shipped feature — drag to explore.")
- Don't use the exact video title verbatim if it's too long; shorten it to a punchy display phrase

---

## 4. Build the App() function

Construct the complete `App()` function from the diagram plan.

**Structure:**
```jsx
function App() {
  return (
    <MapCanvas worldW={WORLD_W} worldH={WORLD_H}>

      {/* — CONNECTORS — must be first child of MapCanvas — */}
      <ConnectorLayer worldW={WORLD_W} worldH={WORLD_H}>

        {/* Main path connectors */}
        <Connector from={{x:...}} to={{x:...}} kind="curve" curvature={0.3} label="..." />
        
        {/* Secondary connectors */}
        <Connector from={{x:...}} to={{x:...}} kind="curve" stroke="#7a726b" strokeWidth={2} />
        
        {/* Loopbacks */}
        <Connector from={{x:...}} to={{x:...}} kind="curve" curvature={0.5} dashed />

      </ConnectorLayer>

      {/* — TITLE — */}
      <TitleBlock x={140} y={140} />

      {/* — §1 SECTION — */}
      <SectionSign x={140} y={440} number="1" label="Hook" />
      <StepMarker x={560} y={660} number={1} label="hook.md" />
      <ConceptNode x={140} y={570} w={340} tag="step · 01" title="..." accent="..." body="..." />
      <ScreenshotNode x={100} y={900} w={380} h={250}
        src="../../../../../content-plugin/data/brand-assets/reference-frames/claude-code/claude-code-initial-state-with-prompt.png"
        caption="claude code — getting started"
        rotate={-2} pin="tape"
      />

      {/* — §2 SECTION — */}
      ...

      {/* — LEGEND — always last, bottom-left — */}
      <div style={{
        position: "absolute", left: 160, top: {WORLD_H - 280}, width: 560,
        padding: "14px 18px",
        background: "#fafaf8", border: "1px solid #d8d2cc", borderRadius: 8,
        fontFamily: "JetBrains Mono, monospace", fontSize: 12, color: "#3d3833",
        letterSpacing: "0.06em", display: "flex", flexDirection: "column", gap: 6,
      }}>
        <div style={{ fontWeight: 700, color: "#d97757", letterSpacing: "0.18em", fontSize: 11 }}>LEGEND</div>
        <div>—— solid : the flow (happy path)</div>
        <div>- - dashed : iteration · loopback · compounding memory</div>
        <div>● numbered circle : a waypoint · something on disk</div>
        <div>◆ diamond : a decision</div>
      </div>

    </MapCanvas>
  );
}
```

**Important:**
- All nodes must have explicit `position: "absolute"` — this is baked into each component
- StepMarker x,y is the CENTER of the circle, not the top-left
- ScreenshotNode x,y is the top-left of the frame (the tape/pin extends 12px above)
- For any ScreenshotNode with `src`, verify the file path exists before writing it

---

## 5. Write the complete HTML file

Take the full template from `html-template.md` and:
1. Replace `{WORLD_W}` with the numeric value (e.g., `3000`)
2. Replace `{WORLD_H}` with the numeric value (e.g., `2000`)
3. Replace `{VIDEO_TITLE}` in the `<title>` tag
4. Replace the placeholder `TitleBlock` and `App()` functions with the ones you built in steps 3-4
5. **Do not modify anything else in the template** — all component code above the `/* === DIAGRAM CONTENT === */` line stays verbatim

Write the result to `{output_html}`.

---

## 6. Verify the output

Do a quick scan of the written HTML file:
- Confirm it starts with `<!DOCTYPE html>` and ends with `</html>`
- Confirm `<script type="text/babel">` is present
- Confirm `ReactDOM.createRoot` is present at the end
- Confirm all image `src` paths are present (search for `ScreenshotNode` with `src=`)
- Confirm `WORLD_W` and `WORLD_H` are numeric (not placeholder strings)

If any issue is found, fix it in-place.

---

## 7. Print completion

```
Diagram written to: {output_html}
World: {WORLD_W} × {WORLD_H}
Sections: {count}
Nodes: {total_node_count}
Connectors: {total_connector_count}
Screenshots: {matched_count} catalog + {generated_count} generated
```

---

**Load next:** `steps-c/step-05-polish.md`
