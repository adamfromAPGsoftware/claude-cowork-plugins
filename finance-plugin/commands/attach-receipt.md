---
description: Process a receipt photo — extract merchant, amount, date, GST via vision and match to transaction
---

Process a receipt image shared in the conversation:

1. Read the receipt image using Claude Code vision
2. Extract: merchant name, total amount, date, GST amount (if shown)
3. Search `finance/finance-data.json` for matching transactions (merchant + amount + date within 7 days)
4. If single match found, attach receipt data to the transaction's `receipt` field and update `gst_amount` / `gst_status`
5. If multiple matches, present candidates and ask which transaction to attach to
6. If no match, offer to store as an unmatched receipt for later reconciliation
7. Save the receipt image to `finance/receipts/` with a descriptive filename

$ARGUMENTS
