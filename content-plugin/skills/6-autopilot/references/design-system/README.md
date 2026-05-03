# {YOUR_NAME} — Design System

The personal brand of **{YOUR_NAME}** (`@{YOUR_HANDLE_PERSONAL}`) — founder of an AI agency, educator building "AI agency OS" content. The visual identity is **warm neutral paper + a single Claude-orange accent** applied with an **AI-tech, blocky sensibility**: light cream backgrounds, sharp Inter display, JetBrains Mono for code and micro-labels, terminal-dark surfaces for emphasis. Low chroma, high contrast, minimal ornament.

The optional **hand-drawn mark** (Caveat handwriting + wobbly underline) is kept as an illustrative flourish for explainer diagrams — not the default voice.

---

## Source material

- **`assets/sample-tutorial-diagram.html`** — the original Fabric.js diagram builder (delivered via `uploads/diagram.html`). Source of truth for the color palette and the three-layer composition pattern.
- No Figma, no codebase, no slide template was provided.

---

## Index

| File / folder | What's in it |
|---|---|
| `README.md` | This file |
| `SKILL.md` | Agent skill entrypoint (Claude Code compatible) |
| `colors_and_type.css` | CSS custom properties: neutrals, orange, typography, shape, motion |
| `assets/` | Source diagram, signature marks, hand-drawn SVG primitives |
| `preview/` | Small HTML cards that populate the Design System review tab |
| `ui_kits/diagrams/` | Instructional-diagram UI kit (React) |

---

## CONTENT FUNDAMENTALS

Voice: **curious engineer teaching in public.** Technical, sure of itself, allergic to jargon, warm without being cute. Copy reads like a builder talking to another builder — short declarative sentences, file paths as proof, pull-quotes that kill buzzwords.

### Tone & casing

- **Sentence case everywhere.** The only uppercase is the micro-label — a mono tag like `APPEND-ONLY`, `LLM-COMPILED`, `PER-AGENT CONTEXT`, tracked wide (`0.14em`).
- **"I built …"** is the signature opener. First-person singular, past tense.
- **Contractions yes.** "It's", "you'll", "don't".
- **One idea per line.** Copy is stacked in 6–12 word lines that survive a phone screen.

### Structure (the {YOUR_NAME} paragraph)

1. **Heavy Inter headline** — the claim. Often starts "I built…" or "How I…".
2. **Mono eyebrow or kicker** — a one-line clarifier in uppercase mono, in orange.
3. **Numbered panels** — three is the magic number. Each panel has a **mono tag** (`APPEND-ONLY`), a **title**, 1–2 lines of explanation, and a **file-path / code snippet**.
4. **Pull-quote caption** — the takeaway, ending with an arrow: _"no RAG, no vector DB — just structured context that compounds →"_.
5. **Footer signature** — `@{YOUR_HANDLE_PERSONAL}` left-aligned, mono, ~55% opacity. That's the only mark.

### Copy examples

- Headline — "I built a YouTube tutorial system at agency scale"
- Tag labels — `APPEND-ONLY` · `LLM-COMPILED` · `PER-AGENT CONTEXT`
- Panel body — "Source docs captured after every session. Never modified. Permanent audit trail."
- Mono / file-path — `tutorial: raw/` · `{your-brand}: meetings/ + follow-ups/`
- Caption — "No RAG. No vector DB. Just structured context that compounds."

### Emoji & symbols

- **No emoji in primary copy.** Only glyphs: `→` / `↔` arrows. No 🧠, no 🚀.
- **Unicode arrows are preferred** over SVG paths for inline text.

---

## VISUAL FOUNDATIONS

**"Blocky paper + one accent."** Warm neutral backgrounds carry the design; Claude orange highlights the one thing that matters; terminal dark surfaces punctuate.

### Color — two families, one accent

**Neutral warm scale** (the "paper"):
`--neutral-50` `#fafaf8` → `--neutral-900` `#1a1614`. Six meaningful stops. Everything fg/bg routes through this scale.

**Dark scale** (terminal / code only): `--dark-900` `#1c2128`, `--dark-700` `#30363d`, `--dark-100` `#c9d1d9`, `--dark-50` `#f0e6d3`.

**Orange — the single accent**:
- `--orange-500` `#d97757` — the accent
- `--orange-700` `#c05f2a` — orange-as-text
- `--orange-100` `#f4a387` — hover / soft
- `--orange-900` `#6a3820` — deep emphasis on cream

There is **no blue link color, no green success color.** Semantic states (errors, success, info) are expressed by neutral rank + orange emphasis + copy, not by new hues. If a future surface genuinely needs them, add them then — not speculatively.

### Typography — Inter + JetBrains Mono

- **Inter** for everything readable. Black (`900`) for display, heavy (`800`) for h1, bold (`700`) for h2/h3, regular (`400`) for body.
- **JetBrains Mono** for code, file paths, eyebrows, labels, and badges. This is the "AI techy" signal.
- **Caveat** is retained but optional — reserved for the hand-drawn illustrative mark on diagrams. Not used for titles, body, or UI.

Scale: display 72 / h1 48 / h2 32 / h3 22 / body 16 / small 14 / label 12 / mono 13.

### Spacing, shape, borders

- **4px base grid.** Stops: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64.
- **Radii are tighter and blockier** than v1: buttons `4`, inputs `6`, panels `10`, pills `999`.
- **1px hairline borders** are the default (`--neutral-200` on cream, `--dark-700` on terminal). A **2px ink border** (`--neutral-900`) is available for deliberate blocky emphasis (pricing cards, hero CTA).
- **No left-border accent cards.** The accent shows up via badges, mono eyebrows, and key color on specific elements.

### Backgrounds

- **Dotted grid on warm neutral** is the signature backdrop. `radial-gradient(circle, #d8d2cc 1.5px, transparent 1.5px)` at `32px` cadence. Apply via `.ag-dotted-bg`.
- **No full-bleed photography, no gradients, no textures.** The paper is the background.
- **Terminal panels are the only dark surface.** Dark mode is earned, not global.

### Shadows

Two, and only two:

- `--shadow-toolbar` — floating UI (nav bar, toolbar)
- `--shadow-card` — an elevated card on the workbench

No colored shadows, no neumorphism, no glow.

### Hand-drawn marks (optional illustrative layer)

Kept in `assets/` for diagram contexts. **Not** used in general UI.

- `underline-mark.svg` — two-layer orange wobble underline under a headline.
- `arrow-mark.svg` — 2.5px orange arrow with triangle head.
- These are decorative accents on educational posters, not a system-wide motif. Use them consciously, not by default.

### Motion

- **Almost no animation.** Hover fades (`120ms ease-out`), focus rings, nothing else by default.
- **No bounces, no springs, no parallax.**
- **Hover**: slightly darker neutral fill, or 10% orange tint on accent elements.
- **Press**: deeper fill only. No scale.

### Transparency & blur

None by default. No `backdrop-filter`. Solid surfaces are solid. The footer watermark at 45% opacity is the only intentional translucency.

### Layout rules

- Instructional posters use a **1080-wide portrait canvas**.
- Three columns for layered panels; each panel ~300–320px wide with 16px gutters.
- Headline + eyebrow top-left, content middle, caption + signature anchor the bottom. Always in that order.

---

## ICONOGRAPHY

- **No custom icon font.** The brand is almost iconless.
- **Unicode glyphs for symbols**: `→` · `↔` · `⟷` · `✦` · `•`.
- **If broader iconography is needed, substitute [Lucide](https://lucide.dev) at `stroke-width: 2`** — clean, single-weight, stroke-only. Flag the substitution for review.
- **Hand-drawn SVG marks** (`underline-mark.svg`, `arrow-mark.svg`, `signature-mark.svg`, `save-for-later.svg`) live in `assets/` and are used only in illustrative diagram contexts.

### Logos / marks

There is no formal wordmark or logomark. The de-facto brand mark is the **`@{YOUR_HANDLE_PERSONAL}`** handle set in JetBrains Mono at ~55% opacity as a footer signature. That's all that's needed. See `assets/signature-mark.svg`.

---

## Font substitutions

**Inter**, **JetBrains Mono**, and **Caveat** are loaded live from Google Fonts. No substitutions. If you want them bundled locally, drop TTFs into `fonts/` and swap the `@import` for `@font-face`.

---

## Caveats

- Only one visual artifact informed this system (the sample tutorial diagram). The instructional-diagram surface is canonical; website / app / email / deck surfaces are not yet proven.
- No Figma, no codebase.
- No formal logo — `@{YOUR_HANDLE_PERSONAL}` footer is the mark.
