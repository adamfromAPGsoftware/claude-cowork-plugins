---
name: respond-dms
description: Generate and send DM replies for a specific account with compliance checks and safety rails
menu-code: RD
---

# Respond DMs

Generate and send DM replies for a single Instagram account.

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
   - Find conversations where the last message has `direction: "inbound"` and no subsequent outbound message

5. **Report pending count:**
   ```
   {display_name} (@{handle}): {pending_count} unresponded DMs found.
   {expired_count} with expired 24h windows (will be skipped).
   {flagged_count} with flagged contacts (will be skipped).
   Rate limit: {current_hour_count}/180 sends used this hour.
   Proceeding with {actionable_count} responses...
   ```

6. **For each unresponded conversation:**

   #### Pre-Response Checks (ALL must pass)

   a. **Contact not flagged** -- check `contact.flags`. Skip if `ai_detection_test`, `off_topic`, or `do_not_respond` is `true`. Log: "SKIPPED @{username} -- flagged: {flag_name}"

   b. **We don't follow them** -- check `contact.we_follow_them`. If `true`, this is a personal contact, SKIP. Log: "SKIPPED @{username} -- we follow this person (personal contact)"

   c. **24-hour window active** -- `window_expires` must be greater than current time. If expired, skip. Log: "SKIPPED @{username} -- 24h window expired at {time}"

   c. **Rate limit OK** -- current hour count must be < 180. If exceeded, STOP all DM sending. Log: "RATE LIMIT REACHED -- stopping DM sends"

   d. **Do-not-respond rules** -- apply rules from conversation-strategy.md. Skip if matched. Log: "SKIPPED @{username} -- matched do-not-respond rule: {rule}"

   #### AI Detection Scan (CRITICAL)

   Read the inbound message(s). If ANY of these patterns are detected, set `contact.flags.ai_detection_test = true` in social-data.json and SKIP immediately:

   - **Bot/AI questions:** "are you a bot", "is this AI", "are you real", "prove you're human", "am I talking to a robot", "is this automated"
   - **Random knowledge tests:** "what's 2+2", "how tall is a building", "what color is the sky", "who is the president"
   - **Meta-questions about response patterns:** "why do you always respond so fast", "you sound like ChatGPT", "this feels like AI", "are you using a script"
   - **Rapid-fire unrelated questions in sequence**

   Log: "FLAGGED @{username} -- ai_detection_test triggered by: {pattern_summary}"

   #### Off-Topic Scan

   If the message is completely unrelated to tech/AI/business/building/content (politics, crypto, NSFW, personal drama, random nonsense):

   - Set `contact.flags.off_topic = true` in social-data.json and SKIP
   - Log: "FLAGGED @{username} -- off_topic: {brief_reason}"

   #### Generate and Send Response

   If all checks pass:

   e. **Read full conversation thread** -- all messages, both directions.

   f. **Determine nurture stage:**
      - **Cold** -- first message, never spoken before
      - **Warm** -- 2+ exchanges, building rapport
      - **Hot** -- asking about pricing, specifics, ready to act

   g. **Generate response** following conversation-strategy.md rules, brand-voice.md tone, and products.md recommendations:
      - Lowercase default, no em dashes or en dashes
      - No AI-sounding words
      - Gender-neutral unless explicitly confirmed male
      - Fragments OK, no formal language
      - Match the energy of the inbound message

   h. **Duplicate check** -- verify the response is not identical to any outbound message sent in the last 24 hours across all conversations. Regenerate if duplicate.

   i. **Send via script:**
      ```
      python3 {project-root}/social-plugin/scripts/send-instagram-dm.py --account {key} --conversation-id {conv_id} --message "{response}"
      ```
      - If sending multiple short messages (1-3 per voice rules), send each separately with a 2-5 second gap.

   j. **Log each send** with username, response preview, and nurture stage.

   **Between conversations:** Wait 30-300 seconds (random) before processing the next one. Use `bash sleep {random_seconds}`.

7. **Present results:**

```
DM responses complete for {display_name} (@{handle}).

  Sent: {sent_count}
  Skipped (expired window): {expired_count}
  Skipped (do-not-respond): {rule_skip_count}
  Skipped (rate limit): {rate_limit_skip_count}
  Flagged: {flagged_count} ({ai_test} ai_detection_test, {off_topic} off_topic)
  Errors: {error_count}

  Sent details:
  - @{username}: "{first 60 chars}..." (stage: {nurture_stage})
  - ...

  Flagged details:
  - @{username}: {flag_type} -- {reason}
  - ...
```

## Important Rules

- **NEVER use em dashes or en dashes** in ANY response.
- **NEVER send identical messages** to different people.
- **STOP immediately** if AI detection patterns detected. Flag and move on.
- **STOP immediately** if off-topic. Flag and move on.
- **Gender-neutral language** unless explicitly confirmed male.
- **Lowercase default**, fragments OK, no formal language.
- **NEVER send a DM if window_expires < now.**
- **NEVER exceed 180 sends per hour.**
- **Random delays between conversations** are mandatory.

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
- Send DM: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/send-instagram-dm.py --account {key} --conversation-id {conv_id} --message '{response}'")`
- Sleep between conversations: `execute_command("sleep {N}")`
- Write updated social-data.json: `execute_command("cat > {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json << 'JSONEOF'\n{json_content}\nJSONEOF")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
