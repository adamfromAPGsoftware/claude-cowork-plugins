---
name: process-receipt
description: Process a receipt photo via vision, extract data, match to transaction, save receipt file
menu-code: PR
---

# Process Receipt

User shares a receipt photo. Read it with vision, extract key fields, match to a transaction, and update the record.

## Process

1. **Read the receipt image** using Claude Code's built-in vision capability. The user will share the image directly in the conversation (drag-and-drop, paste, or file path).

2. **Extract receipt data:**
   - Merchant name (as printed on receipt)
   - Total amount (including GST if shown)
   - GST amount (if separately itemised)
   - Date of transaction
   - Currency (default AUD if not shown)
   - Any other notable line items

3. **Present extracted data for confirmation:**
   ```
   Receipt extracted:
     Merchant: {merchant_name}
     Date: {date}
     Total: ${amount} {currency}
     GST: ${gst_amount} (or "not shown on receipt")
   
   Confirm these details? [y/n/edit]
   ```

4. **Search finance-data.json for matching transaction:**
   - Filter by: amount within ± $0.05 AND date within ± 3 days
   - If **single match**: present it and ask to confirm attachment
   - If **multiple matches**: present all candidates as a numbered list, let user select
   - If **no match**: inform user, ask if they want to attach manually by transaction ID

5. **Save receipt image** to `finance/receipts/{YYYY-MM-DD}-{merchant-slug}.{ext}`:
   - Derive `merchant-slug` from normalized merchant name (lowercase, hyphens, no special chars)
   - If file already exists at that path, append a counter: `-2`, `-3`, etc.
   - Copy (not move) the original file

6. **Update the matched transaction** in finance-data.json:
   - Set `receipt` field to the saved file path (relative to project root)
   - If GST amount was extracted and confirmed by user: set `gst_amount` and `gst_status: "confirmed"`
   - If GST not shown on receipt: set `gst_status: "unknown"`

7. **Save finance-data.json**

## Output

```
Receipt processed.
  Merchant: {merchant_name}
  Amount: ${amount}
  GST: ${gst_amount or "unknown"}
  Matched to: {transaction_id} ({date} | {merchant_name_normalized})
  Saved to: finance/receipts/{filename}
```
