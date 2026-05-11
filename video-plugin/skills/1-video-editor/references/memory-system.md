# Wiki System for Video Editor

**Wiki location:** `{plugin-root}/video-plugin/wiki/`

## Core Principle

Tokens are expensive. Only capture corrections that will prevent a future mistake. Condense everything to its essence.

## File Structure

### `wiki/index.md` — Master Index

**Load on activation.** Contains:
- Page directory (topic → file mapping)
- Session log (date, project, skills used, corrections captured)
- Graduation log (corrections that became permanent rules)

**Update:** Via [SM] — append a session row after each working session.

### `wiki/remotion-build.md` — Remotion Build Corrections

Component patterns, prop mistakes, render issues, scaffold errors.

### `wiki/audio-sync.md` — Audio & Sync Corrections

Audio extraction, sync drift, loudness normalization, per-clip audio patterns.

### `wiki/pacing-timing.md` — Pacing & Timing Corrections

Cut timing, overlay density, dead air thresholds, format-specific pacing violations.

### `wiki/storyboard.md` — Storyboard Corrections

Segment planning mistakes, MG cue placement, brief structure, B-roll strategy errors.

### `wiki/motion-graphics.md` — Motion Graphics Corrections

Hera vs Remotion template selection, animation timing, reference image issues, MG coverage.

### `wiki/rendering-output.md` — Rendering & Output Corrections

FFmpeg flags, quality settings, file naming, output format issues.

### `wiki/platform-specific.md` — Platform-Specific Corrections

YouTube/TikTok/LinkedIn/Instagram format gotchas, dimension requirements, upload issues.

## Write Discipline

### Correction Entry Format

```markdown
### [YYYY-MM-DD] One-line description of what went wrong
**Fix:** The correct approach. 1-2 lines max.
**Applies to:** short-form | vsl | long-form | ad | all
```

### Before Writing, Ask Three Questions

1. **Worth remembering?** — Will this prevent a future mistake? If it's a one-off creative preference that won't generalize, skip it.
2. **Minimum tokens?** — Condense to one line problem + one line fix. No narrative, no context.
3. **Which page?** — Use the topic-to-page mapping in `wiki-update.md`.

## Write-Through Triggers

Capture a correction immediately when:
- User corrects agent output during any workflow step (Correction Detection blocks)
- User explicitly requests a wiki save
- User runs `[WU]` manually after a session
- A pattern from memory is confirmed wrong

## Graduation Rules

When the same correction appears **3 or more times** (same underlying fix, possibly different wording):

1. The agent detects repetition during `[WU]` execution
2. Prompts: "This fix has come up {n} times. Graduate it to `references/` as a permanent rule? [Y/N]"
3. If Y:
   - Append to the relevant `references/` file (e.g., `pacing-timing.md` → `short-form-pacing-rules.md` or `long-form-pacing-rules.md`)
   - Add a row to `wiki/index.md` graduation log
   - Condense the wiki entries to a single line with "(graduated to references/{file})" suffix
4. Graduation requires explicit user confirmation — never graduate silently

## Session Log Update (via [SM])

After each working session, `[SM]` appends to `wiki/index.md` Session Log:

```markdown
| {date} | {project-slug} | {skills used} | {n corrections captured} |
```
