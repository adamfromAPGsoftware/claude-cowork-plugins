---
name: trend-analysis
description: Month-over-month spend trends, category shifts, and seasonal patterns
menu-code: TA
---

# Trend Analysis

Analyze spend trends across time periods.

## Process

1. **Load finance-data.json** — Read all transactions

2. **Group by month** — Aggregate spend per month per category

3. **Generate trend table:**

   ```
   MONTHLY TRENDS
   
   | Category        | Jan     | Feb     | Mar     | Trend    |
   |-----------------|---------|---------|---------|----------|
   | Software        | $1,100  | $1,150  | $1,234  | ↑ +12%   |
   | Hosting         | $900    | $890    | $890    | → flat   |
   | Contractors     | $2,000  | $0      | $3,000  | ↕ sporadic|
   | TOTAL           | $5,200  | $4,800  | $6,500  | ↑ +25%   |
   ```

4. **Highlight notable changes:**
   - Categories with >20% month-over-month increase
   - New categories that appeared (first transaction from a new merchant type)
   - Categories that disappeared (last transaction older than expected for recurring)
   - Overall spend trajectory

5. **Seasonal patterns** (if 6+ months of data):
   - Identify months that are consistently higher/lower
   - Flag one-time spikes vs sustained changes

## Output

Present trend table with period-over-period arrows and percentages. Highlight the top 3 most notable changes with transaction-level evidence.
