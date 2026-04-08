---
name: daily-nurture-run
description: Daily automated scan of all post-discovery leads — detect scenarios, draft nurture emails, log to CRM
menu-code: NDR
---

# Daily Nurture Run

## Purpose

Scan all active post-discovery leads, determine which ones need a nurture email today, draft personalised emails in Gmail, and log everything to CRM lead comments. This is the main capability that runs on a schedule.

## Pre-Run Setup

1. **Load strategy doc** — Read `references/nurture-sequence-strategy.md` (within this skill folder) for sequence definitions, timing, scenarios, and content strategy
2. **Load email voice** — Read `shared-references/adam-email-voice.md` for voice rules
3. **Set today's date** — Use current date for all timing calculations

## Process

### Step 1: Pull Post-Discovery Leads

Use `list_leads` with limit 100. Filter to leads in these stages:
- "Discovery Call - Completed"
- "Qualified"
- "Proposal"
- "Initial Follow-Up Phone Call"
- "Not Showing up to Discovery Call (Need Harassment)"
- "Need Re-Activation"

Exclude leads in: "Won", "Lost", "Disqualified", "New", "Contacted", "Negotiation"

For each lead, note: `lead_id`, `title`, `stage`, `value` (this is the quoted audit price for this client), `priority`, `contact` (name, email, id), `created_at`, `updated_at`.

**Important:** The `value` field on the lead is the price quoted to this specific client. Use it as `{{quoted_price}}` in templates (formatted as "$X,XXX"). Never hardcode "$3,000" because the price varies per client.

### Step 2: Check Nurture State for Each Lead

For each lead from Step 1:

1. **Get lead comments** — `list_lead_comments` for the lead
2. **Scan for nurture tags:**
   - `[NURTURE-COMPLETE]` → Skip, sequence finished
   - `[NURTURE-PAUSED]` → Skip, manually paused
   - `[NURTURE-REPLIED]` → Skip, prospect replied
   - `[NURTURE-START]` → Sequence is active, find current step
   - `[NURTURE]` → Find the most recent step tag to determine progress
   - No nurture tags → New lead, needs sequence initiation

3. **If sequence is active, determine:**
   - Which step was last drafted (N1, N2, N3, N4, or N5)
   - What date the next step is due (from the "Next:" field in the comment)
   - Is the next step due today or earlier?

### Step 3: Check for Replies (Critical Safety Check)

For each lead that might need an email today:

1. **Get contact email** — from the lead's contact data
2. **Search Gmail** — `gmail_search_messages` with query: `from:{contact_email} newer_than:30d`
3. **If any email found from the contact since the last nurture step was drafted:**
   - Add `[NURTURE-REPLIED]` comment to the lead:
     ```
     [NURTURE-REPLIED] Prospect replied on {date} — sequence stopped. Human takeover needed.
     Subject: "{reply_subject}"
     ```
   - Skip this lead — do NOT draft another email

### Step 4: Classify New Leads (No Existing Nurture State)

For leads with no `[NURTURE-START]` tag:

1. **Read lead comments** — scan for timing signals:
   - "follow up in a week", "couple of weeks", "next week" → **Scenario B**
   - "follow up in a month", "after Easter", "Q3", "not right now" → **Scenario C**
   - "cancelled", "can't make it", "something came up", "reschedule" (multiple occurrences) → **Scenario D**
   - None of the above → **Scenario A** (Ghosting — default)

2. **Calculate sequence start date:**
   - **Scenario A:** 3 days after the initial follow-up email date (or lead's `updated_at` if no follow-up date found)
   - **Scenario B:** The requested follow-up date (parse from comments). If date is ambiguous, default to 14 days from last activity.
   - **Scenario C:** The requested follow-up date. If ambiguous, default to 30 days from last activity.
   - **Scenario D:** Same as Scenario A timing, but note the lighter touch requirement.

3. **Calculate full schedule** based on scenario (see strategy doc for timing per scenario)

4. **Add start comment:**
   ```
   [NURTURE-START] Scenario {A/B/C/D} ({description}) — 5-email sequence initiated
   Schedule: N1 {date}, N2 {date}, N3 {date}, N4 {date}, N5 {date}
   Contact: {name} ({email})
   Data source: clients/{slug}/audit/audit-data-lite.json
   ```

5. **If N1 is due today or earlier, proceed to Step 5 for this lead**

### Step 5: Draft the Nurture Email

For each lead where the next step is due today or earlier:

**One email per lead per day maximum.** If multiple steps are overdue, draft only the next one.

#### 5a: Load Client Data

1. **Find client slug** — match from lead title or contact name against `clients/` directory
2. **Load audit-data-lite.json** — Read `clients/{slug}/audit/audit-data-lite.json`
   - If file doesn't exist, also try `clients/{slug}/audit/ssad-lite.json`
   - If neither exists, skip with warning:
     ```
     [NURTURE-SKIP] No audit-data-lite.json found for {lead_title}. Cannot personalise — skipping.
     ```
3. **Extract key fields:**
   - `contact.name` — first name for greeting
   - `top_waste_item` — description, monthly_waste_aud, quote
   - `waste_items[]` — secondary waste items
   - `pain_points[]` — verbatim client quotes
   - `industry_tag` — for tone calibration
   - `positive_signals` — moments of enthusiasm
   - `business_metrics` — company size, revenue context

#### 5b: Draft Based on Step Number

Read the content strategy for the relevant step from `references/nurture-sequence-strategy.md` (within this skill folder).

**For each step, the email MUST:**
- Follow Adam's email voice (loaded in pre-run)
- Be under 150 words (100 words for Scenario D leads)
- Use "Hey {first_name}," greeting (or "Hi" for corporate)
- Include at least one natural qualifier ("just", "probably", "roughly")
- Use contractions throughout
- Reference specific client data — never generic
- End with appropriate sign-off ("Thanks," or "Talk soon," then "Adam" then "{YOUR_COMPANY}")
- Pass the voice-check gate: "Would Adam copy-paste this into Gmail without editing?"

**Step-specific content (refer to strategy doc for full details):**

| Step | Theme | Key Data |
|------|-------|----------|
| N1 | The One Thing | `top_waste_item.quote` + `monthly_waste_aud` |
| N2 | Social Proof | `industry_tag` → matched case study + `positive_signals` |
| N3 | The Hidden Cost | `waste_items[1]` + `waste_items[2]` with figures |
| N4 | Guarantee Reminder | `top_waste_item.monthly_waste_aud` annualised |
| N5 | The Parking Lot | `top_waste_item` reference, graceful exit |

**Scenario D adjustments:** Skip N3 entirely (go N1→N2→N4→N5). Softer CTAs. ~100 word max.

#### 5c: Create Gmail Draft

Use `gmail_create_draft` with:
- `to`: contact's email address
- `subject`: step-specific subject line (must reference their business or a finding, never generic)
- `body`: the drafted email text

**Note:** If you can find the Gmail thread ID from the initial follow-up email (search for the most recent email to/from this contact), use it to keep the conversation in one thread. If not found, create a new thread.

#### 5d: Log to CRM

Use `create_lead_comment` for the lead:

```
[NURTURE] Step {N1-N5} drafted — "{theme_name}"
Subject: "{subject_line}"
Gmail draft created — review and send from drafts
Next: {next_step} due {next_date}
```

For the final step (N5), use:
```
[NURTURE] Step N5 drafted — "The Parking Lot"
Subject: "{subject_line}"
Gmail draft created — review and send from drafts
[NURTURE-COMPLETE] Sequence finished. If no response in 7 days, recommend moving to "Need Re-Activation".
```

### Step 6: Generate Summary

After processing all leads, output a clear summary:

```
## Nurture Run — {today's date}

### Drafted Today
- **{Company}** ({Contact}) — Step N{X}: "{theme}" | Subject: "{subject}"
- ...

### Skipped — Already Replied
- **{Company}** — Replied on {date}, sequence stopped

### Skipped — Not Due Yet
- **{Company}** — Next: N{X} due {date}

### Skipped — Paused/Complete
- **{Company}** — {reason}

### Warnings
- **{Company}** — No audit-data-lite.json found, cannot personalise

### Pipeline
- Active nurture sequences: {count}
- Drafts created today: {count}
- Sequences completed: {count}
- Leads needing data before nurture can start: {count}
```

### Step 7: Monthly Reactivation (N6)

After the main N1-N5 sequence, check for leads in "Need Re-Activation" that have `[NURTURE-COMPLETE]` tags.

For each:

1. **Check last N6 date** — scan comments for `[NURTURE-REACTIVATION]` tags. When was the last one?
2. **If 30+ days since last N6 (or since N5 completed):**
   a. Check for replies first (same as Step 3). If contact replied since last touch, add `[NURTURE-REPLIED]` and skip
   b. Check for opt-out language in their last reply ("don't contact", "stop emailing", "unsubscribe", "not interested"). If found, add `[NURTURE-OPTOUT]` and skip permanently
   c. Check how many N6 sends have been done. If 6 already, add `[NURTURE-EXPIRED]` and skip (6 month max)
   d. Load client data and previous N6 hooks from comments
   e. Write a fresh `{{reactivation_hook}}` that's different from all previous hooks for this contact
   f. Fill template `n6-monthly-reactivation.html`, create Gmail draft
   g. Log to CRM:
      ```
      [NURTURE-REACTIVATION] Monthly N6 (#X of 6) drafted
      Hook used: "{brief description of hook angle}"
      Subject: "{subject}"
      Gmail draft created. Next N6 due: {date +30 days}
      ```

3. **If not yet due:** skip, note in summary

**N6 is deliberately light.** Short email, one fresh hook, static guarantee reminder. The AI's job is just making the hook feel natural and different each time.

---

## Error Handling

- **MCP tool failure:** Log the error, skip the lead, continue with others. Report failures in summary.
- **Missing contact email:** Skip lead, log warning. Can't draft without an email address.
- **Multiple leads for same contact:** Only nurture the highest-value lead. Skip others with note.
