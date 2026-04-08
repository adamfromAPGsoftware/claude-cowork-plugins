---
name: manual-match
description: Present ambiguous matches for user decision
menu-code: MM
---

# Manual Match

Present ambiguous reconciliation matches for user decision, ranked by confidence with full context.

## Process

1. **Load finance-data.json** — filter to transactions where `reconciliation_status == "ambiguous"`

2. **If no ambiguous transactions:** Inform user all matches are resolved. Suggest [AR] Auto-Reconcile if there are unmatched transactions remaining.

3. **For each ambiguous transaction, present:**

   ```
   Transaction #{n} of {total}
   ─────────────────────────────
   ID: {transaction_id}
   Date: {date} | Source: {account_source}
   Merchant: {merchant_name_normalized}
   Amount: ${amount}
   Description: {original_description}

   Candidate matches:
   | # | Type | CRM ID | Reference | Date | Amount | Confidence |
   |---|------|--------|-----------|------|--------|------------|
   | 1 | Invoice | INV-042 | {ref} | 2026-03-12 | $500.00 | 78% |
   | 2 | Bill | BILL-019 | {ref} | 2026-03-14 | $500.00 | 65% |

   Actions:
   [1-N] Select match number
   [U] Mark as unmatched (no CRM record exists)
   [S] Skip for now
   [C] Create new CRM record for this transaction
   ```

4. **Process user decision:**
   - **Select match:** Set `reconciliation_status: "reconciled"`, store CRM entity reference, update confidence to `"manual"`
   - **Mark unmatched:** Set `reconciliation_status: "unmatched_confirmed"` — will not appear in future ambiguous lists
   - **Skip:** Leave as `reconciliation_status: "ambiguous"`
   - **Create new:** Note for [SC] Sync CRM to create the record

5. **Update finance-data.json** after each decision (write-through, not batched)

6. **Update patterns.md** with any new matching patterns discovered (e.g., specific merchant always maps to a specific CRM contact)

## Output

```
Manual matching complete.
  Presented: {count}
  Resolved: {resolved_count}
  - Matched to CRM: {matched_count}
  - Confirmed unmatched: {unmatched_count}
  - Flagged for CRM creation: {create_count}
  Skipped: {skip_count}
```
