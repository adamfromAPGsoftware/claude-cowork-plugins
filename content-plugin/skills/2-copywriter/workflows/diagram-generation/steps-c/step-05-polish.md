---
step: 5
name: polish
description: Quality review, validation, and handoff
---

# Step 5 — Polish

## 1. Read the generated HTML file

Read `{output_html}` and scan its contents.

---

## 2. Automated quality checks

Run through each check. Note any failures:

### Content checks
- [ ] Title block present at approximately (140, 140)
- [ ] At least 4 different node types used across the diagram
- [ ] All sections have a SectionSign and at least one ConceptNode
- [ ] Legend block is present near bottom-left
- [ ] ConnectorLayer is the first child of MapCanvas
- [ ] `worldW` and `worldH` are explicit numbers matching the plan

### Node count checks
- [ ] 4–8 SectionSigns
- [ ] Total nodes ≤ 30
- [ ] Total Connectors ≤ 20

### Screenshot checks
For each `ScreenshotNode` with a `src` prop:
- [ ] File exists at the resolved path (check using Bash: `ls {absolute_path}`)
- [ ] Path uses forward slashes only (no backslashes)
- [ ] For catalog references: uses `../../../../../context/brand-assets/...` pattern
- [ ] For generated images: uses `./images/` pattern

If a screenshot file doesn't exist, either:
1. Fix the path if it's a typo (check the catalog for the correct filename)
2. Remove the `src` prop to fall back to the placeholder

### Coordinate sanity checks (full bounding box)

Using the bounding box formulas from `data/component-reference.md` → "Bounding Box Estimation", verify every node:
- [ ] `left ≥ 20` (no node clips the left edge)
- [ ] `top ≥ 20` (no node clips the top edge)
- [ ] `right ≤ worldW − 40` (no node overflows right — catches wide CodeNodes and ScreenshotNodes)
- [ ] `bottom ≤ worldH − 200` (no node overflows bottom, except the legend block)
- [ ] Title block x ≈ 140, y ≈ 140 (confirm it'll be visible at default zoom)

Fix any violations by adjusting x or y inward before continuing.

---

## 3. Universal overlap detection (ALL node types)

**Parse the HTML** to extract every node instance: type and props (x, y, w, h, lines count, text length, etc.).

**Compute bounding boxes** using the canonical formulas in `data/component-reference.md` → "Bounding Box Estimation". Build a registry:

| Node ID | Type | left | top | right | bottom |
|---------|------|------|-----|-------|--------|
| ... | | | | | |

**Check all pairs** `(N × (N−1)) / 2` for rectangle intersection:
- Overlap when: `left_A < right_B AND right_A > left_B AND top_A < bottom_B AND bottom_A > top_B`

**Auto-fix each overlap:**
1. Compute `overlap_y = min(bottom_A, bottom_B) − max(top_A, top_B)`
2. Shift the lower node (higher y-value) **down** by `overlap_y + 40px`
3. If that would push `bottom > worldH − 200`, shift **right** by `overlap_x + 40px` instead
4. Update the node's `y={...}` (or `x={...}`) prop in the HTML

**Re-run** the check after each correction. Repeat up to 3 iterations until no overlaps remain.

Report: list every overlap found and the correction applied.

---

## 4. Connector endpoint validation (ALL connectors)

**Parse every `<Connector>` element** from the HTML. Extract all `from={{x:N,y:N}}` and `to={{x:N,y:N}}` coordinates.

**Reuse the bounding box registry** from section 3 (no need to recompute).

**For each endpoint** (both `from` and `to` of every connector):

1. Find the nearest node bounding box. For each box, compute the minimum distance from the endpoint to any edge:
   - If point is above the box: `top − point.y`
   - If below: `point.y − bottom`
   - If left of: `left − point.x`
   - If right of: `point.x − right`
   - If inside: distance = 0 (also invalid — endpoint hidden inside node)

2. Classify:
   - **Valid**: distance to nearest node edge ≤ 30px — leave unchanged
   - **Inside**: point falls within a node's bounding box → snap to nearest edge at the axis midpoint
   - **Orphan**: distance > 30px from any node → snap to the nearest node's closest edge

3. **Snap to edge** logic:
   - Determine which edge of the target node is closest to the endpoint (top/right/bottom/left)
   - Place the corrected point at that edge, at the y-midpoint (for left/right edges) or x-midpoint (for top/bottom edges)
   - For main-path connectors (orange, strokeWidth=3): prefer right edge of source node and left edge of target node
   - For branch connectors (grey, strokeWidth=2): prefer the edge that minimises total path length

4. **Rewrite** corrected `from`/`to` coordinates in the HTML for any endpoint that was Inside or Orphan.

Report: list every connector checked, its status, and what was corrected.

---

## 5. Collab mode — present for review

In collab mode, present:
```
Quality check complete.
Issues found: {list or "none"}
Corrections applied: {list or "none"}

Diagram is ready at: {output_html}

Open in browser to preview:
  - Double-click the .html file (Chrome or Safari recommended)
  - Pan: drag anywhere
  - Zoom: scroll wheel or pinch
  - Reset: click ⟲ (bottom-right)

Want to adjust anything before we wrap up? (or type 'done' to finish)
```

In auto mode, print the summary without waiting.

---

## 6. Final handoff

Print the completion message:

```
✓ Diagram generation complete

File: {output_html}
World: {WORLD_W} × {WORLD_H}px
Sections: {section_count}
Nodes: {node_count}
Connectors: {connector_count}

Open in browser: double-click the .html file
Pan: drag anywhere on the canvas  
Zoom: scroll wheel or pinch
Reset view: click ⟲ (bottom-right)

This diagram is ready to use as a visual backdrop for your video.
```

---

**Workflow complete.**
