# GC — Generate Comprehensive Report (Gamma PDF)

## Purpose

Final deliverable step. Compile all audit findings into a professionally designed PDF report via Gamma, merge parts into a single file, save to deliverables, and regenerate the client website so the PDF appears as a download.

## Prerequisites

- `audit-data.json` must exist with completed audit data
- Best results when all deliverables are complete (post-TB / post-GM)
- Gamma MCP tools must be available
- `pdfunite` available on system (installed via Poppler on macOS)
- {YOUR_COMPANY} Gamma theme ID: `kx1k2pzin9xddv9`

## Workflow

### Step 1: Extract Content

Run the extraction script to produce structured markdown:

```bash
python3 {skill-root}/scripts/extract_report_content.py --client-slug {client_slug}
```

Capture the full stdout output. This produces ~1,300 lines of comprehensive markdown covering all audit data.

### Step 2: Split Content for Gamma

Gamma has a 20-card limit per generation. The report must be **comprehensive** — every proposed change gets its own dedicated page with full problem/solution/impact/future state detail. Never compress multiple changes onto one page to save space.

Estimate the required pages from the data:
- Cover + exec summary + company profile: ~3 pages
- Tools landscape: ~1 page
- Process analysis (1 page per stage): ~6 pages
- Waste analysis: ~2 pages
- **Proposed solutions (1 page per change)**: count of `proposed_changes[]` pages
- Strategic approach + tool selection: ~2 pages
- Transformation roadmap (1 page per phase): ~3 pages
- ROI summary + client readiness + next steps: ~3 pages

**Total pages** = ~20 + count of proposed_changes. Split into ceil(total / 20) Gamma generations.

For each part, fill up to 20 cards. The content split should fall on natural section boundaries (e.g., between the last process stage and waste analysis, or between two proposed changes). Never split a single change across two generations.

### Step 3: Generate in Gamma

For each part, call `mcp__claude_ai_Gamma__generate` with:

- **format**: `"document"`
- **cardOptions.dimensions**: `"a4"`
- **exportAs**: `"pdf"`
- **textMode**: `"preserve"`
- **numCards**: `20` (or fewer for Part 2)
- **textOptions**: `{ "amount": "extensive", "tone": "professional", "audience": "business-owner", "language": "en" }`
- **imageOptions**: `{ "source": "noImages" }`
- **themeId**: `"kx1k2pzin9xddv9"` ({YOUR_COMPANY} theme)
- **additionalInstructions**: Keep ALL data, quotes, tables, financial figures. Clean professional layout. Each proposed solution gets dedicated space. Include logo on cover: `{YOUR_LOGO_URL}`. Part 1 should NOT say "Part 1" — document will be merged. Part 2 should NOT include a cover page.

Generate both parts in parallel if possible. Poll `get_generation_status` until both complete.

### Step 4: Download and Merge PDFs

Download all PDFs from the `exportUrl` returned by each Gamma generation:

```bash
curl -sL "{part1_exportUrl}" -o /tmp/{client_slug}-report-part1.pdf
curl -sL "{part2_exportUrl}" -o /tmp/{client_slug}-report-part2.pdf
# ... repeat for any additional parts
```

Merge all parts in order with pdfunite:

```bash
pdfunite /tmp/{client_slug}-report-part1.pdf /tmp/{client_slug}-report-part2.pdf [...] clients/{client_slug}/deliverables/audit-report.pdf
```

### Step 5: Regenerate Client Website

The website generator auto-detects `audit-report.pdf` and adds a download card:

```bash
python3 {skill-root}/scripts/generate.py --client-slug {client_slug} --output client-website
```

### Step 6: Verify and Report

Confirm the PDF exists and report:

```
Comprehensive audit report generated:
  PDF: clients/{client_slug}/deliverables/audit-report.pdf
  Size: {file_size}
  Pages: ~{page_count} (Part 1: 20, Part 2: {part2_pages})

  Gamma sources:
    Part 1: {gammaUrl1}
    Part 2: {gammaUrl2}

  Client website regenerated with PDF download link.

  To deploy: bash scripts/deploy.sh
```

## Notes

- Gamma creates new content — it cannot edit. To regenerate, run GC again (overwrites previous PDF).
- The {YOUR_COMPANY} theme (white background, lime green accent, DM Sans) is applied automatically via themeId.
- The extraction script handles missing data gracefully — earlier-stage clients get partial reports.
- If Gamma is unavailable, the existing `audit-report-print.html` serves as a browser-printable fallback.
- The `pdfunite` merge is seamless — no visible seam between parts.
- After GC, always run GW to ensure the client website includes the PDF download.
