# Motion Graphic Types — Quick Reference

Stage direction tags for the copywriter to indicate where motion graphics should appear in scripts. The storyboard workflow expands these into full Hera API prompts after filming.

---

## Type Reference

| Type | Tag | When to Use | Example Stage Direction |
|------|-----|------------|------------------------|
| A | `[MG-A]` | Speaker says a number/metric | `[MG-A: "$1M+ revenue" — bold white text overlay]` |
| B | `[MG-B]` | First mention of a tool/platform | `[MG-B: Claude Code logo — slide in right]` |
| C | `[MG-C]` | UI Mockup / Platform interface recreation | `[MG-C: Claude chat interface — purple sidebar, user asks about scheduling]` |
| D | `[MG-D]` | Abstract concept explanation | `[MG-D: API concept — boxes with connecting lines]` |
| E | `[MG-E]` | Walking through a list | `[MG-E: 4-item agenda — sequential bullet reveal]` |
| F | `[MG-F]` | Storytelling / narrative context | `[MG-F: B-roll of developer at laptop — film grain]` |
| G | `[MG-G]` | Guiding through a document | `[MG-G: smooth pan across n8n workflow canvas]` |

## Frequency Rules

- **Intro (first 90s):** Place a `[MG-X]` tag every 4–8 seconds
- **Body segments:** Place a `[MG-X]` tag every 15–45 seconds
- **Rule:** Never go more than 8s in the intro without a `[MG-X]` tag (matches P12 max-gap enforcement)

## Usage Notes

- These are outline-level placement hints — the storyboard expands them after filming
- The script specifies WHAT graphic to show; the storyboard decides HOW (Hera prompt, duration, animation)
- Multiple types can appear in quick succession during high-energy intro sections
- During deep technical screen shares, motion graphics should stop (all 5 inspiration creators do this)

## Tool Specificity Rule

When a `[MG-B]`, `[MG-C]`, or `[MG-D]` tag references a named tool or platform, the copywriter MUST name the tool explicitly in the tag description. Generic descriptions like "chat interface" or "automation workflow" are not acceptable — always specify which tool.

**Good examples:**
- `[MG-B: Claude Code logo — slide in from right]`
- `[MG-C: n8n workflow canvas — orange nodes connected with HTTP + AI Agent modules]`
- `[MG-C: ChatGPT dark interface — user asking about code review]`
- `[MG-D: Cursor AI inline edit — purple highlight showing code suggestion]`

**Bad examples (too generic):**
- `[MG-B: AI tool logo]` — which AI tool?
- `[MG-C: chat interface with messages]` — which chat platform?
- `[MG-D: workflow diagram]` — which automation platform?

This specificity enables the storyboard and Hera generation steps to look up the tool's exact visual identity (colors, UI layout, key elements) from the tool visual reference library and produce authentic-looking motion graphics instead of generic placeholders.
