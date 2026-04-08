# Memory System for Close ⚡

**Memory location:** `{project-root}/_bmad/_memory/apg-close-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active close engagements and their status (transcript analyzed / audit-data-lite confirmed / close page generated / email sent)
- Configuration (social proof folder, blended rate, pricing tiers)
- Last session summary

**Update:** Immediately when a close asset is generated or an engagement status changes.

### `access-boundaries.md` — Access Control (Required)

**Load on activation before any file operations.** Contains read/write/deny zones.

**Critical:** Before any file operation, verify the path is within allowed boundaries. If uncertain, ask.

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Successful close language (from Mark, Dale, and future deals)
- Waste framings that land hardest by industry
- Social proof assets that resonate by industry tag
- Objection patterns and what resolved them

**Format:** Append-only. Prune outdated entries when file grows large.

### `chronology.md` — Timeline

**Load when needed.** Contains:
- Session summaries (date, client, what was produced)
- Engagement outcomes (closed / not closed / pending)

**Format:** Append-only. Keep last 20 sessions; archive older ones.

## Memory Persistence Strategy

### Write-Through (Immediate)

Persist immediately when:
1. audit-data-lite confirmed by consultant for a client
2. Close page or email generated and saved
3. User explicitly saves (`[SM]`)

### Checkpoint (Periodic)

Update `patterns.md` and `chronology.md` after:
- A successful close (client booked or paid)
- A pattern or social proof observation made during the session

### Save Triggers

**After these events, always update memory:**
- audit-data-lite confirmed by consultant
- A close asset (page or email) is generated and saved
- A close outcome is noted (won / lost / pending)

## Write Discipline

Before writing to memory, ask:

1. **Is this worth remembering?** — Will it improve the next close session? If no, skip.
2. **Minimum tokens?** — Condense to the essential fact. No narrative, no fluff.
3. **Which file?**
   - `index.md` → active engagements, config, current status
   - `patterns.md` → close language, waste framings, social proof performance
   - `chronology.md` → session summaries, engagement outcomes

## Memory Maintenance

Every 10 sessions or when files exceed ~100 lines:
1. **Condense index.md** — Archive completed engagements to chronology
2. **Prune patterns.md** — Remove patterns superseded by better ones
3. **Archive chronology.md** — Keep only last 20 sessions in active file
