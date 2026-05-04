---
name: init
description: First-run setup for CCS Publisher
menu-code: INIT
---

# First-Run Setup for CCS Publisher

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/context/memory/5-publisher-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — connected channels, scheduling status, lead magnet registry
- `patterns.md` — scheduling patterns, platform performance, API quirks
- `chronology.md` — session timeline

## Setup Questions

1. **Buffer MCP connection** — Verify the Buffer MCP is connected (platform-level — no API key needed)
2. **Connected channels** — Use `mcp__buffer__use_buffer_api(action: "listChannels")` to discover connected social accounts
3. **Primary timezone** — What timezone for scheduling? (e.g. `Australia/Sydney`)

## Channel Discovery

Call the Buffer MCP:

```
mcp__buffer__use_buffer_api(action: "listChannels")
```

Store discovered channels in index.md.

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/context/memory/5-publisher-sidecar/index.md`

```markdown
# CCS Publisher — Session Index

## Connected Channels
{list discovered channels: platform, channelId, name}

## Lead Magnet Keyword Registry
(keyword | channel | post | date)

## Configuration
- Timezone: {confirmed-timezone}
- Buffer: configured

## Last Session
(none)
```

### `{project-root}/context/memory/5-publisher-sidecar/patterns.md`

```markdown
# Publisher Patterns

## Scheduling Patterns
(optimal posting times, day-of-week performance)

## Platform Quirks
(API gotchas, format requirements, known issues)

## Content Calendar History
(scheduling history for reference)
```

### `{project-root}/context/memory/5-publisher-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to schedule and publish content.
