---
description: Scan for financial leaks — duplicates, forgotten subscriptions, anomalies
---

Run a financial leak check against finance-data.json:

1. Read `finance/finance-data.json`
2. Scan for:
   - Duplicate charges (same merchant + amount within 24 hours)
   - Recurring charges to unrecognized merchants
   - Amounts significantly above merchant average
   - Unknown merchants above a configurable threshold
3. Present findings with transaction IDs and recommended actions
4. Update `leak_flags[]` in finance-data.json with any new flags

$ARGUMENTS
