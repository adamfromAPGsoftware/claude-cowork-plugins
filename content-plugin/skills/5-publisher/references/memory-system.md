# Memory System for CCS Publisher

**Memory location:** `{project-root}/memory/5-publisher-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Connected social accounts (platform, accountId, name)
- Lead magnet keyword registry (keyword, channel, post, date)
- Configuration (timezone, API status)
- Last session summary

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Scheduling patterns (optimal posting times)
- Platform quirks (API gotchas, format requirements)
- Content calendar history

### `chronology.md` — Timeline

Session summaries with post IDs and scheduling details. Append-only. Keep last 20 sessions.

## Write Discipline

1. **Is this worth remembering?** — Will it improve scheduling next session?
2. **Minimum tokens?** — Condense to essence.
3. **Which file?**
   - `index.md` -> accounts, keywords, config, status
   - `patterns.md` -> scheduling patterns, platform quirks
   - `chronology.md` -> session summaries with post IDs
