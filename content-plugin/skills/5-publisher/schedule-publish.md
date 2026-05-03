---
name: schedule-publish
description: Format and schedule content for publication via Buffer across social platforms
menu-code: SP
---

# [SP] Schedule and Publish

## Purpose

Take approved content and schedule it for publication across target social platforms using the Buffer MCP. Handles channel verification, calendar conflict checking, platform-specific formatting, scheduling, and record keeping.

## Role Context

You are a content distribution specialist scheduling approved content for publication. You bring expertise in platform formatting, scheduling logistics, and calendar management.

## Prerequisites

Load:
- Platform specs from `{project-root}/content-plugin/skills/5-publisher/workflows/schedule-publish/data/platform-specs.md`
- Posting schedule guide from `{project-root}/content-plugin/skills/5-publisher/workflows/schedule-publish/data/posting-schedule-guide.md`

---

## Phase 1: Channel Verification

### 1.1 Verify Buffer MCP Connection

The Buffer MCP is connected at the platform level — no API key is required. Proceed directly to listing channels. If the MCP call fails, halt and ask the user to check their Claude Code MCP configuration.

### 1.2 List Available Channels

Use the Buffer MCP to retrieve connected social accounts:

```
mcp__buffer__use_buffer_api(action: "listChannels")
```

Present available channels: platform, name, channel ID.

Report any disconnected or missing channels.

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

For each target platform, format the content per the specs in platform-specs.md:

**LinkedIn:** 3,000 chars max. 3-5 hashtags. External links in first comment.

**X/Twitter:** 280 chars (free) / 25,000 chars (X Premium). Use threads for longer content.

**Instagram:** 2,200 chars. First comment for hashtags. 4:5 portrait ratio preferred.

**TikTok:** 2,200 chars caption. Privacy settings required. No text-only posts.

**Facebook:** 63,206 chars. Pages only.

**Pinterest:** 500 chars description. Board ID required. Link field essential.

**Threads:** 500 chars max — hard limit.

**Bluesky:** 300 chars max — hard limit.

Present formatted preview for each platform. Wait for approval.

## Phase 5: Media Upload

Buffer MCP handles media attachment during post creation. Pass media file paths to the MCP tool. For large files, check Buffer's size limits per platform before calling the tool.

## Phase 6: Schedule

For each platform, use the Buffer MCP:

```
mcp__buffer__use_buffer_api(
  action: "createPost",
  profileIds: [channel_id_for_platform],
  text: formatted_content_for_platform,
  scheduledAt: iso_datetime_utc,
  media: [file paths if applicable]
)
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

## Key Platform Rules

- LinkedIn first comment goes in `platformSpecificData` (verify Buffer MCP supports this)
- TikTok requires privacy_level, content_preview_confirmed, express_consent_given
- Pinterest requires boardId on every pin
- Bluesky: 300 chars is a hard limit — ruthlessly concise
- Threads: 500 chars — the #1 cause of failures on this platform
- Buffer supports: Facebook, Instagram, LinkedIn, TikTok, X, Pinterest, Threads, YouTube, Bluesky, Mastodon

---

## Success Criteria

- Channels verified via Buffer MCP
- Calendar conflicts checked before scheduling
- Content formatted per platform specs
- Posts created via Buffer MCP with platform-specific data
- Calendar updated with new entries
- Memory updated with scheduling details
