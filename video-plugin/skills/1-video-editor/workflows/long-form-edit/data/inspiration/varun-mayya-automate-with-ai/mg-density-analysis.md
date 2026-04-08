```markdown
# MG Density Analysis: How to Automate ANYTHING with AI (N8N Tutorial)

## Chapter Map

| # | Chapter Name | Start | End | Duration | Approx MG Count | Avg Inter-MG Spacing | Transition Style |
|---|-------------|-------|-----|----------|-----------------|---------------------|-----------------|
| 1 | Intro | 00:00 | 00:50 | 0m 50s | 8 | 6s | Direct Cut |
| 2 | What is n8n? | 00:50 | 02:22 | 1m 32s | 5 | 18s | Direct Cut |
| 3 | Core Concepts & Hosting (Sponsor) | 02:22 | 03:59 | 1m 37s | 4 | 24s | Direct Cut |
| 4 | Workflow 1: Meeting Scheduler | 03:59 | 17:00 | 13m 01s | 15 | 52s | Direct Cut |
| 5 | Getting API Keys | 17:00 | 20:54 | 3m 54s | 5 | 46s | Direct Cut |
| 6 | Community Templates | 20:54 | 22:48 | 1m 54s | 3 | 38s | Direct Cut |
| 7 | Workflow 2: Idea to Avatar | 22:48 | 26:49 | 4m 01s | 6 | 40s | Direct Cut |
| 8 | Conclusion | 26:49 | 28:45 | 1m 56s | 0 | N/A | Direct Cut |

## Section Transitions

### Transition at 00:50: Intro → What is n8n?
- **Style:** Direct cut from talking head to screen recording with PiP.
- **Audio:** Continuous speaking.

### Transition at 02:22: What is n8n? → Core Concepts & Hosting
- **Style:** Direct cut from screen recording to talking head, then to Hostinger screen recording.
- **Audio:** Continuous speaking.

### Transition at 03:59: Core Concepts & Hosting → Workflow 1: Meeting Scheduler
- **Style:** Direct cut from Hostinger UI to n8n UI screen recording.
- **Audio:** Continuous speaking.

### Transition at 17:00: Workflow 1: Meeting Scheduler → Getting API Keys
- **Style:** Direct cut from screen recording to full-screen talking head, then back to screen recording.
- **Audio:** Continuous speaking.

### Transition at 20:54: Getting API Keys → Community Templates
- **Style:** Direct cut from screen recording to full-screen talking head, then back to screen recording.
- **Audio:** Continuous speaking.

### Transition at 22:48: Community Templates → Workflow 2: Idea to Avatar
- **Style:** Direct cut from full-screen talking head to screen recording.
- **Audio:** Continuous speaking.

### Transition at 26:49: Workflow 2: Idea to Avatar → Conclusion
- **Style:** Direct cut from screen recording to full-screen talking head.
- **Audio:** Continuous speaking.

## MG-Sparse Zones (>30s without visual change)

*Note: As a software tutorial, large portions of this video consist of continuous screen recording with a static Picture-in-Picture (PiP) of the host. While the screen content changes as the host interacts with the software, there are long stretches without added post-production motion graphics (like text overlays, custom animations, or significant zooms).*

| Start | End | Duration | Context |
|-------|-----|----------|---------|
| 04:10 | 05:20 | 70s | Setting up Telegram trigger in n8n UI. |
| 06:00 | 07:00 | 60s | Explaining JSON payload structure. |
| 07:30 | 08:40 | 70s | Debugging a bad request error. |
| 09:30 | 10:30 | 60s | Setting up the audio transcription node. |
| 11:40 | 13:00 | 80s | Configuring the AI Agent system message. |
| 15:20 | 16:30 | 70s | Testing the text-based workflow path. |
| 17:30 | 18:30 | 60s | Setting up a bot via Telegram BotFather. |
| 19:20 | 20:20 | 60s | Navigating Google Cloud Console for API keys. |
| 23:10 | 24:10 | 60s | Explaining the Reddit data extraction nodes. |
| 25:20 | 26:20 | 60s | Explaining the HeyGen API HTTP request setup. |
| 27:00 | 28:45 | 105s | Conclusion; continuous full-screen talking head. |

## CTA Moments

### Mid-Roll CTAs
- **02:48 - 03:52**: Sponsor CTA. Hostinger integration tutorial. Verbal CTA: "visit hostinger.com/in/varun and use the coupon codes listed in the description to receive a discount." Visual: Hostinger UI on screen.

### End CTA
- None detected. The video ends with a sign-off.

## Summary Statistics
- **Total Chapters:** 8
- **Avg Chapter Duration:** 3.6 min
- **Total MG-Sparse Zones:** 11 (total 12.5 min)
- **Estimated Total Body MG Events:** 46
- **Overall Body MG Density:** ~1.6 MGs/minute
```

```json
{
  "bodyAnalysis": {
    "sectionTransitions": [
      {
        "timestamp": "00:50",
        "fromSection": "Intro",
        "toSection": "What is n8n?",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      },
      {
        "timestamp": "02:22",
        "fromSection": "What is n8n?",
        "toSection": "Core Concepts & Hosting",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      },
      {
        "timestamp": "03:59",
        "fromSection": "Core Concepts & Hosting",
        "toSection": "Workflow 1: Meeting Scheduler",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      },
      {
        "timestamp": "17:00",
        "fromSection": "Workflow 1: Meeting Scheduler",
        "toSection": "Getting API Keys",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      },
      {
        "timestamp": "20:54",
        "fromSection": "Getting API Keys",
        "toSection": "Community Templates",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      },
      {
        "timestamp": "22:48",
        "fromSection": "Community Templates",
        "toSection": "Workflow 2: Idea to Avatar",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      },
      {
        "timestamp": "26:49",
        "fromSection": "Workflow 2: Idea to Avatar",
        "toSection": "Conclusion",
        "transitionStyle": "Direct Cut",
        "audioCue": "Continuous speaking"
      }
    ],
    "ctaAnalysis": {
      "midRoll": [
        {
          "timestamp": "02:48",
          "type": "Sponsor",
          "description": "Hostinger sponsor segment with verbal CTA to visit link and use coupon code."
        }
      ],
      "end": []
    },
    "mgDensityByChapter": [
      {
        "chapterName": "Intro",
        "startTime": "00:00",
        "endTime": "00:50",
        "durationSeconds": 50,
        "estimatedMgCount": 8,
        "mgDensityPerMinute": 9.6
      },
      {
        "chapterName": "What is n8n?",
        "startTime": "00:50",
        "endTime": "02:22",
        "durationSeconds": 92,
        "estimatedMgCount": 5,
        "mgDensityPerMinute": 3.26
      },
      {
        "chapterName": "Core Concepts & Hosting",
        "startTime": "02:22",
        "endTime": "03:59",
        "durationSeconds": 97,
        "estimatedMgCount": 4,
        "mgDensityPerMinute": 2.47
      },
      {
        "chapterName": "Workflow 1: Meeting Scheduler",
        "startTime": "03:59",
        "endTime": "17:00",
        "durationSeconds": 781,
        "estimatedMgCount": 15,
        "mgDensityPerMinute": 1.15
      },
      {
        "chapterName": "Getting API Keys",
        "startTime": "17:00",
        "endTime": "20:54",
        "durationSeconds": 234,
        "estimatedMgCount": 5,
        "mgDensityPerMinute": 1.28
      },
      {
        "chapterName": "Community Templates",
        "startTime": "20:54",
        "endTime": "22:48",
        "durationSeconds": 114,
        "estimatedMgCount": 3,
        "mgDensityPerMinute": 1.58
      },
      {
        "chapterName": "Workflow 2: Idea to Avatar",
        "startTime": "22:48",
        "endTime": "26:49",
        "durationSeconds": 241,
        "estimatedMgCount": 6,
        "mgDensityPerMinute": 1.49
      },
      {
        "chapterName": "Conclusion",
        "startTime": "26:49",
        "endTime": "28:45",
        "durationSeconds": 116,
        "estimatedMgCount": 0,
        "mgDensityPerMinute": 0
      }
    ]
  }
}
```