---
name: 'step-03-output'
description: 'Parse 5-section analyze-audio.ts markdown output, assemble JSON schema with classified_regions, write audio-analysis.json'
---

# Step 3: Parse Output & Write JSON

## IMPORTANT: Direct JSON Output

As of the latest update, `analyze-audio.ts` now writes `audio-analysis.json` DIRECTLY alongside the markdown output. This means the JSON is deterministic and does not require LLM parsing. However, this step still validates the JSON, enriches it with project metadata (video_id, project_group, etc.), and writes the final version to the correct analysis folder path.

If the script has already written `audio-analysis.json` to the output directory, read it, merge in the project metadata from Step 1, and write it to the final analysis folder path. If the JSON is missing, fall back to parsing the markdown as described below.

## STEP GOAL:

To validate and enrich the audio analysis JSON with project metadata (video_id, project_group, content_type), write `audio-analysis.json` to the analysis folder, and report completion with key metrics. Falls back to parsing the 5-section markdown if direct JSON is unavailable.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip any section — all 5 sections must be parsed
- 📖 CRITICAL: Read the complete step file before taking any action
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator and audio analyst
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Report results clearly with structured data

### Step-Specific Rules:

- 🎯 Focus on parsing the markdown output and writing valid JSON
- 🚫 FORBIDDEN to re-run analyze-audio.ts — use the markdown output from Step 2
- 💬 Report any parsing issues with the specific section that failed
- 📋 JSON must be valid and consumable by the Video Clipping workflow without transformation

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write the JSON output file to the correct analysis folder
- 📖 Report completion with key metrics summary
- 🚫 FORBIDDEN to write incomplete JSON — all sections must be populated

## CONTEXT BOUNDARIES:

- Available context: The output markdown path from Step 2, video metadata from Step 1
- Focus: Parsing and JSON assembly only
- Limits: Do NOT re-analyse or modify any source files
- Dependencies: Step 2 must have completed successfully with the output markdown written

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Read the Analysis Markdown

Read the full contents of `{analysis_md_path}` produced by Step 2.

The file has 5 sections:

```
## Section 1 — Audio Metadata
## Section 2 — Silence Regions
## Section 3 — VAD Speech Regions
## Section 4 — Speech Boundary Detail (20ms resolution at onset/offset)
## Section 5 — Classified Regions
```

Also extract from the YAML frontmatter:
- `sampleRate` — audio sample rate (Hz)
- `silenceThreshold` — the dBFS threshold used

### 2. Parse Section 1 — Audio Metadata

Extract the metadata table rows:

**Fields to extract:**
- `overall_rms_dbfs` — "Overall RMS" row
- `peak_dbfs` — "Peak Level" row
- `noise_floor_dbfs` — "Noise Floor" row
- `dynamic_range_db` — "Dynamic Range" row
- `total_speech` — "Total Speech" row (parse duration string and percentage)
- `total_silence` — "Total Silence" row
- `total_breath` — "Total Breath" row
- `total_noise` — "Total Noise" row
- `duration_s` — "Duration" row (parse the seconds value in parentheses)

**Build object:**
```json
"audio_metadata": {
  "overall_rms_dbfs": -22.5,
  "peak_dbfs": -5.8,
  "noise_floor_dbfs": -48.2,
  "dynamic_range_db": 42.4,
  "total_speech_ms": 45000,
  "total_silence_ms": 8000,
  "total_breath_ms": 1200,
  "total_noise_ms": 500
}
```

**Populate legacy `volume` and `loudness` fields** from Section 1 for backward compatibility:
```json
"volume": {
  "mean_db": "{overall_rms_dbfs}",
  "max_db": "{peak_dbfs}",
  "n_samples": 0,
  "histogram": {}
},
"loudness": {
  "integrated_lufs": null,
  "threshold_lufs": null,
  "loudness_range_lu": null,
  "lra_threshold_lufs": null,
  "lra_low_lufs": null,
  "lra_high_lufs": null,
  "true_peak_dbfs": "{peak_dbfs}"
}
```

Note: EBU R128 fields are no longer measured by this workflow — set to null.

### 3. Parse Section 2 — Silence Regions

Extract the markdown table rows.

**Table format:**
```
| # | Start (ms) | End (ms) | Duration (ms) |
```

**Build array:**
```json
"silence_regions": [
  {"startMs": 0, "endMs": 1500, "durationMs": 1500},
  {"startMs": 45200, "endMs": 47800, "durationMs": 2600}
]
```

**If no rows:** Set `"silence_regions": []`

### 4. Parse Section 3 — VAD Speech Regions

Extract the markdown table rows.

**Table format:**
```
| # | Start (ms) | End (ms) | Duration (ms) | Avg Probability |
```

**Build array:**
```json
"speech_regions": [
  {"startMs": 1520, "endMs": 45180, "durationMs": 43660, "avgProbability": 0.923}
]
```

### 5. Parse Section 4 — Speech Boundary Detail

For each speech region block in Section 4, extract the onset and offset tables.

**Block format:**
```markdown
### Region N: {startMs}–{endMs}ms (SPEECH, {durationMs}ms)

**Onset:**
| Time (ms) | RMS dBFS | Peak dBFS | VAD |
...

**Offset:**
| Time (ms) | RMS dBFS | Peak dBFS | VAD |
...
```

**Build array:**
```json
"speech_boundary_detail": [
  {
    "regionIdx": 0,
    "startMs": 1520,
    "endMs": 45180,
    "durationMs": 43660,
    "onset": [
      {"timeMs": 1370, "rmsDbfs": -52.1, "peakDbfs": -48.3, "vadProb": 0.02},
      {"timeMs": 1390, "rmsDbfs": -48.6, "peakDbfs": -44.1, "vadProb": 0.05},
      ...
    ],
    "offset": [...]
  }
]
```

### 6. Parse Section 5 — Classified Regions

Extract the markdown table rows.

**Table format:**
```
| # | Start (ms) | End (ms) | Duration (ms) | Classification | Confidence | Avg dB | VAD Prob |
```

**Build array:**
```json
"classified_regions": [
  {
    "startMs": 0,
    "endMs": 1500,
    "durationMs": 1500,
    "classification": "SILENCE",
    "confidence": 0.98,
    "avgDb": -62.3,
    "vadProb": 0.01
  },
  {
    "startMs": 1500,
    "endMs": 45180,
    "durationMs": 43680,
    "classification": "SPEECH",
    "confidence": 0.923,
    "avgDb": -22.4,
    "vadProb": 0.923
  }
]
```

Valid classifications: `SPEECH`, `SILENCE`, `BREATH`, `NOISE`

**Filler Regions (if available):**
The JSON may also contain a `filler_regions` array (extracted from transcript when `--transcript` was provided):
```json
"filler_regions": [
  {"startMs": 95760, "endMs": 96320, "durationMs": 560, "word": "uh"},
  {"startMs": 128200, "endMs": 128650, "durationMs": 450, "word": "um"}
]
```
Preserve this field in the output JSON — it is consumed by the Video Clipping workflow for filler word removal.

### 7. Assemble Complete JSON

Combine all parsed data with metadata from Step 1 into the final JSON schema:

```json
{
  "video_id": "{video-id}",
  "project_group": "{project_group}",
  "content_type": "{content_type}",
  "source_file": "{resolved_filename}",
  "source_path": "{resolved_file_path}",
  "source_role": "{proxy/raw}",
  "analysis_date": "{ISO 8601 timestamp}",
  "workflowType": "audio-analysis",
  "sample_rate": 16000,
  "noise_floor_db": -48.2,
  "dynamic_range_db": 42.4,
  "audio_metadata": { ... },
  "volume": {
    "mean_db": -22.5,
    "max_db": -5.8,
    "n_samples": 0,
    "histogram": {}
  },
  "loudness": {
    "integrated_lufs": null,
    "threshold_lufs": null,
    "loudness_range_lu": null,
    "lra_threshold_lufs": null,
    "lra_low_lufs": null,
    "lra_high_lufs": null,
    "true_peak_dbfs": -5.8
  },
  "silence_regions": [...],
  "speech_regions": [...],
  "speech_boundary_detail": [...],
  "classified_regions": [...]
}
```

**Validate JSON:** Ensure the assembled JSON is valid (properly escaped strings, correct types, no trailing commas).

### 8. Write JSON File

Write the JSON to the output path:

**Project Mode:**
`{project_folder}/{project-slug}/video-editor/analysis/{content-type}/audio-analysis.json`

**Standalone Mode:**
`{standalone_folder}/{date}-video-{video-id}/video-editor/analysis/{content-type}/audio-analysis.json`

Where `{content-type}` is the video's content type from the registry (body, intro, or outro).

Create the analysis/{content-type}/ directory if it does not exist.

**If write fails:**
"**Error: Failed to write JSON output file.**

**Target path:** `{output_path}`
**Error:** `{error_details}`

Check folder permissions and disk space."
→ HALT. Do not proceed.

### 9. Report Completion

"**Audio Analysis Complete.**

**Video ID:** `{video-id}`
**Source:** `{resolved_filename}` ({source_role})
**Output:** `{output_path}`

**Key Metrics:**
| Metric | Value |
|---|---|
| Overall RMS | `{overall_rms_dbfs}` dBFS |
| Peak Level | `{peak_dbfs}` dBFS |
| Noise Floor | `{noise_floor_dbfs}` dBFS |
| Dynamic Range | `{dynamic_range_db}` dB |
| Silence Regions | `{count}` detected |
| Speech Regions (VAD) | `{count}` detected |
| Classified Regions | `{count}` total |
| SPEECH | `{count}` regions |
| SILENCE | `{count}` regions |
| BREATH | `{count}` regions |
| NOISE | `{count}` regions |

**Next Workflow:** This audio analysis is ready for the **Video Clipping** workflow (`classified_regions` field populated).

Would you like to:
- Analyse another video?
- Proceed to Video Clipping?
- Exit?"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 5 sections parsed (metadata, silence, VAD speech, boundary detail, classified)
- `classified_regions` array populated with SPEECH/SILENCE/BREATH/NOISE entries
- `speech_regions` and `speech_boundary_detail` arrays populated
- Legacy `volume` and `loudness` fields preserved for backward compatibility
- Valid JSON assembled with all sections populated
- JSON file written to correct analysis folder
- Completion report displayed with key metrics
- Next workflow recommended (Video Clipping)

### ❌ SYSTEM FAILURE:

- Missing any section data from the JSON
- Missing `classified_regions` field
- Writing invalid JSON (parse errors, wrong types)
- Writing to wrong output path
- Not creating analysis directory when missing
- Re-running analyze-audio.ts instead of using the markdown output

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
