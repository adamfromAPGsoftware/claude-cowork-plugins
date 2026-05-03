---
name: 6-autopilot
description: Content automation — LinkedIn + X daily drafts and 3x/week Instagram + TikTok carousels, both with human approval gate
---

# Content Autopilot

## Overview

Content automation engine for social platforms. Runs on-demand (or on a schedule), researches trending topics and AI/Claude news, drafts posts and carousels in the creator's voice, generates visuals, passes a quality gate, and saves everything to a review queue. Nothing posts without creator approval.

- **[LX]** Daily LinkedIn + X posts — YouTube-first, pillar rotation, 8-step pipeline
- **[IC]** Instagram + TikTok carousels — 3x/week, AI/Claude news-first, creator inspiration scraping, 9-step pipeline

## On Activation

1. Load autopilot state from `{project-root}/content-plugin/data/autopilot-state.yaml`
2. Load brand voice from `{project-root}/references/brand-voice.md`
3. Load content ICP from `{project-root}/references/content-icp.md`
4. Present capability menu below

## Capability Menu

```
CONTENT AUTOPILOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[LX]  LinkedIn + X Daily      Run today's LinkedIn + X content cycle
[IC]  Instagram Carousel       Run the Instagram + TikTok carousel cycle
[RQ]  Review Queue             Review, approve, edit, or reject drafts
[TS]  Test Styles              Generate one test post per creator style profile
[SM]  Save Memory              Save session notes to memory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**State summary on activation:**

Show current state from `autopilot-state.yaml`:
- LX — Today's pillar (next): `{next pillar}` | Format: `{next format}` | Last run: `{lx last_date}`
- IC — Next angle: `{next topic_angle}` | Inspiration: `{days since last scrape}d old` | Last run: `{ic last_date}`
- Drafts in queue: `{count from data/draft-queue/ with status: draft}`

## Script Execution

All Python scripts can be run via the Bash tool.

## Key Paths

- State file: `{project-root}/content-plugin/data/autopilot-state.yaml`
- Draft queue: `{project-root}/content-plugin/data/draft-queue/`
- Content calendar: `{project-root}/content/calendar/content-calendar.yaml`
- YouTube library: `{project-root}/content-plugin/data/youtube/channel-library.json`
- Lead magnet keywords: `{project-root}/content-plugin/data/lead-magnet-keywords.yaml`
- LX inspiration: `{project-root}/content-plugin/data/memory/2-copywriter-sidecar/inspiration/linkedin.md`
- IC watchlist: `{project-root}/content-plugin/data/instagram-watchlist.yaml`
- IC inspiration: `{project-root}/content-plugin/data/inspiration/instagram/`
- Buffer channel IDs: fetched at runtime via `mcp__buffer__use_buffer_api(action: "listChannels")` — stored in scheduling-config.md after setup
