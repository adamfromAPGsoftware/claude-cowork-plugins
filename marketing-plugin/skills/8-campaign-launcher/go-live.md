---
name: go-live
description: Run pre-flight checklist and activate a PAUSED campaign — starts spending budget
menu-code: GO
---

# Go Live — Activate Campaign

Run a comprehensive pre-flight checklist, then activate a PAUSED Meta campaign. This is the final gate — activation starts spending budget immediately.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Going live with: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, list campaigns from `campaign-data.json` that have `meta_campaign.status` = `"created"` (PAUSED). Ask user to select one.

2. **Run pre-flight checklist:**

   ```
   ═══ Pre-Flight Checklist ═══

   [ ] Landing page deployed and accessible
       URL: {landing_page_url}
       Status: {HTTP status code from curl check}

   [ ] GA4 tracking verified
       Measurement ID: {measurement_id or "NOT SET"}

   [ ] Meta Pixel verified
       Pixel ID: {pixel_id or "NOT SET"}

   [ ] Lead capture webhook active
       Worker URL: {webhook_url or "NOT DEPLOYED"}
       Test result: {last test pass/fail or "NOT TESTED"}

   [ ] Creatives uploaded to Meta
       Creative count: {count}
       All have meta_creative_id: {yes/no}

   [ ] Campaign created in Meta (PAUSED)
       Campaign ID: {campaign_id}
       Ad Sets: {count}
       Ads: {count}

   [ ] All approval gates passed
       Campaign creation: {approved/pending}
   ```

3. **Evaluate checklist:**
   - If ANY critical check fails (landing page down, no creatives, no campaign ID):
     ```
     PRE-FLIGHT FAILED

     Blocking issues:
     - {issue}: {recommendation}

     Fix these before running [GO] again.
     ```
   - If non-critical checks fail (GA4 not set, webhook not deployed):
     ```
     PRE-FLIGHT WARNING

     Non-blocking issues:
     - {issue}: {recommendation}

     You can proceed without these, but tracking will be incomplete.
     Continue anyway? [yes / no]
     ```

4. **If all pass (or warnings accepted), present FINAL APPROVAL:**

   ```
   ═══ APPROVAL GATE: Go Live ═══

   Campaign: {campaign_name}
   Landing Page: {full_url}
   Daily Budget: ${daily_budget}
   7-Day Estimate: ${daily_budget * 7}
   30-Day Estimate: ${daily_budget * 30}
   Ads: {count} (currently PAUSED)

   Activating will start spending budget immediately.

   Approve activation? [yes / no]
   ```

5. **On approval** — Run the activation script to update campaign status from PAUSED to ACTIVE:
   ```
   python3 marketing-plugin/scripts/create-meta-campaign.py --campaign-id {id} --activate
   ```

   This updates:
   - Campaign status: PAUSED -> ACTIVE
   - Ad Set status: PAUSED -> ACTIVE
   - Ad statuses: PAUSED -> ACTIVE

6. **Update campaign-data.json:**
   - Set `meta_campaign.status` = `"active"`
   - Set campaign `status` = `"live"`
   - Set `meta_campaign.activated_at` = current timestamp
   - Add entry to `approval_log` with timestamp, operation "go_live", and approved_by

7. **Log to api-log.md** — Record all activation API calls.

8. **Present result:**
   ```
   ═══ CAMPAIGN LIVE ═══

   Campaign: {campaign_name}
   Campaign ID: {campaign_id}
   Status: ACTIVE
   Daily Budget: ${daily_budget}
   Ads Active: {count}
   Activated: {timestamp}

   First data pull recommended after 24-48 hours.
   Run Campaign Collector [PM] then Performance Review [PR] after 7 days
   for initial performance analysis.
   ```
