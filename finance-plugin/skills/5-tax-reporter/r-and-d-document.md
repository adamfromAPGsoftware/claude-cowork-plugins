---
name: r-and-d-document
description: Generate R&D activity documentation with evidence for AusIndustry registration
menu-code: RD
---

# R&D Document

Generate R&D activity documentation with contemporaneous evidence suitable for AusIndustry registration and ATO audit defence.

## Prerequisites

- Load `references/r-and-d-tax-incentive.md` for compliance requirements
- Load `references/r-and-d-activities-fy2025.md` if exists (or create it)

## Process

1. **Get the financial year from user.** Default: FY2025.

2. **Gather evidence sources:**
   - Read git log for the FY period across relevant repositories
   - Read key architecture/design documents (CLAUDE.md, pipeline docs, agent definitions)
   - List Upwork contractor names from finance-data.json to reference payment evidence
   - Check for any experiment logs, decision documents, or technical notes

3. **For each R&D activity, compile:**

   ### Activity Description (AusIndustry format)

   **a) What is the core R&D activity?**
   One paragraph describing the experimental activity.

   **b) What is the technical uncertainty?**
   What couldn't be known or determined in advance? Why couldn't a competent professional predict the outcome?

   **c) What hypothesis was being tested?**
   The specific technical hypothesis or question being investigated.

   **d) What systematic investigation was conducted?**
   How was the experiment designed? What methodology was followed?

   **e) What was the outcome?**
   What was learned? Was the hypothesis confirmed or refuted? What new knowledge was generated?

   **f) How does this advance the state of knowledge?**
   How does the outcome go beyond what was publicly available?

   **g) What evidence supports this?**
   List of contemporaneous records with dates.

4. **Define {YOUR_COMPANY}'s R&D Activities for FY2024-25:**

   **RD-01: BMAD Multi-Agent Orchestration Framework**
   - Type: Core R&D
   - Uncertainty: Whether multiple AI agents could be coordinated through a skill-based architecture with shared memory, sequential handoffs, and data contracts — no existing framework or published methodology existed for this specific orchestration pattern
   - Evidence: Agent definitions, skill manifests, pipeline configuration, memory system design

   **RD-02: Automated Business Process Extraction from Unstructured Transcripts**
   - Type: Core R&D
   - Uncertainty: Whether LLMs could reliably extract structured process data (tools, pain points, waste items, optimisation opportunities) from conversational meeting transcripts with sufficient accuracy for business use
   - Evidence: Extractor skill, audit-data.json schema evolution, extraction prompt engineering

   **RD-03: AI-Driven Sequential Pipeline with Data Contracts**
   - Type: Supporting R&D (supports RD-01 and RD-02)
   - Description: Experimental development of a 7-agent pipeline where each agent's output feeds the next through structured JSON data contracts
   - Evidence: Pipeline documentation, data contract definitions, agent handoff patterns

   **RD-04: AI-to-CRM Integration via MCP Protocol**
   - Type: Supporting R&D (supports RD-01)
   - Description: Novel integration of AI agents with CRM systems using the Model Context Protocol, an emerging standard with no established patterns for production use
   - Evidence: MCP configuration, CRM entity design, integration code

   **RD-05: Automated Deliverable Generation from Structured Data**
   - Type: Supporting R&D (supports RD-02)
   - Description: Experimental system for AI agents to generate client-facing HTML deliverables from structured audit data, with uncertainty in quality, accuracy, and client acceptability
   - Evidence: Builder skill, template system, generated deliverables

5. **Create output files:**

   **`references/r-and-d-activities-fy2025.md`** — Human-readable activity descriptions with evidence mapping

   **`finance/tax/FY2025/r-and-d/activity-register.json`:**
   ```json
   {
     "financial_year": "FY2025",
     "activities": [
       {
         "id": "RD-01",
         "name": "BMAD Multi-Agent Orchestration Framework",
         "type": "core",
         "description": "...",
         "uncertainty": "...",
         "hypothesis": "...",
         "methodology": "...",
         "outcome": "...",
         "evidence": [
           { "type": "code", "ref": "CLAUDE.md", "date_range": "2024-07-01/2025-06-30" },
           { "type": "upwork", "ref": "Upwork milestone records", "contractors": ["{CONTRACTOR_5}", "{CONTRACTOR_6}"] }
         ]
       }
     ],
     "generated_at": "ISO timestamp"
   }
   ```

   **`finance/tax/FY2025/r-and-d/evidence-log.json`:**
   ```json
   {
     "financial_year": "FY2025",
     "evidence_items": [
       {
         "id": "EVD-001",
         "type": "git_commit|upwork_contract|document|code_artifact",
         "date": "YYYY-MM-DD",
         "description": "What this evidence shows",
         "activity_ids": ["RD-01"],
         "source": "repository/path or external reference"
       }
     ],
     "generated_at": "ISO timestamp"
   }
   ```

6. **Present summary** and recommend next steps.

## Output

```
R&D Activity Documentation — {period}

  Activities documented: {count}
    Core R&D:       {core_count}
    Supporting R&D: {supporting_count}

  Evidence items compiled: {evidence_count}
    Git commits:    {git_count}
    Upwork records: {upwork_count}
    Code artifacts: {artifact_count}
    Documents:      {doc_count}

  Files created:
    - references/r-and-d-activities-fy2025.md
    - finance/tax/FY2025/r-and-d/activity-register.json
    - finance/tax/FY2025/r-and-d/evidence-log.json

  Next: Run R&D Categorize (RC) to tag transactions, then Generate Grant Report (GG).
```
