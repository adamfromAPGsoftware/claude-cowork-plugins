# Memory System for CCS Creative Director

**Memory location:** `{project-root}/_bmad/_memory/bmad-apg-ccs-3-creative-director-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active projects and visual asset status
- Configuration (reference photos, inspiration, brand colours)
- Last session summary

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Visual preferences and style choices
- Thumbnail performance data (CTR scores)
- Effective Gemini prompt patterns
- Reference image notes

### `chronology.md` — Timeline

Session summaries. Append-only. Keep last 20 sessions.

## Write Discipline

1. **Is this worth remembering?** — Will it improve visual output next session?
2. **Minimum tokens?** — Condense to essence.
3. **Which file?**
   - `index.md` -> active projects, config, status
   - `patterns.md` -> visual preferences, CTR data, prompt patterns
   - `chronology.md` -> session summaries
