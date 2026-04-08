---
name: 'step-04-compose'
description: 'Assemble the ExcaliDraw storyboard — embed hero images with headings, subtitles, text, and arrows on a wide horizontal canvas'

nextStepFile: './step-05-polish.md'
diagramStandards: '../data/diagram-standards.md'
excalidrawFormatReference: '../data/excalidraw-format-reference.md'
---

# Step 4: Storyboard Composition

## STEP GOAL:

To assemble the complete ExcaliDraw storyboard by composing approved hero illustrations onto a lightweight wide horizontal canvas with numbered headings, subtitles, supporting text, and arrow connectors between segments — producing a valid `.excalidraw` JSON file.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A BUILDER executing prescriptive composition
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual storyboard designer assembling the final canvas
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ This step is PRESCRIPTIVE — follow ExcaliDraw format spec precisely
- ✅ You bring ExcaliDraw format expertise, user brings final creative approval

### Step-Specific Rules:

- 🎯 Focus on assembling the ExcaliDraw JSON from the segment plan and approved hero illustrations
- 🚫 FORBIDDEN to generate new images — use only approved illustrations from step 3
- 💬 Approach: Build the JSON systematically per the segment anatomy pattern
- 📋 Follow the ExcaliDraw format reference exactly for valid output
- 🎯 Keep ExcaliDraw LIGHTWEIGHT — it's scaffolding for the hero images, not the main visual

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write the `.excalidraw` JSON file to the output path
- 📖 Load ExcaliDraw format reference for JSON structure compliance
- 🚫 FORBIDDEN to produce invalid JSON — validate before writing

## CONTEXT BOUNDARIES:

- Available: Segment plan (headings, subtitles, supporting text), approved hero illustrations (file paths), diagram standards, ExcaliDraw format reference
- Focus: Building valid ExcaliDraw JSON with the segment anatomy pattern
- Limits: Do not modify approved illustrations; do not add segments not in the plan
- Dependencies: Step 2 (segment plan) and step 3 (approved illustrations) must be complete

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load References

Load `{diagramStandards}` and `{excalidrawFormatReference}` for reference during composition.

Read the storyboard plan metadata file to retrieve:
- Segment list (headings, subtitles, supporting text)
- Hero illustration file paths per segment

### 2. Calculate Canvas Dimensions

Determine canvas size based on segment count:

- **Segment block width:** ~700-800px per segment (enough for heading + image + text)
- **Segment spacing:** ~100-150px between blocks (room for arrow)
- **Total canvas width:** (segment_count × block_width) + ((segment_count - 1) × spacing) + padding
- **Canvas height:** ~700-900px (heading + subtitle + hero image + supporting text stacked vertically)

### 3. Build Canvas Foundation

Create the base ExcaliDraw JSON structure:

1. Set `type: "excalidraw"` and `version: 2`
2. Set `appState` with white background
3. Initialise empty `elements` array and `files` object

### 4. Build Segment Blocks

For each segment in the storyboard plan, build a vertical block at the correct horizontal position:

**Segment Anatomy (top to bottom within each block):**

1. **Section Number + Heading** — Text element
   - Format: `"{NN}  {Heading}"` (e.g., "01  Your Claude Code, In Your Pocket")
   - Font: Virgil (fontFamily 1), fontSize 36-42, bold
   - Position: Top of the segment block, centred horizontally

2. **Subtitle** — Text element
   - Format: Italic/lighter descriptive line
   - Font: fontFamily 5, fontSize 16-20
   - Position: Below heading, centred

3. **Hero Illustration** — Image element
   - Read the segment's approved PNG file and encode as base64 dataURL
   - Add to the top-level `files` object with a unique hash ID
   - Create an `image` element with `fileId` matching the files entry
   - **CRITICAL — Preserve Aspect Ratio:** Read the actual pixel dimensions of the source PNG (e.g., via PIL/Pillow `Image.open(path).size`). Set the display width to ~500-600px, then calculate `display_height = display_width / (source_width / source_height)`. NEVER hardcode a square (e.g., 500x500) — always derive height from the source image's actual aspect ratio.
   - Position: Below subtitle, centred within block
   - Set `status: "saved"`

4. **Supporting Text** — Text element (if present)
   - Format: Bold takeaway line
   - Font: fontFamily 1, fontSize 20-24, bold
   - Position: Below hero illustration, centred

### 5. Add Arrow Connectors

Between each pair of adjacent segments:

1. Create an `arrow` element pointing from one segment block to the next
2. Position: Horizontally between blocks, roughly vertically centred
3. Set `endArrowhead: "arrow"`
4. Calculate `points` array for the arrow path (simple horizontal arrow)
5. Style: strokeWidth 2, strokeColor dark grey (#495057)

**No arrow after the final segment.**

### 6. Validate JSON Structure

Before writing, validate:

1. All element IDs are unique
2. All `fileId` references exist in the `files` object
3. Fractional indices are properly ordered
4. JSON is valid and parseable
5. No overlapping elements within a segment block

If validation fails, fix the issues before proceeding.

### 7. Present Composed Storyboard for Review

"**Storyboard composition complete.**

**Summary:**
- **Canvas:** {width} x {height}
- **Segments:** {count}
- **Elements:** {count} total
  - Headings: {count}
  - Subtitles: {count}
  - Hero illustrations: {count}
  - Supporting text: {count}
  - Arrow connectors: {count}

**The `.excalidraw` file has been assembled. Open it in ExcaliDraw to review the visual result.**

**File:** {output_path}/storyboard-{name}.excalidraw

**What would you like to adjust?**
- Segment spacing or positioning
- Text content or sizing
- Arrow routing
- Add/remove elements

**Or proceed to final polish if it looks good.**"

**Auto mode:** Auto-approve the composition and proceed directly to {nextStepFile} — no menu.

**Collab mode:** Wait for user feedback. If adjustments requested, apply them and re-present.

### 8. Present MENU OPTIONS

**Auto mode:** Auto-proceed to {nextStepFile} immediately — no menu.

**Collab mode:**

Display: "**Select:** [C] Continue to Polish"

#### Menu Handling Logic:

- IF C: Write final composed JSON to output path, update storyboard plan metadata, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user with adjustments, then [Redisplay Menu Options](#8-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the valid `.excalidraw` JSON file has been written to the output path will you then load and read fully `{nextStepFile}` to execute final polish.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Valid ExcaliDraw JSON structure produced
- All hero illustrations embedded with correct file references (base64 dataURL)
- Text elements properly positioned per segment anatomy
- Arrow connectors link segments in sequence
- Wide horizontal canvas with correct dimensions for segment count
- Lightweight ExcaliDraw — scaffolding only, no complex containers/grids
- JSON validated before writing
- User reviewed and approved the composition

### ❌ SYSTEM FAILURE:

- Invalid JSON structure (broken references, missing fileIds)
- Hero illustrations not embedded (missing base64 data)
- Complex container/grid layouts instead of simple segment flow
- Wrong canvas size for segment count
- Generating new images not from the approved set
- Not validating JSON before writing
- Proceeding without user review

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
