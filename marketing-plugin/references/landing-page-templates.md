# Landing Page Templates

## Overview

Landing pages are template-driven, single-file HTML with inline CSS and tracking scripts. Templates live in `marketing-plugin/templates/landing-pages/` and use `{{double_braces}}` for variable substitution.

## Available Templates

| Template | File | Status | Use Case |
|----------|------|--------|----------|
| Lead Gen | `lead-gen.html` | Ready | Standard lead capture — headline, benefits, social proof, form |
| Webinar | `webinar.html` | TODO | Webinar registration — countdown, speaker bio, agenda |
| Case Study | `case-study.html` | TODO | Case study showcase — problem, solution, results, CTA |
| Quiz | `quiz.html` | TODO | Interactive quiz — multi-step, score reveal, gated results |

## Template Variable Reference

All templates support these core variables:

| Variable | Source | Description |
|----------|--------|-------------|
| `{{headline}}` | `creatives.landing_page_copy.headline` | Main H1 headline |
| `{{subheadline}}` | `creatives.landing_page_copy.subheadline` | Supporting text below headline |
| `{{benefits_html}}` | Generated from `creatives.landing_page_copy.benefits` | Benefits grid HTML |
| `{{social_proof_html}}` | Generated from `creatives.landing_page_copy.social_proof` | Testimonials/stats HTML |
| `{{cta_text}}` | `creatives.landing_page_copy.cta_text` | Button text (e.g., "Get Your Free Audit") |
| `{{form_action}}` | `lead_capture.form_webhook_url` | Form submission URL |
| `{{form_fields_html}}` | Generated from `creatives.landing_page_copy.form_fields` | Form input fields HTML |
| `{{campaign_name}}` | `campaign.name` | Used in page title |
| `{{utm_source}}` | `tracking.utm_source` | Default: "meta" |
| `{{utm_medium}}` | `tracking.utm_medium` | Default: "paid" |
| `{{utm_campaign}}` | `tracking.utm_campaign` | Kebab-case campaign identifier |

## Component Reference

Components live in `templates/landing-pages/components/`:

### `tracking.html`

Injected in place of `<!-- TRACKING_SCRIPTS -->` in the template. Contains:
- GA4 gtag.js with `{{ga4_measurement_id}}`
- Meta Pixel with `{{meta_pixel_id}}`
- UTM parameter capture (sessionStorage)
- Form submission event handlers (GA4 generate_lead + Meta Lead)
- Conversions API placeholder comment

### `form.html`

Reusable form component with:
- `{{form_fields_html}}` placeholder
- Hidden UTM parameter fields
- Submit button with `{{cta_text}}`
- Loading state on submit
- Error display

## Brand Colours (CSS Variables)

```css
:root {
  --brand-primary: #1B2A4A;    /* Deep Navy */
  --brand-accent: #3B82F6;     /* Electric Blue */
  --brand-lime: #7DFF00;       /* Green */
  --brand-bg: #0F1923;         /* Dark background */
  --brand-surface: #162231;    /* Card/surface background */
}
```

## React-Based Templates (go-enhance)

For richer landing pages, the pipeline supports forking a React app instead of filling an HTML template. The source repo is specified via `landing_page.template_repo` in campaign-data.json.

### go-enhance Template

| Field | Value |
|-------|-------|
| Template name | `go-enhance` |
| Source | `marketing-plugin/templates/landing-pages/go-enhance/` |
| Stack | React 18 + TypeScript + Vite + Tailwind CSS + shadcn-ui + Recharts |
| Deploy target | Vercel (vercel.json) or Cloudflare Pages (static build) |
| Full reference | `references/go-enhance-template.md` |

**Page structure (src/pages/Index.tsx):**

```
Header → Hero (VSL video + CTA) → Testimonials (real — {TESTIMONIAL_NAME} + Upwork)
→ Stats → ValueProposition → Portfolio → ROICalculator
→ SocialProof (proof wall + speaking + trust strip)
→ TeamCredibility (Adam + Patrick) → CaseStudy ({CASE_STUDY_4})
→ FAQ → CTA → Footer → QualificationQuiz (modal overlay)
```

**Components fall into two categories:**

*Campaign-specific (swap per campaign):*

| Component | File | What to Change |
|-----------|------|----------------|
| Hero | `src/components/Hero.tsx` | Headline, subheadline, VSL video URL, CTA button text |
| Stats | `src/components/Stats.tsx` | Replace with campaign metrics (e.g., "200 → 20 hours") |
| ValueProposition | `src/components/ValueProposition.tsx` | Replace with campaign benefits |
| ROICalculator | `src/components/ROICalculator.tsx` | Adapt calculator inputs/logic for campaign product |
| QualificationQuiz | `src/components/QualificationQuiz.tsx` | Replace questions, qualification criteria, booking URL |
| Portfolio | `src/components/Portfolio.tsx` | Replace with demo screenshots or prototype embed |
| FAQ | `src/components/FAQ.tsx` | Replace with campaign-specific Q&A |
| CTA | `src/components/CTA.tsx` | Update CTA text and description |
| Header | `src/components/Header.tsx` | Update logo, nav links |
| Footer | `src/components/Footer.tsx` | Update links, legal text |

*social proof (keep across all campaigns):*

| Component | File | Content |
|-----------|------|---------|
| Testimonials | `src/components/Testimonials.tsx` | {TESTIMONIAL_NAME} video + real Upwork reviews |
| SocialProof | `src/components/SocialProof.tsx` | Proof wall, speaking events, trust strip |
| TeamCredibility | `src/components/TeamCredibility.tsx` | Adam + Patrick profiles |
| CaseStudy | `src/components/CaseStudy.tsx` | {CASE_STUDY_4} before/after |

**What to reuse as-is:**
- Page shell and routing (`App.tsx`, `main.tsx`)
- Quiz modal interaction pattern (progress bar, option selection, qualification logic)
- Analytics infrastructure (`src/lib/analytics.ts`, `src/lib/meta-events.ts`)
- MetaPixel component (`src/components/MetaPixel.tsx`)
- Tailwind config and shadcn-ui components (`src/components/ui/`)
- All dependencies and build config
- All social proof components (listed above)

**Tracking configuration:**
- GA4: update measurement ID in `index.html` gtag snippet
- Meta Pixel: update pixel ID in `src/components/MetaPixel.tsx`
- UTM capture: already built into the quiz and analytics lib

### go-enhance Generation Flow

```
campaign-data.json (campaign config)
    ↓
[GL] Fork source repo to data/landing-pages/{campaign_id}/
    ↓
Swap component content using campaign landing_page_copy + product + audience data
    ↓
[ST] Update GA4 measurement ID and Meta Pixel ID in source files
    ↓
[PV] npm run dev → preview locally at localhost:8080
    ↓
[DL] npm run build → deploy dist/ to Vercel or Cloudflare Pages
    ↓
Output: live at {landing_page.full_url}
```

## How to Add a New HTML Template

1. Create `templates/landing-pages/{name}.html`
2. Use the same `{{variable}}` placeholders as the lead-gen template
3. Include `<!-- TRACKING_SCRIPTS -->` in the `<head>` for tracking injection
4. Use the CSS variable system for brand colours
5. Ensure the template is self-contained (inline CSS, no external stylesheets)
6. Include Inter font from Google Fonts
7. Make it mobile-responsive (test at 375px width)
8. Add the template to campaign-data-schema.md `landing_page.template` enum
9. Document it in this file

## HTML Template Generation Flow

```
campaign-data.json (campaign config)
    ↓
generate-landing-page.py --campaign-id {id}
    ↓
Load template: templates/landing-pages/{template}.html
    ↓
Substitute {{variables}} from campaign config
    ↓
Inject tracking from components/tracking.html (if IDs present)
    ↓
Output: data/landing-pages/{campaign_id}/index.html
```
