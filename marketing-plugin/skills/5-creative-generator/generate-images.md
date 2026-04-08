---
name: generate-images
description: Generate ad images in 9:16 vertical format via Nano Banana Pro for selected angles
menu-code: GI
---

# Generate Images

Produce ad images for angles using Nano Banana Pro via the image generation script.

## Process

1. **Load creative-data.json** — Read `marketing-plugin/data/creative-data.json`. When `{active_campaign}` is set, filter batches to those with matching `campaign_id` and show only campaign-relevant batches. When `{active_campaign}` is null, show all batches. Find the current batch (most recent matching) or ask the user which batch to use if multiple exist.

2. **Select angles** — Show the user the angles in the batch. Ask: "Generate images for all angles, or select specific ones? (default: all)"

3. **Load references** — Read these before generating any prompts:
   - `marketing-plugin/references/image-prompt-templates.md` — 8 structured templates
   - `marketing-plugin/references/brand-guidelines.md` — brand colours, tone, restrictions
   - `marketing-plugin/references/openrouter-image-api.md` — model and API reference

4. **For each selected angle:**

   **Model:** All production images MUST use **Nano Banana Pro** (`google/gemini-3-pro-image-preview`). This is the default in `generate-ad-image.py`. Never use the Flash variant for production creatives.

   a. **Load inspiration analysis from competitor-data.json** — For each angle's `inspiration_ads`, find the ad by `ad_id` in competitor-data.json and extract the full `analysis` object. This contains the detailed visual breakdown already performed by the Competitor Intelligence agent.

   b. **Build the inspiration blueprint** — From the analysis, extract:
   ```
   LAYOUT:      {analysis.VISUAL DESCRIPTION.layout_composition}
   BACKGROUND:  {analysis.VISUAL DESCRIPTION.background_treatment}
   COLOURS:     {analysis.VISUAL ANALYSIS.dominant_colours} (hex codes)
   TYPOGRAPHY:  {analysis.VISUAL DESCRIPTION.typography_style}
   TEXT:         {analysis.VISUAL ANALYSIS.text_on_image_content}
   BRANDING:    {analysis.VISUAL DESCRIPTION.branding_elements}
   DECORATIVE:  {analysis.VISUAL DESCRIPTION.decorative_elements}
   CTA:         {analysis.VISUAL DESCRIPTION.cta_placement}
   SCENE:       {analysis.VISUAL DESCRIPTION.scene_description}
   BRIEF:       {analysis.COMPETITIVE INTEL.creative_brief}
   REPLICABLE:  {analysis.COMPETITIVE INTEL.replicable_elements}
   ```

## Prompt Construction Standard

**Core principle:** The inspiration ad's EXISTING analysis in competitor-data.json contains a 65+ field visual breakdown — exact layout, hex colours, typography, text content, spatial positioning, and a designer-ready creative brief. Load this analysis and use it to construct an extremely detailed reconstruction prompt. Never write prompts from scratch or from memory of what the image looks like.

### Step 1: Extract the blueprint
Load the analysis fields listed above. Present the blueprint to yourself before writing the prompt.

### Step 2: Semantic mapping (critical thinking step)
For every element in the inspiration, ask: **"What is this element DOING in the ad, and what's OUR equivalent?"**

Don't just swap text — understand the PURPOSE of each visual element:
- Their headline → our headline (same job: hook the reader)
- Their subtext/tagline → our subtext (same job: support the hook)
- Their feature list items → our feature list items (same job: prove the claim)
- Their CTA text → our CTA text
- Their logo/branding → logo (from reference image) in the same position
- **Their visual metaphors → OUR equivalent metaphor for OUR product.** This is the critical step most prompts miss. Examples:
  - Zapier uses coloured app icon squares to represent integrations → we should use recognisable tool icons (Fathom microphone icon, Claude AI icon, process map icon, prototype wireframe icon) to represent OUR integrations
  - A dashboard screenshot showing their product → a dashboard screenshot showing OUR product (process maps, client portals)
  - A person pointing at features → a person interacting with OUR type of output
  - Random decorative shapes → shapes that relate to our workflow (document icons, connection lines, pipeline arrows)

**Rule: Every visual element must be semantically relevant to our product and argument. No random colours, abstract shapes, or meaningless decoration that was only meaningful in the competitor's context.**

### Step 3: Build the prompt
```
Recreate this exact ad layout:

LAYOUT: [paste layout_composition VERBATIM from analysis]
BACKGROUND: [paste background_treatment VERBATIM — includes hex codes]
COLOURS: Use these exact colours: [paste dominant_colours array]
TYPOGRAPHY: [paste typography_style VERBATIM — font weights, sizes, hierarchy]
DECORATIVE ELEMENTS: [paste decorative_elements VERBATIM]

Replace these specific elements:
- Where the inspiration shows "[their headline text]" → show "[our headline]"
- Where the inspiration shows "[their subtext]" → show "[our subtext]"
- Where the inspiration shows [their product visual/UI cards/illustration] → show [our equivalent visual metaphor relevant to our product]
- Where the inspiration shows [their logo] → show the exact logo from the reference image, same position and size
- Where the inspiration shows "[their CTA]" → show "[our CTA]" OR leave clear space

Keep EVERYTHING else identical to the inspiration: same spatial proportions, same colour relationships, same background treatment, same typography weight hierarchy, same decorative elements.

Aspect ratio: 9:16. No AI artifacts.
```

### Message Clarity Rule (mandatory)

Every generated image MUST communicate the angle's core value proposition through a combination of visual composition AND rendered text. A person scrolling with zero context about or the industry must instantly understand the message.

**Text rendering is REQUIRED when:**
- The inspiration ad renders text (swap their text for ours — same job, our message)
- The angle's value proposition cannot be understood from visuals alone
- Numbers, comparisons, or guarantees are central to the angle (e.g., "200" crossed out → "20", "$5K/month", "5 audits")

**Text rendering rules:**
- Keep rendered text SHORT — max 2-3 words per text element, ideally numbers or punchy phrases
- Use colour contrast to make text the focal point (e.g., red strikethrough on old number, green on new number)
- Position text as the visual anchor — it should be what the eye hits first
- Numbers and symbols render better than long words
- The model handles bold, short text well; it struggles with paragraphs
- Never render full sentences or paragraphs — these will be garbled

**Before finalising any prompt, ask:** "If someone who has never heard of sees this image for 1 second while scrolling, will they understand what we're selling?" If the answer is no, the prompt needs stronger visual messaging.

### Colour Rules
- Use the inspiration's ACTUAL hex colours from `dominant_colours` — NOT brand colours
- The analysis has already extracted the exact palette
- Only the logo uses brand colours
- Different colour schemes across angles = better A/B testing

### Prompt Hygiene
- NEVER include composition percentages as literal text — the model renders them
- NEVER include CSS values ("50% opacity") — same problem
- NEVER say "post-production headline" — the model renders it literally
- For longer ad copy (primary text, descriptions): leave clear space and add in Meta Ads Manager
- For anchor text (numbers, short phrases, value props): render directly in the image — this is the visual hook

### Loading Brand Logo as Reference
**ALWAYS** pass the logo via `--ref-dir`:

```bash
mkdir -p /tmp/ref-apg-logo
cp {plugin_root}/data/reference-images/apg-logo-dark.png /tmp/ref-apg-logo/
```

### Loading Inspiration Images
Pass the actual inspiration images via `--inspo-dir` alongside the analysis-driven prompt:
```bash
mkdir -p /tmp/inspo-{angle_id}
cp {plugin_root}/{inspiration_ad.local_path} /tmp/inspo-{angle_id}/
```

### Concept Review Gate

**BEFORE showing the prompt to the user**, the agent MUST perform a structured relevance review of the entire prompt. For every visual element in the prompt, verify it passes this checklist:

1. **Colour relevance** — Does every colour in the prompt have a clear source (from the inspiration analysis `dominant_colours`)? Remove any colours that appeared randomly or have no connection to the message.
2. **Component relevance** — Does every visual component (icons, shapes, illustrations, UI elements) directly relate to {YOUR_COMPANY}'s product or the angle's specific message? If a component only made sense in the competitor's context, replace it with an APG-relevant equivalent or remove it.
3. **Metaphor relevance** — Do all visual metaphors communicate something meaningful about THIS angle's argument? A "split screen showing before/after" must show OUR before/after, not abstract shapes.
4. **Composition coherence** — Does the overall image tell a single, clear story that a viewer would understand without context? Every element should reinforce the same message.
5. **No filler** — Remove any decorative elements, abstract patterns, or background details that exist purely because the inspiration had them but serve no communicative purpose for our ad.

**If any element fails:** Rewrite that part of the prompt with the correct APG-relevant replacement before proceeding. Do not pass a prompt with irrelevant elements through to generation.

### Approval Gate

**After the concept review, present to the user:**
1. The reviewed prompt with annotations explaining what each major element communicates
2. Any elements that were changed during the concept review and why
3. Which inspiration images will be loaded
4. Wait for user approval or refinement

### Post-Generation Validation (Vision Gate)
After generation, the agent MUST look at each generated image and critically evaluate:

**Layout & Style (compare to inspiration):**
1. Does the layout match the inspiration's spatial arrangement?
2. Does the colour palette match the inspiration's dominant_colours?
3. Is our text swapped in correctly and readable?
4. Is the logo present and recognisable?
5. No AI artifacts (garbled text, extra elements, distortions)?

**Semantic Relevance (critical thinking):**
6. Does EVERY visual element make sense for our product and argument?
7. Are there random/meaningless elements that only made sense in the competitor's context? (e.g., random colour blocks that represented THEIR app integrations but mean nothing for us)
8. Would a viewer unfamiliar with the inspiration ad understand what every element represents?
9. Does the image tell a coherent story about OUR product?

**If any semantic check fails:** Identify the meaningless elements, determine what OUR equivalent should be, update the prompt with specific replacements, and re-generate. Don't accept images with elements that don't serve our message just because they matched the inspiration's layout.

   c. **Prepare inspiration images** — For each angle, copy the `inspiration_ads` images (from their `local_path`) into a temporary directory:

   ```bash
   mkdir -p /tmp/inspo-{angle_id}
   cp {plugin_root}/{inspiration_ad_1.local_path} /tmp/inspo-{angle_id}/
   cp {plugin_root}/{inspiration_ad_2.local_path} /tmp/inspo-{angle_id}/
   ```

   d. **Generate one image in 9:16** — One image per angle, vertical format only:

   ```bash
   python3 {plugin_root}/scripts/generate-ad-image.py \
     --ref-dir /tmp/ref-apg-logo/ \
     --inspo-dir /tmp/inspo-{angle_id}/ \
     --prompt "{prompt}" \
     --aspect 9:16 \
     --output data/creatives/{batch_id}/{angle_id}-9x16.png
   ```

   Where `{plugin_root}` is `marketing-plugin`. The `--ref-dir` passes the logo so the model reproduces it exactly. The `--inspo-dir` passes the competitor winner images as the visual base — the generated ad should closely recreate the winner's layout, colour scheme, and design language but with our content swapped in.

   e. **Update the angle in creative-data.json:**
   - Add generated image path to `images` array:
     ```json
     {
       "format": "9:16",
       "path": "data/creatives/{batch_id}/{angle_id}-9x16.png",
       "prompt": "{prompt used}",
       "template": "{template name used}"
     }
     ```
   - Set `status` to `"images_generated"`

5. **Update meta** — Recalculate `meta.total_creatives` (count all images + videos across all batches). Update `meta.last_generation`.

6. **Report:**

   ```
   Image Generation Complete — Batch: {batch_id}

   | Angle | 9:16 | Status |
   |-------|------|--------|
   | {name} | OK | images_generated |
   | ... |

   Total images generated: {count}
   Output directory: data/creatives/{batch_id}/

   Next: Run [GV] to generate videos, or [PC] to package for upload.
   ```

## Error Handling

- If a generation fails, log the error and continue with the next format/angle
- Mark failed generations in the images array with `"status": "failed"` and `"error": "{message}"`
- Report failures at the end so the user can re-run for specific angles
