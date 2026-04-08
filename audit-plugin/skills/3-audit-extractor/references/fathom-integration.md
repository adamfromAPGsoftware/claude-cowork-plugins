# Fathom Integration Reference

This document is the source of truth for how Fathom recordings are fetched and stored in this system.

---

## Fetch Script

```bash
# Fetch transcripts + videos for a client
python3 scripts/fetch-transcripts.py --client-slug {client_slug}

# Skip video download (faster, transcripts only)
python3 scripts/fetch-transcripts.py --client-slug {client_slug} --no-video
```

**Requirements:**
- `FATHOM_API_KEY` set in `.env` at repo root
- `contact.emails` array populated in `clients/{slug}/audit/audit-data.json`
- `pip install requests python-dotenv` (if not installed)
- `brew install yt-dlp` (for video download)

---

## Fathom API — Verified Details

**Base URL:** `https://api.fathom.ai/external/v1`

**Auth:** `X-Api-Key: {key}` header

### List Meetings

```
GET /meetings
```

**Response shape:**
```json
{
  "items": [
    {
      "recording_id": 131117556,
      "title": "Grace",
      "meeting_title": "Grace and Adam",
      "url": "https://{FATHOM_URL}/calls/605144044",
      "share_url": "https://fathom.video/share/abc123",
      "recording_start_time": "2026-03-19T00:04:10Z",
      "recording_end_time": "2026-03-19T00:38:07Z",
      "scheduled_start_time": "2026-03-19T00:00:00Z",
      "calendar_invitees": [
        { "name": "{EXAMPLE_CLIENT_NAME}", "email": "{EXAMPLE_CLIENT_EMAIL}", "is_external": true },
        { "name": "{YOUR_NAME}",  "email": "{YOUR_EMAIL}",       "is_external": false }
      ],
      "recorded_by": { "name": "{YOUR_NAME}", "email": "{YOUR_EMAIL}" },
      "transcript": null
    }
  ],
  "next_cursor": "eyJwYWdlX251bSI6Mn0="
}
```

**Key notes:**
- Response key is `items` (not `data` or `meetings`)
- Meeting ID field is `recording_id` (integer), not `id`
- `transcript` is always `null` in the list response — fetch separately
- Filter by client email **client-side** via `calendar_invitees[].email` — there is no server-side invitee filter param
- Pagination: pass `cursor={next_cursor}` in subsequent requests

### Get Transcript

```
GET /recordings/{recording_id}/transcript
```

**Response shape:**
```json
{
  "transcript": [
    {
      "speaker": { "display_name": "{EXAMPLE_CLIENT_NAME}", "matched_calendar_invitee_email": "{EXAMPLE_CLIENT_EMAIL}" },
      "text": "Hey Adam, how are you going?",
      "timestamp": "00:00:02"
    }
  ]
}
```

**Key notes:**
- `timestamp` is `HH:MM:SS` string (not seconds)
- Speaker name is under `speaker.display_name`

### Video Download

There is no API endpoint for video files. Use `yt-dlp` with the `share_url`:

```bash
yt-dlp -o "recording.%(ext)s" "https://fathom.video/share/abc123"
```

yt-dlp has native Fathom support and downloads as `.mp4` via HLS (m3u8).

---

## Meeting Folder Structure

After running the fetch script, each meeting is stored as:

```
clients/{client_slug}/meetings/{YYYY-MM-DD}-{title-slug}/
  transcript.txt     # [MM:SS] Speaker: text format
  metadata.json      # recording_id, title, date, fathom_url, share_url, participants
  recording.mp4      # video (if --no-video not passed)
```

**Folder name:** `{YYYY-MM-DD}-{slugified-meeting-title}` derived from `recording_start_time`

**Example:** `2026-03-12-grace-and-adam/`

### transcript.txt format

```
Meeting: Grace and Adam
Date: 2026-03-12T01:14:32Z

[00:00] {EXAMPLE_CLIENT_NAME}: Hey Adam, how are you going?
[00:04] {EXAMPLE_CLIENT_NAME}: I'm good.
[00:11] {YOUR_NAME}: Sweet as, sweet as.
```

### metadata.json fields

```json
{
  "recording_id": 129238398,
  "title": "Grace and Adam",
  "date": "2026-03-12T01:14:32Z",
  "duration_seconds": 4520,
  "participants": [
    { "name": "{EXAMPLE_CLIENT_NAME}", "email": "{EXAMPLE_CLIENT_EMAIL}" },
    { "name": "{YOUR_NAME}",  "email": "{YOUR_EMAIL}" }
  ],
  "fathom_url": "https://{FATHOM_URL}/calls/601234567",
  "share_url": "https://fathom.video/share/abc123"
}
```

---

## Audit Data Contact Block

Client emails are stored as an **array** (supports multiple) in `audit-data.json`:

```json
"contact": {
  "name": "{EXAMPLE_CLIENT_NAME}",
  "emails": ["{EXAMPLE_CLIENT_EMAIL}"]
}
```

Add additional emails if meetings are booked under a different address.

---

## Timestamp Deep-Links

Fathom deep-link format: `https://{FATHOM_URL}/calls/{recording_id}?t={seconds}`

Convert `HH:MM:SS` → seconds: `hours * 3600 + minutes * 60 + seconds`

Example: `[14:32]` → 872 seconds → `https://{FATHOM_URL}/calls/129238398?t=872`

These are stored on process steps as `meeting_references[].timestamp_seconds` and rendered as hover links in the process map HTML.
