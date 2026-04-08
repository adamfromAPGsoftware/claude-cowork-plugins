---
description: Set up a new client directory for an audit
---

Create a new client for the audit pipeline. Ask for the company name and domain, then:

1. Generate a company-only slug (no personal names)
2. Create the client directory structure under `clients/{slug}/`:
   - `audit/` (for audit-data.json)
   - `meetings/` (for Fathom transcripts)
   - `client-provided-materials/` (for emails, PDFs, docs)
   - `diagrams/` (for generated process maps)
   - `follow-up-emails/` (for outbound drafts)
   - `deliverables/` (for generated HTML)
   - `close-page/` (for discovery/close page)
3. Create `audit/audit-data-lite.json` with basic contact info
4. Search Fathom for recent meetings using the company domain

$ARGUMENTS
