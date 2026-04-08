---
name: link-performance
description: Link generated creatives to their Meta ad IDs and pull performance data back to close the feedback loop
menu-code: LP
---

# Link Performance

Connect generated angles to their Meta Ads Manager ad IDs, pull performance data, and store verdicts. This closes the feedback loop so future angle generation can learn from what worked and what didn't.

## Process

1. **Load creative-data.json** — Read `marketing-plugin/data/creative-data.json`. When `{active_campaign}` is set, filter batches to those with matching `campaign_id` and show only campaign-relevant batches. When `{active_campaign}` is null, show all batches. List matching batches with their status.

2. **Select batch** — Ask: "Which batch do you want to link? (show batch IDs with dates and angle counts)"

3. **Load marketing-data.json** — Read `marketing-plugin/data/marketing-data.json` for ad-level performance data.

4. **For each angle in the selected batch:**

   a. **Show the angle** — Display angle name, hook line, and copy variants so the user can identify it.

   b. **Ask for Meta ad IDs** — "What Meta ad ID(s) did you upload this angle as? (comma-separated if multiple, or 'skip' if not uploaded)"
      - The user gets ad IDs from Meta Ads Manager
      - Multiple IDs are common (one per copy variant × format combination)

   c. **Store the ad IDs** on the angle:
      ```json
      "meta_ad_ids": ["120242733238050535", "120242733174760535"],
      "uploaded_at": "2026-04-07T10:00:00Z"
      ```

5. **Pull performance data** — For each linked ad ID, find matching insights in marketing-data.json:
   - Filter insights where `entity_type == "ad"` and `entity_id` matches the ad ID
   - Aggregate across the date range since upload
   - Calculate: spend, impressions, clicks, CTR, CPC, conversions, CPA

6. **Calculate verdict** — Use the same dynamic percentile thresholds as the daily report:
   - Gather all ad-level insights for the same date range
   - Compute 25th/75th percentile for CTR and CPC
   - Classify each angle's aggregate performance:
     - `"winner"` — top 25% CTR AND bottom 25% CPC
     - `"loser"` — bottom 25% CTR OR top 25% CPC
     - `"okay"` — everything else
     - `"insufficient_data"` — less than $10 total spend

7. **Store performance snapshot** on the angle:

   ```json
   "performance_snapshot": {
     "date_range": "2026-04-07 to 2026-04-14",
     "ad_count": 2,
     "spend": 150.00,
     "impressions": 12000,
     "clicks": 180,
     "ctr": 1.50,
     "cpc": 0.83,
     "conversions": 3,
     "cpa": 50.00,
     "roas": 0,
     "verdict": "winner",
     "snapshot_date": "2026-04-15T10:00:00Z"
   }
   ```

8. **Save creative-data.json** with updated angles.

9. **Present results:**

   ```
   Performance Link Complete — Batch: {batch_id}

   | Angle | Framework | Ad IDs | Spend | CTR | CPC | Conv | Verdict |
   |-------|-----------|--------|-------|-----|-----|------|---------|
   | {name} | {framework} | {count} | ${spend} | {ctr}% | ${cpc} | {conv} | WINNER |
   | ... |

   Thresholds: Winner CTR >= {thr}% & CPC <= ${thr} | Loser CTR < {thr}% or CPC > ${thr}

   Winners: {count} — replicate these patterns in next batch
   Losers: {count} — avoid these patterns
   Insufficient data: {count} — need more spend before judging

   Next: Run [BA] to generate new angles informed by these results.
   ```

## Re-Linking

If performance data is re-linked (e.g., checking again after more time), the performance snapshot is updated (not appended). The `snapshot_date` records when the link was last refreshed.

## Principles

- Performance linking is manual and intentional — the user decides when to check results
- Verdicts are relative to the account's own performance, not absolute thresholds
- Angles with insufficient spend ($10 minimum) are not judged — they need more data
- The feedback loop only works if this capability is used regularly after each upload cycle
