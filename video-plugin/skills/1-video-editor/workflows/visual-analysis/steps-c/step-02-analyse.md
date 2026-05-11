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

### 2. Extract Frames via FFmpeg

**Default approach: extract frames at configured FPS, send as base64 image_url via OpenRouter.**

No Files API upload needed — frames are extracted locally and sent inline.

```bash
ffmpeg -i "{proxy_path}" \
  -vf "fps={configured_fps},scale=1280:-1" \
  -q:v 5 \
  "{frames_dir}/frame_%04d.jpg" \
  -y -loglevel error
```

- Output: JPEG frames at 1280px wide (good quality/size balance)
- Frame N timestamp = N × (1 / fps) seconds
- Total frames: duration_s × fps (e.g. 1034s × 0.2 = ~207 frames)

**Chunk plan:** Split into batches of MAX_FRAMES_PER_CHUNK (100) to stay within context limits.

Report: "**Extracted {N} frames, splitting into {chunks} chunk(s) of up to 100 frames...**"

### 3. Execute Analysis via OpenRouter

**Model:** `google/gemini-3.1-pro-preview` via OpenRouter (Nano Banana Pro)
**API:** OpenAI-compatible chat completions at `https://openrouter.ai/api/v1`
**Auth:** `OPENROUTER_API_KEY` from `.env`

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)
```

**For each chunk:**

Build a message with:
1. System prompt text from {geminiPrompt} (first chunk) or continuation prompt (subsequent chunks)
2. For each frame: a `[MM:SS]` timestamp text part followed by an `image_url` base64 JPEG part
3. Closing instruction: "Return ONLY the JSON object with 'segments' array."

```python
content = [{"type": "text", "text": system_prompt}]
for frame_path, ts in chunk:
    b64 = base64.b64encode(frame_path.read_bytes()).decode()
    content.append({"type": "text", "text": f"[{ts_label(ts)}]"})
    content.append({
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
    })
content.append({"type": "text", "text": "Return ONLY the JSON object with 'segments' array. No markdown."})

response = client.chat.completions.create(
    model="google/gemini-3.1-pro-preview",
    messages=[{"role": "user", "content": content}],
    max_tokens=16000,
    temperature=0.2
)
```

**JSON cleanup:** Strip markdown code fences if present before parsing.

**Rate limiting:** 2-second delay between chunks.

**Continuation prompt for chunks 2+:**
"Continue the visual analysis. These frames cover {chunk_start} to {chunk_end}. Return JSON with the same structure — 'segments' array, timestamp/endTimestamp in MM:SS, same field names. No gaps — first segment starts at {chunk_start}."

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
