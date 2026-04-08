---
name: 'step-01b-broll-verify'
description: 'Verify extracted B-roll clips match storyboard intent'

nextStepFile: './step-02-scaffold.md'
---

# Step 01b: B-Roll Content Verification

## STEP GOAL:

Verify that extracted B-roll clips actually show what the storyboard intended. Catch content mismatches before they reach the render pipeline.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction unless mismatches found
- Every `video-extract` segment in the storyboard must be verified
- Missing or zero-length B-roll files BLOCK the pipeline

## MANDATORY SEQUENCE

### 1. Load Storyboard Segments

From the approved storyboard, extract all segments with `visualType: video-extract`. For each, collect:
- `segment_id`
- `asset_ref` (Visual Asset Source Map ID)
- Intended content description from the storyboard
- Expected `source_file` path

### 2. Verify Each B-Roll Clip

For each `video-extract` segment:

1. **File existence check** — verify the B-roll file exists at `source_file` path
2. **File size check** — verify file is > 0 bytes
3. **Duration check** — verify clip has sufficient duration for the segment's `durationInFrames`
4. **Visual spot-check** (if Gemini API available):
   - Extract 1 frame from the middle of the B-roll clip using FFmpeg: `ffmpeg -ss {midpoint} -i {source_file} -frames:v 1 -f image2pipe -`
   - Send to Gemini with prompt: "Does this frame show: {storyboard description}? Answer YES/NO with brief explanation"
   - If NO → flag as content mismatch
5. **Manual fallback** (if no Gemini): Log each B-roll with its storyboard description for user review

### 3. Self-Heal on Failures

- **Missing file**: Check Visual Analysis JSON for the source timestamps, attempt re-extraction via FFmpeg
- **Content mismatch**: Check Visual Analysis JSON for alternative timestamps showing the intended content. If alternative found, re-extract with corrected timestamps
- **No alternative found**: Flag for user intervention — do not silently proceed

### 4. Generate Verification Report

Append results to qa-report.md under `## B-Roll Verification`:

```markdown
## B-Roll Verification

| Segment | Asset Ref | Expected Content | File Status | Content Match | Notes |
|---------|-----------|------------------|-------------|---------------|-------|
| seg-003 | broll-01  | Unified inbox    | OK (2.4MB)  | YES           | —     |
| seg-007 | broll-02  | Kanban dashboard | OK (1.8MB)  | NO — mismatch | Re-extracted from alt timestamp |
```

### 5. Gate Decision

- **All files present + no blocking mismatches** → auto-proceed to scaffold
- **Any file missing or zero-length AND self-heal failed** → HALT and report
- **Content mismatches** → WARN (log for review) but allow proceed — user may override

"**B-Roll Verification Complete**

- Total video-extract segments: {count}
- Files verified: {pass_count}/{count}
- Content matches: {match_count}/{count}
- Warnings: {warn_count}

Proceeding to scaffold..."

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Every video-extract segment's source file verified to exist and be > 0 bytes
- Content spot-checks performed (or logged for manual review)
- Self-heal attempted on any failures before blocking
- Report appended to qa-report.md

### FAILURE:

- Proceeding with missing or zero-length B-roll files
- Not checking file existence before scaffold
- Silently ignoring content mismatches without logging
- Not attempting self-heal on fixable issues
