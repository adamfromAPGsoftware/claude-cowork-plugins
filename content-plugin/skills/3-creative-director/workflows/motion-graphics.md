# Motion Graphics Workflow

**Status:** Redirect — Owned by Video Editor agent

## Purpose

Motion graphics generation via Hera Video API is now owned by the Video Editor agent as part of the integrated video production pipeline.

## Redirect

Use the Video Editor agent's **[HM] Hera Motion Graphics** workflow:
- Location: `{project-root}/video-plugin/skills/1-video-editor/workflows/hera-motion-graphics/workflow.md`
- Supports both storyboard-driven and manual brief input
- Output: `.mp4` files to `{project_folder}/{project-slug}/video-editor/motion-graphics/`

The Creative Director can request motion graphics by providing briefs to the Video Editor, or the Storyboard workflow will automatically identify motion graphic needs during production planning.

## Alternative: fal-ai MCP Video Generation

For simple motion graphic needs that don't require the full Hera pipeline:

- `mcp__fal-ai__generate_video` — text-to-video (short clips, abstract motion)
- `mcp__fal-ai__generate_video_from_image` — animate a still image into a video clip
- `mcp__fal-ai__generate_video_from_video` — restyle or add motion to an existing video

These are available via the platform-level fal-ai MCP. Use `mcp__fal-ai__recommend_model` to find the best model for your specific motion graphic need.
