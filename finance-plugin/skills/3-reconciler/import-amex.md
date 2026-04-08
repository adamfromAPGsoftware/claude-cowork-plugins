---
name: import-amex
description: Parse Amex CSV from finance/amex/, generate amex_{hash} IDs, merge into finance-data.json
menu-code: IA
---

# Import Amex Transactions

Parse Amex CSV files from `finance/amex/`, generate deterministic IDs, and merge into finance-data.json.

## Process

1. **Scan for CSV files:**
   - List all `.csv` files in `finance/amex/`
   - If multiple files found, present list and ask user which to import (or "all")
   - If no files found, inform user to place Amex CSV exports in `finance/amex/`

2. **Run import script:**
   ```
   python3 finance-plugin/scripts/import-amex.py
   ```

3. **CSV format expected:**
   - Columns: `Date`, `Description`, `Amount` (and optionally `Card Member`, `Account #`)
   - Date format: typically `MM/DD/YYYY` or `DD/MM/YYYY` (detect from data)
   - Amount: positive = charge, negative = credit/refund

4. **Transaction ID generation:**
   - For each row, generate: `amex_{sha256(date + amount + description)[:16]}`
   - This ensures idempotent imports — same CSV imported twice produces zero new records

5. **Merge into finance-data.json:**
   - For each transaction:
     - Check if `transaction_id` already exists in finance-data.json — skip if so
     - Set `account_source: "amex"`
     - Set `source: "amex_import"`
     - Set `category_confidence: "UNSET"`
     - Set `reconciliation_status: "unmatched"`
     - Normalize merchant name from Description field
   - Write updated finance-data.json

6. **Flag potential Airwallex duplicates:**
   - For each newly imported Amex transaction, check existing Airwallex transactions:
     - Same amount (exact match)
     - Date within +/- 3 days
     - Merchant name similarity (fuzzy match)
   - If potential duplicate found, flag both transactions with `potential_duplicate: true` and reference each other's ID

7. **Report summary**

## Output

```
Amex import complete.
  File(s): {filename(s)}
  Rows parsed: {count}
  New transactions: {new_count}
  Skipped (already imported): {skip_count}
  Potential Airwallex duplicates flagged: {dupe_count}

  Date range: {earliest} -> {latest}
  Total amount: ${total}

  Next: Run [DD] Dedup Check to review flagged duplicates.
```
