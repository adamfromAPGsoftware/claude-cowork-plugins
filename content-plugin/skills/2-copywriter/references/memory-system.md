# Memory System for CCS Copywriter

**Memory location:** `{project-root}/content-plugin/data/memory/2-copywriter-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active projects and content production status
- Derivative tracking table (date, platform, format, category, hook, keyword, status)
- Last session summary

**Update:** Immediately when content is produced or published.

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Hook effectiveness (which hook types perform best per platform)
- Voice calibration notes (corrections to voice matching)
- Platform performance (what works per platform)

### `chronology.md` — Timeline

**Load when needed.** Session summaries.

## Write Discipline

1. **Is this worth remembering?** — Will it improve the next writing session?
2. **Minimum tokens?** — Condense to essence.
3. **Which file?**
   - `index.md` -> active projects, derivative tracking, status
   - `patterns.md` -> hook effectiveness, voice calibration, platform performance
   - `chronology.md` -> session summaries
