---
name: dedup-check
description: Find potential duplicates across Airwallex and Amex by amount, date proximity, and merchant similarity
menu-code: DD
---

# Dedup Check

Find potential duplicate transactions across Airwallex and Amex sources.

## Process

1. **Load finance-data.json** — separate transactions by `account_source` into Airwallex and Amex groups

2. **Cross-source comparison:**
   - For each Amex transaction, compare against all Airwallex transactions:
     - **Amount match:** Exact amount match (within $0.01 for rounding)
     - **Date proximity:** Transaction dates within +/- 3 days of each other
     - **Merchant similarity:** Fuzzy match on `merchant_name_normalized` (Amex descriptions often differ from Airwallex merchant names)
   - Score each pair: amount match (40%) + date proximity (30%) + merchant similarity (30%)
   - Flag pairs scoring above 70% as potential duplicates

3. **Load known patterns:**
   - Read `_bmad/_memory/bmad-apg-fin-3-reconciler-sidecar/patterns.md`
   - Check "Confirmed Duplicates" — auto-mark known pairs
   - Check "Confirmed Non-Duplicates" — exclude known false positives
   - Check "Known Merchant Aliases" — boost merchant similarity for known Amex-to-Airwallex name mappings

4. **Present results in table:**

   ```
   Potential Duplicates Found: {count}

   | # | Amex ID | Amex Date | Amex Merchant | Airwallex ID | AW Date | AW Merchant | Amount | Score |
   |---|---------|-----------|---------------|--------------|---------|-------------|--------|-------|
   | 1 | amex_abc123 | 2026-03-15 | ANTHROPIC | aw_def456 | 2026-03-14 | Anthropic | $99.00 | 95% |
   ```

5. **For each flagged pair, ask user:**
   - `[D]` Confirm duplicate — mark one as `status: "duplicate"`, link to the other
   - `[N]` Not a duplicate — mark as confirmed non-duplicate in patterns.md
   - `[S]` Skip — leave flagged for later review

6. **Update finance-data.json:**
   - Confirmed duplicates: set `status: "duplicate"` on the Amex record, add `duplicate_of: "{airwallex_id}"`
   - Update `potential_duplicate` flags based on decisions

7. **Update patterns.md:**
   - New merchant alias mappings (Amex name -> Airwallex name)
   - Confirmed duplicate pairs
   - Confirmed non-duplicate pairs

## Output

```
Dedup check complete.
  Pairs evaluated: {count}
  Confirmed duplicates: {dup_count}
  Confirmed non-duplicates: {non_dup_count}
  Skipped (pending review): {skip_count}
  New merchant aliases learned: {alias_count}
```
