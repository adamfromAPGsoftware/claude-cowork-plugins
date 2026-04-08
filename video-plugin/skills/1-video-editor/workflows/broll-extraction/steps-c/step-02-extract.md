---
name: 'step-02-extract'
description: 'Generate and execute FFmpeg extraction commands with mandatory -an flag'

nextStepFile: './step-03-completion.md'
dataFile: '../data/extraction-standards.md'
---

# Step 2: Extract B-Roll Clips

## STEP GOAL:

Generate FFmpeg commands for each extraction target, confirm with user, execute them, and verify output files.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- MUST confirm with user before executing FFmpeg commands
- EVERY FFmpeg command MUST include `-an` — no exceptions
- EVERY FFmpeg command MUST include `-y` — no exceptions
- NEVER use proxy files — full-resolution source only
- Process clips sequentially — one extraction at a time
- Report status after each completed extraction

## MANDATORY SEQUENCE

### 1. Generate FFmpeg Commands

For each extraction target, build the FFmpeg command following {dataFile} standards:

```bash
ffmpeg -y -ss {start_time} -to {end_time} -i "{source_video}" -c:v libx264 -crf 18 -preset fast -an "{output_path}"
```

**CRITICAL VALIDATION before presenting commands:**
- Confirm `-an` flag is present in EVERY command
- Confirm `-y` flag is present in EVERY command
- Confirm source path is full-resolution (not proxy)
- Confirm output path is correct

### 2. Present Commands for Confirmation

"**FFmpeg Extraction Commands:**

**Clip 1: {broll-id}**
```
ffmpeg -y -ss {start} -to {end} -i "{source}" -c:v libx264 -crf 18 -preset fast -an "{output}"
```

**Clip 2: {broll-id}**
```
ffmpeg -y -ss {start} -to {end} -i "{source}" -c:v libx264 -crf 18 -preset fast -an "{output}"
```
...

**Total:** {count} commands

**[E] Execute All** — Run all extraction commands sequentially
**[O] One-by-One** — Confirm each command individually
**[X] Cancel** — Abort extraction

Select: [E] / [O] / [X]"

Wait for user selection.

### 3. Execute Extractions

**If Execute All:**
Run each command sequentially. After each:
"Extracted: {broll-id}.mp4 ({file_size})"

**If One-by-One:**
Before each command:
"**Extracting: {broll-id}**
{full_command}
[Y]es / [S]kip"

**If any extraction fails:**
"Extraction failed for {broll-id}: {error_message}
[R]etry / [S]kip / [A]bort remaining"

### 4. Verify No Audio Streams

For each extracted clip, verify it has no audio stream:
```bash
ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "{output_path}"
```

**Expected:** Empty output (no audio streams)

**If audio stream detected:**
"WARNING: Audio stream detected in {broll-id}.mp4. Re-extracting with `-an` flag."
Re-run the extraction with `-an` explicitly.

### 5. Extraction Summary

"**Extraction Complete**

| # | ID | Duration | File Size | Audio | Status |
|---|-----|----------|-----------|-------|--------|
| 1 | {broll-id} | {dur}s | {size} | None | {ok/failed/skipped} |
...

**Success:** {success_count}/{total_count}"

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All FFmpeg commands include `-an` and `-y` flags
- User confirmed before execution
- All clips extracted and verified with no audio streams
- Full-resolution source used for all extractions

### FAILURE:

- Any FFmpeg command missing `-an` flag
- Executing without user confirmation
- Using proxy files as source
- Not verifying audio stream absence after extraction

**Master Rule:** `-an` flag on every FFmpeg command. ZERO audio in B-roll output.
