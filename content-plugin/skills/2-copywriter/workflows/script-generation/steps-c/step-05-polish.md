---
name: 'step-05-polish'
description: 'Compile teleprompter-ready section, polish the full document, and finalize'

outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/scripts/script-{concept_slug}-{date}.md'
scriptStandards: '../data/script-standards.md'
---

# Step 5: Final Polish

## STEP GOAL:

To compile the teleprompter-ready section from the scripted intro and body points, review the full document for flow and coherence, optimize formatting, and finalize the script document.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- 🚀 This step runs automatically — no user approval checkpoint needed. Compile, polish, save, and present the summary.

### Role Reinforcement:

- ✅ You are a Copywriter doing final polish on a production-ready script
- ✅ You bring expertise in document flow, readability, and teleprompter formatting
- ✅ The user has final approval authority

### Step-Specific Rules:

- 🎯 Focus on compiling the teleprompter section and polishing — do NOT generate new content
- 🚫 FORBIDDEN to add new ideas, change the creative direction, or rewrite approved script content
- 💬 Ensure the document is clean, well-formatted, and production-ready
- 📋 The teleprompter section must be immediately copy-pasteable

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Update {outputFile} with teleprompter section and polish
- 📖 Update frontmatter to mark workflow complete
- 🚫 FORBIDDEN to modify the substance of approved content

## CONTEXT BOUNDARIES:

- Available: Complete output document with all sections from Steps 1-4
- Focus: Polish, teleprompter compilation, and completeness
- Limits: Do not change creative decisions — only improve clarity and formatting
- Dependencies: All content from Steps 1-4

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load and Review Complete Document

Load {outputFile} and review the complete document built across all previous steps.

"**Compiling your final script document...**

Let me review everything and prepare the teleprompter-ready section."

### 2. Compile Teleprompter-Ready Section

Create the Teleprompter-Ready Section by extracting and reformatting:

**From Scripted Intro:** Copy the word-for-word intro as-is, formatted for clean reading.

**From Body Segments:** Convert dot points into clean, readable reminder bullets — large, clear, scannable.

**From CTA/Outro:** Include the closing if it has scripted elements.

**Teleprompter formatting rules (Borumi-compatible):**
- Start with note: "Copy and paste into Borumi for filming"
- No markdown formatting (no bold, italic, headers)
- ALL CAPS section markers on their own line (e.g., INTRO, SEGMENT 1, CTA) — each marker starts a new Borumi scene
- Within each section, write content as a single continuous line with NO line breaks (Borumi treats newlines as new scenes)
- Intro: combine all sentences into one unbroken line per section
- Body points: combine all dash-prefixed points into one line, separated by " — " (em dash with spaces)

Append the compiled teleprompter section to the **Teleprompter-Ready Section** of {outputFile}.

### 3. Document Optimization

Review the full document for:

1. **Completeness** — All 9 sections filled:
   - Script Overview
   - Direction & Angle
   - Scripted Intro
   - Body Segments
   - CTA / Outro
   - YouTube Metadata
   - Thumbnail Concepts
   - B-Roll Suggestions
   - Teleprompter-Ready Section

2. **Coherence** — Consistent narrative thread across all sections

3. **Clarity** — Each section is clear and actionable

4. **Duplication** — Remove any repeated information between sections

5. **Formatting** — Clean markdown, proper headers, consistent style

6. **Pattern Compliance** — Verify the scripted intro follows the Hook > Credibility > Value Promise > Barrier Removal > Bridge structure as defined in the "Data-Driven Quality Standards" section of {scriptStandards}. Confirm hook uses a proven formula, includes a specific number, and credibility stacking uses Adam's real credentials.

Load {scriptStandards} and verify against the validation criteria.

### 4. Finalize Document

Update the frontmatter:
```yaml
stepsCompleted: ['step-01-init', 'step-02-direction', 'step-03-draft', 'step-04-assets', 'step-05-polish']
lastStep: 'step-05-polish'
status: 'complete'
```

Save the final polished document to {outputFile}.

### 5. Present Final Summary

"**Your video script is complete!**

---

**Concept:** [Title]
**Target Length:** [Length]

**Sections:**
1. **Script Overview** — Concept and direction summary
2. **Direction & Angle** — Approved creative approach
3. **Scripted Intro** — Word-for-word teleprompter-ready intro
4. **Body Segments** — [N] segments with key talking points
5. **CTA / Outro** — Closing with call-to-action
6. **YouTube Metadata** — [N] title options, description, [N] tags
7. **Thumbnail Concepts** — [N] concepts for Creative Director
8. **B-Roll Suggestions** — Prioritized shot list (intro + body)
9. **Teleprompter Section** — Clean formatted for copy-paste

**Output saved to:** `{outputFile}`

---

**This script is ready for:**
- **You** — Teleprompter section ready to copy-paste for recording
- **Creative Director** — Thumbnail concepts ready for visual execution
- **Editor** — B-roll suggestions for post-production

---

**Recommended next steps:**
- **Quality Review** — Run the CCS quality review workflow for brand voice check
- **Creative Director** — Hand off thumbnail concepts for visual asset creation

**Great work on this one! Your script is production-ready.**"

### 6. Workflow Complete

This is the final step. No next step to load.

## CRITICAL STEP COMPLETION NOTE

This is the FINAL STEP. After saving the polished document and presenting the summary, the workflow is complete. No further steps to load.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 9 sections present and filled in the output document
- Teleprompter-Ready Section compiled from intro and body points
- Teleprompter section is clean, formatted, and copy-pasteable
- Document polished for coherence, clarity, and formatting
- No duplication between sections
- Frontmatter updated to mark workflow complete
- Final summary presented to user
- Output saved to correct path
- Next workflow recommendations provided

### ❌ SYSTEM FAILURE:

- Missing sections in the final document
- Teleprompter section not formatted for easy copy-paste
- Adding new content not from prior steps
- Changing creative decisions made in prior steps
- Not updating frontmatter to complete status
- Not saving the final document

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
