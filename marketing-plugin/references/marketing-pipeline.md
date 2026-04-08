# Marketing Pipeline

## Overview

The marketing pipeline is a closed-loop system for running Meta ad campaigns end-to-end: plan campaigns, generate intelligence-driven creatives, build and deploy landing pages, launch Meta campaigns programmatically, monitor performance, retire losers, and iterate on winners. Eight agents work together with four central JSON data stores.

**Safety principles:**
- All Meta campaign creation uses `--dry-run` by default — must explicitly pass `--execute`
- Campaigns are always created in PAUSED state — human approval required before activation
- Five approval gates before any money is spent or anything goes public
- API-created campaigns are isolated from existing manual campaigns

## Pipeline Flow

```
PLAN (Agent 6 — Campaign Planner)
  [NC] Define product + audience + buying triggers → campaign-data.json (status: planning)
  [MR] Generate market intelligence report → reports/campaigns/{id}/
  [CS] Build creative strategy + landing page copy → campaign-data.json (status: build)
  ═══ APPROVAL GATE 1: Campaign Plan ═══

BUILD + CREATE (parallel — run both tracks after Gate 1)

  Track A: Landing Page (Agent 8 [GA] + Agent 7)
    [GA] Setup GA4 property + data streams (uses planned domain — no live site needed)
    [GL] Generate landing page from campaign config (HTML template or go-enhance fork)
    [ST] Inject GA4 + Meta Pixel + CAPI tracking code (uses IDs from [GA])
    [SD] Setup subdomain via Cloudflare API
    [DL] Deploy to Cloudflare Pages
    [PV] Preview and verify
    ═══ APPROVAL GATE 3: Landing Page Review ═══
    [LC] Setup lead capture webhook → CRM routing

  Track B: Creatives (Agent 5 — runs in parallel with Track A)
    [BA --campaign-id X] Build angles from campaign intelligence → creative-data.json batch
    [GI] Generate images → data/creatives/{batch_id}/
    [GV] Generate videos → data/creatives/{batch_id}/
    [PC] Package creatives with UTMs
    ═══ APPROVAL GATE 2: Creative Review ═══

LAUNCH (Agent 8 — needs both tracks complete)
  [UC] Upload creatives to Meta → get creative IDs
  [MC] Create Meta campaign structure (campaign → ad sets → ads, all PAUSED)
  ═══ APPROVAL GATE 4: Go-Live (budget confirmation) ═══
  [GO] Activate campaign → status: live

MONITOR + ITERATE (ongoing closed loop)
  Agent 1 [PM] → Pull campaign data (auto-discovers new campaign)
  Agent 2 [CS/AS/QR] → Analyze performance
  Agent 3 [FO] → Map funnels (with landing page data)
  Agent 6 [PR] → Campaign-segregated performance review
    → Retire losers: mark retired, recommend pausing in Meta
    → Extract winner patterns: inform next creative batch
    → Agent 8 [RA] → Pause losing ads in Meta
    ═══ APPROVAL GATE 5: Ad Retirement ═══
    → Agent 5 [BA] → New angles informed by winners
    → Repeat CREATE → LAUNCH cycle for new creatives

INTELLIGENCE (ongoing, feeds into PLAN)
  Agent 4 [SC] → Scrape competitor Meta ads via Apify → competitor-data.json
  Agent 4 [DA/AC/TW] → Download, analyse, and track competitor winners

ARCHIVE (monthly or when data exceeds 2MB)
  archive-old-insights.py → move 90+ day insights to yearly archive files
```

**Note on parallel tracks:** Track A (landing page) and Track B (creatives) have no dependency on each other. Either can start first. The LAUNCH phase is the merge point — it requires the landing page URL (from Track A) and uploaded creatives (from Track B). GA4 moves to the start of Track A so measurement IDs are available when tracking is injected into the landing page.

**Landing page templates:** For React-based templates (e.g., `go-enhance`), [GL] forks the source repo and swaps component content. See `references/landing-page-templates.md` for details.

## Closed-Loop Data Flow

```
                        ┌────────────────────────────────────────────────────────┐
                        │                                                        │
                        ▼                                                        │
  Campaign Planner [NC/MR/CS]                                                    │
        │                                                                        │
        ▼                                                                        │
  campaign-data.json ────────► Campaign Launcher [MC/UC/GO]                      │
        │                          │                                             │
        │                          ▼                                             │
        │                    Meta Ads (campaigns created PAUSED → activated)      │
        │                          │                                             │
        │                          ▼                                             │
  Campaign Collector [PM]    (auto-discovers new campaigns)                      │
        │                                                                        │
        ▼                                                                        │
  marketing-data.json ──────► Performance Analyst [CS/AS/QR]                     │
        │                          │                                             │
        │                          ▼                                             │
        │                    Campaign Planner [PR] ─── performance review ───────┤
        │                          │                                             │
        │                          ├── retire losers → Campaign Launcher [RA]    │
        │                          └── winner patterns ─┐                        │
        │                                               │                        │
  Competitor Intel [SC/DA/AC/TW]                        │                        │
        │                                               │                        │
        ▼                                               ▼                        │
  competitor-data.json ─────────► Creative Generator [BA] (informed by winners)  │
        │                              │                                         │
        │                              ▼                                         │
        │                    Creative Generator [GI/GV/PC]                       │
        │                              │                                         │
        │                              ▼                                         │
        │                    creative-data.json ─► Upload to Meta ───────────────┘
        │                              │
        │                              ▼
        │                    Landing Page Builder [GL/ST/DL]
        │                              │
        │                              ▼
        │                    data/landing-pages/{campaign_id}/
        │
        ▼
  Funnel Mapper [FO] ─── links ad clicks → landing page → conversions
```

## Agent Capability Matrix

| Agent | Code | Capability | Input | Output |
|-------|------|-----------|-------|--------|
| Campaign Collector | PM | Pull Meta | Meta Marketing API | marketing-data.json |
| Campaign Collector | DA | Discover Accounts | Meta Marketing API | meta_ad_account_id |
| Performance Analyst | CS | Campaign Summary | marketing-data.json | Structured summary |
| Performance Analyst | AS | Ad Set Breakdown | marketing-data.json | Comparative analysis |
| Performance Analyst | QR | Query | marketing-data.json | Answer |
| Funnel Mapper | FO | Funnel Overview | marketing-data.json + GA4 | Funnel report |
| Competitor Intelligence | SC | Scrape Competitors | Apify + watchlist | competitor-data.json |
| Competitor Intelligence | DA | Download Assets | competitor-data.json | competitor-assets/ |
| Competitor Intelligence | AC | Analyse Creatives | Assets + Gemini Flash | competitor-data.json analysis |
| Competitor Intelligence | TW | Track Winners | competitor-data.json | Winner leaderboard |
| Competitor Intelligence | MC | Manage Competitors | User input | competitor-data.json watchlist |
| Creative Generator | BA | Build Angles | All data files + market intel + campaign context | creative-data.json angles |
| Creative Generator | GI | Generate Images | Angles + templates + brand guide | creatives/ images |
| Creative Generator | GV | Generate Videos | Angles + motion patterns | creatives/ videos |
| Creative Generator | PC | Package Creatives | creative-data.json | UPLOAD-GUIDE.md |
| Creative Generator | LP | Link Performance | User input + marketing-data.json | creative-data.json snapshots |
| Campaign Planner | NC | New Campaign | User input | campaign-data.json entry |
| Campaign Planner | MR | Market Report | competitor-data.json + web research | Market intelligence report |
| Campaign Planner | CS | Campaign Strategy | Intelligence report | Creative strategy + landing page copy |
| Campaign Planner | SC | Campaign Status | campaign-data.json | Dashboard of all campaigns |
| Campaign Planner | PR | Performance Review | marketing-data.json + creative-data.json + campaign-data.json | Retire losers, flag winners |
| Landing Page Builder | GL | Generate Landing | campaign-data.json + templates | data/landing-pages/ |
| Landing Page Builder | DL | Deploy Landing | Generated HTML | Cloudflare Pages |
| Landing Page Builder | SD | Setup Domain | Cloudflare API | CNAME record for subdomain |
| Landing Page Builder | ST | Setup Tracking | campaign-data.json tracking config | GA4 + Pixel + CAPI injection |
| Landing Page Builder | PV | Preview Landing | Generated HTML | Local preview |
| Campaign Launcher | MC | Meta Campaign | campaign-data.json + creative-data.json | Meta campaign/adset/ads (PAUSED) |
| Campaign Launcher | UC | Upload Creatives | creative-data.json asset paths | Meta creative IDs |
| Campaign Launcher | GA | Setup GA4 | GA4 Admin API | Property + data streams |
| Campaign Launcher | LC | Lead Capture | Cloudflare Workers | Webhook → CRM routing |
| Campaign Launcher | RA | Retire Ads | Performance review results | Pause ads in Meta |
| Campaign Launcher | GO | Go Live | All components ready | Activate campaigns (PAUSED → ACTIVE) |
| VSL Generator | VA | VSL Angles | Offer + pricing + market intel | vsl-data.json angles |
| VSL Generator | GS | Generate Script | Selected angle + pricing + brand guidelines | content/standalone/ script |
| VSL Generator | GE | Edit Instructions | Generated script + pacing rules | content/standalone/ edit-instructions |

## Data Files

| File | Purpose |
|------|---------|
| `data/campaign-data.json` | Campaign registry — product, audience, tracking, Meta campaign IDs, approval log |
| `data/marketing-data.json` | Source of truth — campaigns, ad sets, ads, creative content, daily insights |
| `data/competitor-data.json` | Competitor ad intelligence — watchlist, scraped ads, analysis |
| `data/creative-data.json` | Generated creatives — batches, angles, copy variants, assets, performance |
| `data/landing-pages/` | Generated landing page HTML files organised by campaign |
| `data/archive/` | Archived insights (90+ days old, aggregated to weekly) |
| `data/competitor-assets/` | Downloaded competitor creative files |
| `data/creatives/` | Generated image and video assets organised by batch |

## Campaign-Segregated Performance Loop

The self-improving iteration loop for each campaign:

1. **Pull** — Agent 1 [PM] fetches all campaigns from Meta (unchanged)
2. **Review** — Agent 6 [PR] for a specific campaign:
   - Filters marketing-data.json insights by this campaign's Meta campaign_id
   - Maps each ad back to its angle via creative-data.json `meta_ad_ids`
   - Scores: spend, CPA, CTR, ROAS per angle
   - Compares against `auto_retire_threshold` in campaign config
   - Outputs: winner angles, loser angles, patterns, recommendations
3. **Retire** — Agent 8 [RA] pauses losing ads in Meta (with approval)
4. **Iterate** — Agent 5 [BA --campaign-id] generates new angles:
   - Replicating winner frameworks/hooks/visual styles
   - Avoiding loser patterns
   - Filling gaps identified in review
5. **Deploy** — New creatives uploaded and added to existing campaign
6. **Track** — `iteration_count` increments, `performance_history` grows

## Approval Gates

| Gate | When | What User Sees |
|------|------|----------------|
| Campaign Plan | After NC+MR+CS | Product, audience, strategy, landing page copy |
| Creative Review | After BA+GI+GV | All angles, copy variants, image/video previews |
| Landing Page | After GL+ST+PV | Local preview, tracking verification, form test |
| Go-Live | After MC (dry-run) | Campaign structure, daily budget, 7/30-day cost estimate |
| Ad Retirement | After PR review | List of ads to pause with performance data and reasoning |

## Reference Files

| File | Purpose |
|------|---------|
| `references/campaign-data-schema.md` | Schema for campaign-data.json |
| `references/marketing-data-schema.md` | Schema for marketing-data.json |
| `references/competitor-data-schema.md` | Schema for competitor-data.json |
| `references/creative-data-schema.md` | Schema for creative-data.json |
| `references/landing-page-templates.md` | Landing page template system documentation |
| `references/meta-campaign-creation-api.md` | Meta Marketing API write endpoints |
| `references/cloudflare-domain-api.md` | Cloudflare DNS and Pages domain API |
| `references/image-prompt-templates.md` | 8 structured templates for image generation |
| `references/video-prompt-templates.md` | 7 motion patterns + model selection guide |
| `references/brand-guidelines.md` | Brand colours, tone, restrictions for all creative gen |
| `references/meta-marketing-api.md` | Meta Marketing API endpoint reference (read) |
| `references/apify-facebook-ads-library.md` | Apify actor API reference |
| `references/fal-ai-video-api.md` | fal.ai video generation API reference |
| `references/openrouter-image-api.md` | OpenRouter image generation API reference |

## What's Next Table

| Just Finished | Recommend Next |
|---------------|----------------|
| Campaign Planner [NC] | Campaign Planner [MR] then [CS] |
| Campaign Planner [CS] | **Start both tracks in parallel:** Track A: Campaign Launcher [GA] then Landing Page Builder [GL]. Track B: Creative Generator [BA --campaign-id]. |
| Campaign Launcher [GA] | Landing Page Builder [GL] |
| Landing Page Builder [GL] | Landing Page Builder [ST] then [PV] |
| Landing Page Builder [PV] (approved) | Landing Page Builder [SD] then [DL] |
| Landing Page Builder [DL] | Campaign Launcher [LC]. If Track B complete: Campaign Launcher [UC]. |
| Campaign Launcher [LC] | If Track B complete: Campaign Launcher [UC]. Otherwise: wait for creatives. |
| Creative Generator [BA] | Creative Generator [GI] then [GV] then [PC] |
| Creative Generator [PC] | If Track A complete: Campaign Launcher [UC]. Otherwise: wait for landing page. |
| Campaign Launcher [UC] | Campaign Launcher [MC] |
| Campaign Launcher [MC] (approved) | Campaign Launcher [GO] |
| Campaign Launcher [GO] | Campaign Collector [PM] (after 7+ days) |
| Campaign Collector [PM] | Campaign Planner [PR] |
| Campaign Planner [PR] | Campaign Launcher [RA] then Creative Generator [BA] (next iteration) |
| Competitor Intelligence [SC] | Competitor Intelligence [DA] then [AC] then [TW] |
| Competitor Intelligence [TW] | Campaign Planner [MR] or Creative Generator [BA] |
| VSL Generator [VA] | VSL Generator [GS] |
| VSL Generator [GS] | VSL Generator [GE] |
| VSL Generator [GE] | Record VSL, then vid-1 [VE] with edit instructions |

## Typical Campaign Lifecycle

1. **Week 0 — Plan:** Create campaign [NC], build intelligence [MR], set strategy [CS]
2. **Week 0 — Build + Create (parallel):**
   - Track A: Setup GA4 [GA], generate landing page [GL], inject tracking [ST], preview [PV], setup domain [SD], deploy [DL], lead capture [LC]
   - Track B: Generate angles [BA], images [GI], videos [GV], package [PC]
3. **Week 0 — Launch:** Upload creatives [UC], create Meta campaign [MC], go live [GO]
4. **Week 1+ — Monitor:** Pull data [PM], review performance [PR]
5. **Week 2+ — Iterate:** Retire losers [RA], generate new angles [BA], upload new creatives [UC]
6. **Ongoing:** Repeat steps 4-5 every review cadence (default 7 days)
