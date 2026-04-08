---
name: generate-strategic-approaches
description: "Generate strategic-approaches.html — single recommended SaaS toolkit with configuration guides, cost breakdown, and custom build CTA."
menu-code: GA
---

# Generate Strategic Approaches

## Purpose

Produce `strategic-approaches.html` showing a single recommended SaaS toolkit with the best tool per proposed change, configuration guides, a cost breakdown, and a custom build alternative CTA.

**Requires:** `strategic_approaches` top-level object in audit-data.json (run Analyst [SA] first).

## Process

### Step 1: Pre-flight Check

Client slug is set from activation. Load `clients/{client_slug}/audit/audit-data.json`.

Check that `strategic_approaches` exists and has `strategies[]` populated.

```
✗ strategic_approaches not found. Run Analyst [SA] Build Strategic Approaches first.
```

If `strategic_approaches` exists but `proposed_changes[].research` is also available, the generator reads from `strategic_approaches` as the primary data source — this is pre-built analytical data, not algorithmically computed.

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output strategic-approaches
```

Output is saved to: `clients/{client_slug}/deliverables/strategic-approaches.html`

### Step 3: Content Structure — Buyer-First Presentation

The generated HTML reads from the `strategic_approaches` object and the process map data. It compares three approaches (Quick Wins, SaaS Toolkit, Your Platform) with a buyer-first presentation designed for non-technical decision makers.

**Critical presentation principles (apply to ALL clients):**

1. **Lead with pain, not projections.** The hero section opens with the client's monthly waste figure and weekly hours lost — not 5-year ROI. Buyers process problems before solutions.

2. **Show 90-day outcomes first.** Add a "What Changes in the First 90 Days" section immediately after the hero, with 3 cards showing Weeks 1-3, Weeks 4-8, and Weeks 8-11 outcomes in plain language. No jargon.

3. **Separate hard savings from time savings.** Never present a single annual value figure without breaking it into "Hard Savings" (actual money saved/recovered — leads, overruns, cancelled subscriptions) and "Time Freed Up" (hours back, valued at hourly rate). Include a conservative estimate note.

4. **Add a Financial Summary for Decision Makers.** Collapsible section near the top with 5-6 pure-numbers rows: total investment (after R&D refund), ongoing cost, break-even month, annual net benefit, R&D tax treatment, low-risk entry option.

5. **Rename "Custom Build" to "Your Platform."** The term "custom build" triggers risk anxiety. "Your Platform" frames it as something purpose-built for them.

6. **Lead pricing cards with effective cost.** Show the post-R&D-refund price as the primary number (e.g., $33,900), with the pre-refund price struck through as secondary. Never lead with the highest number.

7. **Use the client's own words.** In admin overhead breakdowns, quote actual client statements about their chaos instead of academic citations. In value calculations, reference specific incidents they described.

8. **Frame SaaS as the DIY alternative.** Section title: "The DIY Route: What You'd Need Without Us" with a visual comparison of 1 platform box vs N scattered tool boxes. The 16-tool list should feel overwhelming BY DESIGN, with explicit framing that this is what they'd face alone.

9. **Guarantee in hours, not dollars.** Reframe 90-day guarantees as "If your team isn't saving at least X hours per week within 90 days, we refund" — hours are tangible, dollar savings from recovered revenue are speculative.

10. **Add "Your Monday Morning" vignettes** to Quick Wins and Your Platform tiers — paint a picture of the transformed daily experience in 2-3 sentences.

11. **Maintenance is included, not a line item.** Do NOT show maintenance retainer costs for Your Platform. Maintenance is included as long as remains the development partner. The only ongoing cost is hosting (~$100/mo). This is a key differentiator — frame it as "maintenance included" in the cost table and in comparison cards. If another developer touches the code, we can't be responsible for their changes — mention this once in the considerations section.

12. **R&D eligibility must say "pending eligibility."** Always include "pending eligibility" or "pending eligibility confirmation" next to R&D tax refund figures. We handle the paperwork but can't guarantee eligibility until the build is assessed. Don't undermine it with "not guaranteed" — just state it's pending confirmation.

**Section order:**
- **Header** with branding
- **Hero** — monthly waste, weekly hours lost, fixes identified, time to results
- **90-Day Outcomes** — 3 cards with weekly milestones
- **Financial Summary for Decision Makers** — collapsible, pure numbers for CFO
- **Cost comparison table** — 3 approaches with expandable calculation details
- **Value breakdown** — hard savings vs time savings, conservative estimate
- **Hidden SaaS costs** — using client's own quotes about tool chaos
- **1 vs N visual comparison** and SaaS toolkit table
- **Why One Platform Beats N Tools** — side-by-side with client-specific framing
- **3-Year cost trajectory chart**
- **Your Options** — 3 pricing tiers with Monday Morning vignettes and hours-based guarantees
- **Process-by-process breakdown** — per-change comparison cards with "Compare DIY vs Your Platform" toggles
- **Priority matrix** — interactive bubble chart
- **Prototype CTA** — prominent, early mention throughout
- **Design tokens:** lime `#7DFF00`, Inter font, card-based layout, self-contained HTML

### Step 4: Post-generation

Confirm the file was created. Report the file path and size.

```
STRATEGIC APPROACHES GENERATED — {company_name}
File: clients/{client_slug}/deliverables/strategic-approaches.html
Size: {size}

Recommended SaaS toolkit generated from {n} proposed changes.
```

Suggest opening in browser to review.
