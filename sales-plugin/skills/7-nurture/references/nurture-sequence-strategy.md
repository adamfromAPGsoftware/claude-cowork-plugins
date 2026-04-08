# Post-Discovery Nurture Sequence

> **Purpose:** Systematically re-engage prospects after a discovery call who haven't committed to the $3,000 audit. Every email references their actual discovery conversation — specific pain points, waste figures, and quotes — so nothing feels generic.
>
> **How it works:** A scheduled skill runs each weekday morning. It checks which leads need a nurture email, drafts it in Gmail (never auto-sends), and logs what it did in the CRM. Adam or the sales team reviews and sends manually.

---

## The Sequence — 5 Emails Over 21 Days

Each email has one job. No email repeats the pitch. The sequence builds value progressively, then exits gracefully if there's no response.

---

### Email 1 — "The One Thing"

**When:** Day 3 after initial follow-up email

**Objective:** Mirror their biggest pain back to them with a real number. Prove you were listening.

**Content strategy:**
- Open by quoting something specific they said in the discovery call — a process they described, a frustration they expressed, a number they mentioned
- One sentence connecting that to a dollar figure: "At X hrs/week across Y staff, that's roughly $Z/month"
- Don't pitch the audit — just ask if they want to see what the fix looks like

**CTA:** "Want me to walk you through what the fix looks like?"

**Personalisation sources:**
- `top_waste_item.quote` — their exact words from the call
- `top_waste_item.monthly_waste_aud` — the calculated waste figure
- `top_waste_item.description` — what the waste is
- Meeting date — "when we chatted on [date]"

**Example angle (not final copy):**
> Hey Dale,
>
> You mentioned your team spends about 3 hours a day just moving data between Monday and Xero — that's roughly $4,200/month across 4 staff. And that's just one process.
>
> Want me to walk you through what the fix looks like? It's simpler than you'd think.

---

### Email 2 — "Social Proof"

**When:** Day 7 after initial follow-up email

**Objective:** Show them someone like them had the same problem and fixed it. Reduce the "am I the only one?" anxiety.

**Content strategy:**
- Open with a reference to a similar business (matched by industry or company size)
- 1-2 sentence case study: what the problem was, what we did, what changed
- Link to social proof (video testimonial, Upwork profile, or close page)
- Reference something positive they said in the call to keep the tone warm

**CTA:** Link to Gavin's video testimonial or their close page

**Personalisation sources:**
- `industry_tag` — match to the most relevant case study
- `positive_signals` — moments of enthusiasm from the call
- Company size — for "a business about your size" framing

**Social proof assets available:**

| Asset | Best for | Link/Location |
|-------|----------|---------------|
| {TESTIMONIAL_NAME} video testimonial | All industries — strong "under budget, within timeframes" quote | `{YOUR_CDN_HOST_2}` |
| Upwork profile | Credibility — 60+ projects, Top 1%, {YOUR_CREDENTIAL} | {YOUR_UPWORK_URL} |
| YouTube channel | AI/tech credibility — 200K+ views | youtube.com/@AdamGoodyer |
| Skool community | Community proof — {YOUR_MEMBER_COUNT}+ members | {YOUR_COMMUNITY_URL} |
| Post-discovery close page | Full pitch with value stack + guarantee | Client-specific URL from `clients/clients.json` |

**Example angle (not final copy):**
> Hey Dale,
>
> We worked with a support services company about your size — same problem, team drowning in admin between their CRM and accounting. After the audit they cut 15 hours a week of manual data entry. No new staff, just better systems.
>
> Gavin from {TESTIMONIAL_COMPANY} said it best — "we did it at well under budget and within timeframes." Worth a quick watch: [link]

---

### Email 3 — "The Hidden Cost"

**When:** Day 12 after initial follow-up email

**Objective:** Expand the opportunity beyond what they focused on in the call. Show there's more waste than they realised.

**Content strategy:**
- Open with "we only scratched the surface" framing
- Surface the 2nd and/or 3rd waste item they didn't focus on during the call
- Total up: "Between [thing 1] and [thing 2], that's roughly $X/month"
- Position the audit as the way to map ALL of it

**CTA:** "The audit maps all of it — and the $3K pays for itself in the first month of savings"

**Personalisation sources:**
- `waste_items[1]` and `waste_items[2]` — secondary waste items with figures
- `pain_points[]` — additional pain points mentioned but not dwelled on
- Total waste calculation across all items

**Skip condition:** If only 1 waste item exists in the data, skip this email entirely and move to Email 4.

**Example angle (not final copy):**
> Hey Dale,
>
> We talked a lot about the data entry problem on our call — but there's another one that's probably costing you more. Your quoting process takes about 45 mins per job, and at 30 quotes a week that's roughly $3,800/month just in quoting time.
>
> Between that and the data entry, you're looking at close to $8K/month. The audit maps all of it — every process, every cost, every fix.

---

### Email 4 — "Guarantee Reminder"

**When:** Day 17 after initial follow-up email

**Objective:** Remove the last barrier — risk. Make the math obvious.

**Content strategy:**
- Acknowledge that $3K is real money
- State the guarantee clearly: if we don't find $5K/month in savings, full refund
- Frame the math: $3K to find $60K+/year, or $0 if we're wrong
- Keep it short — this email should be the shortest in the sequence

**CTA:** "The math is pretty simple — $3K to find $X/year, or $0 if we're wrong"

**Personalisation sources:**
- `top_waste_item.monthly_waste_aud` — their specific monthly figure
- Annualised total — monthly x 12 for impact framing
- Company size — for "a business your size" credibility

**Example angle (not final copy):**
> Hey Dale,
>
> I know $3K is $3K. So here's how we de-risk it completely: if the audit doesn't find at least $5,000/month in savings, you don't pay. Full refund. You keep everything we find.
>
> You're looking at roughly $8K/month in waste we already spotted — and that was just from one conversation. The audit goes deeper. $3K to find $96K/year, or $0 if we're wrong.

---

### Email 5 — "The Parking Lot"

**When:** Day 21 after initial follow-up email

**Objective:** Exit gracefully. No pressure. Leave the door open without being annoying.

**Content strategy:**
- Acknowledge the follow-up directly — "I don't want to be that person"
- Reference their #1 pain point one last time as a reminder of what's at stake
- Make it clear the offer stands whenever they're ready
- No CTA link — just "you know where to find me"

**CTA:** None — just a warm sign-off

**After this email:** Mark the 21-day sequence complete. Move lead to "Need Re-Activation" stage. The monthly reactivation email (N6) kicks in automatically 30 days later.

**Example angle (not final copy):**
> Hey Dale,
>
> I don't want to be that person who keeps following up — so this is the last one. If timing's not right, I totally get it.
>
> But that $4,200/month in manual data entry isn't going anywhere — it just compounds. When you're ready to tackle it, the offer stands. You know where to find me.
>
> Thanks,
> Adam

---

### Email 6 — "Monthly Reactivation"

**When:** Every 30 days after N5 completes (for leads in "Need Re-Activation")

**Objective:** Keep the door open with a light monthly touch. Not a pitch, just a reminder you exist and the offer stands.

**Content strategy:**
- Short email. The `{{reactivation_hook}}` is the only part that changes each month
- The AI writes a fresh 1-2 sentence hook each time, rotating through different angles so it never feels repetitive
- Static reminder of the guarantee and price, booking link, close page CTA

**Hook rotation (AI varies each month, tracked in CRM comments):**
- Month 1: Reference their original #1 waste item and how it compounds over time
- Month 2: Share an industry insight or trend relevant to their business
- Month 3: Reference the demo or a new case study
- Month 4: Quick ROI reminder with their specific numbers
- Month 5: Something timely (end of financial year, new quarter, seasonal)
- Month 6: Final "just checking in, offer still stands" then auto-stop

**Auto-stop conditions:**
- Contact replies (any reply at all, including "not interested")
- Contact explicitly opts out ("don't contact me", "stop emailing", "unsubscribe")
- Lead moves to Won/Lost/Disqualified
- Manual pause via `[NURTURE-PAUSED]`
- 6 months of no response (auto-stop after 6 monthly sends)

**CTA:** Close page link + booking link

---

## Scenario Detection

Not every lead gets the same timing. The system detects which scenario a lead is in and adjusts accordingly.

### Scenario A — Ghosting (Default)

**Signal:** No reply to initial follow-up. No CRM activity. Radio silence.

**Timing:** Standard — Days 3, 7, 12, 17, 21

**Tone:** Normal energy, assume they're busy not disinterested.

---

### Scenario B — "Follow Up Later" (1-2 Weeks)

**Signal:** Lead comment or email contains explicit timing — "follow up in a couple of weeks", "let me think about it for a week", "I'll get back to you next week"

**Timing:** Delay sequence start to their requested date. Then standard gaps from there (Days 0, 4, 9, 14, 18 from the delayed start).

**Tone:** Normal — they asked for time, respect it, then proceed.

---

### Scenario C — Long Delay (Month+)

**Signal:** Lead comment or email says "follow up in a month", "maybe after Easter", "Q3", "not right now but keep in touch"

**Timing:** Delay start to their requested date. Compress remaining emails to 5-day gaps instead of the standard spacing (Days 0, 5, 10, 15, 20 from delayed start).

**Tone:** Slightly warmer, acknowledge the time gap — "I know it's been a while since we chatted"

---

### Scenario D — Cooling Off

**Signal:** Meeting cancellations, rescheduling multiple times, vague excuses in comments ("something came up", "really busy right now"), declining call-backs

**Timing:** Standard gaps but skip Email 3 (The Hidden Cost) — don't pile on with more waste figures when they're already pulling away.

**Tone:** Lighter touch. ~100 words max instead of 150. Softer CTAs. More "no pressure" energy throughout.

---

## Automatic Stop Conditions

The sequence stops immediately if ANY of these occur:

1. **Lead replies** — detected via Gmail search. Human takes over the conversation.
2. **Lead converts** — stage changes to "Won" or "Proposal" or "Negotiation"
3. **Lead lost** — stage changes to "Lost" or "Disqualified"
4. **Manual pause** — Adam or sales team adds a `[NURTURE-PAUSED]` comment
5. **Lead has a meeting scheduled** — detected via Fathom or calendar activity
6. **Insufficient data** — no `audit-data-lite.json` exists (skip with warning, don't send generic emails)

---

## Tracking

Every action is logged as a CRM lead comment so it's visible to the whole team:

**When the sequence starts:**
```
[NURTURE-START] Scenario A (Ghosting) — 5-email sequence initiated
Schedule: N1 Apr 4, N2 Apr 8, N3 Apr 13, N4 Apr 18, N5 Apr 22
```

**When each email is drafted:**
```
[NURTURE] Step N2 drafted — "Social Proof"
Subject: "A support company your size cut 15hrs/week of admin"
Gmail draft created — review and send from drafts
Next: N3 due Apr 13
```

**When the sequence ends:**
```
[NURTURE-COMPLETE] Sequence finished — no reply after 5 emails
Recommendation: Move to "Need Re-Activation" in 7 days if no response
```

---

## Voice Rules (Quick Reference)

All emails must follow Adam's voice. Full rules in `shared-references/adam-email-voice.md`.

**Non-negotiable:**
- Max 150 words (100 for Scenario D)
- Greeting: "Hey {first_name}," (default) or "Hi {first_name}," (corporate only)
- Contractions mandatory — don't, that's, you're, we've
- At least one natural qualifier per email — "just", "probably", "roughly"
- No bold text in body
- No bullet points
- Sign-off: "Thanks," or "Talk soon," then "Adam" then "{YOUR_COMPANY}"

**Forbidden (never use):**
leverage, utilize, facilitate, furthermore, additionally, feel free to reach out, I hope this helps, delve into, seamless, comprehensive, going forward, innovative, game-changing, please don't hesitate

**Industry tone calibration:**
- Home services / trades: plain, direct, no jargon
- NDIS / support work: warm but specific
- Real estate / property: professional, numbers-forward
- Corporate / professional services: crisp, ROI-framed

---

## HTML Email Templates

All 6 emails have HTML templates at `templates/` (within this skill folder):

| Step | Template | Static Content | Dynamic Placeholders |
|------|----------|---------------|---------------------|
| N1 | `n1-the-one-thing.html` | branding, sign-off, booking link | waste_quote, waste_description, hours_per_week, staff_count, monthly_waste |
| N2 | `n2-social-proof.html` | All 3 video testimonials, Upwork/YouTube/Skool/Trustpilot proof, audit demo link | industry_hook (one sentence) |
| N3 | `n3-the-hidden-cost.html` | Value stack (6 deliverables), branding | primary/secondary waste descriptions and figures |
| N4 | `n4-guarantee-reminder.html` | Full guarantee terms, risk reversal block | monthly_waste, annual_waste |
| N5 | `n5-the-parking-lot.html` | Soft reminder block, no-expiry booking link | primary_waste_description, monthly_waste |

Templates use `{{placeholder}}` syntax. The skill reads the template, fills in dynamic values from `audit-data-lite.json`, and creates a Gmail draft with the rendered HTML.

### Static assets embedded in templates:
- **{TESTIMONIAL_NAME}** video testimonial + thumbnail (N2)
- **Dan Benyamin** video testimonial + thumbnail (N2)
- **{CASE_STUDY_SUBJECT} Fay** video testimonial + thumbnail (N2)
- **Upwork profile** screenshot — 60+ projects, Top 1%, {YOUR_CREDENTIAL} (N2)
- **YouTube** — 200K+ views (N2)
- **Skool community** — {YOUR_MEMBER_COUNT}+ members (N2)
- **Trustpilot** — Excellent rating (N2)
- **Audit demo** — https://your-portal.example.com/demo-example (N2)
- **Booking link** — https://link.nilsdigital.com/widget/bookings/adam-goodyear-personal-calendar-bhue8bspw (all emails)
- **logo** — Cloudflare R2 hosted (all emails)

---

## Editing This Document

This document is the source of truth for the nurture sequence. To change the sequence:

- **Change timing:** Edit the "When" field on any email
- **Change content strategy:** Edit the "Content strategy" section of the relevant email
- **Add/remove emails:** Add or remove an email section and update the numbering
- **Change scenario rules:** Edit the relevant scenario section
- **Update social proof:** Edit the social proof assets table in Email 2
- **Change stop conditions:** Edit the "Automatic Stop Conditions" section
- **Change voice rules:** Edit `shared-references/adam-email-voice.md` (applies to all client-facing output, not just nurture)

After editing, the scheduled skill will pick up changes on its next run — no code changes needed.
