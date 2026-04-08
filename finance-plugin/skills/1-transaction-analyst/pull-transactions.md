---
name: pull-transactions
description: Fetch financial transactions from Airwallex and merge into finance-data.json
menu-code: PT
---

# Pull Transactions

Fetch financial transactions from Airwallex and merge into finance-data.json.

## Process

1. **Determine date range:**
   - If user specified dates, use those
   - If finance-data.json has a `last_sync` date, use that as `--from-date` and today as `--to-date`
   - If no prior sync, default to last 90 days

2. **Run fetch script:**
   ```
   python3 finance-plugin/scripts/fetch-transactions.py --from-date {from} --to-date {to}
   ```

3. **Review script output:**
   - Note how many new transactions were fetched
   - Note any errors (auth failure, rate limit, network)

4. **Load the updated finance-data.json** and verify:
   - Total transaction count
   - New transactions added (by comparing before/after counts)
   - Date range coverage

5. **Auto-categorize new transactions:**
   - For each new transaction with `category_confidence: "UNSET"`:
     - Check merchant name against known patterns in memory (`patterns.md`)
     - Check MCC code against standard category mappings
     - If confident match: set `category_id` and `category_confidence: "AUTO"`
     - If uncertain: leave as `UNSET`

6. **Update finance-data.json:**
   - Set `last_sync` to current timestamp
   - Set `sync_status` to `synced` (or `partial` if errors occurred)

## Output

Report summary:

```
Pull complete.
  Date range: {from} → {to}
  New transactions: {count}
  Skipped (duplicates): {count}
  Auto-categorized: {count}
  Still uncategorized: {count}
  
  Top merchants this pull:
  - {merchant}: ${amount} ({count} transactions)
  - ...
```
