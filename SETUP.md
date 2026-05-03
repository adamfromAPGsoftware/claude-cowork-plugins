# Setup Guide

Step-by-step setup for all Claude Cowork Plugins.

## Prerequisites (all plugins)

- [Claude Code CLI](https://claude.ai/code) installed
- Python 3.9+

## Step 1: Configure environment variables

```bash
cp .env.example .env
```

Fill in the values for the plugins you plan to use. Each section of `.env.example` is labelled by plugin.

---

## Sales Plugin

### Requirements
- Google Cloud project with Sheets API and Gmail API enabled
- Twilio account (optional — SMS and click-to-call)
- Fathom account (optional — meeting transcript sync)

### Setup

**1. Google Sheets (service account)**

1. Go to [Google Cloud Console](https://console.cloud.google.com) → create or select a project
2. Enable **Google Sheets API** and **Gmail API**
3. Create a service account: IAM & Admin → Service Accounts → Create → download the JSON key
4. Create an OAuth 2.0 client ID: APIs & Services → Credentials → Create (Desktop app)
5. Create a new Google Sheet and share it with the service account email (Editor access)

Full walkthrough: [sales-plugin/scripts/sheets-auth-setup.md](sales-plugin/scripts/sheets-auth-setup.md)

**2. Run setup wizard**

Open this repo in Claude Code, then:

```
/sales:setup
```

The wizard walks through: company identity, consultant profile, integrations, and first offer.

**3. First sync**

```
/sales:sync
```

Gmail OAuth triggers a browser consent window automatically on first run.

**4. Launch the board**

```
/sales:launch
```

Opens `http://localhost:8765`.

---

## Content Plugin

### Requirements
- [Late.dev](https://getlate.dev) account with connected social accounts (publisher)
- YouTube Data API key (competitive research — optional)
- OpenRouter API key (image generation)
- Supabase project (blog publishing — optional)

### Setup

**1. Install Python dependencies**

```bash
pip install requests python-dotenv
```

**2. Connect Late.dev**

1. Sign up at [getlate.dev](https://getlate.dev)
2. Connect your social accounts (LinkedIn, X, Instagram, TikTok, etc.)
3. Go to Settings → API → create an API key
4. Add `LATE_API_KEY=your-key` to `.env`

**3. Configure your style profiles**

Open Claude Code and run:

```
/content:6-autopilot
```

Then select `[TS] Test Styles` to configure your content voice and style profiles.

**4. Start creating**

```
content:1-content-strategist   # research and ideation
content:2-copywriter            # write posts, scripts, emails
content:5-publisher             # schedule and publish
content:6-autopilot             # daily automated drafts
```

---

## Marketing Plugin

### Requirements
- Meta Business account with a verified ad account
- Cloudflare account (for landing page deployment)
- OpenRouter API key (image generation)
- fal.ai account (video generation — optional)
- Apify account (competitor scraping — optional)

### Setup

**1. Meta API token**

1. Go to [business.facebook.com](https://business.facebook.com) → Settings → Users → System Users
2. Create a system user (Admin role)
3. Click "Generate New Token" → select your app
4. Check permissions: `ads_management`, `ads_read`, `business_management`
5. Add `META_ACCESS_TOKEN=your-token` to `.env`

**2. Cloudflare**

1. Create a free [Cloudflare](https://cloudflare.com) account
2. Go to Profile → API Tokens → Create Token (Custom) with Cloudflare Pages Edit permission
3. Your Account ID is in the right sidebar on any Cloudflare dashboard page
4. Add `CLOUDFLARE_API_TOKEN=` and `CLOUDFLARE_ACCOUNT_ID=` to `.env`

**3. Run setup wizard**

```
/marketing:setup
```

The wizard walks through: company identity, brand colors, social proof, Cloudflare config, and integrations.

**4. Create your first campaign**

```
/marketing:new-campaign
```

---

## Video Plugin

### Requirements
- [Deepgram](https://deepgram.com) API key (transcription)
- OpenRouter API key (visual analysis via Gemini)
- Hera API key (motion graphics)
- Supabase project (reference image hosting for Hera)
- FFmpeg installed (`brew install ffmpeg` on Mac)
- Node.js 18+ (for Remotion rendering)

### Setup

**1. Install system dependencies**

```bash
brew install ffmpeg
# Verify: ffmpeg -version
```

**2. Configure API keys**

Add to `.env`:
```
DEEPGRAM_API_KEY=your-deepgram-key
OPENROUTER_API_KEY=your-openrouter-key
HERA_API_KEY=your-hera-key
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

**3. Install Remotion dependencies** (optional — only needed for motion graphics rendering)

```bash
cd video-plugin/skills/2-remotion/references/template-showcase
npm install
```

**4. Start editing**

Open Claude Code and invoke any video agent:

```
apg-video:1-video-editor   # ingest and transcribe raw footage
apg-video:3-long-form      # edit a YouTube tutorial
apg-video:4-short-form     # edit a Reel or TikTok
apg-video:5-vsl            # edit a VSL
apg-video:6-ad             # edit a Meta ad
```

---

## PM Plugin

### Requirements
- Python 3.9+ with PyYAML (`pip install pyyaml`)
- WeasyPrint (optional — PDF proposals): `pip install weasyprint`
- Fathom account (optional — meeting transcript sync)
- CRM with MCP server (optional — invoicing and task push)

### Setup

**1. Install Python dependencies**

```bash
pip install pyyaml
pip install weasyprint   # optional
```

**2. Run setup wizard**

Open this repo in Claude Code, then:

```
/pm:setup
```

The wizard walks through: company identity, consultant profile, brand colors, pricing & tax defaults, and integrations (CRM and Fathom — both optional).

**3. Create your first client**

```
/pm:new-client
```

Drop meeting transcripts into `pm-plugin/data/clients/{slug}/meetings/{date-slug}/transcript.txt` and materials into `pm-plugin/data/clients/{slug}/materials/`.

**4. Run the pipeline**

```
/pm:sync       → index meetings and materials
/pm:ingest     → analyze all materials
/pm:scope      → build process map
/pm:research   → research automation
/pm:demo       → build a working demo
```

Full setup guide: [pm-plugin/SETUP.md](pm-plugin/SETUP.md)

---

## Adding a new plugin

Install additional plugins from the [marketplace](.claude-plugin/marketplace.json) by running Claude Code in this directory — it will auto-discover all plugins defined in `marketplace.json`.
