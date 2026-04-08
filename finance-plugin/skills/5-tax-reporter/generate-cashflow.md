---
name: generate-cashflow
description: Generate a cash flow statement using the direct method with operating, investing, and financing activities
menu-code: GCF
---

# Generate Cash Flow Statement

Generate a Cash Flow Statement using the **direct method** (standard in Australia per AASB 107). Shows actual cash receipts and payments grouped by activity.

## Process

1. **Get the period from user.** Accept either:
   - Financial year: `FY{YYYY}` (e.g., `FY2026` = 1 Jul 2025 – 30 Jun 2026)
   - Custom range: `{YYYY-MM-DD}` to `{YYYY-MM-DD}`

2. **Load reference** — Read `references/financial-statements-au.md` for format and field mappings.

3. **Filter finance-data.json** to transactions within the date range.

4. **Calculate Operating Activities:**

   a. **Cash received from customers:**
      - Transactions where `direction == "credit"`
      - Exclude transactions tagged: `owner_contribution`, `loan_proceeds`, `asset_sale`
      - Use actual transaction amounts (GST-inclusive — cash flow reflects actual cash moved)

   b. **Cash paid to suppliers and employees:**
      - Transactions where `direction == "debit"`
      - Exclude: transactions tagged as financing (`owner_drawing`, `loan_repayment`)
      - Exclude: asset purchases (`category_id` in ["office", "equipment"] AND absolute `amount > 300`)
      - Use actual transaction amounts (GST-inclusive)

   c. **GST paid / received:**
      - Identify ATO payment/refund transactions (merchant contains "ATO" or "Australian Taxation" or tagged `gst_payment`/`gst_refund`)
      - GST paid = sum of debit ATO transactions
      - GST received = sum of credit ATO transactions
      - If no explicit ATO transactions: note "GST remittances not yet identifiable in transaction data"

   d. **Net cash from operating activities** = Cash received - Cash paid - Net GST paid

5. **Calculate Investing Activities:**

   a. **Purchase of equipment/assets:**
      - Transactions where `category_id` in ["office", "equipment"] AND absolute `amount > 300` AND `direction == "debit"`

   b. **Sale of assets:**
      - Transactions tagged `asset_sale` AND `direction == "credit"`

   c. **Net cash from investing activities** = Asset sales - Asset purchases

6. **Calculate Financing Activities:**

   a. **Owner capital contributed:**
      - Transactions tagged `owner_contribution` AND `direction == "credit"`

   b. **Owner drawings:**
      - Transactions tagged `owner_drawing` AND `direction == "debit"`

   c. **Loan proceeds received:**
      - Transactions tagged `loan_proceeds` AND `direction == "credit"`

   d. **Loan repayments:**
      - Transactions tagged `loan_repayment` AND `direction == "debit"`

   e. **Net cash from financing activities** = Capital + Loans received - Drawings - Loan repayments

7. **Calculate totals:**
   - Net change in cash = Operating + Investing + Financing
   - Opening cash balance: from `finance/balances.json` snapshot at period start, or sum of all transactions before period start
   - Closing cash balance = Opening + Net change
   - Cross-check: Closing balance should approximate `finance/balances.json` at period end (note any discrepancy)

8. **Generate output file** at `finance/tax/FY{YYYY}/cashflow-statement.json`:
   ```json
   {
     "period": "FY2026",
     "date_range": { "from": "2025-07-01", "to": "2026-06-30" },
     "operating": {
       "cash_received_from_customers": 0.00,
       "cash_paid_to_suppliers": 0.00,
       "gst_paid": 0.00,
       "gst_received": 0.00,
       "net": 0.00
     },
     "investing": {
       "equipment_purchases": 0.00,
       "asset_sales": 0.00,
       "net": 0.00
     },
     "financing": {
       "owner_contributions": 0.00,
       "owner_drawings": 0.00,
       "loan_proceeds": 0.00,
       "loan_repayments": 0.00,
       "net": 0.00
     },
     "net_change_in_cash": 0.00,
     "opening_balance": 0.00,
     "closing_balance": 0.00,
     "balance_crosscheck": {
       "airwallex_balance": 0.00,
       "discrepancy": 0.00
     },
     "transaction_count": 0,
     "generated_at": "ISO timestamp"
   }
   ```

9. **Save the file** and present summary.

## Output

```
Cash Flow Statement generated for {period}.

  Date range: {from} → {to}
  Transactions: {count}

  OPERATING ACTIVITIES
    Cash received from customers:   ${cash_received}
    Cash paid to suppliers:         (${cash_paid})
    GST paid:                       (${gst_paid})
    GST received:                   ${gst_received}
    Net cash from operating:        ${operating_net}

  INVESTING ACTIVITIES
    Equipment purchases:            (${equipment})
    Asset sales:                    ${asset_sales}
    Net cash from investing:        ${investing_net}

  FINANCING ACTIVITIES
    Owner contributions:            ${contributions}
    Owner drawings:                 (${drawings})
    Loan proceeds:                  ${loan_proceeds}
    Loan repayments:                (${loan_repayments})
    Net cash from financing:        ${financing_net}

  ─────────────────────────────────
  NET CHANGE IN CASH:               ${net_change}

  Opening balance:                  ${opening}
  Closing balance:                  ${closing}

  Cross-check vs Airwallex:         ${airwallex_balance} {discrepancy ? "(discrepancy: ${discrepancy})" : "✓"}

  Saved to: finance/tax/{period}/cashflow-statement.json
```
