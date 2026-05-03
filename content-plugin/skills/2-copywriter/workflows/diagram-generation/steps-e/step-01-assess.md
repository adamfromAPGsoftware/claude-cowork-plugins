---
step: 1
name: assess
description: Load existing diagram, understand current state, apply requested changes
---

# Step E1 — Assess & Edit

## 1. Load the diagram

Read the HTML file at the path provided by the user. If no path was given, search for `diagram-*.html` files in:
- `{content_output_folder}/{active_project}/copywriter/diagrams/`
- `{standalone_folder}/*/diagrams/`

If multiple found, ask which to edit.

Also read the corresponding plan file: `diagram-plan-{slug}.md` in the same directory (if it exists).

---

## 2. Parse current state

From the HTML file, extract:
- World dimensions (WORLD_W, WORLD_H)
- Section count (count `<SectionSign` occurrences)
- Node types used
- Any ScreenshotNode `src` values

---

## 3. Understand the edit request

Ask the user what they want to change if they haven't specified:

> "What would you like to change?
> - Add or remove a section
> - Change text in a node (tag, title, accent, body)
> - Add or swap a screenshot
> - Change connector routing
> - Add a new node type (CodeNode, QuoteNode, etc.)
> - Adjust layout/coordinates
> - Something else"

---

## 4. Apply changes

Make the requested changes directly to the HTML file. Be surgical — only modify what was requested.

For text changes: use Edit tool to find and replace the specific text.
For new nodes: add the JSX after an appropriate existing node, with planned coordinates that don't overlap with existing nodes.
For screenshot changes: update the `src` prop — verify the new file path exists.
For world dimension changes: update both `const WORLD_W = {n}` and `const WORLD_H = {n}` at the top of the script, and the `WORLD_H - 280` in the legend's top position.

---

## 5. Verify and confirm

Print a summary of changes made and the file path. Offer further edits.
