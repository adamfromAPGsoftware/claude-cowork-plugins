---
step: 3
name: images
description: Generate images for sections with no matching reference frame
---

# Step 3 — Images

## 1. Check if any images are needed

Read `{plan_file}`. Count rows in the screenshot match table with status CAPTURE or GENERATE.

**If count = 0:** Skip this step entirely. Print: "All screenshots matched from reference frame catalog — skipping image generation." Then load Step 4.

**If count > 0:** Continue with sections 2a and 2b below.

---

## 2a. Playwright captures (Tier 1)

For each item in the screenshot match table with status **CAPTURE**:

### Navigate and capture

1. Navigate to the URL:
   ```
   mcp__playwright__browser_navigate(url="{URL}")
   ```

2. Wait 2–3 seconds for the page to fully render. If the page has a cookie/auth banner, dismiss it or scroll past it.

3. Take a screenshot:
   ```
   mcp__playwright__browser_take_screenshot(path="{images_dir}/{descriptive-name}.png")
   ```
   Use a descriptive kebab-case name that reflects the content (e.g., `sample-tutorial-screenshot.png`, `github-audit-repo-tree.png`).

4. Verify the file was created. If successful: update the plan — change status to CAPTURED, record the path `./images/{name}.png`.

### Error handling

If Playwright is unavailable (MCP not connected) OR the page fails (timeout, 404, auth wall, login redirect):
- If a catalog reference frame matches the tool mentioned: fall back to that (mark as MATCHED)
- Otherwise: fall back to GENERATE — write a description for Gemini generation

### Close browser

After processing all CAPTURE items: call `mcp__playwright__browser_close` to free resources.

---

## 2b. Load image prompt templates

Read `{project-root}/content-plugin/skills/2-copywriter/workflows/diagram-generation/data/image-prompt-templates.md`

---

## 3. Generate images (Tier 3) — sequential only, never parallel

Process only items still marked **GENERATE** after the Playwright pass.

For each image in the "Images to Generate" table:

### 3a. Craft the prompt

Using the prompt templates from `data/image-prompt-templates.md`, write a complete image generation prompt. Match the template to the content:
- Terminal/code output → terminal template
- Claude Code in action → Claude Code interface template
- File/folder structure → file explorer template
- Workflow/pipeline → pipeline diagram template
- Abstract concept with no tool context → conceptual diagram template
- Abstract concept that maps to a known tool's aesthetic → **concept-on-backdrop template** (preferred for architecture/layer diagrams)

### 3b. Generate via fal-ai MCP

Call:
```
mcp__fal-ai__generate_image(
  prompt="{FULL_PROMPT}",
  image_size="landscape_4_3"
)
```

Save the returned image to: `{images_dir}/{descriptive-name}.png`

**Descriptive name:** kebab-case, describes what the image shows (e.g., `claude-code-review-session.png`, `workflow-pipeline-overview.png`)

### 3c. Verify output

Check that the file was created at `{images_dir}/{name}.png`. If the script fails, try once more with a simpler prompt. If it fails again, note it and use a placeholder ScreenshotNode (omit `src`) for that node in Step 4.

### 3d. Update the plan

Record the generated image path in `{plan_file}`. The ScreenshotNode `src` for generated images is:
`./images/{name}.png`

(The `images/` folder is a sibling of the HTML file, so this relative path works.)

### 3e. Present generated image (collab mode only)

In collab mode: show the image path and ask if it looks good. If not, regenerate with adjusted prompt. In auto mode: proceed without review.

---

## 4. Generation complete

Print a summary:
```
Generated {count} images:
- {name}.png — {description}
- ...
```

Then load Step 4.

---

**Load next:** `steps-c/step-04-compose.md`
