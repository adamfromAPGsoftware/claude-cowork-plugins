---
name: upload-creatives
description: Upload generated image and video creatives to Meta and store creative IDs
menu-code: UC
---

# Upload Creatives — Push Assets to Meta

Upload generated image and video creatives to Meta Ads Manager and store the returned creative IDs back in creative-data.json.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Uploading creatives for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, list campaigns from `campaign-data.json`. Ask user to select one.

2. **Load creative batches** — From `creative-data.json`, find all batches linked to this campaign ID. Show:
   ```
   Batches for {campaign_name}:
   {For each batch:}
   - {batch_id}: {angle_count} angles, {asset_count} assets ({uploaded_count} already uploaded)
   ```

3. **Find assets to upload** — Scan each batch for image and video files that don't yet have `meta_creative_id` set. List them:
   ```
   Assets to upload:
   {For each asset:}
   - {filename} ({format}, {type}) — {file_size}
   ```

4. **Upload** — For each batch, run:
   ```
   python3 marketing-plugin/scripts/upload-meta-creatives.py --campaign-id {id} [--batch-id {batch_id}]
   ```

   The script handles:
   - Images: POST to `/{account_id}/adimages` with image bytes, returns `image_hash`
   - Ad Creatives: POST to `/{account_id}/adcreatives` with `object_story_spec` using the image hash
   - Videos: POST to `/{account_id}/advideos` with video source (async upload), polls until ready

5. **Store creative IDs** — Update `creative-data.json` with the returned `meta_creative_id` for each asset.

6. **Log to api-log.md** — Record all upload operations.

7. **Present result:**
   ```
   {count} creatives uploaded to Meta. Creative IDs stored.

   {For each uploaded asset:}
   - {filename} -> creative_id: {meta_creative_id}

   Next: Run [MC] to create the campaign structure, or [GA] / [LC] for tracking setup.
   ```
