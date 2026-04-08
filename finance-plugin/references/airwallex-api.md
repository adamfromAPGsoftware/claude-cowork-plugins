# Airwallex API Reference (Read-Only Subset)

## Authentication

Airwallex uses a two-step auth flow:

1. **Login** — `POST /api/v1/authentication/login`
   - Headers: `x-client-id`, `x-api-key`
   - Returns: `{ "token": "...", "expires_at": "..." }`
   - Token is short-lived (~30 min)

2. **Subsequent requests** — `Authorization: Bearer {token}`

## Environment

| Environment | Base URL |
|-------------|----------|
| Demo | `https://api-demo.airwallex.com` |
| Production | `https://api.airwallex.com` |

Controlled by `AIRWALLEX_ENVIRONMENT` in `.env`.

## Endpoints Used (GET only)

### 1. Issuing Transactions (PRIMARY — card spend with merchant detail)
```
GET /api/v1/issuing/transactions
  ?from_created_at=2026-01-01T00:00:00Z
  &to_created_at=2026-04-01T00:00:00Z
  &page_num=0
  &page_size=500
```

Returns card transactions with rich merchant data:
- `merchant.name` — merchant business name
- `merchant.category_code` — MCC code for auto-categorization
- `merchant.city`, `merchant.country` — location
- `transaction_amount`, `billing_amount` — in original and billing currency
- `card_id`, `masked_card_number`, `card_nickname`
- `transaction_type` — AUTHORIZATION, CLEARING, REFUND, REVERSAL

**This is the primary endpoint for spend analysis.** MCC codes enable reliable auto-categorization.

### 2. Financial Transactions (SECONDARY — wallet ledger)
```
GET /api/v1/financial_transactions
  ?from_created_at=2026-01-01T00:00:00Z
  &to_created_at=2026-04-01T00:00:00Z
  &page_num=0
  &page_size=500
```

Returns wallet-level ledger entries (transfers, fees, conversions, payouts, deposits).
**No merchant detail** — used to catch non-card spend. Card-sourced items are excluded
to avoid duplicates with the issuing endpoint.

### 3. Payment Acceptance — Payment Intents (income via payment links)
```
GET /api/v1/pa/payment_intents
  ?from_created_at=2026-01-01T00:00:00Z
  &to_created_at=2026-04-01T00:00:00Z
  &page_num=0
  &page_size=200
```

Returns payments received via Airwallex payment links. **These do NOT appear in the
financial_transactions endpoint.** Only `SUCCEEDED` payments represent actual income.

Key fields: `id`, `amount`, `currency`, `captured_amount`, `status`, `merchant_order_id`,
`customer.name`, `customer.email`, `method`, `created_at`, `payment_link_id`.

### 4. Payment Acceptance — Settlements (batch settlement records)
```
GET /api/v1/pa/financial/settlements
  ?from_created_at=2026-01-01T00:00:00Z
  &to_created_at=2026-04-01T00:00:00Z
  &page_num=0
  &page_size=200
```

Returns batch settlement records showing NET amounts after Airwallex PA fees.
Use for reconciliation: gross (payment_intent) minus net (settlement) = PA fees.

### 5. Balances
```
GET /api/v1/balances/current
```

Returns current balance per currency across all accounts.

## Financial Transaction Source Types

Complete mapping of `source_type` values from `/api/v1/financial_transactions`:

| source_type | Classification | Description |
|-------------|---------------|-------------|
| `DEPOSIT` | income | Bank transfers, Upwork deposits, client wire payments |
| `PAYOUT` (debit) | expense | Contractor payments, withdrawals |
| `PAYOUT` (credit) | refund | Failed payout returned |
| `BATCH_PAYOUT` | expense | Bulk contractor payments |
| `CONVERSION` | internal | FX wallet-to-wallet conversions |
| `PAYMENT_ATTEMPT` | internal | Card funding / payment gateway attempts |
| `TRANSFER` | internal | Internal wallet transfers |
| `YIELD` | internal | Airwallex Yield product (in/out net to zero) |
| `FEE` | expense | Platform fees, FX fees |
| `ADJUSTMENT` | direction-based | Account adjustments (credit=income, debit=expense) |
| `DIRECT_DEBIT` | expense | Direct debit charges |
| `REFUND` | refund | PA refund to customer |
| `REFUND_REVERSAL` | income | Reversed refund (money back) |
| `DISPUTE` (debit) | expense | Chargeback lost |
| `DISPUTE` (credit) | refund | Dispute won |
| `CHARGE` | expense | Platform charges |
| `PURCHASE` | expense | Purchases via Airwallex |
| `REPAYMENT` | expense | Loan/credit repayments |
| `CARD_PURCHASE` | *filtered* | Handled by issuing endpoint |
| `CARD_REFUND` | *filtered* | Handled by issuing endpoint |

**Payment Acceptance income** comes from `/api/v1/pa/payment_intents` (not financial_transactions).

## Safety

**This integration is read-only.** The following endpoints are NEVER called:
- POST /api/v1/payments/create
- POST /api/v1/transfers/create
- Any PUT, PATCH, or DELETE endpoint

The API key should be provisioned with read-only permissions in the Airwallex dashboard.

## Rate Limits

Airwallex applies rate limits per API key. The `fetch-transactions.py` script handles pagination with reasonable page sizes (200) to stay within limits.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AIRWALLEX_CLIENT_ID` | Client ID from Airwallex dashboard |
| `AIRWALLEX_API_KEY` | API key (read-only permissions) |
| `AIRWALLEX_ENVIRONMENT` | `demo` or `prod` |
