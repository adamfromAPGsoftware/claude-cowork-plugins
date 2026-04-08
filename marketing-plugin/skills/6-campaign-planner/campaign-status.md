---
name: campaign-status
description: Dashboard showing all campaigns with pipeline status and next actions
menu-code: SC
---

# Campaign Status

Show a dashboard of all campaigns and their current pipeline state.

## Process

1. **Load campaign-data.json** — Read all campaigns.

2. **For each campaign, determine next action** based on status and what's been done.

3. **Present dashboard:**

```
═══ Campaign Dashboard ═══

| # | Campaign | Status | Product | Active Angles | Iteration | Next Action |
|---|----------|--------|---------|---------------|-----------|-------------|
| 1 | {name} | {status} | {product.name} | {active count} | #{iteration_count} | {next action} |
| 2 | ... |

Total campaigns: {count}
Active (live): {live_count}
In progress: {non-live, non-completed count}
Completed: {completed_count}
```

4. **Show detail for any campaign on request** — If user asks about a specific campaign, show full breakdown:
   - Product and audience summary
   - Intelligence sources
   - Creative batch IDs and angle count
   - Landing page status and URL
   - Meta campaign status and IDs
   - Performance summary (last review date, spend, leads, CPA)
   - Approval log
   - Next recommended action

5. **Compute next action** based on campaign state:
   - `draft` → "Run [NC] to complete product/audience definition"
   - `planning` → "Run [MR] then [CS] to build strategy"
   - `creatives` → "Run Creative Generator [BA --campaign-id {id}]"
   - `landing_page` → "Run Landing Page Builder [GL]"
   - `review` → "Run Campaign Launcher [MC] then [GO]"
   - `live` → "Run [PR] for performance review" (if last_review > review_cadence_days ago)
   - `paused` → "Review and decide: resume or complete"
   - `completed` → "Archived — no action needed"
