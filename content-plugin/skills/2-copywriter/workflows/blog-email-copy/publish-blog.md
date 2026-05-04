# Export Blog Post

## Prerequisites

- Blog post must exist in `{content_output_folder}/projects/{project_slug}/copywriter/blog-email/`
- File naming pattern: `blog-{slug}-{date}.md`

## Workflow

### 1. Validate Prerequisites

- Confirm `{active_project}` is set (not NONE). If NONE, halt and tell user to select a project first.
- Scan `{content_output_folder}/projects/{project_slug}/copywriter/blog-email/` for files matching `blog-*.md`
- If no files found: inform user and suggest running [BL] Blog Content first.
- If exactly one file found: use it automatically and inform user which file will be exported.
- If multiple files found: list them with dates and ask user to select which one to export.

### 2. Extract Metadata

Read the blog post markdown and extract:

- **title**: From the H1 heading (first `# ` line)
- **description**: From a META or frontmatter section's meta description field. If not found, use the first paragraph after the H1.
- **slug**: Generate from `{project_slug}` (already lowercase with hyphens).
- **category**: Ask the user to select or type a category (e.g., "ai-engineering", "automation", "tutorial", "case-study").

### 3. Preview Payload

Present the export summary to the user:

```
Blog Post — Export Ready

Title:       {extracted title}
Slug:        {slug}
Description: {extracted description}
Category:    {selected category}
Content:     {character count} characters of markdown
Output:      {content_output_folder}/projects/{project_slug}/copywriter/blog-email/blog-{slug}-{date}.md
```

### 4. Update Frontmatter

Update the blog file's frontmatter with final metadata:

```yaml
title: '{H1 text}'
meta_title: '{selected meta title}'
meta_description: '{selected meta description}'
primary_keyword: '{keyword}'
secondary_keywords: [{keywords}]
category: '{selected category}'
date: '{current date}'
status: complete
format: blog
```

### 5. Report Result

"**Blog post ready for publishing.**

- **File:** `{file path}`
- **Format:** Markdown
- **Status:** Complete

**Next steps — deploy your blog:**
- **Ghost / WordPress:** Import the markdown file directly
- **Notion:** Paste into a page or use the Notion API
- **Astro / Hugo / Next.js:** Drop the file into your `content/` directory (frontmatter is already structured)
- **Beehiiv / Kit (email):** Copy the body and paste into your email editor
- Any CMS that accepts markdown will work without modification."

### 6. Update Tracking

- Update `{project-root}/context/memory/2-copywriter-sidecar/memories.md` with blog export status and timestamp
