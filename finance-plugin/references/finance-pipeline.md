# Finance Pipeline

## Overview

The finance pipeline provides read-only visibility into {YOUR_COMPANY}'s Airwallex account. It pulls transaction data, categorizes spend, detects anomalies, and (in future phases) reconciles against CRM records.

**Safety principle:** All Airwallex access is read-only. No script or agent writes to Airwallex.

## Pipeline Phases

```
PULL (on demand or scheduled)
  Transaction Analyst [PT] → fetch transactions → merge into finance-data.json
  Transaction Analyst [PB] → fetch account balances → balances.json
  Transaction Analyst [CT] → auto-categorize uncategorized transactions

ANALYZE (on demand)
  Spend Investigator [SS] → categorized spend summary
  Spend Investigator [LD] → leak detection (duplicates, forgotten subs, anomalies)
  Spend Investigator [TA] → month-over-month trends
  Spend Investigator [QR] → freeform financial Q&A

RECONCILE (future — phase 2)
  Reconciler [AR] → auto-match transactions to CRM invoices/bills
  Reconciler [MM] → manual match for ambiguous items
  Reconciler [SC] → store reconciled data to CRM documents

RECEIPTS (future — phase 2)
  Receipt Manager [PR] → process receipt photo via Claude Code vision
  Receipt Manager [AT] → attach receipt to transaction

REPORT (phase 3)
  Tax Reporter [GI]  → income-statement.json
  Tax Reporter [GBS] → balance-sheet.json
  Tax Reporter [GCF] → cashflow-statement.json
  Tax Reporter [GF]  → {period}-financial-pack.xlsx + {period}-financial-statements.html
  Financial Reporter [GS] → spend-report.html (future)
  Financial Reporter [GR] → reconciliation-report.html (future)
  Financial Reporter [GC] → cashflow.html (future)
  Financial Reporter [GL] → leak-report.html (future)
  Financial Reporter [GT] → tax-summary.html (future)
```

## Agent Capability Matrix

| Agent | Code | Capability | Input | Output |
|-------|------|-----------|-------|--------|
| Transaction Analyst | PT | Pull Transactions | Airwallex API | finance-data.json |
| Transaction Analyst | PB | Pull Balances | Airwallex API | balances.json |
| Transaction Analyst | CT | Categorize | finance-data.json | finance-data.json (updated) |
| Spend Investigator | SS | Spend Summary | finance-data.json | Structured summary |
| Spend Investigator | LD | Leak Detector | finance-data.json | Flagged items |
| Spend Investigator | TA | Trend Analysis | finance-data.json | Trend report |
| Spend Investigator | QR | Query | finance-data.json | Answer |
| Tax Reporter | GB | Generate BAS | finance-data.json | bas-data.json |
| Tax Reporter | GT | Generate Tax Summary | finance-data.json | tax-summary.json |
| Tax Reporter | GG | Generate Grant Report | finance-data.json | grant-report.json |
| Tax Reporter | GI | Generate Income Statement | finance-data.json | income-statement.json |
| Tax Reporter | GBS | Generate Balance Sheet | finance-data.json + CRM MCP | balance-sheet.json |
| Tax Reporter | GCF | Generate Cash Flow | finance-data.json | cashflow-statement.json |
| Tax Reporter | QT | Query Tax | finance-data.json | Answer |

## Data Files

| File | Purpose |
|------|---------|
| `finance/finance-data.json` | Source of truth — all transactions, categories, flags |
| `finance/balances.json` | Latest account balance snapshot |
| `finance/tax/` | Generated tax and financial statement JSON files |
| `finance/reports/*.html` | Generated HTML reports (future) |
| `crm-finance-entities.md` | CRM entity roles and MCP tool reference |
| `financial-statements-au.md` | Australian financial statement formats and field mappings |

## Typical Workflow

1. Run `/apg-finance:pull-transactions` to fetch latest from Airwallex
2. Run `/apg-finance:spend-summary` to see where money is going
3. Run `/apg-finance:leak-check` to find anomalies
4. Run `/apg-finance:status` to check overall health
