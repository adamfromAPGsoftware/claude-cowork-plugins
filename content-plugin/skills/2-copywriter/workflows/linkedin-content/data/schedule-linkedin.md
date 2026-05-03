# Schedule LinkedIn Post via Buffer

## Prerequisites

- LinkedIn post content must be ready (from a file or inline)
- Buffer MCP connected in Claude Code (platform-level — no API key needed)
- LinkedIn channel must be connected in Buffer (buffer.com/manage/channels)

## Workflow

### 1. Collect Post Details

Gather the following from the user or from context:

- **Content** — the post text (from a markdown file, agent output, or direct input)
- **Media file path** — absolute path to image/video/PDF to attach (optional)
- **Schedule date/time** — when to publish (user's local timezone, from `scheduling.timezone` in config.yaml)

### 2. Preview Payload

Present the scheduling payload to the user:

```
SCHEDULING TO: Buffer → LinkedIn
Content:     {first 100 chars}... ({total chars} chars)
Media:       {filename or "none"}
Schedule:    {formatted date/time} ({timezone})
```

### 3. Confirm

**MANDATORY** — Get explicit user confirmation before sending.

### 4. Schedule via Buffer MCP

Use the Buffer MCP to create and schedule the post.

**Sequence:**
1. Call `mcp__buffer__use_buffer_api(action: "listChannels")` to retrieve the LinkedIn channel ID
2. If media: include file path in the media field
3. Call `mcp__buffer__use_buffer_api` with:
   - `action`: `"createPost"`
   - `profileIds`: [LinkedIn channel ID]
   - `text`: post content
   - `scheduledAt`: ISO 8601 datetime in UTC
   - `media`: media attachment if applicable

### 5. Report Result

**On success:** Display post ID, scheduled time, and LinkedIn account name.

**On error:** Display the error. Common issues:
- Buffer MCP not connected → check Claude Code MCP settings
- Channel not connected → reconnect LinkedIn in buffer.com/manage/channels
- Content too long → LinkedIn max is 3,000 characters

### 6. Update Tracking (if called from an agent)

If triggered from an agent session:
- Log the schedule event to the agent's `memories.md`
- Update any post file frontmatter with `status: scheduled` and `scheduled_at`
