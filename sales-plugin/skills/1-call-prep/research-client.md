---
name: research-client
description: Scrape client website, research industry context, build company profile with pain hypotheses
menu-code: RC
---

# [RC] Research Client

## Purpose

Build a company profile from web research and generate industry-specific pain point hypotheses. This is the automated version of the manual research done for previous clients (e.g. the Caring Ways company profile in `clients/noah-caring-ways/discovery-call-prep.md`).

## Prerequisites

- `{client_slug}` must be set (run [NC] first if not)
- `prospect-profile.json` must exist with at least `company_domain` and `industry_tag`

## Execution

### Step 1: Load Existing Data

Read `clients/{client_slug}/audit/prospect-profile.json` for domain and industry tag.

### Step 2: Scrape Client Website

Use **WebFetch** to scrape the client's website:

1. **Homepage** — `https://{company_domain}` — company description, headline messaging, service overview
2. **About page** — Try `/about`, `/about-us`, `/our-story` — founding date, team info, mission
3. **Services page** — Try `/services`, `/what-we-do`, `/our-services` — full service list
4. **Team page** — Try `/team`, `/our-team`, `/people` — team size, key roles
5. **Contact page** — Try `/contact`, `/contact-us` — locations, phone numbers, ABN if visible

**Graceful degradation:** If a page returns 404 or is empty, skip it silently. Note which pages were available vs. not.

Extract from each page:
- Company description / tagline
- Services offered (list)
- Team size indicators (staff listed, "our team of X")
- Location(s) and contact details
- ABN if visible
- Technology signals (e.g. booking systems, portals, client logins)
- Any language about processes, workflows, or operational challenges

### Step 3: Industry & Company Research

Use **WebSearch** for:

1. `"{company_name}" site:linkedin.com` — employee count, key staff, company size
2. `"{company_name}" ABN australia` — ABN lookup, registration status
3. `"{company_domain}" reviews OR testimonials` — client feedback, reputation signals
4. Industry-specific searches based on `{industry_tag}`:
   - **ndis**: `"{company_name}" NDIS registration`, check NDIS Commission registration status
   - **construction/trades**: licence status, builder registration
   - **real-estate**: agency licence, listings volume
   - **architecture**: AIA membership, registered architect status
   - **professional-services**: relevant professional body memberships

### Step 4: Competitor Scan

Research 4-6 local competitors to give Adam conversational ammunition about what the market looks like. This is a **lightweight scan** — the deep operational metrics comparison happens later in GDP.

**4a. Find competitors:**

Use WebSearch to find 4-6 local competitors:
- `"best {industry} {region}"` (region from Step 2/3 locations, e.g. "Adelaide")
- `"{industry}" "{city/suburb}" -site:{client_domain}`
- If region is unclear from research, ask: "What area does {company_name} primarily operate in?"

Select competitors that are:
- Real local businesses (not national chains unless dominant locally)
- Similar scale to the client
- Have a scannable website

**4b. Scan each competitor:**

WebFetch **homepage and services page only** (2 pages max per competitor). Extract:
- **Positioning** — how they describe themselves, unique selling points
- **Visible tech** — online booking, client portals, live chat, quote calculators, review widgets
- **Marketing signals** — Google review count if visible, blog/content, social presence
- **Service overlap** — which of the client's services this competitor also offers

**4c. Identify competitor edges:**

Compare what competitors are doing visibly vs. the client. Identify 2-4 "competitor edges" framed conversationally:
- "3 of your 5 competitors have online booking — you don't"
- "Competitor X has 180+ Google reviews vs your 12"
- "Competitor Y is running suburb-specific service pages for SEO"

**Anti-patterns:**
- Do NOT assess the 6 GDP operational metrics (lead response time, quote turnaround, etc.) — that is GDP's job
- Do NOT scan more than 6 competitors — this is a scan, not a research project
- Do NOT fabricate signals. If a competitor's website is minimal, note "minimal web presence" and move on

### Step 5: Industry Standard Tools & Common Pain Points

Instead of guessing what the client uses, state what businesses in their trade typically use. Adam reads this and can say: "Most kitchen manufacturers we talk to are using X for quoting — is that roughly where you're at?"

**5a. Research industry tool landscape:**

Use WebSearch:
- `"{industry_tag} business software Australia 2025 2026"`
- `"{industry_tag} CRM" OR "{industry_tag} job management software"`
- `"best software for {industry_tag} businesses Australia"`

**5b. Compile by category** (only include categories relevant to the industry tag):
- **Quoting/Estimating** — common tools and how most businesses handle it
- **Job/Project Management** — common tools and typical gaps
- **CRM/Lead Management** — common tools, adoption levels
- **Scheduling/Rostering** — if applicable
- **Accounting** — the usual suspects (Xero, MYOB, QuickBooks)

For each category, note: what tools are common, and what the typical reality is (e.g. "most trades businesses still quote from spreadsheets despite tools like Buildxact existing").

**5c. Generate 3-5 relatable industry patterns:**

These are statements framed as industry norms the prospect will immediately identify with. Each includes a `conversation_hook` — a natural way to raise it on the call.

**Examples:**
- Pattern: "Most custom manufacturers track jobs across design, manufacture, and install using a whiteboard or spreadsheet — nothing connects the stages"
  Hook: "Is that roughly how you're tracking jobs across the different stages?"
- Pattern: "Most trades businesses have a website with a contact form but no automated follow-up — leads come in and sit until someone manually checks"
  Hook: "What happens when a lead comes in through your website after hours?"

**Source from:** web search results, `sales-plugin/references/offer-summary.md`, `sales-plugin/references/hormozi-closer-framework.md`, sidecar `patterns.md` (if available). Prioritise sidecar and reference sources over low-quality SEO search results.

### Step 6: Generate Pain Point Hypotheses (Tiered)

Combine research, competitor scan, and industry patterns into a tiered hypothesis list.

**Tier 1: "Industry Reality" hypotheses (HIGH relatability)**

Drawn from Step 5 relatable patterns. Framed as "most businesses in your space..." — statements the prospect reads and thinks "yeah, that's us."
- Always MEDIUM confidence (industry pattern, no client-specific evidence yet)
- 3-4 of these
- Source: `industry_pattern`

**Tier 2: "Client Specific" hypotheses**

Based on website signals, missing tech, and competitor comparison from Steps 2-4. These are the existing pain hypothesis logic:
- Confidence follows standard rules: HIGH (direct website evidence), MEDIUM (strong pattern), LOW (general inference)
- Source: `website_signal`, `competitor_comparison`, or `previous_client_pattern`

**Structure each hypothesis as:**

| # | Tier | Hypothesis | Source | Confidence | Conversation Hook |
|---|---|---|---|---|---|
| 1 | Industry Reality | {pattern-based hypothesis} | industry_pattern | MEDIUM | "{natural question}" |
| 2 | Client Specific | {signal-based hypothesis} | competitor_comparison | HIGH | "{optional}" |

### Step 7: Update Prospect Profile

Update `clients/{client_slug}/audit/prospect-profile.json` with the full `research` block:

```json
{
  "research": {
    "company_description": "",
    "services": [],
    "team_size_estimate": "",
    "locations": [],
    "abn": "",
    "website_tech_signals": [],
    "industry_context": "",
    "competitor_scan": {
      "region": "Adelaide, SA",
      "competitors": [
        {
          "name": "Real Business Name",
          "domain": "realbusiness.com.au",
          "positioning": "How they describe themselves",
          "visible_tech": ["online booking", "client portal"],
          "marketing_signals": ["180 Google reviews", "active blog"],
          "service_overlap": ["kitchens", "bathrooms"]
        }
      ],
      "competitor_edges": [
        "3 of 5 competitors have online booking — client does not",
        "Competitor X has 180+ Google reviews vs minimal review presence"
      ]
    },
    "industry_tools": {
      "tool_landscape": [
        {
          "category": "Quoting/Estimating",
          "common_tools": ["Buildxact", "Quotient", "Excel"],
          "notes": "Most custom manufacturers still use spreadsheets for complex bespoke quotes"
        }
      ],
      "relatable_patterns": [
        {
          "pattern": "Most custom manufacturers track jobs across design, manufacture, and install on a whiteboard or spreadsheet",
          "source": "industry_pattern",
          "conversation_hook": "Is that roughly how you're tracking jobs across the different stages?"
        }
      ]
    },
    "pain_hypotheses": [
      {
        "hypothesis": "",
        "source": "industry_pattern|competitor_comparison|website_signal|previous_client_pattern",
        "confidence": "HIGH|MEDIUM|LOW",
        "tier": "industry_reality|client_specific",
        "conversation_hook": "Optional — natural way to raise this on the call"
      }
    ],
    "professional_memberships": [],
    "research_notes": ""
  },
  "research_completed": true
}
```

### Step 8: Present Summary

Display the research in a scannable format:

```
## Company Profile — {Company Name}

| Field | Value |
|---|---|
| Trading Name | {name} |
| Domain | {domain} |
| ABN | {abn or "not found"} |
| Location | {location} |
| Team Size | {estimate} |
| Industry | {tag} |

### Services
- {service 1}
- {service 2}
...

### Local Competitors ({count})
| Competitor | Positioning | Visible Tech | Reviews |
|---|---|---|---|
| {name} | {positioning} | {tech list} | {review count or "n/a"} |

**Where competitors are ahead:**
- {competitor_edge 1}
- {competitor_edge 2}

### Industry Standard Tools ({industry_tag})
| Category | Common Tools | Typical Reality |
|---|---|---|
| {category} | {tools} | {what most businesses actually do} |

**Relatable patterns you can reference on the call:**
- "{pattern}" → Ask: "{conversation_hook}"

### Pain Point Hypotheses
| # | Tier | Hypothesis | Source | Confidence |
|---|---|---|---|---|
| 1 | Industry Reality | ... | industry_pattern | MEDIUM |
| 2 | Client Specific | ... | website_signal | HIGH |

### Research Notes
{anything noteworthy — tech signals, public reviews, open questions for the call}
```

Ask: "Anything to correct or add before I save?"

### Step 9: Generate Prospect Brief & Sync to CRM

After saving to prospect-profile.json, generate `clients/{client_slug}/prospect-brief.md` using the template in `references/prospect-brief-template.md`.

**At this stage, render only the context sections** (everything above "Discovery Call Prep"):

1. **Header** — Company name, contact, domain, industry, location, ABN, team size, established
2. **What They Do** — 2-3 sentence company description + comma-separated services
3. **What We Know > From Research** — Top 3-5 bullet points: key findings, competitor edges, notable signals
4. **What We Know > From Phone Call** — "No pre-call transcript analyzed."
5. **Key Pain Signals** — Top 5-6 pain hypotheses by confidence (HIGH first), sourced from research
6. **Competitive Context** — 2-3 sentences on local landscape + bullet competitor edges from `research.competitor_scan.competitor_edges`
7. **Industry Tools & Patterns** — Tool landscape summary table + relatable patterns with conversation hooks

**Discovery Call Prep section** shows: "Run [BC] to generate call prep."

**Pipeline footer**: `✓ Research | ○ Phone analysis | ○ Call prep | Discovery: {date or TBD}`

Update `prospect-profile.json`: set `prospect_brief_generated: true`.

**CRM Document Sync:**

1. If `crm.document_id` is set in prospect-profile.json → `update_document(document_id, content: brief_markdown)`
2. If `crm.document_id` is null and `crm.contact_id` is set:
   - `list_documents(entity_type: "contact", entity_id: contact_id)` → look for existing document named "Prospect Brief"
   - If found → `update_document(document_id, content: brief_markdown)` + store `document_id` in `crm.document_id`
   - If not found → `create_document(name: "Prospect Brief", entity_type: "contact", entity_id: contact_id, content: brief_markdown)` + store returned `id` as `crm.document_id`
3. Best-effort — if CRM calls fail, log warning and continue. The local file is always authoritative.

## CRM Lead Update

After saving to prospect-profile.json, if `crm.lead_id` is set:

1. `get_lead(lead_id)` → check current stage
2. If stage is "New": `update_lead(lead_id, stage: "Contacted")` — research counts as first engagement
3. `create_lead_comment(lead_id, content)`:
   ```
   Research completed for {company_name}.
   Team size: {estimate}. Services: {count}.
   Pain hypotheses: {count} (HIGH: {n}, MEDIUM: {n}, LOW: {n}).
   Prospect brief generated and synced to CRM.
   ```
4. Best-effort — if CRM calls fail, log warning and continue.

## Notes

- Research is hypothesis, not fact. The prospect brief will label these clearly as hypotheses vs. evidence from phone calls.
- If the website is minimal or blocks scraping, note what's missing and suggest manual research: "Limited website content. You may want to manually add: {missing fields}."
- Do NOT write any intermediate files. Only `prospect-profile.json` and `prospect-brief.md` get written.
