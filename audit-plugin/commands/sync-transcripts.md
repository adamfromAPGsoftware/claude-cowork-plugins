---
description: Sync latest Fathom transcripts for the current client and update audit-data.json
---

Run the process mapper's sync-and-update workflow for the specified client:

1. Fetch new Fathom meetings using `scripts/fetch-transcripts.py`
2. Extract process data from any new transcripts into `audit-data.json`
3. Report what was found and any new follow-up questions

Client: $ARGUMENTS
