---
name: build-transformation-blueprint
description: After client selects their approach (SaaS strategy or custom build), assign phases, sequence proposed changes, and write future-state step descriptions for the transformation blueprint deliverable.
menu-code: TB
---

# Build Transformation Blueprint (TB)

> **Idempotent.** First run creates everything. Re-runs update phases, sequences, and future-state descriptions.

## Purpose

After the client selects their approach (a SaaS strategy or custom build), group proposed changes into implementation phases, establish dependencies and sequencing, and write the future-state step descriptions that the generator uses to render the "Future State" column of the transformation blueprint.

**Requires:** `proposed_changes[]` with `implementation` and `value` sub-objects populated (run [BR] first). Client must have selected their approach.

---

## Stage 1: Pre-flight

1. Check audit data is loaded and `proposed_changes[]` is populated.

2. Scan for readiness:
   ```
   BLUEPRINT STATUS — {company_name}
   Total proposed changes: {n}
     with implementation + value: {n} — ready for blueprint
     missing implementation:       {n} — run BR first
     missing value:                {n} — run BR first
   ```

3. If any changes lack `implementation` or `value`, warn but proceed with available changes.

---

## Stage 1.5: Approach Selection

The blueprint runs AFTER the client has selected their approach. It must be built against a specific approach so that tool names, costs, and rationale are consistent throughout.

1. Check if `strategic_approaches.selected_approach` exists in audit data.

2. If **set**: load the approach and confirm with the user:
   ```
   Selected approach: {approach_type} — {details}
   Proceeding with this approach's tool references.
   ```

3. If **not set**: ask the user which approach the client selected:
   ```
   APPROACH SELECTION REQUIRED

   Which approach did the client select?

     A) A SaaS strategy — specify which:
        1. use-what-you-have
        2. best-of-breed-saas
        3. smart-saas-mix
     B) Custom build (Solution Designer architecture)

   Enter selection (A1, A2, A3, or B):
   ```

4. Write the selection to `strategic_approaches.selected_approach` in audit data:
   ```json
   {
     "selected_approach": {
       "type": "saas_strategy",
       "strategy_id": "best-of-breed-saas"
     }
   }
   ```
   or:
   ```json
   {
     "selected_approach": {
       "type": "custom_build"
     }
   }
   ```

5. Build the tool lookup map based on approach type:

   **If SaaS strategy:** Build `strategy_tools[change_id] → selected_tool` from the chosen strategy's `tool_selections[]`. Also note `uncovered_changes[]` — these have no tool in this strategy.

   **If custom build:** Build `strategy_tools[change_id] → module_name` from `architecture_doc.modules[]` or `architecture_doc.module_inventory[]`. Map each proposed change to the architecture module that covers it. For changes not covered by a custom module, fall back to `research.tools_researched[]` recommendations.

---

## Stage 2: Phase Assignment

Assign each proposed change to a phase using `payback_tag` from `roi_items[]`:

| payback_tag  | Phase | Label                  |
|-------------|-------|------------------------|
| QUICK_WIN   | 1     | Quick Wins             |
| CORE_BUILD  | 2     | Core Build             |
| FUTURE      | 3     | Future                 |

For changes without a linked roi_item or payback_tag, use `weeks_estimate`:
- `< 2 weeks` → Phase 1
- `2-4 weeks` → Phase 2
- `> 4 weeks` → Phase 3

Calculate timeframes for each phase:
- Sum `weeks_estimate` across changes in the phase
- Phase 1 timeframe starts at Week 1
- Phase 2 starts after Phase 1 ends
- Phase 3 starts after Phase 2 ends
- Format as "Weeks X-Y"

Write `phase` and `phase_label` on each proposed_change.

---

## Stage 3: Dependency Analysis

For each proposed change, scan for dependencies:

1. **Step-level overlap:** If change B affects a step_id that appears later in the same stage's step sequence than a step_id affected by change A, mark B as potentially depending on A.

2. **Tool dependency:** If change B requires a tool upgrade that change A provides (e.g., A upgrades HubSpot plan, B uses HubSpot Sequences), mark B as depending on A.

3. **Logical dependency:** If change A eliminates a step that change B's proposed solution references or builds upon, mark A as depending on B (or vice versa).

Populate `depends_on` array with the change_ids of dependencies.

Reorder `sequence_order` within each phase:
- Changes with no dependencies first
- Then by highest `combined_annual_value_aud` descending
- Number sequentially starting from 1 within each phase

---

## Stage 4: Future-State Descriptions

For each proposed change, derive the future-state step.

### Tool Resolution (do this first for every change)

Before writing any future-state fields, resolve the specific tool name for this change:

1. Look up `change_id` in the `strategy_tools` map built in Stage 1.5.
2. If found: use the strategy's `selected_tool` as the primary tool name.
3. If the change is in `uncovered_changes[]`: use the recommended tool from `research.tools_researched[]` (where `is_recommended: true`), or fall back to `proposed_tools[]`.
4. **Update `proposed_tools[]`** on the change to match the resolved tool name(s). This ensures all downstream generators have specific, named tools — never generic descriptions.

**CRITICAL — No Generic Tool Names:**
- NEVER write `"scheduling platform"`, `"rostering tool"`, `"CRM system"`, `"automation platform"`, `"SMS API integration"` or similar generic descriptions into `future_step_tools[]` or `proposed_tools[]`.
- Every tool must be a specific named product or custom module name: `"RotaWiz"`, `"HubSpot CRM"`, `"Xero"`, `"Cellcast SMS"`, `"Roster Module"`, `"Client Portal"`, etc.
- If you cannot resolve a specific tool name, flag it as a gap and ask the user — do not proceed with a generic placeholder.

### By change_type:

**automate:**
- `future_step_type`: `"automation"`
- `future_step_description`: Describe the automated version. Start with "Automated: " and explain what happens automatically. **Name the specific tool** (e.g., "Automated: RotaWiz generates optimised rosters based on participant preferences and staff availability").
- `future_step_owner`: Set to the automation tool name (e.g., "RotaWiz", "HubSpot Sequences") or "Automated"
- `future_step_tools`: Array of specific tool names that perform the automation

**replace:**
- `future_step_type`: `"step"`
- `future_step_description`: Describe the new tool/method. **Name the specific replacement tool** (e.g., "Staff availability collected via Google Forms weekly, auto-synced to RotaWiz scheduling engine").
- `future_step_owner`: Keep current owner unless the replacement changes who performs it
- `future_step_tools`: Array of specific new tool names

**eliminate:**
- `future_step_type`: `"eliminated"`
- `future_step_description`: Brief reason for elimination (e.g., "No longer needed — handled by HubSpot automation in CH-003")
- `future_step_owner`: empty string
- `future_step_tools`: empty array

**consolidate:**
- `future_step_type`: `"step"`
- `future_step_description`: Use `proposed_step_description` from the change. This describes the merged result.
- `future_step_owner`: Keep primary owner from the original steps
- `future_step_tools`: Combine tools from merged steps + any new tools

### Writing guidelines:
- **Always name the specific tool** — never use generic descriptions like "the new platform" or "scheduling tool"
- Use the client's actual names, tools, and terminology
- Keep descriptions concise (1-2 sentences)
- Reference the specific automation or tool that replaces the manual process
- For consolidated steps, make clear what was merged

---

## Stage 5: Build Blueprint Metadata

Create/update the top-level `transformation_blueprint` object:

```json
{
  "transformation_blueprint": {
    "selected_approach": "{the approach object from Stage 1.5}",
    "approach_narrative": "{2-3 sentence explanation — see below}",
    "phases": [
      {
        "phase_number": 1,
        "label": "Quick Wins",
        "timeframe": "Weeks 1-{n}",
        "description": "{brief description of what this phase achieves}",
        "change_ids": ["CH-001", "CH-003"]
      }
    ],
    "total_phases": 3,
    "estimated_total_weeks": "{sum of all phase weeks}",
    "total_steps_current": "{count of all process steps}",
    "total_steps_future": "{current steps minus eliminated, minus consolidated duplicates}",
    "total_annual_value_aud": "{sum of combined_annual_value_aud}",
    "last_built": "{ISO timestamp}"
  }
}

### Approach Narrative

Write `approach_narrative` as a client-facing paragraph (2-3 sentences) that explains:
1. **Which approach was selected** — name the strategy or "custom build"
2. **Why it suits this client** — reference the approach's strengths and the client's situation
3. **What it means practically** — briefly describe the key tools/modules and any gaps

**If SaaS strategy:** Compose from the selected strategy's `name`, `best_for`, `cost_summary`, and `uncovered_changes[]`.

Example: "We've built this roadmap around the 'Use What You Have' approach — reconfiguring your existing Google Workspace and Xero tools to deliver $153K/yr in savings with zero new software spend. Three higher-value opportunities (scheduling engine, shift notifications, and AI reports) sit outside this approach and would require a specialist tool like RotaWiz."

**If custom build:** Compose from `architecture_doc.modules[]` / `architecture_doc.module_inventory[]`, referencing the platform architecture and any SaaS tools retained alongside custom modules.

Example: "We've built this roadmap around a custom platform — purpose-built modules for rostering, client management, and compliance reporting, hosted on AU infrastructure with a flat monthly fee. Your existing Xero integration is retained for invoicing, while the custom scheduling engine replaces three manual processes."
```

Phase descriptions should be 1 sentence summarising the theme:
- Phase 1: "Low-effort, high-value changes that deliver immediate time savings"
- Phase 2: "Core infrastructure and integration builds that enable advanced automation"
- Phase 3: "AI enablement and complex workflow transformations for long-term productivity gains"

Adjust descriptions based on the actual changes in each phase.

---

## Stage 6: Display Summary

```
TRANSFORMATION BLUEPRINT BUILT — {company_name}

Phase 1 — Quick Wins ({timeframe}):
  {n} changes | ${total_value}/yr | ~{weeks} weeks
  {list change titles}

Phase 2 — Core Build ({timeframe}):
  {n} changes | ${total_value}/yr | ~{weeks} weeks
  {list change titles}

Phase 3 — Future ({timeframe}):
  {n} changes | ${total_value}/yr | ~{weeks} weeks
  {list change titles}

Summary:
  Total annual value: ${total}/yr
  Steps: {current} → {future} ({eliminated} eliminated, {consolidated} consolidated)
  Estimated timeline: {total_weeks} weeks across {phases} phases
  Dependencies identified: {n}

Next step: Run Generator [GT] to create transformation-blueprint.html
```

---

## Stage 7: Save

1. Write updated `proposed_changes[]` with phase/sequence/future-state fields to audit data
2. Write `transformation_blueprint` top-level object to audit data
3. Update `analyst_metadata.last_analysis_run`
4. Confirm save
