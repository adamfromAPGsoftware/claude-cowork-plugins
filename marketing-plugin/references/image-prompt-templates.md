# Image Prompt Templates

Structured templates for generating Meta ad creatives. The Creative Generator agent MUST select a template and fill in angle-specific details rather than writing raw prompts.

## How to Use

1. Choose the template that best matches the angle's `visual_direction`
2. Fill in the `{placeholders}` with angle-specific content
3. Append brand guidelines (from `brand-guidelines.md`) to every prompt
4. Pass the completed prompt to `generate-ad-image.py`

## Mandatory Elements

Every image prompt MUST include these elements regardless of template:

### Style Reference Line
When an angle has `inspiration_ads`, include:
```
Style reference: match the composition and colour palette of the provided inspiration image(s).
```
Load the actual inspiration ad image files as reference images alongside the text prompt.

### Background Specificity
NEVER use generic descriptions like "dark background" or "clean background". Always specify:
- Exact hex colour(s)
- Gradient direction if any
- Subtle texture or pattern (e.g., "faint grid pattern at 5% opacity")
- Example: "Deep navy (#1B2A4A) with subtle diagonal gradient to (#162231), faint geometric grid at 3% opacity"

### Text Overlay Constraints
- Maximum 12 characters for any text rendered in the image
- Specify exact positioning (e.g., "bottom-left quadrant, 20px from edge")
- Specify colour and approximate font style
- If no text overlay: explicitly state "No text in image — text space reserved at {position} for post-production overlay"

### Aspect Ratio Safe Zones
- **1:1 (feed):** Text space in bottom 30% or top 20%. Key visual centred.
- **9:16 (stories/reels):** Keep key elements in centre 60% width. Bottom 160px reserved for platform UI. Top 100px reserved for story UI.

### Approval Gate
Present the complete prompt text to the user before calling the image generation API. User may refine wording, adjust composition, or approve as-is. NEVER generate without approval.

### Post-Generation Validation
After generation, verify:
1. Brand colours correct (compare hex values)?
2. Composition matches the brief?
3. No AI artifacts (extra fingers, garbled text, distorted objects)?
4. Text space reserved correctly for overlay?
5. Would this stop scrolling at mobile feed scale?

If any check fails, note the issue, adjust the prompt, and re-generate.

## Templates

### 1. Product Hero

**Best for:** Feature showcases, SaaS dashboards, tool demonstrations

```
Professional product advertisement photograph. Clean, minimal background with subtle gradient in {brand_colour_bg}. 
Centre frame: {product_description}. Shot from slightly above at 3/4 angle. 
Soft directional lighting from upper left casting gentle shadows. 
Sharp focus on the product, shallow depth of field on background. 
High-end commercial photography style, magazine-quality finish. 
Colour palette: {brand_colours}. 
Leave {text_space_position} clear for headline overlay.
```

**Composition:** Product centred, 60% of frame. Leave 30-40% clear space for text overlay.
**Avoid:** Cluttered backgrounds, multiple products competing for attention, unrealistic lighting.

---

### 2. Lifestyle

**Best for:** Aspirational messaging, "imagine your life with this" angles

```
Candid lifestyle photograph of {person_description} in {setting}. 
Natural warm lighting, golden hour feel. {person_description} is {action_description}. 
Expression: {emotion} — genuine, not posed. 
Environment tells a story: {environmental_details}. 
Shot on 85mm lens, shallow depth of field, subject sharp, background softly blurred. 
Colour grading: warm tones, slightly lifted shadows. 
{brand_element_placement}.
```

**Composition:** Subject at 1/3 line, environment visible. Eye-level or slightly below.
**Avoid:** Stock photo stiffness, perfect staging, overly polished skin.

---

### 3. Bold Graphic

**Best for:** Attention-grabbing, scroll-stopping, announcement-style ads

```
Bold graphic advertisement design. {background_style} background in {brand_colours}. 
Striking visual element: {hero_visual}. 
High contrast between foreground and background. Strong geometric shapes — {shape_description}. 
Dynamic composition with diagonal energy lines. 
Clear visual hierarchy directing the eye from {start_point} to {end_point}. 
Leave prominent space ({text_area_size}) in {text_position} for bold headline text. 
Style: modern, confident, high-impact. No clutter.
```

**Composition:** Asymmetric balance, strong focal point, large text zones.
**Avoid:** More than 3 colours, competing visual elements, symmetrical layouts (too static).

---

### 4. UGC Style

**Best for:** Authenticity, trust-building, "real person" testimonial feel

```
Casual selfie-style photograph taken on a smartphone camera. 
{person_description} in a {natural_setting}. 
Slightly imperfect framing — not centred, natural hand-held feel. 
Indoor lighting or natural daylight, no studio setup. 
Person looking at camera with {expression}. 
Background shows real environment: {background_details}. 
Slight lens distortion typical of phone camera wide angle. 
No filters, no heavy editing — authentic and relatable. 
{optional_prop_or_product_visible}.
```

**Composition:** Off-centre subject, phone-camera perspective (slightly above or at eye level).
**Avoid:** Professional lighting, perfect composition, model-quality appearance.

---

### 5. Before-After

**Best for:** Transformation stories, problem-solution, comparison angles

```
Split-composition advertisement showing transformation. 
LEFT SIDE ({before_percentage}% of frame): {before_state}. 
Muted colours, slightly desaturated, conveying {before_emotion}. 
RIGHT SIDE ({after_percentage}% of frame): {after_state}. 
Vibrant colours in {brand_colours}, conveying {after_emotion}. 
Clear visual dividing line between the two states — {divider_style}. 
Same subject/environment in both halves for direct comparison. 
Dramatic lighting shift from left (flat, grey) to right (bright, warm).
```

**Composition:** Vertical split (50/50 or 40/60 favouring the "after"). Divider can be diagonal for more energy.
**Avoid:** Unclear what changed, too subtle differences, text-only before/after.

---

### 6. Data/Stats

**Best for:** Authority positioning, proof-based claims, "by the numbers" angles

```
Clean infographic-style advertisement layout. 
Prominent {key_metric} displayed large and bold in {accent_colour}. 
Supporting visual: {data_visualisation} — simple, not complex. 
Background: clean {background_colour} with subtle texture or grid pattern. 
Visual hierarchy: number first, context second, source attribution small. 
Professional, trustworthy aesthetic. {brand_element}. 
Minimal decoration — let the data speak. 
Leave space in {text_area} for headline and subtext.
```

**Composition:** Key number occupies 30-40% of visual weight. Clean margins. Grid-aligned.
**Avoid:** Complex charts, more than 3 data points, small unreadable numbers.

---

### 7. Pain Point

**Best for:** Problem-aware audiences, "does this sound familiar?" hooks

```
Visual metaphor photograph capturing the feeling of {pain_point}. 
{metaphor_description} — the image should immediately evoke {target_emotion}. 
{person_or_scene}: {specific_visual}. 
Colour palette: cooler tones, slightly desaturated — {mood_colours}. 
Dramatic but not dark — the image should create recognition, not depression. 
Strong single focal point, minimal distracting elements. 
{composition_direction} — eye naturally moves toward the {solution_hint_area}. 
Leave {text_space} for the hook line.
```

**Composition:** Single powerful image, negative space for text. Slightly moody lighting.
**Avoid:** Overly negative or distressing imagery, cliches (head in hands), stock photo sadness.

---

### 8. Social Proof

**Best for:** Testimonial-based ads, case study highlights, trust signals

```
Testimonial-style advertisement layout. 
{headshot_or_logo}: {subject_description}, positioned {position}. 
Quote visual treatment: large quotation marks or speech bubble aesthetic in {brand_accent}. 
Background: clean, professional — {background_style}. 
Star rating visual: {rating_display} prominently visible. 
Trust signals: {trust_elements}. 
Warm, trustworthy colour palette. Approachable and credible. 
Layout leaves clear space for the actual quote text in {text_area}. 
Overall feel: real person, real result, no corporate polish.
```

**Composition:** Headshot/logo anchors one side, text space dominates the other. Trust signals along bottom.
**Avoid:** Fake-looking testimonials, too many trust signals competing, corporate stock photos.

---

## General Rules for All Templates

1. **Text space:** Always leave 30-50% of the image clear for headline/copy overlay (Meta ads need this)
2. **Brand consistency:** Reference `brand-guidelines.md` for colours, tone, and restrictions
3. **Mobile-first:** Images are viewed on phones — large elements, high contrast, no fine details
4. **Aspect-specific adjustments:**
   - **1:1** (feed): Balanced composition, centred or rule-of-thirds
   - **9:16** (stories/reels): Vertical flow, top-heavy content (bottom gets covered by CTA)
   - **1.91:1** (feed landscape): Wide composition, hero element left or centre, text space right
   - **16:9** (in-stream): Cinematic framing, horizontal flow
5. **Text in images:** Render SHORT anchor text (numbers, 2-3 word phrases, strikethrough comparisons) when the value proposition requires it. The model handles bold short text well. Leave clear space for longer copy (headlines, descriptions) that will be added in Meta Ads Manager. Never render paragraphs or full sentences — these will be garbled.
