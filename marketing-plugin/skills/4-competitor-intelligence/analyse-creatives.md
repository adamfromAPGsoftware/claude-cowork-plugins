---
name: analyse-creatives
description: Analyse downloaded creative assets with Gemini Flash vision (use --quality high for Pro)
menu-code: AC
---

# Analyse Creatives

Analyse downloaded creative assets with Gemini Flash vision (default, ~10x cheaper) or Gemini Pro (`--quality high`). Categorises hook type, visual style, CTA pattern, copy strategy, format type, and provides confidence scores.

## Process

1. **Load competitor-data.json** — Read `{project-root}/marketing-plugin/data/competitor-data.json`

2. **Identify unanalysed assets:**
   - Find all ads where `local_path` is set but `analysis` is null or missing
   - Report count of pending analyses before starting

3. **Run analysis script** using Desktop Commander's `execute_command` tool (or Bash in Claude Code):
   ```
   python3 {plugin_root}/scripts/analyse-competitor-creatives.py
   ```
   Where `{plugin_root}` is the absolute path to the `marketing-plugin` directory.

4. **Review script output:**
   - Note how many creatives were analysed
   - Note any failures (unsupported format, API errors)
   - Each analysis should produce structured fields:
     - `hook_type` — pattern used in the first 3 seconds / top of image (e.g., question, statistic, pain point, testimonial)
     - `visual_style` — design approach (e.g., UGC, polished, screenshot, meme, talking head)
     - `cta_pattern` — call-to-action strategy (e.g., learn more, shop now, sign up, book a call)
     - `copy_strategy` — messaging approach (e.g., benefit-led, fear-based, social proof, authority)
     - `format` — creative format (e.g., single image, carousel, video, slideshow)
     - `summary` — one-sentence description of the creative

5. **Load the updated competitor-data.json** and verify analyses are populated

## Output

Report summary:

```
Analysis complete.
  Pending: {pending_count} creatives
  Analysed: {success_count}
  Failed: {failed_count}

  By competitor:
  - {competitor_name}: {analysed} analysed
    Top hook types: {hook_1}, {hook_2}
    Top visual styles: {style_1}, {style_2}
  - ...

Recommended next: [TW] to check longevity and identify winners.
```
