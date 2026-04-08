---
name: 'step-02-analyse'
description: 'Run analyze-audio.ts (FFmpeg silencedetect + Silero VAD) against the resolved video file'

nextStepFile: './step-03-output.md'
---

# Step 2: Audio Analysis (Three-Layer)

## STEP GOAL:

To run `analyze-audio.ts` (FFmpeg silencedetect + dB waveform + Silero VAD) against the resolved video file, producing a 5-section markdown output consumed by Step 3.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator and audio analyst
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Report execution results clearly with structured data

### Step-Specific Rules:

- 🎯 Focus ONLY on executing analyze-audio.ts and capturing its output markdown path
- 🚫 FORBIDDEN to parse or interpret the output — that is Step 3
- 🚫 FORBIDDEN to modify the video or audio file in any way
- 💬 Report execution status: command used, exit code, output file path
- 📋 The script writes a markdown file — capture the output path for Step 3

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Capture the output markdown path for Step 3
- 📖 Report execution status before proceeding
- 🚫 FORBIDDEN to proceed if the script returns a non-zero exit code

## CONTEXT BOUNDARIES:

- Available context: Resolved video file path from Step 1 (proxy or raw)
- Focus: Script execution only
- Limits: Do NOT parse output or write JSON yet — that is Step 3
- Dependencies: Step 1 must have completed with a valid, accessible file

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Check Dependencies

Verify required tools are available:

```bash
# Check ffmpeg (must support arnndn filter for denoising)
ffmpeg -version 2>&1 | head -1
ffmpeg -filters 2>/dev/null | grep arnndn

# Check python3
python3 --version

# Check silero-vad Python package
python3 -c "from silero_vad import load_silero_vad; print('silero-vad OK')" 2>&1

# Check npx/tsx
npx --version

# Check curl (for auto-downloading RNNoise model)
curl --version 2>&1 | head -1
```

**If any dependency is missing:**
"**Error: Missing dependency — `{tool}`.**

Install instructions:
- ffmpeg (with arnndn): `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- python3: https://python.org
- silero-vad: `pip3 install silero-vad`
- npx/tsx: requires Node.js — `npm install -g tsx`
- curl: should be pre-installed on macOS/Linux

Note: The RNNoise model for denoising is auto-downloaded on first run by the script."
→ HALT. Do not proceed.

**If `node_modules/` is absent** in the `audio-analysis/` script directory:

```bash
cd "{script_dir}" && npm install
```

### 2. Determine Output Path

Construct the output path for the analysis markdown:

**Project Mode:**
`{project_folder}/{project-slug}/video-editor/analysis/{content-type}/audio-analysis.md`

**Standalone Mode:**
`{standalone_folder}/{date}-video-{video-id}/video-editor/analysis/{content-type}/audio-analysis.md`

Create the directory if it does not exist:
```bash
mkdir -p "{output_dir}"
```

### 3. Construct Command

The script directory is: `{workflow_dir}/audio-analysis/`

**Without transcript (no transcript JSON exists yet):**
```bash
npx tsx "{script_dir}/analyze-audio.ts" \
  --video "{resolved_file_path}" \
  --output "{analysis_md_path}" \
  --content-type "{content_type}"
```

**With transcript (transcript JSON already exists in analysis folder):**
```bash
npx tsx "{script_dir}/analyze-audio.ts" \
  --video "{resolved_file_path}" \
  --output "{analysis_md_path}" \
  --content-type "{content_type}" \
  --transcript "{transcript_json_path}"
```

Where `{transcript_json_path}` = `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/transcript.json`

Check if transcript JSON exists before deciding which form to use.

**Parameters:**
- `--video` — The resolved video file path from Step 1
- `--output` — Output path for the analysis markdown
- `--content-type` — Content type: `intro` or `main` (from Step 1 video registry)
- `--transcript` — Optional: path to an existing Deepgram transcript JSON
- `--no-denoise` — Optional: skip audio denoising (not recommended)

**Note:** The script now automatically:
1. Applies audio denoising (highpass 80Hz + RNNoise arnndn) before analysis for cleaner classification
2. Downloads the RNNoise model on first run if not present
3. Writes `audio-analysis.json` directly alongside the markdown (deterministic, no LLM parsing needed)
4. Extracts filler word regions from transcript if provided

### 4. Execute Command

Run the constructed command.

Report during execution:
"**Executing audio analysis (denoised three-layer: highpass+arnndn → FFmpeg + waveform + Silero VAD)...**

**Command:** `{constructed_command}`
**Input file:** `{resolved_file_path}`
**Output:** `{analysis_md_path}`"

Note: The script logs progress to stdout. This may take 30–120 seconds depending on video length. Silero VAD auto-downloads its ONNX model (~40MB) on first run.

### 5. Validate Execution

**Check exit code:**
- **Exit code 0:** Success — proceed
- **Non-zero exit code:** Report error and halt

**If the script fails:**
"**Error: analyze-audio.ts failed.**

**Exit code:** `{exit_code}`
**Error output:** `{error_details}`

Possible causes:
- ffmpeg not in PATH
- silero-vad not installed (`pip3 install silero-vad`)
- Node.js/npx not installed
- Invalid or corrupt video file
- Disk space insufficient for temp audio files"
→ HALT. Do not proceed.

### 6. Report Execution Results

"**Audio analysis complete.**

**Input:** `{resolved_filename}`
**Output:** `{analysis_md_path}`
**Exit code:** 0 (success)

**Proceeding to output parsing...**"

### 7. Auto-Proceed to Output

Display: "**Proceeding to parse 5-section markdown and write JSON...**"

#### Menu Handling Logic:

- After execution results are reported and the script succeeded, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step with no user choices
- Proceed directly to next step after execution report
- If the script fails, HALT and wait for user guidance

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN analyze-audio.ts has executed successfully (exit code 0) and the output markdown path is confirmed will you load and read fully `{nextStepFile}` to execute output parsing and JSON generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Dependencies verified (ffmpeg, python3, silero-vad, npx)
- npm install run if node_modules absent
- Output directory created if missing
- analyze-audio.ts executed successfully (exit code 0)
- Output markdown path captured and confirmed to exist
- Auto-proceeded to step 3

### ❌ SYSTEM FAILURE:

- Proceeding with missing dependencies
- Not capturing the output markdown path
- Proceeding after a non-zero exit code
- Attempting to parse output in this step (that is Step 3)
- Modifying the input file

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
