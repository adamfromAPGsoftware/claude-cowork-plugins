---
name: sync-crm
description: Push reconciled transactions to CRM as documents via MCP tools
menu-code: SC
---

# Sync CRM

Push reconciled transactions to the CRM as documents via `create_document` MCP tool. Link to contacts and projects.

## Process

1. **Load finance-data.json** — filter to transactions where:
   - `reconciliation_status == "reconciled"` AND `crm_synced != true`
   - OR flagged for CRM creation during Manual Match [MM]

2. **If no transactions to sync:** Inform user. Suggest [AR] Auto-Reconcile or [MM] Manual Match if unreconciled transactions remain.

3. **For each transaction to sync:**

   a. **Determine entity linking:**
      - If `crm_entity_type` is `"invoice"`:
        - Fetch invoice details via `mcp__claude_ai_APG_CRM__get_invoice` to get contact/project references
      - If `crm_entity_type` is `"bill"`:
        - Fetch bill details via `mcp__claude_ai_APG_CRM__get_bill` to get contact/project references
      - Extract `contact_id` and `project_id` for linking

   b. **Create CRM document:**
      - Call `mcp__claude_ai_APG_CRM__create_document` with:
        - `title`: "Transaction: {merchant_name} - ${amount} ({date})"
        - `entity_type`: "transactions"
        - `content`: Transaction details including ID, source, amount, date, merchant, category, reconciliation reference
        - Link to contact and/or project if available

   c. **Update finance-data.json:**
      - Set `crm_synced: true`
      - Set `crm_document_id: "{document_id}"` from create response
      - Set `crm_sync_date: "{timestamp}"`

4. **Handle errors:**
   - If MCP call fails, log the error and continue with remaining transactions
   - Mark failed transactions with `crm_sync_error: "{error_message}"`
   - Report failures separately in summary

5. **Report summary**

## Output

```
CRM sync complete.
  Transactions synced: {count}
  Documents created: {doc_count}
  Linked to contacts: {contact_count}
  Linked to projects: {project_count}
  Failed: {fail_count}

  {if failures:}
  Failed transactions:
  - {transaction_id}: {error_message}
  {end if}
```
