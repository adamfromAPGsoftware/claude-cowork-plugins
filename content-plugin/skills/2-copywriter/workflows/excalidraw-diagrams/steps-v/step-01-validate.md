---
name: 'step-01-validate'
description: 'Validate an ExcaliDraw diagram against quality standards and format compliance'

diagramStandards: '../data/diagram-standards.md'
excalidrawFormatReference: '../data/excalidraw-format-reference.md'
---

# Step 1: Validate Diagram

## STEP GOAL:

To validate an existing `.excalidraw` diagram against quality standards and ExcaliDraw format compliance, generating an actionable validation report.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify the diagram during validation
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A VALIDATOR — assess, don't fix
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a visual quality analyst validating diagram compliance
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ Be thorough but fair — report issues with severity levels
- ✅ You bring standards expertise, the diagram brings what it is

### Step-Specific Rules:

- 🎯 Focus on validation checks against standards — assess, report, don't fix
- 🚫 FORBIDDEN to modify the diagram in any way
- 💬 Approach: Systematic checks, structured report output
- 🎯 Use subprocess optimization (Pattern 2) for parallel validation checks when available
- 💬 If subprocess unavailable, perform checks sequentially in main thread

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Generate a structured validation report
- 📖 Load standards for validation criteria
- 🚫 This is a standalone validation step — no next step

## CONTEXT BOUNDARIES:

- Available: User-provided path to diagram file
- Focus: Quality and compliance assessment only
- Limits: Read-only — do not modify the diagram
- Dependencies: User must provide path to `.excalidraw` file

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Diagram and Standards

"**Please provide the path to the diagram you want to validate.**"

Load the `.excalidraw` file. Load `{diagramStandards}` and `{excalidrawFormatReference}`.

### 2. Format Compliance Checks

**With subprocess capability (Pattern 2 — Per-check Analysis):**

DO NOT BE LAZY — For EACH validation category, launch a subprocess that performs the check and returns structured findings.

**Without subprocess capability (Fallback):**

Perform checks sequentially in main thread.

**Check 1: JSON Structure**
- Valid JSON parseable
- Required top-level fields: `type`, `version`, `elements`, `appState`, `files`
- `type` equals `"excalidraw"`
- `version` equals `2`

**Check 2: Element Integrity**
- All elements have unique IDs
- All elements have required properties (id, type, x, y)
- No deleted elements (`isDeleted: false`)
- Fractional indices properly ordered

**Check 3: Binding Integrity**
- All `boundElements` references point to existing elements
- All `containerId` references point to existing containers
- Bidirectional bindings are consistent (container ↔ text)
- All `startBinding`/`endBinding` on arrows point to existing elements

**Check 4: Image Integrity**
- All `fileId` references in image elements exist in `files` object
- All entries in `files` object have valid `dataURL` and `mimeType`
- No orphaned files (files not referenced by any element)

### 3. Visual Quality Checks

**Check 5: Typography Hierarchy**
- Headers use large fontSize (36-48) per standards
- Body text uses medium fontSize (16-20)
- Font families match standards recommendations
- No text elements with tiny/unreadable fontSize

**Check 6: Colour Coding**
- Colours used match the semantic palette from standards
- Consistent colour usage (same concept = same colour)
- No clashing or hard-to-read colour combinations
- Background colours don't obscure text

**Check 7: Layout Quality**
- Minimum 20px padding between elements
- Elements within zones are aligned
- No overlapping elements (except intentional layering)
- Canvas size appropriate for diagram complexity

**Check 8: Visual Hierarchy**
- Clear primary/secondary/supporting element distinction
- Headers visually anchor sections
- Arrows guide the eye through logical flow
- Containers properly group related elements

### 4. Generate Validation Report

"**Validation Report: {diagram filename}**

| # | Check | Status | Severity | Details |
|---|-------|--------|----------|---------|
| 1 | JSON Structure | {✅ PASS / ❌ FAIL / ⚠️ WARN} | {Critical/High/Medium/Low} | {details} |
| 2 | Element Integrity | {status} | {severity} | {details} |
| 3 | Binding Integrity | {status} | {severity} | {details} |
| 4 | Image Integrity | {status} | {severity} | {details} |
| 5 | Typography | {status} | {severity} | {details} |
| 6 | Colour Coding | {status} | {severity} | {details} |
| 7 | Layout Quality | {status} | {severity} | {details} |
| 8 | Visual Hierarchy | {status} | {severity} | {details} |

**Summary:**
- **Passed:** {count}/8
- **Warnings:** {count}
- **Failures:** {count}
- **Overall:** {PASS / PASS WITH WARNINGS / FAIL}

**Recommendations:**
{Numbered list of specific actionable improvements, ordered by severity}

**To fix issues, run the Edit workflow on this diagram.**"

### 5. Final Summary

"**Validation complete.**

**Result:** {PASS / PASS WITH WARNINGS / FAIL}
**File validated:** {path}

**Done!** 🎯"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 8 validation checks performed
- Structured report generated with severity levels
- Actionable recommendations provided
- No modifications made to the diagram
- Clear pass/fail determination

### ❌ SYSTEM FAILURE:

- Modifying the diagram during validation
- Skipping validation checks
- Not providing severity levels
- Not generating actionable recommendations
- Vague or unstructured report

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
