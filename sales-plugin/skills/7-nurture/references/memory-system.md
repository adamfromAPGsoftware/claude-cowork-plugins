# Memory System for Nurture Sequencer

**Memory location:** `{project-root}/_bmad/_memory/apg-nurture-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- Active nurture sequences with current step and scenario
- Last run date and summary
- Configuration (strategy doc path, schedule, voice reference)

**Update:** After every daily run or manual session.

### `access-boundaries.md` — Access Control (Required)

**Load on activation before any file operations.** Contains read/write/deny zones and MCP access list.

**Critical:** Before any file operation, verify the path is within allowed boundaries. If uncertain, ask.

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- Which email steps generate the most replies (N1? N2?)
- Which industries respond best to which angles
- Scenario classification accuracy (did Scenario B leads actually come back in 1-2 weeks?)
- Timing observations (are compressed gaps better or worse?)

**Format:** Append-only. Prune outdated entries when file grows large.

### `chronology.md` — Timeline

**Load when needed.** Contains:
- Daily run summaries (date, leads processed, drafts created, replies detected)
- Conversion outcomes (which leads eventually converted after nurture)
- Sequence completions and their outcomes

**Format:** Append-only. Keep last 30 runs; archive older ones.

## Memory Persistence Strategy

### Write-Through (Immediate)

Persist immediately when:
1. A daily nurture run completes
2. A lead replies (sequence stopped)
3. A lead converts (valuable outcome data)
4. User explicitly saves (`[SM]`)

### Checkpoint (Periodic)

Update `patterns.md` after:
- A nurture sequence leads to conversion (track which step triggered re-engagement)
- 10+ sequences have completed (enough data to spot patterns)

### Save Triggers

**After these events, always update memory:**
- Daily nurture run completes (update index.md with run summary)
- A lead replies during a sequence (note which step they replied to in patterns.md)
- A lead that went through nurture eventually converts (valuable conversion data)

## Write Discipline

Before writing to memory, ask:

1. **Is this worth remembering?** — Will it improve future nurture runs? If no, skip.
2. **Minimum tokens?** — Condense to the essential fact. No narrative, no fluff.
3. **Which file?**
   - `index.md` → active sequences, config, last run
   - `patterns.md` → email performance, industry angles, timing observations
   - `chronology.md` → run summaries, conversion outcomes

## Memory Maintenance

Every 30 runs or when files exceed ~100 lines:
1. **Condense index.md** — Archive completed sequences to chronology
2. **Prune patterns.md** — Remove patterns superseded by better data
3. **Archive chronology.md** — Keep only last 30 runs in active file
