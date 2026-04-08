---
name: generate-videos
description: Generate ad videos in 9:16 and 1:1 formats via Veo 3.1 with extremely detailed scene prompts — scenes, accent, avatar, transitions, motion
menu-code: GV
---

# Generate Videos

Produce ad videos for angles using Veo 3.1 (default for UGC) and Kling (animated graphics only) via fal.ai, with structured motion patterns and mandatory quality gates. Every video requires an extremely detailed scene-by-scene prompt before generation.

## Process

1. **Load creative-data.json** — Read `marketing-plugin/data/creative-data.json`. When `{active_campaign}` is set, filter batches to those with matching `campaign_id` and show only campaign-relevant batches. When `{active_campaign}` is null, show all batches. Find the current batch (most recent matching) or ask the user which batch to use.

2. **Load references** — Read these before building any scene prompts:
   - `marketing-plugin/references/video-prompt-templates.md` — 8 motion patterns + model selection guide + Multi-Scene UGC template
   - `marketing-plugin/references/brand-guidelines.md` — brand tone, colours, character anchors, expression rules

3. **Select angles** — Show the user the angles in the batch. Ask: "Generate videos for all angles, or select specific ones? (default: all)"

4. **For each selected angle:**

   a. **Select model:**
      - **Veo 3.1 Lite (DEFAULT)** — for all UGC and talking head videos. `--model veo` (lite is the default tier). Up to 30s duration (auto-chains via image-to-video if >8s). Native audio + lip-sync. ~$0.05/s.
      - **Veo 3.1 Fast/Standard** — for premium output when lite quality isn't sufficient. `--model veo --tier fast` ($0.15/s) or `--tier standard` ($0.40/s). Chains via extend-video, max 20s.
      - **Kling 3.0** — ONLY for animated graphics (image-to-video). Requires an existing generated image. `--model kling --image {path}`. ~$0.15/video.
      - **HeyGen** — ONLY for budget/long-form (30-90s). `--model heygen`. Last resort.

   b. **Select a motion pattern** from `video-prompt-templates.md` based on the angle's hook type:

   | Hook Type | Recommended Pattern |
   |-----------|-------------------|
   | **UGC/Talking Head** | **Multi-Scene UGC (PRIMARY — use this by default)** |
   | Curiosity | Slow Reveal |
   | Urgency | Quick Cuts |
   | Pain Point | Static-to-Motion |
   | Testimonial/Social Proof | Slow Zoom |
   | Before-After | Split Wipe |
   | Product Demo | Orbit |
   | Brand/Awareness | Drift |

---

## Mandatory Scene Breakdown (HARD BLOCKER)

Before constructing any prompt, build a complete scene breakdown. This is not optional — every field must be filled for every scene. Present this to the user for approval before proceeding to prompt construction.

### Step 1: Select Character Anchor

1. Choose the character: **Agency Founder** or **Agency PM** (from `brand-guidelines.md`)
2. Display the FULL character anchor text — every detail (age, build, height, hair, facial hair, skin, clothing fabric/colour/fit, accessories, posture, expression baseline, energy, accent)
3. Confirm with user: "This character anchor will be used identically across ALL scenes. Confirm or adjust?"

**CRITICAL:** The character anchor is written ONCE in the prompt and reused verbatim in every scene. Changing ANY detail (hair, clothing, build, accessories) between scenes will cause Veo 3.1 to render a different person. Verify clothing, hair, build, and accessories are identical in every scene reference.

### Step 2: Build Scene-by-Scene Breakdown

For EACH scene (typically 3-4 scenes, up to 30s recommended, auto-chains if >8s), fill in ALL fields:

| Field | What to Specify | Example |
|-------|----------------|---------|
| **Scene # + Duration** | Exact timing | "Scene 1 (0-3s)" |
| **Environment** | Specific setting, lighting direction/quality/colour temp (Kelvin), materials, objects, time of day. NEVER generic — no "an office" or "a room" | "Modern home office, floor-to-ceiling window camera-left, warm 4200K afternoon light, ultrawide curved monitor on timber desk showing analytics, ceramic white mug, indoor fern in terracotta pot" |
| **Background Motion** | Environmental movement that makes the scene alive. Static environments look artificial | "Curtain drifts from breeze, monitor data refreshes with subtle glow, steam wisps from coffee, fern leaf sways" |
| **Character Action** | Physical movement with realistic physics. No static talking heads | "Walks briskly from doorway, heel-first with visible weight transfer, reaches for chair, sits with controlled drop" |
| **Object Interaction** | Specific object + specific action | "Picks up coffee mug with right hand, takes sip between sentences, sets down — ceramic clinks on timber" |
| **Exact Dialogue** | Word-for-word script | "You know what kills most small businesses? It's not competition. It's the twenty hours a week you spend on stuff that should take two." |
| **Accent & Delivery** | Region + register + pace + tone. ALL four required | Region: "suburban Sydney Australian". Register: "warm baritone". Pace: "3 words/sec, pause before 'twenty'". Tone: "conversational, measured confidence" |
| **Micro-Expression** | Tied to specific dialogue word(s) | "Eyebrow raise on 'kills', jaw sets on 'twenty hours', asymmetric smile on 'should take two'" |
| **Camera** | Framing + movement + depth of field | "Steadicam follow from slightly ahead, medium shot waist up, shallow DoF — subject sharp, background softly blurred" |
| **Transition to Next** | Specific type between this scene and the next | "Hard cut" / "Match-cut on hand gesture" / "Camera push-through monitor" / "Whip pan right" |
| **Ambient Audio** | Scene-specific sounds (not generic) | "Office ventilation hum, distant keyboard clicks, ceramic mug clink on timber, chair mechanism click" |

### Step 3: Pre-Generation Quality Checklist

**ALL items must pass. If ANY fails → fix it before proceeding. Do NOT generate.**

1. [ ] **Scene durations do not exceed 30s recommended** (32s hard max for lite, 20s for standard/fast — if video_brief from [BA] exceeds limit, rewrite durations. Script auto-chains if >8s.)
2. [ ] Character anchor copied verbatim from brand-guidelines.md — not paraphrased or abbreviated
3. [ ] Character anchor appears ONCE in the prompt — not duplicated or varied between scenes
4. [ ] Every scene has a specific, unique environment (no "same office as Scene 1", no generic "an office")
5. [ ] **No readable text, specific UI, or named interfaces on any screen/monitor** — screens show abstract visuals only (soft colour blocks, blurred shapes, ambient glow). See "Veo 3.1 Limitations" in video-prompt-templates.md
6. [ ] Every scene has background/environmental motion (no static environments)
7. [ ] Every scene has physical character movement (no static talking heads)
8. [ ] Exact dialogue written word-for-word for every scene
9. [ ] Accent region + register + pace + tone specified for every scene's dialogue
10. [ ] Micro-expressions tied to specific dialogue words in every scene
11. [ ] Camera framing, movement, and depth of field specified per scene
12. [ ] Transition type explicitly specified between every scene pair
13. [ ] Ambient audio specified per scene with scene-specific sounds (not generic)
14. [ ] Object interaction with specific named objects in at least 2 of 3 scenes
15. [ ] **STYLE layer included** — camera/lens model, film stock/grade, and 2-3 imperfection cues (see "Realism Boosters" in video-prompt-templates.md)
16. [ ] Total prompt length 300-500 words
17. [ ] Duration does not exceed 30s recommended (32s hard max for lite)

**Present the complete scene breakdown table to the user.** Wait for explicit approval or refinement requests. If the user identifies missing detail, fill it in and re-present.

---

## Prompt Construction

After the scene breakdown is approved, construct the 6-layer prompt.

### Building the Prompt

1. **Load character anchor** from `brand-guidelines.md` — copy the full character description for the specified character (Agency Founder or Agency PM). This anchor is used VERBATIM.

2. **Load motion pattern** from `video-prompt-templates.md` — use the pattern specified in `visual_brief.video_brief.motion_pattern` or as selected above.

3. **Construct the 6-layer prompt:**

```
STYLE: [Camera/lens — e.g., "Shot on Sony FX3, 35mm f/1.4 Sigma Art lens". 
Film stock — e.g., "Natural colour grade, warm skin tones, slightly desaturated highlights". 
Imperfection cues — 2-3 from Realism Boosters in video-prompt-templates.md, e.g., 
"Micro dust motes in light beams, natural skin texture in close-ups, slight lens breathing 
on focus pulls".]

ENVIRONMENT: [From the scene breakdown. Specific setting, lighting direction/quality/colour 
temperature, background elements with materials and colours, time of day. 
EACH SCENE gets its own environment block — describe fresh every time.
SCREEN CONTENT RULE: Any monitor/laptop/phone shows ABSTRACT visuals only — soft colour 
blocks, blurred shapes, ambient glow. Never specific UI, text, or named interfaces.]

CHARACTER: [Full character anchor from brand-guidelines.md, copied verbatim.
This block appears ONCE and applies to ALL scenes. DO NOT modify between scenes.]

ACTION & DIALOGUE:
Scene 1 ({duration}): {Character name} {physical action with physics — "walks briskly, 
heel-first, visible weight transfer"}. {Object interaction — "picks up coffee mug with 
right hand, takes sip"}. {Micro-expression} on "{specific dialogue word}". 
Dialogue: "{Exact spoken words}" — {accent region}, {register}, {pace}, {tone}. 
Background motion: {environmental movement in this scene}.

Scene 2 ({duration}): Hard cut to {new environment with full description}. 
{Character} {different physical action anchored to new object}. 
{New micro-expressions tied to new dialogue words}.
Dialogue: "{Next portion}" — {delivery adjustments from Scene 1 if any}.
Background motion: {different environmental movement}.

Scene 3 ({duration}): {Third environment or tighter framing of previous}. 
{Final action — stillness and eye contact can be powerful here}. 
{Final micro-expression}. 
Dialogue: "{Final line — hook payoff or CTA}" — {slower pace for impact}.
Background motion: {quieter — intimacy}.
{Holds eye contact, slight confident nod after final word}.

CAMERA:
Scene 1: {Framing — medium shot, waist up}. {Movement — steadicam follow from slightly 
ahead}. {Depth of field — shallow, subject sharp, background softly blurred}. 
Transition to Scene 2: {hard cut / match-cut on {specific element} / camera push through}.

Scene 2: {Different framing — static medium-close, chest up}. {Movement — static or 
gentle drift}. {DoF — deep, showing full environment}. 
Transition to Scene 3: {type}.

Scene 3: {Framing — slowly pushes in from medium to close-up}. {Movement — slow push-in 
over full scene duration}. {DoF — increasingly shallow, isolating face}.

AUDIO & STYLE:
Voice: {accent region — "suburban Sydney Australian"}, {register — "warm baritone"}, 
{pace — "3 words/sec, slowing to 2.5 in Scene 3"}.
Ambient Scene 1: {specific sounds — keyboard clicks, coffee mug clink, office hum}.
Ambient Scene 2: {different sounds — espresso machine, conversation murmur}.
Ambient Scene 3: {quieter — room tone only, intimacy}.
Music: {direction — "none" / "subtle lo-fi underneath, never competing with dialogue"}.
Mood: {overall energy — "confident and measured, building to calm authority"}.
Style reference: match the energy and pacing of {inspiration video path if available}.
No captions or subtitles (added in post-production).
```

### Critical Rules
- **Duration budget:** Total scene durations should not exceed 30s (recommended). If the video_brief from [BA] has durations exceeding 30s, rewrite them and inform the user. Each scene should map to one clip (6-8s) for best lite quality.
- **Character consistency:** The CHARACTER block is written ONCE. Veo 3.1 uses this to maintain the same person across all scenes. Changing ANY detail (hair, clothing, build) between scenes will produce a different person.
- **Movement is realism:** Every scene must include physical movement — walking between positions, sitting down, picking up objects, shifting weight, gesturing. Static talking heads are the #1 tell for AI-generated video.
- **Background motion is life:** Every scene must include environmental movement — curtain drift, screen glow, steam, light shifts, background figures. Static environments look dead.
- **Screens show abstract content only:** Veo 3.1 cannot render readable text. Any monitor, laptop, or phone screen must show abstract visuals — soft colour blocks, blurred shapes, ambient glow, shifting gradients. Never reference specific UI elements, dashboards, or readable text on screens. The story is told through dialogue and action.
- **Micro-expressions:** Tie specific expression changes to specific dialogue words. "Slight eyebrow raise on 'five'" is more effective than "looks interested."
- **Scene environments:** Each scene gets its OWN unique environment description. Don't write "same office as Scene 1" — describe it fresh so Veo 3.1 renders it consistently.
- **Transitions:** Explicitly specify the transition type between every scene pair. Never leave it to the model's default.
- **Accent & delivery:** Every dialogue block must specify accent region, register, pace, and tone. These can vary between scenes for dynamics.
- **No captions:** Subtitles and text overlays are added in post-production, not in the video prompt.
- **Film-language realism:** Include a STYLE layer with camera/lens model, film stock/grade, and imperfection cues. See "Realism Boosters" in `video-prompt-templates.md`.

### Approval Gate

**BEFORE calling the video generation API, present ALL of the following:**

1. Full 6-layer prompt text (every word that will be sent to the API)
2. Character anchor confirmation (which character, displayed in full)
3. Scene summary table:
   | Scene | Duration | Environment | Action | Dialogue (first 5 words...) | Transition |
4. Background motion per scene
5. Audio direction (accent, register, pace per scene)
6. Model + estimated cost (e.g., "Veo 3.1, 12s, ~$4.80" or "Veo 3.1 fast, 12s, ~$1.80")
7. Motion pattern name

**If any element is missing or vague, do NOT proceed.** Fill in the gap and re-present. Wait for user approval.

---

## Generation

   c. **Generate end card image** — Before generating videos, create a custom end card for this angle's CTA:

   ```bash
   python3 {plugin_root}/scripts/generate-ad-image.py \
     --ref-dir {plugin_root}/data/reference-images/ \
     --prompt "Meta ad end card, {aspect} format. Solid black (#000000) background. Centred: green gear logo from reference images at 25% frame width. Below: '{YOUR_COMPANY}' in white bold sans-serif. Below: 'www.{YOUR_DOMAIN}' in smaller white. Below: rounded Electric Blue (#3B82F6) button with white text '{cta_text}'. Minimal, clean, premium." \
     --aspect {aspect} \
     --output {plugin_root}/data/creatives/{batch_id}/{angle_id}-endcard-{aspect_slug}.png
   ```

   Where `{cta_text}` is the angle's CTA (e.g., "Book Your Free Audit", "Get Started", "Learn More"). Use the `-2` variant (HD) for the end card.

   d. **Generate video with watermark + end card (9:16 vertical only):**

   ```bash
   python3 {plugin_root}/scripts/generate-ad-video.py \
     --prompt "{full_6_layer_prompt}" \
     --aspect 9:16 \
     --model veo \
     --duration {total_scene_duration} \
     --end-card {plugin_root}/data/creatives/{batch_id}/{angle_id}-endcard-9x16-2.png \
     --output {plugin_root}/data/creatives/{batch_id}/{angle_id}-9x16.mp4
   ```

   Where `{plugin_root}` is `marketing-plugin`. The script automatically:
   - Generates the video via Veo 3.1 lite (default) with native audio + lip-sync
   - Auto-chains if duration >8s: lite uses last-frame extraction + image-to-video; standard/fast use extend-video
   - Applies logo watermark (green gear, bottom-right, 20% width, 30% opacity)
   - Appends the end card (3s, fade-in from black)

   **Tier options:** Default is lite ($0.05/s). Add `--tier fast` ($0.15/s) or `--tier standard` ($0.40/s) for premium quality.

   **Format:** 9:16 vertical only. Square (1:1) is not generated — Meta Reels/Stories placements use 9:16 and it's not cost-effective to generate both.

   e. **Post-Generation Validation** — After each video is generated, review and report:

   1. Character consistent across all scenes (same face, hair, clothing, accessories)?
   2. Dialogue lip-sync natural (mouth movements match words)?
   3. Movement realistic (no AI float/glide/teleportation)?
   4. Background motion present (environments feel alive)?
   5. Environment lighting consistent within each scene?
   6. Transitions clean between scenes?
   7. First 3 seconds grab attention (hook timing)?
   8. Accent sounds correct (Australian, not American/British)?

   **DO NOT auto-regenerate.** Veo 3.1 is expensive. Report any issues to the user with specific notes on what failed and which prompt layer to adjust. The user decides whether to regenerate.

   f. **Update the angle in creative-data.json:**
   - Add generated video to `videos` array (9:16 only):
     ```json
     {
       "format": "9:16",
       "path": "data/creatives/{batch_id}/{angle_id}-9x16.mp4",
       "prompt": "{full 6-layer prompt used}",
       "duration": "{total_scene_duration}",
       "model": "veo",
       "motion_pattern": "{pattern_name}",
       "end_card_cta": "{cta_text}",
       "has_watermark": true
     }
     ```
   - Set `status` to `"videos_generated"`

5. **Update meta** — Recalculate `meta.total_creatives`. Update `meta.last_generation`.

6. **Report:**

   ```
   Video Generation Complete — Batch: {batch_id}

   | Angle | Motion Pattern | Model | 9:16 | Status |
   |-------|---------------|-------|------|--------|
   | {name} | {pattern} | veo | OK | videos_generated |
   | ... |

   Total videos generated: {count}
   Estimated cost: ~${total_seconds * 0.40}
   Output directory: data/creatives/{batch_id}/

   Next: Run [PC] to package all creatives for upload.
   ```

## Error Handling

- Veo 3.1 generation takes 60-300s per clip. Chained videos (>8s) require multiple API calls — expect 2-5 minutes per clip in the chain. The script polls fal.ai every 5s until completion (max 600s per clip).
- If a generation fails, log the error and continue with the next format/angle
- Mark failed generations in the videos array with `"status": "failed"` and `"error": "{message}"`
- If Veo 3.1 produces inconsistent character across scenes, the extend-video chaining should handle this automatically (character inherits from previous clip). If still inconsistent, add more distinguishing features to the character anchor.
- If Veo 3.1 produces unnatural movement, adjust the Action & Dialogue layer — add more physics detail (weight transfer, object interaction, micro-movements)
- If accent sounds wrong, strengthen the accent direction — specify region more precisely (e.g., "inner-west Sydney" not just "Australian")
- Report failures at the end so the user can re-run for specific angles
