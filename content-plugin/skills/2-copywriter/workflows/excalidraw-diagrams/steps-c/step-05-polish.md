---
name: 'step-05-polish'
description: 'Final review and polish — spacing, positioning, text tweaks, and metadata write'

diagramStandards: '../data/diagram-standards.md'
---

# Step 5: Review & Polish

## STEP GOAL:

To perform final adjustments on the composed storyboard — refining segment spacing, heading alignment, arrow flow, and visual balance — then write the final metadata plan and mark the workflow complete.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A POLISHER refining the final output
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual storyboard designer performing final quality review
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ This is the final step — attention to detail matters
- ✅ You bring layout refinement expertise, user brings final sign-off

### Step-Specific Rules:

- 🎯 Focus on refinement — not redesign
- 🚫 FORBIDDEN to add new segments or generate new illustrations
- 💬 Approach: Suggest specific improvements, let user decide
- 📋 This step produces the final deliverables

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write final `.excalidraw` file and metadata plan
- 📖 Mark workflow as complete
- 🚫 This is the FINAL step — no nextStepFile

## CONTEXT BOUNDARIES:

- Available: Composed `.excalidraw` file from step 4, all metadata from previous steps
- Focus: Refinement and final output only
- Limits: Do not add new segments or change the fundamental layout
- Dependencies: Step 4 must have produced a valid `.excalidraw` file

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load and Review Storyboard

Load the composed `.excalidraw` file from step 4 and `{diagramStandards}`.

Perform an automated quality check:

1. **Segment Spacing:** Are all segments evenly spaced with consistent gaps between blocks?
2. **Heading Alignment:** Are all segment headings aligned on the same vertical baseline?
3. **Vertical Consistency:** Within each segment, is the heading → subtitle → image → text stack consistently spaced?
4. **Arrow Flow:** Do all arrows connect cleanly between segments, horizontally aligned?
5. **Readability:** Would a viewer understand the left-to-right flow at a glance?
6. **Completeness:** Are all segments from the plan represented with all elements?

### 2. Present Quality Report

"**Final Quality Review:**

| Check | Status | Notes |
|-------|--------|-------|
| Segment Spacing | {✅/⚠️} | {details} |
| Heading Alignment | {✅/⚠️} | {details} |
| Vertical Consistency | {✅/⚠️} | {details} |
| Arrow Flow | {✅/⚠️} | {details} |
| Readability | {✅/⚠️} | {details} |
| Completeness | {✅/⚠️} | {details} |

**Suggested refinements:**
{List any specific improvements — e.g., 'Adjust segment 03 position 20px right for even spacing', 'Increase heading font size from 36 to 42'}

**Would you like me to apply these refinements, or are there other adjustments you'd like?**"

**Auto mode:** Auto-apply all suggested refinements and proceed directly to step 4 (write metadata) then step 5 (completion summary).

**Collab mode:** Wait for user feedback.

### 3. Apply Final Adjustments

If user requests adjustments or approves suggested refinements:

1. Modify element positions, sizes, or properties in the JSON
2. Re-validate JSON structure after changes
3. Re-present the summary if significant changes were made

### 4. Write Final Metadata Plan

Write the storyboard plan metadata file (`storyboard-plan-{name}.md`) with:

```markdown
---
sourceScript: {script file path}
created: {date}
status: complete
segmentCount: {count}
---

# Storyboard Plan: {name}

## Source
{Script name and path}

## Segments

| # | Heading | Subtitle | Illustration File | Supporting Text |
|---|---------|----------|-------------------|-----------------|
| 01 | {heading} | {subtitle} | {filename} | {text} |
| ... | ... | ... | ... | ... |

## Hero Illustrations Generated

| Segment | Filename | Prompt Used | Revision Notes |
|---------|----------|-------------|----------------|
| 01 | {filename} | {prompt} | {notes} |
| ... | ... | ... | ... |

## Canvas Layout
- Type: Wide horizontal segment flow
- Canvas: {width} x {height}
- Segments: {count} blocks flowing left-to-right
- Connectors: {count} arrows between segments

## Reproduction Notes
{Any notes that would help reproduce or modify this storyboard}
```

### 5. Final Completion Summary

"**Storyboard generation complete!**

**Deliverables:**
- 📊 **Storyboard:** {output_path}/storyboard-{name}.excalidraw
- 🖼️ **Hero Illustrations:** {output_path}/images/ ({count} files)
- 📋 **Metadata:** {output_path}/storyboard-plan-{name}.md

**Storyboard Stats:**
- Segments: {count}
- Elements: {count} total ({headings}, {subtitles}, {images}, {text}, {arrows})
- Hero illustrations: {count} generated via Nano Banana
- Source: {script name}

**Open the `.excalidraw` file in ExcaliDraw to view and further edit the storyboard.**

**Done!**"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Quality review performed against storyboard standards
- User reviewed and approved final storyboard
- Final adjustments applied if requested
- Valid `.excalidraw` file written to output path
- Metadata plan written with full reproduction notes
- Workflow marked as complete

### ❌ SYSTEM FAILURE:

- Skipping the quality review
- Adding new segments or generating new illustrations
- Writing invalid JSON
- Not writing the metadata plan
- Not presenting the final summary

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
