# Schedule Instagram Post via Buffer MCP

## Prerequisites

- Instagram caption content must be ready (from a file or inline)
- Media files (slide PNGs for carousel, or single image) must be accessible at an absolute path
- Buffer MCP connected in Claude Code (platform-level — no API key needed) and Instagram account connected in Buffer

## Workflow

### 1. Collect Post Details

Gather the following from the user or from context:

- **Caption** — the post text (from a markdown file, agent output, or direct input)
- **Media** — either:
  - Directory of numbered slide PNGs for carousel (slide-01.png, slide-02.png, etc.)
  - Single image file path
- **Schedule date/time** — when to publish. Default timezone: AEST (UTC+10) / AEDT (UTC+11)

### 2. Fetch Instagram Channel ID

Call the Buffer MCP to find the Instagram channel:

```
mcp__buffer__use_buffer_api(action: "listChannels")
```

Locate the Instagram channel in the results and note its `channelId`.

### 3. Preview Payload

Present the scheduling payload to the user:

```
SCHEDULING TO: Buffer → Instagram
Account:     {handle from scheduling-config.md}
Caption:     {first 100 chars}... ({total chars} chars)
Media:       {file count} files OR {filename}
Schedule:    {formatted date/time AEST}
```

### 4. Confirm

**MANDATORY** — Get explicit user confirmation before sending.

### 5. Execute

Call the Buffer MCP:

```
mcp__buffer__use_buffer_api(
  action: "createPost",
  channelIds: ["{instagram_channel_id}"],
  text: "{caption}",
  scheduledAt: "{ISO 8601 UTC datetime}",
  media: [
    "{slides_dir}/slide-01.png",
    "{slides_dir}/slide-02.png",
    ...
  ]
)
```

For a single image, pass a single-item `media` array.

### 6. Report Result

**On success:** Display the Buffer `postId`, `status`, and `scheduledAt`.

**On error:** Display the error message. Common issues:
- Buffer MCP not connected — check Claude Code MCP settings
- Instagram account not connected — connect it in your Buffer dashboard
- File path not accessible — verify the media files exist at the specified paths

### 7. Update Tracking (if called from an agent)

If triggered from an agent session:
- Log the schedule event to the agent's memory sidecar
- Update any caption file frontmatter with `status: scheduled` and `scheduled_at`

---

## Reference

| Field | Value |
|-------|-------|
| Instagram max caption chars | 2,200 |
| Max carousel slides | 10 |
| Scheduling | Via `mcp__buffer__use_buffer_api(action: "createPost")` |
| Channel IDs | From `mcp__buffer__use_buffer_api(action: "listChannels")` or `scheduling-config.md` |
