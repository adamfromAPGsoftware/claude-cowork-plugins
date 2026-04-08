---
name: cowork-example-account
description: Poll-and-respond cycle for @{YOUR_HANDLE_PERSONAL} only. Designed for scheduled Cowork execution via Desktop Commander.
menu-code: FA
---

# Full Cycle: Poll and Respond (@{YOUR_HANDLE_PERSONAL})

This is a self-contained, zero-context workflow for scheduled Cowork execution. It polls the @{YOUR_HANDLE_PERSONAL} Instagram account for new DMs and comments, then generates and sends responses using each account's conversation strategy. Everything runs through Desktop Commander.

---

## Step 0: Detect Execution Environment

Try to read a file natively. If that fails, all operations go through `execute_command`.

Test:
```
execute_command("echo 'desktop-commander-active'")
```

If `execute_command` is available, use it for ALL file and script operations below. If you have native file access (Claude Code terminal), use Bash/Read/Write tools directly instead.

**Project root (absolute):** `{PROJECT_ROOT}`

All paths below are relative to this root unless marked as absolute.

---

## Step 1: Account

This workflow processes ONLY the **example-account** account. No discovery needed.

Set account_key = example-account and proceed directly to Step 2.

---

## Step 2: Process @{YOUR_HANDLE_PERSONAL}

### 2a. Read Account Config

```
execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/example-account/config.json")
```

Extract: `display_name`, `handle`, `env_key`, and any feature flags.

### 2b. Poll DMs

```
execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/fetch-instagram-dms.py --account example-account")
```

This pulls new DM conversations from the Instagram Graph API and merges them into social-data.json. The script handles deduplication and 24-hour window calculation.

### 2c. Poll Comments

```
execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/fetch-instagram-comments.py --account example-account --days 3")
```

This pulls recent post/Reel comments. The script handles deduplication.

### 2d. Read Social Data

```
execute_command("cat {PROJECT_ROOT}/social-plugin/data/example-account/social-data.json")
```

Parse the JSON. Identify:
- **Pending DMs:** Inbound messages with no subsequent outbound message in the same conversation
- **Pending comments:** Comments where `reply` is null and `replied` is false

### 2e. Load Account Context

Read ALL three context docs before generating any response:

```
execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/example-account/conversation-strategy.md")
```
```
execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/example-account/brand-voice.md")
```
```
execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/example-account/products.md")
```

These define tone, voice rules, product recommendations, nurture flows, and compliance rules. Every response MUST comply with conversation-strategy.md. No exceptions.

---

## Step 3: Process Pending DMs

For each pending DM conversation, run the full pre-response check pipeline before generating any response.

### Pre-Response Checks (DMs)

Run these checks IN ORDER. If any check triggers a skip/flag, do NOT generate a response for that conversation.

#### Check 1: Contact Flags

Look up the contact in social-data.json. If ANY of these flags are set, SKIP the conversation silently:
- `flags.ai_detection_test` = true
- `flags.off_topic` = true
- `flags.do_not_respond` = true

#### Check 2: Follow Filter

If the conversation-strategy.md specifies an "Ask for Follow" rule:
- Check `contact.we_follow_them` in social-data.json
- If they haven't followed and this is an early conversation (< 3 messages exchanged), include the follow prompt naturally before sending any links

#### Check 3: 24-Hour Window

Check `window_expires` on the most recent inbound message:
- If the current time is PAST `window_expires`, SKIP the conversation. Log as "window expired."
- If within 2 hours of expiry, prioritize this conversation (process it first).

#### Check 4: Rate Limit

Track the number of API sends this cycle. Instagram enforces a 180 messages/hour cap.
- If approaching the limit (170+ sent), STOP processing and log remaining items as "rate limited."

#### Check 5: AI Detection Scan

Read the latest inbound message. If it contains ANY of these patterns, DO NOT RESPOND and set `flags.ai_detection_test = true`:
- "are you a bot?", "is this AI?", "are you real?", "prove you're human"
- "are you actually {name}?", "is this automated?", "who am I talking to?"
- Random knowledge test questions ("what's 2+2?", "how tall is a building?", "capital of France?")
- Meta-questions about response patterns or timing
- "you sound like ChatGPT", "this feels AI", "are you using AI to respond?"

#### Check 6: Off-Topic Scan

If the latest inbound message is about any of these topics, DO NOT RESPOND and set `flags.off_topic = true`:
- Politics, religion, personal life, relationships, NSFW
- Crypto or trading advice
- Random nonsense or trivia questions
- Medical, legal, or financial advice
- Conspiracy theories or misinformation

#### Check 7: Do-Not-Respond Rules

SKIP silently (no flag needed) if the message is:
- A single emoji reaction with no text (fire, thumbs up, heart, etc.)
- An obviously automated or bot message
- "DM me for collab" or similar spam
- Just a link with no context
- A repeated message from the same person within 5 minutes (respond to latest only)
- A story reaction with no accompanying text
- "Follow for follow" or engagement bait
- A natural conversation end ("Cool thanks!", "Cheers!", etc.)

### Generate Response

If ALL checks pass:

1. Read the FULL conversation history (all messages in the thread)
2. Follow the conversation-strategy.md nurture flow and routing logic
3. Generate the response following ALL voice rules:
   - Lowercase default, only capitalize proper nouns
   - Use contractions (can't, don't, it's, you're)
   - Use "reckon" not "think"
   - NEVER use em dashes or en dashes
   - NEVER use more than one exclamation mark
   - NEVER use banned phrases ("I hope this helps", "feel free to", "don't hesitate to", "happy to help", "great question", etc.)
   - NEVER use banned words ("leverage", "utilize", "furthermore", "however", "additionally", "notably", "essentially")
   - NEVER start a message with "I" as the first word
   - NEVER use bullet points or numbered lists in DMs
   - NEVER mention specific prices
   - Gender-neutral language (no "bro", "dude", "man", "mate" unless clearly male)
   - Almost no emoji (max one fire or shaka per turn, most messages zero)
   - Match their energy level
4. Ensure the response is UNIQUE (never send the same message to two different people word-for-word)
5. Include at least one specific reference to something from the conversation context

### Send Response

```
execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/send-instagram-dm.py --account example-account --conversation-id {conv_id} --message '{response}'")
```

**Important:** Escape single quotes in the response message. If the response contains a single quote, use `'\''` to escape it in the shell command.

### Inter-Conversation Delay

After each conversation is processed (sent or skipped), sleep for a random duration:

```
execute_command("sleep {N}")
```

Where N is a random number between 30 and 300 seconds. This prevents detection of automated patterns. Pick a different random value each time.

---

## Step 4: Process Pending Comments

For each pending comment, run the pre-response check pipeline.

### Pre-Response Checks (Comments)

#### Check 1: Contact Flags

Same as DMs. Look up the commenter's username in social-data.json contacts. If flagged, SKIP.

#### Check 2: AI Detection Scan

Same patterns as DMs. Flag and skip if triggered.

#### Check 3: Off-Topic Scan

Same topics as DMs. Flag and skip if triggered.

#### Check 4: Do-Not-Respond Rules

Same rules as DMs, plus:
- Single-word comments that are just the keyword trigger (these need a response, do NOT skip)
- Comments that are just emojis (skip)

#### Check 5: Rate Limit

Same 180/hr cap. Continue tracking from DM sends.

### Comment Reply Flow (DM Check Logic)

This is the most important automation logic for comments. When someone comments a keyword trigger (BUILD, CLAUDE, AI, AUTOMATE, etc.):

**Step A: Check social-data.json**

Look up the commenter's username in social-data.json conversations. Has this person ever sent a DM?

**Step B-1: They HAVE DM'd us before**

- Reply to the comment with a variation of: "just sent it over" / "it's in your DMs" / "check your messages"
- Send them a personalized DM referencing the post they commented on, then include the relevant link

**Step B-2: They have NOT DM'd us before**

We CANNOT initiate a DM with someone who hasn't messaged us first (Instagram API limitation).

- Reply to the comment prompting them to DM us. Vary each time:
  - "hey send me a DM and i'll fire it over"
  - "drop me a DM and i'll send it through"
  - "shoot me a message and i'll get it to you"
  - "send us a DM and i'll sort you out"
- Do NOT attempt to send a DM

### Generate Comment Reply

If ALL checks pass:

1. Read the post/Reel context that the comment is on
2. Follow conversation-strategy.md comment rules:
   - 1-2 sentences MAX (comments are public)
   - For genuine questions: direct, useful 1-sentence answer
   - For compliments: quick thanks + specific follow-up. Never just "thanks"
   - NEVER reply with just "thanks" or emoji-only
   - NEVER reply with more than 2 sentences
3. Apply all voice rules (same as DMs)
4. Ensure uniqueness across all comment replies

### Send Comment Reply

```
execute_command("cd {PROJECT_ROOT} && python3 social-plugin/scripts/send-instagram-comment-reply.py --account example-account --comment-id {comment_id} --message '{response}'")
```

### Inter-Comment Delay

Comments use a longer delay than DMs. Sleep 60-360 seconds between comment replies:

```
execute_command("sleep {N}")
```

---

## Step 5: Update Social Data

After all responses are sent for an account, write the updated social-data.json back:

```
execute_command("cat > {PROJECT_ROOT}/social-plugin/data/example-account/social-data.json << 'ENDOFFILE'
{updated_json}
ENDOFFILE")
```

Ensure all flag changes (ai_detection_test, off_topic, do_not_respond) and outbound message records are persisted.

---

## Step 6: Report Summary

After processing @{YOUR_HANDLE_PERSONAL}, output a structured summary:

```
Full Cycle Complete
===================

Account: {display_name} (@{handle})
  DMs:      {sent} sent | {skipped} skipped | {flagged} flagged | {expired} window expired
  Comments: {sent} sent | {skipped} skipped | {flagged} flagged
  Flags set: {list of new flags set this cycle}

Account: {display_name} (@{handle})
  DMs:      ...
  Comments: ...

Totals: {total_sent} sent | {total_skipped} skipped | {total_flagged} flagged
Rate limit: {messages_sent}/180
```

---

## Compliance Checklist (Quick Reference)

Before sending ANY response, verify:

- [ ] Contact is not flagged (ai_detection_test, off_topic, do_not_respond)
- [ ] 24-hour DM window has not expired
- [ ] Rate limit not exceeded (180/hr)
- [ ] Message does not trigger AI detection patterns
- [ ] Message is not off-topic
- [ ] Message is not in the do-not-respond category
- [ ] Response follows all voice rules (lowercase, contractions, no dashes, no banned phrases)
- [ ] Response is unique (not sent word-for-word to anyone else)
- [ ] Response includes a specific contextual reference
- [ ] No prices mentioned anywhere
- [ ] No gendered terms unless clearly appropriate
- [ ] No calls to action for calls or meetings (redirect to website/community)
- [ ] Follow prompt included if needed (early conversation, no follow yet)
- [ ] Comment reply is 1-2 sentences max
- [ ] Inter-conversation delay applied (30-300s for DMs, 60-360s for comments)
