# Memory System for Video Editor

**Memory location:** `{project-root}/_bmad/_memory/bmad-apg-vid-1-video-editor-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence.

## File Structure

### `memories.md` — Primary Source

**Load on activation.** Contains:
- User profile and preferences
- Session history (date, project, what was processed)
- Patterns and preferences learned across sessions
- Pipeline notes (observations about pipeline behavior)

**Update:** After each session or when significant pipeline work is completed.

### `instructions.md` — Operational Protocols

**Load on activation.** Contains:
- Proxy workflow rules
- Processing order rules (body first, then intro)
- Boundary constraints (read/write zones)
- Startup behavior sequence

### `editing-preferences.md` — Format-Specific Rules

**Load on activation before any editing or analysis task.** Contains:
- Pacing rules per format (talking head, podcast, screen recording, mixed)
- Transition preferences
- Visual style rules
- Platform-specific style guides (YouTube, Shorts, LinkedIn, TikTok, Instagram)

**Update:** Only with explicit user approval.

### `branded-assets/` — Visual Assets

Contains logos, profile images, and brand graphics used in motion graphics and overlays.

### `remotion-templates/` — Template Library

Contains TypeScript Remotion component templates for segment patterns.

## Memory Persistence Strategy

### Write-Through (Immediate)

Persist immediately when:
1. New project ingested via [VI]
2. Analysis completed via [AA], [TR], or [VA]
3. Video clipped via [VC]
4. Storyboard completed via [SB]
5. Render completed via [RE]
6. User explicitly saves via [SM]

### Checkpoint (Periodic)

Update `memories.md` patterns section after:
- A full pipeline run completes
- User gives feedback on edit quality
- New pacing or style preferences are established

## Write Discipline

Before writing to memory, ask:
1. **Is this worth remembering?** — Will it improve the next editing session? If no, skip.
2. **Minimum tokens?** — Condense to the essential fact. No narrative, no fluff.
3. **Which file?**
   - `memories.md` -> session history, user preferences, pipeline observations
   - `editing-preferences.md` -> pacing rules, style preferences (user approval required)
   - `instructions.md` -> operational protocol changes (rare)
