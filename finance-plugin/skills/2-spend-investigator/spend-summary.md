---
name: spend-summary
description: Summarize spend by category, merchant, or time period
menu-code: SS
---

# Spend Summary

Summarize spend from finance-data.json by category, merchant, or time period.

## Process

1. **Load finance-data.json** — Read all transactions

2. **Determine scope:**
   - If user specified a period (e.g., "March 2026", "last 3 months"), filter to that range
   - If user specified a category or merchant, filter to that
   - Default: current month

3. **Generate category breakdown:**

   ```
   SPEND SUMMARY — {period}
   
   Total: ${total_debits} out | ${total_credits} in | ${net} net
   
   By Category:
   | Category              | Amount    | Txns | % of Total | vs Last Period |
   |-----------------------|-----------|------|------------|----------------|
   | Software & Subs       | $1,234    | 12   | 35%        | +8%            |
   | Hosting               | $890      | 3    | 25%        | -2%            |
   | ...                   |           |      |            |                |
   | UNCATEGORIZED         | $150      | 4    | 4%         |                |
   ```

4. **Generate top merchants:**

   ```
   Top Merchants:
   | Merchant          | Amount  | Txns | Category           |
   |-------------------|---------|------|--------------------|
   | Anthropic         | $500    | 1    | Software           |
   | AWS               | $340    | 2    | Hosting            |
   | ...               |         |      |                    |
   ```

5. **Flag notable items:**
   - Categories with >20% increase vs prior period
   - Uncategorized transactions above $50
   - Any open leak flags in the period

## Output

Present the full summary as structured tables. If comparison period data exists, include period-over-period changes.
