---
name: generate-balance-sheet
description: Generate a balance sheet (statement of financial position) using transaction data and CRM MCP for receivables/payables
menu-code: GBS
---

# Generate Balance Sheet

Generate a Statement of Financial Position following Australian small business format (AASB). Uses both finance-data.json and CRM MCP tools.

## Process

1. **Get the as-of date from user.** Default: end of current BAS quarter.
   - Parse to determine which FY period the date falls in.

2. **Load references:**
   - Read `references/financial-statements-au.md` for format and field mappings
   - Read `references/crm-finance-entities.md` for CRM entity roles

3. **Calculate Current Assets:**

   a. **Cash and cash equivalents:**
      - Read `finance/balances.json` for latest Airwallex balance snapshot
      - Sum `available_amount` across all accounts (convert non-AUD to AUD using latest rate)
      - Note the snapshot date — if stale (> 7 days), warn user to run Transaction Analyst [PB] first

   b. **Accounts Receivable:**
      - Call `mcp__claude_ai_APG_CRM__list_invoices`
      - Filter to invoices with status NOT "paid" and NOT "cancelled"
      - Filter to invoices dated on or before the as-of date
      - Sum amounts = Accounts Receivable
      - If CRM unavailable: report as "N/A — CRM not connected" and note in output

4. **Calculate Non-Current Assets:**

   a. **Equipment & technology:**
      - Filter finance-data.json for transactions where `category_id` in ["office", "equipment"] AND absolute `amount > 300`
      - Only include transactions dated on or before the as-of date
      - For items > $300: apply simplified depreciation (instant asset write-off if eligible, otherwise straight-line over useful life)
      - Net value = purchase cost - accumulated depreciation

5. **Calculate Current Liabilities:**

   a. **Accounts Payable:**
      - Call `mcp__claude_ai_APG_CRM__list_bills`
      - Filter to bills with status NOT "paid"
      - Filter to bills dated on or before the as-of date
      - Sum amounts = Accounts Payable
      - If CRM unavailable: report as "N/A — CRM not connected"

   b. **GST Payable / Receivable:**
      - Check for latest BAS data in `finance/tax/BAS-*/bas-data.json`
      - Use `net_gst` from the most recent completed BAS
      - Positive = GST payable (liability), Negative = GST receivable (asset — move to Current Assets)

6. **Calculate Equity:**

   a. **Retained Earnings:**
      - Sum all credit transactions (income) minus all debit transactions (expenses) from finance-data.json
      - Only include transactions dated on or before the as-of date
      - GST-exclusive figures

7. **Verify the accounting equation:**
   - Total Assets = Total Liabilities + Total Equity
   - If imbalance: flag the discrepancy amount and likely cause (missing data, unreconciled items)

8. **Generate output file** at `finance/tax/FY{YYYY}/balance-sheet.json`:
   ```json
   {
     "as_of_date": "YYYY-MM-DD",
     "assets": {
       "current": {
         "cash_and_equivalents": 0.00,
         "accounts_receivable": 0.00,
         "gst_receivable": 0.00,
         "total": 0.00
       },
       "non_current": {
         "equipment": 0.00,
         "accumulated_depreciation": 0.00,
         "net_equipment": 0.00,
         "total": 0.00
       },
       "total": 0.00
     },
     "liabilities": {
       "current": {
         "accounts_payable": 0.00,
         "gst_payable": 0.00,
         "total": 0.00
       },
       "total": 0.00
     },
     "equity": {
       "retained_earnings": 0.00,
       "total": 0.00
     },
     "balanced": true,
     "discrepancy": 0.00,
     "data_sources": {
       "balances_snapshot_date": "YYYY-MM-DD",
       "crm_invoices_count": 0,
       "crm_bills_count": 0,
       "latest_bas_period": "Q3-2025-26"
     },
     "generated_at": "ISO timestamp"
   }
   ```

9. **Save the file** and present summary.

## Output

```
Balance Sheet generated as at {as_of_date}.

  ASSETS
    Current Assets
      Cash and cash equivalents:    ${cash}
      Accounts receivable:          ${receivable}
      GST receivable:               ${gst_recv}
      Total Current Assets:         ${current_assets}

    Non-Current Assets
      Equipment (net):              ${net_equipment}
      Total Non-Current Assets:     ${non_current_assets}

    TOTAL ASSETS:                   ${total_assets}

  LIABILITIES
    Current Liabilities
      Accounts payable:             ${payable}
      GST payable:                  ${gst_pay}
      Total Current Liabilities:    ${current_liabilities}

    TOTAL LIABILITIES:              ${total_liabilities}

  NET ASSETS:                       ${net_assets}

  EQUITY
    Retained earnings:              ${retained}
    TOTAL EQUITY:                   ${total_equity}

  Assets = Liabilities + Equity:    {balanced ? "✓ Balanced" : "✗ Discrepancy: ${discrepancy}"}

  Data sources:
    Airwallex balances: {snapshot_date}
    CRM invoices (unpaid): {invoice_count}
    CRM bills (unpaid): {bill_count}
    Latest BAS: {bas_period}

  Saved to: finance/tax/FY{YYYY}/balance-sheet.json
```
