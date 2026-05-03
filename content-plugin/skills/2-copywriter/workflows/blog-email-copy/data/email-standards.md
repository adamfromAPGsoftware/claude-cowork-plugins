# Email Campaign Standards

## Core Principles

- Every email is a conversation with **one person** — never write to "a list", write to one subscriber sitting at their desk
- **Specifics beat vague** — real dollar amounts, real timelines, real project names. If it could be said by anyone, it shouldn't be said by the creator
- **One CTA per email**, one clear action. Clarity over cleverness, always
- **Brand voice is non-negotiable** — authenticity over polish

---

## Tone & Voice Rules

- **Conversational first-person** — write like explaining to a smart friend, not a marketing department
- **Short paragraphs:** 1-3 sentences max. One idea per paragraph. Let the email breathe
- **Em dashes over commas** — they create natural pauses and feel more spoken than written
- **Specific over vague** — real numbers, real timelines, real project names. Never "recently" when you can say "last Tuesday"
- **Contrarian positioning** — challenge assumptions, share unpopular takes. "Everyone says X. I think that's wrong."
- **No corporate language** — never say "leverage", "synergy", "utilize", "ecosystem", "revolutionize", "game-changing". Say what you mean in plain words
- **Strategic bold** — bold the ONE phrase per section you want skimmers to catch. Never bold full sentences or paragraphs
- **Rhetorical questions** — use sparingly. One per email max. Make it count
- **Anti-hype** — no exclamation marks in body copy unless quoting someone. Energy comes from specificity, not punctuation

---

## Hero Image

Every email includes a hero image at the top of the body, before the opening text.

### Selection Priority (from image catalog)
1. **Thumbnail** (`type: thumbnail`) — Video thumbnails are designed to grab attention and are ideal email heroes
2. **Key diagram** (`type: diagram`) — Strong visual that previews the content (especially for technical/educational emails)
3. **B-roll still** (`type: broll`) — A compelling frame from extracted B-roll footage

### Embedding Rules
- Place the hero image immediately after any email header/preheader, before the first line of body text
- Use markdown image syntax: `![descriptive alt text](path/to/image.ext)`
- Alt text should describe the image AND hint at the email content (for accessibility and image-blocked clients)
- One hero image only — emails should not have multiple images cluttering the flow
- If no image catalog assets are available, skip the hero image — the email still works without it

### Image Hosting (Critical for Emails)
- **Email images MUST be publicly hosted URLs** — local file paths will NOT render in email clients (Gmail, Apple Mail, Outlook, etc.)
- During drafting: use the local project path and flag with `<!-- REQUIRES HOSTING: {local-path} -->`
- Before sending: upload the flagged image to your email platform's media library (Beehiiv, Kit, Mailchimp, etc.) and replace the local path with the public URL
- Remind the user to replace any `<!-- REQUIRES HOSTING -->` flagged paths with hosted URLs before sending

---

## Format A: Story-Driven Style

**Use when:** The content has a personal story angle, a lesson learned, or an experience to share
**Word count target:** 400-500 words
**Style influence:** Story-driven — raw, specific, no fluff, feels like a private email

**Structure:**
1. **Hero image** (from image catalog)
2. **Cold open** (1-2 sentences) — NO greeting. Drop straight into the story or hook. First line should feel like you're mid-conversation. "I spent 6 hours last Tuesday rebuilding something that should've taken 20 minutes."
3. **Story body** (2-3 short paragraphs) — the experience, the mistake, the discovery. Specific details. Real timelines. What actually happened
4. **Insight / lesson** (1 paragraph) — the takeaway. What you learned. What changed
5. **Natural bridge** (1-2 sentences) — connect the story to something the reader can act on. No forced transitions
6. **Single bold CTA** — soft sell, conversational. "If you're curious, here's where I break it all down →". Bold the CTA link text
7. **Sign-off** — "Talk soon," then line break, then "{brand.creator_name}"
8. **PS section** (ALWAYS include) — PS is prime real estate. Use it for a secondary hook, a surprising stat, or a teaser for next week. Italicize the PS content. Format: `**P.S.** *{content}*`

**Tone:** Conversational, personal, like texting a smart friend. No greeting — cold opens only.

**Bullet discipline:** NEVER use bullet points in Format A. Story-driven emails are prose only — bullets break the narrative flow.

---

## Format B: Announcement / Liam Ottley Style

**Use when:** Launching something new, sharing a video drop, promoting a resource
**Word count target:** 150-250 words
**Style influence:** Liam Ottley — direct, high-energy, bullet-driven, gets to the point fast

**Structure:**
1. **Hero image** (from image catalog)
2. **Greeting** — "Hey –" then line break, then "{brand.creator_name} here."
3. **Hook** (1-2 sentences) — what's new, why now, what happened. Lead with the result or the number
4. **Context with bold figures** (1-2 sentences) — social proof, credibility, specific numbers in bold. "This system handles **$47k/mo** in client work"
5. **"What's inside" bullets** (3-5 bullets) — what the reader gets. Each bullet starts with a bold label: "**The exact prompt** I use to...", "**A live demo** showing..."
6. **Direct CTA** — action-oriented, clear. "Watch it here →" or "Grab the template →". Bold the link text
7. **Sign-off** — "Keep going," then line break, then "{brand.creator_name}"
8. **PS** (optional) — secondary hook or teaser. Same italicized format as Format A

**Tone:** Direct, confident, high-energy but not hype. Every sentence earns its place.

**Bullet discipline:** Bullets are ENCOURAGED in Format B — they're the core value delivery mechanism. 3-5 bullets in the "what's inside" section.

---

## CTA Patterns

### Soft Sell (Format A)
- Weave the CTA naturally into the closing paragraph
- "If you're curious, here's where I break the whole thing down →"
- "I recorded the full build — [watch it here →](URL)"
- Never say "Click here" — that's a link, not a CTA

### Direct Sell (Format B)
- Bold, clear, action-oriented
- "**[Watch the full breakdown →](URL)**"
- "**[Get the template →](URL)**"
- Keep it to one line — no paragraph-length CTAs

### PS as Secondary CTA
- PS can contain a different link/action from the main CTA
- Use for referral program, upcoming content teaser, or community invite
- "**P.S.** *Know someone building with AI? [Send them this](URL) — we're running a $1,000 referral program right now.*"

### Anti-Patterns
- NEVER use "Click here" as CTA text
- NEVER use "Don't miss out" or "Act now" — no false urgency
- NEVER have more than one CTA in the body (PS is the exception, it's a bonus)

---

## Subject Line Rules

- **Length:** Under 50 characters — no exceptions
- **Case:** Lowercase or sentence case only — never Title Case or ALL CAPS
- **Style:** Curiosity-driven — make them NEED to open it
- **Avoid:** Clickbait, spam triggers, false urgency, excessive punctuation, emoji
- **Patterns that work:**
  - Curiosity gap: "i was wrong about AI agents"
  - Incomplete thought: "the one thing I changed about my..."
  - Benefit: "how to get 3x more from your content"
  - Question: "are you making this content mistake?"
  - Specific: "i automated my entire content pipeline"
  - Real number: "this agent saves me 6 hours a week"

---

## Preview Text Rules

- **Length:** 1-2 sentences that BUILD ON the subject (don't repeat it)
- **Purpose:** Make the email even more compelling to open
- **Relationship:** Subject line opens the loop, preview text adds specificity
- **Think of it as the subject line's wingman**

---

## Persistent Footer Elements

Include these inside the email body (NOT in the template — template handles header/headshot/social/unsubscribe):

**Exact approved footer copy:**

```
---

🤖 [{YOUR_FREE_COMMUNITY}](https://{YOUR_COMMUNITY_URL}) — Free tools, templates, and tutorials to help you build with AI.
```

**Do NOT paraphrase or rewrite the footer copy.** Use this exact wording every time.

---

## HTML Conversion Rules

When converting email markdown to HTML for your email platform (see `{brand.email.platform}` in config.yaml), apply these inline styles to every element. Many email platforms strip `<style>` blocks — all styling must be inline.

### Element Style Table

| Element | HTML | Inline Style |
|---------|------|-------------|
| Paragraph | `<p>` | `style="margin: 0 0 16px 0; line-height: 1.6; font-size: 16px;"` |
| Unordered list | `<ul>` | `style="margin: 0 0 16px 0; padding-left: 24px;"` |
| List item | `<li>` | `style="margin: 0 0 8px 0; line-height: 1.6; font-size: 16px;"` |
| Horizontal rule | `<hr>` | `style="border: none; border-top: 1px solid #e5e5e5; margin: 24px 0;"` |
| Link | `<a>` | `style="color: #1a73e8; text-decoration: underline;"` |
| Bold | `<strong>` | No additional style needed |
| Italic | `<em>` | No additional style needed |
| Line break | `<br>` | No additional style needed |

### Image Embedding HTML

```html
<img src="{hosted-url}" alt="{alt-text}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 0 0 16px 0;" />
```

### Persistent Footer HTML Block

```html
<hr style="border: none; border-top: 1px solid #e5e5e5; margin: 24px 0;" />
<p style="margin: 0 0 16px 0; line-height: 1.6; font-size: 16px;">
  🤖 <a href="https://{YOUR_COMMUNITY_URL}" style="color: #1a73e8; text-decoration: underline;">{YOUR_FREE_COMMUNITY}</a> — Free tools, templates, and tutorials to help you build with AI.
</p>
```

---

## Email Output Frontmatter Schema

```yaml
---
subject: ""
preview_text: ""
format: "A"  # or "B"
hero_image: ""  # path to selected hero image
date: ""
status: draft
broadcast_id: ""  # populated after email draft push
stepsCompleted: []
---
```

---

## Subject Line Variants

When polishing, generate 2-3 subject line variants:
- **Variant 1:** Curiosity-driven (open a loop)
- **Variant 2:** Benefit-driven (what they get)
- **Variant 3:** Pattern interrupt (unexpected angle)

Present all variants with brief rationale for each. User selects the winner.

---

## Quality Checklist

Before presenting an email draft, verify:

- [ ] Hero image selected from catalog and placed at top of email body (if assets available)
- [ ] Hero image has descriptive alt text
- [ ] Subject line: lowercase/sentence case, under 50 characters, curiosity-driven
- [ ] Preview text: 1-2 sentences, builds on subject line (not repeats it)
- [ ] Format A or B structure followed correctly
- [ ] **Word count in range** — Format A: 400-500, Format B: 150-250
- [ ] Written to ONE person, not a list
- [ ] Specifics used (real numbers, timelines, names) — not vague
- [ ] One clear CTA only (PS may contain secondary)
- [ ] **Sign-off present** — "Talk soon, {brand.creator_name}" (A) or "Keep going, {brand.creator_name}" (B)
- [ ] **PS section present** — always for Format A, optional for Format B
- [ ] Brand voice maintained — authentic, not corporate, no banned words
- [ ] **No bullet points in Format A** — prose only
- [ ] Persistent footer elements included with exact approved copy
- [ ] **HTML-ready formatting** — no complex markdown that won't convert cleanly
- [ ] No blacklisted topics or brands referenced
