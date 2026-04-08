---
name: transcription
description: DeepGram transcription with word-level timestamps
menu-code: TR
---

# [TR] Transcription

**Goal:** Send video/audio to DeepGram Nova-3 for transcription, producing word-level JSON and human-readable transcripts for Video Clipping precision and content repurposing.

**Role:** Transcription pipeline operator. Prescriptive, autonomous pipeline with minimal user interaction.

---

## Phase 1: Init and Resolve Video

### 1.1 Receive Video Target

Ask: "**Which video should I transcribe?** Provide a video ID, registry YAML path, or project slug."

### 1.2 Discover Registry YAML

Search `{project_folder}/{project-slug}/video-editor/raw/` for the matching YAML. Validate it contains `video_id`, `role`, `metadata.source_path`.

### 1.3 Resolve File Path (Proxy Preferred)

Apply proxy resolution logic — use proxy for cost-efficient transcription. Validate file exists on disk.

### 1.4 Gather Optional Parameters

"**Optional transcription settings** (press Enter to skip):
1. **Language:** Default `en`
2. **Speaker diarisation:** yes/no (default: no)
3. **DeepGram model:** Default `nova-3`
4. **Keyterm prompting:** Domain-specific terms (comma-separated) — uses `keyterm` parameter (NOT `keywords`)"

---

## Phase 2: Extract Audio

### 2.1 Check File Type

- Audio file (.mp3, .wav, .flac, .ogg, .aac, .m4a): skip extraction, use directly
- Video file (.mp4, .mov, .mkv, .avi, .webm, .mxf): extract audio track

### 2.2 Extract Audio Track

```bash
ffmpeg -i "{source_file_path}" -vn -ar 16000 -ac 1 -c:a pcm_s16le "{output_audio_path}" -y
```

Output: `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/{content-type}-audio.wav`

Validate: file exists, size > 0.

---

## Phase 3: DeepGram Transcription

### 3.1 Load API Key

Read `DEEPGRAM_API_KEY` from `.env`. HALT if missing.

### 3.2 Build API Request

**Endpoint:** `POST https://api.deepgram.com/v1/listen`

**Required params:** `model=nova-3`, `smart_format=true`, `utterances=true`, `filler_words=true`, `language=en`

**Optional:** `diarize=true` (if enabled), `keyterm={term}:{boost}` for EACH term (NOT `keywords` — incompatible with Nova-3)

### 3.3 Submit and Validate

```bash
curl -s -X POST \
  "https://api.deepgram.com/v1/listen?{params}" \
  -H "Authorization: Token $DEEPGRAM_API_KEY" \
  -H "Content-Type: audio/wav" \
  --data-binary @"{audio_file_path}" \
  -o "{output_path}/deepgram-raw-response.json"
```

Validate: HTTP 200, `results.channels[0].alternatives[0]` exists, `words` array non-empty, each word has `word`, `start`, `end`, `confidence`.

---

## Phase 4: Output Transcript

### 4.1 Generate `transcript.json`

Write structured JSON with:
- `metadata`: video_id, source_file, duration, model, language, word_count, confidence_avg
- `transcript`: full text string
- `words`: array of {word, start, end, confidence, speaker, punctuated_word}
- `utterances`: array of {start, end, text, speaker, confidence}
- `speakers`: {count, labels}

Preserve all timestamp precision. The `transcript` field serves human consumers; `words` serves machine consumers.

### 4.2 Clean Up

Remove `deepgram-raw-response.json` (data now in transcript.json). Keep the extracted audio `.wav`.

### 4.3 Update Registry

Update video registry YAML: `status: 'transcribed'`, `transcribed_at`, `transcript_path`.

### 4.4 Report Completion

Report: Words, Duration, Confidence, Speakers. Recommend next: **Video Clipping**, **Visual Analysis**, or content repurposing.
