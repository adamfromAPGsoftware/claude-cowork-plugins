---
name: poll-dms
description: Fetch new DMs for a specific Instagram account
menu-code: PD
---

# Poll DMs

Fetch new DMs for a single Instagram account and merge into its social-data.json.

## Process

1. **Determine account:**
   - If user specified an account key, use that
   - Otherwise, list available accounts from `{project-root}/social-plugin/accounts/*/config.json` and ask: "Which account? Enter the key or number."

2. **Verify account exists:**
   - Confirm `accounts/{key}/config.json` is present
   - If not, report error and list available accounts

3. **Run fetch script** using Desktop Commander's `execute_command` tool (or Bash in Claude Code):
   ```
   python3 {project-root}/social-plugin/scripts/fetch-instagram-dms.py --account {key}
   ```

4. **Review script output:**
   - Note how many new conversations and messages were fetched
   - Note any errors (auth failure, rate limit, token expiry, permissions)

5. **Load the updated social-data.json** and report:
   - Total conversations
   - New messages this poll
   - Conversations with open 24-hour windows
   - Any windows expiring in < 4 hours (WARNING)

6. **Update poll metadata:**
   - Confirm `last_dm_poll` timestamp was updated by the script

## Output

```
DM poll complete for {display_name} (@{handle}).

  New messages: {new_count}
  Total conversations: {total_count}
  Open windows: {open_window_count}

  {if warnings:}
  WARNING: {count} windows expiring within 4 hours:
  - {sender_name}: expires {time} ({hours}h {mins}m remaining)
  ...
```

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all operations:

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Fetch DMs: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/fetch-instagram-dms.py --account {key}")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
