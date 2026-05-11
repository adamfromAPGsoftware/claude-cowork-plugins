---
description: Show competitor ad winner leaderboard — ads running 30+ days are probable winners
---

Identify competitor ads that have been running long enough to be profitable:

1. Read `{plugin_root}/data/campaigns/{active_campaign_id}/competitor-data.json`
2. Calculate `days_active` for each ad (last_seen - first_seen)
3. Categorise: New (<7d), Testing (7-29d), Winner (30-59d), Super Winner (60+d), Stopped
4. Present winner leaderboard table sorted by days_active descending

$ARGUMENTS
