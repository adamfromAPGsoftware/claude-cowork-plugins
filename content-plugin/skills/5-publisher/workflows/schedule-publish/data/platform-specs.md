# Platform-Specific Formatting Specs

**Purpose:** Reference data for formatting content per social platform before scheduling via Buffer MCP.
**Source:** Buffer API documentation (https://buffer.com/developers/api)
**Last verified:** 2026-04-30

---

## Buffer MCP Overview

### Authentication
Platform-level MCP — no API key or `.env` entry needed. Connected in Claude Code settings.

### Key MCP Tools

| Tool | Description |
|------|-------------|
| `mcp__buffer__use_buffer_api` | Generic action gateway — list channels, create/update/delete posts |
| `mcp__buffer__buffer_api_help` | Returns Buffer API documentation and available action schemas |

Call `mcp__buffer__buffer_api_help` first to discover exact action names and payload schemas.

### Common Action Examples

| Action | Description |
|--------|-------------|
| `listChannels` | List connected social accounts with platform and channel ID |
| `createPost` | Create and schedule a post across one or more channels |
| `listSentPosts` | List published posts |
| `listScheduledPosts` | List upcoming scheduled posts |

### Key Parameters for Post Creation

| Parameter | Description |
|-----------|-------------|
| `profileIds` | Array of channel IDs to post to |
| `text` | Post body text |
| `scheduledAt` | ISO 8601 UTC datetime for scheduling |
| `media` | Media attachments (images, videos) |
| `retweet` | (X only) retweet existing post |

### Supported Platforms
Facebook, Instagram, LinkedIn, TikTok, X (Twitter), Pinterest, Threads, YouTube, Bluesky, Mastodon

### Important Constraints
- Buffer does not support Reddit — exclude from cross-posting plans
- Some platform-specific features (first comments, TikTok privacy settings) — verify current Buffer MCP tool schema
- LinkedIn rejects duplicate content — always vary text across platforms

---

## LinkedIn

| Spec | Value |
|------|-------|
| Platform key | `linkedin` |
| Max post length | 3,000 characters |
| Visible before fold | First ~210 characters (before "see more") |
| Post types | Text, single image, multi-image carousel (up to 20), video, document/carousel (PDF, PPT, DOC) |
| Image specs | Up to 8 MB per file, 552x276 min, 8192x8192 max, 1200x627 recommended |
| Video specs | Up to 5 GB, 10 min (personal) / 30 min (company pages), aspect ratio 1:2.4 to 2.4:1 |
| Document specs | PDF, PPT, PPTX, DOC, DOCX — max 100 MB, 300 pages |
| First comment | **YES** — put `firstComment` inside `platformSpecificData` (NOT at root level). Best practice: put external links in first comment (LinkedIn suppresses posts with links by ~40-50%) |
| Account type | Organisation accounts only |
| Hashtags | 3-5 per post, placed at end |
| Link handling | Put external links in `firstComment` to avoid algorithm suppression |
| Duplicate detection | LinkedIn rejects identical text with 422 error regardless of timing |

**Buffer MCP post options:**
- `documentTitle` — required for document posts (falls back to filename)
- `firstComment` — auto-posted as first comment after publish (VERIFIED WORKING — must be here, not root level)
- `organizationUrn` — for multi-org posting (`urn:li:organization:123456`)

**Best practices:**
- Hook in first 2 lines (before "see more" fold at ~210 chars)
- External links go in first comment, not post body
- Use whitespace for readability
- CTA at end

---

## X (Twitter)

| Spec | Value |
|------|-------|
| Platform key | `twitter` |
| Max post length | **25,000 characters (X Premium)** |
| URL handling | URLs consume 23 characters regardless of actual length |
| Emoji handling | Each emoji counts as 2 characters |
| Post types | Text, images (up to 4), video (1), GIF (1, uses all 4 image slots), threads |
| Image specs | JPEG, PNG, WebP, GIF — min 4x4, max 8192x8192, recommended 1200x675 (16:9) |
| Video specs | MP4/MOV, max 512 MB, max 140 seconds, recommended 1280x720 at 30fps H.264 |
| GIF specs | Max 15 MB, max 1280x1080 |
| First comment | No |
| Threads | Via `platformSpecificData.threadItems` — each item becomes a reply with its own content and media |
| Duplicate detection | Twitter rejects duplicate tweets, even minor variations |

**Best practices:**
- Front-load key message within 280 chars
- Use threads (`threadItems`) for longer content
- 1-2 hashtags max, integrated into text
- Plain text only — no markdown or formatting

---

## Instagram

| Spec | Value |
|------|-------|
| Platform key | `instagram` |
| Max caption length | 2,200 characters |
| Visible before fold | First 125 characters |
| Post types | Feed (image/video), carousels (up to 10 items), stories, reels |
| Image specs | JPEG, PNG — max 8 MB (auto-compressed), recommended 1080x1350 (feed), 1080x1920 (stories) |
| Video — feed | Max 300 MB, 60 min duration |
| Video — reels | Max 300 MB, 90 seconds, must be vertical 9:16 |
| Video — stories | Max 100 MB, 60 seconds |
| Video codec | H.264, 30fps |
| Carousel rules | All items should share same aspect ratio — first item determines ratio for entire carousel |
| First comment | **YES** — use `firstComment` parameter. Essential because captions don't have clickable links |
| Account type | Business or Creator account required (personal accounts cannot post via API) |
| Rate limit | 100 posts per 24-hour rolling window (all content types combined) |
| Stories limitation | Text captions not displayed; link stickers not available via API |

**Buffer MCP post options:**
- `contentType` — `"story"` or `"reels"`
- `collaborators` — up to 3 usernames for co-authoring (Business/Creator only)
- `userTags` — tag users with coordinates (0.0–1.0 range)
- `instagramThumbnail` — custom Reel thumbnail (1080x1920 recommended)
- `thumbOffset` — millisecond offset for auto-generated thumbnail
- `shareToFeed` — control Reel visibility in main feed

**Best practices:**
- Strong first line (only 125 chars visible before fold)
- Hashtags in first comment via `firstComment` parameter
- 5-10 relevant hashtags
- Portrait 4:5 orientation for best feed engagement
- CTA in caption

---

## Facebook

| Spec | Value |
|------|-------|
| Platform key | `facebook` |
| Max post length | 63,206 characters |
| Visible before fold | ~480 characters (before "See more") |
| Post types | Feed (text/image/video/multi-image up to 10), stories (24hr), reels |
| Image specs | JPEG, PNG, GIF (WebP auto-converted) — max 4 MB, recommended 1200x630 |
| Video — feed | MP4, MOV — max 4 GB, 240 min |
| Video — stories | MP4, MOV — 120 seconds max |
| First comment | **YES** — use `firstComment` parameter. Does NOT work with Stories or Reels |
| Account type | Pages only — cannot post to personal profiles or Groups |
| Multi-page | Single account can manage multiple Pages via `pageId` parameter |

**Buffer MCP post options:**
- `contentType` — `"story"` or `"reel"`
- `title` — Reel title (separate from caption)
- `firstComment` — auto-posted comment text
- `pageId` — target specific Page

**Best practices:**
- Short and engaging (40-80 chars for best engagement)
- Questions drive interaction
- 1-2 hashtags max, optional
- Interactive story stickers not supported via API

---

## YouTube

| Spec | Value |
|------|-------|
| Platform key | `youtube` |
| Title max | 100 characters |
| Description max | 5,000 characters |
| Tags | 500 characters total |
| Video types | Regular (long-form, 16:9) and Shorts (vertical 9:16, ≤3 min — auto-detected) |
| Video formats | MP4, MOV, AVI, WMV, FLV, 3GP, WebM — max 256 GB |
| Video duration | 15 min (unverified channels), 12 hours (verified) |
| Thumbnails | JPEG, PNG, GIF — max 2 MB, recommended 1280x720 (regular videos only, not Shorts) |
| First comment | **YES** — max 10,000 characters. Immediate posts: posts right away. Scheduled: posts when video goes live |
| Privacy settings | `public`, `private`, `unlisted` — scheduled videos upload as private, change at scheduled time |

**Buffer MCP post options:**
- `madeForKids` — COPPA flag (permanently disables comments, notification bells, personalized ads)
- `categoryId` — video categorisation
- `containsSyntheticMedia` — AI-generated content disclosure

**Best practices:**
- Keywords in first 2-3 lines of description
- Timestamps in description
- Links below the fold
- Shorts: vertical 9:16, ≤3 min, auto-detected by YouTube

---

## TikTok

| Spec | Value |
|------|-------|
| Platform key | `tiktok` |
| Video caption | 2,200 characters — `content` field is the ONLY text field for videos (no separate title) |
| Photo carousel title | 90 characters (auto-truncated, hashtags stripped) — maps from `content` field |
| Photo carousel description | 4,000 characters — set via `description` in `tiktokSettings` (long-form text for carousels only) |
| Post types | Video (3 sec to 10 min), photo carousel (up to 35 images) |
| Video specs | MP4, MOV, WebM — max 4 GB, recommended 1080x1920 (9:16), H.264 at 30fps |
| Photo specs | JPEG, PNG, WebP — max 20 MB per image, auto-resized to 1080x1920 |
| First comment | No |
| Text-only posts | **Not supported** — media is mandatory |
| Comments | Write-only — cannot read comments via API |

**IMPORTANT — Video vs Photo content field mapping:**
- **Video posts:** `content` = the full caption (max 2,200 chars). There is NO separate title field for TikTok video posts. Structure the caption with CTA first line, then description, then hashtags — all in one field.
- **Photo carousel posts:** `content` = the title (auto-truncated to 90 chars, hashtags stripped). Use `description` in `tiktokSettings` for the full caption (max 4,000 chars). Split content strategically: punchy hook in title, detail + CTA + hashtags in description.

**Buffer MCP post options (several REQUIRED):**
- `privacy_level` — REQUIRED: `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`
- `allow_comment` — REQUIRED: enable/disable comments
- `allow_duet` / `allow_stitch` — REQUIRED for video posts
- `content_preview_confirmed` — REQUIRED: must be `true`
- `express_consent_given` — REQUIRED: must be `true`
- `video_cover_timestamp_ms` — thumbnail position (integer, milliseconds)
- `description` — long-form description for photo carousel posts only (max 4,000 chars)
- `media_type` — `"photo"` for carousels (defaults based on media items)
- `photo_cover_index` — cover image selection (0-based)
- `auto_add_music` — for photo carousels only
- `video_made_with_ai` — AI disclosure flag

**Best practices:**
- Hook in first 3 seconds
- 9:16 vertical orientation mandatory
- 3-5 hashtags, trending + niche mix
- Content moderation is stricter via API than native app
- For videos: front-load the CTA keyword in the caption since there's no separate title

---

## Pinterest

| Spec | Value |
|------|-------|
| Platform key | `pinterest` |
| Title max | 100 characters |
| Description max | 500 characters |
| Post types | Image pin (1 image), video pin (1 video) |
| Image specs | JPEG, PNG, WebP, GIF — max 32 MB, recommended 1000x1500 (2:3), min 100x100 |
| Video specs | MP4, MOV — max 2 GB, 4 sec to 15 min, recommended 1080p at 25+ fps, aspect ratios 2:3, 1:1, or 9:16 |
| First comment | No |
| Board | **REQUIRED** — every pin must have a `boardId` |
| Link | `link` field — destination URL when users click pin. Most important field for driving traffic |
| Text-only pins | **Not supported** — media is mandatory |
| No carousels | Multi-image posts not supported |

**Buffer MCP post options:**
- `boardId` — REQUIRED. Fetch available boards via the Buffer MCP or your Buffer dashboard to find the correct board ID
- `title` — searchable pin title (max 100 chars, defaults to first line of content)
- `link` — destination HTTPS URL
- `coverImageUrl` — custom cover for video pins
- `coverImageKeyFrameTime` — auto-extract frame at N seconds

**Best practices:**
- Keyword-rich description for search discoverability
- Vertical 2:3 images for optimal feed display
- Always include destination link
- Clear text overlay on images

---

## Reddit

| Spec | Value |
|------|-------|
| Platform key | `reddit` |
| Title max | 300 characters (REQUIRED, cannot edit after posting) |
| Body max | 40,000 characters (Markdown supported) |
| Post types | Text, link, image (1), gallery (multiple images — not all subreddits support) |
| Image specs | JPEG, PNG, GIF — max 20 MB, recommended 1200x628 |
| Video | **Not supported** via API (Reddit platform restriction) |
| First comment | No |
| Subreddit | Via `platformSpecificData.subreddit` (without `r/` prefix). REQUIRED — posting fails without one |
| Flair | Many subreddits require flair — check subreddit rules and provide the correct flair ID |
| Failure rate | High — mostly preventable by checking subreddit rules before posting |

**Best practices:**
- Check subreddit rules before posting
- Title is permanent — cannot be edited
- New accounts face karma/age restrictions
- Markdown formatting supported in body

---

## Threads

| Spec | Value |
|------|-------|
| Platform key | `threads` |
| Max post length | **500 characters** — #1 cause of failures. Content from LinkedIn (3,000), Facebook (63,206), Instagram (2,200) MUST be shortened |
| Post types | Text (no media required), single image, single video (up to 5 min, 1 GB), carousels (up to 10 images), thread sequences |
| Image specs | JPEG, PNG, WebP, GIF — max 8 MB (auto-compressed), recommended 1080x1350 (4:5), aspect ratios 4:5, 1:1, 16:9 |
| Video specs | MP4, MOV — max 1 GB, 5 min, H.264 30fps 1080p, AAC 128kbps audio |
| First comment | No |
| Rate limit | 250 API-published posts per 24-hour window |
| Account requirement | Instagram Business/Creator account with Threads enabled |
| Comments | Reply-only — cannot post new top-level comments |

**Best practices:**
- Keep under 500 characters — this is critical
- Text-only posts are valid (no media required)
- No polls, no post editing, no quote posts

---

## Bluesky

| Spec | Value |
|------|-------|
| Platform key | `bluesky` |
| Max post length | **300 characters** — HARD limit. #1 cause of 95% of all Bluesky failures |
| Post types | Text, images (up to 4), video (1), threads |
| Image specs | JPEG, PNG, WebP, GIF — max 1 MB per image (strict), recommended 1200x675 (16:9), alt text up to 1,000 chars |
| Video specs | MP4 only — max 50 MB, max 60 seconds, recommended 1280x720 at 30fps H.264 |
| First comment | No |
| Authentication | App passwords (not OAuth) — handle + app password (`xxxx-xxxx-xxxx-xxxx`) |
| Threads | Via `threadItems` — each item has separate 300-char limit |
| Analytics | Limited — likes, comments, reposts only (no impressions, reach, clicks, views) |

**Best practices:**
- Ruthlessly concise — 300 chars is very tight
- Use threads for longer content
- Include alt text on images (up to 1,000 chars per image)

---

## Google Business

| Spec | Value |
|------|-------|
| Platform key | `google-business` |
| Max post length | 1,500 characters |
| Post types | Text + image (recommended), text-only (lower visibility), posts with CTA buttons |
| Image specs | JPEG, PNG (WebP auto-converted) — max 5 MB, min 400x300, recommended 1200x900 (4:3) |
| Video | **Not supported** |
| CTA buttons | `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL` |
| First comment | No |
| Multi-location | Supported for businesses with multiple locations |
| No comments | Posts do not support comments |

**Best practices:**
- Always include an image (text-only has lower visibility)
- Use CTA buttons for actionable posts
- Location-based — content should be relevant to the business profile

---

## Telegram

| Spec | Value |
|------|-------|
| Platform key | `telegram` |
| Text max | 4,096 characters |
| Caption max | 1,024 characters |
| Post types | Text, photo, video, document (any file type), media albums (up to 10 mixed items) |
| Image specs | JPEG, PNG, GIF, WebP — max 10 MB (auto-compressed) |
| Video specs | MP4, MOV — max 50 MB (auto-compressed) |
| First comment | No |
| Bot setup | Requires a Buffer-managed bot added as admin to channel/group — check Buffer dashboard for setup instructions |
| Formatting | HTML, Markdown, or MarkdownV2 supported |

**Buffer MCP post options:**
- `disableNotification` — silent message delivery
- `disableWebPagePreview` — suppress link previews
- `protectContent` — content protection

**Best practices:**
- Ensure the Buffer bot is added as admin before posting
- Channel posts appear under channel name; group posts appear under the bot's name

---

## Snapchat

| Spec | Value |
|------|-------|
| Platform key | `snapchat` |
| Post types | Story (24hr, no caption), Saved Story (permanent, title max 45 chars), Spotlight (video only, description max 160 chars with hashtags) |
| Image specs | JPEG, PNG — max 20 MB, recommended 1080x1920 (9:16) |
| Video specs | MP4 only — max 500 MB, 5-60 seconds, min 540x960, recommended 1080x1920 (9:16) |
| First comment | No |
| Text-only | **Not supported** — media is mandatory |
| One media item only | No carousels or multi-media |
| Account requirement | Public Profile required |

**Best practices:**
- 9:16 vertical orientation required
- Keep video 5-60 seconds
- No text-only posts — always include media

---

## First Comment Support Summary

| Platform | First Comment | Notes |
|----------|:------------:|-------|
| LinkedIn | **YES** | Put external links here (avoids ~40-50% reach suppression) |
| Instagram | **YES** | Essential — captions don't have clickable links. Use for hashtags |
| Facebook | **YES** | Does NOT work with Stories or Reels |
| YouTube | **YES** | Max 10,000 chars. Scheduled: posts when video goes live |
| X (Twitter) | No | Use threads instead |
| TikTok | No | |
| Pinterest | No | |
| Reddit | No | |
| Threads | No | |
| Bluesky | No | |
| Google Business | No | |
| Telegram | No | |
| Snapchat | No | |

---

## Critical Character Limits (Failure Prevention)

When cross-posting, always check these limits — the #1 cause of API failures:

| Platform | Limit | Risk Level |
|----------|-------|:----------:|
| Bluesky | 300 chars | **CRITICAL** |
| X (Twitter) | 280 chars (free) | **CRITICAL** |
| Threads | 500 chars | **HIGH** |
| Snapchat — Saved Story title | 45 chars | HIGH |
| TikTok — carousel title | 90 chars | MEDIUM |
| Pinterest — title | 100 chars | MEDIUM |
| YouTube — title | 100 chars | MEDIUM |
| Reddit — title | 300 chars | MEDIUM |
| Telegram — caption | 1,024 chars | LOW |
| Google Business | 1,500 chars | LOW |
| Instagram | 2,200 chars | LOW |
| TikTok — caption | 2,200 chars | LOW |
| LinkedIn | 3,000 chars | LOW |
| Telegram — text | 4,096 chars | LOW |
| Facebook | 63,206 chars | LOW |

---

## General Formatting Rules

1. **Never post raw/unformatted content** — every platform gets native-feeling output
2. **Per-platform formatting** — use separate `mcp__buffer__use_buffer_api(action: "createPost")` calls for each platform, each with its own formatted content
3. **Respect character limits** — truncate or rework content per platform. Cross-posting without adaptation is the #1 cause of failures
4. **Use `firstComment`** — LinkedIn (links), Instagram (hashtags), Facebook, YouTube. Pass first comment text via Buffer MCP `create_post` first comment option.
5. **Adapt tone per platform** — LinkedIn (professional), X (concise/punchy), Instagram (visual-first), Facebook (conversational), Reddit (community-native)
6. **Handle media per platform** — each platform has different format, size, and count limits
7. **Check platform-specific required fields** — TikTok requires `privacy_level`, `content_preview_confirmed`, `express_consent_given`; Pinterest requires `boardId`; Reddit requires `subreddit`
8. **Duplicate detection** — LinkedIn and Twitter reject duplicate content. Always vary text across platforms

---

## Thumbnail Attachment Reference

Custom thumbnails for short-form video content (Reels, Shorts, TikTok). Generated thumbnails are found at:
`{project_folder}/creative-director/short-form/{video-title-slug}/sf-{NN}.png`

| Platform | Supports Custom Thumbnail? | Notes |
|----------|:--------------------------:|-------|
| **Instagram Reels** | YES | Attach thumbnail alongside video in Buffer MCP media array |
| **TikTok** | NO (frame select only) | Set `video_cover_timestamp_ms` if Buffer MCP supports it; otherwise TikTok auto-generates |
| **YouTube** | YES | Include thumbnail URL alongside video in Buffer MCP media array |

**YouTube first comment:** Always prepare a first comment for YouTube posts (where Buffer MCP supports it). Use for lead magnet CTAs and links. YouTube first comments should drive to the free community — e.g. "Free resources on this inside my free community → {YOUR_COMMUNITY_URL}". Never use "Comment X" keyword CTAs on YouTube — those only work on Instagram/TikTok via ManyChat.
