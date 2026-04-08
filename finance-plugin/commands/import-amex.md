---
description: Import Amex CSV statement(s) from finance/amex/ into finance-data.json
---

Import Amex AU credit card transactions:

1. Run `python3 scripts/import-amex.py` with optional `--file` argument for a specific CSV
2. Parse all `.csv` files in `finance/amex/` (handles both 3-column and 4-column Amex AU formats)
3. Generate hash-based transaction IDs for dedup, merge new transactions into `finance/finance-data.json`
4. Auto-categorize any uncategorized transactions by merchant name
5. Report: count of new transactions, skipped duplicates, and any potential cross-source duplicates (Amex vs Airwallex)

$ARGUMENTS
