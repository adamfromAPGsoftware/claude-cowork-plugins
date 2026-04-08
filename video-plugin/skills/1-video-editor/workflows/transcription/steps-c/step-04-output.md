---
name: 'step-04-output'
description: 'Parse DeepGram response and write structured JSON transcript'
---

# Step 4: Output Transcript

## STEP GOAL:

To parse the DeepGram API response into a single structured JSON transcript file with word-level timestamps and full text, then update the video registry and report completion.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip writing the output file
- 📖 CRITICAL: Read the complete step file before taking any action
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a transcription pipeline operator
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You execute prescriptive instructions precisely
- ✅ You bring data structuring and output formatting expertise

### Step-Specific Rules:

- 🎯 Focus ONLY on parsing the response and writing the output file
- 🚫 FORBIDDEN to re-call the DeepGram API
- 💬 Report output file path and size
- 📋 JSON file must contain both the full transcript text AND word-level timestamp data — one file serves both human and machine consumers

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write the output file to the correct location
- 📖 Update video registry YAML with transcription status
- 🚫 FORBIDDEN to skip the registry update

## CONTEXT BOUNDARIES:

- Available: Complete DeepGram API response from step 3, video metadata from step 1
- Focus: Output file generation and registry update only
- Limits: Do not re-process audio or re-call API
- Dependencies: Valid API response with word-level data from step 3

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Determine Output Path

**Project mode** (if project context exists):
```
{project_folder}/{project-slug}/video-editor/analysis/{content-type}/
```

**Standalone mode** (if no project context):
```
{standalone_folder}/{date}-video-{video-id}/video-editor/analysis/{content-type}/
```

Where `{content-type}` is the video's content type from the registry (body, intro, or outro).

Ensure the output directory exists. Create it if it doesn't.

### 2. Generate JSON Transcript

Create `transcript.json` with the following structure:

```json
{
  "metadata": {
    "video_id": "{video-id}",
    "source_file": "{resolved source path}",
    "file_type": "{proxy/raw}",
    "duration_seconds": "{from API response}",
    "model": "{model used}",
    "language": "{language}",
    "diarize": "{true/false}",
    "transcribed_at": "{ISO timestamp}",
    "word_count": "{total words}",
    "confidence_avg": "{average confidence across all words}"
  },
  "transcript": "{full transcript text from alternatives[0].transcript}",
  "words": [
    {
      "word": "{word}",
      "start": "{start time in seconds}",
      "end": "{end time in seconds}",
      "confidence": "{confidence score 0-1}",
      "speaker": "{speaker number, if diarisation enabled}",
      "punctuated_word": "{word with punctuation, if available}"
    }
  ],
  "utterances": [
    {
      "start": "{utterance start time}",
      "end": "{utterance end time}",
      "text": "{utterance text}",
      "speaker": "{speaker number, if diarisation enabled}",
      "confidence": "{utterance confidence}"
    }
  ],
  "speakers": {
    "count": "{number of speakers detected, or null}",
    "labels": "{speaker label mapping, if available}"
  }
}
```

**Notes:**
- Include `utterances` array only if utterances were enabled
- Include `speaker` fields only if diarisation was enabled
- Preserve all precision in timestamps (do not round)
- The `transcript` field contains the full human-readable text — downstream agents (Copywriter) read this field directly

Write file: `{output_path}/transcript.json`

### 3. Clean Up Intermediate Files

Remove temporary files from the analysis folder that are no longer needed:

- `deepgram-raw-response.json` — raw API response (data now structured in transcript.json)

**Do NOT delete:**
- `{content-type}-audio.wav` — keep the extracted audio as it may be useful for downstream workflows

### 4. Update Video Registry

Load the video's registry YAML and update:

```yaml
status: 'transcribed'
transcribed_at: '{ISO timestamp}'
transcript_path: '{path to transcript.json}'
```

Write the updated YAML back to the registry.

### 5. Report Completion

"**Transcription Complete!**

| Output | Path | Size |
|--------|------|------|
| Transcript | `{json_path}` | {file_size} |

**Summary:**
- Words: {word_count}
- Duration: {duration}
- Confidence: {avg_confidence}%
- Speakers: {speaker_count or 'N/A'}

**Registry updated:** `{video-id}.yaml` → status: `transcribed`

---

**Recommended next workflows:**
1. **Video Clipping** — Use word-level timestamps for precise cut points
2. **Visual Analysis** — Analyse video frames for visual content
3. **Copywriter** — Repurpose transcript text for written content"

## CRITICAL STEP COMPLETION NOTE

This is the final step. The workflow is complete when the JSON transcript is written, the registry is updated, and the completion summary is presented.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- JSON transcript written with complete word-level data and full text
- Video registry YAML updated with transcription status and path
- Output directory created if it didn't exist
- Completion summary presented with file path and size
- Next workflow recommendations provided

### ❌ SYSTEM FAILURE:

- Not preserving timestamp precision in JSON
- Not updating the video registry YAML
- Not validating output file was written successfully
- Re-calling the DeepGram API instead of using existing response

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
