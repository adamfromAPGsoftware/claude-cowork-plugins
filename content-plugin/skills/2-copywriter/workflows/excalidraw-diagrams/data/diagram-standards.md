# Storyboard Standards

## Visual Style Requirements

### ExcaliDraw Canvas Settings
- **Roughness:** 1-2 (hand-drawn aesthetic, slight wobble)
- **Fill Style:** hachure or solid (context-dependent)
- **Stroke Width:** 2 for standard elements, 4 for emphasis
- **Font Family:** 1 (Virgil/hand-drawn) for headings, 5 (default) for body text

### Colour Palette (Semantic)

| Colour | Hex | Usage |
|--------|-----|-------|
| Blue | #1971c2 | Primary concepts, main flow |
| Green | #2f9e44 | Success, positive outcomes, benefits |
| Red | #e03131 | Errors, warnings, problems, risks |
| Yellow | #f08c00 | Decisions, choices, turning points |
| Orange | #e8590c | Highlights, emphasis, call-outs |
| Violet | #7048e8 | Services, tools, external systems |
| Dark Grey | #495057 | Secondary text, borders, arrows |
| Light Grey | #dee2e6 | Backgrounds, containers |

### Typography Hierarchy

| Level | fontSize | Font | Usage |
|-------|----------|------|-------|
| Segment Heading | 36-42 | Virgil (1), bold | "01  Your Claude Code, In Your Pocket" |
| Subtitle | 16-20 | Default (5) | Descriptive line below heading |
| Supporting Text | 20-24 | Virgil (1), bold | Bold takeaway line below illustration |
| Caption | 12-14 | Default (5), grey | Annotations if needed |

## Segment Anatomy

Each segment in the storyboard follows this vertical structure:

```
┌─────────────────────────────────┐
│  01  Segment Heading            │  ← Virgil 36-42, bold
│  Subtitle description line      │  ← Default 16-20
│                                 │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │    Hero Illustration      │  │  ← 400-600px wide, Nanobanana-generated
│  │    (embedded image)       │  │
│  │                           │  │
│  └───────────────────────────┘  │
│                                 │
│  Bold takeaway line.            │  ← Virgil 20-24, bold
└─────────────────────────────────┘
            ──────────→               ← Arrow to next segment
```

### Segment Block Dimensions
- **Block width:** ~700-800px per segment
- **Block height:** ~700-900px (varies with illustration aspect ratio)
- **Inter-segment gap:** ~100-150px (room for arrow connector)

### Hero Illustration Size
- **Width:** 500-600px display width (the dominant visual element)
- **Height:** MUST be calculated from the source image's actual aspect ratio — `display_height = display_width / (source_width / source_height)`. NEVER hardcode a square. Gemini typically outputs 1408x768 (1.83:1 landscape), so a 600px wide display = ~327px height.
- **Style:** Rich, detailed scene illustration — NOT small icons
- **Background:** White or transparent
- **Aesthetic:** Hand-drawn sketch, black ink, ExcaliDraw-compatible

## Storyboard Layout

### Canvas Type
- **Wide horizontal flow** — segments arranged left-to-right
- Canvas width scales with segment count: (segments × ~850px) + padding
- Canvas height: ~900px fixed

### Flow Pattern
- Each segment block is a vertical stack (heading → subtitle → image → text)
- Horizontal arrows connect segment blocks in sequence
- No arrow after the final segment
- Consistent spacing and alignment across all segments

### Visual Hierarchy Rules
1. Hero illustrations are the dominant visual element — they carry the storytelling
2. Numbered headings anchor each segment at the top
3. Subtitles provide brief context below the heading
4. Supporting text delivers the takeaway below the illustration
5. Arrows guide the eye through the left-to-right narrative flow
6. ExcaliDraw is scaffolding only — minimal containers, no complex grids or panels

## Hero Illustration Integration Standards

### Image Requirements
- Rich, detailed scene compositions (multiple elements, visual storytelling)
- Match ExcaliDraw hand-drawn sketch aesthetic
- Transparent or white background
- Consistent style across all segments in a storyboard
- Large enough to be the hero visual (400-600px wide)

### Image Placement Rules
- Centred horizontally within the segment block
- Below subtitle, above supporting text
- Minimum 20px padding from surrounding text elements
- All hero illustrations should be consistently sized within a storyboard
