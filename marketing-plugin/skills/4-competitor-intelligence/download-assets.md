---
name: download-assets
description: Download creative assets for ads that have a creative_url but no local_path yet
menu-code: DA
---

# Download Assets

Download creative assets (images, videos, thumbnails) for ads that have a `creative_url` but no `local_path` yet.

## Process

1. **Load competitor-data.json** — Read `{project-root}/marketing-plugin/data/competitor-data.json`

2. **Identify pending downloads:**
   - Find all ads where `creative_url` is set but `local_path` is null or missing
   - Report count of pending downloads before starting

3. **Run download script** using Desktop Commander's `execute_command` tool (or Bash in Claude Code):
   ```
   python3 {plugin_root}/scripts/download-competitor-assets.py
   ```
   Where `{plugin_root}` is the absolute path to the `marketing-plugin` directory.

4. **Review script output:**
   - Note successful downloads (with file sizes)
   - Note failed downloads (expired URLs, 404s, timeouts)
   - Note any skipped items (already downloaded)

5. **Load the updated competitor-data.json** and verify:
   - Each downloaded ad now has a `local_path` pointing to `competitor-assets/`
   - Failed downloads are flagged for retry

## Output

Report summary:

```
Download complete.
  Pending: {pending_count} assets
  Downloaded: {success_count} ({total_size_mb} MB)
  Failed: {failed_count}
  Skipped (already local): {skipped_count}

  By competitor:
  - {competitor_name}: {downloaded} downloaded, {failed} failed
  - ...

Recommended next: [AC] to analyse downloaded creatives.
```
