# Memory System — Engagement Responder

## Location

`{project-root}/_bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/`

## Files

| File | Purpose | Load when |
|------|---------|-----------|
| `index.md` | Response history, configuration, current state | Always on activation |
| `access-boundaries.md` | Read/write/deny zones | Always on activation |
| `chronology.md` | Response session timeline | When saving memory (SM) |

## Discipline

- Only remember what matters for the next response session
- Condense to essence — no narrative
- Update index.md immediately after each response run
- Write-through on critical events:
  - New account added to accounts/
  - Send failures (API errors, rate limits, token expiry)
  - Conversations where windows expired before response was sent
  - Do-not-respond rule updates or edge cases discovered
  - Notable conversation patterns (common questions, high-value prospects)
- Prune when files exceed 100 lines
- Keep last 20 chronology entries

## What to Remember

- Account keys and display names currently configured
- Response volume per account (how many DMs/comments per run)
- Common inbound message patterns per account
- Any recurring send failures or API issues
- Do-not-respond edge cases that were ambiguous
- Nurture stage distribution per account (how many first-contact vs qualified)

## What NOT to Remember

- Individual message content (that lives in social-data.json)
- Full conversation threads (read fresh each time from social-data.json)
- Account strategy details (reload from conversation-strategy.md each time)
- Product details (reload from products.md each time)
- Anything derivable from the current social-data.json state
