# Marketing Plugin — Setup Guide

End-to-end paid marketing pipeline: campaign planning → competitor intelligence → creative generation → landing page deployment → Meta campaign launch → performance-driven iteration.

---

## Before You Start — What You'll Need

| Service | What It Does | Required? | Cost |
|---------|-------------|-----------|------|
| Meta Ads MCP | Run and manage ads, pull performance data | Yes | Free (pay for ads) |
| Higgsfield MCP | Generate AI images + video ads | Yes | Pay-per-generation |
| fal-ai MCP | Background music, transcription | Platform-level | No setup needed |
| Cloudflare | Deploy landing pages and lead capture | Yes | Free tier works |
| Apify | Scrape competitor ads | Optional | Free tier (~50/month) |
| Google Analytics 4 | Track landing page conversions | Optional | Free |

---

## Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 2 — Connect MCP Servers

Add these MCP servers to your Claude Code or Cowork settings (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "meta-ads": {
      "url": "https://mcp.facebook.com/ads"
    },
    "higgsfield": {
      "url": "https://mcp.higgsfield.ai"
    }
  }
}
```

Then authenticate each:
- **Meta Ads MCP** — you'll be prompted to connect your Meta Business account via OAuth. Select the ad account you want to manage.
- **Higgsfield MCP** — you'll be prompted to connect your Higgsfield account. No API key needed.

The fal-ai MCP (`mcp__fal-ai__*` tools) is available platform-level in Claude Code — no configuration needed.

---

## Step 3 — Set Environment Variables

Copy the example and fill in only what's needed:

```bash
cp .env.example .env
```

Required `.env` keys:
- `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` — for landing page deployment
- `APIFY_API_TOKEN` — optional, for competitor intelligence
- `GOOGLE_APPLICATION_CREDENTIALS`, `GA4_PROPERTY_ID` — optional, for conversion tracking

See the credential sections below for step-by-step instructions.

---

## Step 4 — Configure the Plugin

Open Claude Code in this directory and run:

```
/marketing:setup
```

The setup wizard walks you through company name, domain, brand colors, social proof, CRM, and integrations. It validates as you go and writes everything to `config.yaml`. Takes about 10 minutes.

---

## Step 5 — Create Your First Campaign

```
/marketing:1-strategist
```

Type `NC` to create your first campaign.

---

## Credential Reference

### Meta Ads MCP

**What it does:** Full Meta ad campaign lifecycle — read performance data, create campaigns, upload creatives, manage budgets.

**Setup (no API key needed):**

1. Add to your Claude Code MCP settings:
   ```json
   "meta-ads": { "url": "https://mcp.facebook.com/ads" }
   ```
2. In Claude Code, type any Meta-related prompt — you'll be redirected to Meta's OAuth flow
3. Log in with your Meta Business account
4. Grant the requested permissions (`ads_management`, `ads_read`, `business_management`)
5. You're connected — no tokens to manage or rotate

**Verify:** Ask Claude "Check Meta MCP connection status" — the `health_check` tool will confirm you're authenticated and show your accessible ad accounts.

---

### Higgsfield MCP

**What it does:** AI image generation (Nano Banana, Soul models) and video generation (Kling 3.0, Veo 3.1, Seedance 2.0) with UGC presets, talking heads, and character training.

**Setup (no API key needed):**

1. Add to your Claude Code MCP settings:
   ```json
   "higgsfield": { "url": "https://mcp.higgsfield.ai" }
   ```
2. Connect your Higgsfield account via the OAuth prompt
3. Add credits at higgsfield.ai if needed (~$0.09 per image, ~$0.41–$2.50 per video)

---

### Cloudflare

**What it does:** Deploys landing pages to Cloudflare Pages and runs lead capture form handlers via Cloudflare Workers.

**Step 1 — Create a Cloudflare account**

Sign up at [cloudflare.com](https://cloudflare.com) if you don't have one. The free tier is sufficient.

**Step 2 — Add your domain to Cloudflare**

1. In your Cloudflare dashboard, click **Add a site**
2. Enter your domain and follow the steps to update your nameservers

**Step 3 — Create an API token**

1. Go to dash.cloudflare.com → Click your profile (top right) → **API Tokens**
2. Click **Create Token** → **Create Custom Token**
3. Name it e.g. `Marketing Plugin`
4. Add these permissions (all Account scope):

   | Account Resource | Permission |
   |-----------------|------------|
   | Cloudflare Pages | Edit |
   | Workers Scripts | Edit |
   | Workers R2 Storage | Edit |

5. Under **Account Resources**, select your account
6. Click **Continue to summary** → **Create Token**

**Step 4 — Find your Account ID**

In your Cloudflare dashboard → Workers & Pages — your Account ID is in the right sidebar.

**Add to `.env`:**
```
CLOUDFLARE_API_TOKEN=your_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
```

---

### Apify — Competitor Intelligence (Optional)

**What it does:** Scrapes the Meta Ad Library to find what your competitors are running.

1. Sign up at [apify.com](https://apify.com) — free tier includes ~50 scrapes/month
2. Go to [console.apify.com/account/integrations](https://console.apify.com/account/integrations)
3. Copy your **Personal API Token**

**Add to `.env`:**
```
APIFY_API_TOKEN=apify_api_xxxxxxxxxx
```

---

### Google Analytics 4 — Conversion Tracking (Optional)

**What it does:** Tracks visitors and conversions on your landing pages.

**Step 1 — Create a Google Cloud project**

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project dropdown → **New Project** → Name it → **Create**
3. Enable **Google Analytics Data API** (APIs & Services → Library)

**Step 2 — Create a service account**

1. Go to **IAM & Admin** → **Service Accounts** → **+ Create Service Account**
2. Name: `marketing-plugin` → **Create and Continue** → skip remaining steps → **Done**

**Step 3 — Download the JSON key**

1. Click on the service account → **Keys** tab → **Add Key** → **JSON** → **Create**
2. Rename the downloaded file to `ga4-service-account.json`
3. Move it into the plugin folder

**Step 4 — Grant access in Google Analytics**

1. Open the JSON file, copy the `client_email` value
2. Go to analytics.google.com → Admin → **Property Access Management**
3. Click **+** → Add the service account email as **Viewer**

**Step 5 — Find your GA4 Property ID**

GA4 → Admin → Property Settings → copy the numeric **Property ID**

**Add to `.env`:**
```
GOOGLE_APPLICATION_CREDENTIALS=ga4-service-account.json
GA4_PROPERTY_ID=123456789
GA4_PROPERTY_ID_HOME=987654321   # optional, main website
```

**Verify:**
```bash
python3 scripts/fetch-ga4-analytics.py --property landing
```

---

## Troubleshooting

### "Meta MCP not connected" or auth error
Reconnect via the Meta OAuth flow — in Claude Code, ask Claude to check the Meta MCP health. Follow the OAuth prompt to re-authenticate. No token rotation needed.

### "Higgsfield MCP not available"
Add the Higgsfield MCP URL to your Claude Code settings and restart. Connect your Higgsfield account via the OAuth prompt.

### "Cloudflare: 403 Forbidden"
Your API token is missing a permission. Go to dash.cloudflare.com → API Tokens and verify Pages, Workers Scripts, and Workers R2 Storage are all set to Edit.

### "403 User does not have sufficient permissions for this property" (GA4)
The service account doesn't have Viewer access. Make sure you added the `client_email` from the JSON file (not a personal Gmail) to the GA4 property.

### "Service account key not found"
The `ga4-service-account.json` file isn't in the plugin folder. It must be in the same folder as this SETUP.md file.

### Config validation shows missing required fields
Run `/marketing:setup` → `[SW]` to complete the setup wizard. The plugin won't work correctly until all required fields in `config.yaml` are filled in.

---

## File Structure

```
marketing-plugin/
├── .env.example              ← Copy to .env and add your credentials
├── .env                      ← Your credentials (never committed to git)
├── ga4-service-account.json  ← Your GA4 key file (never committed to git)
├── config.yaml               ← Plugin configuration (set up via /marketing:setup)
├── SETUP.md                  ← This file
├── HOW-IT-WORKS.md           ← Full system documentation
├── requirements.txt          ← Python dependencies
├── agents/                   ← Agent entry points (0-setup, 1-strategist, 2-creator, 3-analyst)
├── skills/                   ← Skill capability definitions
├── scripts/                  ← Python scripts (for GA4, Cloudflare, Apify — not Meta/image/video)
├── hyperframes/              ← HTML video compositions (captions, logo overlay, end screens)
├── data/                     ← Campaign data (created when you start campaigns)
├── templates/                ← Landing page HTML templates
└── references/               ← Brand guidelines, MCP tool reference, schemas
```
