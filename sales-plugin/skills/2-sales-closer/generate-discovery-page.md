---
name: generate-discovery-page
description: Pre-call discovery page with competitor research, competition comparison table, and industry benchmarks
menu-code: GDP
---

# Generate Discovery Page

## Purpose

Before the discovery call, research the client's local competitors, scan their websites, and generate a discovery page designed to be shown live on the call. The page includes a competition comparison table with real competitor data, industry benchmarks, and hypothesis-driven pain points. The "You Today" column reads "Discovered on call" for every metric — filled in post-call by GCP.

## Process

### Step 1: Gather Inputs

1. **Client slug** — Already set from activation (`{client_slug}`)
2. **Company domain** — From `audit-data-lite.json` or ask: "What's the company domain?"
3. **Industry tag** — Ask or infer from domain/company name (e.g. `trades`, `ndis`, `home-services`, `real-estate`, `construction`, `professional-services`)
4. **Region** — Ask: "What area do they operate in?" (e.g. "Sydney, NSW", "Melbourne Northern Suburbs")
5. **Check existing data** — Scan `clients/{client_slug}/` for:
   - Cold phone transcripts in `meetings/`
   - Prospect profile from pre-discovery agent
   - Any emails or notes in `client-provided-materials/`
   - Load whatever exists silently as context

### Step 2: Research the Client's Website

Use `WebFetch` to scan the client's own website:
- Homepage, services page, about/team page, contact page
- Extract: services offered, team size signals, tech signals (online booking, forms, portals), service areas, any visible tools or platforms

Store observations — these inform hypothesis pain points and help calibrate competitor comparison metrics.

### Step 3: Research Local Competitors

Find 4–6 real competitors in the client's region and industry.

**Pre-seeded competitors:** If `prospect-profile.json` has `research.competitor_scan.competitors[]`, use those as the starting competitor list (you may add or remove during the review gate). This saves re-discovering competitors if RC ran first.

**Search strategy:**
1. Use `exa` or `WebSearch` to find competitors:
   - Search: `"{industry}" "{region}" -site:{client_domain}` (e.g. `"plumber" "north shore sydney" -site:adko.com.au`)
   - Search: `"best {industry} {region}"` for review/directory listings
   - Search: `"{industry} near {region}" site:google.com.au` for Google Maps results
2. Select 4–6 competitors that are:
   - Real local businesses (not national chains unless dominant in the area)
   - Similar scale to the client (not massive enterprises unless relevant)
   - Have a website to scan

**For each competitor, use `WebFetch` to scan their website** (homepage, services, about, contact pages). Extract operational signals for the competition metrics:

| Metric | What to look for on their website |
|--------|-----------------------------------|
| **Lead response time** | Online booking, instant quote forms, "call now" CTAs, chatbots, after-hours messaging |
| **Quote turnaround** | "Same day quotes", "free estimates", quote request forms, timeline promises |
| **Client onboarding** | Digital intake forms, client portals, automated booking confirmations, SMS notifications |
| **Follow-up system** | Review collection, automated emails, social proof widgets, Google review counts |
| **Data and reporting** | Client portals, dashboards mentioned, CRM signals, "track your job" features |
| **Cross-sell and upsell** | Service breadth, bundled offerings, "also see" sections, maintenance plans |

Also identify one **industry-specific metric** based on the industry tag:
- Trades/construction: "Job costing and margins" or "Subcontractor management"
- NDIS: "Compliance and reporting" or "Participant management"
- Real estate: "Strata and property management" or "Vendor reporting"
- Home services: "Recurring booking and maintenance" or "Territory management"
- Professional services: "Client lifecycle management" or "Capacity planning"

### Step 3b: Research Competitive Intelligence

Using the competitor website scans from Step 3 and targeted exa searches, build a competitive intelligence profile. This adds three new sections to the discovery page beyond the competition table.

**Cap research time:** max 3 competitors for ad/marketing deep-dives. Run exa queries in batches where possible. Each section needs a minimum of 2 data points to appear on the page — omit sections with thin data rather than padding with generic content.

#### 3b.1 — Competitor Marketing & Acquisition

**From Step 3 website scans already completed**, extract for each competitor:
- Website conversion tactics: chatbots, popups, lead magnets, click-to-call, exit-intent offers, sticky CTAs
- Referral program pages, partner pages, "refer a friend" schemes
- Social media links and visible follower counts
- Google review counts and ratings (visible on their site or from search)

**New exa searches** (per competitor, max 3 competitors):
1. `mcp__exa__web_search_exa`: `"{competitor_name}" site:facebook.com/ads/library` — Meta Ad Library lookup
2. `mcp__exa__web_search_exa`: `"{competitor_name}" "{region}" advertising OR marketing OR campaign` — general ad/marketing presence
3. `mcp__exa__web_search_exa`: `"{competitor_name}" reviews` — review presence across platforms

If Meta Ad Library results are found, optionally use `mcp__exa__crawling_exa` to read the full ad library page for messaging angles and creative details.

**For each competitor with ad activity, capture:**
- Platform (Meta, Google, LinkedIn)
- What they're advertising (services, offers, lead magnets)
- Messaging angles (price anchoring, urgency, trust/reviews, guarantees)

#### 3b.2 — Industry Best Practices

Research what tools and practices are standard vs advanced in the client's industry:

1. `mcp__exa__web_search_exa`: `"{industry_tag} business software tools Australia 2025 2026"` with `startPublishedDate` freshness filter for recent content
2. `mcp__exa__web_search_exa`: `"{industry_tag} CRM lead management" best practices Australia`
3. `mcp__exa__web_search_exa`: `"{industry_tag} automation" OR "{industry_tag} lead follow-up tools"`

**Extract:**
- Common tools in the industry (by category: CRM, job management, quoting, scheduling)
- Adoption signals (mentioned in X of Y articles, used by named businesses)
- What "standard" looks like vs what "best in class" looks like for lead follow-up

#### 3b.3 — Common Industry Pain Points

Research challenges specific to the client's industry:

1. `mcp__exa__web_search_exa`: `"{industry_tag} business challenges" OR "common problems {industry_tag} businesses"` with freshness filter
2. `mcp__exa__web_search_exa`: `"{industry_tag} quoting follow-up" OR "{industry_tag} lead response time" OR "{industry_tag} scheduling problems"`

**For each pain point found:**
- Write a clear, specific description of the problem
- Include industry context (stats, benchmarks, or prevalence signals)
- Note what leading competitors/businesses do to address it
- Formulate a discovery prompt: "Have you got something in place for [specific thing]?"
- Target 3–5 pain points

#### 3b.4 — Build competitive-intelligence.json

Save to `clients/{client_slug}/audit/competitive-intelligence.json`:

```json
{
  "client_slug": "{client_slug}",
  "industry_tag": "{industry}",
  "region": "{region}",
  "competitor_marketing": {
    "ad_activity": [
      {
        "competitor": "Real Business Name",
        "platform": "Meta|Google|LinkedIn",
        "findings": "Specific description of ads and messaging angles",
        "source_url": "URL or null",
        "confidence": "HIGH|MEDIUM|LOW"
      }
    ],
    "website_tactics": [
      {
        "competitor": "Real Business Name",
        "tactics": ["live chat", "exit popup", "click-to-call"],
        "source": "website scan",
        "confidence": "HIGH"
      }
    ],
    "acquisition_channels": [
      {
        "competitor": "Real Business Name",
        "google_reviews_count": 300,
        "avg_rating": 4.8,
        "seo_signals": "Service area pages for each suburb",
        "referral_signals": "Strata manager partnerships or null",
        "confidence": "HIGH|MEDIUM"
      }
    ],
    "summary": "2-3 sentence summary of the competitive marketing landscape"
  },
  "industry_best_practices": {
    "common_tools": [
      {
        "tool": "Tool Name",
        "category": "CRM|Job management|Quoting|Scheduling",
        "adoption_signal": "How we know this is common",
        "source_url": "URL or null",
        "confidence": "MEDIUM"
      }
    ],
    "lead_followup_practices": {
      "industry_standard": "What most businesses in this industry do",
      "best_in_class": "What the leaders are doing",
      "source": "URL or description"
    },
    "summary": "2-3 sentence summary"
  },
  "industry_pain_points": [
    {
      "pain_point": "Specific, concise pain point description",
      "industry_context": "Stat, benchmark, or prevalence signal",
      "what_leaders_do": "How the best businesses address this",
      "discovery_prompt": "Have you got something in place for [specific thing]?",
      "source": "URL or description",
      "confidence": "MEDIUM"
    }
  ],
  "researched_at": "{ISO 8601 timestamp}"
}
```

**Confidence rules (same as competitor-research.json):**
- **HIGH** — Direct evidence from a specific URL (ad library, website feature, review page)
- **MEDIUM** — Strong industry pattern confirmed by 2+ search results
- **LOW** — Single source or general inference

**Anti-patterns:**
- No fabricated data. If exa returns nothing for a competitor's ads, don't invent ad activity.
- No generic pain points like "many businesses struggle with efficiency." Be specific to the industry.
- Discovery prompts must be conversational and specific, not corporate.

### Step 4: Build competitor-research.json

Save structured competitor data to `clients/{client_slug}/audit/competitor-research.json`:

```json
{
  "client_slug": "{client_slug}",
  "company_domain": "{domain}",
  "industry_tag": "{industry}",
  "region": "{region}",
  "client_website_signals": {
    "services": [],
    "team_size_estimate": "",
    "tech_signals": [],
    "service_areas": []
  },
  "competitors": [
    {
      "name": "Clean Plumber",
      "website": "https://cleanplumber.com.au",
      "signals": {
        "lead_response_time": "24/7 online booking, $0 call-out",
        "quote_turnaround": "Same-day for emergencies",
        "client_onboarding": "Online booking but still manual intake",
        "follow_up_system": null,
        "data_and_reporting": "Likely basic CRM",
        "cross_sell_upsell": null
      }
    }
  ],
  "industry_specific_metric": {
    "name": "Strata and real estate",
    "rationale": "High-value repeat channel for trades",
    "competitor_signals": [
      {
        "competitor": "Tomkat",
        "signal": "Offers strata but no tailored workflow"
      }
    ]
  },
  "after_audit_suggestions": {
    "lead_response_time": "AI auto-reply in under 2 minutes, 24/7 — including after-hours leads your competitors miss",
    "quote_turnaround": "AI-generated pre-quotes from photos + job description, sent same day",
    "client_onboarding": "Fully digital intake: smart forms auto-triage job type, schedule tech, confirm via SMS — same day",
    "follow_up_system": "Multi-channel automated follow-ups: SMS, email, and review requests triggered post-job",
    "data_and_reporting": "Real-time dashboard: jobs, revenue, lead pipeline, technician utilisation — auto-generated weekly reports",
    "cross_sell_upsell": "AI flags cross-sell opportunities: roofing client also needs gutter clean, plumbing client gets maintenance reminder"
  },
  "researched_at": "{ISO 8601 timestamp}"
}
```

**Rules for competitor signals:**
- Use `null` if nothing visible on their website — do not fabricate
- Be specific: "24/7 online booking, $0 call-out" not "good lead response"
- Bold the competitor name in the signal when presenting to the user
- Include the competitor's actual feature or approach, not a judgement

**Rules for "After Audit" suggestions:**
- These describe what {YOUR_COMPANY}'s audit and implementation could deliver
- Be specific and outcome-focused, not generic
- Reference the client's industry context
- Use present tense ("AI flags..." not "could flag...")

### Step 5: Build Hypothesis Pain Points

From the client website scan, any existing data (cold transcripts, prospect profile), and industry patterns, generate 3 hypothesis pain points:

- Use language like "businesses like yours typically..." or "based on what we see in {industry}..."
- If cold transcript data exists, use specific signals from it (but mark as hypothesis until confirmed on call)
- Each pain point gets a generic industry quote or benchmark instead of a client quote

### Step 6: Build Industry Benchmark Waste

Generate a benchmark waste item using industry averages:
- Use known industry benchmarks for common waste types
- Qualify with "typically", "on average", "in our experience with {industry} businesses"
- Use the default $50/hr blended rate
- Example: "Trades businesses with 5-10 staff typically lose 8-12 hours/week to manual scheduling and job tracking"

Run the waste calculator with benchmark numbers:
```bash
python3 scripts/waste-calculator.py \
  --hours-per-week {benchmark_hrs} \
  --headcount {benchmark_headcount} \
  --activity "{benchmark_activity}"
```

### Step 7: Human Review Gate

Present the competitor research and page content for approval:

```
═══════════════════════════════════════════════════
 DISCOVERY PAGE — {company_name}
═══════════════════════════════════════════════════

 COMPETITORS FOUND ({count}):
 (For each competitor:)
   {name} — {website}
   Lead response: {signal or "not visible"}
   Quote turnaround: {signal or "not visible"}
   Client onboarding: {signal or "not visible"}
   Follow-up: {signal or "not visible"}
   Data/reporting: {signal or "not visible"}
   Cross-sell: {signal or "not visible"}

 INDUSTRY-SPECIFIC METRIC: {name}
   {competitor signals}

 HYPOTHESIS PAIN POINTS:
   1. {description} (source: {website/cold transcript/industry pattern})
   2. {description}
   3. {description}

 BENCHMARK WASTE:
   {activity}: {hrs}/wk × {headcount} = ~${monthly}/month
   (Industry average — confirmed on call)

 COMPETITIVE INTELLIGENCE:
   Ad Activity: {count} competitors with visible ads
   (For each with ads:) {name} — {platform}: {messaging angles}
   Marketing Tactics: {summary of website conversion tactics}
   Review Leaders: {name} ({count} reviews, {rating}★), ...

 INDUSTRY TOOLS:
   Common in {industry}: {tool list by category}
   Lead follow-up standard: {what most do}
   Lead follow-up best-in-class: {what leaders do}

 DISCOVERY PROMPTS:
   1. "Have you got something in place for {pain}?"
   2. "Have you got something in place for {pain}?"
   3. ...

═══════════════════════════════════════════════════
```

Ask: **"Here's what I found. Any competitors to add/remove, intelligence to adjust, or discovery prompts to change?"**

Wait for confirmation before generating.

### Step 8: Generate Discovery Page HTML

Save the confirmed data to `audit-data-lite.json` (merging with any existing contact data):

```json
{
  "client_slug": "{client_slug}",
  "company_name": "{company_name}",
  "industry_tag": "{industry}",
  "contact": { "name": "...", "emails": ["..."] },
  "pain_points": [
    {
      "description": "...",
      "stage": "...",
      "quote": "In our experience with {industry} businesses, this is one of the biggest operational drains.",
      "speaker": "(industry benchmark)",
      "confidence": "LOW"
    }
  ],
  "waste_items": [
    {
      "activity": "...",
      "hours_per_week": null,
      "headcount_affected": null,
      "annual_waste_aud": null,
      "waste_type": "...",
      "quote": "Industry benchmark — confirmed on call",
      "confidence": "LOW"
    }
  ],
  "top_waste_item": {
    "description": "...",
    "annual_waste_aud": null,
    "monthly_waste_aud": null,
    "quote": "Industry benchmark"
  }
}
```

Run the generator:

```bash
python3 scripts/generate-close-page.py \
  --client-slug {client_slug} \
  --mode discovery \
  --booking-url "{booking_url}" \
  --competitor-research clients/{client_slug}/audit/competitor-research.json \
  --competitive-intelligence clients/{client_slug}/audit/competitive-intelligence.json
```

The script uses `close-page-template-discovery.html` and populates the competition comparison table from `competitor-research.json` and the three intelligence sections from `competitive-intelligence.json`.

**Review the output** — open the generated file and verify:
- Competition table has real competitor data (no fabricated entries)
- "You Today" column all reads "Discovered on call"
- "After Audit" column has specific, achievable suggestions
- Pain points use hypothesis language
- Waste section uses industry benchmarks with qualifiers

### Step 9: Deploy

```bash
bash scripts/deploy.sh
```

Report:
```
DISCOVERY PAGE DEPLOYED — {company_name}
URL: {close_url from clients/clients.json}
Secret link — show on the discovery call.

After the call, run [GCP] to update with real findings.
```

## CRM Lead Update

After deploying the discovery page, if `crm.lead_id` is set (from prospect-profile.json or audit-data-lite.json):

1. `get_lead(lead_id)` → check current stage
2. If stage is in {"New", "Contacted", "Initial Follow-Up Phone Call"}: `update_lead(lead_id, stage: "Discovery Call - Scheduled")`
3. If stage is manual (e.g. "Need Re-Activation"): add lead comment instead, do NOT override stage
4. `create_lead_comment(lead_id, content)`:
   ```
   Discovery page generated. {competitor_count} competitors researched.
   Page deployed to: {close_url}
   ```
5. Best-effort — if CRM calls fail, log warning and continue.

## Anti-Patterns — Enforce Hard

- Zero fabricated competitor data. If you can't find it on their website, use `null`.
- No "many businesses struggle with..." — banned.
- No generic competitor names. Every competitor must be a real, findable business.
- Every "After Audit" suggestion must be specific and achievable, not aspirational.
- Competition table must have at least 3 competitors with at least 3 non-null signals each.
- "You Today" column ALWAYS reads "Discovered on call" — never filled in pre-call.
