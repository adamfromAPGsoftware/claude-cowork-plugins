---
name: leak-detector
description: Scan for financial leaks — duplicates, forgotten subscriptions, anomalies
menu-code: LD
---

# Leak Detector

Scan finance-data.json for potential financial leaks.

## Process

1. **Load finance-data.json** — Read all transactions

2. **Run detection scans:**

   ### Duplicate Charges
   - Find pairs where: same `merchant_name_normalized` + same `amount` within 24 hours
   - Exclude known legitimate duplicates (user-dismissed flags)
   
   ### Unexpected Recurring
   - Find merchants that charge monthly but aren't in known recurring charges (from memory `patterns.md`)
   - Detect pattern: same merchant, similar amount (within 10%), roughly monthly cadence
   - Flag if not previously acknowledged
   
   ### Anomalous Amounts
   - For each merchant with 3+ transactions, calculate the average and standard deviation
   - Flag any transaction >2 standard deviations above the merchant average
   
   ### Unknown Merchants
   - Find transactions from merchants that appear only once and exceed $100
   - Especially flag if the merchant name is generic or truncated

3. **Present findings:**

   ```
   LEAK DETECTION REPORT
   
   🔴 DUPLICATES ({count})
   | Date       | Merchant    | Amount | Txn IDs          | Status |
   |------------|-------------|--------|------------------|--------|
   | 2026-03-15 | Anthropic   | $500   | txn_001, txn_002 | NEW    |
   
   🟡 UNEXPECTED RECURRING ({count})
   | Merchant       | Amount  | Frequency | First Seen | Last Seen |
   |----------------|---------|-----------|------------|-----------|
   | Unknown SaaS   | $29/mo  | Monthly   | 2026-01    | 2026-03   |
   
   🟡 ANOMALOUS AMOUNTS ({count})
   | Date       | Merchant | Amount | Average | Deviation |
   |------------|----------|--------|---------|-----------|
   | 2026-03-20 | AWS      | $1,200 | $340    | +253%     |
   
   ⚪ UNKNOWN MERCHANTS ({count})
   | Date       | Merchant         | Amount |
   |------------|------------------|--------|
   | 2026-03-10 | STRIPE* UNKN     | $150   |
   ```

4. **For each new finding:**
   - Ask user: "Flag as leak? [confirm / dismiss / investigate]"
   - If confirmed: add to `leak_flags[]` in finance-data.json with status `confirmed`
   - If dismissed: add with status `dismissed` (prevents re-flagging)
   - If investigate: leave as `open`

5. **Update finance-data.json** with new/updated leak flags

## Output

Present the full report, then summarize: "{count} new flags, {count} dismissed, {count} confirmed leaks totalling ${amount}"
