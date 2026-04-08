---
description: Push reconciled transaction batches to CRM as documents linked to contacts and projects
---

Sync reconciled transactions to CRM:

1. Read `finance/finance-data.json` and filter to transactions with `reconciliation.status == "matched"` that have not yet been synced to CRM
2. Group transactions by CRM entity (contact or project)
3. For each group, create or update a CRM "transactions" document via MCP containing the transaction details
4. Link documents to the appropriate CRM contacts and projects
5. Mark synced transactions in finance-data.json to prevent re-syncing
6. Report: documents created/updated, transactions synced, any errors

$ARGUMENTS
