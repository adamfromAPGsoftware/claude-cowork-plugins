---
name: build-and-rate
description: Estimate implementation weeks, calculate value with visible formulas, and write client-facing modal content for the priority matrix.
menu-code: BR
---

# Build & Rate (BR)

> **Idempotent.** First run estimates everything. Re-runs review and update existing estimates, fill gaps.

## Purpose

For each proposed_change with research, estimate how many weeks it takes to implement, calculate the annual value with transparent formulas the client can verify, and write the 5-section modal content that appears when they click a bubble in the priority matrix.

---

## Stage 1: Pre-flight

1. Check audit data is loaded and `proposed_changes[]` is populated.

2. Scan changes for readiness:
   ```
   BUILD & RATE STATUS — {company_name}
   Total proposed changes: {n}
     research complete:     {n} — ready for estimation
     research needs_review: {n} — can estimate with caveats
     research not_started:  {n} — SKIP (run RI first)

   Already rated (has implementation + value):
     complete: {n}
     partial:  {n}
     none:     {n}
   ```

3. Select scope:
   ```
   Scope options:
     A) All unrated changes with research — {n} changes
     B) Specific change by ID
     C) Re-rate specific ID (update existing estimates)
     D) All changes (including already-rated — full refresh)
   ```

---

## Stage 2: Estimate Implementation

For each change in scope, use the effort estimation guide (`references/effort-estimation-guide.md`) and research findings:

### 2a. Estimate dev hours and PM hours

**Check delivery type first.** If this change has `cowork_training_option.viable == true` in its research and is selected as `delivery_type: "cowork_training"` in strategic approaches, use the Cowork estimation model instead:

```
prep_hours = cowork_training_option.estimated_prep_hours (typically 2-4)
training_hours = cowork_training_option.estimated_training_hours (typically 4-8)
followup_hours = cowork_training_option.estimated_followup_hours (typically 2-4)
total_hours = prep_hours + training_hours + followup_hours
dev_hours = prep_hours (MCP setup, custom instructions)
pm_hours = training_hours + followup_hours (delivery + support)
```

Cowork items are significantly faster — training prep is not development. Use the Cowork hours from RI, don't inflate them with traditional dev estimates.

**For traditional (SaaS/automation/custom) delivery:**

Based on:
- `research.tools_researched` — API complexity, integration guides found
- `change_type` — automate (typically 8-40 dev hrs), replace (4-16), eliminate (2-8), consolidate (16-40)
- Number of `affected_step_ids` — more steps = more integration points
- `research.risks` — each risk adds buffer

### 2b. Convert to weeks

```
weeks_estimate = ceil((dev_hours + pm_hours) / 40 * 10) / 10
```

Round to nearest 0.5 for display. Assign `weeks_label`:
- `< 1 week` — total effort under 40 hours
- `1-2 weeks` — 40-80 hours
- `2-4 weeks` — 80-160 hours
- `4+ weeks` — over 160 hours

### 2c. Populate implementation sub-object

```json
{
  "implementation": {
    "weeks_estimate": 1.5,
    "weeks_label": "1-2 weeks",
    "dev_hours": 40,
    "pm_hours": 8,
    "confidence": "MEDIUM"
  }
}
```

---

## Stage 3: Calculate Value

Two value types — calculate whichever applies (or both):

### 3a. Time Saving

When the change reduces hours spent on an existing task:

1. Find `hours_saved_per_week`:
   - From linked `waste_items[]` hours_per_week
   - Or from `time_saving_minutes_per_occurrence × frequency` converted to weekly hours
   - Or estimate from the affected steps' duration_minutes and frequency

2. Determine `hourly_rate_aud` (use the first match in this priority order):
   - From the linked waste_item's `hourly_rate_aud` (if role-specific and `rate_is_estimated: false`)
   - From `staff_roster[]` — match the step owner's role to find a role-specific rate (e.g., Tom at $200/hr vs coaches at $42.50/hr)
   - From `blended_hourly_rate_aud` on the audit data (last resort fallback)

3. Calculate with visible formula:
   ```
   annual_saving_aud = hours_saved_per_week × hourly_rate_aud × 52
   formula = "{hours} hrs/wk × ${rate}/hr × 52 wks = ${total}/yr"
   ```

### 3b. Productivity Enhancement

When the change increases output without reducing hours (e.g., AI enablement):

1. Identify `current_revenue_or_metric`:
   - Revenue attributed to the process/stage (from transcripts or estimates)
   - Or throughput metric (e.g., leads processed, placements made)
   - Or cost-of-error metric (e.g., compliance failures, missed renewals)

2. Estimate `improvement_percentage`:
   - Conservative: 5-10% for AI-assisted decision support
   - Moderate: 10-20% for AI process automation
   - Aggressive: 20-30% for full AI workflow replacement
   - Default to conservative unless research supports higher

3. Calculate with visible formula:
   ```
   estimated_annual_value_aud = current_revenue_or_metric × (improvement_percentage / 100)
   formula = "${metric} × {pct}% improvement = ${total}/yr"
   ```

### 3c. Combined value

```
combined_annual_value_aud = time_saving.annual_saving_aud + productivity_enhancement.estimated_annual_value_aud
formula_summary = "Time: ${time} + Productivity: ${prod} = ${total}/yr"
```

If only one type applies, `combined_annual_value_aud` equals that type's value and `formula_summary` reflects only that calculation.

### 3d. Populate value sub-object

```json
{
  "value": {
    "value_type": "both",
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
      "confidence": "LOW"
    },
    "combined_annual_value_aud": 21100,
    "formula_summary": "Time: $9,100 + Productivity: $12,000 = $21,100/yr"
  }
}
```

Also set `value_type` on the proposed_change root: `"time_saving"`, `"productivity_enhancement"`, or `"both"`.

---

## Stage 4: Write Modal Content

For each change, write the 5 client-facing sections that appear in the priority matrix modal:

### 4a. Gather meeting references

Collect all `meeting_references` from:
- Source pain_points (via `linked_pain_point_ids`)
- Source waste_items (matching stage/activity)
- Source optimisations (matching stage)
- Affected steps (via `affected_step_ids`)

Deduplicate by `(session, timestamp_seconds)`. These appear as Fathom deep-links in the modal.

### 4b. Write sections

```json
{
  "modal_content": {
    "what_is_the_task": "Currently, {owner} manually {describes current process} taking {time} per {frequency}. {Include verbatim quote from transcript if available.}",

    "what_we_will_build": "{Concrete description of the automation/integration/AI tool}. Uses {proposed_tools} to {describe mechanism}.",

    "how_it_works": "When {trigger event} → {step 1} → {step 2} → {outcome}. {Technical detail appropriate for a non-technical business owner.}",

    "how_it_saves_money": "{formula_summary}. {Plain-language explanation of where the value comes from — e.g., 'This eliminates 3.5 hours of manual data entry per week, freeing key staff to focus on client relationships instead.'}",

    "how_quick": "{weeks_label} to implement. {Brief description of implementation phases — e.g., 'Week 1: Configure HubSpot sequences. Week 2: Test with 5 clients, then roll out.'}",

    "meeting_references": [
      { "session": 3, "timestamp_seconds": 2808, "fathom_url": "{FATHOM_CALL_URL}", "transcript_excerpt": "The rest of the staff is probably taking 20 hours of {STAFF_NAME}'s work week away..." }
    ]
  }
}
```

**Writing guidelines:**
- Use the client's actual names (from audit data contact, process step owners)
- Reference their actual tools by name
- Keep language conversational — this is for a business owner, not a developer
- Include at least one verbatim quote from transcripts where possible
- Formulas must be the exact same formulas from the value sub-object

**For Cowork-delivered changes** (`delivery_type: "cowork_training"`), adjust the modal framing:
- `what_we_will_build` → frame as "We'll train your team to use Claude AI connected to {tools} to {outcome}" not "We'll build an automation"
- `how_it_works` → describe the human-AI interaction: "You tell Claude what you need → Claude reads your {tool data} → Claude creates/updates {output}. You review and approve."
- `how_quick` → frame as training timeline: "{weeks_label} — includes setup, hands-on training, and 2 weeks of follow-up support. Your team is self-sufficient after that."
- Emphasise team autonomy: "You can adjust how this works by updating your instructions to Claude — no developer needed for process changes."
- Emphasise control: "This isn't a black box — you're directing the AI, and you can see and approve everything it does."

---

## Stage 5: Update ROI Items

For each change, update the linked `roi_items[]` entry:
- `annual_saving_aud` = `value.combined_annual_value_aud`
- `monthly_saving_aud` = `annual_saving_aud / 12`
- `build_cost_aud` = `(implementation.dev_hours × dev_rate) + (implementation.pm_hours × pm_rate)` — internal only
- `payback_months` = `build_cost_aud / monthly_saving_aud`
- `payback_tag`: < 12 months = `QUICK_WIN`, 12-24 = `CORE_BUILD`, > 24 = `FUTURE`

---

## Stage 6: Display Summary

```
BUILD & RATE COMPLETE — {company_name}

| # | ID     | Title                          | Value Type    | Annual Value | Weeks | Confidence | Modal |
|---|--------|--------------------------------|---------------|-------------|-------|------------|-------|
| 1 | CH-001 | Automate onboarding pack       | time_saving   | $9,100/yr   | 1.5   | HIGH       | ✓     |
| 2 | CH-007 | AI call analysis for BDMs      | productivity  | $12,000/yr  | 2.0   | LOW        | ✓     |
| 3 | CH-008 | ShiftCare API auto-rostering   | both          | $21,100/yr  | 3.0   | MEDIUM     | ✓     |
...

Total annual value: ${total}/yr across {n} changes
Quick wins (<1 wk): {n} changes worth ${total}/yr
Short builds (1-2 wks): {n} changes worth ${total}/yr

Changes without modal content: {n} (run BR on these)
Changes without value calculation: {n} (missing data — check VR)

Next step: Run [VR] to verify research, then [TB] to build blueprint.
```

---

## Stage 7: Save

1. Write updated `proposed_changes[]` and `roi_items[]` to audit data
2. Update `analyst_metadata`
3. Confirm save
