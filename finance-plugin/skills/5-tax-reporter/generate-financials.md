---
name: generate-financials
description: Generate Excel workbook and print-ready HTML for financial statements
menu-code: GF
---

# Generate Financial Pack (Excel + HTML)

Generate accountant-ready Excel workbook and print-to-PDF HTML from finance-data.json.

## Process

1. **Get the period from user.** Format: `FY{YYYY}` (e.g., `FY2025`).

2. **Run the generator script:**
   ```bash
   python3 finance-plugin/scripts/generate-financials.py --period {period} --output all
   ```

3. **Verify outputs exist:**
   - `finance/tax/{period}/{period}-financial-pack.xlsx` — 6-sheet workbook
   - `finance/tax/{period}/{period}-financial-statements.html` — print-ready HTML

4. **Report to user:**

```
Financial pack generated for {period}.

Excel: finance/tax/{period}/{period}-financial-pack.xlsx
  Sheets:
    1. Transaction Ledger — {count} transactions with AUD amounts, FX rates, categories
    2. Income Statement — Revenue, COGS, OpEx, Net Profit
    3. Balance Sheet — Assets, Liabilities, Equity
    4. Cash Flow — Direct method (Operating, Investing, Financing)
    5. Category Summary — Spend by category with % breakdown
    6. FX Summary — Currency volumes and average rates

HTML: finance/tax/{period}/{period}-financial-statements.html
  Open in browser → Ctrl+P → Save as PDF

Data quality: {categorized_pct}% categorized | {aud_pct}% FX converted | {gst_pct}% GST classified
```

## Notes

- The Excel workbook is the primary accountant deliverable — it has the full transaction ledger with IDs for cross-referencing against Airwallex/Amex.
- The HTML file is for formal presentation — opens in any browser, prints clean PDF via Ctrl+P.
- All amounts are in AUD. Original currency amounts and FX rates are included for audit trail.
- If `amount_aud` is missing on any transactions, run `convert-fx.py` first.
