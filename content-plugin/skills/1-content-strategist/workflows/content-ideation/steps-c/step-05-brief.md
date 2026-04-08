---
name: 'step-05-brief'
description: 'Compile all sections into the final structured concept brief and save to output path'

outputFile: '{output_folder}/content-concept-{concept_slug}-{date}.md'
---

# Step 5: Concept Brief Output

## STEP GOAL:

To compile and polish all content from previous steps into a cohesive, actionable concept brief that downstream agents (Copywriter, Creative Director, Video Editor) can pick up and execute.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Content Strategist finalizing a deliverable for downstream teams
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ You bring expertise in clear communication and actionable documentation
- ✅ The user brings final approval authority

### Step-Specific Rules:

- 🎯 Focus only on compiling, polishing, and finalizing — do NOT generate new content
- 🚫 FORBIDDEN to add new ideas, platforms, or evaluations
- 💬 Ensure the brief is clear, complete, and actionable for downstream agents
- 📋 All 5 sections must be present and filled

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Polish and finalize {outputFile}
- 📖 Update frontmatter to mark workflow as complete
- 🚫 FORBIDDEN to modify the substance of decisions made in prior steps

## CONTEXT BOUNDARIES:

- Available: Complete output document with all sections filled from Steps 1-4
- Focus: Polish, coherence, and completeness
- Limits: Do not change strategic decisions — only improve clarity and presentation
- Dependencies: All content from Steps 1-4

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Complete Document

Load {outputFile} and review the complete document built across all previous steps.

"**Compiling your concept brief...**

Let me review everything we've built and ensure it's polished and ready for your team."

### 2. Document Optimization

Review the full document for:

1. **Completeness** — All 5 sections filled:
   - Concept Overview / Hook
   - ICP Alignment Rationale
   - Content Tree (platform breakdown)
   - Key Messages Per Platform
   - Suggested Formats / Angles

2. **Coherence** — Consistent narrative thread across all sections

3. **Clarity** — Each section is clear and actionable for downstream agents

4. **Duplication** — Remove any repeated information between sections

5. **Transitions** — Smooth flow between sections

6. **Actionability** — Downstream agents (Copywriter, Creative Director, Video Editor) have enough detail to execute

### 3. Polish and Finalize

Apply optimizations while maintaining:
- The user's voice and creative direction
- All strategic decisions made in prior steps
- The general structure and order
- Essential details and context

Update the frontmatter:
```yaml
stepsCompleted: ['step-01-init', 'step-02-generate', 'step-03-evaluate', 'step-04-tree', 'step-05-brief']
lastStep: 'step-05-brief'
status: 'complete'
```

### 4. Present Final Brief Summary

"**Your Content Concept Brief is complete!**

---

**Concept:** [Title]
**Score:** [Score]/30 — [Rating]

**Sections:**
1. **Concept Overview / Hook** — [One-line summary]
2. **ICP Alignment Rationale** — [One-line summary]
3. **Content Tree** — [Number] platform branches mapped
4. **Key Messages Per Platform** — Tailored messaging for each platform
5. **Suggested Formats / Angles** — Platform-native formats defined

**Output saved to:** `{outputFile}`

---

**This brief is ready for:**
- **Copywriter** — To develop copy for each platform branch
- **Creative Director** — To plan visual direction per platform
- **Video Editor** — To develop video content from the tree

---

**Thank you for working through this together! Your content concept is strategically grounded and ready for execution.**"

### 5. Workflow Complete

This is the final step. No next step to load.

Save the final polished document to {outputFile} and confirm completion.

## CRITICAL STEP COMPLETION NOTE

This is the FINAL STEP. After saving the polished brief and presenting the summary, the workflow is complete. No further steps to load.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 5 sections present and filled in the output document
- Document polished for coherence, clarity, and actionability
- No duplication between sections
- Frontmatter updated to mark workflow complete
- Final summary presented to user
- Output saved to correct path
- Brief is actionable for downstream agents

### ❌ SYSTEM FAILURE:

- Missing sections in the final brief
- Adding new content not from prior steps
- Changing strategic decisions made in prior steps
- Not updating frontmatter to complete status
- Not saving the final document
- Brief not actionable for downstream agents

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
