---
name: init
description: First-run setup for Inbox Collector
menu-code: INIT
---

# First-Run Setup for Inbox Collector

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — poll history, configuration, current state
- `chronology.md` — poll session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/index.md`

```markdown
# Inbox Collector — Session Index

## Configuration
- Accounts discovered: (set via first PA — poll all)
- Default comment lookback: 7 days

## Poll History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Inbox Collector

## Read Access
- social-plugin/
- _bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/
- .env (for API credentials)

## Write Access
- social-plugin/data/
- _bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (social plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-soc-inbox-collector-sidecar/chronology.md`

```markdown
# Poll Chronology

(Poll sessions logged here as they accumulate)
```

## Account Verification

Scan `{project-root}/social-plugin/accounts/*/config.json` and for each account:

1. **Read config.json** — extract `account_key`, `display_name`, `instagram_handle`
2. **Verify env vars** — check `.env` for:
   - `INSTAGRAM_ACCESS_TOKEN_{KEY}` — Instagram Graph API access token
   - `INSTAGRAM_USER_ID_{KEY}` — Instagram Business Account user ID
   - `INSTAGRAM_PAGE_ID_{KEY}` — Facebook Page ID linked to Instagram account
3. **Report missing vars** — If any are missing, list them and prompt the user to add them to `.env`

## Social Data Bootstrap

For each account where `social-plugin/data/{account-key}/social-data.json` does not exist, create it with this scaffold:

```json
{
  "meta": {
    "account_key": "{account-key}",
    "last_dm_poll": null,
    "last_comment_poll": null,
    "poll_status": "never_polled"
  },
  "conversations": [],
  "comments": []
}
```

## Ready

Setup complete! Ready to poll your Instagram accounts for DMs and comments.
