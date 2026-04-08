# Custom Build Platform — RI Reference

> Loaded by RI (Step 2d) when generating the `custom_build_option` for each proposed change.
> For pricing, load `{project-root}/_bmad/apg-pricing.md` — the single source of truth.

## Role in Pipeline

The custom build is NOT included as a strategic approach in the SA (Build Strategic Approaches) capability. Strategic approaches are SaaS-only — three strategies covering free tools, best-of-breed SaaS, and a smart SaaS mix.

The custom build is handled as a **separate comparison track** by the Solution Designer agent:
1. **RI** still generates `custom_build_option` on each proposed change (module mapping, scope, weeks)
2. **Solution Designer** (RE → BA → BP) uses that data to build requirements, architecture, and a clickable prototype
3. The client sees SaaS strategies alongside the custom build prototype during the **presentation**
4. After the client selects an approach, the **blueprint** (TB) is built for that specific approach

This separation creates a clear "SaaS with all its warts vs custom software with no limitations" comparison.

## Platform Overview

We build custom business applications on a production-ready template platform. Each client deployment is a standalone fork — no multi-tenant complexity, no per-user SaaS fees, client owns their data and deployment.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (App Router), TypeScript 5.3+, Untitled UI (200+ components), Tailwind CSS 4 |
| State | Zustand + React Query |
| API | tRPC (type-safe), Supabase auto-generated REST/GraphQL |
| Database | PostgreSQL 15 via Supabase |
| Auth | Supabase Auth (email/password, magic links, 2FA) |
| Storage | Supabase Storage (S3-compatible, CDN) |
| Real-time | Supabase Realtime (WebSocket subscriptions) |
| Edge Functions | Deno Deploy (serverless business logic) |
| Hosting | Vercel (edge deployment, CI/CD) |
| AI | Pinecone (vector search), OpenAI/Claude API integration |
| Email | Resend (transactional) |
| SMS/Voice | Twilio |
| Accounting | Xero API (bidirectional sync) |

## Architecture Principles

- **API-less**: Supabase auto-generates REST/GraphQL from the database schema. No custom API layer for CRUD.
- **Row Level Security (RLS)**: Access control enforced at the database, not the application. Role-based policies.
- **Real-time by default**: All collaborative features (messaging, tasks, notifications) use Supabase Realtime.
- **Edge Functions**: Complex business logic (payroll calculations, notification routing, AI workflows) runs serverless.
- **PWA with offline**: Installable on all devices, core features work offline, auto-sync on reconnect.
- **Single-tenant**: Each client gets their own Supabase project + Vercel deployment. No shared infrastructure.

## Template Modules

### CRM Core
- **Contacts**: Full contact management with custom fields, tags, activity timeline. Supports multiple entity types (participant, staff, organisation, guardian, support coordinator).
- **Leads**: Pipeline stages with Kanban view, auto-assignment rules, lead scoring, conversion tracking. Gmail/calendar integration.
- **Projects**: Lifecycle management, task association, document linking, budget overview, team assignment.
- **Activity Log**: All actions tracked with metadata (entity type, actor, timestamp, changes). Full audit trail.

### Workspace
- **Messaging**: Real-time channels + DMs. Threaded conversations, @mentions, file attachments, voice notes, typing indicators.
- **Tasks**: Kanban + list views, assignments, due dates, priorities, dependencies, recurring tasks, comments. Multiple configurable views.
- **Files**: Document management with folder structure, versioning, permission-based access (Admin/Management/Company/Public). Drag-drop uploads, previews.
- **Timesheets**: Clock in/out (geo-fenced optional), manual entry, daily/weekly views, submit-for-approval workflow, manager approval, break tracking.

### Financial Operations
- **Invoices**: Create, send, track with line items, tax handling, payment status, PDF generation, payment links.
- **Expenses**: Submission, approval workflow, receipt upload, category tracking.
- **Payroll**: Timesheet aggregation, rate calculation, award interpretation support, payroll run preparation.
- **Accounting Integration**: Bidirectional sync with any accounting platform that supports an API. Pre-built connectors for **Xero** and **QuickBooks Online** (OAuth2). Syncs contacts, invoices, bills, chart of accounts, and financial reporting data. Operations users get read-only financial dashboards without needing direct accounting software access.

### AI Features
- **Semantic Search**: Pinecone vector database. Search across all entities by meaning.
- **AI Chat**: Context-aware assistant that queries CRM data, summarises records, drafts content.
- **Custom Agents**: Configurable AI agents for domain-specific tasks (progress note drafting, lead qualification, report generation).
- **Knowledge Graph**: Entity relationships exposed to AI for contextual reasoning.

### Integrations
- **Accounting (Xero / QuickBooks Online / API-compatible)**: Full bidirectional sync (see Financial Operations). Supports any accounting platform with a REST API.
- **Gmail**: Send/receive emails linked to contacts. Thread tracking. Template support.
- **Twilio SMS/Voice**: Automated SMS notifications, bulk messaging, call logging.
- **Social Media**: Post scheduling across platforms, approval workflows, engagement tracking.
- **Push Notifications**: OneSignal integration for mobile and desktop.

## Deployment Model

1. Fork the template codebase
2. Customise branding (logo, colours, domain), toggle feature modules on/off
3. Configure Supabase project (schema migrations, RLS policies, storage buckets)
4. Customise data model (add custom fields, entity types, business rules)
5. Deploy to Vercel with CI/CD pipeline
6. Data migration from client's existing systems (CSV import, API sync)

**Timeline**: 5 working days for standard configuration. 2-4 weeks for significant customisation.

## Delivery Model — Sprint-Based

Work is delivered in **2-week Growth sprints** ($15,000 each). Each sprint produces a working, deployable increment — not a waterfall build phase. Clients see working features from sprint 1.

- **Sprint 1** typically delivers: platform setup, branding, core CRM/contacts, and 1-2 high-value modules
- **Subsequent sprints** add modules incrementally — each sprint ships to production
- **Typical engagement**: 3-10 sprints ($45,000-$150,000) depending on scope
- **90-day ROI guarantee** covering up to 3 sprints

This means there is no extended build phase before the client sees results. Features ship every 2 weeks.

## Ongoing Costs

The client pays their own infrastructure costs directly to vendors (Vercel, Supabase, etc.). does not mark up infrastructure. See `apg-pricing.md` "Client Infrastructure" section for typical costs ($30-100/mo).

charges a maintenance retainer on top, tiered by client headcount. See `apg-pricing.md` "Maintenance & Support Retainers" section. For most audit clients:
- <10 staff: $200/mo (monitoring only)
- 10-20 staff: $500/mo
- 20-50 staff: $1,000/mo
- 50-100 staff: $2,000/mo

**Total ongoing cost to client:** infrastructure ($30-100/mo) + maintenance retainer ($200-2,000/mo).

This is typically cheaper than the combined SaaS subscription stack it replaces, especially for businesses with 20+ staff where per-user SaaS pricing scales linearly.

## Decision Framework

### Recommend Custom Build When

- Client needs 3+ features that would otherwise require separate SaaS subscriptions
- Data unification is a priority (scheduling + invoicing + CRM sharing data enables AI from day one)
- Per-user SaaS pricing scales unfavourably (e.g., 50 staff × $15/user/mo = $750/mo for one tool)
- Client wants AI features — unified data architecture makes AI immediately useful without migration
- Australian data hosting is required (Supabase Sydney region available)
- Client wants to own their platform and data without vendor lock-in
- Multiple proposed changes share infrastructure (e.g., scheduling + notifications + payroll all on one platform)

### Realistic Considerations (the only real cons)

When generating cons for the Custom Build option, there are only two genuine considerations:

1. **Sensitive data / compliance**: For highly secure information requiring HIPAA, NDIS certification, or similar compliance standards, there are added management costs for that level of security. In most cases, rather than building that functionality, we plug into a purpose-built SaaS tool via API (e.g., Google Drive for secure document storage, Oho for NDIS worker screening). The custom platform orchestrates and connects to these tools — it doesn't replace them.

2. **Ongoing maintenance**: The platform requires light ongoing maintenance (dependency updates, security patches, minor fixes). This is covered by a maintenance retainer. Compare this to the hidden admin cost of managing multiple SaaS vendor relationships, broken integrations, and coordinated updates.

**What is NOT a con:**
- Build complexity — the template platform eliminates most infrastructure work
- Feature limitations — almost everything is buildable on the platform
- Accounting — we integrate with Xero/QuickBooks via API, same as SaaS tools do. We don't replace accounting software, we plug into it.

Do NOT generate cons like "higher cost than X" or "requires engagement for changes" — these are pricing comparisons that belong on the strategic approaches page, not functionality limitations.

### Recommend SaaS When

- A single off-the-shelf tool covers 80%+ of the need with minimal configuration
- Client prefers self-service administration without developer involvement
- Compliance requires a certified/audited platform (e.g., NDIS-certified claiming software)
- Client has internal IT staff who want to manage their own tool stack
- The problem is narrow and a mature, well-supported SaaS solves it with proven reliability

### Consider Hybrid When

- Core operations on custom platform + specialist SaaS for compliance-critical functions
- We plug in specialist tools via API for: accounting (Xero), compliance verification (Oho), secure document storage (Google Drive), and any domain where a certified tool is required
- Example: Custom CRM + scheduling on platform, Xero for accounting, Oho for compliance verification

## Module Mapping Guide (for RI Step 2d)

When evaluating a proposed change, match it to platform module(s):

| Change Pattern | Primary Module(s) | Scope Level |
|---|---|---|
| Lead tracking, pipeline, CRM | CRM Core (Leads + Contacts) | configure_existing |
| Client/participant database | CRM Core (Contacts) with custom fields | configure_existing |
| Internal comms, team messaging | Workspace (Messaging) | configure_existing |
| Task management, project tracking | Workspace (Tasks) | configure_existing |
| Invoice management, billing | Financial Ops (Invoices + Accounting Integration) | configure_existing |
| Accounting dashboard, financial visibility | Financial Ops (Accounting Integration) — read-only dashboards via bidirectional sync | configure_existing |
| Timesheet, hour tracking | Workspace (Timesheets) | configure_existing |
| Automated SMS/email notifications | Integrations (Twilio + Gmail) | configure_existing |
| Document management, file storage | Workspace (Files) | configure_existing |
| Scheduling, rostering, availability | Workspace (Tasks) + custom scheduling views | medium_customisation |
| Digital forms, e-signatures | Custom form builder module | medium_customisation |
| Payroll processing, award calc | Financial Ops (Payroll) + custom rules | medium_customisation |
| AI document generation, reports | AI Features (Custom Agents) | medium_customisation |
| Reporting dashboards, analytics | Custom dashboard module | medium_customisation |
| Compliance tracking, expiry alerts | Custom compliance module | custom_build |
| Funding/budget tracking with alerts | Custom funding module (extends Financial Ops) | custom_build |
| Distance/km calculation | Custom Edge Function + Google Maps API | custom_build |
| Voice-to-text input, dictation | Custom module + Whisper/device API | custom_build |
| Industry-specific claiming/billing | Custom claiming module | heavy_custom |
| Complex rules engine (matching, capacity) | Custom scheduling engine | heavy_custom |

## Scope Estimation Guide (Per Module)

These are weeks to build/configure each **unique platform module** — NOT per proposed change.

| Scope Level | Description | Typical Weeks | Max Weeks |
|---|---|---|---|
| configure_existing | Module exists, needs fields/workflows configured | 0.5 - 1.0 | 1.0 |
| medium_customisation | Module exists, needs additional views, UI tweaks, or business logic | 1.0 - 2.0 | 2.0 |
| custom_build | New module needed, uses platform patterns and infrastructure | 2.0 - 3.0 | 4.0 |
| heavy_custom | Significant new functionality, may require external API integrations | 3.0 - 5.0 | 6.0 |

**CRITICAL — Per Module, Not Per Change:**
Multiple proposed changes often map to the same platform module. The module is built ONCE, not once per change. Example: CH-001 (CRM pipeline) and CH-005 (central database) both use CRM Core — CRM Core is built once at ~1 week, covering both changes.

## Platform Total Estimator

**The correct way to estimate total custom build effort:**

### Step 1: Collect all modules across all proposed changes
For each proposed_change, list its `platform_modules[]` from the Module Mapping Guide.

### Step 2: Deduplicate into unique modules
Group by module name. Each module appears once regardless of how many changes use it. Assign the **highest scope_level** from any change that uses that module.

### Step 3: Estimate per unique module
Use the Scope Estimation Guide above. Stay within the Max Weeks column — never exceed it.

### Step 4: Add platform setup (one-time)
- Platform fork + branding + deployment: 0.5 weeks (first sprint only)
- Data migration from existing systems: 0.5-1.0 weeks per major data source
- Xero/accounting integration: 0.5-1.0 weeks (if needed)

### Step 5: Sum = total platform weeks

**Formula:**
```
total_weeks = platform_setup (0.5)
            + sum(unique_module_weeks)
            + data_migration_weeks
            + integration_weeks
```

### Example (Dale — Great Supports, ~50 staff NDIS provider)

**Phase 1: Core Platform (data & systems first)**

| Unique Module | Scope Level | Weeks | Changes Covered |
|---|---|---|---|
| Platform setup + branding | — | 0.5 | — |
| CRM Core (Contacts + Leads) | configure_existing | 1.0 | CH-001, CH-005 |
| Workspace (Scheduling + Tasks) | medium_customisation | 2.0 | CH-006, CH-007, CH-008, CH-014 |
| Workspace (Files + Onboarding) | configure_existing | 0.5 | CH-003 |
| Workspace (Timesheets) | configure_existing | 0.5 | CH-010 |
| Financial Ops (Invoices + Xero) | medium_customisation | 1.0 | CH-013, CH-015, CH-017 |
| Financial Ops (Funding/Scholarships) | medium_customisation | 1.0 | CH-011, CH-012 |
| Compliance (staff onboarding) | configure_existing | 0.5 | CH-004 |
| Integrations (Maps API + SMS) | configure_existing | 0.5 | CH-008, CH-009 |
| Data migration | — | 0.5 | — |
| **TOTAL Phase 1** | | **8.0 weeks** | Core system |

Phase 1 = 4 Growth sprints × $15,000 = **$60,000** (or ~$33,900 after R&D tax offset)

Ongoing costs (separate line items):
- **maintenance retainer:** $200/mo ($2,400/yr) — monitoring, security alerts, issue notification
- **Client infrastructure (paid directly to vendors):** ~$50/mo ($600/yr) — Vercel + Supabase free/basic tiers
- **Total ongoing:** $250/mo ($3,000/yr)

**Phase 2: AI & Cowork Training (optional, after data is structured)**

| Item | Delivery | Weeks | Changes Covered |
|---|---|---|---|
| Cowork training programme | Training (Complex tier) | 1-2 | CH-002, CH-016 + general productivity |

Phase 2 = $6,500 one-off (Complex training tier)

**Key principle:** Data and systems first, AI second. The platform must aggregate and structure the data before AI/Cowork features can operate on it. Phase 2 is an optional follow-on engagement.

**Compare:** The naive per-change sum was 30.5 weeks. Deduplicated with realistic scope = 8.0 weeks core + optional Cowork training.

### Important Notes
- These are estimates based on template platform experience. As completes more builds, actual timesheet data will replace these estimates.
- The Scope Estimation Guide Max Weeks column is a hard cap. If the AI estimates higher, it must justify why or the estimate is wrong.
- When calculating custom build cost for the client comparison: `total_weeks × $15,000 per 2-week sprint ÷ 2 = total sprints × $15,000`.
