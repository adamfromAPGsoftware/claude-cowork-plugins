---
name: generate-tax-summary
description: Generate annual tax summary for a financial year with income, expenses, FX, GST, and R&D spend
menu-code: GT
---

# Generate Annual Tax Summary

Generate a comprehensive tax summary for an Australian financial year.

## Process

1. **Get the financial year from user.** Format: `FY{YYYY}` (e.g., `FY2026`).
   - FY2026 = Jul 1 2025 → Jun 30 2026
   - The year in `FY{YYYY}` is the year the FY ends.

2. **Filter finance-data.json** to transactions within the FY date range.

3. **Calculate income by source:**
   - Group income transactions by `merchant_name_normalized` or source
   - Show total and count for each source

4. **Calculate expenses by category:**
   - Group expense transactions by `category_id`
   - Show total and count for each category
   - Include subtotals for tax-deductible vs non-deductible

5. **FX gains/losses:**
   - Identify all transactions in non-AUD currencies
   - Report original currency amount and AUD equivalent for each
   - Sum total FX exposure

6. **GST summary:**
   - Total GST collected (across all BAS quarters)
   - Total GST paid (across all BAS quarters)
   - Net GST position
   - GST classification completeness %

7. **Depreciation-eligible items:**
   - Filter transactions where `category_id` is `office` or `equipment` AND amount > $300
   - List each item with date, merchant, amount

8. **R&D eligible spend:**
   - Filter transactions where `r_and_d_eligible == true`
   - Group by category
   - Show total eligible spend

9. **Generate output file** at `finance/tax/FY{YYYY}/tax-summary.json`:
   ```json
   {
     "financial_year": "FY2026",
     "date_range": { "from": "2025-07-01", "to": "2026-06-30" },
     "income_by_source": {},
     "expenses_by_category": {},
     "total_income": 0.00,
     "total_expenses": 0.00,
     "fx_gains_losses": [],
     "gst_summary": {
       "collected": 0.00,
       "paid": 0.00,
       "net": 0.00,
       "completeness_pct": 0.0
     },
     "depreciation_eligible": [],
     "r_and_d_eligible_spend": {},
     "r_and_d_total": 0.00,
     "receipt_coverage_pct": 0.0,
     "generated_at": "ISO timestamp",
     "transaction_count": 0
   }
   ```

10. **Save the file** and present summary.

## Output

```
Tax summary generated for {financial_year}.

  Date range: {from} → {to}
  Transactions: {count}

  Income: ${total_income}
    {source}: ${amount} ({count})
    ...

  Expenses: ${total_expenses}
    {category}: ${amount} ({count})
    ...

  GST Summary:
    Collected: ${collected} | Paid: ${paid} | Net: ${net}
    Classification: {gst_pct}%

  FX Transactions: {fx_count} | Total AUD: ${fx_total}

  Depreciation-eligible items: {count} | ${total}
  R&D eligible spend: ${r_and_d_total}

  Receipt coverage: {receipt_pct}%

  Saved to: finance/tax/{financial_year}/tax-summary.json
```
