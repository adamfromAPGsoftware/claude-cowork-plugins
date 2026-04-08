---
name: verify-research
description: Multi-agent verification of strategic approaches (3 SaaS strategies). Spawns independent research agents that don't see the original tool picks, compares findings, and resolves disagreements. Replaces gap-review.
menu-code: VR
---

# Verify Research (VR)

> **Orchestration capability.** Spawns independent sub-agents to verify strategic approach research. Includes structural completeness checks (absorbed from former gap-review). Updates audit-data.json with verified findings.

## Purpose

The strategic approaches are the highest-value output of the analyst pipeline — they drive every downstream deliverable and the client presentation. A single research pass inherits whatever blind spots the model had in that context window. VR fixes this by running **3 independent verification passes** per strategy, each blind to the original tool selections, then comparing findings to surface disagreements, missed tools, and pricing errors.

**When to run:** After [SA] Build Strategic Approaches (and ideally after [BR] Build & Rate).

---

## Stage 1: Pre-flight & Structural Check

### 1a. Verify prerequisites

```
✗ strategic_approaches not found. Run [SA] Build Strategic Approaches first.
```

If `strategic_approaches` exists, continue.

### 1b. Structural completeness scan (absorbed from gap-review)

For each entry in `proposed_changes[]`, check:

| Check | Field | Status |
|-------|-------|--------|
| ID assigned? | `id` | present / missing |
| Research done? | `research.status` | complete / needs_review / in_progress / not_started / missing |
| Research gaps? | `research.gaps[]` | count of open gaps |
| Tools researched? | `research.tools_researched[]` | count (0 = not researched) |
| Weeks estimated? | `implementation.weeks_estimate` | present / missing |
| Value calculated? | `value.combined_annual_value_aud` | present / missing / $0 |
| Formula visible? | `value.formula_summary` | present / missing |
| Modal written? | `modal_content` (all sections) | present / missing |
| Meeting refs? | `modal_content.meeting_references[]` | count (0 = no transcript links) |
| Source type? | `source` | client / analyst / missing |
| RI field: requires_paid_plan? | `research.tools_researched[].requires_paid_plan` | present / missing |
| RI field: free_plan_limitations? | `research.tools_researched[].free_plan_limitations[]` | present / missing |
| RI field: realistic_tier? | `research.tools_researched[].realistic_tier` | present / missing |
| RI field: setup_cost_aud? | `research.tools_researched[].setup_cost_aud` | present / missing |
| RI field: data_silo_risk? | `research.tools_researched[].data_silo_risk` | present / missing |

### 1b-extra. Paid plan cost validation

For each `tools_researched[]` entry where `requires_paid_plan: true`, verify that the Best-of-Breed strategy uses `realistic_annual_cost_aud` — not the free tier cost. Flag any mismatches:

```
PAID PLAN COST CHECK
  Tool: {tool_name} | requires_paid_plan: true | realistic_tier: {tier}
  Best-of-Breed cost used: ${cost} | realistic_annual_cost_aud: ${realistic_cost}
  ✓ Match / ✗ MISMATCH — strategy is using free tier cost for a tool that needs paid
```

Display summary:

```
VR PRE-FLIGHT — {company_name}

STRUCTURAL CHECK
  Proposed changes: {n}
  ✓ Fully complete: {n}
  ⚠ Partial: {n}
  ✗ Missing fields: {list critical gaps}

STRATEGIC APPROACHES
  Generated: {generated_at}
  Run count: {run_count}
  Strategies: {n} ({list strategy names}) — expect 3 SaaS strategies
  Verification status: {not_verified | verified_at}
  RI field coverage: {n}/{total} tools_researched entries have all required fields

{If structural issues exist, list them but proceed — VR focuses on research quality, not field completeness.}
```

### 1c. Select verification scope

```
Verification scope:
  A) Full verification — all 3 strategies, 3 agents each (9 agent runs)
  B) Targeted — Strategy 1 (Use What You Have) + Strategy 2 (Best-of-Breed) only (6 agent runs)
  C) Single strategy — verify one specific strategy (3 agent runs)
```

Wait for user selection. Recommend **A** for most cases — all 3 strategies are SaaS-based and benefit from blind verification.

---

## Stage 2: Build Verification Briefs

For each strategy in scope, construct a **blind brief** — this is what the verification agents receive. The brief contains the PROBLEM but NOT the SA's tool selections.

### 2a. Extract company context

From audit data, extract (this is shared across all briefs):

```
COMPANY CONTEXT
- Company: {company_name}
- Industry: {industry_tag}
- Size: {contact.company_size}
- Current tools: {list tool_name + use_case from tools[], excluding cost/API details}
- Blended hourly rate: ${blended_hourly_rate_aud}/hr
- Key constraint: {any budget/preference constraints from sessions}
```

### 2b. Extract change briefs

For each proposed_change covered by the strategy, extract:

```
CHANGE: {title}
Problem: {description from linked pain_points — use quotes and speaker names}
Current process: {affected steps — what happens today}
Desired outcome: {proposed_solution — what the client wants}
Value type: {time_saving | productivity_enhancement | both}
Constraints: {any tool-specific requirements, e.g., "must handle NDIS ratio billing"}
```

**Do NOT include:** `research.tools_researched`, `selected_tool`, `rationale`, `integration_notes`, tool pricing, deep-dive data, or any SA output.

### 2c. Build strategy constraint brief

Each strategy has rules the verification agent must follow:

**Strategy 1 (Use What You Have):**
```
CONSTRAINT: Only recommend tools the company already uses or that are completely free.
Current tools: {list from 2a}
If no free option exists for a change, mark it as "uncovered" with a reason.
```

**Strategy 2 (Best-of-Breed SaaS):**
```
CONSTRAINT: Recommend the single best specialist tool for each change. 
Prioritise: value-for-money, integration with existing stack, AU/NDIS suitability.
Every change should be covered — there is always at least one tool option.
Do NOT recommend custom-built solutions.
For any tool where `requires_paid_plan: true`, use `realistic_annual_cost_aud` — not the free tier cost.
```

**Strategy 3 (Smart SaaS Mix):**
```
CONSTRAINT: Blend free/existing tools where they work well with best-of-breed paid tools 
where free options fall short. Optimise for cost-effectiveness and integration cohesion.
Do NOT recommend custom-built solutions.
For any tool where `requires_paid_plan: true`, use `realistic_annual_cost_aud` — not the free tier cost.
```

---

## Stage 3: Direct Verification Research

For each strategy in scope, run **3 independent verification passes directly** using WebSearch. Do NOT use sub-agents — perform all research in the main conversation to avoid freezing and rate-limit issues.

### Verification pass structure

For each pass, work through every change covered by the strategy:

1. **Search broadly** for the problem domain: `"best {use_case} software Australia {year}"`, `"NDIS {use_case} tool comparison"`
2. **Search specifically** for candidate tools: `"{tool_name} pricing {year}"`, `"{tool_name} NDIS disability Australia"`
3. **Record recommendation** with the same JSON structure per change:

```json
{
  "change_title": "string",
  "recommended_tool": "Specific Product Name (tier if relevant)",
  "rationale": "Why this tool is the best fit — 2-3 sentences",
  "annual_cost_aud": number,
  "per_user_monthly_aud": number or null,
  "pricing_source": "URL where you found pricing",
  "alternative_considered": "Another specific tool you evaluated and rejected, with reason",
  "integration_notes": "How this connects to the company's existing tools",
  "confidence": "HIGH|MEDIUM|LOW",
  "key_risk": "The biggest limitation or gotcha with this recommendation"
}
```

### Execution

1. For each strategy in scope, run 3 sequential verification passes
2. Each pass should use WebSearch to independently research every change — approach from a different search angle each time (e.g., pass 1: domain searches, pass 2: competitor comparisons, pass 3: NDIS-specific searches)
3. Between passes, do NOT review previous pass results — keep each pass blind
4. After all 3 passes complete, proceed to Stage 4

**IMPORTANT:** Never use the Agent tool for verification. All research runs directly in the main conversation using WebSearch/WebFetch.

---

## Stage 4: Cross-Comparison

For each strategy, compare the 3 verification results against the original SA output.

### 4a. Build agreement matrix

For each change in the strategy:

```
AGREEMENT MATRIX — {strategy_name}

| Change | SA Original | Agent 1 | Agent 2 | Agent 3 | Consensus |
|--------|-------------|---------|---------|---------|-----------|
| CH-001 | HubSpot CRM | HubSpot CRM | HubSpot CRM | Zoho CRM | 3/4 HubSpot ✓ |
| CH-006 | Humanforce  | RotaCloud | Humanforce | Deputy | No consensus ⚠ |
```

### 4b. Classify findings

For each change, classify the result:

- **Strong agreement (3-4 match):** SA pick confirmed. Mark as `verified: true`.
- **Majority agreement (2-3 match):** SA pick likely correct but note the alternative. Mark as `verified: true` with `alternative_noted`.
- **Split (no majority):** Contested — needs resolution in Stage 5. Mark as `contested`.
- **SA outlier (3 agents agree on different tool):** SA pick may be wrong. Prioritise for resolution. Mark as `sa_challenged`.

### 4c. Pricing comparison

For each change where tool picks agree, compare pricing:

```
PRICING VERIFICATION — {strategy_name}

| Change | Tool | SA Price | Agent 1 | Agent 2 | Agent 3 | Variance |
|--------|------|----------|---------|---------|---------|----------|
| CH-001 | HubSpot | $0/yr | $0/yr | $0/yr | $0/yr | 0% ✓ |
| CH-010 | Xero | $600/yr | $780/yr | $600/yr | $780/yr | 30% ⚠ |
```

Flag any pricing variance > 20%.

### 4d. New discoveries

List any tools recommended by verification agents that SA didn't consider:

```
NEW TOOLS DISCOVERED
| Agent | Change | Tool | Why considered | Worth investigating? |
|-------|--------|------|----------------|---------------------|
| Agent 2 | CH-006 | Skedulo | NDIS-specific scheduling | YES — SA missed NDIS-native option |
```

### 4e. Integration assessment comparison

Compare integration cohesion across agents:

```
INTEGRATION COMPARISON — {strategy_name}
| Metric | SA Original | Agent 1 | Agent 2 | Agent 3 |
|--------|-------------|---------|---------|---------|
| Manual handoffs | 2 | 3 | 2 | 2 |
| Separate logins | 6 | 5 | 6 | 7 |
| Cohesion | medium | medium | medium | low |
```

---

## Stage 5: Resolution

For each **contested** or **sa_challenged** item from Stage 4:

### 5a. Targeted deep-dive

Run focused web searches to resolve the specific disagreement:

1. **Head-to-head comparison:** Search `"{tool_a} vs {tool_b} for {use_case} {year}"`
2. **NDIS/AU suitability:** Search `"{tool_name} NDIS" OR "{tool_name} disability services Australia"`
3. **Pricing verification:** Search `"{tool_name} pricing" site:{tool_domain}` for each contested tool
4. **Integration verification:** Search `"{tool_a} {tool_b} integration"` for the contested combination

### 5b. Resolution decision

For each contested item, make a decision:

- **Keep SA pick:** If deep-dive confirms SA's choice or SA pick has clear advantages for this client
- **Switch tool:** If verification found a genuinely better option — document why
- **Add alternative:** If both are valid — keep SA pick but add the alternative to `tools_researched[]` with a note

### 5c. Display resolution

```
RESOLUTION — {strategy_name}

| Change | Status | Decision | Rationale |
|--------|--------|----------|-----------|
| CH-006 | contested | SWITCH to Skedulo | NDIS-native scheduling, AU-based, better ratio billing support |
| CH-010 | pricing_variance | UPDATED pricing | Xero increased to $87/mo in Jan 2026 — SA had stale price |
```

---

## Stage 6: Update Audit Data

### 6a. Update strategic_approaches

For each strategy that was verified:

1. Update tool selections where resolution changed the pick
2. Update pricing where verification found discrepancies
3. Recalculate `cost_summary` if any costs changed
4. Update `integration_analysis` if tool swaps changed the integration picture
5. Refresh `tool_deep_dives[]` for any new or swapped tools
6. Clear `research_gaps[]` for items that were resolved
7. Add any new gaps discovered during verification

### 6b. Add verification metadata

Add to `strategic_approaches`:

```json
{
  "verification": {
    "verified_at": "{ISO datetime}",
    "verification_run_count": 1,
    "scope": "strategies_1_and_2",
    "agents_per_strategy": 3,
    "results": {
      "use-what-you-have": {
        "changes_verified": 12,
        "strong_agreement": 9,
        "majority_agreement": 2,
        "contested_resolved": 1,
        "sa_challenged_resolved": 0,
        "pricing_corrections": 1,
        "tool_swaps": 0,
        "new_tools_discovered": 1
      },
      "best-of-breed-saas": {
        "changes_verified": 17,
        "strong_agreement": 12,
        "majority_agreement": 3,
        "contested_resolved": 1,
        "sa_challenged_resolved": 1,
        "pricing_corrections": 2,
        "tool_swaps": 1,
        "new_tools_discovered": 2
      }
    },
    "overall_confidence": "HIGH"
  }
}
```

### 6c. Update proposed_changes research

For any tool swap or pricing correction, also update the corresponding `proposed_changes[].research.tools_researched[]` entry so RI data stays in sync with SA data.

### 6d. Structural fixes

If the pre-flight scan (Stage 1b) found structural issues, fix them now:
- Assign missing `id` fields (CH-001 through CH-{n})
- Flag changes with missing value calculations for [BR] re-run
- Flag changes with missing modal content for [BR] re-run

---

## Stage 7: Display Summary

```
VERIFICATION COMPLETE — {company_name}
Run #{verification_run_count} · {datetime}

STRATEGIES VERIFIED: {n}

{For each verified strategy:}
{strategy_name}:
  ✓ Strong agreement:    {n}/{total} changes
  ~ Majority agreement:  {n}/{total} changes  
  ⚠ Contested→resolved:  {n}/{total} changes
  ✗ SA challenged:       {n}/{total} changes
  $ Pricing corrections: {n}
  ↔ Tool swaps:          {n}
  + New tools found:     {n}

TOOL SWAPS MADE:
  • CH-006: Humanforce → Skedulo (NDIS-native, better ratio billing)
  • (none if no swaps)

PRICING CORRECTIONS:
  • CH-010 Xero: $600/yr → $780/yr (price increase Jan 2026)
  • (none if no corrections)

NEW TOOLS WORTH NOTING:
  • Skedulo — NDIS-specific scheduling, discovered by 2/3 verification agents
  • (list any tools SA missed that multiple agents recommended)

STRUCTURAL FIXES APPLIED:
  • Assigned IDs: CH-001 through CH-017
  • (list any other fixes)

REMAINING ACTIONS:
  • Run [BR] on CH-016 — missing value calculation
  • (list any items needing attention)

Overall confidence: {HIGH if <10% contested | MEDIUM if 10-25% | LOW if >25%}

Next step: {If confidence HIGH → Generator [GT] + [GM] + [GW]
            If confidence MEDIUM/LOW → Consider re-running [SA] on weak areas, then [VR] again}
```

---

## Stage 8: Save

1. Write updated `strategic_approaches` (with verification metadata) to `clients/{client_slug}/audit/audit-data.json`
2. Write updated `proposed_changes[]` if any research was corrected
3. Update `analyst_metadata`:
   ```json
   {
     "analyst_metadata": {
       "last_vr_run": "{ISO datetime}",
       "total_vr_runs": 1,
       "last_vr_scope": "strategies_1_and_2",
       "last_vr_confidence": "HIGH"
     }
   }
   ```
4. Confirm save with summary

---

## Re-run Behaviour

On subsequent runs (`verification_run_count > 1`):
- Increment `verification_run_count`
- Focus verification agents on items that were `contested` or `sa_challenged` in previous run
- Compare new findings against previous verification results
- Track whether contested items have stabilised (same result across runs = higher confidence)
