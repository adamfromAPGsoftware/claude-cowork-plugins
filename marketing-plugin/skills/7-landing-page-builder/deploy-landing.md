---
name: deploy-landing
description: Deploy a generated landing page to Cloudflare Pages with dry-run preview
menu-code: DL
---

# Deploy Landing Page

Deploy a generated landing page to the `apg-landing-pages` Cloudflare Pages project.

## Process

1. **Load campaign data** — Read `marketing-plugin/data/campaign-data.json`. List campaigns where `landing_page.status` is `"generated"` or later (excluding `"not_started"`).

2. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Deploying landing page for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, present campaigns with their landing page status. Ask which one to deploy.

3. **Verify landing page exists** — Check that the file at `marketing-plugin/{landing_page.deploy_path}/index.html` exists. If not, inform user to run [GL] first.

4. **Verify tracking injected** — Check if `<!-- TRACKING_SCRIPTS -->` placeholder is still present in the HTML. If yes, warn: "Tracking scripts not yet injected. Run [ST] first for full tracking. Deploy anyway? (tracking can be added post-deploy by re-deploying)"

5. **Dry-run first** — Run:
   ```bash
   python3 marketing-plugin/scripts/deploy-landing-page.py --campaign-id {campaign_id} --dry-run
   ```

6. **Present dry-run results:**
   ```
   Deployment Preview — {campaign.name}

   Files to deploy:
   - data/landing-pages/{campaign_id}/index.html

   Target: apg-landing-pages (Cloudflare Pages)
   Domain: {landing_page.domain or "not configured — run [SD] first"}
   URL: {landing_page.full_url or "will be assigned after deployment"}

   This is APPROVAL GATE — Deploy to production?
   ```

7. **On approval** — Run:
   ```bash
   python3 marketing-plugin/scripts/deploy-landing-page.py --campaign-id {campaign_id} --execute
   ```

8. **Update campaign-data.json** — Set:
   - `landing_page.status` = `"deployed"`
   - `landing_page.deployed_at` = current ISO 8601 timestamp
   - Add to `approval_log`: `{ "gate": "landing_page", "status": "approved", "timestamp": "...", "notes": "Deployed to Cloudflare Pages" }`

9. **Report:**
   ```
   Deployment Complete — {campaign.name}

   URL: {landing_page.full_url}
   Deployed at: {deployed_at}
   Status: deployed

   Next: Verify the live page loads correctly, then proceed to [SD] if custom domain not yet configured.
   ```

10. **On rejection** — Log rejection in approval_log. Ask what needs to change. Offer to re-run [GL] or [ST].

## React Template (go-enhance)

When the campaign's `landing_page.template` is `go-enhance`, the deploy workflow changes:

1. **Build** — Run:
   ```bash
   cd marketing-plugin/{landing_page.deploy_path} && npm run build
   ```
   This produces a `dist/` directory with the production bundle.

2. **Deploy** — Deploy the `dist/` directory to Cloudflare Pages or Vercel. The go-enhance template includes a `vercel.json` for Vercel deployment. Choose based on the campaign's hosting preference.

3. **Domain setup** — The [SD] subdomain/domain setup process remains the same regardless of template type.

4. **Update campaign-data.json and report** — Same as steps 8-9 above.

## Error Handling

- If deployment script fails, show full error output and suggest checking CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in .env
- If domain is not configured, deployment still works (page accessible via Cloudflare Pages default URL) — note this in the report
