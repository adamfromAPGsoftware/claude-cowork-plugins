---
name: linkedin-x-daily
description: Daily LinkedIn + X content generation cycle — 8-step automated workflow
projectRoot: '{project-root}'
stateFile: '{project-root}/autopilot-state.yaml'
draftQueue: '{project-root}/draft-queue/'
contentCalendar: '{content_output_folder}/calendar/content-calendar.yaml'
youtubeLibrary: '{project-root}/context/youtube/channel-library.json'
inspirationLibrary: '{project-root}/memory/2-copywriter-sidecar/inspiration/linkedin.md'
leadMagnetKeywords: '{project-root}/context/lead-magnet-keywords.yaml'
brandVoice: '{project-root}/context/references/brand-voice.md'
contentICP: '{project-root}/context/references/content-icp.md'
linkedinWritingRules: '{project-root}/content-plugin/skills/2-copywriter/workflows/linkedin-content/data/writing-rules.md'
linkedinHookPatterns: '{project-root}/content-plugin/skills/2-copywriter/workflows/linkedin-content/data/hook-patterns.md'
linkedinCTAPatterns: '{project-root}/content-plugin/skills/2-copywriter/workflows/linkedin-content/data/cta-patterns.md'
xWritingRules: '{project-root}/content-plugin/skills/2-copywriter/workflows/x-content/data/writing-rules.md'
pillarData: './data/pillar-rotation.md'
formatData: './data/format-rotation.md'
nickStyleGuide: '{project-root}/content-plugin/skills/6-autopilot/references/external-style-reference.md'
adamStyleProfiles: '{project-root}/content-plugin/skills/6-autopilot/references/style-profiles.md'
linkedinPostsReference: '{project-root}/content-plugin/skills/6-autopilot/references/linkedin-posts/'
postingScheduleGuide: '{project-root}/content-plugin/skills/5-publisher/workflows/schedule-publish/data/posting-schedule-guide.md'
linkedinAccountId: 'd9ed774a-cc62-4131-a08d-64be36f864bd'
xAccountId: 'e7773628-6c48-4de7-b602-cd23b9194a11'
---

# LinkedIn + X Daily Workflow

## Execution Mode

This workflow runs in two modes:
- **Manual**: User invokes `/content:6-autopilot LX` — run steps sequentially, present each step's output, wait for any skip/override signals before proceeding
- **Automated** (scheduled): Run all 8 steps end-to-end without pausing. Save everything to queue. Send push notification at end.

In automated mode: make best-case decisions at each step without asking. Log decisions in the draft frontmatter.

In manual mode: same rule applies to image generation — generate immediately without asking for permission. Image generation is always automatic regardless of mode.

## Step Sequence

Load and execute each step file in order:

1. `./steps-c/step-01-init.md` — Load state, determine today's pillar + format
2. `./steps-c/step-02-research.md` — YouTube-first check, then trend research
3. `./steps-c/step-03-analytics.md` — Pull previous post performance
4. `./steps-c/step-04-ideate.md` — Select topic and angle
5. `./steps-c/step-05-draft.md` — Generate LinkedIn + X drafts
6. `./steps-c/step-06-visual.md` — Generate or select visual asset
7. `./steps-c/step-07-quality.md` — Brand voice + anti-AI quality gate
8. `./steps-c/step-08-queue.md` — Save drafts to queue, update state, notify

## Data Flow

Each step produces a context object that the next step reads:

```
step-01 → { pillar, format, template, cta_type }
step-02 → { topic_source, candidate_topics, youtube_video_id? }
step-03 → { analytics_insights[] }
step-04 → { topic_brief, angle, hook_direction, key_points, cta_config, style_profile }
step-05 → { linkedin_draft, x_draft, first_comment? }
step-06 → { media_path?, ffmpeg_command?, media_type }
step-07 → { quality_score, passed, revisions[] }
step-08 → { draft_files[], calendar_entries[], state_updated }
```

All data is held in context — do not write intermediate files between steps.
