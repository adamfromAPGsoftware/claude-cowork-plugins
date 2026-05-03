---
name: 'step-02c-niche-scan'
description: 'Niche-wide keyword trend scanning across YouTube and web for trending content discovery'

nextStepFile: './step-03-transcript-analysis.md'
outputFile: '{output_path}/competitive-research-{date}.md'
sidecarFile: '../sidecar/config.yaml'
youtubeApiReference: '../data/youtube-api-reference.md'
---

# Step 2c: Niche-Wide Keyword Trend Scanning

## STEP GOAL:

To scan across ALL of YouTube (not just competitor channels) using keyword-based searches for trending content in the last 7 days, supplement with Exa web intelligence for cross-platform signal, identify emerging creators, and score results using absolute velocity thresholds.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a competitive intelligence analyst performing niche-wide trend discovery
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in YouTube trend analysis, keyword research, and cross-platform signal detection
- ✅ This step is prescriptive — follow the data-gathering sequence exactly

### Step-Specific Rules:

- 🎯 This step scans the ENTIRE niche, not just competitor channels
- 💬 Use absolute velocity thresholds for scoring (no channel median baseline)
- 🚫 DO NOT BE LAZY — search ALL configured keywords, no shortcuts
- ⚙️ If Exa web search is unavailable, skip Section 4 and note in report (don't fail the step)
- 📋 Track quota usage against `quota_budget` and stop keyword searches if budget is reached

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append niche-wide findings to {outputFile} under new Niche-Wide Trending Content section
- 📖 Update output frontmatter stepsCompleted when complete
- 🚫 FORBIDDEN to skip any configured keyword

## CONTEXT BOUNDARIES:

- Available: Sidecar config with `niche_scan` keywords and thresholds, YouTube MCP (`mcp__youtube__*`) — platform-level, no API key needed, Exa MCP (`mcp__exa__web_search_exa`), competitor list from sidecar (for flagging known vs new creators)
- Focus: Niche-wide keyword-based trend discovery and cross-platform signal detection
- Limits: Do not analyse transcripts or identify gaps — that comes in later steps
- Dependencies: Step 01 must have completed, step 02a or 02b must have completed, sidecar must be loaded, YouTube MCP must be validated

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Config & Calculate Date Window

Load and read {youtubeApiReference} for correct API call formats, parameter names, and quota management.

Load the sidecar config and extract:
- `niche_scan.keywords` — the keyword list to search
- `niche_scan.timeframe_days` — the lookback window (default: 7)
- `niche_scan.scoring` — velocity thresholds (`velocity_super`, `velocity_strong`, `velocity_standard`, `min_views`, `max_results_per_keyword`)
- `niche_scan.exa_queries` — web intelligence search queries
- `niche_scan.quota_budget` — max quota units for this step
- `competitors` — the known competitor channel list (for flagging new vs known creators)

Calculate `publishedAfter` = today minus `timeframe_days` in ISO 8601 format (e.g., `2026-03-10T00:00:00Z`).

**Validation:** If `niche_scan.enabled` is false or `niche_scan.keywords` is empty, display a warning and skip to {nextStepFile}:

"**Niche scan is disabled or has no keywords configured.** Skipping niche-wide scanning. To enable, update `sidecar/config.yaml` with `niche_scan.keywords`."

Display: "**Scanning niche-wide trends across {N} keywords (last {timeframe_days} days)...**"

### 2. YouTube Keyword Search

For each keyword in `niche_scan.keywords`:

1. **Search YouTube** — use `mcp__youtube__searchVideos` with:
   - `query: keyword`
   - `maxResults: max_results_per_keyword` (default: 25)

2. **Collect all video IDs** across all keyword searches

3. **De-duplicate video IDs** — a video may appear in multiple keyword results. Track which keywords matched each video.

4. **Batch fetch video statistics** — use `mcp__youtube__getVideoDetails` with batched video IDs (up to 50 per call)

5. **Batch fetch channel statistics** — collect unique channel IDs from results and call `mcp__youtube__getChannelStatistics` with batched channel IDs. Extract subscriber counts.

6. **Filter** — remove videos below `min_views` threshold

Display running quota usage: "**Quota used: {used}/{budget}**"

### 3. Niche-Wide Scoring

Since there is no channel median baseline, use a **composite niche trend score** based on absolute thresholds:

```
niche_trend_score = (view_velocity_norm × 0.40)
                  + (engagement_rate_norm × 0.25)
                  + (recency_boost × 0.20)
                  + (small_channel_bonus × 0.15)
```

**Component calculations:**

1. **View Velocity** = `views / days_since_publish`
   - Normalize against config thresholds: 500/day = 3, 3000/day = 7, 10000+/day = 10
   - Linear interpolation between tiers
   - Assign velocity tier label: **Super** (10K+/day), **Strong** (3K+/day), **Standard** (500+/day)

2. **Engagement Rate** = `(likes + comments) / views`
   - Normalize: 1% = 3, 3% = 7, 5%+ = 10
   - Linear interpolation between tiers

3. **Recency Boost** = linear scale based on publish date
   - Published today = 10
   - Published 7 days ago = 1
   - Linear interpolation between

4. **Small Channel Bonus** = inverse of subscriber count (rewards smaller channels going viral)
   - < 10K subs = 10
   - 10K-50K subs = 7
   - 50K-200K subs = 4
   - 200K+ subs = 1

**Flag "New Creator"** if the video's channel is NOT in the competitor list from sidecar config.

**Rank all videos** by `niche_trend_score` (highest first).

### 4. Exa Web Intelligence

For each query in `niche_scan.exa_queries`:

1. **Search using `mcp__exa__web_search_exa`** with a 7-day date filter
2. **Extract trending topics** from blogs, news, forums, and social media results

Cross-reference web results with YouTube keyword search results:

- **Convergent** = topic trending on BOTH YouTube and web → strongest signal
- **YouTube-only** = trending on YouTube but not web → possibly algorithm-boosted
- **Web-only** = trending on web but NOT yet on YouTube → early-mover opportunity

Build a **Cross-Platform Signal Map** with each topic categorised.

**Fallback:** If Exa MCP tools are unavailable or any query fails:
- Skip the failed queries and continue with available results
- Note in the report: "Exa web intelligence partially/fully unavailable — cross-platform analysis limited to YouTube data"
- DO NOT fail the step — web intelligence is supplementary

### 5. Identify Emerging Creators

From the niche-wide results, identify channels that:

1. Are **NOT** in the competitor list (new/unknown creators)
2. Have **multiple** videos in the niche-wide results (not a one-hit wonder)
3. Have at least one video with **Strong or Super** velocity tier

Flag these as **"Emerging Creators to Watch"** with:
- Channel name and subscriber count
- Number of trending videos found
- Best-performing video title and velocity tier
- Primary topic focus (based on video titles)

### 6. Append to Report & Continue

Append to {outputFile}:

**Add new section — Niche-Wide Trending Content (between Outlier Videos and Trending Topics):**

- **Top Trending Videos** — ranked table with: Rank, Video Title, Channel, Subs, Views, Views/Day, Engagement Rate, Velocity Tier, Published Date
- **Cross-Platform Signal Map** — table with: Topic, YouTube Signal, Web Signal, Convergence type, Opportunity assessment
- **Emerging Creators to Watch** — list of non-competitor channels with high-velocity niche content

**Update Trending Topics & Keywords section:**
- Add niche-wide keyword frequency data alongside competitor outlier topics

**Update output frontmatter:**
- Append `'step-02c-niche-scan'` to `stepsCompleted`
- Add `niche_scan_keywords_used: [list of keywords searched]`
- Add `niche_scan_timeframe_days: {timeframe_days}`
- Add `niche_scan_videos_found: {count}`

Display: "**Proceeding to transcript analysis...**"

#### Menu Handling Logic:

- After niche-wide scan and report append complete, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an autonomous data-gathering step with no user choices
- Proceed directly to next step after data is written to report

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All configured keywords searched (or quota budget reached with clear logging)
- Videos scored using composite niche trend score formula
- Velocity tiers assigned (Super/Strong/Standard)
- Cross-platform signal map generated (or Exa unavailability noted)
- Emerging creators identified and flagged
- New Creator flag applied to non-competitor channels
- All findings appended to output report under Niche-Wide Trending Content section
- Quota usage tracked and logged
- Frontmatter updated with step completion and niche scan metadata

### ❌ SYSTEM FAILURE:

- Skipping configured keywords without hitting quota budget
- Using hardcoded or estimated metrics instead of real API data
- Not scoring with the composite formula (using ad-hoc scoring instead)
- Failing the step because Exa is unavailable (should gracefully degrade)
- Not tracking quota usage
- Not flagging new vs known creators
- Not appending findings to the output report
- Analysing transcripts or gaps in this step (wrong step)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
