# Marketing Pipeline

## Overview

The marketing pipeline is a closed-loop system for running Meta ad campaigns end-to-end. Four agents cover the full lifecycle: plan and research, build and publish, monitor and iterate.

**Safety principles:**
- All Meta campaign creation uses `--dry-run` by default — must explicitly pass `--execute`
- Campaigns are always created in PAUSED state — human approval required before activation
- Approval gates before any money is spent or anything goes public
- API-created campaigns are isolated from existing manual campaigns

## Agents

| Agent | Role | When to use |
|-------|------|-------------|
| `0-setup` | Configure the plugin for your company | First run, or when updating credentials |
| `1-strategist` | Plan campaigns and research the market | Before building anything |
| `2-creator` | Build all assets and publish the campaign | After strategy is approved |
| `3-analyst` | Monitor performance and drive iteration | After campaign is live |

## Pipeline Flow

```
SETUP (Agent 0)
  [SW] Setup wizard → config.yaml (company, domains, brand, integrations)

PLAN + RESEARCH (Agent 1 — Strategist)
  [NC] Define product + audience + buying triggers → campaign-data.json (status: planning)
  [SC] Campaign status dashboard → all campaigns + pipeline state
  [MR] Generate market intelligence report
  [CS] Build creative strategy + landing page copy → campaign-data.json (status: build)
  [BT] Battle test angles against ICP personas → surface objections
  [CI] Competitor scan (bundled: scrape → download → analyse → summary)
  [TW] Track competitor winners (30+ day longevity leaderboard)
  [WL] Manage competitor watchlist

  ═══ APPROVAL GATE: Campaign Plan ═══

BUILD + PUBLISH (Agent 2 — Creator)

  AD CREATIVES
    [BA] Build angles from campaign intelligence + competitor winners
    [GI] Generate image creatives (9:16 + 1:1) via Nano Banana Pro
    [GV] Generate video creatives via Veo 3 / Kling
    [GS] Generate on-camera filmable scripts (real video shoots)
    [VS] Generate VSL (bundled: angles → full script → editor handoff)
    [AE] Generate ad-edit instructions for video editor pipeline
    [PC] Package creatives into Meta upload guide
    ═══ APPROVAL GATE: Creative Review ═══

  LANDING PAGE
    [GL] Generate landing page HTML from campaign config + template
    [PV] Preview and verify landing page
    [DP] Deploy page (bundled: setup domain → Cloudflare deploy → inject tracking)
    ═══ APPROVAL GATE: Landing Page Review ═══

  LAUNCH
    [UC] Upload creatives to Meta → store creative IDs
    [GO] Launch campaign (bundled: create Meta structure → lead capture worker → go live)
    ═══ APPROVAL GATE: Go-Live (budget confirmation) ═══

MONITOR + ITERATE (Agent 3 — Analyst)
  [PD] Pull data (bundled: fetch Meta + GA4 → merge into marketing-data.json)
  [AD] Discover all accessible Meta ad accounts
  [CS] Campaign summary — spend, CTR, CPC, CPA by campaign
  [AS] Ad breakdown — performance at ad set / ad level
  [QR] Freeform query against campaign data
  [FO] Funnel overview — spend → clicks → conversions
  [PR] Performance review → retire losers, flag winners, recommend next angles
  [CI] Competitor scan (same bundled workflow as Strategist)
  [TW] Track competitor winners
  ═══ APPROVAL GATE: Ad Retirement ═══

  → Retire losers: Creator [RA] pause losing ads in Meta
  → New creative batch: Creator [BA] informed by winner patterns
  → Repeat BUILD → LAUNCH cycle
```

## Closed-Loop Data Flow

```
                        ┌──────────────────────────────────────────────────┐
                        │                                                  │
                        ▼                                                  │
  Strategist [NC/MR/CS]                                                    │
        │                                                                  │
        ▼                                                                  │
  campaign-data.json ────────► Creator [UC/GO]                             │
        │                          │                                       │
        │                          ▼                                       │
        │                    Meta Ads (PAUSED → activated)                 │
        │                          │                                       │
        │                          ▼                                       │
  Analyst [PD]           (fetches all campaigns)                           │
        │                                                                  │
        ▼                                                                  │
  marketing-data.json ──────► Analyst [CS/AS/QR]                           │
        │                          │                                       │
        │                          ▼                                       │
        │                    Analyst [PR] ── performance review ───────────┤
        │                          │                                       │
        │                          ├── retire losers → Creator [RA]        │
        │                          └── winner patterns ─┐                  │
        │                                               │                  │
  Strategist/Analyst [CI]                               │                  │
        │                                               │                  │
        ▼                                               ▼                  │
  competitor-data.json ───────────► Creator [BA] (informed by winners)     │
                                        │                                  │
                                        ▼                                  │
                                Creator [GI/GV/PC]                         │
                                        │                                  │
                                        ▼                                  │
                                creative-data.json ── upload to Meta ──────┘
                                        │
                                        ▼
                                Creator [GL/DP]
                                        │
                                        ▼
                                data/landing-pages/{campaign_id}/
```

## Capability Matrix

### Agent 1 — Strategist

| Code | Capability | Output |
|------|-----------|--------|
| NC | New Campaign | campaign-data.json entry |
| SC | Campaign Status | Dashboard of all campaigns |
| MR | Market Report | Intelligence report |
| CS | Campaign Strategy | Creative strategy + landing page copy |
| BT | Battle Test | Objection/angle stress test |
| CI | Competitor Scan | competitor-data.json (scrape + download + analyse) |
| TW | Track Winners | Longevity leaderboard |
| WL | Manage Watchlist | competitor-data.json watchlist |
| SM | Save Memory | Sidecar persistence |

### Agent 2 — Creator

| Code | Capability | Output |
|------|-----------|--------|
| BA | Build Angles | creative-data.json angles |
| GI | Generate Images | creatives/ images |
| GV | Generate Videos | creatives/ videos |
| GS | Generate Scripts | On-camera scripts |
| VS | Generate VSL | Full script + edit instructions |
| AE | Ad Edit Instructions | Video editor handoff file |
| PC | Package Creatives | UPLOAD-GUIDE.md |
| GL | Generate Landing | data/landing-pages/ HTML |
| PV | Preview Landing | Preview + verification checklist |
| DP | Deploy Page | Live URL on Cloudflare Pages |
| UC | Upload Creatives | Meta creative IDs |
| GO | Launch Campaign | Active Meta campaign |
| RA | Retire Ads | Paused ads in Meta |
| LP | Link Performance | creative-data.json ← Meta ad IDs |
| SM | Save Memory | Sidecar persistence |

### Agent 3 — Analyst

| Code | Capability | Output |
|------|-----------|--------|
| PD | Pull Data | marketing-data.json (Meta + GA4) |
| AD | Discover Accounts | Meta ad account list |
| CS | Campaign Summary | Spend / CTR / CPC / CPA table |
| AS | Ad Breakdown | Ad set / ad level analysis |
| QR | Query | Freeform data answer |
| FO | Funnel Overview | Drop-off funnel report |
| PR | Performance Review | Winners, losers, next actions |
| CI | Competitor Scan | competitor-data.json (same as Strategist) |
| TW | Track Winners | Longevity leaderboard |
| WL | Manage Watchlist | competitor-data.json watchlist |
| SM | Save Memory | Sidecar persistence |

## Data Files

| File | Purpose |
|------|---------|
| `marketing-plugin/config.yaml` | Plugin config — company, domains, brand, credentials |
| `data/campaign-data.json` | Campaign registry — product, audience, tracking, Meta IDs, status |
| `data/marketing-data.json` | Performance data — campaigns, ad sets, ads, GA4 analytics |
| `data/campaigns/{campaign_id}/competitor-data.json` | Competitor intelligence — watchlist, scraped ads, analysis (campaign-scoped) |
| `data/creative-data.json` | Generated creatives — batches, angles, copy, assets, performance |
| `data/landing-pages/` | Generated landing page HTML files by campaign |
| `data/archive/` | Archived insights (90+ days old) |
| `data/campaigns/{campaign_id}/competitor-assets/` | Downloaded competitor creative files (campaign-scoped) |
| `data/creatives/` | Generated image and video assets by batch |

## Approval Gates

| Gate | Agent | Trigger | What User Sees |
|------|-------|---------|----------------|
| Campaign Plan | Strategist | After CS | Product, audience, strategy, landing page copy |
| Creative Review | Creator | After BA+GI/GV | Angles, copy variants, creative previews |
| Landing Page | Creator | After GL+PV | Preview, tracking verification, form test |
| Go-Live | Creator | After UC (dry-run) | Campaign structure, budget, cost estimate |
| Ad Retirement | Analyst | After PR | Ads to pause with performance data |

## What's Next Table

| Just Finished | Recommend Next |
|---------------|----------------|
| Setup [SW] | Strategist [NC] |
| Strategist [NC] | Strategist [MR] then [CS] |
| Strategist [CS] | Strategist [CI] for competitor scan |
| Strategist [CI] | Creator [BA] |
| Creator [BA] | Creator [GI] or [GV] or [GS] |
| Creator [PC] | Creator [GL] |
| Creator [GL] | Creator [PV] then [DP] |
| Creator [DP] | Creator [UC] then [GO] |
| Creator [GO] | Analyst [PD] after 24–48h |
| Analyst [PD] | Analyst [CS] then [PR] |
| Analyst [PR] | Creator [RA] then Creator [BA] (next iteration) |

## Typical Campaign Lifecycle

1. **Setup:** Run `/marketing:setup` once to configure for your company
2. **Week 0 — Plan:** Strategist [NC → MR → CS → BT], then [CI] competitor scan
3. **Week 0 — Create:** Creator [BA → GI/GV → PC], then [VS] if VSL needed
4. **Week 0 — Landing:** Creator [GL → PV → DP]
5. **Week 0 — Launch:** Creator [UC → GO]
6. **Week 1+ — Monitor:** Analyst [PD → CS → AS → FO]
7. **Week 1+ — Review:** Analyst [PR] → retire losers [RA], new batch [BA]
8. **Ongoing:** Repeat steps 6–7 every 7 days
