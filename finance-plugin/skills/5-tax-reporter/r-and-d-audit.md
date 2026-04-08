---
name: r-and-d-audit
description: Pre-submission self-audit and Airwallex vs accountant reconciliation for R&D claim
menu-code: RA
---

# R&D Audit

Pre-submission self-audit checklist and data reconciliation for R&D Tax Incentive claim.

## Prerequisites

- Load `references/r-and-d-tax-incentive.md` for compliance requirements
- Load `references/r-and-d-activities-fy2025.md` for registered activities
- Ensure R&D Categorize (RC) has been run first

## Process

### Part A: Data Reconciliation (Airwallex vs Accountant)

1. **Load accountant data:**
   - Read `finance/tax/FY2025/income-statement.json` (system-generated from Airwallex)
   - Read accountant PDFs from `finance/tax/FY2025/FY24/25 from Accountant/`

2. **Compare key figures:**

   | Line Item | Accountant (Xero) | Airwallex System | Difference | Explanation |
   |-----------|-------------------|------------------|------------|-------------|
   | Revenue | $193,785.90 | system figure | delta | FX methodology |
   | Freelancers | $85,586.40 | system figure | delta | FX rate source |
   | Software | $21,966.40 | system figure | delta | Category mapping |
   | Contractors | ${CONTRACTOR_PAYMENT} | system figure | delta | Direct match |

3. **Document FX rate differences:**
   - Accountant uses XE.com rates (0.653147 USD, 0.892616 CAD at 30 Jun 2025)
   - System uses RBA daily rates
   - Calculate impact on R&D eligible amounts

4. **Decision: Use accountant's Xero figures as authoritative** for the R&D claim since they match the lodged company tax return.

5. **Create reconciliation report** at `finance/tax/FY2025/r-and-d/reconciliation-report.json`

### Part B: R&D Claim Self-Audit

6. **Check each audit criterion:**

   **Activity Registration:**
   - [ ] All R&D activities have descriptions with hypothesis, uncertainty, methodology
   - [ ] Core activities demonstrate genuine technical uncertainty
   - [ ] Supporting activities are directly related to a core activity
   - [ ] No overseas activities claimed without Overseas Finding
   - [ ] Activities are registered before 30 April 2026 deadline

   **Expenditure:**
   - [ ] Every R&D-tagged transaction has an activity_id
   - [ ] Every R&D-tagged transaction has a category (core/supporting)
   - [ ] Apportionment ratios are documented and defensible
   - [ ] No excluded expense types claimed (travel, meals, rent, etc.)
   - [ ] No overseas contractor payments claimed (no Overseas Finding)
   - [ ] Software tools are predominantly used for R&D, not general business
   - [ ] Total R&D eligible spend crosses minimum threshold ($20K)

   **Evidence:**
   - [ ] Each activity has contemporaneous evidence (created during FY)
   - [ ] Git commits, Upwork records, or other dated evidence exists
   - [ ] Evidence is indexed in evidence-log.json
   - [ ] No after-the-fact documentation presented as contemporaneous

   **Financial Accuracy:**
   - [ ] R&D expenditure totals reconcile with accountant figures
   - [ ] GST correctly excluded from R&D amounts (GST-free exports, 1/11th rule)
   - [ ] FX amounts correctly converted to AUD
   - [ ] No double-counting between Airwallex and Amex sources

7. **Flag any issues found:**
   - CRITICAL: Would likely result in claim rejection or penalty
   - WARNING: Could be questioned in an ATO audit
   - INFO: Minor issue, easily addressed

8. **Generate audit report** at `finance/tax/FY2025/r-and-d/audit-report.json`:
   ```json
   {
     "financial_year": "FY2025",
     "audit_date": "ISO timestamp",
     "reconciliation": { ... },
     "checklist_results": [ ... ],
     "flags": [
       {
         "severity": "CRITICAL|WARNING|INFO",
         "area": "activities|expenditure|evidence|financial",
         "description": "What the issue is",
         "recommendation": "How to fix it"
       }
     ],
     "summary": {
       "total_r_and_d_spend": 0.00,
       "estimated_offset": 0.00,
       "checklist_pass_rate": "X/Y",
       "critical_flags": 0,
       "warning_flags": 0
     }
   }
   ```

## Output

```
R&D Self-Audit — {period}

  RECONCILIATION
    Accountant revenue:    ${accountant_rev}
    System revenue:        ${system_rev}
    Variance:              ${variance} ({variance_pct}%)
    Primary source:        Accountant (Xero)

  CHECKLIST
    Passed: {pass_count}/{total_count}
    Critical issues: {critical_count}
    Warnings: {warning_count}

  {list any CRITICAL or WARNING flags}

  R&D CLAIM SUMMARY
    Total eligible spend:  ${total_spend}
    Estimated offset:      ${offset} (43.5%)
    Activities:            {activity_count}
    Evidence items:        {evidence_count}

  Files created:
    - finance/tax/FY2025/r-and-d/reconciliation-report.json
    - finance/tax/FY2025/r-and-d/audit-report.json

  {recommendations}
```
