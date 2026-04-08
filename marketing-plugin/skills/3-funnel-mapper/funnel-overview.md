---
name: funnel-overview
description: Show end-to-end funnel metrics for each campaign
menu-code: FO
---

# Funnel Overview

Show end-to-end metrics from ad spend through to conversions for each campaign.

## Process

1. **Load marketing-data.json** — Read campaign structure and insights

2. **Filter insights to campaign level:**
   - Select insights where `entity_type` = "campaign"
   - Aggregate across all dates (or filter by user-specified range)

3. **For each campaign, aggregate:**
   - Total spend
   - Total impressions
   - Total clicks
   - Total conversions (from `conversions` field or sum of conversion-type actions)
   - Breakdown of actions array by type (link_click, landing_page_view, lead, purchase, etc.)

4. **Calculate funnel metrics:**
   - Click-through rate: clicks / impressions
   - Cost per click: spend / clicks
   - Conversion rate: conversions / clicks
   - Cost per conversion (CPL): spend / conversions
   - ROAS where available

5. **Present as funnel table:**

   ```
   FUNNEL OVERVIEW — {date_range}
   
   | Campaign              | Spend     | Impressions | Clicks | CTR    | CPC    | Conversions | Conv Rate | CPL       | ROAS  |
   |-----------------------|-----------|-------------|--------|--------|--------|-------------|-----------|-----------|-------|
   | Lead Gen - Retarget   | $890      | 22,000      | 450    | 2.05%  | $1.98  | 15          | 3.33%     | $59.33    | 2.8x  |
   | Brand Awareness       | $1,234    | 45,000      | 890    | 1.98%  | $1.39  | 12          | 1.35%     | $102.83   | 3.2x  |
   | Cold Traffic - Broad  | $650      | 30,000      | 275    | 0.92%  | $2.36  | 3           | 1.09%     | $216.67   | 0.8x  |
   | Engagement Campaign   | $340      | 18,000      | 260    | 1.44%  | $1.31  | 0           | 0.00%     | N/A       | 0.0x  |
   | TOTALS                | $3,114    | 115,000     | 1,875  | 1.63%  | $1.66  | 30          | 1.60%     | $103.80   | 2.4x  |
   ```

6. **Flag campaigns with wasted budget:**
   - Campaigns with $0 conversions but spend > $50 — highlight as "spend without results"
   - Campaigns where CPL is > 3x the account average
   - Campaigns with high CTR but low conversion rate (potential landing page issue)
   - Campaigns with low CTR (potential creative or audience issue)

7. **Show actions breakdown** for campaigns with conversion data:

   ```
   CONVERSION ACTIONS BREAKDOWN
   
   | Campaign              | link_click | landing_page_view | lead | purchase | other |
   |-----------------------|------------|-------------------|------|----------|-------|
   | Lead Gen - Retarget   | 450        | 320               | 15   | 0        | 0     |
   | Brand Awareness       | 890        | 610               | 12   | 0        | 0     |
   ```

8. **Note Phase 2 gap:**
   > Phase 1 limitation: Conversion data comes from Meta's tracking pixel only. On-site behavior between ad click and conversion is invisible. Phase 2 will add GA4 landing page data to show the full journey: ad click → landing page → form submission → conversion.

## Output

Present the funnel table sorted by spend (highest first). Include the flags section and Phase 2 note. If no campaigns have conversion data, emphasize this and suggest verifying that Meta pixel/conversion tracking is configured.
