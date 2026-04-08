---
name: 'step-01-preflight'
description: 'Load APPROVED storyboard, validate prerequisites, check B-roll and MG files exist'

nextStepFile: './step-01b-broll-verify.md'
dataFile: '../data/remotion-hard-rules.md'
---

# Step 1: Preflight Check

## STEP GOAL:

Load the approved storyboard, validate all prerequisites are met, check that B-roll clips and motion graphic files exist. Offer to chain to B-Roll Extraction or Hera Motion Graphics workflows if assets are missing.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- The storyboard MUST have `status: APPROVED` — do not proceed with DRAFT storyboards
- Load hard rules from {dataFile} and keep in context for all subsequent steps
- Validate every file referenced in the storyboard actually exists on disk

## MANDATORY SEQUENCE

### 1. Load Hard Rules

Load and read {dataFile} — these 12 rules are non-negotiable and enforced in QA (step 06).

### 2. Discover Storyboard

Ask for the storyboard path if not already in context:
- Search: `{project_folder}/{project-slug}/video-editor/storyboard/*-storyboard.md`

Read the complete storyboard document.

### 3. Validate Storyboard Status

**Check frontmatter `status`:**
- If `APPROVED`: Continue
- If `DRAFT`: "This storyboard has not been approved. Run **[SB] Storyboard** → Review & Approve first."
  Do NOT proceed.
- If missing: "No status field found. This storyboard may be incomplete."
  Do NOT proceed.

### 4. Validate B-Roll Assets

For each entry in the Visual Asset Source Map:

**Video extracts (`type: video-extract`):**
- Check if extracted file exists: `{project_folder}/{project-slug}/video-editor/broll/{broll-id}.mp4`
- Status: `extracted` (file exists) or `pending-extraction` (file missing)

**Motion graphics (`type: motion-graphic`):**
- Check if generated file exists: `{project_folder}/{project-slug}/video-editor/motion-graphics/{mg-id}.mp4`
- Status: `generated` (file exists) or `pending-generation` (file missing)

### 5. Validate Source Video Files

Check all source video files referenced in the master timeline exist:
- Main speaker video(s)
- Any additional source files

### 6. Present Preflight Report

"**Remotion Edit — Preflight Check**

**Storyboard:** {video-id} (APPROVED)
**Scope:** {scope}
**Total Segments:** {count}
**Total Duration:** {duration}

**Asset Status:**

| Asset Type | Total | Ready | Missing |
|-----------|-------|-------|---------|
| Source Video | {count} | {ready} | {missing} |
| Video Extracts | {count} | {ready} | {missing} |
| Motion Graphics | {count} | {ready} | {missing} |

{If all assets ready:}
All assets verified. Ready to scaffold Remotion project.

**[C] Continue** — Proceed to scaffold

{If B-roll missing:}
**{missing_broll_count} B-roll clip(s) need extraction.**
**[B] Chain to B-Roll Extraction** — Run [BE] workflow for missing clips, then return
**[C] Continue** — Proceed without (segments will use speaker footage as fallback)

{If MG missing:}
**{missing_mg_count} motion graphic(s) need generation.**
**[H] Chain to Hera Motion Graphics** — Run [HM] workflow for missing clips, then return
**[C] Continue** — Proceed without (segments will use speaker footage as fallback)

#### Menu Handling Logic:
- IF C: Load, read entire file, then execute {nextStepFile}
- IF B: Direct user to run [BE] B-Roll Extraction workflow, then restart this preflight
- IF H: Direct user to run [HM] Hera Motion Graphics workflow, then restart this preflight
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Storyboard loaded and APPROVED status verified
- All B-roll and MG asset files checked for existence
- Source video files validated
- Clear preflight report presented
- User confirmed readiness to proceed

### FAILURE:

- Proceeding with a DRAFT storyboard
- Not checking asset file existence
- Not offering chaining to BE/HM for missing assets
- Not loading hard rules for subsequent steps
