#!/usr/bin/env python3
"""Extract audit-data.json into structured markdown for Gamma report generation.

Usage:
    python3 extract_report_content.py --client-slug dale-great-supports

Reads clients/{slug}/audit/audit-data.json and outputs markdown to stdout.
The markdown is structured with ## headings that Gamma uses as page boundaries.
Produces 30-50 pages of comprehensive audit content.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def fmt_aud(v):
    """Format a number as AUD currency string."""
    if v is None or v == 0:
        return "$0"
    if v >= 1000:
        return f"${v:,.0f}"
    return f"${v:.0f}"


def extract(data: dict) -> str:
    """Extract comprehensive markdown from audit-data.json."""
    lines = []

    company = data.get("company_name", "Client")
    contact = data.get("contact", {})
    contact_name = contact.get("name", "")
    contact_role = contact.get("role", "")
    company_size = contact.get("company_size", "")
    industry = data.get("industry_tag", "").upper()
    audit_start = data.get("audit_start_date", "")
    sessions_completed = data.get("sessions_completed", 0)
    stages = data.get("business_stages_covered", [])

    start_display = audit_start
    if audit_start:
        try:
            start_display = datetime.strptime(audit_start, "%Y-%m-%d").strftime("%d %b %Y")
        except ValueError:
            pass
    today = datetime.now().strftime("%d %b %Y")

    stage_labels = {
        "acquisition": "Acquisition",
        "onboarding": "Onboarding",
        "fulfilment": "Fulfilment",
        "retention": "Retention",
        "payroll_invoicing": "Payroll & Invoicing",
        "recruitment": "Recruitment",
        "quoting": "Quoting & Proposals",
        "reactivation": "Reactivation",
    }
    waste_type_labels = {
        "manual_data_entry": "Manual Data Entry",
        "duplicate_work": "Duplicate Work",
        "no_followup": "No Follow-up",
        "communication_gap": "Communication Gap",
        "missing_automation": "Missing Automation",
    }

    # Pre-compute aggregates
    pain_points = data.get("pain_points", [])
    waste_items = data.get("waste_items", [])
    proposed_changes = data.get("proposed_changes", [])
    optimisations = data.get("optimisations", [])
    processes = data.get("processes", [])
    tools = data.get("tools", [])
    entities = data.get("entities", [])
    headcount = data.get("headcount", {})
    roi_items = data.get("roi_items", [])
    business_metrics = data.get("business_metrics", [])
    decision_nodes = data.get("decision_nodes", [])
    positive_signals = data.get("positive_signals", [])

    seen = set()
    qualified_waste = []
    for w in waste_items:
        wid = w.get("waste_id", id(w))
        if wid in seen:
            continue
        seen.add(wid)
        if w.get("confidence") in ("HIGH", "MEDIUM"):
            qualified_waste.append(w)

    total_annual_waste = sum(w.get("annual_waste_aud", 0) or 0 for w in qualified_waste)
    total_weekly_hours = sum(w.get("hours_per_week", 0) or 0 for w in qualified_waste)
    total_annual_value = sum(
        (c.get("value") or {}).get("combined_annual_value_aud", 0) or 0
        for c in proposed_changes
    )
    opp_count = len(optimisations) if optimisations else 0
    stages_display = ", ".join(stage_labels.get(s, s.replace("_", " ").title()) for s in stages)
    changes_by_id = {c.get("change_id"): c for c in proposed_changes}
    roi_by_change = {r.get("linked_change_id"): r for r in roi_items}

    # ═══════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════════════════════════════════════════════
    lines.append(f"# {company} — Business Operations Audit Report")
    lines.append("")
    lines.append(f"Prepared for {contact_name}, {contact_role}" if contact_role else f"Prepared for {contact_name}")
    lines.append(f"{company_size}" if company_size else "")
    lines.append("")
    lines.append(f"Audit commenced: {start_display}")
    lines.append(f"Report generated: {today}")
    lines.append(f"Sessions completed: {sessions_completed}")
    lines.append("")
    lines.append("Prepared by {YOUR_COMPANY}")
    lines.append("{YOUR_EMAIL} | {YOUR_DOMAIN}")
    lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTIVE SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        f"{YOUR_COMPANY} conducted a comprehensive operational audit of {company}"
        f"{' (' + company_size + ')' if company_size else ''} "
        f"across {len(stages)} business stages: {stages_display}."
    )
    lines.append("")
    lines.append(
        f"Over {sessions_completed} discovery sessions, we mapped {sum(len(p.get('steps', [])) for p in processes)} "
        f"process steps, identified {len(pain_points)} pain points and {opp_count} optimisation opportunities, "
        f"and quantified {fmt_aud(total_annual_waste)}/year in operational waste ({total_weekly_hours:.1f} hours/week)."
    )
    lines.append("")
    if proposed_changes:
        lines.append(
            f"We have developed {len(proposed_changes)} proposed changes with a combined annual value of "
            f"**{fmt_aud(total_annual_value)}**, implementable across a phased roadmap."
        )
        lines.append("")

    # Key metrics grid
    lines.append("**Key Findings at a Glance:**")
    lines.append("")
    lines.append(f"- **{sessions_completed}** audit sessions conducted")
    lines.append(f"- **{len(stages)}** business stages mapped")
    lines.append(f"- **{sum(len(p.get('steps', [])) for p in processes)}** process steps documented")
    lines.append(f"- **{len(pain_points)}** pain points identified")
    lines.append(f"- **{opp_count}** optimisation opportunities")
    lines.append(f"- **{len(qualified_waste)}** waste areas quantified — **{fmt_aud(total_annual_waste)}/year**")
    lines.append(f"- **{len(tools)}** software tools assessed")
    if proposed_changes:
        lines.append(f"- **{len(proposed_changes)}** proposed changes — **{fmt_aud(total_annual_value)}/year** combined value")
    lines.append("")

    # Pain point themes
    pps = data.get("pain_points_summary", {})
    top_themes = pps.get("top_themes", [])
    if top_themes:
        lines.append("**Top Pain Point Themes:**")
        lines.append("")
        for theme in top_themes:
            name = theme.get("theme", "")
            count = theme.get("count", 0)
            example = theme.get("example_quote", "")
            lines.append(f"- **{name}** ({count} issues)")
            if example:
                lines.append(f'  > "{example}"')
        lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # COMPANY PROFILE
    # ═══════════════════════════════════════════════════════════════════════════
    lines.append("## Company Profile")
    lines.append("")
    lines.append(f"**{company}** is a {industry} provider" + (f" with {company_size}" if company_size else "") + ".")
    lines.append("")

    if entities:
        lines.append("### Business Entities")
        lines.append("")
        for e in entities:
            ename = e.get("name", "")
            etype = e.get("type", "")
            edesc = e.get("description", "")
            estaff = e.get("staff_count", "")
            lines.append(f"**{ename}**" + (f" ({etype})" if etype else ""))
            if edesc:
                lines.append(f"{edesc}")
            if estaff:
                lines.append(f"Staff: {estaff}")
            quote = e.get("source_quote", "")
            if quote:
                lines.append(f'> "{quote}"')
            lines.append("")

    if headcount:
        lines.append("### Headcount & Scale")
        lines.append("")
        for key in ["support_workers", "offshore_team", "participants_total"]:
            val = headcount.get(key)
            note = headcount.get(f"{key}_note", headcount.get(key.replace("_total", "") + "_note", ""))
            if val:
                label = key.replace("_", " ").title()
                lines.append(f"- **{label}:** {val}" + (f" — {note}" if note else ""))
        lines.append("")

    if business_metrics:
        lines.append("### Key Business Metrics")
        lines.append("")
        for bm in business_metrics:
            if isinstance(bm, dict):
                name = bm.get("metric", bm.get("name", ""))
                val = bm.get("value", "")
                quote = bm.get("quote", "")
                if name and val:
                    lines.append(f"- **{name}:** {val}")
                    if quote:
                        lines.append(f'  > "{quote}"')
            elif isinstance(bm, str):
                lines.append(f"- {bm}")
        lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # CURRENT TOOLS LANDSCAPE
    # ═══════════════════════════════════════════════════════════════════════════
    if tools:
        lines.append("## Current Tools Landscape")
        lines.append("")
        lines.append(f"{company} currently uses {len(tools)} software tools across their operations. "
                      "Several are underutilised or have been abandoned, representing both cost waste and missed capability.")
        lines.append("")

        for t in tools:
            name = t.get("tool_name", "")
            use = t.get("use_case", "")
            cost = t.get("monthly_cost_aud")
            cost_str = f"{fmt_aud(cost)}/mo" if cost else "Free"
            workarounds = t.get("workarounds", "")
            api = t.get("api_available")
            quote = t.get("quote", "")

            lines.append(f"### {name} — {cost_str}")
            lines.append("")
            if use:
                lines.append(f"**Usage:** {use}")
                lines.append("")
            if workarounds:
                lines.append(f"**Workarounds:** {workarounds}")
                lines.append("")
            if api is not None:
                lines.append(f"**API available:** {'Yes' if api else 'No'}")
            if quote:
                lines.append(f'> "{quote}"')
            lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # PROCESS ANALYSIS BY STAGE (full detail)
    # ═══════════════════════════════════════════════════════════════════════════
    if processes:
        lines.append("## Process Analysis")
        lines.append("")
        lines.append(
            f"We documented {sum(len(p.get('steps', [])) for p in processes)} process steps "
            f"across {len(processes)} business stages, identifying pain points, decision nodes, "
            f"and optimisation opportunities at each step."
        )
        lines.append("")

        pain_by_stage = {}
        for pp in pain_points:
            s = pp.get("stage", "other")
            pain_by_stage.setdefault(s, []).append(pp)

        opt_by_stage = {}
        for opt in optimisations:
            s = opt.get("stage", "other")
            opt_by_stage.setdefault(s, []).append(opt)

        for proc in processes:
            stage_key = proc.get("stage", "")
            stage_name = proc.get("name", stage_labels.get(stage_key, stage_key))
            desc = proc.get("description", "")
            steps = proc.get("steps", [])
            stage_pains = pain_by_stage.get(stage_key, [])
            stage_opts = opt_by_stage.get(stage_key, [])

            lines.append(f"### {stage_name}")
            if desc:
                lines.append(f"*{desc}*")
            lines.append("")
            lines.append(f"**{len(steps)} steps** | **{len(stage_pains)} pain points** | **{len(stage_opts)} optimisation opportunities**")
            lines.append("")

            # Document key steps (not pain/opt type steps — those come after)
            regular_steps = [s for s in steps if s.get("type") not in ("pain", "optimisation")]
            if regular_steps:
                lines.append("**Current Process Flow:**")
                lines.append("")
                for i, step in enumerate(regular_steps, 1):
                    sdesc = step.get("description", "")
                    owner = step.get("owner", "")
                    duration = step.get("duration_minutes")
                    freq = step.get("frequency", "")
                    stype = step.get("type", "step")
                    quote = step.get("source_quote", "")

                    prefix = f"{i}."
                    if stype == "decision":
                        prefix = f"{i}. **Decision:**"
                    elif stype == "parallel_group":
                        prefix = f"{i}. **Parallel:**"

                    detail_parts = []
                    if owner:
                        detail_parts.append(f"Owner: {owner}")
                    if duration:
                        detail_parts.append(f"{duration} min")
                    if freq:
                        detail_parts.append(freq)
                    detail_str = f" ({', '.join(detail_parts)})" if detail_parts else ""

                    lines.append(f"{prefix} {sdesc}{detail_str}")

                    if quote:
                        lines.append(f'   > "{quote}"')

                    # Sub-items for parallel groups
                    sub_items = step.get("items", [])
                    if sub_items:
                        for item in sub_items:
                            item_desc = item.get("description", item.get("label", ""))
                            item_quote = item.get("quote", "")
                            if item_desc:
                                lines.append(f"   - {item_desc}")
                            if item_quote:
                                lines.append(f'     > "{item_quote}"')
                lines.append("")

            # Pain points for this stage — full detail
            if stage_pains:
                lines.append("**Pain Points Identified:**")
                lines.append("")
                for pp in stage_pains:
                    desc = pp.get("description", "")
                    quote = pp.get("quote", "")
                    speaker = pp.get("speaker", "")
                    conf = pp.get("confidence", "")
                    lines.append(f"- **{desc}** [{conf}]")
                    if quote:
                        attribution = f" — {speaker}" if speaker else ""
                        lines.append(f'  > "{quote}"{attribution}')
                lines.append("")

            # Optimisations for this stage
            if stage_opts:
                lines.append("**Optimisation Opportunities:**")
                lines.append("")
                for opt in stage_opts:
                    desc = opt.get("description", "")
                    quote = opt.get("quote", "")
                    speaker = opt.get("speaker", "")
                    lines.append(f"- {desc}")
                    if quote:
                        attribution = f" — {speaker}" if speaker else ""
                        lines.append(f'  > "{quote}"{attribution}')
                lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # DECISION NODES
    # ═══════════════════════════════════════════════════════════════════════════
    if decision_nodes:
        lines.append("## Key Decision Points")
        lines.append("")
        lines.append("Critical business logic decision points identified during the audit:")
        lines.append("")
        for dn in decision_nodes:
            condition = dn.get("condition", "")
            yes_path = dn.get("yes_path", "")
            no_path = dn.get("no_path", "")
            owner = dn.get("owner", "")
            stage = dn.get("stage", "")
            quote = dn.get("quote", "")
            lines.append(f"### {condition}")
            if owner:
                lines.append(f"**Owner:** {owner} | **Stage:** {stage_labels.get(stage, stage)}")
            lines.append(f"- **Yes →** {yes_path}")
            lines.append(f"- **No →** {no_path}")
            if quote:
                lines.append(f'> "{quote}"')
            lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # WASTE ANALYSIS (full detail with quotes)
    # ═══════════════════════════════════════════════════════════════════════════
    if qualified_waste:
        lines.append("## Waste Analysis")
        lines.append("")
        lines.append(
            f"We identified {fmt_aud(total_annual_waste)}/year in operational waste across {len(qualified_waste)} areas, "
            f"representing {total_weekly_hours:.1f} hours per week of lost productivity."
        )
        lines.append("")

        # Summary by type
        by_type = {}
        for w in qualified_waste:
            wtype = w.get("waste_type", "other")
            by_type.setdefault(wtype, []).append(w)

        lines.append("### Waste by Category")
        lines.append("")
        lines.append("| Category | Annual Cost | % of Total |")
        lines.append("|----------|-----------|-----------|")
        for wtype, items in sorted(by_type.items(), key=lambda x: sum(w.get("annual_waste_aud", 0) or 0 for w in x[1]), reverse=True):
            type_total = sum(w.get("annual_waste_aud", 0) or 0 for w in items)
            pct = (type_total / total_annual_waste * 100) if total_annual_waste else 0
            lines.append(f"| {waste_type_labels.get(wtype, wtype.replace('_', ' ').title())} | {fmt_aud(type_total)} | {pct:.0f}% |")
        lines.append(f"| **Total** | **{fmt_aud(total_annual_waste)}** | **100%** |")
        lines.append("")

        # Detailed breakdown per waste item
        lines.append("### Detailed Waste Breakdown")
        lines.append("")
        for w in sorted(qualified_waste, key=lambda x: x.get("annual_waste_aud", 0) or 0, reverse=True):
            desc = w.get("description", w.get("activity", ""))
            activity = w.get("activity", "")
            annual = w.get("annual_waste_aud", 0) or 0
            monthly = w.get("monthly_waste_aud", 0) or 0
            hrs = w.get("hours_per_week", 0) or 0
            rate = w.get("hourly_rate_aud", 0) or 0
            conf = w.get("confidence", "")
            wtype = w.get("waste_type", "")
            quote = w.get("quote", "")
            stage = w.get("stage", "")

            lines.append(f"**{desc}**")
            lines.append("")
            lines.append(f"- **Annual cost:** {fmt_aud(annual)} ({fmt_aud(monthly)}/month)")
            if hrs:
                lines.append(f"- **Time consumed:** {hrs:.1f} hours/week")
            lines.append(f"- **Category:** {waste_type_labels.get(wtype, wtype)} | **Stage:** {stage_labels.get(stage, stage)} | **Confidence:** {conf}")
            if rate:
                lines.append(f"- **Hourly rate used:** ${rate}/hr")
            if quote:
                lines.append(f'> "{quote}"')
            lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # PROPOSED SOLUTIONS (full detail with modal content)
    # ═══════════════════════════════════════════════════════════════════════════
    if proposed_changes:
        lines.append("## Proposed Solutions")
        lines.append("")
        lines.append(
            f"Based on the audit findings, we recommend {len(proposed_changes)} automation and process changes "
            f"with a combined annual value of **{fmt_aud(total_annual_value)}**. Each change is detailed below "
            f"with the problem it solves, what we'll build, how it works, and the financial impact."
        )
        lines.append("")

        # Summary table first
        lines.append("### Solutions Overview")
        lines.append("")
        lines.append("| # | Change | Type | Annual Value | Timeline | Phase |")
        lines.append("|---|--------|------|-------------|----------|-------|")
        for c in proposed_changes:
            cid = c.get("change_id", "")
            title = c.get("title", "")
            ctype = c.get("change_type", "").title()
            value = (c.get("value") or {}).get("combined_annual_value_aud", 0) or 0
            weeks = (c.get("implementation") or {}).get("weeks_label", "")
            phase = c.get("phase_label", f"Phase {c.get('phase', '')}")
            if len(title) > 50:
                title = title[:47] + "..."
            lines.append(f"| {cid} | {title} | {ctype} | {fmt_aud(value)} | {weeks} | {phase} |")
        lines.append("")

        # Detailed per-change sections
        for c in proposed_changes:
            cid = c.get("change_id", "")
            title = c.get("title", "")
            ctype = c.get("change_type", "").title()
            stage = c.get("stage", "")
            conf = c.get("confidence", "")
            value_data = c.get("value") or {}
            value_total = value_data.get("combined_annual_value_aud", 0) or 0
            value_formula = value_data.get("formula_summary", "")
            impl = c.get("implementation") or {}
            weeks_label = impl.get("weeks_label", "")
            dev_hours = impl.get("dev_hours", "")
            pm_hours = impl.get("pm_hours", "")
            modal = c.get("modal_content") or {}
            phase_label = c.get("phase_label", "")
            proposed_solution = c.get("proposed_solution", "")
            future_desc = c.get("future_step_description", "")
            future_owner = c.get("future_step_owner", "")

            lines.append(f"### {cid}: {title}")
            lines.append("")
            lines.append(f"**Type:** {ctype} | **Stage:** {stage_labels.get(stage, stage)} | **Phase:** {phase_label} | **Confidence:** {conf}")
            lines.append(f"**Annual Value:** {fmt_aud(value_total)} | **Timeline:** {weeks_label}")
            if dev_hours:
                lines.append(f"**Effort:** {dev_hours} dev hours" + (f", {pm_hours} PM hours" if pm_hours else ""))
            lines.append("")

            # Modal content — the rich narrative
            what_task = modal.get("what_is_the_task", "")
            what_build = modal.get("what_we_will_build", "")
            how_works = modal.get("how_it_works", "")
            how_saves = modal.get("how_it_saves_money", "")
            how_quick = modal.get("how_quick", "")

            if what_task:
                lines.append("**The Problem:**")
                lines.append(what_task)
                lines.append("")

            if what_build:
                lines.append("**What We'll Build:**")
                lines.append(what_build)
                lines.append("")

            if how_works:
                lines.append("**How It Works:**")
                lines.append(how_works)
                lines.append("")

            if how_saves:
                lines.append("**Financial Impact:**")
                lines.append(how_saves)
                lines.append("")
                if value_formula:
                    lines.append(f"*Calculation: {value_formula}*")
                    lines.append("")

            if how_quick:
                lines.append("**Implementation Timeline:**")
                lines.append(how_quick)
                lines.append("")

            if future_desc:
                lines.append("**Future State:**")
                lines.append(future_desc)
                if future_owner:
                    lines.append(f"*Managed by: {future_owner}*")
                lines.append("")

            # Research summary
            research = c.get("research") or {}
            tools_researched = research.get("tools_researched", [])
            feasibility = research.get("feasibility_notes", "")

            if feasibility:
                lines.append(f"**Feasibility:** {feasibility}")
                lines.append("")

            if tools_researched:
                lines.append("**Tools Researched:**")
                lines.append("")
                for tr in tools_researched:
                    tname = tr.get("tool_name", tr.get("name", ""))
                    tier = tr.get("realistic_tier", "")
                    cost = tr.get("realistic_annual_cost_aud")
                    setup = tr.get("setup_cost_aud")
                    pricing = tr.get("pricing_summary", "")
                    integration = tr.get("integration_with_existing", "")
                    pros = tr.get("pros", [])
                    cons = tr.get("cons", [])

                    lines.append(f"**{tname}**" + (f" — {tier}" if tier else ""))
                    if pricing:
                        lines.append(f"Pricing: {pricing}")
                    if cost is not None:
                        lines.append(f"Annual cost: {fmt_aud(cost)}" + (f" | Setup: {fmt_aud(setup)}" if setup else ""))
                    if integration:
                        lines.append(f"Integration: {integration}")
                    if pros:
                        lines.append("Pros: " + "; ".join(pros[:5]))
                    if cons:
                        lines.append("Cons: " + "; ".join(cons[:5]))
                    lines.append("")

            # ROI item
            roi = roi_by_change.get(cid)
            if roi:
                payback = roi.get("payback_months")
                payback_tag = roi.get("payback_tag", "")
                build_cost = roi.get("build_cost_aud")
                roi_quote = roi.get("quote", "")
                if payback is not None:
                    lines.append(f"**ROI:** Payback in {payback:.1f} months" + (f" ({payback_tag})" if payback_tag else ""))
                if build_cost:
                    lines.append(f"**Build cost:** {fmt_aud(build_cost)}")
                if roi_quote:
                    lines.append(f'> "{roi_quote}"')
                lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # STRATEGIC APPROACH (full detail with tool rationale)
    # ═══════════════════════════════════════════════════════════════════════════
    sa = data.get("strategic_approaches", {})
    strategies = sa.get("strategies", [])
    if strategies:
        lines.append("## Strategic Approach")
        lines.append("")

        for strat in strategies:
            name = strat.get("name", "")
            desc = strat.get("description", "")
            best_for = strat.get("best_for", "")
            how_works = strat.get("how_it_works", "")
            cost_summary = strat.get("cost_summary", {})
            coverage = strat.get("coverage", {})
            integration = strat.get("integration_analysis", {})
            limitations = strat.get("limitations", [])

            lines.append(f"### {name}")
            lines.append("")
            if desc:
                lines.append(desc)
                lines.append("")
            if best_for:
                lines.append(f"**Best for:** {best_for}")
                lines.append("")
            if how_works:
                lines.append(f"**How it works:** {how_works}")
                lines.append("")

            # Cost summary
            if cost_summary:
                lines.append("**Cost Summary:**")
                lines.append("")
                impl_weeks = cost_summary.get("implementation_weeks", "")
                ongoing_current = cost_summary.get("ongoing_annual_current_aud", 0) or 0
                ongoing_scaled = cost_summary.get("ongoing_annual_scaled_aud", 0) or 0
                hidden = cost_summary.get("hidden_costs_annual_aud", 0) or 0
                setup = cost_summary.get("total_setup_cost_aud", 0) or 0
                consultant = cost_summary.get("total_consultant_fees_aud", 0) or 0
                lines.append(f"| Metric | Value |")
                lines.append(f"|--------|-------|")
                lines.append(f"| Implementation time | {impl_weeks} weeks |")
                lines.append(f"| Setup cost | {fmt_aud(setup)} |")
                if consultant:
                    lines.append(f"| Consultant fees | {fmt_aud(consultant)} |")
                lines.append(f"| Ongoing annual (current size) | {fmt_aud(ongoing_current)} |")
                if ongoing_scaled and ongoing_scaled != ongoing_current:
                    lines.append(f"| Ongoing annual (scaled to 100 staff) | {fmt_aud(ongoing_scaled)} |")
                if hidden:
                    lines.append(f"| Hidden costs | {fmt_aud(hidden)}/yr |")
                lines.append("")

            if coverage:
                cov_pct = coverage.get("coverage_percentage", 0) or 0
                cov_val = coverage.get("covered_value_aud", 0) or 0
                uncov_val = coverage.get("uncovered_value_aud", 0) or 0
                lines.append(f"**Coverage:** {cov_pct:.0f}% of changes covered ({fmt_aud(cov_val)}/yr value)")
                if uncov_val:
                    lines.append(f"Uncovered value: {fmt_aud(uncov_val)}/yr")
                lines.append("")

            if integration:
                handoffs = integration.get("manual_handoffs", 0)
                logins = integration.get("separate_logins", 0)
                silos = integration.get("data_silos", 0)
                cohesion = integration.get("cohesion_assessment", "")
                int_cost = integration.get("integration_development_cost_aud", 0) or 0
                if cohesion:
                    lines.append("**Integration Analysis:**")
                    lines.append("")
                    lines.append(f"{cohesion}")
                    lines.append("")
                    if handoffs or logins or silos:
                        lines.append(f"- Manual handoffs: {handoffs}")
                        lines.append(f"- Separate logins: {logins}")
                        lines.append(f"- Data silos: {silos}")
                    if int_cost:
                        lines.append(f"- Integration development cost: {fmt_aud(int_cost)}")
                    lines.append("")

            # Tool selections with full rationale
            tool_selections = strat.get("tool_selections", [])
            if tool_selections:
                lines.append("### Recommended Tools — Detailed Selection")
                lines.append("")
                for ts in tool_selections:
                    title = ts.get("title", "")
                    tool = ts.get("selected_tool", "")
                    rationale = ts.get("rationale", "")
                    why_tool = ts.get("why_this_tool", "")
                    int_notes = ts.get("integration_notes", "")
                    annual_cost = ts.get("annual_cost_aud", 0) or 0
                    setup_cost = ts.get("setup_cost_aud", 0) or 0
                    weeks = ts.get("weeks_estimate", "")
                    annual_value = ts.get("annual_value_aud", 0) or 0
                    tier = ts.get("tier_selected", "")
                    config_steps = ts.get("configuration_steps", [])
                    caveats = ts.get("caveats", [])
                    free_limits = ts.get("free_plan_limitations", [])

                    lines.append(f"**{title}** → {tool}")
                    lines.append("")
                    if tier:
                        lines.append(f"Tier: {tier} | Cost: {fmt_aud(annual_cost)}/yr | Setup: {fmt_aud(setup_cost)} | Value: {fmt_aud(annual_value)}/yr")
                    if why_tool:
                        lines.append(f"Why this tool: {why_tool}")
                    elif rationale:
                        lines.append(f"Rationale: {rationale}")
                    if int_notes:
                        lines.append(f"Integration: {int_notes}")

                    if config_steps:
                        lines.append("Configuration steps:")
                        for i, step in enumerate(config_steps, 1):
                            lines.append(f"  {i}. {step}")

                    if caveats:
                        lines.append("Caveats: " + "; ".join(caveats))
                    if free_limits:
                        lines.append("Free plan limitations: " + "; ".join(free_limits))
                    lines.append("")

            if limitations:
                lines.append("### Key Considerations & Risks")
                lines.append("")
                for lim in limitations:
                    lines.append(f"- {lim}")
                lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # TRANSFORMATION ROADMAP (full detail with future state)
    # ═══════════════════════════════════════════════════════════════════════════
    blueprint = data.get("transformation_blueprint", {})
    bp_phases = blueprint.get("phases", [])
    if bp_phases:
        total_effort = blueprint.get("estimated_total_weeks_effort", 0)
        total_duration = blueprint.get("estimated_total_duration_weeks", 0)
        steps_current = blueprint.get("total_steps_current", 0)
        steps_future = blueprint.get("total_steps_future", 0)
        steps_eliminated = blueprint.get("steps_eliminated", 0)
        steps_consolidated = blueprint.get("steps_consolidated", 0)

        lines.append("## Transformation Roadmap")
        lines.append("")
        lines.append(
            f"A {len(bp_phases)}-phase implementation plan spanning {total_duration} weeks "
            f"({total_effort:.0f} weeks development effort), delivering {fmt_aud(total_annual_value)}/year in value."
        )
        lines.append("")
        if steps_current and steps_future:
            lines.append(
                f"Process transformation: {steps_current} current steps → {steps_future} future steps "
                f"({steps_eliminated} eliminated, {steps_consolidated} consolidated)."
            )
            lines.append("")

        for phase in bp_phases:
            pnum = phase.get("phase_number", "")
            plabel = phase.get("label", f"Phase {pnum}")
            timeframe = phase.get("timeframe", "")
            pdesc = phase.get("description", "")
            phase_value = phase.get("total_annual_value_aud", 0) or 0
            phase_effort = phase.get("total_weeks_effort", 0) or 0
            phase_duration = phase.get("effective_duration_weeks", 0) or 0
            change_ids = phase.get("change_ids", [])

            lines.append(f"### Phase {pnum}: {plabel}")
            lines.append(f"**{timeframe}** | Value: {fmt_aud(phase_value)}/year | Effort: {phase_effort:.0f} weeks | Duration: {phase_duration} weeks")
            lines.append("")
            if pdesc:
                lines.append(pdesc)
                lines.append("")

            for cid in change_ids:
                c = changes_by_id.get(cid)
                if c:
                    title = c.get("title", "")
                    value = (c.get("value") or {}).get("combined_annual_value_aud", 0) or 0
                    weeks = (c.get("implementation") or {}).get("weeks_label", "")
                    deps = c.get("depends_on", [])
                    dep_str = f" (depends on: {', '.join(deps)})" if deps else ""
                    lines.append(f"- **{title}** — {fmt_aud(value)}/yr, {weeks}{dep_str}")
            lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # ROI SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    if roi_items:
        lines.append("## Return on Investment Summary")
        lines.append("")
        quick_wins_roi = [r for r in roi_items if r.get("payback_tag") == "QUICK_WIN"]
        lines.append(f"**{len(quick_wins_roi)} quick-win ROI items** (payback under 3 months)")
        lines.append("")

        lines.append("| Change | Annual Saving | Build Cost | Payback | Tag |")
        lines.append("|--------|-------------|-----------|---------|-----|")
        for r in sorted(roi_items, key=lambda x: x.get("annual_saving_aud", 0) or 0, reverse=True):
            activity = r.get("activity", "")
            saving = r.get("annual_saving_aud", 0) or 0
            build = r.get("build_cost_aud", 0) or 0
            payback = r.get("payback_months")
            tag = r.get("payback_tag", "")
            if len(activity) > 45:
                activity = activity[:42] + "..."
            payback_str = f"{payback:.1f} months" if payback is not None else "—"
            lines.append(f"| {activity} | {fmt_aud(saving)} | {fmt_aud(build)} | {payback_str} | {tag} |")
        lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # POSITIVE SIGNALS
    # ═══════════════════════════════════════════════════════════════════════════
    if positive_signals:
        lines.append("## Client Engagement & Readiness")
        lines.append("")
        for sig in positive_signals:
            if isinstance(sig, dict):
                desc = sig.get("description", sig.get("signal", ""))
                quote = sig.get("quote", "")
                lines.append(f"- **{desc}**")
                if quote:
                    lines.append(f'  > "{quote}"')
            elif isinstance(sig, str):
                lines.append(f"- {sig}")
        lines.append("")

    # ═══════════════════════════════════════════════════════════════════════════
    # NEXT STEPS
    # ═══════════════════════════════════════════════════════════════════════════
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. **Review this report** — Understand the full scope of findings, waste, and proposed solutions")
    lines.append("2. **Explore the interactive portal** — Visit your client portal to interact with the priority matrix and detailed process maps")
    lines.append("3. **Select your implementation approach** — Choose between the recommended SaaS toolkit or a custom platform build")
    lines.append("4. **Scope of Work** — {YOUR_COMPANY} will prepare a detailed scope of work, timeline, and fixed-price quote for your chosen approach")
    lines.append("5. **Phase 1 kick-off** — Quick wins can begin immediately with minimal disruption to current operations")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**{YOUR_COMPANY}**")
    lines.append("{YOUR_EMAIL} | {YOUR_DOMAIN}")
    lines.append("")
    lines.append(f"*This report was generated from {sessions_completed} audit sessions conducted between "
                  f"{start_display} and {today}. All findings are supported by direct quotes from session transcripts "
                  f"and verified with the {company} team.*")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract audit data into markdown for Gamma report generation")
    parser.add_argument("--client-slug", required=True, help="Client slug (e.g. dale-great-supports)")
    parser.add_argument("--project-root", default=None, help="Project root directory (auto-detected if omitted)")
    args = parser.parse_args()

    if args.project_root:
        root = Path(args.project_root)
    else:
        root = Path(__file__).resolve().parent
        for _ in range(10):
            if (root / "clients").is_dir():
                break
            root = root.parent
        else:
            print("ERROR: Could not find project root (no clients/ directory found)", file=sys.stderr)
            sys.exit(1)

    audit_path = root / "clients" / args.client_slug / "audit" / "audit-data.json"
    if not audit_path.exists():
        print(f"ERROR: No audit data found at {audit_path}", file=sys.stderr)
        sys.exit(1)

    with open(audit_path) as f:
        data = json.load(f)

    markdown = extract(data)
    print(markdown)


if __name__ == "__main__":
    main()
