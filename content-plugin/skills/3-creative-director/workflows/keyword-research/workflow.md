---
name: keyword-research
description: Standalone YouTube keyword research — run the 3-layer waterfall without a full draft package
web_bundle: true
---

# Keyword Research (Standalone)

**Goal:** Run the 3-layer YouTube keyword research waterfall (Autocomplete, Google Trends, YouTube Data API) and produce a keyword report with high-signal terms, rising/breakout opportunities, competitor tags, and SEO tag suggestions.

**Your Role:** In addition to your name, communication_style, and persona, you are also a YouTube SEO strategist running keyword research for a content creator. You extract actionable keyword data that informs titles, descriptions, and tags.

---

## WORKFLOW RULES

- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- 🛑 NEVER skip seed keyword confirmation with the user
- 📋 Keyword research is non-blocking — if the script fails, present what you can and move on
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `content_output_folder`, `project_folder`, `standalone_folder`, `env_file`

### 2. Resolve Project Context

Check if `{active_project}` is set.

- **If set:** Output will be saved to `{project_folder}/{project-slug}/creative-director/thumbnails/keyword-research.md`
- **If NONE:** Output will be saved to `{standalone_folder}/keyword-research/keyword-research-{date}.md`

---

## EXECUTION SEQUENCE

### 1. Gather Seed Keywords

"**What are the seed keywords for this research?**

Seeds should include:
- Core topic terms (e.g., 'AI agents', 'Claude Code')
- Tool/brand names mentioned in the content
- Target audience terms (e.g., 'developers', 'no-code')

Type your seeds as a comma-separated list."

Wait for user input.

### 2. Check for Content Brief

If an active project is set, check for a content brief at:
`{project_folder}/{project-slug}/strategist/research/`

If found, offer to use it: "Found a content brief — I can pass it to the keyword script for additional context. Use it? [Y/N]"

### 3. Run Keyword Research Script

Load `{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/data/pipeline-scripts.md` for CLI reference.

Execute:
```bash
python scripts/keyword-research.py \
    --seeds "{comma-separated seeds}" \
    --output "{resolved output path}" \
    [--brief "{content-brief-path}"]
```

### 4. Present Results

Load the keyword research report from the output path.

"**Keyword Research Results:**

**Layers Active:** {N}/3

**HIGH-SIGNAL Keywords** (appearing in 2+ layers — priority for title wording):
{list}

**RISING / BREAKOUT Terms** (trending opportunities):
{list}

**Competitor Tags** (what successful videos use):
{top 10}

**Suggested SEO Tags** (for YouTube description):
{list}

**Report saved to:** `{output path}`"

### 5. Handle Script Failure

If the keyword research script fails or all layers return empty:

"**Keyword research returned no results.** This can happen if:
- No internet connection
- YouTube Autocomplete blocked
- pytrends rate-limited

You can:
- **[R] Retry** — run the script again
- **[M] Manual** — I'll help you brainstorm keywords based on your content
- **[D] Done** — exit keyword research"

### 6. Completion

"**Keyword research complete.**

📄 **Report:** `{output path}`
🔑 **High-Signal:** {count} keywords
📈 **Rising:** {count} terms

**Next steps:**
- Use these keywords in **[DP] Draft Package** for title integration
- Or copy the SEO tags directly into your YouTube description

**Select:** [D] Done"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Seeds confirmed with user before running
- Script executed (success or graceful failure)
- Results presented with high-signal, rising, and competitor data
- Report saved to correct location
- Clear next steps provided

### ❌ SYSTEM FAILURE:

- Running script without confirming seeds
- Script failure blocking the workflow (should be non-blocking)
- Not saving the report
- Not presenting clear results

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
