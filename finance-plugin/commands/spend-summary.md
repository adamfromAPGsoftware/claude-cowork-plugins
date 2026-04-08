---
description: Show spend summary by category, merchant, or time period
---

Summarize financial spend from finance-data.json:

1. Read `finance/finance-data.json`
2. If period specified, filter to that range; default is current month
3. Group by category and merchant
4. Show totals, top merchants, category breakdown
5. Flag any categories with unusual increases vs. prior period

$ARGUMENTS
