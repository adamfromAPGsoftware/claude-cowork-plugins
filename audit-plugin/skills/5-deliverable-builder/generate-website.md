---
name: generate-website
description: Generate client-website.html — single-file client-facing site with progressive session unlock
menu-code: GW
---

# Generate Client Website

## Purpose

Produce `client-website.html` — the polished, client-facing single-file HTML site. Light professional theme: white cards, `#f7f9fc` page background, lime `#7DFF00` as structural accent, `#166534` for green text. Sections unlock progressively as sessions are completed and approved by the consultant. The client experiences value being added session by session — not a big reveal at the end.

## Section Structure

The website always renders these sections:

**Always visible (after discovery):**
- Hero — company name, audit scope statement, consultant name
- "What We're Mapping" — the 5-stage audit methodology overview

**Unlocked after Session 1:**
- First Findings — top 2-3 findings from Session 1 with verbatim quotes

**Unlocked after Session 2:**
- Process Insights — key process flows discovered, top pain points

**Unlocked after Session 3:**
- Quick Wins — Three-Number Rule cards for QUICK_WIN roi_items
- Full ROI Summary — total waste found, total annual saving available

**Unlocked when audit_status == "process_map_complete":**
- Priority Matrix — full quick-win / core-build / future grid
- Roadmap — 3-horizon visual
- Next Steps — implementation CTA

**Always at footer:**
- guarantee statement
- Contact / book a call

## Process

### Step 1: Pre-flight

Load the audit data and determine which sections to unlock based on `audit_status` and `sessions_completed`.

Note: the consultant controls unlock timing — ask if the current session count matches what should be unlocked, or if they want to unlock additional sections manually.

### Step 2: Generate

```bash
python3 .claude/skills/bmad-apg-agent-generator/scripts/generate.py \
  --client-slug {client_slug} \
  --output client-website
```

Output: `clients/{client_slug}/deliverables/client-website.html`

### Step 3: Report

```
CLIENT WEBSITE GENERATED — {company_name}
File: clients/{client_slug}/deliverables/client-website.html

Sections unlocked ({audit_status}):
  ✓ Hero + Methodology overview (always visible)
  ✓ First Findings (Session 1 complete)
  ✗ Process Insights — LOCKED (needs Session 2)
  ✗ Quick Wins — LOCKED (needs Session 3)
  ✗ Priority Matrix — LOCKED (needs process_map_complete status)

Design:
  ✓ branding (lime #7DFF00 as accent, #166534 for green text)
  ✓ Mobile responsive
  ✓ Self-contained (no CDN dependencies)
```
