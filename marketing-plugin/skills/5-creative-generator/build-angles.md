---
name: build-angles
description: Generate 5-10 unique ad angles with hooks and copy variants from competitor winners, own performance data, and market intelligence
menu-code: BA
---

# Build Angles

Generate intelligence-driven ad angles with hooks and copy variants. This is LLM-driven — the agent itself generates angles from competitor data, own performance history, and market intelligence. No external script.

## Process

1. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Building angles for: **{active_campaign.name}** ({active_campaign_id}). Proceed?"
   - If `{active_campaign}` is null (standalone mode), inform: "Working in standalone mode — angles won't be linked to a campaign. Continue?"
   - If `{active_campaign}` is null but the user wants to link to a campaign, load `campaign-data.json` and let them select.

2. **Load campaign intelligence** (when `{active_campaign}` is set):
   - If `{active_campaign}.intelligence.market_report_path` exists, auto-load it (skip the manual "provide path" prompt)
   - If `{active_campaign}.intelligence.competitor_winner_ids` has entries, prioritise these winners in competitor analysis (step 4)
   - Note `{active_campaign}.audience.pain_points` and `{active_campaign}.audience.aspirations` for angle generation
   - Note `{active_campaign}.product` details (name, description, usp, guarantee) for copy variant generation
   - Ask: "Should I also pull additional competitor winners from competitor-data.json? (default: yes)" and "Should I review our own ad performance history? (default: yes)"

   **When `{active_campaign}` is null (standalone mode):**
   - "Do you have a market intelligence report to load? (provide path, or skip)"
   - "Should I pull competitor winners from competitor-data.json? (default: yes)"
   - "Should I review our own ad performance history? (default: yes)"

3. **Load own performance data** — Read `marketing-plugin/data/creative-data.json`:
   - When `{active_campaign}` is set, filter to batches with matching `campaign_id` for campaign-specific learnings (also note cross-campaign patterns)
   - Find angles with `performance_snapshot.verdict == "winner"` → note their frameworks, hooks, visual styles, copy patterns
   - Find angles with `performance_snapshot.verdict == "loser"` → note what to avoid
   - Summarise "lessons learned" from our own history before generating new angles
   - If no performance data exists yet, skip this step

4. **Load competitor intelligence** — Read `marketing-plugin/data/competitor-data.json`:
   - When `{active_campaign}` has `intelligence.competitor_winner_ids`, prioritise those specific ads first, then load remaining winners
   - Find all ads with `status` of `"winner"` or `"super_winner"`
   - For each winner, note: hook type, visual style, CTA pattern, copy strategy, days active, format
   - Summarise: what patterns repeat across winners? What hooks dominate? What angles are overused?

5. **Load market intelligence** — When `{active_campaign}` is set and has `intelligence.market_report_path`, auto-load it. Otherwise, if the user provided a report path in step 2, read it. Extract:
   - Key themes and audience pain points
   - Market positioning opportunities
   - Language patterns and terminology the audience uses

6. **Load brand guidelines** — Read `marketing-plugin/references/brand-guidelines.md`:
   - Note the ICP (Australian business owners, 5-50 employees)
   - Note pain language ("drowning in admin", "can't scale") and aspiration language ("run itself", "work smarter")
   - Note copy constraints (125 chars recommended, 40 char headline max)
   - When `{active_campaign}` is set, also use `{active_campaign}.audience.pain_points` and `{active_campaign}.audience.aspirations` to supplement brand guidelines with campaign-specific language

7. **Present intelligence summary** before generating angles:

   ```
   Intelligence Summary:
   - Own winners: {count} ({patterns})
   - Own losers: {count} ({patterns to avoid})
   - Competitor winners: {count} ({dominant hooks, visual styles})
   - Market themes: {key themes}
   - Gaps identified: {what competitors AREN'T doing}
   ```

8. **Generate 5-10 unique angles** using the structured frameworks below. When `{active_campaign}` is set, use `{active_campaign}.product` details (name, description, usp, guarantee) to ground copy variants in the specific product context. Each angle must include:

   | Field | Description |
   |-------|-------------|
   | `angle_id` | Kebab-case slug (e.g., `fear-of-missing-out`) |
   | `angle_name` | Human-readable name |
   | `hook_line` | The opening hook (first 1-2 seconds of attention) |
   | `visual_brief` | Structured creative direction for both image and video formats (see below) |
   | `framework` | Which framework was used (PAS, AIDA, BAB, Curiosity Gap, Social Proof) |
   | `source` | What insight drove this angle (competitor pattern, market theme, or gap) |
   | `inspiration_ads` | 1-3 specific competitor ads that inspire this angle's **design AND messaging** (see below) |
   | `copy_variants` | 3 variants: direct, story, question (see below) |

   Each `inspiration_ad` contains:

   | Field | Description |
   |-------|-------------|
   | `ad_id` | The competitor ad ID from competitor-data.json |
   | `page_name` | Competitor page name |
   | `local_path` | Path to downloaded creative asset (e.g., `data/competitor-assets/{page_id}/{ad_id}.jpg`) |
   | `why` | What specific design elements, layout, colours, or angle themes to adapt from this winner |

   **CRITICAL:** Every angle MUST link to 1-3 specific winner/strong_performer ads. These are not just thematic inspiration — they define the **visual design to recreate**. The generated ad should look like it belongs in the same ad account as the winner, but with branding. The `local_path` images will be passed to the image generation model as style references.

   Each `copy_variant` contains:

   | Field | Description |
   |-------|-------------|
   | `style` | `direct`, `story`, or `question` |
   | `primary_text` | Main ad body text (125 chars recommended, 250 max) |
   | `headline` | Bold headline below the creative (40 chars max) |
   | `description` | Subtext below headline (30 chars max) |
   | `cta` | Call-to-action button text (e.g., "Learn More", "Get Started") |

### Visual Brief Structure

Each angle must include a `visual_brief` object with BOTH image and video direction. This replaces the old `visual_direction` string.

```json
{
  "visual_brief": {
    "image_brief": {
      "scene": "Detailed scene/environment — specific objects, lighting, materials, mood",
      "composition": "Layout — focal point position, secondary elements, text space reservation with exact positioning",
      "colour_palette": "Specific hex codes and where each is used (e.g., '#1B2A4A background, #7DFF00 accent on stat, #3B82F6 divider line')",
      "style_reference": "Match composition and palette of {inspiration_ad local_path}",
      "text_overlay": "Exact text (max 12 chars), colour, positioning — or 'No text, space reserved at {position}'"
    },
    "video_brief": {
      "character": "founder | pm — references the character anchor in brand-guidelines.md",
      "scenes": [
        {
          "scene_number": 1,
          "duration": "3s",
          "environment": "Specific setting — lighting direction/quality/colour temp (e.g., '4200K warm'), background objects, materials, time of day. Screens/monitors show ABSTRACT content only (soft colour blocks, blurred shapes, ambient glow) — never specific UI or readable text.",
          "action": "Physical action + micro-expressions + object interactions (e.g., 'leans forward, picks up coffee mug, slight eyebrow raise on the word five')",
          "dialogue": "Exact spoken words. Accent: Australian, conversational. Tone: {confident/thoughtful/emphatic}.",
          "camera": "Framing (close-up/medium/wide), movement (static/slow push/orbit), depth of field"
        }
      ],
      "style_reference": "Match energy and pacing of {inspiration_ad local_path}. Shot on {camera/lens}. {Film stock/grade}.",
      "audio": "Ambient sound (e.g., 'subtle office hum, keyboard clicks'), music direction if any",
      "motion_pattern": "Name of the motion pattern template to use (e.g., 'Slow Zoom', 'Multi-Scene UGC')"
    }

    NOTE: Scene durations MUST NOT exceed 20s (Veo 3 hard max). Recommended totals: 8s (3+3+2), 12s (5+4+3), or 15s (5+5+5).
  }
}
```

**Rules for visual_brief generation:**
- **Character anchor:** Always reference a character from `brand-guidelines.md` (Agency Founder or Agency PM). The full character description is loaded at prompt time — just specify which character.
- **Scene durations must not exceed 20s** (Veo 3 hard max). Recommended totals: 8s (3+3+2), 12s (5+4+3), or 15s (5+5+5).
- **Screens show abstract content only:** Veo 3 cannot render readable text. Any monitor, laptop, or phone screen in the environment must show abstract visuals — soft colour blocks, blurred shapes, ambient glow, shifting gradients. Never reference specific UI elements ("project management dashboard"), named interfaces ("client portal"), or readable text on any surface. Tell the story through dialogue and action.
- **Environments:** Never generic ("an office"). Always specific ("modern co-working space with floor-to-ceiling windows, warm afternoon light streaming from camera-left, exposed timber beams, MacBook Pro on standing desk").
- **Movement:** Video characters MUST be in motion — walking, sitting, gesturing, picking up objects. Static talking heads look AI-generated. Movement is the primary realism tool.
- **Micro-expressions:** Tie expression changes to specific dialogue words (e.g., "slight head tilt on 'What if?'").
- **Style reference:** MANDATORY — link to the specific inspiration ad asset path from `inspiration_ads[]`. Include film-language realism cues (camera/lens model, film stock/grade) in the style_reference field.
- **Camera per scene:** Specify framing, movement, and depth of field for EACH scene.
- **Image text overlay:** Maximum 12 characters. If no text in image, explicitly reserve space for post-production overlay.

## Angle Generation Frameworks

Use a diverse mix of these frameworks. Tag each angle with its framework.

### PAS (Pain → Agitate → Solution)
**Best for:** Problem-aware audiences who know they have the pain but haven't solved it.

**Structure:**
- Hook: Name the pain directly
- Agitate: Make the consequences vivid
- Solution: Position as the answer

**Example angle:**
```
angle_name: "Admin Drowning"
hook_line: "Still doing your invoicing manually?"
framework: "PAS"
copy_variants:
  direct: "You're spending 15 hours a week on admin that could take 15 minutes. builds AI systems that handle invoicing, scheduling, and follow-ups automatically. Get your time back."
  story: "Last month, a trades business owner told us he was working until 10pm just to keep up with paperwork. Two weeks later, his AI system handles it all by 5pm."
  question: "What would you do with 15 extra hours every week? Most business owners don't realise how much time they're losing to manual processes."
```

### AIDA (Attention → Interest → Desire → Action)
**Best for:** Cold audiences who don't know they have the problem yet.

**Structure:**
- Hook: Bold, unexpected statement to stop the scroll
- Interest: Reveal the insight
- Desire: Paint the outcome
- Action: Clear CTA

**Example angle:**
```
angle_name: "The 15-Hour Week"
hook_line: "This business owner cut their work week from 60 hours to 15"
framework: "AIDA"
```

### Before-After-Bridge (BAB)
**Best for:** Transformation-focused messaging, case study style.

**Structure:**
- Before: Current painful state
- After: Desired future state
- Bridge: How to get there (your solution)

**Example angle:**
```
angle_name: "Before AI vs After AI"
hook_line: "6 months ago, Sarah was drowning in spreadsheets. Now her business runs itself."
framework: "BAB"
```

### Curiosity Gap
**Best for:** Scroll-stopping hooks that create an information gap the viewer must close.

**Structure:**
- Hook: Open a loop (surprising fact, counterintuitive claim, unfinished story)
- Body: Partially close the loop, building intrigue
- CTA: Close the loop requires clicking

**Example angle:**
```
angle_name: "The Automation Secret"
hook_line: "87% of Australian businesses are paying for software they've never properly set up"
framework: "Curiosity Gap"
```

### Social Proof
**Best for:** Trust-building with skeptical audiences, warm retargeting.

**Structure:**
- Hook: Lead with a result or testimonial
- Proof: Specifics (numbers, timeline, context)
- CTA: "You can too" energy

**Example angle:**
```
angle_name: "Client Results Showcase"
hook_line: "We saved this client $47,000/year with one automation"
framework: "Social Proof"
```

## Angle Generation Principles

- **Every angle must trace to a specific insight** (competitor pattern, market theme, own winner, or gap)
- **Hooks must work in the first 1-2 seconds** — they compete for scroll-stopping attention
- **Copy variants give the same angle three different entry points** for A/B testing
- **Angles should be diverse enough** that each could anchor its own ad set
- **Use a mix of frameworks** — don't generate 5 PAS angles. Aim for 3+ different frameworks per batch
- **Explicitly identify gaps** — what competitors AREN'T doing that represents whitespace
- **Replicate own winners** — if a previous angle performed well, create variations of its pattern
- **Avoid own losers** — if a previous angle bombed, don't repeat the same framework/hook combination
- If competitor-data.json has no winners yet, inform the user and offer to generate angles from market intel alone or general best practices

## Output Format

9. **Create a new batch in creative-data.json:**

   ```json
   {
     "batch_id": "batch-{YYYY-MM-DD}-{sequence}",
     "campaign_id": "{active_campaign_id or null}",
     "created": "{ISO timestamp}",
     "intelligence_sources": {
       "competitor_winners": {count},
       "own_winners": {count},
       "own_losers": {count},
       "market_intel_report": "{path or null}"
     },
     "angles": [
       {
         "angle_id": "...",
         "angle_name": "...",
         "hook_line": "...",
         "visual_brief": {},
         "framework": "PAS|AIDA|BAB|Curiosity Gap|Social Proof",
         "source": "competitor pattern: {detail} | market theme: {detail} | gap: {detail} | own winner variation: {detail}",
         "status": "angles_built",
         "copy_variants": [...],
         "images": [],
         "videos": [],
         "meta_ad_ids": [],
         "performance_snapshot": null
       }
     ]
   }
   ```

   Append this batch to the `batches` array. Update `meta.last_generation` and increment `meta.total_batches`.

   **When `{active_campaign}` is set:** Also update `campaign-data.json` → the campaign's `creatives.batch_ids[]` array to include the new `batch_id`.

10. **Present angles table for review:**

   ```
   Batch: {batch_id}
   Intelligence: {winner_count} competitor winners, {own_winner_count} own winners, {report or "no market intel report"}

   | # | Angle | Framework | Hook Line | Source | Status |
   |---|-------|-----------|-----------|--------|--------|
   | 1 | {name} | {framework} | {hook} | {source} | angles_built |
   | ... |

   Copy variants per angle: 3 (direct / story / question)
   Frameworks used: {list of unique frameworks}

   Next: Review angles, then run [GI] to generate images.
   Want me to show the full copy variants for any angle?
   ```
