# Australian Financial Statements Reference

Standard financial statement formats for Australian small businesses (AASB Tier 2 Simplified Disclosures). All line items mapped to `finance-data.json` fields.

## Governing Standards

- **AASB 1060** — General Purpose Financial Statements: Simplified Disclosures
- **AASB 101** — Presentation of Financial Statements
- **AASB 107** — Statement of Cash Flows (direct method preferred in Australia)
- **ATO** — Requires income statement, balance sheet, and cash flow for business tax returns

For small proprietary companies (revenue < $50M, assets < $25M, employees < 100), simplified reporting applies. qualifies.

---

## 1. Income Statement (Profit & Loss)

Also called Statement of Comprehensive Income. Shows revenue, expenses, and profit over a period.

### Format (Multi-Step — Services Business)

```
INCOME STATEMENT — {Period}
────────────────────────────────

Revenue
  Service income                    $XX,XXX
  Other income                      $X,XXX
                                   ─────────
  Total Revenue                     $XX,XXX

Cost of Services
  Contractor fees                   ($X,XXX)
                                   ─────────
  Gross Profit                      $XX,XXX

Operating Expenses
  Software & subscriptions          ($X,XXX)
  Hosting & infrastructure          ($X,XXX)
  Travel                            ($X,XXX)
  Meals & entertainment             ($XXX)
  Office supplies & equipment       ($XXX)
  Marketing                         ($X,XXX)
  Professional services             ($X,XXX)
  Other expenses                    ($XXX)
                                   ─────────
  Total Operating Expenses          ($XX,XXX)

                                   ─────────
  Net Profit Before Tax             $XX,XXX
```

### Field Mapping

| Line Item | finance-data.json Source |
|-----------|------------------------|
| Service income | Transactions where `direction == "credit"`, grouped by merchant |
| Contractor fees (COGS) | Transactions where `category_id == "contractors"` |
| Software & subscriptions | Transactions where `category_id == "software"` |
| Hosting & infrastructure | Transactions where `category_id == "hosting"` |
| Travel | Transactions where `category_id == "travel"` |
| Meals & entertainment | Transactions where `category_id == "meals"` |
| Office supplies & equipment | Transactions where `category_id == "office"` (items ≤ $300) |
| Marketing | Transactions where `category_id == "marketing"` |
| Professional services | Transactions where `category_id == "professional"` |
| Other expenses | Transactions where `category_id == "other"` |

**GST treatment:** All figures are GST-exclusive. For transactions with `gst_status == "included"`, subtract `gst_amount` (or calculate via 1/11th rule) to get the GST-exclusive amount.

---

## 2. Balance Sheet

Also called Statement of Financial Position. Shows assets, liabilities, and equity at a point in time.

### Format

```
BALANCE SHEET — As at {Date}
────────────────────────────────

ASSETS
  Current Assets
    Cash and cash equivalents       $XX,XXX     ← Airwallex balances
    Accounts receivable             $X,XXX      ← Unpaid CRM invoices
                                   ─────────
    Total Current Assets            $XX,XXX

  Non-Current Assets
    Equipment & technology          $X,XXX      ← Items > $300, less depreciation
                                   ─────────
    Total Non-Current Assets        $X,XXX

                                   ─────────
  TOTAL ASSETS                      $XX,XXX

LIABILITIES
  Current Liabilities
    Accounts payable                ($X,XXX)    ← Unpaid CRM bills
    GST payable / (receivable)      ($X,XXX)    ← Net GST from latest BAS
    Credit card balance             ($X,XXX)    ← Outstanding card balance if applicable
                                   ─────────
    Total Current Liabilities       ($XX,XXX)

                                   ─────────
  TOTAL LIABILITIES                 ($XX,XXX)

                                   ─────────
  NET ASSETS                        $XX,XXX

EQUITY
  Owner's equity / capital          $X,XXX
  Retained earnings                 $XX,XXX     ← Cumulative net profit
                                   ─────────
  TOTAL EQUITY                      $XX,XXX

  Assets = Liabilities + Equity     ✓
```

### Data Sources

| Line Item | Source |
|-----------|--------|
| Cash and cash equivalents | `finance/balances.json` → `accounts[].available_amount` (sum all currencies in AUD) |
| Accounts receivable | CRM MCP `list_invoices` → filter status != "paid" → sum amounts |
| Equipment & technology | Transactions with `category_id` in ["office", "equipment"] and `amount > 300`, less accumulated depreciation |
| Accounts payable | CRM MCP `list_bills` → filter status != "paid" → sum amounts |
| GST payable | Latest BAS `net_gst` (positive = payable, negative = receivable) |
| Retained earnings | Cumulative sum of all income minus all expenses from Transactions |

### Accounting Equation

`Total Assets = Total Liabilities + Total Equity`

If this does not balance, flag the discrepancy and investigate before publishing.

---

## 3. Cash Flow Statement (Direct Method)

Shows actual cash receipts and payments. The **direct method** is standard practice in Australia (AASB 107) and maps naturally to transaction-level data.

### Format

```
CASH FLOW STATEMENT — {Period}
────────────────────────────────

OPERATING ACTIVITIES
  Cash received from customers      $XX,XXX     ← Income transactions
  Cash paid to suppliers            ($XX,XXX)   ← Expense transactions (excl. assets & financing)
  GST paid to ATO                   ($X,XXX)    ← Net GST remitted
  GST received from ATO             $X,XXX      ← BAS refunds received
                                   ─────────
  Net cash from operating           $XX,XXX

INVESTING ACTIVITIES
  Purchase of equipment             ($X,XXX)    ← Office/equipment > $300
  Sale of assets                    $XXX        ← If applicable
                                   ─────────
  Net cash from investing           ($X,XXX)

FINANCING ACTIVITIES
  Owner capital contributed         $X,XXX      ← Tagged: owner_contribution
  Owner drawings                    ($X,XXX)    ← Tagged: owner_drawing
  Loan repayments                   ($X,XXX)    ← Tagged: loan_repayment
                                   ─────────
  Net cash from financing           $X,XXX

                                   ─────────
  NET CHANGE IN CASH                $XX,XXX

  Opening cash balance              $XX,XXX
  Closing cash balance              $XX,XXX
```

### Field Mapping

| Line Item | finance-data.json Source |
|-----------|------------------------|
| Cash received from customers | Transactions where `direction == "credit"` (excluding financing tags) |
| Cash paid to suppliers | Transactions where `direction == "debit"` AND `category_id` NOT in investing/financing categories AND amount ≤ $300 for office/equipment |
| GST paid to ATO | BAS net GST remittance transactions (tagged or identified by merchant "ATO") |
| Purchase of equipment | Transactions where `category_id` in ["office", "equipment"] AND `amount > 300` |
| Owner capital / drawings / loans | Transactions with tags: `owner_contribution`, `owner_drawing`, `loan_repayment` |
| Opening cash balance | `finance/balances.json` snapshot at period start, or calculated running total |
| Closing cash balance | Opening + Net Change (should match `finance/balances.json` at period end) |

### Direct Method Notes

- Australia prefers the direct method (AASB 107.18(a)). Most Australian reporting entities use it.
- A reconciliation of net cash from operating activities to net profit should accompany the statement.
- FX transactions: report in AUD using the transaction-date exchange rate.

---

## General Notes

- **Financial year:** 1 July – 30 June (Australian convention)
- **All figures GST-exclusive** except where noted (balance sheet receivables/payables may be GST-inclusive)
- **Materiality:** For small businesses, round to nearest dollar. Disclose rounding policy.
- **Comparative periods:** Where possible, show current period alongside prior period for comparison.
- **Completeness metrics:** Always report % of transactions categorized, % GST classified, and % with receipts before publishing any statement.
