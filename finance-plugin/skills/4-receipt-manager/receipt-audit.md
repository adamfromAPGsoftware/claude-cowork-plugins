---
name: receipt-audit
description: List all transactions above $50 missing receipts, grouped by category
menu-code: RA
---

# Receipt Audit

Identify all transactions above $50 that are missing receipts. Group by category for prioritised action.

## Process

1. **Load finance-data.json** — filter to transactions where:
   - `receipt` field is empty/null AND
   - absolute amount > $50

2. **Group by category** — for each category, list the unreceipted transactions sorted by amount descending

3. **Calculate totals:**
   - Total unreceipted amount (above $50)
   - Count of unreceipted transactions (above $50)
   - Total unreceipted amount (all transactions, for reference)
   - Overall receipt coverage percentage

4. **Present the audit report:**

   ```
   Receipt Audit — Missing Receipts Over $50
   
   Overall coverage: {receipted_count}/{total_count} transactions ({coverage_pct}%)
   
   {category_name} ({count} missing | ${total})
   ┌──────────────┬────────────┬──────────┬──────────────────────┐
   │ Date         │ Amount     │ GST      │ Merchant             │
   ├──────────────┼────────────┼──────────┼──────────────────────┤
   │ {date}       │ ${amount}  │ {status} │ {merchant}           │
   └──────────────┴────────────┴──────────┴──────────────────────┘
   
   (repeat for each category)
   
   Summary:
     Missing receipts (>$50): {count} transactions | ${total}
     Missing receipts (all): {count_all} transactions | ${total_all}
   ```

5. **Suggest next actions:**
   - Which categories have the most gaps
   - Whether any high-value transactions need urgent attention

## Output

The audit report table as shown above, plus actionable next steps.
