---
name: query
description: Freeform marketing data query — ask anything about campaigns, ads, or performance metrics
menu-code: QR
---

# Marketing Query

Answer freeform questions about the marketing data.

## Process

1. **Load marketing-data.json** — Read campaign structure and insights

2. **Understand the question** — Parse what the user wants to know:
   - "Which campaign has the best CTR?" → rank by metric, show top items
   - "How much did I spend last week?" → filter by date range, sum spend
   - "Show me all ads with zero conversions" → filter by metric threshold
   - "Compare Brand vs Retargeting campaigns" → side-by-side comparison
   - "What's my average CPC?" → aggregate metric calculation
   - "Which ad sets are underperforming?" → identify outliers

3. **Answer with evidence:**
   - Always cite specific campaign/ad set/ad names and metric values
   - Show calculations (e.g., "Total spend: $500 + $350 + $150 = $1,000")
   - State the date range the answer covers
   - If the answer requires inference, state assumptions explicitly

4. **Present in the clearest format:**
   - Single number → direct answer with supporting data
   - List → table with entity details and metrics
   - Comparison → side-by-side table with differences highlighted
   - Trend → chronological table with direction indicators

## Principles

- Every answer includes at least one specific metric value as evidence
- If the question can't be answered from the data, say what's missing
- Offer follow-up: "Would you like me to dig deeper into any of these?"
- Distinguish between "no conversions tracked" and "conversion tracking not configured" (check if actions array exists)
- Don't double-count: use campaign-level insights for campaign questions, ad-set-level for ad set questions

## Example

User: "Which campaign gives me the cheapest leads?"

```
Cost Per Lead by Campaign (All Time):

| Campaign              | Spend     | Leads | Cost/Lead | CTR    | Status |
|-----------------------|-----------|-------|-----------|--------|--------|
| Lead Gen - Retarget   | $890      | 15    | $59.33    | 2.05%  | ACTIVE |
| Brand Awareness       | $1,234    | 12    | $102.83   | 1.98%  | ACTIVE |
| Cold Traffic - Broad  | $650      | 3     | $216.67   | 0.92%  | ACTIVE |
| Engagement Campaign   | $340      | 0     | N/A       | 1.45%  | PAUSED |

Cheapest leads: "Lead Gen - Retarget" at $59.33/lead
Note: "Engagement Campaign" has $340 spend with zero leads — worth reviewing.
```
