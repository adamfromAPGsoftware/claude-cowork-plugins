---
description: Show marketing data status — last sync, campaign count, date coverage, data health
---

Show the current state of marketing-data.json:

1. Read `marketing-plugin/data/marketing-data.json`
2. Report:
   - Last sync date
   - Ad account ID
   - Campaign count (active vs paused vs archived)
   - Ad set count
   - Ad count
   - Insight rows and date range coverage
   - Total spend across all insights
   - GA4 status (connected or not)
3. Flag any issues (stale data, missing insights, token expiry warnings)

$ARGUMENTS
