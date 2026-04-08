---
name: build-strategic-approaches
description: Build a single recommended SaaS toolkit with configuration detail per tool. Writes strategic_approaches to audit-data.json. Custom build is handled separately by the Solution Designer.
menu-code: SA
---

# Build Strategic Approaches (SA)

> **Idempotent.** First run builds the recommended toolkit from scratch. Re-runs deepen research, update tool selections, and refresh integration analysis.

## Purpose

Look at the ENTIRE process holistically and build one recommended SaaS toolkit. For each proposed change, select the smartest SaaS tool — free if genuinely adequate, paid if not — and provide configuration detail so the client knows exactly what to set up.

Unlike [RI] which researches each pain point individually, this command asks: "What combination of SaaS tools makes this process smooth end-to-end?" Each tool selection must reference a specific, named product — never generic advice.

**SaaS only.** The custom build option is NOT included here. It is handled separately by the Solution Designer (RE → BA → BP), which builds a prototype. The client then compares the SaaS toolkit against the custom build side-by-side during the presentation.

**This is the core analytical step.** The output drives the strategic-approaches.html deliverable. Run it multiple times to deepen research — each run improves tool selection rationale, integration analysis, and coverage.

---

## Stage 1: Pre-flight

1. Check audit data is loaded and `proposed_changes[]` is populated with research:
   ```
   ✗ proposed_changes[] has no research data. Run [RI] Research Improvements first.
   ```

2. Count research readiness:
   ```
   STRATEGIC APPROACHES STATUS — {company_name}
   Total proposed changes: {n}
     with research complete:   {n}
     with research incomplete: {n}

   Existing strategic_approaches: {present|absent}
   ```

3. If `strategic_approaches` already exists, show existing summary and ask:
   ```
   Existing strategic approaches found (run #{run_count}, {generated_at}).
   Options:
     A) Full rebuild — re-research and rebuild the toolkit
     B) Deepen existing — focus research on gaps and weak areas
     C) Cancel
   ```

4. If research is incomplete on some changes, warn but proceed — tool selections will be marked as lower confidence.

---

## Stage 2: Build the Recommended Toolkit

### 2a. Tool Selection Logic

For every `proposed_change` in scope, select one specific SaaS tool. Rules:

**CRITICAL — Tool Specificity:**
- Every tool selection MUST be a specific, named product: "HubSpot CRM", "ShiftCare", "Make.com", "Excel", "Manual phone call"
- NEVER use generic descriptions: "NDIS scheduling provider", "rostering tool", "CRM system", "automation platform"
- Even manual/existing methods must be named: "Manual phone call", "Excel spreadsheet", "Paper form", "Email (Gmail)"
- If no tool can cover a change, put it in `uncovered_changes` — don't use a generic placeholder
- NEVER select "Custom Build" — custom build is handled separately by the Solution Designer

**CRITICAL — Realistic Pricing:**
- When selecting a tool, use the `realistic_tier` and `realistic_annual_cost_aud` fields from RI research (Step 2b-iv)
- If `requires_paid_plan: true`, do NOT cost the tool at $0 — use the realistic tier pricing

**Selection logic — for each proposed change:**
- If the best free tool has tolerable limitations (`free_plan_limitations` has ≤2 items AND none are dealbreakers for the client's scale), use it
- Otherwise use the recommended paid tool at `realistic_annual_cost_aud`
- Never select "Custom Build"
- Use `is_recommended: true` as a strong signal, but override if the recommended tool is free and clearly inadequate

### 2b. Fields per tool_selection entry

Each entry in `tool_selections[]` must include:

| Field | Type | Description |
|-------|------|-------------|
| `change_id` | string | e.g. "CH-001" |
| `title` | string | The proposed change title |
| `selected_tool` | string | Specific named product with tier, e.g. "HubSpot CRM (Free tier)" |
| `rationale` | string | Why this tool for this change |
| `why_this_tool` | string | 2-3 sentence narrative explaining why this specific tool was chosen over alternatives. Reference the alternatives that were considered. E.g., "HubSpot CRM was selected because Great Supports already has an account and the free tier covers their current pipeline needs. Zoho CRM was considered but would require a fresh setup with no existing data." |
| `tier_selected` | string | Which tier, e.g. "Free", "Starter", "Professional" |
| `configuration_steps` | string[] | 4-8 concrete, actionable setup steps specific to the client's business. E.g., ["Create a new pipeline in HubSpot with stages: Referral Received → Initial Contact → Assessment Booked → Onboarding", "Import existing contacts from the Google Sheets participant database", "Set up auto-assignment rules to route NDIS referrals to Dale"] |
| `caveats` | string[] | 2-4 limitations and gotchas. Pull from `free_plan_limitations`, `hidden_costs` with likelihood "likely", and relevant `cons`. E.g., ["Free tier limited to 1 pipeline — if you need separate pipelines for NDIS and private clients, Starter tier ($30/mo) is required", "No workflow automation on Free — all follow-up reminders must be set manually"] |
| `integration_notes` | string | How this tool connects to others in the toolkit |
| `annual_cost_aud` | number | Annual cost at selected tier |
| `per_user_monthly_aud` | number | Per-user monthly cost (0 if flat rate or free) |
| `weeks_estimate` | number | Implementation weeks |
| `weeks_label` | string | Human-readable estimate, e.g. "<1 week" |
| `annual_value_aud` | number | Annual value of the improvement this tool enables |

### 2c. Cowork Training Programme

Load `references/apg-cowork-training.md` for the full Cowork delivery model and assessment criteria.

Review all proposed changes and identify those where `cowork_training_option.viable == true` (populated by RI Step 2e). Bundle these into a **Cowork Training Programme** within the toolkit:

1. **Group by MCP connection** — changes sharing the same MCP connections (e.g., Google Calendar + Google Sheets) train naturally together
2. **Identify the primary user** — who on the team would be trained (e.g., Dale for scheduling, admin staff for email management)
3. **Calculate bundle scope** — use the training scope tiers from `apg-cowork-training.md`:
   - 1 use case → Micro ($1,800)
   - 2-3 use cases → Standard ($3,800)
   - 4-6 use cases → Complex ($6,500)
4. **Calculate general productivity uplift** — beyond specific use cases, estimate the general productivity value for trained users: `trained_users × conservative_hours_per_week × hourly_rate × 52`

For each Cowork-viable change in the toolkit, the `tool_selections[]` entry should reflect the Cowork approach:

```json
{
  "change_id": "CH-006",
  "title": "Rules-based scheduling engine with voice input",
  "selected_tool": "Claude Cowork (Google Calendar + Google Sheets MCP)",
  "rationale": "Scheduling requires human judgment — staff preferences, participant needs, travel distance. Cowork lets Dale describe the schedule in voice and Claude builds it using the existing tools.",
  "why_this_tool": "Traditional scheduling SaaS (ShiftCare, RotaCloud) was considered but these tools fight against the flexibility Dale needs for complex NDIS scheduling with ratios. Cowork gives Dale direct control — he describes what he needs, Claude handles the calendar entries and spreadsheet updates. No new subscription, no rigid system.",
  "tier_selected": "Cowork Training (Micro)",
  "configuration_steps": [
    "Connect Google Calendar and Google Sheets to Cowork via MCP",
    "Build custom instructions covering Dale's scheduling rules (ratios, travel, preferences)",
    "Train Dale on voice-driven scheduling: 'Build next week's schedule for the Belmont group'",
    "Practice exception handling: cancellations, swaps, last-minute availability changes"
  ],
  "caveats": [
    "Requires Claude Team subscription (~$30/user/mo) for ongoing use",
    "Not fully autonomous — someone must initiate each scheduling session",
    "Complex ratio calculations may need verification initially until Claude learns the patterns"
  ],
  "integration_notes": "Reads staff availability from Google Calendar, writes shifts to both Calendar and the scheduling spreadsheet. No new tools needed.",
  "annual_cost_aud": 360,
  "per_user_monthly_aud": 30,
  "weeks_estimate": 0.5,
  "weeks_label": "<1 week",
  "annual_value_aud": 15600,
  "delivery_type": "cowork_training"
}
```

**Add `delivery_type`** to every `tool_selections[]` entry:
- `"saas_configuration"` — traditional SaaS setup
- `"cowork_training"` — delivered via Cowork training programme
- `"automation"` — n8n/Make/Zapier workflow (use only when Cowork is not viable AND the process must run autonomously)

**Add a `cowork_training_programme` summary** to the strategy:

```json
{
  "cowork_training_programme": {
    "total_cowork_changes": 5,
    "change_ids": ["CH-006", "CH-007", "CH-008", "CH-014", "CH-016"],
    "mcp_connections": ["Google Calendar", "Google Sheets", "Gmail"],
    "primary_users": ["Dale Ross (Operations Manager)"],
    "training_bundle_tier": "standard",
    "training_cost_aud": 3800,
    "ongoing_subscription_aud_monthly": 30,
    "general_productivity_uplift": {
      "trained_users": 1,
      "conservative_hours_per_week": 3,
      "hourly_rate_aud": 40,
      "annual_value_aud": 6240,
      "formula": "1 user × 3 hrs/wk × $40/hr × 52 wks = $6,240/yr"
    },
    "team_autonomy_note": "Dale gains direct control of scheduling, communications, and reporting through Claude — can adapt processes without developer involvement."
  }
}
```

### 2d. Research tool integration and cohesion

Research how the selected tools (including Cowork-delivered ones) work TOGETHER:

1. **Integration points** — For each pair of tools in the toolkit, research:
   - Does a native integration exist? (e.g., HubSpot ↔ Xero)
   - Is a connector available? (Zapier, Make.com, native webhook)
   - What data flows between them? (contacts, invoices, tasks, etc.)
   - Use `mcp__exa__web_search_exa` to verify: `"{tool_a} {tool_b} integration"`

2. **Data flow analysis** — Map how data moves through the process:
   - Where does data originate? Which tool is the source of truth?
   - Where are manual handoffs required? (copy/paste, re-entry, exports)
   - Are there data silos? (information trapped in one tool)

3. **Data silo assessment** — For each tool in the toolkit:
   - What data gets trapped in this tool? (use `data_silo_risk` from RI research)
   - Where will staff need to copy-paste data between tools?
   - What reports require exporting from one tool and importing to another?
   - Populate `data_silos[]` and `copy_paste_handoffs[]` on the strategy

4. **Integration development costs** — Estimate what it would cost to connect these tools:
   - Zapier/Make.com subscription costs for automated workflows
   - Developer time to build custom integrations (at internal dev rate from `apg-pricing.md`)
   - Populate `integration_development_cost_aud` (one-off estimate)

5. **Cohesion assessment** — Evaluate the toolkit as a whole:
   - Does this create a smooth end-to-end workflow?
   - How many separate logins does the team need?
   - Is there a single source of truth or fragmented data?
   - How much manual glue work is needed between tools?
   - Be honest and critical — SaaS fragmentation is real, don't downplay it

### 2e. Deep-dive tool research (SaaS tools only — skip Cowork-delivered changes)

For each unique tool selected across the toolkit, conduct deep research:

1. **User feedback and satisfaction** — Search for recent reviews:
   - `mcp__exa__web_search_exa`: `"{tool_name} review {current_year}"`
   - `mcp__exa__web_search_exa`: `"{tool_name}" site:g2.com`
   - `mcp__exa__web_search_exa`: `"{tool_name}" site:capterra.com`
   - Summarise: overall satisfaction, common praise, common complaints
   - Note the satisfaction rating if found (e.g., "4.3/5 on G2")

2. **Hidden upsells and lock-in risks** — Research what vendors don't advertise:
   - `mcp__exa__web_search_exa`: `"{tool_name} hidden costs" OR "gotchas" OR "what they don't tell you"`
   - `mcp__exa__web_search_exa`: `"{tool_name}" site:costbench.com`
   - Check for: data export limitations, contract lock-in periods, price increases history
   - Check for: feature gates that force tier upgrades, API access restrictions, migration difficulty

3. **Scaling concerns** — Research what happens as the client grows:
   - Per-user pricing trajectory at 2x headcount
   - Feature limits that trigger tier jumps (e.g., "500 contacts free, then $50/mo")
   - `mcp__exa__web_search_exa`: `"{tool_name} pricing increase" OR "scaling costs"`

**If web search is unavailable:** use training knowledge. Mark findings with `confidence: "LOW"` and add to `research_gaps[]`.

### 2f. Calculate costs

Calculate for the single toolkit:

```
implementation_weeks = sum of weeks_estimate for all covered changes
ongoing_annual_total_aud = ongoing_annual_saas_aud + ongoing_annual_cowork_tools_aud + ongoing_annual_cowork_subscriptions_aud
ongoing_annual_saas_aud = sum of annual_cost_aud for SaaS-only tool_selections (delivery_type == "saas_configuration")
ongoing_annual_cowork_tools_aud = sum of annual_cost_aud for Cowork API/tool costs (Google Maps, etc.)
ongoing_annual_cowork_subscriptions_aud = Claude Team subscription cost
ongoing_annual_scaled_aud = sum of scaled costs for selected tools at 2x headcount
hidden_costs_annual_aud = sum of hidden_costs[].estimated_annual_aud where likelihood == "likely"
  NOTE: This MUST be calculated from per-tool hidden_costs data. If no structured hidden_costs exist,
  estimate from hidden_upsells text where dollar amounts are extractable (e.g., "$750/mo" in HubSpot
  upsells = $9,000/yr if likelihood "likely"). MUST NOT be left at 0 if likely upsells have dollar amounts.
total_setup_cost_aud = sum of setup_cost_aud for all selected tools
total_consultant_fees_aud = sum of consultant_fee_estimate_aud for all selected tools
integration_development_cost_aud = estimated cost to connect tools (Zapier/Make subscriptions + dev time)
cowork_training_cost_aud = sum of cowork_training_programme.training_cost_aud (bundled Cowork training package)
cowork_ongoing_annual_aud = cowork_training_programme.ongoing_subscription_aud_monthly × trained_users × 12
saas_training_cost_aud = 8 hours × ${YOUR_CHARGEOUT_RATE}/hr (agency charge-out rate from apg-pricing.md) = $1,200 baseline, adjusted up based on number of new SaaS tools the team needs to learn
training_cost_aud = cowork_training_cost_aud + saas_training_cost_aud
total_first_year_cost_aud = ongoing_annual_total_aud + total_setup_cost_aud + total_consultant_fees_aud + integration_development_cost_aud + training_cost_aud
per_tool_admin_hours_monthly = sum of ongoing_admin_hours_monthly for all selected tools
cross_tool_admin_hours_monthly = estimate the overhead of stitching N distinct tools together:
  - Data sync / duplicate entry: new records must be entered across multiple systems (~20 mins per record × frequency)
  - Cross-system lookups: admin staff searching multiple tools to find info (NDIS providers report 5-10 hrs/week saved by consolidation)
  - Record consistency: keeping N tools in sync when staff leave, details change, funding updates (~N tools × changes/week × 10 mins)
  - Integration maintenance: monitoring automations, API tokens, debugging broken connections (~1 hr/mo)
  - Context switching: productivity lost switching between N+ apps (research shows 9.5 mins to regain focus per switch)
  Scale this based on number of distinct tools and company headcount. More tools and more staff = more cross-tool overhead.
total_ongoing_admin_hours = per_tool_admin_hours_monthly + cross_tool_admin_hours_monthly
```

**Use `realistic_annual_cost_aud`** for tools where `requires_paid_plan: true`. Use `annual_cost_aud` ($0) for tools where free tier is genuinely sufficient.

### 2g. Resolve pain points

Trace which pain points are resolved:
- Collect all `linked_pain_point_ids` from covered changes
- Deduplicate
- Look up from `pain_points[]` — include description, quote, speaker

---

## Stage 3: Write Strategic Approaches to Audit Data

Write the `strategic_approaches` top-level object to audit-data.json. The `strategies[]` array must contain exactly 1 element:

```json
{
  "strategic_approaches": {
    "generated_at": "{ISO datetime}",
    "run_count": 1,
    "total_changes": 17,
    "total_annual_value_aud": 196560,
    "current_staff": 50,
    "scaled_staff": 100,
    "strategies": [
      {
        "strategy_id": "recommended-saas-toolkit",
        "name": "Recommended SaaS Toolkit",
        "icon": "🎯",
        "best_for": "The smartest mix of free and paid SaaS tools for your business",
        "description": "A curated toolkit where each tool earns its place — free where free genuinely works, paid where it doesn't. Every selection includes configuration steps so your team knows exactly what to set up.",
        "how_it_works": "For each of your {total} identified improvements, we selected the best SaaS tool — free if it can handle your scale, paid if the free tier would hold you back. Each tool comes with specific setup steps, caveats, and integration notes.",
        "tool_selections": [
          {
            "change_id": "CH-001",
            "title": "Implement CRM pipeline for lead tracking",
            "selected_tool": "HubSpot CRM (Free tier)",
            "rationale": "Already installed — just activate the pipeline feature. Free tier covers core CRM needs.",
            "why_this_tool": "HubSpot CRM was selected because Great Supports already has an account and the free tier covers their current pipeline volume (~30 leads/month). Zoho CRM was considered but would require a fresh setup and data migration with no existing integrations.",
            "tier_selected": "Free",
            "configuration_steps": [
              "Create a new pipeline in HubSpot with stages: Referral Received → Initial Contact → Assessment Booked → Onboarding",
              "Import existing contacts from the Google Sheets participant database using HubSpot's CSV import tool",
              "Set up auto-assignment rules to route NDIS referrals to Dale",
              "Configure deal properties: Funding Type (NDIS/Private), Service Required, Suburb, Start Date"
            ],
            "caveats": [
              "Free tier limited to 1 pipeline — if you need separate pipelines for NDIS and private clients, Starter tier ($30/mo) is required",
              "No workflow automation on Free — all follow-up reminders must be set manually",
              "Free reporting limited to basic dashboards — no custom report builder"
            ],
            "integration_notes": "Native Gmail + Calendar sync already configured.",
            "annual_cost_aud": 0,
            "per_user_monthly_aud": 0,
            "weeks_estimate": 0.5,
            "weeks_label": "<1 week",
            "annual_value_aud": 63120
          }
        ],
        "uncovered_changes": [
          {
            "change_id": "CH-008",
            "title": "API-based roster sync",
            "reason": "No SaaS tool available — requires custom integration development",
            "annual_value_missed_aud": 15600
          }
        ],
        "integration_analysis": {
          "data_flow": "Leads enter HubSpot → manual handoff to onboarding spreadsheet → ShiftCare for rostering. No automated data flow between stages.",
          "integration_points": [
            {
              "tool_a": "HubSpot CRM",
              "tool_b": "Google Sheets",
              "integration_type": "manual",
              "notes": "Currently requires manual copy of new client details from CRM to onboarding spreadsheet"
            },
            {
              "tool_a": "HubSpot CRM",
              "tool_b": "Xero",
              "integration_type": "native",
              "notes": "HubSpot-Xero sync available on Starter tier ($30/mo) but not on Free"
            }
          ],
          "manual_handoffs": 3,
          "separate_logins": 4,
          "data_silos": [
            "Contact/deal data locked in HubSpot — no sync to rostering or onboarding",
            "Participant records in ShiftCare — manual re-entry for invoicing",
            "Staff availability in Google Calendar — no feed into scheduling"
          ],
          "copy_paste_handoffs": [
            "New client details copied from HubSpot CRM to Google Sheets onboarding tracker",
            "Shift details from scheduling spreadsheet re-entered into ShiftCare for invoicing"
          ],
          "integration_development_cost_aud": 3000,
          "cohesion_assessment": "Moderate fragmentation. Free tools work independently but data doesn't flow between them automatically. Team still needs to manually transfer information between stages.",
          "single_source_of_truth": false
        },
        "tool_deep_dives": [
          {
            "tool_name": "HubSpot CRM",
            "user_feedback_summary": "Highly rated for ease of use (4.4/5 on G2). Users praise the free tier generosity but commonly complain about aggressive upselling to Professional tier for automation features.",
            "satisfaction_rating": "4.4/5 (G2, 12,000+ reviews)",
            "hidden_upsells": [
              "Professional tier ($750/mo) required for workflow automation — most CRM implementations need this within 6 months",
              "Marketing Hub add-on ($65/mo) needed for email sequences beyond basic"
            ],
            "lock_in_risks": [
              "Data export is available but CRM customisations don't transfer",
              "No contract lock-in on free/Starter tiers"
            ],
            "scaling_concerns": [
              "Free tier limited to 1 pipeline — multiple sales processes need Starter ($30/mo)",
              "Contact storage unlimited on free but marketing contacts are capped"
            ],
            "source_urls": [
              "https://www.g2.com/products/hubspot-crm/reviews",
              "https://www.hubspot.com/pricing"
            ],
            "confidence": "HIGH"
          }
        ],
        "cost_summary": {
          "implementation_weeks": 4.0,
          "ongoing_annual_current_aud": 2400,
          "ongoing_annual_scaled_aud": 4800,
          "hidden_costs_annual_aud": 2000,
          "total_setup_cost_aud": 1500,
          "total_consultant_fees_aud": 0,
          "integration_development_cost_aud": 3000,
          "training_cost_aud": 960,
          "total_first_year_cost_aud": 7860,
          "total_ongoing_admin_hours": 10
        },
        "coverage": {
          "covered_count": 16,
          "total_count": 17,
          "covered_value_aud": 180960,
          "uncovered_value_aud": 15600,
          "coverage_percentage": 94.1
        },
        "pain_points_resolved": ["PP-001", "PP-003", "PP-005"],
        "limitations": [
          "Some free-tier tools may need paid upgrades as the business scales",
          "Integration between tools requires Zapier/Make.com or manual handoffs",
          "No unified system — data lives across multiple tools"
        ],
        "research_gaps": []
      }
    ]
  }
}
```

**On re-run (run_count > 1):**
- Increment `run_count`
- Update `generated_at`
- Preserve and deepen existing research — don't discard previous findings
- Focus on areas with `research_gaps[]` or `confidence: "LOW"`

---

## Stage 4: Display Summary

```
RECOMMENDED SAAS TOOLKIT — {company_name}
Run #{run_count} · {datetime}

| Toolkit                  | Coverage     | Annual Cost | Scaled Cost | Hidden Costs | Setup Cost | Training Cost | 1st Year Total | Admin Hrs/mo | Value Covered  | Gaps |
|--------------------------|--------------|-------------|-------------|--------------|------------|---------------|----------------|--------------|----------------|------|
| Recommended SaaS Toolkit | 16/17 (94%) | $2,400/yr   | $4,800/yr   | $2,000/yr    | $1,500     | $960          | $7,860         | 10           | $180,960/yr    | 0    |

Integration Analysis:
  Recommended SaaS Toolkit: 3 manual handoffs, 4 logins, 3 data silos, no single source of truth

Note: Custom build option is handled separately by Solution Designer (RE → BA → BP).
The client will compare this SaaS toolkit against the custom build prototype during the presentation.

Research gaps:
  (none)

Next step: Run Generator [GA] to create strategic-approaches.html.
```

---

## Stage 5: Save

1. Write `strategic_approaches` top-level object to `clients/{client_slug}/audit/audit-data.json`
2. Update `analyst_metadata`:
   ```json
   {
     "analyst_metadata": {
       "last_sa_run": "{ISO datetime}",
       "total_sa_runs": 1
     }
   }
   ```
3. Confirm save with summary
