---
name: analyze-transcript
description: Extract buying signals, pain points, tools, and objection risks from pre-discovery phone call transcript
menu-code: AT
---

# [AT] Analyze Transcript

## Purpose

Extract actionable sales intelligence from a pre-discovery phone call transcript. This is lighter than the Close agent's 4-pass audit-data-lite extraction — focused on sales intelligence for call prep, not full process mapping.

## Prerequisites

- `{client_slug}` must be set
- A phone call transcript must be available (in `clients/{client_slug}/meetings/` or pasted by the user)

## Getting the Transcript

Check for transcripts in order:

1. **Scan `clients/{client_slug}/meetings/`** — look for unprocessed transcript files
2. **If none found**, ask: "I don't see a transcript on file. You can either:
   - Paste the transcript here and I'll save it to `clients/{client_slug}/meetings/{YYYY-MM-DD}-phone-call/transcript.txt`
   - Provide a file path to the transcript"

When saving a pasted transcript:
- Create directory: `clients/{client_slug}/meetings/{today's date}-phone-call/`
- Save as `transcript.txt`
- Create a minimal `metadata.json`: `{"type": "phone-call", "date": "{today}", "source": "manual-paste"}`

## Extraction — Single Pass, Five Lenses

Read the entire transcript and extract through these five lenses simultaneously. For each finding, include the **verbatim quote** that supports it.

### A. Buying Signals

Categorize each signal as **HIGH**, **MEDIUM**, or **LOW** intent:

**HIGH intent indicators:**
- Emotional language about pain ("it's fucking annoying", "drives me crazy", "nightmare")
- Committed to change ("I'm gonna move off it", "we need to sort this out")
- Forward-looking questions ("when could we start?", "what does the process look like?")
- Specific problems raised unprompted (they brought it up, not you)

**MEDIUM intent indicators:**
- General frustration ("it's not great", "we're struggling")
- Exploring options ("we're looking at a few things")
- Implied timeline ("before the end of the year", "soon")

**LOW intent indicators:**
- Vague interest ("just seeing what's out there")
- No emotional language
- Short, closed answers

**Output format:**
```
| Signal | Quote | Intent |
|---|---|---|
| Committed to leaving current tool | "I'm gonna move off of it" | HIGH |
```

### B. Current Tools & Stack

Every software, tool, system, or manual process mentioned:

```
| Tool | What It's Used For | Stated Problems | Status |
|---|---|---|---|
| {name} | {use case} | {problems mentioned} | Keeping / Leaving / Undecided |
```

### C. Pain Signals

Categorize by waste type for later mapping to the CLOSER framework:

- **Usability** — tool is hard to use, staff avoid it
- **Bottleneck** — one person everyone depends on
- **Double handling** — same data entered twice across systems
- **Compliance risk** — things not being done properly
- **Missing capability** — can't do something they need
- **Tool sprawl** — too many disconnected systems
- **Manual process** — doing by hand what could be automated

```
| Pain | Waste Type | Quote | Speaker |
|---|---|---|---|
| {description} | {type} | "{verbatim}" | {who said it} |
```

### D. Decision Context

Extract context about how they'll make the buying decision:

- **Other stakeholders** — Who else is involved? (partner, ops manager, board, accountant)
- **Urgency** — How soon do they want this resolved? (committed timeline vs. browsing)
- **Budget signals** — Any mention of what they're paying now or budget constraints
- **Timeline** — When do they want this sorted by?
- **Trigger event** — What specifically prompted this call?

### E. Objection Risks

What might come up on the discovery call:

- Mentioned constraints (budget, time, team resistance to change)
- Unresolved questions they asked on the phone
- Hesitations or qualifiers in their language ("maybe", "I'm not sure", "we'd have to see")
- Specific concerns raised

For each identified risk, map to the relevant **AAA handler** from `sales-plugin/references/hormozi-closer-framework.md`:

```
| Objection Risk | Evidence | Recommended AAA Handler |
|---|---|---|
| {objection} | "{quote or behaviour}" | {handler from framework} |
```

## Overall Buying Intent Rating

Based on all five lenses, rate overall intent:

- **HIGH** — Emotional pain + committed to change + specific problems + timeline pressure
- **MEDIUM** — Real frustration but no urgency, or urgent but vague on the problem
- **LOW** — Browsing, no emotional language, short answers

## Save Analysis

Update `clients/{client_slug}/audit/prospect-profile.json` with a `phone_analysis` block:

```json
{
  "phone_analysis": {
    "call_date": "{date}",
    "transcript_path": "meetings/{folder}/transcript.txt",
    "duration_estimate": "{if available}",
    "overall_buying_intent": "HIGH|MEDIUM|LOW",
    "buying_signals": [
      {"quote": "", "signal_type": "", "intent": "HIGH|MEDIUM|LOW"}
    ],
    "current_tools": [
      {"name": "", "use_case": "", "stated_problems": "", "status": "keeping|leaving|undecided"}
    ],
    "pain_signals": [
      {"description": "", "waste_type": "", "quote": "", "speaker": ""}
    ],
    "decision_context": {
      "other_stakeholders": [],
      "urgency": "",
      "budget_signals": "",
      "timeline": "",
      "trigger_event": ""
    },
    "objection_risks": [
      {"objection": "", "evidence": "", "recommended_handler": ""}
    ]
  },
  "phone_transcript_analyzed": true
}
```

## Present Summary

Display with the buying intent rating prominently:

```
## Phone Call Analysis — {Contact Name}, {Company Name}

**Overall Buying Intent: {HIGH/MEDIUM/LOW}**

### Buying Signals ({count})
{table}

### Current Tools ({count})
{table}

### Pain Signals ({count})
{table}

### Decision Context
- Stakeholders: {list}
- Urgency: {level}
- Budget signals: {any}
- Trigger: {what prompted the call}

### Objection Risks ({count})
{table with AAA handlers}
```

Ask: "Anything to correct before I save? Did I miss any signals from the call?"

## Update Prospect Brief & Sync to CRM

After saving phone analysis to prospect-profile.json, regenerate `clients/{client_slug}/prospect-brief.md` from the full prospect-profile.json data.

The brief now includes phone analysis data:
- **What We Know > From Phone Call** — Buying intent rating, top signals with inline quotes, decision context
- **Key Pain Signals** — Merge research hypotheses + phone evidence. Phone-confirmed signals first, then research-only hypotheses. De-duplicate where a hypothesis matches confirmed evidence (keep the phone-confirmed version).
- **Pipeline footer** — Mark Phone analysis ✓

Follow the same template structure as defined in `references/prospect-brief-template.md`. If [BC] has not been run, the Discovery Call Prep section still shows "Run [BC] to generate call prep."

**CRM Document Sync:**

1. If `crm.document_id` is set → `update_document(document_id, content: brief_markdown)`
2. If null → look up or create "Prospect Brief" document on the contact (same logic as RC step)
3. Store `document_id` in `crm.document_id` if newly created/found
4. Best-effort — if CRM calls fail, log warning and continue.

## CRM Lead Comment

After saving to prospect-profile.json, if `crm.lead_id` is set:

- `create_lead_comment(lead_id, content)`:
  ```
  Phone transcript analyzed. Buying intent: {HIGH/MEDIUM/LOW}.
  Pain signals: {count} ({top waste types}).
  Tools mentioned: {tool list}.
  Objection risks: {count}.
  Prospect brief updated and synced to CRM.
  ```
- Best-effort — if CRM call fails, log warning and continue.

## Notes

- Do NOT write any intermediate files. Only `prospect-profile.json` and `prospect-brief.md` get written.
- Every finding must include a verbatim quote. If you can't cite it, don't include it.
- This is sales intelligence, not process mapping. Keep findings focused on what helps prep the discovery call.
