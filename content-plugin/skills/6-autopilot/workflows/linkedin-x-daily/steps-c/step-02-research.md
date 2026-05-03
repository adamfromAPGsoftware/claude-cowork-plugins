---
name: step-02-research
description: YouTube-first check for unpromoted videos, then trend research if none found
nextStep: ./step-03-analytics.md
---

# Step 2: Research + YouTube Check

## Goal

Check if any recent YouTube video lacks a companion LinkedIn/X post — if so, use that as today's topic. Otherwise, research trending topics via web search and outlier analysis.

## Sequence

### 1. YouTube-First Check

Read `{youtubeLibrary}` (channel-library.json). Extract the list of recently published videos (last 30 days).

For each recent video:
- Extract the video ID and title
- Check `{contentCalendar}` for any existing LinkedIn or X post entries with this video ID in `project_slug`, `description`, or that mention the video title
- Check `{draftQueue}` for any existing draft files mentioning this video
- If NO companion post found for this video → **select this video as today's topic** (YouTube-repurpose path)

If a YouTube-repurpose candidate is found:
- Load the video's transcript from `{project-root}/content-plugin/data/youtube/transcripts/{video_id}.json` if it exists, otherwise use the video title and description
- Extract 3-5 key insights or memorable moments from the transcript (look for moments where the creator shares a specific number, process step, or surprising result)
- Set `topic_source: youtube-repurpose`, `youtube_video_id: {id}`
- Skip sections 2 and 3 below, proceed directly to output

**If no unpromoted YouTube video found** → continue to sections 2 and 3.

### 2. Trend Research (if no YouTube candidate)

Use `mcp__exa__web_search_exa` to search for trending AI/automation/Claude Code topics from the last 48 hours:

Search queries (run 2-3, pick the most relevant angle for today's pillar):
- "Claude Code automation 2026" (for technical pillar)
- "AI agency freelancing latest" (for lead magnet/personal)
- "n8n Make Zapier alternative AI 2026" (for technical/lead magnet)
- "AI tools productivity business 2026" (for nurture)

Prioritise results that:
- Match today's pillar (personal → human stories, technical → tools/methods, lead-magnet → outcomes/income)
- Have high engagement signals (controversial, surprising stats, new releases)
- Connect to the creator's existing content and expertise

### 3. YouTube Outlier Finder (if no YouTube candidate)

Run: `scripts/find-inspiration-outliers.py --days 7`

Review the outlier videos returned. If any are directly relevant to today's pillar, note them as supporting context (not the topic itself — don't copy competitor topics, but they signal what's resonating).

### 4. Output Summary

```
Research complete.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic source: {youtube-repurpose | exa-trending | inspiration}
{If youtube-repurpose: "YouTube video: {title} ({video_id})"}
{If exa-trending: "Top trend angle: {description}"}

Candidate topics (ranked by pillar fit):
1. {topic description}
2. {topic description}
3. {topic description}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-03.
