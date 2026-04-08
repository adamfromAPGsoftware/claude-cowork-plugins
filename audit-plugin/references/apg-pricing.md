# Pricing

> Central pricing reference loaded by all agents. Single source of truth for all cost calculations.
> Update this file when pricing changes — all agents and skills inherit automatically.

## Package Tiers (One-Off Engagements)

For automations, tool configurations, and small contract work.

| Tier | Client Price | Dev Hours | PM Hours | Total Hours | Use Case |
|------|-------------|-----------|----------|-------------|----------|
| Micro | ${YOUR_MICRO_PRICE} | ~10 | ~3 | ~13 | Simple automation, tool config, single integration flow |
| Standard | ${YOUR_STANDARD_PRICE} | ~20 | ~8 | ~28 | Single integration, moderate custom work |
| Complex | ${YOUR_COMPLEX_PRICE} | ~40 | ~12 | ~52 | Multi-tool integration, custom module, data migration |

## Sprint-Based Pricing (Custom Builds & Large Features)

For platform builds, major feature development, and multi-sprint engagements.

| Sprint Type | Client Price | Dev Hours | PM Hours/Week | Duration | Use Case |
|-------------|-------------|-----------|---------------|----------|----------|
| Growth | ${YOUR_SPRINT_PRICE} | 80 (full-time) | 10 hrs/week | 2 weeks | Main sprint type — feature builds, custom modules, platform delivery |

- Typical engagement: 3-10 Growth sprints
- {YOUR_GUARANTEE_TERMS}

## Ongoing Services

| Service | Monthly | Includes |
|---------|---------|----------|
| Hosting (small) | ${YOUR_HOSTING_SMALL} | Basic infrastructure |
| Hosting (standard) | ${YOUR_HOSTING_STD} | Pro tier + email service |
| Hosting (scale) | ${YOUR_HOSTING_SCALE} | Above + AI features + messaging |
| Maintenance retainer (basic) | ${YOUR_MAINT_BASIC} | Bug fixes, minor updates, monitoring |
| Maintenance retainer (standard) | ${YOUR_MAINT_STD} | Above + feature tweaks, priority support |
| Maintenance retainer (premium) | ${YOUR_MAINT_PREMIUM} | Above + dedicated hours, SLA |

## Internal Rates (Not Shown to Client)

| Role | Internal Rate |
|------|--------------|
| Developer | ${YOUR_DEV_RATE}/hr |
| Project Manager | ${YOUR_PM_RATE}/hr |

## Tier Assignment Heuristic

Used by analyst agents to assign `suggested_tier` on `roi_items[]`:

| Internal Cost Estimate | Suggested Tier |
|----------------------|----------------|
| $0-{YOUR_MICRO_CEILING} | micro |
| {YOUR_MICRO_CEILING}-{YOUR_STD_CEILING} | standard |
| {YOUR_STD_CEILING}-{YOUR_COMPLEX_CEILING} | complex |
| {YOUR_COMPLEX_CEILING}+ | sprint |

Target margin: {YOUR_TARGET_MARGIN}% minimum.

## Tax Incentives (Optional)

If your jurisdiction offers R&D tax incentives or similar programs, document them here.
This can significantly reduce the effective cost for clients on custom development work.
