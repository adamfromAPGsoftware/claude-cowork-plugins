---
name: deploy
description: Deploy client deliverables to Cloudflare Pages portal
menu-code: GD
---

# Deploy to Client Portal

## Purpose

Deploy the current client's deliverables to their password-protected portal on Cloudflare Pages. Each client gets a path like `your-portal.example.com/{EXAMPLE_CLIENT_SLUG}`.

## Process

### Step 1: Verify Configuration

Check that `clients/clients.json` exists at the repo root and contains a configuration entry for the current client.

```bash
cat clients/clients.json
```

If the client is not configured, tell the user what entry to add (refer to `clients.example.json` for the format). Remind them to set a real password.

### Step 2: Verify Deliverables Exist

Check that the client has HTML deliverables to deploy:

```bash
ls clients/{client_slug}/deliverables/*.html
```

If no deliverables exist, suggest running GA first.

### Step 3: Deploy

```bash
bash scripts/deploy.sh
```

### Step 4: Report

```
DEPLOYMENT COMPLETE — {company_name}
Deployed: {timestamp}

Portal URL: https://your-portal.example.com/{client_key}
Password:   (configured in clients/clients.json)

Files deployed:
  • index.html (client website)
  • process-map.html
  • priority-matrix.html
```
