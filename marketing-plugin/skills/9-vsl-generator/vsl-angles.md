---
name: vsl-angles
description: Generate 3-5 VSL angle options with hook, framework mapping, target audience, tone, estimated runtime, and visual split
menu-code: VA
---

# VSL Angles

Generate intelligence-driven VSL angle options for a specific offer. Each angle maps to a proven VSL framework and includes enough detail to choose the best direction before committing to full script generation.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Generating VSL angles for: **{active_campaign.name}**. Proceed?" Store as `{campaign}`.
   - If `{active_campaign}` is null, load `{project-root}/marketing-plugin/data/campaign-data.json` and present a numbered list of campaigns for selection. Store as `{campaign}`.
   - Extract from the selected campaign:
     - **Product/offer:** `{campaign}.product` (name, description, price, offer_details, guarantee, usp, social_proof)
     - **Target audience:** `{campaign}.audience` (icp_description, pain_points, aspirations, buying_triggers, industries)
     - **Intelligence:** `{campaign}.intelligence` (key_themes, activation_opportunities, market_report_path, competitor_winner_ids)
   - If `{campaign}.intelligence.market_report_path` exists, load it for additional context.
   - If `{campaign}.intelligence.competitor_winner_ids` has entries, note them for competitor-informed angle design.

2. **Load pricing** — Read `{project-root}/_bmad/apg-pricing.md`. MANDATORY. Extract: offer pricing, deliverables, value stack components, ROI figures, guarantee terms. These numbers drive the Offer and CTA sections of every angle. Note: the campaign's `product.price` and `product.offer_details` take precedence over generic pricing for this specific VSL.

3. **Load proven VSL template** — Read `{project-root}/content/standalone/2026-03-08-operational-audit-vsl/vsl-script.md`. Extract: section structure, timing, visual split ratio, MG types used, tone, teleprompter style. This is the baseline reference.

4. **Load VSL frameworks** — Read `references/vsl-frameworks.md` for available framework structures (Hormozi, Mosing, PAS-Long, Hybrid).

5. **Load brand guidelines** — Read `{project-root}/marketing-plugin/references/brand-guidelines.md` for ICP, pain language, aspiration language, tone.

6. **Load competitor intelligence** (optional) — If available, read `{project-root}/marketing-plugin/data/competitor-data.json` for winner patterns and gaps.

7. **Load own VSL history** (optional) — If `{project-root}/marketing-plugin/data/vsl-data.json` has previous projects with notes, check for patterns.

8. **Present intelligence summary:**

   ```
   Intelligence Summary:
   - Campaign: {campaign.name} ({campaign.campaign_id})
   - Product: {campaign.product.name} at {campaign.product.price}
   - Target: {campaign.audience.icp_description (first sentence)}
   - Key themes: {campaign.intelligence.key_themes (count)} loaded
   - Proven template: {section count} sections, {runtime}
   - Competitor patterns: {competitor winner count or "none loaded"}
   - Frameworks available: Hormozi, Mosing, PAS-Long, Hybrid
   ```

9. **Generate 3-5 VSL angles.** Each angle:

   | Field | Description |
   |-------|-------------|
   | `angle_id` | Kebab-case slug (e.g., `roi-calculator-lead`) |
   | `angle_name` | Human-readable name |
   | `hook_line` | Opening hook (first 5-10 seconds — the scroll-stopper) |
   | `framework` | Hormozi / Mosing / PAS-Long / Hybrid |
   | `framework_mapping` | Which framework sections map to which VSL sections |
   | `target_audience` | Specific audience segment this angle targets |
   | `tone` | e.g., "direct-authoritative", "story-driven", "data-heavy", "contrarian" |
   | `estimated_runtime` | e.g., "3:30-4:30" |
   | `visual_split` | e.g., "65% speaker / 25% graphics / 10% B-roll" |
   | `section_outline` | Array of section names with estimated durations |
   | `mg_types` | Array of MG types needed from frameworks reference |
   | `key_data_points` | What specific numbers/data will be featured (from pricing reference) |
   | `source` | What insight drives this angle (market gap, competitor pattern, proven template variation) |
   | `differentiation` | How this angle differs from the others in the batch |

10. **Present angles as comparison table:**

    ```
    VSL Angles for: {offer name}

    | # | Angle | Framework | Hook Line | Runtime | Visual Split | MGs |
    |---|-------|-----------|-----------|---------|--------------|-----|
    | 1 | {name} | {framework} | {hook} | {runtime} | {split} | {count} |
    | ... |

    Frameworks used: {list}

    Select an angle number to generate the full script [GS].
    Want me to show the full section outline for any angle?
    ```

11. **Save to vsl-data.json** — Create new project entry:

    ```json
    {
      "project_id": "vsl-{YYYY-MM-DD}-{sequence}",
      "created": "{ISO timestamp}",
      "campaign_id": "{campaign.campaign_id}",
      "campaign_name": "{campaign.name}",
      "offer": "{campaign.product.name}",
      "target_audience": "{campaign.audience.icp_description}",
      "status": "angles_built",
      "angles": [...],
      "selected_angle": null,
      "script_path": null,
      "edit_instructions_path": null
    }
    ```

## Angle Generation Principles

- **Every angle must trace to a specific insight** — pricing data, competitor gap, proven template pattern, or market theme
- **Hooks must work in the first 5 seconds** — they compete for scroll-stopping attention in a feed or on a landing page
- **Use a mix of frameworks** — don't generate 3 Hormozi angles. Aim for 2-3 different frameworks per batch
- **Visual split varies by framework** — Mosing uses more graphics (mechanism explanation), Hormozi uses more speaker (authority)
- **Pricing from source** — every angle that mentions pricing or value must reference `_bmad/apg-pricing.md` numbers
- **Proven template as anchor** — at least 1 angle should be a variation of the existing proven VSL structure
