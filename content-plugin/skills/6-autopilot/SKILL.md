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

1. Load autopilot state from `{project-root}/autopilot-state.yaml`
2. Load brand voice from `{project-root}/context/references/brand-voice.md`
3. Load content ICP from `{project-root}/context/references/content-icp.md`
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
- Drafts in queue: `{count from draft-queue/ with status: draft}`

## Script Execution

All Python scripts can be run via the Bash tool.

## Key Paths

- State file: `{project-root}/autopilot-state.yaml`
- Draft queue: `{project-root}/draft-queue/`
- Content calendar: `{content_output_folder}/calendar/content-calendar.yaml`
- YouTube library: `{project-root}/context/youtube/channel-library.json`
- Lead magnet keywords: `{project-root}/context/lead-magnet-keywords.yaml`
- LX inspiration: `{project-root}/memory/2-copywriter-sidecar/inspiration/linkedin.md`
- IC watchlist: `{project-root}/context/instagram-watchlist.yaml`
- IC inspiration: `{project-root}/context/inspiration/instagram/`
- Buffer channel IDs: fetched at runtime via `mcp__buffer__use_buffer_api(action: "listChannels")` — stored in scheduling-config.md after setup
