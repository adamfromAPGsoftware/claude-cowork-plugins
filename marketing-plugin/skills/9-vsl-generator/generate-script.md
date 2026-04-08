---
name: generate-script
description: Generate full VSL script from selected angle — teleprompter copy, section timing, MG specs, production notes
menu-code: GS
---

# Generate Script

Take the selected VSL angle and produce a complete, filmable VSL script with teleprompter copy, section timing, motion graphic specifications, and production notes.

## Process

1. **Load selected angle** — Ask user which angle to develop (by number or angle_id), or accept if already specified. Load from vsl-data.json.

2. **Load pricing** — Read `{project-root}/_bmad/apg-pricing.md`. MANDATORY for any section involving offer pricing, value stacks, ROI claims, or guarantee terms. Extract exact numbers — never approximate.

3. **Load proven VSL template** — Read `{project-root}/content/standalone/2026-03-08-operational-audit-vsl/vsl-script.md`. Use as structural reference for section annotations, MG spec format, and teleprompter style.

4. **Load VSL frameworks** — Read `references/vsl-frameworks.md` for the selected framework's section structure, timing, and MG types.

5. **Load brand guidelines** — Read `{project-root}/marketing-plugin/references/brand-guidelines.md` for tone, ICP language, design language.

6. **Load design language** — From frameworks reference, load colour palette, typography, and graphic style specs.

7. **Generate the full script.** For each section:

   ```markdown
   ## Section {N}: {SECTION NAME} — {Persuasion Technique} [{start_time}–{end_time}]

   **Format:** {To camera / Graphic with voiceover / Mixed}
   **Speaker delivery:** {conversational / emphatic / story-mode / data-mode / closing}

   ---

   {Full spoken copy — conversational, natural, not teleprompter-stiff}

   **[CUT TO GRAPHIC {N} — "{Graphic Name}"]** ({duration}s) → `vsl-assets/motion-graphics/mg-{NN}-{slug}.mp4`

   > {Graphic description: content, animation, colours, layout}

   **Voiceover:** "{Copy spoken over graphic}"

   ---
   ```

   Rules for script copy:
   - Write conversationally — the speaker should hit talking points naturally, not read robotically
   - Short sentences. Line breaks for breathing room.
   - Key emphasis phrases should be identifiable for subtitle highlighting
   - All pricing/value numbers must match `_bmad/apg-pricing.md` exactly
   - Include format annotations (to-camera, graphic, voiceover) per section
   - Include speaker delivery direction per section

8. **Generate graphics summary table:**

   ```markdown
   ## Graphics Summary

   | # | Name | Screen Time | Type | File |
   |---|------|-------------|------|------|
   | 1 | "{name}" | {duration}s | {type} | `vsl-assets/motion-graphics/mg-{NN}-{slug}.mp4` |
   | ... |

   ### Design Language
   - Background: {hex}
   - Accent: {hex}
   - Text: {hex}
   - Typography: {font}
   - Style: {description}
   ```

9. **Generate Hera Motion Graphics API prompts** — For each graphic, produce a complete Hera API request JSON following the exact pattern from the proven VSL:

   ```json
   {
     "prompt": "{detailed scene description with exact colours, animations, text content, layout}",
     "duration_seconds": {N},
     "outputs": [{ "format": "mp4", "aspect_ratio": "16:9", "fps": "30", "resolution": "1080p" }]
   }
   ```

10. **Generate teleprompter version** — Strip all format annotations, graphic specs, and voiceover directions. Present the spoken copy only in short, line-broken format (2-4 words per line for natural reading pace). Follow the exact pattern from the proven VSL's teleprompter section.

11. **Generate production notes:**

    ```markdown
    ## Production Notes

    - **Recording:** Film all to-camera sections in one sitting. {additional direction}
    - **Tone:** Australian, direct, conversational. Not teleprompter-scripted. Hit talking points naturally.
    - **Runtime target:** ~{minutes} at natural speaking pace
    - **Visual split:** ~{speaker}% you talking, ~{graphic}% graphics with voiceover
    - **Emphasis words:** Words that should be highlighted green (#72E032) in subtitles are marked in **bold** throughout the script
    ```

12. **Save script** — Write to `{project-root}/content/standalone/{YYYY-MM-DD}-{slug}/vsl-script.md`. Create the directory if needed.

13. **Update vsl-data.json** — Set `selected_angle` to the chosen angle_id, `script_path` to the output path, `status` to `script_generated`.

14. **Present summary:**

    ```
    Script generated: {path}

    Sections: {count}
    Runtime: ~{minutes}
    Graphics: {count} ({types list})
    Teleprompter: included at bottom of script

    Next: Run [GE] to generate edit instructions for vid-1 handoff.
    ```
