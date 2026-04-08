---
name: qualify-all
description: Analyse and classify contacts across all CRM-enabled accounts
menu-code: QA
---

# Qualify All

Analyse conversation history and classify contacts across all CRM-enabled accounts.

## Process

1. **Discover CRM-enabled accounts:**
   - Scan `{project-root}/social-plugin/accounts/*/config.json`
   - Filter where `crm.enabled=true`
   - Skip accounts without CRM enabled

2. **For each CRM-enabled account:**

   a. **Load classification docs:**
      - Read `accounts/{key}/icp.md` — ICP criteria and classification signals
      - Read `accounts/{key}/products.md` — product tier definitions
      - Read `accounts/{key}/config.json` — get `qualify_fields` if defined

   b. **Load conversation data:**
      - Read `data/{key}/social-data.json`

   c. **Find classifiable contacts:**
      - Contacts where `qualification.status == "unclassified"` AND `interaction_count >= 2`
      - Skip already-classified contacts

   d. **For each classifiable contact:**
      - Read ALL their conversations and comments (full thread context)
      - Analyse against ICP criteria from icp.md
      - Look for signals matching product tiers from products.md
      - **Classification tiers:**
        - **free_community**: casual interest, learning, exploring, "where do I start"
        - **paid_academy**: structured learning, pricing questions, course interest, ready to invest
        - **agency_services**: business owner, mentions team/staff, wants someone to build it, system pain
        - **not_qualified**: spam, off-topic, competitor, no real interest after 2+ interactions
      - Set confidence score (0.0–1.0). Only classify if >= 0.7, else leave unclassified.
      - Record signals (specific quotes or conversation points that drove the classification)

   e. **Update contact.qualification in social-data.json:**

      ```json
      {
        "status": "qualified",
        "tier": "agency_services",
        "confidence": 0.85,
        "signals": ["mentioned 30 staff", "asked about pricing", "runs an NDIS business"],
        "qualified_at": "2026-04-07T12:00:00Z",
        "crm_lead_id": null
      }
      ```

      For not_qualified contacts:

      ```json
      {
        "status": "not_qualified",
        "tier": "not_qualified",
        "confidence": 0.9,
        "signals": ["only sends memes", "no business context after 3 interactions"],
        "qualified_at": "2026-04-07T12:00:00Z",
        "crm_lead_id": null
      }
      ```

   f. **Save social-data.json**

3. **Present summary table:**

```
Qualification complete.

Account            | Classified | free_community | paid_academy | agency_services | not_qualified | Still Unclassified
-------------------|------------|----------------|--------------|-----------------|---------------|-------------------
{display_name}     | {n}        | {n}            | {n}          | {n}             | {n}           | {n}
...

Total: {total_classified} contacts classified across {account_count} CRM-enabled accounts.
```

4. **Suggest next action:**
   - If paid_academy or agency_services contacts found: "Run [SC] Sync to CRM to push qualified leads."
   - If many still unclassified: "Contacts with < 2 interactions need more conversation before classification."
   - If all classified: "All eligible contacts classified. Run [NS] Nurture Status for the full dashboard."

## Output

The summary table above, plus per-account detail if contacts were classified.

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all file operations. CRM MCP tools work natively in Cowork (no Desktop Commander needed for CRM calls).

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Read ICP doc: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/icp.md")`
- Read products: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/products.md")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`
- Write updated social-data.json: `execute_command("cat > {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json << 'JSONEOF'\n{json_content}\nJSONEOF")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
