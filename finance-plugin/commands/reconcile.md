---
description: Auto-match unreconciled transactions against CRM invoices and bills
---

Run reconciliation against CRM records:

1. Read `finance/finance-data.json` and filter to transactions with `reconciliation.status == "unmatched"`
2. Fetch invoices and bills from CRM via MCP
3. Match transactions by amount and date (± 3 days) against CRM records:
   - Exact amount match to a single invoice/bill → status = "matched"
   - Multiple possible matches → status = "ambiguous" (flag for review)
   - No match found → remains "unmatched"
4. Update `reconciliation` fields on matched transactions (entity type, entity ID, document ID)
5. Report: matched count, ambiguous count, unmatched count, total reconciliation rate

$ARGUMENTS
