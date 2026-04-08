# Memory System — Inbox Collector

## Location

`{project-root}/_bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Poll history, configuration, current state | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Poll session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next poll session
- Condense to essence — no narrative
- Update index.md immediately after each poll
- Write-through on critical events:
  - New account added to accounts/
  - Unusual poll result (errors, rate limits, token expiry)
  - Conversations with windows that expired before being handled
  - API permission changes
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Account keys and display names currently configured
- Poll frequency patterns (how often each account is polled)
- Typical DM/comment volume per account
- Any recurring issues with Instagram API responses (rate limits, token expiry)
- Conversations that had window expiry issues (for pattern detection)

## What NOT to Remember

- Individual message content (that lives in social-data.json)
- Engagement quality judgments (that's the Engagement Responder's job)
- Prospect qualification data (that's the Prospect Qualifier's job)
- Anything derivable from the current social-data.json state
