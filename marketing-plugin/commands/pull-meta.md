---
description: Pull latest Meta ad campaign data — campaigns, ad sets, ads, and daily insights
---

Fetch the latest campaign data from Meta Marketing API and merge into marketing-data.json:

1. Read `{plugin_root}/data/marketing-data.json` for last sync date
2. Use Desktop Commander's `execute_command` (or Bash) to run:
   `python3 {plugin_root}/scripts/fetch-meta-campaigns.py --from-date {from} --to-date {to}`
3. Report: new campaigns, ad sets, ads, insight rows, and spend summary

$ARGUMENTS
