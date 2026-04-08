# Finance Data Schema

## Location

`finance/finance-data.json` — single source of truth for {YOUR_COMPANY}'s financial data.

## Top-Level Structure

```json
{
  "last_sync": "ISO 8601 timestamp of last Airwallex pull",
  "airwallex_account_id": "string — primary Airwallex account ID",
  "sync_status": "synced | partial | error",
  "balances": { ... },
  "categories": [ ... ],
  "transactions": [ ... ],
  "leak_flags": [ ... ]
}
```

## Balances

```json
{
  "snapshot_date": "ISO 8601",
  "accounts": [
    {
      "account_id": "string",
      "currency": "AUD",
      "available_amount": 0.00,
      "pending_amount": 0.00,
      "total_amount": 0.00
    }
  ]
}
```

## Categories

Default spend categories. `monthly_budget` is optional — set to enable budget tracking.

```json
{
  "category_id": "software",
  "label": "Software & Subscriptions",
  "monthly_budget": null
}
```

**Default categories:** software, hosting, contractors, travel, meals, office, marketing, professional, other.

## Transactions

```json
{
  "transaction_id": "string — internal dedup key (airwallex_id or generated)",
  "airwallex_id": "string — original Airwallex transaction ID",
  "date": "YYYY-MM-DD — transaction date",
  "posted_date": "YYYY-MM-DD — settlement date",
  "amount": -49.99,
  "currency": "AUD",
  "direction": "debit | credit",
  "merchant_name": "string — raw merchant name from Airwallex",
  "merchant_name_normalized": "string — cleaned/normalized merchant name",
  "merchant_category_code": "string — MCC code (rich data from issuing endpoint)",
  "merchant_city": "string — merchant city (from issuing endpoint)",
  "merchant_country": "string — merchant country code (from issuing endpoint)",
  "category_id": "string — maps to categories[].category_id",
  "category_confidence": "AUTO | MANUAL | UNSET",
  "description": "string — transaction description/memo",
  "reference": "string — payment reference or retrieval ref",
  "source": "card_transaction | financial_transaction",
  "source_type": "string — for wallet items: PAYOUT, CONVERSION, DEPOSIT, etc.",
  "card_id": "string | null — issuing card ID if applicable",
  "card_last_four": "string | null — last 4 digits",
  "card_nickname": "string — card nickname if set",
  "transaction_type": "string — CLEARING, AUTHORIZATION, REFUND, REVERSAL, etc.",
  "reconciliation": {
    "status": "unmatched | matched | ambiguous | manual",
    "crm_entity_type": "invoice | bill | null",
    "crm_entity_id": "string | null",
    "crm_document_id": "string | null"
  },
  // CRM relationships: Transactions are the primary financial records.
  // Invoices (money IN) and Bills (money OUT) are expected payments
  // that reconcile against actual Transactions.
  // See crm-finance-entities.md for full entity reference.
  "receipt": {
    "attached": false,
    "file_path": "string | null"
  },
  "tags": ["string"],
  "notes": "string",
  "gst_amount": "number | null",
  "gst_status": "included | excluded | exempt | unknown"
}
```

### Transaction Fields

| Field | Required | Description |
|-------|----------|-------------|
| transaction_id | Yes | Dedup key — prevents re-importing |
| airwallex_id | Yes | Original Airwallex ID |
| date | Yes | Transaction date |
| amount | Yes | Signed amount (negative = debit) |
| currency | Yes | 3-letter currency code |
| direction | Yes | debit or credit |
| merchant_name | Yes | Raw merchant name |
| merchant_category_code | No | MCC code from card network (issuing transactions only) |
| merchant_city | No | Merchant city (issuing transactions only) |
| merchant_country | No | Merchant country (issuing transactions only) |
| category_id | No | Assigned category (empty = uncategorized) |
| category_confidence | No | How it was categorized |
| reconciliation | No | CRM matching status (phase 2) |
| receipt | No | Receipt attachment (phase 2) |

## Leak Flags

```json
{
  "flag_id": "string — unique flag ID",
  "type": "duplicate | unexpected_recurring | anomalous_amount | unknown_merchant",
  "transaction_ids": ["string — related transaction IDs"],
  "description": "string — human-readable explanation",
  "status": "open | dismissed | confirmed",
  "flagged_date": "YYYY-MM-DD"
}
```

### Flag Types

| Type | Description |
|------|-------------|
| duplicate | Same merchant + same amount within 24 hours |
| unexpected_recurring | Recurring charge to unrecognized merchant |
| anomalous_amount | Amount significantly above merchant average |
| unknown_merchant | Transaction from merchant never seen before above threshold |
