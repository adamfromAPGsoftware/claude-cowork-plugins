---
name: 'step-04-gap-insights'
description: 'Identify content gaps, supplement with web trend context, and generate actionable opportunity insights'

nextStepFile: './step-05-checkpoint.md'
outputFile: '{output_path}/competitive-research-{date}.md'
---

# Step 4: Gap Identification & Insights

## STEP GOAL:

To cross-reference outlier data and transcript analysis against coverage density, supplement with broader web trend context, identify content gaps (high demand + low coverage), and generate actionable opportunity insights with scores.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a content strategist synthesising data into actionable insights
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in market gap analysis, trend forecasting, and opportunity scoring
- ✅ This step is intent-based — interpret patterns and generate strategic insights

### Step-Specific Rules:

- 🎯 Focus on gap identification, web trend supplementation, and opportunity scoring
- 🚫 FORBIDDEN to make final recommendations — that's the user's job at checkpoint
- 💬 Use web-browsing (Exa or equivalent) for broader trend context
- 📋 Generate opportunity scores that combine demand signals with competition levels

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append gap analysis and insights to {outputFile} under Content Gap Opportunities section
- 📖 Update output frontmatter stepsCompleted when complete
- 🚫 FORBIDDEN to skip web trend research

## CONTEXT BOUNDARIES:

- Available: Outlier data (step 2), transcript insights (step 3), web search tools
- Focus: Synthesising all prior data into gap analysis and opportunities
- Limits: Present findings objectively — don't make final recommendations yet
- Dependencies: Steps 2 and 3 must have completed

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Prior Findings

Read {outputFile} to load:
- Outlier videos with scores and metrics (from step 2a/2b)
- Niche-wide trending content with velocity tiers and cross-platform signals (from step 2c)
- Trending topics and keywords (from steps 2a/2b and 2c)
- Transcript analysis patterns (from step 3)

Extract the key topics and themes identified so far from BOTH competitor outlier and niche-wide datasets.

### 2. Content Gap Analysis

Cross-reference outlier topics against coverage density, incorporating both competitor and niche-wide data:

1. **For each major topic/theme identified in outliers and niche-wide trends:**
   - How many videos cover this topic (from step 2 search data)?
   - What's the average performance of videos on this topic?
   - Is demand (outlier performance) high relative to supply (number of videos)?
   - **Cross-reference competitor outliers vs niche-wide trends:** A topic trending niche-wide but NOT covered by any competitor channels is a stronger gap signal

2. **Classify each topic:**
   - **Hot Gap** — High outlier scores + low video count = strong opportunity
   - **Emerging** — Recent outliers trending up + moderate coverage = timing opportunity
   - **Saturated** — High video count + declining outlier performance = avoid or differentiate
   - **Niche Gold** — Small outlier with unusually high score from small channel = underserved niche

3. **For Idea Validation mode additionally:**
   - Where does the user's idea fall in this classification?
   - What gaps exist within the user's topic that they could exploit?

### 3. Web Trend Supplementation

Leverage Exa web intelligence data already gathered in step 2c (cross-platform signal map). Only run **additional** Exa searches for topics that were surfaced AFTER the niche scan (e.g., new themes from transcript analysis in step 3):

1. **From step 2c cross-platform signal map, review:**
   - **Convergent** topics (trending on both YouTube + web) = strongest signal
   - **YouTube-only** topics = possibly algorithm-boosted
   - **Web-only** topics = early-mover opportunity (not yet on YouTube)

2. **Run additional Exa searches ONLY for new topics** not already covered in step 2c:
   - "{new_topic_from_step3} trend" — topics surfaced from transcript analysis
   - "{niche} trends {current_year}" — if not already covered by step 2c queries

3. **From all web results (step 2c + new), extract:**
   - Industry trends that align with identified outlier topics
   - Emerging topics not yet reflected in YouTube content
   - Seasonal or event-driven trends that could affect timing
   - Platform-wide shifts (algorithm changes, format preferences)

4. **Correlate web trends with YouTube data:**
   - Topics trending on web AND showing YouTube outliers = strong signal
   - Topics trending on web but NOT yet on YouTube = early-mover opportunity
   - Topics with YouTube outliers but no web trend = may be platform-specific

### 4. Generate Opportunity Scores

For each identified opportunity, calculate a composite score:

**Opportunity Score = (Demand Signal × 0.30) + (Competition Gap × 0.25) + (Trend Momentum × 0.20) + (Niche Fit × 0.10) + (Niche-Wide Signal × 0.15)**

Where:
- **Demand Signal** (1-10): Based on outlier scores and view counts from competitor scan
- **Competition Gap** (1-10): Inverse of coverage density (fewer videos = higher score)
- **Trend Momentum** (1-10): Based on recency of outliers and web trend alignment
- **Niche Fit** (1-10): How well the topic fits the AI/tech education space
- **Niche-Wide Signal** (1-10): Based on niche-wide data from step 2c — high velocity videos from non-competitor channels on this topic score higher; convergent cross-platform signal (YouTube + web) scores highest. If niche scan was skipped, default this component to 5 (neutral)

Rank opportunities by composite score.

### 5. Append to Report

Append the following to {outputFile} under the **Content Gap Opportunities** section:

- Gap classification table: Topic, Classification (Hot Gap/Emerging/Saturated/Niche Gold), Demand Signal, Competition Level
- Top 5 opportunities ranked by opportunity score with rationale
- Web trend context: key broader trends and how they relate to YouTube findings
- (Validation mode) Updated competitive landscape assessment with gap context

Update the **Trending Topics & Keywords** section with any new topics surfaced from web research.

Update frontmatter: append `'step-04-gap-insights'` to `stepsCompleted`.

### 6. Present MENU OPTIONS

Display: "**Proceeding to checkpoint for your review...**"

#### Menu Handling Logic:

- After gap analysis and report append complete, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an autonomous analysis step with no user choices
- Proceed directly to next step after findings are written to report

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Content gaps identified and classified
- Web trend research performed (not skipped)
- YouTube data correlated with broader web trends
- Opportunity scores calculated with transparent methodology
- Opportunities ranked and presented with rationale
- All findings appended to output report
- Frontmatter updated with step completion

### ❌ SYSTEM FAILURE:

- Skipping web trend research
- Generating opportunity scores without real data backing
- Making final recommendations (user steers emphasis at checkpoint)
- Not classifying gaps (just listing topics without analysis)
- Not appending findings to the output report

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
