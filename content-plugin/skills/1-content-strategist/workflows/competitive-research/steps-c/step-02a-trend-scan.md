---
name: 'step-02a-trend-scan'
description: 'Scan competitor channels in parallel via sub-agents, calculate outlier scores, and aggregate findings'

nextStepFile: './step-02c-niche-scan.md'
outputFile: '{output_path}/competitive-research-{date}.md'
sidecarFile: '../sidecar/config.yaml'
youtubeApiReference: '../data/youtube-api-reference.md'
---

# Step 2a: Trend Discovery — Competitor Scan

## STEP GOAL:

To scan all competitor channels in parallel using sub-agents, pull recent video data via the YouTube Data API, calculate outlier scores for each video, and aggregate the results into a ranked list of outlier videos across all competitors.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a competitive intelligence analyst performing data-driven channel analysis
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in YouTube metrics, outlier detection, and competitive analysis
- ✅ This step is prescriptive — follow the data-gathering sequence exactly

### Step-Specific Rules:

- 🎯 Use Pattern 4 subprocess optimization — launch one sub-agent per competitor channel for parallel scanning
- 💬 Each sub-agent returns structured findings only (not raw API data)
- 🚫 DO NOT BE LAZY — ensure EVERY competitor channel is scanned, no shortcuts
- ⚙️ If sub-agents are unavailable, scan channels sequentially in main thread

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append outlier findings to {outputFile} under the Outlier Videos section
- 📖 Update output frontmatter stepsCompleted when complete
- 🚫 FORBIDDEN to skip any competitor channel

## CONTEXT BOUNDARIES:

- Available: Sidecar config with competitor list, YouTube MCP (`mcp__youtube__*`) — platform-level, no API key needed
- Focus: Data retrieval and outlier score calculation only
- Limits: Do not analyse content, transcripts, or gaps — that comes in later steps
- Dependencies: Step 01 must have completed, sidecar must be loaded, YouTube MCP must be validated

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load API Reference and Prepare Channel Scan

Load and read {youtubeApiReference} for correct API call formats, parameter names, and quota management. This file contains exact endpoint URLs and known pitfalls — follow it precisely.

Load the competitor list from sidecar config (already in context from step-01).

For each competitor channel, prepare a scan task with these parameters:
- `channel_id`: from sidecar (if only a @handle is available, resolve it via `channels?part=snippet&forHandle={handle}` — see API reference)
- `timeframe_days`: from sidecar defaults (default: 30)
- `video_limit`: from sidecar defaults (default: 50)

Display: "**Scanning {N} competitor channels in parallel...**"

### 2. Launch Parallel Channel Scans

**Launch sub-agents in parallel — one per competitor channel.**

Each sub-agent MUST follow the API reference in {youtubeApiReference} for correct endpoint formats.

Each sub-agent MUST:

1. **Fetch channel statistics** — use `mcp__youtube__getChannelStatistics` with `channelIds: [CHANNEL_ID]`:
   - Subscriber count, total views, total videos

2. **Fetch recent videos** — use `mcp__youtube__getChannelTopVideos` with `channelId`, then `mcp__youtube__getVideoDetails` with batched video IDs:
   - Video title, video ID, published date
   - View count, like count, comment count

3. **Calculate channel baseline:**
   - Median views across last {video_limit} videos
   - Mean views for comparison

4. **Calculate outlier score for each video:**
   - `outlier_score = video_views / channel_median_views`
   - Flag videos: 3x+ (standard outlier), 5x+ (strong), 10x+ (super)

5. **Calculate engagement metrics for outlier videos:**
   - `engagement_rate = (likes + comments) / views`
   - View velocity estimate (views / days since published)

6. **Return structured findings to parent:**

```json
{
  "channel_name": "",
  "channel_id": "",
  "subscribers": 0,
  "median_views": 0,
  "videos_scanned": 0,
  "outliers": [
    {
      "title": "",
      "video_id": "",
      "views": 0,
      "outlier_score": 0.0,
      "engagement_rate": 0.0,
      "view_velocity": 0.0,
      "published_date": "",
      "likes": 0,
      "comments": 0
    }
  ]
}
```

**Fallback:** If sub-agents are unavailable, perform the same operations sequentially for each channel in the main thread.

### 3. Aggregate Results

Once all sub-agents return:

1. **Merge all outlier videos** across channels into a single list
2. **Rank by outlier score** (highest first)
3. **Tag outlier tier:** 3x = Standard, 5x = Strong, 10x+ = Super
4. **Extract trending topics:** Analyse titles and descriptions of all outliers for recurring keywords and themes
5. **Calculate aggregate stats:**
   - Total videos scanned across all channels
   - Total outliers found (by tier)
   - Most common topics among outliers

### 4. Append to Report

Append the following to {outputFile} under the **Outlier Videos** section:

- Ranked table of outlier videos with: Rank, Title, Channel, Views, Outlier Score, Tier, Engagement Rate, Published Date
- Per-channel summary: channel name, subscribers, median views, number of outliers found
- Aggregate stats: total scanned, total outliers by tier

Update the **Trending Topics & Keywords** section with preliminary keyword/topic frequency data extracted from outlier titles.

Update frontmatter: append `'step-02a-trend-scan'` to `stepsCompleted`.

### 5. Present MENU OPTIONS

Display: "**Proceeding to transcript analysis...**"

#### Menu Handling Logic:

- After aggregation and report append complete, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an autonomous data-gathering step with no user choices
- Proceed directly to next step after data is written to report

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All competitor channels scanned (none skipped)
- Outlier scores calculated correctly (views / channel median)
- Videos ranked and tiered (3x/5x/10x+)
- Engagement metrics calculated for outliers
- Trending topics extracted from outlier titles
- All findings appended to output report
- Frontmatter updated with step completion

### ❌ SYSTEM FAILURE:

- Skipping any competitor channel
- Using hardcoded or estimated metrics instead of real API data
- Not calculating outlier scores relative to channel median
- Not appending findings to the output report
- Analysing transcripts or gaps in this step (wrong step)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
