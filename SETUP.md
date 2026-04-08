# Setup Guide

Step-by-step instructions to configure these plugins for your business.

## Prerequisites

- [Claude Code CLI](https://claude.ai/code) installed
- Python 3.10+ (for scripts in audit, finance, marketing plugins)
- `jq` (for the sync script: `brew install jq`)

## 1. Business Identity Configuration

Copy the example config and fill in your values:

```bash
cp config.example.json config.json
```

Edit `config.json` with your business details:

| Field | Description | Example |
|-------|-------------|---------|
| `company.name` | Your company display name | "Acme Software" |
| `company.domain` | Your website domain | "acmesoftware.com" |
| `company.email` | Primary contact email | "hello@acmesoftware.com" |
| `company.address` | Business address | "123 Main St, Suite 100" |
| `company.logo_url` | URL to your logo (square) | "https://cdn.example.com/logo.png" |
| `company.logo_wide_url` | URL to your wide logo | "https://cdn.example.com/logo-wide.png" |
| `company.social_handle` | Social media handle | "@acmesoftware" |
| `company.calendly_url` | Your booking link | "cal.com/acme/consult" |
| `crm.mcp_url` | Your CRM's MCP endpoint | "https://crm.acme.com/api/mcp" |
| `author.name` | Your name | "Jane Smith" |
| `cowork.project_root` | Absolute path to this repo on your machine | "/Users/jane/repos/plugins" |

## 2. API Keys

Copy the environment file and add your credentials:

```bash
cp .env.example .env
```

You only need keys for the plugins you plan to use:

### Sales Plugin
| Key | Service | How to get |
|-----|---------|------------|
| `FATHOM_API_KEY` | Fathom (meeting transcripts) | [fathom.video/settings/api](https://fathom.video/settings/api) |
| `GMAIL_CLIENT_ID` + `GMAIL_CLIENT_SECRET` | Gmail (email drafts) | [Google Cloud Console](https://console.cloud.google.com/apis/credentials) |

### Audit Plugin
| Key | Service | How to get |
|-----|---------|------------|
| `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN` | Cloudflare (portal deployment) | [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens) |

### Content Plugin
| Key | Service | How to get |
|-----|---------|------------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 | [Google Cloud Console](https://console.cloud.google.com/apis/credentials) |
| `LATE_API_KEY` | Late.dev (content scheduling) | [app.getlate.dev/settings/api](https://app.getlate.dev/settings/api) |
| `OPENROUTER_API_KEY` | OpenRouter (AI models) | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `SUPABASE_URL` + `SUPABASE_ANON_KEY` | Supabase (blog publishing) | [Supabase Dashboard](https://supabase.com/dashboard) |

### Marketing Plugin
| Key | Service | How to get |
|-----|---------|------------|
| `META_ACCESS_TOKEN` | Meta Marketing API | [Facebook Developers](https://developers.facebook.com/tools/explorer/) |
| `GA4_PROPERTY_ID` | Google Analytics 4 | GA4 Admin -> Property Settings |
| `GOOGLE_APPLICATION_CREDENTIALS` | GA4 service account | [Google Cloud Console](https://console.cloud.google.com) |

### Video Plugin
| Key | Service | How to get |
|-----|---------|------------|
| `DEEPGRAM_API_KEY` | DeepGram (transcription) | [console.deepgram.com](https://console.deepgram.com) |
| `HERA_API_KEY` | Hera (motion graphics) | Contact Hera |
| `OPENROUTER_API_KEY` | OpenRouter (visual analysis) | [openrouter.ai/keys](https://openrouter.ai/keys) |

## 3. CRM Setup

Each plugin has a `.mcp.json` pointing to your CRM's MCP endpoint. Update all 7 files:

```json
{
  "mcpServers": {
    "your-crm": {
      "type": "http",
      "url": "https://your-crm.example.com/api/mcp"
    }
  }
}
```

If you don't have an MCP-compatible CRM, the plugins still work — CRM calls will fail silently and the pipeline continues.

## 4. Customize Reference Files

These files contain `{YOUR_*}` placeholders. Replace them with your actual business data:

### Required (core functionality)
- `audit-plugin/references/pricing.md` — Your pricing tiers, rates, and margins
- `audit-plugin/skills/shared/email-voice.md` — Your email writing style and tone

### Recommended (for sales pipeline)
- `sales-plugin/references/offer-summary.md` — Your offer, guarantee, ROI framework, objection handlers
- `sales-plugin/references/pipeline.md` — Your sales-to-delivery pipeline flow

## 5. Cowork Configuration

If using Cowork (cloud sandbox), update the Desktop Commander project root in each SKILL.md:

Find: `{PROJECT_ROOT}`
Replace with: Your actual project path (e.g., `/Users/jane/repos/plugins`)

## 6. Install in Claude Code

To use these plugins with Claude Code, copy the plugin directories into your project, or reference them in your Claude Code configuration.

Each plugin's SKILL.md files can be activated as Claude Code skills. The typical approach is to mirror them into `.claude/skills/` in your project.

## 7. Verify

Activate each agent and verify it loads correctly:

1. Open Claude Code
2. Invoke a skill (e.g., `/audit-extractor`)
3. Confirm it loads its SKILL.md, shows the capability menu, and doesn't error on missing config

## Sync Script (For Maintainers)

If you're maintaining a private fork alongside this public repo, use the sync script:

```bash
bash sanitize.sh \
  --source ~/path/to/private-repo \
  --target ~/staging/public-plugins
```

This copies plugins, applies sanitization rules, scans for sensitive patterns, and outputs to a staging directory for review. See `sanitize-rules.json` for the full rule set.
