---
name: competitive-research
description: Scan YouTube trends, competitors, and market performance to produce actionable research reports
menu-code: CR
---

# [CR] Competitive Research

## Purpose

Analyse YouTube trends, competitor content, and high-performing videos in the AI/tech education space to produce data-backed competitive research reports — either discovering new opportunities through outlier analysis, or validating existing video ideas against the current market landscape.

## Role Context

You are a competitive intelligence analyst and YouTube content strategist collaborating with a content creator. This is a partnership — you bring expertise in data analysis, trend identification, and competitive positioning; the user brings domain knowledge, creative vision, and channel context.

## Workflow Architecture

This workflow uses step-file architecture with sequential enforcement. Each phase below must be completed in order. Never skip phases, never load future phases early.

### Critical Rules

- NEVER load multiple phases simultaneously
- ALWAYS complete each phase before moving to the next
- ALWAYS halt at menus and wait for user input
- NEVER create mental todo lists from future phases
- If any instruction references a subprocess or tool you lack, achieve the outcome in your main context thread

---

## Phase 1: Initialization and Mode Selection

### 1.1 Validate Environment

Confirm `YOUTUBE_API_KEY` is loaded from `{project-root}/.env`. If missing, halt:

"**YouTube API key not found.** Add your key to `{project-root}/.env`:
```
YOUTUBE_API_KEY=your_key_here
```
Then restart the workflow."

### 1.2 Load Sidecar Configuration

Load `{project-root}/content-plugin/skills/1-content-strategist/workflows/competitive-research/sidecar/config.yaml`. Extract:
- `niche` — content space to analyse
- `competitors` — channels with names and IDs
- `defaults` — timeframe_days, min_outlier_score, max_transcripts, video_limit_per_channel

Validate at least one competitor has a non-empty `channel_id`. If none, halt.

### 1.3 Detect Project Context

- If active project: `output_path` = `{project_folder}/{project-slug}/strategist/research/`
- If standalone: `output_path` = `{standalone_folder}/{date}-competitive-research/`

Display detected context (niche, competitors, project, output path).

### 1.4 Create Output Report

Create from template at `{project-root}/content-plugin/skills/1-content-strategist/workflows/competitive-research/templates/report-template.md`. Populate frontmatter.

### 1.5 Mode Selection

"**Select your research mode:**

**[T] Trend Discovery** — Scan competitor channels + niche-wide keyword trends for outlier videos, trending topics, and content gaps
**[V] Idea Validation** — Evaluate a specific video idea against the current competitive landscape

Select: [T] / [V]"

If V: gather user's video idea before proceeding.

---

## Phase 2: Data Gathering — Competitor Scan

### 2.1 Scan Competitor Channels

Load `{project-root}/content-plugin/skills/1-content-strategist/workflows/competitive-research/data/youtube-api-reference.md` for API call formats.

For each competitor channel:
1. **Fetch channel statistics** — `channels.list` with `part=snippet,statistics&id={CHANNEL_ID}`
2. **Fetch recent videos** — `playlistItems.list` for uploads playlist, then `videos.list` with batched IDs
3. **Calculate channel baseline** — median and mean views across last {video_limit} videos
4. **Calculate outlier score** — `video_views / channel_median_views`. Flag: 3x+ (standard), 5x+ (strong), 10x+ (super)
5. **Calculate engagement metrics** — `engagement_rate = (likes + comments) / views`, view velocity

### 2.2 Aggregate Results

Merge all outlier videos across channels. Rank by outlier score. Tag tiers. Extract trending topics from outlier titles.

### 2.3 Niche-Wide Scan (Trend Discovery mode)

Use web search (Exa) to scan niche-wide for high-velocity content beyond the competitor list:
- Search for trending topics in the niche
- Cross-reference with YouTube API data
- Identify emerging creators
- Build cross-platform signal map (YouTube + web convergence)

### 2.4 Idea Validation Scan (Validation mode)

Search for videos matching the user's idea:
- Exact and related keyword searches via YouTube API
- Analyse competition density, average performance, content quality
- Identify gaps the user's angle could exploit

Append all findings to output report.

---

## Phase 3: Transcript Analysis

### 3.1 Select Top Videos

Select top 3-5 videos for analysis — mix of competitor outliers and niche-wide trends. Prefer diversity across channels.

### 3.2 Fetch Transcripts

Use `youtube-transcript-api` Python library (no auth needed):
```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
import json
ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch('{VIDEO_ID}')
segments = [{'start': s.start, 'text': s.text} for s in transcript.snippets]
print(json.dumps(segments, indent=2))
"
```

If unavailable, fall back to web search for transcripts or analyse from metadata.

### 3.3 Deep Analysis Per Transcript

For each transcript, analyse:
1. **Hook Structure** (first 30-60 seconds) — technique used, time to value proposition
2. **Content Angle** — unique perspective, differentiation from generic coverage
3. **Structure and Flow** — organisation type, sections, transitions
4. **Key Talking Points** — main arguments, contrarian claims, examples
5. **Engagement Drivers** — comment triggers, shareability, retention mechanisms

### 3.4 Synthesise Patterns

Cross-transcript synthesis:
- Common hook techniques among outliers
- Dominant content structures
- Recurring themes and arguments
- Engagement patterns
- Differentiation strategies

For Validation mode: compare user's planned approach against transcript patterns.

Append findings to report.

---

## Phase 4: Gap Identification and Insights

### 4.1 Content Gap Analysis

Cross-reference outlier topics against coverage density:
- **Hot Gap** — High outlier scores + low video count
- **Emerging** — Recent outliers trending up + moderate coverage
- **Saturated** — High video count + declining performance
- **Niche Gold** — Small outlier with unusually high score from small channel

### 4.2 Web Trend Supplementation

Use Exa for broader trend context. Correlate with YouTube data:
- Topics trending on web AND YouTube = strong signal
- Topics trending on web but NOT YouTube = early-mover opportunity
- YouTube outliers without web trend = platform-specific

### 4.3 Opportunity Scoring

**Score = (Demand 0.30) + (Competition Gap 0.25) + (Trend Momentum 0.20) + (Niche Fit 0.10) + (Niche-Wide Signal 0.15)**

Each factor scored 1-10. Rank opportunities by composite score.

Append gap analysis and scored opportunities to report.

---

## Phase 5: Checkpoint — Review and Steer

Present concise summary of all findings:
- Top outliers, trending topics, transcript patterns, top opportunities
- For Validation mode: idea assessment

Ask user three steering questions:
1. **Which opportunities jump out?**
2. **Anything to deprioritise?**
3. **Anything to dig deeper on?**

Store steering decisions. Wait for user to select **[C] Continue**.

---

## Phase 6: Final Report Compilation

### 6.1 Compile with User Steering

Apply priority, deprioritisation, and deep-dive requests. Write:
- **Executive Summary** — 3-5 bullets, under 150 words
- **Outlier Videos** — Ranked table with commentary
- **Niche-Wide Trends** — Cross-platform signal map
- **Trending Topics** — Grouped by theme
- **Transcript Insights** — Actionable patterns
- **Content Gap Opportunities** — Top 5 ranked with rationale
- **Competitive Landscape** (Validation) or **Recommended Next Steps** (Trend Discovery)

### 6.2 Finalise

Update output file. Mark workflow complete in frontmatter.

Present completion summary with stats: competitors analysed, videos scanned, outliers found, top opportunities.

---

## Success Criteria

- All competitor channels scanned (none skipped)
- Real YouTube API metrics used (no hallucinated data)
- Transcripts deeply analysed (hooks, structure, engagement drivers)
- Web trend context included
- Opportunities scored with transparent methodology
- User steering reflected in final report emphasis
- Report saved to correct output path
