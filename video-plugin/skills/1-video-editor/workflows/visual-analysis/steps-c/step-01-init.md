---
name: 'step-01-init'
description: 'Initialize visual analysis — discover video file, configure analysis granularity, assess chunking requirements'

nextStepFile: './step-02-analyse.md'
classificationTaxonomy: '../data/classification-taxonomy.md'
---

# Step 1: Init & Configuration

## STEP GOAL:

To discover the video file from the Video Ingest registry, configure analysis granularity (FPS), assess whether chunking is needed based on video duration, and prepare all parameters for the Gemini analysis step.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip reading the entire step file before taking action
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video analysis pipeline operator — technical, precise, prescriptive
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Minimal interaction — one configuration question, then autonomous execution
- ✅ You bring video processing expertise, user brings their video content

### Step-Specific Rules:

- 🎯 Focus ONLY on configuration — do not start analysis yet
- 🚫 FORBIDDEN to call Gemini API in this step — that happens in step-02
- 💬 Ask ONE question: analysis granularity preference
- 📋 Validate video file exists and is accessible before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Store configuration parameters for step-02 to consume
- 📖 Calculate token budget estimate for user awareness
- 🚫 FORBIDDEN to proceed without confirmed video file path

## CONTEXT BOUNDARIES:

- Available: CCS module config (video_ingest_folder, project_folder, standalone_folder)
- Focus: Video discovery, configuration, and chunking assessment
- Limits: Do NOT begin Gemini analysis — that is step-02's job
- Dependencies: Video Ingest workflow must have completed

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Discover Video File

Search for video files from the Video Ingest registry:

"**Visual Analysis Pipeline — Initializing**

Searching for video files from Video Ingest..."

**Search locations:**
1. `{video_ingest_folder}/` for registry/manifest files
2. User-provided video path (if given directly)

**If video found:**
"**Found video:** {video filename}
**Path:** {video path}
**Size:** {file size}
**Duration:** {duration if available from registry}

Is this the video you want to analyse?"

**If no video found:**
"**No video found in Video Ingest registry.**
Please provide the path to the video file you want to analyse."

Wait for user confirmation or path input.

### 2. Assess Video Properties

Once video is confirmed:

"**Assessing video properties...**"

- Determine video duration (from registry metadata or file properties)
- Determine file size
- Determine if audio track is present
- Calculate frame count at configured FPS: `duration_s × fps`
- Determine chunk count: `ceil(frame_count / 100)` (100 frames max per API call)

Report findings:
"**Video Assessment:**
- **Duration:** {duration}
- **File size:** {size}
- **Audio:** {yes/no}
- **Frames at {fps} FPS:** ~{frame_count}
- **Chunks needed:** {chunk_count}"

### 3. Configure Analysis Granularity

"**How detailed should the visual analysis be?**

Choose a granularity level based on your needs:

**[H] High Detail** — 1 frame per second
Best for: intros, short videos, fast-paced content
Token cost: ~258 tokens/sec (~929K tokens/hour)

**[S] Standard** — 1 frame every 5 seconds
Best for: most video content, good balance of detail and cost
Token cost: ~52 tokens/sec (~186K tokens/hour)

**[O] Overview** — 1 frame every 15 seconds
Best for: long-form videos (1+ hours), general understanding
Token cost: ~17 tokens/sec (~62K tokens/hour)

**[C] Custom** — specify your own FPS value

Please select: **[H]** High / **[S]** Standard / **[O]** Overview / **[C]** Custom"

**Map selection to FPS:**
- H: fps = 1.0
- S: fps = 0.2
- O: fps = 0.067
- C: Ask user for FPS value (min 0.01, max 24.0)

### 4. Calculate Token Budget & Chunking Plan

Based on video duration and selected FPS, calculate:

- Total frames to analyse: `duration_seconds × fps`
- Estimated tokens: `total_frames × 258` (default resolution) or `total_frames × 66` (low resolution)
- Whether chunking is needed:
  - With audio: chunk if > 45 minutes
  - Without audio: chunk if > 1 hour
  - Low resolution extends to ~3 hours

**If chunking IS needed:**
- Calculate number of chunks (each ≤ 45 min with audio, ≤ 60 min without)
- Plan time offsets for each chunk
- Recommend low media resolution for very long videos

"**Analysis Plan:**
- **FPS:** {selected fps} ({granularity label})
- **Total frames:** ~{count}
- **Estimated tokens:** ~{count}
- **Media resolution:** {default / low}
- **Chunking:** {not needed / X chunks of Y minutes}
- **Estimated cost:** ~{rough cost estimate based on token pricing}

**Ready to proceed with Gemini analysis.**"

### 5. Present MENU OPTIONS

Display: "**Select:** [C] Continue to Analysis"

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user selects C and a valid video file, FPS, and chunking plan are confirmed, will you then load and read fully {nextStepFile} to execute the Gemini analysis step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Video file discovered and confirmed
- Video properties assessed (duration, size, audio)
- Granularity preference captured and mapped to FPS
- Token budget calculated
- Chunking plan determined (if needed)
- All parameters ready for step-02

### ❌ SYSTEM FAILURE:

- Proceeding without confirmed video file
- Starting Gemini analysis in this step
- Not calculating token budget
- Not assessing chunking requirements
- Hardcoded paths instead of variables

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
