---
name: discover-accounts
description: Discover and list all ad accounts accessible with the current Meta access token
menu-code: DA
---

# Discover Accounts

Discover and list all Meta ad accounts accessible with the current access token.

## Process

1. **Run fetch script in discovery mode** using Desktop Commander's `execute_command` tool (or Bash in Claude Code):
   ```
   python3 {plugin_root}/scripts/fetch-meta-campaigns.py --skip-structure --skip-insights
   ```
   Where `{plugin_root}` is the absolute path to this plugin directory.
   Or call the API directly:
   ```
   GET /me/adaccounts?fields=account_id,name,account_status,currency,business_name,amount_spent
   ```

2. **List all discovered accounts:**

   ```
   Ad Accounts Found:
   
   #  | Account ID       | Name              | Status | Currency | Business
   ---|------------------|-------------------|--------|----------|----------
   1  | act_123456789    | {YOUR_AD_ACCOUNT}          | ACTIVE | AUD      | {YOUR_COMPANY_LEGAL}
   2  | act_987654321    | Client Campaigns  | ACTIVE | AUD      | {YOUR_COMPANY_LEGAL}
   ...
   ```

3. **Let user select which account to use:**
   - Ask: "Which account should I use for campaign data? Enter the number."
   - Confirm the selection

4. **Update marketing-data.json:**
   - Set `meta.meta_ad_account_id` to the selected account ID
   - Confirm: "Ad account set to {account_id} ({name}). Ready to pull campaigns."

5. **Update memory:**
   - Record the selected ad account ID and name in `index.md`
