---
name: 'step-02b-idea-search'
description: 'Search YouTube for existing content matching the users video idea and assess competitive landscape'

nextStepFile: './step-02c-niche-scan.md'
outputFile: '{output_path}/competitive-research-{date}.md'
youtubeApiReference: '../data/youtube-api-reference.md'
---

# Step 2b: Idea Validation — Competitive Search

## STEP GOAL:

To search YouTube for existing content that matches the user's video idea, assess competition density and performance metrics, identify top performers on this topic, and calculate how the idea maps against current outlier patterns.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a competitive intelligence analyst assessing market viability for a specific content idea
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in content market analysis and competitive positioning
- ✅ This step is prescriptive — follow the data-gathering sequence exactly

### Step-Specific Rules:

- 🎯 Focus ONLY on searching for and analysing existing content related to the user's video idea
- 🚫 FORBIDDEN to make content recommendations yet — that comes in later steps
- 💬 Use the video idea captured in step-01 as the search basis
- 📋 Generate multiple search queries from the video idea to ensure comprehensive coverage

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append competitive landscape findings to {outputFile}
- 📖 Update output frontmatter stepsCompleted when complete
- 🚫 FORBIDDEN to skip search or use estimated data

## CONTEXT BOUNDARIES:

- Available: User's video idea (from step-01 frontmatter), YouTube MCP (`mcp__youtube__*`) — platform-level, no API key needed, competitor list from sidecar
- Focus: Searching for existing content on the user's topic and assessing competition
- Limits: Do not analyse transcripts, identify gaps, or make recommendations yet
- Dependencies: Step 01 must have completed with videoIdea captured, YouTube MCP must be validated

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load API Reference and Extract Search Queries

Load and read {youtubeApiReference} for correct API call formats, parameter names, and quota management. This file contains exact endpoint URLs and known pitfalls — follow it precisely.

From the user's video idea (stored in output frontmatter `videoIdea`), generate 3-5 search queries:

- The exact topic/title as stated
- Broader keyword variations
- Niche-specific variations within the AI/tech education space
- Alternative phrasings a viewer might search for

Display: "**Searching YouTube for content related to your idea...**"
List the search queries being used.

### 2. Search YouTube

For each search query, follow the API reference in {youtubeApiReference}:

1. **Search for videos** — use `mcp__youtube__searchVideos` with `query: QUERY, maxResults: 25` to retrieve top results per query.
2. **For each result, fetch full statistics** — collect all video IDs from search results and batch them into `mcp__youtube__getVideoDetails` calls (up to 50 IDs per call):
   - Video title, video ID, channel name, channel ID
   - View count, like count, comment count
   - Published date, video duration
   - For channel subscriber counts, batch unique channel IDs into `mcp__youtube__getChannelStatistics`

3. **De-duplicate** results across queries (same video ID appearing in multiple searches)

### 3. Assess Competition Density

From the search results, calculate:

1. **Total unique videos** found on this topic
2. **Competition density score:**
   - Low (< 20 relevant videos with 1K+ views) — opportunity space
   - Medium (20-50 relevant videos) — competitive but viable
   - High (50+ relevant videos) — saturated, needs strong differentiation
3. **Recency:** How many videos were published in the last 30/60/90 days
4. **Channel size distribution:** How many results come from small vs medium vs large channels

### 4. Identify Top Performers

From the search results:

1. **Rank videos by view count** — identify the top 10 performers
2. **Calculate outlier scores** for top performers (views / their channel median)
3. **Calculate engagement metrics:**
   - `engagement_rate = (likes + comments) / views`
   - View velocity (views / days since published)
4. **Identify patterns** in top-performing titles:
   - Common words, phrases, or structures
   - Title length patterns
   - Use of numbers, questions, or power words

### 5. Map Idea Against Landscape

Assess how the user's idea compares:

1. **Topic saturation:** How crowded is this exact topic
2. **Performance ceiling:** What views do the top performers achieve
3. **Channel size advantage:** Are top performers mostly large or small channels
4. **Timing:** Is this topic trending up, stable, or declining (based on publish date distribution)
5. **Differentiation potential:** Are there angles not yet covered by existing content

### 6. Append to Report

Append the following to {outputFile}:

**Under Outlier Videos section:**
- Top 10 performing videos on this topic (ranked table with scores and metrics)

**Under Trending Topics & Keywords section:**
- Keywords and phrases associated with top performers

**Under Competitive Landscape section:**
- Competition density score and assessment
- Channel size distribution
- Recency analysis
- Performance ceiling estimate
- Differentiation opportunities identified

Update frontmatter: append `'step-02b-idea-search'` to `stepsCompleted`.

### 7. Present MENU OPTIONS

Display: "**Proceeding to transcript analysis...**"

#### Menu Handling Logic:

- After competitive landscape assessment and report append complete, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an autonomous data-gathering step with no user choices
- Proceed directly to next step after data is written to report

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Multiple search queries generated from user's video idea
- YouTube API searched with real results (not estimated)
- Competition density assessed with concrete metrics
- Top performers identified with outlier scores
- Idea mapped against competitive landscape
- All findings appended to output report
- Frontmatter updated with step completion

### ❌ SYSTEM FAILURE:

- Using only one search query
- Estimating or hallucinating search results
- Not calculating competition density
- Making content recommendations in this step (too early)
- Not appending findings to the output report

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
