---
name: step-03-analytics
description: Pull previous post performance to inform hook, format, and topic decisions
nextStep: ./step-04-ideate.md
---

# Step 3: Analytics

## Goal

Get a quick read on what's been working in the creator's recent LinkedIn and X posts. Use this to calibrate hook strength, format choice, and CTA mechanics for today's draft.

## Sequence

### 1. Pull Recent Post Analytics

Call the Buffer MCP to list recent published LinkedIn posts:

```
mcp__buffer__use_buffer_api(action: "listSentPosts", platform: "linkedin", limit: 20)
```

Call `mcp__buffer__buffer_api_help` first if you need to confirm the exact action name and parameters for listing sent posts.

This returns the last 20 published LinkedIn posts with engagement data.

If the MCP call fails or returns no data, fall back to step 2.

### 2. Fallback: Inspiration Library Benchmarks

If analytics script fails, load the performance benchmarks from `{inspirationLibrary}` (linkedin.md):
- The 5 proven posts and their engagement metrics
- Category averages by pillar type
- Format performance comparison table

These benchmarks serve as the baseline when live analytics are unavailable.

### 3. Derive 3 Actionable Insights

From the analytics data (or benchmark data), derive exactly 3 insights relevant to today's pillar and format:

Example insights (calibrate to actual data):
- "Lead magnet posts from last 2 weeks averaged 340 comments — text format outperforming image 1.4x"
- "Technical posts: those with specific tool names in the hook (Claude Code, n8n) got 2x more engagement than generic AI posts"
- "Posts scheduled Tuesday 8am AEST outperformed Wednesday 9am by 35%"
- "Last personal post got 89 likes, 12 comments — resonance pattern (high like:comment ratio)"

Insights should be specific and actionable — they should influence a decision in step-04 or step-05.

### 4. Output Summary

```
Analytics brief
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data source: {buffer-sent-posts | inspiration-library-benchmarks}
Posts analyzed: {count}

Key insights for today's {pillar} / {format} post:
1. {insight}
2. {insight}
3. {insight}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-04.
