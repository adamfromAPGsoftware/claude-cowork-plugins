# Memory System for CCS Content Strategist

**Memory location:** `{project-root}/_bmad/_memory/bmad-apg-ccs-1-content-strategist-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active projects and their research/ideation status
- Configuration (niche, platforms, competitor channels)
- Last session summary

**Update:** Immediately when a project status changes or research/ideation completes.

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Research patterns (which strategies yield best data)
- Trending topic clusters (recurring high-signal topics)
- Ideation success patterns (which concept types score highest)

**Format:** Append-only. Prune outdated entries when file grows large.

### `chronology.md` — Timeline

**Load when needed.** Contains:
- Session summaries (date, project, what was produced)
- Research outcomes

**Format:** Append-only. Keep last 20 sessions; archive older ones.

## Write Discipline

Before writing to memory, ask:

1. **Is this worth remembering?** — Will it improve the next session? If no, skip.
2. **Minimum tokens?** — Condense to the essential fact. No narrative, no fluff.
3. **Which file?**
   - `index.md` -> active projects, config, current status
   - `patterns.md` -> research patterns, topic clusters, ideation success
   - `chronology.md` -> session summaries
