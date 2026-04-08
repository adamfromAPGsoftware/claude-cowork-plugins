---
name: generate-followup-comms
description: Post-call personalised follow-up email and SMS text message
menu-code: GFE
---

# Generate Follow-Up Comms

## Purpose

Write a short, direct follow-up email AND an SMS text message that land within 1 hour of the discovery call. The email mirrors the client's exact words, links to the close page, and stays under 150 words. The SMS is a short nudge to check the email. No platitudes.

## Process

### Step 1: Load Inputs

1. **Client slug** — Ask if not in session context
2. **Load audit-data-lite** — Read `clients/{slug}/audit/audit-data-lite.json`
3. **Close page URL** — Read `close_url` from `clients/clients.json` for the client's key. If client is not yet in `clients/clients.json`, use placeholder `[CLOSE PAGE URL]`

Key fields to extract from audit data-lite:
- `contact.name` — client's first name
- `top_waste_item` — description, monthly_waste_aud, quote
- `industry_tag` — for tone calibration
- `positive_signals` — moments of enthusiasm to reference

### Step 2: Draft Email

#### Voice — Load Before Drafting

Read `shared-references/adam-email-voice.md` for the complete email voice reference. The rules below are the non-negotiable subset — the voice reference has the full forbidden phrases table and structural anti-patterns.

**Hard rules — enforce without exception:**
- Maximum 150 words (body only, not subject)
- Subject line must reference their specific business or a specific finding — no generic phrases
- Banned subject lines: "Following up on our call", "Great chatting today", "Next steps from our conversation"
- Opening: use their first name, reference something *specific* they said — not the call itself
- Body: single waste figure + context in one sentence
- CTA: one link, one sentence
- No "I hope this email finds you well" or equivalent
- No bullet points
- No bold text in body
- Contractions mandatory — "don't", "that's", "you're", "we've". Never "do not", "that is", "you are", "we have"
- Include at least one natural qualifier — "just", "probably", "roughly" — to prevent robotic tone
- **Forbidden phrases (hard block):** "leverage", "utilize", "facilitate", "furthermore", "additionally", "feel free to reach out", "I hope this helps", "delve into", "seamless", "comprehensive", "going forward", "it's important to note", "innovative", "game-changing", "please don't hesitate". If any appear, rewrite that sentence.

**Email format:**

```
Subject: {specific to their business or finding}

Hey {first_name},

{One sentence referencing something specific from the call — a number they mentioned, a process they described, a pain they expressed. Not "it was great to meet you" — something that proves you were listening.}

{Single waste figure sentence: "At {hrs}/week across {headcount} staff, that's roughly ${monthly}/month in {waste_type} — and that's before we look at {another_stage}."}

I've put together a short breakdown with the numbers and 2–3 quick wins:
{close_page_url}

If a full audit doesn't find $5K/month in savings, you pay nothing — and you keep everything we find.

Thanks,

Adam
{YOUR_COMPANY}
```

**Greeting calibration:** Use `Hey {first_name},` for most contacts (the default post-discovery). Use `Hi {first_name},` only if `industry_tag` is corporate/professional-services AND this is the very first email.

**Calibrate tone to industry:**
- Home services / construction / trades: plain, direct, no jargon
- NDIS / support work: warm but still specific and fast
- Real estate / property: professional, numbers-forward
- Corporate / professional services: crisp, ROI-framed

#### Voice-Check Gate

After drafting, re-read the email and ask: **"Would Adam copy-paste this into Gmail without editing?"** If any sentence sounds corporate, stiff, or AI-generated — rewrite it. Then scan against the forbidden phrases list one more time.

### Step 3: Present for Review

Show the draft. Ask: "Any changes before I save this?"

### Step 4: Save

Save to: `clients/{slug}/follow-up/discovery-follow-up-email.md`

Output format in the file:
```markdown
# Discovery Follow-Up Email — {company_name}
**Date:** {date}
**To:** {contact_name}

**Subject:** {subject_line}

---

{email_body}
```

Confirm: "Email saved to `clients/{slug}/follow-up/discovery-follow-up-email.md`. Subject line and body are ready to copy."

### Step 5: Draft SMS Text Message

Write a short SMS nudge (under 160 characters) to complement the email:

**SMS rules:**
- Under 160 characters (one SMS segment)
- No links — just a nudge to check their email
- Use their first name
- Reference something specific from the call (not generic)
- Casual, personal tone — like a text from someone you just met
- No sign-off needed (SMS convention)

**SMS format:**
```
Hey {first_name}, just sent through the breakdown from our chat — worth a look at the numbers. Adam
```

**Variations by tone:**
- Trades/home services: `Hey {first_name}, sent you that breakdown we talked about — some interesting numbers in there. Adam`
- NDIS: `Hey {first_name}, just emailed the summary from our conversation — take a look when you get a sec. Adam`
- Corporate: `Hi {first_name}, just sent the analysis from our discussion — the waste figures are worth reviewing. Adam`

Present the SMS for review alongside the email.

### Step 6: Save SMS

Save to: `clients/{slug}/follow-up/discovery-follow-up-sms.txt`

Just the raw SMS text — no headers or formatting.

Confirm: "Email and SMS saved to `clients/{slug}/follow-up/`. Both ready to send."

## CRM Lead Update

After saving email and SMS, if `crm.lead_id` is set:

1. `get_lead(lead_id)` → check current stage
2. If stage is "Discovery Call - Completed": `update_lead(lead_id, stage: "Negotiation")`
3. If stage is manual: add lead comment instead, do NOT override stage
4. `create_lead_comment(lead_id, content)`:
   ```
   Follow-up email and SMS drafted.
   Email saved to: clients/{slug}/follow-up/discovery-follow-up.html
   SMS saved to: clients/{slug}/follow-up/discovery-follow-up-sms.txt
   ```
5. Best-effort — if CRM calls fail, log warning and continue.
