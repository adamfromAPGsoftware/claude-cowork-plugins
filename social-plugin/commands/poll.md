---
description: Poll Instagram for new DMs and comments across all configured accounts
---

Fetch the latest DMs and comments for all accounts:

1. For each account in `accounts/*/config.json`:
   - Run `python3 {plugin_root}/scripts/fetch-instagram-dms.py --account {key}`
   - Run `python3 {plugin_root}/scripts/fetch-instagram-comments.py --account {key}`
2. Report: accounts processed, new items, window warnings

$ARGUMENTS
