# Audit Data Schema

The audit data file is the source of truth for a complete audit engagement. Every output agent reads from this document. The analyst writes to it. The generator reads from it to produce HTML deliverables.

**Path:** `clients/{client_slug}/audit/audit-data.json`

## Schema

```json
{
  "client_slug": "",
  "company_name": "",
  "industry_tag": "ndis|home-services|construction|real-estate|other",
  "audit_start_date": "",
  "audit_status": "discovery|session-1|session-2|session-3|process_map_complete",
  "sessions_completed": 0,
  "google_drive_folder_url": "",
  "crm": {
    "contact_id": null,
    "lead_id": null,
    "project_id": null,
    "task_list_ids": {
      "extraction": null,
      "analysis": null,
      "deliverables": null,
      "solution_design": null
    },
    "last_synced": null
  },
  "contact": {
    "name": "",
    "role": "",
    "company_size": "",
    "revenue_range": "",
    "domain": "",
    "emails": []
  },
  "blended_hourly_rate_aud": null,
  "blended_rate_confidence": "HIGH|MEDIUM|LOW",
  "blended_rate_source": "",
  "business_stages_covered": [],
  "tools": [
    {
      "tool_name": "",
      "current_plan": "",
      "seats": null,
      "monthly_cost_aud": null,
      "use_case": "",
      "workarounds": "",
      "api_available": null,
      "quote": "",
      "source_session": null,
      "source_timestamp_seconds": null,
      "meeting_references": [
        { "meeting_id": "", "timestamp_seconds": null, "label": "" }
      ],
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "processes": [
    {
      "stage": "snake_case key derived from transcript (e.g. acquisition, sales_listing, property_management)",
      "name": "Human-readable stage label (e.g. 'Acquisition', 'Quoting & Proposals')",
      "description": "One-line subtitle (e.g. 'Lead generation, referrals & initial contact')",
      "steps": [
        {
          "step_id": "",
          "description": "",
          "owner": "",
          "type": "step|decision|pain|optimisation|automation|parallel_group",
          "branch_only": false,
          "duration_minutes": null,
          "frequency": "",
          "source_session": null,
          "source_quote": "",
          "source_speaker": "",
          "source_timestamp_seconds": null,
          "confidence": "HIGH|MEDIUM|LOW",
          "tool_ids": [],
          "data_flow": null,
          "meeting_references": [
            {
              "meeting_id": "",
              "timestamp_seconds": null,
              "label": "",
              "transcript_excerpt": ""
            }
          ],
          "email_references": [
            {
              "filename": "",
              "subject": "",
              "excerpt": ""
            }
          ],
          "items": []
        }
      ]
    }
  ],
  "decision_nodes": [
    {
      "node_id": "",
      "condition": "",
      "yes_path": "",
      "no_path": "",
      "yes_branch_step_ids": [],
      "no_branch_step_ids": [],
      "owner": "",
      "stage": "",
      "after_step_id": "",
      "source_session": null,
      "source_quote": "",
      "source_timestamp_seconds": null,
      "meeting_references": [
        { "meeting_id": "", "timestamp_seconds": null, "label": "" }
      ],
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "pain_points": [
    {
      "pain_point_id": "",
      "description": "",
      "stage": "",
      "quote": "",
      "speaker": "",
      "source_session": null,
      "source_timestamp_seconds": null,
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "pain_points_summary": {
    "total_count": 0,
    "by_stage": {},
    "top_themes": [
      {
        "theme": "",
        "count": 0,
        "stages_affected": [],
        "example_quote": ""
      }
    ]
  },
  "optimisations": [
    {
      "optimisation_id": "OPT-001",
      "description": "",
      "stage": "snake_case key matching a processes[].stage entry",
      "quote": "",
      "speaker": "",
      "source_session": null,
      "source_timestamp_seconds": null,
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "waste_items": [
    {
      "waste_id": "W-001",
      "description": "",
      "activity": "",
      "stage": "",
      "hours_per_week": null,
      "headcount_affected": null,
      "hourly_rate_aud": null,
      "rate_is_estimated": true,
      "annual_waste_aud": null,
      "monthly_waste_aud": null,
      "waste_type": "manual_data_entry|duplicate_work|no_followup|communication_gap|missing_automation",
      "quote": "",
      "source_session": null,
      "source_timestamp_seconds": null,
      "meeting_references": [
        { "session": 1, "timestamp_seconds": null, "fathom_url": "" }
      ],
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "roi_items": [
    {
      "roi_item_id": "ROI-001",
      "activity": "",
      "annual_saving_aud": null,
      "monthly_saving_aud": null,
      "suggested_tier": "micro|standard|complex|sprint",
      "build_cost_aud": null,
      "payback_months": null,
      "payback_tag": "QUICK_WIN|CORE_BUILD|FUTURE",
      "quote": "",
      "source_session": null,
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "proposed_changes": [
    {
      "change_id": "CH-001",
      "title": "string",
      "change_type": "automate|replace|eliminate|consolidate",
      "affected_step_ids": ["STEP-012"],
      "linked_roi_item_id": "ROI-002",
      "linked_pain_point_ids": ["PP-003"],
      "proposed_solution": "string",
      "proposed_tools": ["Tool A"],
      "proposed_step_description": "string (optional — for consolidate type, describes the merged step)",
      "time_saving_minutes_per_occurrence": 45,
      "frequency": "per placement",
      "stage": "onboarding_family",
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "quick_wins": [],
  "contradictions": [
    {
      "contradiction_id": "",
      "topic": "",
      "statement_a": {
        "session": null,
        "speaker": "",
        "quote": "",
        "timestamp_seconds": null,
        "meeting_id": ""
      },
      "statement_b": {
        "session": null,
        "speaker": "",
        "quote": "",
        "timestamp_seconds": null,
        "meeting_id": ""
      },
      "resolution": "",
      "status": "unresolved|resolved"
    }
  ],
  "completeness_checklist": {
    "acquisition": {
      "covered": false,
      "confidence": "LOW",
      "items_confirmed": [],
      "items_missing": []
    },
    "quoting": {
      "covered": false,
      "confidence": "LOW",
      "items_confirmed": [],
      "items_missing": []
    },
    "onboarding": {
      "covered": false,
      "confidence": "LOW",
      "items_confirmed": [],
      "items_missing": []
    },
    "fulfilment": {
      "covered": false,
      "confidence": "LOW",
      "items_confirmed": [],
      "items_missing": []
    },
    "retention": {
      "covered": false,
      "confidence": "LOW",
      "items_confirmed": [],
      "items_missing": []
    }
  },
  "follow_up_questions": [
    {
      "question_id": "FQ-001",
      "question": "",
      "stage": "",
      "priority": "HIGH|MEDIUM|LOW",
      "reason": "",
      "status": "pending|answered|researched",
      "answered_in_session": null,
      "classification": "researchable|client_required",
      "classification_reason": "",
      "research_answer": "",
      "research_confidence": "HIGH|MEDIUM|LOW",
      "research_sources": [],
      "researched_at": null
    }
  ],
  "sessions": [
    {
      "session_number": null,
      "date": "",
      "transcript_file": "",
      "fathom_meeting_id": "",
      "fathom_url": "",
      "participants": [],
      "stages_covered": [],
      "key_findings": [],
      "analyzed": false
    }
  ],
  "objections": [],
  "positive_signals": [],
  "data_gaps": []
}
```

## Field Notes

## Parallel Group Example

When multiple parallel sources, channels, or tools feed into the same downstream step, model them as a `parallel_group` instead of a single bundled step:

```json
{
  "step_id": "ACQ-sources",
  "description": "Lead sources",
  "owner": "",
  "type": "parallel_group",
  "source_session": 1,
  "confidence": "HIGH",
  "items": [
    { "label": "Google Ads", "tool": "Google Ads", "owner": null, "source_quote": "", "source_timestamp_seconds": null, "meeting_references": [] },
    { "label": "Meta Ads", "tool": "Meta Ads", "owner": null, "source_quote": "", "source_timestamp_seconds": null, "meeting_references": [] },
    { "label": "Instagram", "tool": "Instagram", "owner": null, "source_quote": "", "source_timestamp_seconds": null, "meeting_references": [] },
    { "label": "SEO", "tool": null, "owner": null, "source_quote": "", "source_timestamp_seconds": null, "meeting_references": [] },
    { "label": "Direct / Referral", "tool": null, "owner": null, "source_quote": "", "source_timestamp_seconds": null, "meeting_references": [] }
  ],
  "meeting_references": [],
  "email_references": [],
  "gemini_screenshots": []
}
```

## Field Notes

- `processes[].name` — human-readable display label for this stage (e.g. "Acquisition", "Quoting & Proposals"). Used by the generator for sidebar nav, zone headers, and all stage references. If omitted, the generator falls back to title-casing the `stage` key.
- `processes[].description` — one-line subtitle shown under the zone header (e.g. "Lead generation, referrals & initial contact"). Optional — if omitted, no subtitle is rendered.
- `google_drive_folder_url` — optional Google Drive folder URL where the client shares documents. When set, `fetch-drive-folder.py` syncs new files into `client-provided-materials/google-drive/` on every SU run. Leave empty string `""` if not applicable.
- `audit_status` progresses: `discovery` → `session-1` → `session-2` → `session-3` → `process_map_complete`. Update after each session is analyzed and confirmed.
- `processes[].steps[].type` drives the HTML box type in the process map: `step` (standard), `decision` (diamond), `pain` (red highlight), `optimisation` (green), `automation` (blue).
- `roi_items` are calculated from `waste_items` after running `payback-gate.py`. `quick_wins` is a filtered view of `roi_items` where `payback_tag == "QUICK_WIN"`.
- `completeness_checklist` tracks per-stage coverage. A stage is `covered: true` only when the consultant confirms it — not when items are inferred.
- `contradictions` are never auto-resolved. Status stays `unresolved` until the consultant explicitly confirms resolution.
- `contradictions[].statement_a.timestamp_seconds` / `statement_b.timestamp_seconds` — integer utterance start time (seconds) from the Fathom transcript. `meeting_id` is the `fathom_meeting_id` from `sessions[]`.
- `decision_nodes[].source_timestamp_seconds` — utterance start time (seconds) from the Fathom transcript where this decision was discussed. Used to generate deep-link URLs.
- `decision_nodes[].meeting_references` — array of timestamped Fathom deep-links, same structure as step-level references: `{ meeting_id, timestamp_seconds, label }`. Populate for every meeting-sourced decision node.
- **`sessions[]` is for Fathom meetings ONLY.** Emails, PDFs, and other client-provided materials are NOT sessions — they are tracked in `extracted_materials[]`. Data extracted from materials uses `"source_material"` (file path) instead of `"source_session"` (session number).
- `extracted_materials[]` — array of processed non-meeting inputs. Each entry: `{ source_file, date, type (email|pdf|document), from, extracted[] }`. Items extracted from materials produce `null` timestamps and empty `meeting_references` — this is expected, not an error.
- `follow_up_questions` and `data_gaps` are analyst-generated meta-observations, not direct extractions — timestamps do not apply.
- `follow_up_questions[].question_id` — sequential identifier (FQ-001, FQ-002, ...). Assigned by FQ pre-flight if missing.
- `follow_up_questions[].status` — `"pending"` (awaiting answer), `"answered"` (confirmed by client in a session), or `"researched"` (answered via web research by FQ capability). `"researched"` is distinct from `"answered"` — research findings should be validated by the client.
- `follow_up_questions[].classification` — `"researchable"` (answerable via web search — tool capabilities, API docs, pricing, regulatory info) or `"client_required"` (needs business knowledge from the client). Set by FQ capability.
- `follow_up_questions[].classification_reason` — one sentence explaining why this classification was chosen.
- `follow_up_questions[].research_answer` — concise answer synthesised from web research. For API questions, must lead with **specific endpoint paths, HTTP methods, key parameters, and response formats** from official documentation. Generic statements ("Tool X has an API") are not acceptable. Only populated when `status: "researched"`.
- `follow_up_questions[].research_confidence` — `"HIGH"` (official API documentation with endpoint references found), `"MEDIUM"` (API confirmed via third-party integrations but official endpoint docs not public), `"LOW"` (training knowledge only, no docs found).
- `follow_up_questions[].research_sources` — array of source URLs. Must prioritise **official API documentation pages** (developer docs, endpoint references) over marketing pages or third-party integration listings. Each URL should be a page a developer could open and start building from. Empty array if based on training knowledge only.
- `follow_up_questions[].researched_at` — ISO 8601 timestamp of when the research was conducted.
- `blended_hourly_rate_aud` is extracted from transcripts (salary ÷ 2,080 for annual; weighted average for multiple roles). Fallback: `50` with `confidence: LOW`.
- `contact.emails` is an array of contact emails used as Fathom API lookup keys. The script queries each email and deduplicates results. Add multiple emails if meetings are booked under different addresses.
- `sessions[].fathom_meeting_id` and `sessions[].fathom_url` are populated from `clients/{slug}/meetings/{meeting_id}/metadata.json` after running `fetch-transcripts.py`.
- `processes[].steps[].source_timestamp_seconds` — the utterance start time (in seconds) from the Fathom transcript where this step was discussed.
- `processes[].steps[].source_quote` — verbatim or near-verbatim quote(s) from the transcript that best capture this step. Can be a **string** (single quote) or an **array of strings** (multiple quotes, e.g. when a step is discussed across several utterances or revisited later). Be generous with length — full sentences are better than paraphrases. If the discussion spans several lines, capture all of them. The generator joins array entries and uses them for keyword-based transcript search, so more distinctive words = better excerpt matching. Avoid vague paraphrases; copy actual phrasing from the transcript.
- `processes[].steps[].meeting_references` — array of timestamped Fathom deep-links for this step. Each entry: `{ meeting_id, timestamp_seconds, label, transcript_excerpt? }`. The deep-link URL is `https://{FATHOM_URL}/calls/{call_id}?t={timestamp_seconds}` (where `call_id` comes from `sessions[].fathom_url`, not from the recording_id / `fathom_meeting_id`). This array is rendered as expandable dialogue dropdowns in the process map HTML. Add **multiple entries** when a step or topic is discussed at more than one point across sessions. `transcript_excerpt` (optional): 3–5 verbatim sentences of surrounding dialogue; if omitted, the generator extracts context automatically from the local transcript file.
- `processes[].steps[].email_references` — array of email evidence files that support this step. Each entry: `{ filename, subject, excerpt }`. Files live in `clients/{slug}/emails/` and are manually added by the analyst. Rendered as green pill links in the process map HTML.
- `clients/{slug}/emails/` — drop zone for email evidence files. Any format accepted (`.eml`, `.pdf`, `.txt`). Files here are manually referenced by filename in `email_references` on process steps.
- `parallel_group` — renders as a horizontal row of individual chips, each optionally with a tool badge and owner badge, all converging with merge arrows into the next step. Use whenever multiple parallel inputs, sources, tools, or paths all lead to the same downstream step. Never bundle these into a single step description.
- `items[].tool` — optional tool name matching `tools[]`. Renders as a tool badge on the chip.
- `items[].owner` — optional person/role. Renders as an owner tag on the chip.
- `items[].meeting_references` — per-item Fathom links, same structure as step-level references.
- `tools[].source_timestamp_seconds` — timestamp of first/most substantive tool mention; MM:SS → seconds.
- `tools[].meeting_references` — one entry per session where the tool was discussed. Same structure as step-level references. Used to render ▶ Recording badges on tool tags in the People Bar.
- `data_gaps` — array of strings documenting known information gaps in the audit. Two categories:
  - **Quantitative gaps**: missing metrics, costs, headcounts (e.g. `"No salary data for ops staff"`)
  - **Handoff gaps**: undocumented system-to-system or person-to-person data transfer mechanisms. Format: `"HANDOFF GAP [STEP-A → STEP-B]: description. Follow-up: specific question"`
- `processes[].steps[].branch_only` — boolean (default: false). When `true`, the step is excluded from the main sequential flow and rendered only inside a decision gate branch column. Set this on any step that belongs exclusively to a YES or NO branch path of a `decision_nodes` entry. Pair with `no_branch_step_ids` / `yes_branch_step_ids` on the decision node.
- `decision_nodes[].no_branch_step_ids` — ordered array of `step_id` strings to render as a stacked sequence inside the NO column of the decision gate. Each referenced step must also have `"branch_only": true` so it is skipped in the main flow. The renderer calls `render_step()` or `render_parallel_group()` for each step in order, with v-arrows between them.
- `decision_nodes[].yes_branch_step_ids` — same as `no_branch_step_ids` but for the YES column. Omit if the YES path is a simple one-liner text (`yes_path` string).
- `processes[].steps[].tool_ids` — array of tool name strings that must each match a `tool_name` in the top-level `tools[]` array. Empty `[]` for purely manual/verbal steps.
- `processes[].steps[].data_flow` — structured handoff descriptor for how data arrives at this step from the previous one. `null` for the first step in a stage. When populated: `from_step_id` references the upstream step, `mechanism` is one of: `manual_entry`, `automated_sync`, `email_notification`, `api_integration`, `manual_check`, `csv_export`, `verbal`, `unknown`. `unknown` explicitly flags an undocumented handoff and should trigger a follow-up question. `confidence` reflects how explicitly the mechanism was described in transcripts.
- `waste_items[].hourly_rate_aud` — the hourly rate used to calculate this specific waste item's dollar cost. When the transcript mentions a specific salary or rate for the role performing the wasted activity, derive the hourly rate (annual salary ÷ 2,080). When no role-specific rate is available, fall back to `blended_hourly_rate_aud` and set `rate_is_estimated: true`.
- `waste_items[].rate_is_estimated` — `true` when `hourly_rate_aud` is a fallback estimate (from `blended_hourly_rate_aud` or industry default), `false` when derived from a specific salary/rate discussed in transcripts. Displayed in the waste page so the client knows which figures are precise vs estimated.
- `waste_items[].source_timestamp_seconds` — utterance start time (seconds) from the Fathom transcript where this waste item was discussed. Used to generate deep-link URLs.
- `waste_items[].meeting_references` — array of timestamped Fathom deep-links, same structure as step-level references: `{ session, timestamp_seconds, fathom_url }`. Populate for every waste item so reviewers can jump directly to the discussion.
- `waste_items[].source_session` — (required) session number where this waste was identified. Must be populated for every waste item.
- `pain_points[].pain_point_id` — unique identifier (e.g., `"PP-001"`) for cross-referencing pain points in the summary and priority matrix.
- `pain_points[].source_timestamp_seconds` — utterance start time (seconds) from the Fathom transcript where this pain point was raised.
- `optimisations[]` — top-level array of client-stated improvement wishes, desired automations, and future-state aspirations. Populated by EB alongside `type: "optimisation"` process steps (which remain in `processes[]` for the process map). Each entry appears on findings.html with a green "OPTIMISATION" eyebrow. `optimisation_id` is sequential (OPT-001, OPT-002, …).
- `pain_points_summary` — computed after extraction. Groups pain points by theme for the process map summary section. `top_themes[].stages_affected` lists which stages the theme appears in. Updated whenever pain_points[] changes.
- `roi_items[].roi_item_id` — unique identifier (e.g., `"ROI-001"`) assigned sequentially. Auto-assigned by EI pre-flight if missing. Required for cross-referencing in `proposed_changes[].linked_roi_item_id`.
- `proposed_changes[]` — populated by the Process Analyst [EI] (Extract Improvements) capability after `audit_status == "process_map_complete"`. Never written during session analysis. Each change maps to one or more `affected_step_ids` and must link to a `linked_roi_item_id`.
- `proposed_changes[].change_type` semantics:
  - `automate` — the step remains but is performed by software/integration instead of a person
  - `replace` — the current tool/method is swapped for a better one
  - `eliminate` — the step is removed entirely (no longer needed)
  - `consolidate` — two or more steps are merged; use `proposed_step_description` to describe the merged result
- `proposed_changes[].proposed_step_description` — optional; required for `consolidate` type to describe what the merged step looks like after change.

## Process Analyst Fields

The following fields are added to `proposed_changes[]` by the Process Analyst agent (RI/BR capabilities). All are optional — backward compatible with SSSADs that have not been through the analyst.

- `proposed_changes[].source` — `"client"` (extracted from transcripts by EI) or `"analyst"` (new opportunity generated by the Process Analyst). Defaults to `"client"` if absent.
- `proposed_changes[].value_type` — `"time_saving"` (reduces hours on existing task), `"productivity_enhancement"` (increases output with same hours, e.g. AI enablement), or `"both"`.

### Research Sub-object

`proposed_changes[].research` — populated by RI (Research Improvements):
```json
{
  "status": "not_started|in_progress|complete|needs_review",
  "last_researched": "2026-03-22T14:30:00Z",
  "run_count": 0,
  "tools_researched": [
    {
      "tool_name": "HubSpot CRM",
      "is_recommended": true,
      "category": "CRM / Sales Pipeline",
      "pricing_model": "per_user|flat|per_unit|free|usage_based|custom",
      "pricing_summary": "Free: $0, Starter: $30/mo, Professional: $155/mo",
      "cost_at_current_headcount": "$0/yr (Free) — only 2-3 users need access",
      "cost_at_scaled_headcount": "$0/yr (Free) — unlimited users",
      "per_user_monthly_aud": 0,
      "flat_monthly_aud": 0,
      "annual_cost_aud": 0,
      "pricing_source_type": "official|aggregator|blog|estimated|training_knowledge",
      "pricing_verified_date": "2026-03-30",
      "pricing_is_estimated": false,
      "pricing_url": "https://www.hubspot.com/pricing",
      "docs_url": "https://developers.hubspot.com/docs/api",
      "source_urls": ["https://www.hubspot.com/pricing"],
      "hidden_costs": [
        {
          "type": "upsell|add_on|implementation|onboarding|data_migration|overage|minimum_commitment|support_tier|api_access",
          "description": "",
          "estimated_cost_aud": null,
          "estimated_annual_aud": null,
          "trigger": "",
          "likelihood": "likely|possible|unlikely",
          "source_url": ""
        }
      ],
      "total_cost_with_hidden_aud": 0,
      "api_available": true,
      "api_notes": "REST API on all tiers. Rate limited on Free. Webhooks require Professional.",
      "pros": [],
      "cons": [],
      "integration_with_existing": "Already have HubSpot as phone directory. Gmail sync available.",
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "custom_build_option": {
    "feasible": true,
    "platform_modules": [],
    "estimated_scope": "",
    "scope_level": "configure_existing|medium_customisation|custom_build|heavy_custom",
    "estimated_weeks": 1.0,
    "confidence": "HIGH|MEDIUM|LOW"
  },
  "industry_landscape": {
    "common_approaches": "",
    "best_practice": "",
    "competitive_position": ""
  },
  "feasibility_notes": "",
  "similar_implementations": "",
  "risks": [],
  "gaps": []
}
```

#### Pricing fields on `tools_researched[]`

- `pricing_model` — `"per_user"` | `"flat"` | `"per_unit"` | `"free"` | `"usage_based"` | `"custom"` — determines how cost scales with headcount
- `per_user_monthly_aud` — if per-user, the monthly AUD cost per user (null if flat/free)
- `flat_monthly_aud` — if flat, the monthly AUD cost regardless of users (null if per-user)
- `annual_cost_aud` — total annual cost at the recommended tier for the client's current headcount
- `cost_at_current_headcount` — human-readable string showing the calculation (e.g., "$21/user × 3 users × 12mo = $756/yr")
- `cost_at_scaled_headcount` — same calculation at 2× current headcount
- `pricing_source_type` — where pricing was sourced. `"official"` = vendor's own pricing page; `"aggregator"` = CostBench, CompareTiers, Vendr, G2, or Capterra; `"blog"` = blog post or comparison article; `"estimated"` = calculated from partial data; `"training_knowledge"` = no web source found, based on model knowledge
- `pricing_verified_date` — ISO date when pricing was last verified via web search
- `pricing_is_estimated` — `true` when pricing could not be confirmed from official or aggregator sources. Rendered as a visual indicator in deliverables so the client knows which numbers are firm vs approximate
- `pricing_url` — direct link to the tool's pricing page (for client verification)
- `total_cost_with_hidden_aud` — `annual_cost_aud` + sum of `hidden_costs[].estimated_annual_aud` where `likelihood == "likely"`. Pre-calculated for downstream consumers.

#### Hidden costs on `tools_researched[]`

- `hidden_costs[]` — array of hidden/upsell costs that may not be apparent from headline pricing. Populated during RI research from CostBench hidden cost pages, vendor fine print, and pricing comparison sites.
- `hidden_costs[].type` — category: `"upsell"` (tier upgrade needed for required features), `"add_on"` (paid feature not in base tier), `"implementation"` (setup/deployment fee), `"onboarding"` (training fee), `"data_migration"` (import fee), `"overage"` (usage exceeding plan limits), `"minimum_commitment"` (annual contract requirement), `"support_tier"` (premium support fee), `"api_access"` (API requires higher tier)
- `hidden_costs[].trigger` — what causes this cost to appear (e.g., "exceeding 1,000 API calls/month", "needing SSO", "more than 5 users")
- `hidden_costs[].likelihood` — `"likely"` (most customers encounter this), `"possible"` (depends on usage pattern), `"unlikely"` (edge case but worth noting). Only `"likely"` costs are factored into `total_cost_with_hidden_aud`.
- `hidden_costs[].source_url` — URL where this hidden cost was documented

#### Confidence semantics for pricing

- `HIGH` — pricing from official page or aggregator with recent data (< 3 months old)
- `MEDIUM` — pricing from blog/comparison post or aggregator with older data
- `LOW` — training knowledge only, or vendor shows "Contact sales" with estimated pricing

### Implementation Sub-object

`proposed_changes[].implementation` — populated by BR (Build & Rate):
```json
{
  "weeks_estimate": 0.5,
  "weeks_label": "<1 week|1-2 weeks|2-4 weeks|4+ weeks",
  "dev_hours": 16,
  "pm_hours": 4,
  "confidence": "HIGH|MEDIUM|LOW"
}
```
- `weeks_estimate` — decimal weeks shown on the priority matrix X axis (e.g., 0.5 = half a week, 2 = two weeks)
- `weeks_label` — human-readable label for the weeks estimate
- `dev_hours` / `pm_hours` — internal effort breakdown, not shown to client

### Value Sub-object

`proposed_changes[].value` — populated by BR (Build & Rate):
```json
{
  "value_type": "time_saving|productivity_enhancement|both",
  "time_saving": {
    "hours_saved_per_week": 3.5,
    "hourly_rate_aud": 50,
    "annual_saving_aud": 9100,
    "formula": "3.5 hrs/wk × $50/hr × 52 wks = $9,100/yr"
  },
  "productivity_enhancement": {
    "description": "AI sales feedback increases close rate by ~10%",
    "current_revenue_or_metric": 120000,
    "improvement_percentage": 10,
    "estimated_annual_value_aud": 12000,
    "formula": "$120,000 revenue × 10% improvement = $12,000/yr",
    "confidence": "LOW|MEDIUM|HIGH"
  },
  "combined_annual_value_aud": 21100,
  "formula_summary": "Time: $9,100 + Productivity: $12,000 = $21,100/yr"
}
```
- `formula` — human-readable calculation string shown to the client in the priority matrix modal
- `combined_annual_value_aud` — sum of time_saving.annual_saving_aud + productivity_enhancement.estimated_annual_value_aud. Used for the priority matrix Y axis.

### Modal Content Sub-object

`proposed_changes[].modal_content` — populated by BR (Build & Rate):
```json
{
  "what_is_the_task": "",
  "what_we_will_build": "",
  "how_it_works": "",
  "how_it_saves_money": "",
  "how_quick": "",
  "meeting_references": [
    { "session": 1, "timestamp_seconds": 420, "fathom_url": "", "transcript_excerpt": "" }
  ]
}
```
- 5 client-facing text sections rendered in the priority matrix modal when the user clicks a bubble
- `meeting_references` — Fathom deep-links to the transcript moments that support this opportunity, same structure as step-level references

### Transformation Blueprint Fields

The following fields are added to `proposed_changes[]` by the Process Analyst [TB] (Build Transformation Blueprint) capability. All are optional — backward compatible with SSADs that have not been through the blueprint pass.

- `proposed_changes[].phase` — integer phase number (1, 2, or 3). Assigned by TB based on `payback_tag`.
- `proposed_changes[].phase_label` — human-readable phase label (e.g., "Quick Wins (Weeks 1-4)").
- `proposed_changes[].sequence_order` — integer ordering within the phase. No-dependency changes first, then by highest value descending.
- `proposed_changes[].depends_on` — array of `change_id` strings that must complete before this change can start. Derived from step-level overlaps.
- `proposed_changes[].future_step_description` — what the affected step looks like after this change is implemented. Used by the generator for the "Future State" column.
- `proposed_changes[].future_step_owner` — who owns the step after the change (may differ from current owner if automation takes over).
- `proposed_changes[].future_step_tools` — array of tool name strings used in the future state.
- `proposed_changes[].future_step_type` — `"step"` (standard post-change step), `"automation"` (fully automated), or `"eliminated"` (step removed entirely). Drives rendering in the transformation blueprint.

### Analyst Metadata (top-level)

```json
{
  "analyst_metadata": {
    "last_analysis_run": "2026-03-22T14:30:00Z",
    "total_runs": 3,
    "changes_researched": 8,
    "changes_with_gaps": 2,
    "new_opportunities_generated": 4
  }
}
```

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
