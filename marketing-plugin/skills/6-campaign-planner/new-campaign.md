---
name: new-campaign
description: Create a new campaign — define product, audience, buying triggers, and campaign config
menu-code: NC
---

# New Campaign

Create a new campaign entry in campaign-data.json. This is LLM-driven — the agent walks the user through defining their campaign.

## Process

1. **Ask for the product/service:**
   - "What product or service is this campaign for?"
   - "What's the price point?"
   - "What's the offer — what does the prospect get?"
   - "Any guarantee or risk reversal?"
   - "What are the unique selling propositions?"

2. **Define the audience:**
   - "Who is your ideal customer? (industry, role, company size)"
   - "What are their main pain points?"
   - "What do they aspire to?"
   - "What triggers them to buy NOW? (events, frustrations, deadlines)"
   - "What locations are you targeting?"
   - "What age range?"

3. **Set campaign config:**
   - "What subdomain should we use? (e.g., audit.{YOUR_DOMAIN})"
   - "What landing page template? (lead-gen, webinar, case-study, quiz)"
   - "What daily budget are you planning?"
   - "What's the campaign objective? (leads, traffic, awareness)"

4. **Generate campaign_id** — Format: `camp-YYYY-MM-DD-NNN` where NNN is a sequence number for that date.

5. **Create the campaign entry** in campaign-data.json with all sections populated:
   - product, audience, intelligence (empty), creatives (empty), performance (defaults), landing_page (config from step 3), tracking (UTMs from campaign name), meta_campaign (not_created), lead_capture (defaults), approval_log (empty)
   - Status: `draft`

6. **Update meta** — Increment total_campaigns, set last_created.

7. **Present summary:**

```
Campaign created: {campaign_id}
Name: {name}
Product: {product.name}
Audience: {icp_description}
Subdomain: {domain}
Template: {template}
Budget: ${daily_budget}/day

Status: draft
Next: Run [MR] to generate a market intelligence report.
```
