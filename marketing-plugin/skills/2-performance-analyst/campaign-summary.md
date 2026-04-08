---
name: campaign-summary
description: Summarize campaign performance by date range
menu-code: CS
---

# Campaign Summary

Summarize campaign performance from marketing-data.json by date range.

## Process

1. **Determine scope:**
   - If user specified a date range (e.g., "last 7 days", "March 2026"), filter insights to that range
   - Default: all available data

2. **Load marketing-data.json** — Read campaign structure and insights

3. **Filter insights to campaign level:**
   - Select insights where `entity_type` = "campaign"
   - Filter by date range if specified

4. **Aggregate by campaign:**

   ```
   CAMPAIGN SUMMARY — {date_range}
   
   Total: ${total_spend} spent | {total_impressions} impressions | {total_clicks} clicks
   
   | Campaign              | Status | Spend     | Impr      | Clicks | CTR    | CPC    | CPM     | Conv | Cost/Conv | ROAS  |
   |-----------------------|--------|-----------|-----------|--------|--------|--------|---------|------|-----------|-------|
   | Brand Awareness       | ACTIVE | $1,234    | 45,000    | 890    | 1.98%  | $1.39  | $27.42  | 12   | $102.83   | 3.2x  |
   | Lead Gen - Retarget   | ACTIVE | $890      | 22,000    | 450    | 2.05%  | $1.98  | $40.45  | 8    | $111.25   | 2.8x  |
   | ...                   |        |           |           |        |        |        |         |      |           |       |
   | TOTALS                |        | $2,124    | 67,000    | 1,340  | 2.00%  | $1.59  | $31.70  | 20   | $106.20   | 3.0x  |
   ```

5. **Sort by spend** (highest first)

6. **Include totals row** with weighted averages for rate metrics (CTR, CPC, CPM)

7. **Flag notable items:**
   - Campaigns with zero conversions but spend > $100
   - Campaigns with CPC > 2x the account average
   - Campaigns with CTR < 0.5% (potential creative fatigue)
   - Paused campaigns that still have recent spend data

## Output

Present the full summary as a structured table. Include the date range in the header. If data spans fewer than 7 days, note that trends may be unreliable.
