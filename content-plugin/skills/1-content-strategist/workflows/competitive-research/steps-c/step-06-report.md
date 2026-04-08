---
name: 'step-06-report'
description: 'Compile the final structured research report with user-steered emphasis and write to output path'

outputFile: '{output_path}/competitive-research-{date}.md'
---

# Step 6: Final Report Compilation

## STEP GOAL:

To compile all findings into a polished, structured competitive research report, applying the user's steering from the checkpoint to adjust emphasis, and write the final document to the output path.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a research analyst compiling a data-backed executive report
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in clear, concise analytical writing
- ✅ The final report should be scannable, actionable, and data-backed

### Step-Specific Rules:

- 🎯 Focus ONLY on compiling, polishing, and finalising the report
- 🚫 FORBIDDEN to gather new data or perform new analysis
- 💬 Apply user's steering from checkpoint to adjust section emphasis
- 📋 Ensure every claim is backed by the real metrics gathered in prior steps

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Rewrite {outputFile} as the final polished report
- 📖 Update output frontmatter to mark workflow complete
- 🚫 FORBIDDEN to hallucinate metrics — only use data from prior steps

## CONTEXT BOUNDARIES:

- Available: Complete output report with all findings and user steering from checkpoint
- Focus: Compilation, polish, and formatting only
- Limits: No new data gathering, no new analysis, no new API calls
- Dependencies: All prior steps must have completed, user steering captured

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load All Content

Read {outputFile} completely, including:
- All findings appended by steps 2-4
- User steering from step 5 checkpoint (priority_topics, deprioritised, deep_dive_requests)
- Mode (trend-discovery or idea-validation)

### 2. Compile Executive Summary

Write the **Executive Summary** section:

- 3-5 bullet points capturing the most important findings
- Lead with the user's priority topics
- Include the single most actionable insight
- State the mode and scope (niche, competitors analysed, timeframe)
- Keep it to 150 words maximum — this should be scannable in 30 seconds

### 3. Polish Outlier Videos Section & Niche-Wide Section

Refine the **Outlier Videos** section:

- Ensure the ranked table is clean and properly formatted
- Add brief commentary on the top 3-5 outliers explaining WHY they outperformed
- If user prioritised specific topics, highlight outliers in those areas
- If user deprioritised topics, keep those outliers in the table but don't expand commentary

Refine the **Niche-Wide Trending Content** section (if present from step 2c):

- Ensure the Top Trending Videos table is clean and properly formatted
- Add brief commentary on the top 3-5 niche-wide trending videos explaining what made them break out
- Ensure the Cross-Platform Signal Map is clear — highlight convergent topics as strongest signals
- Polish the Emerging Creators to Watch list — focus on actionable takeaways (what can be learned from these creators)
- If niche scan was skipped, note this briefly and move on

### 4. Polish Trending Topics Section

Refine the **Trending Topics & Keywords** section:

- Group keywords by theme/cluster
- Indicate trend direction (rising, stable, declining) where data supports it
- Highlight topics that align with user's priority areas
- Cross-reference with web trend data from step 4

### 5. Polish Transcript Insights Section

Refine the **Transcript Insights** section:

- Lead with the most actionable patterns (hooks that work, structures that retain)
- If user requested deep-dives on specific areas, expand those
- Include specific examples from transcripts (quotes or paraphrases)
- Keep each insight tied to a concrete data point

### 6. Polish Content Gap Opportunities Section

Refine the **Content Gap Opportunities** section:

- Lead with the top 3-5 opportunities ranked by opportunity score
- Expand coverage on user's priority topics
- For each opportunity, include: topic, opportunity score, demand signal, competition level, recommended angle
- Summarise or omit deprioritised areas

### 7. Polish Competitive Landscape Section (Validation Mode Only)

**If mode is idea-validation:**

Refine the **Competitive Landscape** section:

- Clear assessment of competition density for the user's idea
- Positioning recommendations based on transcript analysis and gap data
- Specific framing suggestions (title angles, hook approaches, differentiation strategies)
- Risk assessment: what could make this video underperform
- Opportunity assessment: what could make this video outperform

**If mode is trend-discovery:**

Remove or replace the Competitive Landscape section with:

"**Recommended Next Steps:**
- [Top 3 suggested video ideas based on gap analysis, each with a one-line rationale]"

### 8. Final Document Optimisation

Review the complete report for:

1. **Flow and coherence** — sections should build on each other logically
2. **Duplication** — remove repeated information across sections
3. **Proper ## Level 2 headers** — ensure consistent formatting
4. **Data integrity** — every metric cited must come from prior step data (no hallucination)
5. **Actionability** — every section should have a clear "so what" for the user
6. **Length** — aim for a report that can be read in 5-10 minutes

### 9. Finalise Output

Update {outputFile} with the polished report.

Update frontmatter:
- Append `'step-06-report'` to `stepsCompleted`
- Set `status: 'complete'`
- Set `completed_date` to current date

### 10. Present Completion Summary

"**Competitive Research Report Complete!**

**Report saved to:** `{outputFile}`

**Summary:**
- **Mode:** {mode}
- **Competitors analysed:** {N}
- **Videos scanned:** {total}
- **Outliers identified:** {count} ({super}x super, {strong}x strong, {standard}x standard)
- **Top opportunities:** {top 3 opportunity names}
- **Transcript insights from:** {N} videos

Your report is ready for review. Use it to inform your content ideation, or run the workflow again in validation mode to test a specific idea against the market."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Executive summary is concise and actionable (under 150 words)
- User's steering is reflected in section emphasis
- All metrics are real (from prior steps, not hallucinated)
- Report is scannable and well-formatted
- Competitive Landscape section is mode-appropriate
- Document is optimised for flow and readability
- Frontmatter marked as complete
- Completion summary presented to user

### ❌ SYSTEM FAILURE:

- Hallucinating metrics not gathered in prior steps
- Ignoring user's checkpoint steering
- Writing an overly long or dense report
- Including a Competitive Landscape section in trend-discovery mode (or omitting in validation mode)
- Not marking the workflow as complete
- Gathering new data or making new API calls in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
