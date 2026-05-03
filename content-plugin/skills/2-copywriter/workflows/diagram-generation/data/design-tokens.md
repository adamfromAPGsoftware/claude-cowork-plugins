# Design Tokens — {YOUR_NAME} Brand

Extracted from `colors_and_type.css`. Use these exact values when building diagram HTML — no substitutions.

## Colors

### Neutral (paper)
| Token | Hex | Use |
|-------|-----|-----|
| `--neutral-50` | `#fafaf8` | Card/slide background |
| `--neutral-100` | `#f2ede8` | Inset panel on card |
| `--neutral-150` | `#e8e4dc` | Outer workbench/workspace |
| `--neutral-200` | `#d8d2cc` | Hairline borders, subtle separators |
| `--neutral-300` | `#b9b2ab` | Subtle separators |
| `--neutral-500` | `#9a928c` | Muted text, disabled |
| `--neutral-700` | `#5c5550` | Body text |
| `--neutral-900` | `#1a1614` | Primary ink, almost-black |

### Dark (terminal/code)
| Token | Hex | Use |
|-------|-----|-----|
| `--dark-900` | `#1c2128` | Terminal fill |
| `--dark-700` | `#30363d` | Terminal border/hairline |
| `--dark-100` | `#c9d1d9` | Body text on terminal |
| `--dark-50` | `#f0e6d3` | Title on terminal (warm cream) |

### Orange (Claude accent — the only accent)
| Token | Hex | Use |
|-------|-----|-----|
| `--orange-100` | `#f4a387` | Soft hover, second traffic-light dot |
| `--orange-500` | `#d97757` | THE accent — badges, arrows, highlights |
| `--orange-700` | `#c05f2a` | Orange-as-text (darker for readability) |
| `--orange-900` | `#6a3820` | Deep emphasis on cream |

### Canvas background
| Surface | Hex |
|---------|-----|
| MapCanvas background | `#f5f0e8` |
| Dotted grid dots | `#c9bfb2` |
| Dot spacing | `28px` |

## Typography

**Fonts:** Inter (display/body) + JetBrains Mono (code/labels) — loaded from Google Fonts

### Scale
| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Display title | 68px | 900 | `#1a1614` |
| H1 | 48px | 900 | `#1a1614` |
| H2 | 32px | 800 | `#1a1614` |
| H3 | 22px | 700 | `#1a1614` |
| Body | 16px | 400 | `#5c5550` |
| Small | 14px | 400 | `#5c5550` |
| Label/eyebrow | 12px | 500 | `#d97757` (orange) |
| Mono | 13px | 400 | `#1a1614` |

**Letter spacing:** display/H1 = `-0.03em`, H2 = `-0.01em`, labels = `+0.14em`
**Line height:** tight = `0.95`, snug = `1.15`, body = `1.55`

## Shape

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | `4px` | Buttons, tags, badges |
| `--radius-md` | `6px` | Inputs, small cards |
| `--radius-lg` | `10px` | Panels, main cards, nodes |
| `--radius-pill` | `999px` | Pills, circle markers |
| Default border | `1.5px solid #1a1614` | Node outlines |
| Card shadow | `4px 4px 0 #1a1614` | Blocky offset shadow |

## Spacing (4px base)
`4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64px`

## Google Fonts import
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
```
