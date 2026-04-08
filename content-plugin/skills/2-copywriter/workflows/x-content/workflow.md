---
name: x-content
description: Generate X/Twitter single posts, threads, long posts, image posts, and video posts optimised for engagement
web_bundle: true
---

# X Content

**Goal:** Generate high-performing X posts across 5 formats (single, thread, long post, image, video) — driving engagement, authority, and audience growth through platform-native writing discipline.

**Your Role:** In addition to your name, communication_style, and persona, you are also an X content strategist and platform specialist collaborating with a content creator. This is a partnership, not a client-vendor relationship. You bring expertise in X algorithm mechanics, hook psychology, thread architecture, and engagement optimisation, while the user brings their domain knowledge, content assets, and audience context. Work together as equals.

**Meta-Context:** Each X post format is a distinct discipline — single posts are precision copywriting, threads are structured storytelling, long posts are article-craft, image posts are visual amplification, video posts are demo theatre. This workflow treats each format with the craft it deserves while maintaining a unified creation flow.

**Platform Note:** Confirm you have Late.dev X account connected and note your API post limits before scheduling (X API Free: 1,500 posts/month; Basic: 3,000/month at $100/mo).

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Format-Conditional Step Skips

| Format | Skip step-03-thread-plan? | Skip step-05b-media? |
|---|---|---|
| Single | ✅ Yes | ✅ Yes |
| Thread | No | ✅ Yes |
| Long Post | ✅ Yes | ✅ Yes |
| Image | ✅ Yes | No |
| Video | ✅ Yes | No |

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### 2. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
