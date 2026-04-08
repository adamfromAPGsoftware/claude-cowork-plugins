# OpenRouter Image Generation API Reference

## Overview

We use OpenRouter to access Nano Banana Pro (Google Gemini 3 Pro Image) for ad creative image generation. This is the same pattern used by `scripts/generate-brand-image.py` for brand assets.

## Model

| Model | OpenRouter ID | Cost | Best For |
|-------|-------------|------|----------|
| **Nano Banana Pro** (default) | `google/gemini-3-pro-image-preview` | ~$0.002/image | Production creatives — higher quality, character consistency |
| Nano Banana 2 (Flash) | `google/gemini-3.1-flash-image-preview` | ~$0.001/image | Cheap iteration, drafts only |

**Always use Nano Banana Pro for production ad creatives.** Flash is for quick drafts/testing only.

## API Endpoint

```
POST https://openrouter.ai/api/v1/chat/completions
Authorization: Bearer {OPENROUTER_API_KEY}
Content-Type: application/json
```

## Payload Structure

```json
{
  "model": "google/gemini-3-pro-image-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,{base64_encoded_reference_image}"
          }
        },
        {
          "type": "text",
          "text": "Create a Meta ad creative: 1080x1080 square format. Bold headline text 'Stop Wasting 40hrs/Week' in white on a dark gradient background. Show a business owner looking at a laptop with a confident expression. Modern, clean design with a green CTA button 'Learn More'."
        }
      ]
    }
  ],
  "modalities": ["image", "text"],
  "image_config": {
    "aspect_ratio": "1:1",
    "image_size": "2K"
  }
}
```

## Key Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| modalities | `["image", "text"]` | Required — enables image generation |
| image_config.aspect_ratio | `"1:1"`, `"9:16"`, `"16:9"`, `"4:3"`, `"3:4"` | Aspect ratio of generated image |
| image_config.image_size | `"2K"`, `"4K"` | Output resolution |

## Meta Ad Aspect Ratios

| Meta Format | Aspect Ratio | Use |
|-------------|-------------|-----|
| Feed square | 1:1 | Primary feed placement |
| Stories / Reels | 9:16 | Full-screen vertical |
| Feed landscape | 16:9 | Landscape feed (closest to Meta's 1.91:1) |

Note: OpenRouter doesn't support arbitrary ratios like 1.91:1. Use `16:9` as the closest match for Meta's landscape feed format.

## Response Parsing

```python
result = response.json()

# Check for errors
if "error" in result:
    raise Exception(result["error"]["message"])

# Extract images
message = result["choices"][0]["message"]
images = message.get("images", [])

# Each image is a data URL
for img_data_url in images:
    # Format: "data:image/png;base64,{base64_data}"
    header, b64_data = img_data_url.split(",", 1)
    image_bytes = base64.b64decode(b64_data)
    
    with open(output_path, "wb") as f:
        f.write(image_bytes)
```

## Input Images (Reference / Inspiration)

To include reference images (brand photos, competitor creatives for style reference):

```python
import base64
from pathlib import Path

def encode_image(path: Path) -> dict:
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{mime};base64,{b64}"}
    }

content_parts = []
for ref_image in reference_images:
    content_parts.append(encode_image(ref_image))
content_parts.append({"type": "text", "text": prompt})
```

## Best Practices

- **2-second delay** between sequential API calls to avoid rate limits
- **Reference photos first** in the content array, text prompt last
- **Be specific** about text placement, colors, and layout in the prompt
- **Retry on timeout** with 120-second request timeout
- **Skip SVG files** as input — Gemini doesn't support SVG

## Environment

```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxx
```

Already configured in repo root `.env`.
