---
name: 'step-03-output'
description: 'Compile Gemini analysis results into unified JSON output, validate timeline, and save to output path'

classificationTaxonomy: '../data/classification-taxonomy.md'
---

# Step 3: Compile & Output

## STEP GOAL:

To merge all Gemini analysis results (single or chunked) into a unified JSON document with continuous timeline coverage, generate summary statistics, write the final `{video-id}-visual.json` file, and recommend next pipeline steps.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip reading the entire step file before taking action
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video analysis pipeline operator — technical, precise, prescriptive
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ This step is fully autonomous — no user interaction during compilation
- ✅ You bring data compilation expertise and pipeline orchestration precision

### Step-Specific Rules:

- 🎯 Focus ONLY on merging, validating, and writing the final JSON output
- 🚫 FORBIDDEN to re-run Gemini analysis — use only the results from step-02
- 💬 Report progress but do not ask for user input during compilation
- 📋 Output MUST conform exactly to the JSON structure in {classificationTaxonomy}
- 🔧 Resolve any minor timeline gaps from step-02 validation (interpolate missing segments)

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Write final JSON to the correct output path (project or standalone mode)
- 📖 Validate JSON is parseable and complete before writing
- 🚫 FORBIDDEN to modify analysis results — only merge and wrap with metadata

## CONTEXT BOUNDARIES:

- Available: Raw Gemini analysis segments from step-02, video metadata from step-01
- Focus: JSON compilation, timeline validation, file output
- Limits: Do NOT re-analyse video or modify Gemini's classification results
- Dependencies: Step-02 must have provided all raw analysis segments

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Collect Analysis Results

"**Compiling analysis results...**"

Gather all raw segment data from step-02:

- If single request: collect the one response's segments
- If chunked: collect all chunk responses and their offset metadata

Report: "**Collected {segment_count} segments from {chunk_count} analysis request(s).**"

### 2. Merge Chunked Results (If Applicable)

**IF CHUNKED:**

"**Merging {chunk_count} chunk results into unified timeline...**"

1. Sort all segments by timestamp (ascending)
2. Resolve chunk boundaries — where one chunk's last segment meets the next chunk's first:
   - If overlap: keep the segment with higher confidence
   - If gap: create an interpolated transition segment to maintain continuity
3. Re-index all timestamps to form a continuous timeline from 00:00 to video end

Report: "**Merged {total_segments} segments across {chunk_count} chunks. Timeline: 00:00 to {video_duration}.**"

**IF NOT CHUNKED:**

Skip this step — segments are already in a single continuous timeline.

### 3. Final Timeline Validation

"**Running final timeline validation...**"

Validate the complete merged segment list:

1. **Continuity check** — Each segment's endTimestamp matches the next segment's timestamp
2. **Coverage check** — First segment starts at 00:00, last segment ends at video duration
3. **Classification validity** — All classifications are one of: talking-head, screen-share, diagram-slides, transition, mixed-pip
4. **Required fields** — Every segment has: timestamp, endTimestamp, classification, confidence, description, details (with tool, activity, context, elements, brollRelevance)
5. **Confidence range** — All confidence values between 0.0 and 1.0
6. **B-roll validity** — All brollRelevance values are: high, medium, or low
7. **Visual events** — For talking-head and mixed-pip segments, preserve any `visualEvents` array from Gemini's response. Each visual event must have: timestamp, endTimestamp, eventType (distraction/obstruction/break), description

**If issues found:**
- Fix minor gaps by inserting transition segments
- Log any issues that could not be auto-resolved
- Report: "**Validation complete.** {issue_count} issues found and resolved."

**If validation clean:**
- Report: "**Validation complete.** All {segment_count} segments valid. Full timeline coverage confirmed."

### 4. Generate Summary Statistics

"**Generating summary statistics...**"

Calculate:

- **totalSegments** — count of all segments
- **classificationBreakdown:**
  - talking-head: count
  - screen-share: count
  - diagram-slides: count
  - transition: count
  - mixed-pip: count
- **highBrollSegments** — count of segments where brollRelevance is "high"
- **visualEventsTotal** — count of all visual events across all segments
- **visualEventsBreakdown:**
  - distraction: count
  - obstruction: count
  - break: count

### 5. Compile Final JSON Document

"**Building final JSON document...**"

Assemble the complete output JSON per the structure in {classificationTaxonomy}:

```json
{
  "videoId": "{video-id from registry or filename}",
  "analysisDate": "{today's date ISO format}",
  "totalFramesAnalysed": {calculated from FPS × duration},
  "fpsUsed": {configured FPS from step-01},
  "videoDuration": "{MM:SS format}",
  "mediaResolution": "{default or low}",
  "chunked": {true/false},
  "chunks": [{chunk metadata if chunked, empty array if not}],
  "segments": [{all validated segments}],
  "summary": {
    "totalSegments": {count},
    "classificationBreakdown": {counts per classification},
    "highBrollSegments": {count}
  }
}
```

Validate the JSON is parseable before proceeding.

### 6. Write Output File

"**Writing output file...**"

Determine output path:
- **Project mode:** `{project_folder}/{project-slug}/video-editor/analysis/{content-type}/visual-analysis.json`
- **Standalone mode:** `{standalone_folder}/{date}-video-{video-id}/video-editor/analysis/{content-type}/visual-analysis.json`

Where `{content-type}` is the video's content type from the registry (body, intro, or outro).

Create the analysis/{content-type}/ directory if it does not exist.

Write the JSON file to the determined path.

Report: "**Output saved to:** `{output_path}`"

### 7. Present Final Summary

"**Visual Analysis Pipeline — Complete**

**Results:**
- **Video:** {video filename}
- **Duration:** {video duration}
- **FPS:** {configured FPS} ({granularity label})
- **Total segments:** {count}
- **Timeline coverage:** 00:00 to {video duration} (100%)
- **Classification breakdown:**
  - Talking head: {count} ({percentage}%)
  - Screen share: {count} ({percentage}%)
  - Diagram/slides: {count} ({percentage}%)
  - Transition: {count} ({percentage}%)
  - Mixed/PiP: {count} ({percentage}%)
- **High B-roll segments:** {count}
- **Visual events detected:** {count} (distractions: {d}, obstructions: {o}, breaks: {b})
- **Chunks processed:** {count or 'N/A — single request'}
- **Output file:** `{output_path}`

**Recommended next steps:**
- Run **Transcript Analysis** workflow for speech-to-text alignment
- Run **B-Roll Extraction** workflow to identify key visual clips
- Use this JSON as input for **Clip Generation** workflow"

### 8. Pipeline Complete

This is the final step of the visual-analysis workflow. No further steps to load.

The workflow is complete when the JSON file is written and the summary is presented to the user.

## CRITICAL STEP COMPLETION NOTE

This is the FINAL STEP of the visual-analysis workflow. Upon completion, the JSON output file has been written and the pipeline summary has been presented. No nextStepFile exists — the workflow terminates here.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All analysis segments from step-02 collected and merged
- Chunked results properly merged with continuous timeline (if applicable)
- Final timeline validated — no gaps, full coverage
- Summary statistics calculated accurately
- JSON output conforms to classification taxonomy structure
- Output file written to correct path (project or standalone)
- Final summary presented to user with classification breakdown
- Recommended next pipeline steps provided

### ❌ SYSTEM FAILURE:

- Re-running Gemini analysis instead of using step-02 results
- Modifying Gemini's classification results during compilation
- Writing invalid or unparseable JSON
- Missing timeline gaps in the final output
- Not validating the merged results
- Writing to wrong output path
- Skipping summary statistics

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
