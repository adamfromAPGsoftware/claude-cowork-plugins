# Image Prompt Templates

Narrative templates for generating Meta ad creatives with **Nano Banana Pro** (Gemini 3 Pro Image). The Creative Generator MUST pick a template, fill in the angle-specific details, and write the final prompt as **natural-language prose** — not labelled blocks or keyword lists.

Nano Banana Pro is a thinking model. It reads prompts like a creative director reads a brief. Tag-soup and SUBJECT/COMPOSITION block formats are obsolete — they actively hurt output.

## How to Use

1. Choose the template that matches the angle's `visual_direction`
2. Fill the `{placeholders}` with angle-specific content drawn from the creative brief, angle data, and `brand-guidelines.md`
3. Write the final prompt as a natural paragraph (see SCALD checklist below) plus the mandatory constraint lines
4. Run the Concept Review Gate in `generate-images.md` before generating

## SCALD Checklist for Every Template

Every final prompt must contain all five SCALD elements, woven into natural prose:

| Element | What to cover |
|---------|---------------|
| **S — Subject** | Who or what is in the frame. Be specific about age, role, product, or graphic element. |
| **C — Context** | Environment, situation, narrative moment. Real settings beat studio stock. |
| **A — Aesthetics** | Lighting direction, camera/lens, colour mood, photographic style. Cinematographer vocabulary. |
| **L — Layout** | Composition, aspect ratio, eye path, safe zones, where text reserves space. |
| **D — Directive** | What the image should DO — the feeling it should evoke in 1 second of scroll time. |

If any SCALD element is missing from the final prompt, the prompt is incomplete.

---

## Mandatory Elements (every prompt, every template)

Every image prompt MUST include these elements regardless of template.

### Reference Image Roles

When passing reference images to the script, label them **by role** in the prompt so the model disambiguates:

```
Reference images: Image A is the logo — reproduce the exact gear mark at
[top-left / top-right / bottom-left / bottom-right], unchanged, no effects.
Image B is an inspiration reference — use it ONLY for [entry point / emotional
register / composition style] and do NOT copy its specific elements, text, or layout.
```

This is the #1 fix for the "model copied the inspiration wholesale" failure mode. Always label Image A and Image B by role.

### Background Specificity

NEVER use generic descriptions like "dark background" or "clean background". Always specify:
- Exact hex colour(s) from `brand-guidelines.md`
- Gradient direction if any
- Subtle texture or pattern (e.g., "faint diagonal grid at 3% opacity")
- Example: *"Deep navy #1B2A4A with a subtle diagonal gradient to #162231, faint geometric grid at 3% opacity."*

### Text Rendering Rules

Put rendered text in **double quotes** with explicit typography direction:

```
The anchor text "25 HRS" in a heavy geometric sans-serif, pure white #FFFFFF,
centred in the top third, occupying roughly 25% of the frame width.
```

Rules:
- Maximum 8 characters per rendered text element — numbers and short anchors only
- Specify font style in plain English (*heavy geometric, bold condensed, ultra-thin modern serif, hand-lettered brush*), weight, colour (hex), position, approximate size
- Never attempt full headlines or sentences — they garble

If NO rendered text, include the positive reservation line:

```
No rendered text in the image — clean negative space reserved in the [top third /
centre / bottom third] for a post-production headline overlay added in Meta Ads Manager.
```

### Aspect Ratio Safe Zones

| Aspect | When | Safe zones |
|--------|------|------------|
| **4:5** (1080×1350) | **Feed default** (cold traffic) | Text space top 20% or bottom 30%, key visual in centre 70% |
| 1:1 | Feed square, carousel consistency | Balanced centred or rule-of-thirds |
| 9:16 | Stories / Reels only | Centre 60% width for key elements, top ~14% and bottom ~14% reserved for platform UI |
| 1.91:1 | Right-column / in-stream | Hero element left or centre, text space right |

### Positive Constraints Only

Never write negative lists (`no text, no clutter, no competitor logos, no fake lighting`). Describe the desired state positively:
- "single focal point, generous negative space" ✓
- "no clutter" ✗
- "soft natural daylight from camera-left" ✓
- "no studio lighting" ✗

### Approval Gate

Present the complete prompt text to the user before calling the generation script. User may refine or approve. Never generate without approval.

### Post-Generation Validation

After generation, verify:
1. Brand hex codes come through accurately
2. Composition matches the brief
3. Rendered text matches the exact quoted string (if applicable)
4. Logo (Image A) is reproduced cleanly, not merged
5. No AI artifacts (extra fingers, garbled letters, distorted objects)
6. Thumb-test passes at 120px width
7. High contrast against Meta's white/blue Feed chrome

If any check fails, build a **targeted edit prompt** and re-run with the previous output as an extra reference. Don't re-roll from scratch.

---

## Templates

Each template below gives a narrative paragraph skeleton and fill-in guidance. The final prompt the skill produces is prose — not a form.

### 1. Product Hero

**Best for:** Feature showcases, SaaS dashboards, tool demonstrations, product-as-hero

**Narrative skeleton:**

> A professional commercial product photograph of `{product_description}`, framed at `{angle_and_framing}`, sitting on `{surface_or_backdrop}`. The mood is `{directive — e.g., confident, aspirational, quietly powerful}`. Single subject, generous negative space, nothing competing for attention.
>
> Camera and lighting: shot on a 50mm lens at f/2.8, soft directional key light from upper-left, subtle rim light from behind-right, shallow depth of field so the background falls gently out of focus.
>
> Colour palette: `{brand_colour_bg hex}` background with `{accent_colour hex}` highlights. Premium editorial feel.

**Fill-in guide:**
- Subject: the product (SaaS dashboard, physical tool, CRM interface)
- Context: realistic surface, not sterile studio
- Aesthetics: cinematographer lighting language, not "professional lighting"
- Layout: 30–40% negative space for headline overlay
- Directive: what the product should make the viewer feel in 1 second

**Avoid:** cluttered backgrounds, multiple products competing, unrealistic lighting, "4K masterpiece" tag-soup.

---

### 2. Lifestyle

**Best for:** Aspirational messaging, "imagine your life with this" angles, post-transformation calm

**Narrative skeleton:**

> A candid lifestyle photograph of `{person_description — age, role, context}` in `{specific_setting}`, `{action_description}`. The expression is `{emotion}` — genuine, not posed. The environment tells a story: `{environmental_details}`. The scene feels like a Tuesday morning, not a stock shoot.
>
> Camera and lighting: medium shot on an 85mm lens at f/1.8, natural warm daylight from a window out of frame, slightly lifted shadows, shallow depth of field with the subject sharp and the background softly blurred.
>
> Colour palette: warm neutral tones grounded by `{brand_colour hex}` accent elements in the environment. Subject positioned at the rule-of-thirds left or right line.

**Fill-in guide:**
- Subject: real Australian business owner or operator, specific age and context
- Context: their actual environment (warehouse, office, kitchen, site van)
- Aesthetics: natural, warm, golden hour NOT cliché
- Directive: calm confidence, quiet relief, or grounded pride — never wide-eyed excitement

**Avoid:** stock photo stiffness, perfect staging, overly polished skin, "business team" clichés.

---

### 3. Bold Graphic

**Best for:** Attention-grabbing, scroll-stopping, announcement-style ads, single-statement hooks

**Narrative skeleton:**

> A bold graphic advertisement design. The background is `{background_style — solid, gradient, textured}` in `{specific hex codes}`. A single striking visual element dominates the frame: `{hero_visual}`. High contrast, strong geometric shapes, diagonal energy lines. The composition is asymmetric and confident — nothing symmetrical, nothing static.
>
> Camera and lighting: flat graphic treatment, no photographic depth — this is a poster, not a photograph. Crisp edges, clean typography zones.
>
> Colour palette: maximum 3 colours drawn from `{brand_colours hex}`. High-contrast against Meta's white/blue Feed chrome.
>
> Layout: strong focal point in `{position}`, clear visual hierarchy directing the eye from `{start_point}` to `{end_point}`, prominent reserved space for the headline.

**Fill-in guide:**
- Subject: a single hero shape, symbol, or graphic device
- Context: no environment — this is pure graphic design
- Aesthetics: flat, modern, confident, high-impact
- Layout: asymmetric balance, large text zones

**Avoid:** more than 3 colours, competing visual elements, symmetrical layouts, photographic lighting language.

---

### 4. UGC Style

**Best for:** Authenticity, trust-building, "real person" testimonial feel, cold traffic (UGC outperforms studio by ~28% in engagement)

**Narrative skeleton:**

> A casual selfie-style photograph taken on a smartphone front camera by `{person_description}` in a `{natural_everyday_setting}`. The framing is slightly imperfect — not centred, handheld feel, not composed by a photographer. The person is looking at the camera with `{genuine_expression}`. The background shows their real environment: `{background_details}`. No filters, no heavy editing, no studio polish — this should feel like a text message, not an ad.
>
> Camera and lighting: typical phone front-camera perspective, mild wide-angle lens distortion, indoor natural daylight or window light, no professional lighting setup, slight exposure imperfection.
>
> Colour palette: naturally occurring tones from the environment, with `{brand_colour hex}` showing subtly through `{a visible prop / product / screen}`.
>
> Layout: subject off-centre, phone-camera eye level, reserved space in the bottom third for overlay caption.

**Fill-in guide:**
- Subject: pull from `brand-guidelines.md` Veo character anchors (Agency Founder or Agency PM) when appropriate
- Context: their kitchen, car, warehouse, job site — never an office backdrop
- Aesthetics: deliberately imperfect, authentic, "text from a friend"
- Directive: relatability first, trust second

**Avoid:** professional lighting, perfect composition, model-quality appearance, staged-looking hands.

---

### 5. Before-After

**Best for:** Transformation stories, problem-solution, "old way vs new way" comparisons, Huel-style meme-native splits

**Narrative skeleton:**

> A split-composition advertisement showing a transformation. The left `{before_percentage}%` of the frame shows `{before_state}` — muted colours, slightly desaturated, conveying `{before_emotion — overwhelm, friction, sprawl}`. The right `{after_percentage}%` shows `{after_state}` — vibrant colours in `{brand_colours hex}`, conveying `{after_emotion — calm, clarity, ownership}`. The same subject or environment appears in both halves for direct comparison.
>
> Camera and lighting: matched framing across both halves, dramatic lighting shift from left (flat, grey, cool) to right (warm, directional, alive). A clear visual dividing line between the two states — `{divider_style}`.
>
> Colour palette: desaturated cool tones on the left (`{muted hex}`), branded warm tones on the right (`{brand hex codes}`).
>
> Layout: vertical 50/50 split or 40/60 favouring the "after". Divider can be diagonal for added energy.

**Fill-in guide:**
- Subject: same subject in both halves (person, product, screen, workspace)
- Context: the same environment in both states
- Directive: make the upgrade feel obvious at a single glance

**Avoid:** unclear what changed, too-subtle differences, text-only before/after labels.

---

### 6. Data / Stats

**Best for:** Authority positioning, proof-based claims, "by the numbers" angles, ROI storytelling

**Narrative skeleton:**

> A clean infographic-style advertisement. A prominent key metric dominates the frame: the anchor text `"{key_metric — max 8 chars}"` rendered in a heavy geometric sans-serif, `{accent_colour hex}`, occupying roughly `{percentage}%` of the frame width. A minimal supporting visual sits alongside: `{data_visualisation — simple bar, single icon, abstract shape}`. Nothing else competes for attention.
>
> Camera and lighting: flat graphic treatment with subtle depth from a soft drop shadow behind the metric. Clean margins, grid-aligned.
>
> Colour palette: clean `{background hex}` background with subtle `{texture or grid pattern at low opacity}`, anchor text in `{accent hex}`, supporting elements in `{secondary hex}`.
>
> Layout: visual hierarchy runs number → context → source, top to bottom. Generous margins.

**Fill-in guide:**
- Subject: the number is the subject — it must own 30–40% of visual weight
- Context: none — this is pure infographic
- Directive: authority, credibility, "these people know what they're doing"

**Avoid:** complex charts, more than 3 data points, small unreadable numbers, corporate clip-art icons.

---

### 7. Pain Point

**Best for:** Problem-aware audiences, "does this sound familiar?" hooks, recognition-driven angles

**Narrative skeleton:**

> A visual metaphor photograph that captures the feeling of `{pain_point}`. `{metaphor_description}` — the image should immediately evoke `{target_emotion — overwhelm, frustration, that drowning-in-admin feeling}` without being depressing. A single powerful focal point, minimal distracting elements, a slightly moody register that creates recognition, not despair.
>
> Camera and lighting: medium shot with a longer lens (85mm+) for compression, cooler natural lighting, slightly desaturated tones, dramatic but not dark — the viewer should recognise themselves, not pity the subject.
>
> Colour palette: cool neutral tones (`{muted hex}`), with a single subtle `{brand accent hex}` element hinting at the solution.
>
> Layout: eye naturally moves toward the `{solution_hint_area}`. Reserved space for the hook line in `{text_position}`.

**Fill-in guide:**
- Subject: a metaphor, not a literal complaint (a cluttered desk, a phone lit up with notifications at 11pm, tabs stacked on a browser)
- Context: the pain point's natural habitat
- Directive: recognition — "that's me"

**Avoid:** overly negative imagery, clichés (head in hands, fake stressed faces), stock photo sadness.

---

### 8. Social Proof

**Best for:** Testimonial-based ads, case study highlights, trust-signal stacking

**Narrative skeleton:**

> A testimonial-style advertisement layout featuring `{subject_description — real person headshot or client logo}` positioned `{position}`. A clean, credible atmosphere — real person, real result, no corporate polish. A subtle trust-signal treatment: `{star rating visual / client logo / result metric}` prominently visible.
>
> Camera and lighting: natural portrait lighting if a person, flat graphic treatment if a logo. Warm, approachable, credible.
>
> Colour palette: clean `{background hex}` base with `{brand_accent hex}` as the trust marker colour. Warm, trustworthy, never cold or corporate.
>
> Layout: subject anchors one side of the frame, the other side reserves space for the quote text overlay. Trust signals (stars, result numbers) sit along the bottom third.

**Fill-in guide:**
- Subject: a real-feeling person (pull from Veo character anchors) or a real client logo from `brand-guidelines.md` proof points
- Context: the person's real setting, not a testimonial-video studio backdrop
- Directive: believability — "this actually happened to someone like me"

**Avoid:** fake-looking testimonials, too many trust signals competing, corporate stock photos, obvious staged "happy customer" energy.

---

## General Rules for All Templates

1. **Text space:** Leave 30–50% of the image clear for headline/copy overlay. Meta ads need this; the 20% text rule is gone but the spirit (keep text minimal, let copy do the work in Ads Manager) still holds.
2. **Brand consistency:** Always reference explicit hex codes from `brand-guidelines.md` — never generic colour names.
3. **Mobile-first:** Images are viewed on phones. Large elements, high contrast, no fine details.
4. **Aspect-specific adjustments:**
   - **4:5** (Feed default): balanced composition, centred or rule-of-thirds, 15% CTR boost over 1:1
   - **1:1** (Feed square): symmetric compositions, carousel consistency
   - **9:16** (Stories / Reels): top-heavy or centred content, reserve top and bottom ~14% for UI
   - **1.91:1** (landscape in-stream): wide composition, hero element left or centre
5. **Text in images:** Render SHORT anchor text only (numbers, ≤8-char tags, strikethrough comparisons) and always in double quotes with font direction. Never render paragraphs or full sentences — they garble. Reserve space explicitly when text is post-production.
6. **Positive constraints only:** Never write "no X, no Y" lists. Describe the desired state positively.
7. **Narrative prose only:** Final prompts are creative-director paragraphs, not labelled blocks.
