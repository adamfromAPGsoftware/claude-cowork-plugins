# Claude Cowork Plugins

A collection of production-grade plugins for [Claude Code](https://claude.ai/code) — each one a complete vertical workflow you can install into your own Claude Code environment.

## Plugins

### Sales Plugin

A Google-Sheets-powered B2B sales pipeline. Syncs lead activity from Gmail, Twilio, and Fathom into a Google Sheet, classifies leads, drafts personalised follow-up sequences, and presents everything in a local Kanban UI.

| Command | What happens |
|---------|-------------|
| `/sales:setup` | Interactive config wizard — writes `config.yaml` with your company, consultant profile, and integrations |
| `/sales:sync` | Pulls Gmail threads, Twilio SMS/calls, and Fathom transcripts into your Google Sheet |
| `/sales:classify` | AI classifies each lead against your ICP and assigns a nurture sequence |
| `/sales:draft` | Batch-drafts personalised follow-ups for all leads due today |
| `/sales:send` | Dispatches approved drafts via Gmail and Twilio SMS |
| `/sales:launch` | Opens the Kanban UI at `http://localhost:8765` |

**Requirements:** Python 3.9+, Google Cloud project (Sheets + Gmail APIs), Twilio (optional), Fathom (optional)

---

### Content Plugin

A personal brand content pipeline across 13+ social platforms. Research trending topics, generate scripts and LinkedIn posts, design thumbnails and carousels, run editorial quality gates, and publish — all from Claude Code.

| Command / Agent | What happens |
|----------------|-------------|
| `content:1-content-strategist` | Research, trends, competitive analysis, content ideation |
| `content:2-copywriter` | Scripts, LinkedIn posts, X posts, blogs, email copy |
| `content:3-creative-director` | Thumbnails, carousels, visual asset creation |
| `content:4-editor` | Quality gates — brand voice, ICP relevance, value delivery |
| `content:5-publisher` | Schedule and publish via Late.dev across 13+ platforms |
| `content:6-autopilot` | Daily LinkedIn + X drafts, 3×/week Instagram carousels |

**Requirements:** Late.dev API key (publisher), YouTube Data API (research), OpenRouter (images), Supabase (blog publishing — optional)

---

### Marketing Plugin

End-to-end paid campaign pipeline. Plan campaigns, scrape competitor ads, generate creatives, deploy landing pages, launch Meta campaigns, and analyse performance — all in one workflow.

| Command | What happens |
|---------|-------------|
| `/marketing:setup` | Configure company identity, brand, and integrations |
| `/marketing:new-campaign` | Define audience, angle, and funnel for a new campaign |
| `/marketing:generate-creatives` | AI-generate ad images and video scripts |
| `/marketing:build-landing-page` | Generate and deploy a Cloudflare Pages landing page |
| `/marketing:launch-campaign` | Create and launch Meta ad campaign |
| `/marketing:pull-meta` | Pull Meta performance data |
| `/marketing:review-performance` | Analyse results and recommend next actions |

**Requirements:** Meta Marketing API token, Cloudflare account (landing pages), OpenRouter (images), fal.ai (video — optional), Apify (competitor scraping — optional)

---

### Video Plugin

A complete video production pipeline. Ingest raw footage, transcribe, analyse pacing, generate storyboards, build motion graphics with Remotion, and render final edits — for long-form YouTube, short-form Reels/TikTok, VSLs, and Meta ads.

| Agent | Specialty |
|-------|-----------|
| `apg-video:1-video-editor` | Infrastructure — ingest, transcribe, analyse, clip |
| `apg-video:2-remotion` | 41-component Remotion motion graphics library |
| `apg-video:3-long-form` | 16:9 YouTube tutorials — intro decomposition + body passthrough |
| `apg-video:4-short-form` | 9:16 Reels/TikTok/Shorts — MG-first vertical editing |
| `apg-video:5-vsl` | Direct-response VSLs — overlay density, pacing rules |
| `apg-video:6-ad` | 20-30s Meta ads — speaker-first, split-screen |

**Requirements:** Deepgram API key (transcription), OpenRouter (visual analysis), Hera API key (motion graphics), Node.js + FFmpeg (rendering)

---

### PM Plugin

A complete client project delivery pipeline. Create clients, drop in meeting transcripts and materials, ingest them into a structured knowledge base, map the client's process, research automation opportunities, and build a working Claude Desktop demo — all without leaving Claude Code.

| Command | What happens |
|---------|-------------|
| `/pm:setup` | Configure the plugin for your business — company identity, brand, pricing, integrations |
| `/pm:new-client` | Create a client folder with structured materials and meetings directories |
| `/pm:new-project` | Collect engagement scope and generate a branded HTML/PDF proposal |
| `/pm:sync` | Scan for new meeting transcripts and materials (or pull from Fathom if enabled) |
| `/pm:ingest` | Analyze all client materials → structured materials-summary.json |
| `/pm:scope` | Build a granular process map → interactive HTML visual for client review |
| `/pm:research` | Research automation tools and build a phase-collapse plan |
| `/pm:demo` | Build a working Claude Desktop skill or HTML prototype for the demo call |

**Requirements:** Python 3.9+, PyYAML. WeasyPrint optional (PDF proposals). Fathom optional (auto transcript sync). CRM MCP optional (invoice creation and task push).

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-org/public-claude-cowork-plugins
cd public-claude-cowork-plugins

# 2. Configure environment
cp .env.example .env
# Fill in the credentials for the plugins you want to use

# 3. Open in Claude Code
claude

# 4. Run the setup wizard for the plugin you want
/sales:setup
/marketing:setup
```

See [SETUP.md](SETUP.md) for full per-plugin setup instructions.

## Plugin Structure

Each plugin follows the same structure:

```
{name}-plugin/
├── .claude-plugin/plugin.json   # Plugin manifest
├── agents/                      # Agent definitions
├── commands/                    # Slash command shortcuts
├── skills/                      # Capability menus and prompts
├── scripts/                     # Python automation scripts
├── references/                  # Framework and schema docs
├── data/                        # Runtime data (gitignored)
├── config.yaml                  # Business config (written by /setup)
└── CLAUDE.md                    # Plugin wiki (auto-loaded by Claude Code)
```

## License

MIT
