---
name: r-and-d-submit
description: Generate AusIndustry registration form data and submission pack
menu-code: RS
---

# R&D Submit

Generate structured data matching AusIndustry registration form requirements and compile a complete submission pack for the R&D tax consultant.

## Prerequisites

- R&D Document (RD) has been run — activity-register.json exists
- R&D Categorize (RC) has been run — transactions are tagged
- R&D Audit (RA) has been run — no critical flags
- Load `references/r-and-d-tax-incentive.md` for compliance requirements

## Process

1. **Load all R&D data:**
   - `finance/tax/FY2025/r-and-d/activity-register.json`
   - `finance/tax/FY2025/r-and-d/evidence-log.json`
   - `finance/tax/FY2025/r-and-d/expenditure-schedule.json` (from GG)
   - `finance/tax/FY2025/r-and-d/audit-report.json`
   - `finance/tax/FY2025/r-and-d/reconciliation-report.json`

2. **Generate AusIndustry registration data:**

   For each R&D activity, format responses to the standard registration questions:

   **Company Details:**
   - Entity name: {YOUR_COMPANY_LEGAL}
   - ABN: {YOUR_ABN}
   - Income year: 1 July 2024 to 30 June 2025
   - Aggregated turnover: $193,785.90

   **For each Core R&D Activity:**
   - Activity title
   - Describe the new knowledge you sought to generate
   - Describe the technical uncertainty — what could not be determined in advance?
   - Describe the systematic progression of work (hypothesis → experiment → evaluation)
   - What was the outcome?
   - Was any part of this activity conducted overseas? (No — for FY25 claim)

   **For each Supporting R&D Activity:**
   - Activity title
   - Which core activity does this support?
   - How is this activity directly related to the core activity?
   - Was this activity undertaken for the dominant purpose of supporting the core activity?

3. **Generate expenditure summary by activity:**

   ```
   Activity RD-01: BMAD Multi-Agent Orchestration
     Contractors: ${amount}
     Software:    ${amount}
     Hosting:     ${amount}
     Total:       ${amount}

   Activity RD-02: AI Process Extraction
     ...

   TOTAL ELIGIBLE R&D EXPENDITURE: ${grand_total}
   ESTIMATED R&D TAX OFFSET (43.5%): ${offset}
   ```

4. **Compile submission pack** in `finance/tax/FY2025/r-and-d/submission-pack/`:

   ```
   submission-pack/
   ├── registration-data.json      # Structured form data for R&D consultant
   ├── registration-narrative.md   # Human-readable activity descriptions
   ├── expenditure-schedule.json   # Spend by activity, category, quarter
   ├── evidence-index.md           # List of all evidence with locations
   ├── reconciliation-summary.md   # Airwallex vs Xero crosswalk
   └── audit-checklist.md          # Self-audit results and recommendations
   ```

5. **Generate registration-narrative.md** with activity descriptions formatted for copy-paste into the AusIndustry portal.

6. **Generate evidence-index.md** listing all contemporaneous records by activity.

## Output

```
R&D Submission Pack — {period}

  AusIndustry Registration Data
    Core activities:       {core_count}
    Supporting activities: {supporting_count}
    Overseas activities:   0 (none claimed)

  Expenditure Schedule
    Total R&D spend:       ${total_spend}
    Estimated offset:      ${offset} (43.5%)

  Submission Pack Files:
    - finance/tax/FY2025/r-and-d/submission-pack/registration-data.json
    - finance/tax/FY2025/r-and-d/submission-pack/registration-narrative.md
    - finance/tax/FY2025/r-and-d/submission-pack/expenditure-schedule.json
    - finance/tax/FY2025/r-and-d/submission-pack/evidence-index.md
    - finance/tax/FY2025/r-and-d/submission-pack/reconciliation-summary.md
    - finance/tax/FY2025/r-and-d/submission-pack/audit-checklist.md

  NEXT STEPS:
    1. Review registration-narrative.md for accuracy
    2. Hand off submission-pack/ to R&D tax consultant
    3. Consultant submits via AusIndustry portal (incentives.business.gov.au)
    4. Expenditure schedule included in company tax return
```
