---
step: 2
name: concept
description: Parse script into map sections, match reference frames, plan world coordinates
---

# Step 2 — Concept

## 1. Read the Script

Read `{script_content}` in full. Your job: understand the narrative arc, identify the key concepts, demonstrations, tools, and conclusions — then plan a visual map that captures this journey.

---

## 2. Identify Map Sections

Parse the script into **4–8 map sections**. Each section = one major idea or phase of the video.

Rules:
- Sections should tell a complete story from start to finish
- Don't create sections for every paragraph — group related ideas
- Include an opening hook/premise section and a closing takeaway/CTA section
- Aim for 5-7 sections for most 8-15 minute videos

For each section, identify:
- **Section number** (1, 2, 3…)
- **Section label** (1-2 words: "Hook", "The Problem", "Setup", "The Demo", "Why It Works", "What's Next", "CTA")
- **Key concept** (one sentence — what this section explains)
- **Tools/platforms mentioned** (exact names — e.g., "Claude Code", "n8n", "GitHub", "terminal", "VS Code")
- **Quote candidates** — any memorable line from the script worth pulling out
- **Decision points** — any if/else or branching logic discussed
- **Code/prompts shown** — any specific prompts or code snippets in the script

---

## 3. Match Reference Frames + Plan Screenshots

Screenshots follow a 4-tier priority system (see `data/diagram-standards.md` → Screenshot Sourcing Strategy). Work through tiers in order.

### 3a. Extract URLs from script

Scan `{script_content}` for any URLs matching `https?://[^\s)>\]]+`. For each URL found:
- Categorize: GitHub repo/gist, documentation page, or tool/service page
- Record which section it appears in

### 3b. Build the screenshot match table

For each section that will have a ScreenshotNode, apply the 4-tier priority:

**Tier 1 — CAPTURE** (highest priority): If a URL from step 3a appears in this section AND the page is publicly accessible without auth, mark as CAPTURE.

**Tier 2 — MATCHED**: Search `{reference_catalog}` for entries where `display_name` or `aliases[]` contains the tool name (case-insensitive). Select the frame whose `description` and `tags[]` best match how the tool is used in this section.

**Tier 3 — GENERATE**: No URL to capture and no catalog match. Write a brief description of what the image should show. Use the concept-on-backdrop approach if the section discusses abstract architecture (layers, pipelines, data structures) — describe the concept AND specify the tool aesthetic as a backdrop.

**Tier 4 — PLACEHOLDER**: Mark only if both capture and generation are expected to fail (rare — prefer GENERATE).

| Section | URL (if any) | Tool mentioned | Catalog match | Frame file | Status | Image description |
|---------|-------------|---------------|---------------|------------|--------|-------------------|
| §1 Hook | https://gist.github.com/... | GitHub | — | — | CAPTURE | Sample tutorial gist page |
| §2 Setup | — | Claude Code | claude-code | claude-code/...png | MATCHED | — |
| §3 Demo | — | Custom system | — | — | GENERATE: 3-layer diagram on VS Code backdrop | — |

---

## 4. Plan Node Types Per Section

For each section, plan which node types to use:

| Section | SectionSign | StepMarker | ConceptNode | CodeNode | ScreenshotNode | PromptNode | DecisionNode | QuoteNode |
|---------|-------------|------------|-------------|----------|----------------|------------|--------------|-----------|
| §1 Hook | ✓ | ✓ | ✓ | — | ✓ (catalog match) | — | — | — |
| §2 ... | ✓ | ✓ | ✓ | ✓ | — | ✓ | — | ✓ |
...

**Node usage rules from diagram-standards.md:**
- Every section gets a SectionSign + StepMarker
- Every section gets at least one ConceptNode
- Use ≥4 different node types across the full diagram
- Max totals: 8 ConceptNodes, 4 CodeNodes, 4 ScreenshotNodes, 4 PromptNodes, 2 DecisionNodes, 4 QuoteNodes

---

## 5. Plan World Coordinates

Design the treasure-map layout. The main path flows roughly left-to-right but sections weave up and down. Secondary nodes (prompts, screenshots, quotes) branch off perpendicular to the main path.

**Starting point:** Title block at (140, 140). Content starts at ~y=440.

**Plan each section's main node coordinates:**

| Section | SectionSign (x,y) | ConceptNode (x,y,w) | Notes |
|---------|--------------------|----------------------|-------|
| §1 Hook | (140, 440) | (140, 570) w=340 | — |
| §2 ... | (680, 480) | (680, 600) w=340 | Slightly higher |
| ... | ... | ... | ... |

**Plan secondary node coordinates** (branch up/down from main):

| Node | Type | x | y | Props |
|------|------|---|---|-------|
| §1 Screenshot | ScreenshotNode | 100 | 900 | w=380, h=250, rotate=-2, pin=tape |
| §2 Code | CodeNode | 700 | 950 | w=420 |
| §2 Quote | QuoteNode | 160 | 1400 | w=380 |
...

**Plan StepMarker waypoints** (on the main path between sections):

| Marker | x (center) | y (center) | label |
|--------|------------|------------|-------|
| 1 | 570 | 660 | brief.md |
| 2 | 1100 | 640 | ... |
...

**Plan world dimensions:**
- `worldW` = max(x + max_node_width) + 200 (padding)
- `worldH` = max(y + max_node_height) + 300 (for legend at bottom)
- Round up to nearest 100px

---

## 5b. Bounding Box Overlap Pre-Check

After planning all coordinates, validate before writing the plan. Reference the canonical bounding box formulas in `data/component-reference.md` → "Bounding Box Estimation".

**Steps:**

1. Build a bounding box table for every planned node:

   | Node ID | Type | left | top | right | bottom |
   |---------|------|------|-----|-------|--------|
   | §1 SectionSign | SectionSign | x | y | x+300 | y+72 |
   | §1 ConceptNode | ConceptNode | x | y | x+w | y+180 |
   | ... | | | | | |

2. Check all `(N × (N−1)) / 2` pairs for rectangle intersection:
   - Overlap when: `left_A < right_B AND right_A > left_B AND top_A < bottom_B AND bottom_A > top_B`

3. For each overlap found, resolve by shifting the lower node (higher y value) **down** by `(overlap_y + 40px)`.
   - `overlap_y = bottom_A − top_B` (or vice versa — whichever is positive)
   - If shifting down would push `bottom > worldH − 200`, shift **right** instead by `overlap_x + 40px`

4. Re-run the check after each correction. Repeat up to 3 iterations until no overlaps remain.

5. Check canvas edge constraints for every node:
   - `left ≥ 20`
   - `top ≥ 20`
   - `right ≤ worldW − 40`
   - `bottom ≤ worldH − 200`
   Fix any violations by adjusting x or y inward.

6. Update the coordinate tables in section 5 with all corrected values before proceeding.

In collab mode: present the corrected bounding box table and any adjustments made. Wait for acknowledgment.

---

## 6. Plan Connectors

Design connector routing between sections and secondary nodes.

**Main path connectors (solid orange, strokeWidth=3):**
- From right edge of §N's ConceptNode → left edge (or StepMarker) of §N+1
- Use `kind="curve"` with `curvature=0.25–0.4`
- Add a short `label` on each (e.g., "build", "deploy", "review")

**Secondary connectors (grey, strokeWidth=2):**
- Connecting branch nodes back to their parent section
- `stroke="#7a726b"`, `kind="curve"`, `curvature=0.3`, no label
- **Placement rule for QuoteNodes branching right of a ConceptNode:** check that the QuoteNode's right edge does NOT enter the next section's x-range. If it does, place the QuoteNode BELOW the section's CodeNode instead (same column, safer y-position), and connect from the CodeNode bottom rather than the ConceptNode right edge.

**Loopback connectors (dashed):**
- For any iteration/feedback loops
- `dashed={true}`, `kind="curve"`, `curvature=0.5`

**Connector table:**
| From (x,y) | To (x,y) | kind | curvature | label | dashed | stroke | strokeWidth |
|------------|----------|------|-----------|-------|--------|--------|-------------|
| (480,650) | (740,640) | curve | 0.3 | build | false | #d97757 | 3 |
...

**After completing the connector table, validate all endpoints:**

For each connector's `from` and `to` point:
1. Find the closest node bounding box from the table built in section 5b
2. Compute the distance from the endpoint to the nearest edge of that box
3. **Valid**: distance ≤ 30px
4. **Inside**: point falls within the node body → snap to the nearest edge (top/right/bottom/left) at the midpoint along that axis
5. **Orphan**: distance > 30px from any node → snap to the nearest node's closest edge

Correct any invalid endpoints in the connector table before writing the plan file.

---

## 7. Write Diagram Plan

Write the complete diagram plan to `{plan_file}` in this format:

```markdown
---
diagram: {diagram_slug}
script: {script_path}
output: {output_html}
worldW: {worldW}
worldH: {worldH}
sections: {count}
totalNodes: {count}
totalConnectors: {count}
imagesToGenerate: {count of GENERATE items}
---

# Diagram Plan: {VIDEO_TITLE}

## Sections

### §1 — {LABEL}
- Concept: {one sentence}
- ConceptNode: x={x} y={y} w={w} tag="{tag}" title="{title}" accent="{accent}" body="{body}"
- SectionSign: x={x} y={y} number=1 label="{label}"
- StepMarker: x={x} y={y} number=1 label="{label}"
- ScreenshotNode: x={x} y={y} w={w} h={h} src="{ref_path_prefix}{frame_file}" caption="{caption}" rotate={n} pin="{type}"
...

### §2 — {LABEL}
...

## Connectors

| From | To | kind | curvature | label | dashed | stroke | strokeWidth |
...

## Images to Generate

| Section | Description | Prompt summary | Saved to |
...
```

---

## 8. Collab Mode — Present Plan

In collab mode, present the section summary table and connector count. Wait for approval or feedback before proceeding to Step 3.

In auto mode, proceed directly to Step 3.

---

**Load next:** `steps-c/step-03-images.md`
