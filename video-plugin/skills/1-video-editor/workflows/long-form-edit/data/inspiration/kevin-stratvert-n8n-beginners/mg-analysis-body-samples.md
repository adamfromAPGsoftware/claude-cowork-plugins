# MG Body Sample Analysis: kevin-stratvert-n8n-beginners

*3 sample windows analyzed at 0.5fps*

---

# Window 1: 01:30–03:30

```markdown
## Body Sample Window: 00:00 – 02:00

### Context
- **Section:** Getting started with n8n and Docker installation
- **Primary Layout:** full-frame-screen-share
- **PiP State:** off (speaker appears full-frame during returns)

### Pacing Metrics
- **MG Events:** 4 | **Transitions:** 7
- **MG Spacing:** min 5.0s, max 55.0s, avg 23.3s
- **Cuts/min:** 3.5
- **Zoom Events:** 4

### Motion Graphic Events (4 total)

**1. "n8n.io" Lower Third**
- **Timestamp:** 00:20.000 – 00:25.000
- **Duration:** 5.0s
- **Type:** Lower Third
- **Design:** White text "n8n.io" on a solid blue rectangular background with an orange/blue gradient accent bar on the left edge.
- **Animation:** Slides up from the bottom edge with a smooth ease-out. Slides down to exit.
- **Transcript:** "Now we're going to build an AI agent in n8n."

**2. "Docker Desktop" Lower Third**
- **Timestamp:** 00:35.000 – 00:45.000
- **Duration:** 10.0s
- **Type:** Lower Third
- **Design:** White text "docker.com/products/docker-desktop" on a solid blue rectangular background with an orange/blue gradient accent bar.
- **Animation:** Slides up from the bottom edge. Cuts out with the scene change.
- **Transcript:** "First go to the Docker Desktop website. You can find the link in the description below."

**3. URL Highlight Box**
- **Timestamp:** 01:40.000 – 01:43.000
- **Duration:** 3.0s
- **Type:** Annotation (Highlight)
- **Design:** Semi-transparent yellow rectangular highlight box placed directly over the text `http://localhost:5678` in the command prompt.
- **Animation:** Fades in quickly (0.2s).
- **Transcript:** "Well it means you can copy and paste this link..."

**4. "Create Workflow" UI Highlight**
- **Timestamp:** 01:56.000 – 02:00.000
- **Duration:** 4.0s
- **Type:** Annotation (Outline)
- **Design:** Red rectangular outline with rounded corners, highlighting the "Create Workflow" button in the top right of the n8n UI.
- **Animation:** Draws on from the top-left corner clockwise.
- **Transcript:** "In the top right you'll see you can create a new workflow..."

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 00:01.500 | Cut | 0.0s | Split screen to full-frame speaker | None |
| 2 | 00:19.500 | Cut | 0.0s | Speaker to n8n.io website screen share | None |
| 3 | 00:24.000 | Cut | 0.0s | n8n.io website to n8n dashboard | None |
| 4 | 00:30.000 | Cut | 0.0s | Screen share to full-frame speaker | None |
| 5 | 00:34.500 | Cut | 0.0s | Speaker to Docker website screen share | None |
| 6 | 00:45.000 | Cut | 0.0s | Docker website to Windows Desktop | None |
| 7 | 01:43.000 | Cut | 0.0s | Command prompt to web browser | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| 1 | 00:40.000 | 1.5x | Center | 0.5s | Ease In/Out |
| 2 | 01:00.000 | 1.8x | Top Left | 0.5s | Ease In/Out |
| 3 | 01:08.000 | 1.5x | Bottom Center | 0.5s | Ease In/Out |
| 4 | 01:15.000 | 1.3x | Center | 0.5s | Ease In/Out |

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00.000 - 00:01.500 | split-screen | Graphic left, speaker right |
| 00:01.500 - 00:19.500 | full-frame-speaker | Speaker talking directly to camera |
| 00:19.500 - 00:30.000 | full-frame-screen-share | n8n website and dashboard |
| 00:30.000 - 00:34.500 | full-frame-speaker | Speaker transition |
| 00:34.500 - 02:00.000 | full-frame-screen-share | Docker install, CMD, n8n setup |

### MG Spacing Log
- 10.0s (between Lower Third 1 and Lower Third 2)
- 55.0s (between Lower Third 2 and URL Highlight)
- 13.0s (between URL Highlight and UI Highlight)

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| Lower Third | 2 | 7.5s |
| Annotation | 2 | 3.5s |

### Spacing Statistics
- **Overall:** min 10.0s, max 55.0s, avg 26.0s between MG events
- **By Layout:** screen-share: avg 26.0s

### Transition Type Frequency
| Type | Count |
|------|-------|
| Cut | 7 |

### PiP Toggle Pattern
The creator does not use a Picture-in-Picture (PiP) overlay during screen shares in this segment. Instead, he relies entirely on full-frame screen shares and cuts back to a full-frame camera view to re-engage the viewer.

### Speaker Return Cadence
- Min: 10.5s | Max: 10.5s | Avg: 10.5s between speaker returns (only one return in this window at 00:30).

### Zoom Patterns
- Frequency: 2.0 zooms per minute of screen share
- Typical factor: 1.5x
- Common easing: Ease In/Out
```

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "windowRange": "00:00 - 02:00",
        "context": {
          "section": "Getting started with n8n and Docker installation",
          "primaryLayout": "full-frame-screen-share",
          "pipState": "off"
        },
        "pacingMetrics": {
          "mgEventsCount": 4,
          "transitionsCount": 7,
          "mgSpacing": {
            "min": 10.0,
            "max": 55.0,
            "avg": 26.0
          },
          "cutsPerMinute": 3.5,
          "zoomEventsCount": 4
        },
        "motionGraphicEvents": [
          {
            "id": 1,
            "timestamp": "00:20.000 - 00:25.000",
            "duration": 5.0,
            "type": "Lower Third",
            "design": "White text 'n8n.io' on a solid blue rectangular background with an orange/blue gradient accent bar on the left edge.",
            "animation": "Slides up from the bottom edge with a smooth ease-out. Slides down to exit.",
            "transcript": "Now we're going to build an AI agent in n8n."
          },
          {
            "id": 2,
            "timestamp": "00:35.000 - 00:45.000",
            "duration": 10.0,
            "type": "Lower Third",
            "design": "White text 'docker.com/products/docker-desktop' on a solid blue rectangular background with an orange/blue gradient accent bar.",
            "animation": "Slides up from the bottom edge. Cuts out with the scene change.",
            "transcript": "First go to the Docker Desktop website. You can find the link in the description below."
          },
          {
            "id": 3,
            "timestamp": "01:40.000 - 01:43.000",
            "duration": 3.0,
            "type": "Annotation",
            "design": "Semi-transparent yellow rectangular highlight box placed directly over the text http://localhost:5678 in the command prompt.",
            "animation": "Fades in quickly (0.2s).",
            "transcript": "Well it means you can copy and paste this link..."
          },
          {
            "id": 4,
            "timestamp": "01:56.000 - 02:00.000",
            "duration": 4.0,
            "type": "Annotation",
            "design": "Red rectangular outline with rounded corners, highlighting the 'Create Workflow' button in the top right of the n8n UI.",
            "animation": "Draws on from the top-left corner clockwise.",
            "transcript": "In the top right you'll see you can create a new workflow..."
          }
        ],
        "transitions": [
          {
            "id": 1,
            "timestamp": "00:01.500",
            "type": "Cut",
            "duration": 0.0,
            "description": "Split screen to full-frame speaker",
            "sfx": "None"
          },
          {
            "id": 2,
            "timestamp": "00:19.500",
            "type": "Cut",
            "duration": 0.0,
            "description": "Speaker to n8n.io website screen share",
            "sfx": "None"
          },
          {
            "id": 3,
            "timestamp": "00:24.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "n8n.io website to n8n dashboard",
            "sfx": "None"
          },
          {
            "id": 4,
            "timestamp": "00:30.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Screen share to full-frame speaker",
            "sfx": "None"
          },
          {
            "id": 5,
            "timestamp": "00:34.500",
            "type": "Cut",
            "duration": 0.0,
            "description": "Speaker to Docker website screen share",
            "sfx": "None"
          },
          {
            "id": 6,
            "timestamp": "00:45.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Docker website to Windows Desktop",
            "sfx": "None"
          },
          {
            "id": 7,
            "timestamp": "01:43.000",
            "type": "Cut",
            "duration": 0.0,
            "description": "Command prompt to web browser",
            "sfx": "None"
          }
        ],
        "zoomEvents": [
          {
            "id": 1,
            "timestamp": "00:40.000",
            "factor": 1.5,
            "direction": "Center",
            "duration": 0.5,
            "easing": "Ease In/Out"
          },
          {
            "id": 2,
            "timestamp": "01:00.000",
            "factor": 1.8,
            "direction": "Top Left",
            "duration": 0.5,
            "easing": "Ease In/Out"
          },
          {
            "id": 3,
            "timestamp": "01:08.000",
            "factor": 1.5,
            "direction": "Bottom Center",
            "duration": 0.5,
            "easing": "Ease In/Out"
          },
          {
            "id": 4,
            "timestamp": "01:15.000",
            "factor": 1.3,
            "direction": "Center",
            "duration": 0.5,
            "easing": "Ease In/Out"
          }
        ],
        "layoutTimeline": [
          {
            "timeRange": "00:00.000 - 00:01.500",
            "layout": "split-screen",
            "notes": "Graphic left, speaker right"
          },
          {
            "timeRange": "00:01.500 - 00:19.500",
            "layout": "full-frame-speaker",
            "notes": "Speaker talking directly to camera"
          },
          {
            "timeRange": "00:19.500 - 00:30.000",
            "layout": "full-frame-screen-share",
            "notes": "n8n website and dashboard"
          },
          {
            "timeRange": "00:30.000 - 00:34.500",
            "layout": "full-frame-speaker",
            "notes": "Speaker transition"
          },
          {
            "timeRange": "00:34.500 - 02:00.000",
            "layout": "full-frame-screen-share",
            "notes": "Docker install, CMD, n8n setup"
          }
        ],
        "mgSpacingLog": [
          10.0,
          55.0,
          13.0
        ]
      }
    ],
    "bodyMGPatterns": {
      "mgTypeDistribution": [
        {
          "category": "Lower Third",
          "count": 2,
          "avgDuration": 7.5
        },
        {
          "category": "Annotation",
          "count": 2,
          "avgDuration": 3.5
        }
      ],
      "spacingStatistics": {
        "overall": {
          "min": 10.0,
          "max": 55.0,
          "avg": 26.0
        },
        "byLayout": {
          "screenShare": 26.0,
          "speakerReturn": null
        }
      },
      "transitionTypeFrequency": [
        {
          "type": "Cut",
          "count": 7
        }
      ],
      "pipTogglePattern": "The creator does not use a Picture-in-Picture (PiP) overlay during screen shares in this segment. Instead, he relies entirely on full-frame screen shares and cuts back to a full-frame camera view to re-engage the viewer.",
      "speakerReturnCadence": {
        "min": 10.5,
        "max": 10.5,
        "avg": 10.5
      },
      "zoomPatterns": {
        "frequencyPerMinute": 2.0,
        "typicalFactor": 1.5,
        "commonEasing": "Ease In/Out"
      }
    }
  }
}
```

---

# Window 2: 10:00–12:00

## Body Sample Window: 10:00 – 12:00

### Context
- **Section:** Configuring Tools and Agent Prompt
- **Primary Layout:** full-frame-screen-share
- **PiP State:** off

### Pacing Metrics
- **MG Events:** 0 | **Transitions:** 1
- **MG Spacing:** N/A (No traditional MGs, relies on digital zooms)
- **Cuts/min:** 0.5
- **Zoom Events:** 7

### Motion Graphic Events (0 total)

*(No traditional motion graphics overlays, text callouts, or lower thirds are used in this segment. The visual pacing is driven entirely by screen recording interactions and post-production digital zooms.)*

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| 1 | 11:33.500 | Cut | 0.00s | Hard cut from the n8n interface to the ChatGPT interface. | None |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| 1 | 10:02.000 | 1.5x | Center-Right | 0.50s | Ease In/Out |
| 2 | 10:17.500 | 1.8x | Top-Center | 0.40s | Ease In/Out |
| 3 | 10:28.000 | 1.8x | Top-Center | 0.40s | Ease In/Out |
| 4 | 10:38.500 | 1.3x | Center | 0.50s | Ease In/Out |
| 5 | 10:58.000 | 1.2x | Center | 0.40s | Ease In/Out |
| 6 | 11:38.500 | 1.5x | Top-Right | 0.50s | Ease In/Out |
| 7 | 11:54.000 | 1.5x | Bottom-Center | 0.50s | Ease In/Out |

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 10:00.000 - 11:33.500 | full-frame-screen-share | n8n canvas and node configuration panels. |
| 11:33.500 - 12:00.000 | full-frame-screen-share | ChatGPT web interface. |

### MG Spacing Log
*(No MG events to log spacing for. Zoom event spacing: 15.5s, 10.5s, 10.5s, 19.5s, 40.5s, 15.5s)*

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| Digital Zoom | 7 | N/A (Continuous state) |

### Spacing Statistics
- **Overall:** min 10.5s, max 40.5s, avg 18.6s between Zoom events
- **By Layout:** screen-share: avg 18.6s, speaker-return: N/A

### Transition Type Frequency
| Type | Count |
|------|-------|
| Cut | 1 |

### PiP Toggle Pattern
The Picture-in-Picture (PiP) speaker overlay remains completely off during this highly technical configuration segment to maximize screen real estate for the UI.

### Speaker Return Cadence
- Min: N/A | Max: N/A | Avg: N/A between speaker returns (No speaker returns in this window).

### Zoom Patterns
- Frequency: 3.5 zooms per minute of screen share
- Typical factor: 1.5x
- Common easing: Ease In/Out

---

```json
{
  "bodyAnalysis": {
    "bodySampleWindows": [
      {
        "windowStart": "10:00.000",
        "windowEnd": "12:00.000",
        "sectionContext": "Configuring Tools and Agent Prompt",
        "primaryLayout": "full-frame-screen-share",
        "pipState": "off",
        "pacingMetrics": {
          "mgEventsCount": 0,
          "transitionsCount": 1,
          "cutsPerMinute": 0.5,
          "zoomEventsCount": 7
        },
        "motionGraphicEvents": [],
        "transitions": [
          {
            "id": "trans-body-1",
            "timestamp": "11:33.500",
            "type": "Cut",
            "duration": 0.0,
            "description": "Hard cut from the n8n interface to the ChatGPT interface.",
            "sfx": "None"
          }
        ],
        "zoomEvents": [
          {
            "id": "zoom-1",
            "timestamp": "10:02.000",
            "factor": 1.5,
            "direction": "Center-Right",
            "duration": 0.5,
            "easing": "Ease In/Out"
          },
          {
            "id": "zoom-2",
            "timestamp": "10:17.500",
            "factor": 1.8,
            "direction": "Top-Center",
            "duration": 0.4,
            "easing": "Ease In/Out"
          },
          {
            "id": "zoom-3",
            "timestamp": "10:28.000",
            "factor": 1.8,
            "direction": "Top-Center",
            "duration": 0.4,
            "easing": "Ease In/Out"
          },
          {
            "id": "zoom-4",
            "timestamp": "10:38.500",
            "factor": 1.3,
            "direction": "Center",
            "duration": 0.5,
            "easing": "Ease In/Out"
          },
          {
            "id": "zoom-5",
            "timestamp": "10:58.000",
            "factor": 1.2,
            "direction": "Center",
            "duration": 0.4,
            "easing": "Ease In/Out"
          },
          {
            "id": "zoom-6",
            "timestamp": "11:38.500",
            "factor": 1.5,
            "direction": "Top-Right",
            "duration": 0.5,
            "easing": "Ease In/Out"
          },
          {
            "id": "zoom-7",
            "timestamp": "11:54.000",
            "factor": 1.5,
            "direction": "Bottom-Center",
            "duration": 0.5,
            "easing": "Ease In/Out"
          }
        ],
        "layoutTimeline": [
          {
            "timeRange": "10:00.000 - 11:33.500",
            "layout": "full-frame-screen-share",
            "notes": "n8n canvas and node configuration panels."
          },
          {
            "timeRange": "11:33.500 - 12:00.000",
            "layout": "full-frame-screen-share",
            "notes": "ChatGPT web interface."
          }
        ],
        "mgSpacingLog": []
      }
    ],
    "bodyMGPatterns": {
      "mgTypeDistribution": {
        "Digital Zoom": {
          "count": 7,
          "avgDuration": 0
        }
      },
      "spacingStatistics": {
        "overall": {
          "min": 10.5,
          "max": 40.5,
          "avg": 18.6
        },
        "byLayout": {
          "screen-share": 18.6,
          "speaker-return": 0
        }
      },
      "transitionTypeFrequency": {
        "Cut": 1
      },
      "pipTogglePattern": "The Picture-in-Picture (PiP) speaker overlay remains completely off during this highly technical configuration segment to maximize screen real estate for the UI.",
      "speakerReturnCadence": {
        "min": 0,
        "max": 0,
        "avg": 0
      },
      "zoomPatterns": {
        "frequencyPerMinute": 3.5,
        "typicalFactor": 1.5,
        "commonEasing": "Ease In/Out"
      }
    }
  }
}
```

---

# Window 3: 18:00–20:00

```markdown
## Body Sample Window: 18:00 – 20:00

### Context
- **Section:** Late body — testing and running
- **Primary Layout:** full-frame-screen-share
- **PiP State:** off

### Pacing Metrics
- **MG Events:** 24 | **Transitions:** 0
- **MG Spacing:** min 1s, max 13s, avg 4.7s
- **Cuts/min:** 0
- **Zoom Events:** 0

### Motion Graphic Events (24 total)

**1. Cursor Click Highlight**
- **Timestamp:** 00:01
- **Type:** Cursor Effect
- **Description:** Yellow translucent circle expands and fades around the cursor as the user double-clicks the "Agent" node.
- **Duration:** 0.5s

**2. Cursor Click Highlight**
- **Timestamp:** 00:13
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Back to canvas".
- **Duration:** 0.5s

**3. Cursor Click Highlight**
- **Timestamp:** 00:15
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the chat node.
- **Duration:** 0.5s

**4. Cursor Click Highlight**
- **Timestamp:** 00:18
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the trash can icon.
- **Duration:** 0.5s

**5. Cursor Click Highlight**
- **Timestamp:** 00:22
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the "+" button.
- **Duration:** 0.5s

**6. Cursor Click Highlight**
- **Timestamp:** 00:24
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Add another trigger".
- **Duration:** 0.5s

**7. Cursor Click Highlight**
- **Timestamp:** 00:26
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "On a schedule".
- **Duration:** 0.5s

**8. Cursor Click Highlight**
- **Timestamp:** 00:30
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the "Days" dropdown.
- **Duration:** 0.5s

**9. Cursor Click Highlight**
- **Timestamp:** 00:32
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Weeks".
- **Duration:** 0.5s

**10. Cursor Click Highlight**
- **Timestamp:** 00:36
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Back to canvas".
- **Duration:** 0.5s

**11. Cursor Click Highlight**
- **Timestamp:** 00:38
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the trash can icon.
- **Duration:** 0.5s

**12. Cursor Click Highlight**
- **Timestamp:** 00:41
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on double-clicking the "Agent" node.
- **Duration:** 0.5s

**13. Cursor Click Highlight**
- **Timestamp:** 00:44
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Execute step".
- **Duration:** 0.5s

**14. Cursor Click Highlight**
- **Timestamp:** 00:51
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "getInvoices" in the log.
- **Duration:** 0.5s

**15. Cursor Click Highlight**
- **Timestamp:** 01:04
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking inside the prompt text box.
- **Duration:** 0.5s

**16. Cursor Click Highlight**
- **Timestamp:** 01:08
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Execute step".
- **Duration:** 0.5s

**17. Cursor Click Highlight**
- **Timestamp:** 01:14
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the "Output" tab.
- **Duration:** 0.5s

**18. Cursor Click Highlight**
- **Timestamp:** 01:16
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking to expand the JSON details.
- **Duration:** 0.5s

**19. Cursor Click Highlight**
- **Timestamp:** 01:23
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Back to canvas".
- **Duration:** 0.5s

**20. Cursor Click Highlight**
- **Timestamp:** 01:36
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the "+" button on the canvas.
- **Duration:** 0.5s

**21. Cursor Click Highlight**
- **Timestamp:** 01:39
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking the search box.
- **Duration:** 0.5s

**22. Cursor Click Highlight**
- **Timestamp:** 01:40
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Split Out".
- **Duration:** 0.5s

**23. Cursor Click Highlight**
- **Timestamp:** 01:46
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking and dragging the "details" object.
- **Duration:** 0.5s

**24. Cursor Click Highlight**
- **Timestamp:** 01:55
- **Type:** Cursor Effect
- **Description:** Yellow circle highlight on clicking "Execute step".
- **Duration:** 0.5s

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
| - | - | - | - | No video transitions in this window (continuous screen recording). | - |

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
| - | - | - | - | - | No digital zooms in this window. |

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
| 00:00 – 02:00 | full-frame-screen-share | Continuous screen recording of the n8n interface. No camera PiP is present. |

### MG Spacing Log
12s, 2s, 3s, 4s, 2s, 2s, 4s, 2s, 4s, 2s, 3s, 3s, 7s, 13s, 4s, 6s, 2s, 7s, 13s, 3s, 1s, 6s, 9s

---

## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
| Cursor Effect | 24 | 0.5s |

### Spacing Statistics
- **Overall:** min 1s, max 13s, avg 4.7s between MG events
- **By Layout:** screen-share: avg 4.7s

### Transition Type Frequency
| Type | Count |
|------|-------|
| Cut | 0 |

### PiP Toggle Pattern
The PiP remains off for the entirety of this sample window. The focus is entirely on the screen share.

### Speaker Return Cadence
- Min: N/A | Max: N/A | Avg: N/A (No speaker returns in this window)

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
        "start": "18:00",
        "end": "20:00",
        "context": {
          "section": "Late body — testing and running",
          "primaryLayout": "full-frame-screen-share",
          "pipState": "off"
        },
        "pacingMetrics": {
          "mgEventsCount": 24,
          "transitionsCount": 0,
          "mgSpacing": {
            "min": 1,
            "max": 13,
            "avg": 4.7
          },
          "cutsPerMinute": 0,
          "zoomEventsCount": 0
        },
        "motionGraphicEvents": [
          {
            "id": 1,
            "timestamp": "00:01",
            "type": "Cursor Effect",
            "description": "Yellow translucent circle expands and fades around the cursor as the user double-clicks the 'Agent' node.",
            "duration": 0.5
          },
          {
            "id": 2,
            "timestamp": "00:13",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Back to canvas'.",
            "duration": 0.5
          },
          {
            "id": 3,
            "timestamp": "00:15",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the chat node.",
            "duration": 0.5
          },
          {
            "id": 4,
            "timestamp": "00:18",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the trash can icon.",
            "duration": 0.5
          },
          {
            "id": 5,
            "timestamp": "00:22",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the '+' button.",
            "duration": 0.5
          },
          {
            "id": 6,
            "timestamp": "00:24",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Add another trigger'.",
            "duration": 0.5
          },
          {
            "id": 7,
            "timestamp": "00:26",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'On a schedule'.",
            "duration": 0.5
          },
          {
            "id": 8,
            "timestamp": "00:30",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the 'Days' dropdown.",
            "duration": 0.5
          },
          {
            "id": 9,
            "timestamp": "00:32",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Weeks'.",
            "duration": 0.5
          },
          {
            "id": 10,
            "timestamp": "00:36",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Back to canvas'.",
            "duration": 0.5
          },
          {
            "id": 11,
            "timestamp": "00:38",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the trash can icon.",
            "duration": 0.5
          },
          {
            "id": 12,
            "timestamp": "00:41",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on double-clicking the 'Agent' node.",
            "duration": 0.5
          },
          {
            "id": 13,
            "timestamp": "00:44",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Execute step'.",
            "duration": 0.5
          },
          {
            "id": 14,
            "timestamp": "00:51",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'getInvoices' in the log.",
            "duration": 0.5
          },
          {
            "id": 15,
            "timestamp": "01:04",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking inside the prompt text box.",
            "duration": 0.5
          },
          {
            "id": 16,
            "timestamp": "01:08",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Execute step'.",
            "duration": 0.5
          },
          {
            "id": 17,
            "timestamp": "01:14",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the 'Output' tab.",
            "duration": 0.5
          },
          {
            "id": 18,
            "timestamp": "01:16",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking to expand the JSON details.",
            "duration": 0.5
          },
          {
            "id": 19,
            "timestamp": "01:23",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Back to canvas'.",
            "duration": 0.5
          },
          {
            "id": 20,
            "timestamp": "01:36",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the '+' button on the canvas.",
            "duration": 0.5
          },
          {
            "id": 21,
            "timestamp": "01:39",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking the search box.",
            "duration": 0.5
          },
          {
            "id": 22,
            "timestamp": "01:40",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Split Out'.",
            "duration": 0.5
          },
          {
            "id": 23,
            "timestamp": "01:46",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking and dragging the 'details' object.",
            "duration": 0.5
          },
          {
            "id": 24,
            "timestamp": "01:55",
            "type": "Cursor Effect",
            "description": "Yellow circle highlight on clicking 'Execute step'.",
            "duration": 0.5
          }
        ],
        "transitions": [],
        "zoomEvents": [],
        "layoutTimeline": [
          {
            "timeRange": "00:00 - 02:00",
            "layout": "full-frame-screen-share",
            "notes": "Continuous screen recording of the n8n interface. No camera PiP is present."
          }
        ],
        "mgSpacingLog": [12, 2, 3, 4, 2, 2, 4, 2, 4, 2, 3, 3, 7, 13, 4, 6, 2, 7, 13, 3, 1, 6, 9]
      }
    ]
  },
  "bodyMGPatterns": {
    "mgTypeDistribution": [
      {
        "category": "Cursor Effect",
        "count": 24,
        "avgDuration": 0.5
      }
    ],
    "spacingStatistics": {
      "overall": {
        "min": 1,
        "max": 13,
        "avg": 4.7
      },
      "byLayout": {
        "screenShare": {
          "avg": 4.7
        },
        "speakerReturn": {
          "avg": null
        }
      }
    },
    "transitionTypeFrequency": [],
    "pipTogglePattern": "The PiP remains off for the entirety of this sample window. The focus is entirely on the screen share.",
    "speakerReturnCadence": {
      "min": null,
      "max": null,
      "avg": null
    },
    "zoomPatterns": {
      "frequencyPerMinute": 0,
      "typicalFactor": null,
      "commonEasing": null
    }
  }
}
```