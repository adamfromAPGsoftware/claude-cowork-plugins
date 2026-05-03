---
name: step-08-queue
description: Save drafts to queue, update state file, add calendar entries, notify
---

# Step 8: Queue

## Goal

Persist everything from this run: save draft files, update the rotation state, add placeholder calendar entries, and send a push notification.

## Sequence

### 1. Determine Optimal Schedule Time

Load `{postingScheduleGuide}`. Load `{contentCalendar}`.

For LinkedIn:
- Target: weekday only (Mon-Thu preferred, Fri acceptable), 7:00-9:00am AEST
- Check calendar for existing LinkedIn posts this week — apply 18-hour spacing rule
- Select the next available optimal slot

For X:
- Target: same day as LinkedIn, stagger by 1-2 hours (e.g., LinkedIn at 8am → X at 9:30am)
- Check calendar for existing X posts

### 2. Write LinkedIn Draft File

Path: `{draftQueue}/YYYY-MM-DD-linkedin.md` (use today's date)

```markdown
---
date: '{YYYY-MM-DD}'
platform: linkedin
pillar: {pillar}
format: {format}
template: {template name}
cta_type: {none|resource-giveaway|keyword}
first_comment: {URL or null}
keyword: {KEYWORD or null}
topic: '{1-line topic description}'
topic_source: {youtube-repurpose|exa-trending|inspiration}
youtube_video_id: {video_id or null}
media_path: {path or null}
media_type: {image|video-clip|none}
ffmpeg_command: '{command or null}'
hook: '{first line of the post}'
quality_score: '{score summary}'
quality_note: '{manual review note if applicable, else null}'
scheduled_time: '{YYYY-MM-DDTHH:MM:00+10:00}'
status: draft
generated_at: '{ISO datetime}'
---

{full LinkedIn post copy — exactly as drafted in step-05}
```

### 3. Write X Draft File

Path: `{draftQueue}/YYYY-MM-DD-x.md` (use today's date)

Same frontmatter structure, with:
- `platform: x`
- `format: {short-post|long-form|thread}`
- `first_reply: {URL or null}` — resource-giveaway URLs go in a first reply, NOT in the post body (links are suppressed by X algorithm even for Premium accounts)
- `scheduled_time`: staggered 1-2h from LinkedIn slot

```markdown
---
date: '{YYYY-MM-DD}'
platform: x
pillar: {pillar}
format: {format}
template: {template name}
cta_type: {none|resource-giveaway|keyword}
topic: '{1-line topic description}'
topic_source: {youtube-repurpose|exa-trending|inspiration}
media_path: {path or null}
quality_score: '{score summary}'
hook: '{first line}'
scheduled_time: '{YYYY-MM-DDTHH:MM:00+10:00}'
status: draft
generated_at: '{ISO datetime}'
---

{full X post copy — exactly as drafted in step-05}
```

### 4. Add Calendar Entries

Append two entries to `{contentCalendar}` (content-calendar.yaml):

```yaml
  - id: '{YYYY-MM-DD}-linkedin-autopilot'
    title: '{hook - truncated to 60 chars}'
    platform: linkedin
    content_type: {format}
    status: draft
    scheduled_date: '{YYYY-MM-DD}'
    scheduled_time: '{HH:MM}'
    project_slug: autopilot
    description: '{pillar} / {template} — {topic 1-line}'

  - id: '{YYYY-MM-DD}-x-autopilot'
    title: '{hook - truncated to 60 chars}'
    platform: x
    content_type: {format}
    status: draft
    scheduled_date: '{YYYY-MM-DD}'
    scheduled_time: '{HH:MM}'
    project_slug: autopilot
    description: '{pillar} / {template} — {topic 1-line}'
```

### 5. Update State File

Write back to `{stateFile}` (autopilot-state.yaml):
- Update `rotation.pillar.current_index` to the new index from step-01
- Update `rotation.pillar.last_date` to today
- Update `rotation.format.current_index` to the new index from step-01
- Update `rotation.format.last_date` to today
- Append to `history`:

```yaml
  - date: '{YYYY-MM-DD}'
    pillar: {pillar}
    format: {format}
    template: {template}
    topic: '{1-line}'
    topic_source: {source}
    youtube_video_id: {id or null}
    cta_type: {type}
    linkedin_draft: '{YYYY-MM-DD}-linkedin.md'
    x_draft: '{YYYY-MM-DD}-x.md'
    quality_score: '{summary}'
    status: draft
```

### 6. Completion Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Content Autopilot — Run Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pillar:    {pillar}
Format:    {format}
Topic:     {1-line topic}
Source:    {topic_source}

Drafts saved:
  → {draftQueue}/YYYY-MM-DD-linkedin.md
  → {draftQueue}/YYYY-MM-DD-x.md

Scheduled for:
  LinkedIn: {scheduled_time AEST}
  X:        {scheduled_time AEST}

Quality: {LinkedIn score} | {X score}
{If quality_note: "⚠ {quality_note}"}

Run /content:6-autopilot [RQ] to review and approve.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
