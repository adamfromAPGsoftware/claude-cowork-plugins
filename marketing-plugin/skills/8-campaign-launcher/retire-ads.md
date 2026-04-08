---
name: retire-ads
description: Pause underperforming ads identified by Performance Review
menu-code: RA
---

# Retire Ads — Pause Underperformers

Pause underperforming ads in Meta that have been flagged by the Performance Analyst. Maps angle IDs from campaign-data.json to Meta ad IDs and pauses them.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Retiring ads for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, list campaigns from `campaign-data.json` that have status `live`. Ask user to select one.

2. **Read retired angles** — From the selected campaign in `campaign-data.json`, read `retired_angle_ids[]`. These are populated by the Performance Analyst's review process.

   If no retired angles found:
   ```
   No ads flagged for retirement in this campaign.
   Run Performance Review [PR] first to identify underperformers.
   ```

3. **Map to Meta ad IDs** — For each `angle_id` in `retired_angle_ids`:
   - Look up the angle in `creative-data.json`
   - Find all creatives for that angle
   - Get their `meta_ad_id` from the creative or from `marketing-data.json`

   Present the mapping:
   ```
   Ads to retire:
   {For each ad:}
   - Angle: {angle_name} ({angle_id})
     Ad ID: {meta_ad_id}
     Performance: CTR {ctr}%, CPA ${cpa}, Spend ${spend}
   ```

4. **Dry run** — Run:
   ```
   python3 marketing-plugin/scripts/pause-meta-ads.py --ad-ids {comma_separated_ids} --dry-run
   ```

5. **APPROVAL GATE** —
   ```
   ═══ APPROVAL GATE: Retire Ads ═══

   Pause {count} underperforming ads?
   {For each ad: ad_id, angle_name, performance summary}

   [yes / no]
   ```

6. **On approval** — Run:
   ```
   python3 marketing-plugin/scripts/pause-meta-ads.py --ad-ids {comma_separated_ids} --execute
   ```

7. **Update data files:**
   - Update `creative-data.json`: mark affected creatives as `status: "paused"`
   - Update `campaign-data.json`: remove from `retired_angle_ids`, add to `paused_angle_ids`

8. **Log to api-log.md** — Record all pause operations.

9. **Present result:**
   ```
   {count} ads paused in Meta.

   {For each paused ad:}
   - {ad_id} ({angle_name}) — PAUSED

   Remaining active ads: {remaining_count}
   
   Consider generating fresh creatives with Creative Generator [BA] to replace retired angles.
   ```
