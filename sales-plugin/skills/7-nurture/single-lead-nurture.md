---
name: single-lead-nurture
description: Run nurture for a single specific lead — useful for testing or manual triggering
menu-code: NSL
---

# Single Lead Nurture

## Purpose

Run the nurture sequence for one specific lead. Useful for testing, manual triggering, or when you want to draft an email for a specific prospect outside the daily schedule.

## Process

### Step 1: Identify the Lead

Ask: "Which lead? Give me a name, company, or lead ID."

Search for the lead:
1. If lead ID provided → `get_lead` directly
2. If name/company provided → `search_leads` with the query, present matches, confirm

### Step 2: Load Context

1. **Get lead details** — `get_lead` for full lead data including contact
2. **Get contact details** — `get_contact` for sentiment, last communication
3. **Get lead comments** — `list_lead_comments` to find nurture state
4. **Load strategy doc** — Read `references/nurture-sequence-strategy.md` (within this skill folder)
5. **Load email voice** — Read `shared-references/adam-email-voice.md`

### Step 3: Assess Current State

Present the lead's current nurture state:

```
Lead: {title}
Contact: {name} ({email})
Stage: {stage} | Value: ${value} | Priority: {priority}
Last communication: {date} ({X days ago})
Sentiment: {label} — {summary}

Nurture state: {one of:}
  - No sequence started
  - Sequence active — on Step N{X}, next due {date}
  - Sequence paused
  - Sequence complete
  - Prospect replied — sequence stopped
```

### Step 4: Check for Replies

Search Gmail: `from:{contact_email} newer_than:30d`

If any reply found since last nurture step → warn and stop:
"Prospect replied on {date}. Sequence should stop here — tagging as replied."

### Step 5: Determine Next Action

Based on state:

- **No sequence started:**
  1. Classify scenario (A/B/C/D) from lead comments
  2. Find client slug, load `audit-data-lite.json`
  3. Show scenario classification and proposed schedule
  4. Ask: "Ready to start the sequence and draft N1?"

- **Sequence active, next step due:**
  1. Load client data
  2. Draft the next step email
  3. Present for review before creating Gmail draft

- **Sequence active, next step NOT due yet:**
  1. Show when next step is due
  2. Ask: "Want to draft it early anyway?"

- **Sequence paused:**
  1. Ask: "Want to resume the sequence?"

- **Sequence complete:**
  1. Show completion summary
  2. Ask: "Want to restart with a fresh sequence? (Not recommended unless circumstances changed)"

### Step 6: Draft and Review

Draft the email following the same rules as `daily-nurture-run.md` Step 5.

**Present the draft to the user before creating the Gmail draft.** Show:
- Subject line
- Full email body
- Word count
- Voice check notes (any concerns)

Ask: "Any changes before I create the Gmail draft?"

### Step 7: Create Draft and Log

After user approval:
1. `gmail_create_draft` with the email
2. `create_lead_comment` with nurture tracking tag
3. Confirm: "Draft created in Gmail. CRM comment logged. Next step: N{X} due {date}."
