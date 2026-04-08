# Schedule Instagram Post to Internal CRM

## Prerequisites

- Instagram caption content must be ready (from a file or inline)
- Media files (slide PNGs for carousel, or single image) must be accessible at an absolute path
- Environment variables must be set in `.env` at the project root:
  - `INTERNAL_CRM_SUPABASE_URL` — Supabase API URL for the internal CRM project
  - `INTERNAL_CRM_APG_API_KEY` — API key (`apg_` format)

## Workflow

### 1. Collect Post Details

Gather the following from the user or from context:

- **Caption** — the post text (from a markdown file, agent output, or direct input)
- **Media** — either:
  - `--media-dir` — directory of numbered slide PNGs for carousel (slide-01.png, slide-02.png, etc.)
  - `--media` — single image file path
- **Schedule date/time** — when to publish. Default timezone: AEST (UTC+10) / AEDT (UTC+11). If "now", omit `--scheduled-at`

### 2. Preview Payload

Present the scheduling payload to the user:

```
SCHEDULING TO: {YOUR_CRM} → Instagram
Account:     {YOUR_NAME}
Caption:     {first 100 chars}... ({total chars} chars)
Media:       {file count} files from {directory} OR {filename}
Schedule:    {formatted date/time AEST or "now"}
```

### 3. Confirm

**MANDATORY** — Get explicit user confirmation before sending.

### 4. Execute

Run the scheduling script:

```bash
# Carousel (directory of PNGs)
python3 scripts/schedule-instagram-post.py \
  --file "{path/to/caption.md}" \
  --media-dir "{path/to/slides/}" \
  --scheduled-at "{ISO 8601 datetime}"

# Single image
python3 scripts/schedule-instagram-post.py \
  --caption "Caption text here" \
  --media "{path/to/image.png}" \
  --scheduled-at "{ISO 8601 datetime}"
```

**Flags:**
- `--file` — path to markdown file with caption (strips frontmatter)
- `--caption` — inline caption text (alternative to `--file`)
- `--scheduled-at` — ISO 8601 datetime. Omit for immediate posting
- `--media` — path to single media file
- `--media-dir` — directory of numbered slide PNGs (carousel mode)

### 5. Report Result

**On success (201):** Display `post_id`, `status`, `scheduled_at`, media count, and any `media` URLs.

**On error:** Display the error `code`, `message`, and `hint`. Common issues:
- `AUTH_ERROR` — check `INTERNAL_CRM_APG_API_KEY` in `.env`
- `VALIDATION_ERROR` — caption too long, bad file type, or missing field
- `NOT_FOUND` — wrong `account_id`
- `UPLOAD_ERROR` — storage issue, retry

### 6. Update Tracking (if called from an agent)

If triggered from an agent session:
- Log the schedule event to the agent's `memories.md`
- Update any caption file frontmatter with `status: scheduled` and `scheduled_at`

---

## Reference

| Field | Value |
|-------|-------|
| Instagram account_id | `a2867c79-f288-4a16-898b-5f12ed71513c` |
| API Endpoint | `{SUPABASE_URL}/functions/v1/social-media-posts` |
| Auth | `apikey` header with `apg_` key |
| Instagram max caption chars | 2,200 |
| Max carousel slides | 10 |

## Adam's Social Accounts

| Platform | account_id |
|----------|------------|
| LinkedIn | `d9ed774a-cc62-4131-a08d-64be36f864bd` |
| Instagram | `a2867c79-f288-4a16-898b-5f12ed71513c` |
| TikTok | `38f9261d-b51e-4582-b92c-8764058f62dd` |
| Twitter | `e7773628-6c48-4de7-b602-cd23b9194a11` |
| YouTube | `80ffdc97-924a-4a38-a4fe-213aaa24cd40` |
