---
description: Generate BAS quarter data — GST collected, paid, net, expenses by category
---

Generate Business Activity Statement data for a quarter:

1. Read `finance/finance-data.json`
2. Filter transactions to the specified BAS quarter period
3. Calculate:
   - GST collected (1/11th of GST-inclusive income)
   - GST paid on purchases (from `gst_amount` fields or estimated at 1/11th for eligible categories)
   - Net GST payable/refundable
   - Total expenses by category
   - GST-free items (bank fees, FX conversions, government charges)
4. Present summary with transaction counts per category
5. Flag any transactions with `gst_status == "unknown"` that need manual review before lodging

$ARGUMENTS — period (e.g., Q3-2025-26 for January–March 2026)
