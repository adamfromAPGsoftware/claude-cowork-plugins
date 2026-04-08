# Business Profile — Finance Agent Context

This file is loaded on activation by every finance skill. It provides the business context needed to make correct tax, accounting, and reporting decisions.

## Entity

- **Company:** {YOUR_COMPANY_LEGAL}
- **ABN/Tax ID:** {YOUR_TAX_ID}
- **Entity type:** {YOUR_ENTITY_TYPE} (e.g., PTY LTD, LLC, Corp)
- **Tax type:** COMPANY TAX — {YOUR_TAX_RATE}% base rate
- **GST/VAT registered:** Yes/No ({YOUR_TAX_BASIS} basis accounting)
- **Financial year:** {YOUR_FY_START} – {YOUR_FY_END}
- **Turnover band:** {YOUR_TURNOVER_BAND}

## Director / Owner

- **Name:** {YOUR_NAME}
- **Role:** {YOUR_ROLE}
- **No other employees** — all other work is via contractors/freelancers
- **Works from home** — dedicated home office setup

## Business Activity

- Software consulting and development
- AI agent development and automation
- Business process auditing
- Clients: domestic + international
- Contractors: domestic and overseas via {YOUR_PAYMENT_PLATFORM} payouts

## Accounts

### Primary Bank: {YOUR_BANK} (multi-currency business account)
- **{YOUR_PRIMARY_CURRENCY} wallet** — main operating account
- **USD wallet** — international deposits, contractor payments, software subscriptions
- Add additional currency wallets as needed

### Credit Card: {YOUR_CREDIT_CARD}
- Account ending **-XXXXX**
- Credit card is paid from primary bank account
- Statement transactions are separate from bank card transactions

### Accounting Software: {YOUR_ACCOUNTING_SOFTWARE}
- Synced with bank and tax authority
- Receipt inbox: {YOUR_RECEIPT_INBOX_EMAIL}

### Accountant
- Name: {YOUR_ACCOUNTANT_NAME}
- Email: {YOUR_ACCOUNTANT_EMAIL}
- Working papers stored in `finance/tax/accountant-reference/`

## Tax Structure

- Company revenue minus expenses = company profit
- Director salary allocated to reduce/zero out taxable profit
- Personal tax: director salary managed under tax-free threshold where possible
- Tax returns lodged periodically on {YOUR_TAX_BASIS} basis
- Tax collected on domestic sales, input credits claimed on business purchases
- Overseas income is tax-free export where applicable

## Key Tax Rules

- **Company tax rate:** {YOUR_TAX_RATE}%
- **Small Business Entity** concessions may apply
- **GST/VAT:** Collect on domestic sales, claim input credits, exports may be exempt
- **R&D Tax Incentive:** Check eligibility for your jurisdiction
- **Director salary:** Must be reasonable, deductible to company, taxed as personal income
- **Carry-forward losses:** Company losses can be carried forward to offset future profits

## Non-Bank Deductions (Manual Claims)

These are legitimate business expenses not visible in bank transactions:

| Deduction | Amount | Basis |
|-----------|--------|-------|
| Director fee | ${YOUR_DIRECTOR_FEE} | Salary allocation |
| Home office | ${YOUR_HOME_OFFICE} | Working from home deduction |
| Phone | ${YOUR_PHONE} | Business use % of personal plan |
| Insurance | ${YOUR_INSURANCE} | Business insurance premiums |
| Registration fee | ${YOUR_REGISTRATION_FEE} | Annual company registration |

## Transaction Classification Rules

When classifying transactions from your bank:

| Source Type | Direction | Class | Notes |
|-------------|-----------|-------|-------|
| DEPOSIT | credit | **income** | Client payments — the ONLY source of revenue |
| YIELD | credit | **income** | Interest/returns on account balance |
| PAYOUT | debit | **expense** | Contractor payments, supplier payments |
| PAYOUT | credit | **refund** | Failed payment refunds |
| CONVERSION | any | **internal** | FX conversions between wallets — NOT income or expense |
| PAYMENT_ATTEMPT | any | **internal** | Credit card payments, wallet transfers — NOT income or expense |
| FEE | debit | **expense** | Platform fees, FX fees |
| Card (CLEARING) | debit | **expense** | Card purchases |
| Card (REFUND) | credit | **refund** | Merchant refunds |

**Critical:** CONVERSION and PAYMENT_ATTEMPT credits must NEVER be counted as income. These are internal wallet movements.

## Data Sources

| Source | Path | Purpose |
|--------|------|---------|
| Transaction ledger | `finance/finance-data.json` | All bank + credit card transactions |
| Account balances | `finance/balances.json` | Current wallet balances |
| FX rates cache | `finance/rba-rates.json` | Daily/monthly exchange rates |
| Credit card statements | `finance/statements/` | Raw CSV files |
| Accountant reference | `finance/tax/accountant-reference/` | Working papers, tax returns |
| Manual deductions | `finance/tax/{period}/manual-deductions.json` | Non-bank expenses |
| CRM | MCP: {YOUR_CRM} | Invoices, bills, contacts, projects |
| Email | MCP: Gmail | Receipts, accountant correspondence |
