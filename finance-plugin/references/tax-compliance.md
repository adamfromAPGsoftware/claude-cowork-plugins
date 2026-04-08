# Australian Tax Compliance Reference

Tax rules and calculations used by the Finance Plugin for BAS, annual tax summaries, and grant eligibility.

## Financial Year and BAS Quarters

The Australian financial year runs **1 July to 30 June**.

| Quarter | Period | BAS Due Date |
|---------|--------|-------------|
| Q1 | 1 July – 30 September | 28 October |
| Q2 | 1 October – 31 December | 28 February |
| Q3 | 1 January – 31 March | 28 April |
| Q4 | 1 April – 30 June | 28 July |

FY notation: **FY2026** = 1 July 2025 – 30 June 2026.

## GST Calculation

Standard GST rate is **10%**.

For GST-inclusive amounts, the GST component is:

```
GST = total_amount / 11
```

This is the **1/11th rule** — every $11 spent includes $1 of GST.

### GST-Free Categories

The following categories are **always GST-free** (no GST component to claim):

- **Bank fees** — account fees, transaction fees, interest charges
- **FX conversions** — currency conversion charges, spread costs
- **Government charges** — ASIC fees, ABN registration, government levies
- **Financial supplies** — loan repayments, insurance premiums (input-taxed)

### GST Status Values

| Status | Meaning |
|--------|---------|
| `included` | GST is included in the amount — claim 1/11th |
| `excluded` | Amount is GST-exclusive — GST is additional |
| `exempt` | No GST applies (GST-free category) |
| `unknown` | Not yet determined — needs manual review before BAS |

## R&D Tax Incentive

> **Detailed reference:** See `references/r-and-d-tax-incentive.md` for comprehensive R&D Tax Incentive guide including overseas activity rules, eligible expenditure, documentation requirements, and Company-specific guidance.

Summary: 43.5% refundable offset for aggregated turnover under $20M. Core R&D must be conducted in Australia. Overseas activities require an Overseas Finding submitted before end of income year.

| Category | Examples | Eligibility Notes |
|----------|----------|-------------------|
| Software development tools | IDE licenses, GitHub, CI/CD platforms | Must be used predominantly for R&D activities |
| Cloud hosting | AWS, GCP, Azure, Vercel, Railway | Apportion between R&D and production usage |
| Contractor fees for R&D work | Development contractors on R&D projects | Must be AU-based or have Overseas Finding |
| Testing and QA tools | Testing platforms, device farms | Only R&D-related testing, not BAU |

**Not eligible:** General business software (accounting, CRM, email), marketing tools, office supplies, overseas contractor payments without Overseas Finding.

R&D activities must involve **technical uncertainty** and **systematic investigation**. Building a standard website or using off-the-shelf tools in standard ways does not qualify.

## Export Market Development Grants (EMDG)

Marketing spend for overseas markets may be eligible for EMDG reimbursement (up to 50% of eligible spend above $5,000 threshold).

Eligible categories:
- **Overseas marketing** — advertising targeting international markets
- **Trade shows** — international trade fair costs
- **Market research** — research into overseas market opportunities
- **Overseas travel** — business travel for market development (not delivery)

Tag eligible transactions with `emdg_eligible` in the tags array.

## Depreciation

### Instant Asset Write-Off (Small Business)

For businesses with aggregated turnover under $10M:

- Assets costing **$300 or less** — immediate deduction (no depreciation required)
- Assets costing **more than $300** — eligible for instant asset write-off under temporary full expensing provisions (check current threshold with ATO)

Applies to items in `office` and `equipment` categories: computers, monitors, desks, chairs, phones, etc.

### What Counts as an Asset

An asset is a physical item or distinct software license with an independent function. Subscriptions (monthly SaaS) are operating expenses, not assets.

## Foreign Currency Reporting

All amounts in the tax return must be reported in **AUD**.

- Use the **transaction-date exchange rate** (not the settlement date rate)
- Acceptable rate sources: RBA daily rate, Airwallex rate at time of transaction
- The `fx` field on each transaction stores the original currency, amount, and rate
- Flag any transactions missing FX data for manual rate lookup before lodging

## BAS Calculation Summary

For each BAS quarter:

```
1A  GST on sales (collected)     = sum of GST on income transactions
1B  GST on purchases (paid)      = sum of GST on expense transactions (1/11th of GST-inclusive)
                                   excluding GST-free categories
──────────────────────────────────
Net GST = 1A - 1B
  Positive = amount owed to ATO
  Negative = refund from ATO
```

Always exclude transactions with `gst_status == "exempt"` from GST calculations. Flag transactions with `gst_status == "unknown"` as requiring review before the BAS can be lodged.
