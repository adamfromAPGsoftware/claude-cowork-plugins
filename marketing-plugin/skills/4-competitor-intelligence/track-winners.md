---
name: track-winners
description: Calculate days_active for all tracked ads, categorise by longevity tier, and highlight new winners
menu-code: TW
---

# Track Winners

Calculate `days_active` for all tracked ads, categorise by longevity tier, and highlight new winners (30+ days).

## Process

1. **Load competitor-data.json** — Read `{project-root}/marketing-plugin/data/competitor-data.json`

2. **Calculate longevity for each ad:**
   - `days_active` = today - `first_seen` (if `last_seen` is within the last 7 days, ad is still running)
   - If `last_seen` is older than 7 days, ad is considered stopped: `days_active` = `last_seen` - `first_seen`

3. **Categorise each ad into a longevity tier:**

   | Tier | Days Active | Meaning |
   |------|-------------|---------|
   | New | < 7 days | Just launched, too early to judge |
   | Testing | 7 - 29 days | In testing phase, not yet proven |
   | Winner | 30 - 59 days | Probable winner — survived testing |
   | Super Winner | 60+ days | Confirmed winner — long-running proven ad |
   | Stopped | last_seen > 7 days ago | No longer active |

4. **Present longevity table** — Group by competitor, sorted by days_active descending:

   ```
   {competitor_name}
   | Ad ID | Format | Hook Type | Days Active | Tier | First Seen | Last Seen |
   |-------|--------|-----------|-------------|------|------------|-----------|
   ```

5. **Highlight new winners:**
   - Any ad that crossed from Testing to Winner since the last check
   - Any ad that crossed from Winner to Super Winner since the last check

6. **Update winner_count** in competitor-data.json metadata

## Output

Report summary:

```
Winner Tracking Report
  Total ads: {total}
  New: {new_count} | Testing: {testing_count} | Winner: {winner_count} | Super Winner: {super_count} | Stopped: {stopped_count}

  NEW WINNERS (crossed 30+ days):
  - {competitor_name}: "{ad_summary}" — {days_active} days, {format}, {hook_type} hook
  - ...

  {longevity tables per competitor}
```
