---
name: sync-and-update
description: Fetch new Fathom meetings, scan client materials, and extract all unprocessed inputs into the audit data file. The one command to run after every session.
menu-code: SU
---

# Sync & Update

## Purpose

One command to run after every session. Fetches new Fathom recordings, scans client-provided materials for new files, then extracts all unprocessed inputs into the audit data file (`audit-data.json`). Creates the audit data file from schema if it doesn't exist yet.

Every finding gets a confidence score and a verbatim quote. Every gap becomes a follow-up question.

---

## Pipeline

Client slug is already set from activation (`{client_slug}`). Run all stages autonomously. Do not pause for user input between stages.

---

### Stage 1a — Fetch Fathom Meetings

```bash
python3 scripts/fetch-transcripts.py --client-slug {client_slug}
```

After fetching, rescan `clients/{client_slug}/meetings/` for all subdirectories containing `transcript.txt`. For each, read its `metadata.json` to get `fathom_meeting_id`.

Load `clients/{client_slug}/audit/audit-data.json` (create fresh from `references/audit-data-schema.md` if it doesn't exist).

Cross-reference meeting folders against `sessions[]` by `fathom_meeting_id`:
- **New** — meeting folder exists, no matching session at all
- **Unanalyzed** — session exists with `analyzed: false`
- **Done** — session exists with `analyzed: true`

Print status table:

```
MEETING SYNC — {company_name}
─────────────────────────────────────────────────────
  Folder                          Date        Status
  ──────────────────────────────  ──────────  ──────────
  {folder}                        {date}      NEW
  {folder}                        {date}      UNANALYZED
  {folder}                        {date}      DONE
─────────────────────────────────────────────────────
  New: {n}  |  Unanalyzed: {n}  |  Done: {n}
```

---

### Stage 1b — Sync Google Drive Folder

If `google_drive_folder_url` is set in `audit-data.json`:

```bash
python3 scripts/fetch-drive-folder.py --client-slug {client_slug}
```

Downloads new files into `clients/{client_slug}/client-provided-materials/google-drive/`. The script reads the folder URL from audit-data.json automatically. Files already downloaded are skipped.

Print status:

```
GOOGLE DRIVE SYNC — {company_name}
─────────────────────────────────────────────────────
  New files: {n}  |  Already downloaded: {n}
```

If `google_drive_folder_url` is empty or not set, skip silently.

---

### Stage 1d — Fetch Client Emails

```bash
python3 scripts/fetch-emails.py --client-slug {client_slug}
```

After fetching, rescan `clients/{client_slug}/client-provided-materials/emails/` for new subdirectories. Each contains `email.txt` (body), `metadata.json`, and any attachment files. Cross-reference against `extracted_materials[]` by `source_file` to determine NEW vs ALREADY EXTRACTED.

Print status:

```
EMAIL SYNC — {company_name}
─────────────────────────────────────────────────────
  Folder                          Date        Status
  ──────────────────────────────  ──────────  ──────────
  {folder}                        {date}      NEW
  {folder}                        {date}      ALREADY EXTRACTED
─────────────────────────────────────────────────────
  New: {n}  |  Already extracted: {n}
```

If `fetch-emails.py` fails (no credentials, no domain configured), print warning and continue:
```
Gmail sync skipped — {reason}. Run: python3 scripts/fetch-emails.py --auth
```

---

### Stage 1e — Scan Client-Provided Materials

Scan `clients/{client_slug}/client-provided-materials/` for all files (any extension).

For each file found, check whether it is already referenced in:
- `extracted_materials[]` — any entry with a matching `source_file` field

Files not referenced are **unprocessed materials**.

Print materials status:

```
CLIENT-PROVIDED MATERIALS — {company_name}
─────────────────────────────────────────────────────
  File                            Status
  ──────────────────────────────  ──────────────────
  {filename}                      UNPROCESSED
  {filename}                      ALREADY EXTRACTED
─────────────────────────────────────────────────────
  Unprocessed: {n}  |  Already extracted: {n}
```

If `client-provided-materials/` does not exist, note: "client-provided-materials/ not found — skipping."

---

### Stage 2 — Extract All Unprocessed Inputs

If no new meetings and no unprocessed materials:
```
Nothing to extract — all inputs already processed.
```
Skip to Stage 4.

Otherwise, process ALL unextracted meetings (NEW or UNANALYZED) and ALL unprocessed client-provided-materials files in chronological order. Run autonomously without pausing between resources.

**Single resource mode:** If the user explicitly asks to extract just one resource, list all available inputs and let them pick. Then extract only that one using the same pipeline below.

#### 2a. Load Audit Data

If `clients/{client_slug}/audit/audit-data.json` exists, load it — findings will be merged in.
If not, create a fresh audit data file using the schema in `references/audit-data-schema.md`.

#### 2b. Process Each Input

For each unextracted meeting and unprocessed file (chronological order):

**CRITICAL: `sessions[]` is for Fathom meetings ONLY.** Emails, PDFs, and other client-provided materials are NOT sessions. They are tracked in `extracted_materials[]` and any data extracted from them updates existing audit-data fields (staff records, business metrics, constraints, etc.) with `source_material` instead of `source_session`.

**If the resource is a Fathom meeting:**

- Read `clients/{client_slug}/meetings/{folder}/transcript.txt`
- Read `clients/{client_slug}/meetings/{folder}/metadata.json` — store `fathom_meeting_id` and `fathom_url`
- Determine session number: count existing sessions with `analyzed: true`, add 1
- Run the full **5-pass extraction** (see Extraction Passes below)
- Tag Fathom timestamps on all extracted steps and tools
- Append/update session entry in `sessions[]` with `analyzed: true`

**If the resource is a client-provided-materials file (email, PDF, doc, etc.):**

- Read the file content
- Extract any useful data (contact details, business metrics, constraints, staff info, etc.)
- Update existing audit-data fields directly (e.g. add to `business_metrics[]`, `constraints[]`, `staff_roster[]`)
- On each extracted item, use `"source_material": "{relative path}"` instead of `"source_session"`. Leave `source_timestamp_seconds: null` and `meeting_references: []`.
- Add an entry to `extracted_materials[]`:
  ```json
  {
    "source_file": "{relative path from client folder}",
    "date": "{YYYY-MM-DD}",
    "type": "email|pdf|document",
    "from": "{sender or author}",
    "extracted": ["brief description of each data point extracted"]
  }
  ```
- Do NOT add to `sessions[]` — materials are not sessions

Print per-resource result as each completes:
```
  EXTRACTED — {folder or filename}
    Process steps: {count}  |  Waste items: {count}  |  Follow-ups: {count}
```

---

### Stage 3 — Validate & Save

```bash
python3 scripts/validate_audit_data.py --file clients/{client_slug}/audit/audit-data.json --verbose
```

Fix any CRITICAL or HIGH severity issues. Save to `clients/{client_slug}/audit/audit-data.json`.

---

### Stage 4 — Summary

Display combined summary across all inputs processed this run:

```
SYNC & UPDATE COMPLETE — {company_name}
══════════════════════════════════════════════════════

  Resources synced:          {n new meetings} + {n new materials}
  Resources extracted:       {n}
  Process steps extracted:   {n} (cumulative in audit data)
  New pain points:           {n}
  New optimisations:         {n}
  New waste items:           {n} (${total_annual_waste_aud}/yr)
  Follow-up questions:       {n} (HIGH: {n} / MEDIUM: {n} / LOW: {n})
  Contradictions found:      {n}

══════════════════════════════════════════════════════

COMPLETENESS:
  Acquisition:  {covered%}  Quoting: {covered%}  Onboarding: {covered%}
  Fulfilment:   {covered%}  Retention: {covered%}

TOP FOLLOW-UP QUESTIONS (HIGH):
  • {question} [{stage}]
  ...
```

Ask: **"Save this to memory and confirm? [Y / corrections]"**

On Y: update sidecar memory files (`_bmad/_memory/apg-process-mapper-sidecar/index.md` and `chronology.md`) with new session data, then confirm saved.

On corrections: apply corrections to audit data in memory, re-display summary, ask again before saving.

---

### Stage 5 — CRM Sync

**Best-effort.** If any CRM call fails, log a warning and continue. Never block the pipeline.

#### 5a. Find or Create Project

If `crm.project_id` is already set in audit-data.json, skip to 5b.

1. Check if `crm.contact_id` is set. If not:
   - `search_contacts(query: "{company_name}")` → store `contact_id`
   - If no match: `search_contacts(query: "{contact.domain}")` → store `contact_id`
   - If still no match: `create_contact(name: "{company_name}", email_address: "{contact.emails[0]}", is_customer: true)` → store `contact_id`
2. Check if `crm.lead_id` is set. If not:
   - `search_leads(query: "{company_name}")` → store `lead_id`, preferring match linked to `contact_id`
3. `list_projects()` → filter results where `contact_id` matches `crm.contact_id`
   - If found: store `project_id`. Prefer project with "Audit" in name if multiple.
   - If NOT found: `create_project(name: "{company_name} Audit", contact_id: "{crm.contact_id}", status: "active", budget: 3000)` → store `project_id`
4. If lead exists and stage is not "Won": `update_lead(lead_id, stage: "Won")` — only if current stage is in {"Negotiation", "Proposal", "Discovery Call - Completed"}. Otherwise add a lead comment noting audit has started.

#### 5b. Create Task Lists (First Run Only)

`list_tasks(project_id: "{crm.project_id}")` — if empty, create the full task board:

**Create 4 task lists and seed tasks:**

List 1 — **Extraction** (`task_list_id` → `crm.task_list_ids.extraction`):
- `create_task(title: "Session Extraction — Complete all sessions", project_id, task_list_id, priority: 3, status: "In Progress")`
- `create_task(title: "Process Map Complete — All stages covered", project_id, task_list_id, priority: 2)`

List 2 — **Analysis** (`task_list_id` → `crm.task_list_ids.analysis`):
- `create_task(title: "Extract Improvements (EI)", project_id, task_list_id, priority: 2)`
- `create_task(title: "Research Improvements (RI)", project_id, task_list_id, priority: 1)`
- `create_task(title: "Build Strategic Approaches (SA)", project_id, task_list_id, priority: 1)`
- `create_task(title: "Build & Rate (BR)", project_id, task_list_id, priority: 1)`
- `create_task(title: "Verify Research (VR)", project_id, task_list_id, priority: 1)`
- `create_task(title: "Build Transformation Blueprint (TB)", project_id, task_list_id, priority: 1)`

List 3 — **Deliverables** (`task_list_id` → `crm.task_list_ids.deliverables`):
- `create_task(title: "Generate Deliverables", project_id, task_list_id, priority: 1)`

List 4 — **Solution Design** (`task_list_id` → `crm.task_list_ids.solution_design`):
- `create_task(title: "Extract Requirements (RE)", project_id, task_list_id, priority: 1)`
- `create_task(title: "Build Architecture (BA)", project_id, task_list_id, priority: 1)`
- `create_task(title: "Build Prototype (BP)", project_id, task_list_id, priority: 1)`

Store all `task_list_id` values in `crm.task_list_ids`.

**Note:** If `create_task` requires a `task_list_id` but the CRM doesn't support creating task lists via MCP, create all tasks as a flat list on the project and use title prefixes (e.g. "[Extraction] Session Extraction") instead. Skip storing `task_list_ids`.

#### 5c. Update Tasks

1. `list_tasks(project_id: "{crm.project_id}")` → find "Session Extraction" task by title match
2. `create_task_comment(task_id, content)` with extraction summary:
   ```
   SU run {date}: {n} resources extracted.
   Sessions: {sessions_completed} | Steps: {n} | Pain points: {n} | Waste: {n} (${annual}/yr)
   Completeness: Acquisition {%} | Quoting {%} | Onboarding {%} | Fulfilment {%} | Retention {%}
   ```
3. If `audit_status` = `process_map_complete`:
   - Find "Session Extraction" task → `update_task_status(task_id, status: "Done")`
   - Find "Process Map Complete" task → `update_task_status(task_id, status: "Done")`
   - Find "Extract Improvements (EI)" task → `update_task_status(task_id, status: "In Progress")`

#### 5d. Update Project Description

`update_project(project_id, description)`:
```
Audit Status: {audit_status}
Sessions: {sessions_completed} | Steps: {process_step_count} | Waste: ${total_annual_waste}/yr
Last SU: {ISO 8601 timestamp}
```

#### 5e. Save CRM IDs

Update `crm.last_synced` to current ISO 8601 timestamp. Save audit-data.json with all CRM IDs populated.

Print:
```
CRM SYNC — {company_name}
─────────────────────────────────────────────────────
  Project: {project_id} ({found|created})
  Tasks: {n} on board | {n} comments added
  Lead stage: {current_stage}
─────────────────────────────────────────────────────
```

---

## Extraction Passes

Run these five passes for each resource. Each pass has a single lens — do not blend across passes. Treat each as a fresh read.

---

### Pass 1 — Process Flow & Pain Points

Extract:
- Which distinct business areas or process groups are discussed. Use the standard lifecycle (Acquisition → Quoting → Onboarding → Fulfilment → Retention) as a starting framework, but let the transcript reveal the actual business structure. A real estate agency might have "Sales & Listing", "Property Management", "Marketing". An NDIS provider might split onboarding into "Participant Onboarding" and "Support Worker Onboarding". For each stage, derive: a `stage` key (snake_case, e.g. `sales_listing`), a `name` (display label, e.g. "Sales & Listing"), and a `description` (one-line subtitle). Store `name` and `description` on the `processes[]` entry alongside `stage`.
- Process steps (how they currently do things, step by step)
- Explicit pain points (things said to be broken, slow, manual, frustrating)
- Time estimates (hours/week, hours/day, frequency)
- Headcount per role or function
- Staff roles named and described

For each item, capture:
- `speaker` — who said it (use name if identifiable)
- `quote` — verbatim words, not paraphrased
- `confidence` — HIGH (explicitly stated with specifics) | MEDIUM (implied/inferred) | LOW (assumed, needs confirmation)
- `timestamp` — if visible (convert `[MM:SS]` → seconds for `source_timestamp_seconds`)

**Decomposition rules (critical):**
1. **Parallel inputs** — Multiple parallel sources, channels, or tools → model as `type: "parallel_group"` with `items[]`. Never bundle "via X, Y, Z, or W" into one step.
2. **Sequential actions** — Multiple discrete actions by one person → create a separate step for each.
3. **Tool alternatives** — Choice between tools → `decision` node with branch steps.
4. **Branch-only steps** — Steps that only happen on one outcome of a decision → set `"branch_only": true`. Signal phrases: "if they don't", "if no response", "if not suitable", "otherwise", "in that case".

---

### Pass 2 — Tools & Tech Stack

Extract tools the client **ACTIVELY USES** in their current workflow. For each:
- `tool_name`, `current_plan`, `seats`, `monthly_cost_aud`, `use_case`, `workarounds`, `quote`, `confidence`
- `source_timestamp_seconds` — timestamp of first/most substantive mention
- `meeting_references` — one entry per meeting: `{ "meeting_id": "{fathom_meeting_id}", "timestamp_seconds": {n}, "label": "{tool_name} (Session {n})" }`

**Inclusion criteria (must meet at least one):**
- Tool is currently subscribed/licensed and team performs work in it
- Tool is actively used in a process step (e.g. "we do X in Y")
- Tool is paid for and operational, even if underutilized

**Exclude:**
- Provisioned but not yet in use ("account created, nothing running")
- Under evaluation or in trial ("we're considering...")
- Mentioned as hypothetical ("we could use..." / "have you thought about...")
- Named only by auditor as a suggestion
- Client's own platforms that the business doesn't operate in
- Tools with inactive/dormant accounts

If a tool is borderline: note it in `data_gaps[]` as "Tool mentioned but active use unclear: {tool_name}" rather than adding to `tools[]`.

**Tool-to-step linking:** Map each process step to its tool(s) via `tool_ids`:
- Explicit mention → `tool_ids: ["HubSpot"]`, keep step confidence
- Inferred from context → `tool_ids: ["Xero"]`, note as MEDIUM confidence
- No tool involved → `tool_ids: []`

---

### Pass 3 — Time, Waste & Labour Rates

Extract all quantifiable waste signals and staff cost data:
- Hours/week on manual tasks, frequency, volume figures, dollar amounts
- Staff costs: salaries, rates, wages (e.g. "$55k", "$28/hr", "$35 an hour")

**For each waste item, capture traceability fields:**
- `source_session` — session number where this waste was identified (required)
- `source_timestamp_seconds` — convert the nearest `[MM:SS]` marker from the transcript to seconds (required for meeting sessions; `null` for document sessions)
- `quote` — verbatim words from the transcript, not paraphrased
- `meeting_references` — array with one entry per session where this waste was discussed: `{ "session": N, "timestamp_seconds": N, "fathom_url": "" }`. The `fathom_url` is populated later from `sessions[].fathom_url`.

**Determine blended hourly rate:**
- Salary → divide by 2,080 (e.g. $55k ÷ 2,080 = $26.44/hr)
- Multiple roles → average weighted by headcount
- Nothing stated → use $50/hr fallback, `confidence: LOW`
- Store as `blended_hourly_rate_aud` and `blended_rate_confidence`

For each HIGH or MEDIUM confidence waste item with calculable hours, run:

```bash
python3 .claude/skills/bmad-apg-agent-close/scripts/waste-calculator.py \
  --hours-per-week {hours} \
  --headcount {headcount} \
  --hourly-rate {blended_hourly_rate_aud} \
  --activity "{activity_description}"
```

Store `annual_waste_aud` result back into the waste item.

---

### Pass 4 — Decision Points & Contradiction Signals

Extract:
- Conditional logic: "if X, we do Y" → structured as `decision_nodes` entry
- Decision bottlenecks (who approves what, what causes delays)
- Contradictions vs. prior sessions or other speakers in this session
- Data gaps (things that should have been mentioned but weren't)

**Decision node wiring (wire all three atomically):**

1. Add to `decision_nodes[]`:
   ```json
   {
     "node_id": "D00X",
     "condition": "...",
     "yes_path": "...",
     "no_path": "...",
     "yes_branch_step_ids": ["STEP-X"],
     "no_branch_step_ids": ["STEP-Y"],
     "after_step_id": "STEP-ID-BEFORE-GATE",
     "owner": "...",
     "stage": "...",
     "source_session": N,
     "source_quote": "verbatim",
     "source_timestamp_seconds": null,
     "meeting_references": [
       { "meeting_id": "{fathom_meeting_id}", "timestamp_seconds": null, "label": "" }
     ],
     "confidence": "HIGH|MEDIUM|LOW"
   }
   ```
2. Set `"branch_only": true` on every step listed in branch step IDs.
3. Keep main flow clean — the convergence step goes in `processes[].steps[]` normally.

---

### Pass 5 — Data Flow Audit

For each pair of adjacent process steps, populate `data_flow` on the downstream step:

- Explicit handoff described → `mechanism` + `description`, `confidence: HIGH`
- Inferable from context → best-guess mechanism, `confidence: MEDIUM`
- Unknown → `mechanism: "unknown"`, `confidence: LOW`, add to `data_gaps[]`, add HIGH priority follow-up question
- First step in each stage → `data_flow: null`

Mechanisms: `manual_entry|automated_sync|email_notification|api_integration|manual_check|csv_export|verbal|unknown`

---

### Post-extraction — Pain Points Summary

After all five passes:
1. Assign `pain_point_id` to each pain point (`"PP-001"`, etc.)
2. Count totals → `pain_points_summary.total_count`
3. Group by stage → `by_stage`
4. Group by recurring theme → `top_themes[]` ordered by count descending:
   - Manual data entry between systems
   - Communication gaps / missing notifications
   - No follow-up process
   - Duplicate work across tools
   - Missing automation

---

### Post-extraction — Optimisations

For each client-stated improvement wish, desired automation, or future-state aspiration extracted (anything captured as a `type: "optimisation"` step in the process flow), also create a matching entry in `optimisations[]`:
- `optimisation_id` — sequential (OPT-001, OPT-002, …)
- `description` — the improvement described
- `stage` — same stage as the originating process step
- `quote` — verbatim words from the transcript
- `speaker` — who stated it
- `source_session`, `source_timestamp_seconds` — from the process step
- `confidence` — same as the process step

The process step (`type: "optimisation"`) stays in `processes[]` for the process map / priority matrix. The `optimisations[]` entry makes it visible on findings.html.
