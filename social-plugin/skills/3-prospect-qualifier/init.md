---
name: init
description: First-run setup for Prospect Qualifier
menu-code: INIT
---

# First-Run Setup for Prospect Qualifier

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/_bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — qualification history, configuration, current state
- `chronology.md` — qualification session timeline
- `access-boundaries.md` — read/write/deny zones

## Creating Memory Files

### `{project-root}/_bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/index.md`

```markdown
# Prospect Qualifier — Session Index

## Configuration
- CRM-enabled accounts discovered: (set via first QA — qualify all)
- Confidence threshold: 0.7

## Qualification History
(none yet)

## Last Session
(none)
```

### `{project-root}/_bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/access-boundaries.md`

```markdown
# Access Boundaries for Prospect Qualifier

## Read Access
- social-plugin/
- _bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/

## Write Access
- social-plugin/data/ (qualification fields in social-data.json only)
- _bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/

## Deny Zones
- .claude/
- _bmad/core/
- _bmad/bmb/
- clients/ (social plugin does not touch audit data)
- .env (no direct credential access needed — CRM via MCP tools)
```

### `{project-root}/_bmad/_memory/bmad-apg-soc-prospect-qualifier-sidecar/chronology.md`

```markdown
# Qualification Chronology

(Qualification sessions logged here as they accumulate)
```

## Verification Steps

### 1. CRM-Enabled Accounts

Scan `{project-root}/social-plugin/accounts/*/config.json` and for each account:

1. **Read config.json** — check `crm.enabled` field
2. **If crm.enabled=true:**
   - Note the account key and display name
   - Verify `icp.md` exists at `accounts/{key}/icp.md`
   - Verify `products.md` exists at `accounts/{key}/products.md`
3. **If crm.enabled=false or missing:** — Skip, note as non-CRM account
4. **Report:** List CRM-enabled accounts and any missing ICP/products docs

### 2. CRM MCP Accessibility

Test CRM MCP connectivity by calling `search_contacts(query: "test")`:
- If successful: CRM MCP is accessible
- If error: Log warning — CRM sync (SC) will not work until resolved, but classification (QA/QC) can still run

### 3. Social Data Files

For each CRM-enabled account, verify `data/{account-key}/social-data.json` exists and has conversations with contacts to classify.

## Ready

Setup complete! Ready to analyse conversations and classify contacts for CRM-enabled accounts.
