---
name: setup-domain
description: Configure a custom subdomain on Cloudflare DNS pointing to the Pages project
menu-code: SD
---

# Setup Domain

Configure a custom subdomain on {YOUR_DOMAIN} pointing to the `apg-landing-pages` Cloudflare Pages project.

## Process

1. **Load campaign data** — Read `marketing-plugin/data/campaign-data.json`. List campaigns that have a `landing_page.domain` configured.

2. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Setting up domain for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, present campaigns. If multiple, present list.
   - If the selected campaign has no `landing_page.domain`, ask the user for the desired subdomain (e.g., `audit.{YOUR_DOMAIN}`).

3. **Read domain config** — Extract `landing_page.domain` from the selected campaign.

4. **Dry-run first** — Run:
   ```bash
   python3 marketing-plugin/scripts/setup-cloudflare-domain.py --domain {domain} --dry-run
   ```

5. **Present dry-run results:**
   ```
   Domain Setup Preview — {domain}

   DNS Record:
   - Type: CNAME
   - Name: {subdomain} (e.g., "audit")
   - Target: apg-landing-pages.pages.dev
   - Proxied: Yes

   Pages Custom Domain:
   - Project: apg-landing-pages
   - Domain: {domain}

   SSL: Will be automatically provisioned by Cloudflare

   Proceed with domain setup?
   ```

6. **On approval** — Run:
   ```bash
   python3 marketing-plugin/scripts/setup-cloudflare-domain.py --domain {domain} --execute
   ```

7. **Update campaign-data.json** — Set:
   - `landing_page.full_url` = `"https://{domain}{landing_page.path or '/'}"`
   - `landing_page.status` = `"live"` (if already deployed) or leave as-is

8. **Report:**
   ```
   Domain Configured — {domain}

   CNAME: {subdomain} -> apg-landing-pages.pages.dev
   SSL: Auto-provisioned (may take a few minutes)
   URL: https://{domain}/

   Next: Verify the URL resolves correctly. If not yet deployed, run [DL].
   ```

9. **On rejection** — Ask for alternative subdomain or cancel.

## Error Handling

- If the CNAME record already exists, the script will report this — ask user if they want to update it
- If the domain is not on the {YOUR_DOMAIN} zone, report the error and suggest using a subdomain of {YOUR_DOMAIN}
- If Cloudflare API returns permission errors, check CLOUDFLARE_API_TOKEN has DNS edit and Pages edit permissions
