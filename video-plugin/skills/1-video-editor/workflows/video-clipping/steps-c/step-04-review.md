---
name: 'step-04-review'
description: 'Legacy review checkpoint — skipped in autonomous mode'

nextStepFile: './step-05-generate.md'
outputFile: '{project_folder}/{project-slug}/video-editor/clips/{video-id}-clip-plan.md'
---

# Step 4: Review Checkpoint (Autonomous Passthrough)

## STEP GOAL:

Legacy review checkpoint — skipped in autonomous mode. Step 2 now auto-decides all cuts using confidence-gated scoring and proceeds directly to step 5.

If this step is reached (e.g., via manual invocation), it reads the auto-decisions from step 2 and passes them through to the clip plan without any user interaction.

## MANDATORY SEQUENCE

### 1. Read Auto-Decided Cuts

Read the Content Cleanup Findings section from {outputFile}.

**If no content cuts exist:**
"**No content cuts were identified during transcript analysis.** Only deterministic audio cleanup will be applied."

**If auto-decided cuts exist:**
"**Step 4 (review) — passthrough mode. {approved_count} cuts auto-approved, {rejected_count} auto-rejected by step 2.**"

### 2. Write Approved Cuts Section

Copy `AUTO_APPROVED` cuts from the Content Cleanup Findings into the **Approved Content Cuts** section of {outputFile}:

```markdown
## Approved Content Cuts

**Review Decision:** Autonomous (auto-decided in step 2)
**Approved:** {approved_count} of {total} identified cuts
**Rejected:** {rejected_count} of {total} identified cuts
**Total content to remove:** {approved_seconds}s

**Approved Cuts:**

| ID | Type | Start | End | Duration | Reason |
|----|------|-------|-----|----------|--------|
| C1 | Repetition | 00:15.234 | 00:22.456 | 7.2s | Retake — keeping take 1 |
| ... | ... | ... | ... | ... | ... |

**Auto-Rejected Cuts (kept in video):**

| ID | Type | Start | End | Duration | Reason for rejection |
|----|------|-------|-----|----------|---------------------|
| ... | ... | ... | ... | ... | Low confidence — kept |
```

Update frontmatter: append `'step-04-review'` to `stepsCompleted`.

### 3. Proceed

"**Proceeding to clip plan generation...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Auto-decided cuts from step 2 passed through without modification
- No user interaction required
- Frontmatter updated with step completion

### ❌ SYSTEM FAILURE:

- Asking user for input (this is a passthrough step)
- Modifying auto-decisions from step 2
- Adding new cuts not identified in step 2

**Master Rule:** This step is a passthrough. Auto-decisions from step 2 are final. No user interaction.
