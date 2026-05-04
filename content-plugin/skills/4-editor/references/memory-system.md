# Memory System for CCS Editor

**Memory location:** `{project-root}/context/memory/4-editor-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active reviews and gate results
- Configuration (thresholds, reference files)
- Last session summary

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Recurring quality issues across reviews
- Voice drift patterns (where and how brand voice tends to drift)
- Effective feedback patterns

### `chronology.md` — Timeline

Session summaries. Append-only. Keep last 20 sessions.

## Write Discipline

1. **Is this worth remembering?** — Will it improve review quality next session?
2. **Minimum tokens?** — Condense to essence.
3. **Which file?**
   - `index.md` -> active reviews, config, gate results
   - `patterns.md` -> recurring issues, voice drift, feedback effectiveness
   - `chronology.md` -> session summaries
