# Image Prompt Templates — Diagram Generation

Used in Step 3 when a section needs a generated image (no matching reference frame in the catalog).

## Image generation

Images are generated via the fal-ai MCP tool `mcp__fal-ai__generate_image`:

```
mcp__fal-ai__generate_image(
  prompt="PROMPT_HERE",
  image_size="landscape_4_3"
)
```

No API key needed — the fal-ai MCP is connected at the platform level.

**image_size for ScreenshotNodes:** `landscape_4_3` matches the default `420×280` node dimensions well.

---

## Style Direction for Diagram Images

These images appear in `ScreenshotNode` components with the warm cream+orange design aesthetic. They should feel like:
- Real interface screenshots (terminal/code/app UI) OR
- Conceptual illustrations that look like a UI mockup

**NOT:** Stock photos, abstract gradients, generic tech imagery.

### Base style context
```
Create a realistic-looking UI/interface screenshot or mockup.
Style: Clean, modern dark-mode interface. Think Claude Code, VS Code, or a terminal window.
Background: dark (#1c2128 or similar), text in cream/white.
Any code or command text should be readable and realistic.
This will be embedded as a pinned screenshot in an educational diagram.
Keep it simple and readable — it will display at ~420×280px.
```

---

## Prompt Templates by Content Type

### Terminal/command output
```
[BASE STYLE CONTEXT]

Show a terminal window with this content:
{TERMINAL_CONTENT}

Terminal header: dark title bar with three traffic-light dots (orange, peach, grey).
Font: monospace. Background: #1c2128.
Include a subtle orange cursor or highlight on the key line.
```

### Claude Code interface
```
[BASE STYLE CONTEXT]

Show a Claude Code (terminal) session:
- User prompt: "{USER_PROMPT}"
- Claude response beginning: "{RESPONSE_PREVIEW}"
Use the standard Claude Code interface look: dark background, orange/cream accents.
Show the conversation in progress — not an empty screen.
```

### File/folder structure
```
[BASE STYLE CONTEXT]

Show a VS Code-style file explorer tree:
{FILE_TREE}

Dark sidebar (#1c2128), file icons in muted colors, the key file highlighted with orange accent.
Show approximately 15-20 files/folders for realistic density.
```

### Configuration/settings
```
[BASE STYLE CONTEXT]

Show a settings/configuration panel:
Section title: "{SECTION_TITLE}"
Key settings shown:
{SETTINGS_LIST}

Clean card-style UI, dark mode, orange accent highlights on active/important settings.
```

### Conceptual diagram (no UI)
```
Create a simple flat-style illustration on a warm cream background (#fafaf8).
Style: clean, minimal, slightly editorial. Inter/sans-serif typography.
Show: {CONCEPT_DESCRIPTION}
Color palette: warm neutral paper + Claude orange (#d97757) accents only.
No gradients, no photography, no real people.
Think: a hand-drawn diagram someone would sketch to explain this concept.
Size: should read clearly at 420×280px.
```

### Workflow/pipeline
```
Create a simple pipeline diagram on a dark background (#1c2128).
Show a left-to-right flow: {STEP_1} → {STEP_2} → {STEP_3}
Style: blocky mono labels, orange (#d97757) arrows and accents, cream (#f0e6d3) node labels.
Keep it minimal — 3-5 steps max, readable at small size.
Font: monospace/JetBrains Mono style.
```

---

### Concept-on-backdrop (tool context)

Use this template when a section discusses an abstract concept (architecture layers, pipeline flow, data structure) and a specific tool provides the right visual aesthetic as grounding. Better than using a generic tool screenshot that doesn't show the actual concept.

```
[BASE STYLE CONTEXT]

Show a visual representation of this concept:
{CONCEPT_DESCRIPTION}

Render the concept as if it were annotated on top of a simplified {TOOL_NAME}-style interface.
The concept diagram (boxes, arrows, labels) should be the primary focus.
The {TOOL_NAME} aesthetic provides the backdrop: {TOOL_DESCRIPTION}
  - Example for VS Code: dark sidebar (#1c2128), file tree on left, main content area on right
  - Example for terminal: dark full-screen background, monospace prompt at top
  - Example for GitHub: light page with file tree and code view

Use simple geometric shapes for the concept nodes. Label them clearly in cream/white text.
Use Claude orange (#d97757) for arrows and accent highlights.
The result should feel like someone drew a diagram directly on a blurred/simplified version of the tool's UI.
```

**When to use:** The section discusses an abstract concept (3-layer architecture, pipeline stages, memory hierarchy) AND a specific tool aesthetic would help ground the viewer's mental model.

**Example:** Section discussing "how audit-data.json acts as the wiki layer" → Generate a concept image showing the 3-layer stack (raw/ → wiki/ → schema) drawn on a VS Code file-explorer backdrop.

---

## When to generate vs use reference frames

**Always prefer reference frames first** (they're real screenshots of actual tools).

Generate images only when:
1. The concept is abstract (no existing screenshot covers it)
2. The specific context within a known tool doesn't match any catalog frame
3. The section discusses a custom/internal system with no public UI
4. A composite/annotated view would communicate more than any single screenshot

---

## Saving generated images

Save to: `{project_path}/copywriter/diagrams/images/{descriptive-name}.png`

Reference from ScreenshotNode `src` prop using relative path:
`./images/{descriptive-name}.png`

(The HTML file and `images/` folder are siblings within `diagrams/`, so this relative path works.)
