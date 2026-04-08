# Memory System for Pre-Discovery

**Memory location:** `{project-root}/_bmad/_memory/apg-pre-discovery-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active prospect preps and their status (researched / transcript analyzed / prospect brief generated)
- Configuration (booking URL, industry focus)
- Last session summary

**Update:** Immediately when a prospect status changes or a prospect brief is generated.

### `access-boundaries.md` — Access Control (Required)

**Load on activation before any file operations.** Contains read/write/deny zones.

**Critical:** Before any file operation, verify the path is within allowed boundaries. If uncertain, ask.

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Industry pain patterns (which hypotheses proved accurate after discovery calls)
- Effective opening questions (which Clarify questions reliably opened prospects up)
- Phone call signal accuracy (did buying signals predict discovery outcomes?)
- Prospect brief feedback (what worked vs. didn't — corrections from Adam)

**Format:** Append-only. Prune outdated entries when file grows large.

### `chronology.md` — Timeline

**Load when needed.** Contains:
- Session summaries (date, client, what was produced)
- Discovery call outcomes (closed / not closed / pending)

**Format:** Append-only. Keep last 20 sessions; archive older ones.

## Memory Persistence Strategy

### Write-Through (Immediate)

Persist immediately when:
1. New client created via [NC]
2. Research completed via [RC]
3. Transcript analyzed via [AT]
4. Prospect brief generated via [BC]
5. User explicitly saves (`[SM]`)

### Checkpoint (Periodic)

Update `patterns.md` and `chronology.md` after:
- A discovery call outcome is reported (closed / not closed)
- Adam gives feedback on what worked or didn't from the prospect brief

### Save Triggers

**After these events, always update memory:**
- Prospect profile created or updated
- Prospect brief generated and saved
- Discovery call outcome noted (won / lost / pending)

## Write Discipline

Before writing to memory, ask:

1. **Is this worth remembering?** — Will it improve the next prep session? If no, skip.
2. **Minimum tokens?** — Condense to the essential fact. No narrative, no fluff.
3. **Which file?**
   - `index.md` -> active prospects, config, current status
   - `patterns.md` -> industry pain patterns, effective questions, signal accuracy
   - `chronology.md` -> session summaries, discovery outcomes

## Memory Maintenance

Every 10 sessions or when files exceed ~100 lines:
1. **Condense index.md** — Archive completed preps to chronology
2. **Prune patterns.md** — Remove patterns superseded by better ones
3. **Archive chronology.md** — Keep only last 20 sessions in active file
