---
name: auto-reconcile
description: Match transactions to CRM invoices and bills via MCP tools
menu-code: AR
---

# Auto-Reconcile

Match transactions to CRM invoices and bills using MCP tools. Match by amount + date + reference.

## Process

1. **Load finance-data.json** — filter to transactions where `reconciliation_status == "unmatched"` and `status != "duplicate"`

2. **Fetch CRM invoices:**
   - Call `mcp__claude_ai_APG_CRM__list_invoices` to retrieve all invoices
   - Note: invoices represent money coming IN (client payments received)

3. **Fetch CRM bills:**
   - Call `mcp__claude_ai_APG_CRM__list_bills` to retrieve all bills
   - Note: bills represent money going OUT (vendor/supplier payments)

4. **Match transactions to CRM records:**
   - For each unmatched transaction:
     - **Credit/incoming transactions:** Compare against invoices
     - **Debit/outgoing transactions:** Compare against bills
   - Matching criteria (all must align):
     - **Amount:** Exact match (within $0.01)
     - **Date:** Transaction date within +/- 5 days of invoice/bill date
     - **Reference:** If transaction description contains invoice/bill reference number, boost confidence
   - Score matches: amount (50%) + date proximity (25%) + reference match (25%)

5. **Classify matches:**
   - **High confidence (>85%):** Auto-reconcile — set `reconciliation_status: "reconciled"`, store CRM reference
   - **Medium confidence (60-85%):** Mark as `reconciliation_status: "ambiguous"` — queue for Manual Match [MM]
   - **No match (<60%):** Leave as `reconciliation_status: "unmatched"`

6. **Update finance-data.json:**
   - For reconciled transactions, add:
     - `crm_entity_type: "invoice"` or `"bill"`
     - `crm_entity_id: "{invoice_id or bill_id}"`
     - `reconciliation_status: "reconciled"`
     - `reconciliation_confidence: {score}`

7. **Report summary**

## Output

```
Auto-reconcile complete.
  Transactions evaluated: {count}
  Reconciled (high confidence): {reconciled_count}
  Ambiguous (needs review): {ambiguous_count}
  Unmatched: {unmatched_count}

  Reconciled breakdown:
  - Matched to invoices: {inv_count} (${inv_total})
  - Matched to bills: {bill_count} (${bill_total})

  Next: Run [MM] Manual Match to resolve {ambiguous_count} ambiguous matches.
```
