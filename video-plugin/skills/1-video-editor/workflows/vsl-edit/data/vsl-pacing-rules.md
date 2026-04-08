# VSL Pacing Rules (V1–V12)

Enforcement rules for Video Sales Letter editing, derived from production analysis of the VSL (3:05, 16:9 landscape). Each rule includes Gate, Measurement, and Remediation fields.

These rules complement the VSL compliance checklist in `vsl-compliance-checklist.md`.

---

## V1: Layout Change Frequency

- **Target:** 20-25 layout changes per minute (visual change every 2-4 seconds)
- **Minimum:** 15 layout changes per minute
- This is dramatically higher than tutorial editing — VSLs manufacture energy through relentless visual change

**Gate:** FAIL — any 30-second window with fewer than 8 layout changes
**Measurement:** Count all layout changes (speaker ↔ graphic, speaker ↔ B-roll, graphic ↔ speaker) per 30s window
**Remediation:** Add text overlay breakouts, icon pop-ups, or B-roll cuts to fill visual gaps

## V2: Speaker Max Hold

- **Maximum 8 seconds** of uninterrupted speaker-only footage (no overlays, no text breakouts)
- Speaker CAN hold longer if overlays are active (icon pop-ups, subtitle highlights, text breakouts)

**Gate:** FAIL — any speaker-only segment > 8s without a visual overlay element
**Measurement:** Measure duration of each continuous speaker segment where only subtitles are visible (no additional overlays)
**Remediation:** Add emphasis text breakout, icon pop-up, or cut to graphic/B-roll

## V3: Graphic Hold Duration

- **Target:** 2-5 seconds per full-screen graphic
- **Maximum:** 6 seconds for complex graphics (UI mockups, ROI calculators)
- VSL graphics are rapid "proof flashes" — not educational explainers

**Gate:** FAIL — any full-screen graphic holding > 6s
**Measurement:** Measure duration of each continuous full-screen graphic segment
**Remediation:** Split long graphics into sequential reveals or return to speaker mid-graphic

## V4: B-Roll Hold Duration

- **Target:** 2-4 seconds per B-roll segment
- **Maximum:** 5 seconds
- B-roll is a visual punctuation mark, not a scene

**Gate:** FAIL — any B-roll segment > 5s
**Measurement:** Measure duration of each continuous B-roll segment
**Remediation:** Cut B-roll shorter or interleave with speaker returns

## V5: Visual Split Ratio

- **Target:** 65% speaker (including overlays) / 25% full-screen graphics / 10% B-roll
- **Acceptable range:** 55-75% speaker, 15-35% graphics, 5-15% B-roll

**Gate:** WARN — speaker percentage below 55% or above 75%
**Measurement:** Sum duration of each layout type, divide by total runtime
**Remediation:** Adjust balance — if too many graphics, add speaker returns; if too much speaker, add visual proof graphics

## V6: Section Energy Consistency

- **Target:** High visual energy (15+ layout changes/min) maintained throughout the entire video
- Unlike tutorials, VSLs do NOT slow down in the middle — energy stays high from hook to CTA

**Gate:** WARN — any section dropping below 10 layout changes/min
**Measurement:** Calculate layout changes per minute for each VSL section
**Remediation:** Increase visual variety in low-energy sections (text breakouts, icon pop-ups)

## V7: Emphasis Text Frequency

- **Target:** At least 1 emphasis text breakout every 15-20 seconds during speaker segments
- These are large, screen-filling text overlays that highlight key phrases beside the speaker

**Gate:** WARN — speaker run > 20s without an emphasis text breakout
**Measurement:** Measure gaps between emphasis text overlay appearances
**Remediation:** Identify key copywriting phrases in the script and add text breakout overlays

## V8: Icon Pop-Up Density

- **Target:** Whenever a specific tool or brand is mentioned by name, its logo appears within 0.5s
- Pop-ups use spring animation (scale 0→1 with overshoot)
- Multiple icons can appear in sequence (1-2s apart)

**Gate:** SOFT — tool mentioned without corresponding icon pop-up
**Measurement:** Cross-reference transcript tool mentions with icon pop-up timestamps
**Remediation:** Add missing icon pop-ups at tool mention timestamps

## V9: B-Roll Visual Treatment

- **Target:** All B-roll segments use black-and-white treatment with high contrast
- B-roll = "pain state" or "past story" — colour desaturation creates visual separation from speaker (solution state)

**Gate:** HARD — B-roll segment without grayscale + contrast treatment
**Measurement:** Verify CSS filter `grayscale(100%) contrast(120%)` applied to all B-roll
**Remediation:** Apply desaturation filter to B-roll segments

## V10: Subtitle Coverage

- **Target:** 100% of speaker dialogue has visible subtitles (phrase-level)
- Key emphasis words highlighted in brand green (#72E032)
- At least 1 green-highlighted word per phrase burst

**Gate:** HARD — speaker dialogue without subtitles
**Measurement:** Verify subtitle timeline covers all speaker segments
**Remediation:** Generate word-level timestamps from transcript, build phrase bursts

## V11: CTA Visual

- **Target:** Final 10-15 seconds includes a clear CTA visual (website screenshot, button animation, or text card)
- CTA must include specific action text ("Book a call", "Click below") with directional cue (arrow pointing down)

**Gate:** HARD — video ending without visible CTA graphic
**Measurement:** Check final 15 seconds for CTA overlay
**Remediation:** Add CTA end card with button/text and arrow animation

## V12: Audio Continuity

- **Target:** Voiceover bridges ALL visual transitions — audio never pauses for a cut
- Music present throughout at ~10-15% of VO volume
- Optional subtle SFX on icon pop-ups and graphic reveals

**Gate:** HARD — audio gap at any visual transition point
**Measurement:** Check audio waveform continuity at every transition timestamp
**Remediation:** Ensure single continuous audio track with no gaps

---

## Section-Specific Targets

| VSL Section | Layout Changes/Min | Speaker % | Graphic % | Key Visual Elements |
|-------------|-------------------|-----------|-----------|---------------------|
| Hook & Agitate | 20-25 | 70% | 30% | B-roll, icon pop-ups, text breakouts |
| Epiphany/Story | 15-20 | 80% | 20% | B-roll, gear icon, text breakouts |
| Solution Reveal | 20-25 | 50% | 50% | Dashboard mockups, before/after |
| Authority/Trust | 15-20 | 80% | 20% | B-roll, credential graphics |
| The Offer | 20-25 | 20% | 80% | Website hero, value stack, ROI |
| Cost of Inaction | 20-25 | 60% | 40% | ROI results, financial data |
| CTA | 15-20 | 80% | 20% | CTA button/card, arrow |
