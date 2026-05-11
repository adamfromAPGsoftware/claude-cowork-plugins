---
name: 'step-05b-media'
description: 'Handle image or video asset production for X image and video posts'

nextStepFile: './step-06-save.md'
---

# Step 5b: Media Production

## STEP GOAL:

To verify or produce the media asset (image or video) for X image and video posts, and confirm the final file path before saving.

## AUTO-SKIP RULE:

⚠️ **This step applies to IMAGE and VIDEO formats ONLY.**

If `{post_format}` is **Single**, **Thread**, or **Long Post** — this step should NOT have been loaded. If it was loaded in error, immediately load and execute `./step-06-save.md`.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a media operations specialist handling asset production and file management
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response

### Step-Specific Rules:

- 🎯 Focus only on media asset confirmation or production
- 🚫 FORBIDDEN to modify approved post text without user request
- 💬 Confirm all file paths before proceeding
- 📋 Output media to `{project_path}/x/` folder

## EXECUTION PROTOCOLS:

- 🎯 Determine media source (existing asset, generate, or user provides)
- 💾 Confirm final media file path as session variable
- 📖 Verify file specs before proceeding to save
- 🚫 FORBIDDEN to proceed without confirmed media file path

## CONTEXT BOUNDARIES:

- Approved post content and media description from previous steps are available
- Output path: `{project_path}/x/` (project mode) or `{output_folder}/x/` (personal mode)
- Focus: Media file only — content is already approved

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

---

## IF IMAGE FORMAT

### 1. Determine Image Source

"**Image asset for this post:**

From step-04 we specified: {image description from step-04}

**[E] Existing asset** — I already have the image file
**[G] Generate** — use fal-ai/nano-banana-2 to produce it
**[C] Create manually** — I'll make it and provide the path"

**If Existing asset:** Ask for the file path. Verify it exists. Store as `{media_path}`.

**If Generate:** Present a generation prompt based on the post context:

```
IMAGE GENERATION PROMPT:

Style: [clean, minimal, branded / photography / data visualization]
Dimensions: 1200×675 (16:9) or 1080×1080 (square)
Content: {description of what the image should show}
Text overlay: {any text to include — keep minimal}
```

Ask user to confirm the prompt, generate via available tool, and save output to:
`{project_path}/x/{post_slug}-image.{ext}`

Store confirmed path as `{media_path}`.

**If Create manually:** Ask user to provide the path once ready. Store as `{media_path}`.

### 2. Verify Image Specs

Once file path is confirmed, verify:
- File exists at the path
- Format: JPEG, PNG, or GIF
- Approximate file size within limits (JPEG/PNG ≤5MB, GIF ≤15MB)
- Dimensions reasonable (confirm with user if uncertain)

Flag any issues. Do not proceed if file doesn't exist.

### 3. Confirm and Proceed

"**Image confirmed:** `{media_path}`

Moving to save and scheduling."

Load, read entire file, then execute {nextStepFile}.

---

## IF VIDEO FORMAT

### 1. Determine Video Source

"**Video asset for this post:**

From the post context: {video description from step-04}

**[E] Existing file** — I already have the video file
**[T] Trim existing** — I have a longer clip to trim
**[C] Capture/record** — I need to record it first"

**If Existing file:** Ask for the file path. Verify it exists. Store as `{media_path}`.

**If Trim existing:** Ask for:
- Source file path
- Start timestamp (e.g., `00:01:30`)
- End timestamp (e.g., `00:02:45`)

Generate ffmpeg trim command:

```bash
ffmpeg -i "{source_path}" -ss {start_time} -to {end_time} -c copy "{output_path}"
```

Where `{output_path}` = `{project_path}/x/{post_slug}-video.mp4`

Display the command and ask user to run it, then confirm the output path.

**If Capture/record:** Give guidance on what to record based on the video post caption. Ask user to record and provide the path once ready.

### 2. Verify Video Specs

Once file path is confirmed, verify:
- File exists at the path
- Format: MP4 or MOV
- Duration: standard ≤2:20 min; flag if longer (requires X Premium)
- Approximate file size ≤512MB

Flag any issues. Do not proceed if file doesn't exist.

### 3. Confirm and Proceed

"**Video confirmed:** `{media_path}`

Moving to save and scheduling."

Load, read entire file, then execute {nextStepFile}.

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN media file is confirmed at a valid path will you load and read fully `{nextStepFile}` to execute save and scheduling.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Media source determined (existing, generated, or manual)
- File path confirmed and validated
- File specs verified (format, size, dimensions)
- `{media_path}` stored for step-06
- ffmpeg command provided for video trimming if needed
- Proceeds to save step with confirmed media path

### ❌ SYSTEM FAILURE:

- Running this step for single, thread, or long post formats
- Proceeding without a confirmed file path
- Not verifying the file exists before proceeding
- Missing ffmpeg command for video trim scenarios
- Not storing `{media_path}` for the save step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
