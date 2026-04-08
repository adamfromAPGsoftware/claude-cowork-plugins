---
name: campaign-strategy
description: Build creative strategy, angle direction, and landing page copy for a campaign
menu-code: CS
---

# Campaign Strategy

Build the creative strategy for a campaign — angle direction, messaging themes, and landing page copy. This is LLM-driven — the agent synthesises the market intelligence report into actionable creative direction.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Building strategy for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, load `campaign-data.json` and ask which campaign to build strategy for. Show list.

2. **Load campaign context** — Read the campaign's product, audience, and intelligence from campaign-data.json.

3. **Load market intelligence** — Read the report at `intelligence.market_report_path`.

4. **Load brand guidelines** — Read `marketing-plugin/references/brand-guidelines.md`.

5. **Build angle direction** — Recommend 3-5 angle themes for the Creative Generator:
   - Each theme should map to a specific audience pain point or activation opportunity
   - Suggest frameworks (PAS, AIDA, BAB, Curiosity Gap, Social Proof) per theme
   - Note which competitor patterns to adapt and which to avoid

6. **Build landing page copy:**
   - **Headline:** Bold, clear value proposition (max 10 words)
   - **Subheadline:** Supporting detail that adds specificity
   - **Benefits:** 3-5 bullet points, each with a clear outcome
   - **Social proof:** Testimonials, stats, logos, or case studies to include
   - **CTA text:** Action-oriented button text
   - **Form fields:** What to ask for (name, email, phone, company — keep minimal)

7. **Build UTM plan:**
   - utm_source: "meta" (default)
   - utm_medium: "paid" (default)
   - utm_campaign: kebab-case from campaign name

8. **Update campaign-data.json:**
   - Set `creatives.landing_page_copy` with all copy elements
   - Set `tracking.utm_campaign`
   - Update status to `build`

9. **Present the strategy for approval (APPROVAL GATE 1):**

```
═══ APPROVAL GATE: Campaign Plan ═══

Campaign: {name} ({campaign_id})
Product: {product.name}
Audience: {icp_description}

Angle Direction:
1. {theme} — {framework} — {pain point it addresses}
2. {theme} — {framework} — {pain point it addresses}
3. {theme} — {framework} — {pain point it addresses}

Landing Page Copy:
  Headline: {headline}
  Subheadline: {subheadline}
  Benefits: {benefits list}
  Social Proof: {proof points}
  CTA: {cta_text}
  Form: {form_fields}

UTM: ?utm_source=meta&utm_medium=paid&utm_campaign={utm_campaign}

Approve this strategy? [yes / no / modify]
```

10. **On approval:**
    - Log approval in `approval_log`: gate="campaign_plan", status="approved"
    - Update campaign status to `build`
    - Present next step: "Start both tracks in parallel: **Track A** — Campaign Launcher [GA] to setup GA4, then Landing Page Builder [GL] to generate the landing page. **Track B** — Creative Generator [BA --campaign-id {id}] to build ad angles. These tracks are independent and can run simultaneously."

11. **On rejection/modify:**
    - Ask what to change
    - Revise and re-present
