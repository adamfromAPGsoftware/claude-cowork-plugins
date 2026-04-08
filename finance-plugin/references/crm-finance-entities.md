# CRM Finance Entity Reference

How each {YOUR_CRM} entity maps to the finance pipeline. All CRM access is via MCP tools (`mcp__claude_ai_APG_CRM__*`).

## Core Principle

**Transactions are the primary financial records.** Every bank transfer, card payment, and wallet movement is a Transaction. Invoices and Bills are *expected* payments that we reconcile *against* actual Transactions.

## Entity Map

| CRM Entity | Finance Role | Direction | When to Use |
|---|---|---|---|
| **Transactions** | Every real money movement — card spend, bank transfers, wallet activity | Core data | Always — this is the ledger |
| **Invoices** | Client invoices for work delivered — money we expect to receive | Income (credit) | Reconcile against incoming Transactions |
| **Bills** | Vendor/supplier bills for project expenses — money we expect to pay | Expense (debit) | Reconcile against outgoing Transactions |
| **Documents** | Attachments — receipts, reconciliation batches, report snapshots | Supporting | Attach receipts to Transactions; store report artifacts |
| **Contacts** | Vendors and clients linked to Invoices, Bills, and Transactions | Linking | Look up who a Transaction relates to |
| **Projects** | Cost centres — Invoices and Bills are booked against Projects | Grouping | Group financial activity by engagement |

## Relationship Flow

```
Transaction (actual money)
    ↕ reconcile
Invoice / Bill (expected money)
    ↕ linked to
Contact (who)
    ↕ linked to
Project (what for)
    ↕ attached via
Document (receipts, reports)
```

## MCP Tools by Entity

### Transactions (main financial records)

| Tool | Purpose |
|------|---------|
| `create_transaction` | Record a new financial movement |
| `get_transaction` | Fetch a single transaction by ID |
| `list_transactions` | List all transactions (with filters) |
| `update_transaction` | Update transaction metadata (category, reconciliation status) |

### Invoices (money IN — client payments)

| Tool | Purpose |
|------|---------|
| `create_invoice` | Create invoice for client work |
| `get_invoice` | Fetch invoice details |
| `list_invoices` | List invoices — filter by status for receivables |
| `update_invoice` | Update invoice status (draft → sent → paid) |

### Bills (money OUT — vendor expenses against projects)

| Tool | Purpose |
|------|---------|
| `create_bill` | Record a vendor bill against a project |
| `get_bill` | Fetch bill details |
| `list_bills` | List bills — filter by status for payables |
| `update_bill` | Update bill status or details |

### Documents (receipts and attachments)

| Tool | Purpose |
|------|---------|
| `create_document` | Attach a receipt, reconciliation record, or report |
| `get_document` | Fetch document content |
| `list_documents` | List documents for an entity |
| `update_document` | Update document metadata |

### Contacts (vendors and clients)

| Tool | Purpose |
|------|---------|
| `create_contact` | Add a new vendor or client |
| `get_contact` | Fetch contact details |
| `list_contacts` | List all contacts |
| `search_contacts` | Search by name, email, or company |
| `update_contact` | Update contact information |

### Projects (cost centres)

| Tool | Purpose |
|------|---------|
| `create_project` | Create a new project/engagement |
| `get_project` | Fetch project details |
| `list_projects` | List all projects |
| `update_project` | Update project status or details |

## Receipts → Transactions

Receipts attach to Transactions via Documents:

1. Receipt Manager processes the receipt image (vision extraction)
2. Matches to a Transaction by amount + date + merchant
3. Saves receipt file to `finance/receipts/{YYYY-MM-DD}-{merchant-slug}.{ext}`
4. Updates `transaction.receipt.attached = true` and `transaction.receipt.file_path` in finance-data.json
5. Optionally creates a CRM Document linked to the Transaction's contact/project

## Reconciliation Flow

1. **Transactions** in finance-data.json are the source of truth (from Airwallex + Amex imports)
2. **Invoices** (list via MCP) represent expected income — match against credit Transactions
3. **Bills** (list via MCP) represent expected expenses — match against debit Transactions
4. Matched Transactions get `reconciliation.status = "matched"` with CRM entity references
5. Reconciled batches are stored as CRM **Documents** for audit trail
