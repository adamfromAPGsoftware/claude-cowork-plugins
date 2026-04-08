---
description: Show financial data status — last sync, transaction count, balances, health check
---

Check the financial data status:

1. Read `finance/finance-data.json`
2. Report:
   - Last sync date and sync status
   - Total transactions count
   - Unreconciled transaction count
   - Uncategorized transaction count
   - Open leak flags count
3. Read `finance/balances.json` if exists — show account balances
4. Recommend next action (pull transactions, categorize, investigate leaks)

$ARGUMENTS
