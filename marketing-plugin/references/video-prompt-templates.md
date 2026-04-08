# Video Prompt Templates

Structured motion patterns for generating Meta ad videos. The Creative Generator agent MUST select a motion pattern and construct the scene prompt from it.

## Model Selection Guide

| Model | Tier | Cost (720p + audio) | Max Duration | Best For |
|-------|------|---------------------|-------------|----------|
| **Veo 3.1** (fal.ai) | **Lite (DEFAULT)** | **$0.05/s** | **30s recommended (32s max)** | **Default for all UGC — cheap enough for volume** |
| **Veo 3.1** (fal.ai) | Fast | $0.15/s | 20s (extend-video chain) | Premium output when lite quality isn't enough |
| **Veo 3.1** (fal.ai) | Standard | $0.40/s | 20s (extend-video chain) | Maximum quality for hero creatives |
| **Kling 3.0** (fal.ai) | — | ~$0.029/s | 5s | Animated graphics (image-to-video only) |
| **HeyGen** (fal.ai) | — | ~$0.033/s | 90s | Budget / long-form (30-90s). Last resort. |

**Cost examples (Veo 3.1, 720p + audio):**

| Duration | Lite (default) | Fast | Standard |
|----------|---------------|------|----------|
| 8s (single clip) | **$0.40** | $1.20 | $3.20 |
| 16s (2 clips) | **$0.80** | $2.40 | $6.40 |
| 24s (3 clips) | **$1.20** | $3.60 | $9.60 |
| 30s (4 clips) | **$1.60** | N/A | N/A |

**Lite chaining method:** Lite has no extend-video endpoint. Instead, the script auto-chains via **last-frame extraction + image-to-video**: generate clip 1 (text-to-video), extract its last frame, generate clip 2 from that frame (image-to-video), repeat. Character inherits visually from the previous clip's final frame.

**Standard/Fast chaining method:** Uses extend-video endpoint (character inherits from previous clip natively). Max 20s.

**Resolution:** All tiers default to 720p. Lite is cheaper at 720p ($0.05/s vs $0.08/s at 1080p).

**Decision rule:** Default to Veo 3.1 lite for all creatives — it's cheap enough to generate at volume. Use `--tier fast` or `--tier standard` only if lite quality isn't sufficient for a specific creative. Only use Kling for image-to-video animation. Only use HeyGen for budget-constrained long-form.

**Prompting for lite:** Keep prompts focused — one scene per clip. Lite handles straightforward prompts well but complex multi-element scenes degrade. Each clip in a chain gets its own focused prompt with the shared character anchor.

## Veo 3.1 Limitations & Workarounds

Before constructing any prompt, be aware of these hard constraints:

### Duration: Up to 30s Recommended (Auto-Chaining)
Veo 3.1 single clips are max 8 seconds (API accepts 4s/6s/8s). For longer videos, the script **auto-chains**:

- **Lite (default):** Chains via last-frame extraction + image-to-video. Each clip's final frame feeds as the starting image for the next clip. Max 32s (4 × 8s clips).
- **Standard/Fast:** Chains via extend-video endpoint. Character inherits natively. Max 20s.

**How it works:** Pass any duration from 4-32s to the script. If >8s, the script automatically plans and executes the chain:
- `--duration 8` → single 8s clip ($0.40 lite)
- `--duration 16` → 8s + 8s (2 clips, $0.80 lite)
- `--duration 24` → 8s + 8s + 8s (3 clips, $1.20 lite)
- `--duration 30` → 8s + 8s + 8s + 6s (4 clips, $1.60 lite)

**Recommended total durations and scene splits:**
- **8s** (3+3+2) — short-form, scroll-stopping. Good default for Meta feed ads. Single clip.
- **16s** (4+4+4+4 or 5+5+3+3) — standard UGC length. 2-clip chain.
- **24s** (8+8+8 scenes) — extended storytelling. Founder authority pieces. 3-clip chain.
- **30s** (recommended max) — long-form UGC. 4-clip chain. Beyond this, character drift increases.

If a video brief from [BA] specifies scene durations exceeding 30s total, **rewrite the durations** to fit within 30s before proceeding.

**Important for lite chaining:** Each clip in the chain should map to one scene or at most two scenes. Keep per-clip prompts focused — lite handles straightforward prompts well but degrades on complex multi-element scenes. Include the character anchor in every clip's prompt for consistency.

### Text & Screen Content: Abstract Only
Veo 3.1 **cannot render readable text**. Letters appear distorted, garbled, or illegible. This applies to:
- Computer monitors, laptops, phone screens
- Dashboards, UI interfaces, process maps
- Signs, documents, whiteboards with writing
- Any surface with specific words or labels

**Rule:** Screens and monitors must show **abstract/ambient content only** — soft glowing colour blocks, blurred dashboard shapes, abstract data visualisations with no readable labels, gentle screen-glow gradients. Never reference specific UI elements ("one-click install button"), named interfaces ("project management dashboard"), or readable text on any surface.

Tell the story through **dialogue and action**, not on-screen text. If the angle requires showing a product or result, describe it abstractly: "monitor displaying colourful data visualisations with shifting graphs" not "monitor showing a client portal with navigation tabs."

### Realism Boosters
Veo 3.1 responds strongly to film-industry language. Include these cues to push output toward photorealism:

**Camera/Lens (pick one per video):**
- "Shot on Arri Alexa Mini with Cooke S4 primes"
- "Shot on Sony FX3, 35mm f/1.4 Sigma Art lens"
- "Handheld RED Komodo, slight natural camera shake"

**Film Stock/Grade (pick one per video):**
- "35mm Kodak Portra 400 colour science — warm skin tones, lifted shadows"
- "Natural colour grade, slightly desaturated highlights"
- "Clean digital cinema look, no heavy grading"

**Imperfection Cues (use 2-3 per scene):**
- "Micro dust motes catch the light beam from the window"
- "Slight lens breathing on focus pull between scenes"
- "Natural skin texture visible in close-up — pores, micro-blemishes"
- "Faint condensation on glass surface catches overhead light"
- "Papers shift slightly from AC draft"
- "Hair moves naturally with head turns — no rigid AI hair"
- "Fabric creases visible on shirt where arm bends"

**Environmental Physics:**
- "Light spill from window creates soft shadow gradient across wall"
- "Overhead fluorescent creates subtle green cast on skin in wide shot"
- "Steam from coffee dissipates unevenly — thicker at cup, wisps at edges"

---

## Mandatory Prompt Elements

Every video prompt MUST follow the 5-layer structure below, regardless of motion pattern.

### Layer 1 — ENVIRONMENT
Specific setting with exact details. Never "an office" — instead "a modern co-working space with floor-to-ceiling windows, warm afternoon light (4200K) streaming from camera-left, exposed timber beams, scattered indoor plants, a MacBook Pro and ceramic coffee mug on a standing desk." Include:
- Lighting direction, quality, and colour temperature
- Background elements with specifics (objects, materials, colours)
- Time of day and ambient mood
- Each scene gets its OWN environment description — don't reuse "same office" across cuts

### Layer 2 — CHARACTER (define ONCE, reuse across ALL scenes)
Load the character anchor from `brand-guidelines.md` (Agency Founder or Agency PM). Copy the full description verbatim into the prompt. Include:
- Age range, build, height
- Hair colour, style, length
- Facial hair, skin tone
- Clothing with fabric, colour, and fit details
- Posture and expression baseline
- Energy and accent direction

**CRITICAL:** This anchor is written ONCE and reused identically in every scene. Do NOT vary the character description between scenes — Veo 3.1 uses this consistency to maintain the same person across cuts.

### Layer 3 — ACTION & DIALOGUE (per scene)
Each scene must include:
- Physical action (walking, sitting, gesturing at screen, picking up object)
- Micro-expressions tied to specific dialogue words (e.g., "slight eyebrow raise on 'What happens when you have 5 at once?'")
- Object interactions (coffee mug, laptop, whiteboard, phone)
- Exact spoken dialogue with accent/tone direction
- Movement between scenes — transitions like walking from desk to whiteboard make AI video dramatically more realistic than static talking heads

### Layer 4 — CAMERA
Per-scene camera direction:
- Framing: close-up (face + shoulders), medium (waist up), wide (full body + environment)
- Movement: static, slow push-in, orbit, pan, dolly
- Depth of field: shallow (subject sharp, bg blurred) or deep (all in focus)
- Transitions between scenes: cut, match-cut, camera push through

### Layer 5 — AUDIO & STYLE
- Ambient sound (keyboard clicks, coffee shop murmur, office hum)
- Music direction if any (subtle, not overpowering dialogue)
- Overall mood and energy
- Style reference: "Match the energy and pacing of {inspiration video}" when applicable
- No captions or subtitles in the video (added in post-production)

### Character Expression Rules
| Allowed | Forbidden |
|---------|-----------|
| Confident, direct eye contact | Shocked, jaw-drop |
| Thoughtful (slight head tilt) | Wide-eyed surprise |
| Slight smile (asymmetric) | Exaggerated excitement |
| Curious (eyebrow micro-raise) | Unhappy, frowning |
| Calm authority | Overly serious/stern |

### Approval Gate
Present the full scene-by-scene prompt to the user before calling the video generation API. User may adjust dialogue, camera direction, or approve as-is. NEVER generate without approval.

### Post-Generation Validation
1. Character consistent across all scenes (same face, hair, clothing)?
2. Dialogue lip-sync natural?
3. Movement realistic (no AI float/glide)?
4. Environment lighting consistent within each scene?
5. First 3 seconds grab attention (hook timing)?

If any check fails, note the specific issue, adjust the relevant prompt layer, and re-generate.

## Motion Pattern Templates

### 1. Slow Reveal

**Best for:** Curiosity hooks, "wait for it" moments, product reveals

```
Camera slowly pulls back from a tight close-up to reveal the full scene. 
Start: {tight_shot_description} — only a detail visible, creating intrigue. 
Mid: Camera smoothly dollies backward, revealing {context_elements}. 
End: Wide shot showing {full_scene} with {subject} in context. 
Movement: Steady, continuous backward dolly. No stops. 
Lighting: {lighting_description}. 
Pace: Slow and deliberate — build anticipation over 5 seconds.
```

**Duration:** 5s
**Camera:** Dolly back (start tight, end wide)
**Mood:** Curiosity, anticipation

---

### 2. Quick Cuts

**Best for:** Urgency hooks, energy, FOMO, limited-time offers

```
Dynamic rapid montage of {number} distinct scenes cut together. 
Scene 1 (0-1.5s): {scene_1} — sharp, punchy establishing shot. 
Scene 2 (1.5-3s): {scene_2} — contrasting angle or subject. 
Scene 3 (3-5s): {scene_3} — final frame holds steady on {cta_element}. 
Each cut: Hard cut, no transitions. Slight camera shake on first two scenes. 
Final scene: Static, clean, professional — the contrast creates emphasis. 
Energy: High in first 3 seconds, calm authority in final 2 seconds.
```

**Duration:** 5s
**Camera:** Multiple angles, hard cuts
**Mood:** Urgency, energy, action

---

### 3. Static-to-Motion

**Best for:** Pain point hooks ("stuck" → "freed"), transformation reveals

```
Scene starts completely still — frozen moment of {static_state}. 
Hold static for 1.5 seconds. Viewer processes the scene. 
At 1.5s: Sudden but smooth motion begins — {motion_trigger}. 
{Subject} {action_verb} as {transformation_description}. 
Camera: {camera_motion} following the subject's energy shift. 
Colour shift: From {muted_palette} to {vibrant_palette} as motion begins. 
End frame: {resolved_state} — subject in motion, confident, elevated.
```

**Duration:** 5s
**Camera:** Static hold → tracking or pan
**Mood:** Contrast, breakthrough, transformation

---

### 4. Slow Zoom

**Best for:** Testimonial feel, emotional connection, trust-building

```
Gentle, almost imperceptible zoom into {subject_description}. 
Start: Medium shot showing {subject} in {environment}. 
Movement: Extremely slow push-in over 5 seconds — the viewer barely notices the zoom but feels increasing intimacy. 
{Subject} {subtle_action} — natural, not performed. 
Expression: {emotion} — genuine warmth/confidence. 
Background: Softly blurred, {background_details}. 
Lighting: {lighting} — warm, flattering, natural. 
End: Close-up of {subject_face_or_product}, establishing connection.
```

**Duration:** 5s
**Camera:** Imperceptible push-in (start medium, end close-up)
**Mood:** Trust, intimacy, authenticity

---

### 5. Split Wipe

**Best for:** Before-after, comparison, "was this → now this" transformations

```
Split-screen transition from left to right across the frame. 
LEFT (start): {before_state} fills the entire frame. {before_details}. 
Wipe: A clean vertical wipe moves from left to right over 2 seconds, revealing the RIGHT side. 
RIGHT (revealed): {after_state} replaces the left. {after_details}. 
The wipe continues until the "after" state fills the entire frame. 
Contrast: {before_state} uses {muted_colours}, {after_state} uses {vibrant_colours}. 
Final frame: Hold on {after_state} for 1 second — clean, resolved, aspirational.
```

**Duration:** 5s
**Camera:** Static, wipe transition handles all motion
**Mood:** Transformation, progress, proof

---

### 6. Orbit

**Best for:** Product showcase, dashboard demo, 360-degree views

```
Camera orbits smoothly around {subject} at {angle} degrees elevation. 
Start: {starting_angle} view of {subject}. 
Movement: Slow, continuous orbit — {clockwise_or_counter} — covering approximately {degrees} of rotation over 5 seconds. 
{Subject} remains centre-frame throughout. 
Background: {background_description} — slightly blurred, rotating naturally with the orbit. 
Lighting: Consistent, professional — {lighting_setup}. 
End: {final_angle} view, revealing {key_feature_visible_from_this_angle}.
```

**Duration:** 5s
**Camera:** Orbital track around fixed subject
**Mood:** Authority, thoroughness, craftsmanship

---

### 7. Drift

**Best for:** Ambient/atmospheric, brand awareness, mood-setting

```
Dreamy, floating camera movement through {environment}. 
Camera drifts {direction} with gentle, fluid motion — no hard stops or direction changes. 
Environment: {environmental_details}. 
Elements pass by: {foreground_elements} in soft focus, {background_elements} sharp. 
Depth: Layered — multiple planes of motion create parallax. 
Lighting: {atmospheric_lighting} — creates {mood}. 
Speed: Unhurried, contemplative. The viewer absorbs rather than watches. 
End: Camera settles on {final_focal_point}.
```

**Duration:** 5-10s
**Camera:** Floating drift (steadicam/gimbal feel)
**Mood:** Aspirational, calm, premium

---

### 8. Multi-Scene UGC

**Best for:** Talking head ads, founder/expert authority, UGC-style engagement, pain-point hooks with movement

**This is the PRIMARY video format.** Competitor winning videos are 100% talking head. Use Veo 3.1 with multi-scene prompts. Every field below is MANDATORY — do not skip any.

**Hard constraints:** Total scene duration MUST NOT exceed 20s. All screen/monitor content MUST be abstract (see "Veo 3.1 Limitations" above). Include film-language realism cues (see "Realism Boosters" above).

```
CHARACTER ANCHOR (define ONCE — copy verbatim from brand-guidelines.md, reuse identically in every scene):
{Full multi-line character description — age range, build, height, hair colour/style/length, 
facial hair, skin tone, clothing with fabric/colour/fit details, accessories, posture, 
expression baseline, energy, accent. Example:
"Male, mid-30s, Australian. Athletic-lean build, 180cm. Short dark brown hair, clean fade 
sides. Light stubble (3-day growth), no full beard. Fair skin with slight tan. Fitted navy 
crew-neck t-shirt, quality fabric. Silver watch, left wrist. No visible tattoos. Posture: 
upright, shoulders back, relaxed confidence. Expression baseline: calm authority with slight 
warmth. Energy: measured, credible. Accent: Australian, conversational."}

STYLE: {Camera/lens — e.g., "Shot on Sony FX3, 35mm f/1.4 Sigma Art lens"}. 
{Film stock — e.g., "Natural colour grade, slightly desaturated highlights, warm skin tones"}.
{Imperfection — e.g., "Micro dust motes in light beams, natural skin texture in close-ups, 
slight lens breathing on focus pulls"}.

SCENE 1 (0-{X}s):
  ENVIRONMENT: {Specific setting with full detail — "modern home office, floor-to-ceiling 
  window camera-left streaming warm afternoon light at 4200K, timber standing desk with 
  ceramic white coffee mug, small indoor fern in terracotta pot on desk corner, exposed 
  brick feature wall behind". If monitors/screens present, describe ABSTRACT content only — 
  "monitor casting soft blue-white glow with shifting colour blocks" NOT specific UI or text}
  BACKGROUND MOTION: {Environmental movement that makes the scene feel alive — "curtain 
  drifts gently from breeze through cracked window, monitor screen data refreshes with 
  subtle glow shift, steam wisps curl upward from coffee mug, fern leaf sways slightly"}
  CAMERA: {Type + movement + depth of field — "steadicam follow shot from slightly ahead 
  and camera-right, medium shot waist up, shallow depth of field with subject sharp and 
  background elements softly blurred, gentle drift matching character's walking pace"}
  ACTION: {Physical movement with realistic physics — "walks briskly from doorway toward 
  desk, each step heel-first with visible weight transfer, right hand reaches for chair 
  back, pulls it out with controlled motion, sits down with natural controlled drop, shifts 
  weight to settle"}
  DIALOGUE: "{Exact spoken words — e.g., 'You know what kills most small businesses? It's 
  not competition. It's the twenty hours a week you spend on stuff that should take two.'}"
  ACCENT & DELIVERY: Region: {e.g., "suburban Sydney Australian"}. Register: {e.g., "warm 
  baritone"}. Pace: {e.g., "3 words per second, slight pause before 'twenty hours'"}. 
  Tone: {e.g., "conversational, measured confidence — like explaining to a smart friend 
  over coffee"}.
  MICRO-EXPRESSION: {Tied to specific dialogue word — "slight eyebrow raise on 'kills', 
  jaw sets slightly on 'twenty hours', asymmetric smile forms on 'should take two'"}
  OBJECT INTERACTION: {Specific object + specific action — "picks up coffee mug with right 
  hand mid-sentence, takes brief sip between 'competition' and 'It's the', sets down 
  without looking — mug clinks softly on desk"}
  AMBIENT AUDIO: {Scene-specific sounds — "subtle office ventilation hum, distant muffled 
  keyboard clicks from another room, coffee mug ceramic clink on timber desk, chair 
  mechanism soft click"}
  TRANSITION TO SCENE 2: {Specific type — "hard cut" / "match-cut on hand reaching for 
  laptop" / "camera push-through monitor screen" / "whip pan right"}

SCENE 2 ({X}-{Y}s):
  ENVIRONMENT: {NEW specific setting — describe fresh, never "same as Scene 1" — e.g., 
  "bright co-working kitchen area, stainless steel benchtop, espresso machine with chrome 
  finish, morning light from skylight above at 5500K, blurred figures moving in background 
  corridor"}
  BACKGROUND MOTION: {Different environmental movement — "espresso machine drip light 
  blinks, background figure crosses corridor out of focus, overhead light creates subtle 
  lens flare shift as character moves"}
  CAMERA: {Different from Scene 1 — "static medium-close shot, chest up, character 
  slightly off-centre frame-left, deep depth of field showing full kitchen environment"}
  ACTION: {Physical anchored to new object — "leans against benchtop with left hip, right 
  hand gestures outward palm-up on key phrase, weight shifts from left to right foot"}
  DIALOGUE: "{Next portion of script}"
  ACCENT & DELIVERY: {Same accent, can vary tone — "pace quickens slightly to 3.5 words/sec, 
  tone shifts to emphatic on the key stat"}
  MICRO-EXPRESSION: {New expressions tied to new dialogue words}
  OBJECT INTERACTION: {New object — "taps benchtop twice with fingertips for emphasis on 
  the number, picks up glass of water"}
  AMBIENT AUDIO: {New scene-specific — "espresso machine gurgle, distant conversation murmur, 
  glass set down on stainless steel"}
  TRANSITION TO SCENE 3: {Specific type}

SCENE 3 ({Y}-{Z}s):
  ENVIRONMENT: {Third distinct setting or return to first with different framing}
  BACKGROUND MOTION: {Environmental movement}
  CAMERA: {Different again — e.g., "slowly pushes in from medium to close-up over full 
  scene duration, shallow DoF isolating face"}
  ACTION: {Final scene: stillness and eye contact are powerful — "stops moving, squares 
  shoulders to camera, holds direct eye contact, slight confident nod after final word"}
  DIALOGUE: "{Final line — the hook payoff or CTA}"
  ACCENT & DELIVERY: {Pace slows for impact — "2.5 words/sec, deliberate pauses between 
  phrases, tone drops to calm authority"}
  MICRO-EXPRESSION: {Final expression — "holds steady gaze, slight asymmetric smile on 
  last word, single confident nod"}
  OBJECT INTERACTION: {Optional in final scene — stillness can be more powerful}
  AMBIENT AUDIO: {Quieter — "room tone only, no background elements — creates intimacy"}
  TRANSITION: {End — "holds final frame for 0.5s before end card"}

AUDIO SUMMARY:
  Voice: {accent region}, {register}, {pace range across scenes}
  Music: {direction — "none" / "subtle lo-fi fades in Scene 3 underneath" / "light 
  ambient pad, never competing with dialogue"}
  Ambient: {per-scene summary}
  No captions — NEVER include text overlays or subtitles in the prompt (added in post)
```

**Duration:** 8-15s (up to 20s max)
**Camera:** Multiple shots with hard cuts, vary framing (follow → static → push-in)
**Mood:** Authentic, confident, straight-talking expert
**Key principle:** Movement between scenes (walking, sitting, gesturing with objects) makes AI-generated video dramatically more realistic than static talking heads.

### Pre-Prompt Quality Checklist (Multi-Scene UGC)

Before using this template to construct a Veo 3.1 prompt, verify ALL items pass:

1. [ ] **Total scene durations do not exceed 20s** (Veo 3.1 hard max)
2. [ ] Character anchor copied verbatim from brand-guidelines.md — not paraphrased
3. [ ] Character anchor appears ONCE — not duplicated or varied between scenes
4. [ ] Every scene has a specific, unique environment (no "same office as Scene 1")
5. [ ] **No readable text, specific UI, or named interfaces on any screen/monitor** — abstract visuals only
6. [ ] Every scene has background/environmental motion (no static environments)
7. [ ] Every scene has physical character movement (no static talking heads)
8. [ ] Exact dialogue written word-for-word for every scene
9. [ ] Accent region + register + pace + tone specified for every scene
10. [ ] Micro-expressions tied to specific dialogue words in every scene
11. [ ] Camera framing, movement, and depth of field specified per scene
12. [ ] Transition type explicitly specified between every scene pair
13. [ ] Ambient audio specified per scene (not generic "office sounds")
14. [ ] Object interaction with specific objects in at least 2 of 3 scenes
15. [ ] **STYLE layer included** — camera/lens model, film stock/grade, and 2-3 imperfection cues
16. [ ] Total prompt length 300-500 words

**If any item fails → fix it before proceeding. This is a hard blocker.**

---

## Prompt Construction Rules

1. **Always specify duration** — up to 20s for Veo 3.1 UGC (auto-chains if >8s), 5-10s for Kling animated graphics
2. **Describe motion with verbs** — "dolly", "push-in", "orbit", "drift", "cut to", "pan left", "track right"
3. **Specify timing** — "at 1.5 seconds", "over 3 seconds", "hold for 1 second"
4. **Include lighting** — it affects mood and quality dramatically
5. **End frame matters** — the last frame is what viewers see before deciding to act. Make it clean and intentional
6. **No captions** — NEVER include captions/subtitles in the prompt. Captions are added in Meta Ads Manager.
7. **Character anchor** — Define the character ONCE at the top, reuse the exact same description in every scene for consistency
8. **Anchor actions to objects** — "taps desk" not "moves hand down". Physical interaction with objects looks more natural.
9. **Micro-expressions on specific words** — "On 'guarantee' his eyebrow lifts" ties expression to dialogue timing
10. **Background motion in every scene** — Static environments look artificial. Include environmental movement: curtain drift, screen glow, steam, leaves, light shifts, background figures
11. **Transition between every scene pair** — Explicitly specify: hard cut, match-cut (on what), camera push-through, whip pan. Never leave transitions unspecified
12. **Accent and delivery direction per scene** — Every dialogue block MUST include: accent region (e.g., "suburban Sydney Australian"), register (e.g., "warm baritone"), pace (e.g., "3 words/sec"), tone (e.g., "conversational"). These can vary between scenes for dynamics

## Matching Hook Types to Patterns

| Hook Type | Recommended Pattern | Why |
|-----------|-------------------|-----|
| **UGC/Talking Head** | **Multi-Scene UGC** | **Primary format. All competitor winners use this.** |
| Curiosity | Slow Reveal | Builds intrigue, rewards attention |
| Urgency | Quick Cuts | Creates energy and FOMO |
| Pain Point | Static-to-Motion | "Stuck" feeling → breakthrough |
| Testimonial | Slow Zoom | Builds trust and intimacy |
| Before-After | Split Wipe | Clear visual comparison |
| Product Demo | Orbit | Showcases from all angles |
| Brand/Awareness | Drift | Sets mood, builds affinity |

## Model Selection

| Use Case | Model | Why |
|----------|-------|-----|
| **All UGC (default)** | **Veo 3.1 lite** | $0.05/s, chains up to 30s via image-to-video. Cheap enough for volume generation. |
| **Premium UGC** | **Veo 3.1 fast** | $0.15/s, chains up to 20s via extend-video. Better face/hand detail and lip-sync. |
| **Hero creatives** | **Veo 3.1 standard** | $0.40/s, chains up to 20s. Maximum quality for top-performing angles. |
| Animated graphic (image-to-video only) | Kling 3.0 | Cheaper, animates static ad images. NOT for UGC or talking head. |
| Budget / long-form (30-90s) | HeyGen | $0.033/s, avatar-based, less cinematic control. Last resort. |

**Never use Kling for UGC.** Kling is exclusively for animating static images (before-after splits, product UI cards, dashboard animations).

## Text-to-Video (Veo 3.1) vs Image-to-Video (Kling)

- **Veo 3.1 lite text-to-video (DEFAULT):** All UGC and talking head ads. $0.05/s. Chains up to 30s via last-frame extraction + image-to-video. Native audio with dialogue and lip-sync.
- **Veo 3.1 lite image-to-video (auto for chaining):** Used automatically when lite duration >8s. Takes last frame of previous clip as starting image. Character inherits visually.
- **Veo 3.1 extend-video (standard/fast only):** Used automatically when standard/fast duration >8s. Inherits character from previous clip's final frames natively.
- **Kling image-to-video (secondary):** Only for animating a generated static image. The image becomes the starting frame. 5s duration. ~$0.15/video.
- **HeyGen (last resort):** Budget runs or 30+ second videos only. Avatar-based, less cinematic control.
