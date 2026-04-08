---
name: research-improvements
description: Web research for tools, APIs, feasibility per proposed_change + generate new opportunities. Idempotent — re-run to fill gaps.
menu-code: RI
---

# Research Improvements (RI)

> **Idempotent.** First run researches everything + generates new opportunities. Re-runs only target items with `research.status != "complete"` or `research.gaps[]` entries.

## Purpose

For each proposed_change in the audit data, research what's actually possible: which tools exist, what their APIs support, how they integrate with the client's existing stack, and what similar businesses have done. Then scan the audit data for new opportunities the client didn't mention.

---

## Stage 1: Pre-flight

1. Check audit data is loaded and `proposed_changes[]` is populated. If empty:
   ```
   ✗ proposed_changes[] is empty. Run [EI] Extract Improvements first.
   ```

2. Scan research status across all proposed_changes:
   ```
   RESEARCH STATUS — {company_name}
   Total proposed changes: {n}
     complete:     {n}
     needs_review: {n}
     in_progress:  {n}
     not_started:  {n}
   ```

3. Select scope:
   ```
   Scope options:
     A) All unresearched (status != "complete") — {n} changes
     B) Specific change by ID (e.g., CH-003)
     C) Re-research specific ID (force re-run even if complete)
     D) Generate new opportunities only (skip existing changes)
   ```
   Wait for user selection.

---

## Stage 2: Research Existing Changes (source: client)

> **MANDATORY — Web Research Rules:**
> 1. **Always use `WebFetch`** for all web research (pricing pages, API docs, aggregator sites, review pages). Never use Exa or other search MCP tools.
> 2. **Process changes sequentially** — research one proposed_change at a time, complete it fully (all tool options + hidden costs + industry landscape), then move to the next. Do not parallelise research across changes.

For each change in scope where `source == "client"` (created by EI from client-stated optimisations and pain points), in order:

### 2a. Build research context

Read from audit data:
- The proposed_change entry (title, change_type, proposed_solution, proposed_tools, affected_step_ids)
- Linked pain_points via `linked_pain_point_ids` — get descriptions, quotes, speakers, timestamps
- Linked waste_items via stage matching — get hours_per_week, annual_waste_aud, activity descriptions
- Affected steps from `processes[]` — get descriptions, tool_ids, meeting_references
- Relevant tools from `tools[]` — get api_available, use_case, workarounds, monthly_cost_aud
- Client's industry_tag and existing tool stack

### 2b. Structured pricing lookup

For each tool option (primary AND 2-3 alternatives), follow this tiered source hierarchy. Stop at the first tier that yields complete pricing data (all tiers with prices). Record `pricing_source_type` based on where data was found.

**Tier 1 — Official pricing page** (`pricing_source_type: "official"`)
Use `WebFetch` to load the tool's official pricing page (e.g., `https://{tool_domain}/pricing`)
- Look for the tool's own /pricing page
- Extract all tier names, prices, and per-user vs flat pricing model
- If the page says "Contact sales" or "Custom pricing", note this and proceed to Tier 2

**Tier 2 — Aggregator sites** (`pricing_source_type: "aggregator"`)
Try these in order using `WebFetch` to load each URL directly — stop at the first that provides concrete price numbers:
1. **CostBench**: `"{tool_name} pricing" site:costbench.com` — 950+ products, check `/software/[category]/[tool]/calculator/`
2. **CompareTiers**: `"{tool_name}" site:comparetiers.com` — auto-scraped weekly from vendor pages
3. **Vendr**: `"{tool_name}" site:vendr.com/marketplace` — real transaction data from $15B+ in deals
4. **G2**: `"{tool_name} pricing" site:g2.com` — pricing overview pages
5. **Capterra**: `"{tool_name} pricing" site:capterra.com` — 100K+ products

**Tier 3 — Blog posts and comparisons** (`pricing_source_type: "blog"`)
Search: `"{tool_name} pricing {current_year}" review OR comparison`
Use only if Tiers 1-2 yield nothing concrete. Look for recent comparison articles with actual price numbers.

**Tier 4 — Training knowledge** (`pricing_source_type: "training_knowledge"`)
Use model knowledge as last resort. Set `confidence: "LOW"` and `pricing_is_estimated: true`. Add a gap noting that pricing needs verification.

**For all tiers:** Record the actual URL where pricing was found in `pricing_url` and add to `source_urls[]`. Set `pricing_verified_date` to today's date. Set `pricing_is_estimated: true` for Tier 3 and 4 sources.

### 2b-ii. Hidden cost research

For each tool where pricing was found, also research hidden costs. **Always do this even when official pricing was found** — vendors rarely disclose their own hidden costs.

1. **CostBench hidden costs**: Use `WebFetch` to load `https://costbench.com/software/{category}/{tool_name}/hidden-costs/` — CostBench tracks 13 verified hidden cost categories per product (the best hidden cost data available).
2. **Vendor pricing page fine print**: Look for footnotes about:
   - Implementation/onboarding fees
   - Per-seat minimums or annual contract requirements
   - API access tier requirements (many tools gate API behind higher tiers)
   - Add-on features the client's use case likely needs (SSO, advanced reporting, webhooks, email sequences)
   - Overage charges (API calls, storage, contacts, records, automations)
3. **SaaS Price Pulse**: Use `WebFetch` to load `https://saaspricepulse.com/{tool_name}` — check for historical price increases that signal future cost creep

Populate `hidden_costs[]` with each discovered cost. Assess `likelihood` based on whether the client's specific use case and scale would trigger this cost:
- `"likely"` — most customers at this scale encounter this (e.g., needing automation → Professional tier upgrade)
- `"possible"` — depends on growth or usage pattern
- `"unlikely"` — edge case but worth noting for transparency

Calculate `total_cost_with_hidden_aud` = `annual_cost_aud` + sum of `estimated_annual_aud` for all hidden costs with `likelihood: "likely"`.

### 2b-iii. Remaining research per tool

Use `WebFetch` to load relevant pages (pricing, API docs, reviews) to find for EACH option:
- **API availability** — what endpoints exist, rate limits, which tier includes API access
- **Pros** — what this tool does well for this specific use case (3-5 bullet points)
- **Cons/Limitations** — what's missing, what requires upgrade, what doesn't work (3-5 bullet points)
- **Integration with client's stack** — how it connects to their existing tools
- **Source URLs** — pricing page, API docs, relevant review/comparison pages

**CRITICAL:** Every option (primary + alternatives + custom build) must be a separate entry in `tools_researched[]` with the SAME fields. No more storing competitors as strings — they are first-class entries. This enables side-by-side comparison tables in the deliverable.

**CRITICAL — Tool Specificity:** Every `tool_name` MUST be a specific, named product — never generic descriptions.
- **Good:** "HubSpot CRM", "ShiftCare", "Make.com", "Excel", "Xero", "Manual phone call", "Paper form"
- **Bad:** "NDIS scheduling provider", "rostering tool", "CRM system", "automation platform", "accounting software"
- Even manual/existing methods must be named: "Manual phone call", "Excel spreadsheet", "Google Sheets", "Email (Gmail)"
- If you cannot identify a specific tool, research harder — there is always a specific product to name

**If web search is unavailable:** use training knowledge. Mark `confidence` as `LOW` and add a gap.

### 2b-iv. Realistic tier assessment

**CRITICAL — Never assume the free tier is sufficient when the client's stated needs or scale obviously require paid features. Default to the realistic tier, then show free as a limited alternative.**

For EACH tool option researched in 2b-i through 2b-iii, evaluate which tier the client would *actually* need given their headcount (`company_size`), process complexity, and stated needs from the audit data:

1. **Check free tier viability** — Does the free plan support:
   - The client's number of users/seats?
   - The automation/workflow features their proposed changes require?
   - Multiple pipelines, projects, or workspaces if needed?
   - API access for integrations with other tools?
   - If ANY of these are clearly insufficient, set `requires_paid_plan: true`

2. **Determine realistic tier** — Based on the client's actual needs:
   - What tier would they realistically end up on within 6 months?
   - Set `realistic_tier` to that tier name (e.g., "Professional", "Team", "Business")
   - Calculate `realistic_annual_cost_aud` at that tier for the client's current headcount

3. **Document free plan limitations** — Populate `free_plan_limitations[]` with specific things the free tier can't do that the client needs (e.g., "Limited to 1 pipeline — client needs separate pipelines for NDIS referrals and direct enquiries")

4. **Assess setup and configuration costs** — Research typical setup:
   - Use `WebFetch` to search: `"{tool_name} implementation cost"`, `"{tool_name} onboarding fee"`, `"{tool_name} consultant setup"`
   - Set `setup_source`: `"self_service"` (client can configure themselves), `"consultant"` (typical to hire a specialist), or `"vendor_onboarding"` (vendor offers paid onboarding)
   - Populate `setup_cost_aud` (one-time setup/config cost) and `consultant_fee_estimate_aud` (one-off consultant fee if that's the typical path)
   - Populate `consultant_hours` — estimated hours a consultant or internal resource spends on initial setup (e.g., "10-15 hours")
   - Populate `setup_timeline_weeks` — how long from purchase to go-live (e.g., "2-3 weeks")
   - Populate `ongoing_admin_hours_monthly` — estimated hours/month to administer this tool post-setup
   - **Research real rates**: Search for "{tool_name} consultant rates Australia", "{tool_name} implementation cost", "{tool_name} onboarding time". Include source URLs. Do NOT use placeholder values — if no data found, mark confidence LOW and explain why.

5. **Assess data isolation and API access** — For each tool:
   - Set `data_silo_risk` — describe what data gets trapped in this tool and can't easily flow to other systems (e.g., "Participant records locked in ShiftCare — no bulk export, manual re-entry needed for invoicing")
   - Set `api_tier_required` — which pricing tier is needed for API access (e.g., "Professional tier required for REST API and webhooks")

Add these fields to each `tools_researched[]` entry (alongside existing fields from 2b-i through 2b-iii):

```json
{
  "requires_paid_plan": true,
  "free_plan_limitations": [
    "Limited to 1 pipeline — client needs separate pipelines for NDIS referrals and direct enquiries",
    "No workflow automation on Free — all follow-ups remain manual",
    "HubSpot branding on forms — unprofessional for client-facing intake"
  ],
  "realistic_tier": "Professional",
  "realistic_annual_cost_aud": 9000,
  "setup_cost_aud": 2000,
  "setup_source": "consultant",
  "consultant_fee_estimate_aud": 3000,
  "consultant_hours": 15,
  "setup_timeline_weeks": 3,
  "ongoing_admin_hours_monthly": 4,
  "data_silo_risk": "Contact and deal data locked in HubSpot — requires Professional tier for API export, no native sync to rostering tools",
  "api_tier_required": "Professional ($750/mo) for webhooks and custom workflow triggers"
}
```

**If a tool genuinely works well on the free tier** (e.g., Google Forms for simple intake), set `requires_paid_plan: false`, `realistic_tier: "Free"`, `realistic_annual_cost_aud: 0`, and leave `free_plan_limitations: []`.

### 2c. Populate research sub-object

Every option is a full entry in `tools_researched[]`. Include the primary recommended tool, 2-3 alternatives, and the custom build option (from Step 2d) all in the same array:

```json
{
  "research": {
    "status": "complete",
    "last_researched": "{ISO datetime}",
    "run_count": 1,
    "tools_researched": [
      {
        "tool_name": "HubSpot CRM",
        "is_recommended": true,
        "category": "CRM / Sales Pipeline",
        "pricing_model": "per_user",
        "pricing_summary": "Free: $0 (1 pipeline, basic). Starter: $30 AUD/mo. Professional: $750 AUD/mo.",
        "cost_at_current_headcount": "$0/yr (Free) or $360/yr (Starter)",
        "cost_at_scaled_headcount": "$0/yr (Free) — no per-user fees on Free/Starter",
        "per_user_monthly_aud": 0,
        "flat_monthly_aud": 0,
        "annual_cost_aud": 0,
        "pricing_source_type": "official",
        "pricing_verified_date": "2026-03-30",
        "pricing_is_estimated": false,
        "hidden_costs": [
          {
            "type": "upsell",
            "description": "Professional tier ($750/mo) required for workflow automation — most CRM implementations need this within 6 months",
            "estimated_cost_aud": 750,
            "estimated_annual_aud": 9000,
            "trigger": "Needing more than 1 pipeline or any automation rules",
            "likelihood": "likely",
            "source_url": "https://www.hubspot.com/pricing"
          },
          {
            "type": "add_on",
            "description": "Marketing Hub add-on for email sequences",
            "estimated_cost_aud": 65,
            "estimated_annual_aud": 780,
            "trigger": "Running automated email nurture sequences",
            "likelihood": "possible",
            "source_url": ""
          }
        ],
        "total_cost_with_hidden_aud": 9000,
        "api_available": true,
        "api_notes": "REST API on all tiers. Rate limited on Free. Webhooks require Professional.",
        "pros": ["Already installed — just activate pipeline", "Free tier covers core CRM needs", "Native Gmail + Google Calendar integration", "Large ecosystem of integrations"],
        "cons": ["Free tier has no automation — all follow-ups manual", "Single pipeline limit on Free", "HubSpot branding on forms", "No NDIS-specific fields — custom configuration needed"],
        "integration_with_existing": "Already have HubSpot as phone directory. Gmail sync, Calendar sync, Trello connector available.",
        "requires_paid_plan": true,
        "free_plan_limitations": [
          "Limited to 1 pipeline — client needs separate pipelines for NDIS referrals and direct enquiries",
          "No workflow automation on Free — all follow-ups remain manual",
          "HubSpot branding on forms — unprofessional for client-facing intake"
        ],
        "realistic_tier": "Professional",
        "realistic_annual_cost_aud": 9000,
        "setup_cost_aud": 0,
        "setup_source": "self_service",
        "consultant_fee_estimate_aud": 0,
        "ongoing_admin_hours_monthly": 2,
        "data_silo_risk": "Contact and deal data locked in HubSpot — requires Professional tier for API export",
        "api_tier_required": "Professional ($750/mo) for webhooks and custom workflow triggers",
        "pricing_url": "https://www.hubspot.com/pricing",
        "docs_url": "https://developers.hubspot.com/docs/api",
        "source_urls": ["https://www.hubspot.com/pricing"],
        "confidence": "HIGH"
      },
      {
        "tool_name": "Zoho CRM",
        "is_recommended": false,
        "category": "CRM / Sales Pipeline",
        "pricing_model": "per_user",
        "pricing_summary": "Free: 3 users. Standard: $21 AUD/user/mo. Professional: $35 AUD/user/mo.",
        "cost_at_current_headcount": "$0/yr (3 users free) or $756/yr (3 users Standard)",
        "cost_at_scaled_headcount": "$2,520/yr (10 users Standard)",
        "per_user_monthly_aud": 21,
        "flat_monthly_aud": null,
        "annual_cost_aud": 756,
        "pricing_source_type": "official",
        "pricing_verified_date": "2026-03-30",
        "pricing_is_estimated": false,
        "hidden_costs": [
          {
            "type": "add_on",
            "description": "Zoho Analytics BI add-on for advanced reporting",
            "estimated_cost_aud": 35,
            "estimated_annual_aud": 420,
            "trigger": "Needing cross-module reporting or custom dashboards beyond built-in",
            "likelihood": "possible",
            "source_url": "https://www.zoho.com/analytics/pricing.html"
          }
        ],
        "total_cost_with_hidden_aud": 756,
        "api_available": true,
        "api_notes": "REST API from Standard tier. Webhooks from Professional.",
        "pros": ["More automation at lower price points than HubSpot", "Part of larger Zoho ecosystem (Books, Invoice, etc.)", "Workflow rules on Standard tier"],
        "cons": ["Less intuitive UI than HubSpot", "Smaller integration ecosystem", "Would be a new tool — no existing account"],
        "integration_with_existing": "Xero integration via Zapier. Google Workspace integration available.",
        "requires_paid_plan": true,
        "free_plan_limitations": [
          "Free tier limited to 3 users — client needs CRM access for multiple team members",
          "No workflow automation on Free — requires Standard tier"
        ],
        "realistic_tier": "Standard",
        "realistic_annual_cost_aud": 756,
        "setup_cost_aud": 500,
        "setup_source": "self_service",
        "consultant_fee_estimate_aud": 0,
        "ongoing_admin_hours_monthly": 3,
        "data_silo_risk": "CRM data in Zoho ecosystem — exports available but customisations don't transfer to other CRMs",
        "api_tier_required": "Standard tier for REST API, Professional for webhooks",
        "pricing_url": "https://www.zoho.com/crm/zohocrm-pricing.html",
        "docs_url": "",
        "source_urls": [],
        "confidence": "HIGH"
      }
    ],
    "feasibility_notes": "Straightforward. They already own HubSpot.",
    "similar_implementations": "Common pattern in service businesses with 50+ leads/month.",
    "risks": ["Free tier has no automation — risk of reverting to old habits"],
    "gaps": []
  }
}
```

**Pricing fields explained:**
- `pricing_model` — `"per_user"` | `"flat"` | `"per_unit"` | `"free"` | `"usage_based"` | `"custom"` — drives scaling calculation
- `per_user_monthly_aud` — if per-user, the monthly AUD cost per user (null if flat/free)
- `flat_monthly_aud` — if flat, the monthly AUD cost regardless of users (null if per-user)
- `annual_cost_aud` — total annual cost at the recommended tier for the client's current headcount
- `cost_at_current_headcount` — human-readable string showing the calculation (e.g., "$21/user × 3 users × 12mo = $756/yr")
- `cost_at_scaled_headcount` — same calculation at 2× current headcount
- `pricing_source_type` — where pricing was sourced (see Tier 1-4 hierarchy in 2b above)
- `pricing_verified_date` — ISO date when pricing was last confirmed via web search
- `pricing_is_estimated` — `true` for Tier 3/4 sources where pricing could not be confirmed from official or aggregator data
- `hidden_costs[]` — array of hidden/upsell costs discovered during 2b-ii research
- `total_cost_with_hidden_aud` — `annual_cost_aud` + sum of `hidden_costs[].estimated_annual_aud` where `likelihood == "likely"`. This is the "true cost" figure shown in deliverables.

**Realistic tier fields (from Step 2b-iv):**
- `requires_paid_plan` — `true` if the free tier is clearly inadequate for the client's scale/needs
- `free_plan_limitations[]` — specific things the free tier can't do that the client needs
- `realistic_tier` — the tier the client would realistically end up on within 6 months (e.g., "Professional", not "Free")
- `realistic_annual_cost_aud` — annual cost at the realistic tier for the client's current headcount
- `setup_cost_aud` — one-time setup/configuration cost
- `setup_source` — `"self_service"` | `"consultant"` | `"vendor_onboarding"` — how setup typically happens
- `consultant_fee_estimate_aud` — one-off consultant fee if that's the typical path for this tool
- `consultant_hours` — estimated hours a consultant/resource spends on initial setup
- `setup_timeline_weeks` — how long from purchase to go-live
- `ongoing_admin_hours_monthly` — estimated hours per month to administer this tool
- `data_silo_risk` — what data gets trapped in this tool and can't easily flow to other systems
- `api_tier_required` — which pricing tier is needed for API access (e.g., "Professional for webhooks")

**Confidence semantics (updated for pricing accuracy):**
- `HIGH` — pricing from official page or aggregator with recent data (< 3 months old)
- `MEDIUM` — pricing from blog/comparison post or aggregator with older data
- `LOW` — training knowledge only, or vendor shows "Contact sales" with estimated pricing

**Source URLs:** Always include `pricing_url` (the tool's pricing page) and `docs_url` (API documentation) when found via web search. These appear as clickable links in the deliverable so the client can verify.

Set `status`:
- `"complete"` — all fields populated, no open gaps
- `"needs_review"` — research done but gaps remain (listed in `gaps[]`)

### 2d. Custom build option

Load `references/apg-custom-build.md` for platform capabilities and module mapping. Load `{project-root}/_bmad/apg-pricing.md` for cost estimates.

Evaluate whether this change could be addressed by the custom platform:

1. **Module matching** — which template module(s) map to this change? Use the Module Mapping Guide.
2. **Scope assessment** — configure existing, medium customisation, custom build, or heavy custom?
3. **Comparative advantage** — how does custom compare to off-the-shelf tools in 2b?
4. **Feasibility** — set `false` only if the change requires certified/specialist software.

**Add the custom build as an entry in `tools_researched[]`** (same array as off-the-shelf tools) so it appears in the comparison table:

```json
{
  "tool_name": "Custom Build",
  "is_recommended": false,
  "category": "Custom Platform Module",
  "pricing_model": "flat",
  "pricing_summary": "~X weeks within platform. Client pays own infrastructure (~$50-100/mo) + maintenance retainer (from apg-pricing.md based on headcount). No per-user fees.",
  "cost_at_current_headcount": "Infrastructure ~$75/mo ($900/yr) + maintenance retainer — same cost at any headcount",
  "cost_at_scaled_headcount": "Infrastructure ~$75/mo ($900/yr) + retainer — no per-user scaling",
  "per_user_monthly_aud": 0,
  "flat_monthly_aud": null,
  "annual_cost_aud": null,
  "ongoing_infrastructure_monthly_aud": 75,
  "ongoing_retainer_monthly_aud": "LOOKUP from apg-pricing.md Maintenance Retainer Assignment Heuristic based on company_size",
  "api_available": true,
  "api_notes": "Full API access. Supabase auto-generated REST/GraphQL.",
  "pros": ["Unified with all other modules — single data platform", "No per-user fees at any scale", "AI features from day one", "Australian hosting available"],
  "cons": ["See apg-custom-build.md Realistic Considerations — only 2 genuine cons: sensitive data/compliance management and ongoing maintenance"],
  "integration_with_existing": "Replaces fragmented tool stack. Xero integration built in.",
  "pricing_url": "",
  "docs_url": "",
  "source_urls": [],
  "confidence": "HIGH"
}
```

**IMPORTANT — Custom build ongoing cost calculation:**
1. Look up `company_size` from audit data contact
2. Use the Maintenance Retainer Assignment Heuristic in `apg-pricing.md` to get the retainer
3. Add infrastructure estimate (~$75/mo for standard, ~$150/mo for scale)
4. `annual_cost_aud` = (retainer + infrastructure) × 12
5. Compare this to the total SaaS subscription stack it replaces

**Also populate `custom_build_option`** on the research object (for downstream consumers like TB and CP that need scope/module data):

```json
{
  "custom_build_option": {
    "feasible": true,
    "platform_modules": ["CRM Core (Leads)", "Integrations (Twilio)"],
    "estimated_scope": "Configure existing CRM lead pipeline + Twilio auto-acknowledgement",
    "scope_level": "configure_existing",
    "estimated_weeks": 1.0,
    "confidence": "HIGH"
  }
}
```

### 2e. Cowork + MCP training assessment

Load `references/apg-cowork-training.md` for the full Cowork delivery model, MCP availability guide, and assessment criteria.

For each proposed change, evaluate whether it could be delivered via **Claude Cowork + MCP training** instead of traditional SaaS configuration or automation:

1. **MCP viability** — Does the client's existing tool (from `tools[]`) have MCP support or an API that can be wrapped? Check the MCP Availability Guide.
2. **Trigger type** — Is this human-initiated (someone decides to do it) or event-driven (runs automatically)?
3. **Judgment required** — Does the task require context, decisions, or handling exceptions?
4. **Frequency** — Is this a daily/weekly task done by a person, or a high-volume automated process?
5. **User willingness** — Is there someone on the team who would use Cowork for this?

**Populate `cowork_training_option`** on the research object:

```json
{
  "cowork_training_option": {
    "viable": true,
    "viability_rationale": "Scheduling is human-initiated, requires judgment (staff preferences, participant needs, distance), and the tools (Google Calendar, Google Sheets) have MCP support. Dale currently does this manually — Cowork would let him describe the schedule in voice and have Claude build it.",
    "mcp_connections_required": ["Google Calendar", "Google Sheets"],
    "mcp_wrapper_needed": false,
    "training_scope": "single_use_case",
    "estimated_prep_hours": 4,
    "estimated_training_hours": 4,
    "estimated_followup_hours": 2,
    "total_hours": 10,
    "suggested_tier": "micro",
    "replaces_traditional": "n8n workflow + Google Apps Script",
    "general_productivity_uplift": true,
    "team_autonomy_benefit": "Dale can modify scheduling rules by updating his instructions to Claude — no developer needed for process changes.",
    "confidence": "HIGH"
  }
}
```

If **not viable**, still populate with `viable: false` and explain why:

```json
{
  "cowork_training_option": {
    "viable": false,
    "viability_rationale": "NDIS claiming requires certified software for compliance. Must be fully automated without human triggering. Not suitable for Cowork delivery.",
    "mcp_connections_required": [],
    "confidence": "HIGH"
  }
}
```

**Cowork vs traditional automation decision:**
- If the change is human-initiated and benefits from judgment → **prefer Cowork training** over n8n/Make/Zapier
- If the change must run autonomously 24/7 with no human involvement → traditional automation or SaaS
- If both could work → include both options, but flag Cowork as preferred (faster to deploy, client maintains control, no ongoing automation hosting cost)

**IMPORTANT:** When Cowork is viable, this often **replaces** the need for n8n, Make.com, or Zapier recommendations. Do not recommend workflow automation tools for changes that are better served by Cowork training. The client gets more value from understanding how to operate their tools via AI than from a black-box automation they can't modify.

### 2f. Industry landscape

Research what similar businesses in the client's industry (based on `industry_tag`) are doing to solve this same problem:

1. **Common approaches** — what tools and methods do businesses of this size/type typically use?
2. **Best practice** — what are leading organisations in this industry doing?
3. **Competitive position** — would adopting this change put the client ahead of, in line with, or behind their peers?

Use `WebFetch` to load relevant industry pages with queries like:
- `"{industry} {change_type} best practice {year}"`
- `"{industry} providers {tool_category} comparison"`
- `"what software do {industry} businesses use for {function}"`

**If web search is unavailable:** use training knowledge. Note in `common_approaches` that findings are based on general knowledge.

Populate `industry_landscape` in the research sub-object:

```json
{
  "industry_landscape": {
    "common_approaches": "Most NDIS providers of this size (50 staff) use ShiftCare or SupportAbility for rostering...",
    "best_practice": "Leading NDIS providers have moved to integrated platforms connecting participant management, rostering, and invoicing...",
    "competitive_position": "Implementing a CRM pipeline would put Great Supports ahead of most providers this size, where lead tracking is typically ad-hoc."
  }
}
```

### 2g. Quick win qualification

For each proposed_change, evaluate whether it qualifies as a **quick win** — something we can build in <10 dev hours using the client's existing tools.

**Qualification criteria (ALL must be true):**
1. **<10 dev hours** to implement
2. **Uses only the client's existing tools** (from `tools[]` in audit data) or free/trivial additions (N8N workflow, Google Apps Script, email template, Twilio SMS)
3. **No new SaaS subscriptions** required
4. **Concrete implementation plan** — you can describe exactly what gets built in one sentence

**Process:**
1. Review the client's `tools[]` array to know what they already have
2. For each proposed_change, ask: "Can I solve this in <10 hours using what they already have?"
3. If **yes** — write `quick_win_plan`:
   ```json
   {
     "qualified": true,
     "dev_hours": 6,
     "approach": "N8N workflow: trigger on new shift assignment → format SMS with shift details → send via Twilio to worker + participant guardian",
     "existing_tools": ["Google Sheets", "Twilio"],
     "disqualify_reason": null
   }
   ```
4. If **no** — write `quick_win_plan`:
   ```json
   {
     "qualified": false,
     "dev_hours": null,
     "approach": null,
     "existing_tools": [],
     "disqualify_reason": "Requires new scheduling platform (RotaWiz or similar) — not achievable with existing tools"
   }
   ```

**Common quick win patterns:**
- Automated SMS/email notifications (N8N + existing comms tool)
- Google Apps Script automations on existing spreadsheets
- Form automation (connect existing JotForm/Google Forms to actions)
- Dashboard creation from existing data (Google Sheets, Xero reports)
- Template creation and training (no dev work, just configuration)

**Common disqualifiers:**
- Needs a new SaaS tool to be set up first
- Requires database schema or data migration
- Involves complex business logic (scheduling rules, payroll calculations)
- Needs custom UI (forms, dashboards) beyond what existing tools provide
- Estimated >10 dev hours even with existing tools

---

## Stage 3: Generate New Opportunities (source: analyst)

After enriching existing client-stated changes, scan the audit data for untapped opportunities the client didn't mention:

### 3a. Unlinked pain points

Scan `pain_points[]` for entries whose `pain_point_id` does not appear in any `proposed_changes[].linked_pain_point_ids`. For each:
- Can this pain point be addressed by automation, tool replacement, or AI enablement?
- If yes: create a new proposed_change with `source: "analyst"`

### 3b. Unused API potential

Scan `tools[]` for entries with `api_available: true`. Cross-reference against `proposed_changes[].proposed_tools`. For tools with APIs that no change leverages:
- What automations could this API enable?
- What manual steps currently use this tool that could be automated?

### 3c. AI enablement opportunities

Based on the client's processes and industry, identify opportunities for:
- **AI call transcription/analysis** — if they have sales calls, support calls, or client meetings
- **AI document processing** — if they handle forms, applications, or compliance docs
- **AI-assisted decision making** — if they have manual triage, scoring, or matching processes
- **AI content generation** — if they produce reports, emails, or marketing content
- **AI sales coaching** — if they have BDMs or sales teams

These are `value_type: "productivity_enhancement"` — same hours, more output.

### 3d. Create new entries

For each new opportunity:

1. Assign next sequential `change_id` (e.g., if last is CH-006, start at CH-007)
2. Set `source: "analyst"`
3. Determine `change_type` (automate, replace, eliminate, consolidate)
4. Link to relevant `pain_point_ids` and `affected_step_ids`
5. Create a matching `roi_items[]` entry with `roi_item_id` assigned sequentially
6. Set `linked_roi_item_id` on the proposed_change
7. Carry forward `meeting_references` from source pain_points/waste_items/optimisations
8. Populate `research` sub-object (research these the same as existing changes)
9. Set `value_type` based on whether this saves time, enhances productivity, or both

---

## Stage 4: Display Summary

```
RESEARCH COMPLETE — {company_name}
Run #{run_count} · {datetime}

Existing changes researched: {n}/{total}
New opportunities generated: {n}

CLIENT-STATED CHANGES (source: client)
| # | ID     | Title                          | Value Type    | Cowork Viable | Custom Build | Research Status | Gaps |
|---|--------|--------------------------------|---------------|---------------|--------------|-----------------|------|
| 1 | CH-001 | Automate onboarding pack       | time_saving   | no            | feasible     | complete        | 0    |
| 2 | CH-006 | Voice scheduling engine        | time_saving   | YES           | feasible     | complete        | 0    |
...

ANALYST-GENERATED OPPORTUNITIES (source: analyst)
| # | ID     | Title                          | Value Type    | Cowork Viable | Custom Build | Research Status | Gaps |
|---|--------|--------------------------------|---------------|---------------|--------------|-----------------|------|
| 1 | CH-007 | AI call analysis for BDMs      | productivity  | YES           | feasible     | complete        | 0    |
| 2 | CH-008 | ShiftCare API auto-rostering   | time_saving   | no            | not feasible | needs_review    | 1    |
...

Changes with gaps:
  • CH-008: "Need to confirm ShiftCare API rate limits for batch roster updates"

Tool specificity check:
  ✓ All tool names are specific products: {pass_count}/{total_count}
  ✗ Generic tool names found: {list any generic names that need fixing}

⛔ BLOCKED — Generic tool names detected (see above). Fix these before saving.

Next step: Run [SA] to build strategic approaches, then [BR] to estimate weeks and calculate value.
```

### Generic Name Detection

Scan every `proposed_tools[]` entry across all changes. **BLOCK the save** if any match these patterns (case-insensitive):
- "scheduling platform", "scheduling tool", "scheduling system"
- "rostering tool", "rostering platform", "rostering system"
- "CRM system", "CRM platform", "CRM tool"
- "automation platform", "automation tool"
- "SMS API integration", "SMS platform"
- "invoicing platform", "invoicing tool"
- Any entry containing "platform", "tool", "system", or "provider" as a standalone word without a specific product name prefix

If generic names are found, go back and research specific alternatives before proceeding. There is always a specific product to name.

---

## Stage 5: Save

**Pre-save: Sync `proposed_tools[]` from research**

Before writing, for each proposed_change that has a `research.tools_researched[]` array:
1. Find the entry where `is_recommended: true`
2. Set `proposed_tools[]` to the recommended tool's `tool_name` (plus any secondary tools)
3. If `proposed_tools[]` still contains generic names (see Generic Name Detection above), **do not save** — go back and fix

**Save:**

1. Write updated `proposed_changes[]` and any new `roi_items[]` to `clients/{client_slug}/audit/audit-data.json`
2. Update `analyst_metadata` on the audit data:
   ```json
   {
     "analyst_metadata": {
       "last_analysis_run": "{ISO datetime}",
       "total_runs": {n},
       "changes_researched": {n},
       "changes_with_gaps": {n},
       "new_opportunities_generated": {n}
     }
   }
   ```
3. Confirm save with summary
