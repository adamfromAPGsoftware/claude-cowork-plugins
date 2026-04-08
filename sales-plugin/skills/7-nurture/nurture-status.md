---
name: nurture-status
description: Dashboard showing all active nurture sequences, current steps, and next actions
menu-code: NS
---

# Nurture Status Dashboard

## Purpose

Show a complete overview of all nurture sequences — active, paused, completed, and leads not yet started. Provides visibility into the entire post-discovery pipeline from a nurture perspective.

## Process

### Step 1: Pull All Post-Discovery Leads

Use `list_leads` with limit 100. Filter to post-discovery stages:
- "Discovery Call - Completed"
- "Qualified"
- "Proposal"
- "Initial Follow-Up Phone Call"
- "Not Showing up to Discovery Call (Need Harassment)"
- "Need Re-Activation"

### Step 2: Categorise Each Lead

For each lead, read `list_lead_comments` and categorise:

- **Active** — Has `[NURTURE-START]` but no terminal tag (complete/replied/paused)
- **Paused** — Has `[NURTURE-PAUSED]`
- **Completed** — Has `[NURTURE-COMPLETE]`
- **Replied** — Has `[NURTURE-REPLIED]`
- **Not Started** — No nurture tags at all
- **Skipped** — Has `[NURTURE-SKIP]`

### Step 3: Enrich Active Sequences

For active sequences, extract from the most recent `[NURTURE]` comment:
- Current step (N1-N5)
- Next step and due date
- Scenario (A/B/C/D)

For each active lead, also check:
- `get_contact` for `last_communication_at` and `sentiment_label`
- Days since last nurture email was drafted

### Step 4: Present Dashboard

```
## Nurture Dashboard — {today's date}

### Active Sequences ({count})

| Lead | Contact | Scenario | Current Step | Next Step | Due | Days Silent |
|------|---------|----------|-------------|-----------|-----|-------------|
| {title} | {name} | {A/B/C/D} | N{X} | N{Y} | {date} | {days} |

### Due Today ({count})
- **{Company}** — N{X} "{theme}" ready to draft
- ...

### Overdue ({count})
- **{Company}** — N{X} was due {date} ({days} days ago)
- ...

### Replied — Human Takeover Needed ({count})
- **{Company}** — Replied {date}. Last nurture step: N{X}. Check Gmail.

### Paused ({count})
- **{Company}** — Paused at N{X}. Reason: {from comment if available}

### Completed ({count})
- **{Company}** — All 5 emails sent. Last: {date}. No reply.

### Not Yet Started ({count})
- **{Company}** — Stage: {stage}, Last comm: {date}. Eligible for nurture.

### Skipped — Missing Data ({count})
- **{Company}** — No audit-data-lite.json. Needs data extraction first.

### Summary
- Total post-discovery leads: {count}
- In active nurture: {count}
- Due today: {count}
- Replied (needs human): {count}
- Not started (eligible): {count}
- Missing data: {count}
```
