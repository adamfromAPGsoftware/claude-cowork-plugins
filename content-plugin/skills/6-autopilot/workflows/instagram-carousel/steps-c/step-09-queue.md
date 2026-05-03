---
name: step-09-queue
description: Save Instagram and TikTok draft files, update IC state, add calendar entries, notify
---

# Step 9: Queue

## Goal

Save both draft files, update the IC rotation state, add calendar entries, and notify the creator.

## Sequence

### 1. Determine Scheduled Times

Target Instagram posting times (peak reach for your timezone):
- Monday/Wednesday/Friday preferred (3x/week cadence)
- 7:00am–9:00am for peak reach
- Check `{contentCalendar}` for existing Instagram entries — apply 24-hour spacing rule

TikTok: same day, +2-3 hours (e.g., Instagram at 8am → TikTok at 11am for manual upload).

### 2. Write Instagram Draft File

Path: `{draftQueue}/YYYY-MM-DD-instagram-carousel.md`

```markdown
---
date: '{YYYY-MM-DD}'
platform: instagram
type: carousel
topic_angle: {topic_angle}
topic: '{1-line topic description}'
topic_source: exa-trending
source_url: '{source URL}'
slide_count: {N}
slides_dir: '{absolute path to slides_dir}'
cta_keyword: {KEYWORD}
cta_offer: '{what Comment KEYWORD delivers}'
youtube_tie_in: {video_id or null}
quality_score: '{Instagram X/10 | Visual OK|REVIEW}'
quality_note: '{note or null}'
scheduled_time: '{YYYY-MM-DDTHH:MM:00+{timezone_offset}}'
status: draft
generated_at: '{ISO datetime}'
---

{Full Instagram caption — exactly as drafted in step-06}

---

{Hashtags line}
```

### 3. Write TikTok Draft File

Path: `{draftQueue}/YYYY-MM-DD-tiktok-carousel.md`

```markdown
---
date: '{YYYY-MM-DD}'
platform: tiktok
type: carousel
topic_angle: {topic_angle}
topic: '{1-line topic description}'
slides_dir: '{same slides_dir — shared slides}'
cta_type: link-in-bio
quality_score: '{TikTok X/10}'
scheduled_time: '{YYYY-MM-DDTHH:MM:00+{timezone_offset}}'
scheduling_note: 'Manual upload via TikTok app — no API scheduling in v1'
status: draft
generated_at: '{ISO datetime}'
---

{Full TikTok caption — exactly as drafted in step-06}

---

{TikTok hashtags line}
```

### 3b. Publish via Buffer MCP (automated mode)

In automated mode, publish immediately after saving drafts. In manual mode, skip this — creator reviews via [RQ] first.

**Buffer channel IDs** are retrieved dynamically. Match on platform name and account handle from `scheduling.accounts` in config.yaml.

**Publishing flow:**

1. **List channels** — call `mcp__buffer__use_buffer_api(action: "listChannels")`. Identify the Instagram and TikTok channel IDs from the response.

2. **Post to Instagram** — call the Buffer MCP:
   ```
   mcp__buffer__use_buffer_api(
     action: "createPost",
     profileIds: [Instagram channel ID],
     text: instagram caption,
     media: [slide-01.png, slide-02.png, ...],
     scheduledAt: scheduled ISO datetime
   )
   ```

3. **Post to TikTok** — separate Buffer MCP call:
   ```
   mcp__buffer__use_buffer_api(
     action: "createPost",
     profileIds: [TikTok channel ID],
     text: tiktok caption,
     media: [slide-01.png, slide-02.png, ...],
     privacy_level: PUBLIC,
     content_preview_confirmed: true,
     express_consent_given: true
   )
   ```
   
   Call `mcp__buffer__buffer_api_help` to confirm exact TikTok field names before posting.

4. **Verify** — check response for success status and post URL. If failed, log error and set draft status to `publish_failed`.

### 4. Add Calendar Entries

Append to `{contentCalendar}`:

```yaml
  - id: '{YYYY-MM-DD}-instagram-carousel-autopilot'
    title: '{hook headline - truncated to 60 chars}'
    platform: instagram
    content_type: carousel
    status: draft
    scheduled_date: '{YYYY-MM-DD}'
    scheduled_time: '{HH:MM}'
    project_slug: autopilot
    description: '{topic_angle} carousel — {topic 1-line}'

  - id: '{YYYY-MM-DD}-tiktok-carousel-autopilot'
    title: '{hook headline - truncated to 60 chars}'
    platform: tiktok
    content_type: carousel
    status: draft
    scheduled_date: '{YYYY-MM-DD}'
    scheduled_time: '{HH:MM}'
    project_slug: autopilot
    description: '{topic_angle} carousel — {topic 1-line} (manual upload)'
```

### 5. Update State File

Write back to `{stateFile}` (autopilot-state.yaml):

Update the `ic_rotation` block:
- `ic_rotation.topic.current_index` → new index from step-01
- `ic_rotation.topic.last_date` → today

If scrape ran in step-02 and succeeded:
- `ic_rotation.inspiration.last_scrape` → today's ISO date

Append to `ic_history`:

```yaml
  - date: '{YYYY-MM-DD}'
    topic_angle: {topic_angle}
    topic: '{1-line}'
    source_url: '{url}'
    slide_count: {N}
    slides_dir: '{path}'
    cta_keyword: {KEYWORD}
    hook_photo: '{filename of photo used on hook slide}'
    instagram_draft: '{YYYY-MM-DD}-instagram-carousel.md'
    tiktok_draft: '{YYYY-MM-DD}-tiktok-carousel.md'
    quality_score: '{summary}'
    status: draft
```

### 6. Completion Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Content Autopilot — IC Run Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Angle:    {topic_angle}
Topic:    {topic 1-line}
Slides:   {N} generated
CTA:      Comment {KEYWORD}

Drafts saved:
  → {draftQueue}/YYYY-MM-DD-instagram-carousel.md
  → {draftQueue}/YYYY-MM-DD-tiktok-carousel.md
  → Slides: {slides_dir}

Scheduled for:
  Instagram: {scheduled_time}
  TikTok:    {scheduled_time} (manual upload)

Quality: {Instagram score} | {TikTok score} | Visual: {OK|REVIEW}
{if quality_note: "⚠ {quality_note}"}

Run /content:6-autopilot [RQ] to review and approve.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
