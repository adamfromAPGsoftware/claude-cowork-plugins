---
name: meta-campaign
description: Create a Meta campaign structure (campaign, ad sets, ads) — all PAUSED until [GO]
menu-code: MC
---

# Meta Campaign — Create Campaign Structure

Create the full Meta campaign structure programmatically: campaign, ad sets, and ads. Everything is created in PAUSED state — no budget will be spent until [GO] is run.

> **Pipeline Note:** [MC] sits in the LAUNCH phase, which requires BOTH tracks to be complete:
> - **Track A** (landing page): GA4 [GA] -> generate landing page [GL] -> deploy [DL] -> inject tracking [ST]
> - **Track B** (creatives): build angles [BA] -> generate creatives -> package [PC] -> upload to Meta [UC]
>
> If either track is incomplete, warn the user and suggest completing the outstanding steps before proceeding.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Creating Meta campaign for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, list campaigns from `campaign-data.json` that have status `planned` or `ready`. Ask user to select one.

2. **Load campaign config** — From the selected campaign, extract:
   - Product / offering
   - Target audience (locations, age range, interests)
   - Daily budget
   - Campaign objective (e.g., OUTCOME_LEADS, OUTCOME_TRAFFIC, OUTCOME_AWARENESS)
   - Landing page URL

3. **Verify landing page deployed** — Check if the campaign has a deployed landing page (`landing_page.deployed` = true or landing page URL returns HTTP 200). If not:
   - Warn: "Landing page has not been deployed yet (Track A incomplete)."
   - Suggest: "Complete Track A first: [GA] -> [GL] -> [DL] -> [ST]."

4. **Load creative batches** — From `creative-data.json`, find batches linked to this campaign ID. List the angles and creative assets available.

5. **Verify creatives uploaded** — Check if creative batches have `meta_creative_ids` populated. If not:
   - Warn: "Creatives have not been uploaded to Meta yet (Track B incomplete)."
   - Offer: "Run [UC] first to upload creatives, or I can run it inline now."
   - If user wants inline: execute the UC process, then continue.

6. **Dry run** — Run:
   ```
   python3 marketing-plugin/scripts/create-meta-campaign.py --campaign-id {id} --dry-run
   ```

7. **Present what will be created:**

   ```
   ═══ Campaign Creation Preview ═══

   Campaign:
     Name: {campaign_name}
     Objective: {objective}
     Special Ad Categories: [] (none)
     Status: PAUSED

   Ad Set:
     Name: {adset_name}
     Targeting:
       Locations: {locations}
       Age: {age_min}-{age_max}
       Interests: {interests}
     Daily Budget: ${daily_budget}
     Optimization Goal: {optimization_goal}
     Billing Event: IMPRESSIONS
     Status: PAUSED

   Ads ({count}):
     {For each ad:}
     - {ad_name}: creative_id={creative_id}, CTA={cta}, landing={url}
       Status: PAUSED

   ═══ Budget Breakdown ═══
   Daily:   ${daily_budget}
   7-Day:   ${daily_budget * 7}
   30-Day:  ${daily_budget * 30}

   All entities created in PAUSED state — won't spend until [GO].
   ```

8. **APPROVAL GATE** —
   ```
   ═══ APPROVAL GATE: Create Campaign ═══

   Approve creating this campaign in Meta?
   (All PAUSED — won't spend until [GO])

   [yes / no]
   ```

9. **On approval** — Run:
   ```
   python3 marketing-plugin/scripts/create-meta-campaign.py --campaign-id {id} --execute
   ```

10. **Update campaign-data.json:**
    - Set `meta_campaign.status` = `"created"`
    - Store `meta_campaign.campaign_id`
    - Store `meta_campaign.ad_set_ids`
    - Store `meta_campaign.ad_ids`
    - Add entry to `approval_log` with timestamp, operation, and approved_by

11. **Log to api-log.md** — Record all API calls made with endpoints, entity IDs, and results.

12. **Present result:**
    ```
    Campaign created in PAUSED state.

    Campaign ID: {campaign_id}
    Ad Set IDs: {ad_set_ids}
    Ad IDs: {ad_ids}

    Next: Run [GO] to activate when ready.
    ```
