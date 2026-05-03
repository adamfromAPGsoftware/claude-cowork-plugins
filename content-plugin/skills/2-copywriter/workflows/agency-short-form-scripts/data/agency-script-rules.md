# Agency Short-Form Script Rules

> **Extends:** `short-form-scripts/data/script-rules.md` — all base rules apply unless explicitly overridden below. This file documents ONLY the agency-specific modifications.

---

## What Stays the Same (from base script-rules.md)

The following rules from the base `script-rules.md` apply unchanged:

- **Speaking rate guidelines** — 3.5 wps normal, 4.0 wps hook, 3.0 wps CTA
- **Duration calculation formula** — section_duration = word_count / wps
- **Validation rule** — calculated duration must match allocation within +/-1 second
- **Script structure** — Hook -> Body -> CTA (3-part, strict)
- **V1-V7 segment types** — all visual types, same definitions
- **Hook opens with V5 split-screen** — P4 rule, V6 as opener is FORBIDDEN
- **Writing rules** — all 8 rules (write for speaking, one idea per video, no throat-clearing, etc.)
- **Proven engagement signals** — immediate text overlay, comment-gated CTA, MG coverage 65-84%
- **B-roll and MG markers** — REF-FRAME, MG, V4b marker formats
- **MG prompt structure** — 6-part mandatory format (format+orientation, subject, motion, style, colors, timing)
- **MG prompt quality rules** — specific tools with hex colors, describe motion, include background color
- **MG density guidelines** — minimum clips per category, 80%+ target coverage
- **V4b MG cutaway rules** — 1 per 10-12 seconds, 30-60 frames, no caption
- **Pacing guidelines** — P1-P11 rules, max 4s same-shot, min 6 cuts per 15s
- **Caption rules** — sentence case, 1 highlight word in teal, max 3-4 words per burst
- **Speaker zoom values** — V1: 1.03, V2: 1.08, V7: 1.05. 1.25 is FORBIDDEN
- **Ken Burns MG zoom** — mandatory on all non-speaker visuals
- **Teleprompter section** — plain text, one sentence per line, max 8-10 words, ALL CAPS for emphasis
- **Platform copy section** — Instagram, TikTok, YouTube Shorts formats

---

## Agency-Specific Overrides

### Batch Pillar System (OVERRIDE — PRIMARY COMPOSITION RULE)

Every batch of 5 scripts must contain **exactly one script per pillar slot**. Slot assignment takes priority over all other diversity rules.

| Slot | Pillar | Audience State | CTA Type | Description |
|------|--------|---------------|----------|-------------|
| SF-01 | **BOFU A** | Ready | Hard keyword (WASTE/AUDIT/AI) | Problem awareness — reveals operational waste, SaaS cost, or efficiency loss |
| SF-02 | **BOFU B** | Ready | Hard keyword (WASTE/AUDIT/AI) | AI enablement or offer proof — data foundation, audit walkthrough, ROI proof |
| SF-03 | **Reputation** | Stranger + Warm | None — or soft engagement prompt | Opinion/hot take + credibility signal. Builds authority without selling |
| SF-04 | **Case Study** | Warm + Ready | Hard keyword (RESULTS) | Real client transformation — specific metrics, before/after |
| SF-05 | **News** | Stranger + Warm | Soft keyword or engagement CTA | Current news hook + opinion angle |

**Rules:**
- A script may NEVER be placed in a slot that doesn't match its pillar
- The 2 BOFU slots are interchangeable (BOFU A and BOFU B are both "ready" audience — pick the better concept per slot)
- Reputation and News scripts talk to strangers and warm audiences — do NOT add a hard keyword CTA to these
- Case Study slot always uses the RESULTS keyword

---

### Duration Mix (OVERRIDE)

When generating 5 scripts, use this distribution as a guide (secondary to pillar assignment):
- **2x Punchy** (15-20s) — Reputation and News lean Punchy; BOFU can be any duration
- **2x Standard** (22-30s) — BOFU and Case Study lean Standard
- **1x Deep** (35-45s) — Case Study leans Deep; builds authority with before/after story

**Duration guidance by pillar:**
- BOFU A / BOFU B: any duration — match to hook complexity
- Reputation: Punchy (15-20s) preferred — strong takes land fast
- Case Study: Standard or Deep — metrics and story need room
- News: Punchy (15-20s) preferred — news hooks go stale, keep them tight

This replaces the base 1-3-1 distribution.

### Hook Patterns (OVERRIDE)

| Pattern | Template | Priority | Best For |
|---------|----------|----------|----------|
| Pain Interrupt | "Stop [doing wrong thing]" / "[X]% of SMEs [waste/lose] [metric]" | PRIMARY | Bad habit correction, waste exposure, inefficiency reveals |
| Result Reveal | "This [approach] saved [client type] [metric]" / "We found [$X/year] hiding in [their stack]" | PRIMARY | Case studies, audit reveals, ROI proof |
| News Anchor | "[X study/report] just revealed [finding about SMEs]" / "[Platform] just [changed/dropped] [thing] — here's what it means for your business" | SECONDARY | Current events, industry shifts, policy changes |
| Elimination | "You don't need to [pay for X] anymore" | SECONDARY | SaaS replacement, cost-saving alternatives |
| Step-by-Step Tease | "Here's the 3-step audit we run on every SME" | USE SPARINGLY | Framework content, how-to (Deep only) |
| Product Drop | "[Company] just [dropped/launched] [Product]" | DEPRIORITISED | Less relevant for agency BOFU — only if a major tool launch directly impacts the ICP |

**Note:** "Direct Address" pattern ("If you're a [role] who [struggles with X]...") is acceptable for BOFU as it qualifies viewers early. Use sparingly — max 1 per batch of 5.

### CTA Rules by Pillar (OVERRIDE)

CTA assignment is now **pillar-driven**, not content-driven. Use the table below:

| Pillar Slot | CTA Type | Keyword Options | Notes |
|-------------|----------|-----------------|-------|
| **BOFU A** | Hard keyword | AUDIT / WASTE | SaaS waste angle → WASTE; efficiency/general → AUDIT |
| **BOFU B** | Hard keyword | AI / AUDIT | AI readiness angle → AI; offer proof/walkthrough → AUDIT |
| **Reputation** | None (or soft) | No keyword | End on the point, or soft prompt: "Has this been your experience?" / "Drop YES if you agree." — NEVER a keyword |
| **Case Study** | Hard keyword | RESULTS | Always RESULTS for case study slot |
| **News** | Soft or engagement | Optional soft | Can use engagement CTA ("What's your take?") or no CTA. Never a hard keyword on News |

**Hard keyword format:** "Comment [KEYWORD] and I'll send you the [thing]"
- AUDIT → "...the checklist"
- WASTE → "...the SaaS audit template"
- AI → "...the readiness checklist"
- RESULTS → "...the full breakdown"

**Secondary CTA (Deep videos only):** "Link in bio — free discovery call, 30 minutes, we spend most of it listening"

**NEVER use:** "Follow for more" or community/Skool CTAs — those are for @{YOUR_HANDLE_PERSONAL}, not @{YOUR_HANDLE}

### Brand Voice (OVERRIDE)

- **Tone:** 60% Business Value / 40% Technical Proof
- **Audience framing:** Speak to business operators, not developers. Use business outcomes (revenue, savings, hours reclaimed) not technical jargon
- **Credibility signals:** Reference "300+ projects", "Top 1% on Upwork", case study metrics — NOT community size or YouTube views (those are @{YOUR_HANDLE_PERSONAL} signals)
- **Personality:** Confident operator who's been in their shoes. Not a consultant lecturing — a business owner who solved this problem himself
- **Proof language:** "We found...", "Our audit revealed...", "One client went from... to..." — always grounded in specific experience

### Platform Copy (OVERRIDE)

#### Instagram Reel (PRIMARY platform for @{YOUR_HANDLE})

Two-part format:
1. **Hook line** — Under 125 chars, keyword-rich, business-outcome focused. Must match the video's hook angle
2. **Body + CTA** — 1-2 sentence value line connecting pain to audit offer + comment-gated CTA

**Tone:** Business-confident, data-driven, direct. Target 300-900 chars total for lead generation.

**No hashtags** — Instagram auto-classifies content. Top performers use zero hashtags.

#### TikTok (SECONDARY)

Single caption field:
- **Hook** — Self-diagnosis or chaotic/personal style. Can be longer (up to 300 chars)
- **CTA** — Comment-first with DM delivery, matching video CTA keyword. Pattern: "Comment '{KEYWORD}' below and then DM me '{KEYWORD}' — I'll send you [resource]!" The comment is the PRIMARY ask for algorithmic engagement boost; the DM is the ManyChat delivery trigger. Be crystal clear about what word to comment and that they need to DM the same word.
- **Hashtags** — 3-5: #BusinessAutomation #SME #AIForBusiness #OperationalEfficiency #SaaS
- **Voice** — Slightly more personal ("I", "we"), raw/direct

#### YouTube Shorts (SECONDARY)

Two fields:
1. **Title** — Under 40 chars, front-load keyword, business-outcome focus
2. **Description** — 2-3 keyword-rich sentences. Include: audit CTA, link to {YOUR_COMPANY} website. 3-5 hashtags including #Shorts

### Content Pillars

Scripts map to these value pillars. Note: the **Batch Pillar System** above governs slot assignment — a pillar is the *what*, a slot is the *where*.

| Value Pillar | Description | Typical Slot |
|--------|-------------|--------|
| SaaS Waste | Exposing hidden costs of tool sprawl, per-user pricing, integration overhead | BOFU A or BOFU B |
| Efficiency / Automation | Manual process waste, time savings, operational improvement | BOFU A or BOFU B |
| AI Enablement | AI readiness, data foundation, practical AI applications for SMEs | BOFU A or BOFU B |
| Case Study / Social Proof | Real client transformations, specific metrics, before/after | Case Study (SF-04) |
| News Commentary | Current AI/automation/SME news with value connection | News (SF-05) |
| Reputation / Opinion | Hot takes, industry POV, credibility signals — no pitch | Reputation (SF-03) |

**Diversity rule (updated):** The Batch Pillar System guarantees pillar diversity by construction — SF-01 through SF-05 each occupy a distinct slot. Do NOT try to force 3 pillars into BOFU slots. Each batch will naturally cover 5 distinct content purposes.

### Reference Frame Plan (OVERRIDE)

**No long-form video source exists.** Reference frames for Hera MG generation come from:

1. **Branded assets** — logo, client dashboard screenshots, SaaS comparison graphics
   - Path: `{project-root}/content-plugin/skills/2-copywriter/workflows/agency-short-form-scripts/data/branded-assets/` or project-level branded assets
2. **Tool logos/screenshots** — Fetched via `fetch-logo.ts` or `fetch-tool-screenshot.ts`
   - Reference as: `logos/{tool-name}.png` or `reference-frames/ref-{tool-name}.png`
3. **Prompt-only generation** — When no suitable reference image exists, generate MG from detailed prompt alone
   - Reference as: `"none -- prompt-only"`

**MG Reference Frame format (replaces long-form source/timestamp):**

```
[REF-FRAME: source="branded-asset" asset="brand-logo.png" description="{YOUR_COMPANY} logo on dark background" mg_prompt_ref="MG-01"]
[REF-FRAME: source="tool-screenshot" tool="hubspot" description="HubSpot pricing page showing per-user fees" mg_prompt_ref="MG-02"]
[REF-FRAME: source="prompt-only" description="Abstract data flow visualization" mg_prompt_ref="MG-03"]
```

### MG Visual Themes for Agency BOFU

Preferred MG visual concepts for this ICP:

- **SaaS cost comparisons** — Stack of app logos with dollar amounts vs single unified platform
- **Before/after dashboards** — Messy spreadsheet → clean Kanban/dashboard
- **ROI counter animations** — Animated counters showing savings ($5K/mo, $60K/yr)
- **Tool logo grids** — Grid of SaaS logos with red X marks being replaced by one green checkmark
- **Data flow diagrams** — Arrows showing data scattered across tools vs unified flow
- **Case study metrics** — Big bold numbers (40 staff, $18M revenue, $200K→$1M)
- **Audit deliverable stack** — Visual showing the 6 deliverables with their values

### Script Frontmatter (OVERRIDE)

Each agency script file includes these additional frontmatter fields:

```yaml
channel: {YOUR_HANDLE}
content_type: agency-short-form
pillar_slot: '{BOFU-A / BOFU-B / Reputation / Case-Study / News}'
value_pillar: '{SaaS Waste / Efficiency / AI Enablement / Case Study / News Commentary / Reputation}'
news_source: '{headline and source, or "evergreen"}'
cta_keyword: '{AUDIT / WASTE / AI / RESULTS / none}'
```

### Output Path (OVERRIDE)

Scripts save to: `{agency_folder}/{project-slug}/copywriter/agency-sf/scripts/sf-{NN}-script.md`

Combined teleprompter saves to: `{agency_folder}/{project-slug}/copywriter/agency-sf/scripts/sf-all-teleprompter.md`

Raw video recordings go to: `{agency_folder}/{project-slug}/video-editor/agency-short-form/raw/`
