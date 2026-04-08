---
name: 'step-07-review'
description: 'Present complete storyboard section-by-section for user review and approval'

outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
---

# Step 7: Review & Approval

## STEP GOAL:

Present the complete storyboard to the user for section-by-section review. This is the primary approval gate — the storyboard must receive APPROVED status before Remotion Edit can consume it.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- YOU ARE A FACILITATOR presenting work for approval
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is the PRIMARY user interaction step
- Present storyboard in digestible sections, not as a wall of text
- The user can approve, request section edits, adjust pacing, or modify B-roll
- Only change status to APPROVED when user explicitly approves

## EXECUTION PROTOCOLS:

- 🎯 Load complete storyboard, present executive summary, facilitate section-by-section review
- 💾 Set status: APPROVED only on explicit [C]onfirm + [Y]es — never auto-approve
- 🚫 Do NOT approve without explicit user confirmation

## CONTEXT BOUNDARIES:

- Available context: Complete storyboard document ({outputFile})
- Focus: Review, refinement, and final approval
- Limits: Only change status to APPROVED on explicit confirmation — any other outcome leaves status as DRAFT
- Dependencies: All prior steps (01–06) must be complete before review

## MANDATORY SEQUENCE

### 1. Load Complete Storyboard

Read the entire {outputFile} to have full context of:
- Production brief
- Speaker position map
- B-Roll source map
- Text placement strategy
- Master timeline
- Pacing validation report

### 2. Present Executive Summary

"**Storyboard Review — {video-id}**

**Overview:**
- Scope: {scope}
- Total Duration: {duration}
- Sections: {section_count}
- Timeline Segments: {segment_count}
- Video Extracts: {extract_count} ({extracted_count} extracted, {pending_count} pending)
- Motion Graphics: {mg_count} ({generated_count} generated, {pending_count} pending)
- Branded Templates: {bt_count} (always ready)

**Pacing Status:**
- Passing: {pass_count}/{total_count} sections
{If failures: '- Sections needing attention: {fail_sections}'}

**Ready for section-by-section review.**

**[C]onfirm** — Approve the storyboard as-is (sets status: APPROVED)
**[S]ection** — Review a specific section in detail
**[T]une** — Review and adjust pacing recommendations
**[B]-Roll** — Review and modify B-roll source map

#### Menu Handling Logic:
- IF C: Set status to APPROVED (see section 3 below)
- IF S: Present section detail (see section 4 below), then redisplay this menu
- IF T: Present pacing review (see section 5 below), then redisplay this menu
- IF B: Present B-roll review (see section 6 below), then redisplay this menu
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY finalize when user selects 'C' (Confirm)
- After other menu items execution, return to this menu"

### 3. Confirm Approval (IF C)

"**Approving Storyboard...**

This will:
- Set storyboard status to **APPROVED**
- Lock the storyboard as the source of truth for Remotion Edit
- Any video-extract with status `pending-extraction` will need [BE] B-Roll Extraction
- Any motion-graphic with status `pending-generation` will need [HM] Hera Motion Graphics
- Branded templates are always ready — no additional workflow needed

**Confirm approval? [Y]es / [N]o**"

IF Y:
- Update {outputFile} frontmatter: `status: APPROVED`
- Update `stepsCompleted` to append this step
- Update `lastStep: 'step-07-review'`

"**Storyboard APPROVED**

**Next Steps:**
{If pending extracts: '- Run **[BE] B-Roll Extraction** to extract {pending_extract_count} clips'}
{If pending MG: '- Run **[HM] Hera Motion Graphics** to generate {pending_mg_count} clips'}
- Run **[RE] Remotion Edit** to compile the storyboard into a Remotion project

Storyboard saved to: {outputFile}"

IF N: Return to review menu.

### 4. Section Detail Review (IF S)

"Which section would you like to review?"
List all sections by number.

For selected section, display:
- Timeline segments for that section (full row detail)
- Caption text and positions
- B-roll placements
- Pacing metrics
- Template assignments

Allow user to request changes. Apply changes to {outputFile}, then return to review menu.

### 5. Pacing Review (IF P)

Display pacing validation report. For each WARN/FAIL section, present the recommendations. Allow user to:
- Accept recommendations (apply changes to timeline)
- Override pacing targets
- Manually adjust specific segments

Apply changes to {outputFile}, re-run pacing count, then return to review menu.

### 6. B-Roll Review (IF B)

Display complete Visual Asset Source Map. Allow user to:
- Change asset type (video-extract ↔ motion-graphic)
- Edit Hera prompts for motion graphics
- Add/remove visual asset entries
- Change timestamp ranges for extractions

Apply changes to {outputFile}, then return to review menu.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Complete storyboard presented in digestible format
- User given opportunity to review each section
- Changes applied when requested
- Status set to APPROVED only on explicit user approval
- Next steps clearly communicated

### FAILURE:

- Auto-approving without user confirmation
- Not presenting review options
- Not allowing section-by-section review
- Not communicating pending video-extract/MG work
