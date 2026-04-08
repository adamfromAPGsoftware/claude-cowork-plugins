---
description: Generate annual tax summary for a financial year — deductions, R&D eligibility, depreciation
---

Generate an annual tax summary for the specified financial year:

1. Read `finance/finance-data.json`
2. Filter transactions to the FY period (1 July – 30 June)
3. Calculate:
   - Total income and total expenses
   - Deductible expenses by category
   - GST summary (total collected, total paid, net position)
   - R&D Tax Incentive eligible spend (software dev tools, cloud hosting, R&D contractor fees)
   - Export Market Development Grant eligible spend (overseas marketing)
   - Depreciation items (office/equipment purchases > $300, instant asset write-off eligibility)
4. Flag any transactions in foreign currency and verify AUD conversion at transaction-date rate
5. Present summary suitable for tax return preparation

$ARGUMENTS — FY identifier (e.g., FY2026 for the year ending 30 June 2026)
