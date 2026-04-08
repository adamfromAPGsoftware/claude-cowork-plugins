---
name: generate-bas
description: Generate BAS quarter data with GST collected, GST paid, net GST, and completeness metrics
menu-code: GB
---

# Generate BAS Quarter Data

Generate Business Activity Statement data for an Australian BAS quarter.

## Process

1. **Get the BAS period from user.** Format: `Q{N}-{YYYY}-{YY}` (e.g., `Q3-2025-26`).
   - Parse the period to determine date range:
     - Q1: Jul 1 → Sep 30
     - Q2: Oct 1 → Dec 31
     - Q3: Jan 1 → Mar 31
     - Q4: Apr 1 → Jun 30
   - The first year is the FY start year. Example: Q3-2025-26 = Jan 1 2026 → Mar 31 2026.

2. **Filter finance-data.json** to transactions within the date range.

3. **Calculate GST figures:**
   - **GST collected** (1A): Sum of GST on income/sales transactions where `gst_status == "confirmed"`
   - **GST paid** (1B): Sum of `gst_amount` on expense transactions where `gst_status == "confirmed"`
   - **Net GST** (difference): GST collected minus GST paid
   - For transactions with `gst_status == "unknown"`: count and total separately as unclassified

4. **Calculate expenses by category:**
   - Group all expense transactions by `category_id`
   - Show total and count for each category

5. **Flag data quality issues:**
   - Transactions with `gst_status` not confirmed (count and total)
   - Transactions missing receipts (count and total)
   - FX transactions (count and total AUD equivalent)

6. **Calculate completeness:**
   - GST completeness: % of transactions with confirmed GST status
   - Receipt completeness: % of transactions with receipts attached
   - Overall completeness: average of both

7. **Generate output file** at `finance/tax/BAS-{period}/bas-data.json`:
   ```json
   {
     "period": "Q3-2025-26",
     "date_range": { "from": "2026-01-01", "to": "2026-03-31" },
     "gst_collected": 0.00,
     "gst_paid": 0.00,
     "net_gst": 0.00,
     "expenses_by_category": {},
     "missing_gst_count": 0,
     "missing_receipt_count": 0,
     "fx_transactions": [],
     "completeness_pct": 0.0,
     "generated_at": "ISO timestamp",
     "transaction_count": 0
   }
   ```

8. **Save the file** and present summary.

## Output

```
BAS data generated for {period}.

  Date range: {from} → {to}
  Transactions: {count}

  GST Collected (1A): ${gst_collected}
  GST Paid (1B): ${gst_paid}
  Net GST: ${net_gst}

  Expenses by category:
    {category}: ${total} ({count} transactions)
    ...

  Data quality:
    GST classified: {gst_pct}%
    Receipts attached: {receipt_pct}%
    FX transactions: {fx_count}
    Overall completeness: {completeness_pct}%

  Saved to: finance/tax/BAS-{period}/bas-data.json
```
