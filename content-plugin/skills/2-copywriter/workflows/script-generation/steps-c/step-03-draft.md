---
name: 'step-03-draft'
description: 'Generate the video script — fully scripted intro, dot-point body segments, and CTA with iteration support'

nextStepFile: './step-04-assets.md'
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/scripts/script-{concept_slug}-{date}.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
excalidrawCreateStep: '{project-root}/content-plugin/skills/2-copywriter/workflows/excalidraw-diagrams/steps-c/step-01-init.md'
---

# Step 3: Script Draft

## STEP GOAL:

To generate the video script content — a fully scripted word-for-word intro, dot-point body segments with key talking points, and a CTA/outro — based on the approved creative direction.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Copywriter drafting a YouTube video script
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in scriptwriting, hooks, retention, and natural speaking patterns
- ✅ The user brings their voice, style, and domain expertise — the script should sound like THEM, not a generic AI. Reference `creator-voice.md` for Adam's exact speaking patterns.

### Step-Specific Rules:

- 🎯 Focus on generating the script content in the correct format
- 🚫 FORBIDDEN to generate YouTube metadata, thumbnails, or B-roll in this step
- 💬 The intro MUST be word-for-word scripted; the body MUST be dot-point talking points
- 📋 Support iteration — user can request revisions before approving
- 🎯 The script should be natural, conversational, and match the approved tone from the direction step

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Append approved script to the Scripted Intro, Body Segments, and CTA/Outro sections of {outputFile}
- 📖 Update frontmatter stepsCompleted when proceeding
- 🚫 FORBIDDEN to proceed without user approval of the script draft

## CONTEXT BOUNDARIES:

- Available: Concept brief, approved direction (angle, hook strategy, tone), optional inputs (video length, talking points)
- Focus: Script content only — intro, body, CTA
- Limits: No metadata, thumbnails, or B-roll
- Dependencies: Approved direction from step 02

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Review Approved Direction

Before drafting, review:
- The approved angle and approach
- The hook strategy
- The tone and energy
- Target video length
- Any specific talking points requested

**Load Pattern Reference Data:**
- Load `long-form-patterns.md` from `inspiration/` — reference the **Key Takeaways** section for intro structure and pacing
- Load `creator-credentials.md` from `inspiration/` — reference Adam's actual credentials for the credibility stacking sequence
- Load `creator-voice.md` from `inspiration/` — match Adam's sentence structure, contractions, signature phrases, and opening formulas when writing the scripted intro

### 2. Generate Script Draft

Generate and present the complete script draft:

"**Here's your script draft:**

---

### INTRO (Word-for-Word Script)

Write the intro as **natural conversation** — it must sound like Adam talking, not a template being filled in. Target 35–45 seconds total, ~120 words. The sections below should FLOW into each other seamlessly — if you can feel where one section ends and the next begins, it's too rigid.

**Voice check:** Intro must match creator-voice.md — contractions throughout, signature phrases preferred ("jump into", "with all the boring stuff out of the way", "without wasting any more of your time", "genuinely", "actually"), 60/40 long/short sentence mix, "you" every 2-3 sentences, calm authority tone. Open with "Look" or "So" or a direct statement — never "Hey guys" or formal preamble.

**HOOK (0–5s):**
[Approved hook formula from direction step. Under 20 words. Must include a specific number. Single breath — one continuous spoken phrase.]

**CREDIBILITY + CONTEXT (5–15s):**
[ONE sentence only. Rattle off 2–3 credentials from creator-credentials.md rapid-fire, then immediately connect to WHY this matters for the video. Example: "Look, I run {YOUR_COMPANY} — 250 projects, over a million in AI development, top 1% on Upwork — and I use both of these tools every single day. So I actually know where each one breaks down." The "and" bridge connecting creds to context is critical — it makes the creds feel relevant, not performative. 10 seconds MAX then move on.]

**WHAT YOU'LL LEARN (15–30s):**
[Natural tease of what you'll cover. DO NOT use "By the end of this video, you're going to..." followed by a bulleted list. Instead, weave it conversationally: "I'm going to show you [main thing], and then [the surprising part] — because [reason this matters]." One flowing thought. If there's a barrier to address (e.g., "you don't need to be a developer"), fold it in naturally as a single clause — NOT as a standalone paragraph. Most videos don't need barrier removal at all.]

**BRIDGE (30–40s):**
[Adam's signature transition. Pick one: "So with all the boring stuff out of the way — let's jump into it." / "So without wasting any more of your time — let's get into it." / "Let me start by showing you [first thing]." One sentence. Done.]

**ANTI-PATTERNS — NEVER DO THESE:**
- "By the end of this video, you're going to..." + enumerated list = sounds like a table of contents
- "I'm going to... Then I'm going to... And then I'm going to..." = repetitive, robotic
- Standalone "You don't need to be a developer" paragraph = filler, patronising
- Credibility as multiple sentences = over-explaining
- Intro longer than 45 seconds = you've lost them

**MOTION GRAPHIC STAGE DIRECTIONS:**
Include `[MG-X]` tags throughout the intro at visual change intervals (every 4-8s). These are placement hints — the storyboard expands them into full Hera prompts after filming. Use the Type A-G vocabulary:
- `[MG-A: "$1M+ revenue"]` — when speaker says a number/metric
- `[MG-B: n8n logo]` — when speaker first mentions a tool/platform
- `[MG-C: YouTube comments]` — when referencing social proof/audience reaction
- `[MG-D: API concept diagram]` — when explaining an abstract concept
- `[MG-E: 3-item agenda list]` — when walking through a list
- `[MG-F: developer at laptop]` — when storytelling / narrative context
- `[MG-G: smooth pan across workflow]` — when guiding through a document

**Intro targets:** ~150–180 wpm speaking pace. Match approved tone and energy. Include stage directions for visual elements [in brackets].

---

### BODY SEGMENTS

**Segment 1: [Topic/Theme]**
- [Key talking point]
- [Key talking point]
- [Key talking point]
- [Transition note to next segment]

**Segment 2: [Topic/Theme]**
- [Key talking point]
- [Key talking point]
- [Key talking point]
- [Transition note to next segment]

**Segment 3: [Topic/Theme]**
- [Key talking point]
- [Key talking point]
- [Key talking point]

[Add as many segments as needed based on content depth and target length]

---

### CTA / OUTRO

[Write the call-to-action and closing. Should include:
- Natural transition from final body segment
- Clear CTA (subscribe, comment, check link, etc.)
- Brief closing that matches the video's energy]

---

**How does this look?** Want to revise anything — the intro wording, body structure, talking points, or CTA?"

### 3. Handle Iteration

Wait for user feedback.

**If user approves:** Proceed to section 4.

**If user wants revisions [R]:**
- Ask what specifically they want changed
- Revise the flagged sections
- Re-present the updated draft
- Repeat until user is satisfied

Common revision requests:
- **Intro rewording** — adjust hook, tone, or pacing
- **Body restructuring** — reorder segments, add/remove points
- **Talking point additions** — include specific points the user wants
- **Tone adjustment** — more casual, more authoritative, etc.
- **Length adjustment** — expand or condense sections

### 4. Append Script to Output

Once user approves, append the approved content to {outputFile}:

- **Scripted Intro** section — word-for-word intro
- **Body Segments** section — dot-point segments
- **CTA / Outro** section — closing and CTA

Update frontmatter:
```yaml
stepsCompleted: ['step-01-init', 'step-02-direction', 'step-03-draft']
lastStep: 'step-03-draft'
```

"**Script draft locked in! Moving on to YouTube assets.**"

### 5. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [R] Revise Script [D] Diagram (Excalidraw) [C] Continue to YouTube Assets

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions — always respond and then redisplay menu

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF R: Ask user what to revise, regenerate the flagged sections, present updated draft, then [Redisplay Menu Options](#5-present-menu-options)
- IF D: Load, read entirely, then execute {excalidrawCreateStep} — this will discover the script, parse body segments into a diagram plan, generate hero illustrations via Gemini, and compose the Excalidraw storyboard. When complete, redisplay the menu.
- IF C: Save script to {outputFile}, update frontmatter, then load, read entire file, then execute {nextStepFile}
- IF Any other: help user, then [Redisplay Menu Options](#5-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user has approved the script draft AND selected 'C' will you save to {outputFile} and load {nextStepFile}. The [R] Revise option allows unlimited iterations before continuing.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Intro is fully scripted word-for-word and teleprompter-ready
- Body segments are dot-point key talking points (NOT word-for-word)
- CTA/outro is clear and matches video energy
- Script matches approved direction (angle, tone, hook strategy)
- Script sounds natural and conversational
- User has reviewed and approved the draft
- Iteration supported until user is satisfied
- Approved script appended to output document

### ❌ SYSTEM FAILURE:

- Writing body segments as word-for-word script instead of dot points
- Writing intro as dot points instead of word-for-word
- Generating metadata, thumbnails, or B-roll in this step
- Script doesn't match the approved direction
- Proceeding without user approval
- Not supporting the revision loop

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
