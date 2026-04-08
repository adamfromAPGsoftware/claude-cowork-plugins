---
name: nurture-status
description: Show qualification stats, tier breakdown, and CRM sync status across all accounts
menu-code: NS
---

# Nurture Status

Dashboard showing qualification stats, tier breakdown, and CRM sync status across all accounts.

## Process

1. **Scan all accounts** (both CRM-enabled and not):
   - Read `{project-root}/social-plugin/accounts/*/config.json`
   - Read `data/{key}/social-data.json` for each account

2. **For each account, gather stats from social-data.json:**
   - Total contacts
   - Contacts by qualification status: unclassified, qualified, not_qualified
   - Contacts by tier: free_community, paid_academy, agency_services, not_qualified
   - CRM sync status: synced (crm_lead_id != null) vs pending (qualified but no crm_lead_id)

3. **Present per-account table:**

```
Qualification Dashboard

Account            | CRM | Total | Unclassified | free_community | paid_academy | agency_services | not_qualified
-------------------|-----|-------|--------------|----------------|--------------|-----------------|---------------
{display_name}     | Yes | {n}   | {n}          | {n}            | {n}          | {n}             | {n}
{display_name}     | No  | {n}   | {n}          | {n}            | {n}          | {n}             | {n}
...
```

4. **CRM sync status (CRM-enabled accounts only):**

```
CRM Sync Status

Account            | Qualified | Synced to CRM | Pending Sync | free_community (no sync)
-------------------|-----------|---------------|--------------|-------------------------
{display_name}     | {n}       | {n}           | {n}          | {n}
...
```

5. **Recent classifications (last 10 across all accounts):**

```
Recent Classifications

Date       | Account   | Contact     | Tier              | Confidence | Key Signal
-----------|-----------|-------------|-------------------|------------|----------
{date}     | {account} | @{username} | agency_services   | 0.85       | mentioned 30 staff
{date}     | {account} | @{username} | paid_academy      | 0.72       | asked about course pricing
...
```

6. **Summary:**

```
Totals:
- {total_contacts} contacts across {account_count} accounts
- {total_classified} classified ({pct}%)
- {total_crm_synced} synced to CRM
- {total_pending_sync} pending CRM sync
- {total_unclassified} still unclassified ({n} with < 2 interactions)
```

7. **Suggest next actions:**
   - If unclassified contacts with >= 2 interactions: "Run [QA] Qualify All to classify {n} eligible contacts."
   - If pending CRM sync: "Run [SC] Sync to CRM to push {n} qualified contacts."
   - If all up to date: "All eligible contacts classified and synced. Check back after more conversations."

## Output

The three tables above plus summary and next actions.

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all file operations:

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Read social data per account: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
