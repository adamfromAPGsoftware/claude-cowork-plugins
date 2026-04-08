---
name: 'step-03-completion'
description: 'Verify all extracted clips exist with no audio streams and present summary'
---

# Step 3: Completion — Verify and Summarize

## STEP GOAL:

Final verification of all extracted B-roll clips — confirm files exist, have correct sizes, and contain zero audio streams. Present a complete summary with file paths.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Focus ONLY on verification and summary
- FORBIDDEN to extract any new clips in this step
- Auto-complete — no user interaction required unless issues found

## MANDATORY SEQUENCE

### 1. Final File Verification

For each clip that was marked as "extracted" in the previous step:
1. Verify the `.mp4` file exists at the output path
2. Check file size is non-zero
3. Run ffprobe to confirm no audio streams:
```bash
ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "{output_path}"
```
4. Get video resolution to confirm full-res extraction

### 2. Handle Issues

**If all files verified:**
Proceed to summary.

**If any issues found:**
"**Verification Issues:**

| # | ID | Issue |
|---|-----|-------|
| {n} | {broll-id} | {File missing / Zero-byte / Audio detected / Low resolution} |

[R]etry extraction for failed items / [S]kip and complete / [A]bort"

Wait for user input.

### 3. Final Summary

"**B-Roll Extraction — Complete**

**Extracted Clips:**

| # | ID | Duration | Resolution | Size | Path |
|---|-----|----------|-----------|------|------|
| 1 | {broll-id} | {dur}s | {WxH} | {size} | {path} |
...

**Total:** {success_count} extracted | {skip_count} skipped | {fail_count} failed
**Audio Streams:** None (all clips verified silent)

These clips are ready for use in the Storyboard and Remotion Edit workflows.

**Next Steps:**
- Use **[SB] Storyboard** to plan video production referencing these clips
- Use **[RE] Remotion Edit** if storyboard is already approved
- Use **[HM] Hera Motion Graphics** if motion graphic assets are also needed"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All extracted files verified at correct output paths
- Zero audio streams confirmed on every clip
- Full resolution confirmed
- Clear summary with file paths provided

### FAILURE:

- Not verifying audio stream absence
- Not checking file existence
- Extracting new clips in this step
