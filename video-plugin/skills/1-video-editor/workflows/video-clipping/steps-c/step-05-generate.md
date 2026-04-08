---
name: 'step-05-generate'
description: 'Merge all cuts into unified list, generate FFmpeg commands, finalize clip plan'

outputFile: '{project_folder}/{project-slug}/video-editor/clips/{video-id}-clip-plan.md'
---

# Step 5: Generate Final Clip Plan

## STEP GOAL:

Merge audio cleanup cuts and approved content cuts into a unified final cut list sorted by timestamp, generate ready-to-execute FFmpeg commands, and finalize the clip plan document.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify auto-decided cuts from step 2
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 This step is DETERMINISTIC — merge, sort, and generate commands
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video editing automation assistant generating the final execution plan
- ✅ Technical precision is critical — FFmpeg commands must be valid and executable
- ✅ No creative interpretation — merge data and generate commands

### Step-Specific Rules:

- 🎯 Focus ONLY on merging cuts and generating FFmpeg commands
- 🚫 FORBIDDEN to add new cuts or modify existing decisions
- 🚫 FORBIDDEN to use `silenceremove` in any generated FFmpeg command
- ✅ MUST use `trim`/`atrim` + `concat` filter for cuts
- ✅ MUST use stream copy (`-c copy`) where possible for speed
- ✅ Generated commands MUST be copy-paste executable

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Append final cut list and FFmpeg commands to {outputFile}
- 📖 Update frontmatter to mark workflow complete
- 🚫 This is the FINAL step — no next step
- ✅ MUST execute FFmpeg and produce the clipped video file
- ✅ Output path: `{project_folder}/{project-slug}/video-editor/clips/{content_type}-clipped.mp4`

## CONTEXT BOUNDARIES:

- Step 2 produced: auto-decided content cuts with raw transcript timestamps (AUTO_APPROVED / AUTO_REJECTED)
- Step 3 produced: audio precision keep segments with refined content cut boundaries
- This step merges both into a unified execution plan, executes FFmpeg, and updates the registry
- Output: finalized clip plan + clipped video file

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise.

### 1. Load All Cut Data

Read {outputFile} and extract:
- Audio precision keep segments from step 3
- AUTO_APPROVED content cuts from step 2 (with boundaries refined in step 3)

"**Generating final clip plan...**"

### 2. Merge Cuts into Unified Timeline

**Algorithm:**

1. Start with the audio cleanup keep segments (these define the base timeline after silence removal)
2. For each AUTO_APPROVED content cut from step 2 (with boundaries refined in step 3):
   - Find which keep segment(s) the content cut falls within
   - Split the keep segment to exclude the content cut
   - Adjust timestamps accordingly
3. Sort all final keep segments by start timestamp
4. Remove any segments shorter than 100ms (artifact cleanup)
5. **Orphaned fragment cleanup** — After content cuts split speech regions, short debris fragments may survive all filters. Remove any keep segment shorter than:
   - **1000ms** for `content_type = main`
   - **1500ms** for `content_type = intro`
   These fragments are cut debris — leftover tails of speech regions that were split by content cuts. They typically contain a single throwaway word (e.g., "alright", "so", "okay") and are not valuable content.
   Log each removed orphan: `"Orphaned fragment removed: {startMs}-{endMs} ({durationMs}ms)"`
6. Result: unified ordered list of final keep segments

### 3. Calculate Final Statistics

Compute:
- **Original video duration:** {seconds}s
- **Audio silence removed:** {seconds}s ({count} cuts)
- **Content cuts applied:** {seconds}s ({count} cuts)
- **Orphaned fragments removed:** {count} ({seconds}s)
- **Total removed:** {seconds}s
- **Final estimated duration:** {seconds}s
- **Total reduction:** {percentage}%

### 4. Generate FFmpeg Commands

Generate the FFmpeg command(s) to produce the final clipped video.

**Approach: Complex filter with trim and concat**

**Source video selection:**
- Use `raw_source_file` from the clip plan frontmatter as the FFmpeg input (full-resolution raw video)
- If `raw_source_file` is not set or the file does not exist, fall back to `source_file` (proxy) and log a warning: "Warning: Raw source not available. Clipping from proxy file."
- The proxy was used for all analysis (DeepGram, Gemini, audio analysis) — timestamps are identical since proxy and raw are the same content at different resolutions

For each keep segment, generate a trim filter:

```bash
ffmpeg -i "{raw_source_video}" \
  -filter_complex "
    [0:v]trim=start={seg1_start}:end={seg1_end},setpts=PTS-STARTPTS[v0];
    [0:a]atrim=start={seg1_start}:end={seg1_end},asetpts=PTS-STARTPTS[a0];
    [0:v]trim=start={seg2_start}:end={seg2_end},setpts=PTS-STARTPTS[v1];
    [0:a]atrim=start={seg2_start}:end={seg2_end},asetpts=PTS-STARTPTS[a1];
    ...
    [v0][a0][v1][a1]...[vN][aN]concat=n={segment_count}:v=1:a=1[outv][outa]
  " \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 18 \
  -c:a aac -b:a 192k \
  "{output_video}"
```

**Notes on the generated command:**
- `setpts=PTS-STARTPTS` resets timestamps for each segment
- `asetpts=PTS-STARTPTS` resets audio timestamps to match
- `concat` merges all segments sequentially
- `-crf 18` provides high quality output
- `-preset fast` balances speed and compression

**If segment count exceeds 50:**
Split into a two-pass approach:
1. First pass: Generate intermediate segments using stream copy (`-c copy`)
2. Second pass: Concatenate using a concat file list

Generate a `concat_list.txt`:
```
file 'segment_001.mp4'
file 'segment_002.mp4'
...
```

And the concat command:
```bash
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy "{output_video}"
```

### 5. Append Final Cut List and Commands to Clip Plan

Update the **Final Cut List** and **FFmpeg Commands** sections of {outputFile}:

```markdown
## Final Cut List

**Final Statistics:**

| Metric | Value |
|--------|-------|
| Original duration | {seconds}s |
| Audio silence removed | {seconds}s ({count} cuts) |
| Content cuts applied | {seconds}s ({count} cuts) |
| Total removed | {seconds}s |
| Final estimated duration | {seconds}s |
| Total reduction | {percentage}% |

**Final Keep Segments ({count}):**

| # | Start | End | Duration | Source |
|---|-------|-----|----------|--------|
| 1 | 00:00.000 | 00:05.528 | 5.528s | Audio cleanup |
| 2 | 00:05.862 | 00:12.345 | 6.483s | Audio cleanup |
| 3 | 00:12.345 | 00:15.000 | 2.655s | Audio + content cut |
| ... | ... | ... | ... | ... |

---

## FFmpeg Commands

**Execute the following command to produce the clipped video:**

\`\`\`bash
{generated_ffmpeg_command}
\`\`\`

**Output file:** {output_video_path}
```

### 6. Execute FFmpeg

**Output path:** `{project_folder}/{project-slug}/video-editor/clips/{content_type}-clipped.mp4`
- `body` / `main` → `body-clipped.mp4`
- `intro` → `intro-clipped.mp4`
- `outro` → `outro-clipped.mp4`

Execute the generated FFmpeg command via Bash with a **10-minute timeout**:
- Run the command and capture stdout/stderr
- On success: verify the output file exists and has non-zero size
- On failure: **HALT** with error details — do NOT continue

"**Executing FFmpeg...**"

After successful execution:
"**FFmpeg complete. Output: {output_path} ({file_size_mb}MB)**"

### 7. Update Registry YAML

Find the proxy registry YAML for this video and update it:

```yaml
status: 'clipped'
clipped_at: '{ISO_timestamp}'
clipped_video_path: '{relative_path_to_clipped_video}'
```

"**Registry updated: {video_id} → status: clipped**"

### 7b. Remap Transcript to Clipped Timeline

**Why this step exists:** After clipping, the original word timestamps from DeepGram no longer map to the clipped video timeline. Captions and storyboard need timestamps relative to the clipped video, not the raw source. This is deterministic math — no re-transcription or API calls needed.

**Algorithm:**

1. Load the original `transcript.json` (word-level timestamps from DeepGram)
2. Load the final keep-segments list from section 2 (the unified timeline)
3. For each word in the transcript:
   a. Find which keep-segment contains it: `word.start >= seg.start && word.start < seg.end`
   b. Calculate cumulative offset: sum of durations of all previous keep-segments
   c. Compute remapped timestamps:
      - `clipped_start = (word.start - seg.start) + cumulative_offset`
      - `clipped_end = (word.end - seg.start) + cumulative_offset`
   d. If the word falls in a removed segment (between keep-segments), drop it — it's no longer in the video
4. Remap paragraph and sentence boundaries using the same offset logic
5. Write `{project_folder}/{project-slug}/video-editor/clips/{content_type}-clipped-transcript.json` with the remapped timestamps

**Output format:** Same structure as the original DeepGram transcript JSON, but with all timestamps adjusted to the clipped video's timeline.

**Validation:**
- Total duration of remapped words should approximately equal the clipped video duration
- No word should have a negative timestamp
- Word order must be preserved
- Gaps between consecutive words should be small (< 1s) — large gaps indicate a remapping error

"**Transcript remapped to clipped timeline: {word_count} words, {dropped_count} dropped (in removed segments). Output: {output_path}**"

### 8. Finalize Clip Plan

Update {outputFile} frontmatter:

```yaml
---
stepsCompleted: ['step-01-init', 'step-02-transcript-analysis', 'step-03-audio-precision', 'step-05-generate']
lastStep: 'step-05-generate'
status: COMPLETE
clipped_video: '{output_path}'
clipped_transcript: '{content_type}-clipped-transcript.json'
date: '{current_date}'
---
```

### 9. Present Completion Summary

"**Clip Plan Complete — Video Clipped**

**Video:** {video-id}
**Original Duration:** {seconds}s
**Final Duration:** {seconds}s ({percentage}% reduction)

**Cuts Applied:**
- Content cuts (transcript-vs-script): {count} cuts ({seconds}s)
- Audio cleanup (silence, breath, noise): {count} cuts ({seconds}s)

**Clipped Video:** {output_path}
**Clip Plan:** {outputFile}

**Workflow complete.**"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Audio cleanup and auto-approved content cuts merged into unified timeline
- Orphaned fragments (< 1000ms main / < 1500ms intro) removed after merge
- Keep segments sorted by timestamp, no overlaps
- Raw source video used for FFmpeg output (proxy used only for analysis)
- FFmpeg commands generated and are valid/executable
- FFmpeg executed successfully, producing a non-zero-size clipped video file
- Registry YAML updated with `status: clipped` and output path
- Final statistics computed accurately
- Clip plan document finalized with complete data
- Frontmatter marked as COMPLETE
- Clear completion summary presented

### ❌ SYSTEM FAILURE:

- Overlapping keep segments in final cut list
- Invalid FFmpeg commands (syntax errors, wrong filter usage)
- Using `silenceremove` in generated commands
- Modifying auto-decisions from step 2
- Missing timestamps or segments
- Not executing FFmpeg (just generating commands without running them)
- Not updating registry YAML after successful clipping
- Not marking workflow as complete

**Master Rule:** The final clip plan must produce valid FFmpeg commands, execute them, and produce a clipped video file. Every keep segment must have accurate timestamps with no overlaps or gaps. Registry MUST be updated.
