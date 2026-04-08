---
name: 'step-02-extract-audio'
description: 'Extract audio track from video file, or skip if input is already audio'

nextStepFile: './step-03-transcribe.md'
---

# Step 2: Extract Audio

## STEP GOAL:

To extract the audio track from the resolved video file for submission to DeepGram. If the input is already an audio file, skip extraction and proceed directly to transcription.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip the file type check
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a transcription pipeline operator
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You execute prescriptive instructions precisely
- ✅ You bring media processing expertise

### Step-Specific Rules:

- 🎯 Focus ONLY on audio extraction or bypass
- 🚫 FORBIDDEN to call the DeepGram API in this step
- 💬 Report extraction status clearly
- 📋 Output must be a valid audio file path for the next step

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Track the audio file path for the next step
- 📖 Validate the audio file exists after extraction
- 🚫 FORBIDDEN to proceed without a valid audio file

## CONTEXT BOUNDARIES:

- Available: Resolved source file path and metadata from step 1
- Focus: Audio extraction only
- Limits: Do not call DeepGram API or generate transcripts
- Dependencies: Step 1 must have resolved a valid source file path

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Check File Type

Examine the resolved source file from step 1:

**Audio file extensions:** `.mp3`, `.wav`, `.flac`, `.ogg`, `.aac`, `.m4a`, `.wma`
**Video file extensions:** `.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`, `.mxf`

**IF audio file:**
- Report: "Input is already an audio file ({extension}). Skipping extraction."
- Set audio file path = source file path
- Skip to step 4 (Auto-Proceed)

**IF video file:**
- Report: "Input is a video file ({extension}). Extracting audio track..."
- Continue to step 2

### 2. Extract Audio Track

Use `ffmpeg` to extract the audio track as 16kHz mono WAV (optimal for speech-to-text — smaller file size, no quality loss for transcription):

```bash
ffmpeg -i "{source_file_path}" -vn -ar 16000 -ac 1 -c:a pcm_s16le "{output_audio_path}" -y
```

**Output path:** Write to the analysis output folder for this content type:
- **Project mode:** `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/{content-type}-audio.wav`
- **Standalone mode:** `{standalone_folder}/{date}-video-{video-id}/video-editor/analysis/{content-type}/{content-type}-audio.wav`
- Example: body video → `analysis/body/body-audio.wav`

Create the output directory if it does not exist.

### 3. Validate Extraction

- Confirm the output audio file exists
- Confirm file size is greater than 0
- Report: "Audio extracted successfully: {output_audio_path} ({file_size})"

**If extraction fails:**
- Report the error
- Suggest: "Audio extraction failed. Check that ffmpeg is installed and the source file is not corrupted."
- Do NOT proceed to next step

### 4. Auto-Proceed

Display: "**Proceeding to DeepGram transcription...**"

#### Menu Handling Logic:

- After audio file path is confirmed (either extracted or bypassed), immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step — proceed directly after audio is ready
- If extraction fails, halt and report error

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN a valid audio file path is confirmed (either from extraction or direct audio input), will you then load and read fully `{nextStepFile}` to execute DeepGram transcription.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- File type correctly identified (audio vs video)
- Audio extraction completed successfully (if needed)
- Audio file validated (exists, non-zero size)
- Audio file path ready for next step
- Proceeding to transcription

### ❌ SYSTEM FAILURE:

- Not checking file type before extraction
- Attempting extraction on an audio file
- Proceeding with a non-existent or empty audio file
- Not validating extraction output
- Calling DeepGram API in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
