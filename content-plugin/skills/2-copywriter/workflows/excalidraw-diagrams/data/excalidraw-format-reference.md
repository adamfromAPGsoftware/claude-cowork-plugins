# ExcaliDraw Format Reference

## File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Element Types

| Type | Usage | Key Properties |
|------|-------|----------------|
| `rectangle` | Containers, boxes, panels | x, y, width, height, backgroundColor |
| `ellipse` | Circles, ovals | x, y, width, height |
| `diamond` | Decision nodes | x, y, width, height |
| `text` | Labels, headers, body text | x, y, fontSize, fontFamily, text |
| `arrow` | Connections, flow | startBinding, endBinding, points |
| `line` | Dividers, decorative lines | points |
| `freedraw` | Hand-drawn marks | points, simulatePressure |
| `image` | Embedded images (PNG/SVG) | fileId, width, height |
| `frame` | Grouping frame | x, y, width, height, name |

## Common Element Properties

```json
{
  "id": "unique-id-string",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#ffffff",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a0",
  "roundness": { "type": 3 },
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Fill Styles

| Style | Value | Visual |
|-------|-------|--------|
| Hachure | `"hachure"` | Diagonal line fill (hand-drawn feel) |
| Cross-hatch | `"cross-hatch"` | Cross-hatched fill |
| Solid | `"solid"` | Flat colour fill |

## Roughness

| Value | Style | Usage |
|-------|-------|-------|
| 0 | Architect (clean) | Technical diagrams |
| 1 | Artist (slight wobble) | Standard hand-drawn |
| 2 | Cartoonist (very hand-drawn) | Casual/fun diagrams |

## Font Families

| ID | Name | Usage |
|----|------|-------|
| 1 | Virgil (hand-drawn) | Headers, emphasis |
| 2 | Helvetica | Clean body text |
| 3 | Cascadia (monospace) | Code, technical |
| 5 | Default | General purpose |

## Text Element

```json
{
  "type": "text",
  "text": "Hello World",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "Hello World",
  "autoResize": true,
  "lineHeight": 1.25
}
```

## Text Container Binding

Text inside shapes requires bidirectional binding:

**Shape side:**
```json
{
  "type": "rectangle",
  "id": "shape-1",
  "boundElements": [
    { "id": "text-1", "type": "text" }
  ]
}
```

**Text side:**
```json
{
  "type": "text",
  "id": "text-1",
  "containerId": "shape-1",
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

## Arrow Bindings

```json
{
  "type": "arrow",
  "points": [[0, 0], [200, 100]],
  "startBinding": {
    "elementId": "source-shape-id",
    "focus": 0,
    "gap": 5,
    "fixedPoint": null
  },
  "endBinding": {
    "elementId": "target-shape-id",
    "focus": 0,
    "gap": 5,
    "fixedPoint": null
  },
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

## Image Element

```json
{
  "type": "image",
  "id": "img-1",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 150,
  "fileId": "file-hash-id",
  "status": "saved",
  "scale": [1, 1]
}
```

**Files object (top-level):**
```json
{
  "files": {
    "file-hash-id": {
      "mimeType": "image/png",
      "id": "file-hash-id",
      "dataURL": "data:image/png;base64,...",
      "created": 1700000000000,
      "lastRetrieved": 1700000000000
    }
  }
}
```

## Fractional Indexing (Z-Order)

Elements are ordered using fractional indices with **lexicographic** ordering.

**CRITICAL**: Indices MUST be in ascending lexicographic order. Single-digit suffixes
like `"a1"`, `"a2"`, ..., `"a9"`, `"a10"` will BREAK because `"a9" > "a10"` lexicographically.

**Correct approach** — use 2-character base-62 suffixes for files with more than 62 elements:
- Charset: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`
- Sequence: `"a00"`, `"a01"`, ..., `"a09"`, `"a0A"`, `"a0B"`, ..., `"a0z"`, `"a10"`, `"a11"`, ...
- This supports up to 3,844 elements (62×62) in correct lexicographic order
- For ≤62 elements, single-char suffixes work: `"a0"`, `"a1"`, ..., `"a9"`, `"aA"`, ..., `"az"`

```python
FRAC_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def gen_fractional_index(n):
    """Generate the nth fractional index in lexicographic order."""
    d1 = n // 62
    d2 = n % 62
    return "a" + FRAC_CHARS[d1] + FRAC_CHARS[d2]
```

- Lower values render behind higher values
- Use sequential values when building programmatically

## ID Generation

- IDs should be unique strings
- Common pattern: 8-character alphanumeric (e.g., `"xK9mP2nQ"`)
- Must be unique across all elements in the file

## Canvas Sizing Guidelines

| Storyboard Type | Recommended Size |
|----------------|-----------------|
| 3-segment storyboard | ~2700 x 900 |
| 5-segment storyboard | ~4400 x 900 |
| 7-segment storyboard | ~6100 x 900 |
| Formula | (segments × ~850) + 200 padding × 900 height |

## Grouping

Elements can be grouped by sharing the same `groupIds` array value:
```json
{ "groupIds": ["group-1"] }
```

Multiple elements with `"groupIds": ["group-1"]` move and select together.
