# Prospect Brief Template

Reference skeleton for consistent output. See `research-client.md` (initial generation) and `build-battle-card.md` (full generation with call prep) for rules.

```markdown
<!-- Auto-generated from prospect-profile.json. Do not edit manually. -->
# Prospect Brief — {Company Name}

**Contact**: {name} | **Email**: {email} | **Phone**: {phone}
**Domain**: {domain} | **Industry**: {industry_tag} | **Location**: {location}
**ABN**: {abn} | **Team size**: {estimate} | **Est.**: {year}

---

## What They Do
{2-3 sentence company description. Services: comma-separated list.}

## What We Know

### From Research
- {Top 3-5 bullet points: key findings, competitor edges, notable signals}

### From Phone Call
{If analyzed: buying intent rating, top signals with inline quotes, decision context}
{If not: "No pre-call transcript analyzed."}

## Key Pain Signals
| # | Signal | Source | Confidence |
|---|---|---|---|
| 1 | {description} | {research/phone/both} | HIGH/MEDIUM/LOW |
{Max 5-6 rows. Phone-confirmed first, then research hypotheses.}

## Competitive Context
{2-3 sentences on local landscape + 2-3 bullet competitor edges}

## Industry Tools & Patterns
| Category | Common Tools | Reality |
|---|---|---|
| {category} | {tools} | {what actually happens} |

**Relatable patterns:**
- "{pattern}" → Ask: "{conversation_hook}"

---

## Discovery Call Prep

{If [BC] has not been run: "Run [BC] to generate call prep."}

### Waste Areas to Explore
| Waste Type | What to Ask | Why It Matters |
|---|---|---|
| {type} | "{specific open-ended question}" | {reason} |
{6-12 rows, open-ended questions only}

### CLOSER Framework

#### C — Clarify: Why Are You Here?
**Opening questions**:
- "{tailored question 1}"
- "{tailored question 2}"
- "{tailored question 3}"

#### L — Label: Name the Pattern
1. **{Label}**: "{tailored phrasing}"
2. **{Label}**: "{tailored phrasing}"

**Then confirm**: "Does that feel like a fair summary of where you're at?"

#### O — Overview: What Have You Already Tried?
- "{question about competitors/alternatives}"
- "{question about previous attempts}"
- "{question about ideal setup}"

#### S — Sell the Vacation
"{Dream state paragraph tailored to industry and team size}"

**Anchor questions**:
- "{quantifying question 1}"
- "{quantifying question 2}"
- "{quantifying question 3}"

#### E — Explain Concerns
**"{Objection}"**
- **Acknowledge**: "{...}"
- **Associate**: "{...}"
- **Ask**: "{...}"

#### R — Reinforce: Close to the Audit
- Summarise pain in their words
- Quantify: staff x hours x rate
- Audit: $3,000, 2-4 weeks
- Guarantee: $5K/month savings or money back
- Credit: 100% toward the build

### Talking Points
- {Industry-specific experience}
- {Compliance/regulatory context}
- {Competitor insights to reference}
- {Relatable patterns to drop in}

### Pre-Call Checklist
- [ ] Review this brief (5 min)
- [ ] Have demo ready showing {industry}-relevant features
- [ ] Prepare ROI calculator (need: staff count, avg hourly rate, admin hours/week)
- [ ] {industry-specific item}

---
**Pipeline**: {✓/○} Research | {✓/○} Phone analysis | {✓/○} Call prep | Discovery: {date or TBD}
```
