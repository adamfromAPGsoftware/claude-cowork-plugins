---
name: pull-balances
description: Fetch current account balances from Airwallex
menu-code: PB
---

# Pull Balances

Fetch current account balances from Airwallex and update balances.json.

## Process

1. **Run balance script:**
   ```
   python3 finance-plugin/scripts/fetch-balances.py
   ```

2. **Review script output:**
   - Account balances per currency
   - Available vs pending amounts

3. **Update finance-data.json** balances section with the snapshot

4. **Update finance/balances.json** with the full response

## Output

Report:

```
Balances as of {timestamp}:
  AUD: ${available} available | ${pending} pending | ${total} total
  {other currencies if any}
```
