---
name: 'step-02-edit'
description: 'Apply edits to existing diagram — modify elements, regenerate images, update JSON'

diagramStandards: '../data/diagram-standards.md'
excalidrawFormatReference: '../data/excalidraw-format-reference.md'
imagePromptTemplates: '../data/image-prompt-templates.md'
---

# Step 2: Apply Edits

## STEP GOAL:

To apply the confirmed edits to the existing diagram — modifying elements, regenerating images if needed, and writing the updated `.excalidraw` JSON file.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER apply edits beyond what was confirmed in step 1
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE AN EDITOR applying confirmed changes
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual communication designer applying precise edits
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Apply only what was confirmed — no scope creep
- ✅ You bring ExcaliDraw format expertise, user brings final approval

### Step-Specific Rules:

- 🎯 Focus on applying the confirmed edit plan from step 1
- 🚫 FORBIDDEN to add edits not in the confirmed plan without user approval
- 💬 Approach: Apply changes systematically, present results for approval
- 📋 Validate JSON after every modification

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write the updated `.excalidraw` file
- 📖 Load format reference for JSON compliance
- 🚫 This is the FINAL edit step — no nextStepFile

## CONTEXT BOUNDARIES:

- Available: Existing diagram JSON, confirmed edit plan from step 1, diagram standards
- Focus: Applying confirmed edits precisely
- Limits: Do not exceed the confirmed edit scope
- Dependencies: Step 1 must have provided confirmed edit requirements

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load References

Load `{diagramStandards}`, `{excalidrawFormatReference}`, and `{imagePromptTemplates}` (if image edits needed).

### 2. Apply Edits Systematically

For each edit in the confirmed plan:

**Image edits:**
- Regenerate: Prepare new prompt from `{imagePromptTemplates}`, generate, replace in files object
- Swap: Replace fileId reference and base64 data
- Add: Generate new image, add to files and elements
- Remove: Delete from files and elements, update any bound elements

**Text edits:**
- Update `text` and `originalText` properties
- Adjust `fontSize` if needed
- Update bidirectional bindings if container changed

**Layout edits:**
- Modify `x`, `y`, `width`, `height` of affected elements
- Recalculate arrow points if connected elements moved
- Ensure minimum 20px padding maintained

**Arrow edits:**
- Add/remove arrow elements
- Update `startBinding`/`endBinding` references
- Recalculate `points` array

**Colour edits:**
- Update `strokeColor`, `backgroundColor` properties
- Maintain semantic colour coding from diagram standards

### 3. Validate Updated JSON

After all edits applied:

1. Validate all element IDs are unique
2. Validate all binding references are intact
3. Validate all fileId references exist in files object
4. Validate JSON is parseable
5. Fix any issues found

### 4. Present Updated Diagram

"**Edits applied:**

| Edit | Status |
|------|--------|
| {Edit 1} | ✅ Applied |
| {Edit 2} | ✅ Applied |
| ... | ... |

**Updated file:** {output_path}

**Open in ExcaliDraw to review. Any further adjustments needed?**"

Wait for user feedback. Apply additional adjustments if requested.

### 5. Final Completion

Once user approves:

"**Edit complete!**

**Updated:** {output_path}/diagram-{name}.excalidraw
**Changes applied:** {count} edits

**Done!** 🎯"

Update metadata plan if it exists.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All confirmed edits applied
- JSON validated after modifications
- Binding references intact
- User approved the updated diagram
- Updated file written

### ❌ SYSTEM FAILURE:

- Applying edits not in the confirmed plan
- Breaking JSON structure (invalid bindings, missing references)
- Not validating after edits
- Not presenting updated diagram for approval

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
