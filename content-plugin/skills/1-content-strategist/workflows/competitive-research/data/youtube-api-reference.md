# YouTube Data API v3 — Quick Reference

**Purpose:** Correct API call formats for the competitive research workflow. All endpoints use `YOUTUBE_API_KEY` loaded from `{project-root}/.env`.

**Base URL:** `https://www.googleapis.com/youtube/v3`

---

## Authentication

All requests append `&key={YOUTUBE_API_KEY}` as a query parameter. Do NOT use `source` to load the `.env` file — extract the key cleanly to avoid trailing whitespace/newline issues.

---

## Endpoints Used by This Workflow

### 1. channels.list — Fetch Channel Statistics

**Use:** Get subscriber count, total views, total videos for a channel.

```
GET /channels?part=snippet,statistics&id={CHANNEL_ID}&key={YOUTUBE_API_KEY}
```

**Common Mistake:** The filter parameter is `id`, NOT `channelId`. Using `channelId` will return a "No filter selected" error.

**Example:**
```bash
curl "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=UCbo-KbSjJDG6JWQ_MTZ_rNA&key=YOUR_KEY"
```

**Response fields of interest:**
- `items[0].statistics.subscriberCount`
- `items[0].statistics.viewCount`
- `items[0].statistics.videoCount`
- `items[0].snippet.title`

**To resolve a @handle to a channel ID:**
```
GET /channels?part=snippet,statistics&forHandle={HANDLE_WITHOUT_AT}&key={YOUTUBE_API_KEY}
```

---

### 2. search.list — Search for Videos

**Use:** Search YouTube for videos matching a query.

```
GET /search?part=snippet&q={QUERY}&type=video&maxResults={LIMIT}&key={YOUTUBE_API_KEY}
```

**Optional parameters:**
- `order=viewCount` — sort by views (useful for finding top performers)
- `order=date` — sort by upload date (useful for recency analysis)
- `publishedAfter={ISO_DATE}` — filter to videos after a date (e.g., `2026-01-01T00:00:00Z`)
- `channelId={CHANNEL_ID}` — restrict search to a specific channel
- `maxResults` — max 50 per request

**Note:** search.list returns snippet data only. To get view counts, likes, and comments, you must take the video IDs from search results and call `videos.list` (see below).

**Example:**
```bash
curl "https://www.googleapis.com/youtube/v3/search?part=snippet&q=AI+agents+tutorial&type=video&maxResults=25&key=YOUR_KEY"
```

---

### 3. videos.list — Fetch Video Statistics

**Use:** Get view count, like count, comment count, duration for specific videos.

```
GET /videos?part=snippet,statistics,contentDetails&id={VIDEO_ID_1},{VIDEO_ID_2},...&key={YOUTUBE_API_KEY}
```

**Batch up to 50 video IDs** in a single comma-separated request to minimise quota usage.

**Example:**
```bash
curl "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=dQw4w9WgXcQ,jNQXAC9IVRw&key=YOUR_KEY"
```

**Response fields of interest:**
- `items[].statistics.viewCount`
- `items[].statistics.likeCount`
- `items[].statistics.commentCount`
- `items[].contentDetails.duration` (ISO 8601 format, e.g., PT12M34S)
- `items[].snippet.publishedAt`
- `items[].snippet.title`
- `items[].snippet.channelId`
- `items[].snippet.channelTitle`

---

### 4. playlistItems.list — Fetch Recent Channel Uploads

**Use:** Get a channel's recent uploads (more reliable than search for "all videos from a channel").

**Two-step process:**

**Step A:** Get the channel's uploads playlist ID:
```
GET /channels?part=contentDetails&id={CHANNEL_ID}&key={YOUTUBE_API_KEY}
```
Response: `items[0].contentDetails.relatedPlaylists.uploads` → gives you the uploads playlist ID (starts with `UU...`)

**Step B:** List videos from that playlist:
```
GET /playlistItems?part=snippet&playlistId={UPLOADS_PLAYLIST_ID}&maxResults=50&key={YOUTUBE_API_KEY}
```

Then use the video IDs from the response with `videos.list` to get full statistics.

---

### 5. Transcripts — via `youtube-transcript-api` (Python)

**Important:** The YouTube Data API `captions.download` endpoint requires OAuth 2.0 — do NOT use it. Instead, use the `youtube-transcript-api` Python library which requires **no API key and no OAuth**.

**Dependency:** `youtube-transcript-api` (installed via `pip3 install youtube-transcript-api`)

**How it works:** The library fetches transcripts directly from YouTube's public caption data. It works with both manual and auto-generated subtitles.

**Usage via shell command:**

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
import json

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch('{VIDEO_ID}')

# Convert to plain text
full_text = ' '.join([s.text for s in transcript.snippets])
print(full_text)
"
```

**Usage with timestamps (for hook analysis):**

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
import json

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch('{VIDEO_ID}')

# Output as JSON with timestamps
segments = [{'start': s.start, 'text': s.text} for s in transcript.snippets]
print(json.dumps(segments, indent=2))
"
```

**Key notes:**
- Pass the **video ID only** (e.g., `czLrUyA_Bh4`), NOT the full URL
- No API key or authentication needed
- Works with auto-generated captions
- Add 1-second delay between requests if fetching multiple transcripts to avoid throttling
- If a video has captions disabled or unavailable, the library will raise an error — catch it and skip to the next video

**Fallback if `youtube-transcript-api` fails:**
1. **YouTube MCP Server** — If available, use it to fetch transcripts directly
2. **Web search** — Search for "{video title} transcript" via Exa or web search
3. **Video description + comments** — Extract insight from metadata as a partial substitute

---

## Niche-Wide Keyword Scanning Pattern

**Use:** Discover trending content across the entire niche (not just competitor channels) by searching YouTube for high-view-count videos published in the last N days.

### search.list with viewCount ordering + date filter

```
GET /search?part=snippet&q={KEYWORD}&type=video&order=viewCount&publishedAfter={ISO_DATE}&maxResults=25&key={YOUTUBE_API_KEY}
```

**Key parameters:**
- `order=viewCount` — sort results by view count (highest first)
- `publishedAfter` — ISO 8601 date (e.g., `2026-03-10T00:00:00Z`) to restrict to recent videos
- `maxResults` — up to 50 per request (default 25 for niche scanning to manage quota)

**Pattern for niche scanning:**
1. Loop through configured keywords, calling `search.list` for each
2. Collect all video IDs across searches, de-duplicate
3. Batch `videos.list` (50 IDs per call) for full statistics
4. Batch `channels.list` (50 IDs per call) for subscriber counts of discovered channels
5. Score videos using absolute velocity thresholds (no channel median needed)

**Quota note:** Each `search.list` call = 100 units. For 10 keywords = 1,000 units. Track against `niche_scan.quota_budget` from sidecar config.

---

## Exa Web Search — MCP Tool Reference

**Use:** Cross-platform trend intelligence — supplement YouTube data with web signals from blogs, news, forums, and social media.

**Tool name:** `web_search_exa` (available via Exa MCP server)

**Usage pattern:**
```
web_search_exa(query="{search query}", date_filter="last_7_days")
```

**Best practices:**
- Use for broad trend queries (e.g., "Claude Code trending", "AI agents news this week")
- Cross-reference results with YouTube keyword search to classify topics as Convergent, YouTube-only, or Web-only
- Exa is supplementary — if unavailable, the workflow should gracefully degrade (skip web intelligence, note in report)
- Date filtering ensures results are timely (matching the niche scan timeframe)

---

## Quota Management

YouTube Data API has a daily quota of 10,000 units (default).

| Operation | Cost |
|---|---|
| channels.list | 1 unit |
| search.list | 100 units |
| videos.list | 1 unit |
| playlistItems.list | 1 unit |

**search.list is expensive** — prefer `playlistItems.list` + `videos.list` for scanning a channel's recent videos (2 units vs 100 units).

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| "No filter selected" on channels.list | Using `channelId=` instead of `id=` | Use `id=` parameter |
| "API key not valid" | Key has trailing whitespace, wrong key, or API not enabled | Clean the key, verify in Cloud Console |
| "unregistered callers" | YouTube Data API v3 not enabled in the key's GCP project | Enable the API in Cloud Console |
| 403 quota exceeded | Daily quota reached | Wait 24h or request quota increase |
