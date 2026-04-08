# MG Body Sample Analysis: nick-saraev-claude-code-course

*6 sample windows analyzed at 0.5fps*

---

# Window 1: 03:00–05:00

```markdown
## Body Sample Window: 00:00 – 02:00

### Context
- **Section:** Setting up Claude Code (Pricing, Account Creation, Documentation)
- **Primary Layout:** screen-share-with-pip
- **PiP State:** on (bottom-left)

### Pacing Metrics
- **MG Events:** 1 | **Transitions:** 8
- **MG Spacing:** N/A (only one event)
- **Cuts/min:** 4.0
- **Zoom Events:** 0

### Motion Graphic Events (1 total)

#### 1. Chapter Title Card
- **Timestamp:** 00:00.000 – 00:03.000
- **Duration:** 3.000s
- **Type:** Chapter Card
- **Visual Description:** A minimalist title card featuring a solid black background. Centered on the screen is the text "Setting up Claude Code." in a bold, sans-serif font (likely Inter or Helvetica Neue), colored pure white.
- **Choreography:**
  1. `00:00.000`: Text and background appear immediately at the start of the video.
  2. `00:03.000`: Hard cuts to the screen share layout.
- **Transcript Correlation:** "So the first thing we have to do is we actually have to purchase Claude Code."
- **Design Elements:**
  - **Typography:** Bold, sans-serif, white (#FFFFFF).
  - **Background:** Solid black (#000000).

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 00:03.000 | Hard Cut | 0.000s | Cut from chapter card to screen share (Pricing page) with PiP. | None |
| 2 | 00:44.130 | Hard Cut | 0.000s | Cut to Anthropic login page. | None |
| 3 | 00:48.200 | Hard Cut | 0.000s | Cut to "Let's create your account" page. | None |
| 4 | 00:55.230 | Hard Cut | 0.000s | Cut to "When is your birthday?" page. | None |
| 5 | 01:02.030 | Hard Cut | 0.000s | Cut to Canadian Pricing page. | None |
| 6 | 01:13.230 | Hard Cut | 0.000s | Cut to Stripe checkout page. | None |
| 7 | 01:16.130 | Hard Cut | 0.000s | Cut to Claude dashboard. | None |
| 8 | 01:21.130 | Hard Cut | 0.000s | Cut to Claude Code Docs page. | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| - | - | - | - | - | - |
*(No digital zoom events detected in this window; all scale changes are native browser zooms or hard cuts to pre-scaled recordings)*

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00.000 – 00:03.000 | full-frame-mg | Chapter title card. |
| 00:03.000 – 02:00.000 | screen-share-with-pip | Browser screen share. Speaker PiP is a rounded rectangle in the bottom-left corner with a subtle drop shadow. |

### MG Spacing Log
*(Only one MG event in this window)*

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| Chapter Card | 1 | 3.000s |

### Spacing Statistics
- **Overall:** N/A (insufficient data for spacing in this window)
- **By Layout:** screen-share: N/A, speaker-return: N/A

### Transition Type Frequency
| Type | Count |
|------|-------|
| Hard Cut | 8 |

### PiP Toggle Pattern
The PiP remains strictly **ON** during all screen share segments. It is positioned consistently in the bottom-left corner, utilizing a rounded rectangle mask to blend cleanly with the background content.

### Speaker Return Cadence
- Min: N/A | Max: N/A | Avg: N/A between speaker returns (No full-frame speaker returns in this 2-minute window).

### Zoom Patterns
- Frequency: 0 zooms per minute of screen share
- Typical factor: N/A
- Common easing: N/A
```

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "windowRange": "00:00 - 02:00",
        "context": {
          "section": "Setting up Claude Code (Pricing, Account Creation, Documentation)",
          "primaryLayout": "screen-share-with-pip",
          "pipState": "on"
        },
        "pacingMetrics": {
          "mgEventsCount": 1,
          "transitionsCount": 8,
          "mgSpacing": {
            "min": 0,
            "max": 0,
            "avg": 0
          },
          "cutsPerMinute": 4.0,
          "zoomEventsCount": 0
        },
        "motionGraphicEvents": [
          {
            "id": "mg-body-1",
            "timestamp": "00:00.000 - 00:03.000",
            "duration": 3.000,
            "type": "Chapter Card",
            "visualDescription": "A minimalist title card featuring a solid black background. Centered on the screen is the text 'Setting up Claude Code.' in a bold, sans-serif font, colored pure white.",
            "choreography": [
              "00:00.000: Text and background appear immediately at the start of the video.",
              "00:03.000: Hard cuts to the screen share layout."
            ],
            "transcriptCorrelation": "So the first thing we have to do is we actually have to purchase Claude Code.",
            "designElements": {
              "typography": "Bold, sans-serif, white (#FFFFFF)",
              "colorPalette": ["#000000", "#FFFFFF"],
              "layout": "Centered text on solid background"
            }
          }
        ],
        "transitions": [
          {
            "id": "trans-body-1",
            "timestamp": "00:03.000",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut from chapter card to screen share (Pricing page) with PiP.",
            "sfx": "None"
          },
          {
            "id": "trans-body-2",
            "timestamp": "00:44.130",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to Anthropic login page.",
            "sfx": "None"
          },
          {
            "id": "trans-body-3",
            "timestamp": "00:48.200",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to 'Let's create your account' page.",
            "sfx": "None"
          },
          {
            "id": "trans-body-4",
            "timestamp": "00:55.230",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to 'When is your birthday?' page.",
            "sfx": "None"
          },
          {
            "id": "trans-body-5",
            "timestamp": "01:02.030",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to Canadian Pricing page.",
            "sfx": "None"
          },
          {
            "id": "trans-body-6",
            "timestamp": "01:13.230",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to Stripe checkout page.",
            "sfx": "None"
          },
          {
            "id": "trans-body-7",
            "timestamp": "01:16.130",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to Claude dashboard.",
            "sfx": "None"
          },
          {
            "id": "trans-body-8",
            "timestamp": "01:21.130",
            "type": "Hard Cut",
            "duration": 0.000,
            "description": "Cut to Claude Code Docs page.",
            "sfx": "None"
          }
        ],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "timeRange": "00:00.000 - 00:03.000",
            "layout": "full-frame-mg",
            "notes": "Chapter title card."
          },
          {
            "timeRange": "00:03.000 - 02:00.000",
            "layout": "screen-share-with-pip",
            "notes": "Browser screen share. Speaker PiP is a rounded rectangle in the bottom-left corner with a subtle drop shadow."
          }
        ],
        "mgSpacingLog": []
      }
    ],
    "bodyMGPatterns": {
      "mgTypeDistribution": {
        "Chapter Card": {
          "count": 1,
          "avgDuration": 3.000
        }
      },
      "spacingStatistics": {
        "overall": {
          "min": 0,
          "max": 0,
          "avg": 0
        },
        "byLayout": {
          "screen-share": {
            "avg": 0
          },
          "speaker-return": {
            "avg": 0
          }
        }
      },
      "transitionTypeFrequency": {
        "Hard Cut": 8
      },
      "pipTogglePattern": "The PiP remains strictly ON during all screen share segments. It is positioned consistently in the bottom-left corner, utilizing a rounded rectangle mask.",
      "speakerReturnCadence": {
        "min": 0,
        "max": 0,
        "avg": 0
      },
      "zoomPatterns": {
        "frequencyPerMinute": 0,
        "typicalFactor": 0,
        "commonEasing": "N/A"
      }
    }
  }
}
```

---

# Window 2: 30:00–32:00

```markdown
## Body Sample Window: 30:00 – 32:00

### Context
- **Section:** Workflow Standardization and Design Methodologies
- **Primary Layout:** screen-share-with-pip
- **PiP State:** on (persistent, bottom-left corner)

### Pacing Metrics
- **MG Events:** 0 | **Transitions:** 3
- **MG Spacing:** N/A (0 post-production MGs in this window)
- **Cuts/min:** 1.5
- **Zoom Events:** 0 (post-production), multiple in-app canvas pans/zooms

### Motion Graphic Events (0 total)

*Note: This specific 2-minute window relies entirely on screen-share content switching and native application interactions (scrolling, Excalidraw canvas panning) rather than post-production motion graphics or overlays.*

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 00:50 | Hard Cut | 0s | Switches from VS Code (`CLAUDE.md`) to a full-screen browser showing an Excalidraw whiteboard diagram. | None |
| 2 | 01:35 | Hard Cut | 0s | Switches from Excalidraw to a browser tab showing the "Acctual" website. | None |
| 3 | 01:52 | Hard Cut | 0s | Switches from the "Acctual" website to a browser tab showing the "LeftClick" website. | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| - | - | - | - | - | - |

*Note: No post-production digital zooms are applied in this window. The user natively zooms and pans within the Excalidraw web application from 00:50 to 01:35.*

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00 - 00:50 | screen-share-with-pip | VS Code showing `CLAUDE.md` file. Speaker PiP in bottom left. |
| 00:50 - 01:35 | screen-share-with-pip | Browser showing Excalidraw diagram ("The way CLAUDE.md affects your prompts"). Speaker PiP in bottom left. |
| 01:35 - 01:52 | screen-share-with-pip | Browser showing "Acctual" inspiration website. Speaker scrolls down. Speaker PiP in bottom left. |
| 01:52 - 02:00 | screen-share-with-pip | Browser showing "LeftClick" website. Speaker scrolls down. Speaker PiP in bottom left. |

### MG Spacing Log
- N/A

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| N/A | 0 | 0s |

### Spacing Statistics
- **Overall:** N/A (No post-production MGs in this sample)
- **By Layout:** screen-share: N/A, speaker-return: N/A

### Transition Type Frequency
| Type | Count |
|------|-------|
| Hard Cut | 3 |

### PiP Toggle Pattern
The PiP remains strictly **ON** and locked to the bottom-left corner for the entirety of this 2-minute window. The creator uses the screen share as the primary visual driver, relying on changing the on-screen application rather than toggling the camera full-screen.

### Speaker Return Cadence
- Min: N/A | Max: N/A | Avg: N/A (0 full-screen speaker returns in this window)

### Zoom Patterns
- Frequency: 0 post-production zooms per minute.
- Typical factor: N/A
- Common easing: N/A
- *Observation:* The creator prefers to use native application zooming (e.g., inside Excalidraw) rather than applying digital zooms in the editing timeline during this segment.
```

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "windowRange": "30:00-32:00",
        "context": {
          "section": "Workflow Standardization and Design Methodologies",
          "primaryLayout": "screen-share-with-pip",
          "pipState": "on"
        },
        "pacingMetrics": {
          "mgEventsCount": 0,
          "transitionsCount": 3,
          "cutsPerMinute": 1.5,
          "zoomEventsCount": 0
        },
        "motionGraphicEvents": [],
        "transitions": [
          {
            "id": 1,
            "timestamp": "00:50",
            "type": "Hard Cut",
            "duration": "0s",
            "description": "Switches from VS Code to Excalidraw whiteboard.",
            "sfx": "None"
          },
          {
            "id": 2,
            "timestamp": "01:35",
            "type": "Hard Cut",
            "duration": "0s",
            "description": "Switches from Excalidraw to Acctual website.",
            "sfx": "None"
          },
          {
            "id": 3,
            "timestamp": "01:52",
            "type": "Hard Cut",
            "duration": "0s",
            "description": "Switches from Acctual website to LeftClick website.",
            "sfx": "None"
          }
        ],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "timeRange": "00:00-00:50",
            "layout": "screen-share-with-pip",
            "notes": "VS Code showing CLAUDE.md"
          },
          {
            "timeRange": "00:50-01:35",
            "layout": "screen-share-with-pip",
            "notes": "Excalidraw diagram"
          },
          {
            "timeRange": "01:35-01:52",
            "layout": "screen-share-with-pip",
            "notes": "Acctual website"
          },
          {
            "timeRange": "01:52-02:00",
            "layout": "screen-share-with-pip",
            "notes": "LeftClick website"
          }
        ],
        "mgSpacingLog": []
      }
    ]
  },
  "bodyMGPatterns": {
    "mgTypeDistribution": [],
    "spacingStatistics": {
      "overall": {
        "min": null,
        "max": null,
        "avg": null
      },
      "byLayout": {
        "screenShare": null,
        "speakerReturn": null
      }
    },
    "transitionTypeFrequency": [
      {
        "type": "Hard Cut",
        "count": 3
      }
    ],
    "pipTogglePattern": "Persistent ON state in the bottom-left corner.",
    "speakerReturnCadence": {
      "min": null,
      "max": null,
      "avg": null
    },
    "zoomPatterns": {
      "frequency": 0,
      "typicalFactor": null,
      "commonEasing": null
    }
  }
}
```

---

# Window 3: 1:00:00–1:02:00

```markdown
## Body Sample Window: 1:00:00 – 1:02:00

### Context
- **Section:** Chapter boundary — first hour mark (Rules Configuration)
- **Primary Layout:** screen-share-with-pip
- **PiP State:** on (bottom left)

### Pacing Metrics
- **MG Events:** 0 | **Transitions:** 2
- **MG Spacing:** N/A
- **Cuts/min:** 1.0
- **Zoom Events:** 0

### Motion Graphic Events (0 total)

*(No post-production motion graphics, text overlays, or highlights were added in this window. All visual changes are native to the screen-recorded applications.)*

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 00:06.000 | Cut | 0.0s | Hard cut from Excalidraw browser window to VS Code application. | None |
| 2 | 01:46.000 | Cut | 0.0s | Hard cut from VS Code application back to Excalidraw browser window. | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
*(No digital zooms detected in this window)*

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00.000 - 00:06.000 | screen-share-with-pip | Browser showing Excalidraw diagram about scoped rules. Speaker PiP bottom left. |
| 00:06.000 - 01:46.000 | screen-share-with-pip | VS Code showing Claude Code terminal and markdown files. Speaker PiP bottom left. |
| 01:46.000 - 02:00.000 | screen-share-with-pip | Browser showing Excalidraw diagram about CLAUDE.md effects. Speaker PiP bottom left. |

### MG Spacing Log
*(No MG events to measure)*

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| None | 0 | 0s |

### Spacing Statistics
- **Overall:** N/A
- **By Layout:** screen-share: N/A, speaker-return: N/A

### Transition Type Frequency
| Type | Count |
|------|-------|
| Hard Cut | 2 |

### PiP Toggle Pattern
The PiP remains constantly visible in the bottom left corner throughout the entire segment, with no toggling or repositioning.

### Speaker Return Cadence
- Min: N/A | Max: N/A | Avg: N/A between speaker returns (No full-frame speaker returns in this window).

### Zoom Patterns
- Frequency: 0 zooms per minute of screen share
- Typical factor: N/A
- Common easing: N/A
```

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "start": "1:00:00",
        "end": "1:02:00",
        "context": {
          "section": "Chapter boundary — first hour mark",
          "primaryLayout": "screen-share-with-pip",
          "pipState": "on"
        },
        "pacingMetrics": {
          "mgEventsCount": 0,
          "transitionsCount": 2,
          "mgSpacing": {
            "min": null,
            "max": null,
            "avg": null
          },
          "cutsPerMinute": 1.0,
          "zoomEventsCount": 0
        },
        "motionGraphicEvents": [],
        "transitions": [
          {
            "id": 1,
            "timestamp": "00:06.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from Excalidraw browser window to VS Code application.",
            "sfx": "None"
          },
          {
            "id": 2,
            "timestamp": "01:46.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from VS Code application back to Excalidraw browser window.",
            "sfx": "None"
          }
        ],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "timeRange": "00:00.000 - 00:06.000",
            "layout": "screen-share-with-pip",
            "notes": "Browser showing Excalidraw diagram about scoped rules. Speaker PiP bottom left."
          },
          {
            "timeRange": "00:06.000 - 01:46.000",
            "layout": "screen-share-with-pip",
            "notes": "VS Code showing Claude Code terminal and markdown files. Speaker PiP bottom left."
          },
          {
            "timeRange": "01:46.000 - 02:00.000",
            "layout": "screen-share-with-pip",
            "notes": "Browser showing Excalidraw diagram about CLAUDE.md effects. Speaker PiP bottom left."
          }
        ],
        "mgSpacingLog": []
      }
    ],
    "bodyMGPatterns": {
      "mgTypeDistribution": [],
      "spacingStatistics": {
        "overall": {
          "min": null,
          "max": null,
          "avg": null
        },
        "byLayout": {
          "screenShare": null,
          "speakerReturn": null
        }
      },
      "transitionTypeFrequency": [
        {
          "type": "Hard Cut",
          "count": 2
        }
      ],
      "pipTogglePattern": "The PiP remains constantly visible in the bottom left corner throughout the entire segment, with no toggling or repositioning.",
      "speakerReturnCadence": {
        "min": null,
        "max": null,
        "avg": null
      },
      "zoomPatterns": {
        "frequency": 0,
        "typicalFactor": null,
        "commonEasing": null
      }
    }
  }
}
```

---

# Window 4: 2:00:00–2:02:00

```markdown
## Body Sample Window: 00:00 – 02:00

### Context
- **Section:** Mid-course section
- **Primary Layout:** screen-share-with-pip
- **PiP State:** on

### Pacing Metrics
- **MG Events:** 1 | **Transitions:** 4
- **MG Spacing:** min 0s, max 0s, avg 0s
- **Cuts/min:** 2
- **Zoom Events:** 0

### Motion Graphic Events (1 total)

#### 1. Prompt Chat Bubble Overlay
- **Timestamp:** 00:16.000 – 01:41.000
- **Duration:** 85.000s
- **Type:** text-overlay
- **Description:** A dark grey, rounded-rectangle chat bubble appears in the bottom right corner of the screen, overlaying the screen share. It contains white text representing a prompt or feedback the speaker is dictating. The text updates and expands several times throughout its duration, simulating a live transcription or prompt building process.
- **Visual Properties:**
  - **Shape:** Rounded rectangle
  - **Color:** Dark grey background, white text
  - **Position:** Bottom right quadrant
  - **Animation:** Slight fade/slide up on initial appearance. Subsequent text additions appear instantly.
- **State Changes:**
  - **00:16.000:** Appears with text: "I don't like how the text immediately under your problem areas is really constrained width-wise. You should make that a little longer, maybe two times as wide."
  - **00:46.000:** Text updates to include: "In each of the sub-benefits underneath 01, 02, 03, 04, it's a little too wide now, so make that maybe 75% as wide. Do the same thing with the text under your solution."
  - **00:58.000:** Text updates to include: "Under "Why Us" looks great. I want to have that image of myself, Alex Hormozi, and Sam Ovens in there somewhere, so find a way to include the image in a high-quality manner."
  - **01:16.000:** Text updates to include: "There's some minor spacing problems with the "We've done this before", "We focus on money", and "We don't treat AI as a fad." They're not perfectly lined up to the numbers 1, 2, 3 on the left-hand side."
  - **01:35.000:** Text updates to include: "Add some images of myself and Noah. The "What You're Investing" looks pretty clean."
  - **01:41.000:** Disappears abruptly upon a hard cut to a different screen share.

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 01:38.000 | Cut | 0.000s | Hard cut from browser window to VS Code editor. | None |
| 2 | 01:41.000 | Cut | 0.000s | Hard cut from VS Code editor back to browser window. | None |
| 3 | 01:53.000 | Cut | 0.000s | Hard cut from proposal page to Stripe checkout page. | None |
| 4 | 01:58.000 | Cut | 0.000s | Hard cut from Stripe checkout page to payment confirmation page. | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| - | - | - | - | - | - |

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00.000 - 01:38.000 | screen-share-with-pip | Browser showing 1SecondCopy proposal. PiP in bottom left. |
| 01:38.000 - 01:41.000 | screen-share-with-pip | VS Code editor. PiP in bottom left. |
| 01:41.000 - 02:00.000 | screen-share-with-pip | Browser showing proposal signing, then Stripe checkout. PiP in bottom left. |

### MG Spacing Log
0

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| text-overlay | 1 | 85.000s |

### Spacing Statistics
- **Overall:** min 0s, max 0s, avg 0s between MG events
- **By Layout:** screen-share: avg 0s, speaker-return: avg 0s

### Transition Type Frequency
| Type | Count |
|------|-------|
| Cut | 4 |

### PiP Toggle Pattern
The PiP remains consistently on throughout the entire sample window, positioned in the bottom left corner.

### Speaker Return Cadence
- Min: 0s | Max: 0s | Avg: 0s between speaker returns (No speaker returns in this window).

### Zoom Patterns
- Frequency: 0 zooms per minute of screen share
- Typical factor: N/A
- Common easing: N/A
```

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "start": "00:00",
        "end": "02:00",
        "context": {
          "section": "Mid-course section",
          "primaryLayout": "screen-share-with-pip",
          "pipState": "on"
        },
        "pacingMetrics": {
          "mgEvents": 1,
          "transitions": 4,
          "mgSpacing": {
            "min": 0,
            "max": 0,
            "avg": 0
          },
          "cutsPerMin": 2,
          "zoomEvents": 0
        },
        "motionGraphicEvents": [
          {
            "id": "mg-b1-1",
            "timestamp": "00:16.000",
            "duration": 85.0,
            "type": "text-overlay",
            "description": "A dark grey, rounded-rectangle chat bubble appears in the bottom right corner of the screen, overlaying the screen share. It contains white text representing a prompt or feedback the speaker is dictating. The text updates and expands several times throughout its duration.",
            "visualProperties": {
              "shape": "Rounded rectangle",
              "color": "Dark grey background, white text",
              "position": "Bottom right quadrant",
              "animation": "Slight fade/slide up on initial appearance. Subsequent text additions appear instantly."
            }
          }
        ],
        "transitions": [
          {
            "id": "tr-b1-1",
            "timestamp": "01:38.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from browser window to VS Code editor.",
            "sfx": "None"
          },
          {
            "id": "tr-b1-2",
            "timestamp": "01:41.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from VS Code editor back to browser window.",
            "sfx": "None"
          },
          {
            "id": "tr-b1-3",
            "timestamp": "01:53.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from proposal page to Stripe checkout page.",
            "sfx": "None"
          },
          {
            "id": "tr-b1-4",
            "timestamp": "01:58.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from Stripe checkout page to payment confirmation page.",
            "sfx": "None"
          }
        ],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "timeRange": "00:00.000 - 01:38.000",
            "layout": "screen-share-with-pip",
            "notes": "Browser showing 1SecondCopy proposal. PiP in bottom left."
          },
          {
            "timeRange": "01:38.000 - 01:41.000",
            "layout": "screen-share-with-pip",
            "notes": "VS Code editor. PiP in bottom left."
          },
          {
            "timeRange": "01:41.000 - 02:00.000",
            "layout": "screen-share-with-pip",
            "notes": "Browser showing proposal signing, then Stripe checkout. PiP in bottom left."
          }
        ],
        "mgSpacingLog": [
          0
        ]
      }
    ],
    "bodyMGPatterns": {
      "mgTypeDistribution": {
        "text-overlay": {
          "count": 1,
          "avgDuration": 85.0
        }
      },
      "spacingStatistics": {
        "overall": {
          "min": 0,
          "max": 0,
          "avg": 0
        },
        "byLayout": {
          "screen-share": {
            "avg": 0
          },
          "speaker-return": {
            "avg": 0
          }
        }
      },
      "transitionTypeFrequency": {
        "Cut": 4
      },
      "pipTogglePattern": "The PiP remains consistently on throughout the entire sample window, positioned in the bottom left corner.",
      "speakerReturnCadence": {
        "min": 0,
        "max": 0,
        "avg": 0
      },
      "zoomPatterns": {
        "frequency": 0,
        "typicalFactor": 0,
        "commonEasing": "N/A"
      }
    }
  }
}
```

---

# Window 5: 3:30:00–3:32:00

## Body Sample Window: 00:00 – 02:00

*(Note: Timestamps are relative to the provided 2-minute video file, which corresponds to the 3:30:00 – 3:32:00 window of the original video).*

### Context
- **Section:** Late body — advanced content (Comparing Subagents and Agent teams)
- **Primary Layout:** screen-share-with-pip
- **PiP State:** mixed (on, then off)

### Pacing Metrics
- **MG Events:** 0 | **Transitions:** 1
- **MG Spacing:** N/A
- **Cuts/min:** 0.5
- **Zoom Events:** 0

### Motion Graphic Events (0 total)

*Note: There are no post-production motion graphics in this window. The annotations (lines, underlines, plus signs) appearing on the screen are drawn live by the speaker using the Excalidraw application's built-in tools, as evidenced by the visible Excalidraw UI and the real-time cursor movement. The panning across the canvas is also an in-app action, not a post-production digital zoom or pan.*

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 01:53.500 | Cut | 0.000s | Cut from screen-share-with-pip to full-frame speaker | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| - | - | - | - | - | - |

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00.000 - 01:53.500 | screen-share-with-pip | Browser showing Excalidraw. Speaker is panning the canvas and drawing live annotations. PiP is in the bottom left corner. |
| 01:53.500 - 02:00.000 | full-frame-speaker | Speaker talking directly to the camera. |

### MG Spacing Log
N/A

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| N/A | 0 | 0s |

### Spacing Statistics
- **Overall:** min N/As, max N/As, avg N/As between MG events
- **By Layout:** screen-share: avg N/As, speaker-return: avg N/As

### Transition Type Frequency
| Type | Count |
|------|-------|
| Cut | 1 |

### PiP Toggle Pattern
PiP is active during the screen share segment, positioned in the bottom left corner. It disappears entirely when the video cuts to a full-frame speaker shot.

### Speaker Return Cadence
- Min: N/As | Max: N/As | Avg: N/As between speaker returns (Only one return occurred in this sample window).

### Zoom Patterns
- Frequency: 0 zooms per minute of screen share
- Typical factor: N/A
- Common easing: N/A

---

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "windowId": "3:30:00-3:32:00",
        "start": "00:00.000",
        "end": "02:00.000",
        "context": "Late body — advanced content",
        "primaryLayout": "screen-share-with-pip",
        "pipState": "mixed",
        "pacingMetrics": {
          "mgEvents": 0,
          "transitions": 1,
          "cutsPerMin": 0.5,
          "zoomEvents": 0
        },
        "motionGraphics": [],
        "transitions": [
          {
            "id": 1,
            "timestamp": "01:53.500",
            "type": "Cut",
            "duration": 0.0,
            "description": "Cut from screen-share-with-pip to full-frame speaker",
            "sfx": "None"
          }
        ],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "start": "00:00.000",
            "end": "01:53.500",
            "layout": "screen-share-with-pip",
            "notes": "Browser showing Excalidraw. Speaker is panning the canvas and drawing live annotations. PiP is in the bottom left corner."
          },
          {
            "start": "01:53.500",
            "end": "02:00.000",
            "layout": "full-frame-speaker",
            "notes": "Speaker talking directly to the camera."
          }
        ],
        "mgSpacingLog": []
      }
    ],
    "bodyMGPatterns": {
      "mgTypeDistribution": {},
      "spacingStatistics": {
        "overall": {
          "min": null,
          "max": null,
          "avg": null
        },
        "byLayout": {
          "screen-share": null,
          "speaker-return": null
        }
      },
      "transitionTypeFrequency": {
        "Cut": 1
      },
      "pipTogglePattern": "PiP is active during the screen share segment, positioned in the bottom left corner. It disappears entirely when the video cuts to a full-frame speaker shot.",
      "speakerReturnCadence": {
        "min": null,
        "max": null,
        "avg": null
      },
      "zoomPatterns": {
        "frequency": 0,
        "typicalFactor": null,
        "commonEasing": null
      }
    }
  }
}
```

---

# Window 6: 4:05:00–4:11:35

```markdown
## Body Sample Window: 0:00 – 5:43

### Context
- **Section:** Deploying to Modal and Closing CTA
- **Primary Layout:** screen-share-with-pip
- **PiP State:** mixed (on during screen share, off during full-frame speaker)

### Pacing Metrics
- **MG Events:** 0 | **Transitions:** 3
- **MG Spacing:** min 0s, max 0s, avg 0s
- **Cuts/min:** 0.52
- **Zoom Events:** 0

### Motion Graphic Events (0 total)

*(No motion graphic overlays were used in this segment. The visual presentation relies entirely on screen recording and camera footage.)*

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 1:39.83 | hard cut | 0s | Cut from screen share with PiP to full-frame speaker | none |
| 2 | 1:49.95 | hard cut | 0s | Cut from full-frame speaker back to screen share with PiP | none |
| 3 | 4:49.83 | hard cut | 0s | Cut from screen share with PiP to full-frame speaker for closing | none |

### Zoom Events

*(No digital zoom events were used in this segment.)*

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 0:00 – 1:39.83 | screen-share-with-pip | Demonstrating web app and Modal website |
| 1:39.83 – 1:49.95 | full-frame-speaker | Speaker addressing camera directly regarding Modal credits |
| 1:49.95 – 4:49.83 | screen-share-with-pip | Modal dashboard, VS Code terminal, and Scrape Leads app demonstration |
| 4:49.83 – 5:43.00 | full-frame-speaker | Closing remarks and call to action for Maker School |

### MG Spacing Log
*(N/A - No MG events)*

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| N/A | 0 | 0s |

### Spacing Statistics
- **Overall:** min 0s, max 0s, avg 0s between MG events
- **By Layout:** screen-share: avg 0s, speaker-return: avg 0s

### Transition Type Frequency
| Type | Count |
|------|-------|
| hard cut | 3 |

### PiP Toggle Pattern
The PiP is strictly tied to the screen share layout. It is always visible in the bottom-left corner when the screen is being shared, and it disappears completely when the edit cuts to the full-frame A-roll camera. There are no instances of the PiP toggling on or off while remaining in the screen share layout.

### Speaker Return Cadence
- Min: 180s | Max: 180s | Avg: 180s between speaker returns (based on the single return interval in this clip)

### Zoom Patterns
- Frequency: 0 zooms per minute of screen share
- Typical factor: 1.0x
- Common easing: N/A
```

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "windowRange": "0:00 - 5:43",
        "sectionContext": "Deploying to Modal and Closing CTA",
        "primaryLayout": "screen-share-with-pip",
        "pipState": "mixed",
        "pacingMetrics": {
          "mgEventsCount": 0,
          "transitionsCount": 3,
          "mgSpacing": {
            "min": 0,
            "max": 0,
            "avg": 0
          },
          "cutsPerMinute": 0.52,
          "zoomEventsCount": 0
        },
        "motionGraphicEvents": [],
        "transitions": [
          {
            "id": "trans-1",
            "timestamp": "1:39.83",
            "type": "hard cut",
            "duration": 0,
            "description": "Cut from screen share to full frame speaker",
            "sfx": "none"
          },
          {
            "id": "trans-2",
            "timestamp": "1:49.95",
            "type": "hard cut",
            "duration": 0,
            "description": "Cut from full frame speaker to screen share",
            "sfx": "none"
          },
          {
            "id": "trans-3",
            "timestamp": "4:49.83",
            "type": "hard cut",
            "duration": 0,
            "description": "Cut from screen share to full frame speaker",
            "sfx": "none"
          }
        ],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "timeRange": "0:00 - 1:39.83",
            "layout": "screen-share-with-pip",
            "notes": "VS Code and Browser"
          },
          {
            "timeRange": "1:39.83 - 1:49.95",
            "layout": "full-frame-speaker",
            "notes": "Speaker talking to camera"
          },
          {
            "timeRange": "1:49.95 - 4:49.83",
            "layout": "screen-share-with-pip",
            "notes": "Modal dashboard, VS Code, Browser"
          },
          {
            "timeRange": "4:49.83 - 5:43.00",
            "layout": "full-frame-speaker",
            "notes": "Closing remarks and CTA"
          }
        ],
        "mgSpacingLog": []
      }
    ]
  },
  "bodyMGPatterns": {
    "mgTypeDistribution": [],
    "spacingStatistics": {
      "overall": {
        "min": 0,
        "max": 0,
        "avg": 0
      },
      "byLayout": {
        "screenShare": 0,
        "speakerReturn": 0
      }
    },
    "transitionTypeFrequency": [
      {
        "type": "hard cut",
        "count": 3
      }
    ],
    "pipTogglePattern": "PiP is visible during all screen share segments and hidden during full-frame speaker segments.",
    "speakerReturnCadence": {
      "min": 180,
      "max": 180,
      "avg": 180
    },
    "zoomPatterns": {
      "frequency": 0,
      "typicalFactor": 1,
      "commonEasing": "none"
    }
  }
}
```