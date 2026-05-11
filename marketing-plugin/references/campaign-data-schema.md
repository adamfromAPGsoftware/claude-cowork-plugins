# Campaign Data Schema

## Location

`marketing-plugin/data/campaign-data.json` — campaign registry and orchestration hub for managing multiple marketing campaigns end-to-end.

## Top-Level Structure

```json
{
  "meta": {
    "last_created": "ISO 8601 timestamp of last campaign creation",
    "total_campaigns": 0
  },
  "campaigns": [ ... ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| meta.last_created | Yes | Timestamp of most recent campaign creation (null if none) |
| meta.total_campaigns | Yes | Count of campaigns |
| campaigns | Yes | Array of campaign objects |

## Campaign

```json
{
  "campaign_id": "camp-YYYY-MM-DD-NNN",
  "name": "Human-readable campaign name",
  "status": "draft | planning | creatives | landing_page | review | live | paused | completed",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601",

  "product": { ... },
  "audience": { ... },
  "intelligence": { ... },
  "creatives": { ... },
  "performance": { ... },
  "landing_page": { ... },
  "tracking": { ... },
  "meta_campaign": { ... },
  "lead_capture": { ... },
  "approval_log": [ ... ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| campaign_id | Yes | Unique identifier. Format: `camp-YYYY-MM-DD-NNN`. **Dedup key.** |
| name | Yes | Human-readable campaign name |
| status | Yes | Current pipeline stage |
| created_at | Yes | When the campaign was created |
| updated_at | Yes | Last modification timestamp |

## Status Progression

```
draft → planning → creatives → landing_page → review → live → paused → completed
```

- `draft` — Campaign entry created, product/audience being defined
- `planning` — Market report and creative strategy in progress
- `creatives` — Angles and creative assets being generated
- `landing_page` — Landing page being built and deployed
- `review` — All components ready, awaiting go-live approval
- `live` — Campaign active in Meta, performance being monitored
- `paused` — Campaign temporarily paused (manual or auto)
- `completed` — Campaign ended, archived for reference

## Product

```json
{
  "name": "string",
  "description": "string — what this product/service does",
  "price": "string — e.g. '$3,000'",
  "offer_details": "string — what the prospect gets",
  "guarantee": "string — risk reversal (e.g. '$5K+/month savings or full refund')",
  "usp": ["string — unique selling propositions"]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Product or service name |
| description | Yes | What it does, who it's for |
| price | No | Price point (may not be public) |
| offer_details | No | What's included in the offer |
| guarantee | No | Risk reversal or guarantee statement |
| usp | No | Array of unique selling propositions |

## Audience

```json
{
  "icp_description": "string — ideal customer profile narrative",
  "pain_points": ["string"],
  "aspirations": ["string"],
  "buying_triggers": ["string — what makes them act NOW"],
  "industries": ["string"],
  "locations": ["string — country codes or region names"],
  "age_range": "string — e.g. '30-55'",
  "custom_audience_ids": ["string — Meta custom audience IDs"]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| icp_description | Yes | Narrative description of ideal customer |
| pain_points | Yes | What keeps them up at night |
| aspirations | Yes | What they want to achieve |
| buying_triggers | No | Events or conditions that trigger purchase decisions |
| industries | No | Target industry verticals |
| locations | Yes | Geographic targeting |
| age_range | No | Age range for targeting |
| custom_audience_ids | No | Meta Custom Audience IDs for targeting |

## Intelligence

```json
{
  "market_report_path": "string — path to market-intelligence.md or null",
  "competitor_winner_ids": ["string — ad_ids from competitor-data.json"],
  "own_winner_angle_ids": ["string — angle_ids from creative-data.json"],
  "key_themes": ["string — market themes and trends"],
  "activation_opportunities": ["string — gaps and opportunities identified"]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| market_report_path | No | Path to the market intelligence report for this campaign |
| competitor_winner_ids | No | Competitor ad IDs that informed this campaign's strategy |
| own_winner_angle_ids | No | Own winning angles from previous campaigns to replicate |
| key_themes | No | Key market themes driving this campaign |
| activation_opportunities | No | Gaps and opportunities the campaign aims to exploit |

## Creatives

```json
{
  "batch_ids": ["string — batch IDs from creative-data.json"],
  "active_angle_ids": ["string — currently running angle IDs"],
  "retired_angle_ids": ["string — retired/stopped angle IDs"],
  "landing_page_copy": {
    "headline": "string",
    "subheadline": "string",
    "benefits": ["string"],
    "social_proof": ["string — testimonials, stats, logos"],
    "cta_text": "string — e.g. 'Get Your Free Audit'",
    "form_fields": ["string — e.g. 'name', 'email', 'phone', 'company'"]
  },
  "creative_brief": {
    "budget_tier": "testing | testing_plus | validated | scaling | aggressive",
    "daily_budget": 50,
    "prescribed_angles": 4,
    "images_per_angle": 1,
    "videos_per_angle": 1,
    "total_prescribed_images": 4,
    "total_prescribed_videos": 4,
    "primary_aspect": "3:4",
    "stories_aspect": "9:16",
    "format_split": "55% image / 45% video",
    "refresh_cadence_days": 12,
    "testing_budget_pct": 20,
    "derived_from": "creative-testing-framework.md"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| batch_ids | Yes | Linked creative batch IDs (from creative-data.json) |
| active_angle_ids | Yes | Angles currently running in Meta |
| retired_angle_ids | Yes | Angles retired due to poor performance |
| landing_page_copy | No | Copy for the campaign landing page (populated by CS capability) |
| creative_brief | No | Andromeda-backed creative production prescription — populated by [CS] Campaign Strategy. Specifies how many angles, images, videos, and formats to produce based on daily budget. Creator [GI]/[GV] reads this to show production targets. |

### creative_brief Fields

| Field | Description |
|-------|-------------|
| budget_tier | Tier classification from `creative-testing-framework.md` |
| daily_budget | Daily budget in dollars (from meta_campaign.daily_budget) |
| prescribed_angles | Number of distinct creative angles to produce |
| images_per_angle | Images to generate per angle (primary Feed aspect) |
| videos_per_angle | Videos to generate per angle (9:16 Reels/Stories) |
| total_prescribed_images | prescribed_angles × images_per_angle |
| total_prescribed_videos | prescribed_angles × videos_per_angle |
| primary_aspect | Primary image format — always "3:4" (Feed portrait) |
| stories_aspect | Video/Stories format — always "9:16" |
| format_split | Descriptive split e.g. "55% image / 45% video" |
| refresh_cadence_days | Days between creative refresh cycles |
| testing_budget_pct | Percentage of budget allocated to new creative tests (default 20) |
| derived_from | Source reference (always "creative-testing-framework.md") |

## Performance

```json
{
  "last_review": "ISO 8601 | null",
  "review_cadence_days": 7,
  "phase": "learning | evaluation | optimization",
  "phase_start_date": "ISO 8601 | null",
  "optimization_events_count": 0,
  "auto_retire_threshold": {
    "min_spend": 50,
    "min_days": 7,
    "max_cpa": null,
    "min_roas": null,
    "min_ctr": 0.5
  },
  "iteration_count": 0,
  "performance_history": [
    {
      "date": "ISO 8601",
      "spend": 0,
      "leads": 0,
      "cpa": 0,
      "roas": 0,
      "best_angle": "string — angle_id",
      "worst_angle": "string — angle_id",
      "active_angles": 0,
      "retired_this_review": 0
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| last_review | Yes | When the last performance review was run (null if never) |
| review_cadence_days | Yes | How often to review (default 7 days) |
| phase | No | Current campaign phase (default: learning). See `performance-optimization-playbook.md` for phase definitions and evaluation rules |
| phase_start_date | No | When the current phase began (ISO 8601). Set to campaign activation date initially, updated on phase transitions |
| optimization_events_count | No | Number of optimization events (conversions) accumulated. Learning phase ends at 50 events |
| auto_retire_threshold | Yes | Thresholds for auto-retiring underperforming angles |
| auto_retire_threshold.min_spend | Yes | Minimum spend before evaluating (don't retire too early) |
| auto_retire_threshold.min_days | Yes | Minimum days active before evaluating |
| auto_retire_threshold.max_cpa | No | Maximum cost per acquisition (retire if CPA exceeds this) |
| auto_retire_threshold.min_roas | No | Minimum ROAS (retire if below this) |
| auto_retire_threshold.min_ctr | No | Minimum CTR percentage (retire if below this) |
| iteration_count | Yes | How many creative iteration cycles have been completed |
| performance_history | Yes | Array of performance snapshots from each review |

## Landing Page

```json
{
  "status": "not_started | generated | deployed | live",
  "template": "lead-gen | webinar | case-study | quiz | go-enhance",
  "template_repo": "string | null — path to source repo for React-based templates (e.g. ~/Documents/Repositories/go-enhance)",
  "domain": "string — e.g. 'audit.{YOUR_DOMAIN}'",
  "path": "string — e.g. '/' or '/offer'",
  "full_url": "string — e.g. 'https://audit.{YOUR_DOMAIN}/'",
  "deploy_path": "string — local path to generated files",
  "generated_at": "ISO 8601 | null",
  "deployed_at": "ISO 8601 | null"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| status | Yes | Current state of the landing page |
| template | Yes | Which template was used. `go-enhance` = React app fork (see landing-page-templates.md) |
| template_repo | No | Absolute path to source repo when using a React-based template. If set, [GL] forks this repo instead of using the HTML template. |
| domain | Yes | Subdomain of {YOUR_DOMAIN} (primary approach) |
| path | No | Path on the domain (default "/") |
| full_url | No | Complete URL (computed from domain + path) |
| deploy_path | No | Local path to generated landing page files |
| generated_at | No | When the landing page HTML was generated |
| deployed_at | No | When deployed to Cloudflare Pages |

## Tracking

```json
{
  "ga4_property_id": "string | null",
  "ga4_measurement_id": "string | null",
  "ga4_api_secret": "string | null",
  "meta_pixel_id": "string | null",
  "meta_capi_token": "string | null",
  "utm_source": "meta",
  "utm_medium": "paid",
  "utm_campaign": "string — kebab-case campaign identifier",
  "conversions_api_enabled": false
}
```

| Field | Required | Description |
|-------|----------|-------------|
| ga4_property_id | No | GA4 property ID for this campaign's domain |
| ga4_measurement_id | No | GA4 measurement ID (e.g. G-XXXXXXXXXX) |
| ga4_api_secret | No | GA4 Measurement Protocol API secret (for server-side events) |
| meta_pixel_id | No | Meta Pixel ID for tracking |
| meta_capi_token | No | Meta Conversions API access token |
| utm_source | Yes | UTM source parameter (default: "meta") |
| utm_medium | Yes | UTM medium parameter (default: "paid") |
| utm_campaign | Yes | UTM campaign parameter (kebab-case) |
| conversions_api_enabled | Yes | Whether server-side CAPI is active |

## Meta Campaign

```json
{
  "status": "not_created | pending_approval | created | active | paused",
  "campaign_id": "string | null — Meta campaign ID",
  "ad_set_ids": ["string — Meta ad set IDs"],
  "ad_ids": ["string — Meta ad IDs"],
  "daily_budget": 0,
  "objective": "OUTCOME_LEADS | OUTCOME_TRAFFIC | OUTCOME_AWARENESS | OUTCOME_SALES | OUTCOME_ENGAGEMENT",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP | COST_CAP | BID_CAP | MINIMUM_ROAS",
  "campaign_budget_optimization": false,
  "budget_tier": "testing | validated | scaling",
  "advantage_plus": false,
  "approved_at": "ISO 8601 | null",
  "approved_by": "string | null"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| status | Yes | Current state of the Meta campaign |
| campaign_id | No | Meta campaign ID (populated after creation) |
| ad_set_ids | No | Meta ad set IDs (populated after creation) |
| ad_ids | No | Meta ad IDs (populated after creation) |
| daily_budget | Yes | Daily budget in cents (Meta API format) |
| objective | Yes | Campaign objective (must use OUTCOME_* format) |
| bid_strategy | No | Bidding strategy (default: LOWEST_COST_WITHOUT_CAP). See `campaign-setup-strategy.md` for selection guidance |
| campaign_budget_optimization | No | Whether CBO is enabled at campaign level (default: false = ABO). When true, daily_budget is set on the campaign, not individual ad sets |
| budget_tier | No | Budget tier classification for strategy reference (testing/validated/scaling). See `campaign-setup-strategy.md` |
| advantage_plus | No | Whether Advantage+ is intentionally enabled (default: false). When true, CBO + broad targeting + all placements are configured |
| approved_at | No | When the campaign was approved for creation |
| approved_by | No | Who approved it |

## Lead Capture

```json
{
  "form_webhook_url": "string | null — Cloudflare Worker endpoint",
  "crm_pipeline": "string — CRM pipeline name",
  "auto_create_lead": true,
  "notification_email": "string"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| form_webhook_url | No | Webhook URL for form submissions |
| crm_pipeline | Yes | Which CRM pipeline to create leads in |
| auto_create_lead | Yes | Whether to auto-create CRM leads on form submission |
| notification_email | Yes | Email to notify on new leads |

## Funnel

Configures the inline qualification funnel on the landing page. When `enabled: true`, the generate-landing-page.py script replaces the standard form with a multi-step question flow. Qualifying visitors see a Cal.com booking calendar inline; disqualified visitors see an alternative offer.

When `enabled: false` or the `funnel` key is absent, the standard form is used unchanged.

```json
{
  "enabled": true,
  "heading": "See if we're a fit",
  "subtext": "Answer 3 quick questions — takes 30 seconds.",
  "questions": [
    {
      "id": "revenue",
      "label": "What's your approximate annual revenue?",
      "type": "slider",
      "required": true,
      "slider": {
        "min": 0,
        "max": 2000000,
        "step": 50000,
        "format": "currency",
        "currency": "AUD",
        "labels": ["$0", "$500K", "$1M", "$1.5M", "$2M+"]
      }
    },
    {
      "id": "intent",
      "label": "Are you ready to invest in improving your operations?",
      "type": "radio",
      "required": true,
      "options": [
        { "label": "Yes — actively looking", "value": "yes_active" },
        { "label": "Yes — still researching", "value": "yes_research" },
        { "label": "Not sure yet", "value": "unsure" },
        { "label": "No — just exploring", "value": "no" }
      ]
    }
  ],
  "qualification": {
    "logic": "all",
    "rules": [
      { "field": "revenue", "operator": "gte", "values": ["100000"] },
      { "field": "intent", "operator": "in", "values": ["yes_active", "yes_research"] }
    ]
  },
  "pass": {
    "action": "booking",
    "heading": "You're a great fit — book your free strategy call",
    "subtext": "Choose a time below. 30 minutes, no pressure.",
    "booking_embed": {
      "cal_link": "username/event-slug",
      "layout": "month_view",
      "theme": "dark",
      "brand_color": "#1B2A4A"
    }
  },
  "fail": {
    "action": "message",
    "heading": "Not quite the right fit — yet",
    "message": "Body text explaining the situation.",
    "alternative_offer": {
      "label": "Optional label above CTA",
      "url": "https://example.com",
      "cta_text": "CTA button text"
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `funnel.enabled` | Yes | When false, page uses standard form instead |
| `funnel.heading` | No | Section heading shown above the quiz |
| `funnel.subtext` | No | Supporting text below heading |
| `funnel.questions[].id` | Yes | Unique key — used in qualification rules |
| `funnel.questions[].label` | Yes | Question text shown to visitor |
| `funnel.questions[].type` | Yes | `radio` / `slider` / `checkbox` / `text` |
| `funnel.questions[].options[]` | For radio/checkbox | Array of `{ label, value }` pairs |
| `funnel.questions[].slider{}` | For slider | `{ min, max, step, format, currency, labels }` |
| `funnel.qualification.logic` | Yes | `all` (AND) or `any` (OR) across rules |
| `funnel.qualification.rules[].field` | Yes | Question id to evaluate |
| `funnel.qualification.rules[].operator` | Yes | See operator table below |
| `funnel.qualification.rules[].values` | Yes | Acceptable values for the rule |
| `funnel.pass.action` | Yes | `booking` (Cal.com embed) or `message` |
| `funnel.pass.booking_embed.cal_link` | For booking | `username/event-slug` — overrides `config.yaml booking` |
| `funnel.fail.alternative_offer` | No | Optional CTA card: `{ label, url, cta_text }` |

**Operator reference:**

| Operator | Description | Example |
|----------|-------------|---------|
| `in` | Answer value is in the values array | `{ "operator": "in", "values": ["yes_active", "yes_research"] }` |
| `not_in` | Answer value is NOT in values array | `{ "operator": "not_in", "values": ["no"] }` |
| `eq` | String equality | `{ "operator": "eq", "values": ["solo"] }` |
| `gte` | Numeric ≥ (slider answers) | `{ "operator": "gte", "values": ["100000"] }` |
| `lte` | Numeric ≤ (slider answers) | `{ "operator": "lte", "values": ["50"] }` |

Configure via: `/marketing:1-strategist` → `[CF]`

## Approval Log

```json
{
  "gate": "campaign_plan | creatives | landing_page | meta_campaign | go_live | ad_retirement",
  "status": "pending | approved | rejected",
  "timestamp": "ISO 8601",
  "notes": "string — approval notes or rejection reason"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| gate | Yes | Which approval gate this entry is for |
| status | Yes | Approval status |
| timestamp | Yes | When the approval decision was made |
| notes | No | Notes or reason for the decision |

## Linking to Other Data Files

Campaign data links to the other three data files:

| Link | How |
|------|-----|
| creative-data.json | `creatives.batch_ids` → `batches[].batch_id`. Batches also have optional `campaign_id` field. |
| marketing-data.json | `meta_campaign.campaign_id` → `meta.campaigns[].campaign_id` |
| competitor-data.json | `intelligence.competitor_winner_ids` → `ads[].ad_id` |

Campaign-data.json is the orchestration layer. The other three files remain independent and continue to work without campaigns.
