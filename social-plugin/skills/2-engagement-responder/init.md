---
name: init
description: First-run setup for Engagement Responder
menu-code: INIT
---

# First-Run Setup for Engagement Responder

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — response history, configuration, current state
- `chronology.md` — response session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/index.md`

```markdown
# Engagement Responder — Session Index

## Configuration
- Accounts discovered: (set via first RA — respond all)
- Response mode: direct send (no human review)

## Response History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Engagement Responder

## Read Access
- social-plugin/
- _bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/
- .env (for API credentials)

## Write Access
- social-plugin/data/
- _bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (social plugin does not touch audit data)
```

### `{project-root}/_bmad/_memory/bmad-apg-soc-engagement-responder-sidecar/chronology.md`

```markdown
# Response Chronology

(Response sessions logged here as they accumulate)
```

## Account Verification

Scan `{project-root}/social-plugin/accounts/*/config.json` and for each account:

1. **Read config.json** — extract `account_key`, `display_name`, `instagram_handle`
2. **Verify account docs exist** — check for:
   - `accounts/{key}/conversation-strategy.md` — response rules and nurture flow
   - `accounts/{key}/brand-voice.md` — tone and style guide
   - `accounts/{key}/products.md` — product catalogue for recommendations
3. **Report missing docs** — If any are missing, list them and prompt the user to create them before running RA
4. **Verify env vars** — check `.env` for:
   - `INSTAGRAM_ACCESS_TOKEN_{KEY}` — Instagram Graph API access token
   - `INSTAGRAM_USER_ID_{KEY}` — Instagram Business Account user ID
   - `INSTAGRAM_PAGE_ID_{KEY}` — Facebook Page ID linked to Instagram account
5. **Report missing vars** — If any are missing, list them and prompt the user to add them to `.env`

## Send Script Verification

Verify the following scripts exist:
- `{project-root}/social-plugin/scripts/send-instagram-dm.py`
- `{project-root}/social-plugin/scripts/send-instagram-comment-reply.py`

If missing, report error — these scripts are required for sending responses.

## Social Data Check

For each account, verify `social-plugin/data/{account-key}/social-data.json` exists. If not, warn that Agent 1 (Inbox Collector) must be run first to populate data.

## Ready

Setup complete! Ready to generate and send responses for your Instagram accounts.
