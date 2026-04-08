# Audit Pipeline — Complete Reference

This document explains the full audit pipeline end-to-end: from pre-engagement discovery through to client conversion.

## 1. Pipeline Overview

The audit is a structured process for mapping a client's business operations, identifying waste, and proposing improvements with clear ROI. The pipeline runs through six phases:

1. **Pre-Engagement** — Research the prospect, run a discovery call, generate a close page
2. **Sessions** — 1-3 meetings to map their processes, extract pain points, quantify waste
3. **Process Map Complete** — Synthesise proposed changes, research tools, estimate value
4. **Presentation** — Walk through the interactive priority matrix with the client
5. **Post-Presentation** — Extract requirements, build architecture, generate prototype
6. **Conversion** — Present prototype to close the deal

## 2. Agents

### Pre-Discovery Agent
**Skill:** `bmad-apg-pre-discovery`
**When:** Before first contact with a prospect
**Does:** Researches the prospect's company, analyses phone transcripts, builds battle cards for the discovery call.

### Close Agent
**Skill:** `bmad-apg-agent-close`
**When:** Pre-engagement, after a discovery call
**Does:** Processes discovery call transcripts, generates `audit-data-lite.json`, produces `close-page.html` and follow-up emails.

### Process Mapper
**Skill:** `bmad-apg-process-mapper`
**When:** After every audit session (meeting)
**Does:** Extracts structured process documentation from transcripts into `audit-data.json`. Every step, tool, time cost, pain point, and decision node is captured from what was actually said. Never invents or researches.

**Capabilities:**
| Code | Name | Purpose |
|------|------|---------|
| SU | sync-and-update | Fetch new Fathom meetings, extract all data into audit-data.json |
| AC | audit-check | Re-run completeness and contradiction checks |
| GQ | generate-questions | Audit readiness, generate/research follow-up questions, export email |
| SM | save-memory | Persist session progress |

### Process Analyst
**Skill:** `bmad-apg-process-analyst`
**When:** After `audit_status = "process_map_complete"`
**Does:** Synthesises proposed changes from audit data, researches tools/APIs, estimates implementation effort, calculates value with visible formulas, writes client-facing modal content.

**Capabilities:**
| Code | Name | Purpose |
|------|------|---------|
| EI | extract-improvements | Synthesise proposed_changes[] from pain points + optimisations + waste |
| RI | research-improvements | Per-change tool research + generate new analyst opportunities |
| SA | build-strategic-approaches | Holistic process-wide tool strategy with deep research |
| BR | build-and-rate | Estimate weeks, calculate value, write modal content |
| GR | gap-review | Read-only gap scan, recommend re-runs |
| TB | build-transformation-blueprint | Assign phases, sequence, write future-state descriptions |
| SM | save-memory | Persist session progress |

### Generator
**Skill:** `bmad-apg-agent-generator`
**When:** After data updates (progressive generation)
**Does:** Generates self-contained HTML deliverables from audit-data.json. Script-driven — agent validates, script produces HTML.

**Capabilities:**
| Code | Name | Output |
|------|------|--------|
| GW | generate-website | client-website.html |
| GP | generate-process-map | process-map.html |
| GF | generate-findings | findings.html |
| GV | generate-waste | waste.html |
| GS | generate-solutions-overview | solutions-overview.html |
| GA | generate-strategic-approaches | strategic-approaches.html |
| GT | generate-transformation-blueprint | transformation-blueprint.html |
| GM | generate-priority-matrix | priority-matrix.html |
| GR | generate-report | audit-report.html (internal) |

### Solution Architect
**Skill:** `bmad-apg-solution-architect`
**When:** Post-presentation, after client has seen the priority matrix
**Does:** Extracts technical requirements, builds architecture documentation, and generates clickable prototypes for client conversion.

**Capabilities:**
| Code | Name | Purpose |
|------|------|---------|
| RE | extract-requirements | Internal requirements spec (screens, roles, data model) |
| BA | build-architecture | Architecture documentation (user journeys, data models, access policies) |
| BP | build-prototype | Clickable HTML prototype from architecture |
| SM | save-memory | Persist session progress |

## 3. Data Flow

All agents read from and write to a single source of truth: `clients/{client_slug}/audit/audit-data.json`.

### How the data evolves:

**After Mapper [SU]:**
- `processes[]` — stage-based workflow steps with quotes and citations
- `tools[]` — software/services with use cases and workarounds
- `pain_points[]` — problems with verbatim quotes
- `optimisations[]` — client-stated improvement wishes
- `waste_items[]` — quantified cost of inefficiencies (hours/week, annual cost)
- `sessions[]` — meeting metadata with Fathom links

**After Analyst [EI]:**
- `proposed_changes[]` — concrete improvement opportunities with change_type, affected_step_ids, linked pain points
- `roi_items[]` — ROI entries linked to each proposed change

**After Analyst [RI]:**
- `proposed_changes[].research` — tool pricing, API docs, feasibility, risks, gaps
- New `proposed_changes[]` entries with `source: "analyst"` (new opportunities)

**After Analyst [BR]:**
- `proposed_changes[].implementation` — weeks_estimate, dev_hours, pm_hours
- `proposed_changes[].value` — annual_saving_aud with visible formulas
- `proposed_changes[].modal_content` — 5 client-facing sections for priority matrix modals
- `roi_items[]` updated with payback_months, payback_tag

**After Analyst [SA]:**
- `strategic_approaches{}` — 4 pre-built strategies with tool selections, integration analysis, deep-dive research, and cost summaries

**After Analyst [TB]:**
- `proposed_changes[].phase` — phase assignment (1=Quick Wins, 2=Core Build, 3=Future)
- `proposed_changes[].future_step_*` — future-state descriptions
- `transformation_blueprint{}` — phase groupings and summary metrics

**After Solution Architect [RE]:**
- `requirements_spec{}` — functional requirements, user roles, screen inventory, data model, integrations

## 4. Client Folder Structure

```
clients/{client_slug}/
  audit/                      ← audit-data.json (single source of truth)
  meetings/                   ← Fathom-fetched transcripts + metadata
  client-provided-materials/  ← emails, PDFs, forwarded docs
  deliverables/               ← generated HTML files
  follow-up-emails/           ← outbound email drafts
```

## 5. Deliverables

| File | Generated by | Description | When |
|------|-------------|-------------|------|
| `process-map.html` | Generator [GP] | Zone-based current-state process map with waste heatmap | After each session |
| `findings.html` | Generator [GA] | "What We Discussed" session summary | After each session |
| `waste.html` | Generator [GA] | "Total Waste Identified" breakdown | After each session |
| `client-website.html` | Generator [GW] | Progressive client portal with session unlocks | After each session |
| `solutions-overview.html` | Generator [GS] | Researched automation/integration options per opportunity | After Analyst [RI] |
| `strategic-approaches.html` | Generator [GA] | Four holistic implementation strategies | After Analyst [SA] |
| `transformation-blueprint.html` | Generator [GT] | Side-by-side current vs future state | After Analyst [TB] |
| `priority-matrix.html` | Generator [GM] | Interactive bubble chart with clickable modals | After Analyst [TB] |
| `audit-report.html` | Generator [GR] | Internal working document | On demand |

## 6. Running the Pipeline — Step by Step

### New Client Setup
1. Run **Pre-Discovery** agent to research the prospect
2. After discovery call: Run **Close** agent to generate close-page.html + follow-up email
3. Create client folder: `clients/{company-slug}/` with standard subdirectories

### Session 1
1. Run **Mapper [SU]** — syncs Fathom transcript, extracts into audit-data.json
2. Run **Mapper [GQ]** — generates follow-up questions, exports email
3. Run **Generator [GP] + [GW]** — generates process-map.html and client-website.html

### Sessions 2-3 (repeat)
Same as Session 1. Each run enriches the existing audit-data.json.

### Process Map Complete
1. Mark `audit_status: "process_map_complete"` in audit-data.json
2. Run **Analyst [EI]** — synthesises proposed_changes[] from audit data
3. Run **Analyst [RI]** — per-change tool research, generates new opportunities
4. Run **Generator [GS]** — generates solutions-overview.html
5. Run **Analyst [SA]** — builds 4 holistic strategic approaches with deep tool research
6. Run **Generator [GA]** — generates strategic-approaches.html
7. Run **Analyst [BR]** — estimates weeks, calculates value, writes modal content
8. Run **Analyst [GR]** — checks for gaps, recommends re-runs if needed
9. Run **Analyst [TB]** — assigns phases, sequences, writes future-state descriptions
10. Run **Generator [GT] + [GM] + [GW]** — generates blueprint, priority-matrix, updates website

### Presentation
Walk the client through `priority-matrix.html`. Click bubbles to show modal content.

### Post-Presentation
1. Run **Solution Architect [RE]** — extracts requirements (internal)
2. Run **Solution Architect [BA]** — builds architecture documentation
3. Run **Solution Architect [BP]** — generates clickable prototype

### Conversion
Present prototype to client to close the deal.

## 7. Design Tokens (for HTML deliverables)

All HTML outputs use these consistent design tokens:
- **Primary accent:** `#7DFF00` (lime)
- **Dark background:** `#0f1825`
- **Light background:** `#f7f9fc`
- **Text on white:** `#166534` (dark green, 7.1:1 contrast)
- **Muted text:** `#64748b`
- **Font:** Inter (Google Fonts)
- **All deliverables are self-contained single HTML files** (no external dependencies beyond fonts)
