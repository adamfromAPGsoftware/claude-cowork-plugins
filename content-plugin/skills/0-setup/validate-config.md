# Validate Config [VC]

Read `{project-root}/config.yaml` and check all required fields. Then check that all five reference files exist.

## Config file location

`{project-root}/config.yaml`

---

## Validation checks

### Pre-flight — Content Workspace

Required fields:
- `paths.workspace` — must not be empty
- `paths.project_folder` — must not be empty
- `paths.content_output_folder` — must not be empty
- `paths.standalone_folder` — must not be empty

Also verify the workspace directory exists on disk: check that `paths.workspace` is an existing directory and that `projects/`, `context/references/`, `standalone/`, `context/brand-assets/`, `memory/`, and `draft-queue/` subdirectories exist. If missing, the scaffold was never created or the path was changed manually.

### Section 1 — Brand Identity

Required fields:
- `brand.name` — must not be empty or default placeholder
- `brand.creator_name` — must not be empty
- `brand.website` — must be a valid URL

### Section 2 — Brand Voice

Required fields:
- `voice.tone_descriptors` — must have at least 1 entry
- `voice.banned_words` — must have at least 1 entry
- `voice.max_sentence_words` — must be a number

### Section 3 — Content ICP

Required fields:
- `icp.role` — must not be empty
- `icp.job_to_be_done` — must not be empty

### Section 4 — Platforms

Required fields:
- `platforms.primary` — must not be empty
- `platforms.active` — must have at least 1 entry

### Section 5 — Credentials (MCP Connectivity)

Test that each MCP server is reachable:
- **YouTube MCP** — call `mcp__youtube__searchVideos` with query "test". Pass if any response returned.
- **Buffer MCP** — call `mcp__buffer__buffer_api_help`. Pass if any response returned.
- **fal-ai MCP** — call `mcp__fal-ai__list_models`. Pass if any response returned.

If a server is unreachable, show: "{Service} MCP not connected. Check your Claude Code MCP settings — these are platform-level MCP servers, not plugin-level."

### Section 6 — Scheduling & Accounts

Required fields:
- `scheduling.timezone` — must not be empty

### Section 7 — Brand Assets

Required fields:
- `brand.colors.primary` — must not be empty
- `brand.assets.logo_dir` — must not be empty; verify directory exists on disk
- `brand.assets.reference_photos_dir` — must not be empty; verify directory exists on disk
- `brand.email.sign_off` — must not be empty
- `brand.email.greeting` — must not be empty
- `brand.email.platform` — must not be empty

### Section 8 — Content Strategy

Optional section — warn if empty but do not fail:
- `strategy.competitors` — note count (can be empty array)
- `strategy.content_pillars` — note count (can be empty array)
- `strategy.x_premium` — must be true or false

### Reference files

Check that all five files exist:
- `{project-root}/context/references/brand-voice.md`
- `{project-root}/context/references/content-icp.md`
- `{project-root}/context/references/platform-config.md`
- `{project-root}/context/references/scheduling-config.md`
- `{project-root}/context/references/brand-assets.md`

---

## Output format

```
Content Plugin — Config Validation

  Content Workspace ........ ✓ / ✗ {reason if failed}
  Brand Identity ........... ✓ / ✗ {reason if failed}
  Brand Voice .............. ✓ / ✗ {reason if failed}
  Content ICP .............. ✓ / ✗ {reason if failed}
  Platforms ................ ✓ / ✗ {reason if failed}
  Credentials .............. ✓ / ✗ {reason if failed}
  Scheduling & Accounts .... ✓ / ✗ {reason if failed}
  Brand Assets ............. ✓ / ✗ {reason if failed}
  Content Strategy ......... ✓ / ⚠ not configured (optional)

  Reference files:
    brand-voice.md .......... ✓ exists / ✗ missing
    content-icp.md .......... ✓ exists / ✗ missing
    platform-config.md ...... ✓ exists / ✗ missing
    scheduling-config.md .... ✓ exists / ✗ missing
    brand-assets.md ......... ✓ exists / ✗ missing

{if all pass}
Everything looks good. Run /content:1-content-strategist to start.

{if any fail}
To fix: run [SW] to rerun the full setup wizard, or [UC] to update a specific section.
```
