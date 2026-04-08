---
name: package-creatives
description: Compile copy, assets, and campaign structure into an upload guide for Meta Ads Manager
menu-code: PC
---

# Package Creatives

Compile all copy variants, image files, and video files for a batch into a structured upload guide for Meta Ads Manager.

## Process

1. **Load creative-data.json** — Read `marketing-plugin/data/creative-data.json`. When `{active_campaign}` is set, filter batches to those with matching `campaign_id` and show only campaign-relevant batches. When `{active_campaign}` is null, show all batches. Identify the target batch — use the most recent matching, or ask the user which batch to package.

2. **Validate batch readiness** — Check that angles have at least images generated. Warn if any angles are still in `angles_built` status (no creatives yet). Videos are optional but recommended. If any angles have `ad_scripts` with `status == "script_written"` (not yet filmed/edited), display a warning: "{N} ad script(s) are written but not yet filmed — these won't be included as video assets in the upload guide. Film and edit them first, or proceed without."

3. **For each angle in the batch, compile:**
   - All 3 copy variants (direct, story, question) with `primary_text`, `headline`, `description`, `cta`
   - All image file paths (1:1, 9:16, 16:9)
   - All video file paths (9:16, 1:1) if generated
   - All filmed video paths from `ad_scripts` where `status == "edited"` (edited_video_path)
   - Landing page URL — use `landing_page.full_url` from campaign-data.json. If the landing page hasn't been deployed yet (Track A still in progress), use the planned URL from the campaign config. Final ad URLs are set during [MC], not during packaging.

4. **Generate UPLOAD-GUIDE.md** with the following structure:

   ```markdown
   # Upload Guide — {batch_id}

   Generated: {timestamp}
   Angles: {count} | Images: {count} | Videos: {count}

   ## Recommended Campaign Structure

   - **1 Campaign** — "{campaign_name}" (Conversions objective)
   - **1 Ad Set per angle** — each angle gets its own ad set for clean A/B testing
   - **Multiple Ads per ad set** — one ad per copy variant x creative format combination

   ## A/B Testing Recommendations

   - Week 1: Run all angles with "direct" copy variant only — identify winning angles
   - Week 2: Expand winning angles with "story" and "question" variants
   - Kill angles with CTR < 1% after $50 spend
   - Promote angles with CTR > 2% to higher budgets

   ## AI Disclosure

   IMPORTANT: AI-generated creatives (images via Nano Banana Pro, videos via Veo 3.1) require
   the "AI-generated content" disclosure box in Meta Ads Manager. Filmed video ads do NOT
   require AI disclosure unless they contain AI-generated motion graphic overlays.

   ---

   ## Angle 1: {angle_name}

   **Hook:** {hook_line}

   ### Copy Variant: Direct
   - **Primary Text:** {primary_text}
   - **Headline:** {headline}
   - **Description:** {description}
   - **CTA Button:** {cta}

   ### Copy Variant: Story
   - **Primary Text:** {primary_text}
   - **Headline:** {headline}
   - **Description:** {description}
   - **CTA Button:** {cta}

   ### Copy Variant: Question
   - **Primary Text:** {primary_text}
   - **Headline:** {headline}
   - **Description:** {description}
   - **CTA Button:** {cta}

   ### Creative Assets
   | Format | Type | File Path | Source |
   |--------|------|-----------|--------|
   | 1:1 | Image | data/creatives/{batch_id}/{angle_id}-1x1.png | AI (Nano Banana Pro) |
   | 9:16 | Image | data/creatives/{batch_id}/{angle_id}-9x16.png | AI (Nano Banana Pro) |
   | 16:9 | Image | data/creatives/{batch_id}/{angle_id}-16x9.png | AI (Nano Banana Pro) |
   | 9:16 | Video | data/creatives/{batch_id}/{angle_id}-9x16.mp4 | AI (Veo 3.1) |
   | 1:1 | Video | data/creatives/{batch_id}/{angle_id}-1x1.mp4 | AI (Veo 3.1) |
   | 9:16 | Video (Filmed) | {ad_scripts[].edited_video_path} | Filmed + SF Edit |

   **Landing Page URL:** {url}

   ---
   (repeat for each angle)
   ```

5. **Save the guide** to `marketing-plugin/data/creatives/{batch_id}/UPLOAD-GUIDE.md`

6. **Update creative-data.json:**
   - Set each packaged angle's `status` to `"packaged"`
   - Update `meta.last_generation`

7. **Report:**

   ```
   Package Complete — Batch: {batch_id}

   | Angle | Copy Variants | Images | Videos | Status |
   |-------|--------------|--------|--------|--------|
   | {name} | 3 | 3 | 2 | packaged |
   | ... |

   Upload guide: data/creatives/{batch_id}/UPLOAD-GUIDE.md

   Next steps:
   1. Open Meta Ads Manager
   2. Follow the upload guide — copy is ready to paste
   3. Remember to check the AI disclosure box for each ad
   4. Set budgets per the A/B testing recommendations
   ```

## Principles

- The upload guide must be self-contained — someone who didn't generate the creatives should be able to upload from it alone
- Copy is formatted for direct paste into Meta Ads Manager fields
- File paths are relative to the plugin root for portability
- AI disclosure reminder is non-negotiable — it's a Meta policy requirement
