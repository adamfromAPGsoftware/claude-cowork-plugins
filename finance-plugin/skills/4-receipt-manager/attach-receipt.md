---
name: attach-receipt
description: Manually link a receipt file path to a specific transaction by ID
menu-code: AT
---

# Attach Receipt

Manually link a receipt file to a specific transaction when auto-matching isn't suitable.

## Process

1. **Get transaction ID from user.** If not provided, ask for it. Optionally accept a search term (merchant name, date, amount) to help locate the transaction.

2. **Validate the transaction exists** in finance-data.json. Show the transaction details:
   ```
   Transaction: {transaction_id}
     Date: {date}
     Merchant: {merchant_name_normalized}
     Amount: ${amount}
     Current receipt: {receipt or "none"}
   ```

3. **Get the receipt file path from user.** Verify the file exists at the given path.

4. **Copy the receipt** to `finance/receipts/{YYYY-MM-DD}-{merchant-slug}.{ext}`:
   - Use the transaction date and merchant name for the filename
   - If the file is already in `finance/receipts/`, just record the path without copying

5. **Ask about GST** if `gst_status` is not already `"confirmed"`:
   ```
   Does this receipt show a GST amount? [amount / no / skip]
   ```
   - If amount provided: set `gst_amount` and `gst_status: "confirmed"`
   - If no: set `gst_status: "no_gst"`
   - If skip: leave as-is

6. **Update the transaction** in finance-data.json:
   - Set `receipt` field to the saved file path
   - Update GST fields if provided

7. **Save finance-data.json**

## Output

```
Receipt attached.
  Transaction: {transaction_id} ({date} | {merchant_name_normalized} | ${amount})
  Receipt: finance/receipts/{filename}
  GST: ${gst_amount or status}
```
