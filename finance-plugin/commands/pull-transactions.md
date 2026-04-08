---
description: Pull latest transactions from Airwallex and update finance-data.json
---

Run the transaction analyst's pull workflow:

1. Run `python3 scripts/fetch-transactions.py` with optional date range arguments
2. Merge new transactions into `finance/finance-data.json` (skip duplicates by transaction ID)
3. Auto-categorize any uncategorized transactions by merchant name and MCC code
4. Report: count of new transactions, total spend, and any flagged items

$ARGUMENTS
