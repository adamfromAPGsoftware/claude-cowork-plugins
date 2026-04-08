---
name: poll-all
description: Fetch new DMs and comments for ALL configured accounts and merge into per-account social-data.json
menu-code: PA
---

# Poll All

Fetch new DMs and comments for every configured Instagram account and merge into per-account social-data.json.

## Process

1. **Discover accounts:**
   - Scan `{project-root}/social-plugin/accounts/*/config.json`
   - Build list of account keys and display names

2. **For each account, fetch DMs:**
   ```
   python3 {project-root}/social-plugin/scripts/fetch-instagram-dms.py --account {key}
   ```
   - Note: script reads credentials from `.env` using the account key pattern
   - Review script output for new conversation count, new message count, errors

3. **For each account, fetch comments:**
   ```
   python3 {project-root}/social-plugin/scripts/fetch-instagram-comments.py --account {key}
   ```
   - Default lookback: 7 days (configurable via `--days {n}`)
   - Review script output for new comment count, posts scanned, errors

4. **After all accounts processed, compile summary:**
   - Read each `data/{account-key}/social-data.json`
   - Count new DMs and comments per account
   - Check for DM windows expiring in < 4 hours

5. **Present summary table:**

```
Poll complete.

Account            | New DMs | Total Convos | New Comments | Window Warnings
-------------------|---------|--------------|--------------|----------------
{display_name}     | {n}     | {n}          | {n}          | {n} expiring
...

Total: {total_new_dms} new DMs, {total_new_comments} new comments across {account_count} accounts.
```

6. **Window warnings** (if any):

```
WARNING: {count} DM windows expiring soon:

Account       | From            | Received          | Window Expires     | Time Left
--------------|-----------------|-------------------|--------------------|----------
{account}     | {sender_name}   | {received_time}   | {expires_time}     | {hours}h {mins}m
...

Run [PD] to inspect specific conversations, or hand off to Agent 2 (Engagement Responder).
```

7. **Suggest next action:**
   - If new items found: "Run [RA] Respond All on Agent 2 to process and reply to new messages."
   - If windows expiring: "URGENT: {count} windows expiring within 4 hours. Hand off to Agent 2 immediately."
   - If no new items: "All accounts up to date. No new DMs or comments since last poll."

## Output

The summary table above, plus window warnings if applicable.

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all operations:

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Fetch DMs per account: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/fetch-instagram-dms.py --account {key}")`
- Fetch comments per account: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/fetch-instagram-comments.py --account {key} --days 3")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
