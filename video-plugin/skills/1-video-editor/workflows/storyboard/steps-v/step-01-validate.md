---
name: 'step-01-validate'
description: 'Run storyboard against storyboard-standards.md checklist'

dataFile: '../data/storyboard-standards.md'
---

# Step 1: Validate Storyboard

## STEP GOAL:

Run the storyboard document against the complete validation checklist from storyboard standards. Generate a pass/fail report with specific findings for each criterion.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 DO NOT BE LAZY - CHECK EVERY SECTION AND CATEGORY SYSTEMATICALLY
- CRITICAL: Read the complete step file before taking any action
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is a standalone validation — do not modify the storyboard
- Auto-proceed through all checks
- Present findings as a structured report

## EXECUTION PROTOCOLS:

- 🎯 Load storyboard and standards, run systematic 5-category validation checklist
- 📖 Load {dataFile} before running any checks
- 🚫 Do NOT modify the storyboard — validation is strictly read-only
- ✅ Auto-proceed through all checks — present findings as structured report

## CONTEXT BOUNDARIES:

- Available context: Target storyboard document, storyboard-standards.md
- Focus: Validation only — no modifications to the storyboard
- Limits: Read-only — never edit the storyboard during validation
- Dependencies: A storyboard document must exist to validate

## MANDATORY SEQUENCE

### 1. Load Storyboard

Ask user for the storyboard path if not provided:
- Search: `{project_folder}/{project-slug}/video-editor/storyboard/*-storyboard.md`

Read the complete storyboard document.

### 2. Load Standards

Load and read {dataFile} for the complete validation checklist.

### 3. Run Validation Checks

**Category 1: Document Structure**
- [ ] Frontmatter present with required fields (status, scope, stepsCompleted, video_id)
- [ ] Production Brief section present
- [ ] Speaker Position Map section present (or noted as unavailable)
- [ ] Visual Asset Source Map section present
- [ ] Text Placement Strategy section present
- [ ] Master Timeline section present
- [ ] Pacing Validation Report section present

**Category 2: Timeline Integrity**
- [ ] All segments have required fields (segment_id, start_time, end_time, visual_type, template)
- [ ] Zero gaps between segments
- [ ] No overlaps between segments
- [ ] Total duration matches production brief
- [ ] All segments reference valid Remotion templates
- [ ] All asset references match entries in Visual Asset Source Map

**Category 3: Visual Asset Source Map**
- [ ] Every entry has a unique ID
- [ ] Video-extract entries have source video + timestamps verified against visual analysis
- [ ] Motion-graphic entries have detailed prompt, duration, aspect_ratio, and reference_image where brands/logos are involved
- [ ] Branded-template entries reference valid template names (UpworkProfile, AgencyBrand)
- [ ] All statuses are valid enum values

**Category 4: Pacing Compliance**
- [ ] Hook sections: 15+ visual events/min
- [ ] Intro sections: 12-15 visual events/min
- [ ] Body sections: 7-10 visual events/min
- [ ] No section has zero visual events

**Category 5: Production Readiness**
- [ ] Status is APPROVED (required for Remotion Edit)
- [ ] All `stepsCompleted` steps are present
- [ ] B-roll asset status summary (how many extracted vs pending)
- [ ] Motion graphic asset status summary (how many generated vs pending)

**Category 6: Visual Asset Density**
- [ ] D1: Talking head intro has ≥ 1 B-roll or MG per 8s of timeline
- [ ] D2: Intro hook (first 15s) has ≥ 2 motion graphics
- [ ] D3: No talking head intro section > 15s without B-roll or MG
- [ ] D4: Total MG count for talking head intro ≥ (intro_duration_seconds / 8)
- [ ] D5: B-roll count ≥ 2 for talking head intros > 45s
- [ ] D6: Body sections have ≥ 1 visual break per 15s of speaker footage
- [ ] D7: Screen share/agenda sections have ≥ 1 visual change per 15s
- [ ] D8: Talking head intro ≤ 90s (WARN if exceeded)
- [ ] D9: Talking head intro ≤ 120s (FAIL if exceeded)

### 4. Generate Validation Report

"**Storyboard Validation Report — {video-id}**

**Overall Status: {PASS / FAIL}**

| Category | Checks | Passed | Failed | Score |
|----------|--------|--------|--------|-------|
| Document Structure | {count} | {pass} | {fail} | {pass/count} |
| Timeline Integrity | {count} | {pass} | {fail} | {pass/count} |
| Visual Asset Source Map | {count} | {pass} | {fail} | {pass/count} |
| Pacing Compliance | {count} | {pass} | {fail} | {pass/count} |
| Production Readiness | {count} | {pass} | {fail} | {pass/count} |
| Visual Asset Density | {count} | {pass} | {fail} | {pass/count} |

**Failures:**

{For each failed check:}
- **{category} — {check_name}:** {specific finding and recommendation}

**Summary:**
- Total checks: {total}
- Passed: {pass_count}
- Failed: {fail_count}
- Score: {pass_count}/{total} ({percentage}%)

{If all pass: 'Storyboard is valid and ready for Remotion Edit.'}
{If failures: 'Use [E]dit mode to address {fail_count} issues before proceeding to Remotion Edit.'}"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All validation categories checked
- Specific findings provided for each failure
- Actionable recommendations generated
- Clear pass/fail report presented

### FAILURE:

- Skipping validation categories
- Not providing specific findings for failures
- Modifying the storyboard (validation is read-only)
