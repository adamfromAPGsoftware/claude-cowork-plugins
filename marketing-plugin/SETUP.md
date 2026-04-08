# Marketing Analytics Plugin — Setup Guide

This plugin pulls Meta (Facebook/Instagram) ad campaign performance data and Google Analytics 4 landing page analytics into a unified `marketing-data.json` file for analysis.

## Prerequisites

- **Python 3.9+** installed
- **pip** (Python package manager)
- **Claude Desktop** with Desktop Commander MCP enabled (or Claude Code)

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests python-dotenv google-analytics-data
```

### 2. Set up credentials

```bash
cp .env.example .env
```

Then edit `.env` and fill in your values. See the sections below for how to get each credential.

### 3. Pull data

```bash
# Pull Meta campaign data (last 30 days)
python3 scripts/fetch-meta-campaigns.py

# Pull GA4 analytics (last 30 days, landing page property)
python3 scripts/fetch-ga4-analytics.py --property landing

# Pull both GA4 properties
python3 scripts/fetch-ga4-analytics.py --property all
```

Data is saved to `data/marketing-data.json`.

---

## Setting Up Meta Marketing API

### Step 1: Create a Meta App (if you don't have one)

1. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps/)
2. Click **Create App** → select **Business** type
3. Name it (e.g., "Marketing Analytics")
4. In the app dashboard, click **Add Product** → add **Marketing API**

### Step 2: Get an access token

1. Go to [developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app from the dropdown
3. Under **Token Permissions**, check:
   - `ads_read`
   - `read_insights`
4. Click **Generate Access Token**
5. Copy the token and paste it into your `.env` file as `META_ACCESS_TOKEN`

**Important:** This token is short-lived (~1-2 hours). When it expires, you'll see an authentication error. Just generate a new one from the same page and update `.env`.

### Step 3: Verify

```bash
python3 scripts/fetch-meta-campaigns.py
```

The script will auto-discover your ad accounts and pull campaign data. If you have multiple ad accounts, it will list them and use the first one by default. You can change this in `data/marketing-data.json` by editing the `meta_ad_account_id` field.

---

## Setting Up Google Analytics 4 (Optional)

GA4 integration requires a Google Cloud service account. This is a one-time setup.

### Step 1: Create a GCP project (or use existing)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project or select an existing one

### Step 2: Enable the Analytics Data API

1. In GCP Console, go to **APIs & Services** → **Library**
2. Search for **"Google Analytics Data API"**
3. Click it → click **Enable**

### Step 3: Create a service account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **+ Create Service Account**
3. Name: `ga4-reader` (or anything descriptive)
4. Click **Create and Continue**
5. Skip the optional role/access steps → click **Done**
6. Click into the new service account
7. Go to the **Keys** tab → **Add Key** → **Create new key** → **JSON**
8. A `.json` file will download

### Step 4: Place the key file

Move the downloaded JSON file into this plugin directory and name it `ga4-service-account.json`:

```bash
mv ~/Downloads/your-project-abc123.json ga4-service-account.json
```

Make sure the filename in your `.env` matches:
```
GOOGLE_APPLICATION_CREDENTIALS=ga4-service-account.json
```

### Step 5: Grant access in GA4

1. Go to [analytics.google.com](https://analytics.google.com)
2. Select your property → **Admin** (gear icon)
3. Under **Property**, click **Property Access Management**
4. Click **+** → **Add users**
5. Email: paste the service account email (found in the JSON file under `client_email`, e.g., `ga4-reader@your-project.iam.gserviceaccount.com`)
6. Role: **Viewer**
7. Click **Add**

Repeat for each GA4 property you want to track.

### Step 6: Add property IDs to .env

Find your GA4 Property ID:
1. In GA4 → **Admin** → **Property Settings**
2. Copy the numeric **Property ID**

Add to `.env`:
```
# Primary landing page (e.g., go.yourdomain.com)
GA4_PROPERTY_ID=123456789

# Main website (optional, e.g., yourdomain.com)
GA4_PROPERTY_ID_HOME=987654321
```

### Step 7: Verify

```bash
# Test landing page property
python3 scripts/fetch-ga4-analytics.py --property landing

# Test both properties
python3 scripts/fetch-ga4-analytics.py --property all
```

---

## Setting Up Apify (Competitor Intelligence)

Apify is used to scrape competitor ads from Meta's Ad Library.

### Step 1: Create an Apify account

1. Sign up at [apify.com](https://apify.com)
2. The free tier includes 0.5 compute units/month (enough for ~10-50 small scrapes)

### Step 2: Get your API token

1. Go to [console.apify.com/account/integrations](https://console.apify.com/account/integrations)
2. Copy your **Personal API Token**
3. Add to `.env`:
   ```
   APIFY_API_TOKEN=apify_api_xxxxxxxxxx
   ```

### Step 3: Verify

```bash
python3 scripts/scrape-competitor-ads.py --pages 123456789 --country AU
```

Replace `123456789` with a real Facebook Page ID. You can find Page IDs by searching on [facebook.com/ads/library](https://www.facebook.com/ads/library/) and checking the URL.

---

## Setting Up fal.ai (Video Generation)

fal.ai provides access to video generation models (Kling 3.0, Veo 3.1) for creating video ad creatives.

### Step 1: Create a fal.ai account

1. Sign up at [fal.ai](https://fal.ai)
2. Add credits (pay-as-you-go, ~$0.03-0.60 per video depending on model)

### Step 2: Get your API key

1. Go to [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
2. Create a new API key
3. Add to `.env`:
   ```
   FAL_API_KEY=your_fal_api_key_here
   ```

### Step 3: Verify

```bash
python3 scripts/generate-ad-video.py --prompt "A small business owner smiling at a laptop" --aspect 9:16 --output test-video.mp4 --model kling --duration 5
```

---

## Setting Up Image Generation

Image generation uses Nano Banana Pro (Google Gemini Flash Image) via OpenRouter. The `OPENROUTER_API_KEY` should already be configured in the repo root `.env` file. No additional setup is needed for this plugin.

If you don't have an OpenRouter key:
1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Add credits and generate an API key
3. Add to the repo root `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxx
   ```

---

## Using in Claude Desktop

This plugin requires **Desktop Commander MCP** to execute Python scripts. Make sure it's enabled in your Claude Desktop MCP settings.

When you activate the plugin skills, Claude will use Desktop Commander's `execute_command` tool to run the fetch scripts. The skills will guide you through the process interactively.

### Available skills:

| Skill | What it does |
|-------|-------------|
| Campaign Collector | Pull Meta campaigns and GA4 data |
| Performance Analyst | Analyze campaign spend, CTR, CPC, conversions |
| Funnel Mapper | Map ad spend to conversions |
| Competitor Intelligence | Scrape competitor ads, download creatives, analyse with AI, track winners |
| Creative Generator | Build angles, generate image/video creatives, package for upload |

### Available commands:

| Command | What it does |
|---------|-------------|
| pull-meta | Fetch latest Meta campaign data |
| status | Show data health and sync status |
| campaign-summary | Summarize campaign performance |
| funnel-overview | Show ad-to-conversion funnel |
| scrape-competitors | Scrape competitor ads from Meta Ad Library |
| track-winners | Show competitor ad winner leaderboard |
| build-angles | Generate ad angles from competitor intel |
| generate-creatives | Produce image/video ad creatives |

---

## Using in Claude Code

In Claude Code, the plugin works with the Bash tool directly. The skills and commands are available as slash commands (e.g., `/bmad-apg-mkt-1-campaign-collector`).

---

## Troubleshooting

### "META_ACCESS_TOKEN not set"
Copy `.env.example` to `.env` and add your token. See "Setting Up Meta Marketing API" above.

### "Authentication failed — Invalid token"
Your Meta token has expired (they last ~1-2 hours). Generate a new one at [developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer/).

### "403 User does not have sufficient permissions for this property"
The service account doesn't have Viewer access to the GA4 property. Follow Step 5 in "Setting Up Google Analytics 4".

### "Service account key not found"
Make sure `ga4-service-account.json` is in the plugin directory (not somewhere else), and the filename in `.env` matches.

### No campaigns found
You may have multiple ad accounts. Run the script — it will list all accounts. Edit `data/marketing-data.json` and change `meta_ad_account_id` to the correct account ID.

---

## File Structure

```
marketing-plugin/
├── .env.example          ← Copy to .env and add your credentials
├── .env                  ← Your credentials (not committed)
├── ga4-service-account.json  ← Your GA4 key (not committed)
├── SETUP.md              ← This file
├── requirements.txt      ← Python dependencies
├── scripts/
│   ├── fetch-meta-campaigns.py        ← Meta data fetcher
│   ├── fetch-ga4-analytics.py         ← GA4 data fetcher
│   ├── scrape-competitor-ads.py       ← Apify competitor ad scraper
│   ├── download-competitor-assets.py  ← Competitor creative downloader
│   ├── analyse-competitor-creatives.py ← Gemini vision creative analyser
│   ├── generate-ad-image.py           ← Nano Banana Pro image generator
│   └── generate-ad-video.py           ← fal.ai video generator
├── data/
│   ├── marketing-data.json            ← Campaign performance data
│   ├── competitor-data.json           ← Competitor ad intelligence
│   ├── creative-data.json             ← Generated creative batches
│   ├── competitor-assets/             ← Downloaded competitor creatives
│   └── creatives/                     ← Generated ad creatives
├── skills/               ← Agent skill definitions
├── agents/               ← Agent entry points
├── commands/             ← Quick commands
└── references/           ← API docs and schema reference
```
