---
name: ad-set-breakdown
description: Break down performance at ad set level for a specific campaign
menu-code: AS
---

# Ad Set Breakdown

Break down performance at the ad set level for a specific campaign.

## Process

1. **Identify campaign:**
   - If user specified a campaign name or ID, use that
   - If not, list all campaigns with their spend and ask which to analyze:
     ```
     Which campaign would you like to break down?
     
     | # | Campaign              | Status | Total Spend |
     |---|-----------------------|--------|-------------|
     | 1 | Brand Awareness       | ACTIVE | $1,234      |
     | 2 | Lead Gen - Retarget   | ACTIVE | $890        |
     | 3 | ...                   |        |             |
     ```

2. **Load ad sets for the selected campaign:**
   - Filter `meta.ad_sets` by `campaign_id`
   - Filter insights where `entity_type` = "ad_set" and `entity_id` matches

3. **Aggregate insights by ad set:**

   ```
   AD SET BREAKDOWN — {campaign_name}
   Date range: {date_range}
   
   | Ad Set                | Status | Targeting              | Spend   | Impr    | Clicks | CTR    | CPC    | Conv | Cost/Conv |
   |-----------------------|--------|------------------------|---------|---------|--------|--------|--------|------|-----------|
   | 25-44 Interest Based  | ACTIVE | 25-44, Interest: Fitness| $650   | 25,000  | 520    | 2.08%  | $1.25  | 8    | $81.25    |
   | 18-24 Lookalike       | ACTIVE | 18-24, Lookalike 1%    | $584    | 20,000  | 370    | 1.85%  | $1.58  | 4    | $146.00   |
   ```

4. **Compare targeting across ad sets:**
   - Note which targeting approaches yield the best CTR and CPC
   - Identify audience overlap risks if targeting descriptions suggest similar audiences

5. **Identify best and worst performers:**
   - Best: lowest cost per conversion (with minimum 3 conversions)
   - Worst: highest spend with zero or lowest conversions
   - Note any ad sets with significantly different performance from siblings

## Output

Present the breakdown as a structured table with targeting context. Highlight the best and worst performing ad sets with specific metric comparisons.
