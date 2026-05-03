---
name: step-03-trends
description: Find YouTube outliers in the Claude AI niche from the last 48 hours — same scoring as LX workflow
nextStep: ./step-04-analyze.md
---

# Step 3: Trend Research (YouTube Outliers)

## Goal

Find what's breaking through in the Claude AI niche on YouTube right now. Use the same outlier scoring approach as the LX competitive research workflow — `outlier_score = video_views / channel_median_views` — but with a 2-day window to surface only what's hot in the last 48 hours.

This replaces web/Exa searches. YouTube outliers are the signal.

## Sequence

### 1. Run Outlier Script

Execute via Bash:

```bash
python3 {project-root}/scripts/find-inspiration-outliers.py --days 2 --json
```

The `--days 2` flag scopes results to videos published in the last 48 hours.
The `--json` flag returns structured output for parsing.

If the script fails (API key missing, quota exceeded, network error):
- Log the failure in context
- Fall back to `--days 7` (broader window) and note the fallback
- If still failing, use the topic_angle's example carousel concepts from step-01 as the trend candidate and note "no live YouTube data — using angle defaults"

### 2. Parse Results

From the JSON output, extract each video's:
- `title` — video title
- `channel` (or `creator`) — channel name
- `video_id` — YouTube video ID
- `views` — total view count
- `outlier_score` — views / channel_median_views
- `publish_date` — ISO date published
- `engagement_rate` — (likes + comments) / views

### 3. Filter to Claude AI Niche

Keep only videos where the title or channel is clearly about:
- Claude, Anthropic, or Claude Code
- AI tools, AI agents, or AI automation
- AI for business or AI productivity

Discard unrelated videos (pure Python tutorials, general ML papers, etc.).

### 4. Score Carousel Fit

For each qualifying video, score carousel fit (1–5):

- **Novelty** — Is this a new feature, release, or surprising result? (not a rehash)
- **Specificity** — Does it have a concrete number, stat, or capability claim?
- **Carousel fit** — Can this topic be broken into 5–7 discrete insight slides?
- **ICP resonance** — Does it appeal to AI builders and agency owners?
- **Outlier signal** — Is the outlier_score ≥ 2.0? (performing above channel average)

Combined carousel_fit_score = average of the 5 dimensions.

### 5. Rank and Select Top 5

Rank by `outlier_score × carousel_fit_score` combined.

Select top 5. If fewer than 3 results pass niche filtering, loosen the filter to include adjacent AI content (e.g., GPT, Gemini, general AI agents).

### 6. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Trend Research — YouTube Outliers (last 48h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top outlier candidates (ranked):

1. [outlier: {score}x | carousel: {score}/5] {title}
   Channel: {channel} | Views: {views} | Published: {date}
   Why it works: {1-sentence carousel angle}

2. [outlier: {score}x | carousel: {score}/5] {title}
   ...

3–5. ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: YouTube outlier script (--days 2)
{if fallback: "⚠ Fallback: {reason}"}
```

Then immediately load and execute step-04.
