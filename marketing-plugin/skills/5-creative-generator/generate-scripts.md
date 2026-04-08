---
name: generate-scripts
description: Generate 2-3 filmable ad video scripts (15-30s) from batch angles for real on-camera filming, designed for Meta ad placements
menu-code: GS
---

# Generate Scripts

Generate standalone ad video scripts that Adam films to camera — real UGC-style ads for Meta Reels/Stories placements. These are NOT AI-generated videos (that's [GV]). These are filmable scripts that produce the highest-trust creative format: a real person delivering a message directly to camera.

After filming, the raw landscape video is processed through the Video Editor SF pipeline (`/apg-video:1-video-editor` [SF]) to produce polished 9:16 vertical ads with motion graphics.

## Why Filmed Scripts

Meta's current best practices (2025-2026) recommend creative diversity across formats. Each batch already produces AI images ([GI]) and AI videos ([GV]). Filmed video ads add a high-trust format that consistently outperforms synthetic content on engagement and conversion. Budget recommendation: $100-150 minimum spend per creative for meaningful data.

## Process

1. **Load creative-data.json** — Read `marketing-plugin/data/creative-data.json`. When `{active_campaign}` is set, filter batches to those with matching `campaign_id` and show only campaign-relevant batches. When `{active_campaign}` is null, show all batches. Find the current batch (most recent matching) or ask the user which batch to use.

2. **Load references** — Read these before writing any scripts:
   - `marketing-plugin/references/brand-guidelines.md` — ICP, pain/aspiration language, character anchors
   - `_bmad/ccs/data/adam-voice-library.md` — Adam's speaking voice, cadence, natural phrasing
   - `content-plugin/skills/2-copywriter/workflows/agency-short-form-scripts/data/agency-script-rules.md` — pacing rules (WPS rates, hook patterns, CTA keyword format)

3. **Select 2-3 angles for filming** — Not every angle benefits from filmed video. Present a selection with rationale:

   **Selection criteria (in priority order):**

   | Criterion | Why |
   |-----------|-----|
   | **Framework fit** | PAS, BAB, and Social Proof frameworks work best on camera — they tell stories. Curiosity Gap and pure data angles often work better as images. |
   | **Spoken hook strength** | The hook_line must work when spoken aloud, not just read. Test: say it out loud. If it sounds unnatural, skip it. |
   | **Framework diversity** | Select angles with DIFFERENT frameworks to maximise creative diversity across the filmed set. |
   | **Human authenticity advantage** | Prioritise angles where a real person delivering the message adds trust that AI video cannot match — guarantees, personal experience, case study references. |

   **Present to user:**
   ```
   Recommended scripts (2-3 from {total} angles):

   1. {angle_name} ({framework}) — {why this works on camera}
   2. {angle_name} ({framework}) — {why this works on camera}
   3. {angle_name} ({framework}) — {why this works on camera}

   Skipped: {angle_name} — {why it's better as image/Veo}

   Approve, adjust, or select different angles?
   ```

   Wait for user approval before writing scripts.

4. **For each selected angle, generate the script:**

   ### Script Structure

   Every script follows the 3-part structure: **HOOK → BODY → CTA**

   | Section | Duration | WPS | Purpose |
   |---------|----------|-----|---------|
   | Hook | 2-4s | 4.0 | Stop the scroll. Adapted from the angle's `hook_line` for spoken delivery. |
   | Body | 8-20s | 3.5 | 2-3 beats delivering the angle's argument. Each beat is one clear idea. |
   | CTA | 3-5s | 3.0 | Hard keyword CTA (Comment AUDIT/WASTE/AI/RESULTS) or direct CTA (Book a call). |

   **Total duration: 15-30s.** Shorter than organic AS scripts (15-45s) because paid ad attention spans are shorter and Meta Reels placements favour punchy delivery.

   ### Writing Rules

   1. **Write for speaking, not reading.** Every sentence must sound natural spoken aloud. No written-English constructions ("In order to", "Furthermore", "It is worth noting").
   2. **Load Adam's voice** from the voice library. Match his cadence, contractions, Australianisms. If the voice library says he'd say "reckon" not "believe", use "reckon".
   3. **One idea per beat.** The body has 2-3 beats. Each beat is one complete thought. No compound ideas within a beat.
   4. **Hook adapts, doesn't copy.** The angle's `hook_line` was written for text (primary_text in Meta). Adapt it for spoken delivery — it may need to be shorter, punchier, or restructured. The core message stays the same.
   5. **Numbers land harder spoken.** "Five thousand dollars a month" beats "significant savings". Use the angle's specific metrics.
   6. **No throat-clearing.** No "So...", "Look...", "Here's the thing..." — unless that's genuinely how Adam opens (check voice library).
   7. **CTA keyword format** follows agency rules: "Comment [KEYWORD] and I'll send you the [thing]"

   ### Motion Graphic Markers

   Insert `[MG: description]` markers in the script body where motion graphics should overlay the speaker during post-production. These are consumed by the Video Editor SF pipeline.

   **MG marker rules:**
   - Minimum 2 MG markers per script (target 65-80% non-speaker visual coverage)
   - Each MG should visualise the point being made — not decorate
   - Use agency MG visual themes: SaaS cost comparisons, before/after dashboards, ROI counters, tool logo grids, case study metrics
   - MG prompt format (6-part, Hera-compatible):
     1. Format + orientation (e.g., "16:9 horizontal motion graphic")
     2. Subject (what's shown)
     3. Motion (how it moves)
     4. Style (flat/3D/isometric + colour palette)
     5. Colours (specific hex codes from brand guidelines)
     6. Timing (duration in frames or seconds)

   ### Script Output Format

   Save each script to `marketing-plugin/data/creatives/{batch_id}/scripts/{angle_id}-gs-{NN}.md`:

   ```markdown
   ---
   script_id: {angle_id}-gs-01
   batch_id: {batch_id}
   angle_id: {angle_id}
   angle_name: {angle_name}
   framework: {PAS|AIDA|BAB|Curiosity Gap|Social Proof}
   duration_target: {15-30}
   cta_keyword: {AUDIT|WASTE|AI|RESULTS|none}
   status: script_written
   ---

   # Ad Script: {angle_name}

   **Batch:** {batch_id} | **Angle:** {angle_id} | **Duration:** {duration}s
   **Target:** Meta Ads (Reels/Stories 9:16)
   **Framework:** {framework}

   ## Word Count Validation

   | Section | Words | WPS | Calculated Duration | Allocated |
   |---------|-------|-----|---------------------|-----------|
   | Hook    | {n}   | 4.0 | {n/4.0}s            | {alloc}s  |
   | Body    | {n}   | 3.5 | {n/3.5}s            | {alloc}s  |
   | CTA     | {n}   | 3.0 | {n/3.0}s            | {alloc}s  |
   | **TOTAL** | {n} |     | {total}s            | {target}s |

   > Validation: calculated duration must match allocation within +/- 1 second per section.

   ## Script

   ### HOOK (0-{X}s)

   {Word-for-word spoken dialogue. Adapted from angle's hook_line for spoken delivery.}

   ### BODY ({X}-{Y}s)

   **Beat 1:**
   {Spoken dialogue}
   [MG: {description — what visual overlays the speaker here}]

   **Beat 2:**
   {Spoken dialogue}
   [MG: {description}]

   **Beat 3 (optional):**
   {Spoken dialogue}

   ### CTA ({Y}-{end}s)

   {Hard CTA: "Comment AUDIT and I'll send you the checklist" — or direct CTA for angles where keyword comment doesn't fit}

   ## Motion Graphic Prompts

   ### MG-01: {name}
   1. **Format:** 16:9 horizontal motion graphic
   2. **Subject:** {what's shown}
   3. **Motion:** {how it moves}
   4. **Style:** {flat/3D/isometric, colour palette}
   5. **Colours:** {hex codes}
   6. **Timing:** {duration}

   ### MG-02: {name}
   {same 6-part structure}

   ## Teleprompter

   {Plain text version.
   One sentence per line.
   Max 8-10 words per line.
   ALL CAPS for emphasis words.
   No markers, no formatting.}

   ## Filming Notes

   - Film ALL scripts in one continuous landscape session (16:9, 4K)
   - 3-second pause between scripts for clean cuts
   - Centre-frame, waist up
   - Natural lighting, home office or clean background
   - Conversational tone — read from teleprompter but deliver naturally
   - Look directly at camera (eye contact with lens)
   - After filming, process through Video Editor SF pipeline for 9:16 vertical cuts + MG overlays
   ```

   ### Quality Gate

   Before saving each script, verify:

   1. [ ] Word count validation passes (calculated vs allocated within +/- 1s per section)
   2. [ ] Total duration is 15-30s
   3. [ ] Hook is adapted for spoken delivery (not copy-pasted from angle's hook_line)
   4. [ ] Body has 2-3 distinct beats with one idea each
   5. [ ] At least 2 MG markers with 6-part Hera-compatible prompts
   6. [ ] CTA uses correct keyword format (or justified reason for no keyword)
   7. [ ] Teleprompter version is clean plain text
   8. [ ] Voice matches Adam's speaking style from voice library
   9. [ ] Read the full script aloud mentally — does every sentence sound natural?

   Present each completed script to the user for review before saving.

5. **Save combined teleprompter** — After all scripts are approved, generate a combined teleprompter file at `marketing-plugin/data/creatives/{batch_id}/scripts/gs-all-teleprompter.md`:

   ```markdown
   # Teleprompter — Ad Scripts Batch {batch_id}

   ---
   ## Script 1: {angle_name} ({duration}s)
   ---

   {teleprompter text}

   [3 SECOND PAUSE]

   ---
   ## Script 2: {angle_name} ({duration}s)
   ---

   {teleprompter text}

   [3 SECOND PAUSE]

   ---
   ## Script 3: {angle_name} ({duration}s)
   ---

   {teleprompter text}

   [END]
   ```

6. **Update creative-data.json** — For each scripted angle, add `ad_scripts` array:

   ```json
   {
     "ad_scripts": [
       {
         "script_id": "{angle_id}-gs-01",
         "path": "data/creatives/{batch_id}/scripts/{angle_id}-gs-01.md",
         "duration": 25,
         "word_count": 88,
         "cta_keyword": "AUDIT",
         "status": "script_written",
         "filmed_video_path": null,
         "edited_video_path": null
       }
     ]
   }
   ```

   Update angle `status` to `"scripts_generated"` (only if images/videos already generated; otherwise leave current status).

7. **Report:**

   ```
   Ad Script Generation Complete — Batch: {batch_id}

   | Angle | Framework | Duration | CTA | Status |
   |-------|-----------|----------|-----|--------|
   | {name} | {framework} | {duration}s | {keyword} | script_written |
   | ... |

   Scripts: {count}
   Combined teleprompter: data/creatives/{batch_id}/scripts/gs-all-teleprompter.md
   Output directory: data/creatives/{batch_id}/scripts/

   Next steps:
   1. Open the combined teleprompter on your phone/tablet
   2. Film all scripts in one landscape session (16:9, 4K)
   3. Save raw video to marketing-plugin/data/creatives/{batch_id}/scripts/raw/
   4. Run Video Editor SF pipeline to produce 9:16 vertical cuts
   5. Run [PC] to package all creatives (images + AI videos + filmed videos) for upload
   ```

## Post-Filming Workflow

After Adam films the scripts:

1. **Raw video** goes to `data/creatives/{batch_id}/scripts/raw/`
2. **Video Editor SF pipeline** (`/apg-video:1-video-editor` [SF]) processes:
   - Proxy generation → audio analysis → transcription → clipping → storyboard → MG asset generation → Remotion render → 9:16 output
3. **Edited videos** are placed in `data/creatives/{batch_id}/` alongside AI-generated assets
4. **Update creative-data.json** — set `ad_scripts[].filmed_video_path` and `ad_scripts[].edited_video_path`; update status to `"filmed"` then `"edited"`
5. **Run [PC]** to package everything into the upload guide

## Error Handling

- If the voice library cannot be loaded, proceed but warn the user that voice matching may be less accurate
- If fewer than 2 angles are suitable for filming (e.g., all are data/curiosity angles), inform the user and generate scripts for the best available angles with a note on why they're suboptimal for camera
- If word count validation fails, adjust the script — never save a script that exceeds +/- 1s tolerance per section
