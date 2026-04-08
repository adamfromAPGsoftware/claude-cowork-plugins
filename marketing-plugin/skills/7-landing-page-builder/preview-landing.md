---
name: preview-landing
description: Preview a generated landing page and run through the verification checklist
menu-code: PV
---

# Preview Landing Page

Preview a generated landing page and verify it meets quality standards before deployment.

## Process

1. **Load campaign data** — Read `marketing-plugin/data/campaign-data.json`. List campaigns where `landing_page.status` is `"generated"` or `"deployed"`.

2. **Resolve campaign context:**
   - If `{active_campaign}` is set from activation, confirm: "Previewing landing page for: **{active_campaign.name}**. Proceed?"
   - If `{active_campaign}` is null, present campaigns. Ask which one to preview.

3. **Read the generated landing page** — Load `marketing-plugin/data/landing-pages/{campaign_id}/index.html`.

4. **Provide local file path** — Tell the user:
   ```
   Landing page ready for preview:
   {project-root}/marketing-plugin/data/landing-pages/{campaign_id}/index.html

   Open this file in your browser to preview.
   ```

5. **Present verification checklist:**
   ```
   Verification Checklist — {campaign.name}

   Content:
   - [ ] Headline matches campaign strategy
   - [ ] Subheadline supports the headline
   - [ ] Benefits are clear and compelling
   - [ ] Social proof is visible and credible
   - [ ] CTA is prominent and clear

   Form:
   - [ ] All required fields present
   - [ ] Form action URL is set (not "#")
   - [ ] Hidden UTM fields present

   Tracking:
   - [ ] GA4 gtag.js script present
   - [ ] Meta Pixel script present
   - [ ] UTM capture script present
   - [ ] Form submission event handlers present

   Design:
   - [ ] Mobile-responsive (check at 375px width)
   - [ ] Brand colours correct (navy #1B2A4A, blue #3B82F6, lime #7DFF00)
   - [ ] Inter font loading
   - [ ] No broken images or links

   Performance:
   - [ ] Single-file HTML (no external CSS/JS dependencies except fonts + tracking)
   - [ ] Page loads fast (no heavy assets)
   ```

6. **Automated checks** — Parse the HTML and verify programmatically:
   - `<!-- TRACKING_SCRIPTS -->` placeholder is gone (tracking injected)
   - `{{` double braces are gone (all variables substituted)
   - Form has an action attribute that is not "#"
   - GA4 measurement ID is present (search for `gtag`)
   - Meta Pixel ID is present (search for `fbq`)
   - Report any issues found automatically.

7. **Ask for approval:**
   ```
   Does the landing page look good? This is APPROVAL GATE 3.
   - Approve: Ready for deployment via [DL]
   - Reject: Tell me what to change
   ```

8. **On approval:**
   - Add to `approval_log`: `{ "gate": "landing_page", "status": "approved", "timestamp": "...", "notes": "Preview verified" }`
   - Update status to indicate ready for deployment

9. **On rejection:**
   - Ask what needs to change
   - Offer options: re-run [GL] to regenerate, [ST] to fix tracking, or manual edits
   - Add to `approval_log`: `{ "gate": "landing_page", "status": "rejected", "timestamp": "...", "notes": "{user feedback}" }`

## React Template (go-enhance)

When the campaign's `landing_page.template` is `go-enhance`, the preview workflow changes:

1. **Start dev server** — Run:
   ```bash
   cd marketing-plugin/{landing_page.deploy_path} && npm run dev
   ```
   Preview at `http://localhost:8080`.

2. **Verification checklist** — Replace the standard HTML checklist with:
   ```
   Verification Checklist — {campaign.name} (React)

   Functionality:
   - [ ] Qualification quiz opens and flows correctly through all steps
   - [ ] Form submission works (check network tab for POST)
   - [ ] Tracking fires in browser console (GA4 + Meta Pixel events)
   - [ ] UTM parameters captured from URL and passed with form

   Design:
   - [ ] Responsive at 375px width (mobile)
   - [ ] Brand colours and fonts correct
   - [ ] No console errors or broken assets
   - [ ] Animations and transitions smooth
   ```

3. **Automated checks** — For React templates, verify:
   - GA4 measurement ID is set in `index.html` (not placeholder)
   - Meta Pixel ID is set in `src/components/MetaPixel.tsx` (not placeholder)
   - `npm run build` completes without errors

4. **Approval gate and next steps** — Same as steps 7-9 above.

## Error Handling

- If landing page file doesn't exist, inform user to run [GL] first
- If automated checks find issues, present them prominently before the approval question
