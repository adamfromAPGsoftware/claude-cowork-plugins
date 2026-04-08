---
name: generate-landing
description: Generate a landing page from campaign config and templates with variable substitution
menu-code: GL
---

# Generate Landing Page

Generate a complete landing page from campaign configuration — supports both HTML template substitution and React app forking workflows.

## Process

1. **Load campaign data** — Read `marketing-plugin/data/campaign-data.json`. List campaigns that have `creatives.landing_page_copy` populated. If none, inform the user they need to populate landing page copy first (via Campaign Planner).

2. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Generating landing page for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, present a numbered list of campaigns with landing page copy. If multiple, ask which one. If only one, use it.

3. **Determine workflow** — Check `landing_page.template` and `landing_page.template_repo` on the selected campaign:
   - If `template` is `go-enhance` and `template_repo` is set → use the **React Template Workflow** (section below)
   - Otherwise → use the **HTML Template Workflow** (section below)

---

## React Template Workflow (go-enhance)

Use this workflow when `landing_page.template` is `go-enhance` and `landing_page.template_repo` points to a local React app directory.

### R1. Load campaign details

Extract from the selected campaign:
- `product.name`, `product.description`, `product.offer_details`, `product.guarantee`, `product.usp`
- `audience.pain_points`, `audience.aspirations`
- `creatives.landing_page_copy` (all fields: headline, subheadline, benefits, social_proof, cta_text, cta_description, faq)
- `tracking.utm_source`, `tracking.utm_medium`, `tracking.utm_campaign`
- `landing_page.template_repo` (absolute path to the source React app)
- `lead_capture.form_webhook_url`

### R2. Fork the source repo

Copy the entire `{template_repo}` directory to `marketing-plugin/data/landing-pages/{campaign_id}/`. This creates a standalone copy of the React app for this campaign.

### R3. Install dependencies

Run `npm install` inside the forked directory to ensure all dependencies are in place.

### R4. Edit component content

Edit each component file directly in the forked app, replacing content while preserving the React component structure, imports, and Tailwind/shadcn patterns. **DO NOT use template variables** — edit the actual TSX code with real campaign content.

Components to update:

- **`src/components/Hero.tsx`** — Replace headline, subheadline, and CTA button text using `creatives.landing_page_copy.headline`, `.subheadline`, and `.cta_text`

- **`src/components/Stats.tsx`** — Replace stat metrics using `product.usp` values (e.g., "200→20 hours", "90% reduction", concrete before/after numbers)

- **`src/components/ValueProposition.tsx`** — Replace benefit items using `creatives.landing_page_copy.benefits` (title + description for each)

- **`src/components/Testimonials.tsx`** — Replace testimonial content using `creatives.landing_page_copy.social_proof`

- **`src/components/QualificationQuiz.tsx`** — Adapt quiz questions for the campaign audience:
  - Team size, revenue range, scoping hours per week, concurrent projects
  - Set qualification criteria that match the campaign's ideal customer profile
  - Set booking URL from `lead_capture.form_webhook_url` or campaign booking link

- **`src/components/ROICalculator.tsx`** — Adapt calculator inputs and formulas for the campaign product (e.g., scoping time savings, cost reduction, hours reclaimed)

- **`src/components/Portfolio.tsx`** — Replace with demo screenshots or interactive prototype embed relevant to the campaign product

- **`src/components/FAQ.tsx`** — Replace Q&A items using `creatives.landing_page_copy.faq` or generate campaign-specific FAQs from product and audience data

- **`src/components/CTA.tsx`** — Replace CTA text and description using `creatives.landing_page_copy.cta_text` and `.cta_description`

- **`src/components/Header.tsx`** — Update logo reference, nav links, and branding for the campaign

- **`src/components/Footer.tsx`** — Update footer links, legal text, and company info

### R5. Leave tracking placeholder

Keep any existing tracking script placeholders or `<!-- TRACKING_SCRIPTS -->` comments in place. Tracking is injected separately via [ST].

### R6. Update campaign-data.json

Set:
- `landing_page.status` = `"generated"`
- `landing_page.deploy_path` = `"data/landing-pages/{campaign_id}"`
- `landing_page.workflow` = `"react"`
- `landing_page.generated_at` = current ISO 8601 timestamp

### R7. Report

```
Landing Page Generated (React) — {campaign.name}

Template: go-enhance (React fork)
Source: {template_repo}
Output: data/landing-pages/{campaign_id}/
Status: generated

Components updated:
- Hero: headline, subheadline, CTA
- Stats: {usp_count} metrics from product.usp
- ValueProposition: {benefit_count} benefits
- Testimonials: {social_proof_count} items
- QualificationQuiz: adapted for campaign audience
- ROICalculator: adapted for campaign product
- Portfolio: demo content
- FAQ: {faq_count} items
- CTA: text and description
- Header: branding
- Footer: links and legal

Next: Run [ST] to inject tracking codes, then [PV] to preview.
```

---

## HTML Template Workflow

Use this workflow when `landing_page.template` is anything other than `go-enhance`, or when `template_repo` is not set.

### H1. Load campaign details

Extract from the selected campaign:
- `product.name`, `product.description`, `product.offer_details`, `product.guarantee`, `product.usp`
- `audience.pain_points`, `audience.aspirations`
- `creatives.landing_page_copy.headline`
- `creatives.landing_page_copy.subheadline`
- `creatives.landing_page_copy.benefits`
- `creatives.landing_page_copy.social_proof`
- `creatives.landing_page_copy.cta_text`
- `creatives.landing_page_copy.form_fields`
- `tracking.utm_source`, `tracking.utm_medium`, `tracking.utm_campaign`
- `landing_page.template` (default: "lead-gen")
- `lead_capture.form_webhook_url`

### H2. Load template

Read `marketing-plugin/templates/landing-pages/{template}.html` where `{template}` is from `landing_page.template`.

### H3. Load form component

Read `marketing-plugin/templates/landing-pages/components/form.html`.

### H4. Build benefits HTML

For each benefit in `landing_page_copy.benefits`, generate:
```html
<div class="benefit-card">
  <div class="benefit-icon">...</div>
  <h3>{benefit_title}</h3>
  <p>{benefit_description}</p>
</div>
```
If benefits are simple strings, use the string as both title and description.

### H5. Build social proof HTML

For each item in `landing_page_copy.social_proof`, generate appropriate HTML (testimonial quotes, stat callouts, or logo references).

### H6. Build form fields HTML

For each field in `landing_page_copy.form_fields`, generate:
```html
<div class="form-group">
  <input type="{type}" name="{name}" placeholder="{placeholder}" required>
</div>
```
Map common field names: `name` -> text, `email` -> email, `phone` -> tel, `company` -> text, `message` -> textarea.

### H7. Perform substitution

Replace all `{{variables}}` in the template:
- `{{headline}}` -> `landing_page_copy.headline`
- `{{subheadline}}` -> `landing_page_copy.subheadline`
- `{{benefits_html}}` -> generated benefits HTML
- `{{social_proof_html}}` -> generated social proof HTML
- `{{cta_text}}` -> `landing_page_copy.cta_text`
- `{{form_action}}` -> `lead_capture.form_webhook_url` or "#"
- `{{form_fields_html}}` -> generated form fields HTML
- `{{campaign_name}}` -> `campaign.name`
- `{{utm_source}}` -> `tracking.utm_source`
- `{{utm_medium}}` -> `tracking.utm_medium`
- `{{utm_campaign}}` -> `tracking.utm_campaign`

### H8. Leave tracking placeholder

Keep `<!-- TRACKING_SCRIPTS -->` in place. Tracking is injected separately via [ST].

### H9. Write output

Save to `marketing-plugin/data/landing-pages/{campaign_id}/index.html`. Create the directory if it doesn't exist.

### H10. Update campaign-data.json

Set:
- `landing_page.status` = `"generated"`
- `landing_page.deploy_path` = `"data/landing-pages/{campaign_id}"`
- `landing_page.workflow` = `"html"`
- `landing_page.generated_at` = current ISO 8601 timestamp

### H11. Report

```
Landing Page Generated (HTML) — {campaign.name}

Template: {template}
Output: data/landing-pages/{campaign_id}/index.html
Status: generated

Substitutions applied:
- Headline: {headline}
- Benefits: {benefit_count} items
- Social proof: {social_proof_count} items
- Form fields: {field_count} fields
- Form action: {form_action or "not set"}
- Tracking: placeholder present (run [ST] to inject)

Next: Run [ST] to inject tracking codes, then [PV] to preview.
```

---

## Error Handling

- If template file is missing (HTML workflow), report which template was expected and where
- If template_repo directory does not exist (React workflow), report the expected path and ask user to verify
- If landing_page_copy is incomplete, list missing fields and ask user to populate them
- If form_webhook_url is not set, warn but proceed with `action="#"` — can be updated later
- If `npm install` fails (React workflow), report the error and suggest checking Node.js/npm installation
