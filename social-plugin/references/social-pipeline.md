# Social Engagement Pipeline

## Overview

The Social Plugin automates Instagram (and future TikTok) engagement across multiple accounts. Each account is self-contained with its own conversation strategy, brand voice, and optional CRM integration.

## Pipeline Flow

POLL (on demand or scheduled loop)
  Inbox Collector [PA] → for each account in accounts/*/config.json:
    fetch-instagram-dms.py --account {key}
    fetch-instagram-comments.py --account {key}
    → data/{account-key}/social-data.json

RESPOND (on demand or chained after poll)
  Engagement Responder [RA] → for each account:
    Load accounts/{key}/conversation-strategy.md
    Load accounts/{key}/brand-voice.md
    Load accounts/{key}/products.md
    For each new inbound DM: generate response → send-instagram-dm.py → update social-data.json
    For each new comment needing reply: generate response → send-instagram-comment-reply.py → update social-data.json

QUALIFY (periodic, CRM-enabled accounts only)
  Prospect Qualifier [QA] → for each account where config.json has crm.enabled=true:
    Analyse conversation history in data/{key}/social-data.json
    Classify contacts against accounts/{key}/icp.md
    Push qualified leads to CRM via MCP tools

## Account Discovery

Agents discover accounts by scanning `accounts/*/config.json`. Adding a new account = adding a new folder. No code changes required.

## Data Flow

accounts/{key}/conversation-strategy.md  →  AI response generation context
accounts/{key}/brand-voice.md            →  Tone and style rules
accounts/{key}/products.md               →  What to recommend
accounts/{key}/icp.md                    →  Who we're talking to
accounts/{key}/config.json               →  Platform, credentials, CRM settings
data/{key}/social-data.json              →  All fetched + sent messages/comments

## Rate Limits

- Instagram DMs: 200/hour per account
- 24-hour messaging window: can only respond to DMs where the last inbound message was within 24 hours
- Comments: no documented rate limit, but pace replies to avoid looking like a bot

## Adding a New Account

1. Create `accounts/{new-key}/` with config.json, conversation-strategy.md, brand-voice.md, products.md, icp.md
2. Add env vars: INSTAGRAM_ACCESS_TOKEN_{KEY}, INSTAGRAM_PAGE_ID_{KEY}, INSTAGRAM_IG_USER_ID_{KEY}
3. Create `data/{new-key}/social-data.json` with empty schema
4. Run [PA] to start polling

## Adding a New Platform (e.g., TikTok)

1. Write platform-specific scripts: `fetch-tiktok-dms.py`, `send-tiktok-dm.py`, etc.
2. Create account folder with `platform: "tiktok"` in config.json
3. Agents already dispatch by platform field — no agent changes needed
