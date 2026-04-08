---
name: build-battle-card
description: Generate prospect brief with CLOSER-framework discovery call prep, tailored questions, objection handlers, and waste exploration
menu-code: BC
---

# [BC] Build Battle Card

## Purpose

Generate the complete `prospect-brief.md` with all sections including CLOSER-framework discovery call prep. This is the crown jewel of the pre-discovery agent — the output Adam reads before walking into the call.

Output: `clients/{client_slug}/prospect-brief.md`

## Prerequisites

- `{client_slug}` must be set
- `prospect-profile.json` must exist
- **Research ([RC]) should be completed** — if `research_completed == false`, warn: "Research hasn't been run yet. The prospect brief will be weaker without it. Run [RC] first, or continue with what we have?"
- **Phone transcript ([AT]) is optional** — if `phone_transcript_analyzed == false`, the "What We Know From the Phone Call" section shows: "No pre-call transcript analyzed — use Clarify questions to surface pain from scratch."

## Data Sources

Load all available data before generating:

1. `clients/{client_slug}/audit/prospect-profile.json` — research + phone analysis
2. `sales-plugin/references/hormozi-closer-framework.md` — CLOSER framework, AAA objection handlers, buying signals, close sequence
3. `sales-plugin/references/offer-summary.md` — pricing ($3K audit), guarantees ($5K/month savings), value framework (3 pillars), ROI benchmarks
4. `sales-plugin/references/post-discovery-overview.md` — what the audit delivers, two-phase engagement model
5. Sidecar `patterns.md` — accumulated patterns from previous preps (if available)

## Prospect Brief Structure

Generate `clients/{client_slug}/prospect-brief.md` with this exact structure, following `references/prospect-brief-template.md`. The gold standard reference is `clients/noah-caring-ways/discovery-call-prep.md` — match its depth and specificity.

---

### Header

```markdown
# Discovery Call Prep — {Contact Name}, {Company Name}

**Date**: {discovery_call_date or "TBD"}
**Pre-call**: {phone call date if analyzed, or "None"}
**Website**: {company_domain}
**Phone**: {if found in research}
**Email**: {contact email if available}
**Location**: {from research}
```

---

### Section 1: Company Profile

Compiled from [RC] research. Table format:

```markdown
## Company Profile

**Trading as**: {name} | **Legal name**: {if found}
**ABN**: {if found}
**Founded**: {if found}
**Team size**: {estimate from research}

### Services Offered
- {service 1}
- {service 2}
...
```

Include any professional memberships, registrations, or compliance requirements relevant to their industry.

---

### Section 2: What We Know From the Phone Call

**If [AT] was run:** Structure as per the phone analysis data:

```markdown
## What We Know From the Phone Call

**{Contact name}'s current stack**:
1. **{Tool}** — {what it does, stated problems, keeping/leaving status}
2. ...

**Key quotes (buying signals)**:
- "{verbatim quote}" — {signal type, intent level}
- ...

**Decision context**: {stakeholders, urgency, trigger event}
```

**If no phone call analyzed:**

```markdown
## What We Know From the Phone Call

No pre-call transcript analyzed. Discovery call is first substantive contact — use the Clarify section below to surface pain from scratch.
```

---

### Section 3: Industry-Specific Research Notes

Context about their industry that's relevant to the discovery call. Source from research + industry knowledge.

If `research.industry_tools` exists, incorporate tool landscape data — name specific tools so Adam can reference them on the call ("most businesses in your space use Tradify or ServiceM8 for job management").

If `research.competitor_scan` exists, weave in competitor context — what the local market looks like and where competitors are investing.

```markdown
## {Industry}-Specific Research Notes

{2-4 paragraphs of industry context relevant to operational pain points.
E.g. for NDIS: registration groups, compliance requirements, common tool stacks.
E.g. for architecture: project lifecycle, stakeholder coordination, design iteration.
Reference similar clients if applicable (anonymized).}

### Common Tools in {Industry}
| Category | What Most Use | Reality |
|---|---|---|
| {category} | {tools} | {what actually happens} |

### Local Competitor Landscape
{Brief summary of what competitors are doing — 2-3 sentences max.}
```

**Graceful fallback:** If `research.competitor_scan` or `research.industry_tools` is absent (older profiles), skip those enrichments — generate from `industry_context` and general knowledge as before.

---

### Section 4: Waste Areas to Explore

Table format matching the noah-caring-ways pattern. Combine:
- Pain hypotheses from [RC] research (both tiers — industry reality and client specific)
- Confirmed pain signals from [AT] phone analysis (if available)
- Industry-standard waste patterns
- If `research.competitor_scan.competitor_edges` exists, use them to frame exploration questions (e.g. "We noticed 3 of your competitors have online booking — walk me through what happens when a lead comes in after hours for you?")

```markdown
## Waste Areas to Explore on the Call

| Waste Type | What to Ask | Why It Matters |
|---|---|---|
| {type} | "{specific open-ended question}" | {why this matters for the close} |
```

**Rules:**
- Minimum 6 rows, maximum 12
- Questions must be open-ended (start with "How", "Walk me through", "What happens when")
- Never use closed questions ("Do you use X?")
- If phone analysis available, put confirmed pain areas first, hypotheses second
- Label source: confirmed (from phone) vs. hypothesis (from research)

---

### Section 5: Discovery Call Structure (CLOSER Framework)

The core of the prospect brief. Each section maps to a CLOSER stage from `sales-plugin/references/hormozi-closer-framework.md`, but tailored to this specific prospect.

#### C — Clarify: Why Are You Here?

```markdown
### C — Clarify: Why Are You Here?

{If phone call analyzed: reference what they said, ask them to expand on specifics.}
{If no phone call: use standard openers from the framework.}

**Opening questions**:
- "{Tailored question referencing something specific from phone/research}"
- "{Second tailored question — different angle}"
- "{Third tailored question — opens up a new area}"
```

**Rules:**
- If we have phone data, the first question MUST reference something they specifically said
- Questions should be open-ended, getting them to describe their situation
- Never start with features or your offer

#### L — Label: Name the Pattern

```markdown
### L — Label: Name the Pattern

Based on what we know, {contact name}'s problems map to:

1. **{Label name}**: "{Exact phrasing tailored to this prospect's situation}"

2. **{Label name}**: "{...}"

**Then confirm**: "Does that feel like a fair summary of where you're at?"
```

**Label options** (from the framework):
- **SaaS Waste** — paying for tools that don't deliver value
- **Efficiency Drain** — best people spending time on admin, not revenue work
- **AI Blindness** — data scattered, can't leverage AI
- **Usability Tax** — tool technically works but team can't/won't use it
- **Tool Gap** — separate systems that don't connect

Pick 2-3 labels that best match research + phone data. Write the phrasing specifically for this prospect.

#### O — Overview: What Have You Already Tried?

```markdown
### O — Overview: What Have You Already Tried?

- "{Question about competitors/alternatives specific to their industry}"
- "{Question about previous attempts to solve this}"
- "{Question about what their ideal setup looks like}"
```

Reference industry-specific alternatives they might have explored.

#### S — Sell the Vacation

```markdown
### S — Sell the Vacation

**The dream for a {industry} business {contact name}'s size:**

"{2-3 sentence dream state painted specifically for their industry and team size. Use their specific context — team roles, service types, operational challenges.}"

**Anchor questions**:
- "How many {relevant role} do you have?"
- "How much time would you say {bottleneck person/role} spends each week on {specific admin task from research}?"
- "If your team got back even {X} minutes per {task} — across all your {workers} — what does that add up to?"
```

#### E — Explain Concerns (Objections to Prep For)

```markdown
### E — Explain Concerns (Objections to Prep For)

{For each objection risk from phone analysis + industry patterns, provide the AAA handler:}

**"{Likely objection}"**
- **Acknowledge**: "{...}"
- **Associate**: "{...}"
- **Ask**: "{...}"
```

If phone analysis identified specific objection risks, put those first. Then add 2-3 industry-standard objections from the framework.

#### R — Reinforce: Close to the Audit

```markdown
### R — Reinforce: Close to the Audit

- Summarise pain in their words (from phone + discovery)
- Quantify with their numbers: staff count x wasted hours x hourly rate
- Present the audit: "$3,000, 2-4 weeks, we do the heavy lifting"
- Guarantee: "If we don't find at least $5,000/month in savings, you pay nothing"
- Credit: "100% of the $3,000 goes toward the build if you proceed"
```

---

### Section 6: Industry-Specific Talking Points

If `research.competitor_scan` exists, include competitor highlights as concrete talking points.
If `research.industry_tools.relatable_patterns` exists, include them as patterns Adam can drop into conversation.

```markdown
## {Industry}-Specific Talking Points

- {Relevant experience in this industry — anonymized}
- {Compliance/regulatory context specific to their industry}
- {Common patterns from similar businesses}

### Competitor Insights to Reference
- "{competitor_edge}" — use to show market awareness
- ...

### Relatable Patterns to Drop In
- "{relatable_pattern}" → "{conversation_hook}"
- ...
```

**Graceful fallback:** If competitor scan or industry tools data is absent, generate this section from general industry knowledge as before.

---

### Section 7: Pre-Call Checklist

```markdown
## Pre-Call Checklist

- [ ] Review this brief (5 min)
- [ ] Have the demo ready showing {industry}-relevant features
- [ ] Prepare rough ROI calculator (need: staff count, avg hourly rate, estimated admin hours/week)
- [ ] {Industry-specific prep item}
- [ ] {Any specific prep from research/phone analysis}
```

---

## After Generation

1. **Save to:** `clients/{client_slug}/prospect-brief.md`
2. **Update `prospect-profile.json`:** Set `prospect_brief_generated: true`
3. **CRM Document Sync:**
   - If `crm.document_id` is set → `update_document(document_id, content: brief_markdown)`
   - If null → look up or create "Prospect Brief" document on the contact (same logic as RC step)
   - Store `document_id` in `crm.document_id` if newly created/found
   - Best-effort — if CRM calls fail, log warning and continue.
4. **CRM Lead Comment** — If `crm.lead_id` is set in prospect-profile.json:
   - `create_lead_comment(lead_id, content)`:
     ```
     Prospect brief generated for {contact_name} with full call prep.
     Waste areas identified: {count}. Key labels: {label1}, {label2}.
     Overall prep confidence: {HIGH/MEDIUM/LOW based on data quality}.
     Prospect brief synced to CRM.
     ```
   - Best-effort — if CRM call fails, log warning and continue.
5. **Present the prospect brief** for review
6. **Ask:** "Anything to adjust? Once you're happy with it, you're ready for the call."

## Notes

- The prospect brief is an internal document — it's for Adam, not the client. Write in direct, practical language.
- Every tailored question and label must trace to something specific we know (research or phone). If it's generic, it doesn't belong.
- Match the depth and specificity of `clients/noah-caring-ways/discovery-call-prep.md`. That's the benchmark.
