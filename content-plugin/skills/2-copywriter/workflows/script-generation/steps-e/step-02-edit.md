---
name: 'step-02-edit'
description: 'Apply requested edits to specific sections, re-polish, and save'

validationWorkflow: '../steps-v/step-01-validate.md'
scriptStandards: '../data/script-standards.md'
---

# Step 2: Apply Edits

## STEP GOAL:

To apply the user's requested edits to the specified sections, re-polish affected areas, regenerate the teleprompter section if the intro or body changed, and save the updated document.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Copywriter making targeted edits to an existing script
- ✅ Preserve the user's voice and creative direction
- ✅ Only change what was requested — don't rewrite everything

### Step-Specific Rules:

- 🎯 Focus only on the sections the user identified for editing
- 🚫 FORBIDDEN to modify sections the user didn't request changes to
- 💬 Present edits for approval before saving
- 📋 If intro or body changed, regenerate the teleprompter section

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Save edited document
- 📖 Preserve frontmatter, update lastStep

## CONTEXT BOUNDARIES:

- Available: Existing script document, user's edit requests from step 01
- Focus: Targeted edits only
- Limits: Do not modify sections not flagged for editing
- Dependencies: Assessment from step 01

## MANDATORY SEQUENCE

### 1. Apply Requested Edits

For each edit the user requested:

1. Load the current section content
2. Apply the requested change
3. Present the edited section for review

"**Here's the updated [section name]:**

---
[Updated content]
---

**Does this look right, or want me to adjust further?**"

Iterate until user approves each edit.

### 2. Regenerate Teleprompter Section (If Needed)

**If the Scripted Intro or Body Segments were edited:**

Recompile the Teleprompter-Ready Section using the same Borumi-compatible formatting rules from the create workflow:
- No markdown formatting
- ALL CAPS section markers on their own line — each marker starts a new Borumi scene
- Within each section, single continuous line with NO line breaks (Borumi treats newlines as new scenes)
- Intro: combine all sentences into one unbroken line per section
- Body points: combine into one line, separated by " — " (em dash with spaces)

"**Teleprompter section updated to reflect your edits.**"

### 3. Polish Affected Sections

Load {scriptStandards} and verify the edited sections still meet standards.

Check for:
- Coherence with unchanged sections
- No duplication introduced
- Consistent tone and formatting
- If Scripted Intro was edited, verify it still follows the 5-part structure: Hook > Credibility > Value Promise > Barrier Removal > Bridge
- If hook was changed, verify the new hook uses a proven formula from the pattern library and includes a specific number

### 4. Save and Finalize

Update the document frontmatter:
```yaml
lastStep: 'edit-step-02-edit'
lastEdited: '{current date}'
```

Save the updated document.

"**Edits applied and saved!**

**Changes made:**
- [Summary of edit 1]
- [Summary of edit 2]
[- Teleprompter section regenerated (if applicable)]

**Document saved to:** [path]"

### 5. Offer Validation

"**Would you like to run validation on the updated script?**

**[V]** Run validation
**[D]** Done — exit workflow

Select: [V] Validate / [D] Done"

#### Menu Handling Logic:

- IF V: Load, read entire file, then execute {validationWorkflow}
- IF D: "**Edit complete. Your script has been updated!**"
- IF Any other: help user, then redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:
- Only requested sections modified
- Edits approved by user before saving
- Teleprompter section regenerated if intro/body changed
- Document saved with updated frontmatter
- Validation offered

### ❌ SYSTEM FAILURE:
- Modifying sections the user didn't request
- Not regenerating teleprompter section when intro/body changed
- Saving without user approval of edits

**Master Rule:** Skipping steps is FORBIDDEN.
