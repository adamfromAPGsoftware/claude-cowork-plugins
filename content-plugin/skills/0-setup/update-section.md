# Update Section [UC]

Update a single section of `{project-root}/config.yaml` without rerunning the full wizard.

## Config file location

`{project-root}/config.yaml`

Read the current file first to prefill existing values as defaults.

---

## On activation

Ask: "Which section do you want to update?"

```
  W. Content Workspace  — the folder where all your content is stored
  1. Brand Identity     — name, website, creator name and title
  2. Brand Voice        — tone, contractions, banned words, sentence max
  3. Content ICP        — role, knowledge level, job-to-be-done, anti-patterns
  4. Platforms          — active platforms, primary platform, posting frequency
  5. Credentials        — API key references
  6. Scheduling         — timezone and Buffer channel names
  7. Brand Assets       — colours, logos, reference photos, email config
  8. Content Strategy   — competitors, content pillars, X Premium (optional)
```

Once the user selects a section, show the current values for that section (so they can see what they're changing), then ask only the questions for that section.

After collecting the new values:
1. Update only that section in `config.yaml` — leave all other sections unchanged
2. If the updated section affects a reference file (sections 2, 3, 4, 6, 7, or 8), regenerate that reference file

### Workspace section (W)

Show the current workspace path from `paths.workspace`.

Ask: "Enter a new workspace path, or press Enter to keep the current path."

If changed:
1. Create the folder scaffold at the new path (same structure as the setup wizard pre-flight, skip any subdirectories that already exist)
2. Update all `paths.*` keys in config.yaml to reflect the new workspace root
3. Warn: "Existing content at the old path has NOT been moved. If you have content there, move it manually to the new workspace or point back to the old path."

---

## Reference file regeneration rules

| Section updated | Reference file to regenerate |
|----------------|------------------------------|
| Content Workspace (W) | No reference files — only config.yaml paths updated |
| Brand Identity (1) | Update header in all five reference files |
| Brand Voice (2) | `{project-root}/context/references/brand-voice.md` |
| Content ICP (3) | `{project-root}/context/references/content-icp.md` |
| Platforms (4) | `{project-root}/context/references/platform-config.md` |
| Credentials (5) | No reference files to regenerate |
| Scheduling (6) | `{project-root}/context/references/scheduling-config.md` |
| Brand Assets (7) | `{project-root}/context/references/brand-assets.md` |
| Content Strategy (8) | `{project-root}/context/references/brand-assets.md` (strategy section) |

---

## Output format

```
✓ Section {N} updated — {Section Name}

  {key: value for each field in the section}

{if reference file regenerated}
  context/references/{filename}.md regenerated ✓
```
