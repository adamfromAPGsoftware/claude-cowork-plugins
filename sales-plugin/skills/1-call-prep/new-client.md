---
name: new-client
description: Create client directory structure and initialize prospect metadata
menu-code: NC
---

# [NC] New Client Setup

## Purpose

Create a new client directory with the standard folder structure and initialize a `prospect-profile.json` with basic metadata. This is the first step for any new prospect.

## Input Collection

Ask for the following (do NOT guess — ask the user):

1. **Company name** — Full trading name (e.g. "Carabiner Architects")
2. **Client slug** — Short, company-only identifier for the directory (e.g. `cara`). **No personal names in slugs.** Suggest one based on the company name and confirm.
3. **Company domain** — Website domain (e.g. `carabiner.com.au`). Ask for domain, NOT email address.
4. **Industry tag** — Suggest from known set: `ndis`, `home-services`, `construction`, `real-estate`, `trades`, `professional-services`, `architecture`, `other`. Confirm with user.
5. **Contact name** — Primary contact's full name (stored in metadata, not in the slug)
6. **Contact email(s)** — Optional at this stage. If unknown, skip — can be populated later from Fathom discovery.

## Execution

### Step 1: Create Directory Structure

```
clients/{client_slug}/
  audit/
  meetings/
  client-provided-materials/
  close-page/
  deliverables/
  follow-up-emails/
```

### Step 2: Search Fathom for Existing Meetings

Run: `python3 scripts/fetch-transcripts.py --client-slug {client_slug}`

If `FATHOM_API_KEY` is not set or no contact emails are available yet, skip silently and note it.

**Domain-based discovery:** If no emails are set but domain is known, note this for the user: "No contact emails set yet — once you add an email, I can search Fathom for past meetings with anyone @{domain}."

If meetings are found:
- Display them with dates and titles
- Ask user to confirm which ones are relevant
- Note discovered invitee emails for `contact.emails[]`

### Step 3: CRM Lookup — Contact & Lead

**Contacts and leads almost always already exist in the CRM.** Always search first.

#### CRM Schema Reference

**create_contact — supported fields only:**
- `name` (required) — display name (use company name)
- `first_name` — contact's first name
- `last_name` — contact's last name
- `email_address` — must be valid email format
- `website` — full URL including https://
- `is_customer` — boolean (default false)
- `is_supplier` — boolean (default false)
- **NOT supported:** `phone`, `notes` — store phone number in prospect-profile.json instead

**create_lead — supported fields only:**
- `title` (required) — opportunity title
- `contact_id` — UUID of associated contact
- `value` — estimated deal value (number)
- `currency` — ISO 4217 code (default AUD)
- `stage` — pipeline stage (default "New")
- `source` — lead source text
- `assigned_to` — user UUID
- `notes` — lead notes
- **NOT supported for insert:** `priority` — auto-defaults to "Cold", cannot be set on creation

#### 3a. Find or Create Contact

1. `search_contacts(query: "{company_name}")` — look for existing contact
2. If no match: `search_contacts(query: "{domain}")` — try domain
3. If found: store `contact_id`. If multiple matches, prefer the one with `is_customer: true` or matching email domain.
4. If NOT found: `create_contact(name: "{company_name}", first_name: "{first_name}", last_name: "{last_name}", email_address: "{contact_email}", website: "https://{domain}", is_customer: true)` — store returned `id` as `contact_id`

#### 3b. Find or Create Lead

1. `search_leads(query: "{company_name}")` — look for existing lead
2. If found: store `lead_id`. If multiple matches, prefer the one linked to the matched `contact_id`.
3. If NOT found: `create_lead(title: "{company_name} - Operational Audit", contact_id: "{contact_id}", value: 3000, currency: "AUD", stage: "New")` — store returned `id` as `lead_id`

If CRM calls fail, log warning and continue — CRM is best-effort, never blocks client setup.

### Step 4: Create Prospect Profile

Save to `clients/{client_slug}/audit/prospect-profile.json`:

```json
{
  "client_slug": "{client_slug}",
  "company_name": "{company_name}",
  "company_domain": "{domain}",
  "industry_tag": "{industry_tag}",
  "contact": {
    "name": "{contact_name}",
    "emails": []
  },
  "crm": {
    "contact_id": "{contact_id or null}",
    "lead_id": "{lead_id or null}",
    "project_id": null,
    "task_list_ids": {
      "extraction": null,
      "analysis": null,
      "deliverables": null,
      "solution_design": null
    },
    "document_id": null,
    "last_synced": "{ISO 8601 timestamp}"
  },
  "status": "pre-discovery",
  "research_completed": false,
  "phone_transcript_analyzed": false,
  "prospect_brief_generated": false,
  "discovery_call_date": null
}
```

### Step 5: Set Session Context

Store `{client_slug}` as the active client for this session.

### Step 6: Confirm and Suggest Next Step

```
Client created: clients/{client_slug}/
CRM: Contact {found|created} ({contact_id}) | Lead {found|created} ({lead_id})

Next steps:
- [RC] Research Client — scrape their website and build a company profile
- [AT] Analyze Transcript — if you have a phone call transcript to process
```

## Notes

- **prospect-profile.json** is NOT the same as `audit-data-lite.json` (Close agent) or `audit-data.json` (Process Mapper). It's a lighter pre-discovery metadata file that those agents can read later to pre-populate their data.
- Only `prospect-profile.json` belongs in the `audit/` folder at this stage. No intermediate or temp files.
