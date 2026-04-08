# Content Plugin Setup

## Prerequisites

- Node.js 18+ and Python 3.10+ installed
- Claude Code CLI installed and authenticated
- Access to the `_bmad/ccs/` shared infrastructure (config, data, workflows)

## API Credentials

### 1. YouTube Data API (Content Strategist)

Used for competitive research — scanning competitor channels, fetching video metrics, pulling transcripts.

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a project or select existing
3. Enable "YouTube Data API v3"
4. Create an API Key
5. Add to `.env` as `YOUTUBE_API_KEY`

### 2. Late.dev API (Publisher)

Used for scheduling and publishing content across 13+ social platforms.

1. Sign up at [late.dev](https://getlate.dev)
2. Connect your social accounts (LinkedIn, X, Instagram, TikTok, YouTube, etc.)
3. Go to Settings > API
4. Generate an API key (format: `sk_` + 64 hex chars)
5. Add to `.env` as `LATE_API_KEY`

### 3. Gemini API (Creative Director)

Used for thumbnail generation with identity preservation and image generation.

1. Go to [AI Studio](https://aistudio.google.com/apikey)
2. Create an API key
3. Add to `.env` as `GEMINI_API_KEY`

### 4. Supabase (Copywriter — Blog Publishing)

Used for uploading media and publishing blog posts.

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project > Settings > API
3. Copy the project URL and anon key
4. Add to `.env` as `SUPABASE_URL` and `SUPABASE_ANON_KEY`

## Python Dependencies

```bash
pip install youtube-transcript-api pytrends google-generativeai
```

## Node Dependencies (LinkedIn Comment Processor)

```bash
cd content-plugin/skills/5-publisher/workflows/linkedin-comment-processor
npm install
npx playwright install chromium
```

## First Run

Each agent will run its `init.md` setup on first activation, creating the memory sidecar structure. You will be prompted for configuration specific to each agent.

## Plugin Structure

```
content-plugin/
  agents/          5 agent definitions (persona, skills reference)
  skills/          5 skill directories (SKILL.md, capabilities, memory system)
  commands/        CLI commands (empty — future use)
  hooks/           Event hooks (empty — future use)
  references/      Shared reference documents (future use)
  scripts/         Shared utility scripts (future use)
```
