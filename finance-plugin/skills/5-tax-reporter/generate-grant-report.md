---
name: generate-grant-report
description: Generate R&D and eligible spend summary for government incentive applications
menu-code: GG
---

# Generate Grant Report

Generate an R&D and eligible spend summary for government incentive applications such as the R&D Tax Incentive and Export Market Development Grants.

## Process

1. **Get the reporting period from user.** Accept either:
   - A financial year: `FY{YYYY}` (e.g., `FY2026` = Jul 2025 → Jun 2026)
   - A custom date range: `{from} to {to}`

2. **Filter finance-data.json** to transactions within the date range where `r_and_d_eligible == true`.

3. **Group eligible transactions by category:**
   - software — development tools, APIs, SaaS for R&D
   - hosting — cloud infrastructure for R&D projects
   - contractors — development and research contractors
   - other — any other tagged R&D spend

4. **For each category, list transactions:**
   - Date, merchant, amount, receipt status
   - Flag any without receipts (will weaken grant claims)

5. **Calculate totals:**
   - Total R&D eligible spend
   - Spend with receipts vs without
   - Spend by quarter (for BAS alignment)

6. **Assess grant readiness:**
   - Receipt coverage % for R&D transactions
   - Any transactions missing category or GST classification
   - Recommend actions to strengthen the claim

7. **Generate output file** at `finance/tax/{period}/grant-report.json`:
   ```json
   {
     "period": "FY2026",
     "date_range": { "from": "2025-07-01", "to": "2026-06-30" },
     "total_eligible_spend": 0.00,
     "spend_by_category": {},
     "spend_by_quarter": {},
     "receipt_coverage_pct": 0.0,
     "transactions": [],
     "flags": [],
     "generated_at": "ISO timestamp"
   }
   ```

8. **Save the file** and present summary.

## Output

```
Grant report generated for {period}.

  Total R&D eligible spend: ${total}

  By category:
    {category}: ${amount} ({count} transactions)
    ...

  By quarter:
    {quarter}: ${amount}
    ...

  Data quality:
    Receipt coverage: {receipt_pct}%
    Missing classification: {missing_count}

  {flags/recommendations if any}

  Saved to: finance/tax/{period}/grant-report.json
```
