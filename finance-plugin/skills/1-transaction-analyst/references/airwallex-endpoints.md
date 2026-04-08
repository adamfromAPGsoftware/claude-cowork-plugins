# Airwallex API Endpoints — Transaction Analyst

## Authentication

```
POST /api/v1/authentication/login
Headers:
  x-client-id: {AIRWALLEX_CLIENT_ID}
  x-api-key: {AIRWALLEX_API_KEY}
Response:
  { "token": "Bearer token", "expires_at": "ISO 8601" }
```

## Endpoints Used

### 1. Issuing Transactions (PRIMARY — card spend)
```
GET /api/v1/issuing/transactions
Headers:
  Authorization: Bearer {token}
Query params:
  from_created_at: ISO 8601 (required)
  to_created_at: ISO 8601 (required)
  page_num: int (0-based)
  page_size: int (default 100, try up to 500-1000)
  transaction_type: AUTHORIZATION | CLEARING | REFUND | REVERSAL (optional filter)
  card_id: string (optional — filter to specific card)
Response:
  {
    "items": [
      {
        "transaction_id": "txn_xxx",
        "transaction_date": "2026-04-01T10:00:00Z",
        "posted_date": "2026-04-01T12:00:00Z",
        "transaction_amount": 49.99,
        "transaction_currency": "USD",
        "billing_amount": 74.50,
        "billing_currency": "AUD",
        "transaction_type": "CLEARING",
        "status": "SETTLED",
        "card_id": "card_xxx",
        "masked_card_number": "****1234",
        "card_nickname": "Business",
        "merchant": {
          "name": "ANTHROPIC",
          "category_code": "5817",
          "city": "SAN FRANCISCO",
          "country": "US",
          "identifier": "...",
          "additional_merchant_info": {
            "merchant_category": "Digital Goods",
            "merchant_sub_category": "...",
            "merchant_full_name": "..."
          }
        },
        "retrieval_ref": "...",
        "auth_code": "..."
      }
    ],
    "has_more": true,
    "page_num": 0
  }
```

**Key fields for spend analysis:**
- `merchant.name` + `merchant.category_code` → auto-categorization
- `merchant.city` + `merchant.country` → location context
- `billing_amount` + `billing_currency` → AUD cost
- `card_nickname` → which card was used

### 2. Financial Transactions (SECONDARY — wallet ledger)
```
GET /api/v1/financial_transactions
Headers:
  Authorization: Bearer {token}
Query params:
  from_created_at: ISO 8601
  to_created_at: ISO 8601
  page_num: int (0-based)
  page_size: int (max 1000)
  currency: string (optional filter)
  status: PENDING | SETTLED (optional filter)
Response:
  {
    "items": [
      {
        "id": "ft_xxx",
        "amount": -500.00,
        "currency": "AUD",
        "created_at": "2026-04-01T10:00:00Z",
        "settled_at": "2026-04-01T12:00:00Z",
        "source_type": "PAYOUT | CONVERSION | DEPOSIT | PAYMENT_ATTEMPT | ...",
        "transaction_type": "PAYOUT | FX_CONVERSION | ...",
        "description": "Wire transfer to ...",
        "batch_id": "..."
      }
    ],
    "has_more": true,
    "page_num": 0
  }
```

**Note:** This endpoint has NO merchant detail. Card-sourced items (CARD_PURCHASE, ISSUING_CAPTURE, etc.) are filtered out by the script to avoid duplicates with the issuing endpoint.

### 3. Balances
```
GET /api/v1/balances/current
Headers:
  Authorization: Bearer {token}
Response:
  {
    "items": [
      {
        "available_amount": 15000.00,
        "pending_amount": 500.00,
        "total_amount": 15500.00,
        "currency": "AUD"
      }
    ]
  }
```

## Safety Reminder

**These are the ONLY endpoints this skill uses. All are GET requests.**

Never call:
- POST /api/v1/payments/create
- POST /api/v1/transfers/create
- Any PUT, PATCH, or DELETE endpoint
