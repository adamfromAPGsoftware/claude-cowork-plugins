---
name: 'step-05-image'
description: 'Generate images via fal-ai nano-banana-2 — comparison graphics, annotated screenshots, any non-identity image'

pipelineScriptsData: '../data/pipeline-scripts.md'
---

# Step 5: General Image Creation

## STEP GOAL:

To generate images via fal-ai MCP (model: `fal-ai/nano-banana-2`) for any use case that doesn't require identity preservation — comparison graphics, logo combinations, annotated screenshots, style transfers, and freeform image generation.

> **MANDATORY TOOL + MODEL RULE:**
> - Text-only → `generate_image` with `model_id: "fal-ai/nano-banana-2"`
> - With reference photo → `edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`
> - Never use `generate_image_from_image` — the model expects `image_urls` (array), not `image_url` (string). `edit_image` wraps correctly.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Creative Director with expertise in image composition and visual design
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring visual design expertise — composition, colour theory, contrast
- ✅ The user brings their content need and desired outcome

### Step-Specific Rules:

- 🎯 Focus on general image generation
- 🚫 FORBIDDEN to execute the script before user approves the prompt
- 💬 Help the user describe their desired image with specificity
- 📋 If the image includes a person, **default to using reference photos** from `{reference_photos_folder}` for identity preservation (same protocol as thumbnails — load all 5 in order, never describe face in prompt)
- 📋 If the user explicitly wants a person who is NOT the creator, they'll say so — otherwise assume it's the creator

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 📖 Execute script via bash tool call
- 🚫 FORBIDDEN to skip prompt review

## CONTEXT BOUNDARIES:

- Available: CCS config, brand tokens, project context
- Focus: General image generation only
- Limits: For images with people, use reference photos from `{reference_photos_folder}` for identity preservation
- Dependencies: Step 01 init, step 02 selection (IM)

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 0b. Load Social Post Inspiration

Before gathering requirements, auto-check the global social post inspiration folder:

```bash
ls "{workspace}/context/inspiration/social-posts/" 2>/dev/null | wc -l
```

**If images are found:**
- Load `{workspace}/context/references/visual-inspiration.md` and extract the "Social Post Patterns" section.
- If the file does not exist, read up to 3 images directly using the Read tool (multimodal) and note dominant style patterns: background treatment, text density, colour usage, composition style.
- Store as `social_inspiration_notes`.
- Mention inline when presenting to the user: "I have {N} social post inspiration images from your workspace — I'll apply those style patterns to the prompt."

**If the folder is empty:** Continue without blocking.

### 1. Gather Image Requirements

"**What image do you need?**

Tell me:
1. **What should the image show?** (be specific — subject, layout, elements)
2. **Any input images?** (logos, screenshots, existing graphics to modify or combine)
3. **Dimensions?** (or I'll use a sensible default)
4. **Style direction?** (dark/light, minimal/detailed, colour palette)

Common use cases:
- Logo 'VS' comparison graphics
- Annotated screenshot overlays
- Abstract concept illustrations
- Social media header graphics

**Note:** If the image includes a person, I'll automatically include your reference photos for identity preservation (same as thumbnails). Let me know if you want someone other than you in the image."

Wait for user input.

### 2. Build the Prompt

Construct a clear image prompt from the user's description.

**If `social_inspiration_notes` were extracted in section 0b**, append as a style modifier at the end of the prompt: `"Style reference from brand inspiration: {social_inspiration_notes}"`

"**Here's the image prompt:**

---
{complete prompt including subject, composition, style, colours, dimensions}
---

**Input images:** {list or 'none — text-only generation'}
**Inspiration applied:** {social_inspiration_notes summary or 'none'}
**Output:** {output path}

**Ready to generate?**"

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Generate Image

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Proceed to execution (section 3)
- IF user wants to modify: Adjust prompt, redisplay
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY execute when user selects 'C'
- After other menu items execution, return to this menu

### 3. Execute Image Generation

Load {pipelineScriptsData} for the fal-ai MCP reference.

Execute via fal-ai MCP:

```
# Text-only generation:
mcp__fal-ai__generate_image(
  model_id="fal-ai/nano-banana-2",
  prompt="[the approved prompt]",
  image_size="[appropriate preset]"
)

# With reference/input images — use edit_image (NOT generate_image_from_image):
mcp__fal-ai__upload_file(file_path="[input image path]")  → input_url
mcp__fal-ai__edit_image(
  model="fal-ai/nano-banana-2/edit",
  image_url=input_url,
  prompt="[the approved prompt]",
  strength=0.92
)
```

> **TOOL + MODEL RULE:** Text-only → `generate_image` with `model_id: "fal-ai/nano-banana-2"`. With any reference image → `edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92`. Never use `generate_image_from_image` — it sends `image_url` as a string but the model expects an array.

Save to: `[output path]/[slug]-image-[date].png`

Report result:
- If success: "**Image generated!** Saved to: {output path} ({size}KB)"
- If failure: Report error, offer to adjust prompt and retry

### 4. Completion

"**Image complete.**

**File:** {output path}

Session complete."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Image requirements gathered with specificity
- Prompt constructed and approved by user
- Script executed successfully
- Output saved to correct location

### ❌ SYSTEM FAILURE:

- Executing before user approves prompt
- Vague prompts without specific composition direction
- Not offering input image support when relevant

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
