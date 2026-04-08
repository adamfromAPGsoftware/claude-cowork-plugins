---
name: qualify-contacts
description: Classify contacts for a specific CRM-enabled account
menu-code: QC
---

# Qualify Contacts

Analyse conversation history and classify contacts for a single CRM-enabled account.

## Process

1. **Ask which account:**
   - List all CRM-enabled accounts (where config.json has `crm.enabled=true`)
   - Ask user to select one
   - If selected account does not have CRM enabled, refuse and explain why

2. **Load classification docs for selected account:**
   - Read `accounts/{key}/icp.md` — ICP criteria and classification signals
   - Read `accounts/{key}/products.md` — product tier definitions
   - Read `accounts/{key}/config.json` — get `qualify_fields` if defined

3. **Load conversation data:**
   - Read `data/{key}/social-data.json`

4. **Find classifiable contacts:**
   - Contacts where `qualification.status == "unclassified"` AND `interaction_count >= 2`
   - Report count before starting

5. **For each classifiable contact:**
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

6. **Update contact.qualification in social-data.json:**

   ```json
   {
     "status": "qualified",
     "tier": "{tier}",
     "confidence": 0.85,
     "signals": ["signal 1", "signal 2"],
     "qualified_at": "2026-04-07T12:00:00Z",
     "crm_lead_id": null
   }
   ```

7. **Save social-data.json**

8. **Present results:**

```
Classification results for {display_name} (@{handle}):

Contact          | Tier              | Confidence | Key Signals
-----------------|-------------------|------------|------------
@{username}      | agency_services   | 0.85       | mentioned 30 staff, asked about pricing
@{username}      | paid_academy      | 0.72       | asked about course structure
@{username}      | not_qualified     | 0.90       | only sends memes
...

Classified: {n} | Still unclassified (low confidence): {n} | Still unclassified (< 2 interactions): {n}
```

9. **Suggest next action:**
   - If paid_academy or agency_services contacts found: "Run [SC] Sync to CRM to push qualified leads."
   - If low-confidence contacts remain: "These contacts need more conversation data before classification."

## Output

The results table above with evidence for each classification.

## Cowork Execution

If running in Cowork (no native file access), use Desktop Commander MCP (`execute_command`) for all file operations. CRM MCP tools work natively in Cowork (no Desktop Commander needed for CRM calls).

- List accounts: `execute_command("ls {PROJECT_ROOT}/social-plugin/accounts/")`
- Read account config: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/config.json")`
- Read ICP doc: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/icp.md")`
- Read products: `execute_command("cat {PROJECT_ROOT}/social-plugin/accounts/{key}/products.md")`
- Read social data: `execute_command("cat {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json")`
- Write updated social-data.json: `execute_command("cat > {PROJECT_ROOT}/social-plugin/data/{key}/social-data.json << 'JSONEOF'\n{json_content}\nJSONEOF")`

All paths must be absolute. Python scripts auto-load .env via python-dotenv.
