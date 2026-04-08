---
name: 'step-02-analyse'
description: 'Upload video to Gemini and execute visual analysis with configured parameters'

nextStepFile: './step-03-output.md'
geminiPrompt: '../data/gemini-prompt.md'
classificationTaxonomy: '../data/classification-taxonomy.md'
---

# Step 2: Video Upload & Gemini Analysis

## STEP GOAL:

To upload the video to the Gemini Files API, send it with the configured FPS and prescriptive analysis prompt, and receive structured visual segment analysis covering the entire video timeline.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip reading the entire step file before taking action
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video analysis pipeline operator — technical, precise, prescriptive
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ This step is fully autonomous — no user interaction during analysis
- ✅ You bring Gemini API expertise and video processing precision

### Step-Specific Rules:

- 🎯 Focus ONLY on Gemini API interaction — upload, analyse, collect results
- 🚫 FORBIDDEN to compile final JSON output — that is step-03's job
- 💬 Report progress to user but do not ask for input during analysis
- 📋 Use ONLY the prescriptive prompt from {geminiPrompt} — do not improvise analysis instructions
- 🔧 Use structured output (`response_mime_type: "application/json"` with `response_schema`) to guarantee valid JSON
- ⚙️ Set `temperature: 0.2` for consistent, accurate classification

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Store raw Gemini analysis results for step-03 to consume
- 📖 Load the prescriptive prompt and classification taxonomy before analysis
- 🚫 FORBIDDEN to modify or improvise the Gemini prompt — use {geminiPrompt} exactly

## CONTEXT BOUNDARIES:

- Available: Video file path, FPS setting, chunking plan from step-01
- Focus: Gemini API upload and analysis execution
- Limits: Do NOT compile final output — raw results only
- Dependencies: Step-01 must have provided all configuration parameters

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Analysis Resources

Load {geminiPrompt} and {classificationTaxonomy} to prepare the analysis prompt and output schema.

"**Loading analysis configuration...**"

- Read the system prompt from {geminiPrompt}
- Read the Pydantic schema / JSON schema from {classificationTaxonomy}
- Confirm FPS, chunking plan, and media resolution from step-01 configuration

### 2. Upload Video to Gemini Files API

"**Uploading video to Gemini Files API...**"

**Upload process:**

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# Upload via Files API (recommended for all production use)
video_file = client.files.upload(file=video_path)

# Wait for processing to complete
# Files API processes video asynchronously — poll until state is ACTIVE
```

**Report upload status:**
"**Upload complete.** File URI: {file_uri}
Waiting for Gemini to finish processing..."

**Wait for processing:**
- Poll `client.files.get(name=video_file.name)` until state is `ACTIVE`
- Report when ready: "**Video processed and ready for analysis.**"

### 3. Execute Analysis

**IF NO CHUNKING NEEDED (video within single-request limits):**

"**Running visual analysis on full video...**"

Send single request to Gemini with:
- The uploaded video file
- System prompt from {geminiPrompt}
- Custom FPS via `videoMetadata(fps=configured_fps)`
- Media resolution setting (default or low based on step-01 assessment)
- Structured output config: `response_mime_type: "application/json"`, `response_schema: VisualAnalysisSegments`
- `temperature: 0.2`

```python
response = client.models.generate_content(
    model="gemini-3.1-pro-preview",  # Note: gemini-3-pro-preview was deprecated March 9, 2026. Always use gemini-3.1-pro-preview.
    contents=[
        types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(
                        file_uri=video_file.uri,
                        mime_type="video/mp4"
                    ),
                    video_metadata=types.VideoMetadata(fps=configured_fps)
                ),
                types.Part(text=system_prompt),
            ],
        ),
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema": VisualAnalysisSegments,
        "temperature": 0.2,
        "media_resolution": media_resolution_setting
    }
)
```

Store the response segments.

**IF CHUNKING IS NEEDED (video exceeds single-request limits):**

"**Video requires chunked analysis ({chunk_count} chunks)...**"

For each chunk:

1. Use `videoMetadata` with `start_offset` and `end_offset` to query a time range
2. Send the same prescriptive prompt and schema for each chunk
3. Report progress: "**Analysing chunk {N} of {total} ({start_time} - {end_time})...**"
4. Store chunk results

```python
for i, chunk in enumerate(chunk_plan):
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",  # Note: gemini-3-pro-preview was deprecated March 9, 2026. Always use gemini-3.1-pro-preview.
        contents=[
            types.Content(
                parts=[
                    types.Part(
                        file_data=types.FileData(
                            file_uri=video_file.uri,
                            mime_type="video/mp4"
                        ),
                        video_metadata=types.VideoMetadata(
                            fps=configured_fps,
                            start_offset=f"{chunk['start_seconds']}s",
                            end_offset=f"{chunk['end_seconds']}s"
                        )
                    ),
                    types.Part(text=system_prompt),
                ],
            ),
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": VisualAnalysisSegments,
            "temperature": 0.2,
            "media_resolution": media_resolution_setting
        }
    )
    # Store chunk results with offset metadata
```

### 4. Validate Analysis Results

"**Validating analysis results...**"

For each set of results (single or per-chunk):

1. **Timeline continuity** — Verify no gaps between segments (endTimestamp of one matches timestamp of next)
2. **Full coverage** — First segment starts at 00:00, last segment ends at video duration
3. **Valid classifications** — All classifications match taxonomy (talking-head, screen-share, diagram-slides, transition, mixed-pip)
4. **Required fields** — Every segment has all required fields populated
5. **Confidence scores** — All between 0.0 and 1.0

**If validation issues found:**
- Log issues but do not re-query (step-03 will handle gaps in compilation)
- Report: "**Validation complete.** {issue_count} minor issues found — will be resolved during compilation."

**If validation passes:**
- Report: "**Validation complete.** All segments valid."

### 5. Report Analysis Summary

"**Analysis complete.**

**Results:**
- **Total segments:** {count}
- **Timeline coverage:** {start} to {end}
- **Classifications found:**
  - Talking head: {count}
  - Screen share: {count}
  - Diagram/slides: {count}
  - Transition: {count}
  - Mixed/PiP: {count}
- **High B-roll segments:** {count}
- **Chunks processed:** {count or 'N/A — single request'}

**Proceeding to output compilation...**"

### 6. Auto-Proceed to Output

Display: "**Proceeding to output compilation...**"

#### Menu Handling Logic:

- After analysis is complete and results are stored, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step with no user choices during analysis
- Proceed directly to next step after analysis completes

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN analysis is fully complete, validated, and summary reported, will you then load and read fully {nextStepFile} to compile the final JSON output.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Video uploaded to Gemini Files API successfully
- Analysis executed with correct FPS and prescriptive prompt
- Structured output used (response_schema) for guaranteed valid JSON
- All chunks processed (if chunked)
- Timeline continuity validated
- Results stored for step-03 consumption
- Summary reported to user

### ❌ SYSTEM FAILURE:

- Improvising the analysis prompt instead of using {geminiPrompt}
- Not using structured output (response_schema)
- Not validating timeline continuity
- Skipping chunks in a chunked analysis
- Compiling final JSON in this step (that is step-03's job)
- Using temperature above 0.3

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
