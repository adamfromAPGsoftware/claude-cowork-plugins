---
name: 'step-01-init'
description: 'Discover and load content concept brief, gather optional inputs, create output document'

nextStepFile: './step-02-direction.md'
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/scripts/script-{concept_slug}-{date}.md'
standaloneOutputFile: '{standalone_folder}/{date}-script-{concept_slug}/script.md'
templateFile: '../templates/script-template.md'
inputDocuments: []
requiredInputCount: 1
moduleInputFolder: '{content_output_folder}'
inputFilePatterns:
  - 'content-concept-*.md'
  - '**/content-concept-*.md'
---

# Step 1: Init & Load Concept

## STEP GOAL:

To discover and load a content concept brief from the Content Ideation workflow, gather optional inputs (target video length, specific talking points), and create the output script document from the template.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Copywriter preparing to write a video script
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in scriptwriting, YouTube content strategy, and hooks
- ✅ The user brings their brand knowledge, creative direction, and domain expertise

### Step-Specific Rules:

- 🎯 Focus only on discovering the concept brief and gathering inputs
- 🚫 FORBIDDEN to start writing any script content
- 💬 Help user select the right concept brief if multiple are found
- 📋 Ensure concept brief is loaded and understood before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Create output document from {templateFile}
- 📖 Load concept brief into context for subsequent steps
- 🚫 FORBIDDEN to proceed without a loaded concept brief

## CONTEXT BOUNDARIES:

- Available: CCS module config, concept briefs from Content Ideation
- Focus: Input discovery and setup only
- Limits: Do not generate any script content
- Dependencies: Content Ideation workflow must have produced at least one concept brief

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Discover Concept Briefs

**Search scope depends on the active mode (already resolved during agent startup):**

- **If in project mode:** Search ONLY within `{project_path}` (the active project folder) for files matching {inputFilePatterns}. Do NOT search other projects.
- **If in standalone mode:** Search `{moduleInputFolder}/standalone/*/` for files matching {inputFilePatterns}.

"**Let me find your content concept briefs...**"

**If exactly 1 brief found:**

Auto-select it. No need to prompt the user — display the brief summary in step 2 and let them confirm.

**If multiple briefs found:**

"**Found these concept briefs:**

[1] {filename} — {concept title from frontmatter} ({date})
[2] {filename} — {concept title from frontmatter} ({date})
...

**Which concept would you like to create a script for?** Enter the number, or provide a path to a different brief."

**If no briefs found:**

"**No concept briefs found** in the active project.

You can:
- **Provide a path** to a concept brief file
- **Run the Content Ideation workflow** first to generate a concept

**Path or action:**"

Wait for user selection (unless auto-selected).

### 2. Validate and Load Selected Brief

Load the selected concept brief and validate:

1. Check frontmatter for `stepsCompleted` — warn if incomplete
2. Read all sections: Concept Overview/Hook, ICP Alignment, Content Tree, Key Messages, Suggested Formats
3. Confirm brief is loaded

"**Loaded concept brief: {concept_title}**

**Quick summary:**
- **Hook:** {concept overview/hook summary}
- **ICP Alignment:** {brief alignment summary}
- **Platforms:** {platforms from content tree}
- **Key angle:** {suggested format/angle for YouTube}

Does this look right?"

Add to {inputDocuments}.

### 3. Gather Optional Inputs

"**A couple of optional inputs before we start:**

1. **Target video length?** (e.g., 8-10 minutes, 15 minutes, no preference)
2. **Any specific talking points** you want to make sure we include?

These are optional — just hit enter to skip."

Wait for user input. Document responses.

### 4. Determine Output Path

Use the mode already established during agent startup (from startup-protocol.md):

- **If in project mode:** Output path = `{outputFile}` (project folder)
- **If in standalone mode:** Output path = `{standaloneOutputFile}` (standalone folder)

Do not ask the user to re-select — the mode is already known. Confirm the resolved path silently and proceed.

### 5. Create Output Document

Create the output document from {templateFile} at the confirmed output path.

Fill in the frontmatter:
```yaml
stepsCompleted: ['step-01-init']
lastStep: 'step-01-init'
date: '{current date}'
user_name: '{user_name}'
concept_slug: '{concept_slug}'
concept_source: '{path to loaded concept brief}'
target_length: '{user provided or empty}'
```

Fill in the Script Overview section with the concept title, source brief path, target length, and date.

"**Script document created!** Ready to start developing the creative direction."

### 6. Auto-Proceed to Direction Pitch

"**Proceeding to direction pitch...**"

Load, read entire file, then execute {nextStepFile}.

## CRITICAL STEP COMPLETION NOTE

After creating the output document and loading the concept brief, auto-proceed to {nextStepFile}. No menu needed — init steps auto-proceed.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Concept brief discovered and loaded successfully
- All sections of the brief read and understood
- Optional inputs gathered (video length, talking points)
- Output path confirmed (project or standalone)
- Output document created from template with frontmatter filled
- Script Overview section populated
- Auto-proceeding to step 02

### ❌ SYSTEM FAILURE:

- Proceeding without a loaded concept brief
- Generating script content in this step
- Not validating the concept brief completeness
- Not creating the output document before proceeding
- Hardcoding output paths instead of using variables

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
