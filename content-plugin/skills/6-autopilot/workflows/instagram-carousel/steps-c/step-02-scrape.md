---
name: step-02-scrape
description: Scrape Instagram creator watchlist via Apify if inspiration is stale (conditional step)
nextStep: ./step-03-trends.md
---

# Step 2: Scrape Inspiration (Conditional)

## Goal

Refresh the inspiration library from the creator watchlist when it's stale. This step is conditional — skip it if the library was scraped recently.

## Sequence

### 1. Check Condition

If `needs_scrape = false` from step-01:

```
Inspiration library up to date ({days_since_scrape}d old). Using cached posts.
→ Skipping scrape.
```

Skip to step-03 immediately.

---

If `needs_scrape = true`, continue below.

### 2. Run Scraper

Execute via Bash:

```bash
python3 {project-root}/scripts/scrape-instagram-inspiration.py \
  --config {watchlist}
```

This downloads carousel posts from all profiles in the watchlist to:
`{inspirationDir}/{handle}/{post-id}/` with `meta.json` + slide PNGs

### 3. Handle Failures

If the scraper fails (Apify error, no token, network issue):
- Log the failure in context
- Set `scrape_status: failed`
- Continue to step-03 using whatever existing posts are in `{inspirationDir}` or the Creative Director's existing `{existingInspiration}` library as fallback

Do NOT abort the workflow — a scrape failure means we use older inspiration, not that we stop.

### 4. Count Results

After scrape completes, list directories in `{inspirationDir}`:
- Count total post directories across all handle subdirectories
- Note which handles returned results

### 5. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Inspiration Scrape
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:   {ok | failed}
Profiles: {handle1} ({N} posts), {handle2} ({N} posts)
Total:    {N} carousel posts available
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-03.
