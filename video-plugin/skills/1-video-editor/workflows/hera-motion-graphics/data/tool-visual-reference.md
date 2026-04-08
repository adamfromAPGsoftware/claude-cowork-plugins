# Tool Visual Reference Library

A comprehensive library of AI/tech tool visual identities for creating tool-specific motion graphics. When a storyboard MG brief references a named tool, look it up here to produce authentic-looking UI recreations and branded graphics.

Logos for any tool below can be fetched via `scripts/fetch-logo.ts`.

---

## AI Chat Interfaces

### Claude
- **Primary Colors:** `#D97757` (terracotta/orange), `#1A1A2E` (dark background), `#F5F0E8` (warm cream chat area)
- **UI Layout:** Left sidebar (dark, lists conversations), main chat panel with warm cream/beige background, rounded message bubbles
- **Key Visual Elements:** Terracotta-colored Claude icon (sparkle/asterisk shape), "Claude" wordmark, user messages right-aligned in darker bubbles, Claude responses left-aligned, thinking indicator with pulsing dots
- **Default `image_source`:** `canvas-build` or `frame-extract`

### ChatGPT
- **Primary Colors:** `#10A37F` (green accent), `#202123` (dark sidebar), `#343541` (dark chat bg), `#FFFFFF` (light mode bg)
- **UI Layout:** Dark left sidebar with conversation history, main chat area (dark or light mode), centered input bar at bottom
- **Key Visual Elements:** Green OpenAI logo/dot, "ChatGPT" text, model selector dropdown, message bubbles with subtle dividers, code blocks with dark background
- **Default `image_source`:** `canvas-build` or `frame-extract`

### Gemini
- **Primary Colors:** `#8E75B2` (purple), `#4285F4` (blue), `#EA4335` (red), `#FBBC04` (yellow), `#1F1F1F` (dark bg)
- **UI Layout:** Clean minimal interface, centered chat, Google-style material design, floating input bar
- **Key Visual Elements:** Multi-colored Gemini star/sparkle logo, Google account avatar top-right, response cards with subtle borders
- **Default `image_source`:** `canvas-build`

### Microsoft Copilot
- **Primary Colors:** `#0078D4` (Microsoft blue), `#242424` (dark bg), `#FFFFFF` (light bg)
- **UI Layout:** Centered chat interface, suggestion chips below input, Bing-integrated results
- **Key Visual Elements:** Multi-colored Copilot gradient icon (blue/green/orange/pink), "Copilot" wordmark, conversation style selector (Creative/Balanced/Precise)
- **Default `image_source`:** `canvas-build`

### Perplexity
- **Primary Colors:** `#1B9AAA` (teal), `#20B2AA` (light teal), `#0F172A` (dark bg), `#FFFFFF` (light bg)
- **UI Layout:** Search-first interface, answer panel with inline citations (numbered superscripts), source cards below
- **Key Visual Elements:** Teal Perplexity logo (abstract circular), numbered citation badges, "Sources" section with favicon + title cards, follow-up suggestions
- **Default `image_source`:** `canvas-build`

### Grok
- **Primary Colors:** `#000000` (black bg), `#FFFFFF` (white text), `#1D9BF0` (X/Twitter blue accent)
- **UI Layout:** Dark interface integrated with X/Twitter, minimal chrome, centered chat
- **Key Visual Elements:** Grok logo (stylized "G"), dark theme, witty/casual tone indicators, X integration elements
- **Default `image_source`:** `canvas-build`

### DeepSeek
- **Primary Colors:** `#4D6BFE` (blue), `#0F172A` (dark bg), `#FFFFFF` (light bg)
- **UI Layout:** Clean chat interface, conversation list sidebar, centered messages
- **Key Visual Elements:** Blue DeepSeek logo (whale/dolphin shape), "DeepThink" reasoning mode toggle, clean sans-serif typography
- **Default `image_source`:** `canvas-build`

---

## AI Companies / Brands

### Anthropic
- **Primary Colors:** `#D97757` (terracotta), `#1A1A2E` (dark), `#F5F0E8` (warm cream)
- **UI Layout:** Corporate website — clean, warm-toned, editorial feel
- **Key Visual Elements:** Anthropic wordmark (clean sans-serif), warm color palette, research-paper style layouts
- **Default `image_source`:** `fetch-logo`

### OpenAI
- **Primary Colors:** `#10A37F` (green), `#000000` (black), `#FFFFFF` (white)
- **UI Layout:** Minimal corporate site, heavy whitespace, green accents
- **Key Visual Elements:** OpenAI hexagonal logo, green accent color, clean sans-serif typography
- **Default `image_source`:** `fetch-logo`

### Google DeepMind
- **Primary Colors:** `#4285F4` (Google blue), `#0F9D58` (green), `#F4B400` (yellow), `#DB4437` (red)
- **UI Layout:** Google Material Design aesthetic, research publication style
- **Key Visual Elements:** DeepMind logo (layered triangles), Google colors, scientific paper layouts
- **Default `image_source`:** `fetch-logo`

### Meta AI
- **Primary Colors:** `#0668E1` (Meta blue), `#FFFFFF` (white), `#1C2B33` (dark)
- **UI Layout:** Clean corporate interface, blue gradient accents
- **Key Visual Elements:** Meta infinity logo, blue gradient, Llama branding for open-source models
- **Default `image_source`:** `fetch-logo`

### Mistral AI
- **Primary Colors:** `#FF7000` (orange), `#000000` (black), `#FFFFFF` (white)
- **UI Layout:** Bold, European-startup aesthetic, orange accents on dark/light backgrounds
- **Key Visual Elements:** Mistral windrose/compass logo (orange-black gradient tiles), bold typography
- **Default `image_source`:** `fetch-logo`

---

## Coding Assistants

### Cursor
- **Primary Colors:** `#7B61FF` (purple), `#1E1E2E` (dark editor bg), `#FFFFFF` (white text)
- **UI Layout:** VS Code-based editor with AI chat panel on right side, dark theme default
- **Key Visual Elements:** Purple Cursor logo (stylized cursor arrow), inline AI suggestions with purple highlight, AI chat sidebar, "Cmd+K" inline edit interface, tab completion ghost text
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Windsurf (Codeium)
- **Primary Colors:** `#09B6A2` (teal/green), `#1E1E2E` (dark bg), `#FFFFFF` (white)
- **UI Layout:** VS Code-based editor with AI "Cascade" panel, dark theme
- **Key Visual Elements:** Teal Windsurf logo (wave/sail shape), Cascade flow panel, inline completions with teal highlights
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Claude Code (CLI)
- **Primary Colors:** `#D97757` (terracotta), `#0F172A` (terminal dark bg), `#E2E8F0` (terminal text)
- **UI Layout:** Terminal/CLI interface, dark background, monospace text, command-line interactions
- **Key Visual Elements:** `claude` command prompt, terracotta-colored status indicators, tool use output blocks, cost counter, permission prompts (Allow/Deny)
- **Default `image_source`:** `frame-extract` or `canvas-build`

### GitHub Copilot
- **Primary Colors:** `#000000` (black), `#6E40C9` (purple), `#79C0FF` (light blue)
- **UI Layout:** VS Code integration, ghost text suggestions in editor, Copilot chat sidebar
- **Key Visual Elements:** Copilot logo (two-toned glasses/pilot), ghost text in gray, inline suggestion acceptance (Tab), chat panel with "@workspace" mentions
- **Default `image_source`:** `canvas-build`

### Codex (OpenAI)
- **Primary Colors:** `#10A37F` (OpenAI green), `#1E1E1E` (dark bg), `#FFFFFF` (white)
- **UI Layout:** Cloud-based coding agent interface, task-driven UI with sandboxed environments
- **Key Visual Elements:** OpenAI branding, task cards, terminal output panels, file tree sidebar
- **Default `image_source`:** `canvas-build`

### Aider
- **Primary Colors:** `#00D4AA` (green), `#1A1A2E` (terminal dark bg), `#E0E0E0` (text)
- **UI Layout:** Terminal-based pair programming, dark CLI, git-aware diff output
- **Key Visual Elements:** `aider` command prompt, green accent text, inline diff display (red/green), model selection indicator
- **Default `image_source`:** `frame-extract`

---

## Automation Platforms

### n8n
- **Primary Colors:** `#FF6D5A` (coral/orange-red), `#1A1A1A` (dark canvas bg), `#FFFFFF` (white node bg)
- **UI Layout:** Node-based workflow canvas, left sidebar with node types, dark background with white node cards connected by lines
- **Key Visual Elements:** Orange-red n8n logo (stacked squares), draggable workflow nodes with icons, colored connection lines between nodes, execution status indicators (green check/red x), sticky notes on canvas
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Zapier
- **Primary Colors:** `#FF4F00` (orange), `#1A1A1A` (dark), `#FFFFFF` (white bg)
- **UI Layout:** Linear step-by-step "Zap" builder, vertical flow with trigger → action cards
- **Key Visual Elements:** Orange Zapier lightning bolt logo, step cards with app icons, trigger/action flow arrows, "Zap" terminology
- **Default `image_source`:** `canvas-build`

### Make (Integromat)
- **Primary Colors:** `#6D00CC` (purple), `#1A1A2E` (dark bg), `#FFFFFF` (white)
- **UI Layout:** Circular node-based canvas (unique bubble/module design), purple accents
- **Key Visual Elements:** Purple Make logo, circular modules connected by lines, operation counters on connections, scenario builder
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Power Automate
- **Primary Colors:** `#0066FF` (blue), `#FFFFFF` (white bg), `#F3F2F1` (light gray)
- **UI Layout:** Microsoft Fluent UI, vertical flow designer, card-based steps
- **Key Visual Elements:** Blue Power Automate logo (flow arrows), Microsoft 365 integration icons, condition branches, approval steps
- **Default `image_source`:** `canvas-build`

---

## Dev Tools

### VS Code
- **Primary Colors:** `#007ACC` (blue), `#1E1E1E` (dark bg), `#252526` (sidebar), `#D4D4D4` (text)
- **UI Layout:** Editor with file explorer sidebar, bottom terminal panel, top tab bar, activity bar (left icon strip)
- **Key Visual Elements:** Blue VS Code logo, file explorer tree, syntax-highlighted code, integrated terminal, extensions sidebar, minimap on right edge
- **Default `image_source`:** `frame-extract`

### GitHub
- **Primary Colors:** `#24292E` (dark), `#FFFFFF` (white), `#2EA44F` (green button), `#0969DA` (link blue)
- **UI Layout:** Repository page with file tree, README display, top navigation (Code/Issues/Pull requests/Actions)
- **Key Visual Elements:** GitHub Octocat logo, green "Code" button, PR/issue badges, contribution graph (green squares), repository cards
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Vercel
- **Primary Colors:** `#000000` (black), `#FFFFFF` (white), `#0070F3` (blue accent)
- **UI Layout:** Minimal dark dashboard, deployment cards with status indicators, domain management
- **Key Visual Elements:** Vercel triangle logo (black), deployment status (green/red dots), preview URLs, framework detection badges (Next.js, etc.)
- **Default `image_source`:** `canvas-build`

### Supabase
- **Primary Colors:** `#3ECF8E` (green), `#1C1C1C` (dark bg), `#FFFFFF` (white)
- **UI Layout:** Dashboard with left sidebar navigation, table editor, SQL editor panel, dark theme
- **Key Visual Elements:** Green Supabase logo (abstract database icon), table editor grid, SQL editor with syntax highlighting, realtime listeners panel, auth user management
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Docker
- **Primary Colors:** `#2496ED` (blue), `#FFFFFF` (white), `#0F172A` (dark)
- **UI Layout:** Docker Desktop dashboard with container list, image management, terminal logs
- **Key Visual Elements:** Blue Docker whale logo (with containers on back), container status indicators, image layers visualization, Docker Compose file view
- **Default `image_source`:** `fetch-logo`

### Terraform
- **Primary Colors:** `#7B42BC` (purple), `#FFFFFF` (white), `#1A1A2E` (dark)
- **UI Layout:** HCL code in editor, plan/apply terminal output, state visualization
- **Key Visual Elements:** Purple Terraform logo (stacked hexagons), `terraform plan` output, resource graph visualization, HashiCorp branding
- **Default `image_source`:** `fetch-logo`

### Postman
- **Primary Colors:** `#FF6C37` (orange), `#FFFFFF` (white bg), `#212121` (dark text)
- **UI Layout:** API request builder with method selector (GET/POST), URL bar, tabbed response panel, collection sidebar
- **Key Visual Elements:** Orange Postman rocket logo, HTTP method badges (green GET, blue POST, etc.), JSON response viewer, collection folders
- **Default `image_source`:** `frame-extract` or `canvas-build`

---

## Platforms

### YouTube
- **Primary Colors:** `#FF0000` (red), `#FFFFFF` (white), `#0F0F0F` (dark bg)
- **UI Layout:** Video player with recommendation sidebar, channel page with video grid, Studio dashboard
- **Key Visual Elements:** Red play button logo, subscriber count, video thumbnails with duration badges, like/dislike buttons, comment section
- **Default `image_source`:** `frame-extract` or `canvas-build`

### LinkedIn
- **Primary Colors:** `#0A66C2` (blue), `#FFFFFF` (white bg), `#000000` (text)
- **UI Layout:** Feed with post cards, profile page with banner/headshot, messaging panel
- **Key Visual Elements:** Blue LinkedIn "in" logo, profile cards with headshot + title, post engagement metrics (likes/comments), connection badges
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Twitter / X
- **Primary Colors:** `#000000` (black), `#FFFFFF` (white), `#1D9BF0` (legacy blue), `#F7F9F9` (light bg)
- **UI Layout:** Feed with tweet cards, left sidebar navigation, trending panel right side
- **Key Visual Elements:** X logo (or legacy bird), tweet cards with engagement metrics, verified checkmarks, reply threads, quote tweets
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Slack
- **Primary Colors:** `#4A154B` (aubergine/purple), `#36C5F0` (blue), `#2EB67D` (green), `#ECB22E` (yellow), `#E01E5A` (pink)
- **UI Layout:** Left sidebar (workspace/channels list), main message area, thread panel on right
- **Key Visual Elements:** Slack hashtag logo (multi-colored), channel names with # prefix, message threads, emoji reactions, app integrations sidebar
- **Default `image_source`:** `canvas-build`

### Notion
- **Primary Colors:** `#000000` (black), `#FFFFFF` (white), `#F7F6F3` (warm gray bg)
- **UI Layout:** Clean page editor with sidebar navigation, block-based content, database views
- **Key Visual Elements:** Notion logo (stylized "N"), page icons (emoji), toggle blocks, database tables/boards/galleries, breadcrumb navigation, slash command menu
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Discord
- **Primary Colors:** `#5865F2` (blurple), `#23272A` (dark bg), `#2C2F33` (darker), `#FFFFFF` (white)
- **UI Layout:** Server list (left icon strip), channel list, main chat area, member list (right)
- **Key Visual Elements:** Discord logo (game controller face), server icons, voice channel indicators, role-colored usernames, embed cards
- **Default `image_source`:** `canvas-build`

### Reddit
- **Primary Colors:** `#FF4500` (orange-red), `#FFFFFF` (white), `#1A1A1B` (dark bg), `#DAE0E6` (light bg)
- **UI Layout:** Feed with post cards, subreddit sidebar, voting arrows
- **Key Visual Elements:** Reddit Snoo mascot, upvote/downvote arrows, subreddit banners, comment threads with indentation, award icons
- **Default `image_source`:** `canvas-build`

---

## AI Infrastructure

### Hugging Face
- **Primary Colors:** `#FFD21E` (yellow), `#000000` (black), `#FFFFFF` (white)
- **UI Layout:** Model/dataset hub with search, model cards with metrics, Spaces gallery
- **Key Visual Elements:** Yellow Hugging Face emoji logo (🤗 style), model cards with download counts, dataset viewers, Spaces app thumbnails, leaderboard tables
- **Default `image_source`:** `canvas-build`

### Replicate
- **Primary Colors:** `#000000` (black), `#FFFFFF` (white), `#3B82F6` (blue accent)
- **UI Layout:** Model playground with input/output panels, API code snippets, model gallery
- **Key Visual Elements:** Replicate logo, model prediction interface, API code examples, output image/video previews
- **Default `image_source`:** `canvas-build`

### Together AI
- **Primary Colors:** `#6366F1` (indigo), `#000000` (black bg), `#FFFFFF` (white)
- **UI Layout:** API playground, model selection, inference dashboard
- **Key Visual Elements:** Together AI logo, model benchmarking charts, API endpoint cards, inference speed metrics
- **Default `image_source`:** `fetch-logo`

### Groq
- **Primary Colors:** `#F55036` (red-orange), `#000000` (black bg), `#FFFFFF` (white)
- **UI Layout:** Minimal playground interface, speed-focused metrics display
- **Key Visual Elements:** Groq logo, inference speed counters (tokens/sec), LPU branding, model selector
- **Default `image_source`:** `canvas-build`

### OpenRouter
- **Primary Colors:** `#6366F1` (indigo), `#1E1B4B` (dark purple bg), `#FFFFFF` (white)
- **UI Layout:** Model marketplace, unified API dashboard, pricing comparison tables
- **Key Visual Elements:** OpenRouter logo, model comparison cards, pricing per million tokens, provider badges
- **Default `image_source`:** `fetch-logo`

### LangChain
- **Primary Colors:** `#1C3C3C` (dark teal), `#65E89D` (green), `#FFFFFF` (white)
- **UI Layout:** Documentation site, LangSmith tracing dashboard with trace trees
- **Key Visual Elements:** LangChain parrot logo, chain/graph visualizations, LangSmith trace waterfall, node-based LCEL diagrams
- **Default `image_source`:** `fetch-logo`

### LangGraph
- **Primary Colors:** `#1C3C3C` (dark teal), `#65E89D` (green), `#FFFFFF` (white)
- **UI Layout:** Graph visualization of agent workflows, state machine diagrams
- **Key Visual Elements:** LangGraph logo, directed graph visualizations with nodes and edges, state annotations, conditional branching arrows
- **Default `image_source`:** `canvas-build`

---

## AI Coding & Agent Platforms

### Replit
- **Primary Colors:** `#F26207` (orange), `#0E1525` (dark bg), `#FFFFFF` (white)
- **UI Layout:** Browser-based IDE with file tree, editor, console, and AI chat panel
- **Key Visual Elements:** Orange Replit logo (play button), browser-based editor, Replit Agent chat, deployment URL preview, multiplayer cursors
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Bolt.new
- **Primary Colors:** `#1389FD` (blue), `#0F172A` (dark bg), `#FFFFFF` (white)
- **UI Layout:** AI chat on left, live app preview on right, file tree
- **Key Visual Elements:** Bolt logo (lightning bolt), split-pane chat + preview, StackBlitz integration, "Deploy" button
- **Default `image_source`:** `canvas-build`

### Lovable
- **Primary Colors:** `#9B59B6` (purple), `#1A1A2E` (dark bg), `#FFFFFF` (white)
- **UI Layout:** AI chat with live app preview, component-based UI generation
- **Key Visual Elements:** Lovable logo (heart), chat interface, live preview panel, Supabase integration badges
- **Default `image_source`:** `canvas-build`

### v0 (Vercel)
- **Primary Colors:** `#000000` (black), `#FFFFFF` (white), `#0070F3` (Vercel blue)
- **UI Layout:** Prompt input at top, generated UI component preview below, code panel
- **Key Visual Elements:** v0 logo, component preview cards, "Open in v0" badges, shadcn/ui component style, iterative prompt refinement
- **Default `image_source`:** `canvas-build`

---

## Data & Analytics

### Jupyter Notebook
- **Primary Colors:** `#F37626` (orange), `#FFFFFF` (white bg), `#E8E8E8` (cell borders)
- **UI Layout:** Vertical notebook with code cells, markdown cells, output cells, toolbar at top
- **Key Visual Elements:** Jupyter logo (three circles), numbered code cells `In [1]:`, output cells `Out [1]:`, kernel status indicator, cell type selector
- **Default `image_source`:** `frame-extract` or `canvas-build`

### Streamlit
- **Primary Colors:** `#FF4B4B` (red), `#FFFFFF` (white bg), `#262730` (dark theme)
- **UI Layout:** Single-page web app with sidebar controls, main content area with charts/widgets
- **Key Visual Elements:** Streamlit logo (red S), sidebar with sliders/inputs, data tables, Plotly/Matplotlib charts, "Made with Streamlit" badge
- **Default `image_source`:** `frame-extract`

---

## Cloud & Infrastructure

### AWS
- **Primary Colors:** `#232F3E` (dark navy), `#FF9900` (orange), `#FFFFFF` (white)
- **UI Layout:** AWS Console with service search bar, resource dashboards, region selector
- **Key Visual Elements:** AWS logo (orange smile arrow), service icons (Lambda, S3, EC2), console breadcrumbs, CloudWatch graphs
- **Default `image_source`:** `canvas-build`

### Google Cloud (GCP)
- **Primary Colors:** `#4285F4` (blue), `#EA4335` (red), `#FBBC04` (yellow), `#34A853` (green), `#FFFFFF` (white)
- **UI Layout:** Google Cloud Console with left nav, project selector, resource dashboards
- **Key Visual Elements:** Google Cloud logo (colored hexagon), project selector dropdown, service cards, Cloud Shell terminal
- **Default `image_source`:** `canvas-build`

### Cloudflare
- **Primary Colors:** `#F38020` (orange), `#FFFFFF` (white), `#1B1B1B` (dark)
- **UI Layout:** Dashboard with analytics graphs, DNS management table, Workers editor
- **Key Visual Elements:** Cloudflare logo (orange cloud with rays), analytics timeline graphs, DNS record table, Workers code editor
- **Default `image_source`:** `canvas-build`

---

## Usage Instructions

### For Storyboard (step-02 / step-03)
When creating MG briefs for Type B, C, or D that reference a named tool:
1. Look up the tool in this reference
2. `Default image_source` is **MANDATORY** — use it unless there's a specific reason not to
3. For Type C (UI mockup): `image_source` **MUST** be `frame-extract` or `web-screenshot` — these types require a visual reference to produce recognizable tool interfaces
4. `image_source: none` is **ONLY** acceptable for Type A (text overlays), Type E (sequential reveals), and Type F (stylized B-roll)
5. Include the tool's primary hex codes in the brief
6. Describe the recognizable UI layout elements
7. Add `tool_name` and `tool_visual_details` fields to the MG entry

**Reference image resolution:** Use `scripts/resolve-reference-image.ts` to automatically resolve the best reference image through the 3-tier waterfall (frame-extract → web-screenshot → logo).

### For Hera Generation (step-02)
When building Hera API prompts for tool-referencing MGs:
1. Look up the tool in this reference
2. Inject specific colors, UI elements, and layout into the prompt
3. For Type C: describe the exact UI being recreated (sidebar color, layout, key elements)
4. For Type B: use the tool's primary color for glow/accent effects
5. For Type D: style diagram elements using the tool's visual language

### Adding New Tools
Add entries following the same format:
- **Primary Colors:** hex codes
- **UI Layout:** one-line spatial description
- **Key Visual Elements:** 3-5 instantly recognizable features
- **Default `image_source`:** recommendation
