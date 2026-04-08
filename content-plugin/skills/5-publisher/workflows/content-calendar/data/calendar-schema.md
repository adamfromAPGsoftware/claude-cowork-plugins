# Content Calendar YAML Schema

## File Location

`{content_output_folder}/calendar/content-calendar.yaml`

This is a **global** calendar — shared across all projects. Not project-scoped.

## Schema

```yaml
metadata:
  last_updated: '2026-02-27'       # ISO date of last modification
  total_entries: 0                   # Total count of entries

entries:
  - id: 1                           # Auto-incrementing integer
    title: 'Content Title'          # Required — descriptive title
    platform: 'linkedin'            # Required — target platform
    content_type: 'video'           # Required — content format
    status: 'draft'                 # Required — lifecycle status
    scheduled_date: '2026-03-01'    # Optional — planned publish date
    publish_date: ''                # Optional — actual publish date
    project_slug: 'my-project'     # Optional — source project reference
    description: 'Brief summary'   # Optional — what the content is about
    created_date: '2026-02-27'     # Auto-set on creation
```

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Auto-incrementing, unique per entry |
| title | string | Descriptive title of the content |
| platform | string | Target platform (see valid values below) |
| content_type | string | Content format (see valid values below) |
| status | string | Lifecycle status (see valid values below) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| scheduled_date | string (ISO date) | Planned publish date |
| publish_date | string (ISO date) | Actual publish date |
| project_slug | string | Source project slug for traceability |
| description | string | Brief summary of the content |
| created_date | string (ISO date) | Auto-set when entry is created |

## Valid Values

### platform

`linkedin`, `youtube`, `twitter`, `instagram`, `tiktok`, `facebook`, `threads`, `bluesky`, `pinterest`, `substack`, `medium`, `website`, `podcast`, `newsletter`

### content_type

`video`, `short-video`, `article`, `post`, `reel`, `story`, `carousel`, `thread`, `podcast-episode`, `newsletter-issue`, `blog-post`, `infographic`, `live-stream`

### status

| Status | Description |
|--------|-------------|
| `draft` | Content planned but not yet scheduled |
| `scheduled` | Content confirmed for a specific date |
| `published` | Content has been published |
| `cancelled` | Content was planned but cancelled |

## Empty Calendar Template

```yaml
metadata:
  last_updated: ''
  total_entries: 0

entries: []
```

## Duplicate Detection Rules

A potential duplicate is flagged when:
1. **Same platform** AND **similar title** (case-insensitive substring match or >70% word overlap)
2. **Same platform** AND **same scheduled_date** (collision — two items on same platform, same day)
3. **Same title** across **different platforms** within a 3-day window (intentional cross-posting should be noted)
