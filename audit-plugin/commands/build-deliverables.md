---
description: Generate HTML deliverables from audit data for a client
---

Generate HTML deliverables for the specified client using the agent-generator workflow:

1. Read `clients/{client}/audit/audit-data.json` to check current status
2. Determine which deliverables can be generated based on `audit_status` and data completeness
3. Run `scripts/generate.py` to produce the appropriate HTML files
4. Report which deliverables were generated and saved to `clients/{client}/deliverables/`

Client: $ARGUMENTS
