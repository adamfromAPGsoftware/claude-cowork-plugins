---
description: Generate image and video ad creatives for the latest angle batch
---

Produce ad creatives for selected angles using AI generation:

1. Read `{plugin_root}/data/creative-data.json` for the latest batch
2. For each angle, generate images via Nano Banana Pro (1:1, 9:16, 16:9)
3. Optionally generate videos via fal.ai (Kling 3.0 or Veo 3.1)
4. Update creative-data.json with generated asset paths

$ARGUMENTS
