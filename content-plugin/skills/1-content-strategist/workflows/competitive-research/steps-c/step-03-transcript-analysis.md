---
name: 'step-03-transcript-analysis'
description: 'Pull and analyse transcripts of top outlier videos to extract content patterns and insights'

nextStepFile: './step-04-gap-insights.md'
outputFile: '{output_path}/competitive-research-{date}.md'
youtubeApiReference: '../data/youtube-api-reference.md'
---

# Step 3: Transcript Analysis

## STEP GOAL:

To pull transcripts from the top 3-5 outlier videos identified in step 2 (either mode), analyse their content angles, hook structures, talking points, and unique value propositions, and synthesise patterns across transcripts.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a content analyst specialising in reverse-engineering successful video content
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in content structure analysis, hook identification, and pattern recognition
- ✅ This step uses intent-based analysis — interpret patterns, don't just extract text

### Step-Specific Rules:

- 🎯 Use Pattern 2 subprocess optimization — DO NOT BE LAZY — launch one sub-agent per transcript for deep analysis
- 💬 Each sub-agent returns structured analysis findings, NOT full transcript text
- 🚫 FORBIDDEN to return raw transcripts to parent — only structured insights
- ⚙️ If sub-agents are unavailable, analyse transcripts sequentially in main thread
- 📋 If transcripts are unavailable for any video, note this in the report and continue with available transcripts

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append transcript analysis findings to {outputFile} under Transcript Insights section
- 📖 Update output frontmatter stepsCompleted when complete
- 🚫 FORBIDDEN to skip available transcripts

## CONTEXT BOUNDARIES:

- Available: Outlier video list from step 2 (in output report), `youtube-transcript-api` Python library for transcript retrieval (no auth needed), YouTube MCP (`mcp__youtube__getTranscripts`) for video metadata if needed
- Focus: Deep content analysis of top outlier transcripts
- Limits: Do not identify gaps or make recommendations — that comes next
- Dependencies: Step 2a or 2b must have completed with outlier videos identified, YouTube MCP must be validated

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load API Reference and Select Videos

Load and read {youtubeApiReference} — particularly the **Transcripts / Captions** section for important limitations.

Read the outlier videos from {outputFile} (written by step 2a or 2b).

Select the top 3-5 videos for transcript analysis from **both** data pools:

**From competitor outliers (step 2a/2b):**
- Top 2-3 videos by highest outlier scores
- Preference for videos from different channels (diversity of perspectives)

**From niche-wide trending (step 2c):**
- Top 1-2 videos by highest niche trend score
- Prefer videos from **non-competitor channels** for novelty (flagged as "New Creator" in step 2c)
- If no niche-wide data exists (niche scan was disabled/skipped), fill all slots from competitor outliers

**Combined selection rules:**
- Maximum of `max_transcripts` from sidecar defaults (total across both pools)
- De-duplicate — if a video appears in both pools, count it once and fill the slot from the other pool

Display: "**Analysing transcripts from {N} top-performing videos...**"
List the selected videos with their titles and outlier scores.

### 2. Fetch Transcripts

**Do NOT use the YouTube Data API for transcripts** — the `captions.download` endpoint requires OAuth. Instead, use the `youtube-transcript-api` Python library which requires no authentication at all. See {youtubeApiReference} section 5 for full usage details.

**Primary method — shared `fetch-youtube-transcript.py` script:**

For each selected video, fetch the transcript with timestamps by running:

```bash
python3 scripts/fetch-youtube-transcript.py "{VIDEO_ID_OR_URL}"
```

The script accepts either a bare 11-char video ID or a full YouTube URL (watch, youtu.be, shorts, embed). Output is JSON with `video_id`, `url`, `segments: [{start, text}, ...]`, and `plain_text`.

**Important:** Add a 1-second delay between requests if fetching multiple transcripts.

**Fallback if `youtube-transcript-api` fails for a video:**
1. `mcp__youtube__getTranscripts` — try the YouTube MCP
2. Web search via `mcp__exa__web_search_exa` — search for "{video title} transcript"
3. Video description + comments — extract insight from metadata as partial substitute

**For each video:**
- Attempt to fetch transcript using the method above
- If the library raises an error (captions disabled/unavailable), log it and move to the next video
- Store the timestamped transcript for analysis — timestamps are critical for hook structure analysis (first 30-60 seconds)

**If NO transcripts are available for any video:**
- Note in the report: "Transcripts unavailable — analysis based on available metadata"
- Attempt analysis using video titles, descriptions, and comments instead
- If insufficient data, skip to step 5 (append to report with note) and proceed

### 3. Launch Parallel Transcript Analysis

**DO NOT BE LAZY — For EACH transcript, launch a sub-agent that performs deep analysis.**

Each sub-agent MUST analyse the transcript for:

1. **Hook Structure** (first 30-60 seconds):
   - How does the video open?
   - What hook technique is used? (question, bold claim, story, problem statement, curiosity gap)
   - How quickly does it get to the value proposition?

2. **Content Angle:**
   - What specific angle or perspective does this video take?
   - How does it differentiate from generic coverage of the topic?
   - What makes it unique?

3. **Structure & Flow:**
   - How is the content organised? (listicle, tutorial, story arc, problem-solution)
   - How many distinct sections or segments?
   - Where are the key transitions?

4. **Key Talking Points:**
   - Top 3-5 main points or arguments
   - Any surprising or contrarian claims
   - Specific examples, data, or case studies mentioned

5. **Engagement Drivers:**
   - What elements would drive comments? (controversial takes, questions posed, calls to action)
   - What makes this shareable?
   - How does it create retention (keeping viewers watching)?

6. **Niche Crossover Analysis:**
   - Does this video combine a trending topic with a crossover audience?
   - What is the PRIMARY audience (e.g., AI developers)?
   - What is the SECONDARY audience captured (e.g., video editors, traders, productivity enthusiasts)?
   - Is the crossover explicit (stated in title/hook) or implicit (embedded in content)?
   - How does the crossover contribute to the outlier score? (small channels capturing 2+ audiences = viral signal)

7. **Return structured findings to parent:**

```json
{
  "video_title": "",
  "video_id": "",
  "hook_technique": "",
  "hook_summary": "",
  "content_angle": "",
  "structure_type": "",
  "key_talking_points": [],
  "engagement_drivers": [],
  "unique_differentiator": "",
  "estimated_hook_duration_seconds": 0,
  "niche_crossover": {
    "has_crossover": false,
    "primary_audience": "",
    "secondary_audience": "",
    "crossover_type": "",
    "crossover_contribution": ""
  }
}
```

**Fallback:** If sub-agents are unavailable, perform the same analysis sequentially for each transcript in the main thread.

### 4. Synthesise Patterns

Once all sub-agents return, synthesise across all analysed transcripts:

1. **Common hook techniques:** Which hook types appear most frequently among outliers?
2. **Dominant content structures:** Are outliers mostly tutorials, stories, listicles?
3. **Recurring talking points:** What themes or arguments keep appearing?
4. **Engagement patterns:** What drives engagement across multiple outliers?
5. **Differentiation strategies:** How do top performers stand out from each other?
6. **Niche crossover patterns:** Which outliers combine trending topics with crossover audiences? Is there a correlation between crossover presence and outlier score magnitude?

**For Idea Validation mode additionally:**
- Compare the user's planned approach against what's working in the transcripts
- Identify where the user's angle aligns with or diverges from successful patterns
- Note potential advantages and risks based on transcript analysis

### 5. Append to Report

Append the following to {outputFile} under the **Transcript Insights** section:

- Per-video analysis summary (hook, angle, structure, key points)
- Cross-video pattern synthesis (common hooks, structures, themes)
- Top engagement drivers identified
- (Validation mode) How user's idea compares to what's working

Update frontmatter: append `'step-03-transcript-analysis'` to `stepsCompleted`.

### 6. Present MENU OPTIONS

Display: "**Proceeding to gap identification & insights...**"

#### Menu Handling Logic:

- After transcript analysis and report append complete, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an autonomous analysis step with no user choices
- Proceed directly to next step after findings are written to report

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Top 3-5 outlier videos selected for analysis
- Transcripts fetched (or unavailability noted)
- Each transcript deeply analysed (not surface-level)
- Patterns synthesised across transcripts
- Validation mode comparison included (if applicable)
- All findings appended to output report
- Frontmatter updated with step completion

### ❌ SYSTEM FAILURE:

- Returning raw transcript text instead of structured analysis
- Surface-level analysis (just summarising content without extracting hooks, structure, engagement drivers)
- Skipping available transcripts
- Making content recommendations in this step (too early)
- Not appending findings to the output report

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
