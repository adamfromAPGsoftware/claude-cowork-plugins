---
name: 'step-06-pacing-validation'
description: 'Count visual events per minute per section, flag failures, generate recommendations'

nextStepFile: './step-07-review.md'
outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
dataFile: '../data/pacing-rules.md'
---

# Step 6: Pacing Validation

## STEP GOAL:

Count visual events per minute for each section of the timeline, compare against pacing targets from the pacing rules, flag any failures, and generate actionable recommendations for improvement.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is a DETERMINISTIC step — count and compare, no creative decisions
- No user interaction — auto-proceed after validation
- A "visual event" is: segment change, caption appearance, B-roll cut, template transition

## EXECUTION PROTOCOLS:

- 🎯 Count visual events per section, compare against pacing targets from {dataFile}
- 💾 Append pacing report to {outputFile}, auto-proceed to review
- 📖 Load {dataFile} before counting to get correct targets per section type
- 🚫 No user interaction — deterministic counting and reporting only

## CONTEXT BOUNDARIES:

- Available context: Master timeline from step 5, pacing rules from data file
- Focus: Event counting and target comparison — report pass/fail with actionable recommendations
- Limits: No creative decisions — count and report only
- Dependencies: Master timeline must be complete before pacing can be counted

## MANDATORY SEQUENCE

### 1. Load Pacing Rules

Load and read {dataFile} for targets:
- Hook: 15+ visual events/min
- Intro: 12-15 visual events/min
- Body: 7-10 visual events/min

### 2. Count Visual Events Per Section

For each section in the master timeline:

**Visual events include:**
- Each new segment (visual change)
- Each caption appearance (new text on screen)
- Each B-roll cut (in or out)
- Each motion graphic appearance
- Each template transition

Count total visual events and divide by section duration in minutes.

### 3. Evaluate Against Targets

For each section:
- Calculate: `events_per_min = total_events / duration_minutes`
- Compare against target range for section type
- Status: `PASS` (within range), `WARN` (within 2 of range), `FAIL` (outside range)

### 4. Generate Recommendations

For each section that doesn't PASS:

**If too few events (pacing too slow):**
- Add more caption moments
- Insert B-roll cuts to break up long speaker segments
- Add motion graphic transitions
- Split long segments into shorter ones

**If too many events (pacing too fast):**
- Merge rapid-fire caption sequences
- Extend B-roll segments
- Remove redundant transitions

### 4a. Template Diversity Check (P19)

In addition to pacing counts, validate template diversity from the completed timeline:

1. Build `template_category` usage count for intro and full video.
2. **FAIL** for each template exceeding the intro cap (2) or full-video cap (3).
3. **FAIL** for each pair of adjacent MG segments using the same `template_category`.
4. **FAIL** for each `motion-graphic` segment without `hera: true` in the Visual Asset Source Map.
5. **FAIL** if total `hera: true` segments in intro > 3.

### 4b. Symbolic Alignment Audit

Spot-check 3–5 MG segments from across the video:

1. Read the narration text at each segment's timestamp from the clipped transcript.
2. Read the `symbolic_alignment:` value from the segment's `notes`.
3. **FAIL** if any `symbolic_alignment:` is missing, blank, or clearly mismatched (e.g., a counter showing "$600" while speaker says "we connected Gmail").

Add all P19 and symbolic alignment violations to the Recommendations section.

### 5. Build Pacing Report

```markdown
## Pacing Validation Report

| Section | Type | Duration | Visual Events | Events/Min | Target | Status |
|---------|------|----------|---------------|-----------|--------|--------|
| Hook | hook | {dur} | {count} | {rate} | 15+ | {PASS/WARN/FAIL} |
| Intro-1 | intro | {dur} | {count} | {rate} | 12-15 | {PASS/WARN/FAIL} |
| Body-1 | body | {dur} | {count} | {rate} | 7-10 | {PASS/WARN/FAIL} |
...

### Recommendations

{For each WARN/FAIL section, specific actionable recommendations}

### Overall Pacing Score

- Sections passing: {pass_count}/{total_count}
- Sections with warnings: {warn_count}
- Sections failing: {fail_count}
```

### 6. Append and Auto-Proceed

Append the pacing validation report to {outputFile}.

"**Pacing Validation Complete**

- Passing: {pass_count}/{total_count} sections
- Warnings: {warn_count}
- Failures: {fail_count}

{If all pass: 'All sections meet pacing targets.'}
{If failures: 'Recommendations generated for {fail_count} sections. These can be addressed in the review step.'}

Proceeding to review..."

Update {outputFile} frontmatter with `stepsCompleted` appended, then load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Visual events counted for every section
- Pacing compared against correct targets per section type
- Actionable recommendations generated for WARN/FAIL sections
- Template diversity validated: no showcase template > 2 in intro or > 3 in video, no adjacent identical templates, Hera count ≤ 3 in intro
- Symbolic alignment spot-checked and all sampled segments pass
- Pacing report appended to storyboard

### FAILURE:

- Not counting all visual event types
- Using wrong pacing targets for section types
- Not generating recommendations for failures
- Skipping the Template Diversity Check (P19)
- Skipping the Symbolic Alignment Audit
- Requiring user interaction (this is deterministic)
