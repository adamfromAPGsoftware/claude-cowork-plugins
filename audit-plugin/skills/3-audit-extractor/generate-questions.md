---
name: generate-questions
description: Audit audit data against all deliverable requirements, cross-reference transcripts, generate targeted follow-up questions, research researchable ones, export client-ready email.
menu-code: GQ
---

# Generate Questions (GQ)

> **Idempotent.** Re-running picks up new gaps and skips already-classified/researched questions. Safe to run after every extraction.

## Purpose

Single command for the post-extraction workflow. Audits the audit data against everything the deliverables need (waste.html, findings.html, process-map.html), cross-references transcripts to catch already-answered items, generates targeted follow-up questions for unresolved gaps, researches what's researchable via exa, and exports a concise client-ready email.

**When to run:** After every SU extraction. Also useful at any audit stage to see "what do we still need?"

---

## Step 1: Load & Inventory

1. Client slug from activation. Load `clients/{client_slug}/audit/audit-data.json`.

2. Count and display:
   ```
   AUDIT DATA INVENTORY — {company_name}
   ══════════════════════════════════════════
   Audit status:      {audit_status}
   Sessions:          {sessions_completed}
   Process steps:     {count across all stages}
   Pain points:       {n}
   Optimisations:     {n}
   Waste items:       {n} ({quantified} quantified, {unquantified} unquantified)
   Staff roster:      {n} entries ({with_rate} have hourly rates)
   Follow-up Qs:      {pending} pending | {answered} answered | {researched} researched
   ```

---

## Step 2: Deliverable Readiness Audit

Check readiness across three deliverable dimensions plus staff rates. This is the core gap-finding logic.

### 2a. Waste Quantification Readiness (drives waste.html)

For each `waste_items[]` entry, classify into one of three categories:

**Time-based waste items** (the standard model — hours × rate × 52):
- Check `hours_per_week` present (null = **hard gap**)
- Check `headcount_affected` present (null = gap, default 1 is acceptable if single person stated)
- Check `hourly_rate_aud` present AND `rate_is_estimated == false` (estimated = **soft gap** — calculable but unreliable)
- Check `annual_waste_aud` derivable: all three above must be non-null

**Revenue leakage items** (hours_per_week is null by design — these measure lost money, not lost time):
- Identify by waste_type `"missing_automation"` or `"no_followup"` where the description references revenue, conversion, or financial loss
- Check if `annual_waste_aud` is populated with a custom formula
- If null, flag need for three data points: **volume metric** (occurrences per year, lost leads per month), **per-unit value** (avg plan value, avg customer value), **miss/loss rate** (% missed, % churned)

**One-off items** (not recurring waste):
- Identify items describing a one-time cleanup or retroactive fix
- Flag these separately — they shouldn't inflate the annual waste figure
- Suggest removing from recurring waste or adding a `recurring: false` flag

Build a per-item status table:

```
WASTE QUANTIFICATION READINESS
──────────────────────────────────────────────────────────────────────
ID     │ Type          │ hrs/wk │ rate    │ annual    │ Gaps
───────┼───────────────┼────────┼─────────┼───────────┼──────────────
W-001  │ Time-based    │ ✗      │ $50 est │ ✗         │ Need hrs/wk, rate
W-005  │ Time-based    │ 15     │ $50 est │ $36,000*  │ Need real rate
W-010  │ Rev. leakage  │ n/a    │ n/a     │ ✗         │ Need volume, value, miss rate
W-012  │ Time-based    │ 20     │ $50 est │ $48,000*  │ Need real rate
W-019  │ One-off       │ n/a    │ n/a     │ ✗         │ Not recurring — flag
──────────────────────────────────────────────────────────────────────
* = calculated using estimated rate

Summary: {n}/{total} fully quantified | {n} on estimated rates | {n} revenue leakage unquantified
```

### 2b. Findings Readiness (drives findings.html)

- Count `pain_points[]` by confidence: HIGH / MEDIUM / LOW
- Check which stages have zero pain points — flag as potential blind spots
- Count `optimisations[]` and check coverage
- findings.html doesn't require quantification — it's discovery data. Flag only if a stage has NO findings at all.

```
FINDINGS READINESS
  Pain points:    {n} (HIGH: {n}, MEDIUM: {n}, LOW: {n})
  Optimisations:  {n}
  Stages with no findings: {list or "none — all covered"}
```

### 2c. Process Map Readiness (drives process-map.html)

Run the same checks AC uses:

**Tool coverage:**
- Count steps with non-empty `tool_ids[]` vs total steps
- Flag steps where description implies a tool ("enter", "update", "send", "log", "export", "import", "sync") but `tool_ids` is empty

**Data flow coverage:**
- Count steps with `data_flow` populated vs total eligible steps (exclude first step per stage)
- Count `mechanism: "unknown"` entries

**Stage coverage:**
- Check for stages in `business_stages_covered` with zero process steps

```
PROCESS MAP READINESS
  Tool coverage:      {n}/{total} steps ({pct}%) — {n} steps imply tools but have none
  Data flow coverage: {n}/{total} handoffs ({pct}%) — {n} unknown mechanisms
  Empty stages:       {list or "none"}
```

### 2d. Staff Rate Readiness

- Check each `staff_roster[]` entry for missing `hourly_rate` (or equivalent salary data)
- Check `blended_hourly_rate_aud` and `blended_rate_confidence`
- Count how many waste items use `rate_is_estimated: true`

```
STAFF RATE READINESS
  Roster entries with rates: {n}/{total}
  Blended rate confidence:   {level}
  Waste items on estimated rate: {n}/{total}
  ⚠ {impact statement — e.g., "All waste calculations use $50/hr fallback — total waste figure is unreliable until real rates are provided"}
```

---

## Step 3: Transcript Cross-Reference

For each gap identified in Step 2 AND each existing `follow_up_questions[]` with `status: "pending"`:

### 3a. Search transcripts

Use Grep to search `clients/{client_slug}/meetings/*/transcript.txt` for key terms extracted from the question or gap description. For example:
- A gap about {STAFF_NAME}'s salary → search for "salary", "pay", "rate", "wage", "{STAFF_NAME}" + "earn"/"cost"/"paid"
- A gap about families per week → search for "families per week", "new families", "how many join", "per week"
- A gap about BDM bonus time → search for "bonus", "calculation", "hours", "how long"

Run 2-3 targeted searches per gap. Scan results for relevant context.

### 3b. Classify findings

For each gap/question searched:

**Found in transcript — data was stated:**
If the data point was explicitly stated (e.g., "we get about 10 new families a week"), flag as:
- "Data stated in Session {n} but not extracted into audit data"
- This is an **extraction gap** → recommend re-running EB on that session, not a follow-up question
- Quote the relevant transcript excerpt

**Found in transcript — mentioned but not answered:**
If the topic was discussed but the specific data wasn't given (e.g., they talked about salary but didn't state numbers), note this and still generate the follow-up question — but reference the conversation: "You discussed X in session {n} — can you confirm the specific number?"

**Not found in transcripts:**
Proceed to Step 4 — this is a genuine gap that needs a follow-up question.

### 3c. Present findings

```
TRANSCRIPT CROSS-REFERENCE
──────────────────────────────────────────────────────────────
✓ FOUND — likely answered in transcripts:
  • "{STAFF_NAME}'s hourly rate" — Session 3 [42:15]: "{STAFF_NAME} is on about $75k"
    → Extraction gap — re-run EB to capture this

⚠ DISCUSSED but not answered:
  • "Families per week" — Session 2 [18:30]: discussed family onboarding volume
    but no specific number stated → Still needs follow-up question

✗ NOT FOUND in any transcript:
  • "Sherilyn's hourly rate" — no mention of VA pay in any session
  • "Time for pay-week reminders" — process mentioned but time never discussed
──────────────────────────────────────────────────────────────
```

**Pause:** "I found {n} items that may already be answered in transcripts. Please confirm which ones are genuinely answered before I proceed."

Wait for user confirmation. Mark confirmed items as `status: "answered"` with `answered_in_session` set. Never auto-resolve.

---

## Step 4: Generate New Questions

For each unresolved gap from Step 2 that was NOT found in transcripts (Step 3):

### Question format rules (same as CC)

- Reference their own words where possible ("You mentioned X — can you tell me...")
- Ask for exactly what's missing (a number, a name, a process step)
- Never ask compound questions (one gap = one question)
- Frame around their experience ("How long does that typically take?" not "What is the duration?")

### Priority assignment

- **HIGH** — blocks waste calculation: missing `hours_per_week`, `hourly_rate_aud`, or revenue leakage data for any waste item
- **HIGH** — blocks multiple items: a single data point (e.g., "families per week") that unlocks 3+ waste items
- **MEDIUM** — upgrades confidence: would move an item from LOW to MEDIUM/HIGH, or fill a findings/process map gap
- **LOW** — context enrichment: nice to have but not blocking any deliverable

### Consolidation

Before generating individual questions, group related gaps:
- If multiple waste items need the same data point (e.g., "families per week" unlocks W-002, W-009, W-016), generate ONE question, not three
- If salary data is needed for multiple roles, group into one salary question block rather than individual questions
- Note which waste items each question unlocks in the `reason` field

### Deduplication

Before adding each question to the audit data:
- Check existing `follow_up_questions[]` for semantic matches (not just string matches)
- If a matching question exists with `status: "pending"`, skip — don't create a duplicate
- If a matching question exists with `status: "answered"` or `"researched"`, skip — it's already resolved
- Assign `question_id` continuing from the highest existing FQ-NNN

### Tag each question

Set on each new audit data entry:
- `question_id`: FQ-{NNN}
- `question`: the question text
- `stage`: relevant stage slug
- `priority`: HIGH / MEDIUM / LOW
- `reason`: what this unlocks (e.g., "Unlocks W-001, W-003 waste calculation — need hrs/wk for HubSpot admin")
- `status`: "pending"
- `classification`: pre-classify as `"researchable"` or `"client_required"` using FQ's rules (Step 5 will confirm)
- `deliverable_impact`: array of which deliverables this question affects — `["waste"]`, `["findings"]`, `["process_map"]`, or combinations

---

## Step 5: Classify & Research

Apply the classification and research logic below.

### Classification rules

**researchable** — answer findable via web search:
- Names a specific tool, API, platform, or software product
- Asks about pricing, features, integrations, or technical capabilities
- Asks about regulatory or compliance information publicly available
- Asks about industry benchmarks or publicly available data

**client_required** — only the client can answer:
- Asks about their specific internal process, timing, or headcount
- Asks about business decisions, preferences, or future plans
- Asks about specific dollar amounts internal to their business (salaries, revenue, costs)
- Asks about specific staff roles, names, or responsibilities
- Asks about how they personally use a tool (not what the tool can do)

### Research (for researchable questions)

Use `mcp__exa__web_search_exa` with API research discipline:
- For API questions: capture specific endpoints, HTTP methods, parameters, documentation URLs
- Confidence: HIGH = official docs with endpoints, MEDIUM = confirmed via third-party, LOW = no docs found
- Set `status: "researched"`, `research_answer`, `research_confidence`, `research_sources`, `researched_at`

**Skip** any questions already classified or researched from a prior GQ run.

---

## Step 6: Export Client Email

Generate markdown at:
```
clients/{client_slug}/follow-up-emails/{YYYY-MM-DD}-follow-up-questions.md
```

Use current date. Overwrite if file exists (latest run wins).

### Voice Rules — Apply to All Client-Facing Text

Read `shared-references/adam-email-voice.md` before generating the export. This document gets emailed to the client — it must sound like Adam personally wrote it. Key constraints:

- Greeting: "Hey {contact.name},"
- Contractions mandatory — "we've", "don't", "I've", "that's". Never "we have", "do not".
- Use natural qualifiers — "just", "roughly", "ballpark"
- No corporate jargon. No AI tells.
- Vary paragraph length.
- **Forbidden in client-facing text:** "we'd love to clarify", "furthermore", "additionally", "it's important to note", "comprehensive", "facilitate", "feel free to reach out", "please don't hesitate", "leverage", "utilize"

### Format

The document must be **client-ready** — no internal jargon (no "audit-data.json", no "FQ-001", no "HIGH confidence"). Written in `{communication_language}` from config.

```markdown
# Follow-Up Questions — {company_name}

Prepared: {date} | Sessions completed: {sessions_completed}

---

## Questions for Our Next Conversation

Hey {contact.name or company shortname},

{1-2 sentences referencing specific sessions and areas covered. Be direct —
state what you need and why. Use Adam's natural qualifiers ("just", "roughly",
"ballpark"). Never use "we'd love to", "please don't hesitate", or any phrase
from the forbidden list. Example tone: "We've mapped out [areas] across your
[N] sessions. To lock in the waste figures, I just need a few ballpark numbers
from you — most are quick answers, no need to dig through records."}

---

### Salary & Wage Data

{Only include if staff rate gaps exist. Brief explainer in Adam's voice — e.g.,
"To calculate the real cost of manual work, I just need approximate rates for
each role. Ballpark is fine — we can refine later."}

1. **{Name} ({Role})** — approximate salary or hourly rate?
   _{One-line context if HIGH priority}_

---

### Weekly Volumes

{Only include if volume multiplier gaps exist. Brief explainer in Adam's voice —
e.g., "These turn the per-task times into annual figures."}

N. **{Question}**
   _{Context}_

---

### Time Estimates

{Only include if per-task time gaps exist.}

N. **{Question}**

---

### Revenue & Financial Data

{Only include if revenue leakage gaps exist.}

N. **{Question}**
   _{Context}_

---

### Process Clarification

{Only include if process map or findings gaps exist.}

N. **{Question}**

---

### Tool Costs & Other

{Catch-all for remaining questions.}

N. **{Question}**

---

## Already Answered via Research

{Only include if researched questions exist.}

We looked these up ourselves — just sharing in case any need correcting.

| # | Question | What We Found | Source |
|---|----------|---------------|--------|
| 1 | {question} | {research_answer} | {source} |

---

*Prepared by {YOUR_COMPANY} — {YOUR_DOMAIN}*
```

### Section rules

- **Omit empty sections entirely** — if no salary gaps, don't show the Salary section header
- **Consolidate related questions** — salary questions for multiple roles go in one numbered block, not separate items
- **Include context lines** for HIGH priority questions only — one sentence explaining why
- **Keep it concise** — the goal is minimum questions for maximum data. If one question unlocks 3 waste items, phrase it as one question
- **Sequential numbering** across all sections (1, 2, 3... not restarting per section)
- **Stage name formatting:** Convert slugs to readable names (acquisition → "Acquisition", onboarding_family → "Family Onboarding", payroll_invoicing → "Payroll & Invoicing", etc.)
- **Priority descriptions** (if used in section headers):
  - HIGH: "These are the ones that unlock the biggest numbers"
  - MEDIUM: "Would sharpen a few specific areas"
  - LOW: "Nice to have, not urgent"

### Post-Generation Voice Check

Before presenting the export:
1. Scan every sentence against the forbidden phrases list in `adam-email-voice.md`
2. Check: no sentence starts with "Furthermore", "Additionally", "Moreover"
3. Check: contractions used throughout (no "we have", "do not", "it is")
4. Check: paragraph lengths vary
5. Ask: "Would Adam copy-paste this into Gmail without editing?" If not — rewrite.

---

## Step 7: Save & Summarise

1. Write all new/updated `follow_up_questions[]` back to the audit data.

2. Display combined report:

```
GENERATE QUESTIONS COMPLETE — {company_name}
══════════════════════════════════════════════════════════════

DELIVERABLE READINESS
  waste.html:       {n}/{total} items fully quantified ({pct}%)
  findings.html:    {status — "ready" or "{n} stages with no findings"}
  process-map.html: {pct}% tool coverage, {pct}% data flow coverage

WASTE QUANTIFICATION GAPS
  Missing hours/week:           {n}
  Missing headcount:            {n}
  On estimated rate:            {n}
  Revenue leakage unquantified: {n}

TRANSCRIPT CROSS-REFERENCE
  Found in transcripts:  {n} (extraction gaps — re-run SU)
  Discussed not answered: {n}
  Not found:             {n}

QUESTIONS
  New generated:    {n}
  Researched (exa): {n}
  Client-required:  {n} (in exported email)
  Total pending:    {n}

Exported: clients/{client_slug}/follow-up-emails/{YYYY-MM-DD}-follow-up-questions.md

Next steps:
  1. Send the exported email to {contact.name or "the client"}
  2. After receiving answers, run [SU] to re-extract and then [GQ] to check remaining gaps
```
