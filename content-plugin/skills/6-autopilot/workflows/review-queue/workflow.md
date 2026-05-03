---
name: review-queue
description: Review, approve, edit, reject, or regenerate drafts from the autopilot queue — handles LinkedIn/X posts and Instagram/TikTok carousels
draftQueue: '{project-root}/content-plugin/data/draft-queue/'
contentCalendar: '{project-root}/content/calendar/content-calendar.yaml'
platformSpecs: '{project-root}/content-plugin/skills/5-publisher/workflows/schedule-publish/data/platform-specs.md'
schedulingConfig: '{project-root}/references/scheduling-config.md'
---

# Review Queue Workflow

## Step 1: Load Queue

Read all `.md` files from `{draftQueue}` where frontmatter `status: draft`.

Sort by date ascending (oldest drafts first).

Group by draft type:
- **Post drafts**: `platform: linkedin` or `platform: x` (present as pairs)
- **Carousel drafts**: `platform: instagram` or `platform: tiktok` with `type: carousel` (present as pairs sharing the same `slides_dir`)

If no drafts found:
```
No drafts in queue.
Run /content:6-autopilot [LX] to generate LinkedIn + X content.
Run /content:6-autopilot [IC] to generate an Instagram carousel.
```

## Step 2: Present Drafts

### LinkedIn + X Post Pairs

For each LinkedIn + X pair for the same date, present:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DRAFT — {date}
Pillar: {pillar} | Format: {format} | Template: {template}
CTA: {cta_type} {if keyword: "— [{keyword}]"} {if resource-giveaway: "— {first_comment URL}"}
Source: {topic_source} {if youtube_repurpose: "— {youtube_video_id}"}
Quality: {quality_score} {if quality_note: "⚠ {quality_note}"}
Scheduled for: LinkedIn {time} | X {time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LINKEDIN ({char_count} chars)
{post body}

{if first_comment: "── First comment ──\n{first_comment}"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

X ({format})
{post body}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[A] Approve both    [AL] LinkedIn only    [AX] X only
[E] Edit            [R] Reject            [S] Swap (regenerate same pillar/format)
```

Wait for input.

## Step 3: Handle Actions

### [A] Approve both / [AL] LinkedIn only / [AX] X only

For each approved platform:

1. Load platform specs from `{platformSpecs}`
2. Load Buffer channel IDs from `{schedulingConfig}`
3. Call the Buffer MCP to schedule each post:

**LinkedIn:**
```
mcp__buffer__use_buffer_api(
  action: "createPost",
  channelIds: [linkedin_channel_id],
  text: "{full post body}",
  scheduledAt: "{scheduledTime ISO8601}",
  media: ["{media_path}"]  # omit if no media
)
```

If `first_comment` is set, include it as the first comment option in the Buffer call.

**X:**
```
mcp__buffer__use_buffer_api(
  action: "createPost",
  channelIds: [x_channel_id],
  text: "{full X post body}",
  scheduledAt: "{scheduledTime ISO8601}"
)
```

4. On success: capture `postId` from the Buffer response
5. Update draft file frontmatter: `status: scheduled`, `buffer_post_id: {postId}`
6. Update `{contentCalendar}` entry: `status: scheduled`
7. Confirm:
```
Scheduled.
  LinkedIn: {scheduledTime AEST} (Buffer ID: {postId})
  X: {scheduledTime AEST} (Buffer ID: {postId})
```

### [E] Edit

Present both drafts for editing. User makes changes directly.

After editing:
- Re-run quality gate checks from step-07 (inline, not full workflow)
- Show updated quality scores
- Present [A] Approve or [R] Reject

### [R] Reject

```
Rejected. Reason? (optional — press Enter to skip)
```

Update draft frontmatter: `status: skipped`, `rejection_reason: {reason}`
Update calendar entry: `status: cancelled`

### [S] Swap (Regenerate)

Re-run the [LX] workflow steps 04-08 with the same pillar, format, and today's date. New topic/angle/drafts replace the existing ones.

Confirm: "Regenerating with same pillar ({pillar}) and format ({format})..."

---

### Instagram + TikTok Carousel Pairs

For each Instagram + TikTok pair (same `slides_dir`), present:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CAROUSEL DRAFT — {date}
Angle: {topic_angle} | Slides: {slide_count} | CTA: Comment {cta_keyword}
Topic: {topic}
Source: {source_url}
Quality: {quality_score} {if quality_note: "⚠ {quality_note}"}
Slides: {slides_dir}
Scheduled for: Instagram {time} | TikTok {time} (manual)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTAGRAM CAPTION ({char_count} chars)
{caption body}

{if first_comment: "── First comment ──\n{first_comment}"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIKTOK CAPTION
{caption body}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[A] Approve Instagram     [AT] TikTok only (manual)    [AB] Approve both
[E] Edit captions         [R] Reject                   [S] Swap (regenerate)
[V] View slides           (opens slides_dir in Finder/path)
```

Wait for input.

#### [A] Approve Instagram / [AB] Approve both

For Instagram:

1. Load Buffer channel IDs from `{schedulingConfig}`
2. Call the Buffer MCP with all carousel slide paths:

```
mcp__buffer__use_buffer_api(
  action: "createPost",
  channelIds: [instagram_channel_id],
  text: "{instagram caption}",
  scheduledAt: "{scheduledTime ISO8601}",
  media: [
    "{slides_dir}/slide-01.png",
    "{slides_dir}/slide-02.png",
    ...
  ]
)
```

If `first_comment` is set, include it as first comment option.

3. On success: capture `postId`
4. Update Instagram draft frontmatter: `status: scheduled`, `buffer_post_id: {postId}`
5. Update calendar entry: `status: scheduled`

Confirm:
```
Instagram carousel scheduled.
  Slides: {slide_count}
  Time: {scheduledTime AEST}
  Post ID: {postId}
```

#### [AT] TikTok only (manual upload)

TikTok scheduling via API is not available in v1. Mark the TikTok draft as ready for manual upload:

Update TikTok draft frontmatter: `status: ready-for-upload`

```
TikTok draft marked for manual upload.
  Slides dir: {slides_dir}
  Caption saved to draft file — copy and paste when uploading.
```

#### [AB] Approve both

Run [A] Instagram approval above, then [AT] TikTok marking.

#### [E] Edit captions

Present both captions for editing. User makes changes directly.

After editing:
- Re-run caption quality checks (voice, hook, CTA compliance)
- Show updated quality scores
- Present [A] / [AB] / [R] options

#### [R] Reject carousel

Update both carousel draft files: `status: skipped`
Update both calendar entries: `status: cancelled`

#### [S] Swap (Regenerate carousel)

Re-run the [IC] workflow steps 05-09 with the same topic_angle to generate a fresh carousel on a different trending topic.

Confirm: "Regenerating carousel with same angle ({topic_angle})..."

#### [V] View slides

Output the absolute path to `slides_dir` so the creator can open it directly:
```
Slides location: {slides_dir}
  {slide_count} files: slide-01.png ... slide-{N:02d}.png
```

---

## Step 4: After All Drafts Reviewed

```
Queue clear. {N} approved, {M} rejected.
Next LX run: {next scheduled or 'run /content:6-autopilot [LX]'}
Next IC run: {next scheduled or 'run /content:6-autopilot [IC]'}
```
