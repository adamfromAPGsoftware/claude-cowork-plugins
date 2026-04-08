---
name: lead-capture
description: Deploy a Cloudflare Worker for lead capture — form submission to CRM and Meta Conversions API
menu-code: LC
---

# Lead Capture — Deploy Form Webhook

Deploy a Cloudflare Worker that receives landing page form submissions, creates leads in the CRM, and fires Meta Conversions API lead events.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Setting up lead capture for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, list campaigns from `campaign-data.json`. Ask user to select one.

2. **Determine webhook config** — From the campaign config, extract:
   - Landing page URL (where the form lives)
   - CRM pipeline for lead creation
   - Notification email for new leads
   - Meta Pixel ID for Conversions API events

3. **Dry run** — Run:
   ```
   python3 marketing-plugin/scripts/setup-lead-webhook.py --campaign-id {id} --dry-run
   ```

4. **Present what will be deployed:**
   ```
   ═══ Lead Capture Worker Preview ═══

   Worker URL: https://leads.{YOUR_DOMAIN}/{campaign_slug}
   
   On form submission:
   1. Validate form data (name, email, phone)
   2. Create lead in CRM (your-crm.example.com/api/mcp)
      Pipeline: {pipeline}
      Auto-create: true
   3. Fire Meta Conversions API Lead event
      Pixel ID: {pixel_id}
      Hashed fields: email (SHA256), phone (SHA256)
   4. Return success redirect to thank-you page

   Notification: {notification_email}
   ```

5. **APPROVAL GATE** —
   ```
   ═══ APPROVAL GATE: Deploy Lead Capture Worker ═══

   Approve deploying this Worker to Cloudflare?
   [yes / no]
   ```

6. **On approval** — Run:
   ```
   python3 marketing-plugin/scripts/setup-lead-webhook.py --campaign-id {id} --execute
   ```

7. **Update campaign-data.json** — Set in the campaign:
   - `lead_capture.form_webhook_url`
   - `lead_capture.worker_name`
   - `lead_capture.deployed_at`

8. **Test the webhook** — Send a test form submission:
   ```
   curl -X POST {worker_url} \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Lead", "email": "test@{YOUR_DOMAIN}", "phone": "+61400000000", "test": true}'
   ```
   Verify the response is 200 and the test flag prevents CRM creation.

9. **Log to api-log.md** — Record Cloudflare deployment and test result.

10. **Present result:**
    ```
    Lead capture Worker deployed.

    Worker URL: {worker_url}
    Test: {pass/fail}

    Update the landing page form action to POST to this URL.

    Next: Run [MC] for campaign creation, or [GO] if everything is ready.
    ```
