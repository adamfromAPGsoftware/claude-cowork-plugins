# Audit Pipeline

Shared pipeline config loaded by all agents on activation. Provides cross-agent awareness of the full workflow.

## Plugin Split

| Plugin | Skills | CRM Entity | Purpose |
|--------|--------|------------|---------|
| **sales-plugin** | 1-call-prep, 2-sales-closer | Lead (+ Contact) | Pre/post discovery, sales pipeline |
| **audit-plugin** | 3-audit-extractor, 4-improvement-researcher, 5-deliverable-builder, 6-solution-designer | Project (+ Tasks) | Audit extraction, analysis, deliverables, solution design |

## CRM Integration

Every skill run updates the corresponding CRM entity. See `references/crm-integration.md` in each plugin for full details.

- **Skills 1-2** -> update CRM lead stages and add lead comments
- **Skills 3-6** -> update CRM project tasks and add task comments
- **Data flow**: one-way, local files -> CRM. CRM IDs stored in `crm` block of audit-data.json / prospect-profile.json
- **Best-effort**: CRM failures never block the pipeline

## Central Pricing

All cost calculations, tier assignments, and build estimates MUST reference:
**`{project-root}/audit-plugin/references/pricing.md`** — single source of truth for pricing.

## Agents & Capabilities

| Agent | Code | Capability | Description | Runs When | CRM Update |
|-------|------|------------|-------------|-----------|------------|
| 1. Call Prep | NC | new-client | Create client, find/create CRM contact + lead | New prospect | Contact + Lead lookup/create |
| 1. Call Prep | RC | research-client | Research prospect website + industry | Before call | Lead -> "Contacted" + comment |
| 1. Call Prep | AT | analyze-transcript | Extract buying signals from phone transcript | After phone call | Lead comment (buying intent) |
| 1. Call Prep | BC | build-battle-card | CLOSER framework call prep | Before discovery | Lead comment (battle card summary) |
| 2. Sales Closer | GDP | generate-discovery-page | Pre-call: research competitors, generate discovery page | Pre-call | Lead -> "Discovery Call - Scheduled" |
| 2. Sales Closer | GCP | generate-close-page | Post-call: analyse transcript, update discovery page with real findings | Post-call | Lead -> "Discovery Call - Completed" + value |
| 2. Sales Closer | GFE | generate-followup-comms | Post-call: follow-up email and SMS | Post-call | Lead -> "Negotiation" + comment |
| 3. Audit Extractor | SU | sync-and-update | Sync transcripts + extract into audit-data.json | After every session | Project lookup/create, task board seed, task comments |
| 3. Audit Extractor | AC | audit-check | Completeness + contradiction diagnostics | On demand | — |
| 3. Audit Extractor | GQ | generate-questions | Deliverable readiness, questions, email export | After SU | — |
| 4. Improvement Researcher | EI | extract-improvements | Synthesise proposed_changes[] from audit data | audit_status = process_map_complete | Task "EI" -> Done |
| 4. Improvement Researcher | RI | research-improvements | Per-change tool research + generate new opportunities | After EI | Task "RI" -> Done |
| 4. Improvement Researcher | SA | build-strategic-approaches | SaaS implementation strategies | After RI | Task "SA" -> Done |
| 4. Improvement Researcher | BR | build-and-rate | Estimate weeks, calculate value, write modal content | After SA | Task "BR" -> Done |
| 4. Improvement Researcher | VR | verify-research | Multi-agent verification of strategic approaches | After BR | Task "VR" -> Done |
| 4. Improvement Researcher | TB | build-transformation-blueprint | Phases, sequencing, future-state descriptions | After client selects approach | Task "TB" -> Done |
| 5. Deliverable Builder | GP | generate-process-map | process-map.html | After SU | Task comment |
| 5. Deliverable Builder | GF | generate-findings | findings.html | After SU | Task comment |
| 5. Deliverable Builder | GV | generate-waste | waste.html | After waste items identified | Task comment |
| 5. Deliverable Builder | GS | generate-solutions-overview | solutions-overview.html | After Researcher [RI] | Task comment |
| 5. Deliverable Builder | GA | generate-strategic-approaches | strategic-approaches.html | After Researcher [SA] | Task comment |
| 5. Deliverable Builder | GT | generate-transformation-blueprint | transformation-blueprint.html | After TB | Task comment |
| 5. Deliverable Builder | GM | generate-priority-matrix | priority-matrix.html | After TB | Task "Deliverables" -> Done |
| 5. Deliverable Builder | GW | generate-website | client-website.html (progressive unlock) | After any update | Task comment |
| 6. Solution Designer | RE | extract-requirements | Internal requirements spec | After VR | Task "RE" -> Done |
| 6. Solution Designer | BA | build-architecture | Architecture documentation (custom build alternative) | After RE | Task "BA" -> Done |
| 6. Solution Designer | BP | build-prototype | Clickable HTML prototype (custom build demo) | After BA | Task "BP" -> Done |

## Pipeline Flow

```
PRE-CALL
  Sales Closer [GDP] -> competitor research -> discovery page (shown on call)

POST-CALL
  Sales Closer [GCP] -> analyse transcript -> update discovery page with real findings
  Sales Closer [GFE] -> follow-up email + SMS

SESSIONS 1-N  (repeat after each meeting)
  Extractor [SU] -> sync + extract into audit-data.json
  Extractor [GQ] -> audit readiness, questions, email
  Builder        -> process-map.html, findings.html, waste.html, client-website.html

PROCESS MAP COMPLETE  (audit_status = "process_map_complete")
  Researcher [EI] -> synthesise proposed_changes[] from pain points + optimisations + waste
  Researcher [RI] -> per-change tool research + generate new opportunities
  Builder [GS] -> solutions-overview.html
  Researcher [SA] -> SaaS implementation strategies
  Builder [GA] -> strategic-approaches.html
  Researcher [BR] -> estimate weeks, calculate value, write modal content
  Researcher [VR] -> multi-agent verification of strategic approaches
  Solution Designer [RE] -> extract requirements (internal)
  Solution Designer [BA] -> architecture documentation (custom build alternative)
  Solution Designer [BP] -> clickable prototype (custom build demo)

PRESENTATION
  Compare SaaS strategies vs custom build prototype

CLIENT SELECTS APPROACH
  Researcher [TB] -> phases, sequencing, future-state descriptions
  Builder [GT] -> transformation-blueprint.html
  Builder [GM] -> priority-matrix.html
  Builder [GW] -> client-website.html (unlocked)

CONVERSION
  -> SOW generation from requirements_spec
```

## Recommended Next Steps

Use this table when an agent finishes and the user asks "what's next?":

| Just finished | Recommend next |
|---------------|----------------|
| Sales Closer [GFE] | Follow up nurture sequence |
| Extractor [SU] | Extractor [GQ] then Builder [GP] + [GF] + [GV] + [GW] |
| Extractor [GQ] | Another session OR mark audit_status = process_map_complete |
| Researcher [EI] | Researcher [RI] |
| Researcher [RI] | Builder [GS] then Researcher [SA] |
| Researcher [SA] | Builder [GA] then Researcher [BR] |
| Researcher [BR] | Researcher [VR] |
| Researcher [VR] | Solution Designer [RE] |
| Solution Designer [RE] | Solution Designer [BA] then [BP] |
| Solution Designer [BP] | Presentation meeting |
| Presentation | Researcher [TB] |
| Researcher [TB] | Builder [GT] + [GM] + [GW] |

## Data Contracts

| From | To | What travels |
|------|----|-------------|
| Extractor -> Researcher | audit-data.json | processes[], tools[], pain_points[], optimisations[], waste_items[] |
| Researcher [EI] -> [RI] | audit-data.json | proposed_changes[] (source: client), roi_items[] |
| Researcher [RI] -> [SA] | audit-data.json | proposed_changes[].research, new proposed_changes[] (source: analyst) |
| Researcher [SA] -> Builder [GA] | audit-data.json | strategic_approaches{} |
| Researcher [BR] -> [VR] | audit-data.json | proposed_changes[].implementation, .value, .modal_content |
| Researcher [VR] -> Solution Designer [RE] | audit-data.json | proposed_changes[], strategic_approaches{} (verified) |
| Solution Designer [RE] -> [BA] -> [BP] | audit-data.json | requirements_spec{}, architecture_doc{}, prototype |
| Researcher [TB] -> Builder | audit-data.json | proposed_changes[].phase/sequence, transformation_blueprint{} |
