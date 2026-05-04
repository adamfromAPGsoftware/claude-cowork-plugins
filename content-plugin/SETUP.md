# Content Plugin — Setup Guide

## Prerequisites

- Node.js 18+ and Python 3.10+ installed
- Claude Code CLI installed and authenticated
- Content plugin installed (this directory lives at `content-plugin/` inside your repo root)

## Step 1 — Configure the plugin

Run the setup wizard:

```
/content:0-setup
```

Type `SW` to start the setup wizard. It first asks you for a **content workspace path** — the folder on your computer where all your content, projects, and outputs will be stored — then walks you through 8 sections:

- **Content workspace** — where on your computer to store content (e.g. `~/Content`). The plugin creates the folder scaffold for you.
1. **Creator profile** — your name, niche, and content goals
2. **Brand voice** — tone, style, vocabulary, anti-AI red flags
3. **Content ICP** — ideal viewer/reader profile, pain points, transformation
4. **Platform config** — which platforms you publish to, account handles
5. **Credentials** — verifies each MCP server is connected
6. **Scheduling config** — Buffer channel connections, posting cadence
7. **Brand assets** — primary colour, logo path, email header/footer config
8. **Content strategy** — competitor channels, content pillars, X Premium status

## Step 2 — MCP servers (platform-level)

The content plugin uses four MCP servers connected at the Claude Code platform level:

- **YouTube MCP** (`mcp__youtube__*`) — video search, channel stats, transcripts
- **fal-ai MCP** (`mcp__fal-ai__*`) — image generation, video generation
- **Buffer MCP** (`mcp__buffer__*`) — social media scheduling and publishing
- **Exa MCP** (`mcp__exa__*`) — web search for trend research

These are already connected in Claude Code. No API keys or config needed in this plugin.

## Step 3 — Install Python dependencies

```bash
pip install youtube-transcript-api pytrends
```

Node dependencies (LinkedIn comment processor only):

```bash
cd content-plugin/skills/5-publisher/workflows/linkedin-comment-processor
npm install
npx playwright install chromium
```

## Step 4 — Verify setup

```
/content:0-setup
```

Type `VC` to run the verification check. It confirms all required config fields are set, reference files exist, and each MCP server is reachable.

## What gets configured

After completing the setup wizard, the plugin creates or populates:

| File / Location | Contents |
|------|---------|
| `config.yaml` | Workspace paths, env var names, brand config |
| Your content workspace folder | `projects/`, `context/references/`, `standalone/`, `context/brand-assets/logos/`, `context/brand-assets/reference-photos/` — created automatically |
| `context/references/brand-voice.md` | Tone guide, vocabulary list, anti-AI filter |
| `context/references/content-icp.md` | Ideal viewer/reader profile |
| `context/references/platform-config.md` | Active platforms, account handles, format specs |
| `context/references/scheduling-config.md` | Buffer channel names, posting cadence per platform |
| `context/references/brand-assets.md` | Primary colour, logo path, email header/footer config |

## Blog publishing

Blog posts are exported as CMS-ready markdown files with YAML frontmatter. You deploy them yourself:

- **Ghost / WordPress:** Import the markdown file directly
- **Astro / Hugo / Next.js:** Drop into your `content/` directory
- **Notion:** Paste body or use Notion API import
- **Beehiiv / Kit:** Copy body into your email editor

## Next steps

Start your first competitive research session:

```
/content:1-content-strategist
```

Type `CR` to begin competitive research.

## Plugin structure

After running setup, your project root contains:

```
{project-root}/
  config.yaml            Brand, voice, ICP, platform, and scheduling config
  context/
    references/
      brand-voice.md       Tone guide, vocabulary rules, anti-AI filter
      content-icp.md       Ideal viewer/reader profile
      platform-config.md   Active platforms, cadence, repurposing flow
      scheduling-config.md Buffer channel names, timezone
      brand-assets.md      Colours, logos, email config, content strategy
    brand-assets/
      logos/               Brand logos (brand-logo.png, brand-logo-dark.png, etc.)
      reference-photos/    Creator headshots for identity-preserving generation
  projects/              Content projects (one folder per project slug)
  standalone/            Non-project content
  content-plugin/        The plugin (skills, agents, workflows, data)
```
