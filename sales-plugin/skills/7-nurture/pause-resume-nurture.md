---
name: pause-resume-nurture
description: Pause or resume a lead's nurture sequence
menu-code: NPR
---

# Pause / Resume Nurture

## Purpose

Manually pause or resume a lead's nurture sequence. Use when Adam or the sales team wants to hold off on automated follow-ups (e.g. lead is in a meeting cycle, there's a sensitive situation, or they want to take over manually).

## Process

### Step 1: Identify the Lead

Ask: "Which lead do you want to pause or resume? Give me a name, company, or lead ID."

Search and confirm the lead (same as `single-lead-nurture.md` Step 1).

### Step 2: Check Current State

Read `list_lead_comments` and determine:
- Is the sequence active? → Can pause
- Is the sequence paused? → Can resume
- Is the sequence complete or replied? → Neither — inform user

Present current state:
```
Lead: {title}
Contact: {name}
Current nurture state: {Active at N{X} / Paused at N{X} / Complete / Replied / Not started}
```

### Step 3: Execute Action

#### To Pause:

Ask: "Any reason to note? (optional — helps when reviewing later)"

Add comment:
```
[NURTURE-PAUSED] Sequence paused at Step N{X} by {user_name}
Reason: {reason if provided, otherwise "Manual pause"}
Resume with [NPR] when ready.
```

Confirm: "Sequence paused. No more nurture emails will be drafted until you resume."

#### To Resume:

Show where the sequence left off:
```
Sequence was paused at Step N{X}.
Next step would be N{Y}, originally due {date}.
```

Ask: "Resume from N{Y}? I'll recalculate the remaining schedule from today."

If confirmed, recalculate remaining dates from today using the original scenario's gap pattern, then add comment:
```
[NURTURE-RESUME] Sequence resumed from Step N{Y}
New schedule: N{Y} {date}, N{Z} {date}, ...
Previous pause reason: {reason}
```

Confirm: "Sequence resumed. Next email (N{Y}) due {date}."
