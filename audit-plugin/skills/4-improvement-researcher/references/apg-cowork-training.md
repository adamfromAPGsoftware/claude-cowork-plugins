# Claude Cowork Training — RI Reference

> Loaded by RI (Step 2f) when evaluating whether a proposed change can be delivered via Claude Cowork + MCP training instead of traditional automation or SaaS configuration.

## What This Is

Claude Cowork is an AI-powered workspace where users interact with Claude to operate their business tools via MCP (Model Context Protocol) connections. Instead of building automation workflows (n8n, Make.com, Zapier) or buying new SaaS, we train the client's team to use Cowork connected to their existing tools.

**The key insight:** Many "automation" opportunities are better delivered as training — the client learns to use Claude Cowork as their operations assistant, connected to their actual tools via MCP. This gives them control, flexibility, and understanding rather than a black-box automation they can't modify.

## How It Works

1. **MCP connections** — Claude Cowork connects to business tools via MCP servers (Google Calendar, Gmail, Sheets, CRMs, accounting platforms, etc.)
2. **Natural language operation** — Users talk to Claude in plain language: "Build next week's schedule considering staff availability and participant preferences"
3. **Tool execution** — Claude reads from and writes to connected tools: creates calendar events, sends emails, updates spreadsheets, queries databases
4. **Voice input** — Cowork supports voice, making it accessible for non-technical users who find typing instructions slower

## Delivery Model

Training is delivered as a structured programme, not a one-off session:

| Component | Hours | Description |
|-----------|-------|-------------|
| Preparation | 2-4 hrs | Configure MCP connections, build custom instructions for the client's specific workflows, test with their data |
| Training delivery | 4-8 hrs | Hands-on sessions with the team — each use case practised live |
| Follow-up support | 2-4 hrs | Async support over 2 weeks post-training to troubleshoot and refine |

**Total per training module:** 8-16 hours (typically 1-2 weeks elapsed, <1 week effort)

Multiple use cases can be bundled into a single training programme. A bundle of 3-5 use cases typically takes 2-3 days of preparation + 1-2 days of delivery.

## Cost Model

Training is priced using {YOUR_COMPANY}'s standard package tiers (see `apg-pricing.md`):

| Scope | Tier | Price (AUD) | Covers |
|-------|------|-------------|--------|
| Single use case | Micro | $1,800 | 1 MCP connection + training for 1 workflow |
| 2-3 use cases | Standard | $3,800 | Multiple MCP connections + bundled training |
| Full Cowork programme | Complex | $6,500 | 4-6 use cases + team rollout + custom instructions |

**Ongoing cost to client:** $20-30/mo for Claude Team subscription (per user who needs access). No automation hosting, no per-workflow fees, no Make/Zapier subscriptions.

## What Cowork Replaces

Cowork training **replaces** these traditional delivery approaches for suitable changes:

| Traditional Approach | Cowork Replaces When... |
|---------------------|------------------------|
| n8n / Make.com / Zapier workflow | The automation is user-triggered (not fully autonomous) and benefits from human judgment |
| Custom script / Edge Function | The task involves reading + deciding + acting across multiple tools |
| New SaaS tool training | The client's existing tool + Cowork achieves the same outcome without a new subscription |
| Manual process documentation | Claude can be the "documentation" — users describe what they need, Claude knows the process |

**Cowork does NOT replace:**
- Fully autonomous background automations (scheduled jobs, webhooks, event-driven flows that must run without human involvement)
- Compliance-critical automated processes (payroll calculations, NDIS claiming)
- High-volume data processing (bulk imports, batch API calls)
- Systems that must run 24/7 without human interaction

## MCP Availability Guide

Common business tools with MCP support (or API that can be wrapped):

| Tool | MCP Available | Notes |
|------|--------------|-------|
| Google Calendar | Yes | Read/write events, check availability, schedule |
| Gmail | Yes | Read/send emails, search threads, manage labels |
| Google Sheets | Yes | Read/write cells, create/modify spreadsheets |
| Google Drive | Yes | List/read/upload files |
| HubSpot | Yes | Contacts, deals, pipeline management |
| Xero | Via API wrapper | Invoices, contacts, financial queries |
| Slack | Yes | Messages, channels, search |
| Notion | Yes | Pages, databases, search |
| Trello | Via API wrapper | Cards, boards, lists |
| Calendar (generic) | Yes | Most calendar tools have MCP or API support |

**If a tool has an API but no MCP server:** We can build a lightweight MCP wrapper as part of the preparation phase. This is included in the training package cost.

## Assessment Criteria

For each proposed change, evaluate Cowork viability using these criteria:

| Criterion | Cowork Viable | Not Cowork Viable |
|-----------|--------------|-------------------|
| **Trigger** | Human-initiated ("I need to...") | Event-driven (webhook, schedule, trigger) |
| **Judgment** | Requires context, decisions, exceptions | Pure data transformation, no decisions |
| **Frequency** | Daily/weekly tasks done by a person | Runs hundreds of times per day automatically |
| **Tools** | Existing tools with MCP/API | Requires new purpose-built software |
| **User** | Non-technical but willing to learn | No one will interact with it — must be autonomous |
| **Flexibility** | Process varies, needs human input | Process is rigid and rule-based |

**Best candidates:** Tasks that a skilled assistant would do — reading information, making decisions, taking actions across multiple tools, drafting communications, scheduling, searching.

**General productivity gains:** Beyond specific use cases, Cowork training delivers hard-to-quantify but real value: faster email responses, quicker information lookup across tools, ad-hoc reporting, and general operational fluency. Estimate conservatively at 2-5 hrs/week saved per trained user on miscellaneous tasks.

## Value Framing

When calculating value for Cowork-delivered changes:

1. **Direct time savings** — Calculate as normal (hours_saved × rate × 52)
2. **General productivity uplift** — Add a conservative estimate for the trained user's general efficiency gains: `trained_users × 2 hrs/wk × hourly_rate × 52 wks` (conservative) to `trained_users × 5 hrs/wk × hourly_rate × 52 wks` (moderate)
3. **Team autonomy** — Frame qualitatively: the team can modify, extend, and adapt their workflows without calling a developer. This is a strategic advantage, not just a cost saving.

## Client Messaging

When writing modal content for Cowork-delivered changes:

- Frame as "your team learns to use AI to do this" not "we build an automation"
- Emphasise control: "You can adjust how this works by telling Claude what you need"
- Emphasise speed: "Your team is up and running in days, not weeks"
- Emphasise flexibility: "As your process changes, just update your instructions to Claude"
- Use concrete examples: "You say 'build next week's schedule' and Claude checks availability, considers preferences, and creates the calendar events"
