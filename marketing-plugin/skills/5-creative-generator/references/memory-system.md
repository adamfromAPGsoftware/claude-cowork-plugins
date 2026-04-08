# Memory System — Creative Generator

## Location

`{project-root}/_bmad/_memory/bmad-apg-mkt-creative-generator-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Batch history, configuration, last session | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Generation session timeline | When saving memory (SM) |
| `angles.md` | Proven angle patterns and performance notes | When building angles (BA) |

## Discipline

- Only remember what matters for the next creative session
- Condense to essence — no narrative
- Update index.md immediately after each generation batch
- Write-through on critical events:
  - New batch generated with angle count and creative count
  - Angle pattern that produced high-performing ads (feedback from Performance Analyst)
  - Generation failures or API issues (rate limits, model errors)
  - Format or prompt patterns that produced better results
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Batch IDs and what intelligence sources informed them
- Angle patterns that trace to competitor winners (what worked and why)
- Prompt engineering patterns that produce better images/videos
- Generation success rates by format and model
- Any recurring issues with image or video generation APIs

## What NOT to Remember

- Individual copy variant text (that lives in creative-data.json)
- Full image/video prompts (stored in creative-data.json per asset)
- Ad performance metrics (that's the Performance Analyst's job)
- Anything derivable from the current creative-data.json state
