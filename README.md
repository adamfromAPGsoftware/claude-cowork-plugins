# Claude Cowork Plugins

A collection of 5 AI-powered business operations plugins for [Claude Code](https://claude.ai/code) and [Cowork](https://cowork.anthropic.com). These plugins implement a full consulting delivery pipeline — from sales prospecting through to client deliverable generation — using numbered AI agents that chain together through structured data contracts.

## Plugins

| Plugin | Agents | Purpose | Key Integrations |
|--------|--------|---------|-----------------|
| **sales-plugin** | Call Prep, Sales Closer | Pre-call research, competitor analysis, close pages, follow-up emails | Fathom, Gmail, CRM |
| **audit-plugin** | Extractor, Researcher, Builder, Designer | Process mapping, improvement research, HTML deliverables, solution architecture | CRM, Cloudflare |
| **content-plugin** | Strategist, Copywriter, Creative Director, Editor, Publisher | Content research, copywriting, visual design, quality gates, publishing | YouTube, Late.dev, OpenRouter, Supabase |
| **marketing-plugin** | Campaign Collector, Performance Analyst, Funnel Mapper | Ad campaign data collection, performance analysis, funnel mapping | Meta Ads, Google Analytics |
| **video-plugin** | Video Editor | Video ingest, transcription, clipping, storyboarding, motion graphics | DeepGram, Hera, OpenRouter |

## Architecture

Each plugin is self-contained and follows this structure:

```
{domain}-plugin/
├── .claude-plugin/plugin.json    # Plugin metadata
├── .mcp.json                     # CRM MCP server binding
├── .env.example                  # Required API keys
├── agents/                       # Agent persona definitions
├── skills/{N}-{name}/            # Numbered skill implementations
│   ├── SKILL.md                  # On-activation instructions + capability menu
│   ├── bmad-manifest.json        # Capability registry (codes → prompt files)
│   └── {capability}.md           # Implementation prompts per capability
├── commands/                     # CLI command definitions
├── hooks/                        # Event-triggered automation
├── references/                   # Business logic docs, API guides
├── scripts/                      # Python/bash automation
└── templates/                    # HTML/email templates
```

### How Agents Chain

Agents are numbered to reflect pipeline order. Each agent produces structured data (typically in `audit-data.json`) that downstream agents consume:

```
1-Call Prep → 2-Sales Closer → 3-Audit Extractor → 4-Improvement Researcher
→ 5-Deliverable Builder → 6-Solution Designer
```

Data flows one-way through `audit-data.json`, which accumulates structured extractions at each stage. See `references/pipeline.md` in the sales or audit plugin for the full pipeline definition and data contracts.

### CRM Integration

All plugins sync to a CRM via HTTP MCP (Model Context Protocol). The `.mcp.json` in each plugin points to your CRM endpoint. CRM updates are best-effort — failures never block the pipeline.

### Dual Environment: Terminal & Cowork

Plugins run in both environments without code changes:

- **Claude Code (terminal)**: Skills use native file system access directly
- **Cowork (cloud sandbox)**: Skills detect the sandbox and route through Desktop Commander MCP to proxy operations back to your host machine

Each SKILL.md includes a "Desktop Commander / Cowork Execution" section that activates automatically when running in Cowork.

## Quick Start

1. **Clone this repo**
   ```bash
   git clone https://github.com/your-org/public-claude-cowork-plugins.git
   cd public-claude-cowork-plugins
   ```

2. **Configure your business identity** — copy and fill in `config.example.json`

3. **Set up API keys** — copy `.env.example` to `.env` and add credentials for the plugins you plan to use

4. **Point CRM to your endpoint** — update the `url` in each plugin's `.mcp.json`

5. **Install plugins in Claude Code** — copy the plugin directories to your project or reference them

See [SETUP.md](SETUP.md) for detailed step-by-step instructions.

## Plugin Details

### Sales Plugin
**Agents**: 1-Call Prep, 2-Sales Closer

Pre-discovery research, competitor battle cards, close page generation, post-call transcript analysis, follow-up email and SMS drafting. Includes the CLOSER sales framework and nurture email sequences.

### Audit Plugin
**Agents**: 3-Extractor, 4-Researcher, 5-Builder, 6-Designer

The core consulting delivery pipeline. Extracts structured process data from meeting transcripts, researches improvement opportunities with ROI estimates, generates HTML deliverables (process maps, findings, waste analysis, strategic approaches), and builds clickable prototypes for custom solutions.

### Content Plugin
**Agents**: Strategist, Copywriter, Creative Director, Editor, Publisher

Full content production pipeline — competitive research and trend analysis, script writing across platforms (YouTube, LinkedIn, X, blog, email), visual asset generation, editorial quality gates, and multi-platform publishing.

### Marketing Plugin
**Agents**: Campaign Collector, Performance Analyst, Funnel Mapper

Pulls Meta ad campaign data, analyzes landing page performance via GA4, maps ad-to-conversion funnels through UTM parameters, and maintains marketing-data.json as the analytics source of truth.

### Video Plugin
**Agent**: Video Editor

Full video pipeline — ingest, transcription (DeepGram), visual analysis, B-roll extraction, storyboarding, Remotion-based editing, motion graphics (Hera), and short-form clip generation.

## Customization

All plugins use `{YOUR_*}` placeholders for business-specific values. Key files to customize:

| File | What to customize |
|------|-------------------|
| Each `.mcp.json` | Your CRM endpoint URL |
| Each `plugin.json` | Your name and domain |
| `audit-plugin/references/pricing.md` | Your pricing tiers and rates |
| `audit-plugin/skills/shared/email-voice.md` | Your email writing style |
| `sales-plugin/references/offer-summary.md` | Your offer, ROI framework, objection handlers |

## License

MIT — see [LICENSE](LICENSE)
