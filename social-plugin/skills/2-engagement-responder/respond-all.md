---
name: respond-all
description: Process and respond to all new DMs and comments across all configured accounts with compliance checks and safety rails
menu-code: RA
---

# Respond All

Generate and send responses to all new DMs and comments for every configured Instagram account.

## Pre-Flight

1. **Discover accounts:**
   - Scan `{project-root}/social-plugin/accounts/*/config.json`
   - Build list of account keys and display names

2. **For each account, load context:**
   - Read `{project-root}/social-plugin/accounts/{key}/conversation-strategy.md` -- response rules, nurture flow, do-not-respond rules, edge cases
   - Read `{project-root}/social-plugin/accounts/{key}/brand-voice.md` -- tone, style, emoji usage, message length
   - Read `{project-root}/social-plugin/accounts/{key}/products.md` -- what to recommend and when
   - **CRITICAL:** Hold this context for all responses for THIS account. Clear and reload when switching to next account.

## Per-Account Processing

**For each account:**

### A. Load Data

- Read `{project-root}/social-plugin/data/{key}/social-data.json`
- Read `{project-root}/social-plugin/data/{key}/rate-limit.json` (if exists) to check current hour's send count

### B. Process DMs

For each conversation where the last message has `direction: "inbound"` and there is no subsequent outbound message:

#### Pre-Response Checks (ALL must pass)

1. **Contact not flagged** -- check `contact.flags`. Skip if `ai_detection_test`, `off_topic`, or `do_not_respond` is `true`. Log: "SKIPPED @{username} -- flagged: {flag_name}"
2. **We don't follow them** -- check `contact.we_follow_them`. If `true`, this is a personal contact, SKIP. Log: "SKIPPED @{username} -- we follow this person (personal contact)"
3. **24-hour window active** -- `window_expires` must be greater than current time. If expired, skip. Log: "SKIPPED @{username} -- 24h window expired at {time}"
3. **Rate limit OK** -- current hour count must be < 180 (leave buffer below the 200 platform limit). If exceeded, STOP all DM sending for this account. Log: "RATE LIMIT REACHED for {account} -- stopping DM sends"
4. **Do-not-respond rules** -- apply rules from conversation-strategy.md (single emoji, spam, bot messages, etc.). If matched, skip. Log: "SKIPPED @{username} -- matched do-not-respond rule: {rule}"

#### AI Detection Scan (CRITICAL)

Read the inbound message(s). If ANY of these patterns are detected, set `contact.flags.ai_detection_test = true` in social-data.json and SKIP immediately:

- **Bot/AI questions:** "are you a bot", "is this AI", "are you real", "prove you're human", "am I talking to a robot", "is this automated"
- **Random knowledge tests:** "what's 2+2", "how tall is a building", "what color is the sky", "who is the president"
- **Meta-questions about response patterns:** "why do you always respond so fast", "you sound like ChatGPT", "this feels like AI", "are you using a script"
- **Rapid-fire unrelated questions in sequence:** multiple unrelated questions fired in quick succession designed to test response coherence

Log: "FLAGGED @{username} -- ai_detection_test triggered by: {pattern_summary}"

#### Off-Topic Scan

If the message is completely unrelated to tech/AI/business/building/content (politics, crypto, NSFW, personal drama, random nonsense):

- Set `contact.flags.off_topic = true` in social-data.json and SKIP
- Log: "FLAGGED @{username} -- off_topic: {brief_reason}"

#### Generate and Send Response

If all checks pass:

1. **Read the FULL conversation history** -- all messages, both directions. Note what has been discussed, what the person asked, what links have been shared.

2. **Determine nurture stage:**
   - **Cold** -- first message, never spoken before
   - **Warm** -- 2+ exchanges, building rapport
   - **Hot** -- asking about pricing, specifics, ready to act

3. **Load conversation-strategy.md** and follow the rules for this stage exactly.

4. **Generate response** following ALL voice rules from brand-voice.md:
   - Lowercase default
   - No em dashes or en dashes ever
   - No AI-sounding words (leverage, utilize, streamline, etc.)
   - Gender-neutral language unless explicitly confirmed male
   - Fragments OK, no formal language
   - Match the energy of the inbound message

5. **Duplicate check** -- VERIFY the response is not identical to any outbound message sent in the last 24 hours across ALL conversations for this account. If it is, regenerate with different wording.

6. **Send via script:**
   ```
   python3 {project-root}/social-plugin/scripts/send-instagram-dm.py --account {key} --conversation-id {conv_id} --message "{response}"
   ```
   - Check script exit code. If error, log and continue to next conversation.

7. **Multi-message sends** -- if sending multiple short messages (1-3 per the voice rules), send each separately with a 2-5 second gap between them using `sleep`.

8. **Log:** "SENT DM to @{username}: {first 60 chars of response}..." (stage: {nurture_stage})

**Between conversations:** Wait 30-300 seconds (random) before processing the next one. Use `bash sleep {random_seconds}`.

### C. Process Comments

For each comment where `reply` is null or absent:

#### Pre-Response Checks (ALL must pass)

1. **Contact not flagged** -- same flag checks as DMs (ai_detection_test, off_topic, do_not_respond)
2. **Rate limit OK** -- same hourly check (comments share the rate limit pool)
3. **Do-not-respond rules** -- apply rules from conversation-strategy.md. Skip if matched.

Note: 24-hour window does NOT apply to comments.

#### AI Detection and Off-Topic Scans

Apply the same AI detection and off-topic scans as DMs. Flag the contact if triggered.

#### Generate and Send Reply

If all checks pass:

1. **Read the post caption** for context on what the comment is about.

2. **Read the comment text.**

3. **Keyword trigger check** -- if the comment contains a keyword trigger (BUILD, CLAUDE, AI, AUTOMATE, FREE, SKILL, PLUGIN, RESULTS, AUTOMATION, AGENT):
   - Reply to the comment with a short variation. Rotate between: "just sent it over", "it's with you now", "dropped it in your inbox", "just DM'd you", "check your DMs"
   - ALSO send a DM to that user with a personalized message referencing the post content + relevant link from products.md
   - Send comment reply first, then DM

4. **Genuine question** -- reply with a direct 1-2 sentence answer.

5. **Compliment** -- quick thanks + specific follow-up question.

6. **Send comment reply via script:**
   ```
   python3 {project-root}/social-plugin/scripts/send-instagram-comment-reply.py --account {key} --comment-id {id} --message "{reply}"
   ```
   - Check script exit code. If error, log and continue.

7. **Log:** "REPLIED to @{username} on post {post_id}: {first 60 chars of reply}..."

**Between comments:** Wait 10-60 seconds (random) before processing the next one.

### D. Summary

After all accounts processed, present:

```
Response run complete.

Account          | DMs Sent | Comments Replied | Skipped | Flagged
-----------------|----------|------------------|---------|--------
{display_name}   | {n}      | {n}              | {n}     | {n} ({flag_types})
...

Total: {total_dms} DMs sent, {total_comments} comments replied across {account_count} accounts.
Skipped: {total_skipped} ({window_expired} expired windows, {rule_matched} do-not-respond, {rate_limited} rate limited)
Flagged: {total_flagged} ({ai_test_count} ai_detection_test, {off_topic_count} off_topic)
Errors: {total_errors}
```

If errors occurred:
```
Errors encountered:
- {account}: {error_type} for @{username} -- {error_message}
```

## Important Rules (repeated for emphasis)

- **NEVER use em dashes or en dashes** in ANY response. Not in DMs, not in comments, not anywhere.
- **NEVER send identical messages** to different people. Every response must be unique.
- **STOP immediately** if AI detection patterns are detected. Flag the contact and move on.
- **STOP immediately** if off-topic/random questions. Flag the contact and move on.
- **Gender-neutral language** unless the person has explicitly confirmed they are male.
- **Lowercase default**, fragments OK, no formal language.
- **NEVER generate a response without loading conversation-strategy.md first.** Non-negotiable.
- **NEVER send a DM if window_expires < now.** The API will reject it and it wastes rate limit.
- **NEVER exceed 180 sends per hour.** Stop sending if limit reached.
- **Random delays between messages** are mandatory, not optional. This prevents bot-like send patterns.

## Output

The summary table above, plus error details if applicable.

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
- Send comment reply: `execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/send-instagram-comment-reply.py --account {key} --comment-id {id} --message '{reply}'")`
- Sleep between conversations: `execute_command("sleep {N}")`
- Write updated social-data.json: `execute_command("cat > {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json << 'JSONEOF'\n{json_content}\nJSONEOF")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
