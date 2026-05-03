---
name: instagram-carousel
description: 3x/week Instagram + TikTok carousel generation — scrape inspiration, research AI/Claude news trends, draft carousel, generate visuals, queue for review
projectRoot: '{project-root}'
stateFile: '{project-root}/content-plugin/data/autopilot-state.yaml'
watchlist: '{project-root}/content-plugin/data/instagram-watchlist.yaml'
inspirationDir: '{project-root}/content-plugin/data/inspiration/instagram/'
draftQueue: '{project-root}/content-plugin/data/draft-queue/'
contentCalendar: '{project-root}/content/calendar/content-calendar.yaml'
carouselGuidelines: '{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/data/instagram-carousel-guidelines-claude-niche.md'
existingInspiration: '{project-root}/content-plugin/skills/6-autopilot/references/carousel-inspiration/'
brandVoice: '{project-root}/references/brand-voice.md'
contentICP: '{project-root}/references/content-icp.md'
leadMagnetKeywords: '{project-root}/content-plugin/data/lead-magnet-keywords.yaml'
instagramReferencePhotos: '{project-root}/content-plugin/data/instagram-reference-photos/'
assetCatalog: '{project-root}/content-plugin/data/brand-assets/asset-catalog.yaml'
designSystem: '{project-root}/content-plugin/skills/6-autopilot/references/design-system/'
hookInspirationDir: '{project-root}/content-plugin/skills/6-autopilot/references/hook-slide-inspiration/'
topicRotation: './data/topic-rotation.md'
instagramAccountId: 'a2867c79-f288-4a16-898b-5f12ed71513c'
tiktokAccountId: '38f9261d-b51e-4582-b92c-8764058f62dd'
---

# Instagram Carousel Workflow

## Goal

Research what's going viral in AI/Claude content right now, model the psychology and structure of high-performing carousels, and generate a ready-to-post carousel for Instagram + TikTok on today's trending topic. Draft-first — nothing posts without creator approval.

## Core Principle

**Trend-first, not YouTube-first.** The IC workflow targets recency — content posted in the last 48 hours that's getting outsized engagement. Carousels live or die by timing. Pick the sharpest angle on the freshest news.

**Replicate structure, not content.** The inspiration library shows you WHAT WORKS — slide count, hook technique, text density, visual flow — not WHAT TO SAY. Your job is to apply those proven patterns to original content about Claude/AI.

## Execution Mode

- **Manual**: User invokes `/content:6-autopilot IC` — run steps sequentially, present each step's output, wait for any skip/override signals before proceeding
- **Automated** (scheduled): Run all 9 steps end-to-end without pausing. Make best-case decisions. Save to queue. Send push notification at end.

In both modes: image generation is always automatic without asking permission.

## Step Sequence

Load and execute each step file in order:

1. `./steps-c/step-01-init.md` — Load IC state, advance topic rotation, flag stale inspiration
2. `./steps-c/step-02-scrape.md` — Scrape creator watchlist if inspiration is stale (conditional)
3. `./steps-c/step-03-trends.md` — Search Exa for AI/Claude news in last 48 hours
4. `./steps-c/step-04-analyze.md` — Analyze top scraped posts for style and psychology patterns
5. `./steps-c/step-05-ideate.md` — Select topic, map to carousel structure, choose CTA keyword
6. `./steps-c/step-06-draft.md` — Write per-slide copy + Instagram caption + TikTok caption
7. `./steps-c/step-07-generate.md` — Generate carousel slide images via Gemini
8. `./steps-c/step-08-quality.md` — Quality gate: brand voice, hook strength, CTA, visual consistency
9. `./steps-c/step-09-queue.md` — Save drafts, update state, add calendar entries, notify

## Data Flow

Each step produces context that the next step reads:

```
step-01 → { topic_angle, needs_scrape, ic_rotation_index }
step-02 → { scrape_status, new_posts_count, inspiration_available }
step-03 → { trend_candidates[] }
step-04 → { style_brief }
step-05 → { carousel_brief: { topic, slide_plan[], caption_hook, cta_keyword, youtube_tie_in? } }
step-06 → { slides_copy[], instagram_caption, tiktok_caption }
step-07 → { slides_dir, slide_count, slides_generated[] }
step-08 → { quality_score, passed, caption_revised }
step-09 → { draft_files[], calendar_entries[], state_updated }
```

All data is held in context — do not write intermediate files between steps.
