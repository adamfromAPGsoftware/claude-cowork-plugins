---
name: market-report
description: Generate a market intelligence report from competitor winners, trends, and web research
menu-code: MR
---

# Market Report

Generate a market intelligence report for a campaign. This is LLM-driven — the agent synthesises competitor data, market research, and optionally web search results.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Generating market report for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, load `campaign-data.json` and ask which campaign to generate the report for. Show list.

2. **Load competitor intelligence** — Read `marketing-plugin/data/competitor-data.json`:
   - Find all ads with `status` of `"winner"` or `"super_winner"`
   - For each winner: note hook type, visual style, CTA pattern, copy strategy, days active
   - Summarise: dominant patterns, overused angles, whitespace opportunities

3. **Load own performance** — Read `marketing-plugin/data/creative-data.json`:
   - Find angles with `performance_snapshot.verdict == "winner"` → patterns to replicate
   - Find angles with `performance_snapshot.verdict == "loser"` → patterns to avoid

4. **Audience-specific research** — Based on the campaign's audience:
   - What language does this audience use to describe their problems?
   - What are the buying triggers specific to this industry/role?
   - What messaging angles resonate (fear, aspiration, social proof, urgency)?

5. **Optional: web research** — Ask user: "Should I search the web for current trends in {industry}?"
   - If yes, use WebSearch for: market trends, audience behaviour, competitor positioning
   - Synthesise findings into actionable themes

6. **Generate the report** — Save to `data/reports/campaigns/{campaign_id}/market-intelligence.md`:

```markdown
# Market Intelligence Report — {campaign_name}

Generated: {timestamp}
Campaign: {campaign_id}

## Competitor Landscape
- {count} competitor winners analysed
- Dominant hooks: {list}
- Dominant visual styles: {list}
- Dominant CTAs: {list}
- Overused angles: {list}

## Whitespace Opportunities
- {gap 1}: {description}
- {gap 2}: {description}

## Audience Language
- Pain language: {phrases they use}
- Aspiration language: {phrases they use}
- Buying triggers: {what makes them act}

## Key Themes
1. {theme} — {insight}
2. {theme} — {insight}

## Activation Opportunities
1. {opportunity} — {why it works for this audience}
2. {opportunity} — {why it works for this audience}

## Own Performance Insights
- Winners to replicate: {patterns}
- Losers to avoid: {patterns}
```

7. **Update campaign-data.json:**
   - Set `intelligence.market_report_path` to the report path
   - Set `intelligence.key_themes` from the report
   - Set `intelligence.activation_opportunities` from the report
   - Set `intelligence.competitor_winner_ids` from the winners used

8. **Present summary:**
```
Market Intelligence Report generated for {campaign_name}.
Path: {report_path}

Competitor winners analysed: {count}
Whitespace opportunities: {count}
Key themes: {count}

Next: Run [CS] to build creative strategy from this intelligence.
```
