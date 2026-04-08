---
name: poll-comments
description: Fetch new comments on recent posts/Reels for a specific Instagram account
menu-code: PC
---

# Poll Comments

Fetch new comments on recent posts and Reels for a single Instagram account and merge into its social-data.json.

## Process

1. **Determine account:**
   - If user specified an account key, use that
   - Otherwise, list available accounts from `{project-root}/social-plugin/accounts/*/config.json` and ask: "Which account? Enter the key or number."

2. **Determine lookback period:**
   - If user specified `--days {n}`, use that
   - Default: 7 days

3. **Verify account exists:**
   - Confirm `accounts/{key}/config.json` is present
   - If not, report error and list available accounts

4. **Run fetch script** using Desktop Commander's `execute_command` tool (or Bash in Claude Code):
   ```
   python3 {project-root}/social-plugin/scripts/fetch-instagram-comments.py --account {key} --days {days}
   ```

5. **Review script output:**
   - Note how many posts were scanned and new comments found
   - Note any errors (auth failure, rate limit, token expiry, permissions)

6. **Load the updated social-data.json** and report:
   - Posts scanned in lookback period
   - New comments this poll
   - Total comments tracked
   - Comments awaiting reply (no `reply_id` set)

7. **Update poll metadata:**
   - Confirm `last_comment_poll` timestamp was updated by the script

## Output

```
Comment poll complete for {display_name} (@{handle}).

  Posts scanned: {post_count} (last {days} days)
  New comments: {new_count}
  Total comments tracked: {total_count}
  Awaiting reply: {unreplied_count}

  Top commented posts:
  - {post_caption_preview}: {comment_count} new comments
  - ...
```

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all operations:

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Fetch comments: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/fetch-instagram-comments.py --account {key} --days {days}")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
