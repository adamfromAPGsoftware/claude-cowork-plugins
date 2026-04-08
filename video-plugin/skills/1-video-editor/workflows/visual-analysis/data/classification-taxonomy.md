# Visual Analysis Classification Taxonomy

## Scene Classifications

| Classification | Description | Examples |
|---|---|---|
| `talking-head` | Presenter visible, face-to-camera | Solo presenter, interview, webcam overlay |
| `screen-share` | Screen recording showing tool usage | IDE, browser, terminal, design tools |
| `diagram-slides` | Static or animated visual aids | PowerPoint slides, diagrams, whiteboard, architecture drawings |
| `transition` | Scene change between content types | Fade, cut, intro/outro animation |
| `mixed-pip` | Picture-in-picture or split view | Talking head overlaid on screen share, side-by-side |

## Detail Fields Per Segment

### Required Fields

| Field | Type | Description |
|---|---|---|
| `timestamp` | string | Start time in MM:SS format (e.g., 01:30) |
| `endTimestamp` | string | End time in MM:SS format (e.g., 01:45) |
| `classification` | string | One of the classifications above |
| `confidence` | float | 0.0-1.0 confidence in classification |
| `description` | string | Human-readable summary of what's happening |

### Details Object Fields

| Field | Type | Description |
|---|---|---|
| `tool` | string/null | Tool being used (VS Code, Chrome, Terminal, Figma, PowerPoint, etc.) |
| `activity` | string | What the user is doing (typing, navigating, demonstrating, explaining, presenting, scrolling, clicking) |
| `context` | string | Specific detail about what's being typed/shown/discussed |
| `elements` | array | Visual elements present on screen (code editor, terminal, sidebar, browser tabs, etc.) |
| `brollRelevance` | string | B-roll extraction relevance: "high", "medium", or "low" |

## B-Roll Relevance Criteria

| Rating | Criteria |
|---|---|
| `high` | Clear demonstration of a tool, feature, or concept; visually distinct; good for standalone clip |
| `medium` | Useful context but may need surrounding segments; partially relevant |
| `low` | Transition, repetitive content, or low visual interest |

## Visual Events (Sub-Segment Presenter Actions)

Within talking-head or mixed-pip segments, the analysis flags moments where the presenter does something visually distracting. These are reported as an array of events within the segment.

| Event Type | Description | Examples |
|---|---|---|
| `distraction` | Brief physical action that breaks delivery | Nose wipe, face scratch, fidgeting, adjusting glasses/hair/clothing |
| `obstruction` | Hand or object blocking the presenter's face | Hand over mouth, looking down at phone, turning away from camera |
| `break` | Non-speaking pause or interruption | Drinking water, sneezing, coughing, yawning |

### Visual Event Fields

| Field | Type | Description |
|---|---|---|
| `timestamp` | string | Event start time in MM:SS format |
| `endTimestamp` | string | Event end time in MM:SS format |
| `eventType` | string | One of: `distraction`, `obstruction`, `break` |
| `description` | string | Brief description of what happened |

## Pydantic Schema (for Gemini Structured Output)

Use this schema with `response_schema` to force Gemini to produce valid, typed output:

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SceneClassification(str, Enum):
    TALKING_HEAD = "talking-head"
    SCREEN_SHARE = "screen-share"
    DIAGRAM_SLIDES = "diagram-slides"
    TRANSITION = "transition"
    MIXED_PIP = "mixed-pip"

class BrollRelevance(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class VisualEventType(str, Enum):
    DISTRACTION = "distraction"
    OBSTRUCTION = "obstruction"
    BREAK = "break"

class VisualEvent(BaseModel):
    timestamp: str = Field(..., description="Event start time in MM:SS format")
    endTimestamp: str = Field(..., description="Event end time in MM:SS format")
    eventType: VisualEventType = Field(..., description="Type of visual event")
    description: str = Field(..., description="Brief description of what happened")

class SegmentDetails(BaseModel):
    tool: Optional[str] = Field(None, description="Tool being used (VS Code, Chrome, Terminal, etc.) or null if not applicable")
    activity: str = Field(..., description="What the user is doing: typing, navigating, demonstrating, explaining, presenting, scrolling, clicking")
    context: str = Field(..., description="Specific detail about what is being typed, shown, or discussed")
    elements: list[str] = Field(..., description="Visual elements present on screen")
    brollRelevance: BrollRelevance = Field(..., description="B-roll extraction relevance rating")
    visualEvents: Optional[list[VisualEvent]] = Field(None, description="Sub-segment visual events (distractions, obstructions, breaks) within talking-head/mixed-pip segments. Null for non-presenter segments.")

class VisualSegment(BaseModel):
    timestamp: str = Field(..., description="Start time in MM:SS format")
    endTimestamp: str = Field(..., description="End time in MM:SS format")
    classification: SceneClassification = Field(..., description="Scene type classification")
    confidence: float = Field(..., description="Classification confidence 0.0-1.0")
    description: str = Field(..., description="Human-readable description of what is happening on screen")
    details: SegmentDetails

class VisualAnalysisSegments(BaseModel):
    segments: list[VisualSegment] = Field(..., description="Ordered list of visual segments covering the entire video timeline")
```

## JSON Output Structure (Full Document)

The final output JSON file wraps Gemini's segment analysis with metadata:

```json
{
  "videoId": "",
  "analysisDate": "",
  "totalFramesAnalysed": 0,
  "fpsUsed": 1,
  "videoDuration": "MM:SS",
  "mediaResolution": "default",
  "chunked": false,
  "chunks": [],
  "segments": [
    {
      "timestamp": "01:30",
      "endTimestamp": "01:45",
      "classification": "screen-share",
      "confidence": 0.95,
      "description": "VS Code editor with Python file open, writing a FastAPI endpoint",
      "details": {
        "tool": "VS Code",
        "activity": "typing",
        "context": "Writing async route handler for /api/users endpoint",
        "elements": ["code editor", "terminal panel", "file explorer sidebar"],
        "brollRelevance": "high"
      }
    }
  ],
  "summary": {
    "totalSegments": 0,
    "classificationBreakdown": {
      "talking-head": 0,
      "screen-share": 0,
      "diagram-slides": 0,
      "transition": 0,
      "mixed-pip": 0
    },
    "highBrollSegments": 0
  }
}
```

## Gemini API Configuration

```python
config={
    "response_mime_type": "application/json",
    "response_schema": VisualAnalysisSegments,
    "temperature": 0.2
}
```

- `response_mime_type`: Forces JSON output — no parsing ambiguity
- `response_schema`: Enforces exact field structure via Pydantic model
- `temperature: 0.2`: Low temperature for consistent, accurate classification
