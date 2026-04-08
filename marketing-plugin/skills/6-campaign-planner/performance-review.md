---
name: performance-review
description: Campaign-segregated performance review — retire losers, flag winners, recommend next angles
menu-code: PR
---

# Performance Review

Run a campaign-segregated performance review. This is the self-improving loop — retire underperforming angles and extract winner patterns to inform the next creative iteration.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Running performance review for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, load `campaign-data.json` and ask which live campaign to review. Show list of live campaigns.

2. **Load campaign config** — Read the campaign's performance thresholds from `performance.auto_retire_threshold`.

3. **Load Meta performance data** — Read `marketing-plugin/data/marketing-data.json`:
   - Filter insights by this campaign's `meta_campaign.campaign_id`
   - Aggregate by ad_id: total spend, impressions, clicks, CTR, CPC, conversions, CPA, ROAS
   - Only include ads with data from the last `review_cadence_days` days

4. **Map ads to angles** — Read `marketing-plugin/data/creative-data.json`:
   - For each ad_id in the campaign, find the matching angle via `meta_ad_ids`
   - Group performance metrics by angle

5. **Score each angle:**

   | Metric | Threshold | Source |
   |--------|-----------|--------|
   | Min spend | `auto_retire_threshold.min_spend` | Must have spent enough to evaluate |
   | Min days | `auto_retire_threshold.min_days` | Must have run long enough |
   | Max CPA | `auto_retire_threshold.max_cpa` | Retire if CPA exceeds this |
   | Min ROAS | `auto_retire_threshold.min_roas` | Retire if ROAS below this |
   | Min CTR | `auto_retire_threshold.min_ctr` | Retire if CTR below this |

   **Verdict logic:**
   - If spend < min_spend OR days < min_days → `insufficient_data` (don't retire yet)
   - If CPA > max_cpa (when set) → `loser`
   - If ROAS < min_roas (when set) → `loser`
   - If CTR < min_ctr (when set) → `loser`
   - If top 25% by ROAS or CTR → `winner`
   - Otherwise → `okay`

6. **Present review:**

```
═══ Performance Review: {campaign_name} ═══

Period: {start_date} to {end_date}
Iteration: #{iteration_count + 1}
Total spend: ${total_spend}
Total leads: {total_leads}
Overall CPA: ${overall_cpa}

| Angle | Framework | Spend | Leads | CPA | CTR | ROAS | Verdict |
|-------|-----------|-------|-------|-----|-----|------|---------|
| {angle_name} | {framework} | ${spend} | {leads} | ${cpa} | {ctr}% | {roas}x | WINNER |
| {angle_name} | {framework} | ${spend} | {leads} | ${cpa} | {ctr}% | {roas}x | LOSER |
| ... |

Winners ({count}): {list angle names}
  Patterns: {common framework, hook type, visual style}

Losers ({count}): {list angle names}
  Patterns: {what they have in common}

Recommended retirements: {count}
Recommended next angles: Riff on {winner patterns}, avoid {loser patterns}
```

7. **Ask for retirement approval (APPROVAL GATE 5):**

```
═══ APPROVAL GATE: Ad Retirement ═══

Ads to pause in Meta:
- Ad {ad_id} ({angle_name}): CPA ${cpa} exceeded max ${max_cpa}
- Ad {ad_id} ({angle_name}): CTR {ctr}% below min {min_ctr}%

Approve pausing these ads? [yes / no / modify]
```

8. **On approval:**
   - Mark angles as retired in creative-data.json: set `retired_at`, `retirement_reason`, `status: "retired"`
   - Move angle_ids from `creatives.active_angle_ids` to `creatives.retired_angle_ids` in campaign-data.json
   - Log approval in `approval_log`: gate="ad_retirement", status="approved"
   - Update `performance.last_review`, increment `performance.iteration_count`
   - Add entry to `performance.performance_history`
   - Present: "Angles marked for retirement. Run Campaign Launcher [RA] to pause ads in Meta, then Creative Generator [BA --campaign-id {id}] to build next iteration angles."

9. **Update winner patterns in intelligence:**
   - Add winning angle_ids to `intelligence.own_winner_angle_ids`
   - These will be loaded by Creative Generator [BA] for the next batch
