---
name: schedule-publish
description: Format and schedule content for publication via Late.dev across social platforms
menu-code: SP
---

# [SP] Schedule and Publish

## Purpose

Take approved content and schedule it for publication across target social platforms using the Late.dev API. Handles API verification, calendar conflict checking, platform-specific formatting, scheduling, and record keeping.

## Role Context

You are a content distribution specialist scheduling approved content for publication. You bring expertise in platform formatting, scheduling logistics, and calendar management.

## Prerequisites

Load:
- Platform specs from `{project-root}/content-plugin/skills/5-publisher/workflows/schedule-publish/data/platform-specs.md`
- Posting schedule guide from `{project-root}/content-plugin/skills/5-publisher/workflows/schedule-publish/data/posting-schedule-guide.md`

---

## Phase 1: API Verification

### 1.1 Check Late.dev API Key

Verify `LATE_API_KEY` is set in environment. If missing, halt.

### 1.2 Verify Account Health

```bash
curl -s "https://getlate.dev/api/v1/accounts/health" -H "Authorization: Bearer $LATE_API_KEY"
```

Report account status. Flag any disconnected or expired accounts.

### 1.3 List Available Accounts

```bash
curl -s "https://getlate.dev/api/v1/accounts" -H "Authorization: Bearer $LATE_API_KEY"
```

Present available accounts: platform, name, accountId.

---

## Phase 2: Content Selection

"**What content are we scheduling?**

Options:
- Provide a file path to the content
- Name the project and content type (I'll find it)
- Paste the content directly

**Your content:**"

Load and confirm the content.

## Phase 3: Calendar Conflict Check

Load content-calendar.yaml. Check for:
- Same platform + similar content within 7 days
- Lead magnet keyword conflicts
- Time slot collisions (within 2 hours on same platform)

Report any conflicts. Allow user to override or adjust timing.

## Phase 4: Platform Formatting

For each target platform, format the content:

**LinkedIn:**
- Character limit: 3,000
- Hashtags: 3-5
- Document/carousel: upload via presigned URL
- First comment: inside platformSpecificData

**X/Twitter:**
- Single: 280 characters
- Thread: plan tweet breaks
- Media: image or video attachment

**Instagram:**
- Caption: 2,200 characters max
- Carousel: PDF or multi-image
- Reels: video + caption

**TikTok:**
- Caption: 2,200 characters
- Video: via presigned URL upload
- No custom thumbnail support

**YouTube:**
- Title in platformSpecificData
- First comment for captions/CTAs
- Thumbnail on mediaItems entry

Present formatted preview for each platform. Wait for approval.

## Phase 5: Media Upload

For any content with media:
1. Check file size
2. Under 4MB: use `POST /media` multipart upload
3. Over 4MB: use `POST /media/presign` presigned URL flow
4. Store public URLs for post creation

## Phase 6: Schedule

For each platform:
```bash
curl -X POST "https://getlate.dev/api/v1/posts" \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "{formatted_content}",
    "platforms": [{
      "platform": "{platform}",
      "accountId": "{account_id}",
      "platformSpecificData": { ... }
    }],
    "scheduledFor": "{iso_datetime}",
    "mediaItems": [{...}],
    "title": "{internal_title}"
  }'
```

Report per-platform results: post ID, scheduled time, status.

## Phase 7: Record Keeping

1. Update content-calendar.yaml with new entries
2. Update publisher memory with scheduling details
3. Present confirmation summary

"**Scheduling Complete:**

| Platform | Status | Post ID | Scheduled For |
|----------|--------|---------|---------------|
| {platform} | {status} | {id} | {datetime} |

**Content Calendar updated.**"

---

## Key API Rules

- `firstComment` goes INSIDE `platformSpecificData`, NOT at root level
- Published posts CANNOT be deleted — only draft/scheduled
- PUT updates revert posts to "draft" — delete and recreate instead
- Media presigned URL: `POST /media/presign` (not GET, not /presigned-url)
- Field name for multipart upload: `files` (not file, media, or upload)
- LinkedIn rejects duplicate content with 422

---

## Success Criteria

- API verified and accounts healthy
- Calendar conflicts checked before scheduling
- Content formatted per platform specs
- Media uploaded via correct flow (multipart vs presigned)
- Posts created with correct platform-specific data
- Calendar updated with new entries
- Memory updated with scheduling details
