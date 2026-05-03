---
step: 1
name: init
description: Discover script, load reference frame catalog, set output path
---

# Step 1 — Init

## 1. Script Discovery

Search for the script in the active project folder. Check these paths in order:

1. `{content_output_folder}/{active_project}/copywriter/scripts/` — look for `*-script.md`, `*script*.md`, or the most recently modified `.md` file
2. `{content_output_folder}/{active_project}/copywriter/` — any `*script*` file
3. `{content_output_folder}/{active_project}/strategist/ideation/` — brief or ideation doc if no script yet

If multiple script files found, ask the user which to use.

If no script found, ask the user to paste the script content directly or provide a path.

**Store:** `{script_path}` and `{script_content}`

---

## 2. Generate Slug

Derive a short kebab-case slug from the active project name or video title:
- Remove common words (how, the, a, an, I, my, to)
- Max 4 words, kebab-case
- Example: "claude-opus-killed-video-editors" → `claude-opus-video-editors`

**Store:** `{diagram_slug}`

---

## 3. Load Reference Frame Catalog

Read the full reference frame catalog:
`{project-root}/brand-assets/reference-frames/catalog.yaml`

Hold in working memory. You'll use it in Step 2 to match script content to available screenshots.

**Note the catalog structure:**
- Each tool entry has: `display_name`, `aliases`, `frames[]`
- Each frame has: `file` (relative path from catalog dir), `description`, `tags[]`, `analyzed`

**Store:** `{reference_catalog}` (full YAML contents in memory)

---

## 4. Set Output Paths

Determine output directory based on project mode:

**Project mode** (active project set):
```
{content_output_folder}/{active_project}/copywriter/diagrams/
```

**Standalone mode:**
```
{standalone_folder}/{date}-{diagram_slug}/diagrams/
```

Create the `diagrams/` directory if it doesn't exist. Also create `diagrams/images/` for any generated images.

**Store:**
- `{output_dir}` — the diagrams directory path
- `{output_html}` — `{output_dir}/diagram-{diagram_slug}.html`
- `{plan_file}` — `{output_dir}/diagram-plan-{diagram_slug}.md`
- `{images_dir}` — `{output_dir}/images/`
- `{ref_frames_root}` — `{project-root}/brand-assets/reference-frames/`

---

## 5. Compute Relative Path Prefix

The HTML file at `{output_html}` needs to reference images in `{ref_frames_root}` using relative paths.

Count the directory depth from `{output_html}` to `{project-root}` and build the relative prefix.

Standard case: `content/projects/{slug}/copywriter/diagrams/diagram-{slug}.html`
- `diagrams/` → `copywriter/` → `{slug}/` → `projects/` → `content/` → `[repo root]`
- That's 5 levels up: `../../../../../`

**Store:** `{ref_path_prefix}` = `../../../../../` (adjust if output path differs)

So a reference frame at `brand-assets/reference-frames/claude-code/file.png` would be referenced in the HTML as:
`{ref_path_prefix}brand-assets/reference-frames/claude-code/file.png`

---

## 6. Load Design References

Read these data files (skim if already in context):
- `{project-root}/content-plugin/skills/2-copywriter/workflows/diagram-generation/data/diagram-standards.md`
- `{project-root}/content-plugin/skills/2-copywriter/workflows/diagram-generation/data/component-reference.md`

---

## 7. Confirm Setup

Present a brief init summary:

```
Script: {script_path}
Output: {output_html}
Ref frames: {reference_catalog — count of tools found}
```

Then proceed immediately to Step 2 (or wait in collab mode).

---

**Load next:** `steps-c/step-02-concept.md`
