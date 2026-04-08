---
name: r-and-d-categorize
description: Tag transactions as R&D eligible based on eligibility rules and interactive review
menu-code: RC
---

# R&D Categorize

Tag transactions in finance-data.json as R&D eligible for the R&D Tax Incentive claim.

## Prerequisites

- Load `references/r-and-d-tax-incentive.md` for eligibility rules
- Load `references/r-and-d-activities-fy2025.md` for activity definitions (if exists)

## Process

1. **Get the financial year from user.** Default: FY2025 (1 Jul 2024 - 30 Jun 2025).

2. **Filter finance-data.json** to transactions within the date range.

3. **Apply automatic categorization rules:**

   **Australian Contractors → R&D eligible (auto-tag):**
   - merchant_name contains "{CONTRACTOR_5}" → `r_and_d_eligible: true, r_and_d_category: "core"`
   - merchant_name contains "Asher" or "Lewis Tucker" → `r_and_d_eligible: true, r_and_d_category: "core"`
   - merchant_name contains "{CONTRACTOR_7}" → `r_and_d_eligible: true, r_and_d_category: "core"`
   - merchant_name contains "{CONTRACTOR_8}" → `r_and_d_eligible: true, r_and_d_category: "supporting"`

   **R&D Software Tools → R&D eligible (auto-tag):**
   - merchant_name contains "Anthropic" or "Claude" → `r_and_d_eligible: true, r_and_d_category: "core"`
   - merchant_name contains "GitHub" → `r_and_d_eligible: true, r_and_d_category: "supporting"`
   - merchant_name contains "Cursor" → `r_and_d_eligible: true, r_and_d_category: "supporting"`
   - merchant_name contains "OpenRouter" → `r_and_d_eligible: true, r_and_d_category: "core"`
   - merchant_name contains "Supabase" → `r_and_d_eligible: true, r_and_d_category: "supporting"`
   - merchant_name contains "Vercel" → `r_and_d_eligible: true, r_and_d_category: "supporting", r_and_d_apportionment: 0.7`
   - merchant_name contains "Railway" → `r_and_d_eligible: true, r_and_d_category: "supporting", r_and_d_apportionment: 0.7`
   - merchant_name contains "Cloudflare" → `r_and_d_eligible: true, r_and_d_category: "supporting", r_and_d_apportionment: 0.5`

   **Overseas Contractors → NOT eligible for FY2024-25 (auto-exclude):**
   - merchant_name contains "{CONTRACTOR_1_FIRST}" or "{CONTRACTOR_1_LAST}" → `r_and_d_eligible: false, r_and_d_notes: "Overseas contractor - no Overseas Finding for FY2024-25"`
   - merchant_name contains "Muhammad" or "Reginaldo" → same
   - merchant_name contains "{CONTRACTOR_3}" → same
   - merchant_name contains "Yuliia" or "Dus" → same
   - merchant_name contains "{CONTRACTOR_9_FIRST}" or "{CONTRACTOR_9_LAST}" → `r_and_d_eligible: false, r_and_d_notes: "NZ contractor - no Overseas Finding for FY2024-25"`

   **Not Eligible (auto-exclude):**
   - category_id in ["travel", "meals", "office", "marketing", "professional", "insurance"] → `r_and_d_eligible: false`
   - merchant_name contains "Xero", "PandaDoc", "Google", "Skool", "Hireflix", "Lusha", "Calendly", "Webflow" → `r_and_d_eligible: false`

4. **Present borderline transactions** for user review:
   - Any software/hosting transactions not in the auto-tag lists above
   - Any contractors not in the known lists
   - Director fee transactions (may be partially eligible with time records)

5. **For each borderline transaction**, ask user:
   - Is this R&D related? (yes/no/partially)
   - If partially, what apportionment? (0.0 to 1.0)
   - Which R&D activity does it relate to?

6. **Update finance-data.json** with all R&D tags:
   ```json
   "tax": {
     "r_and_d_eligible": true|false,
     "r_and_d_category": "core"|"supporting"|null,
     "r_and_d_activity_id": "RD-01"|"RD-02"|...|null,
     "r_and_d_apportionment": 1.0,
     "r_and_d_notes": "justification string"|null
   }
   ```

7. **Calculate and present summary:**

## Output

```
R&D Categorization Complete — {period}

  Eligible transactions: {count} of {total}
  Total R&D eligible spend: ${total_eligible} (after apportionment)

  By category:
    Core R&D:       ${core_total} ({core_count} transactions)
    Supporting R&D: ${supporting_total} ({supporting_count} transactions)

  By type:
    Contractors (AU): ${contractor_total}
    Software & tools: ${software_total}
    Hosting:          ${hosting_total}
    Other:            ${other_total}

  Excluded (overseas, no Finding): ${overseas_total} ({overseas_count} transactions)

  Estimated R&D offset (43.5%): ${offset}

  Borderline items reviewed: {borderline_count}
  Items needing further review: {review_count}

  Finance-data.json updated with R&D tags.
```

8. **Save the file** and recommend running Generate Grant Report (GG) next.
