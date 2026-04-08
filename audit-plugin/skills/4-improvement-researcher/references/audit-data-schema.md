# Audit Data Schema — Process Analyst Reference

This is the analyst's reference for fields it reads and writes. For the full schema, see the Process Mapper's `references/audit-data-schema.md`.

## Fields the Analyst Reads

| Field | Source | Used by |
|-------|--------|---------|
| `proposed_changes[]` | Analyst EI | RI, BR, VR, TB |
| `pain_points[]` | Process Mapper SU | EI (synthesis), RI (unlinked scan) |
| `waste_items[]` | Process Mapper SU | EI (linking), RI (unlinked scan), BR (value calc) |
| `optimisations[]` | Process Mapper SU | EI (synthesis), RI (context) |
| `tools[]` | Process Mapper SU | RI (API scan, existing stack) |
| `processes[].steps[]` | Process Mapper SU | EI (step linking), BR (affected steps context) |
| `blended_hourly_rate_aud` | Process Mapper SU | BR (value calculation fallback) |
| `staff_roster[]` | Process Mapper SU | BR (role-specific rate lookup) |
| `industry_tag` | Process Mapper | RI (industry-specific research) |
| `sessions[]` | Process Mapper | BR (meeting references) |
| `roi_items[]` | Analyst EI | BR (update with estimates) |
| `pain_points_summary` | Process Mapper SU | EI (theme clustering) |

## Fields the Analyst Writes

### On `proposed_changes[]` entries

```
source                  "client|analyst"
value_type              "time_saving|productivity_enhancement|both"
research                { status, last_researched, run_count, tools_researched[],
                          feasibility_notes, similar_implementations, risks[], gaps[],
                          custom_build_option{}, industry_landscape{} }
implementation          { weeks_estimate, weeks_label, dev_hours, pm_hours, confidence }
value                   { value_type, time_saving{}, productivity_enhancement{},
                          combined_annual_value_aud, formula_summary }
quick_win_plan          null | { qualified: boolean, dev_hours: number,
                          approach: string, existing_tools: string[],
                          disqualify_reason: string|null }
modal_content           { what_is_the_task, what_we_will_build, how_it_works,
                          how_it_saves_money, how_quick, meeting_references[] }
```

### Quick Win Plan (added by RI Stage 2e)

Set on each `proposed_changes[]` entry by the RI quick win qualification step:

- `qualified` — true if this can be implemented in <10 dev hours using the client's existing tools
- `dev_hours` — estimated hours (must be <10 to qualify)
- `approach` — concrete implementation plan (e.g., "N8N workflow: Google Form responses → Twilio bulk SMS to staff")
- `existing_tools` — array of tool names from the client's `tools[]` that are used
- `disqualify_reason` — if `qualified: false`, explains why (e.g., "Requires new SaaS subscription", "Estimated 15+ dev hours")

Items with `quick_win_plan.qualified: true` are shown as Quick Wins on the options page. Items without qualification or with `qualified: false` fall into the SaaS Toolkit or Custom Platform tiers.

### Research — Pricing Accuracy Fields

Added by RI on each `tools_researched[]` entry to track pricing source quality:

```
pricing_source_type       "official|aggregator|blog|estimated|training_knowledge" — where pricing was found
pricing_verified_date     ISO date — when pricing was last verified via web search
pricing_is_estimated      boolean — true when not from official/aggregator source
hidden_costs[]            array of hidden/upsell costs (see below)
total_cost_with_hidden_aud  number — annual_cost_aud + sum of likely hidden costs
```

`hidden_costs[]` entry:
```
type                      "upsell|add_on|implementation|onboarding|data_migration|overage|minimum_commitment|support_tier|api_access"
description               string — what this cost is and when it applies
estimated_cost_aud        number (monthly) or null
estimated_annual_aud      number or null
trigger                   string — what causes this cost (e.g., "needing SSO", "exceeding 1000 API calls/month")
likelihood                "likely|possible|unlikely"
source_url                string — where this hidden cost was documented
```

Field notes:
- `pricing_source_type` semantics: `"official"` = vendor's own pricing page; `"aggregator"` = CostBench, CompareTiers, Vendr, G2, or Capterra; `"blog"` = blog post or comparison article; `"estimated"` = calculated from partial data; `"training_knowledge"` = no web source, model knowledge only
- `hidden_costs[].likelihood`: `"likely"` = most customers encounter this; `"possible"` = depends on usage; `"unlikely"` = edge case. Only `"likely"` costs feed into `total_cost_with_hidden_aud`.
- Confidence semantics for pricing: HIGH = official/recent aggregator (< 3 months); MEDIUM = blog or older aggregator; LOW = training knowledge or "Contact sales" with estimates

### Research — Custom Build Option (`research.custom_build_option`)

Added by RI (Step 2d). Evaluates whether the custom platform can address this change. Loads `references/apg-custom-build.md` for module mapping and `{project-root}/_bmad/apg-pricing.md` for cost estimates.

```
feasible                true|false — can the platform address this change?
platform_modules        string[] — which template modules apply (e.g., ["CRM Core (Leads)", "Workspace (Tasks)"])
estimated_scope         string — plain-English description of what's needed within the platform
scope_level             "configure_existing|medium_customisation|custom_build|heavy_custom"
advantages              string[] — specific advantages of custom build for THIS change
disadvantages           string[] — specific disadvantages for THIS change
estimated_weeks         number — weeks to implement within the platform
confidence              "HIGH|MEDIUM|LOW"
```

### Research — Industry Landscape (`research.industry_landscape`)

Added by RI (Step 2e). How similar businesses in the client's industry solve this problem.

```
common_approaches       string — what tools/methods peers typically use
best_practice           string — what leading organisations in this industry do
competitive_position    string — where adopting this change positions the client vs peers
```

### On `roi_items[]` entries

```
annual_saving_aud       updated from value.combined_annual_value_aud
monthly_saving_aud      annual / 12
build_cost_aud          (dev_hours × dev_rate) + (pm_hours × pm_rate)
payback_months          build_cost_aud / monthly_saving_aud
payback_tag             QUICK_WIN (<12mo) | CORE_BUILD (12-24mo) | FUTURE (>24mo)
```

### Top-level

```
analyst_metadata        { last_analysis_run, total_runs, changes_researched,
                          changes_with_gaps, new_opportunities_generated }
```

## New `proposed_changes[]` entries (source: "analyst")

When RI generates new opportunities, it creates full proposed_change entries:
- `change_id` — sequential after existing (e.g., CH-007 if last is CH-006)
- `source` — always `"analyst"`
- `linked_roi_item_id` — points to a new roi_items entry also created by RI
- `meeting_references` carried forward from source pain_points/waste_items
- All standard fields (title, change_type, affected_step_ids, etc.) populated

### Transformation Blueprint Fields

The following fields are added to `proposed_changes[]` by the Process Analyst [TB] (Build Transformation Blueprint) capability. All are optional — backward compatible with audit data files that have not been through the blueprint pass.

- `proposed_changes[].phase` — integer phase number (1, 2, or 3). Assigned by TB based on `payback_tag`.
- `proposed_changes[].phase_label` — human-readable phase label (e.g., "Quick Wins (Weeks 1-4)").
- `proposed_changes[].sequence_order` — integer ordering within the phase. No-dependency changes first, then by highest value descending.
- `proposed_changes[].depends_on` — array of `change_id` strings that must complete before this change can start. Derived from step-level overlaps.
- `proposed_changes[].future_step_description` — what the affected step looks like after this change is implemented. Used by the generator for the "Future State" column.
- `proposed_changes[].future_step_owner` — who owns the step after the change (may differ from current owner if automation takes over).
- `proposed_changes[].future_step_tools` — array of tool name strings used in the future state.
- `proposed_changes[].future_step_type` — `"step"` (standard post-change step), `"automation"` (fully automated), or `"eliminated"` (step removed entirely). Drives rendering in the transformation blueprint.

### Transformation Blueprint (top-level)

`transformation_blueprint` — populated by the Process Analyst [TB] capability. Contains phase groupings and summary metrics for the transformation blueprint HTML deliverable.

```json
{
  "transformation_blueprint": {
    "phases": [
      {
        "phase_number": 1,
        "label": "Quick Wins",
        "timeframe": "Weeks 1-4",
        "description": "Low-effort, high-value changes that can be implemented immediately",
        "change_ids": ["CH-001", "CH-003"]
      }
    ],
    "total_phases": 3,
    "estimated_total_weeks": 12,
    "total_steps_current": 47,
    "total_steps_future": 32,
    "total_annual_value_aud": 85000,
    "last_built": "2026-03-22T14:30:00Z"
  }
}
```

Field notes:
- `phases[].phase_number` — 1 = Quick Wins (QUICK_WIN payback_tag), 2 = Core Build (CORE_BUILD), 3 = Future (FUTURE).
- `phases[].timeframe` — human-readable estimated timeframe for this phase.
- `phases[].change_ids` — array of `change_id` strings included in this phase.
- `total_steps_current` — count of all process steps across all stages (pre-transformation).
- `total_steps_future` — count of steps remaining after eliminations and consolidations.
- `total_annual_value_aud` — sum of `combined_annual_value_aud` across all proposed changes.
- `last_built` — ISO timestamp of last TB run.
