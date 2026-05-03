# Thumbnail Prompt Templates

## Wide Format (16:9) — YouTube Thumbnail

```
YouTube thumbnail: [scene description with the person from the reference photos].
Expression: [specific expression direction — e.g., "shocked, mouth slightly open, wide eyes"].
Composition: [face position] + [object/context element] + [text overlay].
Text on image: "[EXACT TEXT]" in [colour] [font style], positioned [location].
Style reference: match the composition and colour palette of the provided inspiration thumbnails.
Background: [specific background direction].
Aspect ratio: 16:9. High contrast, bold, mobile-readable.
```

## Prompt Construction Rules

1. **Never describe the face** — let reference photos handle identity preservation
2. **Expression goes in the prompt text** — not in the reference photos (which should be neutral)
3. **Text overlay must be under 12 characters** — mandatory for mobile readability
4. **Always specify aspect ratio** — 16:9 for wide, 9:16 for vertical
5. **Include style reference line** if inspiration thumbnails are provided
6. **Background must be specific** — not just "dark background" but "dark gradient with subtle code editor lines"

## Reference Photo Protocol

- **Always load from `{reference_photos_folder}`** (resolved from CCS config) — foundation image first
- **Loading order matters:**
  1. creator-hero-front.jpg (foundation — ALWAYS FIRST)
  2. creator-3quarter-left.jpg
  3. creator-3quarter-right.jpg
  4. creator-smiling.jpg
  5. creator-talking.jpg
- **3-5 photos is the sweet spot** — all 5 recommended
- **API limits:** Up to 14 images total, up to 5 human faces, up to 6 get high fidelity

## Expression Direction Guide

| Content Tone | Expression Direction |
|-------------|---------------------|
| New tool / free resource | Excited, slight smile, eyebrows raised |
| Problem being solved | Thoughtful, hand on chin, slight head tilt |
| Shocking result / claim | Surprised, mouth slightly open, wide eyes |
| Tutorial / how-to | Confident, direct eye contact, slight smile |
| Controversial take | Serious, slight frown, direct gaze |

## Example Prompts

### Tech Tutorial Thumbnail
```
YouTube thumbnail: the person from the reference photos sitting at a desk with a glowing laptop screen showing code, with a floating Claude Code logo beside them.
Expression: confident, direct eye contact, slight knowing smile.
Composition: face on the left third, laptop and logo centre-right, text overlay top-right.
Text on image: "10X FASTER" in white bold Impact font, positioned top-right with dark shadow.
Style reference: match the composition and colour palette of the provided inspiration thumbnails.
Background: dark gradient with subtle blue code editor lines, moody tech atmosphere.
Aspect ratio: 16:9. High contrast, bold, mobile-readable.
```

### Comparison / VS Thumbnail
```
YouTube thumbnail: the person from the reference photos in the centre, arms crossed, with two tool logos flanking them — [Logo A] on the left and [Logo B] on the right.
Expression: thoughtful, slight head tilt, evaluating expression.
Composition: face centred, logos on either side at same height, "VS" text between logos.
Text on image: "VS" in red bold, positioned between the two logos.
Style reference: match the composition and colour palette of the provided inspiration thumbnails.
Background: split dark background, slightly different hue on each side.
Aspect ratio: 16:9. High contrast, bold, mobile-readable.
```
