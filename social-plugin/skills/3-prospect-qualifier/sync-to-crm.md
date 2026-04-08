---
name: sync-to-crm
description: Push qualified prospects to {YOUR_CRM}. Lookup-first — search before creating.
menu-code: SC
---

# Sync to CRM

Push qualified contacts to {YOUR_CRM} for all CRM-enabled accounts. Uses lookup-first pattern — always search before creating.

## Process

1. **Discover CRM-enabled accounts:**
   - Scan `{project-root}/social-plugin/accounts/*/config.json`
   - Filter where `crm.enabled=true`

2. **For each CRM-enabled account:**

   a. **Load social-data.json:**
      - Read `data/{key}/social-data.json`

   b. **Find contacts to sync:**
      - Where `qualification.status == "qualified"`
      - AND `qualification.crm_lead_id == null`
      - AND `qualification.tier` in `["paid_academy", "agency_services"]`
      - Skip `free_community` (not high enough intent for CRM) and `not_qualified`

   c. **For each contact to sync:**

      **Step 1 — Search for existing contact:**
      ```
      search_contacts(query: "{username}")
      ```
      - If found: use existing contact_id, skip creation
      - If not found: create new contact

      **Step 2 — Create contact (if needed):**
      ```
      create_contact(
        name: "{name or username}",
        email: null,
        phone: null,
        notes: "Instagram contact — @{username}"
      )
      ```
      - Store returned contact_id

      **Step 3 — Search for existing lead:**
      ```
      search_leads(query: "{username}")
      ```
      - If found: use existing lead_id, skip creation
      - If not found: create new lead

      **Step 4 — Create lead (if needed):**
      ```
      create_lead(
        title: "{name} - Instagram [{tier}]",
        contact_id: {contact_id},
        value: 0,
        stage: "New"
      )
      ```
      - Store returned lead_id

      **Step 5 — Add lead comment:**
      ```
      create_lead_comment(
        lead_id: {lead_id},
        body: "[SOCIAL] Instagram qualification — {date}\nPlatform: Instagram | Account: @{account_key}\nClassification: {tier} ({confidence})\nSignals: {signals joined}\nInteraction count: {interaction_count}\nLast interaction: {last_interaction}"
      )
      ```

      **Step 6 — Update social-data.json:**
      - Set `contact.qualification.crm_lead_id` to the lead_id

   d. **Save social-data.json**

3. **Error handling:**
   - If any CRM call fails, log warning with error details
   - Continue to next contact — never block on CRM errors
   - Report failures at end

4. **Present report:**

```
CRM sync complete.

Account            | Contacts Synced | Leads Created | Existing Leads | Errors
-------------------|-----------------|---------------|----------------|-------
{display_name}     | {n}             | {n}           | {n}            | {n}
...

Total: {total_synced} contacts synced, {total_leads_created} new leads created.
```

5. **If errors occurred:**

```
CRM errors ({count}):
- @{username}: {error_message}
...

These contacts were NOT synced. Re-run [SC] after resolving CRM issues.
```

6. **Suggest next action:**
   - "Run [NS] Nurture Status for full dashboard including CRM sync status."
   - "New leads created at 'New' stage — sales pipeline handles stage progression from here."

## CRM MCP Tools Used

| Tool | Purpose |
|------|---------|
| `search_contacts(query)` | Lookup existing contact before creating |
| `create_contact(name, notes)` | Create new CRM contact |
| `search_leads(query)` | Lookup existing lead before creating |
| `create_lead(title, contact_id, value, stage)` | Create new CRM lead at "New" stage |
| `create_lead_comment(lead_id, body)` | Log social context on the lead |

## Output

The sync report table above, plus any error details.

## Cowork Execution

If running in Cowork (no native file access), CRM MCP tools work natively (no Desktop Commander needed for CRM calls). Use Desktop Commander MCP (`execute_command`) only for file operations:

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`
- Write updated social-data.json: `execute_command("cat > {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json << 'JSONEOF'\n{json_content}\nJSONEOF")`

CRM operations (`search_contacts`, `create_contact`, `search_leads`, `create_lead`, `create_lead_comment`) use the CRM MCP tools directly -- no Desktop Commander proxy needed.

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
