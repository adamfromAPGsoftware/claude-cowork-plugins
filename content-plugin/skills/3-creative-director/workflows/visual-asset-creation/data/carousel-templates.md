# Carousel Templates

Reusable carousel patterns with hardcoded design decisions. Agents fill in text only — photos, layout, and styling are predetermined.

---

## Template: Saraev Alternating

**Style:** Alternating photo slides and text slides with a clean dark aesthetic.

**Best for:** Lead magnet carousels, educational breakdowns, nurture content.

**Slide sequence (8 slides):**

| # | Type | Purpose |
|---|------|---------|
| 1 | `photo-title` | Hook — Gemini-generated intro photo + bold headline + SWIPE |
| 2 | `text-only` | Problem context / scene-setting (optional image) + SWIPE |
| 3 | `body` (labeled) | First key point + SWIPE |
| 4 | `text-only` | Bridge / transition text (optional image) + SWIPE |
| 5 | `body` (labeled) | Second key point + SWIPE |
| 6 | `text-only` | Supporting detail / comparison + SWIPE |
| 7 | `body` (labeled) | Third key point / audience + SWIPE |
| 8 | `photo-title` | CTA — Gemini-generated CTA photo + follow bubble (NO swipe) |

**Design rules:**
- **Photo slides (intro):** Gemini-generated image as full-bleed bg (creator on right, dark branded bg with green blobs), gradient overlay, headline at bottom-left, "SWIPE >>>" bottom-right.
- **Photo slides (CTA / last slide):** Same as intro BUT no swipe — instead a green pill-shaped "Follow" bubble at bottom-right. Optional `ctaText` field customises the bubble text.
- **Text-only slides:** Dark bg + blobs, white body text. If `imagePath` is provided, image renders in the upper portion (rounded, contained) with text directly below it. If no image, text is vertically centered. "SWIPE >>>" bottom-right.
- **Body slides:** Dark bg + blobs + green accent bar, with uppercase green label above headline (e.g., "WHAT IT DOES"). Clear spacing between accent bar → label → headline. "SWIPE >>>" bottom-right.
- **All slides:** Company brand top-right, author bottom-left.
- **Text colour:** White (`#ffffff`) for body text on text-only slides, grey (`#999999`) for supporting body on other slide types.

**Hardcoded photo paths (Gemini-generated, dark branded bg with the creator):**
- Slide 1 (intro — warm/smiling): `{reference_photos_folder}/carousel-bg-intro.png`
- Slide 8 (CTA — confident/direct): `{reference_photos_folder}/carousel-bg-cta.png`

Where `{reference_photos_folder}` = `content-plugin/data/reference-photos`

These backgrounds were generated via `scripts/generate-carousel-photos.py` using Gemini with reference photos. They show the creator naturally placed on the right side over a dark background with subtle green blobs — text space is on the left. To regenerate or create new variants, run:
```bash
python3 scripts/generate-carousel-photos.py --ref-dir content-plugin/data/reference-photos --output-dir content-plugin/data/reference-photos --slides intro,cta
```

**JSON skeleton:**

```json
{
  "branding": { "company": "SOFTWARE", "author": "{YOUR_NAME}" },
  "slides": [
    {
      "type": "photo-title",
      "photoPath": "{reference_photos_folder}/carousel-bg-intro.png",
      "headline": ["LINE ONE", "LINE TWO", "LINE THREE"],
      "highlightIndex": 0,
      "body": "Optional supporting text"
    },
    {
      "type": "text-only",
      "imagePath": "/optional/path/to/relevant-image.png",
      "body": "Problem context text here."
    },
    {
      "type": "body",
      "label": "LABEL HERE",
      "headline": ["LINE ONE", "LINE TWO", "LINE THREE"],
      "highlightIndex": 0,
      "body": "Detail text here."
    },
    {
      "type": "text-only",
      "imagePath": "/optional/path/to/relevant-image.png",
      "body": "Bridge / transition text here."
    },
    {
      "type": "body",
      "label": "LABEL HERE",
      "headline": ["LINE ONE", "LINE TWO", "LINE THREE"],
      "highlightIndex": 0,
      "body": "Detail text here."
    },
    {
      "type": "text-only",
      "body": "Supporting detail or comparison text here."
    },
    {
      "type": "body",
      "label": "LABEL HERE",
      "headline": ["LINE ONE", "LINE TWO", "LINE THREE"],
      "highlightIndex": 0,
      "body": "Detail text here."
    },
    {
      "type": "photo-title",
      "photoPath": "{reference_photos_folder}/carousel-bg-cta.png",
      "headline": ["CTA LINE ONE", "CTA LINE TWO"],
      "highlightIndex": 0,
      "body": "Short CTA message",
      "ctaText": "Follow + ♻️"
    }
  ]
}
```

**Agent instructions:**
- Replace all placeholder text. Do NOT change `photoPath`, `type`, slide order, or branding.
- Labels should be short uppercase descriptors (2-3 words max).
- `imagePath` on text-only slides is optional — use project B-roll, screenshots, or logo canvases when available. Omit for text-only presentation.
- `ctaText` on the last photo-title slide customises the follow bubble. Defaults to "Follow for more" if omitted.
- SWIPE appears automatically on all slides except the last. Do not add it manually.
