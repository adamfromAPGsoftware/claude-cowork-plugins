---
description: Generate and send Instagram DM replies and comment responses across all accounts
---

Process all new DMs and comments for all configured accounts:

1. For each account in `accounts/*/config.json`:
   - Load conversation strategy and brand voice
   - Generate and send DM replies for messages with active 24h windows
   - Generate and send comment replies for unreplied comments
2. Report: responses sent per account, skipped items, errors

$ARGUMENTS
