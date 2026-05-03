# Setup Wizard [SW]

Walk the user through configuring all sections of `config.yaml` conversationally.
After each section, write the answers to the file and show a confirmation.
At the end, generate five reference files from the collected answers.

## Config file location

`{project-root}/config.yaml`

If the file does not exist, treat all values as empty and create it fresh during the first section write. If it exists, read it first to prefill existing values as defaults so re-runs preserve previously entered data.

---

## Pre-flight — Content Workspace

Before starting the numbered sections, configure the content workspace.

Ask:
"Where should your content workspace live? This is the folder where all your projects and outputs will be stored.

Default: `~/Content`

Enter an absolute path or press Enter to use the default."

- If the user presses Enter or types nothing, use `~/Content`
- Expand `~` to the user's home directory (run `echo $HOME` via Bash to resolve it)
- Validate: check the **parent** directory exists (e.g., if they enter `/Users/jane/MyContent`, confirm `/Users/jane/` exists)
- If the path does not already exist, create it with `mkdir -p {workspace}`
- Create the folder scaffold using `mkdir -p` for each subdirectory (skip if already exists):
  ```
  {workspace}/projects/
  {workspace}/references/
  {workspace}/standalone/
  {workspace}/brand-assets/logos/
  {workspace}/brand-assets/reference-photos/
  ```
- If `{workspace}/projects/_index.yaml` does not exist, create it with content:
  ```yaml
  projects: []
  ```
- Write the workspace and derived paths to config.yaml:
  ```yaml
  paths:
    workspace: "{absolute_workspace_path}"
    content_output_folder: "{absolute_workspace_path}"
    project_folder: "{absolute_workspace_path}/projects"
    standalone_folder: "{absolute_workspace_path}/standalone"
    output_folder: "{absolute_workspace_path}"
  ```

Show confirmation:
```
Workspace configured:
  Path:    {workspace}
  Created: projects/, references/, standalone/, brand-assets/logos/, brand-assets/reference-photos/
  (Existing directories were left unchanged)
```

---

## Section 1 of 8 — Brand Identity

Ask:
1. "What's your name? (This appears in the generated reference files)" → `brand.creator_name`
2. "What's your title or role?" Example: "Agency Owner", "Content Creator", "Consultant" → `brand.creator_title`
3. "What's your business or brand name?" → `brand.name`
4. "What's your main website URL?" → `brand.website`
5. "In one sentence — what do you help people with?" This becomes the plugin's north star for all content decisions. → `brand.what_you_do`

After collecting answers, write Section 1 to config.yaml.
Show confirmation:
```
✓ Section 1 of 8 saved — Brand Identity:
  Creator: {brand.creator_name} — {brand.creator_title}
  Brand:   {brand.name}
  Website: {brand.website}
  Focus:   {brand.what_you_do}
```

---

## Section 2 of 8 — Brand Voice

Explain first: "Most people write their brand voice like this: 'warm, professional, approachable.' Claude can't check its output against that. We're going to write it so it's checkable."

Ask:
1. "How would you describe your writing tone in 2–4 words?"
   Example: "direct and practical", "authoritative but conversational", "bold and no-nonsense"
   → `voice.tone_descriptors` (split into array)

2. "Do you use contractions? (you're / you are, we've / we have)"
   Yes or no — firm answer, no "sometimes"
   → `voice.contractions` (true or false)

3. "What words do you NEVER want to appear in your content?"
   Give them examples to prompt: leverage, seamless, game-changing, robust, utilize, synergy, holistic, innovative, cutting-edge
   Ask them to name at least 3. Add their list to the examples.
   → `voice.banned_words` (array)

4. "What's the maximum sentence length you want? (word count)"
   Default: 18 words. Explain: this keeps sentences punchy and scannable.
   → `voice.max_sentence_words`

5. "How do you open your content — do you lead with the takeaway, build up to it, or start with a question/hook?"
   → `voice.opening_style` (short description they give you, or let them pick: "lead with takeaway", "hook first", "build context then land")

6. "Any other writing rules that matter to you? (numbers as numerals, no passive voice, specific things you hate seeing, etc.)"
   → `voice.additional_rules` (array, can be empty)

After collecting answers, write Section 2 to config.yaml.
Show confirmation:
```
✓ Section 2 of 8 saved — Brand Voice:
  Tone:     {voice.tone_descriptors joined}
  Contractions: {yes/no}
  Banned:   {voice.banned_words joined}
  Max sentence: {voice.max_sentence_words} words
  Opening:  {voice.opening_style}
```

---

## Section 3 of 8 — Content ICP

Explain first: "ICP = Ideal Content Persona. The person you're making content for. We need this specific enough that Claude can ask 'would this person care about this?' and get a yes or no."

Ask:
1. "What role or title does your ideal audience member have?"
   Example: "agency owner", "solo founder", "SaaS marketer", "freelance designer"
   → `icp.role`

2. "How big is their business or team? (if relevant)"
   → `icp.company_size` (can be "any" or "solo" if not relevant)

3. "What do they already know? (don't over-explain this to them)"
   Example: "basic business ops, have tried Zapier at least once, comfortable with Google Workspace"
   → `icp.they_know`

4. "What do they NOT know? (don't assume this either)"
   Example: "MCP, LLM internals, token budgeting, prompt engineering jargon"
   → `icp.they_dont_know`

5. "What's the job they're trying to get done? (the outcome they want from your content)"
   Example: "delegate reliably without babysitting the output", "build something that runs without them", "land their first $10K client"
   → `icp.job_to_be_done`

6. "What's the #1 mistake you see content creators make when talking to this audience?"
   This becomes an anti-pattern instruction. Example: "selling them on AI in general — they're already sold, they want specifics"
   → `icp.anti_patterns` (array with this as first entry, ask if they have more)

After collecting answers, write Section 3 to config.yaml.
Show confirmation:
```
✓ Section 3 of 8 saved — Content ICP:
  Role:     {icp.role} ({icp.company_size})
  Know:     {icp.they_know}
  Don't:    {icp.they_dont_know}
  JTBD:     {icp.job_to_be_done}
```

---

## Section 4 of 8 — Target Platforms

Ask:
1. "Which platforms do you publish on? (select all that apply)"
   Options: YouTube, YouTube Shorts, LinkedIn, X (Twitter), Instagram, TikTok, Blog, Email newsletter
   → `platforms.active` (array of slugs: youtube, youtube-shorts, linkedin, x, instagram, tiktok, blog, email)

2. "Which is your lead platform — where your flagship content lives first?"
   Everything else should be derivatives or distribution from this.
   → `platforms.primary`

3. "How often do you post on each? (rough cadence is fine)"
   Go through each active platform and ask. Example: "YouTube: 1x/week, LinkedIn: 5x/week"
   → `platforms.frequency` (map of platform → cadence string)

After collecting answers, write Section 4 to config.yaml.
Show confirmation:
```
✓ Section 4 of 8 saved — Platforms:
  Lead:   {platforms.primary}
  Active: {platforms.active joined}
  Frequency: {platforms.frequency as compact table}
```

---

## Section 5 of 8 — Credentials

Explain: "The content plugin uses MCP servers connected at the Claude Code platform level. No API keys needed — I'll verify each one is reachable now."

For each MCP server, test connectivity:

1. **YouTube MCP** — call `mcp__youtube__searchVideos` with a simple query (e.g., "test"). If it returns any response, mark as connected.
2. **Buffer MCP** — call `mcp__buffer__buffer_api_help`. If it returns any response, mark as connected.
3. **fal-ai MCP** — call `mcp__fal-ai__list_models`. If it returns any response, mark as connected.

For any that aren't reachable, show:
```
⚠ {Service} MCP not connected.
  This is a platform-level MCP server — check your Claude Code MCP settings
  and ensure the {service} MCP is enabled.
```

Write Section 5 to config.yaml using these exact keys:

```yaml
credentials:
  youtube_mcp: "connected"      # or "not connected"
  buffer_mcp: "connected"       # or "not connected"
  fal_ai_mcp: "connected"       # or "not connected"
```

---

## Section 6 of 8 — Scheduling & Accounts

Explain first: "These connect the plugin to your Buffer account for publishing. Buffer account names must match what you see in your Buffer dashboard."

Ask:
1. "What timezone are you in? (for scheduling posts at the right local time)"
   Example: "Australia/Sydney", "America/New_York", "Europe/London"
   → `scheduling.timezone`

2. "What account handles do you use in Buffer for each platform?"
   For each platform they listed in Section 4 as active, ask for the Buffer channel name/handle.
   Example: "LinkedIn: My Company, Instagram: @my_brand, X: @myhandle"
   → `scheduling.accounts.{platform}` (e.g., `scheduling.accounts.linkedin`, `scheduling.accounts.instagram`)

After collecting answers, write Section 6 to config.yaml.
Show confirmation:
```
✓ Section 6 of 8 saved — Scheduling & Accounts:
  Timezone: {scheduling.timezone}
  Accounts: {accounts as compact list}
```

---

## Section 7 of 8 — Brand Assets

Explain first: "These control how your visuals look. You can skip any you're not ready to configure — you can always update them later with [UC] Update Section."

Ask:
1. "What's your primary brand accent colour? (hex code)"
   Example: "#39FF14" (neon green), "#3B82F6" (blue), "#F59E0B" (amber)
   Default if skipped: "#3B82F6"
   → `brand.colors.primary`

2. "Do you have a secondary/supporting colour? (hex code, or press Enter to skip)"
   → `brand.colors.secondary` (optional)

3. "Your logo files go in `brand-assets/logos/` in your workspace. Drop your logo files there — expected: `brand-logo.png`, `brand-logo-dark.png`, `brand-logo-light.png`."
   Default: `{workspace}/brand-assets/logos/`
   → `brand.assets.logo_dir`

4. "Reference photos for identity-preserving thumbnail generation go in `brand-assets/reference-photos/`. These are headshots/portraits of you that AI uses to keep your face consistent in thumbnails. Expected: `creator-hero-front.jpg`, `creator-3quarter-left.jpg`, `creator-3quarter-right.jpg`, `creator-smiling.jpg`, `creator-talking.jpg`."
   Default: `{workspace}/brand-assets/reference-photos/`
   → `brand.assets.reference_photos_dir`

5. "How do you sign off your emails? (the closing line above your name)"
   Examples: "Talk soon,", "Best,", "Until next time,", "Keep going,"
   → `brand.email.sign_off`

6. "How do you open your emails? (the greeting line)"
   Examples: "Hey –", "Hi [first name],", "Hello,"
   → `brand.email.greeting`

7. "Which email platform do you use for newsletters?"
   Options: ConvertKit, Beehiiv, Mailchimp, Kit, other (specify)
   → `brand.email.platform`

After collecting answers, write Section 7 to config.yaml.
Show confirmation:
```
✓ Section 7 of 8 saved — Brand Assets:
  Primary colour: {brand.colors.primary}
  Logos: {configured / not configured}
  Reference photos: {configured / not configured}
  Email sign-off: {brand.email.sign_off}
  Email platform: {brand.email.platform}
```

---

## Section 8 of 8 — Content Strategy (Optional)

Tell them: "This section is optional but helps the Content Strategist and Autopilot work more accurately. You can skip and configure later."

Ask:
1. "Who are your top 3–5 competitor or inspiration channels on YouTube? (name + YouTube handle)"
   These are channels your audience also watches — used for competitive research.
   Example: "Alex Hormozi (@AlexHormozi), Matt Gray (@MattGray)"
   → `strategy.competitors` (array of {name, youtube_handle})
   (Skip option: "I'll add these later")

2. "What are your 3–5 core content pillars? (the main topics you cover)"
   Example: "AI tools, agency operations, client delivery, personal development, business systems"
   → `strategy.content_pillars` (array)
   (Skip option: "I'll add these later")

3. "Do you have X Premium? (affects character limits for X/Twitter posts)"
   Yes or No
   → `strategy.x_premium` (true or false)

After collecting answers, write Section 8 to config.yaml.
If they skip, write empty values with a note.
Show confirmation:
```
✓ Section 8 of 8 saved — Content Strategy:
  Competitors: {N configured / skipped}
  Content pillars: {pillars joined / skipped}
  X Premium: {yes / no}
```

---

## Final step — Generate reference files

After all 8 sections are saved, generate five reference files:

### 1. `{project-root}/references/brand-voice.md`

```markdown
# Brand Voice — {brand.creator_name}

## Creator

**{brand.creator_name}** — {brand.creator_title}  
**{brand.name}** · {brand.website}  
**Focus:** {brand.what_you_do}

## Voice Rules

**Tone:** {voice.tone_descriptors joined with ", "}

**Writing rules:**
- Contractions: {always use them / never use them} — ({you're} not "you are", {we've} not "we have")
- Numbers as numerals: 3 steps, not three steps
- Sentence max: {voice.max_sentence_words} words
- {voice.opening_style}
- One idea per sentence

**Never use:** {voice.banned_words joined with ", "}

{if voice.additional_rules not empty}
**Additional rules:**
{voice.additional_rules as bullet list}
{endif}

## Anti-AI Red Flags

Flag and remove any of these before presenting a draft:

- Generic buzzwords: leverage, seamless, game-changing, robust, utilize, synergy, holistic, innovative, cutting-edge
- Filler openers: "It's worth noting that...", "I'd like to take a moment to...", "That being said...", "In today's fast-paced world..."
- Passive constructions when active is possible
- Hedging language: "might be", "could potentially", "may want to consider"
- Any word from the banned list above

## Before / After Examples

**Before (generic AI output):**
"In today's rapidly evolving digital landscape, leveraging AI-powered solutions can provide a seamless pathway to optimizing your content strategy."

**After (voice-compliant):**
"AI cuts the time to publish by 80%. Here's the exact workflow."
```

### 2. `{project-root}/references/content-icp.md`

```markdown
# Content ICP — {brand.name}

## Audience Profile

**Role:** {icp.role}
**Business size:** {icp.company_size}

**They already know:**  
{icp.they_know}

**They don't know — don't assume or over-explain:**  
{icp.they_dont_know}

**Their job-to-be-done (what they want from your content):**  
{icp.job_to_be_done}

## Anti-Patterns

Avoid these mistakes when writing for this audience:

{icp.anti_patterns as bullet list}
```

### 3. `{project-root}/references/platform-config.md`

```markdown
# Platform Config — {brand.name}

## Lead Platform

**{platforms.primary}** — flagship content lives here first. All other platforms are derivatives or distribution.

## Active Platforms

| Platform | Cadence |
|----------|---------|
{for each platform in platforms.active: | {platform} | {platforms.frequency[platform] or "as needed"} |}

## Repurposing Flow

1. Create for {platforms.primary} first — full depth, full length
2. {if youtube-shorts or instagram or tiktok in active}: Clip to short-form for {short-form platforms}
3. {if linkedin or x in active}: Adapt the key insight to text-form for {text platforms}
4. {if blog in active}: Expand the argument to long-form blog
5. {if email in active}: Wrap into email newsletter

## Publishing Notes

- Lead platform sets the release date — everything else follows within 24–48 hours
- Never publish identical copy across platforms — every platform gets native formatting
- Schedule for impact, not convenience — timing is distribution strategy
```

### 4. `{project-root}/references/scheduling-config.md`

```markdown
# Scheduling Config — {brand.name}

## Timezone

**{scheduling.timezone}**

## Buffer

Connect social accounts at: buffer.com/manage/channels

## Account Names

| Platform | Buffer Channel Name/Handle |
|----------|---------------------------|
{for each account in scheduling.accounts: | {platform} | {account_name} |}
```

### 5. `{project-root}/references/brand-assets.md`

```markdown
# Brand Assets — {brand.name}

## Colours

**Primary accent:** {brand.colors.primary}
{if brand.colors.secondary}**Secondary:** {brand.colors.secondary}{endif}

## Logo Files

Logo directory: {brand.assets.logo_dir}

Expected files:
- `brand-logo.png` — primary logo (light background)
- `brand-logo-dark.png` — dark mode logo
- `brand-logo-light.png` — light mode logo

## Creator Reference Photos

Directory: {brand.assets.reference_photos_dir}

Expected files:
- `creator-hero-front.jpg` — front-facing hero shot
- `creator-3quarter-left.jpg` — three-quarter left
- `creator-3quarter-right.jpg` — three-quarter right
- `creator-smiling.jpg` — smiling portrait
- `creator-talking.jpg` — mid-speech or animated

## Email

**Platform:** {brand.email.platform}
**Sign-off:** {brand.email.sign_off}
**Greeting:** {brand.email.greeting}

## Content Strategy

### Competitors / Inspiration Channels
{strategy.competitors as list: "- {name} (@{youtube_handle})"}

### Content Pillars
{strategy.content_pillars as bullet list}

### X Premium
{strategy.x_premium ? "Active — 25,000 character limit" : "Not active — 280 character limit"}
```

---

## Completion summary

After all five reference files are generated, show:

```
✅ Setup complete! (8 of 8 sections saved)

  Creator:   {brand.creator_name} — {brand.creator_title}
  Brand:     {brand.name} · {brand.website}
  Platforms: {platforms.active joined} (lead: {platforms.primary})
  Workspace: {paths.workspace}

config.yaml:
  config.yaml                                      ✓

Reference files:
  references/brand-voice.md        ✓
  references/content-icp.md        ✓
  references/platform-config.md    ✓
  references/scheduling-config.md  ✓
  references/brand-assets.md       ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next step: run /content:1-content-strategist → type CR to start research.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
