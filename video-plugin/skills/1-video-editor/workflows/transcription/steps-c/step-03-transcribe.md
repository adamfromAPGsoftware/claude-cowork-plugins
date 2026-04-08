---
name: 'step-03-transcribe'
description: 'Send audio to DeepGram Nova-3 API for pre-recorded transcription with word-level timestamps'

nextStepFile: './step-04-output.md'
---

# Step 3: DeepGram Transcription

## STEP GOAL:

To send the prepared audio file to the DeepGram Nova-3 pre-recorded speech-to-text API and receive a transcription response with word-level timestamps, confidence scores, and optional speaker diarisation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed without validating the API response
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a transcription pipeline operator
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You execute prescriptive instructions precisely
- ✅ You bring DeepGram API integration expertise

### Step-Specific Rules:

- 🎯 Focus ONLY on the DeepGram API call and response validation
- 🚫 FORBIDDEN to parse the response into output files in this step
- 💬 Report API call status and response summary
- 📋 The raw API response is passed to step 4 for output generation

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Hold the complete API response for the next step
- 📖 Validate response contains word-level data
- 🚫 FORBIDDEN to proceed if API call fails or response is invalid

## CONTEXT BOUNDARIES:

- Available: Audio file path from step 2, optional params from step 1
- Focus: API call and response validation only
- Limits: Do not write output files — that's step 4
- Dependencies: Valid audio file from step 2, `DEEPGRAM_API_KEY` in environment

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load API Key

Read `DEEPGRAM_API_KEY` from the `.env` file at `{env_file}` (project root).

```bash
source "{env_file}"
```

**If API key is missing or empty:**
- Report: "DEEPGRAM_API_KEY not found in .env file. Please add it and retry."
- Do NOT proceed

### 2. Build API Request

**Endpoint:** `POST https://api.deepgram.com/v1/listen`

**Required query parameters:**
- `model=nova-3` (or user override from step 1)
- `smart_format=true` (includes punctuation — no need to also set `punctuate=true`)
- `utterances=true`
- `filler_words=true` (transcribes uh, um, mhmm, etc. verbatim for downstream filler detection)
- `language=en` (or user override from step 1)

**Optional query parameters (from step 1 settings):**
- If diarisation enabled: add `diarize=true`
- If keyterms provided: add `keyterm={term}:{boost}` for EACH term as a separate query parameter
  - **IMPORTANT:** Nova-3 uses `keyterm`, NOT `keywords`. The `keywords` parameter will return a 400 error on Nova-3.
  - Boost value is 1-5 (default 2 for moderate boosting)
  - URL-encode terms containing spaces: `keyterm=Claude%20Code:2`

**Construct the curl command:**

```bash
curl -s -X POST \
  "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&utterances=true&filler_words=true&language=en&keyterm={term1}:{boost}&keyterm={term2}:{boost}" \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H "Content-Type: audio/wav" \
  --data-binary @"{audio_file_path}" \
  -o "{output_path}/deepgram-raw-response.json" \
  -w "\n%{http_code}\n%{size_download}"
```

**Output location:** Save the raw response JSON to the same `analysis/{content-type}/` folder as the audio file. This is a temporary file that will be cleaned up after step 4 generates the structured transcript.

Report: "Configured DeepGram request: model={model}, language={language}, diarize={yes/no}, smart_format=true, utterances=true, filler_words=true, keyterms={list or 'none'}"

### 3. Submit Audio to DeepGram

Execute the curl command.

Report: "Submitting audio to DeepGram Nova-3... ({audio_file_size})"

**Check HTTP status code from curl output:**
- **200:** Success — proceed to validation
- **400:** Bad request — check error message. Common causes:
  - Using `keywords` instead of `keyterm` (Nova-3 requires `keyterm`)
  - Invalid model name
  - Unsupported parameter combination
- **401/403:** Authentication failed — check DEEPGRAM_API_KEY
- **413:** File too large — consider splitting audio
- **Other:** Report full error and halt

**If API call fails:**
"**Error: DeepGram API returned HTTP {status_code}.**

**Response:** `{error_message}`

Check the API key, parameters, and audio file format."
→ HALT. Do not proceed.

### 4. Validate API Response

Parse the response JSON and validate structure:

- Confirm `results.channels[0].alternatives[0]` exists
- Confirm `words` array is present and non-empty
- Confirm each word has: `word`, `start`, `end`, `confidence`

**If diarisation was enabled:**
- Confirm each word has a `speaker` field

**If utterances was enabled:**
- Confirm `results.utterances` array exists

**Calculate summary metrics:**
- Word count from `words` array length
- Average confidence across all words
- Duration from `metadata.duration`

**Report summary:**
"**DeepGram Response Received:**
- Words transcribed: {word_count}
- Utterances: {utterance_count}
- Duration: {duration}s
- Channels: {channels}
- Confidence (avg): {average_confidence}
- Speakers detected: {speaker_count or 'N/A'}"

### 5. Auto-Proceed

Display: "**Proceeding to output generation...**"

#### Menu Handling Logic:

- After API response is validated, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step — proceed directly after response validation
- If API call fails, halt and report error — do NOT proceed

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the DeepGram API response is received and validated (contains word-level timestamps with non-empty words array), will you then load and read fully `{nextStepFile}` to execute output generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- API key loaded from .env file
- Request configured with correct parameters (keyterm NOT keywords for Nova-3)
- Audio submitted successfully via curl
- HTTP 200 received
- Response validated (words array non-empty, required fields present)
- Summary reported to user
- Proceeding to output generation

### ❌ SYSTEM FAILURE:

- Proceeding without API key
- Using `keywords` parameter instead of `keyterm` (Nova-3 incompatible)
- Not applying optional parameters from step 1
- Not validating response structure
- Proceeding with failed or incomplete response
- Writing output files in this step (that's step 4)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
