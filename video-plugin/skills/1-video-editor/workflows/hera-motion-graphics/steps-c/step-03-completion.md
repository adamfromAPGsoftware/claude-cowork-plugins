---
name: 'step-03-completion'
description: 'Verify all generated motion graphic files and present summary with file paths'
---

# Step 3: Completion — Verify and Summarize

## STEP GOAL:

Verify all generated motion graphic `.mp4` files exist at their expected output paths, confirm file integrity, and present a final summary to the user.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Focus ONLY on verification and summary
- FORBIDDEN to generate any new motion graphics in this step
- Auto-complete — no user interaction required unless issues found

## MANDATORY SEQUENCE

### 1. Verify Generated Files

For each motion graphic that was marked as "generated" in the previous step:
1. Check the file exists at the resolved output path
2. Verify non-zero file size
3. Note any missing or zero-byte files

### 2. Handle Missing Files

**If all files verified:**
Proceed to summary.

**If any files missing or zero-byte:**
"**Verification Issues Found:**

| # | ID | Issue |
|---|-----|-------|
| {n} | {mg-id} | {File missing / Zero-byte file} |

[R]etry generation for failed items / [S]kip and complete / [A]bort"

Wait for user input.
- IF R: Route back to step-02-generate for failed items only
- IF S: Continue to summary, noting skipped items
- IF A: End workflow

### 3. Final Summary

"**Hera Motion Graphics — Complete**

**Generated Assets:**

| # | ID | File | Size | Path |
|---|-----|------|------|------|
| 1 | {mg-id} | {filename}.mp4 | {size} | {full_path} |
...

**Total:** {success_count} generated | {skip_count} skipped | {fail_count} failed

These assets are ready for use in the Storyboard and Remotion Edit workflows.

**Next Steps:**
- Use **[SB] Storyboard** to plan video production referencing these assets
- Use **[RE] Remotion Edit** if storyboard is already approved"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All generated files verified at correct output paths
- Clear summary with file paths provided
- Next workflow recommendations given

### FAILURE:

- Not verifying file existence
- Not reporting file sizes
- Generating new content in this step

**Master Rule:** This is a verification and summary step only. No generation.
