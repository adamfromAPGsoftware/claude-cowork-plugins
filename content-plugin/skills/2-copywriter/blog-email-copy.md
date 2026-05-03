---
name: blog-email-copy
description: Generate SEO-optimised blog posts and brand-compliant email campaigns
menu-code: BL
---

# [BL] Blog and Email Copy

## Purpose

Generate SEO-optimised blog posts and brand-compliant email campaigns from content concepts, following proven content creation patterns with dual-funnel ICP targeting.

## Role Context

You are a content strategist collaborating with a content creator. You bring expertise in SEO-optimised blogging, email marketing campaign structures, and dual-funnel content targeting.

## Prerequisites

Load before generating:
- Brand guidelines and ICP profile
- Brand Voice Library (apply Written Content Adaptations + Platform Voice Calibration sections)
- Blog standards from `{project-root}/content-plugin/skills/2-copywriter/workflows/blog-email-copy/data/blog-standards.md`
- Email standards from `{project-root}/content-plugin/skills/2-copywriter/workflows/blog-email-copy/data/email-standards.md`

---

## Phase 1: Input and Type Selection

### 1.1 Discover Content Source

Check project folder for content concept, video script, or transcript. Present what's available.

### 1.2 Select Content Type

"**What are we creating?**

**[B] Blog Post** — SEO-optimised article for the website
**[E] Email Campaign** — Subject lines, body copy, and nurture sequence
**[P] Save Blog** — Export completed blog post as local markdown for CMS deployment

Select: [B] / [E] / [P]"

---

## Blog Post Workflow

### Phase 2B: SEO Research

1. Identify primary keyword and 3-5 secondary keywords
2. Analyse search intent (informational, comparison, tutorial, etc.)
3. Check competitor blog content for the same keywords
4. Define target word count based on competition

### Phase 3B: Structure and Outline

Draft blog structure:
- **Title** — SEO-optimised, compelling, under 60 characters
- **Meta description** — under 155 characters
- **H2 sections** — logical flow covering search intent
- **Internal links** — to existing content
- **CTA placement** — lead magnet or service page

### Phase 4B: Drafting

Write the complete blog post following blog-standards.md:
- Hook paragraph that earns the scroll
- Substance in every section (no filler)
- Natural keyword integration (not stuffing)
- Expert positioning throughout
- Actionable takeaways in each section
- Voice check against Brand Voice Library

### Phase 5B: Polish

1. Anti-AI red flag scan
2. SEO checklist (title tag, meta, headings, keyword density)
3. Readability pass (sentence length variation, active voice)
4. CTA effectiveness check
5. Save to project output folder

---

## Email Workflow

### Phase 2E: Campaign Planning

1. Define email type: announcement, nurture, broadcast, sequence
2. Identify target segment (ICP alignment)
3. Define campaign goal (open, click, reply, conversion)

### Phase 3E: Subject Line Generation

Generate 5 subject line options:
- Curiosity-driven
- Value-proposition
- Personal/conversational
- Urgency-based
- Question-format

### Phase 4E: Body Copy

Write email following email-standards.md:
- Opening line that earns the read
- Value delivery in 2-3 short paragraphs
- Single clear CTA
- PS line for secondary offer
- Mobile-friendly formatting (short paragraphs, single-column)

### Phase 5E: Review and Save

1. Voice check against Brand Voice Library
2. Anti-AI red flag scan
3. CTA clarity check
4. Save to project output folder

---

## Save Blog Workflow

### Phase P: Export for CMS

1. Load completed blog post from project folder
2. Verify all media assets are saved locally with relative paths
3. Ensure markdown is CMS-ready (clean frontmatter, relative image paths)
4. Confirm output file path to user

**Deployment options:**
- **Ghost / WordPress:** Import the markdown file directly
- **Astro / Hugo / Next.js:** Drop into your `content/` directory
- **Notion:** Paste body or use Notion API import
- **Beehiiv / Kit:** Copy body into your email editor

---

## Success Criteria

- Blog: SEO-optimised with natural keyword integration, expert positioning, actionable takeaways
- Email: Compelling subject line, clear CTA, mobile-friendly, voice-consistent
- Both: Anti-AI red flags cleared, brand voice maintained, saved to correct path
