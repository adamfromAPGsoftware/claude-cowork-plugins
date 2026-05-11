---
name: 'step-05b-media-production'
description: 'Produce all required media assets before save and schedule — video ffmpeg, carousel PDF, image generation'

nextStepFile: './step-06-save.md'
---

# Step 5b: Media Production

## STEP GOAL:

To produce all media assets required by the approved post before allowing save or scheduling. No post with media can proceed to step-06 until its media file is confirmed to exist on disk.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step, ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 Text posts skip this step entirely — auto-proceed to step-06
- 🚫 FORBIDDEN to proceed to step-06 if the media file does not exist on disk
- ⚙️ Build and execute all commands automatically — do NOT ask the user to run them
- ✅ Verify file existence after every production command before proceeding
- 🔁 If production fails, diagnose and retry or report the error clearly to the user

---

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Format Check

**If `{post_format}` is text:**
Display: "**Text post — no media required. Proceeding to save...**"
Immediately load, read entire file, then execute {nextStepFile}. Do NOT continue.

**If `{post_format}` is image, carousel, or video:** Continue to section 2.

---

### 2. Resolve Output Paths

Resolve from session context:

- `{project_path}` = `{content_output_folder}/projects/{active_project}/`
- `{linkedin_path}` = `{project_path}linkedin/`
- `{post_slug}` = slug derived from the approved post hook (e.g. `the-next-wave-isnt-n8n-or-chatbots`)
- `{source_video}` = path to source video from `{media_plan}` (set in step-03)

Ensure the linkedin output folder exists:
```bash
mkdir -p "{linkedin_path}"
```

---

### 3. Media Production — VIDEO Format

**If `{post_format}` is video:**

#### 3a. Check if output already exists

Check whether `{linkedin_path}{post_slug}-video.mp4` already exists.

**If it exists:**
Display: "**Video file already exists at `{linkedin_path}{post_slug}-video.mp4`. Using existing file.**"
Skip to section 6.

**If it does not exist:** Continue to 3b.

#### 3b. Build ffmpeg command from media plan

Read `{media_plan}` from session context (stored in step-03). Extract:
- `source_file` — path to the proxy source video
- `segments` — array of `{start, end}` pairs in seconds
- `speed_multiplier` — e.g. 20
- `output_file` — `{linkedin_path}{post_slug}-video.mp4`

Build the ffmpeg filter_complex command dynamically:

```
For each segment[i] with start=S, end=E:
  video filter: [0:v]trim=start={S}:end={E},setpts=(PTS-STARTPTS)/{speed}[v{i}]

Concat: [v0][v1]...[vN]concat=n={N}:v=1:a=0[outv]
```

Full command template:
```bash
ffmpeg -i "{source_file}" \
  -filter_complex "
    [0:v]trim=start={S0}:end={E0},setpts=(PTS-STARTPTS)/{speed}[v0];
    [0:v]trim=start={S1}:end={E1},setpts=(PTS-STARTPTS)/{speed}[v1];
    ... (repeat for each segment) ...
    [v0][v1]...[vN]concat=n={N}:v=1:a=0[outv]
  " \
  -map "[outv]" \
  -an \
  -c:v libx264 -preset fast -crf 18 \
  "{output_file}"
```

Display the command to the user before executing so they can see what will run.

#### 3c. Execute the command

Run the ffmpeg command via Bash. Stream output so the user can see progress.

#### 3d. Verify output

Check that `{output_file}` exists and is non-zero bytes.

**If success:** Display: "**Video rendered: `{output_file}`**" and continue to section 6.

**If failure:** Display the ffmpeg error, diagnose the likely cause (missing source file, invalid timestamps, codec issue), suggest the fix, and ask the user how to proceed before retrying.

---

### 4. Media Production — CAROUSEL Format

**If `{post_format}` is carousel:**

#### 4a. Check if output already exists

Check whether `{linkedin_path}{post_slug}-carousel.pdf` already exists.

**If it exists:** Display: "**Carousel PDF already exists. Using existing file.**" Skip to section 6.

**If it does not exist:** Continue to 4b.

#### 4b. Save slides JSON

Save the slides JSON config (from step-03 media plan) to:
`{linkedin_path}{post_slug}-slides.json`

#### 4c. Run carousel generator

Use the carousel generator tool configured in your environment to convert the slides JSON to a PDF carousel.

```
Input:  {linkedin_path}{post_slug}-slides.json
Output: {linkedin_path}{post_slug}-carousel.pdf
Mode:   carousel
```

Display the command before executing.

#### 4d. Verify output

Check that `{linkedin_path}{post_slug}-carousel.pdf` exists.

**If success:** Display: "**Carousel PDF generated: `{linkedin_path}{post_slug}-carousel.pdf`**" and continue to section 6.
**If failure:** Report the error and ask user how to proceed.

---

### 5. Media Production — IMAGE Format

**If `{post_format}` is image:**

Inspect `{media_plan}` source type:

**If source is `existing-asset`:**
- Verify the asset path from `{media_plan}` exists on disk
- If it exists: Display "**Image asset confirmed at `{asset_path}`**" and continue to section 6
- If it does not exist: Report the missing file and ask the user to confirm the correct path

**If source is `carousel-generator (single-image)`:**

#### 5a. Check if output already exists

Check whether `{linkedin_path}{post_slug}-image.png` already exists.
**If it exists:** Display: "**Image already exists. Using existing file.**" Skip to section 6.

#### 5b. Save single-slide JSON

Save the single-slide JSON config (from step-03 media plan) to:
`{linkedin_path}{post_slug}-slide.json`

#### 5c. Run carousel generator in single-image mode

Use the carousel generator tool configured in your environment to convert the single-slide JSON to a PNG image.

```
Input:  {linkedin_path}{post_slug}-slide.json
Output: {linkedin_path}{post_slug}-image.png
Mode:   single-image
```

Display the command before executing.

#### 5d. Verify output

Check `{linkedin_path}{post_slug}-image.png` exists.
**If success:** Display: "**Image generated: `{linkedin_path}{post_slug}-image.png`**" and continue to section 6.
**If failure:** Report the error and ask user how to proceed.

**If source is `nano-banana-generated`:**
- Generate the image using mcp__fal-ai__generate_image with model_id: "fal-ai/nano-banana-2"
- Ask the user to confirm when the image is saved to `{linkedin_path}{post_slug}-image.png`
- Verify it exists on disk before proceeding

---

### 6. Media Confirmed — Proceed

Display summary:

```
MEDIA READY:
  Format:  {post_format}
  File:    {confirmed_media_path}
  Status:  ✅ Confirmed on disk
```

Display: "**Media confirmed. Proceeding to save and schedule...**"

Immediately load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Text posts auto-skip without any media checks
- Video: ffmpeg command built from media plan, executed automatically, output verified
- Carousel: slides JSON saved, PDF generated, output verified
- Image (existing): asset path verified on disk
- Image (branded): single-slide JSON saved, image generated, output verified
- Media confirmed before proceeding to save and schedule

### ❌ SYSTEM FAILURE:

- Proceeding to step-06 before media file is confirmed on disk
- Asking the user to manually run commands that can be executed automatically
- Not verifying output file existence after production
- Skipping this step for non-text formats
- Losing media plan context needed to build the production command

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
