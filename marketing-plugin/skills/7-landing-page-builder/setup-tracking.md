---
name: setup-tracking
description: Inject GA4, Meta Pixel, UTM capture, and form event tracking into a landing page
menu-code: ST
---

# Setup Tracking

Inject GA4 gtag.js, Meta Pixel, UTM parameter capture, and form submission event handlers into a generated landing page.

## Process

1. **Load campaign data** — Read `marketing-plugin/data/campaign-data.json`. List campaigns where `landing_page.status` is `"generated"` or `"deployed"` (tracking can be injected or re-injected at any stage).

2. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Setting up tracking for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, present campaigns with their tracking status. Ask which one.

3. **Load tracking config** — Extract from the selected campaign:
   - `tracking.ga4_measurement_id`
   - `tracking.meta_pixel_id`
   - `tracking.meta_capi_token`
   - `tracking.utm_source`, `tracking.utm_medium`, `tracking.utm_campaign`

4. **Check tracking IDs** — If `ga4_measurement_id` or `meta_pixel_id` are null/missing:
   - Inform user: "Tracking IDs not configured. You can either:"
   - "1. Run Campaign Launcher [GA] to set up GA4 property and Meta Pixel"
   - "2. Enter them manually now"
   - If user provides IDs manually, update campaign-data.json tracking section immediately.

5. **Load tracking template** — Read `marketing-plugin/templates/landing-pages/components/tracking.html`.

6. **Build tracking snippet** — Substitute into the tracking template:
   - `{{ga4_measurement_id}}` -> `tracking.ga4_measurement_id`
   - `{{meta_pixel_id}}` -> `tracking.meta_pixel_id`
   - Remove GA4 block entirely if `ga4_measurement_id` is null
   - Remove Meta Pixel block entirely if `meta_pixel_id` is null

7. **Read the generated landing page** — Load `marketing-plugin/data/landing-pages/{campaign_id}/index.html`.

8. **Inject tracking** — Replace `<!-- TRACKING_SCRIPTS -->` with the built tracking snippet. If the placeholder is not found, inject before `</head>`.

9. **Write updated HTML** — Save back to the same file.

10. **Update campaign-data.json** — Set:
    - `tracking.conversions_api_enabled` = `true` if `meta_capi_token` is present, `false` otherwise

11. **Report:**
    ```
    Tracking Injected — {campaign.name}

    GA4: {ga4_measurement_id or "not configured"}
    Meta Pixel: {meta_pixel_id or "not configured"}
    Conversions API: {enabled or "not configured (no CAPI token)"}

    Events configured:
    - PageView (GA4 + Meta Pixel)
    - generate_lead (GA4, on form submit)
    - Lead (Meta Pixel, on form submit)
    - UTM capture (sessionStorage, passed with form)

    File updated: data/landing-pages/{campaign_id}/index.html

    Next: Run [PV] to preview and verify tracking, then [DL] to deploy.
    ```

## React Template (go-enhance)

When the campaign's `landing_page.template` is `go-enhance`, the tracking infrastructure is already built into the React source. Instead of injecting HTML snippets, update the existing IDs in the source files:

1. **GA4** — Open `{deploy_path}/index.html` and update the measurement ID in the existing gtag.js snippet (replace the `G-XXXXXXXXXX` value with `tracking.ga4_measurement_id`).

2. **Meta Pixel** — Open `{deploy_path}/src/components/MetaPixel.tsx` and update the pixel ID in the existing `fbq('init', '...')` call (replace the placeholder with `tracking.meta_pixel_id`).

3. **No further injection needed** — The analytics infrastructure (`src/lib/analytics.ts` for UTM capture, `src/lib/meta-events.ts` for conversion events) is pre-wired. Once the IDs are set, all tracking flows automatically.

4. **Skip steps 5-8** from the HTML workflow above (no template loading, no snippet building, no placeholder injection).

5. **Update campaign-data.json and report** — Same as steps 10-11 above.

## Error Handling

- If landing page file doesn't exist, inform user to run [GL] first
- If neither GA4 nor Meta Pixel ID is available, warn that the page will have no tracking — proceed only if user confirms
- If tracking was already injected (no placeholder found), offer to re-inject (replace existing tracking block)
