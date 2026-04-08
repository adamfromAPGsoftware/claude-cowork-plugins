# Email Template Reference

> **Source of truth:** `references/nurture-sequence-strategy.md` (within this skill folder)
> **HTML templates:** `{skill-root}/templates/`
>
> This file is a quick-reference for email drafting. The HTML templates in `templates/` (within this skill folder) are mostly static — the skill only fills in the dynamic `{{placeholders}}` marked in each template's HTML comments. For the full content strategy, scenario rules, and personalisation details, always load the strategy doc.

## HTML Template Files

| Step | File | Dynamic Placeholders |
|------|------|---------------------|
| N1 | `n1-the-one-thing.html` | client_name, waste_description, waste_quote, hours_per_week, staff_count, monthly_waste, annual_waste, meeting_date, close_page_url, booking_link |
| N2 | `n2-social-proof.html` | client_name, industry_hook, close_page_url, booking_link |
| N3 | `n3-the-hidden-cost.html` | client_name, primary_waste_description, primary_monthly_waste, secondary_waste_description, secondary_detail, secondary_monthly_waste, total_monthly_waste, total_annual_waste, quoted_price, close_page_url, booking_link |
| N4 | `n4-guarantee-reminder.html` | client_name, monthly_waste, annual_waste, quoted_price, close_page_url, booking_link |
| N5 | `n5-the-parking-lot.html` | client_name, primary_waste_description, monthly_waste, quoted_price, booking_link |
| N6 | `n6-monthly-reactivation.html` | client_name, reactivation_hook (AI-varied each month), quoted_price, close_page_url |

## Template Structure (All Steps)

```
Subject: {specific to their business or a finding — never generic}

Hey {first_name},

{Body — max 150 words, 100 for Scenario D}

{Sign-off — "Thanks," or "Talk soon,"}
Adam
{YOUR_COMPANY}
```

## Step Quick Reference

### N1 — "The One Thing" (Day 3)

**Data needed:** `top_waste_item.quote`, `top_waste_item.monthly_waste_aud`, `top_waste_item.description`, meeting date
**Subject pattern:** Reference the specific waste or quote — e.g. "That 12hrs/week at {company}"
**Body:** One specific thing from the call + dollar figure + soft CTA
**CTA:** "Want me to walk you through what the fix looks like?"

### N2 — "Social Proof" (Day 7)

**Data needed:** `industry_tag`, `positive_signals`
**Subject pattern:** Reference a similar company — e.g. "A support company your size cut 15hrs/week of admin"
**Body:** Brief case study matched to their industry + link to proof
**CTA:** Link to Gavin video testimonial or close page
**Case study matching:**
- Home services / trades → operations waste angle
- NDIS / support → admin burden angle
- Real estate → data/lead management angle
- Corporate → ROI / efficiency angle

### N3 — "The Hidden Cost" (Day 12)

**Data needed:** `waste_items[1]`, `waste_items[2]`, total waste calculation
**Subject pattern:** Reference the secondary waste — e.g. "The quoting problem is actually costing you more"
**Body:** 2nd/3rd waste item + total figure combining all known waste
**CTA:** "The audit maps all of it"
**Skip if:** Only 1 waste item OR Scenario D

### N4 — "Guarantee Reminder" (Day 17)

**Data needed:** `top_waste_item.monthly_waste_aud`, annualised figure
**Subject pattern:** Reference the guarantee — e.g. "$0 risk on a ${monthly}/month problem"
**Body:** Acknowledge $3K, state guarantee, frame the math
**CTA:** "The math is pretty simple"
**Shortest email in the sequence**

### N5 — "The Parking Lot" (Day 21)

**Data needed:** `top_waste_item` reference (one last time)
**Subject pattern:** Low-pressure — e.g. "Last one from me"
**Body:** Graceful exit, acknowledge the follow-up, reference #1 pain, door open
**CTA:** None — "you know where to find me"
**Mark [NURTURE-COMPLETE] after this step, lead moves to "Need Re-Activation"**

### N6 — "Monthly Reactivation" (Every 30 days after N5)

**Data needed:** `top_waste_item`, `industry_tag`, `waste_items[]`, previous N6 hooks (from CRM comments)
**Subject pattern:** Varies each month. Never generic, always references their business.
**Body:** Short. AI-written `{{reactivation_hook}}` (1-2 sentences, unique each month) + static guarantee/price reminder
**CTA:** Close page link + booking link
**Hook rotation:** waste compound, industry trend, demo/case study, ROI reminder, timely/seasonal, final check-in
**Auto-stops after 6 monthly sends or any reply/opt-out**
**Track each hook used in CRM comment so it's never repeated**

## Voice Checklist (Run After Every Draft)

1. Under 150 words? (100 for Scenario D)
2. Contractions used throughout?
3. At least one natural qualifier? ("just", "probably", "roughly")
4. No forbidden phrases? (leverage, utilize, facilitate, furthermore, etc.)
5. No bold text in body?
6. No bullet points?
7. References specific client data, not generic statements?
8. "Would Adam copy-paste this into Gmail without editing?"
