---
name: respond-comments
description: Generate and send comment replies for a specific account with compliance checks and safety rails
menu-code: RC
---

# Respond Comments

Generate and send comment replies for a single Instagram account.

## Process

1. **Determine account:**
   - If user specified an account key, use that
   - Otherwise, list available accounts from `{project-root}/social-plugin/accounts/*/config.json` and ask: "Which account? Enter the key or number."

2. **Verify account exists:**
   - Confirm `accounts/{key}/config.json` is present
   - If not, report error and list available accounts

3. **Load account context:**
   - Read `{project-root}/social-plugin/accounts/{key}/conversation-strategy.md`
   - Read `{project-root}/social-plugin/accounts/{key}/brand-voice.md`
   - Read `{project-root}/social-plugin/accounts/{key}/products.md`
   - If any are missing, warn and ask whether to proceed with available docs

4. **Load data:**
   - Read `{project-root}/social-plugin/data/{key}/social-data.json`
   - Read `{project-root}/social-plugin/data/{key}/rate-limit.json` (if exists) to check current hour's send count
   - Find comments where `reply` is null or absent (no reply sent yet)

5. **Report pending count:**
   ```
   {display_name} (@{handle}): {pending_count} unreplied comments found.
   {flagged_count} from flagged contacts (will be skipped).
   Rate limit: {current_hour_count}/180 sends used this hour.
   Proceeding with {actionable_count} replies...
   ```

6. **For each unreplied comment:**

   #### Pre-Response Checks (ALL must pass)

   a. **Contact not flagged** -- check `contact.flags`. Skip if `ai_detection_test`, `off_topic`, or `do_not_respond` is `true`. Log: "SKIPPED comment by @{username} -- flagged: {flag_name}"

   b. **Rate limit OK** -- current hour count must be < 180. If exceeded, STOP all comment replies. Log: "RATE LIMIT REACHED -- stopping comment replies"

   c. **Do-not-respond rules** -- apply rules from conversation-strategy.md (spam, single emojis, irrelevant, etc.). Skip if matched. Log: "SKIPPED comment by @{username} on {post_id} -- matched do-not-respond rule: {rule}"

   Note: 24-hour window does NOT apply to comments.

   #### AI Detection Scan (CRITICAL)

   Read the comment text. If ANY of these patterns are detected, set `contact.flags.ai_detection_test = true` in social-data.json and SKIP immediately:

   - **Bot/AI questions:** "are you a bot", "is this AI", "are you real", "prove you're human"
   - **Random knowledge tests:** "what's 2+2", "how tall is a building", "what color is the sky"
   - **Meta-questions about response patterns:** "you sound like ChatGPT", "this feels like AI", "are you using a script"

   Log: "FLAGGED @{username} -- ai_detection_test triggered by comment: {pattern_summary}"

   #### Off-Topic Scan

   If the comment is completely unrelated to tech/AI/business/building/content (politics, crypto, NSFW, personal drama, random nonsense):

   - Set `contact.flags.off_topic = true` in social-data.json and SKIP
   - Log: "FLAGGED @{username} -- off_topic comment: {brief_reason}"

   #### Generate and Send Reply

   If all checks pass:

   d. **Read post context** -- load the post caption for context on what the comment is about.

   e. **Read the comment text.**

   f. **Keyword trigger check** -- if the comment contains a keyword trigger (BUILD, CLAUDE, AI, AUTOMATE, FREE, SKILL, PLUGIN, RESULTS, AUTOMATION, AGENT):
      - Reply to the comment with a short variation. Rotate between: "just sent it over", "it's with you now", "dropped it in your inbox", "just DM'd you", "check your DMs"
      - ALSO send a DM to that user with a personalized message referencing the post content + relevant link from products.md
      - Send comment reply first, then DM

   g. **Genuine question** -- reply with a direct 1-2 sentence answer.

   h. **Compliment** -- quick thanks + specific follow-up question.

   i. **Send comment reply via script:**
      ```
      python3 {project-root}/social-plugin/scripts/send-instagram-comment-reply.py --account {key} --comment-id {id} --message "{reply}"
      ```
      - Check script exit code. If error, log and continue.

   j. **Log:** "REPLIED to @{username} on post {post_id}: {first 60 chars of reply}..."

   **Between comments:** Wait 10-60 seconds (random) before processing the next one. Use `bash sleep {random_seconds}`.

7. **Present results:**

```
Comment responses complete for {display_name} (@{handle}).

  Replied: {replied_count}
  Skipped (do-not-respond): {rule_skip_count}
  Skipped (rate limit): {rate_limit_skip_count}
  Flagged: {flagged_count} ({ai_test} ai_detection_test, {off_topic} off_topic)
  Errors: {error_count}

  Reply details:
  - @{username} on post {post_id}: "{first 60 chars}..."
  - ...

  Flagged details:
  - @{username}: {flag_type} -- {reason}
  - ...
```

## Important Rules

- **NEVER use em dashes or en dashes** in ANY response.
- **NEVER send identical replies** to different people. Every comment reply must be unique.
- **STOP immediately** if AI detection patterns detected. Flag and move on.
- **STOP immediately** if off-topic. Flag and move on.
- **Gender-neutral language** unless explicitly confirmed male.
- **Lowercase default**, fragments OK, no formal language.
- **NEVER exceed 180 sends per hour.**
- **Random delays between comments** are mandatory.

## Output

The results summary above.

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all operations:

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Read conversation strategy: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/conversation-strategy.md")`
- Read brand voice: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/brand-voice.md")`
- Read products: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/products.md")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`
- Read rate limit: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/rate-limit.json")`
- Send comment reply: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/send-instagram-comment-reply.py --account {key} --comment-id {id} --message '{reply}'")`
- Send DM (for keyword triggers): `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/send-instagram-dm.py --account {key} --conversation-id {conv_id} --message '{response}'")`
- Sleep between comments: `execute_command("sleep {N}")`
- Write updated social-data.json: `execute_command("cat > {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json << 'JSONEOF'\n{json_content}\nJSONEOF")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
