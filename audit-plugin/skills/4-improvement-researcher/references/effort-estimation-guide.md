# Effort Estimation Guide

Reference benchmarks for estimating implementation weeks. Used by BR (Build & Rate) capability.

## Rates

Load rates from central pricing: `{project-root}/_bmad/apg-pricing.md`

- **Agency charge-out (client-facing):** ${YOUR_CHARGEOUT_RATE}/hr — used for all client pricing, package tiers, sprint pricing
- **Internal cost rates (not shown to client):** Dev ${YOUR_DEV_COST}/hr, PM ${YOUR_PM_COST}/hr — used for margin analysis only

## Effort Benchmarks by Change Type

### Automate (step remains, executed by software)

| Complexity | Dev Hours | PM Hours | Total Weeks | Example |
|-----------|-----------|----------|-------------|---------|
| Simple API call | 4-8 | 2 | <1 week | Auto-send email on CRM stage change |
| Workflow automation (Make/Zapier) | 8-16 | 4 | 1-2 weeks | Multi-step Zap: form → CRM → email → task |
| Custom API integration | 16-40 | 8 | 2-4 weeks | Bidirectional sync between CRM and rostering |
| Complex multi-system | 40-80 | 16 | 4+ weeks | Full onboarding pipeline automation |

### Replace (swap tool/method)

| Complexity | Dev Hours | PM Hours | Total Weeks | Example |
|-----------|-----------|----------|-------------|---------|
| Direct swap (same data model) | 4-8 | 4 | <1 week | Switch from spreadsheet to proper CRM |
| Migration + reconfiguration | 16-24 | 8 | 2-4 weeks | Move from Trello to Monday with automations |
| Platform migration | 40-80 | 16 | 4+ weeks | Full CRM replacement with data migration |

### Eliminate (remove step entirely)

| Complexity | Dev Hours | PM Hours | Total Weeks | Example |
|-----------|-----------|----------|-------------|---------|
| Simple removal | 2-4 | 2 | <1 week | Remove manual step that upstream automation handles |
| Removal + redirect | 4-8 | 4 | <1 week | Eliminate manual handoff by connecting tools directly |

### Consolidate (merge multiple steps)

| Complexity | Dev Hours | PM Hours | Total Weeks | Example |
|-----------|-----------|----------|-------------|---------|
| 2-3 steps merged | 8-16 | 4 | 1-2 weeks | Merge data entry across 3 tools into one |
| Multi-stage merge | 16-40 | 8 | 2-4 weeks | Consolidate onboarding flow across CRM + forms + docs |

### AI Enablement (productivity enhancement)

| Complexity | Dev Hours | PM Hours | Total Weeks | Example |
|-----------|-----------|----------|-------------|---------|
| Off-the-shelf AI tool setup | 4-8 | 4 | <1 week | Configure Fathom/Fireflies for call transcription |
| AI + integration | 16-24 | 8 | 2-4 weeks | AI call analysis → auto-populate CRM fields |
| Custom AI workflow | 40-80 | 16 | 4+ weeks | AI-powered lead scoring with custom model |

## Adjustment Factors

Add to base estimate when:
- **Multiple tools involved:** +25% per additional tool beyond the first
- **Data migration required:** +8-16 dev hours
- **Staff training needed:** +4-8 PM hours per tool
- **Custom integrations (no existing connector):** +50% dev hours
- **Compliance/security review needed:** +4-8 PM hours
- **Research confidence is LOW:** +25% buffer

## Converting to Weeks

```
total_hours = dev_hours + pm_hours
weeks_estimate = round(total_hours / 40, 1)  # round to nearest 0.5
```

| Total Hours | weeks_estimate | weeks_label |
|-------------|----------------|-------------|
| 1-39 | 0.5-1.0 | <1 week |
| 40-79 | 1.0-2.0 | 1-2 weeks |
| 80-159 | 2.0-4.0 | 2-4 weeks |
| 160+ | 4.0+ | 4+ weeks |
