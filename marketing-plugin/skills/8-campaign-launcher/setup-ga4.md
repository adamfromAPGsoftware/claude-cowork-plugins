---
name: setup-ga4
description: Create or configure a GA4 property and data stream for the campaign URL
menu-code: GA
---

# Setup GA4 — Configure Analytics Tracking

> **Pipeline Note:** GA4 setup is now the FIRST step in Track A of the build phase (runs before [GL]). The GA4 property and data stream can be created before the landing page is deployed — they use the planned domain URL from the campaign config. Data only starts flowing once the page is live with the measurement ID injected via [ST]. This means GA4 setup can run in parallel with Track B (creative generation).

Create or configure a GA4 property and web data stream for the campaign's landing page URL, then set up key events for conversion tracking.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Setting up GA4 for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, list campaigns from `campaign-data.json`. Ask user to select one.

2. **Check existing GA4** — Look at the campaign's `tracking` section in campaign-data.json. If `ga4_property_id` and `ga4_measurement_id` are already set:
   ```
   GA4 already configured for this campaign:
     Property ID: {property_id}
     Measurement ID: {measurement_id}

   Skip to event setup? [yes / no]
   ```

3. **Dry run** — If no existing property, run:
   ```
   python3 marketing-plugin/scripts/setup-ga4-property.py --campaign-id {id} --dry-run
   ```

4. **Present what will be created:**
   ```
   ═══ GA4 Property Setup Preview ═══

   Property Name: {property_name}
   Data Stream URL: {campaign_url}
   Measurement ID: (will be generated)

   Key Events to Create:
   - generate_lead (conversion)
   - form_submit
   - page_view

   Custom Dimensions:
   - utm_campaign
   - utm_source
   - utm_medium
   ```

5. **APPROVAL GATE** —
   ```
   ═══ APPROVAL GATE: Create GA4 Property ═══

   Approve creating this GA4 property?
   [yes / no]
   ```

6. **On approval** — Run:
   ```
   python3 marketing-plugin/scripts/setup-ga4-property.py --campaign-id {id} --execute
   ```

7. **Update campaign-data.json** — Set in the campaign's `tracking` section:
   - `ga4_property_id`
   - `ga4_measurement_id`

8. **Set up events** — Run the existing events setup script:
   ```
   python3 marketing-plugin/scripts/setup-ga4-events.py --property-id {property_id}
   ```

9. **Log to api-log.md** — Record GA4 API operations.

10. **Present result:**
    ```
    GA4 configured for {campaign_name}.

    Property ID: {property_id}
    Measurement ID: {measurement_id}
    Key Events: generate_lead, form_submit, page_view
    
    Add this measurement ID to the landing page's <head>:
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>

    Next: Run [LC] for lead capture webhook, or [MC] for campaign creation.
    ```
