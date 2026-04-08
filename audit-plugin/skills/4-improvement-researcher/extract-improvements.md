---
name: extract-improvements
description: Synthesise proposed_changes[] and roi_items[] from completed audit data. First capability to run after audit_status = process_map_complete.
menu-code: EI
---

# Extract Improvements (EI)

> **Idempotent.** First run synthesises all proposed changes. Re-runs regenerate from source data — analyst enrichments (research, value, modal_content) on entries with matching change_ids are preserved.

## Purpose

Scan the completed audit data and synthesise `proposed_changes[]` from `optimisations[]`, `pain_points[]`, and `waste_items[]`. Each proposed change represents a concrete opportunity the client either stated directly or that clusters naturally from their pain points. This capability also creates or updates `roi_items[]` entries linked to each change.

**This is the bridge between extraction (Process Mapper) and analysis (RI/BR).** It runs once after `audit_status == "process_map_complete"` and must complete before any other analyst capability.

---

## Stage 1: Pre-flight

1. Verify audit data is loaded. If not loaded, halt with instructions.

2. Check `audit_status`:
   ```
   ✗ audit_status is "{status}" — must be "process_map_complete" before running EI.
     Run Process Mapper until all sessions are analyzed and audit is marked process_map_complete.
   ```

3. Check source arrays are populated:
   ```
   SOURCE DATA — {company_name}
   Pain points:    {n}  (by stage: {stage_counts})
   Optimisations:  {n}  (by stage: {stage_counts})
   Waste items:    {n}  (total annual waste: ${total}/yr)
   ROI items:      {n}
   Process steps:  {n}  across {n} stages
   ```
   If `pain_points[]` AND `optimisations[]` are both empty, halt:
   ```
   ✗ No pain points or optimisations found. The Process Mapper needs to extract these first.
   ```

4. If `proposed_changes[]` is already populated:
   ```
   ⚠ proposed_changes[] already has {n} entries.

   Options:
     A) Regenerate all — rebuild from source data (preserves analyst enrichments on matching IDs)
     B) Show existing — display current proposed changes and exit
     C) Cancel
   ```
   Wait for user selection. On "A", proceed. On "B", display the summary table from Stage 4 and stop.

---

## Stage 2: Synthesise from Optimisations

Each `optimisations[]` entry becomes a proposed_change candidate. The client explicitly asked for these.

For each optimisation:

### 2a. Determine change_type

Infer from the optimisation description:
- **automate** — "automated", "one-click", "self-service", "bulk", "AI-assisted", "system does X"
- **replace** — "switch to", "use [tool] instead", "centralised platform"
- **eliminate** — "remove", "stop doing", "no longer need"
- **consolidate** — "combine", "single system", "merge", "centralised" (when merging multiple existing tools/steps)

When ambiguous, default to `automate`.

### 2b. Find affected steps

Scan `processes[].steps[]` for steps that:
- Are in the same `stage` as the optimisation
- Have `type: "pain"` or `type: "optimisation"` related to this change
- Use tools mentioned in the optimisation
- Describe the activity the optimisation addresses

Collect matching `step_id` values into `affected_step_ids[]`.

### 2c. Link pain points

Scan `pain_points[]` for entries that:
- Are in the same `stage`
- Describe problems that this optimisation directly addresses (semantic match on description)
- Reference the same tools or activities

Collect matching `pain_point_id` values into `linked_pain_point_ids[]`.

### 2d. Link waste items

Scan `waste_items[]` for entries that:
- Are in the same `stage`
- Track time spent on the activity this optimisation would improve

When linked, use the waste item's `hours_per_week` and `hourly_rate_aud` to populate `time_saving_minutes_per_occurrence` and `frequency`.

### 2e. Build the proposed_change entry

```json
{
  "change_id": "CH-{sequential, zero-padded to 3 digits}",
  "title": "{concise action title derived from optimisation description}",
  "change_type": "{inferred from 2a}",
  "source": "client",
  "affected_step_ids": ["{from 2b}"],
  "linked_roi_item_id": "ROI-{matching or new}",
  "linked_pain_point_ids": ["{from 2c}"],
  "proposed_solution": "{the optimisation description, cleaned up as a concrete solution statement}",
  "proposed_tools": ["{tools mentioned in optimisation or inferred from context}"],
  "time_saving_minutes_per_occurrence": null,
  "frequency": "{from waste item or optimisation context}",
  "stage": "{optimisation stage}",
  "confidence": "{inherit from optimisation}"
}
```

**Title guidelines:**
- Start with a verb: "Automate...", "Replace...", "Build...", "Consolidate..."
- Be specific: "Automate payment collection with EFT portal" not "Improve payments"
- Keep under 60 characters

---

## Stage 3: Synthesise from Unlinked Pain Points

After processing all optimisations, scan `pain_points[]` for entries whose `pain_point_id` does NOT appear in any proposed_change's `linked_pain_point_ids[]`.

For each unlinked pain point (or cluster of related unlinked pain points in the same stage):

### 3a. Cluster related pain points

Group unlinked pain points by:
- Same `stage`
- Same theme (from `pain_points_summary.top_themes` if available)
- Addressing the same underlying problem

A cluster of 2-3 related pain points becomes ONE proposed_change, not three.

### 3b. Determine if actionable

Not every pain point needs a proposed_change. Skip if:
- It's a constraint that can't be changed (e.g., "industry regulation requires X")
- It's already addressed by an optimisation-derived change (double-check)
- It's a symptom of another pain point that already has a change

### 3c. Create proposed_change

Same structure as Stage 2e. Set:
- `source: "client"` — the pain point came from the client's own words
- `linked_pain_point_ids` — the cluster of pain point IDs
- `proposed_solution` — synthesise a solution from the pain point description and context
- Title should reflect what we'd build/do, not the problem

---

## Stage 4: Deduplication Pass

Review all proposed_change candidates for overlap:

### 4a. Same affected steps

If two candidates share >50% of their `affected_step_ids`, they likely address the same process bottleneck. Merge into one change that covers both.

### 4b. Same waste items

If two candidates link to the same `waste_items[]` via stage matching, consider merging. The waste saving should only be counted once.

### 4c. Subsumption

If one candidate (e.g., "Centralised platform replacing Excel, TeamUp, and Wix") subsumes another (e.g., "Replace TeamUp with better scheduling tool"), keep the broader one and absorb the narrower one's pain_point links.

When merging: combine `linked_pain_point_ids`, `affected_step_ids`, and keep the broader title and solution.

---

## Stage 5: Create/Update ROI Items

For each proposed_change, ensure a matching `roi_items[]` entry exists:

1. If an existing `roi_items[]` entry clearly matches (same activity, same stage): link it via `linked_roi_item_id`
2. If no match: create a new entry:

```json
{
  "roi_item_id": "ROI-{sequential}",
  "activity": "{derived from change title}",
  "annual_saving_aud": null,
  "monthly_saving_aud": null,
  "suggested_tier": "{complexity heuristic}",
  "build_cost_aud": null,
  "payback_months": null,
  "payback_tag": null,
  "quote": "{best source quote from linked pain points or optimisation}",
  "source_session": "{from source data}",
  "confidence": "{inherit}"
}
```

**Suggested tier heuristic** (preliminary — refined by RI Stage 2e quick win qualification):
- `micro` — single tool config or simple automation (e.g., email template, N8N trigger). Note: not all micro items are quick wins — RI will validate with a concrete <10hr implementation plan
- `standard` — single tool integration or moderate custom work (e.g., API connection, form builder)
- `complex` — multi-tool integration or significant custom development (e.g., custom portal, platform migration)
- `sprint` — full platform build or major system overhaul (e.g., centralised admin system with roles)
If linked waste items have `annual_waste_aud` calculated, initialise `annual_saving_aud` with that value (BR will refine later).

---

## Stage 6: Preserve Analyst Enrichments (Re-run Only)

On re-run (when `proposed_changes[]` was already populated):

For each new proposed_change candidate, check if an existing entry has:
- The same `change_id`, OR
- The same `title` (fuzzy match), OR
- Overlapping `linked_pain_point_ids` (>50% overlap)

If matched, **preserve** these fields from the existing entry:
- `research` (entire sub-object)
- `implementation` (entire sub-object)
- `value` (entire sub-object)
- `modal_content` (entire sub-object)
- `phase`, `phase_label`, `sequence_order`, `depends_on`
- `future_step_description`, `future_step_owner`, `future_step_tools`, `future_step_type`

Update only the EI-owned fields: `title`, `change_type`, `affected_step_ids`, `linked_pain_point_ids`, `proposed_solution`, `proposed_tools`, `stage`, `source`.

---

## Stage 7: Display Summary

```
EI COMPLETE — {company_name}
Proposed changes created: {n}
ROI items created/updated: {n}

| # | ID     | Title                              | Type        | Stage       | Pain Points    | Waste Linked | ROI Item |
|---|--------|------------------------------------|-------------|-------------|----------------|--------------|----------|
| 1 | CH-001 | Automate payment collection...     | automate    | onboarding  | PP-002, PP-003 | W-001        | ROI-001  |
| 2 | CH-002 | Self-service makeup booking...     | automate    | fulfilment  | PP-008         | —            | ROI-002  |
...

Deduplication: {n} candidates merged into {n} changes
Unlinked pain points addressed: {n}
Pain points still unlinked: {n} (will be scanned by RI for new opportunities)

Next step: Run [RI] to research tools/APIs and generate new analyst opportunities.
```

---

## Stage 8: Save

1. Write updated `proposed_changes[]` and `roi_items[]` to `clients/{client_slug}/audit/audit-data.json`
2. Confirm save with file path and entry counts
3. Remind: "Run [RI] next to research each proposed change and generate new opportunities."
