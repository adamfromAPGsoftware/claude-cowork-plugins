---
name: pull-meta
description: Fetch campaigns, ad sets, ads, and insights from Meta Marketing API and merge into marketing-data.json
menu-code: PM
---

# Pull Meta

Fetch campaigns, ad sets, ads, and daily insights from Meta Marketing API and merge into marketing-data.json.

## Process

1. **Determine date range:**
   - If user specified dates, use those
   - If marketing-data.json has a `last_sync` date, use that as `--from-date` and today as `--to-date`
   - If no prior sync, default to last 30 days

2. **Run fetch script** using Desktop Commander's `execute_command` tool (or Bash in Claude Code):
   ```
   python3 {plugin_root}/scripts/fetch-meta-campaigns.py --from-date {from} --to-date {to}
   ```
   Where `{plugin_root}` is the absolute path to this plugin directory.

3. **Review script output:**
   - Note how many campaigns, ad sets, ads, and insight rows were fetched
   - Note any errors (auth failure, rate limit, network, permissions)

4. **Load the updated marketing-data.json** and verify:
   - Total campaign count
   - Total ad set count
   - Total ad count
   - Total insight rows
   - Date range coverage

5. **Update sync metadata:**
   - Set `last_sync` to current timestamp
   - Set `sync_status` to `synced` (or `partial` if errors occurred)

## Output

Report summary:

```
Pull complete.
  Date range: {from} → {to}
  Campaigns: {count} ({new_count} new)
  Ad Sets: {count} ({new_count} new)
  Ads: {count} ({new_count} new)
  Insight rows: {count} ({new_count} new, {skipped_count} skipped)

  Spend by campaign:
  - {campaign_name}: ${spend} ({impressions} impressions, {clicks} clicks)
  - ...

  Total spend this range: ${total_spend}
```
