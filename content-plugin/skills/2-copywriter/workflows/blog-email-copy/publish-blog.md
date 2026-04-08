# Publish Blog Post to Supabase

## Prerequisites

- Blog post must exist in `{content_output_folder}/projects/{project_slug}/copywriter/blog-email/`
- File naming pattern: `blog-{slug}-{date}.md`
- Environment variables must be set:
  - `APG_LANDER_SUPABASE_URL` — Supabase API URL for the lander project
  - `APG_LANDER_SUPABASE_SECRET_KEY` — Secret API key (bypasses RLS for inserts)

## Workflow

### 1. Validate Prerequisites

- Confirm `{active_project}` is set (not NONE). If NONE, halt and tell user to select a project first.
- Scan `{content_output_folder}/projects/{project_slug}/copywriter/blog-email/` for files matching `blog-*.md`
- If no files found: inform user and suggest running [BL] Blog Content first.
- If exactly one file found: use it automatically and inform user which file will be published.
- If multiple files found: list them with dates and ask user to select which one to publish.

### 2. Extract Metadata

Read the blog post markdown and extract:

- **title**: From the H1 heading (first `# ` line)
- **description**: From a META or frontmatter section's meta description field. If not found, use the first paragraph after the H1.
- **slug**: Generate from `{project_slug}` (already lowercase with hyphens). If the blog file name contains a more specific slug (e.g. `blog-my-specific-topic-2026-01-15.md`), use `{project_slug}-my-specific-topic` as the slug.
- **category**: Ask the user to select or type a category (e.g., "ai-engineering", "automation", "tutorial", "case-study"). This will be used for filtering on the lander site.
- **thumbnail**: Check `{content_output_folder}/projects/{project_slug}/creative-director/thumbnails/` for a generated thumbnail image. If multiple exist, ask user which to use. If none exist, ask user to provide a path or URL, or skip (thumbnail is optional).

### 3. Media Upload

The script automatically handles all local media files referenced in the markdown:

**Detected patterns:**
- `![alt](path)` — markdown images
- `[text](path)` — markdown links (only when pointing to media files)
- `<img src="path">`, `<video src="path">`, `<source src="path">` — HTML elements

**Supported file types:** jpg, jpeg, png, gif, webp, svg, mp4, webm

**Behaviour:**
- **Relative paths** (e.g., `../assets/screenshot.png`): uploaded to Supabase Storage bucket `resource-media/{slug}/filename.ext`, path rewritten to the public URL
- **Absolute URLs** (already `https://...`): left unchanged
- **Non-media local files** (e.g., `.md`, `.txt`): left unchanged
- **Missing files**: warned but skipped — publishing continues with remaining content

All media stored at: `storage/resource-media/{slug}/` and served from public URLs.

### 4. Preview Payload

Present the publishing payload to the user for review:

```
Publishing to: Lander — resources table + storage

Title:       {extracted title}
Slug:        {slug}
Description: {extracted description}
Category:    {selected category}
Thumbnail:   {thumbnail path or URL or "none"}
Content:     {character count} characters of markdown
Media:       {count} local files will be uploaded to resource-media/{slug}/
Published:   true
```

### 5. Confirm with User

**MANDATORY** — Ask user to confirm before publishing:

"Ready to publish to Supabase. This will upload images to storage and upsert the resource (insert new or update existing if slug matches). Proceed? [Y/N]"

- If N: Return to agent menu
- If Y: Continue to step 6

### 6. Execute Publishing Script

Run the Python publishing script via Bash:

```bash
python3 "{project-root}/scripts/publish-to-supabase.py" \
  --file "{content_output_folder}/projects/{project_slug}/copywriter/blog-email/{selected_blog_file}" \
  --title "{extracted title}" \
  --slug "{slug}" \
  --description "{extracted description}" \
  --category "{selected category}" \
  --thumbnail "{thumbnail path or URL}"
```

Omit `--thumbnail` if the user skipped thumbnail selection.

The script reads `APG_LANDER_SUPABASE_URL` and `APG_LANDER_SUPABASE_SECRET_KEY` from environment variables.

### 7. Report Result

- **On success**: Display the published resource URL pattern: `https://{YOUR_DOMAIN}/resources/{slug}` and confirm it's live.
- **On error**: Display the error message from the script. Common issues:
  - Missing env vars → tell user to set `APG_LANDER_SUPABASE_URL` and `APG_LANDER_SUPABASE_SECRET_KEY`
  - Auth error → secret key may be invalid or expired
  - Network error → check connectivity

### 8. Update Tracking

- Update `{project-root}/_bmad/_memory/copywriter-sidecar/memories.md` with blog publish status and timestamp
- Log the publish event: date, slug, title, status (published/failed)

---

## Supabase Table Reference

**Table:** `public.resources`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Auto-generated |
| slug | text | Unique — used for upsert |
| title | text | Required |
| description | text | Nullable |
| thumbnail | text | Nullable — public URL to thumbnail image (uploaded to storage or external URL) |
| category | text | Nullable |
| content | text | Required — full markdown |
| is_published | boolean | Default: true |
| created_at | timestamptz | Auto-generated |
| updated_at | timestamptz | Auto-generated |

**RLS:** Public can read published resources. Inserts require secret key.

**Storage Bucket:** `resource-media`

| Property | Value |
|----------|-------|
| Public | Yes (images accessible via URL) |
| Max file size | 50MB |
| Allowed types | jpeg, png, gif, webp, svg, mp4, webm |
| Path pattern | `resource-media/{slug}/{filename}` |
| Public URL | `{SUPABASE_URL}/storage/v1/object/public/resource-media/{slug}/{filename}` |

**Storage RLS:** Public can view. Uploads/updates/deletes require secret key.
