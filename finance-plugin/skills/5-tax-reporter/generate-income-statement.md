---
name: generate-income-statement
description: Generate an income statement (P&L) for a financial year or custom period with GST-exclusive figures
menu-code: GI
---

# Generate Income Statement (P&L)

Generate a Profit & Loss statement following Australian small business format (AASB). All figures GST-exclusive.

## Process

1. **Get the period from user.** Accept either:
   - Financial year: `FY{YYYY}` (e.g., `FY2026` = 1 Jul 2025 – 30 Jun 2026)
   - Custom range: `{YYYY-MM-DD}` to `{YYYY-MM-DD}`

2. **Load reference** — Read `references/financial-statements-au.md` for format and field mappings.

3. **Filter finance-data.json** to transactions within the date range.

4. **Calculate Revenue:**
   - All transactions where `direction == "credit"` (excluding financing tags: `owner_contribution`, `loan_proceeds`)
   - Group by `merchant_name_normalized`
   - For GST-inclusive transactions: subtract `gst_amount` (or apply 1/11th rule) to get GST-exclusive amount
   - Show: Service income (total), Other income (if applicable)

5. **Calculate Cost of Services (COGS):**
   - Transactions where `category_id == "contractors"` and `direction == "debit"`
   - GST-exclusive amounts
   - Gross Profit = Revenue - COGS

6. **Calculate Operating Expenses:**
   - Group remaining debit transactions by `category_id` (excluding contractors, financing tags, and asset purchases > $300)
   - Categories: software, hosting, travel, meals, office (≤$300 items), marketing, professional, other
   - GST-exclusive amounts for each
   - Total Operating Expenses = sum of all categories

7. **Calculate Net Profit:**
   - Net Profit Before Tax = Gross Profit - Total Operating Expenses

8. **Calculate completeness metrics:**
   - % of transactions with `category_id` assigned (not UNSET)
   - % of transactions with `gst_status` confirmed (not unknown)
   - % of transactions with receipts attached
   - Count of uncategorized transactions (with total amount)

9. **Generate output file** at `finance/tax/FY{YYYY}/income-statement.json`:
   ```json
   {
     "period": "FY2026",
     "date_range": { "from": "2025-07-01", "to": "2026-06-30" },
     "revenue": {
       "service_income": 0.00,
       "other_income": 0.00,
       "total": 0.00,
       "breakdown": []
     },
     "cost_of_services": {
       "contractors": 0.00,
       "total": 0.00
     },
     "gross_profit": 0.00,
     "operating_expenses": {
       "software": 0.00,
       "hosting": 0.00,
       "travel": 0.00,
       "meals": 0.00,
       "office": 0.00,
       "marketing": 0.00,
       "professional": 0.00,
       "other": 0.00,
       "total": 0.00
     },
     "net_profit_before_tax": 0.00,
     "completeness": {
       "categorized_pct": 0.0,
       "gst_classified_pct": 0.0,
       "receipt_coverage_pct": 0.0,
       "uncategorized_count": 0,
       "uncategorized_total": 0.00
     },
     "transaction_count": 0,
     "generated_at": "ISO timestamp"
   }
   ```

10. **Save the file** and present summary.

## Output

```
Income Statement generated for {period}.

  Date range: {from} → {to}
  Transactions: {count}

  Revenue
    Service income:                 ${service_income}
    Other income:                   ${other_income}
    Total Revenue:                  ${total_revenue}

  Cost of Services
    Contractors:                    ${contractors}
    Gross Profit:                   ${gross_profit}

  Operating Expenses
    Software & subscriptions:       ${software}
    Hosting & infrastructure:       ${hosting}
    Travel:                         ${travel}
    Meals & entertainment:          ${meals}
    Office supplies:                ${office}
    Marketing:                      ${marketing}
    Professional services:          ${professional}
    Other:                          ${other}
    Total Operating Expenses:       ${total_opex}

  ─────────────────────────────────
  Net Profit Before Tax:            ${net_profit}

  Data quality:
    Categorized: {cat_pct}% | GST classified: {gst_pct}% | Receipts: {receipt_pct}%
    Uncategorized: {uncat_count} transactions (${uncat_total})

  Saved to: finance/tax/{period}/income-statement.json
```
