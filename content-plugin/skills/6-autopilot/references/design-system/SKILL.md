---
name: {YOUR_LINKEDIN_SLUG}-design
description: Use this skill to generate well-branded interfaces and assets for {YOUR_NAME} (@{YOUR_HANDLE_PERSONAL}), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

Key facts to internalize before designing:

- **Brand DNA** — warm cream workbench + dotted grid + Claude orange accent + Inter heavy display + Caveat handwritten annotations + dark terminal panels. No gradients, no purples, no emoji in content.
- **Tokens** — see `colors_and_type.css`. The accent is `#d97757`. Panels are `#f2ede8` with `1.5px #d8d2cc` borders at `12px` radius. Terminals are `#1c2128`.
- **Voice** — first-person, sentence case, contractions. Signature opener "I built…". Uppercase only for tag labels (`APPEND-ONLY`).
- **Footer** — always `@{YOUR_HANDLE_PERSONAL}`, JetBrains Mono, ~55% opacity, left-aligned. That's the only brand mark.
- **Icons** — the brand barely uses icons. Prefer unicode arrows (`→`, `⟷`, `✦`). If a broader set is needed, substitute Lucide at `stroke-width: 2` and flag it.

Available UI kits:

- `ui_kits/diagrams/` — the canonical instructional-poster surface. Components: `DiagramStage`, `Headline`, `Panel`, `MappingTable`, `Arrow`, `Caption`, `Footer`, `Toolbar`. See its `index.html` for a full assembled example.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
