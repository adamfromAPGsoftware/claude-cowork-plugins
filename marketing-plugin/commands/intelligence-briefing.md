---
name: intelligence-briefing
description: Cross-agent intelligence briefing — performance, competitors, creative pipeline, and recommendations
---

# Intelligence Briefing

Read all three marketing data files and present a unified intelligence summary across all agents.

## Process

1. **Load all data sources:**
   - `marketing-plugin/data/marketing-data.json` — own campaign performance
   - `marketing-plugin/data/campaigns/{active_campaign_id}/competitor-data.json` — competitor intelligence
   - `marketing-plugin/data/creative-data.json` — creative pipeline status

2. **Performance Section** — From marketing-data.json:
   - 7-day total spend, impressions, clicks, CTR, CPC, conversions
   - Week-over-week change (vs previous 7 days) with direction arrows
   - Top 3 performing ads (by CTR) and bottom 3 (by CPC)
   - Any ads showing fatigue (frequency > 3.0)
   - ROAS if available

3. **Competitor Section** — From competitor-data.json:
   - Watchlist count and last scrape date
   - New ads spotted since last briefing (first_seen in last 7 days)
   - Current winners (30+ days active) — count and dominant patterns
   - Super winners (90+ days active) — these are proven
   - Emerging patterns: what hook types, visual styles, and CTAs are trending

4. **Creative Pipeline Section** — From creative-data.json:
   - Active batches: count, dates, status breakdown
   - Angles awaiting image generation
   - Angles awaiting video generation
   - Angles packaged but not yet uploaded
   - Performance-linked angles: winners vs losers vs unlinked

5. **Recommendations** — Synthesise across all three sources:
   - **Pause:** Ads that are losing or fatigued → name them
   - **Scale:** Ads that are winning → suggest budget increase
   - **Create:** Gaps identified from competitors that we're not testing
   - **Research:** Competitor winners we haven't analysed yet
   - **Link:** Uploaded creatives that haven't been performance-linked yet
   - **Scrape:** If competitor data is >7 days old, suggest re-scrape

6. **Present briefing:**

   ```
   ═══════════════════════════════════════════════════════
   Marketing Intelligence Briefing — {date}
   ═══════════════════════════════════════════════════════

   PERFORMANCE (7-day)
   ───────────────────
   Spend: ${spend} ({change}% vs prev week)
   Impressions: {impressions} | Clicks: {clicks} | CTR: {ctr}%
   CPC: ${cpc} | Conversions: {conv} | CPA: ${cpa}
   
   Top performers: {ad1}, {ad2}, {ad3}
   Underperformers: {ad1}, {ad2}, {ad3}
   Fatigued: {count} ads with frequency > 3.0

   COMPETITORS
   ───────────
   Watching: {count} competitors | Last scrape: {date}
   New ads this week: {count}
   Active winners (30+ days): {count}
   Dominant patterns: {hook_types}, {visual_styles}

   CREATIVE PIPELINE
   ─────────────────
   Batches: {count} | Angles: {total}
   Awaiting images: {count} | Awaiting videos: {count}
   Packaged for upload: {count} | Uploaded & linked: {count}
   Performance: {winners} winners | {losers} losers | {unlinked} unlinked

   RECOMMENDATIONS
   ───────────────
   ! [PAUSE] {specific ads to pause}
   - [SCALE] {specific ads to scale}
   - [CREATE] {gaps to fill with new angles}
   - [RESEARCH] {competitor analysis to run}
   - [LINK] {uploaded creatives to performance-link}
   ```

## When to Use

Run this briefing:
- At the start of each marketing session to get oriented
- Before generating new angles (informs the intelligence summary in build-angles)
- Weekly as a status check
