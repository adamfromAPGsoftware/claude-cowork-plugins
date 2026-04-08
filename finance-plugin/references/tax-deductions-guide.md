# Tax Deductions & Credits Guide — {YOUR_COMPANY_LEGAL}

> Company tax reference for a small proprietary company (< $10M turnover, sole director, software consultancy).
> All thresholds are FY2024-25 unless noted. ATO references included for each item.

---

## 1. Home Office Deductions

operates primarily from Adam's home. As a **company**, the deduction method differs from sole traders.

### Company Claiming Method

A company cannot use the individual 67c/hr fixed-rate method. Instead, the company must have a **genuine, market-rate rental agreement** with the property owner (Adam) if it wants to claim occupancy expenses directly.

**Without a formal lease:** The company can reimburse the director for home office expenses, which the company claims as a deduction and the director declares as income (wash for tax but allows the deduction at company level).

### What's Claimable

| Expense | Method | Notes |
|---------|--------|-------|
| Running costs (electricity, internet, cleaning) | Actual cost × business use % | Need records of usage split |
| Occupancy costs (rent/mortgage interest, rates, insurance) | Only with formal lease to company | Creates rental income for Adam |
| Depreciation of home office assets | Per-asset basis | Laptops, monitors, desk, chair |

### Current Approach (Long's Method)

Long used **${HOME_OFFICE_DEDUCTION}.45** as "Utilities/Internet/Home Office" — this is the 67c/hr fixed rate method applied to Adam as an employee/director of the company. This is the simplest compliant approach.

**ATO Reference:** [Home-based business expenses – company or trust](https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/income-and-deductions-for-business/deductions/deductions-for-home-based-business-expenses)

### Action Items

- [x] Current claim of ${HOME_OFFICE_DEDUCTION} via director reimbursement is reasonable
- [ ] Consider formal lease arrangement if home office has character of "place of business" — could claim occupancy expenses (mortgage interest, rates) but creates CGT implications on home sale

---

## 2. Motor Vehicle & Travel

### Cents-per-Kilometre Method

- **Rate:** 85 cents per km (FY2024-25)
- **Cap:** 5,000 business km per year = max $4,250 deduction
- No written evidence required but must be able to show how you calculated business km

### Logbook Method

- Keep a logbook for a continuous 12-week period (valid for 5 years)
- Claim actual expenses × business use percentage
- Includes fuel, rego, insurance, depreciation, servicing

### Travel (Non-Car)

- Flights, accommodation, meals during business travel are fully deductible
- Must be primarily for business purpose
- International travel: apportion if mixed business/personal

### Specifics

- Long claimed **$25,529** in travel for FY25 — this includes flights and accommodation for business trips
- No car logbook currently maintained
- Consider starting a logbook if regular client visits expected

**ATO Reference:** [Motor vehicle expenses](https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/income-and-deductions-for-business/deductions/motor-vehicle-expenses)

---

## 3. Technology & Equipment — Instant Asset Write-Off

### FY2024-25 Rules

- **Threshold:** $20,000 per asset (cost must be **less than** $20,000)
- **Eligibility:** Aggregated turnover < $10M + using simplified depreciation rules
- **Per-asset basis** — can write off multiple assets, each under $20K
- Covers new and second-hand assets
- First used or installed ready for use between 1 Jul 2024 – 30 Jun 2025

### What Can Write Off Instantly

- Laptops, monitors, peripherals (< $20K each)
- Office furniture (desk, chair, etc.)
- Software licenses (if capitalised as an asset)
- Phone and tablet devices

### Assets $20K or More

- Go into the small business depreciation pool
- Pool balance < $20K at end of year = write off the entire pool
- Otherwise: 15% first year, 30% subsequent years

### Simplified Depreciation Rules

If you choose simplified depreciation, you must use it for **at least 2 years** before opting out. If you opt out, you can't re-enter for 2 years.

**ATO Reference:** [Instant asset write-off for eligible businesses](https://www.ato.gov.au/businesses-and-organisations/small-business-newsroom/$20000-instant-asset-write-off-for-2024-25)

---

## 4. R&D Tax Incentive

### Eligibility

- **Turnover:** < $20M → entitled to **refundable** tax offset
- **Rate:** Company tax rate (25%) + 18.5% premium = **43.5% refundable offset**
- **LOE (Letter of Engagement):** Already signed with R&D tax consultant
- **Entity type:** PTY LTD incorporated in Australia ✓

### Offset Calculation

For every $1 of eligible R&D expenditure, gets a **43.5 cent** refundable tax offset. Since company tax rate is 25%, the **net benefit is 18.5 cents per dollar** of R&D spend.

If company has no tax liability (profit zeroed by director salary), the **full 43.5% offset is refunded as cash**.

### What Qualifies as R&D (Software)

Per the ATO Software Development Sector Guide:

**Eligible (core R&D):**
- Developing new algorithms or AI models where outcome is genuinely uncertain
- Building novel software architectures that haven't been done before
- Experimental development to resolve technical uncertainty

**Eligible (supporting R&D):**
- Data collection, testing, and analysis directly supporting core R&D
- Building prototypes to test hypotheses
- Infrastructure work directly enabling core R&D activities

**NOT eligible:**
- Routine software development, bug fixes, maintenance
- Adapting existing solutions to new clients
- Activities where the outcome could reasonably be determined in advance
- Commercial implementation of proven technology

### R&D Activities (Potentially Eligible)

- AI agent development (BMAD framework) — novel multi-agent orchestration
- Automated business process extraction from unstructured transcripts
- Custom AI pipeline development with uncertainty in outcomes

### Key Requirements

1. Register with AusIndustry **within 10 months** of end of FY (April 2026 for FY25)
2. Must demonstrate "technical uncertainty" — can't just be new to the company
3. Contemporaneous records are critical (git commits, experiment logs, decision docs)
4. R&D activities must be conducted on behalf of the registered entity (PTY LTD)

**ATO Reference:** [R&D Tax Incentive](https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/incentives-and-concessions/research-and-development-tax-incentive-and-concessions/research-and-development-tax-incentive/rates-of-r-d-tax-incentive-offset)
**Sector Guide:** [Software Development](https://business.gov.au/grants-and-programs/research-and-development-tax-incentive/sector-guides-for-r-and-d-tax-incentive-applicants/software-development)

---

## 5. Director Salary & Superannuation Optimisation

### Director Salary

- Director salary reduces company profit → reduces company tax liability
- Long set FY25 director fee at **${DIRECTOR_SALARY}** — just under tax-free threshold ($18,200) + low-income tax offset (LITO)
- With LITO ($700 max for income ≤ $37,500), effective tax-free threshold is ~$21,884
- **Result:** $0 company tax, $0 personal tax (or minimal)

### Superannuation — Company Contributions

The company can make **tax-deductible** super contributions for Adam as a director/employee:

- **Concessional cap:** $30,000 per year (FY2024-25)
- **SG rate:** 11.5% of ordinary time earnings (FY2024-25)
- SG on ${DIRECTOR_SALARY} salary = $2,530 (mandatory)
- **Voluntary employer contributions** up to the $30,000 cap are also deductible
- Super contributions are taxed at **15%** in the fund (vs 25% company tax or marginal personal rate)

### Carry-Forward Unused Concessional Cap

If total super balance < $500,000 at 30 June prior year, you can carry forward **unused** cap amounts from the past 5 years.

**Example:** If Adam contributed $3,000/yr for 5 years, unused cap = ~$125,000+ available in a single year.

### Optimisation Strategy

| Scenario | Company Tax | Personal Tax | Super Tax | Total Tax |
|----------|-------------|-------------|-----------|-----------|
| Current (salary $22K, no extra super) | $0 | $0 | ~$380 | ~$380 |
| Salary $22K + $27.5K super top-up | $0 | $0 | $4,500 | $4,500 |
| Higher salary $50K + $30K super | Tax on remaining profit | ~$5,000 | $4,500 | Variable |

**Key insight:** Making voluntary super contributions is tax-efficient (15% vs 25% company or 19-32.5% personal) BUT locks funds until preservation age.

**ATO Reference:** [Contributions caps](https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/contributions-caps)

---

## 6. GST on Exports

### Rule

Services supplied to **non-residents outside Australia** are **GST-free** under s38-190 of the GST Act.

### Application

- **Upwork contracts** with overseas clients → GST-free (services performed for non-residents, consumed outside Australia)
- **Direct overseas clients** (e.g., via Wise transfers) → GST-free if recipient is outside Australia
- **Australian clients** → GST-inclusive (10%)

### What This Means

- Don't charge GST on overseas invoices
- Still claim full GST input credits on purchases used to deliver those services
- Must report GST-free export sales in BAS (G2 field: Export sales)

### Long's FY25 Split

- GST-free sales: **$119,126.37** (Upwork + overseas direct)
- GST-inclusive sales: **$74,659.54** (Australian clients)
- GST collected: ~$6,787 (1/11th of GST-inclusive sales)

**ATO Reference:** [Exports and GST](https://www.ato.gov.au/businesses-and-organisations/international-tax-for-business/australians-doing-business-overseas/exports-and-gst)

---

## 7. Small Business Entity (SBE) Concessions

qualifies as an SBE (aggregated turnover < $10M). Available concessions:

| Concession | Benefit | Status |
|-----------|---------|------------|
| Instant asset write-off | Immediate deduction for assets < $20K | ✓ Available |
| Simplified depreciation pool | 15% first year, 30% ongoing for pooled assets | ✓ Available |
| Simplified trading stock | Don't account for trading stock changes < $5K | N/A (services business) |
| Prepaid expenses | Immediate deduction for prepayments ≤ 12 months | ✓ Available |
| Two-year amendment period | ATO has 2 years (not 4) to amend assessments | ✓ Applies |
| PAYG instalments | Can use GDP-adjusted notional tax | ✓ Available |
| FBT car parking exemption | No FBT on car parking if SBE | ✓ Available |
| CGT concessions | 50% active asset reduction, 15-year exemption, retirement exemption, rollover | ✓ Available |

### Prepaid Expenses

If prepays annual software subscriptions (e.g., 12-month Claude Pro, GitHub, etc.), the **entire amount is deductible in the year of payment** under SBE rules, rather than being spread over the service period.

**ATO Reference:** [Small business entity concessions](https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/incentives-and-concessions/small-business-entity-concessions)

---

## 8. Superannuation — Detailed

### Mandatory SG

- **Rate:** 11.5% (FY2024-25), rising to 12% from 1 Jul 2025
- **On:** Ordinary time earnings (director salary)
- **Due:** Quarterly (28 days after end of quarter)
- **Penalty:** SG charge (non-deductible) if late

### Voluntary Employer Contributions

- Company makes additional super contributions for Adam
- Tax-deductible for the company
- Taxed at 15% in the super fund
- Counts toward concessional cap ($30,000)

### Personal Deductible Contributions

- Adam can make personal contributions and claim a tax deduction (s290-150 notice)
- Also counts toward concessional cap
- Useful if company doesn't make voluntary employer contributions

### Division 293 Tax

- Additional 15% tax on concessional contributions if income + contributions > $250,000
- **Not applicable to {YOUR_COMPANY}** (total well under $250K)

---

## 9. Training & Professional Development

### Deductible for the Company

The company can deduct costs of training that:
- Maintains or improves skills used in the business
- Is sufficiently connected to current income-earning activities

### Examples for APG

- AI/ML courses, cloud certifications (AWS, GCP)
- Business coaching and mentoring programs
- Conference attendance (including travel)
- Professional memberships and subscriptions
- Books, online courses (Udemy, Coursera, etc.)
- Industry event tickets

### Not Deductible

- Training for a completely new career or qualification unrelated to current business
- General interest courses with no business connection

**ATO Reference:** [Self-education expenses](https://www.ato.gov.au/individuals-and-families/income-deductions-offsets-and-records/deductions-you-can-claim/education-training-and-seminars/self-education-expenses)

---

## 10. Export Market Development Grant (EMDG)

### What It Is

Australian Government grant (via Austrade) that reimburses up to **50% of eligible export marketing expenses**.

### Eligibility

- Australian business with turnover < $20M in grant year
- Spent at least $15,000 on eligible export promotion activities
- Income from exports (or likely to earn income from exports)
- Products/services must be substantially of Australian origin

### Eligible Expenses

- Overseas marketing/advertising
- International trade fairs and exhibitions
- Market research for overseas markets
- Overseas buyer visits
- Communications for export promotion
- Free samples for overseas buyers
- Overseas business travel (export promotion purpose)

### Grant Amount

- 50% reimbursement of eligible expenses above a $5,000 threshold
- Maximum grant: $770,000 over up to 8 grant agreements
- Paid in arrears after the grant period

### Applicability

- earns export income via Upwork (overseas software consulting)
- Could claim EMDG for: Upwork platform fees as marketing costs, overseas client travel, marketing materials targeting overseas clients
- **Minimum $15,000 spend** may be hard to reach currently
- Worth monitoring as overseas revenue grows

**Reference:** [EMDG — Austrade](https://www.austrade.gov.au/en/how-we-can-help-you/grants/export-market-development-grants)

---

## 11. Carry-Forward Tax Losses

### Company Rules

- A company can carry forward tax losses **indefinitely**
- Must satisfy either the **Continuity of Ownership Test (COT)** or the **Business Continuity Test (BCT)** to use carried-forward losses
- **COT:** Same persons must own majority (>50%) of voting/dividend/capital rights from loss year to deduction year
- (sole director/shareholder) easily satisfies COT

### Loss Carry-Back Offset

- Eligible companies can carry back losses to **offset against tax paid in prior years**
- Available for losses in FY2019-20 through FY2022-23 income years
- Offset claimed in the year the loss is made
- **Not currently available for FY2024-25** losses (scheme ended after FY2022-23)

### Specifics

- If has tax losses from prior years (FY23/24), these can offset future profits
- Since Long zeroes profit with director salary, unlikely to have carried-forward losses
- But if R&D offset creates a loss, that loss carries forward

**ATO Reference:** [Business losses](https://www.ato.gov.au/businesses-and-organisations/income-deductions-and-concessions/income-and-deductions-for-business/business-losses)

---

## Summary — Deduction Checklist (FY2025)

| # | Deduction/Credit | Est. Value | Status |
|---|-----------------|-----------|--------|
| 1 | Home office (67c/hr via director) | ${HOME_OFFICE_DEDUCTION} | ✓ Claimed |
| 2 | Travel (flights, accommodation) | $25,529 | ✓ Claimed |
| 3 | Instant asset write-off (< $20K/asset) | Variable | ✓ Available |
| 4 | R&D Tax Incentive (43.5% offset) | **High value** | ◐ LOE signed, needs registration |
| 5 | Director salary (tax-free threshold) | ${DIRECTOR_SALARY} | ✓ Claimed |
| 6 | Super contributions (concessional) | Up to $30,000 | ◐ Only SG minimum currently |
| 7 | GST-free exports | Reduces GST payable | ✓ Applied |
| 8 | SBE prepaid expenses | Variable | ✓ Available |
| 9 | Training & development | Variable | ✓ Deductible |
| 10 | EMDG grant | Up to 50% of export marketing | ○ Not yet applied |
| 11 | Carry-forward losses | N/A currently | ○ No losses to carry |

### Highest-Impact Actions

1. **R&D Tax Incentive** — Register eligible activities with AusIndustry by April 2026. At 43.5% refundable offset, even $50K of eligible R&D spend = $21,750 cash refund.
2. **Super top-up** — Voluntary employer contributions up to $30K cap. Tax-efficient at 15% vs 25% company rate. Consider carry-forward of unused cap from prior years.
3. **EMDG** — Monitor export marketing spend. If approaching $15K threshold, apply for reimbursement.
