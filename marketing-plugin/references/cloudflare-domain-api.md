# Cloudflare Domain API Reference

## Overview

Landing pages are deployed to a dedicated Cloudflare Pages project (`{YOUR_CF_PAGES_PROJECT}`) and accessed via custom subdomains on `{YOUR_DOMAIN}`. Domain setup requires two API calls: creating a CNAME DNS record and adding the domain to the Pages project.

## Required Environment Variables

| Variable | Description | Permissions Required |
|----------|-------------|---------------------|
| `CLOUDFLARE_API_TOKEN` | API token for authentication | DNS:Edit, Pages:Edit |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account identifier | — |

## DNS Records API

### List DNS Records

```
GET /zones/{zone_id}/dns_records
```

Query parameters:
- `type` — Record type filter (e.g., `CNAME`)
- `name` — Record name filter (e.g., `audit.{YOUR_DOMAIN}`)

### Create DNS Record

```
POST /zones/{zone_id}/dns_records
```

Payload for subdomain CNAME:
```json
{
  "type": "CNAME",
  "name": "audit",
  "content": "{YOUR_CF_PAGES_PROJECT}.pages.dev",
  "proxied": true,
  "ttl": 1
}
```

- `proxied: true` enables Cloudflare proxy (required for SSL)
- `ttl: 1` means automatic TTL when proxied

### Update DNS Record

```
PUT /zones/{zone_id}/dns_records/{record_id}
```

Same payload as create. Use when the CNAME already exists and needs updating.

### Get Zone ID

```
GET /zones?name={YOUR_DOMAIN}&status=active
```

Returns the zone ID needed for all DNS operations.

## Cloudflare Pages API

### Deploy to Pages (Direct Upload)

```
POST /accounts/{account_id}/pages/projects/{project_name}/deployments
```

Multipart form upload of HTML files. Each file is a form field where the key is the relative path and the value is the file content.

### Add Custom Domain

```
POST /accounts/{account_id}/pages/projects/{project_name}/domains
```

Payload:
```json
{
  "name": "audit.{YOUR_DOMAIN}"
}
```

Returns 409 if domain already exists on the project (safe to ignore).

### List Custom Domains

```
GET /accounts/{account_id}/pages/projects/{project_name}/domains
```

## CNAME Record Format

For a subdomain `audit.{YOUR_DOMAIN}` pointing to the `{YOUR_CF_PAGES_PROJECT}` project:

```
Type:    CNAME
Name:    audit
Target:  {YOUR_CF_PAGES_PROJECT}.pages.dev
Proxied: Yes
TTL:     Auto
```

## SSL

SSL is automatically provisioned by Cloudflare when:
1. The CNAME record exists and is proxied
2. The domain is added as a custom domain on the Pages project

No manual certificate management is needed. SSL typically activates within 1-5 minutes.

## Script Reference

| Script | Purpose |
|--------|---------|
| `scripts/setup-cloudflare-domain.py --domain {domain}` | Dry-run: show planned DNS changes |
| `scripts/setup-cloudflare-domain.py --domain {domain} --execute` | Create CNAME + add custom domain |
| `scripts/deploy-landing-page.py --campaign-id {id}` | Dry-run: show deployment plan |
| `scripts/deploy-landing-page.py --campaign-id {id} --execute` | Upload files to Pages project |
