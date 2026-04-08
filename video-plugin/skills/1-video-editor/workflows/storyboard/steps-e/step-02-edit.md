---
name: 'step-02-edit'
description: 'Apply edits to storyboard and re-validate pacing on affected sections'

outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
dataFile: '../data/pacing-rules.md'
---

# Step 2: Apply Edits

## STEP GOAL:

Apply the user's requested edits to the storyboard document, then re-validate pacing on any affected sections to ensure compliance with pacing rules.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Apply ONLY the edits the user requested in the assessment step
- After edits, re-validate pacing on affected sections only
- If storyboard was APPROVED, warn that edits will reset status to DRAFT
- Present results for user approval

## EXECUTION PROTOCOLS:

- 🎯 Apply user-requested edits, re-validate pacing on affected sections only
- 💾 Update {outputFile} with edits — set status APPROVED only on explicit [C]onfirm
- 📖 Load {dataFile} for pacing targets before re-validation
- 🚫 Do NOT apply edits not explicitly requested by user

## CONTEXT BOUNDARIES:

- Available context: Storyboard document, user's edit goals captured in step-01-assess
- Focus: Apply ONLY requested edits + pacing re-validation on affected sections
- Limits: Do NOT make unrequested changes to other sections
- Dependencies: Edit goals must be captured from step-01-assess before proceeding

## MANDATORY SEQUENCE

### 1. Status Warning (if APPROVED)

If the storyboard has `status: APPROVED`:
"**WARNING:** This storyboard is currently APPROVED. Applying edits will reset status to DRAFT and require re-approval before Remotion Edit can consume it.

Proceed with edits? [Y]es / [N]o"

If Y: Set `status: DRAFT` in frontmatter.
If N: Return to agent menu.

### 2. Apply Edits

Based on the user's edit goals from the assessment step, apply changes to {outputFile}:

**Section edits:** Modify specific sections (production brief, B-roll map, text placement)
**Timeline edits:** Add, remove, or modify segments in the master timeline
**B-roll changes:** Update B-roll source map entries
**Pacing adjustments:** Modify segments to hit pacing targets

For each edit applied, report:
"Applied: {description of change}"

### 3. Re-Validate Pacing

Load pacing rules from {dataFile}.

For each section affected by edits:
1. Recount visual events
2. Recalculate events/min
3. Compare against target
4. Report new status

"**Pacing Re-Validation (Affected Sections):**

| Section | Before | After | Target | Status |
|---------|--------|-------|--------|--------|
| {section} | {old_rate}/min | {new_rate}/min | {target} | {PASS/WARN/FAIL} |
..."

### 4. Validate Timeline Continuity

After edits, verify:
1. Zero gaps between segments
2. No overlaps
3. Total duration is correct

Report any issues found.

### 5. Present Results

"**Edits Applied**

Changes made: {edit_count}
Pacing status: {pass_count}/{affected_count} sections passing
Timeline continuity: {verified/issues}

**[C]onfirm** — Set status to APPROVED
**[E]dit** — Make additional edits
**[X] Exit** — Save as DRAFT and exit

#### Menu Handling Logic:
- IF C: Update frontmatter `status: APPROVED`, save, and complete
- IF E: Gather new edit goals, loop back to section 2
- IF X: Save as DRAFT and complete
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- Only set APPROVED on explicit user approval"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Requested edits applied to storyboard
- Pacing re-validated on affected sections
- Timeline continuity verified after edits
- Status updated appropriately (DRAFT or APPROVED)

### FAILURE:

- Applying edits not requested by user
- Not re-validating pacing after changes
- Not checking timeline continuity
- Auto-approving without user confirmation
