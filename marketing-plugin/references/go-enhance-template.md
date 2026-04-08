# go-enhance Landing Page Template Reference

## Overview

The `go-enhance` template is a React-based landing page stored at `marketing-plugin/templates/landing-pages/go-enhance/`. It includes real social proof (testimonials, speaking events, case studies, team profiles) baked in, so new campaigns only need to swap campaign-specific content.

**Stack:** React 18 + TypeScript + Vite + Tailwind CSS + shadcn-ui + Recharts

## How to Fork for a New Campaign

```
1. Copy templates/landing-pages/go-enhance/ → data/landing-pages/{campaign_id}/
2. Swap campaign-specific components (see below)
3. Update tracking IDs (GA4 + Meta Pixel)
4. npm install && npm run dev → preview
5. npm run build → deploy
```

## Section Order

```
Header
Hero (VSL video + dual CTA)
Testimonials ({TESTIMONIAL_NAME} video + 2 Upwork reviews)
Stats (4 KPI cards)
ValueProposition (5 benefits + CTA)
Portfolio (4 deliverable showcases)
ROICalculator (interactive sliders + chart)
SocialProof (proof wall + speaking + trust strip)
TeamCredibility (Adam + Patrick profiles)
CaseStudy ({CASE_STUDY_4} before/after)
FAQ (6-question accordion)
CTA (final push)
Footer
QualificationQuiz (modal overlay)
```

## Campaign-Specific Components (Swap Per Campaign)

These components contain content specific to the campaign product/offer:

| Component | File | What to Replace |
|-----------|------|-----------------|
| Hero | `Hero.tsx` | H1 headline, subheadline, guarantee text, VSL video URL (Cloudflare Stream), CTA button text |
| Stats | `Stats.tsx` | 4 KPI values, labels, descriptions, icons |
| ValueProposition | `ValueProposition.tsx` | 5 benefits with descriptions, section headline |
| Portfolio | `Portfolio.tsx` | 4 project cards (name, description, tags, result, image) |
| ROICalculator | `ROICalculator.tsx` | Slider ranges/defaults, calculation logic, assumption text, section headline |
| FAQ | `FAQ.tsx` | 6 Q&A pairs |
| QualificationQuiz | `QualificationQuiz.tsx` | 5 questions, answer options, qualification logic, booking URL (GHL widget), field mapping |
| CTA | `CTA.tsx` | Headline, subheadline, button text, trust indicator text |
| Header | `Header.tsx` | Logo, nav anchor links, CTA button text |
| Footer | `Footer.tsx` | Copyright text, legal links |

## Social Proof Components (Keep Across All Campaigns)

These components contain real, verified credibility content. They should NOT be replaced per campaign — they're the same across all landing pages:

| Component | File | Content |
|-----------|------|---------|
| Testimonials | `Testimonials.tsx` | {TESTIMONIAL_NAME} video testimonial (DealBuddi), CampaignCompassAI Upwork review, App Design Upwork review |
| SocialProof | `SocialProof.tsx` | 4 proof panels (Upwork, YouTube, Skool, Reviews), 3 speaking events (Africa AI, AAA Sydney, Podcast), trust strip (60+ reviews, 300+ projects, Trustpilot) |
| TeamCredibility | `TeamCredibility.tsx` | Adam profile (badges, speaking, stats), Patrick profile (certifications, bio, Upwork screenshot) |
| CaseStudy | `CaseStudy.tsx` | {CASE_STUDY_4} — $200K → $2M/year, 10x growth in 9 months |

**Image CDN:** All social proof images are hosted on R2 at `{YOUR_CDN_HOST}/`. No local assets needed.

## Tracking Configuration

Per campaign, update:

| Item | Location | What to Change |
|------|----------|----------------|
| GA4 | `index.html` | Replace `G-XXXXXXXXXX` measurement ID in gtag snippet |
| Meta Pixel | `src/components/MetaPixel.tsx` | Replace pixel ID string |
| Meta CAPI | `api/meta-capi.ts` | Replace pixel ID and access token |
| Booking URL | `QualificationQuiz.tsx` | Replace GHL widget booking URL |

## Infrastructure (Never Touch)

- `App.tsx`, `main.tsx` — routing shell
- `src/contexts/QuizContext.tsx` — quiz modal state
- `src/lib/analytics.ts` — GA4 event wrapper
- `src/lib/meta-events.ts` — Meta Pixel browser events
- `src/components/ui/` — 51 shadcn-ui Radix components
- `tailwind.config.ts`, `vite.config.ts` — build config
- `components.json` — shadcn-ui config
