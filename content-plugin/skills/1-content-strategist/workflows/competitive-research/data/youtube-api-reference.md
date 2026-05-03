# YouTube MCP — Quick Reference

**Purpose:** Correct MCP tool usage for the competitive research workflow. All tools use the platform-level YouTube MCP — no API key or env var needed.

---

## Tools Used by This Workflow

### 1. `mcp__youtube__getChannelStatistics` — Fetch Channel Statistics

**Use:** Get subscriber count, total views, total videos for a channel.

**Parameters:**
- `channelIds` — array of YouTube channel IDs (e.g., `["UCbo-KbSjJDG6JWQ_MTZ_rNA"]`)

**Returns per channel:**
- `statistics.subscriberCount`
- `statistics.viewCount`
- `statistics.videoCount`
- `snippet.title`

---

### 2. `mcp__youtube__searchVideos` — Search for Videos

**Use:** Search YouTube for videos matching a query.

**Parameters:**
- `query` — search term (e.g., `"AI agents tutorial"`)
- `maxResults` — number of results (optional)

**Note:** Returns snippet data. To get view counts, take the video IDs and call `mcp__youtube__getVideoDetails`.

**Tip:** Prefer `mcp__youtube__getChannelTopVideos` + `mcp__youtube__getVideoDetails` when scanning a known channel — fewer calls, same data.

---

### 3. `mcp__youtube__getVideoDetails` — Fetch Video Statistics

**Use:** Get view count, like count, comment count, duration for specific videos. Batch up to 50 IDs.

**Parameters:**
- `videoIds` — array of video IDs (e.g., `["dQw4w9WgXcQ", "jNQXAC9IVRw"]`)

**Returns per video:**
- `statistics.viewCount`
- `statistics.likeCount`
- `statistics.commentCount`
- `contentDetails.duration`
- `snippet.publishedAt`
- `snippet.title`
- `snippet.channelId`

---

### 4. `mcp__youtube__getChannelTopVideos` — Fetch Top Videos from a Channel

**Use:** Get the most-viewed videos from a specific channel (by view count).

**Parameters:**
- `channelId` — channel ID
- `maxResults` — number of videos (optional)

**Returns:** Array of video IDs and stats for the channel's top-performing videos.

---

### 5. `mcp__youtube__getTranscripts` — Fetch Video Transcripts

**Use:** Get transcripts from YouTube videos. No API quota used.

**Parameters:**
- `videoIds` — array of video IDs
- `lang` — (optional) language code, e.g., `"en"`

**Note:** Falls back to auto-generated captions if manual captions are unavailable. If unavailable, use the `youtube-transcript-api` Python library as a backup.

---

### 6. `mcp__youtube__getTrendingVideos` — Fetch Trending Videos

**Use:** Get currently trending videos by region and category.

**Parameters:**
- `regionCode` — (optional) ISO country code, e.g., `"US"`, `"AU"`
- `categoryId` — (optional) YouTube category ID (28 = Science & Technology)
- `maxResults` — (optional)

---

### 7. `mcp__youtube__getRelatedVideos` — Find Related Videos

**Use:** Find videos similar to a specific video — useful for competitor content discovery.

**Parameters:**
- `videoId` — single video ID
- `maxResults` — (optional)

---

### 8. `mcp__youtube__compareVideos` — Compare Video Performance

**Use:** Side-by-side comparison of video statistics — useful for benchmarking competitor content.

**Parameters:**
- `videoIds` — array of video IDs to compare

---

### 9. `mcp__youtube__getVideoEngagementRatio` — Engagement Analysis

**Use:** Calculate engagement ratio (views, likes, comments, calculated ratio) for multiple videos.

**Parameters:**
- `videoIds` — array of video IDs

---

## Niche-Wide Keyword Scanning Pattern

1. Call `mcp__youtube__searchVideos` with each seed keyword
2. Collect all video IDs, de-duplicate
3. Batch call `mcp__youtube__getVideoDetails` (50 IDs per call) for full stats
4. Call `mcp__youtube__getChannelStatistics` for subscriber counts of discovered channels
5. Score videos using absolute velocity thresholds

**Prefer channel-first scanning:** `mcp__youtube__getChannelTopVideos` + `mcp__youtube__getVideoDetails` is more efficient than search when analysing a known competitor channel.

---

## Exa Web Search — MCP Tool Reference

**Use:** Cross-platform trend intelligence — supplement YouTube data with web signals.

**Tool name:** `mcp__exa__web_search_exa`

**Usage pattern:**
```
mcp__exa__web_search_exa(query="{search query}", numResults=10)
```

Use for broad trend queries (e.g., "Claude Code trending", "AI agents news this week"). Exa is supplementary — gracefully degrade if unavailable.
