# Audit Data Schema — Solution Architect Reference

This is the Solution Architect's reference for fields it reads and writes. For the full schema, see the Process Mapper's `references/audit-data-schema.md`.

## Fields the Solution Architect Reads

| Field | Source | Used by |
|-------|--------|---------|
| `proposed_changes[]` | Improvement Researcher EI/RI | RE (decomposition) |
| `proposed_changes[].implementation` | Improvement Researcher BR | RE (scope estimation) |
| `proposed_changes[].value` | Improvement Researcher BR | RE (priority weighting) |
| `proposed_changes[].proposed_tools[]` | Improvement Researcher EI/RI | RE (integration specs) |
| `proposed_changes[].depends_on` | Improvement Researcher TB | RE (dependency mapping) |
| `proposed_changes[].phase` | Improvement Researcher TB | RE (phase-aware requirements) |
| `proposed_changes[].modal_content` | Improvement Researcher BR | RE (user story derivation) |
| `proposed_changes[].affected_step_ids` | Improvement Researcher EI | RE (screen inventory, data model) |
| `proposed_changes[].research` | Improvement Researcher RI | RE (integration specs, API details, pricing accuracy) |
| `proposed_changes[].research.tools_researched[].hidden_costs[]` | Improvement Researcher RI | CP (net saving calculation) |
| `proposed_changes[].research.tools_researched[].total_cost_with_hidden_aud` | Improvement Researcher RI | CP (true cost comparison) |
| `proposed_changes[].research.tools_researched[].pricing_source_type` | Improvement Researcher RI | CP (pricing confidence) |
| `proposed_changes[].research.tools_researched[].requires_paid_plan` | Improvement Researcher RI | RE (realistic costing) |
| `proposed_changes[].research.tools_researched[].realistic_tier` | Improvement Researcher RI | RE (tier assessment) |
| `proposed_changes[].research.tools_researched[].realistic_annual_cost_aud` | Improvement Researcher RI | RE (cost comparison) |
| `proposed_changes[].research.tools_researched[].free_plan_limitations[]` | Improvement Researcher RI | RE (limitation analysis) |
| `proposed_changes[].research.tools_researched[].setup_cost_aud` | Improvement Researcher RI | RE (implementation costing) |
| `proposed_changes[].research.tools_researched[].data_silo_risk` | Improvement Researcher RI | RE (integration assessment) |
| `strategic_approaches.strategies[].cost_summary.total_first_year_cost_aud` | Improvement Researcher SA | RE (cost comparison) |
| `strategic_approaches.strategies[].integration_analysis.data_silos[]` | Improvement Researcher SA | RE (integration gaps) |
| `transformation_blueprint` | Improvement Researcher TB | RE (phase structure reference) |
| `tools[]` | Process Mapper SU | RE (existing tool stack context), BA (integration architecture) |
| `staff_roster[]` | Process Mapper SU | RE (user role identification), BP (prototype data) |
| `session_economics` | Process Mapper SU | BP (prototype data) |
| `waste_items[]` | Process Mapper SU | BP (prototype data) |
| `processes[].steps[]` | Process Mapper SU | RE (step context for requirements) |
| `requirements_spec` | Architect RE | BA (architecture source), BP (prototype source) |
| `architecture_doc` | Architect BA | VA (verification), BP (prototype generation) |
| `pain_points[]` | Process Mapper SU | VA (coverage matrix) |
| `optimisations[]` | Process Mapper SU | VA (optimisation coverage) |
| `proposed_changes[].linked_pain_point_ids` | Improvement Researcher EI | VA (trace chain) |
| `proposed_changes[].linked_optimisation_ids` | Improvement Researcher EI | VA (trace chain) |
| `requirements_spec.requirements[].user_stories[].acceptance_criteria[]` | Architect RE | VA (interactivity cross-ref) |
| `architecture_doc.user_journeys[]` | Architect BA | VA (journey step analysis) |
| `architecture_doc.page_structure` | Architect BA | VA (screen analysis) |
| `architecture_doc.data_models[]` | Architect BA | VA (addressability check) |
| `architecture_doc.module_inventory[]` | Architect BA | VA (addressability check) |
| `architecture_verification` | Architect VA | BP (prototype brief) |

## Fields the Solution Architect Writes

### `requirements_spec` (top-level) — written by [RE]

```
generated_at              ISO timestamp
scope                     all_packages|specific_package|standalone_items|all
package_ids_included[]    which packages were decomposed
requirements[]
  requirement_id          REQ-001, REQ-002, etc.
  change_id               source proposed change
  package_id              parent package
  title                   requirement title
  user_stories[]          {story_id, role, action, outcome, acceptance_criteria[]}
  priority                must-have|should-have|nice-to-have
  complexity              low|medium|high
  notes                   additional context
user_roles[]
  role_id                 ROLE-001, etc.
  name                    role name
  source                  staff_roster|end_user
  staff_members[]         named staff in this role
  affected_packages[]     which packages this role touches
  permission_level        admin|standard|read-only|external
  notes
screen_inventory[]
  screen_id               SCR-001, etc.
  name                    screen name
  type                    configuration|dashboard|input|notification|integration
  package_id              parent package
  requirement_ids[]       linked requirements
  platform                which system hosts this screen
  description             what the screen does
  user_roles[]            who uses this screen
  is_custom_build         true if custom dev needed (vs. native platform UI)
  notes
data_model
  entities[]              {entity_id, name, source_system, key_fields[], relationships[], package_ids[], notes}
  data_flows[]            {flow_id, name, source_entity, source_system, destination_system, trigger, fields_mapped[], frequency, package_id}
integrations[]
  integration_id          INT-001, etc.
  name                    integration name
  source_system           origin system
  target_system           destination system
  integration_method      API|webhook|middleware|manual
  middleware              integration platform (e.g., Make.com)
  package_id              parent package
  api_details             {source_api, target_api, auth_method, rate_limits}
  data_entities[]         linked entity IDs
  requirements[]          linked requirement IDs
  risks[]                 integration risks
  notes
summary
  total_requirements, total_user_stories, total_user_roles,
  total_screens, custom_build_screens, total_entities,
  total_integrations, total_data_flows
```

### `architecture_doc` (top-level) — written by [BA]

```
generated_at              ISO timestamp
selected_strategy_id      which strategy was architected (e.g., "apg-unified-platform")
module_inventory[]
  module_name             extracted module name (e.g., "CRM Module")
  scope_level             configure_existing|medium_customisation|custom_build|heavy_custom
  change_ids[]            linked proposed change IDs
  template_modules[]      platform template modules this maps to
  weeks_estimate          estimated build weeks
user_journeys[]
  role                    user role ID
  journey_name            descriptive name
  module                  which module this journey primarily uses
  change_ids[]            linked proposed change IDs (traceability)
  steps[]
    screen                screen ID (SCR-xxx)
    action                what the user does
    data_shown[]          data fields/entities visible on this screen
    data_input[]          data fields the user enters
    integration           external system triggered (optional)
    next                  next screen ID in journey
page_structure
  pages[]
    screen_id             SCR-xxx
    name                  screen display name
    route                 URL route (kebab-case, e.g., /crm/leads)
    parent                parent route (null for top-level)
    module                which module this page belongs to
    roles[]               which roles can access this page
    components[]          Untitled UI component names (Table, Input, Badge, etc.)
  navigation[]
    section               nav section label (usually module name)
    module                module this section represents
    items[]
      label               nav item display text
      route               URL route
      icon                Untitled UI icon name (e.g., Users01, Calendar01)
      roles[]             which roles see this nav item
data_models[]
  entity                  entity name
  table_name              Supabase table name (snake_case)
  module                  which module owns this entity
  fields[]
    name                  field name
    type                  uuid|string|integer|decimal|boolean|timestamp|enum|jsonb
    primary               true if primary key
    required              true if not nullable
    unique                true if unique constraint
    default               default value expression
    foreign_key           referenced table.field (if FK)
    values[]              enum values (if type=enum)
  relationships[]
    to                    target entity name
    type                  one-to-many|many-to-one|many-to-many
    foreign_key           FK field name
    label                 human-readable relationship name
access_policies[]
  role                    role ID
  permission_level        admin|standard|read-only|external
  entity_policies[]
    entity                entity name
    read                  true|false|"assigned_only"|"own_only"|"team_only"
    write                 true|false|"own_only"|specific action string
    delete                true|false
    scope_field           field used for row-level scoping
  rls_policies[]          (platform only)
    entity                entity name
    policy_name           Supabase RLS policy name
    rls_policy            SQL expression for RLS
  screen_access
    accessible[]          screen IDs this role can navigate to
    hidden[]              screen IDs hidden from this role
integration_architecture[]
  integration_id          INT-xxx
  name                    integration display name
  source                  source system
  target                  target system
  type                    REST API|webhook|OAuth2|manual
  direction               inbound|outbound|bidirectional
  auth_method             OAuth2|API key|webhook secret
  endpoints[]
    method                GET|POST|PUT|DELETE
    path                  API endpoint path
    purpose               what this endpoint does
  trigger                 what initiates the sync
  sync_frequency          real-time|daily|on-demand
  entities_synced[]       entity names involved
  field_mappings[]
    platform_field        field in {YOUR_COMPANY} platform
    external_field        field in external system
  error_handling          error strategy description
  implementation          (platform only)
    type                  edge_function|webhook|cron|realtime
    function_name         Supabase Edge Function name
    trigger               database event or schedule
    cron                  cron expression (if scheduled)
    secrets[]             required environment secrets
    estimated_complexity  low|medium|high
tech_stack
  framework               e.g., "Next.js 15 (App Router)"
  language                e.g., "TypeScript 5.3+"
  ui_library              e.g., "Untitled UI (200+ components)"
  css                     e.g., "Tailwind CSS 4"
  state                   e.g., "Zustand + React Query"
  api                     e.g., "tRPC + Supabase auto-generated REST"
  database                e.g., "PostgreSQL 15 via Supabase"
  auth                    e.g., "Supabase Auth"
  storage                 e.g., "Supabase Storage"
  realtime                e.g., "Supabase Realtime"
  hosting                 e.g., "Vercel + Supabase (Sydney region)"
  external_apis[]         list of external API names
  template_modules[]      platform modules used as-is
  custom_modules[]        modules requiring custom build
```

### `architecture_verification` (top-level) — written by [VA]

```
generated_at              ISO timestamp
run_count                 count
architecture_doc_timestamp  snapshot of architecture_doc.generated_at at verification time

pain_point_coverage[]
  pain_point_id           PP-xxx
  description             copied from pain_points[] for readability
  stage                   business stage
  coverage_status         fully_covered|view_only|partial|missing|deferred
  trace
    proposed_change_ids[] linked change IDs
    requirement_ids[]     linked requirement IDs
    user_story_ids[]      linked user story IDs
    journey_refs[]        {journey_name, role, step_index, screen, action, has_interaction, interaction_type[]}
    prototype_screens[]   {screen_id, route, resolution_description}
  resolution_summary      human-readable explanation of how pain point is resolved

optimisation_coverage[]
  optimisation_id         OPT-xxx
  description             copied from optimisations[]
  stage                   business stage
  coverage_status         addressed_this_phase|addressed_later_phase|addressable_but_missing|not_addressable|fully_covered|view_only|partial|missing
  phase                   implementation phase number
  trace                   same structure as pain_point_coverage trace
  resolution_summary
  recommendation          null or recommendation text (for addressable_but_missing)
  suggested_module        null or module name
  suggested_change_id     null or change ID
  effort_estimate         null or low|medium|high

interactivity_issues[]
  issue_id                INT-xxx
  journey_name
  role
  step_index
  screen                  SCR-xxx
  action
  current_level           interactive|navigational|view_only
  expected_level          interactive
  reason                  why interaction is expected here
  recommendation          specific fix to architecture_doc
  severity                high|medium|low
  linked_pain_point_ids[]
  linked_acceptance_criteria[]

simplicity_recommendations[]
  rec_id                  SIMP-xxx
  type                    screen_consolidation|redundant_entry|depth_reduction|journey_overlap|over_engineered
  description
  affected_screens[]
  affected_journeys[]
  impact
  severity                high|medium|low

prototype_brief[]
  pain_point_id           PP-xxx or null for optimisation-only
  optimisation_id         null or OPT-xxx
  headline                short tagline for resolution
  screen_route            URL route
  screen_name
  primary_action          key thing the user does
  data_the_user_sees[]
  data_the_user_enters[]
  interaction_model       how the user interacts (drag-drop, form, modal, etc.)
  demo_scenario           step-by-step scenario for prototype demo
  linked_optimisation_ids[]
  original_quote          client's own words about the pain

summary
  total_pain_points, pain_points_fully_covered, pain_points_view_only,
  pain_points_partial, pain_points_missing, pain_points_deferred,
  total_optimisations, optimisations_this_phase, optimisations_later_phase,
  optimisations_addressable_now, optimisations_not_addressable,
  total_interactivity_issues, interactivity_high, interactivity_medium, interactivity_low,
  total_simplicity_recommendations, prototype_brief_items,
  verification_pass       boolean (true when no missing PPs, no high interactivity issues)
  blocking_issues[]       list of blocking issue descriptions
```

### `architect_metadata` (top-level)

```
last_re_run               ISO timestamp of last RE run
total_re_runs             count
requirements_extracted    count
packages_covered[]        package IDs with requirements
last_ba_run               ISO timestamp of last BA run
total_ba_runs             count
selected_strategy_id      which strategy was last architected
last_va_run               ISO timestamp of last VA run
total_va_runs             count
last_va_pass              boolean
va_blocking_issues        count of blocking issues
last_bp_run               ISO timestamp of last BP run
total_bp_runs             count
prototype_pages           count of pages generated
prototype_path            output directory path
```
