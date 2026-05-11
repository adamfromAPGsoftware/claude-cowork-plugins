---
name: init
description: First-run setup for Video Editor
menu-code: INIT
---

# First-Run Setup for Video Editor

Welcome! Setting up your video production workspace.

## Wiki Location

Corrections wiki lives inside the plugin at `{plugin-root}/video-plugin/wiki/`.

The wiki is already initialized — 7 topic pages and an index are pre-created. No setup needed.

## Branded Assets

Brand images (logos, profile photos) used by Remotion templates:
`{plugin-root}/video-plugin/assets/branded-assets/`

Add PNG files here for use in branded Remotion templates (UpworkProfile, AgencyBrand, etc.).

## Setup Questions

1. **Primary content format** — What do you primarily edit? (e.g. `talking-head`, `screen-recording`, `podcast`, `mixed`)
2. **Proxy workflow** — Do you film in 4K and want automatic 720p proxy generation? (yes/no, default: yes)
3. **Default output folder** — Where should rendered videos be saved?

## Wiki Confirmation

Confirm that the wiki is accessible at `{plugin-root}/video-plugin/wiki/index.md`. It should already exist — if not, the plugin may need reinstalling.

Save setup answers to `wiki/index.md` Session Log as the first row:
```markdown
| {today} | SETUP | Init | 0 |
```

## Ready

Setup complete! Ready to process your first video.
