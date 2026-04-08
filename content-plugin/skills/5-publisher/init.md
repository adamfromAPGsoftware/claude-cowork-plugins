---
name: init
description: First-run setup for CCS Publisher
menu-code: INIT
---

# First-Run Setup for CCS Publisher

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-ccs-5-publisher-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — connected accounts, scheduling status, lead magnet registry
- `patterns.md` — scheduling patterns, platform performance, API quirks
- `chronology.md` — session timeline

## Setup Questions

1. **Late.dev API key** — Confirm `LATE_API_KEY` is set in `.env`
2. **Connected accounts** — Run `GET /accounts` to discover connected social accounts
3. **Primary timezone** — What timezone for scheduling? (e.g. `Australia/Sydney`)

## Account Discovery

After confirming API key, run:
```bash
curl -s "https://getlate.dev/api/v1/accounts" -H "Authorization: Bearer $LATE_API_KEY" | jq '.[]|{platform,accountId,name}'
```

Store discovered accounts in index.md.

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/_bmad/_memory/bmad-apg-ccs-5-publisher-sidecar/index.md`

```markdown
# CCS Publisher — Session Index

## Connected Accounts
{list discovered accounts: platform, accountId, name}

## Lead Magnet Keyword Registry
(keyword | channel | post | date)

## Configuration
- Timezone: {confirmed-timezone}
- Late.dev API: confirmed

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-ccs-5-publisher-sidecar/patterns.md`

```markdown
# Publisher Patterns

## Scheduling Patterns
(optimal posting times, day-of-week performance)

## Platform Quirks
(API gotchas, format requirements, known issues)

## Content Calendar History
(scheduling history for reference)
```

### `{project-root}/_bmad/_memory/bmad-apg-ccs-5-publisher-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to schedule and publish content.
