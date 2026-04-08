# fal.ai Video Generation API Reference

## Overview

We use fal.ai as the unified API gateway for video generation models. fal.ai provides access to Kling 3.0, Veo 3.1, and other models through a consistent queue-based API.

## Supported Models

| Model | fal.ai Model ID | Best For | Cost | Notes |
|-------|----------------|----------|------|-------|
| **Veo 3 (default)** | `fal-ai/veo3` | **UGC talking head, multi-scene, dialogue** | $0.40/s with audio | Default for all UGC video. Max 8s. Native audio + lip-sync. |
| Kling 3.0 Pro (i2v) | `fal-ai/kling-video/v3/pro/image-to-video` | Animating static ad images | ~$0.112/s | Use for before-after, product UI animations |
| Kling 3.0 Pro (t2v) | `fal-ai/kling-video/v3/pro/text-to-video` | Text-to-video with voice | ~$0.196/s with voice | 2,500 char prompt limit. Max 15s. |
| HeyGen | `fal-ai/heygen/v2/video-agent` | Budget UGC, long-form | $0.033/s | 500+ avatars. 30-90s. Less cinematic control. |

## Queue API Pattern

All fal.ai video generation uses an async queue pattern: submit → poll → download.

### 1. Submit Job

```
POST https://queue.fal.run/{model_id}
Authorization: Key {FAL_API_KEY}
Content-Type: application/json

{
  "prompt": "A business owner looking frustrated at paperwork, then smiling at a laptop screen",
  "duration": "5",
  "aspect_ratio": "9:16",
  "image_url": "https://... or data:image/png;base64,..."
}
```

**Response:**
```json
{
  "request_id": "abc123-def456",
  "status": "IN_QUEUE"
}
```

### 2. Poll for Status

**CRITICAL:** Use the `status_url` returned in the submit response — do NOT construct the URL manually. POST to the model endpoint creates new jobs, so polling must use GET on the canonical status URL.

```
GET {status_url from submit response}
Authorization: Key {FAL_API_KEY}
```

The `status_url` uses a shortened model path (e.g., `fal-ai/kling-video/requests/...` not `fal-ai/kling-video/v3/pro/image-to-video/requests/...`).

**Response:**
```json
{
  "status": "IN_QUEUE | IN_PROGRESS | COMPLETED | FAILED",
  "queue_position": 5
}
```

Poll every 5 seconds. Max wait: 600 seconds.

### 3. Fetch Result

**Use the `response_url` from the submit response:**

```
GET {response_url from submit response}
Authorization: Key {FAL_API_KEY}
```

**Response:**
```json
{
  "video": {
    "url": "https://fal.media/files/...",
    "content_type": "video/mp4",
    "file_name": "output.mp4",
    "file_size": 5242880
  }
}
```

Download the video URL with streaming (8192-byte chunks).

## Model-Specific Input Parameters

### Kling 3.0 Pro (Image-to-Video)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | Yes | Scene description and motion direction |
| image_url | string | Yes | Reference image (URL or base64 data URI) |
| duration | string | No | `"5"` or `"10"` seconds (default: 5) |
| aspect_ratio | string | No | `"16:9"`, `"9:16"`, `"1:1"` (default: 16:9) |

### Kling 3.0 Pro (Text-to-Video)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | Yes | Detailed scene description |
| duration | string | No | `"5"` or `"10"` seconds |
| aspect_ratio | string | No | `"16:9"`, `"9:16"`, `"1:1"` |

### Veo 3.1

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | Yes | Detailed scene description |
| duration | int | No | 5-10 seconds |
| aspect_ratio | string | No | `"16:9"`, `"9:16"`, `"1:1"` |
| enhance_prompt | boolean | No | Let model expand the prompt (default: true) |

## Meta Ad Video Specs

| Placement | Aspect | Max Duration | Min Resolution |
|-----------|--------|-------------|----------------|
| Feed | 1:1 or 4:5 | 241 min | 1080px |
| Stories / Reels | 9:16 | 90s (Reels), 120s (Stories) | 1080x1920 |
| In-stream | 16:9 | 15s recommended | 1080px |

For Meta ads, generate 9:16 (Stories/Reels) and 1:1 (Feed) as the primary formats.

## Environment

```
FAL_API_KEY=your_fal_api_key_here
```

Get your key at: https://fal.ai/dashboard/keys

## Cost Estimates

| Scenario | Model | Duration | Cost |
|----------|-------|----------|------|
| 1 ad video | Kling 3.0 | 10s | ~$0.29 |
| 1 ad video | Veo 3.1 | 10s | ~$2-6 |
| 10 videos batch | Kling 3.0 | 10s each | ~$2.90 |
| 3 videos batch | Veo 3.1 | 10s each | ~$6-18 |
