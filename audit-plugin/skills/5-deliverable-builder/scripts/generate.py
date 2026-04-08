#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
generate.py — HTML deliverable generator.

Reads clients/{slug}/audit/audit-data.json and generates:
  - process-map.html    — HTML/CSS zone-based current-state process map
  - findings.html       — "What We Discussed" session summary with pain points and optimisations
  - waste.html          — "Total Waste Identified" cost/time breakdown
  - transformation-blueprint.html — Side-by-side current vs future process map (separate target, not in 'all')
  - audit-report.html   — Full audit report with ROI model and priority matrix
  - client-website.html  — Client-facing site with progressive session unlock

Usage:
  python3 generate.py --client-slug {slug} --output process-map|findings|waste|transformation-blueprint|priority-matrix|audit-report|audit-report-print|client-website|all

  --output all generates: process-map, findings, waste, client-website
  (transformation-blueprint and priority-matrix require proposed_changes[] from the process analyst agent)

Output files written to: clients/{slug}/deliverables/
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from html import escape


# ─── Design tokens ────────────────────────────────────────────────────────────

COMPANY_LOGO_URL = "{YOUR_LOGO_URL}"
BRAND_FAVICON = f'<link rel="icon" type="image/png" href="{COMPANY_LOGO_URL}">'
COMPANY_NAME = "{YOUR_COMPANY}"
COMPANY_ADDRESS = "{YOUR_ADDRESS}"
COMPANY_EMAIL = "{YOUR_EMAIL}"
COMPANY_WEBSITE = "{YOUR_DOMAIN}"

BRAND_PRIMARY = "#7DFF00"
BRAND_PRIMARY_TEXT = "#166534"   # dark green for text — 7.1:1 contrast on white
BRAND_DARK = "#0f1825"
BRAND_GREY = "#64748b"
BRAND_LIGHT = "#f7f9fc"
BRAND_WHITE = "#ffffff"
BRAND_BORDER = "#e2e8f0"
STEP_COLORS = {
    "step": "#f7f9fc",
    "decision": "#fffbeb",
    "pain": "#fef2f2",
    "optimisation": "#f0fdf4",
    "automation": "#eff6ff",
}
STEP_BORDERS = {
    "step": "#e2e8f0",
    "decision": "#fcd34d",
    "pain": "#fca5a5",
    "optimisation": "#86efac",
    "automation": "#93c5fd",
}
STAGE_ACCENT_DEFAULT = "#7DFF00"


def _build_stage_lookups(ssad: dict) -> tuple:
    """Build stage label and subtitle dicts from audit data processes[].name/description."""
    labels = {}
    subtitles = {}
    for proc in ssad.get("processes", []):
        stage = proc["stage"]
        labels[stage] = proc.get("name") or stage.replace("_", " ").title()
        if proc.get("description"):
            subtitles[stage] = proc["description"]
    return labels, subtitles


def _stage_label(stage: str, labels: dict) -> str:
    """Look up a stage display name, falling back to title-cased key."""
    return labels.get(stage, stage.replace("_", " ").title())

# ─── Shared constants for change overlays ────────────────────────────────────

CHANGE_BADGE = {
    "automate":    ("AUTOMATED",   "#10B981", "#D1FAE5"),
    "replace":     ("REPLACED",    "#3B82F6", "#DBEAFE"),
    "eliminate":   ("ELIMINATED",  "#EF4444", "#FEE2E2"),
    "consolidate": ("CONSOLIDATED","#8B5CF6", "#EDE9FE"),
}

VALUE_TYPE_COLOR = {
    "time_saving": "#10B981",
    "productivity_enhancement": "#3B82F6",
    "both": "#8B5CF6",
}




def _stat_box(value: str, label: str) -> str:
    """Render a single stat box."""
    return f"""<div class="stat-box">
               <div class="stat-val">{value}</div>
               <div class="stat-label">{label}</div>
               </div>"""


def _render_current_step_simple(step: dict, changes: list) -> str:
    """Render a step card for the current-state process map."""
    stype = step.get("type", "step")
    desc = escape(step.get("description", ""))
    is_changed = bool(changes)
    opacity_style = "opacity:0.5;" if is_changed else ""
    bg = STEP_COLORS.get(stype, "#fff")
    border = STEP_BORDERS.get(stype, "#E5E7EB")
    return f"""<div style="background:{bg};border:1.5px solid {border};border-radius:8px;
               padding:10px 12px;margin-bottom:6px;font-size:12px;{opacity_style}">
               {desc}</div>"""


def _render_proposed_step_simple(step: dict, changes: list) -> str:
    """Render a step card for the proposed-state process map with change overlays."""
    desc = escape(step.get("description", ""))
    if not changes:
        return f"""<div style="background:#F9FAFB;border:1.5px solid #E5E7EB;border-radius:8px;
                   padding:10px 12px;margin-bottom:6px;font-size:12px;opacity:0.55;">
                   {desc}</div>"""
    ch = changes[0]
    ctype = ch.get("change_type", "automate")
    badge_label, border_color, bg_color = CHANGE_BADGE.get(ctype, ("CHANGED", "#6B7280", "#F3F4F6"))
    tools = ch.get("proposed_tools", [])
    tool_html = ""
    if tools:
        pills = "".join(f'<span style="background:#E0F2FE;color:#0369A1;border-radius:4px;padding:1px 6px;font-size:10px;margin-right:3px">{escape(t)}</span>' for t in tools)
        tool_html = f'<div style="margin-top:5px">{pills}</div>'
    merged_desc = ch.get("proposed_step_description", "")
    display_desc = escape(merged_desc) if merged_desc else desc
    eliminate_style = "opacity:0.35;text-decoration:line-through;" if ctype == "eliminate" else ""
    return f"""<div style="background:{bg_color};border:2px solid {border_color};border-radius:8px;
               padding:10px 12px;margin-bottom:6px;font-size:12px;{eliminate_style}position:relative">
               <span style="position:absolute;top:6px;right:8px;background:{border_color};color:#fff;
                 font-size:9px;font-weight:700;padding:1px 5px;border-radius:3px">{badge_label}</span>
               <div style="padding-right:90px">{display_desc}</div>
               {tool_html}
               </div>"""


def _build_change_lookup(proposed_changes: list) -> dict:
    """Build step_id → list of change dicts lookup."""
    change_by_step: dict = {}
    for ch in proposed_changes:
        for sid in ch.get("affected_step_ids", []):
            change_by_step.setdefault(sid, []).append(ch)
    return change_by_step


def _render_side_by_side_maps(processes: list, change_by_step: dict) -> str:
    """Render side-by-side current vs proposed process map zones."""
    zones_html = ""
    for proc in processes:
        stage = proc.get("stage", "")
        stage_label = proc.get("name") or stage.replace("_", " ").title()
        accent = STAGE_ACCENT_DEFAULT
        steps = [s for s in proc.get("steps", []) if not s.get("branch_only", False)]
        if not steps:
            continue
        current_col = ""
        proposed_col = ""
        for step in steps:
            sid = step.get("step_id", "")
            changes = change_by_step.get(sid, [])
            current_col += _render_current_step_simple(step, changes)
            proposed_col += _render_proposed_step_simple(step, changes)
        zones_html += f"""
        <div style="margin-bottom:32px">
          <div style="border-left:4px solid {accent};padding-left:12px;margin-bottom:12px">
            <span style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{accent}">{escape(stage_label)}</span>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
            <div>
              <div style="font-size:11px;font-weight:600;text-transform:uppercase;color:{BRAND_GREY};margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #E5E7EB">Current State</div>
              {current_col}
            </div>
            <div>
              <div style="font-size:11px;font-weight:600;text-transform:uppercase;color:{BRAND_GREY};margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #E5E7EB">Proposed State</div>
              {proposed_col}
            </div>
          </div>
        </div>"""
    return zones_html or f'<p style="color:{BRAND_GREY};font-style:italic">No process data available.</p>'


def _value_color(value: float, sorted_values: list) -> str:
    """Return a color based on where value falls in the distribution."""
    n = len(sorted_values)
    if n == 0:
        return "#94A3B8"
    rank = sum(1 for v in sorted_values if v <= value)
    pct = rank / n
    if pct >= 0.8:
        return "#059669"   # top tier – deep green
    elif pct >= 0.5:
        return "#10B981"   # mid-high – green
    elif pct >= 0.2:
        return "#F59E0B"   # mid-low – amber
    else:
        return "#94A3B8"   # low – slate


def _render_priority_chart(ssad: dict) -> tuple:
    """Build the priority matrix chart HTML.

    Returns (scatter_html, modals_html, has_interactive).
    scatter_html contains the bubble chart (interactive or SVG fallback) plus tooltip div.
    modals_html contains the modal backdrop divs for each enriched change.
    """
    import math

    proposed_changes = ssad.get("proposed_changes", [])
    roi_items = ssad.get("roi_items", [])

    has_interactive = any(c.get("modal_content") and c.get("value") for c in proposed_changes)

    scatter_html = ""
    modals_html = ""

    if has_interactive:
        # ── Interactive CSS div chart (analyst-enriched data) ──
        enriched = [c for c in proposed_changes if c.get("value", {}).get("combined_annual_value_aud") is not None
                    and c.get("implementation", {}).get("weeks_estimate") is not None]

        if enriched:
            # ── Group by process area (stage) ──
            roi_tier_lookup = {r.get("linked_change_id", ""): r.get("suggested_tier", "standard") for r in roi_items}
            processes = ssad.get("processes", [])
            stage_labels = {p["stage"]: p["name"] for p in processes}

            stage_groups = {}
            for c in enriched:
                stage = c.get("stage", "other")
                stage_groups.setdefault(stage, []).append(c)

            _TIER_COLOR = {"quick_win": "#ea580c", "micro": "#ea580c", "standard": "#2563eb", "complex": "#2563eb", "sprint": "#16a34a"}

            def _effective_tier(c, roi_tier_lookup):
                """Return effective tier: quick_win if qualified, else from ROI suggested_tier."""
                qwp = c.get("quick_win_plan", {})
                if qwp.get("qualified") is True:
                    return "quick_win"
                return roi_tier_lookup.get(c.get("change_id", ""), "standard")

            grouped_bubbles = []
            for stage, items in stage_groups.items():
                group_val = sum(c["value"]["combined_annual_value_aud"] for c in items)
                group_weeks = max(c["implementation"]["weeks_estimate"] for c in items)
                group_label = stage_labels.get(stage, stage.replace("_", " ").title())
                group_id = f"GRP-{stage}"

                # Determine dominant tier (quick_win_plan.qualified overrides suggested_tier)
                tiers = [_effective_tier(c, roi_tier_lookup) for c in items]
                tier_counts = {}
                for t in tiers:
                    tier_counts[t] = tier_counts.get(t, 0) + 1
                if "sprint" in tier_counts:
                    dominant_tier = "sprint"
                else:
                    dominant_tier = max(tier_counts, key=tier_counts.get)
                color = _TIER_COLOR.get(dominant_tier, "#2563eb")

                # Weeks label
                if group_weeks < 1:
                    wlabel = "< 1 week"
                elif group_weeks <= 1:
                    wlabel = "~1 week"
                else:
                    wlabel = f"~{group_weeks:.0f} weeks"

                grouped_bubbles.append({
                    "group_id": group_id, "stage": stage, "label": group_label,
                    "annual_val": group_val, "weeks": group_weeks, "wlabel": wlabel,
                    "color": color, "dominant_tier": dominant_tier, "items": items,
                })

            weeks_vals = [g["weeks"] for g in grouped_bubbles]
            value_vals = [g["annual_val"] for g in grouped_bubbles]
            sorted_vals = sorted(value_vals)
            max_val = max(value_vals)

            x_max_weeks = max(max(weeks_vals) * 1.2, 5)
            y_max_value = max(max_val * 1.15, 5000)

            CHART_W, CHART_H = 700, 420

            low_week_ratio = sum(1 for w in weeks_vals if w <= 1) / len(weeks_vals)
            use_sqrt_x = low_week_ratio > 0.6

            def x_pos(weeks):
                if use_sqrt_x:
                    return min(math.sqrt(weeks / x_max_weeks) * 100, 98)
                return min((weeks / x_max_weeks) * 100, 98)

            # ── Phase 1: Compute all bubble positions ──
            bubble_data = []
            for g in grouped_bubbles:
                cid = g["group_id"]
                title = g["label"]
                weeks = g["weeks"]
                annual_val = g["annual_val"]
                color = g["color"]
                wlabel = g["wlabel"]

                bx = x_pos(weeks)
                by = max(100 - (annual_val / y_max_value) * 100, 2)
                size = max(32, min(100, 32 + math.sqrt(annual_val / max_val) * 68))
                font_size = 11 if size >= 60 else (9 if size >= 40 else 8)
                val_label = f"${annual_val/1000:.0f}k"

                bubble_data.append({
                    "c": None, "cid": cid, "title": title, "weeks": weeks,
                    "annual_val": annual_val, "vtype": "both", "color": color,
                    "wlabel": wlabel, "source": "", "dominant_tier": g["dominant_tier"],
                    "x": bx, "y": by, "size": size,
                    "font_size": font_size, "val_label": val_label,
                    "items": g["items"],
                })

            # ── Phase 2: Anti-overlap collision pass ──
            for i in range(len(bubble_data)):
                for j in range(i):
                    bi, bj = bubble_data[i], bubble_data[j]
                    dx = (bi["x"] - bj["x"]) / 100 * CHART_W
                    dy = (bi["y"] - bj["y"]) / 100 * CHART_H
                    min_dist = (bi["size"] + bj["size"]) / 2 + 4
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < min_dist and dist > 0:
                        push = (min_dist - dist) / 2
                        angle = math.atan2(dy, dx)
                        bi["x"] = max(1, min(98, bi["x"] + math.cos(angle) * push / CHART_W * 100))
                        bi["y"] = max(1, min(98, bi["y"] + math.sin(angle) * push / CHART_H * 100))
                        bj["x"] = max(1, min(98, bj["x"] - math.cos(angle) * push / CHART_W * 100))
                        bj["y"] = max(1, min(98, bj["y"] - math.sin(angle) * push / CHART_H * 100))

            # ── Phase 3: Find top bubble for pulse animation ──
            top_cid = max(bubble_data, key=lambda b: b["annual_val"])["cid"]

            # ── Phase 4: Generate bubble HTML ──
            bubbles_divs = ""
            for b in bubble_data:
                extra_class = " pm-bubble-top" if b["cid"] == top_cid else ""
                bubbles_divs += f"""<div class="pm-bubble{extra_class}" data-id="{b['cid']}"
                  style="left:{b['x']:.1f}%;top:{b['y']:.1f}%;width:{b['size']:.0f}px;height:{b['size']:.0f}px;
                         background:{b['color']};border-color:{b['color']}"
                  onclick="openModal('{b['cid']}')"
                  onmouseenter="showTip(this,'{b['title']}','{fmt_aud(b['annual_val'])}/yr','{b['wlabel']}')"
                  onmouseleave="hideTip()">
                  <span class="pm-bubble-label" style="font-size:{b['font_size']}px">{b['val_label']}</span>
                </div>\n"""

            # ── Phase 5: Top-item annotations (top 3 by value) ──
            top_items = sorted(bubble_data, key=lambda b: b["annual_val"], reverse=True)[:3]
            annotations_html = ""
            for idx, b in enumerate(top_items):
                short_title = b["title"][:28] + ("..." if len(b["title"]) > 28 else "")
                label_x = b["x"] + (b["size"] / CHART_W * 100) + 1.5
                label_y = b["y"] - 1 + (idx * 3.5)
                if label_x > 72:
                    label_x = b["x"] - (b["size"] / CHART_W * 100) - 1.5
                    align = "text-align:right;transform:translateX(-100%)"
                else:
                    align = ""
                annotations_html += f"""<div style="position:absolute;left:{label_x:.1f}%;top:{label_y:.1f}%;
                    font-size:10px;font-weight:600;color:{BRAND_DARK};white-space:nowrap;pointer-events:none;z-index:5;{align}">
                    {short_title} <span style="color:#059669;font-weight:800">{b['val_label']}/yr</span>
                </div>\n"""

            # Build grouped modals — each modal lists the sub-items in that process area
            _TIER_LABELS = {"micro": "Quick Win", "standard": "SaaS Toolkit", "complex": "SaaS Toolkit", "sprint": "Custom Platform"}
            _TIER_BADGE_COLORS = {"micro": "#ea580c", "standard": "#2563eb", "complex": "#2563eb", "sprint": "#16a34a"}

            for b in bubble_data:
                cid = b["cid"]
                title = b["title"]
                annual_val = b["annual_val"]
                wlabel = b["wlabel"]
                items = b.get("items", [])
                dominant_tier = b.get("dominant_tier", "standard")
                tier_label = _TIER_LABELS.get(dominant_tier, "SaaS Toolkit")
                tier_color = _TIER_BADGE_COLORS.get(dominant_tier, "#2563eb")

                # Build sub-item list
                sub_items_html = ""
                for c in items:
                    c_title = escape(c.get("title", ""))
                    c_val = c.get("value", {}).get("combined_annual_value_aud", 0)
                    c_wlabel = escape(c.get("implementation", {}).get("weeks_label", ""))
                    c_tier = roi_tier_lookup.get(c.get("change_id", ""), "standard")
                    c_tier_label = _TIER_LABELS.get(c_tier, "SaaS Toolkit")
                    c_tier_color = _TIER_BADGE_COLORS.get(c_tier, "#2563eb")
                    c_type = escape(c.get("change_type", ""))

                    mc = c.get("modal_content", {})
                    c_desc = escape(mc.get("what_we_will_build", mc.get("what_is_the_task", "")))

                    sub_items_html += f"""<div style="padding:12px 0;border-bottom:1px solid #F1F5F9">
                      <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:4px">
                        <div style="font-size:14px;font-weight:600;color:{BRAND_DARK}">{c_title}</div>
                        <div style="font-size:14px;font-weight:700;color:#059669;white-space:nowrap;margin-left:12px">{fmt_aud(c_val)}/yr</div>
                      </div>
                      <div style="display:flex;gap:6px;margin-bottom:6px">
                        <span style="background:{c_tier_color};color:#fff;border-radius:4px;padding:1px 8px;font-size:10px;font-weight:600">{c_tier_label}</span>
                        <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px;text-transform:uppercase">{c_type}</span>
                        <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px">{c_wlabel}</span>
                      </div>
                      <div style="font-size:13px;color:#64748b;line-height:1.4">{c_desc}</div>
                    </div>\n"""

                modals_html += f"""<div class="pm-modal-backdrop" id="modal-{cid}" style="display:none" onclick="if(event.target===this)closeModal()">
  <div class="pm-modal">
    <button class="pm-modal-close" onclick="closeModal()">&times;</button>
    <div style="margin-bottom:16px">
      <h3 style="font-size:18px;font-weight:700;margin-bottom:8px">{title}</h3>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
        <span style="background:{tier_color};color:#fff;border-radius:4px;padding:1px 8px;font-size:10px;font-weight:600">{tier_label}</span>
        <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px">{len(items)} improvements</span>
        <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px">{wlabel}</span>
      </div>
    </div>
    <div style="margin-bottom:16px">
      {sub_items_html}
    </div>
    <div class="pm-modal-stats">
      <div><span class="pm-modal-stat-val">{fmt_aud(annual_val)}</span><span class="pm-modal-stat-lbl">Combined annual value</span></div>
      <div><span class="pm-modal-stat-val">{len(items)}</span><span class="pm-modal-stat-lbl">Improvements</span></div>
    </div>
  </div>
</div>\n"""

            # X axis ticks for weeks
            x_ticks_html = ""
            tick_values = [1, 2, 3, 4, 5, 6, 8]
            for tv in tick_values:
                if tv > x_max_weeks:
                    break
                pct = x_pos(tv)
                label = f"{tv}w"
                x_ticks_html += f'<span style="position:absolute;left:{pct:.1f}%;bottom:-20px;transform:translateX(-50%);font-size:10px;color:{BRAND_GREY}">{label}</span>\n'
                x_ticks_html += f'<span style="position:absolute;left:{pct:.1f}%;top:0;bottom:0;width:1px;background:#E5E7EB"></span>\n'

            # Y axis ticks for value
            y_ticks_html = ""
            y_tick_values = [5000, 10000, 25000, 50000, 100000, 200000]
            for yv in y_tick_values:
                if yv > y_max_value:
                    break
                pct = 100 - (yv / y_max_value) * 100
                y_ticks_html += f'<span style="position:absolute;top:{pct:.1f}%;left:-48px;transform:translateY(-50%);font-size:10px;color:{BRAND_GREY};text-align:right;width:44px">${yv//1000}k</span>\n'
                y_ticks_html += f'<span style="position:absolute;top:{pct:.1f}%;left:0;right:0;height:1px;background:#E5E7EB"></span>\n'

            # ── Quadrant zone backgrounds ──
            x_mid_pct = min(x_pos(2.0), 50)
            y_mid_pct = 50
            zones_html = f"""<div style="position:absolute;left:0;top:0;width:{x_mid_pct:.1f}%;height:{y_mid_pct}%;background:rgba(16,185,129,0.06);border-radius:8px 0 0 0">
                  <span style="position:absolute;top:8px;left:10px;font-size:10px;font-weight:600;color:#10B981;opacity:0.7;text-transform:uppercase;letter-spacing:0.05em">Quick Wins</span>
                </div>
                <div style="position:absolute;left:{x_mid_pct:.1f}%;top:0;width:{100-x_mid_pct:.1f}%;height:{y_mid_pct}%;background:rgba(245,158,11,0.05);border-radius:0 8px 0 0">
                  <span style="position:absolute;top:8px;right:10px;font-size:10px;font-weight:600;color:#F59E0B;opacity:0.7;text-transform:uppercase;letter-spacing:0.05em">Strategic Bets</span>
                </div>
                <div style="position:absolute;left:0;top:{y_mid_pct}%;width:{x_mid_pct:.1f}%;height:{100-y_mid_pct}%;background:rgba(59,130,246,0.04);border-radius:0 0 0 8px">
                  <span style="position:absolute;bottom:8px;left:10px;font-size:10px;font-weight:600;color:#3B82F6;opacity:0.7;text-transform:uppercase;letter-spacing:0.05em">Low Effort</span>
                </div>
                <div style="position:absolute;left:{x_mid_pct:.1f}%;top:{y_mid_pct}%;width:{100-x_mid_pct:.1f}%;height:{100-y_mid_pct}%;background:rgba(148,163,184,0.04);border-radius:0 0 8px 0">
                  <span style="position:absolute;bottom:8px;right:10px;font-size:10px;font-weight:600;color:#94A3B8;opacity:0.5;text-transform:uppercase;letter-spacing:0.05em">Consider Later</span>
                </div>\n"""

            # ── Total opportunity callout ──
            total_annual = sum(b["annual_val"] for b in bubble_data)
            n_areas = len(bubble_data)
            callout_html = f"""<div style="text-align:center;margin-bottom:20px;padding:16px 24px;
                 background:linear-gradient(135deg, #F0FDF4, #ECFDF5);border:1px solid #BBF7D0;border-radius:10px">
              <div style="font-size:13px;font-weight:600;color:#059669;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px">Total Annual Opportunity</div>
              <div style="font-size:36px;font-weight:800;color:#166534;letter-spacing:-0.02em">{fmt_aud(total_annual)}<span style="font-size:16px;font-weight:600;color:#059669">/yr</span></div>
              <div style="font-size:12px;color:#6B7280;margin-top:4px">across {n_areas} process areas</div>
            </div>"""

            # ── Legend (tier colors) ──
            legend_items = ""
            _legend_colors = [("#ea580c", "Quick Win"), ("#2563eb", "SaaS Toolkit"), ("#16a34a", "Custom Platform")]
            for col, label in _legend_colors:
                legend_items += f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:16px;font-size:12px"><span style="width:10px;height:10px;border-radius:50%;background:{col};display:inline-block"></span>{label}</span>'

            scatter_html = f"""
            {callout_html}
            <div style="display:flex;gap:8px;margin-bottom:12px;align-items:center">
              {legend_items}
              <span style="font-size:11px;color:{BRAND_GREY};margin-left:auto">Click a bubble for details</span>
            </div>
            <div style="position:relative;width:100%;max-width:{CHART_W}px;height:{CHART_H}px;margin:0 auto 24px auto;padding:0 0 24px 52px">
              <div class="pm-chart-area" style="position:relative;width:100%;height:100%;background:#FAFBFC;border:1px solid #E5E7EB;border-radius:8px;overflow:visible">
                {zones_html}
                {y_ticks_html}
                {x_ticks_html}
                {bubbles_divs}
                {annotations_html}
              </div>
              <div style="position:absolute;bottom:-4px;left:50%;transform:translateX(-50%);font-size:11px;color:{BRAND_GREY};font-weight:600">Implementation Time (weeks)</div>
              <div style="position:absolute;top:50%;left:-4px;transform:translateY(-50%) rotate(-90deg);font-size:11px;color:{BRAND_GREY};font-weight:600;white-space:nowrap">Annual Value (AUD)</div>
            </div>
            <div id="pm-tooltip" style="display:none;position:fixed;pointer-events:none;background:{BRAND_DARK};color:#fff;
                 border-radius:8px;padding:10px 14px;font-size:12px;z-index:1000;max-width:260px;box-shadow:0 4px 12px rgba(0,0,0,0.3)">
            </div>"""
        else:
            scatter_html = f'<p style="color:{BRAND_GREY};font-style:italic">Proposed changes lack value or implementation data. Run Process Analyst [BR] to estimate.</p>'

    else:
        # ── Fallback: static SVG scatter plot (pre-analyst data) ──
        plottable = [r for r in roi_items if r.get("payback_months") is not None and r.get("annual_saving_aud") is not None]

        if plottable:
            paybacks = [r["payback_months"] for r in plottable]
            savings = [r["annual_saving_aud"] for r in plottable]
            build_costs = [r.get("build_cost_aud") or 0 for r in plottable]
            p90_payback = sorted(paybacks)[int(len(paybacks) * 0.9)] if paybacks else 24
            x_max = max(p90_payback * 1.2, 24)
            y_max_data = max(savings) if savings else 100000
            y_max = max(y_max_data * 1.1, 10000)
            max_build = max(build_costs) if any(build_costs) else 1
            max_build = max(max_build, 1)
            SVG_W, SVG_H = 520, 380
            PAD_L, PAD_R, PAD_T, PAD_B = 70, 30, 30, 50

            def to_svg_x(pm):
                clamped = min(pm, x_max)
                return PAD_L + (clamped / x_max) * (SVG_W - PAD_L - PAD_R)

            def to_svg_y(saving):
                return PAD_T + (1 - saving / y_max) * (SVG_H - PAD_T - PAD_B)

            def bubble_r(build_cost):
                bc = build_cost or 1
                return max(5, min(28, math.sqrt(bc / max_build) * 28))

            TAG_COLOR = {"QUICK_WIN": "#10B981", "CORE_BUILD": "#F59E0B", "FUTURE": "#6B7280"}
            y_gridlines = [10000, 25000, 50000, 100000]
            grid_html = ""
            for yv in y_gridlines:
                if yv > y_max:
                    continue
                gy = to_svg_y(yv)
                grid_html += f'<line x1="{PAD_L}" y1="{gy:.1f}" x2="{SVG_W - PAD_R}" y2="{gy:.1f}" stroke="#E5E7EB" stroke-width="1"/>'
                grid_html += f'<text x="{PAD_L - 4}" y="{gy:.1f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="{BRAND_GREY}">${yv//1000}k</text>'
            mid_x = to_svg_x(12)
            mid_y = to_svg_y(y_max / 2)
            quad_html = f"""
            <rect x="{PAD_L}" y="{PAD_T}" width="{mid_x - PAD_L}" height="{mid_y - PAD_T}" fill="#D1FAE5" opacity="0.3"/>
            <rect x="{mid_x}" y="{PAD_T}" width="{SVG_W - PAD_R - mid_x}" height="{mid_y - PAD_T}" fill="#FEF3C7" opacity="0.3"/>
            <rect x="{PAD_L}" y="{mid_y}" width="{mid_x - PAD_L}" height="{SVG_H - PAD_B - mid_y}" fill="#DBEAFE" opacity="0.3"/>
            <rect x="{mid_x}" y="{mid_y}" width="{SVG_W - PAD_R - mid_x}" height="{SVG_H - PAD_B - mid_y}" fill="#F3F4F6" opacity="0.3"/>"""
            x_ticks = [0, 6, 12, 18, 24, 36]
            x_axis_html = ""
            for xv in x_ticks:
                if xv > x_max:
                    break
                gx = to_svg_x(xv)
                x_axis_html += f'<text x="{gx:.1f}" y="{SVG_H - PAD_B + 14}" text-anchor="middle" font-size="10" fill="{BRAND_GREY}">{xv}mo</text>'
                x_axis_html += f'<line x1="{gx:.1f}" y1="{SVG_H - PAD_B}" x2="{gx:.1f}" y2="{SVG_H - PAD_B + 4}" stroke="{BRAND_GREY}" stroke-width="1"/>'
            bubbles_html = ""
            for r in plottable:
                pm = r["payback_months"]
                saving = r["annual_saving_aud"]
                build = r.get("build_cost_aud") or 0
                tag = r.get("payback_tag", "FUTURE")
                activity = escape(r.get("activity", ""))
                color = TAG_COLOR.get(tag, BRAND_GREY)
                cx = to_svg_x(pm)
                cy = to_svg_y(saving)
                radius = bubble_r(build)
                title_text = f"{activity} — ${saving:,.0f}/yr · {pm}mo payback · ${build:,.0f} build"
                bubbles_html += f"""
                <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.1f}"
                        fill="{color}" fill-opacity="0.7" stroke="{color}" stroke-width="1.5">
                  <title>{title_text}</title>
                </circle>"""
            axis_labels = f"""
            <text x="{(PAD_L + SVG_W - PAD_R) / 2}" y="{SVG_H}" text-anchor="middle" font-size="11" fill="{BRAND_GREY}" font-weight="600">Payback Period (months)</text>
            <text x="12" y="{(PAD_T + SVG_H - PAD_B) / 2}" text-anchor="middle" font-size="11" fill="{BRAND_GREY}" font-weight="600" transform="rotate(-90 12 {(PAD_T + SVG_H - PAD_B) / 2})">Annual Saving</text>"""
            legend_svg = ""
            lx = PAD_L
            for tag, color in TAG_COLOR.items():
                label = tag.replace("_", " ").title()
                legend_svg += f'<circle cx="{lx}" cy="{PAD_T - 14}" r="5" fill="{color}" fill-opacity="0.7"/>'
                legend_svg += f'<text x="{lx + 9}" y="{PAD_T - 10}" font-size="10" fill="{BRAND_GREY}">{label}</text>'
                lx += 100
            scatter_html = f"""
            <svg width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}"
                 style="max-width:100%;display:block;margin:0 auto">
              {quad_html}
              {grid_html}
              <line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{SVG_H - PAD_B}" stroke="#9CA3AF" stroke-width="1.5"/>
              <line x1="{PAD_L}" y1="{SVG_H - PAD_B}" x2="{SVG_W - PAD_R}" y2="{SVG_H - PAD_B}" stroke="#9CA3AF" stroke-width="1.5"/>
              {x_axis_html}
              {bubbles_html}
              {axis_labels}
              {legend_svg}
            </svg>
            <p style="font-size:11px;color:{BRAND_GREY};text-align:center;margin-top:8px">Bubble size = build cost. Hover for details.</p>"""
        else:
            scatter_html = f'<p style="color:{BRAND_GREY};font-style:italic">No ROI items with payback and saving data to plot. Run EI to populate proposed_changes.</p>'

    return (scatter_html, modals_html, has_interactive)


# ─── Utilities ────────────────────────────────────────────────────────────────

def load_audit_data(client_slug: str) -> dict:
    path = Path(f"clients/{client_slug}/audit/audit-data.json")
    if not path.exists():
        print(f"Error: audit data not found at {path}", file=sys.stderr)
        sys.exit(2)
    with open(path) as f:
        return json.load(f)


def load_client_sections(client_slug: str) -> dict:
    """Load section unlock flags from clients.json for the given client slug."""
    clients_path = Path("clients/clients.json")
    default_sections = {
        "process_map": False, "findings": False, "waste": False,
        "solutions_overview": False, "strategic_approaches": False,
        "priority_matrix": False, "transformation": False, "prototype": False,
    }
    if not clients_path.exists():
        return default_sections
    with open(clients_path) as f:
        clients = json.load(f)
    for entry in clients.values():
        if entry.get("slug") == client_slug:
            merged = {**default_sections, **entry.get("sections", {})}
            # Pass prototype_url through sections so JS can read it
            if entry.get("prototype_url"):
                merged["prototype_url"] = entry["prototype_url"]
            return merged
    return default_sections


def ensure_deliverables_dir(client_slug: str) -> Path:
    d = Path(f"clients/{client_slug}/deliverables")
    d.mkdir(parents=True, exist_ok=True)
    return d


def fmt_aud(amount) -> str:
    if amount is None:
        return "N/A"
    if amount < 0:
        return f"-${abs(amount):,.0f}"
    return f"${amount:,.0f}"


def confidence_badge(conf: str) -> str:
    colors = {"HIGH": "#10B981", "MEDIUM": "#F59E0B", "LOW": "#EF4444"}
    c = colors.get(conf, BRAND_GREY)
    return f'<span style="background:{c};color:#fff;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:600">{conf}</span>'


def pricing_source_badge(source_type: str) -> str:
    """Render a badge indicating where pricing data was sourced from."""
    badges = {
        "official": ("#10B981", "#D1FAE5", "OFFICIAL"),
        "aggregator": ("#3B82F6", "#DBEAFE", "AGGREGATOR"),
        "blog": ("#F59E0B", "#FEF3C7", "BLOG"),
        "estimated": ("#EF4444", "#FEE2E2", "ESTIMATED"),
        "training_knowledge": ("#EF4444", "#FEE2E2", "ESTIMATED"),
    }
    if not source_type or source_type not in badges:
        return ""
    color, bg, label = badges[source_type]
    return f'<span style="background:{bg};color:{color};padding:1px 6px;border-radius:3px;font-size:10px;font-weight:600;margin-left:6px">{label}</span>'


def hidden_costs_html(hidden_costs: list) -> str:
    """Render a collapsible hidden costs section if any exist."""
    if not hidden_costs:
        return ""
    likelihood_colors = {
        "likely": ("#EF4444", "#FEE2E2"),
        "possible": ("#F59E0B", "#FEF3C7"),
        "unlikely": ("#64748B", "#F1F5F9"),
    }
    items = ""
    for hc in hidden_costs:
        hc_type = escape(str(hc.get("type", "")).replace("_", " ").title())
        desc = escape(str(hc.get("description", "")))
        annual = hc.get("estimated_annual_aud")
        annual_str = f"${annual:,.0f}/yr" if annual else "—"
        trigger = escape(str(hc.get("trigger", "")))
        lh = hc.get("likelihood", "possible")
        lh_color, lh_bg = likelihood_colors.get(lh, ("#64748B", "#F1F5F9"))
        lh_badge = f'<span style="background:{lh_bg};color:{lh_color};padding:1px 5px;border-radius:3px;font-size:9px;font-weight:600;text-transform:uppercase">{lh}</span>'
        items += f"""<div class="so-hc-item">
            <div class="so-hc-row"><span class="so-hc-type">{hc_type}</span> {lh_badge} <span class="so-hc-cost">{annual_str}</span></div>
            <div class="so-hc-desc">{desc}</div>
            {"<div class='so-hc-trigger'>Trigger: " + trigger + "</div>" if trigger else ""}
        </div>"""
    return f"""<details class="so-hidden-costs">
        <summary>Hidden Costs ({len(hidden_costs)} identified)</summary>
        <div class="so-hc-body">{items}</div>
    </details>"""


def base_css() -> str:
    return f"""
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {BRAND_DARK}; background: {BRAND_LIGHT}; font-size: 15px; line-height: 1.5; }}
    .apg-header {{ background: {BRAND_DARK}; color: #fff; padding: 20px 32px;
                   display: flex; align-items: center; gap: 16px;
                   border-bottom: 3px solid #7DFF00; }}
    .apg-header .logo {{ font-size: 20px; font-weight: 800; color: #ffffff; }}
    .apg-header .subtitle {{ font-size: 13px; color: #9CA3AF; margin-top: 2px; }}
    .container {{ max-width: 1400px; margin: 0 auto; padding: 24px 24px; }}
    h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; }}
    h2 {{ font-size: 20px; font-weight: 700; margin: 24px 0 12px; color: {BRAND_DARK}; }}
    h3 {{ font-size: 16px; font-weight: 600; margin: 16px 0 8px; }}
    .meta {{ font-size: 13px; color: {BRAND_GREY}; margin-bottom: 20px; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px;
               font-size: 12px; font-weight: 600; }}
    .card {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 10px;
              padding: 20px; margin-bottom: 16px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ background: {BRAND_DARK}; color: #fff; padding: 10px 12px; text-align: left;
          font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
    td {{ padding: 9px 12px; border-bottom: 1px solid #F3F4F6; vertical-align: top; }}
    tr:hover td {{ background: {BRAND_LIGHT}; }}
    .highlight {{ color: #166534; font-weight: 700; }}
    .warning {{ background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 6px;
                padding: 10px 14px; font-size: 13px; margin: 12px 0; }}
    blockquote {{ border-left: 3px solid #7DFF00; padding: 8px 16px;
                  background: #f0fdf4; font-style: italic; font-size: 13px;
                  color: #374151; margin: 10px 0; border-radius: 0 6px 6px 0; }}
    @media (max-width: 768px) {{
        .container {{ padding: 16px; }}
        table {{ font-size: 12px; }}
        th, td {{ padding: 8px; }}
    }}
    """


# ─── Transcript Helpers ───────────────────────────────────────────────────────

def _load_client_transcripts(client_dir: str, sessions: list) -> dict:
    """Returns {recording_id_str: [(seconds, speaker, text), ...]} for all sessions with transcripts."""
    result = {}
    meetings_dir = Path(client_dir) / "meetings"
    if not meetings_dir.is_dir():
        return result
    for folder in meetings_dir.iterdir():
        if not folder.is_dir():
            continue
        meta_file = folder / "metadata.json"
        tx_file = folder / "transcript.txt"
        if not (meta_file.exists() and tx_file.exists()):
            continue
        try:
            meta = json.loads(meta_file.read_text())
            mid = str(meta.get("recording_id", ""))
        except Exception:
            continue
        if not mid:
            continue
        lines = []
        for line in tx_file.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^\[(\d+):(\d+)\]\s+(.+?):\s+(.+)$", line.strip())
            if m:
                mins, secs, speaker, text = m.groups()
                lines.append((int(mins) * 60 + int(secs), speaker.strip(), text.strip()))
        result[mid] = lines
    return result


def _extract_transcript_window(transcripts: dict, meeting_id: str, ts: int,
                                before: int = 2, after: int = 6,
                                hint_text: str = "") -> str:
    """Extract a dialogue window anchored on the best keyword match for hint_text.
    Falls back to timestamp-based lookup if no keywords match."""
    lines = transcripts.get(str(meeting_id), [])
    if not lines:
        return ""

    anchor_idx = None

    # Primary: pure keyword search on source_quote (no proximity bias)
    if hint_text:
        keywords = [w.lower() for w in re.split(r'\W+', hint_text) if len(w) > 4]
        if keywords:
            best_score = 0
            for i, (s, speaker, text) in enumerate(lines):
                text_lower = text.lower()
                kw_matches = sum(1 for kw in keywords if kw in text_lower)
                if kw_matches > best_score:
                    best_score = kw_matches
                    anchor_idx = i

    # Fallback: timestamp-based lookup
    if anchor_idx is None:
        anchor_idx = 0
        for i, (s, _, _) in enumerate(lines):
            if s <= ts:
                anchor_idx = i

    start = max(0, anchor_idx - before)
    end = min(len(lines), anchor_idx + after + 1)

    # Group consecutive same-speaker utterances into single blocks
    grouped = []
    for s, speaker, text in lines[start:end]:
        if grouped and grouped[-1][0] == speaker:
            grouped[-1] = (speaker, grouped[-1][1] + " " + text)
        else:
            grouped.append((speaker, text))
    parts = [f"{speaker}: {text}" for speaker, text in grouped]
    return "\n".join(parts)


def _find_best_transcript_match(transcripts: dict, meeting_id: str, ts: int,
                                  hint_text: str = "") -> int:
    """Return the timestamp (seconds) of the best keyword match for hint_text.
    Falls back to ts if no keywords match."""
    lines = transcripts.get(str(meeting_id), [])
    if not lines or not hint_text:
        return ts

    keywords = [w.lower() for w in re.split(r'\W+', hint_text) if len(w) > 4]
    if not keywords:
        return ts

    best_score = 0
    best_ts = ts
    for s, speaker, text in lines:
        text_lower = text.lower()
        kw_matches = sum(1 for kw in keywords if kw in text_lower)
        if kw_matches > best_score:
            best_score = kw_matches
            best_ts = s

    return best_ts if best_score > 0 else ts


# ─── Process Map Generator ─────────────────────────────────────────────────────

# Stage → zone number (1-based)




def _norm_quote(value) -> str:
    """Normalise source_quote — accepts str or list[str], returns a single str."""
    if isinstance(value, list):
        return " ".join(str(v) for v in value if v)
    return str(value) if value else ""


def generate_process_map(ssad: dict) -> str:
    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    sessions = ssad.get("sessions_completed", 0)
    # Stages come only from the audit data — no hardcoded fallback list
    stages = [p["stage"] for p in ssad.get("processes", [])]
    stage_labels, stage_subtitles = _build_stage_lookups(ssad)
    # Build zone numbers dynamically (1-based, sequential)
    stage_zone = {s: i + 1 for i, s in enumerate(stages)}

    # Build processes dict keyed by stage
    processes_by_stage = {}
    for proc in ssad.get("processes", []):
        processes_by_stage[proc["stage"]] = proc.get("steps", [])

    def render_email_refs(email_references: list) -> str:
        """Render email evidence links for a process step (green pill, hover-reveal)."""
        if not email_references:
            return ""
        links = []
        for ref in email_references:
            filename = ref.get("filename", "").strip()
            subject = ref.get("subject", "").strip()
            excerpt = ref.get("excerpt", "").strip()
            if not filename:
                continue
            label = subject or filename
            # Deliverable is in clients/{slug}/deliverables/ → emails are at ../emails/
            href = f"../emails/{escape(filename)}"
            title_attr = f' title="{escape(excerpt)}"' if excerpt else ""
            links.append(
                f'<a class="email-link" href="{href}" target="_blank" rel="noopener"{title_attr}>'
                f'&#128231; {escape(label)}'
                f'</a>'
            )
        if not links:
            return ""
        return f'<div class="email-refs">{"".join(links)}</div>'

    # Build lookup: fathom_meeting_id (recording_id) → fathom_url (calls/{call_id})
    _fathom_base_url: dict = {}
    for _s in ssad.get("sessions", []):
        _mid = _s.get("fathom_meeting_id", "")
        _furl = _s.get("fathom_url", "")
        if _mid and _furl:
            _fathom_base_url[str(_mid)] = _furl.rstrip("/")

    # Load local transcript files for excerpt extraction
    _client_dir = Path("clients") / ssad.get("client_slug", "")
    _transcripts = _load_client_transcripts(str(_client_dir), ssad.get("sessions", []))

    def render_meeting_refs(meeting_references: list, source_quote: str = "") -> str:
        """Render expandable Fathom transcript dropdowns for a process step."""
        if not meeting_references:
            return ""
        items_html = []
        for ref in meeting_references:
            meeting_id = ref.get("meeting_id", "")
            ts = ref.get("timestamp_seconds")
            label = ref.get("label", "")
            if not meeting_id or ts is None:
                continue
            minutes = int(ts) // 60
            seconds = int(ts) % 60
            time_str = f"{minutes}:{seconds:02d}"
            short_label = label or "Meeting ref"
            _base = _fathom_base_url.get(str(meeting_id), f"https://{FATHOM_URL}/calls/{meeting_id}")
            resolved_ts = _find_best_transcript_match(_transcripts, meeting_id, int(ts), hint_text=source_quote)
            href = f"{_base}?t={resolved_ts}"

            # Excerpt priority: analyst-provided > transcript file window > step source_quote
            excerpt_text = (
                ref.get("transcript_excerpt", "").strip()
                or _extract_transcript_window(_transcripts, meeting_id, int(ts), hint_text=source_quote)
                or source_quote
            )
            if excerpt_text:
                lines_html = "".join(
                    f'<div class="tx-line">{escape(line)}</div>'
                    for line in excerpt_text.splitlines()
                    if line.strip()
                )
                excerpt_html = f'<div class="fathom-excerpt">{lines_html}</div>'
            else:
                excerpt_html = ""

            items_html.append(
                f'<details class="fathom-dropdown">'
                f'<summary><span class="ref-label">{escape(short_label)}</span>'
                f'<span class="ref-time">{time_str}</span></summary>'
                f'<div class="fathom-panel">'
                f'{excerpt_html}'
                f'<a class="fathom-open-btn" href="{href}" target="_blank" rel="noopener">'
                f'&#9654; Open Recording</a>'
                f'</div>'
                f'</details>'
            )
        if not items_html:
            return ""
        return f'<div class="fathom-refs">{"".join(items_html)}</div>'

    def render_step(step: dict, zn: int = 1, owner_color_map: dict = None) -> str:
        if owner_color_map is None:
            owner_color_map = {}
        stype = step.get("type", "step")
        desc = escape(step.get("description", ""))
        owner_raw = step.get("owner", "").strip()
        owner = escape(owner_raw)
        conf = step.get("confidence", "LOW")
        quote = escape(_norm_quote(step.get("source_quote", "")))
        session = step.get("source_session", "")
        speaker = escape(step.get("source_speaker", ""))
        hours = step.get("waste_hours_per_week") or 0
        meeting_refs = step.get("meeting_references") or []
        email_refs = step.get("email_references") or []

        # Map type to CSS class; standard steps get zone-tinted class
        if stype == "step":
            box_class = f"step step-z{zn}"
        else:
            box_class_map = {
                "decision": "decision-box",
                "pain": "pain-box",
                "optimisation": "opp-box",
                "automation": "auto-box",
            }
            box_class = box_class_map.get(stype, "step")

        # LOW confidence adds dashed border override
        low_conf_style = "border-style:dashed!important;" if conf == "LOW" else ""

        # Tooltip from source quote
        tooltip = ""
        if quote:
            source_info = f"Session {session}" if session else ""
            if speaker:
                source_info += f" · {speaker}"
            q_text = quote[:120] + ("..." if len(quote) > 120 else "")
            tooltip_text = f"{source_info}: {q_text}" if source_info else q_text
            tooltip = f'title="{tooltip_text}"'

        # Owner tag: use assigned color class from owner_color_map
        if owner_raw:
            tag_cls, _ = owner_color_map.get(owner_raw, ("person-tag", None))
            owner_html = f'<div class="box-body"><span class="person-tag {tag_cls}">{owner}</span></div>'
        else:
            owner_html = ""

        # Tool tags from tool_ids
        tool_ids = step.get("tool_ids") or []
        if tool_ids:
            tool_pills = "".join(f'<span class="step-tool-tag">{escape(t)}</span>' for t in tool_ids)
            tools_html = f'<div class="step-tools">{tool_pills}</div>'
        else:
            tools_html = ""

        sq = step.get("source_quote", "") or step.get("source_quotes", "")
        if isinstance(sq, list):
            sq = " ".join(sq)
        meeting_refs_html = render_meeting_refs(meeting_refs, sq)
        email_refs_html = render_email_refs(email_refs)

        # Metadata chips
        meta_parts = []
        if step.get("duration_minutes"):
            meta_parts.append(f"{step['duration_minutes']} min")
        if step.get("frequency"):
            meta_parts.append(escape(str(step["frequency"])))
        meta_html = (
            '<div class="step-meta">' +
            "".join(f'<span class="meta-chip">{p}</span>' for p in meta_parts) +
            '</div>'
        ) if meta_parts else ""

        # Inline source quote (full text) + session badge
        quote_html = ""
        if quote:
            session_badge = f'<span class="step-session">Session {session}</span>' if session else ""
            quote_html = f'<div class="step-quote">&ldquo;{quote}&rdquo;{session_badge}</div>'

        return f"""
        <div class="box {box_class} process-step" {tooltip}
             style="{low_conf_style}">
          <div class="box-title">{desc}</div>
          {owner_html}
          {tools_html}
          {meta_html}
          {quote_html}
          {meeting_refs_html}
          {email_refs_html}
        </div>"""

    def render_parallel_group(step: dict, zn: int = 1) -> str:
        items = step.get("items") or []
        label = escape(step.get("description", ""))
        conf = step.get("confidence", "LOW")
        low_conf = "border-style:dashed!important;" if conf == "LOW" else ""

        chip_parts = []
        for item in items:
            # Guard: item may be a plain string if audit data was written incorrectly
            if isinstance(item, str):
                item = {"label": item}
            lbl = escape(item.get("label", ""))
            tool = item.get("tool", "") or ""
            owner = item.get("owner", "") or ""
            q = escape(_norm_quote(item.get("source_quote") or "").strip())
            title_attr = f' title="{q}"' if q else ""

            refs = item.get("meeting_references") or []
            link_html = ""
            if refs and refs[0].get("meeting_id") and refs[0].get("timestamp_seconds") is not None:
                _mid0 = str(refs[0]['meeting_id'])
                _base0 = _fathom_base_url.get(_mid0, f"https://{FATHOM_URL}/calls/{_mid0}")
                _url = f"{_base0}?t={int(refs[0]['timestamp_seconds'])}"
                _item_quote = _norm_quote(item.get("source_quote") or "").strip()
                _chip_excerpt = f'<p class="chip-excerpt">{escape(_item_quote)}</p>' if _item_quote else ""
                link_html = (
                    f'<details class="chip-dropdown">'
                    f'<summary>▶ Recording</summary>'
                    f'<div class="chip-panel">'
                    f'{_chip_excerpt}'
                    f'<a class="chip-open-btn" href="{_url}" target="_blank" rel="noopener">Open Recording &#8599;</a>'
                    f'</div>'
                    f'</details>'
                )

            tool_html = f'<span class="chip-tool">{escape(tool)}</span>' if tool else ""
            owner_html = f'<span class="chip-owner person-tag">{escape(owner)}</span>' if owner else ""

            chip_parts.append(
                f'<div class="pg-chip"{title_attr}>'
                f'{lbl}{tool_html}{owner_html}{link_html}'
                f'</div>'
            )

        n = max(len(items), 1)
        crossbar_pct = round((n - 1) / n * 100, 1) if n > 1 else 0
        legs = "".join(
            f'<div class="pg-leg"><div class="v-line"></div></div>' for _ in range(n)
        )

        return f"""
        <div class="process-step" style="{low_conf}">
          <div class="pg-label">{label}</div>
          <div class="pg-row">{"".join(chip_parts)}</div>
          <div class="pg-merge">
            <div class="pg-legs">{legs}</div>
            <div class="pg-crossbar" style="width:{crossbar_pct}%"></div>
            <div class="pg-drop">
              <div class="v-line"></div>
              <div class="v-tip"></div>
            </div>
          </div>
        </div>"""

    # Build decision_nodes dict keyed by stage (list, consumed sequentially)
    _decision_nodes_by_stage: dict = {}
    for dn in ssad.get("decision_nodes", []):
        s = dn.get("stage", "")
        _decision_nodes_by_stage.setdefault(s, []).append(dn)

    def render_decision_gate(node: dict, steps_by_id: dict = None, zn: int = 1) -> str:
        condition = escape(node.get("condition", ""))
        yes = escape(node.get("yes_path", ""))
        no  = escape(node.get("no_path", ""))
        v_tip = '<div class="v-arrow"><div class="v-line" style="height:8px;"></div><div class="v-tip"></div></div>'

        _steps_by_id = steps_by_id or {}
        no_branch_ids  = node.get("no_branch_step_ids")  or []
        yes_branch_ids = node.get("yes_branch_step_ids") or []

        yes_col_html = (_render_branch_sequence(yes_branch_ids, _steps_by_id, zn)
                        if yes_branch_ids
                        else f'<div class="box branch-yes-box"><div class="box-title">{yes}</div></div>')
        no_col_html  = (_render_branch_sequence(no_branch_ids, _steps_by_id, zn)
                        if no_branch_ids
                        else f'<div class="box branch-no-box"><div class="box-title">{no}</div></div>')

        return f"""
        <div class="decision-gate">
          <div class="gate-condition">&#11042; {condition}</div>
          <div class="two-col" style="margin-top:10px;align-items:start;">
            <div class="col">
              <span class="fork-label yes">&#10003; Yes</span>
              {v_tip}
              {yes_col_html}
            </div>
            <div class="col">
              <span class="fork-label no">&#10007; No</span>
              {v_tip}
              {no_col_html}
            </div>
          </div>
          <div class="gate-merge-spacer"></div>
        </div>"""

    def _render_branch_sequence(step_ids: list, steps_by_id: dict, zn: int) -> str:
        v_tip = '<div class="v-arrow"><div class="v-line" style="height:10px;"></div><div class="v-tip"></div></div>'
        parts = []
        for j, sid in enumerate(step_ids):
            s = steps_by_id.get(sid)
            if not s:
                continue
            if s.get("type") == "optimisation":
                continue
            if s.get("type") == "parallel_group":
                parts.append(render_parallel_group(s, zn=zn))
            else:
                parts.append(render_step(s, zn=zn, owner_color_map=owner_color_map))
            if j < len(step_ids) - 1:
                parts.append(v_tip)
        return "\n".join(parts)

    # Data flow mechanism → (color, short label)
    _FLOW_STYLES = {
        "automated_sync":     ("#10B981", "Auto-sync"),
        "api_integration":    ("#10B981", "API"),
        "manual_entry":       ("#EF4444", "Manual"),
        "manual_check":       ("#EF4444", "Manual check"),
        "email_notification": ("#F59E0B", "Email"),
        "csv_export":         ("#F59E0B", "CSV"),
        "verbal":             ("#9CA3AF", "Verbal"),
        "unknown":            ("#9CA3AF", "?"),
    }

    def render_labeled_arrow(data_flow: dict) -> str:
        """Render a v-arrow with a colored mechanism label."""
        mechanism = data_flow.get("mechanism", "unknown")
        color, label = _FLOW_STYLES.get(mechanism, ("#9CA3AF", mechanism.replace("_", " ").title()))
        return (
            f'<div class="v-arrow labeled-arrow">'
            f'<div class="v-line" style="height:6px;background:{color}"></div>'
            f'<span class="flow-label" style="color:{color};border-color:{color}">{escape(label)}</span>'
            f'<div class="v-line" style="height:6px;background:{color}"></div>'
            f'<div class="v-tip" style="border-top-color:{color}"></div>'
            f'</div>'
        )

    def render_zone(stage: str) -> str:
        steps = processes_by_stage.get(stage, [])
        label = stage_labels.get(stage, stage.replace("_", " ").title())
        subtitle = stage_subtitles.get(stage, "")
        zn = stage_zone.get(stage, 1)
        # Clamp z-number to CSS vars we define (z1–z9)
        zn = max(1, min(zn, 9))
        zone_class = f"zone z{zn}"

        # Build decision gate lookup: after_step_id → list of nodes; unanchored → list
        nodes_by_step: dict = {}
        nodes_unanchored: list = []
        for dn in _decision_nodes_by_stage.get(stage, []):
            anchor = dn.get("after_step_id", "").strip()
            if anchor:
                nodes_by_step.setdefault(anchor, []).append(dn)
            else:
                nodes_unanchored.append(dn)

        steps_by_id: dict = {s.get("step_id", ""): s for s in steps}

        v_arrow = '<div class="v-arrow"><div class="v-line" style="height:14px;"></div><div class="v-tip"></div></div>'

        if steps:
            step_parts = []
            prev_pg = False
            for i, s in enumerate(steps):
                if s.get("branch_only"):
                    continue
                if s.get("type") == "optimisation":
                    continue
                if s.get("type") == "parallel_group":
                    step_parts.append(render_parallel_group(s, zn=zn))
                    prev_pg = True
                else:
                    step_parts.append(render_step(s, zn=zn, owner_color_map=owner_color_map))
                    prev_pg = False
                sid = s.get("step_id", "")
                # Inject anchored decision gates after their step
                for dn in nodes_by_step.get(sid, []):
                    step_parts.append(v_arrow)
                    step_parts.append(render_decision_gate(dn, steps_by_id=steps_by_id, zn=zn))
                # Legacy fallback: type=="decision" steps consume unanchored nodes
                if s.get("type") == "decision" and nodes_unanchored:
                    step_parts.append(render_decision_gate(nodes_unanchored.pop(0), steps_by_id=steps_by_id, zn=zn))
                if i < len(steps) - 1 and not prev_pg:
                    # Look ahead for data_flow on the next non-branch step
                    next_flow = None
                    for ns in steps[i + 1:]:
                        if not ns.get("branch_only"):
                            next_flow = ns.get("data_flow")
                            break
                    if next_flow and next_flow.get("mechanism"):
                        step_parts.append(render_labeled_arrow(next_flow))
                    else:
                        step_parts.append(v_arrow)
            # Any remaining unanchored nodes go at end of zone
            for dn in nodes_unanchored:
                step_parts.append(v_arrow)
                step_parts.append(render_decision_gate(dn, steps_by_id=steps_by_id, zn=zn))
            steps_html = "\n".join(step_parts)
            badge_text = f"{len(steps)} step{'s' if len(steps) != 1 else ''}"
        else:
            steps_html = """
            <div style="text-align:center;padding:28px 12px;color:#9CA3AF;font-size:12px;
                        border:2px dashed #E5E7EB;border-radius:10px;margin:8px 0">
              <div style="font-size:24px;margin-bottom:8px">&#x23F3;</div>
              Data collection in progress
            </div>"""
            badge_text = "pending"

        return f"""
        <div class="{zone_class}" id="zone-{stage}">
          <span class="zone-badge">{badge_text}</span>
          <div class="zone-title">{label}</div>
          <div class="zone-subtitle">{subtitle}</div>
          {steps_html}
        </div>"""

    # ── Build owner → (css_class, hex_color) palette mapping ──────────────────
    OWNER_TAG_PALETTE = [
        ("tag-pink",    "#d63384"),
        ("tag-orange",  "#c75000"),
        ("tag-teal",    "#0d9488"),
        ("tag-purple",  "#7b2fbe"),
        ("tag-amber",   "#d97706"),
        ("tag-blue",    "#2563EB"),
        ("tag-green",   "#198754"),
        ("tag-health",  "#0891b2"),
        ("tag-rose",    "#be185d"),
    ]
    _tool_kw = {"automated", "hubspot", "monday", "twilio", "xero", "foundu", "system", "planned",
                "google", "sheets", "zapier", "slack", "notion", "airtable", "asana", "jira",
                "salesforce", "stripe", "quickbooks", "myob", "deputy", "employment hero"}
    owner_color_map: dict = {}  # owner_str → (css_class, hex)
    _palette_idx = 0
    for _proc in ssad.get("processes", []):
        for _step in _proc.get("steps", []):
            _o = _step.get("owner", "").strip()
            if _o and _o not in owner_color_map:
                if any(k in _o.lower() for k in _tool_kw):
                    owner_color_map[_o] = ("tool-tag", None)
                else:
                    _cls, _hex = OWNER_TAG_PALETTE[_palette_idx % len(OWNER_TAG_PALETTE)]
                    owner_color_map[_o] = (_cls, _hex)
                    _palette_idx += 1

    # ── Parse owner strings into canonical people + tools ─────────────────────
    _KNOWN_TOOLS = {
        "hubspot", "twilio", "monday", "foundu", "xero",
        "system", "automated", "automation", "planned automation",
        "google sheets", "sheets", "google", "zapier", "slack",
        "notion", "airtable", "asana", "jira", "salesforce",
        "stripe", "quickbooks", "myob", "deputy", "employment hero",
        "ucollect", "easydebit",
    }
    _STRIP_ALL_PARENS = re.compile(r'\s*\([^)]*\)')   # strip ALL parens first
    _SEPARATORS = re.compile(r'\s*\u2192\s*|\s*/\s*|\s*,\s*|\s+&\s+|\s*\+\s*')
    _SKIP = {"none", "planned", "payroll", "accountant", "nannies", "family",
             "va", "recruitment team", "bdm", "marketing", "",
             "videographer", "organic specialist", "specialist", "external", "admin"}
    _DEPARTMENTS = {"contractors", "management", "operations", "sales", "finance",
                    "hr", "support", "leadership", "founders"}

    # Build canonical name map from staff_roster
    _roster = ssad.get("staff_roster", [])
    _canonical_name: dict = {}  # lowercase token → display first name
    for _person in _roster:
        _full = _person.get("name", "").strip()
        if _full:
            _first = _full.split()[0]
            _canonical_name[_full.lower()] = _first
            _canonical_name[_first.lower()] = _first

    canonical_people: dict = {}       # display_name → css_class (first-seen wins)
    canonical_departments: dict = {}  # dept_name → css_class
    canonical_tools: set = set()

    for _owner_str, (_cls, _hex_) in owner_color_map.items():
        # Strip all parentheticals BEFORE splitting on / so "Alice (15hrs/wk)" works
        _clean_full = _STRIP_ALL_PARENS.sub('', _owner_str).strip()
        for _part in _SEPARATORS.split(_clean_full):
            _clean = _part.strip()
            _low = _clean.lower()
            if not _clean or _low in _SKIP or _low.startswith("none") or _low.startswith("planned"):
                continue
            if any(_t in _low for _t in _KNOWN_TOOLS):
                canonical_tools.add(_clean)
            elif _low in _DEPARTMENTS:
                if _clean not in canonical_departments:
                    canonical_departments[_clean] = "dept-tag"
            else:
                # Normalize to staff roster name
                _display = _canonical_name.get(_low, _clean)
                if _display not in canonical_people:
                    canonical_people[_display] = _cls

    # Also pull tool names directly from tools[] in the audit data
    for _tool_entry in ssad.get("tools", []):
        _tn = _tool_entry.get("tool_name", "").strip()
        if _tn:
            canonical_tools.add(_tn)

    def _render_tool_badge(name: str) -> str:
        return f'<span class="tool-tag">{escape(name)}</span>'

    # ── People Bar HTML ────────────────────────────────────────────────────────
    _team_tags = [
        f'<span class="person-tag {cls}">{escape(name)}</span>'
        for name, cls in canonical_people.items()
    ]
    _dept_tags = [
        f'<span class="dept-tag">{escape(name)}</span>'
        for name in canonical_departments
    ]
    _tool_tags = [
        _render_tool_badge(t)
        for t in sorted(canonical_tools)
    ]
    _pb_sections = []
    if _team_tags:
        _pb_sections.append(
            f'<div class="pb-section"><span class="pb-label">Team</span>{"".join(_team_tags)}</div>'
        )
    if _dept_tags:
        _pb_sections.append(
            f'<div class="pb-section"><span class="pb-label">Depts</span>{"".join(_dept_tags)}</div>'
        )
    if _tool_tags:
        _pb_sections.append(
            f'<div class="pb-section"><span class="pb-label">Tools</span>{"".join(_tool_tags)}</div>'
        )
    people_bar_html = (
        f'<div class="people-bar"><div class="people-bar-inner">{"".join(_pb_sections)}</div></div>'
        if _pb_sections else ""
    )

    zones_html = "\n".join(render_zone(stage) for stage in stages)

    # ── Pain Points Summary Section ──────────────────────────────────────────
    pain_summary = ssad.get("pain_points_summary") or {}
    pain_points = ssad.get("pain_points") or []
    pain_summary_html = ""

    if pain_points:
        # Theme cards from pain_points_summary.top_themes
        theme_cards = ""
        for theme in (pain_summary.get("top_themes") or []):
            t_name = escape(theme.get("theme", ""))
            t_count = theme.get("count", 0)
            t_stages = ", ".join(escape(s.replace("_", " ").title()) for s in theme.get("stages_affected", []))
            t_quote = escape(theme.get("example_quote", ""))
            quote_html = f'<div class="pain-summary-quote">&ldquo;{t_quote}&rdquo;</div>' if t_quote else ""
            theme_cards += (
                f'<div class="pain-theme-card">'
                f'<div class="pain-theme-name">{t_name}</div>'
                f'<div class="pain-theme-meta">{t_count} occurrence{"s" if t_count != 1 else ""} &middot; {t_stages}</div>'
                f'{quote_html}'
                f'</div>'
            )

        # Individual pain points grouped by stage
        pp_by_stage: dict = {}
        for pp in pain_points:
            st = pp.get("stage", "unknown")
            pp_by_stage.setdefault(st, []).append(pp)

        detail_html = ""
        for st, pps in pp_by_stage.items():
            st_label = escape(st.replace("_", " ").title())
            items = ""
            for pp in pps:
                pp_desc = escape(pp.get("description", ""))
                pp_quote = escape(pp.get("quote", ""))
                pp_speaker = escape(pp.get("speaker", ""))
                speaker_html = f' &mdash; {pp_speaker}' if pp_speaker else ""
                quote_part = f'<div class="pp-item-quote">&ldquo;{pp_quote}&rdquo;{speaker_html}</div>' if pp_quote else ""
                items += f'<div class="pp-item"><div class="pp-item-desc">{pp_desc}</div>{quote_part}</div>'
            detail_html += f'<div class="pp-stage-group"><div class="pp-stage-label">{st_label}</div>{items}</div>'

        total_count = pain_summary.get("total_count", len(pain_points))
        pain_summary_html = f"""
        <div class="pain-summary-section" id="pain-points">
          <div class="pain-summary-header">Pain Points Summary &mdash; {total_count} identified</div>
          {"<div class='pain-themes-row'>" + theme_cards + "</div>" if theme_cards else ""}
          <div class="pain-details">{detail_html}</div>
        </div>"""

    # ── Opportunities Summary Section ─────────────────────────────────────────
    # Read from top-level optimisations[] array (same source as findings.html)
    all_optimisations = ssad.get("optimisations") or []

    opportunities_html = ""
    if all_optimisations:
        opp_by_stage: dict = {}
        for o in all_optimisations:
            st = o.get("stage", "unknown")
            opp_by_stage.setdefault(st, []).append(o)

        opp_detail_html = ""
        for st, opps in opp_by_stage.items():
            st_label = escape(st.replace("_", " ").title())
            items = ""
            for o in opps:
                o_desc = escape(o.get("description", ""))
                o_quote = escape(o.get("quote", ""))
                o_speaker = escape(o.get("speaker", "") or "")
                speaker_html = f' &mdash; {o_speaker}' if o_speaker else ""
                quote_part = f'<div class="opp-item-quote">&ldquo;{o_quote}&rdquo;{speaker_html}</div>' if o_quote else ""
                items += f'<div class="opp-item"><div class="opp-item-desc">{o_desc}</div>{quote_part}</div>'
            opp_detail_html += f'<div class="opp-stage-group"><div class="opp-stage-label">{st_label}</div>{items}</div>'

        opp_count = len(all_optimisations)
        opportunities_html = f"""
        <div class="opp-summary-section" id="opportunities">
          <div class="opp-summary-header">Optimisations &mdash; {opp_count} identified</div>
          <div class="opp-details">{opp_detail_html}</div>
        </div>"""

    # Legend items
    legend_items = [
        ("#FFFFFF", "#E5E7EB", "Standard Step"),
        ("#FEE2E2", "#EF4444", "Pain Point"),
        ("#FEF3C7", "#F59E0B", "Decision"),
        ("#DBEAFE", "#3B82F6", "Automation"),
    ]
    legend_html = "".join(
        f'<div class="legend-item">'
        f'<div class="legend-swatch" style="background:{bg};border:1.5px solid {border}"></div>'
        f'{label}</div>'
        for bg, border, label in legend_items
    )
    legend_html += (
        '<div class="legend-item" style="color:#6B7280;font-style:italic">Dashed border = LOW confidence</div>'
    )

    # ── Sidebar Navigation ────────────────────────────────────────────────────
    nav_links = []
    for stage in stages:
        label = stage_labels.get(stage, stage.replace("_", " ").title())
        nav_links.append(f'<a href="#zone-{stage}" data-target="zone-{stage}">{label}</a>')
    if pain_points:
        nav_links.append('<a href="#pain-points" data-target="pain-points">Pain Points</a>')
    if all_optimisations:
        nav_links.append('<a href="#opportunities" data-target="opportunities">Optimisations</a>')

    sidebar_html = (
        '<nav class="sidebar-nav" id="sidebarNav">'
        '<div class="nav-header">Sections</div>'
        + "".join(nav_links)
        + '</nav>'
        '<button class="sidebar-toggle" id="sidebarToggle" '
        'onclick="document.getElementById(\'sidebarNav\').classList.toggle(\'open\')">'
        '&#9776;</button>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Process Map</title>
{BRAND_FAVICON}
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  html {{ scroll-behavior: smooth; }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --pain-bg: #fef2f2; --pain-border: #fca5a5; --pain-text: #dc2626;
    --opp-bg: #f0fdf4; --opp-border: #86efac; --opp-text: #16a34a;
    --decision-bg: #fffbeb; --decision-border: #fcd34d; --decision-text: #92400e;
    --auto-bg: #eff6ff; --auto-border: #93c5fd; --auto-text: #1d4ed8;
  }}
  body {{ background: #f7f9fc; font-family: 'Inter', -apple-system, sans-serif;
          color: #0f1825; min-height: 100vh; }}

  /* ── HEADER ── */
  .apg-header {{ background: #0f1825; color: #fff; padding: 20px 32px;
                 display: flex; align-items: center; gap: 16px;
                 border-bottom: 3px solid #7DFF00; }}
  .apg-header .logo {{ font-size: 20px; font-weight: 800; color: #ffffff; }}
  .apg-header .subtitle {{ font-size: 13px; color: #9CA3AF; margin-top: 2px; }}

  /* ── SUBHEADER ── */
  .subheader {{ background: #ffffff;
                border-bottom: 1px solid #e2e8f0;
                padding: 24px 32px 20px; text-align: center; }}
  .subheader h1 {{ font-family: 'Inter', sans-serif;
                   font-size: 28px; font-weight: 700; color: #0f1825; margin-bottom: 4px; }}
  .subheader .meta {{ font-size: 12px; color: #6B7280; }}

  /* ── LEGEND ── */
  .legend {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 14px;
             padding: 12px 20px; background: #f7f9fc; border-bottom: 1px solid #e2e8f0; }}
  .legend-item {{ display: flex; align-items: center; gap: 5px; font-size: 11px;
                  color: #475569; font-weight: 500; }}
  .legend-swatch {{ width: 13px; height: 13px; border-radius: 3px; flex-shrink: 0; }}

  /* ── CANVAS ── */
  .canvas {{ padding: 30px 24px 60px; max-width: 100%; margin-right: auto; }}

  /* ── ZONES ── */
  .zone {{ border-radius: 14px; padding: 20px 22px 24px;
           margin-bottom: 28px; position: relative;
           background: #ffffff; border: 1px solid #e2e8f0;
           box-shadow: 0 1px 8px rgba(15,24,37,0.06); }}
  .zone-title {{ font-family: 'Inter', sans-serif;
                 font-size: 18px; font-weight: 800; margin-bottom: 4px;
                 color: #0f1825; letter-spacing: -0.02em; }}
  .zone-subtitle {{ font-size: 11px; font-weight: 400; color: #64748b; margin-bottom: 14px; }}
  .zone-badge {{ position: absolute; top: 16px; right: 18px; font-size: 10px; font-weight: 600;
                 padding: 3px 10px; border-radius: 20px; letter-spacing: 0.5px; text-transform: uppercase;
                 color: #64748b; background: #f1f5f9; border: 1px solid #e2e8f0; }}
  .z1,.z2,.z3,.z4,.z5,.z6,.z7,.z8,.z9 {{ background: #ffffff; border: 1px solid #e2e8f0;
    box-shadow: 0 1px 8px rgba(15,24,37,0.06); }}
  .z1 .zone-title,.z2 .zone-title,.z3 .zone-title,.z4 .zone-title,
  .z5 .zone-title,.z6 .zone-title,.z7 .zone-title,.z8 .zone-title,
  .z9 .zone-title {{ color: #0f1825; }}
  .z1 .zone-badge,.z2 .zone-badge,.z3 .zone-badge,.z4 .zone-badge,
  .z5 .zone-badge,.z6 .zone-badge,.z7 .zone-badge,.z8 .zone-badge,
  .z9 .zone-badge {{ color: #64748b; background: #f1f5f9; border: 1px solid #e2e8f0; }}

  /* ── BOXES ── */
  .box {{ border-radius: 10px; padding: 12px 14px; font-size: 12px; line-height: 1.55;
          position: relative; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
          transition: box-shadow 0.15s; }}
  .box:hover {{ box-shadow: 0 4px 14px rgba(0,0,0,0.10); }}
  .box-title {{ font-weight: 600; font-size: 13px; margin-bottom: 4px; color: #0f1825; }}
  .box-body {{ font-size: 12px; color: #374151; line-height: 1.6; }}
  .step {{ background: #f7f9fc; border: 1px solid #e2e8f0; }}
  .step-z1 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z1 .box-title {{ color:#0f1825; }}
  .step-z2 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z2 .box-title {{ color:#0f1825; }}
  .step-z3 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z3 .box-title {{ color:#0f1825; }}
  .step-z4 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z4 .box-title {{ color:#0f1825; }}
  .step-z5 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z5 .box-title {{ color:#0f1825; }}
  .step-z6 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z6 .box-title {{ color:#0f1825; }}
  .step-z7 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z7 .box-title {{ color:#0f1825; }}
  .step-z8 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z8 .box-title {{ color:#0f1825; }}
  .step-z9 {{ background:#f7f9fc; border:1px solid #e2e8f0; }} .step-z9 .box-title {{ color:#0f1825; }}
  .decision-box {{ background: var(--decision-bg); border: 2px dashed var(--decision-border); border-radius: 50px; text-align: center; }}
  .decision-box .box-title {{ color: var(--decision-text); }}
  .auto-box {{ background: var(--auto-bg); border: 1.5px solid var(--auto-border); }}
  .auto-box .box-title {{ color: var(--auto-text); }}
  .pain-box {{ background: var(--pain-bg); border: 1.5px solid var(--pain-border); }}
  .pain-box .box-title {{ color: var(--pain-text); }}
  .opp-box {{ background: var(--opp-bg); border: 1.5px solid var(--opp-border); }}
  .opp-box .box-title {{ color: var(--opp-text); }}

  /* ── V-ARROW ── */
  .v-arrow {{ display:flex; flex-direction:column; align-items:center; margin: 3px 0; }}
  .v-line {{ width:2px; background:#94a3b8; }}
  .v-tip {{ width:0; height:0; border-left:5px solid transparent; border-right:5px solid transparent; border-top:7px solid #94a3b8; }}

  /* ── GRID LAYOUTS ── */
  .two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  .three-col {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }}
  .col {{ display:flex; flex-direction:column; align-items:center; }}
  .col .box {{ width:100%; }}

  /* ── FORK LABELS ── */
  .fork-label {{ font-size:10px; font-weight:700; color:white; border-radius:10px;
                 padding:3px 10px; display:inline-block; margin-bottom:4px; }}
  .fork-label.yes {{ background:#16a34a; }}
  .fork-label.no  {{ background:#dc2626; }}
  .branch-yes-box {{ background:#f0fdf4; border:1.5px solid #86efac; }}
  .branch-no-box  {{ background:#fef2f2; border:1.5px solid #fca5a5; }}
  .branch-yes-box .box-title {{ color:#15803d; }}
  .branch-no-box  .box-title {{ color:#dc2626; }}
  .decision-gate {{ position: relative; margin: 4px 0; }}
  .gate-merge-spacer {{ height: 16px; }}
  .gate-condition {{ background: #fffbeb; border: 2px dashed #fcd34d;
                     border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600;
                     color: #92400e; text-align: center; }}

  /* ── PEOPLE BAR ── */
  .people-bar {{ background:#ffffff; border-bottom:1px solid #e2e8f0; padding:12px 24px; }}
  .people-bar-inner {{ max-width:1300px; margin:0 auto; display:flex; flex-direction:column; gap:10px; }}
  .pb-section {{ display:flex; flex-wrap:wrap; align-items:center; gap:6px; }}
  .pb-label {{ font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
               color:#9CA3AF; white-space:nowrap; min-width:38px; }}

  /* ── PERSON / TOOL TAGS ── */
  .person-tag,
  .person-tag.tag-pink, .person-tag.tag-orange, .person-tag.tag-teal,
  .person-tag.tag-purple, .person-tag.tag-amber, .person-tag.tag-blue,
  .person-tag.tag-green, .person-tag.tag-health, .person-tag.tag-rose
    {{ background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;
       border-radius: 6px; font-size: 11px; padding: 3px 10px; display: inline-block; margin-top: 2px; }}
  .tool-tag {{ display: inline-block; font-size: 10px; font-weight: 600;
               background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0;
               padding: 2px 9px; border-radius: 20px; margin-top: 2px; }}
  .dept-tag {{ display: inline-block; font-size: 10px; font-weight: 600;
               background: #f8fafc; color: #64748b; border: 1px dashed #94a3b8;
               padding: 2px 9px; border-radius: 20px; margin-top: 2px; }}

  /* ── STEP TOOL TAGS ── */
  .step-tools {{ margin-top:4px; display:flex; flex-wrap:wrap; gap:3px; }}
  .step-tool-tag {{ display:inline-block; font-size:11px; font-weight:600;
    background:#f0fdf4; color:#166534; border:1px solid #bbf7d0;
    padding:1px 7px; border-radius:10px; }}

  /* ── LABELED FLOW ARROWS ── */
  .labeled-arrow {{ gap: 0; }}
  .flow-label {{ font-size:10px; font-weight:700; padding:1px 8px;
    border:1.5px solid #94a3b8; border-radius:10px; background:#ffffff;
    color:#475569; }}

  /* ── PAIN POINTS SUMMARY ── */
  .pain-summary-section {{ background:#fef2f2; border-left:4px solid #ef4444; border-radius:12px;
    padding:20px 22px 24px; margin-top:28px; }}
  .pain-summary-header {{ font-family:'Inter',sans-serif; font-size:18px;
    font-weight:800; color:#991b1b; margin-bottom:14px; }}
  .pain-themes-row {{ display:flex; flex-wrap:wrap; gap:10px; margin-bottom:16px; }}
  .pain-theme-card {{ background:#fff; border:1px solid #FECACA; border-radius:8px;
    padding:10px 14px; flex:1 1 220px; min-width:200px; }}
  .pain-theme-name {{ font-weight:700; font-size:12px; color:#991B1B; margin-bottom:3px; }}
  .pain-theme-meta {{ font-size:10px; color:#6B7280; }}
  .pain-summary-quote {{ font-size:10px; font-style:italic; color:#9A8A80;
    border-left:2px solid #FECACA; padding:2px 6px; margin-top:5px; }}
  .pain-details {{ display:flex; flex-direction:column; gap:10px; }}
  .pp-stage-group {{ }}
  .pp-stage-label {{ font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.06em; color:#991B1B; margin-bottom:4px; }}
  .pp-item {{ background:#fff; border:1px solid #FECACA; border-radius:6px;
    padding:8px 12px; margin-bottom:4px; }}
  .pp-item-desc {{ font-size:11px; font-weight:600; color:#1A1A2E; }}
  .pp-item-quote {{ font-size:10px; font-style:italic; color:#9A8A80; margin-top:3px; }}

  /* ── OPPORTUNITIES SUMMARY ── */
  .opp-summary-section {{ background:#f0fdf4; border-left:4px solid #22c55e; border-radius:12px;
    padding:20px 24px; margin-top:28px; }}
  .opp-summary-header {{ font-family:'Inter',sans-serif; font-size:18px;
    font-weight:800; color:#166534; margin-bottom:14px; }}
  .opp-details {{ display:flex; flex-direction:column; gap:12px; }}
  .opp-stage-group {{ }}
  .opp-stage-label {{ font-size:11px; font-weight:700; text-transform:uppercase;
    letter-spacing:0.06em; color:#059669; margin-bottom:6px; }}
  .opp-item {{ background:#fff; border:1px solid #A7F3D0; border-radius:6px;
    padding:8px 12px; margin-bottom:4px; }}
  .opp-item-desc {{ font-size:11px; font-weight:600; color:#1A1A2E; }}
  .opp-item-quote {{ font-size:10px; font-style:italic; color:#6B7280; margin-top:3px; }}

  /* ── STEP METADATA + QUOTE ── */
  .step-meta {{ margin-top:5px; display:flex; flex-wrap:wrap; gap:4px; }}
  .meta-chip {{ font-size:10px; font-weight:600; color:#64748b; background:#f1f5f9;
                border-radius:4px; padding:1px 5px; }}
  .step-quote {{ font-size:10px; font-style:italic; color:#64748b;
                 border-left:2px solid #cbd5e1; padding:3px 7px; margin-top:5px; }}

  /* ── FATHOM TIMESTAMP DROPDOWNS ── */
  .fathom-refs {{ margin-top: 5px; display: flex; flex-direction: column; gap: 3px; }}
  .fathom-dropdown {{ border: 1px solid rgba(91,79,207,0.2); border-radius: 6px;
                      background: rgba(91,79,207,0.04); overflow: visible; }}
  .fathom-dropdown > summary {{ display: flex; align-items: center; gap: 8px; font-size: 10px;
    font-weight: 600; color: #5B4FCF; padding: 4px 8px; cursor: pointer;
    list-style: none; user-select: none; }}
  .fathom-dropdown > summary::-webkit-details-marker {{ display: none; }}
  .fathom-dropdown > summary::before {{ display: none; }}
  .fathom-dropdown > summary::after {{ content: "›"; margin-left: auto; font-size: 14px;
    line-height: 1; transition: transform 0.15s; display: inline-block; }}
  .fathom-dropdown[open] > summary::after {{ transform: rotate(90deg); }}
  .fathom-dropdown:hover {{ background: rgba(91,79,207,0.08); border-color: rgba(91,79,207,0.35); }}
  .ref-label {{ flex: 1; }}
  .ref-time {{ font-size: 9px; color: #8B7FCF; font-weight: 500; font-variant-numeric: tabular-nums; }}
  .fathom-panel {{ padding: 6px 10px 8px; border-top: 1px solid rgba(91,79,207,0.15);
                   display: flex; flex-direction: column; gap: 6px; }}
  .fathom-excerpt {{ font-size: 10px; color: #3D3560; background: rgba(91,79,207,0.05);
    border-left: 2px solid rgba(91,79,207,0.25); margin: 0; padding: 6px 10px;
    border-radius: 0 4px 4px 0; line-height: 1.5; }}
  .tx-line {{ margin-bottom: 3px; }}
  .tx-line:last-child {{ margin-bottom: 0; }}
  .fathom-open-btn {{ align-self: flex-start; font-size: 9px; font-weight: 700; color: #5B4FCF;
    text-decoration: none; background: rgba(91,79,207,0.1); border: 1px solid rgba(91,79,207,0.25);
    border-radius: 4px; padding: 3px 10px; letter-spacing: 0.02em; }}
  .fathom-open-btn:hover {{ background: rgba(91,79,207,0.2); }}

  /* ── EMAIL CITATION LINKS ── */
  .email-refs {{ margin-top: 3px; display: flex; flex-direction: column; gap: 2px; opacity: 0; transition: opacity 0.15s; }}
  .box:hover .email-refs {{ opacity: 1; }}
  .email-link {{ display: inline-block; font-size: 10px; font-weight: 600; color: #1a7f5a;
                 text-decoration: none; background: rgba(26,127,90,0.08);
                 border: 1px solid rgba(26,127,90,0.2); border-radius: 4px;
                 padding: 2px 6px; white-space: nowrap; }}
  .email-link:hover {{ background: rgba(26,127,90,0.15); text-decoration: underline; }}

  /* ── TOOL TAG RECORDING DROPDOWNS ── */
  .tool-dropdown {{ display: inline-block; vertical-align: middle; position: relative; }}
  .tool-dropdown > summary {{ display: inline-flex; align-items: center; gap: 3px; font-size: 10px;
    font-weight: 600; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0;
    padding: 2px 9px; border-radius: 20px; margin-top: 2px; cursor: pointer;
    list-style: none; user-select: none; }}
  .tool-dropdown > summary::-webkit-details-marker {{ display: none; }}
  .tool-dropdown[open] > summary {{ background: #dcfce7; border-color: #86efac;
    border-radius: 10px 10px 0 0; }}
  .tool-dropdown-panel {{ position: absolute; z-index: 20; left: 0; top: 100%;
    background: #f7fef0; border: 1px solid #bbf7d0; border-radius: 0 8px 8px 8px;
    padding: 6px 10px 8px; display: flex; flex-direction: column; gap: 5px;
    min-width: 200px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
  .tool-excerpt {{ font-size: 10px; font-style: italic; color: #166534;
    background: rgba(22,101,52,0.06); border-left: 2px solid rgba(22,101,52,0.3);
    margin: 0; padding: 3px 7px; border-radius: 0 3px 3px 0; line-height: 1.4; }}
  .tool-open-btn {{ align-self: flex-start; font-size: 9px; font-weight: 700; color: #166534;
    text-decoration: none; background: rgba(22,101,52,0.08); border: 1px solid rgba(22,101,52,0.25);
    border-radius: 4px; padding: 2px 8px; }}
  .tool-open-btn:hover {{ background: rgba(22,101,52,0.15); }}

  /* ── PARALLEL GROUP ── */
  .pg-label {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #9CA3AF; text-align: center; margin-bottom: 6px; }}
  .pg-row {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; margin: 4px 0; }}
  .pg-chip {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 8px 12px; font-size: 11px; font-weight: 600; color: #0f1825;
    text-align: center; min-width: 80px; flex: 1 1 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .pg-chip .chip-tool {{ display: block; font-size: 9px; font-weight: 600; color: #166634;
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px;
    padding: 1px 6px; margin-top: 3px; }}
  .pg-chip .chip-owner {{ display: block; font-size: 9px; margin-top: 3px; }}
  .pg-chip .chip-dropdown {{ display: block; margin-top: 4px; }}
  .pg-chip .chip-dropdown > summary {{ display: inline-flex; align-items: center; gap: 3px;
    font-size: 9px; color: #5B4FCF; cursor: pointer; list-style: none; opacity: 0.7; }}
  .pg-chip .chip-dropdown > summary::-webkit-details-marker {{ display: none; }}
  .pg-chip:hover .chip-dropdown > summary {{ opacity: 1; }}
  .pg-chip .chip-panel {{ margin-top: 4px; background: rgba(91,79,207,0.06);
    border: 1px solid rgba(91,79,207,0.2); border-radius: 6px; padding: 5px 8px;
    display: flex; flex-direction: column; gap: 5px; text-align: left; }}
  .pg-chip .chip-excerpt {{ font-size: 9px; font-style: italic; color: #5B4FCF;
    border-left: 2px solid rgba(91,79,207,0.3); padding-left: 5px; margin: 0; line-height: 1.4; }}
  .pg-chip .chip-open-btn {{ align-self: flex-start; font-size: 9px; font-weight: 700;
    color: #5B4FCF; text-decoration: none; background: rgba(91,79,207,0.1);
    border: 1px solid rgba(91,79,207,0.25); border-radius: 4px; padding: 1px 6px; }}
  .pg-merge {{ display: flex; flex-direction: column; align-items: center; }}
  .pg-legs {{ display: flex; justify-content: center; width: 100%; }}
  .pg-leg {{ flex: 1; display: flex; justify-content: center; }}
  .pg-leg .v-line {{ height: 10px; width: 2px; background: #94a3b8; }}
  .pg-crossbar {{ height: 2px; background: #94a3b8; }}
  .pg-drop {{ display: flex; flex-direction: column; align-items: center; }}
  .pg-drop .v-line {{ height: 10px; width: 2px; background: #94a3b8; }}
  .pg-drop .v-tip {{ width: 0; height: 0; border-left: 5px solid transparent;
    border-right: 5px solid transparent; border-top: 7px solid #94a3b8; }}

  /* ── FOOTER NOTE ── */
  .footer-note {{ font-size: 11px; color: #94a3b8; margin-top: 8px; padding-top: 12px;
                  border-top: 1px dashed #e2e8f0; }}

  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .box {{ animation: fadeUp 0.3s ease both; }}

  .step-session {{ font-size: 10px; color: #9CA3AF; font-weight: 500; margin-top: 4px; }}

  /* ── SIDEBAR NAV ── */
  .sidebar-nav {{ position: fixed; top: 0; left: 0; width: 210px; height: 100vh;
    background: rgba(15,24,37,0.97); padding: 20px 0; z-index: 100;
    overflow-y: auto; border-right: 1px solid #1e293b; }}
  .sidebar-nav .nav-header {{ padding: 12px 16px; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; }}
  .sidebar-nav a {{ display: block; padding: 8px 16px; font-size: 12px; font-weight: 500;
    color: #94a3b8; text-decoration: none; border-left: 3px solid transparent;
    transition: all 0.15s; }}
  .sidebar-nav a:hover {{ color: #e2e8f0; background: rgba(255,255,255,0.04); }}
  .sidebar-nav a.active {{ color: #7DFF00; border-left-color: #7DFF00;
    background: rgba(125,255,0,0.06); font-weight: 600; }}
  .sidebar-toggle {{ display: none; position: fixed; top: 12px; left: 12px; z-index: 200;
    background: #0f1825; color: #7DFF00; border: 1px solid #1e293b;
    border-radius: 6px; padding: 8px 10px; cursor: pointer; font-size: 16px; }}
  .apg-header, .subheader, .legend, .people-bar {{ margin-left: 210px; }}
  .canvas {{ margin-left: 210px; }}
  @media (max-width: 768px) {{
    .sidebar-nav {{ transform: translateX(-100%); transition: transform 0.2s; }}
    .sidebar-nav.open {{ transform: translateX(0); }}
    .sidebar-toggle {{ display: block; }}
    .apg-header, .subheader, .legend, .people-bar {{ margin-left: 0; }}
    .canvas {{ margin-left: 0; }}
  }}
</style>
</head>
<body>

{sidebar_html}

<div class="apg-header">
  <div style="display:flex;align-items:center;gap:12px;">
    <img src="{YOUR_LOGO_URL}"
         alt="{YOUR_COMPANY}" style="height:38px;width:auto;display:block;">
    <div>
      <div class="logo">{YOUR_COMPANY}</div>
      <div class="subtitle">Business Operations Audit</div>
    </div>
  </div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:20px;">
    <div style="text-align:right">
      <div style="font-weight:700;font-size:16px">{company}</div>
      <div style="font-size:12px;color:#9CA3AF">Current-State Process Map &middot; {generated}</div>
    </div>
  </div>
</div>

<div class="subheader">
  <h1>Current-State Process Map</h1>
  <div class="meta">{company} &nbsp;&middot;&nbsp; {sessions} session{'s' if sessions != 1 else ''} completed &nbsp;&middot;&nbsp; Generated {generated}</div>
</div>

<div class="legend">
  {legend_html}
</div>

{people_bar_html}

<div class="canvas">
  {zones_html}
  {pain_summary_html}
  {opportunities_html}
  <div class="footer-note">
    Hover over any step to see the source quote from the audit session transcript.
    Dashed borders indicate LOW confidence &mdash; data to be confirmed in a future session.
    Steps with recording references show an expandable dropdown with transcript dialogue &mdash; expand to read context and open the recording at that exact moment.
    Tool tags with &#9654; in the People Bar link to the recording where that tool was discussed.
  </div>
</div>

<script>
/* ── Decision-gate branch connectors (SVG, drawn after layout) ── */
window.addEventListener('load', function() {{
  var C = '#94a3b8', W = 2;
  function svgEl(tag, attrs) {{
    var el = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.keys(attrs).forEach(function(k) {{ el.setAttribute(k, attrs[k]); }});
    return el;
  }}
  document.querySelectorAll('.decision-gate').forEach(function(gate) {{
    var twocol = gate.querySelector('.two-col');
    var spacer = gate.querySelector('.gate-merge-spacer');
    if (!twocol || !spacer) return;
    var cols = twocol.querySelectorAll(':scope > .col');
    if (cols.length !== 2) return;

    var gR = gate.getBoundingClientRect();
    var centerX = gR.width / 2;

    /* Actual bottom-center of each col's last child */
    var colPts = Array.from(cols).map(function(col) {{
      var colR = col.getBoundingClientRect();
      var kids = Array.from(col.children);
      var last = kids.length ? kids[kids.length - 1] : col;
      var lR   = last.getBoundingClientRect();
      return {{ x: colR.left + colR.width / 2 - gR.left, y: lR.bottom - gR.top }};
    }});

    /* Merge Y = bottom of the taller column */
    var mergeY = Math.max(colPts[0].y, colPts[1].y);

    /* Connect Y = bottom of the v-arrow below the gate (SVG overflow:visible handles the gap) */
    var connectY = spacer.getBoundingClientRect().bottom - gR.top;
    var nextEl = gate.nextElementSibling;
    if (nextEl && nextEl.classList.contains('v-arrow')) {{
      connectY = nextEl.getBoundingClientRect().bottom - gR.top;
    }}

    var svg = svgEl('svg', {{
      style: 'position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:visible;z-index:1'
    }});

    colPts.forEach(function(pt) {{
      svg.appendChild(svgEl('line', {{ x1:pt.x, y1:pt.y, x2:pt.x,      y2:mergeY, stroke:C, 'stroke-width':W }}));
      svg.appendChild(svgEl('line', {{ x1:pt.x, y1:mergeY, x2:centerX, y2:mergeY, stroke:C, 'stroke-width':W }}));
    }});

    /* Vertical from merge point down to next v-arrow */
    svg.appendChild(svgEl('line', {{ x1:centerX, y1:mergeY, x2:centerX, y2:connectY, stroke:C, 'stroke-width':W }}));

    gate.appendChild(svg);
  }});
}});

/* ── Sidebar scroll-spy ── */
(function() {{
  var sections = document.querySelectorAll('[id^="zone-"], #pain-points, #opportunities');
  var navLinks = document.querySelectorAll('.sidebar-nav a');
  if (!sections.length || !navLinks.length) return;
  var observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        navLinks.forEach(function(l) {{ l.classList.remove('active'); }});
        var active = document.querySelector('.sidebar-nav a[data-target="' + entry.target.id + '"]');
        if (active) active.classList.add('active');
      }}
    }});
  }}, {{ rootMargin: '-20% 0px -70% 0px' }});
  sections.forEach(function(s) {{ observer.observe(s); }});
  navLinks.forEach(function(link) {{
    link.addEventListener('click', function(e) {{
      e.preventDefault();
      var target = document.getElementById(this.getAttribute('data-target'));
      if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      document.getElementById('sidebarNav').classList.remove('open');
    }});
  }});
}})();
</script>
</body>
</html>"""


# ─── Shared Blueprint Rendering ──────────────────────────────────────────────

def _build_blueprint_renderers(ssad: dict) -> dict:
    """Build reusable rendering closures for blueprint-style side-by-side views.

    Returns a dict of rendering functions that can be used by both the
    transformation blueprint and strategic approaches generators.
    """
    # ── Fathom URL lookup ──
    _fathom_base_url: dict = {}
    for _s in ssad.get("sessions", []):
        _mid = _s.get("fathom_meeting_id", "")
        _furl = _s.get("fathom_url", "")
        if _mid and _furl:
            _fathom_base_url[str(_mid)] = _furl.rstrip("/")

    _client_dir = Path("clients") / ssad.get("client_slug", "")
    _transcripts = _load_client_transcripts(str(_client_dir), ssad.get("sessions", []))

    # ── Owner color map ──
    OWNER_TAG_PALETTE = [
        ("tag-pink", "#d63384"), ("tag-orange", "#c75000"), ("tag-teal", "#0d9488"),
        ("tag-purple", "#7b2fbe"), ("tag-amber", "#d97706"), ("tag-blue", "#2563EB"),
        ("tag-green", "#198754"), ("tag-health", "#0891b2"), ("tag-rose", "#be185d"),
    ]
    _tool_kw = {"automated", "hubspot", "monday", "twilio", "xero", "foundu", "system", "planned",
                "google", "sheets", "zapier", "slack", "notion", "airtable", "asana", "jira",
                "salesforce", "stripe", "quickbooks", "myob", "deputy", "employment hero"}
    owner_color_map: dict = {}
    _palette_idx = 0
    for _proc in ssad.get("processes", []):
        for _step in _proc.get("steps", []):
            _o = _step.get("owner", "").strip()
            if _o and _o not in owner_color_map:
                if any(k in _o.lower() for k in _tool_kw):
                    owner_color_map[_o] = ("tool-tag", None)
                else:
                    _cls, _hex = OWNER_TAG_PALETTE[_palette_idx % len(OWNER_TAG_PALETTE)]
                    owner_color_map[_o] = (_cls, _hex)
                    _palette_idx += 1

    # ── Decision nodes by stage ──
    _decision_nodes_by_stage: dict = {}
    for dn in ssad.get("decision_nodes", []):
        s = dn.get("stage", "")
        _decision_nodes_by_stage.setdefault(s, []).append(dn)

    # ── Stage data ──
    stages = [p["stage"] for p in ssad.get("processes", [])]
    stage_labels, stage_subtitles = _build_stage_lookups(ssad)
    stage_zone = {s: i + 1 for i, s in enumerate(stages)}

    processes_by_stage = {}
    for proc in ssad.get("processes", []):
        processes_by_stage[proc["stage"]] = proc.get("steps", [])

    # ── Flow label styles ──
    _FLOW_STYLES = {
        "automated_sync": ("#10B981", "Auto-sync"), "api_integration": ("#10B981", "API"),
        "manual_entry": ("#EF4444", "Manual"), "manual_check": ("#EF4444", "Manual check"),
        "email_notification": ("#F59E0B", "Email"), "csv_export": ("#F59E0B", "CSV"),
        "verbal": ("#9CA3AF", "Verbal"), "unknown": ("#9CA3AF", "?"),
    }

    # ── Rendering functions ──
    def render_email_refs(email_references: list) -> str:
        if not email_references:
            return ""
        links = []
        for ref in email_references:
            filename = ref.get("filename", "").strip()
            subject = ref.get("subject", "").strip()
            excerpt = ref.get("excerpt", "").strip()
            if not filename:
                continue
            label = subject or filename
            href = f"../emails/{escape(filename)}"
            title_attr = f' title="{escape(excerpt)}"' if excerpt else ""
            links.append(
                f'<a class="email-link" href="{href}" target="_blank" rel="noopener"{title_attr}>'
                f'&#128231; {escape(label)}</a>'
            )
        if not links:
            return ""
        return f'<div class="email-refs">{"".join(links)}</div>'

    def render_meeting_refs(meeting_references: list, source_quote: str = "") -> str:
        if not meeting_references:
            return ""
        items_html = []
        for ref in meeting_references:
            meeting_id = ref.get("meeting_id", "")
            ts = ref.get("timestamp_seconds")
            label = ref.get("label", "")
            if not meeting_id or ts is None:
                continue
            minutes = int(ts) // 60
            seconds = int(ts) % 60
            time_str = f"{minutes}:{seconds:02d}"
            short_label = label or "Meeting ref"
            _base = _fathom_base_url.get(str(meeting_id), f"https://{FATHOM_URL}/calls/{meeting_id}")
            resolved_ts = _find_best_transcript_match(_transcripts, meeting_id, int(ts), hint_text=source_quote)
            href = f"{_base}?t={resolved_ts}"
            excerpt_text = (
                ref.get("transcript_excerpt", "").strip()
                or _extract_transcript_window(_transcripts, meeting_id, int(ts), hint_text=source_quote)
                or source_quote
            )
            if excerpt_text:
                lines_html = "".join(
                    f'<div class="tx-line">{escape(line)}</div>'
                    for line in excerpt_text.splitlines() if line.strip()
                )
                excerpt_html = f'<div class="fathom-excerpt">{lines_html}</div>'
            else:
                excerpt_html = ""
            items_html.append(
                f'<details class="fathom-dropdown">'
                f'<summary><span class="ref-label">{escape(short_label)}</span>'
                f'<span class="ref-time">{time_str}</span></summary>'
                f'<div class="fathom-panel">{excerpt_html}'
                f'<a class="fathom-open-btn" href="{href}" target="_blank" rel="noopener">'
                f'&#9654; Open Recording</a></div></details>'
            )
        if not items_html:
            return ""
        return f'<div class="fathom-refs">{"".join(items_html)}</div>'

    def render_step(step: dict, zn: int = 1) -> str:
        stype = step.get("type", "step")
        desc = escape(step.get("description", ""))
        owner_raw = step.get("owner", "").strip()
        owner = escape(owner_raw)
        conf = step.get("confidence", "LOW")
        quote = escape(_norm_quote(step.get("source_quote", "")))
        session = step.get("source_session", "")
        speaker = escape(step.get("source_speaker", ""))
        meeting_refs = step.get("meeting_references") or []
        email_refs = step.get("email_references") or []
        if stype == "step":
            box_class = f"step step-z{zn}"
        else:
            box_class_map = {"decision": "decision-box", "pain": "pain-box",
                             "optimisation": "opp-box", "automation": "auto-box"}
            box_class = box_class_map.get(stype, "step")
        low_conf_style = "border-style:dashed!important;" if conf == "LOW" else ""
        tooltip = ""
        if quote:
            source_info = f"Session {session}" if session else ""
            if speaker:
                source_info += f" · {speaker}"
            q_text = quote[:120] + ("..." if len(quote) > 120 else "")
            tooltip_text = f"{source_info}: {q_text}" if source_info else q_text
            tooltip = f'title="{tooltip_text}"'
        if owner_raw:
            tag_cls, _ = owner_color_map.get(owner_raw, ("person-tag", None))
            owner_html = f'<div class="box-body"><span class="person-tag {tag_cls}">{owner}</span></div>'
        else:
            owner_html = ""
        tool_ids = step.get("tool_ids") or []
        if tool_ids:
            tool_pills = "".join(f'<span class="step-tool-tag">{escape(t)}</span>' for t in tool_ids)
            tools_html = f'<div class="step-tools">{tool_pills}</div>'
        else:
            tools_html = ""
        sq = step.get("source_quote", "") or step.get("source_quotes", "")
        if isinstance(sq, list):
            sq = " ".join(sq)
        meeting_refs_html = render_meeting_refs(meeting_refs, sq)
        email_refs_html = render_email_refs(email_refs)
        meta_parts = []
        if step.get("duration_minutes"):
            meta_parts.append(f"{step['duration_minutes']} min")
        if step.get("frequency"):
            meta_parts.append(escape(str(step["frequency"])))
        meta_html = (
            '<div class="step-meta">' +
            "".join(f'<span class="meta-chip">{p}</span>' for p in meta_parts) +
            '</div>'
        ) if meta_parts else ""
        quote_html = ""
        if quote:
            session_badge = f'<span class="step-session">Session {session}</span>' if session else ""
            quote_html = f'<div class="step-quote">&ldquo;{quote}&rdquo;{session_badge}</div>'
        return f"""
        <div class="box {box_class} process-step" {tooltip}
             style="{low_conf_style}">
          <div class="box-title">{desc}</div>
          {owner_html}
          {tools_html}
          {meta_html}
          {quote_html}
          {meeting_refs_html}
          {email_refs_html}
        </div>"""

    def render_parallel_group(step: dict, zn: int = 1) -> str:
        items = step.get("items") or []
        label = escape(step.get("description", ""))
        conf = step.get("confidence", "LOW")
        low_conf = "border-style:dashed!important;" if conf == "LOW" else ""
        chip_parts = []
        for item in items:
            if isinstance(item, str):
                item = {"label": item}
            lbl = escape(item.get("label", ""))
            tool = item.get("tool", "") or ""
            item_owner = item.get("owner", "") or ""
            q = escape(_norm_quote(item.get("source_quote") or "").strip())
            title_attr = f' title="{q}"' if q else ""
            refs = item.get("meeting_references") or []
            link_html = ""
            if refs and refs[0].get("meeting_id") and refs[0].get("timestamp_seconds") is not None:
                _mid0 = str(refs[0]['meeting_id'])
                _base0 = _fathom_base_url.get(_mid0, f"https://{FATHOM_URL}/calls/{_mid0}")
                _url = f"{_base0}?t={int(refs[0]['timestamp_seconds'])}"
                _item_quote = _norm_quote(item.get("source_quote") or "").strip()
                _chip_excerpt = f'<p class="chip-excerpt">{escape(_item_quote)}</p>' if _item_quote else ""
                link_html = (
                    f'<details class="chip-dropdown">'
                    f'<summary>▶ Recording</summary>'
                    f'<div class="chip-panel">{_chip_excerpt}'
                    f'<a class="chip-open-btn" href="{_base0}?t={int(refs[0]["timestamp_seconds"])}" target="_blank" rel="noopener">Open Recording &#8599;</a>'
                    f'</div></details>'
                )
            tool_html = f'<span class="chip-tool">{escape(tool)}</span>' if tool else ""
            owner_html = f'<span class="chip-owner person-tag">{escape(item_owner)}</span>' if item_owner else ""
            chip_parts.append(
                f'<div class="pg-chip"{title_attr}>{lbl}{tool_html}{owner_html}{link_html}</div>'
            )
        n = max(len(items), 1)
        crossbar_pct = round((n - 1) / n * 100, 1) if n > 1 else 0
        legs = "".join(f'<div class="pg-leg"><div class="v-line"></div></div>' for _ in range(n))
        return f"""
        <div class="process-step" style="{low_conf}">
          <div class="pg-label">{label}</div>
          <div class="pg-row">{"".join(chip_parts)}</div>
          <div class="pg-merge">
            <div class="pg-legs">{legs}</div>
            <div class="pg-crossbar" style="width:{crossbar_pct}%"></div>
            <div class="pg-drop"><div class="v-line"></div><div class="v-tip"></div></div>
          </div>
        </div>"""

    def _render_bp_branch_seq(step_ids: list, steps_by_id: dict, zn: int) -> str:
        v_tip = '<div class="v-arrow"><div class="v-line" style="height:10px;"></div><div class="v-tip"></div></div>'
        parts = []
        for j, sid in enumerate(step_ids):
            s = steps_by_id.get(sid)
            if not s:
                continue
            if s.get("type") == "optimisation":
                continue
            if s.get("type") == "parallel_group":
                parts.append(render_parallel_group(s, zn=zn))
            else:
                parts.append(render_step(s, zn=zn))
            if j < len(step_ids) - 1:
                parts.append(v_tip)
        return "\n".join(parts)

    def render_decision_gate(node: dict, steps_by_id: dict = None, zn: int = 1) -> str:
        condition = escape(node.get("condition", ""))
        yes = escape(node.get("yes_path", ""))
        no = escape(node.get("no_path", ""))
        v_tip = '<div class="v-arrow"><div class="v-line" style="height:8px;"></div><div class="v-tip"></div></div>'
        _steps_by_id = steps_by_id or {}
        no_branch_ids = node.get("no_branch_step_ids") or []
        yes_branch_ids = node.get("yes_branch_step_ids") or []
        yes_col_html = (_render_bp_branch_seq(yes_branch_ids, _steps_by_id, zn)
                        if yes_branch_ids
                        else f'<div class="box branch-yes-box"><div class="box-title">{yes}</div></div>')
        no_col_html = (_render_bp_branch_seq(no_branch_ids, _steps_by_id, zn)
                       if no_branch_ids
                       else f'<div class="box branch-no-box"><div class="box-title">{no}</div></div>')
        return f"""
        <div class="decision-gate">
          <div class="gate-condition">&#11042; {condition}</div>
          <div class="two-col" style="margin-top:10px;align-items:start;">
            <div class="col"><span class="fork-label yes">&#10003; Yes</span>{v_tip}{yes_col_html}</div>
            <div class="col"><span class="fork-label no">&#10007; No</span>{v_tip}{no_col_html}</div>
          </div>
          <div class="gate-merge-spacer"></div>
        </div>"""

    def render_labeled_arrow(data_flow: dict) -> str:
        mechanism = data_flow.get("mechanism", "unknown")
        color, label = _FLOW_STYLES.get(mechanism, ("#9CA3AF", mechanism.replace("_", " ").title()))
        return (
            f'<div class="v-arrow labeled-arrow">'
            f'<div class="v-line" style="height:6px;background:{color}"></div>'
            f'<span class="flow-label" style="color:{color};border-color:{color}">{escape(label)}</span>'
            f'<div class="v-line" style="height:6px;background:{color}"></div>'
            f'<div class="v-tip" style="border-top-color:{color}"></div>'
            f'</div>'
        )

    def render_change_card(ch: dict, steps_by_id: dict, tool_override: str = None,
                           tool_description: str = None,
                           uncovered: bool = False, uncovered_reason: str = "") -> str:
        """Render a change card for the right column.

        tool_override: if set, replaces future_step_tools with this single tool name.
        tool_description: if set, replaces the future_step_description with this text.
        uncovered: if True, renders as greyed-out NOT COVERED card.
        """
        cid = ch.get("change_id", "")
        title = escape(ch.get("title", ""))
        ctype = ch.get("change_type", "automate")

        if uncovered:
            badge_label = "NOT COVERED"
            border_color = "#9CA3AF"
            bg_color = "#F3F4F6"
        else:
            badge_label, border_color, bg_color = CHANGE_BADGE.get(ctype, ("CHANGED", "#6B7280", "#F3F4F6"))

        # Affected steps
        affected_ids = ch.get("affected_step_ids", [])
        steps_html_parts = []
        for sid in affected_ids:
            s = steps_by_id.get(sid)
            if not s:
                continue
            step_desc = escape(s.get("description", ""))
            steps_html_parts.append(
                f'<div style="font-size:11px;color:#475569;padding:3px 0;border-bottom:1px solid rgba(0,0,0,0.05)">'
                f'<span style="color:#9CA3AF;font-size:10px;font-weight:600;margin-right:4px">{escape(sid)}</span> {step_desc}</div>'
            )
        steps_list_html = "".join(steps_html_parts) if steps_html_parts else ""

        # Future description
        if uncovered:
            future_html = f'<div style="margin-top:8px;font-size:12px;color:#9CA3AF;font-style:italic;padding:8px 10px;background:#f7f9fc;border-left:3px solid #CBD5E1;border-radius:0 6px 6px 0">{escape(uncovered_reason) if uncovered_reason else "No tool available in this approach"}</div>'
        else:
            future_desc = tool_description or ch.get("future_step_description", "") or ch.get("proposed_solution", "") or ch.get("proposed_step_description", "")
            future_html = ""
            if future_desc:
                future_html = f'<div style="margin-top:8px;font-size:12px;color:#0f1825;font-weight:500;padding:8px 10px;background:rgba(125,255,0,0.06);border-left:3px solid #7DFF00;border-radius:0 6px 6px 0">{escape(future_desc)}</div>'

        # Tools
        if uncovered:
            tool_html = ""
        elif tool_override:
            tool_html = f'<div style="margin-top:6px"><span style="background:#E0F2FE;color:#0369A1;border-radius:4px;padding:2px 8px;font-size:10px;margin-right:3px;font-weight:600">{escape(tool_override)}</span></div>'
        else:
            future_tools = ch.get("future_step_tools", []) or ch.get("proposed_tools", [])
            tool_html = ""
            if future_tools:
                pills = "".join(
                    f'<span style="background:#E0F2FE;color:#0369A1;border-radius:4px;padding:2px 8px;font-size:10px;margin-right:3px;font-weight:600">{escape(t)}</span>'
                    for t in future_tools
                )
                tool_html = f'<div style="margin-top:6px">{pills}</div>'

        # Value & weeks metadata
        value = ch.get("value") or {}
        impl = ch.get("implementation") or {}
        annual_val = value.get("combined_annual_value_aud", 0)
        weeks = impl.get("weeks_label", "")
        phase = ch.get("phase", "")
        meta_parts = []
        if annual_val:
            meta_parts.append(f'<span style="background:#D1FAE5;color:#065F46;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700">${annual_val:,.0f}/yr</span>')
        if weeks:
            meta_parts.append(f'<span style="background:#DBEAFE;color:#1E40AF;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700">{escape(weeks)}</span>')
        if phase:
            meta_parts.append(f'<span style="background:#F3F4F6;color:#374151;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">Phase {phase}</span>')
        meta_html = f'<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">{"".join(meta_parts)}</div>' if meta_parts else ""

        opacity_style = "opacity:0.5;" if uncovered else ""

        return f"""<div style="background:{bg_color};border:2px solid {border_color};border-radius:10px;
                   padding:14px 16px;margin-bottom:12px;font-size:12px;position:relative;
                   box-shadow:0 1px 4px rgba(0,0,0,0.06);{opacity_style}">
                   <span style="position:absolute;top:10px;right:10px;background:{border_color};color:#fff;
                     font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;letter-spacing:0.02em">{badge_label}</span>
                   <div style="font-weight:700;font-size:14px;color:#0f1825;padding-right:90px;margin-bottom:6px">{title}</div>
                   <div style="margin-bottom:4px">{steps_list_html}</div>
                   {future_html}
                   {tool_html}
                   {meta_html}
                   </div>"""

    def render_left_column(steps: list, stage: str, change_by_step: dict) -> str:
        """Render the left (current state) column for a blueprint zone."""
        zn = stage_zone.get(stage, 1)
        zn = max(1, min(zn, 9))
        nodes_by_step: dict = {}
        nodes_unanchored: list = []
        for dn in _decision_nodes_by_stage.get(stage, []):
            anchor = dn.get("after_step_id", "").strip()
            if anchor:
                nodes_by_step.setdefault(anchor, []).append(dn)
            else:
                nodes_unanchored.append(dn)
        steps_by_id: dict = {s.get("step_id", ""): s for s in steps}
        v_arrow = '<div class="v-arrow"><div class="v-line" style="height:14px;"></div><div class="v-tip"></div></div>'

        left_parts = []
        prev_pg = False
        for i, s in enumerate(steps):
            if s.get("branch_only"):
                continue
            if s.get("type") == "optimisation":
                continue
            sid = s.get("step_id", "")
            changes = change_by_step.get(sid, [])
            change_indicator = ""
            if changes:
                ctype = changes[0].get("change_type", "automate")
                _, border_color, _ = CHANGE_BADGE.get(ctype, ("", "#6B7280", ""))
                change_indicator = f'<div style="position:absolute;left:0;top:0;bottom:0;width:4px;background:{border_color};border-radius:10px 0 0 10px"></div>'

            if s.get("type") == "parallel_group":
                step_html = render_parallel_group(s, zn=zn)
                if changes:
                    step_html = step_html.replace('class="process-step"', f'class="process-step" style="position:relative"', 1)
                    step_html = step_html.replace('<div class="pg-label">', f'{change_indicator}<div class="pg-label">', 1)
                left_parts.append(step_html)
                prev_pg = True
            else:
                step_html = render_step(s, zn=zn)
                if changes:
                    step_html = f'<div style="position:relative">{change_indicator}{step_html}</div>'
                left_parts.append(step_html)
                prev_pg = False
            for dn in nodes_by_step.get(sid, []):
                left_parts.append(v_arrow)
                left_parts.append(render_decision_gate(dn, steps_by_id=steps_by_id, zn=zn))
            if s.get("type") == "decision" and nodes_unanchored:
                left_parts.append(render_decision_gate(nodes_unanchored.pop(0), steps_by_id=steps_by_id, zn=zn))
            if i < len(steps) - 1 and not prev_pg:
                next_flow = None
                for ns in steps[i + 1:]:
                    if not ns.get("branch_only"):
                        next_flow = ns.get("data_flow")
                        break
                if next_flow and next_flow.get("mechanism"):
                    left_parts.append(render_labeled_arrow(next_flow))
                else:
                    left_parts.append(v_arrow)
        for dn in nodes_unanchored:
            left_parts.append(v_arrow)
            left_parts.append(render_decision_gate(dn, steps_by_id=steps_by_id, zn=zn))
        return "\n".join(left_parts)

    def render_blueprint_zone(stage: str, change_by_step: dict,
                              tool_overrides: dict = None,
                              tool_descriptions: dict = None,
                              uncovered_map: dict = None) -> str:
        """Render a single blueprint zone (one process stage).

        tool_overrides: dict mapping change_id -> tool name string.
        tool_descriptions: dict mapping change_id -> detailed description string.
        uncovered_map: dict mapping change_id -> reason string.
        """
        steps = processes_by_stage.get(stage, [])
        label = stage_labels.get(stage, stage.replace("_", " ").title())
        subtitle = stage_subtitles.get(stage, "")
        accent = STAGE_ACCENT_DEFAULT
        zn = stage_zone.get(stage, 1)
        zn = max(1, min(zn, 9))

        if not steps:
            return ""

        steps_by_id: dict = {s.get("step_id", ""): s for s in steps}

        # Left column
        left_html = render_left_column(steps, stage, change_by_step)

        # Right column — collect unique changes in this stage
        seen_change_ids = set()
        stage_changes_ordered = []
        for s in steps:
            if s.get("branch_only"):
                continue
            sid = s.get("step_id", "")
            for ch in change_by_step.get(sid, []):
                cid = ch.get("change_id", "")
                if cid and cid not in seen_change_ids:
                    seen_change_ids.add(cid)
                    stage_changes_ordered.append(ch)

        right_parts = []
        _uncovered_map = uncovered_map or {}
        _tool_overrides = tool_overrides or {}
        _tool_descriptions = tool_descriptions or {}
        for ch in stage_changes_ordered:
            cid = ch.get("change_id", "")
            if cid in _uncovered_map:
                right_parts.append(render_change_card(ch, steps_by_id, uncovered=True,
                                                      uncovered_reason=_uncovered_map[cid]))
            elif cid in _tool_overrides:
                right_parts.append(render_change_card(ch, steps_by_id,
                                                      tool_override=_tool_overrides[cid],
                                                      tool_description=_tool_descriptions.get(cid)))
            else:
                right_parts.append(render_change_card(ch, steps_by_id))

        right_html = "\n".join(right_parts) if right_parts else '<div style="padding:20px;text-align:center;color:#9CA3AF;font-size:12px;font-style:italic">No changes proposed for this stage</div>'

        # Badge
        stage_changes = set()
        for s in steps:
            sid = s.get("step_id", "")
            for ch in change_by_step.get(sid, []):
                stage_changes.add(ch.get("change_id", ""))
        change_count = len(stage_changes)
        badge = f"{change_count} change{'s' if change_count != 1 else ''}" if change_count else "no changes"

        return f"""
        <div class="bp-zone" id="bp-zone-{stage}">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <div style="border-left:4px solid {accent};padding-left:12px">
              <div style="font-size:18px;font-weight:800;color:#0f1825;letter-spacing:-0.02em">{escape(label)}</div>
              <div style="font-size:11px;color:#64748b">{escape(subtitle)}</div>
            </div>
            <span style="font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;
                  letter-spacing:0.5px;text-transform:uppercase;color:#64748b;background:#f1f5f9;
                  border:1px solid #e2e8f0;margin-left:auto">{badge}</span>
          </div>
          <div class="bp-columns">
            <div class="bp-col">
              <div class="bp-col-header" style="border-color:#EF4444;color:#EF4444">Current State</div>
              {left_html}
            </div>
            <div class="bp-col">
              <div class="bp-col-header" style="border-color:#10B981;color:#10B981">What Changes</div>
              {right_html}
            </div>
          </div>
        </div>"""

    return {
        "render_email_refs": render_email_refs,
        "render_meeting_refs": render_meeting_refs,
        "render_step": render_step,
        "render_parallel_group": render_parallel_group,
        "render_decision_gate": render_decision_gate,
        "render_labeled_arrow": render_labeled_arrow,
        "render_change_card": render_change_card,
        "render_left_column": render_left_column,
        "render_blueprint_zone": render_blueprint_zone,
        "_render_bp_branch_seq": _render_bp_branch_seq,
        # Context data
        "stages": stages,
        "stage_labels": stage_labels,
        "stage_subtitles": stage_subtitles,
        "stage_zone": stage_zone,
        "processes_by_stage": processes_by_stage,
        "owner_color_map": owner_color_map,
        "fathom_base_url": _fathom_base_url,
        "transcripts": _transcripts,
        "decision_nodes_by_stage": _decision_nodes_by_stage,
    }


# ─── Transformation Blueprint Generator ────────────────────────────────────────

def generate_transformation_blueprint(ssad: dict) -> str:
    """Generate transformation-blueprint.html — side-by-side current vs future process map."""
    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    blueprint = ssad.get("transformation_blueprint", {})
    proposed_changes = ssad.get("proposed_changes", [])
    change_by_step = _build_change_lookup(proposed_changes)

    # Build stage ordering from audit data
    stages = [p["stage"] for p in ssad.get("processes", [])]
    stage_labels, stage_subtitles = _build_stage_lookups(ssad)
    stage_zone = {s: i + 1 for i, s in enumerate(stages)}

    processes_by_stage = {}
    for proc in ssad.get("processes", []):
        processes_by_stage[proc["stage"]] = proc.get("steps", [])

    # ── Fathom URL lookup (same as process map) ──
    _fathom_base_url: dict = {}
    for _s in ssad.get("sessions", []):
        _mid = _s.get("fathom_meeting_id", "")
        _furl = _s.get("fathom_url", "")
        if _mid and _furl:
            _fathom_base_url[str(_mid)] = _furl.rstrip("/")

    _client_dir = Path("clients") / ssad.get("client_slug", "")
    _transcripts = _load_client_transcripts(str(_client_dir), ssad.get("sessions", []))

    # ── Owner color map (same as process map) ──
    OWNER_TAG_PALETTE = [
        ("tag-pink", "#d63384"), ("tag-orange", "#c75000"), ("tag-teal", "#0d9488"),
        ("tag-purple", "#7b2fbe"), ("tag-amber", "#d97706"), ("tag-blue", "#2563EB"),
        ("tag-green", "#198754"), ("tag-health", "#0891b2"), ("tag-rose", "#be185d"),
    ]
    _tool_kw = {"automated", "hubspot", "monday", "twilio", "xero", "foundu", "system", "planned",
                "google", "sheets", "zapier", "slack", "notion", "airtable", "asana", "jira",
                "salesforce", "stripe", "quickbooks", "myob", "deputy", "employment hero"}
    owner_color_map: dict = {}
    _palette_idx = 0
    for _proc in ssad.get("processes", []):
        for _step in _proc.get("steps", []):
            _o = _step.get("owner", "").strip()
            if _o and _o not in owner_color_map:
                if any(k in _o.lower() for k in _tool_kw):
                    owner_color_map[_o] = ("tool-tag", None)
                else:
                    _cls, _hex = OWNER_TAG_PALETTE[_palette_idx % len(OWNER_TAG_PALETTE)]
                    owner_color_map[_o] = (_cls, _hex)
                    _palette_idx += 1

    # ── Decision nodes by stage ──
    _decision_nodes_by_stage: dict = {}
    for dn in ssad.get("decision_nodes", []):
        s = dn.get("stage", "")
        _decision_nodes_by_stage.setdefault(s, []).append(dn)

    # ── Inner render functions (same as process map for left column) ──

    def render_email_refs(email_references: list) -> str:
        if not email_references:
            return ""
        links = []
        for ref in email_references:
            filename = ref.get("filename", "").strip()
            subject = ref.get("subject", "").strip()
            excerpt = ref.get("excerpt", "").strip()
            if not filename:
                continue
            label = subject or filename
            href = f"../emails/{escape(filename)}"
            title_attr = f' title="{escape(excerpt)}"' if excerpt else ""
            links.append(
                f'<a class="email-link" href="{href}" target="_blank" rel="noopener"{title_attr}>'
                f'&#128231; {escape(label)}</a>'
            )
        if not links:
            return ""
        return f'<div class="email-refs">{"".join(links)}</div>'

    def render_meeting_refs(meeting_references: list, source_quote: str = "") -> str:
        if not meeting_references:
            return ""
        items_html = []
        for ref in meeting_references:
            meeting_id = ref.get("meeting_id", "")
            ts = ref.get("timestamp_seconds")
            label = ref.get("label", "")
            if not meeting_id or ts is None:
                continue
            minutes = int(ts) // 60
            seconds = int(ts) % 60
            time_str = f"{minutes}:{seconds:02d}"
            short_label = label or "Meeting ref"
            _base = _fathom_base_url.get(str(meeting_id), f"https://{FATHOM_URL}/calls/{meeting_id}")
            resolved_ts = _find_best_transcript_match(_transcripts, meeting_id, int(ts), hint_text=source_quote)
            href = f"{_base}?t={resolved_ts}"
            excerpt_text = (
                ref.get("transcript_excerpt", "").strip()
                or _extract_transcript_window(_transcripts, meeting_id, int(ts), hint_text=source_quote)
                or source_quote
            )
            if excerpt_text:
                lines_html = "".join(
                    f'<div class="tx-line">{escape(line)}</div>'
                    for line in excerpt_text.splitlines() if line.strip()
                )
                excerpt_html = f'<div class="fathom-excerpt">{lines_html}</div>'
            else:
                excerpt_html = ""
            items_html.append(
                f'<details class="fathom-dropdown">'
                f'<summary><span class="ref-label">{escape(short_label)}</span>'
                f'<span class="ref-time">{time_str}</span></summary>'
                f'<div class="fathom-panel">{excerpt_html}'
                f'<a class="fathom-open-btn" href="{href}" target="_blank" rel="noopener">'
                f'&#9654; Open Recording</a></div></details>'
            )
        if not items_html:
            return ""
        return f'<div class="fathom-refs">{"".join(items_html)}</div>'

    def render_step(step: dict, zn: int = 1) -> str:
        stype = step.get("type", "step")
        desc = escape(step.get("description", ""))
        owner_raw = step.get("owner", "").strip()
        owner = escape(owner_raw)
        conf = step.get("confidence", "LOW")
        quote = escape(_norm_quote(step.get("source_quote", "")))
        session = step.get("source_session", "")
        speaker = escape(step.get("source_speaker", ""))
        meeting_refs = step.get("meeting_references") or []
        email_refs = step.get("email_references") or []
        if stype == "step":
            box_class = f"step step-z{zn}"
        else:
            box_class_map = {"decision": "decision-box", "pain": "pain-box",
                             "optimisation": "opp-box", "automation": "auto-box"}
            box_class = box_class_map.get(stype, "step")
        low_conf_style = "border-style:dashed!important;" if conf == "LOW" else ""
        tooltip = ""
        if quote:
            source_info = f"Session {session}" if session else ""
            if speaker:
                source_info += f" · {speaker}"
            q_text = quote[:120] + ("..." if len(quote) > 120 else "")
            tooltip_text = f"{source_info}: {q_text}" if source_info else q_text
            tooltip = f'title="{tooltip_text}"'
        if owner_raw:
            tag_cls, _ = owner_color_map.get(owner_raw, ("person-tag", None))
            owner_html = f'<div class="box-body"><span class="person-tag {tag_cls}">{owner}</span></div>'
        else:
            owner_html = ""
        tool_ids = step.get("tool_ids") or []
        if tool_ids:
            tool_pills = "".join(f'<span class="step-tool-tag">{escape(t)}</span>' for t in tool_ids)
            tools_html = f'<div class="step-tools">{tool_pills}</div>'
        else:
            tools_html = ""
        sq = step.get("source_quote", "") or step.get("source_quotes", "")
        if isinstance(sq, list):
            sq = " ".join(sq)
        meeting_refs_html = render_meeting_refs(meeting_refs, sq)
        email_refs_html = render_email_refs(email_refs)
        meta_parts = []
        if step.get("duration_minutes"):
            meta_parts.append(f"{step['duration_minutes']} min")
        if step.get("frequency"):
            meta_parts.append(escape(str(step["frequency"])))
        meta_html = (
            '<div class="step-meta">' +
            "".join(f'<span class="meta-chip">{p}</span>' for p in meta_parts) +
            '</div>'
        ) if meta_parts else ""
        quote_html = ""
        if quote:
            session_badge = f'<span class="step-session">Session {session}</span>' if session else ""
            quote_html = f'<div class="step-quote">&ldquo;{quote}&rdquo;{session_badge}</div>'
        return f"""
        <div class="box {box_class} process-step" {tooltip}
             style="{low_conf_style}">
          <div class="box-title">{desc}</div>
          {owner_html}
          {tools_html}
          {meta_html}
          {quote_html}
          {meeting_refs_html}
          {email_refs_html}
        </div>"""

    def render_parallel_group(step: dict, zn: int = 1) -> str:
        items = step.get("items") or []
        label = escape(step.get("description", ""))
        conf = step.get("confidence", "LOW")
        low_conf = "border-style:dashed!important;" if conf == "LOW" else ""
        chip_parts = []
        for item in items:
            if isinstance(item, str):
                item = {"label": item}
            lbl = escape(item.get("label", ""))
            tool = item.get("tool", "") or ""
            item_owner = item.get("owner", "") or ""
            q = escape(_norm_quote(item.get("source_quote") or "").strip())
            title_attr = f' title="{q}"' if q else ""
            refs = item.get("meeting_references") or []
            link_html = ""
            if refs and refs[0].get("meeting_id") and refs[0].get("timestamp_seconds") is not None:
                _mid0 = str(refs[0]['meeting_id'])
                _base0 = _fathom_base_url.get(_mid0, f"https://{FATHOM_URL}/calls/{_mid0}")
                _url = f"{_base0}?t={int(refs[0]['timestamp_seconds'])}"
                _item_quote = _norm_quote(item.get("source_quote") or "").strip()
                _chip_excerpt = f'<p class="chip-excerpt">{escape(_item_quote)}</p>' if _item_quote else ""
                link_html = (
                    f'<details class="chip-dropdown">'
                    f'<summary>▶ Recording</summary>'
                    f'<div class="chip-panel">{_chip_excerpt}'
                    f'<a class="chip-open-btn" href="{_url}" target="_blank" rel="noopener">Open Recording &#8599;</a>'
                    f'</div></details>'
                )
            tool_html = f'<span class="chip-tool">{escape(tool)}</span>' if tool else ""
            owner_html = f'<span class="chip-owner person-tag">{escape(item_owner)}</span>' if item_owner else ""
            chip_parts.append(
                f'<div class="pg-chip"{title_attr}>{lbl}{tool_html}{owner_html}{link_html}</div>'
            )
        n = max(len(items), 1)
        crossbar_pct = round((n - 1) / n * 100, 1) if n > 1 else 0
        legs = "".join(f'<div class="pg-leg"><div class="v-line"></div></div>' for _ in range(n))
        return f"""
        <div class="process-step" style="{low_conf}">
          <div class="pg-label">{label}</div>
          <div class="pg-row">{"".join(chip_parts)}</div>
          <div class="pg-merge">
            <div class="pg-legs">{legs}</div>
            <div class="pg-crossbar" style="width:{crossbar_pct}%"></div>
            <div class="pg-drop"><div class="v-line"></div><div class="v-tip"></div></div>
          </div>
        </div>"""

    def render_decision_gate(node: dict, steps_by_id: dict = None, zn: int = 1) -> str:
        condition = escape(node.get("condition", ""))
        yes = escape(node.get("yes_path", ""))
        no = escape(node.get("no_path", ""))
        v_tip = '<div class="v-arrow"><div class="v-line" style="height:8px;"></div><div class="v-tip"></div></div>'
        _steps_by_id = steps_by_id or {}
        no_branch_ids = node.get("no_branch_step_ids") or []
        yes_branch_ids = node.get("yes_branch_step_ids") or []
        yes_col_html = (_render_bp_branch_seq(yes_branch_ids, _steps_by_id, zn)
                        if yes_branch_ids
                        else f'<div class="box branch-yes-box"><div class="box-title">{yes}</div></div>')
        no_col_html = (_render_bp_branch_seq(no_branch_ids, _steps_by_id, zn)
                       if no_branch_ids
                       else f'<div class="box branch-no-box"><div class="box-title">{no}</div></div>')
        return f"""
        <div class="decision-gate">
          <div class="gate-condition">&#11042; {condition}</div>
          <div class="two-col" style="margin-top:10px;align-items:start;">
            <div class="col"><span class="fork-label yes">&#10003; Yes</span>{v_tip}{yes_col_html}</div>
            <div class="col"><span class="fork-label no">&#10007; No</span>{v_tip}{no_col_html}</div>
          </div>
          <div class="gate-merge-spacer"></div>
        </div>"""

    def _render_bp_branch_seq(step_ids: list, steps_by_id: dict, zn: int) -> str:
        v_tip = '<div class="v-arrow"><div class="v-line" style="height:10px;"></div><div class="v-tip"></div></div>'
        parts = []
        for j, sid in enumerate(step_ids):
            s = steps_by_id.get(sid)
            if not s:
                continue
            if s.get("type") == "optimisation":
                continue
            if s.get("type") == "parallel_group":
                parts.append(render_parallel_group(s, zn=zn))
            else:
                parts.append(render_step(s, zn=zn))
            if j < len(step_ids) - 1:
                parts.append(v_tip)
        return "\n".join(parts)

    _FLOW_STYLES = {
        "automated_sync": ("#10B981", "Auto-sync"), "api_integration": ("#10B981", "API"),
        "manual_entry": ("#EF4444", "Manual"), "manual_check": ("#EF4444", "Manual check"),
        "email_notification": ("#F59E0B", "Email"), "csv_export": ("#F59E0B", "CSV"),
        "verbal": ("#9CA3AF", "Verbal"), "unknown": ("#9CA3AF", "?"),
    }

    def render_labeled_arrow(data_flow: dict) -> str:
        mechanism = data_flow.get("mechanism", "unknown")
        color, label = _FLOW_STYLES.get(mechanism, ("#9CA3AF", mechanism.replace("_", " ").title()))
        return (
            f'<div class="v-arrow labeled-arrow">'
            f'<div class="v-line" style="height:6px;background:{color}"></div>'
            f'<span class="flow-label" style="color:{color};border-color:{color}">{escape(label)}</span>'
            f'<div class="v-line" style="height:6px;background:{color}"></div>'
            f'<div class="v-tip" style="border-top-color:{color}"></div>'
            f'</div>'
        )

    # ── Future-state rendering for the right column ──

    def render_change_card(ch: dict, steps_by_id: dict) -> str:
        """Render a single change card for the right column — one card per unique change."""
        cid = ch.get("change_id", "")
        title = escape(ch.get("title", ""))
        ctype = ch.get("change_type", "automate")
        badge_label, border_color, bg_color = CHANGE_BADGE.get(ctype, ("CHANGED", "#6B7280", "#F3F4F6"))

        # Affected steps in this stage — show what's changing
        affected_ids = ch.get("affected_step_ids", [])
        steps_html_parts = []
        for sid in affected_ids:
            s = steps_by_id.get(sid)
            if not s:
                continue
            step_desc = escape(s.get("description", ""))
            steps_html_parts.append(
                f'<div style="font-size:11px;color:#475569;padding:3px 0;border-bottom:1px solid rgba(0,0,0,0.05)">'
                f'<span style="color:#9CA3AF;font-size:10px;font-weight:600;margin-right:4px">{escape(sid)}</span> {step_desc}</div>'
            )
        steps_list_html = "".join(steps_html_parts) if steps_html_parts else ""

        # Proposed solution / future description
        future_desc = ch.get("future_step_description", "") or ch.get("proposed_solution", "") or ch.get("proposed_step_description", "")
        future_html = ""
        if future_desc:
            future_html = f'<div style="margin-top:8px;font-size:12px;color:#0f1825;font-weight:500;padding:8px 10px;background:rgba(125,255,0,0.06);border-left:3px solid #7DFF00;border-radius:0 6px 6px 0">{escape(future_desc)}</div>'

        # Tools
        future_tools = ch.get("future_step_tools", []) or ch.get("proposed_tools", [])
        tool_html = ""
        if future_tools:
            pills = "".join(
                f'<span style="background:#E0F2FE;color:#0369A1;border-radius:4px;padding:2px 8px;font-size:10px;margin-right:3px;font-weight:600">{escape(t)}</span>'
                for t in future_tools
            )
            tool_html = f'<div style="margin-top:6px">{pills}</div>'

        # Value & weeks metadata
        value = ch.get("value") or {}
        impl = ch.get("implementation") or {}
        annual_val = value.get("combined_annual_value_aud", 0)
        weeks = impl.get("weeks_label", "")
        phase = ch.get("phase", "")
        meta_parts = []
        if annual_val:
            meta_parts.append(f'<span style="background:#D1FAE5;color:#065F46;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700">${annual_val:,.0f}/yr</span>')
        if weeks:
            meta_parts.append(f'<span style="background:#DBEAFE;color:#1E40AF;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700">{escape(weeks)}</span>')
        if phase:
            meta_parts.append(f'<span style="background:#F3F4F6;color:#374151;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">Phase {phase}</span>')
        meta_html = f'<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">{"".join(meta_parts)}</div>' if meta_parts else ""

        # Details button (opens modal if modal_content exists)
        details_btn = ""
        if ch.get("modal_content"):
            details_btn = f'<div style="margin-top:8px"><button onclick="openBpModal(\'{cid}\')" style="font-size:10px;font-weight:700;color:#5B4FCF;background:rgba(91,79,207,0.08);border:1px solid rgba(91,79,207,0.2);border-radius:4px;padding:3px 10px;cursor:pointer">Details &rarr;</button></div>'

        return f"""<div style="background:{bg_color};border:2px solid {border_color};border-radius:10px;
                   padding:14px 16px;margin-bottom:12px;font-size:12px;position:relative;
                   box-shadow:0 1px 4px rgba(0,0,0,0.06)">
                   <span style="position:absolute;top:10px;right:10px;background:{border_color};color:#fff;
                     font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;letter-spacing:0.02em">{badge_label}</span>
                   <div style="font-weight:700;font-size:14px;color:#0f1825;padding-right:90px;margin-bottom:6px">{title}</div>
                   <div style="margin-bottom:4px">{steps_list_html}</div>
                   {future_html}
                   {tool_html}
                   {meta_html}
                   {details_btn}
                   </div>"""

    # ── Build zone HTML for blueprint (two-column per stage) ──

    def render_blueprint_zone(stage: str) -> str:
        steps = processes_by_stage.get(stage, [])
        label = stage_labels.get(stage, stage.replace("_", " ").title())
        subtitle = stage_subtitles.get(stage, "")
        accent = STAGE_ACCENT_DEFAULT
        zn = stage_zone.get(stage, 1)
        zn = max(1, min(zn, 9))

        if not steps:
            return ""

        # Build decision gate lookup for the left column
        nodes_by_step: dict = {}
        nodes_unanchored: list = []
        for dn in _decision_nodes_by_stage.get(stage, []):
            anchor = dn.get("after_step_id", "").strip()
            if anchor:
                nodes_by_step.setdefault(anchor, []).append(dn)
            else:
                nodes_unanchored.append(dn)
        steps_by_id: dict = {s.get("step_id", ""): s for s in steps}
        v_arrow = '<div class="v-arrow"><div class="v-line" style="height:14px;"></div><div class="v-tip"></div></div>'

        # Left column: current state (full process map rendering)
        left_parts = []
        prev_pg = False
        for i, s in enumerate(steps):
            if s.get("branch_only"):
                continue
            if s.get("type") == "optimisation":
                continue
            sid = s.get("step_id", "")
            changes = change_by_step.get(sid, [])
            # Add change indicator border on the left column for changed steps
            change_indicator = ""
            if changes:
                ctype = changes[0].get("change_type", "automate")
                _, border_color, _ = CHANGE_BADGE.get(ctype, ("", "#6B7280", ""))
                change_indicator = f'<div style="position:absolute;left:0;top:0;bottom:0;width:4px;background:{border_color};border-radius:10px 0 0 10px"></div>'

            if s.get("type") == "parallel_group":
                step_html = render_parallel_group(s, zn=zn)
                if changes:
                    step_html = step_html.replace('class="process-step"', f'class="process-step" style="position:relative"', 1)
                    step_html = step_html.replace('<div class="pg-label">', f'{change_indicator}<div class="pg-label">', 1)
                left_parts.append(step_html)
                prev_pg = True
            else:
                step_html = render_step(s, zn=zn)
                if changes:
                    # Wrap with a relative-positioned container with change indicator
                    step_html = f'<div style="position:relative">{change_indicator}{step_html}</div>'
                left_parts.append(step_html)
                prev_pg = False
            # Inject anchored decision gates
            for dn in nodes_by_step.get(sid, []):
                left_parts.append(v_arrow)
                left_parts.append(render_decision_gate(dn, steps_by_id=steps_by_id, zn=zn))
            if s.get("type") == "decision" and nodes_unanchored:
                left_parts.append(render_decision_gate(nodes_unanchored.pop(0), steps_by_id=steps_by_id, zn=zn))
            if i < len(steps) - 1 and not prev_pg:
                next_flow = None
                for ns in steps[i + 1:]:
                    if not ns.get("branch_only"):
                        next_flow = ns.get("data_flow")
                        break
                if next_flow and next_flow.get("mechanism"):
                    left_parts.append(render_labeled_arrow(next_flow))
                else:
                    left_parts.append(v_arrow)
        for dn in nodes_unanchored:
            left_parts.append(v_arrow)
            left_parts.append(render_decision_gate(dn, steps_by_id=steps_by_id, zn=zn))
        left_html = "\n".join(left_parts)

        # Right column: one card per unique change in this stage
        # Collect unique changes that affect steps in this stage
        seen_change_ids = set()
        stage_changes_ordered = []
        for s in steps:
            if s.get("branch_only"):
                continue
            sid = s.get("step_id", "")
            for ch in change_by_step.get(sid, []):
                cid = ch.get("change_id", "")
                if cid and cid not in seen_change_ids:
                    seen_change_ids.add(cid)
                    stage_changes_ordered.append(ch)

        right_parts = []
        for ch in stage_changes_ordered:
            right_parts.append(render_change_card(ch, steps_by_id))

        right_html = "\n".join(right_parts) if right_parts else '<div style="padding:20px;text-align:center;color:#9CA3AF;font-size:12px;font-style:italic">No changes proposed for this stage</div>'

        # Count changes in this stage
        stage_changes = set()
        for s in steps:
            sid = s.get("step_id", "")
            for ch in change_by_step.get(sid, []):
                stage_changes.add(ch.get("change_id", ""))
        change_count = len(stage_changes)
        badge = f"{change_count} change{'s' if change_count != 1 else ''}" if change_count else "no changes"

        return f"""
        <div class="bp-zone" id="bp-zone-{stage}">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <div style="border-left:4px solid {accent};padding-left:12px">
              <div style="font-size:18px;font-weight:800;color:#0f1825;letter-spacing:-0.02em">{escape(label)}</div>
              <div style="font-size:11px;color:#64748b">{escape(subtitle)}</div>
            </div>
            <span style="font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;
                  letter-spacing:0.5px;text-transform:uppercase;color:#64748b;background:#f1f5f9;
                  border:1px solid #e2e8f0;margin-left:auto">{badge}</span>
          </div>
          <div class="bp-columns">
            <div class="bp-col">
              <div class="bp-col-header" style="border-color:#EF4444;color:#EF4444">Current State</div>
              {left_html}
            </div>
            <div class="bp-col">
              <div class="bp-col-header" style="border-color:#10B981;color:#10B981">What Changes</div>
              {right_html}
            </div>
          </div>
        </div>"""

    # ── Build all zones ──
    zones_html = "\n".join(render_blueprint_zone(stage) for stage in stages)

    # ── Stats ──
    # Steps today: count actionable steps only (step, pain, decision, parallel_group) — exclude optimisation
    _actionable_types = {"step", "pain", "decision", "parallel_group"}
    total_steps_current = blueprint.get("total_steps_current", sum(
        len([s for s in proc.get("steps", []) if not s.get("branch_only") and s.get("type", "step") in _actionable_types])
        for proc in ssad.get("processes", [])
    ))
    # Steps after: subtract eliminated + automated + consolidated duplicates
    _eliminated = sum(1 for c in proposed_changes if c.get("change_type") == "eliminate")
    _automated = sum(1 for c in proposed_changes if c.get("change_type") == "automate")
    _consolidated_saved = sum(max(len(c.get("affected_step_ids", [])) - 1, 0) for c in proposed_changes if c.get("change_type") == "consolidate")
    total_steps_future = blueprint.get("total_steps_future", max(total_steps_current - _eliminated - _automated - _consolidated_saved, 0))
    total_value = blueprint.get("total_annual_value_aud", sum(
        (ch.get("value") or {}).get("combined_annual_value_aud", 0) for ch in proposed_changes
    ))
    # Hours saved: total across all team members (waste_items hours × headcount)
    total_hours_saved = sum(
        (w.get("hours_per_week") or 0) * max(w.get("headcount_affected") or 1, 1)
        for w in ssad.get("waste_items", [])
    )
    phases = blueprint.get("phases", [])
    num_phases = blueprint.get("total_phases", len(phases)) if phases else 0

    stats_html = f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;margin-bottom:32px">
      {_stat_box(str(total_steps_current), "Steps today")}
      {_stat_box(str(total_steps_future), "Steps after")}
      {_stat_box(f"{total_hours_saved:.1f}", "Hrs saved / wk")}
      {_stat_box(f"${total_value:,.0f}", "Annual value")}
      {_stat_box(str(num_phases), "Phases")}
    </div>"""

    # ── Phase timeline ──
    phase_timeline_html = ""
    if phases:
        phase_bars = []
        for ph in phases:
            ph_num = ph.get("phase_number", 0)
            ph_label = escape(ph.get("label", f"Phase {ph_num}"))
            ph_timeframe = escape(ph.get("timeframe", ""))
            ph_changes = len(ph.get("change_ids", []))
            # Calculate phase value
            ph_change_ids = set(ph.get("change_ids", []))
            ph_value = sum(
                ch.get("value", {}).get("combined_annual_value_aud", 0)
                for ch in proposed_changes if ch.get("change_id") in ph_change_ids
            )
            phase_bars.append(f"""
            <div class="bp-phase-card">
              <div class="bp-phase-num">Phase {ph_num}</div>
              <div class="bp-phase-label">{ph_label}</div>
              <div class="bp-phase-time">{ph_timeframe}</div>
              <div class="bp-phase-meta">{ph_changes} change{'s' if ph_changes != 1 else ''} &middot; ${ph_value:,.0f}/yr</div>
            </div>""")
        phase_timeline_html = f"""
        <div style="margin-bottom:32px">
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#64748b;margin-bottom:12px">Implementation Phases</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px">
            {"".join(phase_bars)}
          </div>
        </div>"""

    # ── Legend ──
    legend_items = [
        (CHANGE_BADGE["automate"][2], CHANGE_BADGE["automate"][1], "Automated"),
        (CHANGE_BADGE["replace"][2], CHANGE_BADGE["replace"][1], "Replaced"),
        (CHANGE_BADGE["eliminate"][2], CHANGE_BADGE["eliminate"][1], "Eliminated (hidden in future)"),
        (CHANGE_BADGE["consolidate"][2], CHANGE_BADGE["consolidate"][1], "Consolidated"),
        ("#f7f9fc", "#e2e8f0", "Unchanged (dimmed)"),
    ]
    legend_html = "".join(
        f'<div class="legend-item">'
        f'<div class="legend-swatch" style="background:{bg};border:1.5px solid {border}"></div>'
        f'{lbl}</div>'
        for bg, border, lbl in legend_items
    )

    # ── Sidebar navigation ──
    nav_links = []
    for stage in stages:
        s_steps = processes_by_stage.get(stage, [])
        if s_steps:
            label = stage_labels.get(stage, stage.replace("_", " ").title())
            nav_links.append(f'<a href="#bp-zone-{stage}" data-target="bp-zone-{stage}">{label}</a>')

    sidebar_html = (
        '<nav class="sidebar-nav" id="sidebarNav">'
        '<div class="nav-header">Stages</div>'
        + "".join(nav_links)
        + '</nav>'
        '<button class="sidebar-toggle" id="sidebarToggle" '
        'onclick="document.getElementById(\'sidebarNav\').classList.toggle(\'open\')">'
        '&#9776;</button>'
    )

    # ── Modals for proposed changes ──
    modals_html = ""
    for ch in proposed_changes:
        cid = ch.get("change_id", "")
        title = escape(ch.get("title", ""))
        mc = ch.get("modal_content", {})
        if not mc:
            continue
        sections = [
            ("What is the task?", mc.get("what_is_the_task", "")),
            ("What we'll build", mc.get("what_we_will_build", "")),
            ("How it works", mc.get("how_it_works", "")),
            ("How it saves money", mc.get("how_it_saves_money", "")),
            ("How quick?", mc.get("how_quick", "")),
        ]
        sections_html = ""
        for s_title, s_body in sections:
            if s_body:
                sections_html += f'<div style="margin-bottom:16px"><div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;margin-bottom:4px">{s_title}</div><div style="font-size:13px;line-height:1.6;color:#1e293b">{escape(s_body)}</div></div>'
        # Meeting references
        refs_html = ""
        for ref in mc.get("meeting_references", []):
            furl = ref.get("fathom_url", "")
            excerpt = ref.get("transcript_excerpt", "")
            if furl:
                refs_html += f'<a href="{furl}" target="_blank" rel="noopener" style="display:inline-block;font-size:10px;font-weight:600;color:#5B4FCF;text-decoration:none;background:rgba(91,79,207,0.08);border:1px solid rgba(91,79,207,0.2);border-radius:4px;padding:2px 8px;margin-right:4px;margin-bottom:4px">&#9654; Session {ref.get("session","")}</a>'
        if refs_html:
            refs_html = f'<div style="margin-top:8px;padding-top:8px;border-top:1px solid #e2e8f0"><div style="font-size:10px;font-weight:700;color:#64748b;margin-bottom:4px">MEETING REFERENCES</div>{refs_html}</div>'
        # Value badge
        val = ch.get("value", {})
        val_display = f"${val.get('combined_annual_value_aud', 0):,.0f}/yr" if val.get("combined_annual_value_aud") else ""
        impl = ch.get("implementation", {})
        weeks_display = impl.get("weeks_label", "")
        header_badges = ""
        if val_display:
            header_badges += f'<span style="background:#D1FAE5;color:#065F46;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">{val_display}</span>'
        if weeks_display:
            header_badges += f'<span style="background:#DBEAFE;color:#1E40AF;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">{escape(weeks_display)}</span>'
        ctype = ch.get("change_type", "automate")
        badge_label, badge_color, _ = CHANGE_BADGE.get(ctype, ("CHANGED", "#6B7280", ""))
        modals_html += f"""<div class="bp-modal-backdrop" id="modal-{cid}" style="display:none" onclick="if(event.target===this)closeBpModal()">
          <div style="background:#fff;border-radius:16px;max-width:600px;width:90%;max-height:90vh;overflow-y:auto;padding:28px 24px;position:relative;box-shadow:0 24px 60px rgba(0,0,0,0.2)">
            <button onclick="closeBpModal()" style="position:absolute;top:12px;right:16px;background:none;border:none;font-size:20px;cursor:pointer;color:#94a3b8">&times;</button>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;flex-wrap:wrap">
              <span style="background:{badge_color};color:#fff;font-size:9px;font-weight:700;padding:3px 8px;border-radius:4px">{badge_label}</span>
              {header_badges}
            </div>
            <div style="font-size:18px;font-weight:800;color:#0f1825;margin-bottom:16px">{title}</div>
            {sections_html}
            {refs_html}
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Transformation Blueprint</title>
{BRAND_FAVICON}
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  html {{ scroll-behavior: smooth; }}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --pain-bg: #fef2f2; --pain-border: #fca5a5; --pain-text: #dc2626;
    --opp-bg: #f0fdf4; --opp-border: #86efac; --opp-text: #16a34a;
    --decision-bg: #fffbeb; --decision-border: #fcd34d; --decision-text: #92400e;
    --auto-bg: #eff6ff; --auto-border: #93c5fd; --auto-text: #1d4ed8;
  }}
  body {{ background: #f7f9fc; font-family: 'Inter', -apple-system, sans-serif;
          color: #0f1825; min-height: 100vh; }}

  /* ── HEADER ── */
  .apg-header {{ background: #0f1825; color: #fff; padding: 20px 32px;
                 display: flex; align-items: center; gap: 16px;
                 border-bottom: 3px solid #7DFF00; }}
  .apg-header .logo {{ font-size: 20px; font-weight: 800; color: #ffffff; }}
  .apg-header .subtitle {{ font-size: 13px; color: #9CA3AF; margin-top: 2px; }}

  /* ── SIDEBAR NAV ── */
  .sidebar-nav {{ position: fixed; top: 0; left: 0; width: 210px; height: 100vh;
    background: rgba(15,24,37,0.97); padding: 20px 0; z-index: 100;
    overflow-y: auto; border-right: 1px solid #1e293b; }}
  .sidebar-nav .nav-header {{ padding: 12px 16px; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; }}
  .sidebar-nav a {{ display: block; padding: 8px 16px; font-size: 12px; font-weight: 500;
    color: #94a3b8; text-decoration: none; border-left: 3px solid transparent;
    transition: all 0.15s; }}
  .sidebar-nav a:hover {{ color: #e2e8f0; background: rgba(255,255,255,0.04); }}
  .sidebar-nav a.active {{ color: #7DFF00; border-left-color: #7DFF00;
    background: rgba(125,255,0,0.06); font-weight: 600; }}
  .sidebar-toggle {{ display: none; position: fixed; top: 12px; left: 12px; z-index: 200;
    background: #0f1825; color: #7DFF00; border: 1px solid #1e293b;
    border-radius: 6px; padding: 8px 10px; cursor: pointer; font-size: 16px; }}
  .apg-header {{ margin-left: 210px; }}
  .bp-canvas {{ margin-left: 210px; padding: 30px 24px 60px; max-width: 100%; }}
  @media (max-width: 900px) {{
    .sidebar-nav {{ transform: translateX(-100%); transition: transform 0.2s; }}
    .sidebar-nav.open {{ transform: translateX(0); }}
    .sidebar-toggle {{ display: block; }}
    .apg-header {{ margin-left: 0; }}
    .bp-canvas {{ margin-left: 0; }}
  }}

  /* ── BLUEPRINT ZONES ── */
  .bp-zone {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 20px 22px 24px; margin-bottom: 28px;
    box-shadow: 0 1px 8px rgba(15,24,37,0.06); }}
  .bp-columns {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  .bp-col {{ min-width: 0; }}
  .bp-col-header {{ font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; margin-bottom: 12px; padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0; }}
  @media (max-width: 768px) {{
    .bp-columns {{ grid-template-columns: 1fr; }}
  }}

  /* ── PHASE CARDS ── */
  .bp-phase-card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }}
  .bp-phase-num {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #7DFF00; margin-bottom: 4px; }}
  .bp-phase-label {{ font-size: 16px; font-weight: 800; color: #0f1825; margin-bottom: 2px; }}
  .bp-phase-time {{ font-size: 12px; color: #64748b; margin-bottom: 6px; }}
  .bp-phase-meta {{ font-size: 11px; color: #9CA3AF; }}

  /* ── STAT BOXES ── */
  .stat-box {{ background: #fff; border: 1px solid #E5E7EB; border-radius: 10px;
    padding: 20px 16px; text-align: center; }}
  .stat-val {{ font-size: 28px; font-weight: 800; color: #0f1825; letter-spacing: -0.03em; margin-bottom: 4px; }}
  .stat-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; }}

  /* ── LEGEND ── */
  .legend {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 14px;
    padding: 12px 20px; background: #f7f9fc; border-bottom: 1px solid #e2e8f0;
    margin-left: 210px; }}
  .legend-item {{ display: flex; align-items: center; gap: 5px; font-size: 11px;
    color: #475569; font-weight: 500; }}
  .legend-swatch {{ width: 13px; height: 13px; border-radius: 3px; flex-shrink: 0; }}
  @media (max-width: 900px) {{
    .legend {{ margin-left: 0; }}
  }}

  /* ── PROCESS MAP STYLES (for left column) ── */
  .box {{ border-radius: 10px; padding: 12px 14px; font-size: 12px; line-height: 1.55;
    position: relative; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    transition: box-shadow 0.15s; }}
  .box:hover {{ box-shadow: 0 4px 14px rgba(0,0,0,0.10); }}
  .box-title {{ font-weight: 600; font-size: 13px; margin-bottom: 4px; color: #0f1825; }}
  .box-body {{ font-size: 12px; color: #374151; line-height: 1.6; }}
  .step {{ background: #f7f9fc; border: 1px solid #e2e8f0; }}
  .step-z1,.step-z2,.step-z3,.step-z4,.step-z5,.step-z6,.step-z7,.step-z8,.step-z9
    {{ background:#f7f9fc; border:1px solid #e2e8f0; }}
  .decision-box {{ background: var(--decision-bg); border: 2px dashed var(--decision-border); border-radius: 50px; text-align: center; }}
  .decision-box .box-title {{ color: var(--decision-text); }}
  .auto-box {{ background: var(--auto-bg); border: 1.5px solid var(--auto-border); }}
  .auto-box .box-title {{ color: var(--auto-text); }}
  .pain-box {{ background: var(--pain-bg); border: 1.5px solid var(--pain-border); }}
  .pain-box .box-title {{ color: var(--pain-text); }}
  .opp-box {{ background: var(--opp-bg); border: 1.5px solid var(--opp-border); }}
  .opp-box .box-title {{ color: var(--opp-text); }}
  .v-arrow {{ display:flex; flex-direction:column; align-items:center; margin: 3px 0; }}
  .v-line {{ width:2px; background:#94a3b8; }}
  .v-tip {{ width:0; height:0; border-left:5px solid transparent; border-right:5px solid transparent; border-top:7px solid #94a3b8; }}
  .two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  .col {{ display:flex; flex-direction:column; align-items:center; }}
  .col .box {{ width:100%; }}
  .fork-label {{ font-size:10px; font-weight:700; color:white; border-radius:10px;
    padding:3px 10px; display:inline-block; margin-bottom:4px; }}
  .fork-label.yes {{ background:#16a34a; }}
  .fork-label.no  {{ background:#dc2626; }}
  .branch-yes-box {{ background:#f0fdf4; border:1.5px solid #86efac; }}
  .branch-no-box  {{ background:#fef2f2; border:1.5px solid #fca5a5; }}
  .branch-yes-box .box-title {{ color:#15803d; }}
  .branch-no-box  .box-title {{ color:#dc2626; }}
  .decision-gate {{ position: relative; margin: 4px 0; }}
  .gate-merge-spacer {{ height: 16px; }}
  .gate-condition {{ background: #fffbeb; border: 2px dashed #fcd34d;
    border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600;
    color: #92400e; text-align: center; }}
  .person-tag {{ background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;
    border-radius: 6px; font-size: 11px; padding: 3px 10px; display: inline-block; margin-top: 2px; }}
  .step-tools {{ margin-top:4px; display:flex; flex-wrap:wrap; gap:3px; }}
  .step-tool-tag {{ display:inline-block; font-size:11px; font-weight:600;
    background:#f0fdf4; color:#166534; border:1px solid #bbf7d0;
    padding:1px 7px; border-radius:10px; }}
  .step-meta {{ margin-top:5px; display:flex; flex-wrap:wrap; gap:4px; }}
  .meta-chip {{ font-size:10px; font-weight:600; color:#64748b; background:#f1f5f9;
    border-radius:4px; padding:1px 5px; }}
  .step-quote {{ font-size:10px; font-style:italic; color:#64748b;
    border-left:2px solid #cbd5e1; padding:3px 7px; margin-top:5px; }}
  .step-session {{ font-size: 10px; color: #9CA3AF; font-weight: 500; margin-top: 4px; }}
  .labeled-arrow {{ gap: 0; }}
  .flow-label {{ font-size:10px; font-weight:700; padding:1px 8px;
    border:1.5px solid #94a3b8; border-radius:10px; background:#ffffff; color:#475569; }}
  .fathom-refs {{ margin-top: 5px; display: flex; flex-direction: column; gap: 3px; }}
  .fathom-dropdown {{ border: 1px solid rgba(91,79,207,0.2); border-radius: 6px;
    background: rgba(91,79,207,0.04); overflow: visible; }}
  .fathom-dropdown > summary {{ display: flex; align-items: center; gap: 8px; font-size: 10px;
    font-weight: 600; color: #5B4FCF; padding: 4px 8px; cursor: pointer;
    list-style: none; user-select: none; }}
  .fathom-dropdown > summary::-webkit-details-marker {{ display: none; }}
  .fathom-dropdown > summary::after {{ content: "›"; margin-left: auto; font-size: 14px;
    line-height: 1; transition: transform 0.15s; display: inline-block; }}
  .fathom-dropdown[open] > summary::after {{ transform: rotate(90deg); }}
  .fathom-dropdown:hover {{ background: rgba(91,79,207,0.08); border-color: rgba(91,79,207,0.35); }}
  .ref-label {{ flex: 1; }}
  .ref-time {{ font-size: 9px; color: #8B7FCF; font-weight: 500; font-variant-numeric: tabular-nums; }}
  .fathom-panel {{ padding: 6px 10px 8px; border-top: 1px solid rgba(91,79,207,0.15);
    display: flex; flex-direction: column; gap: 6px; }}
  .fathom-excerpt {{ font-size: 10px; color: #3D3560; background: rgba(91,79,207,0.05);
    border-left: 2px solid rgba(91,79,207,0.25); margin: 0; padding: 6px 10px;
    border-radius: 0 4px 4px 0; line-height: 1.5; }}
  .tx-line {{ margin-bottom: 3px; }}
  .tx-line:last-child {{ margin-bottom: 0; }}
  .fathom-open-btn {{ align-self: flex-start; font-size: 9px; font-weight: 700; color: #5B4FCF;
    text-decoration: none; background: rgba(91,79,207,0.1); border: 1px solid rgba(91,79,207,0.25);
    border-radius: 4px; padding: 3px 10px; letter-spacing: 0.02em; }}
  .fathom-open-btn:hover {{ background: rgba(91,79,207,0.2); }}
  .email-refs {{ margin-top: 3px; display: flex; flex-direction: column; gap: 2px; opacity: 0; transition: opacity 0.15s; }}
  .box:hover .email-refs {{ opacity: 1; }}
  .email-link {{ display: inline-block; font-size: 10px; font-weight: 600; color: #1a7f5a;
    text-decoration: none; background: rgba(26,127,90,0.08);
    border: 1px solid rgba(26,127,90,0.2); border-radius: 4px;
    padding: 2px 6px; white-space: nowrap; }}
  .email-link:hover {{ background: rgba(26,127,90,0.15); text-decoration: underline; }}
  .pg-label {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #9CA3AF; text-align: center; margin-bottom: 6px; }}
  .pg-row {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; margin: 4px 0; }}
  .pg-chip {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 8px 12px; font-size: 11px; font-weight: 600; color: #0f1825;
    text-align: center; min-width: 60px; flex: 1 1 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .pg-chip .chip-tool {{ display: block; font-size: 9px; font-weight: 600; color: #166634;
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px;
    padding: 1px 6px; margin-top: 3px; }}
  .pg-chip .chip-owner {{ display: block; font-size: 9px; margin-top: 3px; }}
  .pg-chip .chip-dropdown {{ display: block; margin-top: 4px; }}
  .pg-chip .chip-dropdown > summary {{ display: inline-flex; align-items: center; gap: 3px;
    font-size: 9px; color: #5B4FCF; cursor: pointer; list-style: none; opacity: 0.7; }}
  .pg-chip .chip-dropdown > summary::-webkit-details-marker {{ display: none; }}
  .pg-chip:hover .chip-dropdown > summary {{ opacity: 1; }}
  .pg-chip .chip-panel {{ margin-top: 4px; background: rgba(91,79,207,0.06);
    border: 1px solid rgba(91,79,207,0.2); border-radius: 6px; padding: 5px 8px;
    display: flex; flex-direction: column; gap: 5px; text-align: left; }}
  .pg-chip .chip-excerpt {{ font-size: 9px; font-style: italic; color: #5B4FCF;
    border-left: 2px solid rgba(91,79,207,0.3); padding-left: 5px; margin: 0; line-height: 1.4; }}
  .pg-chip .chip-open-btn {{ align-self: flex-start; font-size: 9px; font-weight: 700;
    color: #5B4FCF; text-decoration: none; background: rgba(91,79,207,0.1);
    border: 1px solid rgba(91,79,207,0.25); border-radius: 4px; padding: 1px 6px; }}
  .pg-merge {{ display: flex; flex-direction: column; align-items: center; }}
  .pg-legs {{ display: flex; justify-content: center; width: 100%; }}
  .pg-leg {{ flex: 1; display: flex; justify-content: center; }}
  .pg-leg .v-line {{ height: 10px; width: 2px; background: #94a3b8; }}
  .pg-crossbar {{ height: 2px; background: #94a3b8; }}
  .pg-drop {{ display: flex; flex-direction: column; align-items: center; }}
  .pg-drop .v-line {{ height: 10px; width: 2px; background: #94a3b8; }}
  .pg-drop .v-tip {{ width: 0; height: 0; border-left: 5px solid transparent;
    border-right: 5px solid transparent; border-top: 7px solid #94a3b8; }}

  /* ── MODAL ── */
  .bp-modal-backdrop {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); z-index: 500;
    display: flex; align-items: center; justify-content: center; }}

  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .box {{ animation: fadeUp 0.3s ease both; }}
</style>
</head>
<body>

{sidebar_html}

<div class="apg-header">
  <div style="display:flex;align-items:center;gap:12px;">
    <img src="{COMPANY_LOGO_URL}" alt="{YOUR_COMPANY}" style="height:38px;width:auto;display:block;">
    <div>
      <div class="logo">{YOUR_COMPANY}</div>
      <div class="subtitle">Business Operations Audit</div>
    </div>
  </div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:20px;">
    <div style="text-align:right">
      <div style="font-weight:700;font-size:16px">{company}</div>
      <div style="font-size:12px;color:#9CA3AF">Transformation Blueprint &middot; {generated}</div>
    </div>
  </div>
</div>

<div class="legend">
  {legend_html}
</div>

<div class="bp-canvas">
  {stats_html}
  {phase_timeline_html}
  {zones_html}
</div>

{modals_html}

<script>
function openBpModal(id) {{
  var el = document.getElementById('modal-' + id);
  if (el) {{ el.style.display = 'flex'; document.body.style.overflow = 'hidden'; }}
}}
function closeBpModal() {{
  document.querySelectorAll('.bp-modal-backdrop').forEach(function(m) {{ m.style.display = 'none'; }});
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeBpModal(); }});

// Sidebar scroll tracking
(function() {{
  var sections = document.querySelectorAll('.bp-zone');
  var navLinks = document.querySelectorAll('.sidebar-nav a[data-target]');
  if (!sections.length || !navLinks.length) return;
  var observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        navLinks.forEach(function(l) {{ l.classList.remove('active'); }});
        var active = document.querySelector('.sidebar-nav a[data-target="' + entry.target.id + '"]');
        if (active) active.classList.add('active');
      }}
    }});
  }}, {{ rootMargin: '-20% 0px -70% 0px' }});
  sections.forEach(function(s) {{ observer.observe(s); }});
  navLinks.forEach(function(link) {{
    link.addEventListener('click', function(e) {{
      e.preventDefault();
      var target = document.getElementById(this.getAttribute('data-target'));
      if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      document.getElementById('sidebarNav').classList.remove('open');
    }});
  }});
}})();
</script>
</body>
</html>"""


# ─── Audit Report Generator ────────────────────────────────────────────────────

def generate_audit_report(ssad: dict) -> str:
    company = escape(ssad.get("company_name", "Client"))
    industry = escape(ssad.get("industry_tag", ""))
    generated = datetime.now().strftime("%d %b %Y")
    _print_stage_labels, _ = _build_stage_lookups(ssad)
    _print_stage_order = [p["stage"] for p in ssad.get("processes", [])]
    contact = ssad.get("contact", {})
    contact_name = escape(contact.get("name", ""))
    sessions = ssad.get("sessions_completed", 0)
    audit_status = ssad.get("audit_status", "")

    waste_items = ssad.get("waste_items", [])
    roi_items = ssad.get("roi_items", [])
    pain_points = ssad.get("pain_points", [])
    contradictions = ssad.get("contradictions", [])
    unresolved = [c for c in contradictions if c.get("status") == "unresolved"]
    follow_ups = [q for q in ssad.get("follow_up_questions", [])
                  if q.get("priority") == "HIGH" and q.get("status") == "pending"]

    total_annual_waste = sum(w.get("annual_waste_aud") or 0 for w in waste_items if w.get("confidence") in ("HIGH", "MEDIUM"))
    total_monthly_waste = sum(w.get("monthly_waste_aud") or 0 for w in waste_items if w.get("confidence") in ("HIGH", "MEDIUM"))

    quick_wins = [r for r in roi_items if r.get("payback_tag") == "QUICK_WIN"]
    core_builds = [r for r in roi_items if r.get("payback_tag") == "CORE_BUILD"]
    future_items = [r for r in roi_items if r.get("payback_tag") == "FUTURE"]

    # Warnings
    warnings_html = ""
    if unresolved:
        warnings_html += f'<div class="warning">⚠ {len(unresolved)} unresolved contradiction(s) noted below — confirm with client before final delivery.</div>'
    if follow_ups:
        warnings_html += f'<div class="warning">⚠ {len(follow_ups)} HIGH priority follow-up question(s) still pending — audit data may be incomplete in some areas.</div>'

    # ROI table
    def roi_row(item):
        activity = escape(item.get("activity", ""))
        annual = fmt_aud(item.get("annual_waste_aud"))
        monthly = fmt_aud(item.get("monthly_waste_aud"))
        conf = item.get("confidence", "LOW")
        quote = escape(item.get("quote", ""))
        hrs = item.get("hours_per_week", "")
        hc = item.get("headcount_affected", "")
        calc = f"{hrs} hrs/wk × {hc} staff" if hrs and hc else ""
        calc_cell = f"<br><small style='color:#9CA3AF'>{calc}</small>" if calc else ""
        q80 = quote[:80]
        ellipsis = "..." if len(quote) > 80 else ""
        quote_cell = f'"{q80}{ellipsis}"' if quote else ""
        return f"""<tr>
          <td><strong>{activity}</strong>{calc_cell}</td>
          <td class="highlight">{annual}/yr</td>
          <td style="color:{BRAND_GREY}">{monthly}/mo</td>
          <td>{confidence_badge(conf)}</td>
          <td style="font-style:italic;color:{BRAND_GREY};font-size:12px">{quote_cell}</td>
        </tr>"""

    waste_rows = "".join(roi_row(w) for w in waste_items) if waste_items else "<tr><td colspan='5' style='color:#9CA3AF;text-align:center'>No waste items recorded yet</td></tr>"

    # Priority matrix
    def priority_card(item, tag_color):
        activity = escape(item.get("activity", ""))
        build = fmt_aud(item.get("build_cost_aud"))
        saving = fmt_aud(item.get("monthly_saving_aud"))
        months = item.get("payback_months")
        payback = f"{months:.1f} months" if months else "—"
        return f"""
        <div style="background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:14px;
                    border-left:4px solid {tag_color}">
          <div style="font-weight:600;font-size:13px;margin-bottom:8px">{activity}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:12px">
            <div><div style="color:{BRAND_GREY}">Build cost</div><div style="font-weight:700">{build}</div></div>
            <div><div style="color:{BRAND_GREY}">Monthly saving</div><div style="font-weight:700;color:#10B981">{saving}</div></div>
            <div><div style="color:{BRAND_GREY}">Payback</div><div style="font-weight:700">{payback}</div></div>
          </div>
        </div>"""

    qw_cards = "".join(priority_card(r, "#10B981") for r in quick_wins) or "<p style='color:#9CA3AF;font-size:13px'>None identified yet</p>"
    cb_cards = "".join(priority_card(r, "#7DFF00") for r in core_builds) or "<p style='color:#9CA3AF;font-size:13px'>None identified yet</p>"
    fu_cards = "".join(priority_card(r, BRAND_GREY) for r in future_items) or "<p style='color:#9CA3AF;font-size:13px'>None identified yet</p>"

    # Pain points
    pain_rows = ""
    for pp in pain_points:
        stage = escape(pp.get("stage", ""))
        desc = escape(pp.get("description", ""))
        quote = escape(pp.get("quote", ""))
        speaker = escape(pp.get("speaker", ""))
        conf = pp.get("confidence", "LOW")
        pain_rows += f"""<tr>
          <td style="text-transform:capitalize">{stage}</td>
          <td>{desc}</td>
          <td style="font-style:italic;font-size:12px;color:{BRAND_GREY}">"{quote[:100]}{"..." if len(quote) > 100 else ""}" — {speaker}</td>
          <td>{confidence_badge(conf)}</td>
        </tr>"""
    if not pain_rows:
        pain_rows = "<tr><td colspan='4' style='color:#9CA3AF;text-align:center'>No pain points recorded yet</td></tr>"

    # Contradictions section
    contradictions_html = ""
    if unresolved:
        items_html = ""
        for c in unresolved:
            topic = escape(c.get("topic", ""))
            sa = c.get("statement_a", {})
            sb = c.get("statement_b", {})
            items_html += f"""
            <div style="background:#FFF7ED;border:1px solid #FCD34D;border-radius:6px;padding:12px;margin-bottom:10px">
              <div style="font-weight:600;margin-bottom:6px">⚠ {topic}</div>
              <div style="font-size:12px;color:{BRAND_GREY}">Session {sa.get('session','?')}, {escape(sa.get('speaker',''))}:
                <em>"{escape(sa.get('quote',''))}"</em></div>
              <div style="font-size:12px;color:{BRAND_GREY};margin-top:4px">Session {sb.get('session','?')}, {escape(sb.get('speaker',''))}:
                <em>"{escape(sb.get('quote',''))}"</em></div>
            </div>"""
        contradictions_html = f"<h2>Contradictions to Resolve</h2>{items_html}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Audit Report</title>
{BRAND_FAVICON}
<style>{base_css()}</style>
</head>
<body>
<div class="apg-header">
  <div>
    <div class="logo">{YOUR_COMPANY}</div>
    <div class="subtitle">Business Operations Audit Report</div>
  </div>
  <div style="margin-left:auto;text-align:right">
    <div style="font-weight:700;font-size:16px">{company}</div>
    <div style="font-size:12px;color:#9CA3AF">{contact_name} · {industry} · {generated}</div>
  </div>
</div>
<div class="container">
  <h1>Audit Report</h1>
  <div class="meta">{sessions} session{'s' if sessions != 1 else ''} completed · Status: {audit_status}</div>

  {warnings_html}

  <!-- Executive Summary -->
  <div class="card" style="border-left:4px solid #7DFF00">
    <h2 style="margin-top:0">Executive Summary</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-top:12px">
      <div>
        <div style="font-size:28px;font-weight:800;color:#166534">{fmt_aud(total_annual_waste)}</div>
        <div style="font-size:13px;color:{BRAND_GREY}">Annual operational waste identified</div>
      </div>
      <div>
        <div style="font-size:28px;font-weight:800;color:#10B981">{fmt_aud(total_monthly_waste)}</div>
        <div style="font-size:13px;color:{BRAND_GREY}">Monthly recoverable cost</div>
      </div>
      <div>
        <div style="font-size:28px;font-weight:800">{len(quick_wins)}</div>
        <div style="font-size:13px;color:{BRAND_GREY}">Quick wins (payback &lt;12mo)</div>
      </div>
      <div>
        <div style="font-size:28px;font-weight:800">{len(pain_points)}</div>
        <div style="font-size:13px;color:{BRAND_GREY}">Pain points documented</div>
      </div>
    </div>
  </div>

  <!-- ROI Model -->
  <h2>ROI Model — Waste Identified</h2>
  <p style="font-size:13px;color:{BRAND_GREY};margin-bottom:12px">
    All figures derived from verbatim statements made during audit sessions.
    HIGH confidence = explicitly stated. MEDIUM = inferred. LOW = estimated, needs confirmation.
  </p>
  <div style="overflow-x:auto">
  <table>
    <thead><tr>
      <th>Activity</th><th>Annual Waste</th><th>Monthly</th><th>Confidence</th><th>Source Quote</th>
    </tr></thead>
    <tbody>{waste_rows}</tbody>
  </table>
  </div>

  <!-- Priority Matrix -->
  <h2>Priority Matrix</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
    <div>
      <h3 style="color:#10B981">✓ Quick Wins <small style="font-weight:400;color:{BRAND_GREY}">(payback &lt;12mo)</small></h3>
      {qw_cards}
    </div>
    <div>
      <h3 style="color:#7DFF00">◉ Core Platform <small style="font-weight:400;color:{BRAND_GREY}">(12–24mo)</small></h3>
      {cb_cards}
    </div>
    <div>
      <h3 style="color:{BRAND_GREY}">○ Future <small style="font-weight:400;color:{BRAND_GREY}">(24mo+)</small></h3>
      {fu_cards}
    </div>
  </div>

  <!-- Pain Points -->
  <h2>Pain Points by Stage</h2>
  <div style="overflow-x:auto">
  <table>
    <thead><tr><th>Stage</th><th>Pain Point</th><th>Verbatim Quote</th><th>Confidence</th></tr></thead>
    <tbody>{pain_rows}</tbody>
  </table>
  </div>

  {contradictions_html}

  <div style="font-size:11px;color:{BRAND_GREY};margin-top:32px;padding-top:16px;border-top:1px solid #E5E7EB">
    Generated by {YOUR_COMPANY} Audit System · {generated} · All findings cite original transcript sources.
  </div>
</div>
</body>
</html>"""


# ─── Opportunity Map Generator ─────────────────────────────────────────────────

def generate_priority_matrix(ssad: dict) -> str:
    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")

    proposed_changes = ssad.get("proposed_changes", [])
    roi_items = ssad.get("roi_items", [])

    # ── Build chart via shared helper ──
    scatter_html, modals_html, has_interactive = _render_priority_chart(ssad)

    # ── Stats summary ──
    total_annual_saving = sum(r.get("annual_saving_aud") or 0 for r in roi_items if r.get("confidence") in ("HIGH", "MEDIUM"))
    n_qw = sum(1 for r in roi_items if r.get("suggested_tier") == "micro")
    n_saas = sum(1 for r in roi_items if r.get("suggested_tier") in ("standard", "complex"))
    n_custom = sum(1 for r in roi_items if r.get("suggested_tier") == "sprint")
    n_areas = len(set(c.get("stage", "other") for c in proposed_changes))

    stats_bar = f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px">
      {_stat_box(fmt_aud(total_annual_saving), "Annual value identified")}
      {_stat_box(str(n_qw), "Quick wins")}
      {_stat_box(str(n_saas), "SaaS tool setups")}
      {_stat_box(str(n_areas), "Process areas")}
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Priority Matrix</title>
{BRAND_FAVICON}
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        color: {BRAND_DARK}; background: {BRAND_LIGHT}; font-size: 15px; line-height: 1.5; }}
.apg-header {{ background: {BRAND_DARK}; color: #fff; padding: 20px 32px;
               display: flex; align-items: center; gap: 16px; }}
.apg-header .logo {{ font-size: 20px; font-weight: 800; color: #ffffff; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 32px 24px; }}
.section {{ margin-bottom: 48px; }}
.section-title {{ font-size: 20px; font-weight: 700; margin-bottom: 6px; padding-bottom: 10px;
                  border-bottom: 2px solid #E5E7EB; }}
.section-sub {{ font-size: 13px; color: {BRAND_GREY}; margin-bottom: 20px; }}
.stat-box {{ background: #fff; border: 1px solid #E5E7EB; border-radius: 10px;
             padding: 20px 16px; text-align: center; }}
.stat-val {{ font-size: 28px; font-weight: 800; color: {BRAND_DARK}; letter-spacing: -0.03em; margin-bottom: 4px; }}
.stat-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: {BRAND_GREY}; }}
/* Interactive priority matrix */
.pm-bubble {{ position:absolute; border-radius:50%; border:2px solid; opacity:0.85;
              cursor:pointer; display:flex; align-items:center; justify-content:center;
              transform:translate(-50%,-50%); transition:transform 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease; }}
.pm-bubble:hover {{ transform:translate(-50%,-50%) scale(1.18); opacity:1; box-shadow:0 4px 16px rgba(0,0,0,0.25); z-index:10; }}
.pm-bubble-label {{ font-weight:700; color:#fff; pointer-events:none; text-shadow:0 1px 2px rgba(0,0,0,0.5); line-height:1.1; }}
@keyframes pm-pulse {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(5,150,105,0.3); }} 50% {{ box-shadow:0 0 0 8px rgba(5,150,105,0); }} }}
.pm-bubble-top {{ animation:pm-pulse 2s ease-in-out 3; }}
.pm-modal-backdrop {{ position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.6);
                      z-index:2000; display:flex; align-items:center; justify-content:center; padding:24px; }}
.pm-modal {{ background:#fff; border-radius:14px; max-width:560px; width:100%; max-height:85vh; overflow-y:auto;
             padding:28px 32px; position:relative; box-shadow:0 20px 60px rgba(0,0,0,0.3); }}
.pm-modal-close {{ position:absolute; top:12px; right:16px; background:none; border:none; font-size:24px;
                   color:{BRAND_GREY}; cursor:pointer; padding:4px 8px; line-height:1; }}
.pm-modal-close:hover {{ color:{BRAND_DARK}; }}
.pm-modal-section {{ margin-bottom:16px; }}
.pm-modal-section h4 {{ font-size:13px; font-weight:700; color:{BRAND_GREY}; text-transform:uppercase;
                        letter-spacing:0.05em; margin-bottom:4px; }}
.pm-modal-section p {{ font-size:14px; line-height:1.55; color:{BRAND_DARK}; }}
.pm-modal-formula {{ background:#F0FDF4; border:1px solid #BBF7D0; border-radius:6px; padding:8px 12px;
                     font-size:13px; font-weight:600; color:#166534; margin:8px 0 16px 0; font-family:monospace; }}
.pm-modal-stats {{ display:flex; gap:24px; margin-top:20px; padding-top:16px; border-top:1px solid #E5E7EB; }}
.pm-modal-stat-val {{ font-size:20px; font-weight:800; color:{BRAND_DARK}; display:block; }}
.pm-modal-stat-lbl {{ font-size:10px; text-transform:uppercase; letter-spacing:0.06em; color: {BRAND_GREY}; }}
</style>
</head>
<body>

<div class="apg-header">
  <div class="logo">{YOUR_COMPANY}</div>
  <div>
    <div style="font-weight:700;font-size:16px">{company} — Priority Matrix</div>
    <div style="font-size:13px;color:#9CA3AF">Generated {generated}</div>
  </div>

</div>

<div class="container">

<!-- Stats bar -->
{stats_bar}

<!-- Priority matrix -->
<div class="section">
  <div class="section-title">Priority Matrix</div>
  <div class="section-sub">{"X = weeks to implement · Y = annual value · Click a bubble for details" if has_interactive else "X = payback period · Y = annual saving · Bubble size = build cost"}</div>
  <div style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:24px">
    {scatter_html}
  </div>
</div>

<div style="font-size:11px;color:{BRAND_GREY};margin-top:32px;padding-top:16px;border-top:1px solid #E5E7EB">
  Generated by {YOUR_COMPANY} Audit System · {generated} · All findings cite original transcript sources.
</div>

</div>

<!-- Modals (interactive priority matrix) -->
{modals_html}

<script>
function openModal(id) {{
  var el = document.getElementById('modal-' + id);
  if (el) {{ el.style.display = 'flex'; document.body.style.overflow = 'hidden'; }}
}}
function closeModal() {{
  document.querySelectorAll('.pm-modal-backdrop').forEach(function(m) {{ m.style.display = 'none'; }});
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeModal(); }});
function showTip(el, title, value, weeks) {{
  var tip = document.getElementById('pm-tooltip');
  if (!tip) return;
  tip.innerHTML = '<div style="font-weight:700;margin-bottom:2px">' + title + '</div>'
    + '<div style="color:#9CA3AF;font-size:11px">' + value + ' &middot; ' + weeks + '</div>';
  tip.style.display = 'block';
  var r = el.getBoundingClientRect();
  tip.style.left = (r.left + r.width/2) + 'px';
  tip.style.top = (r.top - 8) + 'px';
  tip.style.transform = 'translate(-50%, -100%)';
}}
function hideTip() {{
  var tip = document.getElementById('pm-tooltip');
  if (tip) tip.style.display = 'none';
}}
</script>
</body>
</html>"""


# _opp_stat replaced by module-level _stat_box()


# ─── Quadrant Priority Matrix Helper ────────────────────────────────────────────

def _render_quadrant_matrix(ssad: dict, enriched_changes: list = None) -> tuple:
    """Build the quadrant priority matrix HTML grouped by process area.

    Returns (pm_quadrant_html, pm_modals_html).
    If *enriched_changes* is None, builds the list from ssad['proposed_changes']
    filtering for changes that have both value and implementation estimates.
    """
    import math as _math

    if enriched_changes is None:
        enriched_changes = [
            c for c in ssad.get("proposed_changes", [])
            if c.get("value", {}).get("combined_annual_value_aud") is not None
            and c.get("implementation", {}).get("weeks_estimate") is not None
        ]

    pm_quadrant_html = ""
    pm_modals_html = ""
    if enriched_changes:
        _roi_tier_lookup = {r.get("linked_change_id", ""): r.get("suggested_tier", "standard") for r in ssad.get("roi_items", [])}
        _pm_processes = ssad.get("processes", [])
        _pm_stage_labels = {p["stage"]: p["name"] for p in _pm_processes}
        _PM_TIER_COLOR = {"quick_win": "#ea580c", "micro": "#ea580c", "standard": "#2563eb", "complex": "#2563eb", "sprint": "#16a34a"}

        def _pm_effective_tier(c, _roi_tier_lookup):
            qwp = c.get("quick_win_plan", {})
            if qwp.get("qualified") is True:
                return "quick_win"
            return _roi_tier_lookup.get(c.get("change_id", ""), "standard")
        _PM_TIER_LABELS = {"micro": "Quick Win", "standard": "SaaS Toolkit", "complex": "SaaS Toolkit", "sprint": "Custom Platform"}

        # Group by stage
        _pm_stage_groups = {}
        for c in enriched_changes:
            stage = c.get("stage", "other")
            _pm_stage_groups.setdefault(stage, []).append(c)

        grouped = []
        for stage, items in _pm_stage_groups.items():
            group_val = sum(c["value"]["combined_annual_value_aud"] for c in items)
            group_weeks = max(c["implementation"]["weeks_estimate"] for c in items)
            tiers = [_pm_effective_tier(c, _roi_tier_lookup) for c in items]
            tier_counts = {}
            for t in tiers:
                tier_counts[t] = tier_counts.get(t, 0) + 1
            dominant_tier = "sprint" if "sprint" in tier_counts else max(tier_counts, key=tier_counts.get)
            color = _PM_TIER_COLOR.get(dominant_tier, "#2563eb")
            grouped.append({
                "stage": stage, "label": _pm_stage_labels.get(stage, stage.replace("_", " ").title()),
                "annual_val": group_val, "weeks": group_weeks, "color": color,
                "dominant_tier": dominant_tier, "items": items,
                "group_id": f"GRP-{stage}",
            })

        values = [g["annual_val"] for g in grouped]
        weeks_list = [g["weeks"] for g in grouped]
        min_val, max_val = min(values), max(values)
        val_range = max(max_val - min_val, 1)

        def _impact(v):
            norm = _math.sqrt((v - min_val) / val_range) if val_range > 0 else 0.5
            return max(1, min(10, round(1 + norm * 9)))

        max_weeks = max(weeks_list)
        min_weeks = min(weeks_list)
        weeks_range = max(max_weeks - min_weeks, 0.5)

        def _ease(w):
            norm = 1 - ((w - min_weeks) / weeks_range)
            return max(1, min(10, round(1 + norm * 9)))

        bubble_data = []
        for g in grouped:
            impact = _impact(g["annual_val"])
            ease = _ease(g["weeks"])
            size = max(45, min(90, 45 + _math.sqrt(g["annual_val"] / max_val) * 45))
            savings_label = f"${g['annual_val']/1000:.0f}k/yr" if g["annual_val"] >= 1000 else f"${g['annual_val']:,.0f}/yr"
            bubble_data.append({
                "group_id": g["group_id"], "label": g["label"], "impact": impact, "ease": ease,
                "size": size, "color": g["color"], "savings_label": savings_label,
                "annual_val": g["annual_val"], "dominant_tier": g["dominant_tier"], "items": g["items"],
            })

        # Anti-overlap jitter pass
        for i in range(len(bubble_data)):
            for j in range(i):
                bi, bj = bubble_data[i], bubble_data[j]
                if bi["impact"] == bj["impact"] and bi["ease"] == bj["ease"]:
                    bi["impact"] = min(10, bi["impact"] + (1 if i % 2 == 0 else 0))
                    bi["ease"] = max(1, bi["ease"] - (1 if i % 2 == 1 else 0))
                elif abs(bi["impact"] - bj["impact"]) <= 1 and abs(bi["ease"] - bj["ease"]) <= 1:
                    bi["impact"] = min(10, max(1, bi["impact"] + (1 if i % 2 == 0 else -1)))

        # Build bubbles HTML
        bubbles_html = ""
        for i, b in enumerate(bubble_data):
            left = 12 + ((b["impact"] - 1) / 9) * 76
            bottom = 12 + ((b["ease"] - 1) / 9) * 76
            bubbles_html += f"""<div class="qm-bubble" data-idx="{i}" data-cid="{b['group_id']}"
              style="left:{left:.1f}%;bottom:{bottom:.1f}%;width:{b['size']:.0f}px;height:{b['size']:.0f}px;
                     border-color:{b['color']};background:{b['color']}20"
              onclick="qmClick({i})" onmouseenter="qmHover({i})" onmouseleave="qmHover(null)">
              <div class="qm-tip" id="qm-tip-{i}">
                <div style="font-size:13px;font-weight:700">{b['label']}</div>
                <div style="font-size:11px;color:{BRAND_GREY};margin-top:2px">{len(b['items'])} improvements &middot; {_PM_TIER_LABELS.get(b['dominant_tier'], 'SaaS')}</div>
                <div style="font-size:12px;font-weight:700;color:#166534;margin-top:2px">{b['savings_label']}</div>
              </div>
            </div>\n"""

        # Build legend buttons
        legend_html = ""
        for i, b in enumerate(bubble_data):
            legend_html += f"""<button class="qm-legend-btn" data-idx="{i}"
              onclick="qmSelect(qmSelected==={i}?null:{i})" onmouseenter="qmHover({i})" onmouseleave="qmHover(null)"
              style="border-color:var(--border)">
              <span style="width:12px;height:12px;border-radius:50%;border:2px solid {b['color']};background:{b['color']}30;flex-shrink:0;display:inline-block"></span>
              <span style="font-size:12px;font-weight:500">{b['label']}</span>
            </button>\n"""

        pm_quadrant_html = f"""<div class="qm-container">
          <div class="qm-axis-x"></div>
          <div class="qm-axis-y"></div>
          <div class="qm-mid-x"></div>
          <div class="qm-mid-y"></div>
          <div class="qm-label qm-label-tl">Nice-to-Haves</div>
          <div class="qm-label qm-label-tr" style="color:var(--lime-text)">Quick Wins</div>
          <div class="qm-label qm-label-br" style="color:#3b82f6">Big Swings</div>
          <div class="qm-label qm-label-bl">Future Plans</div>
          <div class="qm-axis-label-x">Business Impact &rarr;</div>
          <div class="qm-axis-label-y">Ease of Implementation &rarr;</div>
          {bubbles_html}
        </div>
        <div class="qm-legend">{legend_html}</div>"""

        # Build grouped modals
        for b in bubble_data:
            group_id = b["group_id"]
            label = b["label"]
            annual_val = b["annual_val"]
            dominant_tier = b["dominant_tier"]
            tier_label = _PM_TIER_LABELS.get(dominant_tier, "SaaS Toolkit")
            tier_color = _PM_TIER_COLOR.get(dominant_tier, "#2563eb")
            items = b["items"]

            sub_items_html = ""
            for c in items:
                c_title = escape(c.get("title", ""))
                c_val = c.get("value", {}).get("combined_annual_value_aud", 0)
                c_wlabel = escape(c.get("implementation", {}).get("weeks_label", ""))
                c_tier = _roi_tier_lookup.get(c.get("change_id", ""), "standard")
                c_tier_label = _PM_TIER_LABELS.get(c_tier, "SaaS Toolkit")
                c_tier_color = _PM_TIER_COLOR.get(c_tier, "#2563eb")
                c_type = escape(c.get("change_type", ""))
                mc = c.get("modal_content", {})
                c_desc = escape(mc.get("what_we_will_build", mc.get("what_is_the_task", "")))
                sub_items_html += f"""<div style="padding:12px 0;border-bottom:1px solid #F1F5F9">
                  <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:4px">
                    <div style="font-size:14px;font-weight:600;color:{BRAND_DARK}">{c_title}</div>
                    <div style="font-size:14px;font-weight:700;color:#059669;white-space:nowrap;margin-left:12px">{fmt_aud(c_val)}/yr</div>
                  </div>
                  <div style="display:flex;gap:6px;margin-bottom:6px">
                    <span style="background:{c_tier_color};color:#fff;border-radius:4px;padding:1px 8px;font-size:10px;font-weight:600">{c_tier_label}</span>
                    <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px;text-transform:uppercase">{c_type}</span>
                    <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px">{c_wlabel}</span>
                  </div>
                  <div style="font-size:13px;color:#64748b;line-height:1.4">{c_desc}</div>
                </div>\n"""

            pm_modals_html += f"""<div class="pm-modal-backdrop" id="modal-{group_id}" style="display:none" onclick="if(event.target===this)closeModal()">
  <div class="pm-modal">
    <button class="pm-modal-close" onclick="closeModal()">&times;</button>
    <div style="margin-bottom:16px">
      <h3 style="font-size:18px;font-weight:700;margin-bottom:8px">{label}</h3>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
        <span style="background:{tier_color};color:#fff;border-radius:4px;padding:1px 8px;font-size:10px;font-weight:600">{tier_label}</span>
        <span style="background:#1E293B;color:#E5E7EB;border-radius:4px;padding:1px 8px;font-size:10px">{len(items)} improvements</span>
      </div>
    </div>
    <div style="margin-bottom:16px">{sub_items_html}</div>
    <div class="pm-modal-stats">
      <div><span class="pm-modal-stat-val">{fmt_aud(annual_val)}</span><span class="pm-modal-stat-lbl">Combined annual value</span></div>
      <div><span class="pm-modal-stat-val">{len(items)}</span><span class="pm-modal-stat-lbl">Improvements</span></div>
    </div>
  </div>
</div>\n"""

    return (pm_quadrant_html, pm_modals_html)


# ─── Client Website Generator ──────────────────────────────────────────────────

def generate_client_website(ssad: dict, sections: dict = None) -> str:
    company = escape(ssad.get("company_name", "Client"))
    industry = escape(ssad.get("industry_tag", ""))
    generated = datetime.now().strftime("%d %b %Y")

    # Section unlock flags from clients.json (or fallback to all-locked)
    if sections is None:
        sections = {
            "process_map": False, "findings": False, "waste": False,
            "solutions_overview": False, "priority_matrix": False, "review": False, "transformation": False, "prototype": False,
        }
    sections_json = json.dumps(sections)

    # Pre-render transformation blueprint summary
    proposed_changes = ssad.get("proposed_changes", [])
    processes = ssad.get("processes", [])
    blueprint_data = ssad.get("transformation_blueprint", {})
    # Stats for blueprint summary
    _bp_actionable_types = {"step", "pain", "decision", "parallel_group"}
    total_steps = sum(len([s for s in p.get("steps", []) if not s.get("branch_only") and s.get("type", "step") in _bp_actionable_types]) for p in processes)
    _bp_eliminated = sum(1 for c in proposed_changes if c.get("change_type") == "eliminate")
    _bp_automated = sum(1 for c in proposed_changes if c.get("change_type") == "automate")
    _bp_consolidated_saved = sum(max(len(c.get("affected_step_ids", [])) - 1, 0) for c in proposed_changes if c.get("change_type") == "consolidate")
    steps_after = max(total_steps - _bp_eliminated - _bp_automated - _bp_consolidated_saved, 0)
    total_hrs_saved = sum((w.get("hours_per_week") or 0) * max(w.get("headcount_affected") or 1, 1) for w in ssad.get("waste_items", []))
    total_annual_value = sum((c.get("value") or {}).get("combined_annual_value_aud", 0) for c in proposed_changes)
    bp_phases = blueprint_data.get("phases", [])
    blueprint_stats_html = f"""<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-bottom:20px">
      <div style="background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:800;color:{BRAND_DARK}">{total_steps} &rarr; {steps_after}</div>
        <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:{BRAND_GREY}">Steps</div>
      </div>
      <div style="background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:800;color:{BRAND_DARK}">{total_hrs_saved:.0f} hrs/wk</div>
        <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:{BRAND_GREY}">Time saved</div>
      </div>
      <div style="background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:800;color:{BRAND_DARK}">${total_annual_value:,.0f}</div>
        <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:{BRAND_GREY}">Annual run rate</div>
      </div>
      <div style="background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:14px;text-align:center">
        <div style="font-size:22px;font-weight:800;color:{BRAND_DARK}">{len(bp_phases) or len(proposed_changes)}</div>
        <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:{BRAND_GREY}">{"Phases" if bp_phases else "Changes"}</div>
      </div>
    </div>"""
    # Phase timeline (if blueprint has been built)
    bp_phase_html = ""
    if bp_phases:
        phase_items = []
        for ph in bp_phases:
            ph_label = escape(ph.get("label", f"Phase {ph.get('phase_number', '?')}"))
            ph_time = escape(ph.get("timeframe", ""))
            ph_count = len(ph.get("change_ids", []))
            phase_items.append(f'<div style="flex:1;background:#fff;border:1px solid #E5E7EB;border-radius:8px;padding:12px;text-align:center;min-width:120px"><div style="font-size:10px;font-weight:700;text-transform:uppercase;color:{BRAND_PRIMARY_TEXT};letter-spacing:0.06em">Phase {ph.get("phase_number","")}</div><div style="font-size:14px;font-weight:800;color:{BRAND_DARK}">{ph_label}</div><div style="font-size:10px;color:{BRAND_GREY}">{ph_time} &middot; {ph_count} changes</div></div>')
        bp_phase_html = f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">{"".join(phase_items)}</div>'
    # ── Pre-render cumulative savings chart + Gantt for transformation section ──
    import math as _math
    savings_gantt_html = ""
    chart_tip_json = "[]"
    enriched_changes = [c for c in proposed_changes if c.get("value", {}).get("combined_annual_value_aud") is not None
                        and c.get("implementation", {}).get("weeks_estimate") is not None]
    if enriched_changes:
        # ── 5-month compressed schedule: front-load quick wins into M1-M2 ──
        NUM_MONTHS = 5
        sorted_changes = sorted(enriched_changes, key=lambda c: c["implementation"]["weeks_estimate"])

        # Split into quick wins (<=1 week) and core (>1 week)
        quick_items = [c for c in sorted_changes if c["implementation"]["weeks_estimate"] <= 1]
        core_items = [c for c in sorted_changes if c["implementation"]["weeks_estimate"] > 1]

        change_schedule = []
        # Quick wins: pack into M1 and M2, each takes 1 month
        for i, c in enumerate(quick_items):
            start = 0 if i < len(quick_items) // 2 else 1
            change_schedule.append({
                "cid": escape(c.get("change_id", "")),
                "title": escape(c.get("title", "")),
                "start": start,
                "end": start + 1,
                "monthly_value": c["value"]["combined_annual_value_aud"] / 12,
                "annual_value": c["value"]["combined_annual_value_aud"],
                "weeks": c["implementation"]["weeks_estimate"],
                "horizon": 1,
            })

        # Core items: spread across M2-M5 with duration based on weeks
        core_start = 1  # Start from M2
        for i, c in enumerate(core_items):
            weeks = c["implementation"]["weeks_estimate"]
            duration_months = max(1, min(3, _math.ceil(weeks / 2)))
            start = min(core_start, NUM_MONTHS - 1)
            end = min(start + duration_months, NUM_MONTHS)
            change_schedule.append({
                "cid": escape(c.get("change_id", "")),
                "title": escape(c.get("title", "")),
                "start": start,
                "end": end,
                "monthly_value": c["value"]["combined_annual_value_aud"] / 12,
                "annual_value": c["value"]["combined_annual_value_aud"],
                "weeks": weeks,
                "horizon": 2 if weeks <= 4 else 3,
            })
            core_start = start + max(1, duration_months // 2)
            if core_start >= NUM_MONTHS:
                core_start = NUM_MONTHS - 1

        # Compute cumulative savings: M1-M5 rollout, M6-M12 at full run rate
        CHART_MONTHS = 12
        monthly_cumulative = []
        cumulative = 0.0
        # M1-M5: staggered rollout
        for m in range(NUM_MONTHS):
            active_monthly = sum(cs["monthly_value"] for cs in change_schedule if cs["end"] <= m + 1)
            cumulative += active_monthly
            monthly_cumulative.append(round(cumulative / 1000, 1))
        # M6-M12: full monthly run rate (all items live)
        full_monthly_rate = total_annual_value / 12
        for m in range(NUM_MONTHS, CHART_MONTHS):
            cumulative += full_monthly_rate
            monthly_cumulative.append(round(cumulative / 1000, 1))

        max_cum = max(monthly_cumulative) if monthly_cumulative else 1
        final_cum = monthly_cumulative[-1] if monthly_cumulative else 0
        rollout_cum = monthly_cumulative[NUM_MONTHS - 1] if len(monthly_cumulative) >= NUM_MONTHS else 0

        # ── SVG Area Chart (12 months) ──
        SVG_W, SVG_H = 600, 220
        PAD_L, PAD_R, PAD_T, PAD_B = 50, 20, 10, 30
        chart_w = SVG_W - PAD_L - PAD_R
        chart_h = SVG_H - PAD_T - PAD_B

        def cx(month_idx):
            return PAD_L + (month_idx / (CHART_MONTHS - 1)) * chart_w

        def cy(val):
            if max_cum == 0:
                return PAD_T + chart_h
            return PAD_T + chart_h - (val / max_cum) * chart_h

        # Grid lines
        grid_svg = ""
        y_ticks = [v for v in [5, 10, 25, 50, 100, 200, 500] if v <= max_cum * 1.1]
        if not y_ticks:
            y_ticks = [max(1, round(max_cum / 2))]
        for yv in y_ticks:
            gy = cy(yv)
            grid_svg += f'<line x1="{PAD_L}" y1="{gy:.0f}" x2="{SVG_W - PAD_R}" y2="{gy:.0f}" stroke="{BRAND_BORDER}" stroke-width="1"/>'
            grid_svg += f'<text x="{PAD_L - 6}" y="{gy:.0f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="{BRAND_GREY}">${int(yv)}K</text>'

        # X-axis month labels
        x_labels = ""
        for i in range(CHART_MONTHS):
            x_labels += f'<text x="{cx(i):.0f}" y="{SVG_H - 8}" text-anchor="middle" font-size="10" fill="{BRAND_GREY}">M{i+1}</text>'

        # Solid area path (M1-M5 rollout)
        rollout_points = " ".join(f"{cx(i):.1f},{cy(monthly_cumulative[i]):.1f}" for i in range(NUM_MONTHS))
        rollout_bottom = f"{cx(NUM_MONTHS - 1):.1f},{PAD_T + chart_h} {cx(0):.1f},{PAD_T + chart_h}"

        # Projected area path (M5-M12 dashed)
        proj_points = " ".join(f"{cx(i):.1f},{cy(monthly_cumulative[i]):.1f}" for i in range(NUM_MONTHS - 1, CHART_MONTHS))
        proj_bottom = f"{cx(CHART_MONTHS - 1):.1f},{PAD_T + chart_h} {cx(NUM_MONTHS - 1):.1f},{PAD_T + chart_h}"

        # Vertical separator at M5
        sep_x = cx(NUM_MONTHS - 1)
        separator_svg = f'<line x1="{sep_x:.1f}" y1="{PAD_T}" x2="{sep_x:.1f}" y2="{PAD_T + chart_h}" stroke="{BRAND_GREY}" stroke-width="1" stroke-dasharray="4 3" opacity="0.5"/>'
        separator_svg += f'<text x="{(cx(0) + sep_x) / 2:.0f}" y="{PAD_T + 14}" text-anchor="middle" font-size="9" fill="{BRAND_GREY}" font-weight="600">ROLLOUT</text>'
        separator_svg += f'<text x="{(sep_x + cx(CHART_MONTHS - 1)) / 2:.0f}" y="{PAD_T + 14}" text-anchor="middle" font-size="9" fill="{BRAND_GREY}" font-weight="600">FULL RUN RATE</text>'

        # Pre-compute per-month breakdown for tooltip
        month_breakdown = []
        for m in range(CHART_MONTHS):
            if m < NUM_MONTHS:
                live_this_month = [cs for cs in change_schedule if cs["end"] == m + 1]
                lines = []
                for cs in live_this_month:
                    v = f"${cs['annual_value']/1000:.0f}k/yr" if cs["annual_value"] >= 1000 else f"${cs['annual_value']:,.0f}/yr"
                    lines.append(f"{cs['title']}: {v}")
                month_breakdown.append(lines)
            else:
                month_breakdown.append(["All items live \u2014 full run rate"])

        # Build SVG dots for all 12 months
        dots_svg = ""
        import json as _json
        chart_tip_data = []
        for i in range(CHART_MONTHS):
            dot_cx = cx(i)
            dot_cy = cy(monthly_cumulative[i])
            chart_tip_data.append({
                "month": f"M{i+1}",
                "cumulative": f"${monthly_cumulative[i]:.0f}K cumulative",
                "items": month_breakdown[i],
            })
            is_projected = i >= NUM_MONTHS
            dot_fill = "#7DFF00" if not is_projected else f"{BRAND_GREY}"
            dot_stroke = "#ffffff"
            dots_svg += f"""<circle cx="{dot_cx:.1f}" cy="{dot_cy:.1f}" r="{'4' if is_projected else '5'}" fill="{dot_fill}" stroke="{dot_stroke}" stroke-width="2"
              style="cursor:pointer;transition:r 0.15s"
              onmouseenter="this.setAttribute('r','8');showChartDot(this,{i})"
              onmouseleave="this.setAttribute('r','{'4' if is_projected else '5'}');hideChartTip()"/>
            """
        chart_tip_json = _json.dumps(chart_tip_data)

        area_chart_svg = f"""<div style="position:relative">
          <svg viewBox="0 0 {SVG_W} {SVG_H}" style="width:100%;height:auto;display:block">
          <defs>
            <linearGradient id="sg" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#7DFF00" stop-opacity="0.25"/>
              <stop offset="100%" stop-color="#7DFF00" stop-opacity="0.03"/>
            </linearGradient>
            <linearGradient id="sg-proj" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#7DFF00" stop-opacity="0.10"/>
              <stop offset="100%" stop-color="#7DFF00" stop-opacity="0.01"/>
            </linearGradient>
          </defs>
          {grid_svg}
          <line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{PAD_T + chart_h}" stroke="{BRAND_BORDER}" stroke-width="1"/>
          <line x1="{PAD_L}" y1="{PAD_T + chart_h}" x2="{SVG_W - PAD_R}" y2="{PAD_T + chart_h}" stroke="{BRAND_BORDER}" stroke-width="1"/>
          <polygon points="{rollout_points} {rollout_bottom}" fill="url(#sg)"/>
          <polygon points="{proj_points} {proj_bottom}" fill="url(#sg-proj)"/>
          <polyline points="{rollout_points}" fill="none" stroke="#7DFF00" stroke-width="2.5" stroke-linejoin="round"/>
          <polyline points="{proj_points}" fill="none" stroke="#7DFF00" stroke-width="2" stroke-linejoin="round" stroke-dasharray="6 4"/>
          {separator_svg}
          {dots_svg}
          {x_labels}
        </svg>
        <div id="chart-tip" style="display:none;position:absolute;pointer-events:none;background:{BRAND_DARK};color:#fff;
             border-radius:8px;padding:10px 14px;font-size:12px;z-index:100;max-width:300px;box-shadow:0 4px 12px rgba(0,0,0,0.3)"></div>
        </div>"""

        # ── Gantt Timeline (5 months) ──
        h1 = [cs for cs in change_schedule if cs["horizon"] == 1]
        h2 = [cs for cs in change_schedule if cs["horizon"] == 2]
        h3 = [cs for cs in change_schedule if cs["horizon"] == 3]
        gantt_horizons = [
            ("Horizon 1 — Quick Wins", h1, "1"),
            ("Horizon 2 — Core Platform", h2, "0.7"),
            ("Horizon 3 — Growth Engine", h3, "0.4"),
        ]

        month_headers = "".join(f'<div style="text-align:center;font-size:10px;color:{BRAND_GREY};font-family:monospace">M{i+1}</div>' for i in range(NUM_MONTHS))
        gantt_rows = ""
        for label, items, opacity in gantt_horizons:
            if not items:
                continue
            gantt_rows += f'<div style="font-size:11px;font-weight:700;color:{BRAND_PRIMARY_TEXT};text-transform:uppercase;letter-spacing:0.08em;margin:16px 0 8px 0">{label}</div>'
            for item in items:
                cid = item["cid"]
                title = item["title"]
                val_label = f"${item['annual_value']/1000:.0f}k/yr" if item["annual_value"] >= 1000 else f"${item['annual_value']:,.0f}/yr"
                cells = ""
                for mi in range(NUM_MONTHS):
                    if mi >= item["start"] and mi < item["end"]:
                        cells += f'<div style="height:24px;padding:0 1px"><div onclick="openModal(&quot;{cid}&quot;)" style="height:100%;background:{BRAND_PRIMARY};opacity:{opacity};border-radius:2px;cursor:pointer" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity={opacity}"></div></div>'
                    else:
                        cells += '<div style="height:24px"></div>'
                name_html = (
                    f'<span onclick="openModal(&quot;{cid}&quot;)" '
                    f'style="cursor:pointer;border-bottom:1px dashed {BRAND_BORDER};padding-bottom:1px" '
                    f'onmouseover="this.style.color=&quot;{BRAND_PRIMARY_TEXT}&quot;" '
                    f'onmouseout="this.style.color=&quot;{BRAND_GREY}&quot;">'
                    f'{title}</span> <span style="font-size:10px;font-weight:700;color:{BRAND_PRIMARY_TEXT}">{val_label}</span>'
                )
                gantt_rows += f'<div style="display:grid;grid-template-columns:240px repeat({NUM_MONTHS},1fr);gap:0;margin-bottom:4px;align-items:center"><div style="font-size:12px;color:{BRAND_GREY};overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:8px">{name_html}</div>{cells}</div>'

        savings_gantt_html = f"""<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px 28px;margin-top:24px">
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{BRAND_GREY};margin-bottom:16px">Cumulative Savings ($K)</div>
          {area_chart_svg}
          <div style="display:flex;justify-content:flex-end;margin-top:8px;align-items:baseline">
            <span style="font-size:18px;font-weight:800;color:var(--lime-text)">${final_cum:.0f}K</span>
            <span style="font-size:13px;color:{BRAND_GREY};margin-left:4px">projected Year 1 total</span>
          </div>
        </div>
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px 28px;margin-top:16px;overflow-x:auto">
          <div style="display:grid;grid-template-columns:240px repeat({NUM_MONTHS},1fr);gap:0;margin-bottom:12px">
            <div></div>{month_headers}
          </div>
          {gantt_rows}
        </div>"""

    savings_gantt_js = savings_gantt_html.replace("'", "\\'").replace("\n", " ")

    # Escape for JS embedding (single quotes, newlines)
    blueprint_content_js = (blueprint_stats_html + bp_phase_html + savings_gantt_html).replace("'", "\\'").replace("\n", " ")

    # ── Pre-render quadrant priority matrix for embedding (grouped by process area) ──
    pm_quadrant_html, pm_modals_html = _render_quadrant_matrix(ssad, enriched_changes)

    pm_quadrant_js = pm_quadrant_html.replace("'", "\\'").replace("\n", " ")

    # Format audit start date from "2026-03-12" to "12 Mar 2026"
    raw_start = ssad.get("audit_start_date", "")
    if raw_start:
        try:
            audit_start_display = datetime.strptime(raw_start, "%Y-%m-%d").strftime("%d %b %Y")
        except ValueError:
            audit_start_display = escape(raw_start)
    else:
        audit_start_display = generated

    sessions = ssad.get("sessions", [])
    # Deduplicate waste_items by waste_id (must match waste.html logic)
    _raw_waste = ssad.get("waste_items", [])
    _seen_wids: set = set()
    waste_items = []
    for _w in _raw_waste:
        _wid = _w.get("waste_id", "")
        if _wid and _wid in _seen_wids:
            continue
        _seen_wids.add(_wid)
        waste_items.append(_w)

    roi_items = ssad.get("roi_items", [])

    all_pain_points = ssad.get("pain_points", [])
    all_optimisations = ssad.get("optimisations", [])
    # Fallback: count optimisation steps from processes if optimisations[] is empty
    opp_count = len(all_optimisations) if all_optimisations else sum(
        1 for p in ssad.get("processes", []) for s in p.get("steps", []) if s.get("type") == "optimisation"
    )
    findings_count = len(all_pain_points) + opp_count

    qualified_waste = [w for w in waste_items if w.get("confidence") in ("HIGH", "MEDIUM")]
    total_annual = sum(w.get("annual_waste_aud") or 0 for w in qualified_waste)
    total_monthly = sum(w.get("monthly_waste_aud") or 0 for w in qualified_waste)

    # Pre-compute available downloads for the downloads section
    _downloads = [
        {"file": "process-map.html", "label": "How You Work", "desc": "Full map of your current operations across every business stage.", "icon": "&#128506;"},
        {"file": "findings.html", "label": "What We Found", "desc": "Pain points and optimisation opportunities from our sessions.", "icon": "&#128269;"},
        {"file": "waste.html", "label": "Hidden Costs", "desc": "Operational waste breakdown with annual and monthly costs.", "icon": "&#128200;"},
    ]
    if proposed_changes and any(c.get("research", {}).get("status") for c in proposed_changes):
        _downloads.append({"file": "solutions-overview.html", "label": "Opportunities", "desc": "Researched approaches for every identified opportunity.", "icon": "&#128300;"})
        _downloads.append({"file": "strategic-approaches.html", "label": "Options & Pricing", "desc": "Full cost comparison, timeline, priority matrix, and prototype — everything you need to decide.", "icon": "&#127919;"})
    if sections and sections.get("prototype") and sections.get("prototype_url"):
        _downloads.append({"file": sections["prototype_url"], "label": "Clickable Prototype", "desc": "Interactive walkthrough of your future platform — click through real screens and flows.", "icon": "&#128241;"})
    is_demo = ssad.get("client_slug", "").startswith("demo-")
    if Path(f"clients/{ssad.get('client_slug', '')}/deliverables/audit-report.pdf").exists():
        _dl = {"file": "audit-report.pdf", "label": "Full Audit Report (PDF)", "desc": "Complete audit report with all findings, solutions, strategy, and roadmap.", "icon": "&#128218;", "pdf": True}
        if is_demo:
            _dl["demo"] = True
        _downloads.append(_dl)
    else:
        _downloads.append({"file": "audit-report-print.html", "label": "Full Audit Report", "desc": "Complete audit summary \u2014 opens and saves as a PDF document.", "icon": "&#128196;", "pdf": True})
    downloads_json = json.dumps(_downloads)

    demo_pdf_modal_html = ""
    if is_demo:
        demo_pdf_modal_html = f"""<div class="pm-modal-backdrop" id="modal-demo-pdf" style="display:none" onclick="if(event.target===this)closeModal()">
  <div class="pm-modal" style="text-align:center;padding:40px 32px">
    <button class="pm-modal-close" onclick="closeModal()">&times;</button>
    <div style="font-size:48px;margin-bottom:16px">&#128218;</div>
    <h3 style="font-size:20px;font-weight:700;margin:0 0 12px">Full Audit Report</h3>
    <p style="font-size:15px;line-height:1.6;color:var(--muted);margin:0 0 20px">This is a public demo portal. In a real engagement, this downloads a comprehensive 40+ page PDF report covering all findings, solutions, strategic recommendations, and your transformation roadmap.</p>
    <button onclick="closeModal()" class="btn-download" style="cursor:pointer;margin:0 auto">Got it</button>
  </div>
</div>"""

    # Stage labels from audit data
    stage_label_map, _ = _build_stage_lookups(ssad)

    def _fmt_date(raw: str) -> str:
        """Format 2026-03-12 to 12 Mar 2026."""
        try:
            return datetime.strptime(raw, "%Y-%m-%d").strftime("%d %b %Y")
        except (ValueError, TypeError):
            return escape(str(raw)) if raw else ""

    # Derive hero status text from unlocked sections
    _section_status_order = [
        ("prototype", "Audit complete &mdash; your prototype is ready to explore."),
        ("priority_matrix", "Audit complete &mdash; priority matrix mapped."),
        ("transformation", "Audit in progress &mdash; transformation blueprint ready."),
        ("strategic_approaches", "Audit in progress &mdash; strategic approaches outlined."),
        ("solutions_overview", "Audit in progress &mdash; solutions researched."),
        ("waste", "Audit in progress &mdash; waste analysis complete."),
        ("findings", "Audit in progress &mdash; findings analysis complete."),
        ("process_map", "Audit in progress &mdash; process map under review."),
    ]
    hero_status_text = "Audit in progress &mdash; discovery sessions underway."
    for sec_key, status_text in _section_status_order:
        if sections.get(sec_key):
            hero_status_text = status_text
            break

    # ── Derive stages_covered per session from processes if not in session data ──
    _session_stages: dict = {}  # session_number → set of stage keys
    for proc in ssad.get("processes", []):
        stage_key = proc.get("stage", "")
        for step in proc.get("steps", []):
            src = step.get("source_session")
            if src and stage_key:
                _session_stages.setdefault(src, set()).add(stage_key)

    # Canonical stage order for sorting
    _stage_order = ["acquisition", "onboarding_family", "recruitment", "fulfilment",
                    "onboarding_nanny", "payroll_invoicing", "health_safety", "retention"]

    # ── Meeting cards HTML (exclude document-type sessions) ──
    meeting_cards_html = ""
    meeting_count = 0
    for s in sessions:
        # Skip non-meeting sessions (documents, emails) — only show actual meetings
        if s.get("session_type") in ("document", "email"):
            continue
        meeting_count += 1
        s_num = meeting_count
        s_date = _fmt_date(s.get("date", ""))
        s_title = escape(s.get("title", f"Session {s_num}"))
        # Fallback: build summary from key_findings if summary field is missing
        s_summary_raw = s.get("summary", "")
        if not s_summary_raw and s.get("key_findings"):
            s_summary_raw = ". ".join(s["key_findings"][:5])
            if len(s["key_findings"]) > 5:
                s_summary_raw += "."
        s_summary = escape(s_summary_raw)
        stages_covered = s.get("stages_covered", [])
        orig_num = s.get("session_number", "")
        if not stages_covered and orig_num in _session_stages:
            stages_covered = sorted(_session_stages[orig_num],
                                    key=lambda x: _stage_order.index(x) if x in _stage_order else 99)
        stage_tags = ""
        for sc in stages_covered:
            label = stage_label_map.get(sc, escape(sc).replace("_", " ").title())
            stage_tags += f'<span class="stage-tag">{label}</span>\n          '
        meeting_cards_html += f"""
      <div class="meeting-card">
        <div class="meeting-card-head">
          <span class="session-badge">Session {s_num}</span>
          <span class="complete-badge">&#10003; Complete</span>
        </div>
        <div class="meeting-date">{s_date}</div>
        <div class="meeting-title">{s_title}</div>
        <div class="meeting-summary">{s_summary}</div>
        <div class="stage-tags">
          {stage_tags.strip()}
        </div>
      </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} &mdash; Business Operations Audit</title>
<link rel="icon" type="image/png" href="{YOUR_LOGO_URL}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #f7f9fc;
  --card: #ffffff;
  --border: #e2e8f0;
  --lime: #7DFF00;
  --lime-text: #166534;   /* dark green — 7.1:1 on white, use for all lime-coloured text */
  --muted: #64748b;
  --fg: #0f1825;
  --lime-dim: rgba(125,255,0,0.08);
  --lime-glow: 0 4px 20px rgba(0,0,0,0.08);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--fg);
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: inherit; text-decoration: none; }}

/* ── Nav ── */
.site-nav {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(247,249,252,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 24px;
}}
.nav-inner {{
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}}
.nav-logo {{ height: 32px; display: block; }}
.nav-client {{
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  letter-spacing: -0.01em;
}}

/* ── Layout ── */
.site-container {{ max-width: 960px; margin: 0 auto; padding: 0 24px; }}

/* ── Hero ── */
.hero {{
  padding: 80px 24px 72px;
  text-align: center;
  position: relative;
  overflow: hidden;
  background-image:
    linear-gradient(rgba(0,0,0,0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.035) 1px, transparent 1px);
  background-size: 60px 60px;
}}
.hero::before {{
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 50% at 50% 0%, rgba(125,255,0,0.12) 0%, transparent 70%);
  pointer-events: none;
}}
.hero-apg-label {{
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--lime-text);
  margin-bottom: 20px;
}}
.hero h1 {{
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--fg);
  line-height: 1.05;
  margin-bottom: 16px;
}}
.hero-meta {{
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 16px;
}}
.hero-status {{
  display: inline-block;
  font-size: 13px;
  color: var(--fg);
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--lime);
  border-radius: 8px;
  padding: 10px 20px;
  margin-top: 8px;
}}

/* ── Sections ── */
.page-section {{
  padding: 80px 0;
  border-bottom: 1px solid var(--border);
}}
.section-label {{
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--lime-text);
  margin-bottom: 12px;
}}
.section-heading {{
  font-size: clamp(24px, 4vw, 40px);
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--fg);
  margin-bottom: 8px;
}}
.section-sub {{
  font-size: 15px;
  color: var(--muted);
  margin-bottom: 40px;
}}

/* ── Progress Bar ── */
.progress-bar-wrap {{
  margin: 36px 0 40px;
  overflow-x: auto;
  padding-bottom: 4px;
}}
.progress-steps {{
  display: flex;
  align-items: center;
  gap: 0;
  min-width: 560px;
}}
.progress-step {{
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  position: relative;
}}
.progress-step:not(:last-child)::after {{
  content: '';
  position: absolute;
  top: 14px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--border);
  z-index: 0;
}}
.progress-step.done:not(:last-child)::after,
.progress-step.active:not(:last-child)::after {{
  background: var(--lime);
}}
.step-dot {{
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--card);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  position: relative;
  z-index: 1;
  margin-bottom: 8px;
}}
.progress-step.done .step-dot {{
  background: var(--lime);
  border-color: var(--lime);
  color: #0f1825;
}}
.progress-step.active .step-dot {{
  background: var(--card);
  border-color: var(--lime);
  color: var(--lime-text);
  box-shadow: 0 0 0 4px rgba(125,255,0,0.18);
}}
.step-name {{
  font-size: 11px;
  font-weight: 600;
  color: var(--muted);
  text-align: center;
  white-space: nowrap;
}}
.progress-step.done .step-name,
.progress-step.active .step-name {{
  color: var(--fg);
}}

/* ── Meeting Cards ── */
.meetings-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 32px;
}}
.meeting-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  transition: box-shadow 0.2s;
}}
.meeting-card:hover {{ box-shadow: var(--lime-glow); }}
.meeting-card-head {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
  gap: 12px;
}}
.session-badge {{
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #0f1825;
  background: var(--lime);
  border-radius: 6px;
  padding: 3px 10px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.complete-badge {{
  font-size: 10px;
  font-weight: 700;
  color: var(--lime-text);
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 6px;
  padding: 3px 10px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.meeting-date {{
  font-size: 11px;
  color: var(--muted);
  margin-bottom: 6px;
}}
.meeting-title {{
  font-size: 14px;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 10px;
  line-height: 1.4;
}}
.meeting-summary {{
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 14px;
}}
.stage-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}}
.stage-tag {{
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
  background: #f1f5f9;
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 2px 8px;
}}

/* ── Process Map Feature Card ── */
.pm-feature-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  margin-top: 0;
  position: relative;
}}
.pm-feature-card::before {{
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 80% at 80% 50%, rgba(125,255,0,0.10) 0%, transparent 70%);
  pointer-events: none;
}}
.pm-feature-top {{
  border-top: 3px solid var(--lime);
}}
.pm-feature-inner {{
  padding: 40px 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  flex-wrap: wrap;
}}
.pm-feature-text {{ flex: 1; min-width: 260px; }}
.pm-ready-badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--lime-text);
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 20px;
  padding: 4px 14px;
  margin-bottom: 16px;
}}
.pm-ready-dot {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--lime);
  animation: pulse-dot 1.8s ease-in-out infinite;
}}
@keyframes pulse-dot {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50% {{ opacity: 0.5; transform: scale(0.7); }}
}}
.pm-feature-heading {{
  font-size: clamp(22px, 3vw, 32px);
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--fg);
  line-height: 1.1;
  margin-bottom: 10px;
}}
.pm-feature-sub {{
  font-size: 14px;
  color: var(--muted);
  line-height: 1.6;
  max-width: 440px;
}}
.pm-feature-action {{ flex-shrink: 0; }}
.btn-pm {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--lime);
  color: #0f1825;
  font-weight: 900;
  font-size: 15px;
  padding: 16px 36px;
  border-radius: 10px;
  letter-spacing: -0.02em;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 0 0 0 rgba(125,255,0,0.3);
  white-space: nowrap;
}}
.btn-pm:hover {{
  opacity: 0.95;
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(125,255,0,0.2);
}}
.btn-pm-arrow {{
  font-size: 18px;
  transition: transform 0.2s;
}}
.btn-pm:hover .btn-pm-arrow {{ transform: translateX(3px); }}

/* ── Process Map Button (old / generic) ── */
.btn-primary {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--lime);
  color: #0f1825;
  font-weight: 800;
  font-size: 14px;
  padding: 12px 28px;
  border-radius: 8px;
  letter-spacing: -0.01em;
  transition: opacity 0.2s, transform 0.1s;
}}
.btn-primary:hover {{ opacity: 0.9; transform: translateY(-1px); }}
.btn-disabled {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f1f5f9;
  color: var(--muted);
  font-weight: 700;
  font-size: 14px;
  padding: 12px 28px;
  border-radius: 8px;
  letter-spacing: -0.01em;
  cursor: not-allowed;
  border: 1px solid var(--border);
  position: relative;
}}
.btn-tooltip {{
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: #334155;
  color: #ffffff;
  font-size: 11px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 6px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s;
}}
.btn-disabled:hover .btn-tooltip {{ opacity: 1; }}

/* ── Lock Card ── */
.lock-card {{
  background: var(--card);
  border: 2px dashed var(--border);
  border-radius: 12px;
  padding: 48px 40px;
  text-align: center;
  margin-top: 32px;
  position: relative;
  overflow: hidden;
}}
.lock-icon {{
  font-size: 28px;
  margin-bottom: 12px;
}}
.lock-title {{
  font-size: 16px;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 8px;
}}
.lock-label {{
  font-size: 14px;
  color: var(--muted);
  max-width: 360px;
  margin: 0 auto;
}}
.lock-ghost {{
  margin-top: 28px;
  filter: blur(3px);
  opacity: 0.45;
  pointer-events: none;
  user-select: none;
}}

/* ── Pain Point Cards ── */
.pain-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 32px;
}}
.pain-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--lime);
  border-radius: 12px;
  padding: 24px;
  transition: box-shadow 0.2s;
}}
.pain-card:hover {{ box-shadow: var(--lime-glow); }}
.pain-desc {{
  font-weight: 600;
  font-size: 15px;
  color: var(--fg);
  margin-bottom: 12px;
}}
.pain-divider {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 12px 0;
}}
.pain-quote {{
  font-size: 13px;
  font-style: italic;
  color: var(--muted);
  line-height: 1.5;
}}

/* ── Bottom Line ── */
.bottomline-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 48px;
  text-align: center;
  margin-top: 32px;
  position: relative;
  overflow: hidden;
}}
.bottomline-card::before {{
  content: '';
  position: absolute;
  top: -60px; left: 50%; transform: translateX(-50%);
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(125,255,0,0.14) 0%, transparent 70%);
  pointer-events: none;
}}
.waste-label {{
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--lime-text);
  margin-bottom: 16px;
}}
.waste-number {{
  font-size: clamp(56px, 10vw, 96px);
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--lime-text);
  font-variant-numeric: tabular-nums;
  line-height: 1;
}}
.waste-sub {{
  font-size: 20px;
  color: var(--muted);
  margin-top: 8px;
  margin-bottom: 24px;
}}
.waste-explain {{
  font-size: 14px;
  color: var(--muted);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.6;
}}

/* ── Dark Table ── */
.dark-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}}
.dark-table thead tr {{
  border-bottom: 2px solid var(--border);
}}
.dark-table th {{
  padding: 10px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}}
.dark-table td {{
  padding: 12px 14px;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}}
.dark-table tbody tr:hover td {{ background: var(--lime-dim); color: var(--fg); }}
.conf-badge {{
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}}
.source-cell {{
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-style: italic;
}}

/* ── Horizons ── */
.horizons-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 32px;
}}
.horizon-col {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
}}
.horizon-title {{
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 4px;
}}
.horizon-subtitle {{
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}}
.horizon-row {{
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}}
.horizon-row:last-child {{ border-bottom: none; }}
.horizon-name {{
  font-size: 13px;
  font-weight: 600;
  color: var(--fg);
  margin-bottom: 4px;
}}
.horizon-build {{
  font-size: 12px;
  color: var(--muted);
}}
.horizon-saving {{
  font-size: 13px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}}
.horizon-empty {{
  font-size: 13px;
  color: var(--muted);
  text-align: center;
  padding: 20px 0;
}}

/* ── Quadrant Priority Matrix ── */
.qm-container {{
  position: relative;
  aspect-ratio: 16/10;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 48px;
  overflow: visible;
  margin-top: 40px;
}}
.qm-axis-x {{
  position: absolute;
  left: 48px; right: 48px; bottom: 48px;
  height: 2px;
  background: var(--fg);
  opacity: 0.5;
}}
.qm-axis-y {{
  position: absolute;
  left: 48px; top: 48px; bottom: 48px;
  width: 2px;
  background: var(--fg);
  opacity: 0.5;
}}
.qm-mid-x {{
  position: absolute;
  left: 48px; right: 48px; top: 50%;
  height: 1px;
  background: var(--fg);
  opacity: 0.2;
}}
.qm-mid-y {{
  position: absolute;
  top: 48px; bottom: 48px; left: 50%;
  width: 1px;
  background: var(--fg);
  opacity: 0.2;
}}
.qm-label {{
  position: absolute;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  opacity: 0.4;
}}
.qm-label-tl {{ top: 56px; left: 56px; }}
.qm-label-tr {{ top: 56px; right: 56px; opacity: 1 !important; }}
.qm-label-br {{ bottom: 56px; right: 56px; opacity: 1 !important; }}
.qm-label-bl {{ bottom: 56px; left: 56px; }}
.qm-axis-label-x {{
  position: absolute;
  bottom: 8px; left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}}
.qm-axis-label-y {{
  position: absolute;
  left: 4px; top: 50%;
  transform: translateY(-50%) rotate(-90deg);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  white-space: nowrap;
}}
.qm-bubble {{
  position: absolute;
  border-radius: 50%;
  border: 2px solid;
  transform: translate(-50%, 50%);
  cursor: pointer;
  transition: all 0.3s ease;
}}
.qm-bubble.qm-dimmed {{
  opacity: 0.3 !important;
}}
.qm-bubble.qm-active {{
  transform: translate(-50%, 50%) scale(1.25) !important;
}}
.qm-tip {{
  display: none;
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  z-index: 20;
  white-space: nowrap;
  pointer-events: none;
}}
.qm-bubble.qm-active .qm-tip {{ display: block; }}
.qm-legend {{
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}}
.qm-legend-btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  color: var(--fg);
}}
.qm-legend-btn:hover, .qm-legend-btn.qm-legend-active {{
  border-color: var(--lime);
  background: rgba(125,255,0,0.08);
}}

/* ── Transformation Blueprint ── */
.blueprint-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  margin-top: 32px;
}}
.blueprint-cols {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}}
.blueprint-col-label {{
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 12px;
}}
.blueprint-col-label.current {{ color: #ef4444; }}
.blueprint-col-label.proposed {{ color: var(--lime-text); }}
.blueprint-col-body {{
  font-size: 14px;
  color: var(--muted);
  line-height: 1.7;
}}
.blueprint-cta {{
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}}
.coming-soon-badge {{
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  background: #f1f5f9;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 12px;
}}

/* ── Interactive Priority Matrix (embedded chart) ── */
.pm-bubble {{ position:absolute; border-radius:50%; border:2px solid; opacity:0.85;
              cursor:pointer; display:flex; align-items:center; justify-content:center;
              transform:translate(-50%,-50%); transition:transform 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease; }}
.pm-bubble:hover {{ transform:translate(-50%,-50%) scale(1.18); opacity:1; box-shadow:0 4px 16px rgba(0,0,0,0.25); z-index:10; }}
.pm-bubble-label {{ font-weight:700; color:#fff; pointer-events:none; text-shadow:0 1px 2px rgba(0,0,0,0.5); line-height:1.1; }}
@keyframes pm-pulse {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(5,150,105,0.3); }} 50% {{ box-shadow:0 0 0 8px rgba(5,150,105,0); }} }}
.pm-bubble-top {{ animation:pm-pulse 2s ease-in-out 3; }}
.pm-modal-backdrop {{ position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.6);
                      z-index:2000; display:flex; align-items:center; justify-content:center; padding:24px; }}
.pm-modal {{ background:var(--card); border-radius:14px; max-width:560px; width:100%; max-height:85vh; overflow-y:auto;
             padding:28px 32px; position:relative; box-shadow:0 20px 60px rgba(0,0,0,0.3); }}
.pm-modal-close {{ position:absolute; top:12px; right:16px; background:none; border:none; font-size:24px;
                   color:var(--muted); cursor:pointer; padding:4px 8px; line-height:1; }}
.pm-modal-close:hover {{ color:var(--fg); }}
.pm-modal-section {{ margin-bottom:16px; }}
.pm-modal-section h4 {{ font-size:13px; font-weight:700; color:var(--muted); text-transform:uppercase;
                        letter-spacing:0.05em; margin-bottom:4px; }}
.pm-modal-section p {{ font-size:14px; line-height:1.55; color:var(--fg); }}
.pm-modal-formula {{ background:#F0FDF4; border:1px solid #BBF7D0; border-radius:6px; padding:8px 12px;
                     font-size:13px; font-weight:600; color:#166534; margin:8px 0 16px 0; font-family:monospace; }}
.pm-modal-stats {{ display:flex; gap:24px; margin-top:20px; padding-top:16px; border-top:1px solid var(--border); }}
.pm-modal-stat-val {{ font-size:20px; font-weight:800; color:var(--fg); display:block; }}
.pm-modal-stat-lbl {{ font-size:10px; text-transform:uppercase; letter-spacing:0.06em; color:var(--muted); }}

/* ── Downloads ── */
.downloads-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 8px;
}}
.download-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
.download-card:hover {{
  border-color: var(--lime);
  box-shadow: 0 4px 16px rgba(125, 255, 0, 0.08);
}}
.download-icon {{
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(125, 255, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}}
.download-card h3 {{
  font-size: 15px;
  font-weight: 700;
  color: var(--fg);
  margin: 0;
}}
.download-card p {{
  font-size: 13px;
  color: var(--muted);
  line-height: 1.5;
  margin: 0;
  flex: 1;
}}
.btn-download {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  background: var(--lime);
  color: #166534;
  transition: opacity 0.15s ease;
  align-self: flex-start;
}}
.btn-download:hover {{ opacity: 0.85; }}
.btn-download-pdf {{
  background: transparent;
  border: 1px solid var(--lime);
  color: var(--lime-text);
}}
.btn-download-pdf:hover {{ background: rgba(125, 255, 0, 0.08); opacity: 1; }}

/* ── Prototype CTA (in deliverables section) ── */
.prototype-cta {{
  margin-top: 28px;
  background: linear-gradient(135deg, #0f1825 0%, #1a2e12 100%);
  border: 1px solid rgba(125, 255, 0, 0.2);
  border-radius: 16px;
  padding: 36px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
.prototype-cta:hover {{
  border-color: var(--lime);
  box-shadow: 0 8px 32px rgba(125, 255, 0, 0.12);
}}
.prototype-cta-text {{
  flex: 1;
}}
.prototype-cta-badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--lime);
  margin-bottom: 10px;
}}
.prototype-cta-badge .dot {{
  width: 6px; height: 6px; border-radius: 50%; background: var(--lime);
}}
.prototype-cta h3 {{
  font-size: 22px;
  font-weight: 800;
  color: #fff;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}}
.prototype-cta p {{
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  line-height: 1.5;
  max-width: 520px;
}}
.btn-prototype {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  background: var(--lime);
  color: #0f1825;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  white-space: nowrap;
}}
.btn-prototype:hover {{
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(125, 255, 0, 0.25);
}}
.btn-prototype .arrow {{
  font-size: 18px;
  transition: transform 0.15s ease;
}}
.btn-prototype:hover .arrow {{
  transform: translateX(3px);
}}
@media (max-width: 768px) {{
  .prototype-cta {{ flex-direction: column; text-align: center; padding: 28px 24px; }}
  .prototype-cta p {{ max-width: none; }}
  .btn-prototype {{ width: 100%; justify-content: center; }}
}}

/* ── Footer ── */
.site-footer {{
  padding: 32px 0;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 12px;
  color: var(--muted);
}}

/* ── Responsive ── */
@media (max-width: 768px) {{
  .pm-feature-inner {{ flex-direction: column; gap: 28px; padding: 32px 24px; }}
  .btn-pm {{ width: 100%; justify-content: center; }}
  .meetings-grid {{ grid-template-columns: 1fr; }}
  .horizons-grid {{ grid-template-columns: 1fr; }}
  .qm-container {{ padding: 24px; }}
  .qm-label {{ font-size: 8px; }}
  .qm-axis-x {{ left: 24px; right: 24px; bottom: 24px; }}
  .qm-axis-y {{ left: 24px; top: 24px; bottom: 24px; }}
  .qm-mid-x {{ left: 24px; right: 24px; }}
  .qm-mid-y {{ top: 24px; bottom: 24px; }}
  .qm-label-tl, .qm-label-tr {{ top: 28px; }}
  .qm-label-bl, .qm-label-br {{ bottom: 28px; }}
  .qm-label-tl, .qm-label-bl {{ left: 28px; }}
  .qm-label-tr, .qm-label-br {{ right: 28px; }}
  .blueprint-cols {{ grid-template-columns: 1fr; gap: 20px; }}
  .bottomline-card {{ padding: 32px 24px; }}
  .blueprint-card {{ padding: 28px 24px; }}
  .lock-card {{ padding: 40px 24px; }}
}}
</style>
</head>
<body>

<script>
var SECTIONS = {sections_json};
var STAGE_ORDER = ['process_map','findings','waste','solutions_overview','strategic_approaches'];
function stageReached(s) {{ return !!SECTIONS[s]; }}
</script>

<!-- ── Nav ── -->
<nav class="site-nav">
  <div class="nav-inner">
    <img src="{YOUR_LOGO_URL}" alt="{YOUR_COMPANY}" class="nav-logo">
    <span class="nav-client">{company}</span>
  </div>
</nav>

<!-- ── Hero ── -->
<section class="hero">
  <div class="hero-apg-label">{YOUR_COMPANY} &middot; Business Operations Audit</div>
  <h1>{company}</h1>
  <div class="hero-meta">{industry}{" &middot; " if industry else ""}Audit started {audit_start_display}</div>
  <div class="hero-status" id="hero-status">{hero_status_text}</div>
</section>

<!-- ── Audit Journey ── -->
<section class="page-section">
  <div class="site-container">
    <div class="section-label">AUDIT PROGRESS</div>
    <h2 class="section-heading">Your Audit Journey</h2>
    <p class="section-sub">Track every stage of the audit as we move through your business together.</p>

    <!-- Progress Bar -->
    <div class="progress-bar-wrap">
      <div class="progress-steps" id="progress-steps">
        <!-- Injected by JS -->
      </div>
    </div>

    <!-- Meeting Cards -->
    <div class="meetings-grid">{meeting_cards_html}
    </div>

  </div>
</section>

<!-- ── Process Map ── -->
<section class="page-section" id="section-process-map">
  <div class="site-container">
    <div class="section-label">HOW YOU WORK</div>
    <h2 class="section-heading">How You Work Today</h2>
    <p class="section-sub">A full map of how your business operates today &mdash; every step, every handoff, every tool.</p>
    <div id="process-map-cta">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- ── What We Found ── -->
<section class="page-section" id="section-findings">
  <div class="site-container">
    <div class="section-label">SESSION SUMMARY</div>
    <h2 class="section-heading">What We Discussed</h2>
    <div id="findings-content">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- ── Total Waste ── -->
<section class="page-section" id="section-waste">
  <div class="site-container">
    <div class="section-label">HIDDEN COSTS</div>
    <h2 class="section-heading">Hidden Costs Uncovered</h2>
    <div id="waste-content">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- ── Solutions Overview ── -->
<section class="page-section" id="section-solutions">
  <div class="site-container">
    <div class="section-label">OPPORTUNITIES</div>
    <h2 class="section-heading">Opportunities We Found</h2>
    <div id="solutions-content">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- ── Strategic Approaches ── -->
<section class="page-section" id="section-strategies">
  <div class="site-container">
    <div class="section-label">YOUR OPTIONS</div>
    <h2 class="section-heading">Ways to Get There</h2>
    <div id="strategies-content">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- Transformation and Priority Matrix sections removed — now embedded in Options & Pricing page -->
<!-- Prototype now rendered inside deliverables section via JS -->

<!-- ── Downloads ── -->
<section class="page-section" id="section-downloads">
  <div class="site-container">
    <div class="section-label">YOUR DELIVERABLES</div>
    <h2 class="section-heading">Downloads</h2>
    <div id="downloads-content">
      <!-- Injected by JS -->
    </div>
  </div>
</section>

<!-- ── Footer ── -->
<footer class="site-footer">
  <div class="site-container">
    {YOUR_COMPANY} &middot; {company} &middot; {generated}
  </div>
</footer>

<script>
// ── Progress Bar ──
(function() {{
  var steps = [
    {{ key: 'process_map', label: 'How You Work' }},
    {{ key: 'findings', label: 'What We Found' }},
    {{ key: 'waste', label: 'Hidden Costs' }},
    {{ key: 'solutions_overview', label: 'Opportunities' }},
    {{ key: 'strategic_approaches', label: 'Options & Pricing' }},
  ];
  var container = document.getElementById('progress-steps');
  // Find the furthest unlocked section index for progress display
  var currentIdx = -1;
  for (var i = steps.length - 1; i >= 0; i--) {{
    if (SECTIONS[steps[i].key]) {{ currentIdx = i; break; }}
  }}
  steps.forEach(function(step, i) {{
    var div = document.createElement('div');
    var cls = 'progress-step';
    if (i < currentIdx) cls += ' done';
    else if (i === currentIdx) cls += ' active';
    div.className = cls;
    div.innerHTML =
      '<div class="step-dot">' + (i < currentIdx ? '&#10003;' : (i + 1)) + '</div>' +
      '<div class="step-name">' + step.label + '</div>';
    container.appendChild(div);
  }});
}})();

// ── Process Map CTA ──
(function() {{
  var wrap = document.getElementById('process-map-cta');
  if (stageReached('process_map')) {{
    wrap.innerHTML =
      '<div class="pm-feature-card pm-feature-top">' +
        '<div class="pm-feature-inner">' +
          '<div class="pm-feature-text">' +
            '<div class="pm-ready-badge"><span class="pm-ready-dot"></span>Now available</div>' +
            '<div class="pm-feature-heading">Your Process Map<br>is ready to explore.</div>' +
            '<p class="pm-feature-sub">We\\'re mapping every step of your current operation across 8 business stages \\u2014 every handoff, every tool, every pain point. This is being built directly from what you told us.</p>' +
          '</div>' +
          '<div class="pm-feature-action">' +
            '<a href="process-map.html" target="_blank" class="btn-pm">Open Process Map <span class="btn-pm-arrow">&rarr;</span></a>' +
          '</div>' +
        '</div>' +
      '</div>';
  }} else {{
    wrap.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128274;</div>' +
        '<div class="lock-title">How You Work</div>' +
        '<div class="lock-label">Your process map is being prepared \\u2014 it will appear here once ready.</div>' +
      '</div>';
  }}
}})();

// ── Findings ──
(function() {{
  var el = document.getElementById('findings-content');
  if (!stageReached('findings')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128274;</div>' +
        '<div class="lock-title">What We Discussed</div>' +
        '<div class="lock-label">This section will unlock once the process map review is complete.</div>' +
        '<div class="lock-ghost">' +
          '<div style="height:12px;background:rgba(255,255,255,0.15);border-radius:6px;margin-bottom:10px;width:80%"></div>' +
          '<div style="height:12px;background:rgba(255,255,255,0.10);border-radius:6px;margin-bottom:10px;width:60%"></div>' +
          '<div style="height:12px;background:rgba(255,255,255,0.08);border-radius:6px;width:70%"></div>' +
        '</div>' +
      '</div>';
  }} else {{
    el.innerHTML =
      '<div class="pm-feature-card pm-feature-top">' +
        '<div class="pm-feature-inner">' +
          '<div class="pm-feature-text">' +
            '<div class="pm-ready-badge"><span class="pm-ready-dot"></span>Now available</div>' +
            '<div class="pm-feature-heading">What We Discussed</div>' +
            '<p class="pm-feature-sub">{findings_count} talking points from our conversations \\u2014 pain points you raised and optimisation ideas we explored together, each traced back to what you told us. This is not our proposed solution; that comes next.</p>' +
          '</div>' +
          '<div class="pm-feature-action">' +
            '<a href="findings.html" target="_blank" class="btn-pm">View What We Found <span class="btn-pm-arrow">&rarr;</span></a>' +
          '</div>' +
        '</div>' +
      '</div>';
  }}
}})();

// ── Waste ──
(function() {{
  var el = document.getElementById('waste-content');
  if (!stageReached('waste')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128274;</div>' +
        '<div class="lock-title">Hidden Costs</div>' +
        '<div class="lock-label">This section will unlock once findings have been reviewed with you.</div>' +
        '<div class="lock-ghost">' +
          '<div style="height:60px;background:rgba(125,255,0,0.12);border-radius:8px;margin-bottom:12px;width:40%;margin-left:auto;margin-right:auto"></div>' +
          '<div style="height:12px;background:rgba(255,255,255,0.08);border-radius:6px;margin-bottom:8px"></div>' +
          '<div style="height:12px;background:rgba(255,255,255,0.06);border-radius:6px;width:80%"></div>' +
        '</div>' +
      '</div>';
  }} else {{
    el.innerHTML =
      '<div class="pm-feature-card pm-feature-top">' +
        '<div class="pm-feature-inner">' +
          '<div class="pm-feature-text">' +
            '<div class="pm-ready-badge"><span class="pm-ready-dot"></span>Now available</div>' +
            '<div class="pm-feature-heading">Hidden Costs Uncovered</div>' +
            '<p class="pm-feature-sub">{fmt_aud(total_annual)} in annual operational waste identified across {len(waste_items)} areas \\u2014 every figure traces to something you or your team said directly during our sessions.</p>' +
          '</div>' +
          '<div class="pm-feature-action">' +
            '<a href="waste.html" target="_blank" class="btn-pm">View Hidden Costs <span class="btn-pm-arrow">&rarr;</span></a>' +
          '</div>' +
        '</div>' +
      '</div>';
  }}
}})();

// ── Solutions Overview ──
(function() {{
  var el = document.getElementById('solutions-content');
  if (!stageReached('solutions_overview')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128300;</div>' +
        '<div class="lock-title">Opportunities</div>' +
        '<div class="lock-label">This section will unlock once we\\'ve researched the best approaches for each opportunity.</div>' +
        '<div class="lock-ghost">' +
          '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px">' +
            '<div style="height:80px;background:rgba(125,255,0,0.08);border-radius:8px"></div>' +
            '<div style="height:80px;background:rgba(59,130,246,0.08);border-radius:8px"></div>' +
          '</div>' +
        '</div>' +
      '</div>';
  }} else {{
    el.innerHTML =
      '<div class="pm-feature-card pm-feature-top">' +
        '<div class="pm-feature-inner">' +
          '<div class="pm-feature-text">' +
            '<div class="pm-ready-badge"><span class="pm-ready-dot"></span>Now available</div>' +
            '<div class="pm-feature-heading">Opportunities</div>' +
            '<p class="pm-feature-sub">{len(proposed_changes)} opportunities researched with off-the-shelf SaaS tools and industry benchmarks \\u2014 so you can see all the ways to solve each problem before we prioritise.</p>' +
          '</div>' +
          '<div class="pm-feature-action">' +
            '<a href="solutions-overview.html" target="_blank" class="btn-pm">View Opportunities <span class="btn-pm-arrow">&rarr;</span></a>' +
          '</div>' +
        '</div>' +
      '</div>';
  }}
}})();

// ── Strategic Approaches ──
(function() {{
  var el = document.getElementById('strategies-content');
  if (!stageReached('strategic_approaches')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128161;</div>' +
        '<div class="lock-title">Your Options</div>' +
        '<div class="lock-label">This section will unlock once we\\'ve outlined different ways to implement your improvements.</div>' +
        '<div class="lock-ghost">' +
          '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px">' +
            '<div style="height:80px;background:rgba(125,255,0,0.08);border-radius:8px"></div>' +
            '<div style="height:80px;background:rgba(59,130,246,0.08);border-radius:8px"></div>' +
          '</div>' +
        '</div>' +
      '</div>';
  }} else {{
    el.innerHTML =
      '<div class="pm-feature-card pm-feature-top">' +
        '<div class="pm-feature-inner">' +
          '<div class="pm-feature-text">' +
            '<div class="pm-ready-badge"><span class="pm-ready-dot"></span>Now available</div>' +
            '<div class="pm-feature-heading">Your Options</div>' +
            '<p class="pm-feature-sub">Three ways to implement your improvements \\u2014 from quick automation wins to a fully unified platform.</p>' +
          '</div>' +
          '<div class="pm-feature-action">' +
            '<a href="strategic-approaches.html" target="_blank" class="btn-pm">View Your Options <span class="btn-pm-arrow">&rarr;</span></a>' +
          '</div>' +
        '</div>' +
      '</div>';
  }}
}})();

// ── Transformation Blueprint ──
(function() {{
  var el = document.getElementById('transformation-content');
  if (!el) return;
  if (!stageReached('transformation')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128274;</div>' +
        '<div class="lock-title">The Roadmap</div>' +
        '<div class="lock-label">Coming next \\u2014 your step-by-step plan is being prepared.</div>' +
        '<div class="lock-ghost">' +
          '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px">' +
            '<div style="height:100px;background:rgba(239,68,68,0.1);border-radius:8px"></div>' +
            '<div style="height:100px;background:rgba(125,255,0,0.08);border-radius:8px"></div>' +
          '</div>' +
        '</div>' +
      '</div>';
  }} else {{
    el.innerHTML =
      '<p class="section-sub">Side-by-side view of how you work today vs how things could look after implementing the recommended changes.</p>' +
      '{blueprint_content_js}' +
      '<div style="text-align:center;margin-top:24px">' +
        '<a href="transformation-blueprint.html" target="_blank" class="btn-pm" style="display:inline-flex;align-items:center;gap:8px">View The Roadmap <span class="btn-pm-arrow">&rarr;</span></a>' +
      '</div>';
  }}
}})();

// ── Priority Matrix ──
(function() {{
  var el = document.getElementById('priority-content');
  if (!el) return;
  if (!stageReached('priority_matrix')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128274;</div>' +
        '<div class="lock-title">What to Do First</div>' +
        '<div class="lock-label">This section will unlock once we\\'ve mapped out all your opportunities.</div>' +
        '<div class="lock-ghost">' +
          '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:16px">' +
            '<div style="height:80px;background:rgba(255,255,255,0.08);border-radius:8px"></div>' +
            '<div style="height:80px;background:rgba(255,255,255,0.06);border-radius:8px"></div>' +
            '<div style="height:80px;background:rgba(255,255,255,0.04);border-radius:8px"></div>' +
          '</div>' +
        '</div>' +
      '</div>';
  }} else {{
    el.innerHTML =
      '<p class="section-sub">Each initiative plotted by business impact and ease of implementation. Click a bubble to see details.</p>' +
      '{pm_quadrant_js}';
  }}
}})();

// ── Prototype now rendered inside Downloads section ──

// ── Downloads ──
(function() {{
  var el = document.getElementById('downloads-content');
  if (!stageReached('transformation')) {{
    el.innerHTML =
      '<div class="lock-card">' +
        '<div class="lock-icon">&#128274;</div>' +
        '<div class="lock-title">Downloads</div>' +
        '<div class="lock-label">Your deliverables will be available here once the audit is complete.</div>' +
        '<div class="lock-ghost">' +
          '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:16px">' +
            '<div style="height:80px;background:rgba(255,255,255,0.08);border-radius:8px"></div>' +
            '<div style="height:80px;background:rgba(255,255,255,0.06);border-radius:8px"></div>' +
            '<div style="height:80px;background:rgba(255,255,255,0.04);border-radius:8px"></div>' +
          '</div>' +
        '</div>' +
      '</div>';
  }} else {{
    var items = {downloads_json};
    var cards = '';
    items.forEach(function(d) {{
      var btnClass = d.pdf ? 'btn-download btn-download-pdf' : 'btn-download';
      var btnLabel = d.pdf ? 'Save as PDF \\u2192' : 'Open \\u2192';
      var btnHtml = d.demo
        ? '<button onclick="openModal(\\x27demo-pdf\\x27)" class="' + btnClass + '" style="cursor:pointer">' + btnLabel + '</button>'
        : '<a href="' + d.file + '" target="_blank" class="' + btnClass + '">' + btnLabel + '</a>';
      cards +=
        '<div class="download-card">' +
          '<div class="download-icon">' + d.icon + '</div>' +
          '<h3>' + d.label + '</h3>' +
          '<p>' + d.desc + '</p>' +
          btnHtml +
        '</div>';
    }});
    var protoCta = '';
    if (stageReached('prototype')) {{
      var pUrl = SECTIONS.prototype_url || '';
      if (pUrl) {{
        protoCta =
          '<div class="prototype-cta">' +
            '<div class="prototype-cta-text">' +
              '<div class="prototype-cta-badge"><span class="dot"></span>Interactive Prototype</div>' +
              '<h3>See your future platform in action</h3>' +
              '<p>A clickable prototype built from everything we discussed \\u2014 real screens, real workflows, real data. Explore it before a single line of production code is written.</p>' +
            '</div>' +
            '<a href="' + pUrl + '" target="_blank" class="btn-prototype">Open Prototype <span class="arrow">&rarr;</span></a>' +
          '</div>';
      }}
    }}
    el.innerHTML =
      '<p class="section-sub">All audit materials are available below. Open any deliverable or save the full report as a PDF.</p>' +
      '<div class="downloads-grid">' + cards + '</div>' +
      protoCta;
  }}
}})();

// ── Modal functions ──
function openModal(id) {{
  var el = document.getElementById('modal-' + id);
  if (el) {{ el.style.display = 'flex'; document.body.style.overflow = 'hidden'; }}
}}
function closeModal() {{
  document.querySelectorAll('.pm-modal-backdrop').forEach(function(m) {{ m.style.display = 'none'; }});
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeModal(); }});

// ── Chart tooltip ──
var chartTipData = null;
function _loadChartData() {{
  if (chartTipData) return;
  try {{ chartTipData = JSON.parse(document.getElementById('chart-tip-data')?.textContent || '[]'); }} catch(e) {{ chartTipData = []; }}
}}
function showChartDot(el, idx) {{
  _loadChartData();
  var tip = document.getElementById('chart-tip');
  if (!tip || !chartTipData[idx]) return;
  var d = chartTipData[idx];
  var lines = d.items.map(function(l) {{ return '<div style="font-size:11px;margin-top:3px">&#8226; ' + l + '</div>'; }}).join('');
  if (!d.items.length) lines = '<div style="font-size:11px;margin-top:3px;color:#9CA3AF">No new items this month</div>';
  tip.innerHTML = '<div style="font-weight:700;margin-bottom:4px">' + d.month + ' &mdash; ' + d.cumulative + '</div>' + lines;
  tip.style.display = 'block';
  var r = el.getBoundingClientRect();
  var container = tip.parentElement;
  var cr = container.getBoundingClientRect();
  tip.style.left = (r.left - cr.left + r.width/2) + 'px';
  tip.style.top = (r.top - cr.top - 8) + 'px';
  tip.style.transform = 'translate(-50%, -100%)';
}}
function hideChartTip() {{
  var tip = document.getElementById('chart-tip');
  if (tip) tip.style.display = 'none';
}}

// ── Quadrant matrix interaction ──
var qmHovered = null, qmSelected = null;
function qmUpdate() {{
  var active = qmHovered !== null ? qmHovered : qmSelected;
  document.querySelectorAll('.qm-bubble').forEach(function(b) {{
    var idx = parseInt(b.dataset.idx);
    b.classList.toggle('qm-active', idx === active);
    b.classList.toggle('qm-dimmed', active !== null && idx !== active);
    if (idx === active) {{
      b.style.boxShadow = '0 0 20px ' + b.style.borderColor + '80';
      b.style.background = b.style.borderColor + '40';
    }} else {{
      b.style.boxShadow = 'none';
      b.style.background = b.style.borderColor.replace(')', ',0.12)').replace('rgb', 'rgba');
    }}
  }});
  document.querySelectorAll('.qm-legend-btn').forEach(function(b) {{
    var idx = parseInt(b.dataset.idx);
    b.classList.toggle('qm-legend-active', idx === active);
  }});
}}
function qmHover(idx) {{ qmHovered = idx; qmUpdate(); }}
function qmSelect(idx) {{ qmSelected = (qmSelected === idx) ? null : idx; qmUpdate(); }}
function qmClick(idx) {{
  qmSelected = idx; qmUpdate();
  var b = document.querySelector('.qm-bubble[data-idx="' + idx + '"]');
  if (b && b.dataset.cid) openModal(b.dataset.cid);
}}
</script>

<!-- Chart tooltip data -->
<script type="application/json" id="chart-tip-data">{chart_tip_json}</script>

<!-- Priority matrix modals -->
{pm_modals_html}

{demo_pdf_modal_html}

</body>
</html>"""



# ─── Print-Optimized Audit Report ─────────────────────────────────────────────




def generate_audit_report_print(ssad: dict) -> str:
    """Generate a print-optimised HTML page that auto-triggers the browser print
    dialog.  Designed to produce a professional PDF via Chrome's Save-as-PDF."""

    company = escape(ssad.get("company_name", "Client"))
    industry = escape(ssad.get("industry_tag", ""))
    generated = datetime.now().strftime("%d %b %Y")
    audit_start = ssad.get("audit_start_date", "")
    if audit_start:
        try:
            dt = datetime.strptime(audit_start, "%Y-%m-%d")
            audit_start_display = dt.strftime("%d %b %Y")
        except ValueError:
            audit_start_display = audit_start
    else:
        audit_start_display = "N/A"

    contact = ssad.get("contact", {})
    contact_name = escape(contact.get("name", ""))
    contact_role = escape(contact.get("role", ""))
    company_size = escape(contact.get("company_size", ""))

    sessions = [s for s in ssad.get("sessions", []) if s.get("session_type") not in ("document", "email")]
    session_count = len(sessions)
    stages_covered = ssad.get("business_stages_covered", [])

    # ── Pain points & optimisations ──
    pain_points = ssad.get("pain_points", [])
    optimisations = ssad.get("optimisations", [])
    opp_count = len(optimisations) if optimisations else sum(
        1 for p in ssad.get("processes", []) for s in p.get("steps", []) if s.get("type") == "optimisation"
    )

    # ── Waste ──
    waste_items = ssad.get("waste_items", [])
    seen_wids = set()
    deduped_waste = []
    for w in waste_items:
        wid = w.get("waste_id", id(w))
        if wid in seen_wids:
            continue
        seen_wids.add(wid)
        deduped_waste.append(w)
    qualified_waste = [w for w in deduped_waste if w.get("confidence") in ("HIGH", "MEDIUM")]
    total_annual = sum(w.get("annual_waste_aud") or 0 for w in qualified_waste)
    total_monthly = sum(w.get("monthly_waste_aud") or 0 for w in qualified_waste)

    # ── Proposed changes ──
    proposed_changes = ssad.get("proposed_changes", [])
    total_annual_value = sum((c.get("value") or {}).get("combined_annual_value_aud", 0) for c in proposed_changes)

    # ── Transformation blueprint ──
    blueprint = ssad.get("transformation_blueprint", {})
    bp_phases = blueprint.get("phases", [])

    # ── Tools ──
    tools = ssad.get("tools", [])

    # ── Build sections ──

    # --- Findings by stage ---
    pain_by_stage = {}
    for pp in pain_points:
        stage = pp.get("stage", "other")
        pain_by_stage.setdefault(stage, []).append(pp)
    opt_by_stage = {}
    for opt in optimisations:
        stage = opt.get("stage", "other")
        opt_by_stage.setdefault(stage, []).append(opt)

    all_stages = []
    for s in _print_stage_order:
        if s in pain_by_stage or s in opt_by_stage:
            all_stages.append(s)
    for s in list(pain_by_stage.keys()) + list(opt_by_stage.keys()):
        if s not in all_stages:
            all_stages.append(s)

    findings_html = ""
    for stage in all_stages:
        label = _print_stage_labels.get(stage, stage.replace("_", " ").title())
        pains = pain_by_stage.get(stage, [])
        opts = opt_by_stage.get(stage, [])
        findings_html += f'<h3 style="color:{BRAND_DARK};font-size:14px;font-weight:700;margin:20px 0 8px 0;padding-bottom:4px;border-bottom:2px solid {BRAND_PRIMARY}">{label}</h3>\n'
        for pp in pains:
            desc = escape(pp.get("description", ""))
            quote = pp.get("quote", "")
            findings_html += f'<div style="margin-bottom:10px"><span style="background:#FEE2E2;color:#991B1B;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:600;margin-right:6px">PAIN</span> {desc}</div>\n'
            if quote:
                findings_html += f'<blockquote style="margin:0 0 10px 16px;padding-left:10px;border-left:3px solid #E5E7EB;color:{BRAND_GREY};font-size:12px;font-style:italic">&ldquo;{escape(quote)}&rdquo;</blockquote>\n'
        for opt in opts:
            desc = escape(opt.get("description", ""))
            findings_html += f'<div style="margin-bottom:10px"><span style="background:#D1FAE5;color:#065F46;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:600;margin-right:6px">OPPORTUNITY</span> {desc}</div>\n'

    # --- Waste table ---
    waste_rows = ""
    for w in qualified_waste:
        desc = escape(w.get("description", ""))
        annual = fmt_aud(w.get("annual_waste_aud"))
        monthly = fmt_aud(w.get("monthly_waste_aud"))
        conf = w.get("confidence", "")
        waste_rows += f"<tr><td>{desc}</td><td style='text-align:right;white-space:nowrap;font-weight:600'>{annual}</td><td style='text-align:right;white-space:nowrap'>{monthly}</td><td style='text-align:center'>{conf}</td></tr>\n"

    # --- Proposed changes table ---
    changes_rows = ""
    for c in proposed_changes:
        title = escape(c.get("title", ""))
        ctype = escape(c.get("change_type", "")).title()
        value = fmt_aud((c.get("value") or {}).get("combined_annual_value_aud"))
        weeks = escape((c.get("implementation") or {}).get("weeks_label", ""))
        changes_rows += f"<tr><td>{title}</td><td style='text-align:center'>{ctype}</td><td style='text-align:right;white-space:nowrap;font-weight:600'>{value}</td><td style='text-align:center;white-space:nowrap'>{weeks}</td></tr>\n"

    # --- Blueprint phases ---
    phases_html = ""
    changes_by_id = {c.get("change_id"): c for c in proposed_changes}
    for phase in bp_phases:
        pnum = phase.get("phase_number", "")
        plabel = escape(phase.get("label", f"Phase {pnum}"))
        timeframe = escape(phase.get("timeframe", ""))
        change_ids = phase.get("change_ids", [])
        phase_changes = [changes_by_id[cid] for cid in change_ids if cid in changes_by_id]
        phases_html += f'<div style="margin-bottom:16px;padding:14px 16px;background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;page-break-inside:avoid">'
        phases_html += f'<div style="font-size:13px;font-weight:700;color:{BRAND_DARK};margin-bottom:2px">Phase {pnum}: {plabel}</div>'
        phases_html += f'<div style="font-size:11px;color:{BRAND_GREY};margin-bottom:8px">{timeframe}</div>'
        for pc in phase_changes:
            ptitle = escape(pc.get("title", ""))
            pvalue = fmt_aud((pc.get("value") or {}).get("combined_annual_value_aud"))
            phases_html += f'<div style="font-size:12px;color:{BRAND_DARK};margin-bottom:3px">&bull; {ptitle} <span style="color:{BRAND_GREY}">({pvalue}/yr)</span></div>'
        phases_html += '</div>\n'

    # --- Tools table ---
    tools_rows = ""
    for t in tools:
        tname = escape(t.get("tool_name", ""))
        tuse = escape(t.get("use_case", ""))
        tcost = t.get("monthly_cost_aud")
        tcost_str = fmt_aud(tcost) + "/mo" if tcost else "Free"
        tools_rows += f"<tr><td style='font-weight:600'>{tname}</td><td>{tuse}</td><td style='text-align:right;white-space:nowrap'>{tcost_str}</td></tr>\n"

    # --- Stage summary for exec summary ---
    stages_display = ", ".join(
        _print_stage_labels.get(s, s.replace("_", " ").title()) for s in stages_covered
    ) or "Multiple stages"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Audit Report &mdash; {company}</title>
{BRAND_FAVICON}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: {BRAND_DARK};
    line-height: 1.6;
    font-size: 13px;
    background: #fff;
  }}

  /* ── Print controls ── */
  .print-bar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    background: {BRAND_DARK};
    color: #fff;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 1000;
    font-size: 13px;
  }}
  .print-bar button {{
    background: {BRAND_PRIMARY};
    color: #166534;
    border: none;
    padding: 8px 20px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 13px;
    cursor: pointer;
  }}
  .print-bar button:hover {{ opacity: 0.85; }}

  /* ── Page layout ── */
  .report {{ max-width: 800px; margin: 0 auto; padding: 80px 40px 40px 40px; }}

  /* ── Cover page ── */
  .cover {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 90vh;
    text-align: center;
    page-break-after: always;
  }}
  .cover-logo {{ width: 80px; height: 80px; border-radius: 16px; margin-bottom: 40px; }}
  .cover h1 {{ font-size: 28px; font-weight: 900; color: {BRAND_DARK}; margin-bottom: 8px; }}
  .cover .cover-company {{ font-size: 22px; font-weight: 700; color: {BRAND_DARK}; margin-bottom: 4px; }}
  .cover .cover-industry {{ font-size: 14px; color: {BRAND_GREY}; margin-bottom: 32px; }}
  .cover .cover-meta {{ font-size: 12px; color: {BRAND_GREY}; line-height: 1.8; }}
  .cover .cover-divider {{ width: 60px; height: 3px; background: {BRAND_PRIMARY}; margin: 24px auto; border-radius: 2px; }}

  /* ── Section headings ── */
  .section-break {{ page-break-before: always; }}
  .report h2 {{
    font-size: 18px;
    font-weight: 800;
    color: {BRAND_DARK};
    margin: 32px 0 16px 0;
    padding-bottom: 6px;
    border-bottom: 3px solid {BRAND_PRIMARY};
  }}

  /* ── Stat cards ── */
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
  }}
  .stat-card {{
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
  }}
  .stat-card .stat-value {{ font-size: 22px; font-weight: 800; color: {BRAND_DARK}; }}
  .stat-card .stat-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em; color: {BRAND_GREY}; margin-top: 2px; }}

  /* ── Tables ── */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 12px;
  }}
  thead th {{
    background: {BRAND_DARK};
    color: #fff;
    padding: 8px 10px;
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  tbody td {{
    padding: 8px 10px;
    border-bottom: 1px solid #E5E7EB;
    vertical-align: top;
  }}
  tbody tr:nth-child(even) {{ background: #F9FAFB; }}

  /* ── Footer on each page ── */
  .page-footer {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    text-align: center;
    font-size: 9px;
    color: {BRAND_GREY};
    padding: 8px;
  }}

  /* ── Print styles ── */
  @media print {{
    .print-bar {{ display: none !important; }}
    .report {{ padding: 0; max-width: none; }}
    body {{ font-size: 11px; }}
    @page {{
      size: A4;
      margin: 20mm 18mm 25mm 18mm;
      @bottom-center {{
        content: "Confidential — Prepared for {company} by {COMPANY_NAME}";
        font-size: 8px;
        color: {BRAND_GREY};
      }}
    }}
    .cover {{ min-height: auto; padding: 120px 0; }}
    h2 {{ font-size: 16px; }}
    .stat-card .stat-value {{ font-size: 18px; }}
    table {{ font-size: 10px; }}
    thead th {{ font-size: 9px; }}
    .page-footer {{ display: none; }}
  }}
</style>
</head>
<body>

<!-- Print control bar (hidden when printing) -->
<div class="print-bar">
  <span>Audit Report &mdash; {company}</span>
  <button onclick="window.print()">Save as PDF</button>
</div>

<div class="report">

  <!-- ── Cover Page ── -->
  <div class="cover">
    <img src="{COMPANY_LOGO_URL}" alt="{COMPANY_NAME}" class="cover-logo">
    <h1>Business Operations<br>Audit Report</h1>
    <div class="cover-divider"></div>
    <div class="cover-company">{company}</div>
    <div class="cover-industry">{industry}</div>
    <div class="cover-meta">
      {"Prepared for " + contact_name + (" &mdash; " + contact_role if contact_role else "") + "<br>" if contact_name else ""}
      Audit commenced {audit_start_display}<br>
      Report generated {generated}<br><br>
      Prepared by {COMPANY_NAME}<br>
      {COMPANY_ADDRESS}<br>
      {COMPANY_EMAIL} &middot; {COMPANY_WEBSITE}
    </div>
  </div>

  <!-- ── Executive Summary ── -->
  <div class="section-break">
    <h2>Executive Summary</h2>
    <p style="margin-bottom:16px">
      {YOUR_COMPANY} conducted a comprehensive operational audit of {company}{" (" + company_size + ")" if company_size else ""}
      across {len(stages_covered)} business stage{"s" if len(stages_covered) != 1 else ""}: {stages_display}.
      Over {session_count} session{"s" if session_count != 1 else ""}, we identified
      {len(pain_points)} pain point{"s" if len(pain_points) != 1 else ""} and
      {opp_count} optimisation opportunit{"ies" if opp_count != 1 else "y"}.
    </p>
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-value">{session_count}</div>
        <div class="stat-label">Sessions</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{len(pain_points)}</div>
        <div class="stat-label">Pain Points</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{opp_count}</div>
        <div class="stat-label">Opportunities</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{fmt_aud(total_annual)}</div>
        <div class="stat-label">Annual Waste</div>
      </div>
      {"<div class='stat-card'><div class='stat-value'>" + fmt_aud(total_annual_value) + "</div><div class='stat-label'>Annual Value of Changes</div></div>" if total_annual_value else ""}
      {"<div class='stat-card'><div class='stat-value'>" + str(len(proposed_changes)) + "</div><div class='stat-label'>Proposed Changes</div></div>" if proposed_changes else ""}
    </div>
  </div>

  <!-- ── Findings ── -->
  {('<div class="section-break"><h2>Findings</h2><p style="margin-bottom:12px">Issues and opportunities identified during audit sessions, grouped by business stage.</p>' + findings_html + '</div>') if findings_html else ''}

  <!-- ── Waste Analysis ── -->
  {('<div class="section-break"><h2>Waste Analysis</h2><p style="margin-bottom:12px">Operational waste totalling <strong>' + fmt_aud(total_annual) + '/year</strong> (' + fmt_aud(total_monthly) + '/month) identified across ' + str(len(qualified_waste)) + ' areas.</p><table><thead><tr><th>Activity</th><th style="text-align:right">Annual</th><th style="text-align:right">Monthly</th><th style="text-align:center">Confidence</th></tr></thead><tbody>' + waste_rows + '</tbody></table></div>') if waste_rows else ''}

  <!-- ── Proposed Changes ── -->
  {('<div class="section-break"><h2>Proposed Changes</h2><p style="margin-bottom:12px">Recommended automation and process changes with estimated value and implementation timeline.</p><table><thead><tr><th>Change</th><th style="text-align:center">Type</th><th style="text-align:right">Annual Value</th><th style="text-align:center">Timeline</th></tr></thead><tbody>' + changes_rows + '</tbody></table></div>') if changes_rows else ''}

  <!-- ── Transformation Roadmap ── -->
  {('<div class="section-break"><h2>Transformation Roadmap</h2><p style="margin-bottom:12px">Phased implementation plan for recommended changes.</p>' + phases_html + '</div>') if phases_html else ''}

  <!-- ── Tools Inventory ── -->
  {('<div class="section-break"><h2>Current Tools</h2><p style="margin-bottom:12px">Software and systems currently in use across the business.</p><table><thead><tr><th>Tool</th><th>Use Case</th><th style="text-align:right">Cost</th></tr></thead><tbody>' + tools_rows + '</tbody></table></div>') if tools_rows else ''}

  <!-- ── End ── -->
  <div style="text-align:center;margin-top:40px;padding-top:20px;border-top:2px solid {BRAND_PRIMARY}">
    <img src="{COMPANY_LOGO_URL}" alt="{COMPANY_NAME}" style="width:36px;height:36px;border-radius:8px;margin-bottom:8px">
    <div style="font-size:11px;color:{BRAND_GREY}">{COMPANY_NAME} &middot; {COMPANY_ADDRESS}</div>
    <div style="font-size:11px;color:{BRAND_GREY}">{COMPANY_EMAIL} &middot; {COMPANY_WEBSITE}</div>
  </div>

</div>

<script>
  window.addEventListener('load', function() {{
    setTimeout(function() {{ window.print(); }}, 400);
  }});
</script>

</body>
</html>"""


# ─── Findings & Waste Partial Generators ──────────────────────────────────────



_WASTE_TYPE_LABELS = {
    "manual_data_entry":  "Manual Data Entry",
    "duplicate_work":     "Duplicate Work",
    "no_followup":        "No Follow-up",
    "communication_gap":  "Communication Gap",
    "missing_automation": "Missing Automation",
}


def _findings_stage_label(stage: str, labels: dict = None) -> str:
    if labels:
        return labels.get(stage, stage.replace("_", " ").title())
    return stage.replace("_", " ").title()


def _waste_type_label(wt: str) -> str:
    return _WASTE_TYPE_LABELS.get(wt, wt.replace("_", " ").title())


def _waste_basis_note(blended_rate, confidence: str) -> str:
    """Build the calculation basis explanation shown in the waste hero."""
    rate_str = f"${blended_rate}/hr"
    if confidence == "HIGH":
        qualifier = "This rate was derived from salary data discussed during our sessions."
    elif confidence == "MEDIUM":
        qualifier = "This rate is an estimate based on information shared during our sessions and will be validated during your review call."
    else:
        qualifier = "This rate is a conservative estimate and will be validated during your review call."
    return (
        f"Calculated using a blended average hourly rate of <strong>{rate_str}</strong> "
        f"across affected roles &times; wasted hours &times; 52 weeks. {qualifier}"
    )


_PARTIAL_FONT = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'


def generate_findings_partial(ssad: dict) -> str:
    pain_items = [
        {**pp, "item_type": "pain", "item_id": pp.get("pain_point_id", "")}
        for pp in ssad.get("pain_points", [])
    ]
    opp_items = [
        {**op, "item_type": "optimisation", "item_id": op.get("optimisation_id", "")}
        for op in ssad.get("optimisations", [])
    ]
    # Fallback: extract optimisation steps from processes if optimisations[] is empty
    # (backwards compat for SDADs built before optimisations[] was populated)
    if not opp_items:
        for proc in ssad.get("processes", []):
            stage = proc.get("stage", "")
            for step in proc.get("steps", []):
                if step.get("type") == "optimisation":
                    opp_items.append({
                        "item_type": "optimisation",
                        "item_id": step.get("step_id", ""),
                        "stage": stage,
                        "description": step.get("description", ""),
                        "quote": step.get("source_quote", ""),
                        "speaker": step.get("source_speaker", ""),
                        "source_session": step.get("source_session"),
                        "source_timestamp_seconds": step.get("source_timestamp_seconds"),
                        "confidence": step.get("confidence", "MEDIUM"),
                    })
    all_items = pain_items + opp_items
    if not all_items:
        return "<html><body><p>No pain_points or optimisations found in audit data.</p></body></html>"

    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")

    _findings_labels, _ = _build_stage_lookups(ssad)
    _findings_order = [p["stage"] for p in ssad.get("processes", [])]
    session_map = {s.get("session_number"): s for s in ssad.get("sessions", [])}

    groups: dict = {}
    for item in all_items:
        s = item.get("stage", "unknown")
        groups.setdefault(s, []).append(item)
    ordered_stages = [s for s in _findings_order if s in groups]
    for s in groups:
        if s not in ordered_stages:
            ordered_stages.append(s)

    modal_data = []
    for item in all_items:
        sess = session_map.get(item.get("source_session"))
        rec_href = None
        if sess and sess.get("fathom_url") and item.get("source_timestamp_seconds") is not None:
            rec_href = f"{sess['fathom_url']}?t={item['source_timestamp_seconds']}"
        modal_data.append({
            "id":          item.get("item_id", ""),
            "itemType":    item.get("item_type", "pain"),
            "stage":       item.get("stage", ""),
            "stageLabel":  _findings_stage_label(item.get("stage", ""), _findings_labels),
            "description": item.get("description", ""),
            "quote":       item.get("quote", ""),
            "speaker":     item.get("speaker", ""),
            "session":     item.get("source_session"),
            "confidence":  item.get("confidence", "LOW"),
            "recHref":     rec_href,
        })

    pills = [f'<button class="pill active" data-stage="all">All ({len(all_items)})</button>']
    for stage in ordered_stages:
        lbl = _findings_stage_label(stage, _findings_labels)
        n = len(groups[stage])
        pills.append(f'<button class="pill" data-stage="{escape(stage)}">{escape(lbl)} ({n})</button>')
    pills_html = "".join(pills)

    conf_colors = {"HIGH": ("#d1fae5", "#166534", "#6ee7b7"), "MEDIUM": ("#fef3c7", "#92400e", "#fcd34d"), "LOW": ("#f1f5f9", "#475569", "#cbd5e1")}
    type_eyebrow = {
        "pain":        ("PAIN POINT",  "#fef2f2", "#b91c1c"),
        "optimisation": ("OPTIMISATION", "#f0fdf4", "#15803d"),
    }
    groups_html = ""
    for stage in ordered_stages:
        lbl = _findings_stage_label(stage, _findings_labels)
        items_in = groups[stage]
        cards_html = ""
        for item in items_in:
            pid = escape(item.get("item_id", ""))
            desc = item.get("description", "")
            desc_short = escape(desc[:115] + ("…" if len(desc) > 115 else ""))
            conf = item.get("confidence", "LOW")
            bg, fg, bd = conf_colors.get(conf, ("#f1f5f9", "#475569", "#cbd5e1"))
            session_num = item.get("source_session", "")
            session_tag = f'<span class="session-tag">Session {session_num}</span>' if session_num else ""
            etype = item.get("item_type", "pain")
            eyebrow_label, eyebrow_bg, eyebrow_fg = type_eyebrow.get(etype, type_eyebrow["pain"])
            cards_html += f"""
            <div class="finding-card" data-id="{pid}" role="button" tabindex="0" aria-haspopup="dialog">
              <div class="card-eyebrow" style="background:{eyebrow_bg};color:{eyebrow_fg}">{eyebrow_label}</div>
              <div class="card-top">
                <span class="card-id">{pid}</span>
                <span class="conf-pill" style="background:{bg};color:{fg};border:1px solid {bd}">{conf}</span>
              </div>
              <div class="card-desc">{desc_short}</div>
              <div class="card-foot">
                <span class="stage-tag">{escape(lbl)}</span>
                {session_tag}
              </div>
            </div>"""
        groups_html += f"""
        <div class="stage-group" data-stage="{escape(stage)}">
          <h3 class="stage-heading">{escape(lbl)}<span class="stage-count">{len(items_in)}</span></h3>
          <div class="card-grid">{cards_html}
          </div>
        </div>"""

    items_json = json.dumps(modal_data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — What We Discussed</title>
{BRAND_FAVICON}
{_PARTIAL_FONT}
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg: #f7f9fc; --fg: #0f1825; --card: #ffffff;
  --border: #e2e8f0; --lime: #7DFF00; --lime-fg: #166534;
  --muted: #64748b; --radius: 10px;
}}
body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--fg); font-size: 15px; line-height: 1.5; }}
.findings-root {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px 80px; }}
.findings-header {{ margin-bottom: 32px; }}
.findings-eyebrow {{ font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--lime-fg); background: #dcfce7; display: inline-block; padding: 3px 10px; border-radius: 4px; margin-bottom: 10px; }}
.findings-title {{ font-size: 32px; font-weight: 800; line-height: 1.2; margin-bottom: 8px; }}
.findings-sub {{ font-size: 15px; color: var(--muted); }}
.stage-filters {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 36px; }}
.pill {{ background: var(--card); border: 1px solid var(--border); border-radius: 999px; padding: 6px 16px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all .15s; color: var(--muted); font-family: inherit; }}
.pill:hover {{ border-color: var(--lime); color: var(--fg); }}
.pill.active {{ background: var(--lime); border-color: var(--lime); color: var(--lime-fg); font-weight: 700; }}
.stage-group {{ margin-bottom: 48px; }}
.stage-group[hidden] {{ display: none; }}
.stage-heading {{ font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }}
.stage-count {{ background: var(--border); color: var(--fg); font-size: 11px; padding: 1px 7px; border-radius: 999px; font-weight: 700; }}
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }}
.finding-card {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px; cursor: pointer; transition: transform .15s, box-shadow .15s, border-color .15s; display: flex; flex-direction: column; gap: 10px; }}
.finding-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.08); border-color: #bfdbfe; }}
.finding-card:focus-visible {{ outline: 2px solid var(--lime); outline-offset: 2px; }}
.card-eyebrow {{ font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; align-self: flex-start; }}
.card-top {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; }}
.card-id {{ font-size: 11px; font-weight: 700; color: var(--muted); font-family: monospace; }}
.conf-pill {{ font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: .05em; }}
.card-desc {{ font-size: 13px; line-height: 1.55; color: var(--fg); flex: 1; }}
.card-foot {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; }}
.stage-tag {{ font-size: 11px; font-weight: 600; color: var(--muted); background: var(--bg); border: 1px solid var(--border); padding: 2px 8px; border-radius: 4px; }}
.session-tag {{ font-size: 11px; color: var(--muted); }}
.modal-overlay {{ display: none; position: fixed; inset: 0; background: rgba(15,24,37,.55); backdrop-filter: blur(4px); z-index: 1000; align-items: center; justify-content: center; padding: 20px; }}
.modal-overlay.open {{ display: flex; }}
.modal-body {{ background: var(--card); border-radius: 16px; max-width: 640px; width: 100%; max-height: 90vh; overflow-y: auto; padding: 36px; position: relative; box-shadow: 0 24px 60px rgba(0,0,0,.2); }}
.modal-top {{ display: flex; align-items: flex-start; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }}
.modal-id {{ font-size: 12px; font-weight: 700; color: var(--muted); font-family: monospace; background: var(--bg); padding: 3px 8px; border-radius: 4px; }}
.modal-stage {{ font-size: 12px; font-weight: 600; color: var(--muted); background: var(--bg); padding: 3px 10px; border-radius: 4px; border: 1px solid var(--border); }}
.modal-conf {{ font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 4px; }}
.modal-type {{ font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: 3px 10px; border-radius: 4px; }}
.modal-desc {{ font-size: 16px; line-height: 1.6; color: var(--fg); margin-bottom: 20px; }}
.modal-quote {{ border-left: 3px solid var(--lime); padding: 12px 18px; background: #f0fdf4; border-radius: 0 8px 8px 0; font-style: italic; font-size: 14px; color: #374151; margin-bottom: 16px; line-height: 1.6; }}
.modal-quote cite {{ display: block; margin-top: 8px; font-style: normal; font-size: 12px; color: var(--muted); font-weight: 600; }}
.modal-meta {{ font-size: 13px; color: var(--muted); margin-bottom: 24px; }}
.btn-recording {{ display: inline-flex; align-items: center; gap: 8px; background: var(--lime); color: var(--lime-fg); font-weight: 700; font-size: 13px; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-bottom: 12px; transition: opacity .15s; }}
.btn-recording:hover {{ opacity: .85; }}
.btn-close {{ display: block; width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; background: transparent; color: var(--muted); font-size: 13px; font-family: inherit; cursor: pointer; transition: background .15s; }}
.btn-close:hover {{ background: var(--bg); }}
.modal-close-x {{ position: absolute; top: 16px; right: 16px; background: none; border: none; font-size: 20px; color: var(--muted); cursor: pointer; padding: 4px 8px; border-radius: 4px; }}
.modal-close-x:hover {{ background: var(--bg); }}
.type-toggle {{ display: flex; align-items: stretch; gap: 0; margin-bottom: 28px; border-radius: 12px; overflow: hidden; border: 2px solid var(--border); width: fit-content; }}
.type-btn {{ background: var(--card); border: none; padding: 14px 28px; font-size: 15px; font-weight: 700; cursor: pointer; transition: all .2s; color: var(--muted); font-family: inherit; white-space: nowrap; position: relative; letter-spacing: -0.01em; }}
.type-btn:not(:last-child) {{ border-right: 2px solid var(--border); }}
.type-btn:hover {{ color: var(--fg); background: #f1f5f9; }}
.type-btn .type-count {{ display: inline-block; font-size: 12px; font-weight: 800; padding: 1px 7px; border-radius: 999px; margin-left: 6px; background: var(--border); color: var(--muted); }}
.type-btn.active-all {{ background: var(--fg); color: #fff; }}
.type-btn.active-all .type-count {{ background: rgba(255,255,255,0.2); color: #fff; }}
.type-btn.active-pain {{ background: #dc2626; color: #fff; }}
.type-btn.active-pain .type-count {{ background: rgba(255,255,255,0.25); color: #fff; }}
.type-btn.active-opt {{ background: #16a34a; color: #fff; }}
.type-btn.active-opt .type-count {{ background: rgba(255,255,255,0.25); color: #fff; }}
.finding-card.type-hidden {{ display: none; }}
@media (max-width: 600px) {{
  .findings-root {{ padding: 24px 16px 60px; }}
  .card-grid {{ grid-template-columns: 1fr; }}
  .modal-body {{ padding: 24px; }}
}}
</style>
</head>
<body>
<div class="findings-root">
  <div class="findings-header">
    <div class="findings-eyebrow">Session Summary</div>
    <h1 class="findings-title">What We Discussed</h1>
    <p class="findings-sub">Everything below comes directly from our conversations &mdash; these are the pain points you raised and the optimisation ideas we explored together. This is not our proposed solution; that comes next.</p>
  </div>

  <div class="type-toggle" role="group" aria-label="Filter by type">
    <button class="type-btn active-all" data-type="all">All<span class="type-count" id="count-all">{len(all_items)}</span></button>
    <button class="type-btn" data-type="pain">Pain Points<span class="type-count" id="count-pain">{sum(1 for i in all_items if i.get('item_type') == 'pain')}</span></button>
    <button class="type-btn" data-type="optimisation">Optimisations<span class="type-count" id="count-opt">{sum(1 for i in all_items if i.get('item_type') == 'optimisation')}</span></button>
  </div>

  <div class="stage-filters" role="group" aria-label="Filter by stage">
    {pills_html}
  </div>

  {groups_html}

  <p style="font-size:12px;color:var(--muted);text-align:right">Generated {generated}</p>

  <div class="modal-overlay" id="finding-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div class="modal-body">
      <button class="modal-close-x" id="modal-close-x" aria-label="Close">&times;</button>
      <div class="modal-top">
        <span class="modal-id" id="modal-id"></span>
        <span class="modal-type" id="modal-type"></span>
        <span class="modal-stage" id="modal-stage"></span>
        <span class="modal-conf" id="modal-conf"></span>
      </div>
      <p class="modal-desc" id="modal-desc"></p>
      <blockquote class="modal-quote" id="modal-quote-wrap">
        <span id="modal-quote"></span>
        <cite id="modal-speaker"></cite>
      </blockquote>
      <div class="modal-meta" id="modal-meta"></div>
      <div id="modal-rec-wrap"></div>
      <button class="btn-close" id="modal-close-btn">Close</button>
    </div>
  </div>
</div>

<script>
const ITEMS = {items_json};
const itemMap = Object.fromEntries(ITEMS.map(i => [i.id, i]));
const modal = document.getElementById('finding-modal');
const confColors = {{
  HIGH:   ['#d1fae5','#166534','#6ee7b7'],
  MEDIUM: ['#fef3c7','#92400e','#fcd34d'],
  LOW:    ['#f1f5f9','#475569','#cbd5e1'],
}};
const typeStyles = {{
  pain:        ['PAIN POINT',  '#fef2f2','#b91c1c'],
  optimisation: ['OPTIMISATION', '#f0fdf4','#15803d'],
}};

function openModal(id) {{
  const d = itemMap[id]; if (!d) return;
  document.getElementById('modal-id').textContent = d.id;
  const typeEl = document.getElementById('modal-type');
  const [tlabel, tbg, tfg] = typeStyles[d.itemType] || typeStyles.pain;
  typeEl.textContent = tlabel;
  typeEl.style.cssText = `background:${{tbg}};color:${{tfg}}`;
  document.getElementById('modal-stage').textContent = d.stageLabel;
  const conf = document.getElementById('modal-conf');
  conf.textContent = d.confidence;
  const [bg,fg,bd] = confColors[d.confidence] || ['#f1f5f9','#475569','#cbd5e1'];
  conf.style.cssText = `background:${{bg}};color:${{fg}};border:1px solid ${{bd}}`;
  document.getElementById('modal-desc').textContent = d.description;
  const qwrap = document.getElementById('modal-quote-wrap');
  if (d.quote) {{
    document.getElementById('modal-quote').textContent = '\u201c' + d.quote + '\u201d';
    document.getElementById('modal-speaker').textContent = d.speaker || '';
    qwrap.style.display = '';
  }} else {{
    qwrap.style.display = 'none';
  }}
  document.getElementById('modal-meta').textContent = d.session ? 'Session ' + d.session : '';
  const recWrap = document.getElementById('modal-rec-wrap');
  if (d.recHref) {{
    recWrap.innerHTML = '<a class="btn-recording" href="' + d.recHref + '" target="_blank" rel="noopener">&#9654; Watch in recording &rarr;</a><br>';
  }} else {{
    recWrap.innerHTML = '';
  }}
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function closeModal() {{
  modal.classList.remove('open');
  document.body.style.overflow = '';
}}

document.querySelectorAll('.finding-card').forEach(card => {{
  card.addEventListener('click', () => openModal(card.dataset.id));
  card.addEventListener('keydown', e => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); openModal(card.dataset.id); }} }});
}});
document.getElementById('modal-close-x').addEventListener('click', closeModal);
document.getElementById('modal-close-btn').addEventListener('click', closeModal);
modal.addEventListener('click', e => {{ if (e.target === modal) closeModal(); }});
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});

// ── Type + Stage filtering ──
let activeType = 'all';
let activeStage = 'all';

function applyFilters() {{
  document.querySelectorAll('.finding-card').forEach(card => {{
    const item = itemMap[card.dataset.id];
    if (!item) return;
    const typeMatch = activeType === 'all' || item.itemType === activeType;
    card.classList.toggle('type-hidden', !typeMatch);
  }});
  document.querySelectorAll('.stage-group').forEach(g => {{
    const stageMatch = activeStage === 'all' || g.dataset.stage === activeStage;
    const hasVisible = g.querySelectorAll('.finding-card:not(.type-hidden)').length > 0;
    g.hidden = !stageMatch || !hasVisible;
    const countEl = g.querySelector('.stage-count');
    if (countEl) countEl.textContent = g.querySelectorAll('.finding-card:not(.type-hidden)').length;
  }});
  document.querySelectorAll('.pill').forEach(pill => {{
    const stage = pill.dataset.stage;
    let count;
    if (stage === 'all') {{
      count = ITEMS.filter(i => activeType === 'all' || i.itemType === activeType).length;
    }} else {{
      count = ITEMS.filter(i => i.stage === stage && (activeType === 'all' || i.itemType === activeType)).length;
    }}
    const label = pill.textContent.replace(/\\s*\\(\\d+\\)/, '');
    pill.textContent = label + ' (' + count + ')';
  }});
  const totalVisible = ITEMS.filter(i => activeType === 'all' || i.itemType === activeType).length;
  const sub = document.querySelector('.findings-sub');
  if (sub) sub.innerHTML = totalVisible + ' talking points from our conversations &mdash; these are the pain points you raised and the optimisation ideas we explored together. This is not our proposed solution; that comes next.';
}}

document.querySelectorAll('.type-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.type-btn').forEach(b => b.className = 'type-btn');
    const type = btn.dataset.type;
    btn.classList.add(type === 'all' ? 'active-all' : type === 'pain' ? 'active-pain' : 'active-opt');
    activeType = type;
    applyFilters();
  }});
}});

document.querySelectorAll('.pill').forEach(pill => {{
  pill.addEventListener('click', () => {{
    document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
    pill.classList.add('active');
    activeStage = pill.dataset.stage;
    applyFilters();
  }});
}});
</script>
</body>
</html>"""


def generate_waste_partial(ssad: dict) -> str:
    waste_items = ssad.get("waste_items", [])
    # Deduplicate by waste_id
    seen_ids: set = set()
    deduped = []
    for w in waste_items:
        wid = w.get("waste_id", "")
        if wid and wid in seen_ids:
            continue
        seen_ids.add(wid)
        deduped.append(w)
    waste_items = deduped

    if not waste_items:
        return "<html><body><p>No waste_items found in audit data.</p></body></html>"

    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    blended_rate = ssad.get("blended_hourly_rate_aud") or 0

    session_map = {s.get("session_number"): s for s in ssad.get("sessions", [])}

    qualified = [w for w in waste_items if w.get("confidence") in ("HIGH", "MEDIUM")]
    total_annual = sum(w.get("annual_waste_aud") or 0 for w in qualified)
    total_hrs_pw = sum(w.get("hours_per_week") or 0 for w in waste_items)

    type_totals: dict = {}
    for w in waste_items:
        wt = w.get("waste_type", "other")
        type_totals[wt] = type_totals.get(wt, 0) + (w.get("annual_waste_aud") or 0)

    quantified_types = [(t, v) for t, v in type_totals.items() if v > 0]
    quantified_types.sort(key=lambda x: x[1], reverse=True)

    bars_html = ""
    for wt, amt in quantified_types:
        pct = round(amt / max(total_annual, 1) * 100)
        lbl = _waste_type_label(wt)
        bars_html += f"""
        <div class="bar-row">
          <div class="bar-label">{escape(lbl)}</div>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%" title="{fmt_aud(amt)}/yr"></div></div>
          <div class="bar-amt">{fmt_aud(amt)}</div>
        </div>"""
    if not bars_html:
        bars_html = '<p style="color:#64748b;font-size:13px">Waste quantities not yet calculated.</p>'

    _waste_labels, _ = _build_stage_lookups(ssad)
    modal_data = []
    items_html = ""
    conf_colors = {"HIGH": ("#d1fae5", "#166534", "#6ee7b7"), "MEDIUM": ("#fef3c7", "#92400e", "#fcd34d"), "LOW": ("#f1f5f9", "#475569", "#cbd5e1")}

    for i, w in enumerate(waste_items):
        wid = w.get("waste_id") or f"W-{i+1:03d}"
        stage = w.get("stage", "")
        stage_lbl = _findings_stage_label(stage, _waste_labels) if stage else "—"
        wt = w.get("waste_type", "")
        wt_lbl = _waste_type_label(wt) if wt else "—"
        desc = w.get("description") or w.get("activity", "")
        annual = w.get("annual_waste_aud")
        monthly = w.get("monthly_waste_aud")
        hrs = w.get("hours_per_week")
        headcount = w.get("headcount_affected")
        conf = w.get("confidence", "LOW")
        quote = w.get("quote", "")
        session_num = w.get("source_session")
        item_rate = w.get("hourly_rate_aud") or blended_rate
        rate_estimated = w.get("rate_is_estimated", True) if w.get("hourly_rate_aud") else True
        rec_href = None
        if session_num:
            sess = session_map.get(session_num)
            ts = w.get("source_timestamp_seconds")
            if sess and sess.get("fathom_url") and ts is not None:
                rec_href = f"{sess['fathom_url']}?t={ts}"
        # Also check meeting_references for deep-links
        if not rec_href:
            for mref in w.get("meeting_references", []):
                ms = mref.get("session")
                mts = mref.get("timestamp_seconds")
                murl = mref.get("fathom_url")
                if murl and mts is not None:
                    rec_href = f"{murl}?t={mts}"
                    break
                elif ms and session_map.get(ms) and session_map[ms].get("fathom_url") and mts is not None:
                    rec_href = f"{session_map[ms]['fathom_url']}?t={mts}"
                    break

        derived_annual = annual
        if not derived_annual and hrs and item_rate:
            derived_annual = round(hrs * headcount * item_rate * 52) if headcount else round(hrs * item_rate * 52)

        modal_data.append({
            "id": wid, "stage": stage, "stageLabel": stage_lbl,
            "wasteType": wt_lbl, "description": desc,
            "quote": quote, "session": session_num,
            "hoursPerWeek": hrs, "headcount": headcount,
            "hourlyRate": item_rate, "rateIsEstimated": rate_estimated,
            "annual": annual, "monthly": monthly,
            "derivedAnnual": derived_annual,
            "confidence": conf, "recHref": rec_href,
        })

        bg, fg, bd = conf_colors.get(conf, ("#f1f5f9", "#475569", "#cbd5e1"))
        desc_short = escape(desc[:100] + ("…" if len(desc) > 100 else ""))
        annual_display = fmt_aud(annual) if annual else (fmt_aud(derived_annual) + "*" if derived_annual else "")
        rate_tag = " (est)" if rate_estimated and item_rate else ""
        rec_badge = f'<a class="wi-rec-link" href="{rec_href}" target="_blank" rel="noopener" onclick="event.stopPropagation()">&#9654;</a>' if rec_href else ""

        # Build formula parts for visual breakdown
        formula_parts = []
        if hrs:
            formula_parts.append(f"{hrs} hrs/wk")
        if headcount and headcount > 1:
            formula_parts.append(f"{headcount} people")
        if item_rate:
            formula_parts.append(f"${item_rate}/hr{rate_tag}")
        formula_parts.append("52 wks")
        formula_str = " &times; ".join(formula_parts)

        if annual or derived_annual:
            right_html = (
                f"<span class='wi-amt-val'>{annual_display}</span>"
                f"<div class='wi-amt-label'>per year</div>"
                f"<div class='wi-formula'>{formula_str}</div>"
            )
        elif hrs:
            right_html = (
                f"<span class='wi-unquant'>Needs quantification</span>"
                f"<div class='wi-formula'>{formula_str}</div>"
            )
        else:
            right_html = "<span class='wi-unquant'>Needs quantification</span>"

        items_html += f"""
        <div class="waste-item" data-id="{escape(wid)}" role="button" tabindex="0" aria-haspopup="dialog">
          <div class="wi-left">
            <div class="wi-top">
              <span class="wi-id">{escape(wid)}</span>
              <span class="wi-type">{escape(wt_lbl)}</span>
              <span class="conf-pill" style="background:{bg};color:{fg};border:1px solid {bd}">{conf}</span>
              {rec_badge}
            </div>
            <div class="wi-desc">{desc_short}</div>
          </div>
          <div class="wi-right">
            {right_html}
          </div>
        </div>"""

    items_json = json.dumps(modal_data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Total Waste Identified</title>
{BRAND_FAVICON}
{_PARTIAL_FONT}
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --bg: #f7f9fc; --fg: #0f1825; --card: #ffffff; --border: #e2e8f0; --lime: #7DFF00; --lime-fg: #166534; --muted: #64748b; --radius: 10px; }}
body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--fg); font-size: 15px; line-height: 1.5; }}
.waste-root {{ max-width: 960px; margin: 0 auto; padding: 40px 24px 80px; }}
.hero {{ background: var(--fg); color: #fff; border-radius: 16px; padding: 40px; margin-bottom: 32px; }}
.hero-eyebrow {{ font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--lime); margin-bottom: 12px; }}
.hero-amount {{ font-size: 64px; font-weight: 900; color: var(--lime); line-height: 1; margin-bottom: 6px; font-variant-numeric: tabular-nums; }}
.hero-label {{ font-size: 16px; color: #9ca3af; margin-bottom: 24px; }}
.hero-stats {{ display: flex; gap: 32px; flex-wrap: wrap; }}
.hero-stat-val {{ font-size: 28px; font-weight: 800; color: #fff; }}
.hero-stat-lbl {{ font-size: 13px; color: #9ca3af; }}
.hero-basis {{ margin-top: 20px; padding: 12px 16px; background: rgba(255,255,255,0.08); border-radius: 8px; font-size: 13px; color: #9ca3af; line-height: 1.5; border-left: 3px solid var(--lime); }}
.hero-basis strong {{ color: #fff; }}
.breakdown {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; margin-bottom: 32px; }}
.breakdown-title {{ font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 16px; }}
.bar-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }}
.bar-label {{ font-size: 13px; color: var(--fg); width: 180px; flex-shrink: 0; }}
.bar-track {{ flex: 1; background: var(--border); border-radius: 999px; height: 8px; overflow: hidden; }}
.bar-fill {{ height: 100%; background: var(--lime); border-radius: 999px; transition: width .4s; }}
.bar-amt {{ font-size: 13px; font-weight: 600; color: var(--fg); width: 80px; text-align: right; flex-shrink: 0; }}
.items-list {{ display: flex; flex-direction: column; gap: 10px; }}
.waste-item {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px 20px; cursor: pointer; transition: transform .15s, box-shadow .15s, border-color .15s; display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
.waste-item:hover {{ transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,.07); border-color: #bfdbfe; }}
.wi-left {{ flex: 1; min-width: 0; }}
.wi-top {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }}
.wi-id {{ font-size: 11px; font-weight: 700; color: var(--muted); font-family: monospace; }}
.wi-type {{ font-size: 11px; color: var(--muted); background: var(--bg); border: 1px solid var(--border); padding: 1px 7px; border-radius: 4px; }}
.conf-pill {{ font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: .05em; }}
.wi-desc {{ font-size: 13px; color: var(--fg); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.wi-right {{ text-align: right; flex-shrink: 0; }}
.wi-amt-val {{ font-size: 18px; font-weight: 800; color: var(--fg); display: block; }}
.wi-amt-label {{ font-size: 11px; color: var(--muted); }}
.wi-hrs {{ font-size: 12px; color: var(--muted); margin-top: 2px; }}
.wi-unquant {{ font-size: 12px; color: var(--muted); font-style: italic; }}
.wi-formula {{ font-size: 11px; color: var(--muted); margin-top: 4px; white-space: nowrap; }}
.wi-rec-link {{ display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%; background: var(--lime); color: var(--lime-fg); font-size: 10px; text-decoration: none; flex-shrink: 0; transition: opacity .15s; }}
.wi-rec-link:hover {{ opacity: .8; }}
.modal-overlay {{ display: none; position: fixed; inset: 0; background: rgba(15,24,37,.55); backdrop-filter: blur(4px); z-index: 1000; align-items: center; justify-content: center; padding: 20px; }}
.modal-overlay.open {{ display: flex; }}
.modal-body {{ background: var(--card); border-radius: 16px; max-width: 600px; width: 100%; max-height: 90vh; overflow-y: auto; padding: 36px; position: relative; box-shadow: 0 24px 60px rgba(0,0,0,.2); }}
.modal-top {{ display: flex; align-items: flex-start; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }}
.modal-id {{ font-size: 12px; font-weight: 700; color: var(--muted); font-family: monospace; background: var(--bg); padding: 3px 8px; border-radius: 4px; }}
.modal-conf {{ font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 4px; }}
.modal-desc {{ font-size: 16px; line-height: 1.6; margin-bottom: 20px; }}
.modal-stats {{ display: flex; gap: 24px; flex-wrap: wrap; background: var(--bg); border-radius: 8px; padding: 16px; margin-bottom: 20px; }}
.modal-stat-val {{ font-size: 22px; font-weight: 800; color: var(--fg); }}
.modal-stat-lbl {{ font-size: 12px; color: var(--muted); }}
.modal-quote {{ border-left: 3px solid var(--lime); padding: 12px 18px; background: #f0fdf4; border-radius: 0 8px 8px 0; font-style: italic; font-size: 14px; color: #374151; margin-bottom: 16px; line-height: 1.6; }}
.modal-meta {{ font-size: 13px; color: var(--muted); margin-bottom: 24px; }}
.btn-recording {{ display: inline-flex; align-items: center; gap: 8px; background: var(--lime); color: var(--lime-fg); font-weight: 700; font-size: 13px; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-bottom: 12px; transition: opacity .15s; }}
.btn-recording:hover {{ opacity: .85; }}
.btn-close {{ display: block; width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; background: transparent; color: var(--muted); font-size: 13px; font-family: inherit; cursor: pointer; }}
.btn-close:hover {{ background: var(--bg); }}
.modal-close-x {{ position: absolute; top: 16px; right: 16px; background: none; border: none; font-size: 20px; color: var(--muted); cursor: pointer; padding: 4px 8px; border-radius: 4px; }}
.modal-close-x:hover {{ background: var(--bg); }}
@media (max-width: 600px) {{ .waste-root {{ padding: 24px 16px 60px; }} .modal-body {{ padding: 24px; }} .bar-label {{ width: 120px; }} }}
</style>
</head>
<body>
<div class="waste-root">
  <div class="hero">
    <div class="hero-eyebrow">Total Waste Identified</div>
    <div class="hero-amount">{fmt_aud(total_annual)}</div>
    <div class="hero-label">estimated annual waste</div>
    <div class="hero-stats">
      <div><div class="hero-stat-val">{len(waste_items)}</div><div class="hero-stat-lbl">waste areas</div></div>
      <div><div class="hero-stat-val">{total_hrs_pw:.1f}</div><div class="hero-stat-lbl">hrs/week wasted</div></div>
      <div><div class="hero-stat-val">${blended_rate}<span style="font-size:14px;font-weight:600">/hr</span></div><div class="hero-stat-lbl">default hourly rate</div></div>
    </div>
    <div class="hero-basis">Each waste item uses a role-specific hourly rate where discussed, falling back to <strong>${blended_rate}/hr</strong> as a default estimate. Rates marked <em>(est)</em> will be validated during your review call. The rate used is shown on each row.</div>
  </div>

  <div class="breakdown">
    <div class="breakdown-title">Breakdown by waste type</div>
    {bars_html}
  </div>

  <div class="items-list">
    {items_html}
  </div>

  <p style="font-size:12px;color:var(--muted);text-align:right;margin-top:24px">Generated {generated}</p>

  <div class="modal-overlay" id="waste-modal" role="dialog" aria-modal="true">
    <div class="modal-body">
      <button class="modal-close-x" id="modal-close-x" aria-label="Close">&times;</button>
      <div class="modal-top">
        <span class="modal-id" id="modal-id"></span>
        <span class="modal-conf" id="modal-conf"></span>
      </div>
      <p class="modal-desc" id="modal-desc"></p>
      <div class="modal-stats" id="modal-stats"></div>
      <blockquote class="modal-quote" id="modal-quote-wrap"><span id="modal-quote"></span></blockquote>
      <div class="modal-meta" id="modal-meta"></div>
      <div id="modal-rec-wrap"></div>
      <button class="btn-close" id="modal-close-btn">Close</button>
    </div>
  </div>
</div>

<script>
const ITEMS = {items_json};
const itemMap = Object.fromEntries(ITEMS.map(i => [i.id, i]));
const modal = document.getElementById('waste-modal');
const confColors = {{ HIGH:['#d1fae5','#166534','#6ee7b7'], MEDIUM:['#fef3c7','#92400e','#fcd34d'], LOW:['#f1f5f9','#475569','#cbd5e1'] }};

function fmtAud(v) {{
  if (v == null) return null;
  return '$' + Math.round(v).toLocaleString('en-AU');
}}

function openModal(id) {{
  const d = itemMap[id]; if (!d) return;
  document.getElementById('modal-id').textContent = d.id;
  const conf = document.getElementById('modal-conf');
  conf.textContent = d.confidence;
  const [bg,fg,bd] = confColors[d.confidence] || ['#f1f5f9','#475569','#cbd5e1'];
  conf.style.cssText = `background:${{bg}};color:${{fg}};border:1px solid ${{bd}}`;
  document.getElementById('modal-desc').textContent = d.description;
  const stats = document.getElementById('modal-stats');
  let statsHtml = '';
  if (d.annual || d.derivedAnnual) statsHtml += `<div><div class="modal-stat-val">${{fmtAud(d.annual || d.derivedAnnual)}}</div><div class="modal-stat-lbl">per year${{d.annual ? '' : '*'}}</div></div>`;
  if (d.hoursPerWeek) statsHtml += `<div><div class="modal-stat-val">${{d.hoursPerWeek}}</div><div class="modal-stat-lbl">hrs/week</div></div>`;
  if (d.headcount) statsHtml += `<div><div class="modal-stat-val">${{d.headcount}}</div><div class="modal-stat-lbl">people affected</div></div>`;
  if (d.hourlyRate) statsHtml += `<div><div class="modal-stat-val">${{d.hourlyRate}}/hr</div><div class="modal-stat-lbl">${{d.rateIsEstimated ? 'estimated rate' : 'discussed rate'}}</div></div>`;
  stats.innerHTML = statsHtml;
  stats.style.display = statsHtml ? '' : 'none';
  const qwrap = document.getElementById('modal-quote-wrap');
  if (d.quote) {{ document.getElementById('modal-quote').textContent = '\u201c' + d.quote + '\u201d'; qwrap.style.display = ''; }}
  else {{ qwrap.style.display = 'none'; }}
  document.getElementById('modal-meta').textContent = d.session ? 'Session ' + d.session : '';
  const recWrap = document.getElementById('modal-rec-wrap');
  recWrap.innerHTML = d.recHref ? '<a class="btn-recording" href="' + d.recHref + '" target="_blank" rel="noopener">&#9654; Watch in recording &rarr;</a><br>' : '';
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function closeModal() {{ modal.classList.remove('open'); document.body.style.overflow = ''; }}

document.querySelectorAll('.waste-item').forEach(el => {{
  el.addEventListener('click', () => openModal(el.dataset.id));
  el.addEventListener('keydown', e => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); openModal(el.dataset.id); }} }});
}});
document.getElementById('modal-close-x').addEventListener('click', closeModal);
document.getElementById('modal-close-btn').addEventListener('click', closeModal);
modal.addEventListener('click', e => {{ if (e.target === modal) closeModal(); }});
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});
</script>
</body>
</html>"""


# ─── CLI ───────────────────────────────────────────────────────────────────────

import re as _re_mod

_PRICING_PATTERN = _re_mod.compile(
    r'\$\d|/mo\b|/yr\b|/user|/seat|per.user|per-user|per.seat|per-seat'
    r'|pricing\b|priced|price\b|\bfree\b|\bcosts?\b|\bcheap|\bexpens'
    r'|\bupsell|\bsubscription|\btier\b|\bpaid\b|\bafford',
    _re_mod.IGNORECASE)

def _is_pricing_text(text: str) -> bool:
    """Return True if text is primarily about pricing/cost rather than functionality."""
    return bool(_PRICING_PATTERN.search(text))


def generate_solutions_overview(ssad: dict) -> str:
    """Generate solutions-overview.html — researched options per proposed change with unified comparison tables."""
    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    changes = ssad.get("proposed_changes", [])
    stage_labels, _ = _build_stage_lookups(ssad)
    headcount = ssad.get("headcount", {})
    current_staff = headcount.get("support_workers", 50) + headcount.get("offshore_team", 0)
    # Use contact.company_size to extract rough number, fallback to 50
    try:
        size_str = ssad.get("contact", {}).get("company_size", "")
        import re as _re
        _nums = _re.findall(r'\d+', size_str)
        if _nums:
            current_staff = int(_nums[0])
    except Exception:
        pass
    scaled_staff = current_staff * 2  # Show what happens at 2x scale

    by_stage = {}
    for c in changes:
        by_stage.setdefault(c.get("stage", "other"), []).append(c)

    n_total = len(changes)
    n_researched = sum(1 for c in changes if c.get("research", {}).get("status") in ("complete", "needs_review"))
    n_tools = sum(1 for c in changes for t in c.get("research", {}).get("tools_researched", []) if "Custom" not in str(t.get("tool_name", "")))
    # Order stages by the customer journey (process map order), not alphabetically
    _process_stage_order = []
    for p in ssad.get("processes", []):
        ps = p.get("stage", "")
        if ps and ps not in _process_stage_order:
            _process_stage_order.append(ps)
    stages_covered = sorted(by_stage.keys(),
                            key=lambda s: _process_stage_order.index(s) if s in _process_stage_order else 999)

    # Pain point lookup
    pp_map = {p["pain_point_id"]: p for p in ssad.get("pain_points", [])}

    stats_bar = f"""
    <div class="so-stats">
      {_stat_box(str(n_total), "Opportunities")}
      {_stat_box(str(n_researched), "Researched")}
      {_stat_box(str(n_tools), "Tools evaluated")}
      {_stat_box(str(len(stages_covered)), "Stages covered")}
    </div>"""

    # Build cards
    cards_html = ""
    card_idx = 0
    for stage in stages_covered:
        stage_name = _stage_label(stage, stage_labels)
        stage_changes = by_stage[stage]
        cards_html += f'<div class="so-stage"><div class="so-stage-title">{escape(stage_name)}</div>'

        for c in stage_changes:
            card_idx += 1
            cid = c.get("change_id", "")
            title = escape(c.get("title", ""))
            change_type = c.get("change_type", "")
            badge_label, badge_color, badge_bg = CHANGE_BADGE.get(change_type, ("OTHER", BRAND_GREY, "#F1F5F9"))
            source = c.get("source", "client")
            source_badge = f'<span class="so-badge" style="background:#E0E7FF;color:#4338CA">ANALYST</span>' if source == "analyst" else ""

            research = c.get("research", {})
            tools = research.get("tools_researched", [])
            custom = research.get("custom_build_option", {})
            landscape = research.get("industry_landscape", {})
            risks = research.get("risks", [])

            val = c.get("value", {})
            annual_val = val.get("combined_annual_value_aud", 0)
            formula = val.get("formula_summary", "")
            impl = c.get("implementation", {})
            weeks_lbl = impl.get("weeks_label", "—")

            # Quote from first linked pain point
            pp_ids = c.get("linked_pain_point_ids", [])
            quote_html = ""
            for pid in pp_ids[:1]:
                pp = pp_map.get(pid)
                if pp and pp.get("quote"):
                    quote_html = f'<div class="so-quote">&ldquo;{escape(pp["quote"][:180])}&rdquo;</div>'

            # ── UNIFIED COMPARISON TABLE ──
            # SaaS tools only — custom build is handled separately via the Solution Designer
            saas_tools = [t for t in tools if "Custom" not in str(t.get("tool_name", ""))]
            option_cards = ""
            for t in saas_tools:
                tname = escape(str(t.get("tool_name", "—")))
                rec_badge = ""
                row_bg = "so-opt-default"

                pricing_sum = escape(str(t.get("pricing_summary", ""))[:200])
                cost_current = escape(str(t.get("cost_at_current_headcount", "—")))
                cost_scaled = escape(str(t.get("cost_at_scaled_headcount", "—")))
                annual = t.get("annual_cost_aud", 0)
                annual_str = f"${annual:,.0f}/yr" if annual else "Free"

                # Upsell indicator — show likely next-tier cost below "Free" label
                upsell_hint = ""
                if not annual:
                    likely_upsells = [h for h in t.get("hidden_costs", []) if h.get("likelihood") == "likely"]
                    if likely_upsells:
                        upsell_cost = sum(h.get("estimated_annual_aud", 0) or 0 for h in likely_upsells)
                        if upsell_cost > 0:
                            upsell_hint = f'<div style="font-size:11px;color:#EA580C;font-weight:600;margin-top:2px">Likely upsell: ${upsell_cost:,.0f}/yr</div>'

                # Pricing source and hidden costs
                src_badge = pricing_source_badge(t.get("pricing_source_type", ""))
                estimated_note = ' <span class="so-estimated-note">(estimated)</span>' if t.get("pricing_is_estimated") else ""
                hc_html = hidden_costs_html(t.get("hidden_costs", []))
                total_with_hidden = t.get("total_cost_with_hidden_aud", 0) or 0
                true_cost_html = ""
                if total_with_hidden and total_with_hidden > (annual or 0):
                    true_cost_html = f"""<div class="so-true-cost">
                        <span class="so-scale-label">True annual cost (incl. likely hidden costs)</span>
                        <span class="so-true-cost-val">${total_with_hidden:,.0f}/yr</span>
                    </div>"""

                pros_html = "".join(f"<li>{escape(str(p))}</li>" for p in t.get("pros", [])[:5])
                cons_html = "".join(f"<li>{escape(str(c2))}</li>" for c2 in t.get("cons", [])[:5])

                # Source links
                links = ""
                purl = t.get("pricing_url", "")
                durl = t.get("docs_url", "")
                if purl:
                    links += f'<a href="{escape(purl)}" target="_blank" class="so-source-link">Pricing</a>'
                if durl:
                    links += f'<a href="{escape(durl)}" target="_blank" class="so-source-link">Docs</a>'

                option_cards += f"""
                <div class="so-option {row_bg}">
                    <div class="so-opt-header">
                        <div class="so-opt-name"><strong>{tname}</strong> {rec_badge} {src_badge}</div>
                        <div style="text-align:right"><div class="so-opt-annual">{annual_str}{estimated_note}</div>{upsell_hint}</div>
                    </div>
                    <div class="so-opt-pricing">{pricing_sum}</div>
                    <div class="so-opt-scaling">
                        <div class="so-scale-col"><span class="so-scale-label">At {current_staff} staff</span><span class="so-scale-val">{cost_current}</span></div>
                        <div class="so-scale-col"><span class="so-scale-label">At {scaled_staff} staff</span><span class="so-scale-val">{cost_scaled}</span></div>
                        <div class="so-scale-col"><span class="so-scale-label">API</span><span class="so-scale-val">{"✓" if t.get("api_available") else "✗"}</span></div>
                    </div>
                    {true_cost_html}
                    {hc_html}
                    <div class="so-opt-proscons">
                        <div><div class="so-pc-label so-pro-label">Pros</div><ul>{pros_html}</ul></div>
                        <div><div class="so-pc-label so-con-label">Cons</div><ul>{cons_html}</ul></div>
                    </div>
                    <div class="so-opt-footer">{links} {confidence_badge(t.get("confidence", "—"))}</div>
                </div>"""

            comparison_table = ""
            if option_cards:
                comparison_table = f"""
                <div class="so-comparison">
                    <div class="so-label">OPTIONS COMPARISON — {len(saas_tools)} approaches evaluated</div>
                    {option_cards}
                </div>"""

            # Industry landscape (collapsible)
            landscape_html = ""
            if landscape:
                landscape_html = f"""
                <details class="so-details so-details-blue">
                    <summary>Industry Landscape</summary>
                    <div class="so-details-body">
                        <div class="so-landscape-row"><strong>What peers do:</strong> {escape(landscape.get("common_approaches", ""))}</div>
                        <div class="so-landscape-row"><strong>Best practice:</strong> {escape(landscape.get("best_practice", ""))}</div>
                        <div class="so-landscape-row so-highlight"><strong>Your position:</strong> {escape(landscape.get("competitive_position", ""))}</div>
                    </div>
                </details>"""

            # Risks (collapsible)
            risks_html = ""
            if risks:
                risk_items = "".join(f"<li>{escape(str(r))}</li>" for r in risks[:4])
                risks_html = f"""
                <details class="so-details so-details-grey">
                    <summary>Risks &amp; Considerations ({len(risks)})</summary>
                    <div class="so-details-body"><ul class="so-risk-list">{risk_items}</ul></div>
                </details>"""

            # Value footer
            value_html = ""
            if annual_val or formula:
                value_html = f"""
                <div class="so-value-bar">
                    <div class="so-value-amount">{fmt_aud(annual_val)}<span class="so-value-yr">/yr</span></div>
                    <div class="so-value-formula">{escape(formula)}</div>
                    <div class="so-value-weeks">{escape(weeks_lbl)}</div>
                </div>"""

            cards_html += f"""
            <div class="so-card" id="card-{escape(cid)}">
                <div class="so-card-header">
                    <div class="so-card-badges">
                        <span class="so-badge" style="background:{badge_bg};color:{badge_color}">{badge_label}</span>
                        {source_badge}
                        <span class="so-card-id">{escape(cid)}</span>
                    </div>
                    <h3 class="so-card-title">{title}</h3>
                    <p class="so-card-desc">{escape(c.get("proposed_solution", "")[:200])}</p>
                    {quote_html}
                </div>
                {comparison_table}
                {landscape_html}
                {risks_html}
                {value_html}
            </div>"""

        cards_html += "</div>"

    # ── PRICING REFERENCE & VERIFICATION TABLE ──
    seen_tools: dict = {}
    for c in changes:
        cid = c.get("change_id", "")
        for t in c.get("research", {}).get("tools_researched", []):
            tname = str(t.get("tool_name", "")).strip()
            if not tname or "Custom" in tname:
                continue
            if tname not in seen_tools:
                seen_tools[tname] = {
                    "tool_name": tname,
                    "annual_cost_aud": t.get("annual_cost_aud"),
                    "realistic_annual_cost_aud": t.get("realistic_annual_cost_aud"),
                    "pricing_url": t.get("pricing_url", ""),
                    "source_urls": list(t.get("source_urls", [])),
                    "pricing_source_type": t.get("pricing_source_type", ""),
                    "pricing_is_estimated": t.get("pricing_is_estimated", False),
                    "pricing_verified_date": t.get("pricing_verified_date", ""),
                    "confidence": t.get("confidence", ""),
                    "pricing_model": t.get("pricing_model", ""),
                    "per_user_monthly_aud": t.get("per_user_monthly_aud"),
                    "flat_monthly_aud": t.get("flat_monthly_aud"),
                    "change_ids": [cid],
                }
            else:
                existing = seen_tools[tname]
                if cid and cid not in existing["change_ids"]:
                    existing["change_ids"].append(cid)
                for url in t.get("source_urls", []):
                    if url and url not in existing["source_urls"]:
                        existing["source_urls"].append(url)

    ref_rows = ""
    for tname in sorted(seen_tools.keys(), key=str.lower):
        t = seen_tools[tname]
        annual = t["annual_cost_aud"]
        realistic = t["realistic_annual_cost_aud"]
        if annual is not None and annual != "":
            try:
                price_str = f"${float(annual):,.0f}/yr"
            except (ValueError, TypeError):
                price_str = escape(str(annual))
        elif realistic is not None and realistic != "":
            try:
                price_str = f"${float(realistic):,.0f}/yr"
            except (ValueError, TypeError):
                price_str = escape(str(realistic))
        else:
            price_str = '<span style="color:#9CA3AF;font-style:italic">No pricing</span>'

        est_flag = ' <span class="so-estimated-note">(est.)</span>' if t["pricing_is_estimated"] else ""

        purl = t["pricing_url"]
        pricing_link = f'<a href="{escape(purl)}" target="_blank" class="so-source-link">Official pricing</a>' if purl else '<span style="color:#9CA3AF;font-size:11px">&mdash;</span>'

        src_links = ""
        for i, url in enumerate(t["source_urls"]):
            if url:
                src_links += f'<a href="{escape(url)}" target="_blank" class="so-source-link">Source {i + 1}</a> '
        if not src_links:
            src_links = '<span style="color:#9CA3AF;font-size:11px">None</span>'

        src_badge = pricing_source_badge(t["pricing_source_type"])
        conf_badge = confidence_badge(t["confidence"])
        verified = escape(str(t["pricing_verified_date"])) if t["pricing_verified_date"] else "&mdash;"

        # ── Pricing model cell: show per-unit cost (e.g. "$31/user/mo") alongside the annual total ──
        pmodel = (t.get("pricing_model") or "").strip().lower()
        puu = t.get("per_user_monthly_aud")
        pflat = t.get("flat_monthly_aud")
        def _fmt_money(v):
            try:
                return f"${float(v):,.0f}"
            except (ValueError, TypeError):
                return None
        if pmodel == "per_user":
            m = _fmt_money(puu)
            model_cell = f"{m}/user/mo" if m and float(puu) > 0 else "Per user"
        elif pmodel == "flat":
            m = _fmt_money(pflat)
            model_cell = f"{m}/mo flat" if m and float(pflat) > 0 else "Flat fee"
        elif pmodel == "per_unit":
            model_cell = "Per unit"
        elif pmodel == "usage_based":
            model_cell = "Usage-based"
        elif pmodel == "free":
            model_cell = "Free"
        elif pmodel == "custom":
            model_cell = "Custom quote"
        else:
            model_cell = '<span style="color:#9CA3AF;font-size:11px">&mdash;</span>'

        ref_rows += f"""<tr>
            <td><strong>{escape(tname)}</strong></td>
            <td style="white-space:nowrap">{price_str}{est_flag}</td>
            <td style="white-space:nowrap">{model_cell}</td>
            <td>{src_badge}</td>
            <td>{conf_badge}</td>
            <td>{verified}</td>
            <td>{pricing_link}</td>
            <td><div class="so-ref-links">{src_links}</div></td>
        </tr>"""

    pricing_ref_html = ""
    if ref_rows:
        pricing_ref_html = f"""
<div class="so-pricing-ref">
    <div class="so-pricing-ref-title">Pricing Reference &amp; Verification</div>
    <p class="so-pricing-ref-desc">All tools mentioned in this report with their quoted pricing, data sources, and verification status.
    Verify pricing directly via the official links before making purchasing decisions.</p>
    <div style="overflow-x:auto">
    <table class="so-pricing-table">
        <thead><tr>
            <th>Tool</th>
            <th>Quoted Price</th>
            <th>Pricing Model</th>
            <th>Source</th>
            <th>Confidence</th>
            <th>Verified</th>
            <th>Pricing Page</th>
            <th>Reference URLs</th>
        </tr></thead>
        <tbody>{ref_rows}</tbody>
    </table>
    </div>
    <div class="so-pricing-ref-legend">
        <strong>Source types:</strong>
        {pricing_source_badge("official")} Scraped from vendor pricing page &nbsp;
        {pricing_source_badge("aggregator")} From comparison / review sites &nbsp;
        {pricing_source_badge("blog")} From blog or article &nbsp;
        {pricing_source_badge("estimated")} Estimated from training data
    </div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Solutions Overview</title>
{BRAND_FAVICON}
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        color: {BRAND_DARK}; background: {BRAND_LIGHT}; font-size: 15px; line-height: 1.6; }}
.apg-header {{ background: {BRAND_DARK}; color: #fff; padding: 20px 32px;
               display: flex; align-items: center; gap: 16px; }}
.apg-header .logo {{ font-size: 20px; font-weight: 800; }}
.container {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px; }}

/* Stats */
.so-stats {{ display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 28px; }}
.stat-box {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 10px; padding: 16px 12px; text-align: center; }}
.stat-val {{ font-size: 26px; font-weight: 800; color: {BRAND_DARK}; letter-spacing: -0.03em; margin-bottom: 2px; }}
.stat-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em; color: {BRAND_GREY}; }}

/* Stages */
.so-stage {{ margin-bottom: 40px; }}
.so-stage-title {{ font-size: 18px; font-weight: 700; padding-bottom: 8px; margin-bottom: 16px;
                   border-bottom: 2px solid {BRAND_BORDER}; }}

/* Cards */
.so-card {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 12px;
            margin-bottom: 16px; overflow: hidden; }}
.so-card-header {{ padding: 20px 24px 16px; }}
.so-card-badges {{ display: flex; align-items: center; gap: 6px; margin-bottom: 8px; }}
.so-badge {{ padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;
             text-transform: uppercase; letter-spacing: 0.04em; }}
.so-card-id {{ font-size: 11px; font-weight: 700; color: {BRAND_GREY}; margin-left: auto; }}
.so-card-title {{ font-size: 17px; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }}
.so-card-desc {{ font-size: 13px; color: {BRAND_GREY}; margin-bottom: 8px; }}
.so-quote {{ font-style: italic; font-size: 13px; color: {BRAND_GREY}; padding: 6px 0 6px 14px;
             border-left: 3px solid {BRAND_PRIMARY}; margin: 8px 0; }}

/* Strategic approaches */
.sa-section {{ margin-bottom: 40px; }}
.sa-header {{ margin-bottom: 20px; }}
.sa-title {{ font-size: 22px; font-weight: 800; color: {BRAND_DARK}; margin-bottom: 4px; }}
.sa-subtitle {{ font-size: 14px; color: {BRAND_GREY}; line-height: 1.5; }}
.sa-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.sa-card {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 12px; padding: 24px;
            display: flex; flex-direction: column; }}
.sa-card-custom {{ border-color: #BBF7D0; background: #FAFFFE; }}
.sa-card-hybrid {{ border-color: #BFDBFE; background: #FAFBFF; }}
.sa-card-icon {{ font-size: 28px; margin-bottom: 8px; }}
.sa-card-name {{ font-size: 17px; font-weight: 800; color: {BRAND_DARK}; margin-bottom: 4px; }}
.sa-card-cost {{ font-size: 24px; font-weight: 800; color: {BRAND_DARK}; margin-bottom: 12px; }}
.sa-yr {{ font-size: 13px; font-weight: 600; color: {BRAND_GREY}; margin-left: 2px; }}
.sa-card-desc {{ font-size: 13px; color: {BRAND_DARK}; line-height: 1.6; margin-bottom: 12px; flex: 1; }}
.sa-card-tradeoff {{ font-size: 12px; color: {BRAND_GREY}; background: #F8FAFC; border-radius: 6px;
                     padding: 8px 10px; margin-bottom: 12px; line-height: 1.5; }}
.sa-card-changes {{ display: flex; flex-wrap: wrap; gap: 4px; }}
.sa-link {{ font-size: 11px; color: #3B82F6; text-decoration: none; padding: 2px 6px;
            border: 1px solid #DBEAFE; border-radius: 3px; white-space: nowrap; }}
.sa-link:hover {{ background: #EFF6FF; }}
.sa-more {{ font-size: 11px; color: {BRAND_GREY}; padding: 2px 6px; }}
@media (max-width: 768px) {{ .sa-grid {{ grid-template-columns: 1fr; }} }}

/* Option cards */
.so-comparison {{ padding: 0 24px 16px; }}
.so-label {{ font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
             color: {BRAND_GREY}; margin-bottom: 10px; }}
.so-option {{ border: 1px solid {BRAND_BORDER}; border-radius: 8px; margin-bottom: 10px; overflow: hidden; }}
.so-opt-rec {{ border-color: {BRAND_PRIMARY}; border-width: 2px; }}
.so-opt-custom {{ border-color: #BBF7D0; background: #FAFFFE; }}
.so-opt-default {{ }}
.so-opt-header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 16px 4px; }}
.so-opt-name {{ font-size: 14px; display: flex; align-items: center; gap: 8px; }}
.so-opt-annual {{ font-size: 16px; font-weight: 800; color: {BRAND_DARK}; }}
.so-rec-badge {{ background: {BRAND_PRIMARY}; color: #166534; padding: 2px 8px; border-radius: 4px;
                 font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }}
.so-opt-pricing {{ padding: 0 16px 8px; font-size: 12px; color: {BRAND_GREY}; }}
.so-opt-scaling {{ display: grid; grid-template-columns: 1fr 1fr auto; gap: 12px; padding: 8px 16px;
                   background: #F8FAFC; border-top: 1px solid {BRAND_BORDER}; border-bottom: 1px solid {BRAND_BORDER}; }}
.so-scale-col {{ display: flex; flex-direction: column; }}
.so-scale-label {{ font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {BRAND_GREY}; }}
.so-scale-val {{ font-size: 12px; font-weight: 600; color: {BRAND_DARK}; margin-top: 2px; }}
.so-opt-proscons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding: 10px 16px; }}
.so-opt-proscons ul {{ margin: 4px 0 0 14px; padding: 0; font-size: 12px; line-height: 1.6; color: {BRAND_DARK}; }}
.so-pc-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }}
.so-pro-label {{ color: #166534; }}
.so-con-label {{ color: #991B1B; }}
.so-opt-footer {{ display: flex; align-items: center; gap: 8px; padding: 6px 16px 10px;  }}
.so-source-link {{ font-size: 11px; color: #3B82F6; text-decoration: none; padding: 2px 8px;
                   border: 1px solid #BFDBFE; border-radius: 4px; }}
.so-source-link:hover {{ background: #EFF6FF; }}
.so-scope-badge {{ background: #D1FAE5; color: #166534; padding: 1px 6px; border-radius: 3px;
                   font-size: 9px; font-weight: 700; text-transform: uppercase; margin-left: 4px; }}

/* Hidden costs & true cost */
.so-estimated-note {{ font-size: 11px; color: #EF4444; font-weight: 400; }}
.so-true-cost {{ display: flex; justify-content: space-between; align-items: center; padding: 6px 16px;
                 background: #FEF2F2; border-top: 1px dashed #FECACA; border-bottom: 1px dashed #FECACA; }}
.so-true-cost-val {{ font-size: 14px; font-weight: 800; color: #DC2626; }}
.so-hidden-costs {{ border-top: 1px solid {BRAND_BORDER}; }}
.so-hidden-costs summary {{ padding: 8px 16px; font-size: 12px; font-weight: 600; cursor: pointer;
                            color: #B45309; background: #FFFBEB; user-select: none; list-style: none;
                            display: flex; align-items: center; gap: 6px; }}
.so-hidden-costs summary::before {{ content: '⚠'; font-size: 11px; }}
.so-hidden-costs summary::-webkit-details-marker {{ display: none; }}
.so-hc-body {{ padding: 8px 16px 12px; background: #FFFBEB; }}
.so-hc-item {{ margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #FEF3C7; }}
.so-hc-item:last-child {{ margin-bottom: 0; padding-bottom: 0; border-bottom: none; }}
.so-hc-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }}
.so-hc-type {{ font-size: 11px; font-weight: 700; color: #92400E; }}
.so-hc-cost {{ font-size: 12px; font-weight: 700; color: #B45309; margin-left: auto; }}
.so-hc-desc {{ font-size: 12px; color: #78716C; }}
.so-hc-trigger {{ font-size: 11px; color: #A8A29E; margin-top: 2px; font-style: italic; }}

/* Collapsible details */
.so-details {{ border-top: 1px solid {BRAND_BORDER}; }}
.so-details summary {{ padding: 10px 24px; font-size: 13px; font-weight: 600; cursor: pointer;
                       color: {BRAND_DARK}; user-select: none; list-style: none; display: flex;
                       align-items: center; gap: 8px; }}
.so-details summary::before {{ content: '▸'; font-size: 12px; color: {BRAND_GREY}; transition: transform 0.15s; }}
.so-details[open] summary::before {{ transform: rotate(90deg); }}
.so-details summary::-webkit-details-marker {{ display: none; }}
.so-details-body {{ padding: 0 24px 16px; font-size: 13px; }}
.so-details-green summary {{ background: #F0FDF4; }}
.so-details-blue summary {{ background: #EFF6FF; }}
.so-details-grey summary {{ background: #F8FAFC; }}

/* Pros/cons */
.so-pros-cons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.so-pros-cons ul {{ margin: 6px 0 0 16px; padding: 0; font-size: 12px; line-height: 1.6; }}
.so-pro-label {{ color: #166534; font-size: 12px; }}
.so-con-label {{ color: #991B1B; font-size: 12px; }}
.so-scope-note {{ margin-top: 10px; font-size: 12px; color: {BRAND_GREY}; }}

/* Landscape */
.so-landscape-row {{ margin-bottom: 8px; font-size: 13px; }}
.so-highlight {{ background: #EFF6FF; border-radius: 6px; padding: 8px 10px; margin-top: 4px; }}

/* Risks */
.so-risk-list {{ margin: 0 0 0 16px; padding: 0; font-size: 12px; color: {BRAND_GREY}; line-height: 1.7; }}

/* Value bar */
.so-value-bar {{ display: flex; align-items: center; gap: 12px; padding: 12px 24px;
                 border-top: 1px solid {BRAND_BORDER}; background: #FAFBFC; }}
.so-value-amount {{ font-size: 20px; font-weight: 800; color: {BRAND_DARK}; white-space: nowrap; }}
.so-value-yr {{ font-size: 13px; font-weight: 600; color: {BRAND_GREY}; }}
.so-value-formula {{ font-size: 12px; color: {BRAND_GREY}; flex: 1; }}
.so-value-weeks {{ background: {BRAND_DARK}; color: #fff; padding: 4px 12px; border-radius: 4px;
                   font-size: 12px; font-weight: 700; white-space: nowrap; }}

/* Info box */
.so-info {{ background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 8px;
            padding: 14px 18px; margin-bottom: 28px; font-size: 13px; }}

/* Pricing Reference Table */
.so-pricing-ref {{ margin-top: 48px; padding-top: 32px; border-top: 2px solid {BRAND_BORDER}; }}
.so-pricing-ref-title {{ font-size: 18px; font-weight: 700; margin-bottom: 6px; }}
.so-pricing-ref-desc {{ font-size: 13px; color: {BRAND_GREY}; margin-bottom: 16px; line-height: 1.6; }}
.so-pricing-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.so-pricing-table th {{ background: {BRAND_DARK}; color: #fff; padding: 10px 12px; text-align: left;
                        font-size: 10px; font-weight: 700; text-transform: uppercase;
                        letter-spacing: 0.05em; white-space: nowrap; }}
.so-pricing-table td {{ padding: 10px 12px; border-bottom: 1px solid {BRAND_BORDER}; vertical-align: middle; }}
.so-pricing-table tbody tr:nth-child(even) {{ background: #F8FAFC; }}
.so-pricing-table tbody tr:hover {{ background: #EFF6FF; }}
.so-ref-links {{ display: flex; flex-wrap: wrap; gap: 4px; }}
.so-pricing-ref-legend {{ margin-top: 12px; font-size: 12px; color: {BRAND_GREY}; display: flex;
                          flex-wrap: wrap; align-items: center; gap: 8px; }}

@media (max-width: 640px) {{
  .so-stats {{ grid-template-columns: repeat(3, 1fr); }}
  .so-pros-cons {{ grid-template-columns: 1fr; }}
  .so-value-bar {{ flex-wrap: wrap; }}
  .so-pricing-table {{ font-size: 11px; }}
  .so-pricing-table th, .so-pricing-table td {{ padding: 6px 8px; }}
}}
</style>
</head>
<body>

<div class="apg-header">
  <div class="logo">{YOUR_COMPANY}</div>
  <div>
    <div style="font-weight:700;font-size:16px">{company} — Solutions Overview</div>
    <div style="font-size:13px;color:#9CA3AF">{n_total} opportunities &middot; {n_tools} tools evaluated &middot; Generated {generated}</div>
  </div>
</div>

<div class="container">

{stats_bar}

<div class="so-info">
  <strong>How to read this:</strong> Each card shows an identified opportunity with all researched tool options,
  pricing at your current headcount, scaling projections, pros/cons, and source links.
</div>

{cards_html}

{pricing_ref_html}

<div style="font-size:11px;color:{BRAND_GREY};margin-top:32px;padding-top:16px;border-top:1px solid {BRAND_BORDER}">
  Generated by {YOUR_COMPANY} Audit System &middot; {generated} &middot; Current team size: {current_staff} staff.
  All findings cite original transcript sources.
</div>

</div>
</body>
</html>"""


def generate_options_pricing(ssad: dict) -> str:
    """Generate options-pricing page — pricing & options comparison with SaaS vs Custom vs Hybrid."""
    import math

    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    changes = ssad.get("proposed_changes", [])
    roi_items = ssad.get("roi_items", [])
    blueprint = ssad.get("transformation_blueprint", {})
    phases = blueprint.get("phases", [])
    sa = ssad.get("strategic_approaches", {})
    strategies = sa.get("strategies", [])
    strategy = strategies[0] if strategies else {}
    tool_selections = strategy.get("tool_selections", [])
    cost_summary = strategy.get("cost_summary", {})
    blended_rate = ssad.get("blended_hourly_rate_aud", 40)

    # Extract current staff count
    current_staff = sa.get("current_staff", 50)
    try:
        size_str = ssad.get("contact", {}).get("company_size", "")
        _nums = re.findall(r'\d+', size_str)
        if _nums:
            current_staff = int(_nums[0])
    except Exception:
        pass
    scaled_staff = sa.get("scaled_staff", current_staff * 2)

    # Build lookups
    changes_by_id = {c["change_id"]: c for c in changes}
    roi_by_change = {r["linked_change_id"]: r for r in roi_items if r.get("linked_change_id")}
    ts_by_change = {t["change_id"]: t for t in tool_selections}

    # ── DEDUPLICATE SaaS TOOLS ──
    # Group tool_selections by normalised tool name to find actual distinct tools
    _bundled_keywords = {"bundled", "rostering platform", "custom config"}
    _free_keywords = {"free", "(free", "built-in"}

    distinct_tools = {}  # tool_name -> {change_ids, annual_cost, category, is_free, is_bundled}
    for ts_item in tool_selections:
        raw_name = ts_item.get("selected_tool", "Unknown")
        annual = ts_item.get("annual_cost_aud", 0)
        cid = ts_item.get("change_id", "")
        name_lower = raw_name.lower()

        # Detect bundled items (part of rostering platform)
        is_bundled = any(kw in name_lower for kw in _bundled_keywords)
        is_free = any(kw in name_lower for kw in _free_keywords) or annual == 0
        is_custom_api = "custom" in name_lower and ("ai" in name_lower or "api" in name_lower or "mobile" in name_lower or "workflow" in name_lower)

        # Normalise: bundled rostering items → group under the main rostering tool
        if is_bundled:
            norm_name = "RotaWiz Premium"
            category = "bundled"
        elif is_custom_api:
            norm_name = raw_name
            category = "custom_api"
        elif is_free:
            norm_name = raw_name
            category = "free"
        else:
            norm_name = raw_name
            category = "paid"

        if norm_name not in distinct_tools:
            distinct_tools[norm_name] = {"change_ids": [], "annual_cost": 0, "category": category,
                                         "display_name": raw_name if not is_bundled else norm_name,
                                         "per_user_monthly": ts_item.get("per_user_monthly_aud", 0)}
        distinct_tools[norm_name]["change_ids"].append(cid)
        # Only add cost once for bundled items (avoid double-counting)
        if not is_bundled or len(distinct_tools[norm_name]["change_ids"]) == 1:
            distinct_tools[norm_name]["annual_cost"] += annual

    paid_tools = {k: v for k, v in distinct_tools.items() if v["category"] == "paid"}
    free_tools = {k: v for k, v in distinct_tools.items() if v["category"] == "free"}
    custom_api_tools = {k: v for k, v in distinct_tools.items() if v["category"] == "custom_api"}
    bundled_tools = {k: v for k, v in distinct_tools.items() if v["category"] == "bundled"}
    n_paid_tools = len(paid_tools) + len(bundled_tools)  # distinct paid subscriptions
    n_free_tools = len(free_tools)
    n_distinct_tools = len(distinct_tools)

    # ── PRICING CONSTANTS ──
    SPRINT_PRICE = 15000
    HOSTING_ANNUAL = 1200  # $100/mo estimated
    RD_OFFSET = 0.435

    # ── SaaS TCO ──
    saas_ongoing_current = (
        cost_summary.get("ongoing_annual_total_aud", 0)
        or cost_summary.get("ongoing_annual_current_aud", 0)
        or (cost_summary.get("ongoing_annual_saas_aud", 0)
            + cost_summary.get("ongoing_annual_cowork_tools_aud", 0)
            + cost_summary.get("ongoing_annual_cowork_subscriptions_aud", 0))
    )
    saas_ongoing_scaled = cost_summary.get("ongoing_annual_scaled_aud", 0)
    saas_setup = cost_summary.get("total_setup_cost_aud", 0)
    saas_consultant = cost_summary.get("total_consultant_fees_aud", 0)
    saas_integration = cost_summary.get("integration_development_cost_aud", 0)
    saas_hidden = cost_summary.get("hidden_costs_annual_aud", 0)
    saas_training = cost_summary.get("training_cost_aud", 0)
    saas_admin_hours = cost_summary.get("total_ongoing_admin_hours", 0)
    saas_admin_annual = saas_admin_hours * blended_rate * 12

    # Custom/hybrid: training ~ equal to SaaS (one platform vs many tools, roughly same)
    custom_training = round(saas_training * 0.8)  # slightly less — one platform to learn
    # Custom/hybrid: admin overhead = SaaS / n_paid_tools (one tool to manage vs many)
    custom_admin_hours = round(saas_admin_hours / max(n_paid_tools, 1))
    custom_admin_annual = custom_admin_hours * blended_rate * 12

    saas_year1 = saas_ongoing_current + saas_setup + saas_consultant + saas_integration + saas_hidden + saas_training + saas_admin_annual
    saas_year2 = saas_ongoing_current + saas_hidden + saas_admin_annual
    saas_year3 = saas_ongoing_scaled + saas_hidden + saas_admin_annual
    saas_3yr = saas_year1 + saas_year2 + saas_year3

    # ── CUSTOM BUILD TCO ──
    total_build_internal = sum(r.get("build_cost_aud") or 0 for r in roi_items)
    n_sprints = max(1, math.ceil(total_build_internal / SPRINT_PRICE))
    custom_build_cost = n_sprints * SPRINT_PRICE
    custom_rd_offset = round(custom_build_cost * RD_OFFSET)
    custom_effective = custom_build_cost - custom_rd_offset

    custom_year1 = custom_build_cost + HOSTING_ANNUAL + custom_training + custom_admin_annual
    custom_year1_with_rd = custom_year1 - custom_rd_offset
    custom_year2 = HOSTING_ANNUAL + custom_admin_annual
    custom_year3 = HOSTING_ANNUAL + custom_admin_annual
    custom_3yr = custom_year1 + custom_year2 + custom_year3
    custom_3yr_with_rd = custom_year1_with_rd + custom_year2 + custom_year3

    # ── HYBRID TCO ── (Phase 1 = SaaS quick wins, Phase 2+3 = Custom)
    phase1_ids = set(phases[0]["change_ids"]) if phases else set()
    phase23_ids = set()
    for p in phases[1:]:
        phase23_ids.update(p.get("change_ids", []))

    hybrid_saas_annual = 0
    hybrid_saas_setup = 0
    hybrid_saas_admin_hrs = 0
    for ts in tool_selections:
        if ts["change_id"] in phase1_ids:
            hybrid_saas_annual += ts.get("annual_cost_aud", 0)
            hybrid_saas_setup += ts.get("setup_cost_aud", 0) + ts.get("consultant_fee_estimate_aud", 0)
            hybrid_saas_admin_hrs += ts.get("ongoing_admin_hours_monthly", 0)
    hybrid_saas_admin_annual = hybrid_saas_admin_hrs * blended_rate * 12

    hybrid_build_internal = sum(roi_by_change[cid].get("build_cost_aud", 0) for cid in phase23_ids if cid in roi_by_change)
    hybrid_n_sprints = max(1, math.ceil(hybrid_build_internal / SPRINT_PRICE))
    hybrid_build_cost = hybrid_n_sprints * SPRINT_PRICE
    hybrid_rd_offset = round(hybrid_build_cost * RD_OFFSET)

    hybrid_year1 = hybrid_saas_annual + hybrid_saas_setup + hybrid_saas_admin_annual + hybrid_build_cost + HOSTING_ANNUAL + custom_training + custom_admin_annual
    hybrid_year1_with_rd = hybrid_year1 - hybrid_rd_offset
    hybrid_year2 = hybrid_saas_annual + hybrid_saas_admin_annual + HOSTING_ANNUAL + custom_admin_annual
    hybrid_year3 = hybrid_saas_annual + hybrid_saas_admin_annual + HOSTING_ANNUAL + custom_admin_annual
    hybrid_3yr = hybrid_year1 + hybrid_year2 + hybrid_year3
    hybrid_3yr_with_rd = hybrid_year1_with_rd + hybrid_year2 + hybrid_year3

    # ── VALUE ──
    total_annual_value = blueprint.get("total_annual_value_aud", 0) or sum(
        c.get("value", {}).get("combined_annual_value_aud", 0) or 0 for c in changes)
    total_3yr_value = total_annual_value * 3
    monthly_value = total_annual_value / 12 if total_annual_value else 1

    saas_payback = round(saas_year1 / monthly_value, 1) if monthly_value else 0
    custom_payback = round(custom_year1_with_rd / monthly_value, 1) if monthly_value else 0
    hybrid_payback = round(hybrid_year1_with_rd / monthly_value, 1) if monthly_value else 0

    saas_net3 = total_3yr_value - saas_3yr
    custom_net3 = total_3yr_value - custom_3yr
    custom_net3_rd = total_3yr_value - custom_3yr_with_rd
    hybrid_net3 = total_3yr_value - hybrid_3yr
    hybrid_net3_rd = total_3yr_value - hybrid_3yr_with_rd

    # ── Years 4-5 (SaaS keeps scaling, Custom stays flat) ──
    # Year 4: SaaS at ~2.2x headcount (organic growth)
    saas_ongoing_y4 = round(saas_ongoing_scaled * 1.1)  # 10% beyond scaled
    saas_year4 = saas_ongoing_y4 + saas_hidden + saas_admin_annual
    custom_year4 = HOSTING_ANNUAL + custom_admin_annual
    hybrid_year4 = hybrid_saas_annual + hybrid_saas_admin_annual + HOSTING_ANNUAL + custom_admin_annual
    # Year 5: SaaS at ~2.5x (continued growth)
    saas_ongoing_y5 = round(saas_ongoing_scaled * 1.25)
    saas_year5 = saas_ongoing_y5 + saas_hidden + saas_admin_annual
    custom_year5 = HOSTING_ANNUAL + custom_admin_annual
    hybrid_year5 = hybrid_saas_annual + hybrid_saas_admin_annual + HOSTING_ANNUAL + custom_admin_annual

    saas_5yr = saas_3yr + saas_year4 + saas_year5
    custom_5yr = custom_3yr + custom_year4 + custom_year5
    custom_5yr_with_rd = custom_3yr_with_rd + custom_year4 + custom_year5
    hybrid_5yr = hybrid_3yr + hybrid_year4 + hybrid_year5
    hybrid_5yr_with_rd = hybrid_3yr_with_rd + hybrid_year4 + hybrid_year5

    total_5yr_value = total_annual_value * 5
    saas_net5 = total_5yr_value - saas_5yr
    custom_net5_rd = total_5yr_value - custom_5yr_with_rd
    hybrid_net5_rd = total_5yr_value - hybrid_5yr_with_rd

    # AI development velocity advantage estimate
    # Custom: new AI features ~$2,250/feature (15 hrs × ${YOUR_CHARGEOUT_RATE}/hr, one unified DB)
    # SaaS: new AI features ~$11,250/feature (75 hrs × ${YOUR_CHARGEOUT_RATE}/hr, integrating across N tools)
    # Conservative estimate: 4 AI features/year × difference = annual AI dev cost advantage
    ai_features_per_year = 4
    ai_cost_custom = 15 * 150 * ai_features_per_year  # $9,000/yr
    ai_cost_saas = 75 * 150 * ai_features_per_year    # $45,000/yr
    ai_advantage = ai_cost_saas - ai_cost_custom       # $36,000/yr

    # ── Determine recommendation ──
    best_net = max(saas_net5, custom_net5_rd, hybrid_net5_rd)
    if best_net == custom_net5_rd:
        rec_approach = "Custom Build"
        rec_reason = f"delivers the highest 5-year net return ({fmt_aud(custom_net5_rd)}) with no per-user scaling costs, a single unified platform, and full ownership of your data"
    elif best_net == hybrid_net5_rd:
        rec_approach = "Hybrid"
        rec_reason = f"balances quick SaaS wins with a custom core platform for the best 5-year return ({fmt_aud(hybrid_net5_rd)})"
    else:
        rec_approach = "SaaS Toolkit"
        rec_reason = f"offers the lowest upfront cost with a 5-year net return of {fmt_aud(saas_net5)}"

    # ── SECTION 1: Hero ──
    hero_html = f"""
    <div class="op-hero">
      <div class="op-hero-rec">OUR RECOMMENDATION</div>
      <h1 class="op-hero-title">The <span style="color:{BRAND_PRIMARY}">{rec_approach}</span> approach {rec_reason}.</h1>
      <div class="op-hero-stats">
        {_stat_box(fmt_aud(total_annual_value), "Annual value")}
        {_stat_box(str(len(changes)), "Improvements")}
        {_stat_box(f"{n_sprints} sprints", "Custom build")}
        {_stat_box(fmt_aud(custom_effective), "After R&D offset")}
      </div>
    </div>"""

    # ── SECTION 2: Aggregate cost comparison ──
    def _cost_row(label, saas_v, custom_v, hybrid_v, bold=False, highlight=False, note="", detail=""):
        tag = "strong" if bold else "span"
        bg = ' style="background:#F0FDF4"' if highlight else ""
        note_html = f'<div class="op-note">{note}</div>' if note else ""
        detail_html = ""
        if detail:
            detail_html = f'<details style="margin-top:4px"><summary style="font-size:11px;color:#94a3b8;cursor:pointer;user-select:none">▸ How this was calculated</summary><div style="font-size:11px;color:#64748b;padding:6px 0 2px 0;line-height:1.6">{detail}</div></details>'
        return f"""<tr{bg}>
            <td><{tag}>{label}</{tag}>{note_html}{detail_html}</td>
            <td class="op-num"><{tag}>{fmt_aud(saas_v)}</{tag}></td>
            <td class="op-num"><{tag}>{fmt_aud(custom_v)}</{tag}></td>
            <td class="op-num"><{tag}>{fmt_aud(hybrid_v)}</{tag}></td>
        </tr>"""

    # ── Build per-tool detail breakdowns for cost table dropdowns ──
    tool_deep_dives = strategy.get("tool_deep_dives", [])
    # Software subscriptions detail
    sub_lines = []
    saas_sub_total = cost_summary.get("ongoing_annual_saas_aud", 0)
    cowork_tools = cost_summary.get("ongoing_annual_cowork_tools_aud", 0)
    cowork_subs = cost_summary.get("ongoing_annual_cowork_subscriptions_aud", 0)
    for name, info in sorted(paid_tools.items(), key=lambda x: -x[1]["annual_cost"]):
        sub_lines.append(f"{escape(name)}: {fmt_aud(info['annual_cost'])}/yr")
    if cowork_tools:
        sub_lines.append(f"Cowork API/tool costs: {fmt_aud(cowork_tools)}/yr")
    if cowork_subs:
        sub_lines.append(f"Claude Team subscription: {fmt_aud(cowork_subs)}/yr")
    subs_detail = "<br>".join(sub_lines) if sub_lines else ""

    # Setup & consultant fees detail
    setup_lines = []
    for ts in tool_selections:
        s_cost = ts.get("setup_cost_aud", 0)
        c_cost = ts.get("consultant_fee_estimate_aud", 0)
        if s_cost or c_cost:
            tool_n = escape(ts.get("selected_tool", ts.get("change_id", "?")))
            parts = []
            if s_cost:
                parts.append(f"Setup: {fmt_aud(s_cost)}")
            if c_cost:
                c_hrs = ts.get("consultant_hours", 0)
                parts.append(f"Consultant: {fmt_aud(c_cost)}" + (f" (~{c_hrs} hrs)" if c_hrs else ""))
            timeline = ts.get("setup_timeline_weeks", 0)
            if timeline:
                parts.append(f"~{timeline} weeks")
            source = ts.get("setup_source", "")
            source_label = {"self_service": "self-service", "consultant": "specialist consultant", "vendor_onboarding": "vendor onboarding"}.get(source, "")
            notes = ts.get("setup_notes", "")
            setup_lines.append(f"<strong>{tool_n}</strong>: {' · '.join(parts)}" + (f" ({source_label})" if source_label else "") + (f"<br><span style='color:#94a3b8'>{escape(notes)}</span>" if notes else ""))
    setup_detail = "<br>".join(setup_lines) if setup_lines else ""

    # Integration development detail
    integ_detail = f"Estimated cost to build MCP connectors and API integrations between tools: {fmt_aud(saas_integration)}" if saas_integration else ""

    # Admin overhead detail — per-tool + cross-tool
    per_tool_hrs = cost_summary.get("per_tool_admin_hours_monthly", saas_admin_hours)
    cross_tool_hrs = cost_summary.get("cross_tool_admin_hours_monthly", 0)
    cross_tool_breakdown = cost_summary.get("cross_tool_admin_breakdown", {})

    admin_lines = ["<strong>Per-tool maintenance:</strong>"]
    for ts in tool_selections:
        a_hrs = ts.get("ongoing_admin_hours_monthly", 0)
        if a_hrs:
            tool_n = escape(ts.get("selected_tool", ts.get("change_id", "?")))
            admin_lines.append(f"&nbsp;&nbsp;{tool_n}: {a_hrs} hrs/mo")
    admin_lines.append(f"&nbsp;&nbsp;<em>Subtotal: {per_tool_hrs} hrs/mo</em>")

    if cross_tool_hrs:
        admin_lines.append(f"<br><strong>Cross-tool overhead ({n_paid_tools}+ tools stitched together):</strong>")
        for key, item in cross_tool_breakdown.items():
            hrs = item.get("hours_monthly", 0)
            desc = escape(item.get("description", ""))
            source = item.get("source", "")
            source_link = f' <a href="{escape(source)}" target="_blank" style="color:#7DFF00;font-size:10px">[source]</a>' if source else ""
            label = key.replace("_", " ").title()
            admin_lines.append(f"&nbsp;&nbsp;{label}: {hrs} hrs/mo — <span style='color:#94a3b8'>{desc}</span>{source_link}")
        admin_lines.append(f"&nbsp;&nbsp;<em>Subtotal: {cross_tool_hrs} hrs/mo</em>")

    admin_lines.append(f"<br><strong>Total: {saas_admin_hours} hrs/mo × ${blended_rate}/hr × 12 = {fmt_aud(saas_admin_annual)}/yr</strong>")
    admin_detail = "<br>".join(admin_lines)

    # Hidden costs detail
    hidden_lines = []
    hidden_notes = cost_summary.get("hidden_costs_notes", "")
    for tdd in tool_deep_dives:
        upsells = tdd.get("hidden_upsells", [])
        if upsells:
            hidden_lines.append(f"<strong>{escape(tdd.get('tool_name', ''))}</strong>: " + "; ".join(escape(u) for u in upsells[:2]))
    hidden_detail = "<br>".join(hidden_lines) + (f"<br><span style='color:#94a3b8'>{escape(hidden_notes)}</span>" if hidden_notes else "") if hidden_lines else ""

    # Training detail
    cowork_train = cost_summary.get("cowork_training_cost_aud", 0)
    saas_train = cost_summary.get("saas_training_cost_aud", 0)
    train_lines = []
    if cowork_train:
        train_lines.append(f"Cowork training programme: {fmt_aud(cowork_train)} (AI workflow training for 11 Cowork-delivered changes)")
    if saas_train:
        train_lines.append(f"SaaS tool training: {fmt_aud(saas_train)} ({n_paid_tools} paid tools × guided onboarding sessions)")
    train_lines.append(f"<strong>Total: {fmt_aud(saas_training)}</strong>")
    training_detail = "<br>".join(train_lines) if train_lines else ""

    comparison_html = f"""
    <div class="op-section">
      <h2 class="op-section-title">Cost Comparison: Three Approaches</h2>
      <p class="op-section-desc">All figures in AUD. SaaS costs include subscriptions, setup, consultants, and internal admin time. Custom build uses sprint-based pricing at $15,000 per 2-week sprint. All prices exclude GST.</p>
      <div class="op-table-wrap">
      <table class="op-table">
        <thead>
          <tr>
            <th style="text-align:left">Line Item</th>
            <th>SaaS Toolkit</th>
            <th>Custom Build</th>
            <th>Hybrid</th>
          </tr>
        </thead>
        <tbody>
          {_cost_row("Software subscriptions", saas_ongoing_current, 0, hybrid_saas_annual, detail=subs_detail)}
          {_cost_row("Setup &amp; consultant fees", saas_setup + saas_consultant, 0, hybrid_saas_setup, detail=setup_detail)}
          {_cost_row("Integration development", saas_integration, 0, 0, detail=integ_detail)}
          {_cost_row(f"Admin overhead", saas_admin_annual, custom_admin_annual, hybrid_saas_admin_annual + custom_admin_annual, note=f"SaaS: {saas_admin_hours} hrs/mo across {n_paid_tools} tools &middot; Custom: {custom_admin_hours} hrs/mo (1 platform) &middot; @ ${blended_rate}/hr", detail=admin_detail)}
          {_cost_row("Hidden costs (likely upsells)", saas_hidden, 0, 0, detail=hidden_detail)}
          {_cost_row("Training", saas_training, custom_training, custom_training, note="Custom: one platform to learn vs multiple tools", detail=training_detail)}
          {_cost_row(f"Build investment ({n_sprints} sprints)", 0, custom_build_cost, hybrid_build_cost)}
          {_cost_row("Platform hosting ($100/mo est.)", 0, HOSTING_ANNUAL, HOSTING_ANNUAL)}
          {_cost_row("Year 1 (before R&amp;D)", saas_year1, custom_year1, hybrid_year1, bold=True)}
          {_cost_row('R&amp;D Tax Offset (43.5%) <span class="op-rd-info" title="Hover for details">ℹ</span>', 0, -custom_rd_offset, -hybrid_rd_offset, note="Estimated reimbursement — may not apply to entire build. Check with your accountant.")}
          {_cost_row("Year 1 Effective Cost", saas_year1, custom_year1_with_rd, hybrid_year1_with_rd, bold=True, highlight=True)}
          <tr class="op-spacer"><td colspan="4"></td></tr>
          {_cost_row("Year 2 Ongoing", saas_year2, custom_year2, hybrid_year2, detail=f"SaaS: {fmt_aud(saas_ongoing_current)} subscriptions + {fmt_aud(saas_hidden)} hidden + {fmt_aud(saas_admin_annual)} admin<br>Custom: {fmt_aud(HOSTING_ANNUAL)} hosting + {fmt_aud(custom_admin_annual)} admin")}
          {_cost_row("Year 3 Ongoing (scaled)", saas_year3, custom_year3, hybrid_year3, note=f"SaaS scaled to {scaled_staff} staff &middot; Custom hosting stays flat", detail=f"SaaS subscriptions scale with headcount: {fmt_aud(saas_ongoing_scaled)}/yr at {scaled_staff} staff<br>Custom: {fmt_aud(HOSTING_ANNUAL)} hosting + {fmt_aud(custom_admin_annual)} admin — flat regardless of headcount")}
          {_cost_row("Year 4 Ongoing", saas_year4, custom_year4, hybrid_year4, detail=f"SaaS: {fmt_aud(saas_ongoing_y4)} subscriptions (projected growth) + {fmt_aud(saas_admin_annual)} admin<br>Custom: {fmt_aud(HOSTING_ANNUAL)} hosting + {fmt_aud(custom_admin_annual)} admin — still flat")}
          {_cost_row("Year 5 Ongoing", saas_year5, custom_year5, hybrid_year5, detail=f"SaaS: {fmt_aud(saas_ongoing_y5)} subscriptions (continued growth) + {fmt_aud(saas_admin_annual)} admin<br>Custom: {fmt_aud(HOSTING_ANNUAL)} hosting + {fmt_aud(custom_admin_annual)} admin — still flat")}
          <tr class="op-spacer"><td colspan="4"></td></tr>
          {_cost_row("5-Year Total (with R&amp;D offset)", saas_5yr, custom_5yr_with_rd, hybrid_5yr_with_rd, bold=True, highlight=True)}
          {_cost_row("5-Year Value Delivered", total_5yr_value, total_5yr_value, total_5yr_value)}
          {_cost_row("5-Year Net Position", saas_net5, custom_net5_rd, hybrid_net5_rd, bold=True, highlight=True)}
          {_cost_row("Payback Period", 0, 0, 0)}
          <tr class="op-spacer"><td colspan="4"></td></tr>
          {_cost_row("AI &amp; New Feature Development", ai_cost_saas, ai_cost_custom, ai_cost_custom, note="Estimated annual cost to build 4 new AI features / automations", detail=f"<strong>SaaS ({n_distinct_tools} tools):</strong> Each AI feature requires connecting to multiple APIs, handling different auth methods, reconciling data formats. ~75 hrs × ${YOUR_CHARGEOUT_RATE}/hr × {ai_features_per_year} features = {fmt_aud(ai_cost_saas)}/yr<br><br><strong>Custom (1 platform):</strong> AI reads directly from one unified database. No integration overhead, no API stitching. ~15 hrs × ${YOUR_CHARGEOUT_RATE}/hr × {ai_features_per_year} features = {fmt_aud(ai_cost_custom)}/yr<br><br><strong>Advantage: {fmt_aud(ai_advantage)}/yr saved</strong> — and this gap widens as AI becomes more central to operations. With a unified platform, AI can generate reports, flag compliance risks, and automate scheduling from a single data source. With {n_distinct_tools} separate tools, each AI feature is 5x harder to build and maintain.")}
        </tbody>
      </table>
      </div>
    </div>"""

    # Fix payback row to show months not dollars
    comparison_html = comparison_html.replace(
        f'<td class="op-num"><span>{fmt_aud(0)}</span></td>\n            <td class="op-num"><span>{fmt_aud(0)}</span></td>\n            <td class="op-num"><span>{fmt_aud(0)}</span></td>\n        </tr>\n        </tbody>',
        f'<td class="op-num"><span>{saas_payback} months</span></td>\n            <td class="op-num"><span>{custom_payback} months</span></td>\n            <td class="op-num"><span>{hybrid_payback} months</span></td>\n        </tr>\n        </tbody>'
    )

    # ── SECTION 2b: Your SaaS Toolkit (what the tools actually are) ──
    # Stage label lookup for toolkit descriptions
    stage_labels, _ = _build_stage_lookups(ssad)

    def _tool_row(name, info):
        cost = info["annual_cost"]
        cids = info["change_ids"]
        cat = info["category"]
        cat_badge = {"paid": ("PAID", "#EF4444", "#FEE2E2"),
                     "free": ("FREE", "#10B981", "#D1FAE5"),
                     "custom_api": ("CUSTOM", "#3B82F6", "#DBEAFE"),
                     "bundled": ("PAID", "#EF4444", "#FEE2E2")}.get(cat, ("", BRAND_GREY, "#F1F5F9"))
        cost_str = fmt_aud(cost) + "/yr" if cost > 0 else "Free"

        # Build descriptive "covers" from change titles, grouped by stage
        covers_parts = []
        for cid in cids:
            ch = changes_by_id.get(cid, {})
            title = ch.get("title", cid)
            # Shorten long titles to key phrase
            short = title.split(" with ")[0].split(" for ")[0].split(" from ")[0]
            if len(short) > 60:
                short = short[:57] + "..."
            stage = ch.get("stage", "")
            stage_lbl = _stage_label(stage, stage_labels) if stage else ""
            covers_parts.append((stage_lbl, short, cid))

        # Group by stage for cleaner display
        by_stage = {}
        for stage_lbl, short, cid in covers_parts:
            by_stage.setdefault(stage_lbl, []).append(short)

        covers_html = ""
        for stage_lbl, titles in by_stage.items():
            stage_tag = f'<span style="color:{BRAND_GREY};font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.04em">{escape(stage_lbl)}</span> ' if stage_lbl else ""
            items = "; ".join(escape(t) for t in titles)
            covers_html += f'<div style="margin-bottom:2px">{stage_tag}{items}</div>'

        return f"""<tr>
            <td><strong>{escape(name)}</strong></td>
            <td><span class="so-badge" style="background:{cat_badge[2]};color:{cat_badge[1]}">{cat_badge[0]}</span></td>
            <td class="op-num">{cost_str}</td>
            <td>{covers_html}</td>
        </tr>"""

    toolkit_rows = ""
    total_saas_toolkit_cost = 0
    # Show paid/bundled first, then custom API, then free
    for category_group in [paid_tools, bundled_tools, custom_api_tools, free_tools]:
        for name, info in sorted(category_group.items(), key=lambda x: -x[1]["annual_cost"]):
            toolkit_rows += _tool_row(name, info)
            total_saas_toolkit_cost += info["annual_cost"]

    toolkit_html = f"""
    <div class="op-section">
      <h2 class="op-section-title">The SaaS Toolkit: What You'd Actually Use</h2>
      <p class="op-section-desc">If you went the SaaS route, here are the {n_distinct_tools} tools we'd recommend — {n_paid_tools} paid subscriptions, {n_free_tools} free tools you already have, and {len(custom_api_tools)} custom API integrations.</p>
      <div class="op-table-wrap">
      <table class="op-table">
        <thead><tr><th style="text-align:left">Tool</th><th>Type</th><th>Annual Cost</th><th style="text-align:left">Covers</th></tr></thead>
        <tbody>{toolkit_rows}</tbody>
        <tfoot><tr style="background:#F8FAFC"><td colspan="2"><strong>Total SaaS subscriptions</strong></td><td class="op-num"><strong>{fmt_aud(saas_ongoing_current)}/yr</strong></td><td></td></tr></tfoot>
      </table>
      </div>
    </div>"""

    # ── Extract hidden upsells from tool deep dives ──
    upsell_items_html = ""
    for tdd in tool_deep_dives:
        tool_name = tdd.get("tool_name", "")
        upsells = tdd.get("hidden_upsells", [])
        if upsells:
            upsell_list = "".join(f"<li style='margin:2px 0;font-size:12px'>{escape(u)}</li>" for u in upsells)
            upsell_items_html += f'<div style="margin-bottom:10px"><strong style="font-size:13px">{escape(tool_name)}</strong><ul style="margin:4px 0 0 16px;padding:0">{upsell_list}</ul></div>'
    upsell_card = ""
    if upsell_items_html:
        upsell_card = f"""
        <div class="op-hidden-card" style="grid-column: 1 / -1">
          <div class="op-hidden-icon">💰</div>
          <div class="op-hidden-label">Likely Upsells &amp; Price Traps</div>
          <div class="op-hidden-detail">{upsell_items_html}
            <span class="op-note">These are real risks identified through vendor research — not hypothetical</span></div>
        </div>"""

    # ── SECTION 3: Hidden cost of SaaS ──
    hidden_html = f"""
    <div class="op-section op-hidden-section">
      <h2 class="op-section-title">The True Cost of SaaS</h2>
      <p class="op-section-desc">SaaS subscription fees are only part of the picture. Here's what most quotes don't show you.</p>
      <div class="op-hidden-grid">
        <div class="op-hidden-card">
          <div class="op-hidden-icon">👥</div>
          <div class="op-hidden-label">Per-User Scaling</div>
          <div class="op-hidden-detail">At {current_staff} staff: <strong>{fmt_aud(saas_ongoing_current)}/yr</strong><br>
            At {scaled_staff} staff: <strong>{fmt_aud(saas_ongoing_scaled)}/yr</strong><br>
            <span class="op-note">Every new hire increases your software bill</span></div>
        </div>
        <div class="op-hidden-card">
          <div class="op-hidden-icon">🔧</div>
          <div class="op-hidden-label">Consultant &amp; Setup Fees</div>
          <div class="op-hidden-detail">Someone has to configure {n_paid_tools} paid tools: <strong>{fmt_aud(saas_consultant + saas_setup)}</strong><br>
            <span class="op-note">If you're not paying a custom builder, you're paying a consultant — or spending your own time</span></div>
        </div>
        <div class="op-hidden-card">
          <div class="op-hidden-icon">⏱️</div>
          <div class="op-hidden-label">Internal Admin Overhead</div>
          <div class="op-hidden-detail">{saas_admin_hours} hrs/month managing tools: <strong>{fmt_aud(saas_admin_annual)}/yr</strong><br>
            <span class="op-note">Your team's time has a cost — {saas_admin_hours} hours/month &times; ${blended_rate}/hr &times; 12 months</span></div>
        </div>
        <div class="op-hidden-card">
          <div class="op-hidden-icon">🔗</div>
          <div class="op-hidden-label">Data Silos &amp; Fragmentation</div>
          <div class="op-hidden-detail">{n_distinct_tools} separate tools, no shared data<br>
            <span class="op-note">Copy-paste between systems, no unified reporting, no AI across your data</span></div>
        </div>
        {upsell_card}
      </div>
      <div class="op-hidden-compare">
        <strong>Compare with Custom Build:</strong> One platform, {fmt_aud(HOSTING_ANNUAL)}/yr hosting, no per-user fees, no consultant fees after build, all data in one place.
      </div>
    </div>"""

    # ── SECTION 3b: SaaS vs Custom — The Bigger Picture ──
    bigger_picture_html = f"""
    <div class="op-section" style="margin-top:32px">
      <h2 class="op-section-title">SaaS vs Custom Build: The Bigger Picture</h2>
      <p class="op-section-desc">Beyond the numbers above, here's why the choice between SaaS and custom matters more than ever.</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px">
        <div style="background:#1E293B;border-radius:12px;padding:24px;border:1px solid #334155">
          <div style="font-size:15px;font-weight:700;color:#F8FAFC;margin-bottom:12px">📦 The SaaS Approach</div>
          <div style="font-size:12px;color:#94a3b8;margin-bottom:12px">Best when: the tool has exclusive data access (e.g., accounting, banking), or the vendor invests heavily in compliance certifications you'd struggle to replicate.</div>
          <div style="font-size:13px;font-weight:600;color:#4ADE80;margin-bottom:6px">Strengths</div>
          <ul style="font-size:12px;color:#CBD5E1;margin:0 0 12px 16px;padding:0;line-height:1.7">
            <li>Fast to start — sign up and go</li>
            <li>Vendor handles security patches &amp; infrastructure</li>
            <li>Established user communities and support</li>
            <li>Ideal for regulated domains (accounting, payroll, banking)</li>
          </ul>
          <div style="font-size:13px;font-weight:600;color:#F87171;margin-bottom:6px">The Reality</div>
          <ul style="font-size:12px;color:#CBD5E1;margin:0 0 0 16px;padding:0;line-height:1.7">
            <li><strong>{n_distinct_tools} separate logins</strong> — each one is a security surface</li>
            <li><strong>Your data lives in their servers</strong> — some tools restrict export or charge for API access</li>
            <li>Every tool is built on a different tech stack by a different team — you're at the mercy of their roadmap</li>
            <li>Configuring a generic tool to fit your processes can cost as much — or more — than building your own</li>
            <li>Per-user pricing means your software bill grows with every hire</li>
            <li><strong>AI across silos is 10x harder</strong> — building AI that connects to {n_distinct_tools} separate tools with different APIs, auth, and data formats is an order of magnitude more work than AI on one unified database</li>
          </ul>
        </div>
        <div style="background:#1E293B;border-radius:12px;padding:24px;border:1px solid #7DFF00">
          <div style="font-size:15px;font-weight:700;color:#F8FAFC;margin-bottom:12px">🔧 The Custom Build Approach</div>
          <div style="font-size:12px;color:#94a3b8;margin-bottom:12px">Best when: your processes are unique, you need tools to talk to each other, or you want AI working across your entire business.</div>
          <div style="font-size:13px;font-weight:600;color:#4ADE80;margin-bottom:6px">Strengths</div>
          <ul style="font-size:12px;color:#CBD5E1;margin:0 0 12px 16px;padding:0;line-height:1.7">
            <li><strong>One login, one database</strong> — all your data in one place, fully under your control</li>
            <li>No per-user fees — same cost whether you have 10 or 200 staff</li>
            <li>Built exactly for your workflows — not bent to fit a generic tool</li>
            <li><strong>AI-ready from day one</strong> — with all data unified, AI can generate reports, flag risks, and automate tasks across your entire operation</li>
            <li>You own the code — no vendor lock-in, no forced migrations, no surprise price increases</li>
          </ul>
          <div style="font-size:13px;font-weight:600;color:#FBBF24;margin-bottom:6px">Considerations</div>
          <ul style="font-size:12px;color:#CBD5E1;margin:0 0 0 16px;padding:0;line-height:1.7">
            <li>Upfront build investment (offset by R&amp;D tax incentive at 43.5%)</li>
            <li>Requires a development partner for ongoing maintenance</li>
            <li>Not suitable for domains where vendor certifications matter (e.g., Xero for accounting — we keep that)</li>
          </ul>
        </div>
      </div>
      <div style="background:#0F172A;border:1px solid #334155;border-radius:12px;padding:20px;margin-top:20px">
        <div style="font-size:14px;font-weight:700;color:#7DFF00;margin-bottom:8px">🤖 Why this is changing fast</div>
        <p style="font-size:12px;color:#CBD5E1;line-height:1.7;margin:0">
          AI has fundamentally shifted the economics of custom software. What took a team of developers months to build 3 years ago can now be built in weeks. Maintaining custom code — once the biggest risk — is becoming trivial as AI handles bug fixes, updates, and feature additions. The trajectory is clear: <strong>the cost to build and maintain custom software is dropping rapidly, while SaaS subscription costs only go up.</strong>
          <br><br>
          More importantly, the real value of AI isn't in any single tool — it's in connecting your data. When your participant records, scheduling, compliance, invoicing, and communications all live in one system, AI can do things no collection of SaaS tools can: generate progress reports from case notes, flag funding exhaustion before it happens, auto-schedule based on your actual business rules, and surface insights across your entire operation. <strong>That only works when your data isn't locked in {n_distinct_tools} separate vendor silos.</strong>
        </p>
      </div>
    </div>"""

    # ── SECTION 4: 3-Year TCO Chart (inline SVG) ──
    chart_w, chart_h = 700, 300
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 50
    plot_w = chart_w - pad_l - pad_r
    plot_h = chart_h - pad_t - pad_b

    # Build monthly cumulative data points
    def _monthly_cumulative(y1, y2, y3):
        points = []
        m1 = y1 / 12
        m2 = y2 / 12
        m3 = y3 / 12
        cumulative = 0
        for m in range(37):
            if m > 0:
                if m <= 12:
                    cumulative += m1
                elif m <= 24:
                    cumulative += m2
                else:
                    cumulative += m3
            points.append(cumulative)
        return points

    saas_pts = _monthly_cumulative(saas_year1, saas_year2, saas_year3)
    custom_pts = _monthly_cumulative(custom_year1_with_rd, custom_year2, custom_year3)
    hybrid_pts = _monthly_cumulative(hybrid_year1_with_rd, hybrid_year2, hybrid_year3)
    value_pts = [total_annual_value / 12 * m for m in range(37)]

    all_vals = saas_pts + custom_pts + hybrid_pts + value_pts
    max_val = max(all_vals) if all_vals else 1

    def _to_svg(pts, color, dash=""):
        coords = []
        for i, v in enumerate(pts):
            x = pad_l + (i / 36) * plot_w
            y = pad_t + plot_h - (v / max_val) * plot_h
            coords.append(f"{x:.1f},{y:.1f}")
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{" ".join(coords)}" fill="none" stroke="{color}" stroke-width="2.5"{dash_attr}/>'

    # Y-axis labels
    y_labels = ""
    for i in range(5):
        val = max_val * i / 4
        y = pad_t + plot_h - (i / 4) * plot_h
        y_labels += f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-size="10" fill="{BRAND_GREY}">${val / 1000:.0f}k</text>'
        y_labels += f'<line x1="{pad_l}" y1="{y}" x2="{pad_l + plot_w}" y2="{y}" stroke="{BRAND_BORDER}" stroke-width="0.5"/>'

    # X-axis labels
    x_labels = ""
    for m in [0, 6, 12, 18, 24, 30, 36]:
        x = pad_l + (m / 36) * plot_w
        x_labels += f'<text x="{x}" y="{pad_t + plot_h + 20}" text-anchor="middle" font-size="10" fill="{BRAND_GREY}">M{m}</text>'

    chart_html = f"""
    <div class="op-section">
      <h2 class="op-section-title">3-Year Total Cost of Ownership</h2>
      <p class="op-section-desc">Cumulative cost over 36 months. The green dashed line shows cumulative value delivered — where lines cross is your break-even point.</p>
      <div class="op-chart-wrap">
      <svg viewBox="0 0 {chart_w} {chart_h}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{chart_w}px;height:auto">
        {y_labels}
        {x_labels}
        {_to_svg(value_pts, "#10B981", "6 3")}
        {_to_svg(saas_pts, "#EF4444")}
        {_to_svg(custom_pts, "#3B82F6")}
        {_to_svg(hybrid_pts, "#8B5CF6")}
      </svg>
      </div>
      <div class="op-chart-legend">
        <span class="op-legend-item"><span class="op-legend-dot" style="background:#EF4444"></span> SaaS Toolkit</span>
        <span class="op-legend-item"><span class="op-legend-dot" style="background:#3B82F6"></span> Custom Build</span>
        <span class="op-legend-item"><span class="op-legend-dot" style="background:#8B5CF6"></span> Hybrid</span>
        <span class="op-legend-item"><span class="op-legend-dot" style="background:#10B981;border-radius:0;height:2px;width:16px;border-top:2px dashed #10B981;background:none"></span> Value Delivered</span>
      </div>
    </div>"""

    # ── SECTION 4b: Your Options — Hormozi-style tiered offer ──
    # Calculate quick win data from phase 1
    qw_phase = phases[0] if phases else {}
    qw_cids = qw_phase.get("change_ids", [])
    qw_value = sum(changes_by_id.get(cid, {}).get("value", {}).get("combined_annual_value_aud", 0) for cid in qw_cids)
    qw_monthly = round(qw_value / 12)
    qw_count = len(qw_cids)
    # Quick wins package price: Complex ($6,500) if >4 changes, Standard ($3,800) if ≤4
    qw_price = 6500 if qw_count > 4 else 3800
    qw_items = []
    for cid in qw_cids:
        c = changes_by_id.get(cid, {})
        qw_items.append(escape(c.get("title", cid)[:65]))

    # SaaS full implementation
    saas_monthly_guarantee = round(total_annual_value / 12)

    # Custom build
    custom_monthly_guarantee = saas_monthly_guarantee  # same value delivered

    # ROI multipliers
    qw_roi = round(qw_value / max(qw_price, 1), 1)
    saas_roi = round(total_annual_value / max(saas_year1, 1), 1)
    custom_roi = round(total_annual_value / max(custom_year1_with_rd, 1), 1)

    qw_list_html = "".join(f"<li>{item}</li>" for item in qw_items)

    options_html = f"""
    <div class="op-section" style="margin-top:32px">
      <h2 class="op-section-title">Your Options</h2>
      <p class="op-section-desc">Three ways to move forward — each with a guarantee. Start small and scale, or go all-in from day one. <strong>Every dollar you spend on a smaller package is credited if you upgrade.</strong></p>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px">

        <!-- Tier 1: Quick Wins -->
        <div style="background:#1E293B;border-radius:14px;padding:24px;border:1px solid #334155;display:flex;flex-direction:column">
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;margin-bottom:4px">Start Here</div>
          <div style="font-size:18px;font-weight:800;color:#F8FAFC;margin-bottom:4px">Quick Wins</div>
          <div style="font-size:28px;font-weight:800;color:#7DFF00;margin-bottom:2px">{fmt_aud(qw_price)}</div>
          <div style="font-size:11px;color:#94a3b8;margin-bottom:16px">One-time · {qw_count} improvements · 2-3 weeks</div>
          <div style="font-size:12px;color:#CBD5E1;margin-bottom:12px">We implement the {qw_count} standalone quick wins that deliver immediate value with no dependencies:</div>
          <ul style="font-size:11px;color:#CBD5E1;margin:0 0 16px 14px;padding:0;line-height:1.7;flex-grow:1">{qw_list_html}</ul>
          <div style="background:rgba(125,255,0,0.08);border:1px solid rgba(125,255,0,0.2);border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:11px;font-weight:700;color:#7DFF00;margin-bottom:2px">💰 {fmt_aud(qw_value)}/yr value unlocked</div>
            <div style="font-size:11px;color:#94a3b8">{qw_roi}x return on investment</div>
          </div>
          <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:11px;font-weight:600;color:#4ADE80">✓ 90-day guarantee</div>
            <div style="font-size:10px;color:#94a3b8">If quick wins don't save {fmt_aud(qw_monthly)}/mo within 90 days, we refund the difference</div>
          </div>
          <div style="font-size:10px;color:#64748b;text-align:center">100% credited if you upgrade</div>
        </div>

        <!-- Tier 2: Full SaaS Implementation -->
        <div style="background:#1E293B;border-radius:14px;padding:24px;border:1px solid #334155;display:flex;flex-direction:column">
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#94a3b8;margin-bottom:4px">Most Comprehensive</div>
          <div style="font-size:18px;font-weight:800;color:#F8FAFC;margin-bottom:4px">SaaS Toolkit</div>
          <div style="font-size:28px;font-weight:800;color:#F8FAFC;margin-bottom:2px">{fmt_aud(saas_year1)}<span style="font-size:13px;color:#94a3b8">/yr1</span></div>
          <div style="font-size:11px;color:#94a3b8;margin-bottom:16px">All {len(changes)} improvements · {n_distinct_tools} tools · 8 weeks</div>
          <div style="font-size:12px;color:#CBD5E1;margin-bottom:12px;flex-grow:1">Everything in Quick Wins, plus the full recommended SaaS toolkit with Cowork AI training — all {len(changes)} improvements across every process. Includes tool configuration, integrations, and team training.
            <br><br><span style="color:#FBBF24;font-size:11px">⚠ Ongoing: {fmt_aud(saas_ongoing_current)}/yr in subscriptions + {fmt_aud(saas_admin_annual)}/yr admin overhead ({saas_admin_hours} hrs/mo)</span>
          </div>
          <div style="background:rgba(125,255,0,0.08);border:1px solid rgba(125,255,0,0.2);border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:11px;font-weight:700;color:#7DFF00;margin-bottom:2px">💰 {fmt_aud(total_annual_value)}/yr value unlocked</div>
            <div style="font-size:11px;color:#94a3b8">{saas_roi}x return in year 1</div>
          </div>
          <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:11px;font-weight:600;color:#4ADE80">✓ 90-day ROI guarantee</div>
            <div style="font-size:10px;color:#94a3b8">If you don't see {fmt_aud(saas_monthly_guarantee)}/mo in savings within 90 days, we refund implementation fees</div>
          </div>
          <div style="font-size:10px;color:#64748b;text-align:center">Implementation fees credited toward Custom upgrade</div>
        </div>

        <!-- Tier 3: Custom Platform -->
        <div style="background:#1E293B;border-radius:14px;padding:24px;border:2px solid #7DFF00;display:flex;flex-direction:column;position:relative">
          <div style="position:absolute;top:-12px;right:16px;background:#7DFF00;color:#0F172A;font-size:10px;font-weight:800;padding:4px 12px;border-radius:20px;text-transform:uppercase;letter-spacing:0.05em">Best 3-Year Value</div>
          <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#7DFF00;margin-bottom:4px">Recommended</div>
          <div style="font-size:18px;font-weight:800;color:#F8FAFC;margin-bottom:4px">Custom Platform</div>
          <div style="font-size:28px;font-weight:800;color:#F8FAFC;margin-bottom:2px">{fmt_aud(custom_year1)}</div>
          <div style="font-size:12px;color:#4ADE80;margin-bottom:2px">Potential R&amp;D offset: {fmt_aud(custom_year1_with_rd)} <span style="color:#94a3b8">(if eligible — not guaranteed)</span></div>
          <div style="font-size:11px;color:#94a3b8;margin-bottom:16px">All {len(changes)} improvements · 1 platform · {n_sprints} sprints · You own everything</div>
          <div style="font-size:12px;color:#CBD5E1;margin-bottom:12px;flex-grow:1">One unified platform built for your exact processes. No per-user fees, no vendor lock-in, AI-ready from day one. Replaces {n_distinct_tools} separate tools with a single login.
            <br><br><span style="color:#4ADE80;font-size:11px">✓ Flat ongoing: {fmt_aud(HOSTING_ANNUAL)}/yr hosting · No per-user scaling · R&amp;D tax offset reduces build from {fmt_aud(custom_build_cost)} to ~{fmt_aud(custom_build_cost - custom_rd_offset)}</span>
          </div>
          <div style="background:rgba(125,255,0,0.08);border:1px solid rgba(125,255,0,0.2);border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:11px;font-weight:700;color:#7DFF00;margin-bottom:2px">💰 {fmt_aud(total_annual_value)}/yr value unlocked</div>
            <div style="font-size:11px;color:#94a3b8">{custom_roi}x return in year 1 (after R&amp;D offset)</div>
          </div>
          <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:10px;margin-bottom:12px">
            <div style="font-size:11px;font-weight:600;color:#4ADE80">✓ 90-day ROI guarantee</div>
            <div style="font-size:10px;color:#94a3b8">Covering first 3 sprints. Own everything — code, data, infrastructure. Prototype-first: see it before you commit.</div>
          </div>
          <div style="font-size:10px;color:#7DFF00;text-align:center;font-weight:600">5-year net return: {fmt_aud(custom_net5_rd)}</div>
        </div>

      </div>
      <div style="text-align:center;margin-top:16px;font-size:12px;color:#64748b">
        Not sure which option? Start with Quick Wins — prove the value, then decide. Every dollar spent is credited toward an upgrade.
      </div>
    </div>"""

    # ── SECTION 5: Module-by-module breakdown with pros/cons ──
    modules_html = ""
    for phase in phases:
        p_num = phase.get("phase_number", 0)
        p_label = escape(phase.get("label", f"Phase {p_num}"))
        p_time = escape(phase.get("timeframe", ""))
        p_desc = escape(phase.get("description", ""))
        p_val = phase.get("total_annual_value_aud", 0)
        cids = phase.get("change_ids", [])

        # Phase header
        modules_html += f"""
        <div class="op-phase">
          <div class="op-phase-header">
            <div class="op-phase-num">Phase {p_num}</div>
            <div class="op-phase-info">
              <div class="op-phase-label">{p_label}</div>
              <div class="op-phase-meta">{p_time} &middot; {len(cids)} changes &middot; {fmt_aud(p_val)}/yr value</div>
              <div class="op-phase-desc">{p_desc}</div>
            </div>
          </div>"""

        # Per-change comparison cards
        for cid in cids:
            ch = changes_by_id.get(cid, {})
            roi = roi_by_change.get(cid, {})
            ts = ts_by_change.get(cid, {})
            title = escape(ch.get("title", cid))
            change_type = ch.get("change_type", "")
            badge_label, badge_color, badge_bg = CHANGE_BADGE.get(change_type, ("OTHER", BRAND_GREY, "#F1F5F9"))

            # SaaS data
            saas_tool = escape(ts.get("selected_tool", "—"))
            saas_annual = ts.get("annual_cost_aud", 0)
            saas_setup_cost = ts.get("setup_cost_aud", 0)
            saas_consult_cost = ts.get("consultant_fee_estimate_aud", 0)
            saas_setup_c = saas_setup_cost + saas_consult_cost
            saas_admin_hrs_m = ts.get("ongoing_admin_hours_monthly", 0)
            saas_admin_c = saas_admin_hrs_m * blended_rate * 12
            saas_setup_weeks = ts.get("setup_timeline_weeks", 0)
            saas_total_yr1 = saas_annual + saas_setup_c + saas_admin_c
            saas_ongoing_c = saas_annual + saas_admin_c

            # Custom data
            build_cost = roi.get("build_cost_aud", 0)
            value_obj = ch.get("value", {})
            annual_val = value_obj.get("combined_annual_value_aud", 0) or 0
            formula_summary = value_obj.get("formula_summary", "")
            time_formula = (value_obj.get("time_saving") or {}).get("formula", "")
            prod_formula = (value_obj.get("productivity_enhancement") or {}).get("formula", "")
            payback_m = roi.get("payback_months", 0)
            payback_tag = roi.get("payback_tag", "")
            qw_badge = '<span class="op-qw-badge">QUICK WIN</span>' if payback_tag == "QUICK_WIN" else ""

            # Pros/cons for SaaS
            saas_pros = []
            saas_cons = []
            if ts.get("why_this_tool"):
                # Extract key benefit
                saas_pros.append("Vendor-supported with existing user community")
            if ts.get("configuration_steps"):
                saas_pros.append(f"{len(ts['configuration_steps'])} configuration steps to go live")
            saas_caveats = ts.get("caveats", [])
            for cav in saas_caveats[:3]:
                saas_cons.append(str(cav)[:120])
            if ts.get("per_user_monthly_aud", 0) > 0:
                saas_cons.append(f"Per-user pricing scales with headcount")
            if ts.get("data_silo_risk", ""):
                saas_cons.append("Data silo — separate system from your other tools")

            # Pros/cons for Custom
            custom_pros = ["No per-user fees — scales to any team size",
                           "Unified with all other modules — shared data, single login",
                           "Built exactly for your processes — not generic workflows"]
            custom_cons = ["Upfront build investment required",
                           "Ongoing maintenance retainer recommended"]

            saas_pros_html = "".join(f"<li>{escape(p)}</li>" for p in saas_pros)
            saas_cons_html = "".join(f"<li>{escape(c2)}</li>" for c2 in saas_cons)
            custom_pros_html = "".join(f"<li>{escape(p)}</li>" for p in custom_pros)
            custom_cons_html = "".join(f"<li>{escape(c2)}</li>" for c2 in custom_cons)

            modules_html += f"""
          <div class="op-change-card" id="card-{escape(cid)}">
            <div class="op-change-header">
              <span class="so-badge" style="background:{badge_bg};color:{badge_color}">{badge_label}</span>
              {qw_badge}
              <span class="op-change-id">{escape(cid)}</span>
            </div>
            <div class="op-change-title">{title}</div>
            <div class="op-change-value">Annual value: <strong>{fmt_aud(annual_val)}/yr</strong>
              {'<div style="font-size:12px;color:#64748b;margin-top:2px">' + escape(formula_summary) + '</div>' if formula_summary else ''}
              {'<details style="margin-top:4px"><summary style="font-size:11px;color:#94a3b8;cursor:pointer">Show calculation</summary><div style="font-size:11px;color:#64748b;padding:4px 0">' + ('<div>' + escape(time_formula) + '</div>' if time_formula else '') + ('<div>' + escape(prod_formula) + '</div>' if prod_formula else '') + '</div></details>' if (time_formula or prod_formula) else ''}
            </div>
            <details class="op-compare-toggle">
              <summary class="op-compare-summary">
                <span class="op-compare-arrow">&#x25B6;</span> Compare SaaS vs Custom Build
                <span class="op-compare-hint">SaaS {fmt_aud(saas_total_yr1)} yr1 &middot; Custom {fmt_aud(build_cost)} build</span>
              </summary>
              <div class="op-compare-grid">
                <div class="op-compare-col op-compare-saas">
                  <div class="op-compare-heading">SaaS: {saas_tool}</div>
                  <div class="op-compare-cost">Year 1: <strong>{fmt_aud(saas_total_yr1)}</strong></div>
                  {'<div style="font-size:11px;color:#64748b;margin:-2px 0 4px 0">' + ' + '.join(filter(None, [f"Subscription: {fmt_aud(saas_annual)}/yr" if saas_annual else "", f"Setup: {fmt_aud(saas_setup_cost)}" if saas_setup_cost else "", f"Consultant: {fmt_aud(saas_consult_cost)}" if saas_consult_cost else "", f"Admin: {fmt_aud(saas_admin_c)}/yr" if saas_admin_c else ""])) + '</div>' if (saas_setup_cost or saas_consult_cost or saas_admin_c) else ''}
                  <div class="op-compare-cost">Ongoing: {fmt_aud(saas_ongoing_c)}/yr</div>
                  {'<div style="font-size:11px;color:#64748b;margin:-2px 0 4px 0">' + f"{saas_admin_hrs_m} hrs/mo admin × ${blended_rate}/hr × 12" + ('  ·  Setup: ~' + str(saas_setup_weeks) + ' weeks' if saas_setup_weeks else '') + '</div>' if saas_admin_hrs_m else ''}
                  <div class="op-compare-proscons">
                    <div class="so-pc-label so-pro-label">Pros</div>
                    <ul>{saas_pros_html}</ul>
                    <div class="so-pc-label so-con-label" style="margin-top:8px">Cons</div>
                    <ul>{saas_cons_html}</ul>
                  </div>
                </div>
                <div class="op-compare-col op-compare-custom">
                  <div class="op-compare-heading">Custom Build</div>
                  <div class="op-compare-cost">Build: <strong>{fmt_aud(build_cost)}</strong></div>
                  <div class="op-compare-cost">Ongoing: Included in platform hosting</div>
                  <div class="op-compare-proscons">
                    <div class="so-pc-label so-pro-label">Pros</div>
                    <ul>{custom_pros_html}</ul>
                    <div class="so-pc-label so-con-label" style="margin-top:8px">Cons</div>
                    <ul>{custom_cons_html}</ul>
                  </div>
                </div>
              </div>
            </details>
          </div>"""

        # Phase subtotals
        phase_saas_yr1 = sum(
            (ts_by_change.get(cid, {}).get("annual_cost_aud", 0)
             + ts_by_change.get(cid, {}).get("setup_cost_aud", 0)
             + ts_by_change.get(cid, {}).get("consultant_fee_estimate_aud", 0)
             + ts_by_change.get(cid, {}).get("ongoing_admin_hours_monthly", 0) * blended_rate * 12)
            for cid in cids)
        phase_custom_build = sum(roi_by_change.get(cid, {}).get("build_cost_aud", 0) for cid in cids)
        modules_html += f"""
          <div class="op-phase-totals">
            <div>Phase {p_num} totals:</div>
            <div>SaaS Year 1: <strong>{fmt_aud(phase_saas_yr1)}</strong></div>
            <div>Custom Build: <strong>{fmt_aud(phase_custom_build)}</strong></div>
            <div>Annual Value: <strong>{fmt_aud(p_val)}</strong></div>
          </div>
        </div>"""

    # ── SECTION 6: Implementation Timeline (Gantt) ──
    gantt_w, gantt_h = 700, 40 + len(phases) * 60 + 20
    total_duration = blueprint.get("estimated_total_duration_weeks", 11) or 11
    gantt_pad_l = 130

    gantt_bars = ""
    gantt_y = 40
    phase_colors = ["#10B981", "#3B82F6", "#8B5CF6"]
    for i, phase in enumerate(phases):
        p_label = escape(phase.get("label", f"Phase {phase.get('phase_number', i+1)}"))
        p_timeframe = phase.get("timeframe", "")
        # Parse week range from timeframe like "Weeks 1-3"
        week_nums = re.findall(r'\d+', p_timeframe)
        if len(week_nums) >= 2:
            w_start, w_end = int(week_nums[0]), int(week_nums[1])
        elif len(week_nums) == 1:
            w_start = int(week_nums[0])
            w_end = w_start + phase.get("effective_duration_weeks", 2) - 1
        else:
            w_start, w_end = 1, 2

        bar_x = gantt_pad_l + ((w_start - 1) / total_duration) * (gantt_w - gantt_pad_l - 20)
        bar_w = max(30, ((w_end - w_start + 1) / total_duration) * (gantt_w - gantt_pad_l - 20))
        color = phase_colors[i % len(phase_colors)]
        p_val = phase.get("total_annual_value_aud", 0)

        gantt_bars += f"""
        <text x="5" y="{gantt_y + 16}" font-size="11" font-weight="600" fill="{BRAND_DARK}">{p_label}</text>
        <text x="5" y="{gantt_y + 32}" font-size="9" fill="{BRAND_GREY}">{escape(p_timeframe)}</text>
        <rect x="{bar_x:.0f}" y="{gantt_y}" width="{bar_w:.0f}" height="36" rx="6" fill="{color}" opacity="0.15"/>
        <rect x="{bar_x:.0f}" y="{gantt_y}" width="{bar_w:.0f}" height="36" rx="6" fill="none" stroke="{color}" stroke-width="1.5"/>
        <text x="{bar_x + bar_w / 2:.0f}" y="{gantt_y + 15}" text-anchor="middle" font-size="11" font-weight="700" fill="{color}">{len(phase.get('change_ids', []))} changes</text>
        <text x="{bar_x + bar_w / 2:.0f}" y="{gantt_y + 30}" text-anchor="middle" font-size="9" fill="{BRAND_GREY}">{fmt_aud(p_val)}/yr</text>"""
        gantt_y += 60

    # Week markers
    week_markers = ""
    for w in range(total_duration + 1):
        x = gantt_pad_l + (w / total_duration) * (gantt_w - gantt_pad_l - 20)
        week_markers += f'<line x1="{x:.0f}" y1="20" x2="{x:.0f}" y2="{gantt_h - 10}" stroke="{BRAND_BORDER}" stroke-width="0.5"/>'
        if w % 2 == 0:
            week_markers += f'<text x="{x:.0f}" y="14" text-anchor="middle" font-size="9" fill="{BRAND_GREY}">W{w + 1}</text>'

    timeline_html = f"""
    <div class="op-section">
      <h2 class="op-section-title">Implementation Timeline</h2>
      <p class="op-section-desc">Phased delivery over {total_duration} weeks. Each 2-week sprint ships working features to production — you see results from week 1.</p>
      <div class="op-chart-wrap">
      <svg viewBox="0 0 {gantt_w} {gantt_h}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{gantt_w}px;height:auto">
        {week_markers}
        {gantt_bars}
      </svg>
      </div>
    </div>"""

    # ── SECTION 7: Priority Matrix (reuse shared helper) ──
    qm_html, qm_modals_html = _render_quadrant_matrix(ssad)
    priority_matrix_html = (f"""
    <div class="op-section">
      <h2 class="op-section-title">Priority Matrix</h2>
      <p class="op-section-desc">Each process area plotted by business impact and ease of implementation. Click a bubble for details.</p>
      {qm_html}
    </div>""" if qm_html else "")

    # Quick wins section removed — comparison is now inline on each change card via collapsible toggle
    qw_html = ""

    # ── SECTION 8: Functionality comparison ──
    func_html = f"""
    <div class="op-section">
      <h2 class="op-section-title">What You Get With Each Approach</h2>
      <div class="op-table-wrap">
      <table class="op-table op-func-table">
        <thead><tr><th style="text-align:left">Capability</th><th>SaaS Toolkit</th><th>Custom Build</th><th>Hybrid</th></tr></thead>
        <tbody>
          <tr><td>Single login</td><td class="op-no">&#x2717; {n_paid_tools} paid tools + free tools</td><td class="op-yes">&#x2713; One platform</td><td class="op-mid">Partial</td></tr>
          <tr><td>Scales without per-user fees</td><td class="op-no">&#x2717; Costs rise with headcount</td><td class="op-yes">&#x2713; Flat hosting</td><td class="op-mid">Partial</td></tr>
          <tr><td>All data in one place</td><td class="op-no">&#x2717; Data spread across {n_distinct_tools} tools</td><td class="op-yes">&#x2713; Unified database</td><td class="op-mid">Partial</td></tr>
          <tr><td>AI-ready from day one</td><td class="op-no">&#x2717; Need to connect data first</td><td class="op-yes">&#x2713; AI built into platform</td><td class="op-mid">Custom modules only</td></tr>
          <tr><td>Built for your processes</td><td class="op-no">&#x2717; Generic workflows</td><td class="op-yes">&#x2713; Tailored to your business</td><td class="op-mid">Core processes custom</td></tr>
          <tr><td>No vendor lock-in</td><td class="op-no">&#x2717; Data export varies by tool</td><td class="op-yes">&#x2713; You own everything</td><td class="op-mid">Custom modules owned</td></tr>
          <tr><td>Lower upfront cost</td><td class="op-yes">&#x2713; Pay as you go</td><td class="op-no">&#x2717; Sprint investment</td><td class="op-mid">Moderate</td></tr>
        </tbody>
      </table>
      </div>
    </div>"""

    # ── SECTION 9: Prototype CTA ──
    # Get prototype URL from clients.json sections (most reliable), then architecture_doc, then audit data
    _proto_url = ""
    _client_sections = load_client_sections(ssad.get("client_slug", ""))
    if _client_sections.get("prototype_url"):
        _proto_url = _client_sections["prototype_url"]
    else:
        for _src in [ssad.get("architecture_doc", {}), ssad]:
            if _src.get("prototype_url"):
                _proto_url = _src["prototype_url"]
                break

    prototype_html = ""
    if _proto_url:
        prototype_html = f"""
    <div class="op-proto-card">
      <div class="op-proto-inner">
        <div class="op-proto-text">
          <div class="op-proto-badge"><span class="op-proto-dot"></span>Now available</div>
          <div class="op-proto-heading">Your Prototype<br>is ready to explore.</div>
          <p class="op-proto-sub">A clickable prototype built from everything we discussed — see how your future platform will look and feel before a single line of production code is written.</p>
        </div>
        <div class="op-proto-action">
          <a href="{escape(_proto_url)}" target="_blank" class="op-proto-btn">Open Prototype <span style="margin-left:6px">&rarr;</span></a>
        </div>
      </div>
    </div>"""

    # ── SECTION 10: Assumptions footer ──
    assumptions_html = f"""
    <div class="op-assumptions">
      <strong>Assumptions &amp; Notes</strong>
      <ul>
        <li><strong>Blended hourly rate:</strong> ${blended_rate}/hr AUD ({escape(ssad.get('blended_rate_confidence', 'MEDIUM'))} confidence) — {escape(ssad.get('blended_rate_source', '')[:200])}</li>
        <li><strong>R&amp;D Tax Offset:</strong> 43.5% refundable offset under Div 355 ITAA 1997 for incorporated Australian companies with turnover under $20M. The offset shown is an estimate — it may not apply to the entire build. Activities involving genuine technical uncertainty (novel data models, untested integrations, experimental automation workflows) are most likely to qualify. Routine configuration, standard website development, and off-the-shelf tool setup do not qualify. You must register with AusIndustry within 10 months of financial year end and spend at least $20,000 on eligible R&amp;D. <strong>We structure our documentation to support eligibility where applicable, but please confirm with your accountant or R&amp;D tax adviser before claiming.</strong></li>
        <li><strong>Scaling:</strong> SaaS Year 3 costs projected at {scaled_staff} staff ({current_staff} current &times; 2). Custom build hosting remains flat.</li>
        <li><strong>Sprint pricing:</strong> $15,000 AUD (excl. GST) per 2-week Growth sprint (80 dev hours + 10 PM hours/week). 90-day ROI guarantee covering first 3 sprints.</li>
        <li><strong>Hosting:</strong> $100/month estimated — covers Vercel + Supabase for a standard custom application.</li>
        <li><strong>Admin overhead:</strong> SaaS: estimated {saas_admin_hours} hrs/month across {n_paid_tools} paid tools. Custom: {custom_admin_hours} hrs/month (one platform). Both at ${blended_rate}/hr blended rate.</li>
      </ul>
    </div>"""

    # ── ASSEMBLE PAGE ──
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{company} — Your Options &amp; Pricing</title>
{BRAND_FAVICON}
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        color: {BRAND_DARK}; background: {BRAND_LIGHT}; font-size: 15px; line-height: 1.6; }}
.apg-header {{ background: {BRAND_DARK}; color: #fff; padding: 20px 32px;
               display: flex; align-items: center; gap: 16px; }}
.apg-header .logo {{ font-size: 20px; font-weight: 800; }}
.container {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px; }}

/* Hero */
.op-hero {{ background: {BRAND_DARK}; color: #fff; border-radius: 16px; padding: 36px 32px; margin-bottom: 32px; }}
.op-hero-rec {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
                color: {BRAND_PRIMARY}; margin-bottom: 8px; }}
.op-hero-title {{ font-size: 22px; font-weight: 800; line-height: 1.35; margin-bottom: 24px; }}
.op-hero-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
.op-hero-stats .stat-box {{ background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15); }}
.op-hero-stats .stat-val {{ color: #fff; font-size: 22px; }}
.op-hero-stats .stat-label {{ color: rgba(255,255,255,0.6); }}

/* Sections */
.op-section {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 12px;
               padding: 28px 24px; margin-bottom: 24px; }}
.op-section-title {{ font-size: 20px; font-weight: 800; color: {BRAND_DARK}; margin-bottom: 6px; }}
.op-section-desc {{ font-size: 13px; color: {BRAND_GREY}; margin-bottom: 20px; line-height: 1.6; }}

/* Cost table */
.op-table-wrap {{ overflow-x: auto; }}
.op-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.op-table th {{ background: {BRAND_DARK}; color: #fff; padding: 10px 14px; font-size: 12px;
                font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; text-align: center; }}
.op-table th:first-child {{ text-align: left; border-radius: 8px 0 0 0; }}
.op-table th:last-child {{ border-radius: 0 8px 0 0; }}
.op-table td {{ padding: 8px 14px; border-bottom: 1px solid {BRAND_BORDER}; }}
.op-table .op-num {{ text-align: center; font-variant-numeric: tabular-nums; }}
.op-table tr.op-spacer td {{ padding: 4px; border-bottom: 2px solid {BRAND_BORDER}; }}
.op-note {{ font-size: 11px; color: {BRAND_GREY}; margin-top: 2px; }}

/* R&D info tooltip */
.op-rd-info {{ display: inline-block; width: 16px; height: 16px; border-radius: 50%; background: #DBEAFE;
               color: #1D4ED8; font-size: 11px; text-align: center; line-height: 16px; cursor: help;
               margin-left: 4px; position: relative; vertical-align: middle; }}
.op-rd-info:hover::after {{
  content: "R&D Tax Incentive: Companies under $20M turnover can claim 43.5% refundable offset on eligible custom development. Qualifying activities include developing novel algorithms, new integration architectures, and automation logic requiring experimentation. Routine configuration or off-the-shelf SaaS setup does NOT qualify. Must register with AusIndustry. We document our builds to support eligibility where applicable — check with your accountant.";
  position: absolute; bottom: 24px; left: -140px; width: 320px; padding: 12px 14px;
  background: {BRAND_DARK}; color: #fff; font-size: 11px; line-height: 1.6; border-radius: 8px;
  z-index: 100; box-shadow: 0 4px 20px rgba(0,0,0,0.25); font-weight: 400; text-transform: none;
  letter-spacing: 0; }}

/* Hidden cost cards */
.op-hidden-section {{ background: #FFFBEB; border-color: #FCD34D; }}
.op-hidden-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
.op-hidden-card {{ background: #fff; border: 1px solid #FDE68A; border-radius: 10px; padding: 16px; }}
.op-hidden-icon {{ font-size: 24px; margin-bottom: 6px; }}
.op-hidden-label {{ font-size: 14px; font-weight: 700; color: {BRAND_DARK}; margin-bottom: 6px; }}
.op-hidden-detail {{ font-size: 13px; color: {BRAND_DARK}; line-height: 1.6; }}
.op-hidden-compare {{ background: #D1FAE5; border-radius: 8px; padding: 12px 16px; font-size: 13px; color: #166534; line-height: 1.6; }}

/* Chart */
.op-chart-wrap {{ text-align: center; margin-bottom: 12px; }}
.op-chart-legend {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }}
.op-legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 12px; color: {BRAND_GREY}; }}
.op-legend-dot {{ width: 12px; height: 12px; border-radius: 50%; display: inline-block; }}

/* Phase modules */
.op-phase {{ margin-bottom: 28px; }}
.op-phase-header {{ display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px;
                     padding-bottom: 12px; border-bottom: 2px solid {BRAND_BORDER}; }}
.op-phase-num {{ background: {BRAND_DARK}; color: #fff; font-size: 12px; font-weight: 800;
                  padding: 6px 12px; border-radius: 6px; white-space: nowrap; }}
.op-phase-label {{ font-size: 18px; font-weight: 800; color: {BRAND_DARK}; }}
.op-phase-meta {{ font-size: 12px; color: {BRAND_GREY}; margin-top: 2px; }}
.op-phase-desc {{ font-size: 13px; color: {BRAND_GREY}; margin-top: 4px; line-height: 1.5; }}
.op-phase-totals {{ display: flex; gap: 20px; padding: 12px 16px; background: #F8FAFC;
                     border-radius: 8px; font-size: 13px; color: {BRAND_DARK}; flex-wrap: wrap; }}

/* Change comparison cards */
.op-change-card {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 10px;
                   margin-bottom: 12px; overflow: hidden; }}
.op-change-header {{ display: flex; align-items: center; gap: 6px; padding: 12px 16px 0; }}
.op-change-id {{ font-size: 11px; font-weight: 700; color: {BRAND_GREY}; margin-left: auto; }}
.op-change-title {{ font-size: 15px; font-weight: 700; padding: 4px 16px 4px; }}
.op-change-value {{ font-size: 13px; color: {BRAND_GREY}; padding: 0 16px 12px; }}
.op-compare-grid {{ display: grid; grid-template-columns: 1fr 1fr; }}
.op-compare-col {{ padding: 14px 16px; }}
.op-compare-saas {{ background: #FEF2F2; border-top: 2px solid #FECACA; }}
.op-compare-custom {{ background: #F0FDF4; border-top: 2px solid #BBF7D0; }}
.op-compare-heading {{ font-size: 13px; font-weight: 700; color: {BRAND_DARK}; margin-bottom: 8px; }}
.op-compare-cost {{ font-size: 12px; color: {BRAND_DARK}; margin-bottom: 4px; }}
.op-compare-proscons {{ margin-top: 10px; }}
.op-compare-proscons ul {{ margin: 4px 0 0 14px; padding: 0; font-size: 12px; line-height: 1.6; color: {BRAND_DARK}; }}
.so-pc-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }}
.so-pro-label {{ color: #166534; }}
.so-con-label {{ color: #991B1B; }}
.so-badge {{ padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;
             text-transform: uppercase; letter-spacing: 0.04em; }}
.op-qw-badge {{ background: {BRAND_PRIMARY}; color: #166534; padding: 2px 8px; border-radius: 4px;
                font-size: 9px; font-weight: 700; text-transform: uppercase; }}

/* Collapsible compare toggle on change cards */
.op-compare-toggle {{ border-top: 1px solid {BRAND_BORDER}; }}
.op-compare-toggle summary {{ list-style: none; cursor: pointer; user-select: none;
               padding: 10px 16px; font-size: 13px; font-weight: 600; color: #3B82F6;
               display: flex; align-items: center; gap: 6px; }}
.op-compare-toggle summary::-webkit-details-marker {{ display: none; }}
.op-compare-toggle summary:hover {{ background: #F8FAFC; }}
.op-compare-arrow {{ font-size: 10px; transition: transform 0.15s; display: inline-block; }}
.op-compare-toggle[open] .op-compare-arrow {{ transform: rotate(90deg); }}
.op-compare-hint {{ margin-left: auto; font-size: 11px; font-weight: 400; color: {BRAND_GREY}; }}

/* Priority matrix bubbles & modals */
.pm-bubble {{ position:absolute; border-radius:50%; border:2px solid; opacity:0.85;
              cursor:pointer; display:flex; align-items:center; justify-content:center;
              transform:translate(-50%,-50%); transition:transform 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease; }}
.pm-bubble:hover {{ transform:translate(-50%,-50%) scale(1.18); opacity:1; box-shadow:0 4px 16px rgba(0,0,0,0.25); z-index:10; }}
.pm-bubble-label {{ font-weight:700; color:#fff; pointer-events:none; text-shadow:0 1px 2px rgba(0,0,0,0.5); line-height:1.1; }}
@keyframes pm-pulse {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(5,150,105,0.3); }} 50% {{ box-shadow:0 0 0 8px rgba(5,150,105,0); }} }}
.pm-bubble-top {{ animation:pm-pulse 2s ease-in-out 3; }}
.pm-modal-backdrop {{ position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.6);
                      z-index:2000; display:flex; align-items:center; justify-content:center; padding:24px; }}
.pm-modal {{ background:#fff; border-radius:14px; max-width:560px; width:100%; max-height:85vh; overflow-y:auto;
             padding:28px 32px; position:relative; box-shadow:0 20px 60px rgba(0,0,0,0.3); }}
.pm-modal-close {{ position:absolute; top:12px; right:16px; background:none; border:none; font-size:24px;
                   color:{BRAND_GREY}; cursor:pointer; padding:4px 8px; line-height:1; }}
.pm-modal-close:hover {{ color:{BRAND_DARK}; }}
.pm-modal-section {{ margin-bottom:16px; }}
.pm-modal-section h4 {{ font-size:13px; font-weight:700; color:{BRAND_GREY}; text-transform:uppercase;
                        letter-spacing:0.05em; margin-bottom:4px; }}
.pm-modal-section p {{ font-size:14px; line-height:1.55; color:{BRAND_DARK}; }}
.pm-modal-formula {{ background:#F0FDF4; border:1px solid #BBF7D0; border-radius:6px; padding:8px 12px;
                     font-size:13px; font-weight:600; color:#166534; margin:8px 0 16px 0; font-family:monospace; }}
.pm-modal-stats {{ display:flex; gap:24px; margin-top:20px; padding-top:16px; border-top:1px solid #E5E7EB; }}
.pm-modal-stat-val {{ font-size:20px; font-weight:800; color:{BRAND_DARK}; display:block; }}
.pm-modal-stat-lbl {{ font-size:10px; text-transform:uppercase; letter-spacing:0.06em; color:{BRAND_GREY}; }}

/* Quadrant Priority Matrix */
.qm-container {{ position:relative; aspect-ratio:16/10; background:#fff; border:1px solid {BRAND_BORDER};
                  border-radius:12px; padding:48px; overflow:visible; margin-top:12px; }}
.qm-axis-x {{ position:absolute; left:48px; right:48px; bottom:48px; height:2px; background:{BRAND_DARK}; opacity:0.5; }}
.qm-axis-y {{ position:absolute; left:48px; top:48px; bottom:48px; width:2px; background:{BRAND_DARK}; opacity:0.5; }}
.qm-mid-x {{ position:absolute; left:48px; right:48px; top:50%; height:1px; background:{BRAND_DARK}; opacity:0.2; }}
.qm-mid-y {{ position:absolute; top:48px; bottom:48px; left:50%; width:1px; background:{BRAND_DARK}; opacity:0.2; }}
.qm-label {{ position:absolute; font-size:10px; font-weight:700; text-transform:uppercase;
             letter-spacing:0.08em; color:{BRAND_GREY}; opacity:0.4; }}
.qm-label-tl {{ top:56px; left:56px; }}
.qm-label-tr {{ top:56px; right:56px; opacity:1 !important; color:#166534; }}
.qm-label-br {{ bottom:56px; right:56px; opacity:1 !important; color:#3b82f6; }}
.qm-label-bl {{ bottom:56px; left:56px; }}
.qm-axis-label-x {{ position:absolute; bottom:8px; left:50%; transform:translateX(-50%);
                     font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:{BRAND_GREY}; }}
.qm-axis-label-y {{ position:absolute; left:4px; top:50%; transform:translateY(-50%) rotate(-90deg);
                     font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;
                     color:{BRAND_GREY}; white-space:nowrap; }}
.qm-bubble {{ position:absolute; border-radius:50%; border:2px solid; transform:translate(-50%,50%);
              cursor:pointer; transition:all 0.3s ease; }}
.qm-bubble.qm-dimmed {{ opacity:0.3 !important; }}
.qm-bubble.qm-active {{ transform:translate(-50%,50%) scale(1.25) !important; }}
.qm-tip {{ display:none; position:absolute; bottom:calc(100% + 8px); left:50%; transform:translateX(-50%);
           background:#fff; border:1px solid {BRAND_BORDER}; border-radius:8px; padding:10px 14px;
           box-shadow:0 4px 16px rgba(0,0,0,0.12); z-index:20; white-space:nowrap; pointer-events:none; }}
.qm-bubble.qm-active .qm-tip {{ display:block; }}
.qm-legend {{ margin-top:20px; display:flex; flex-wrap:wrap; gap:8px; justify-content:center; }}
.qm-legend-btn {{ display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border-radius:8px;
                   border:1px solid {BRAND_BORDER}; background:transparent; cursor:pointer;
                   transition:all 0.2s; font-family:inherit; color:{BRAND_DARK}; }}
.qm-legend-btn:hover, .qm-legend-btn.qm-legend-active {{ border-color:{BRAND_PRIMARY}; background:rgba(125,255,0,0.08); }}
@media (max-width:768px) {{ .qm-container {{ padding:24px; }} }}

/* Prototype CTA card */
.op-proto-card {{ background: linear-gradient(135deg, {BRAND_DARK} 0%, #1a2535 100%); border-radius: 16px;
                   padding: 40px 36px; margin: 24px 0; overflow: hidden; }}
.op-proto-inner {{ display: flex; align-items: center; gap: 32px; flex-wrap: wrap; }}
.op-proto-text {{ flex: 1; min-width: 280px; }}
.op-proto-badge {{ display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.08em; color: #10B981; margin-bottom: 12px; }}
.op-proto-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #10B981;
                  animation: op-proto-pulse 2s ease-in-out infinite; }}
@keyframes op-proto-pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
.op-proto-heading {{ font-size: 28px; font-weight: 800; color: #fff; line-height: 1.2; margin-bottom: 12px; }}
.op-proto-sub {{ font-size: 14px; color: #94A3B8; line-height: 1.6; }}
.op-proto-action {{ flex-shrink: 0; }}
.op-proto-btn {{ display: inline-flex; align-items: center; padding: 14px 28px; background: {BRAND_PRIMARY};
                  color: {BRAND_DARK}; font-size: 15px; font-weight: 800; border-radius: 10px;
                  text-decoration: none; transition: all 0.2s; }}
.op-proto-btn:hover {{ background: #9FFF40; transform: translateY(-1px); box-shadow: 0 4px 16px rgba(125,255,0,0.3); }}

/* Functionality table */
.op-func-table td {{ text-align: center; }}
.op-func-table td:first-child {{ text-align: left; font-weight: 600; }}
.op-yes {{ color: #166534; background: #F0FDF4; }}
.op-no {{ color: #991B1B; background: #FEF2F2; }}
.op-mid {{ color: #92400E; background: #FFFBEB; }}

/* Stats */
.stat-box {{ background: #fff; border: 1px solid {BRAND_BORDER}; border-radius: 10px; padding: 16px 12px; text-align: center; }}
.stat-val {{ font-size: 26px; font-weight: 800; color: {BRAND_DARK}; letter-spacing: -0.03em; margin-bottom: 2px; }}
.stat-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em; color: {BRAND_GREY}; }}

/* Assumptions */
.op-assumptions {{ font-size: 12px; color: {BRAND_GREY}; padding: 20px 0; border-top: 1px solid {BRAND_BORDER};
                    margin-top: 16px; }}
.op-assumptions ul {{ margin: 8px 0 0 18px; line-height: 1.8; }}
.op-assumptions strong {{ color: {BRAND_DARK}; }}

@media (max-width: 768px) {{
  .op-hero-stats {{ grid-template-columns: repeat(2, 1fr); }}
  .op-hidden-grid {{ grid-template-columns: 1fr; }}
  .op-compare-grid {{ grid-template-columns: 1fr; }}
  .op-phase-totals {{ flex-direction: column; gap: 8px; }}
}}
@media print {{
  body {{ font-size: 11px; }}
  .op-hero {{ padding: 20px; }}
  .op-section {{ break-inside: avoid; }}
  .op-change-card {{ break-inside: avoid; }}
}}
</style>
</head>
<body>

<div class="apg-header">
  <div class="logo">{YOUR_COMPANY}</div>
  <div>
    <div style="font-weight:700;font-size:16px">{company} — Your Options &amp; Pricing</div>
    <div style="font-size:13px;color:#9CA3AF">{len(changes)} improvements &middot; 3 approaches compared &middot; Generated {generated}</div>
  </div>
</div>

<div class="container">

{hero_html}
{comparison_html}
{toolkit_html}
{hidden_html}
{bigger_picture_html}
{chart_html}
{options_html}

<h2 style="font-size:22px;font-weight:800;color:{BRAND_DARK};margin-bottom:20px">Process-by-Process Breakdown</h2>
{modules_html}

{timeline_html}
{priority_matrix_html}
{qw_html}
{func_html}
{prototype_html}
{assumptions_html}

<div style="font-size:11px;color:{BRAND_GREY};margin-top:12px;padding-top:12px;border-top:1px solid {BRAND_BORDER}">
  Generated by {YOUR_COMPANY} Audit System &middot; {generated} &middot; Current team size: {current_staff} staff.
</div>

</div>

{qm_modals_html}

<script>
function openModal(id) {{
  var el = document.getElementById('modal-' + id);
  if (el) {{ el.style.display = 'flex'; document.body.style.overflow = 'hidden'; }}
}}
function closeModal() {{
  document.querySelectorAll('.pm-modal-backdrop').forEach(function(m) {{ m.style.display = 'none'; }});
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeModal(); }});
function showTip(el, title, value, weeks) {{
  var tip = document.getElementById('pm-tooltip');
  if (!tip) return;
  tip.innerHTML = '<div style="font-weight:700;margin-bottom:2px">' + title + '</div>'
    + '<div style="color:#9CA3AF;font-size:11px">' + value + ' &middot; ' + weeks + '</div>';
  tip.style.display = 'block';
  var r = el.getBoundingClientRect();
  tip.style.left = (r.left + r.width/2) + 'px';
  tip.style.top = (r.top - 8) + 'px';
  tip.style.transform = 'translate(-50%, -100%)';
}}
function hideTip() {{
  var tip = document.getElementById('pm-tooltip');
  if (tip) tip.style.display = 'none';
}}
// ── Quadrant matrix interaction ──
var qmHovered = null, qmSelected = null;
function qmUpdate() {{
  var active = qmHovered !== null ? qmHovered : qmSelected;
  document.querySelectorAll('.qm-bubble').forEach(function(b) {{
    var idx = parseInt(b.dataset.idx);
    b.classList.toggle('qm-active', idx === active);
    b.classList.toggle('qm-dimmed', active !== null && idx !== active);
    if (idx === active) {{
      b.style.boxShadow = '0 0 20px ' + b.style.borderColor + '80';
      b.style.background = b.style.borderColor + '40';
    }} else {{
      b.style.boxShadow = 'none';
      b.style.background = b.style.borderColor.replace(')', ',0.12)').replace('rgb', 'rgba');
    }}
  }});
  document.querySelectorAll('.qm-legend-btn').forEach(function(b) {{
    var idx = parseInt(b.dataset.idx);
    b.classList.toggle('qm-legend-active', idx === active);
  }});
}}
function qmHover(idx) {{ qmHovered = idx; qmUpdate(); }}
function qmSelect(idx) {{ qmSelected = (qmSelected === idx) ? null : idx; qmUpdate(); }}
function qmClick(idx) {{
  qmSelected = idx; qmUpdate();
  var b = document.querySelector('.qm-bubble[data-idx="' + idx + '"]');
  if (b && b.dataset.cid) openModal(b.dataset.cid);
}}
</script>
</body>
</html>"""


def generate_strategic_approaches(ssad: dict) -> str:
    """Generate strategic-approaches.html — pipeline pipe overview with click-to-expand blueprint detail."""
    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    changes = ssad.get("proposed_changes", [])
    processes = ssad.get("processes", [])
    stage_labels_map, stage_subtitles_map = _build_stage_lookups(ssad)

    pp_lookup = {pp.get("pain_point_id", ""): pp for pp in ssad.get("pain_points", [])}

    _bp = _build_blueprint_renderers(ssad)
    bp_render_left = _bp["render_left_column"]
    bp_processes_by_stage = _bp["processes_by_stage"]
    bp_stage_labels = _bp["stage_labels"]
    bp_stage_subtitles = _bp["stage_subtitles"]

    change_by_step = _build_change_lookup(changes)

    changes_by_stage = {}
    cross_process_changes = []
    for c in changes:
        stage = c.get("stage", "other")
        if stage == "all":
            cross_process_changes.append(c)
        else:
            changes_by_stage.setdefault(stage, []).append(c)

    n_total = len(changes)

    # ── Load recommended toolkit from strategic_approaches ──
    sa = ssad.get("strategic_approaches", {})
    strategies = sa.get("strategies", [])
    # Pick the recommended strategy (first one, or smart-saas-mix for backward compat)
    rec_strategy = None
    if strategies:
        rec_strategy = strategies[0]
        for s in strategies:
            if s.get("strategy_id") in ("recommended-saas-toolkit", "smart-saas-mix"):
                rec_strategy = s
                break

    # Build lookup: change_id → tool_selection from the recommended strategy
    tool_sel_by_change = {}
    if rec_strategy:
        for ts in rec_strategy.get("tool_selections", []):
            tool_sel_by_change[ts.get("change_id", "")] = ts

    cost_summary = rec_strategy.get("cost_summary", {}) if rec_strategy else {}

    # ── Recommended tool card renderer ──
    def render_recommended_tool(change_id):
        ts = tool_sel_by_change.get(change_id)
        if not ts:
            return '<div style="font-size:11px;color:#9CA3AF;font-style:italic;padding:8px 0">No tool recommendation available</div>'
        tname = escape(str(ts.get("selected_tool", "Unknown")))
        annual = ts.get("annual_cost_aud", 0) or 0
        cost_display = "${:,.0f}/yr".format(annual) if annual > 0 else "Free"
        tier = escape(str(ts.get("tier_selected", "")))
        tier_badge = '<span style="background:#EFF6FF;color:#1D4ED8;font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;margin-left:6px">{}</span>'.format(tier) if tier and tier != "Free" else ""
        weeks = ts.get("weeks_label", "") or ts.get("weeks_estimate", "")
        weeks_html = '<span style="font-size:10px;color:#64748b;margin-left:auto">{} to set up</span>'.format(escape(str(weeks))) if weeks else ""

        why = escape(str(ts.get("why_this_tool", ts.get("rationale", ""))))
        why_html = '<div style="font-size:12px;color:#374151;line-height:1.6;margin:8px 0">{}</div>'.format(why) if why else ""

        config = ts.get("configuration_steps", [])
        config_html = ""
        if config:
            items = "".join('<li style="padding:3px 0">{}</li>'.format(escape(str(s))) for s in config)
            config_html = '<details style="margin-top:6px"><summary style="font-size:11px;font-weight:700;color:#166534;cursor:pointer">Configuration Steps</summary><ol style="font-size:11px;color:#374151;line-height:1.6;margin:6px 0 0 16px;padding:0">{}</ol></details>'.format(items)

        caveats = ts.get("caveats", [])
        caveats_html = ""
        if caveats:
            items = "".join('<li style="padding:2px 0">{}</li>'.format(escape(str(c))) for c in caveats)
            caveats_html = '<details style="margin-top:6px"><summary style="font-size:11px;font-weight:700;color:#EA580C;cursor:pointer">&#9888; Things to Know ({n})</summary><ul style="font-size:11px;color:#374151;line-height:1.6;margin:6px 0 0 16px;padding:0">{items}</ul></details>'.format(n=len(caveats), items=items)

        return (
            '<div style="margin-top:10px;background:#f0fdf4;border:1.5px solid #86efac;border-radius:8px;padding:12px 14px">'
            '<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">'
            '<span style="font-size:13px;font-weight:700;color:#0f1825">{tn}</span>'
            '{tb}'
            '<span style="font-size:14px;font-weight:800;color:#166534;margin-left:auto">{cd}</span>'
            '</div>'
            '<div style="display:flex;align-items:center;gap:6px">'
            '<span style="background:#D1FAE5;color:#166534;font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;text-transform:uppercase">Recommended</span>'
            '{wh}'
            '</div>'
            '{why}{cfg}{cav}'
            '</div>'
        ).format(tn=tname, tb=tier_badge, cd=cost_display, wh=weeks_html,
                 why=why_html, cfg=config_html, cav=caveats_html)

    # ── Improvement card renderer ──
    def render_improvement_card(ch, steps_by_id, current_stage):
        cid = ch.get("change_id", "")
        title = escape(ch.get("title", ""))
        ctype = ch.get("change_type", "automate")
        badge_label, border_color, bg_color = CHANGE_BADGE.get(ctype, ("CHANGED", "#6B7280", "#F3F4F6"))
        affected_ids = ch.get("affected_step_ids", [])
        steps_html_parts = []
        for sid in affected_ids:
            s = steps_by_id.get(sid)
            if not s:
                continue
            step_desc = escape(s.get("description", ""))
            steps_html_parts.append(
                '<div style="font-size:11px;color:#475569;padding:3px 0;border-bottom:1px solid rgba(0,0,0,0.05)">'
                '<span style="color:#9CA3AF;font-size:10px;font-weight:600;margin-right:4px">{}</span> {}</div>'.format(escape(sid), step_desc)
            )
        steps_list_html = "".join(steps_html_parts)
        change_stage = ch.get("stage", "")
        other_stages = []
        if change_stage == "all":
            for proc in processes:
                pstage = proc["stage"]
                if pstage != current_stage:
                    psteps = {s.get("step_id",""): s for s in proc.get("steps",[])}
                    if any(sid in psteps for sid in affected_ids):
                        other_stages.append(bp_stage_labels.get(pstage, pstage))
        cross_note = ""
        if other_stages:
            cross_note = '<div style="font-size:10px;color:#9CA3AF;margin-top:4px;font-style:italic">Also applies to: {}</div>'.format(", ".join(other_stages))
        future_desc = ch.get("future_step_description", "") or ch.get("proposed_solution", "")
        future_html = ""
        if future_desc:
            future_html = '<div style="margin-top:8px;font-size:12px;color:#0f1825;font-weight:500;padding:8px 10px;background:rgba(125,255,0,0.06);border-left:3px solid #7DFF00;border-radius:0 6px 6px 0">{}</div>'.format(escape(future_desc))
        # Recommended tool from strategic approaches
        tool_rec_html = render_recommended_tool(cid)
        linked_pps = ch.get("linked_pain_point_ids", [])
        pp_html = ""
        if linked_pps:
            pp_items = []
            for ppid in linked_pps[:3]:
                pp = pp_lookup.get(ppid, {})
                pp_desc = escape(str(pp.get("description", ""))[:80])
                if pp_desc:
                    pp_items.append('<div style="font-size:10px;color:#dc2626;padding:2px 0">&#x26A0; {}</div>'.format(pp_desc))
            if pp_items:
                pp_html = '<div style="margin-top:6px;padding:6px 8px;background:#fef2f2;border-radius:6px;border:1px solid #fca5a5">{}</div>'.format("".join(pp_items))
        return (
            '<div class="sa-change-card" style="border-color:{bc};background:{bg}" id="sa-card-{cid}">'
            '<span class="sa-change-badge" style="background:{bc}">{bl}</span>'
            '<div class="sa-change-title">{title}</div>'
            '<div class="sa-change-steps">{sl}</div>'
            '{cn}{fh}{pp}{tr}'
            '</div>'
        ).format(bc=border_color, bg=bg_color, cid=cid, bl=badge_label, title=title,
                 sl=steps_list_html, cn=cross_note, fh=future_html, pp=pp_html, tr=tool_rec_html)

    # ── Build pipe segments and detail panels ──
    pipe_segments_html = ""
    detail_panels_html = ""

    for proc in processes:
        stage = proc["stage"]
        steps = bp_processes_by_stage.get(stage, [])
        label = bp_stage_labels.get(stage, stage.replace("_", " ").title())
        subtitle = bp_stage_subtitles.get(stage, "")
        if not steps:
            continue
        steps_by_id = {s.get("step_id", ""): s for s in steps}
        seen_ids = set()
        stage_changes = []
        for s in steps:
            if s.get("branch_only"):
                continue
            sid = s.get("step_id", "")
            for ch in change_by_step.get(sid, []):
                cid_val = ch.get("change_id", "")
                if cid_val and cid_val not in seen_ids:
                    seen_ids.add(cid_val)
                    stage_changes.append(ch)
        for ch in changes_by_stage.get(stage, []):
            cid_val = ch.get("change_id", "")
            if cid_val not in seen_ids:
                seen_ids.add(cid_val)
                stage_changes.append(ch)
        n_changes = len(stage_changes)
        n_steps = len([s for s in steps if not s.get("branch_only")])
        tooltip_changes = ""
        for ch in stage_changes[:4]:
            tooltip_changes += '<div class="tt-change"><div class="tt-dot" style="background:#10B981"></div> {}</div>'.format(escape(ch.get("title","")[:45]))
        if n_changes > 4:
            tooltip_changes += '<div class="tt-change"><div class="tt-dot" style="background:#10B981"></div> +{} more...</div>'.format(n_changes - 4)
        badge_text = "{} improvement{}".format(n_changes, "s" if n_changes != 1 else "")

        pipe_segments_html += (
            '<div class="pipe-seg" data-stage="{stage}" onclick="toggleStage(\'{stage}\')">'
            '<span class="seg-badge">{badge}</span>'
            '<span class="seg-label">{label}</span>'
            '<div class="seg-tt">'
            '<div class="tt-title">{label}</div>'
            '<div class="tt-sub">{sub}</div>'
            '<div class="tt-stats">'
            '<div class="tt-stat"><div class="tt-stat-val">{nc}</div><div class="tt-stat-lbl">Improvements</div></div>'
            '<div class="tt-stat"><div class="tt-stat-val">{ns}</div><div class="tt-stat-lbl">Current Steps</div></div>'
            '</div>'
            '<div class="tt-changes">{tc}</div>'
            '<div class="tt-cta">Click to explore &darr;</div>'
            '</div>'
            '</div>'
        ).format(stage=stage, badge=badge_text, label=escape(label), sub=escape(subtitle),
                 nc=n_changes, ns=n_steps, tc=tooltip_changes)

        # Detail panel
        left_html = bp_render_left(steps, stage, change_by_step)
        right_parts = []
        for ch in stage_changes:
            right_parts.append(render_improvement_card(ch, steps_by_id, stage))
        right_html = "\n".join(right_parts) if right_parts else '<div style="padding:20px;text-align:center;color:#9CA3AF;font-size:12px;font-style:italic">No improvements identified</div>'
        badge_count = "{} change{}".format(n_changes, "s" if n_changes != 1 else "") if n_changes else "no changes"
        detail_panels_html += (
            '<div class="stage-panel" id="panel-{stage}" style="display:none">'
            '<div class="bp-zone">'
            '<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">'
            '<div style="border-left:4px solid #7DFF00;padding-left:12px">'
            '<div style="font-size:18px;font-weight:800;color:#0f1825;letter-spacing:-0.02em">{label}</div>'
            '<div style="font-size:11px;color:#64748b">{sub}</div>'
            '</div>'
            '<span style="font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;'
            'letter-spacing:0.5px;text-transform:uppercase;color:#64748b;background:#f1f5f9;'
            'border:1px solid #e2e8f0;margin-left:auto">{bc}</span>'
            '<button class="panel-close" onclick="closeDetail()">&times;</button>'
            '</div>'
            '<div class="bp-columns">'
            '<div class="bp-col"><div class="bp-col-header" style="border-color:#EF4444;color:#EF4444">Current State</div>{left}</div>'
            '<div class="bp-col"><div class="bp-col-header" style="border-color:#7DFF00;color:#166534">Recommended</div>{right}</div>'
            '</div></div></div>'
        ).format(stage=stage, label=escape(label), sub=escape(subtitle), bc=badge_count,
                 left=left_html, right=right_html)

    # Cross-process panel
    if cross_process_changes:
        all_steps_by_id = {}
        for proc in processes:
            for s in proc.get("steps", []):
                all_steps_by_id[s.get("step_id", "")] = s
        cross_cards = "\n".join(render_improvement_card(ch, all_steps_by_id, "all") for ch in cross_process_changes)
        n_cross = len(cross_process_changes)
        detail_panels_html += (
            '<div class="stage-panel" id="panel-cross-process" style="display:none">'
            '<div class="bp-zone">'
            '<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">'
            '<div style="border-left:4px solid #8B5CF6;padding-left:12px">'
            '<div style="font-size:18px;font-weight:800;color:#0f1825">Cross-Process Improvements</div>'
            '<div style="font-size:11px;color:#64748b">Improvements that apply across multiple business areas</div>'
            '</div>'
            '<span style="font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;'
            'letter-spacing:0.5px;text-transform:uppercase;color:#64748b;background:#f1f5f9;'
            'border:1px solid #e2e8f0;margin-left:auto">{nc} change{s}</span>'
            '<button class="panel-close" onclick="closeDetail()">&times;</button>'
            '</div>{cards}</div></div>'
        ).format(nc=n_cross, s="s" if n_cross != 1 else "", cards=cross_cards)

    cross_bar_html = ""
    if cross_process_changes:
        n_cross = len(cross_process_changes)
        cross_bar_html = (
            '<div class="cross-wrap">'
            '<div class="cross-label">Spanning all processes</div>'
            '<div class="cross-bar" onclick="toggleStage(\'cross-process\')">'
            '<span class="cross-text">Cross-Process Improvements</span>'
            '<span class="cross-count">{n} improvement{s}</span>'
            '</div></div>'
        ).format(n=n_cross, s="s" if n_cross != 1 else "")

    # ── Prototype CTA ──
    client_slug = ssad.get("client_slug", "")
    proto_dir = Path(f"clients/{client_slug}/prototype") if client_slug else None
    has_prototype = proto_dir and proto_dir.exists() and any(proto_dir.iterdir()) if proto_dir and proto_dir.exists() else False
    if has_prototype:
        proto_cta = '<a href="prototype/" target="_blank" style="display:inline-block;background:#0f1825;color:#7DFF00;font-weight:700;font-size:13px;padding:12px 28px;border-radius:8px;text-decoration:none;letter-spacing:0.02em">View Custom Build Prototype &rarr;</a>'
    else:
        proto_cta = '<div style="display:inline-block;background:#f1f5f9;color:#64748b;font-weight:600;font-size:12px;padding:10px 24px;border-radius:8px;border:1px dashed #cbd5e1">Prototype coming soon &mdash; being built by the Solution Designer</div>'

    # ── Cost summary section ──
    ongoing = (
        cost_summary.get("ongoing_annual_total_aud", 0)
        or cost_summary.get("ongoing_annual_current_aud", 0)
        or cost_summary.get("tool_subscriptions_annual_aud", 0)
        or (cost_summary.get("ongoing_annual_saas_aud", 0)
            + cost_summary.get("ongoing_annual_cowork_tools_aud", 0)
            + cost_summary.get("ongoing_annual_cowork_subscriptions_aud", 0))
        or 0
    )
    setup = cost_summary.get("total_setup_cost_aud", 0) or 0
    integration = cost_summary.get("integration_development_cost_aud", 0) or 0
    training = cost_summary.get("training_cost_aud", 0) or 0
    consultant = cost_summary.get("total_consultant_fees_aud", 0) or 0
    first_year = cost_summary.get("total_first_year_cost_aud", 0) or (ongoing + setup + integration + training + consultant)
    impl_weeks = cost_summary.get("implementation_weeks", 0) or 0
    admin_hrs = cost_summary.get("total_ongoing_admin_hours", 0) or 0
    hidden = cost_summary.get("hidden_costs_annual_aud", 0) or 0
    scaled = cost_summary.get("ongoing_annual_scaled_aud", 0) or 0

    cost_rows = ""
    if ongoing: cost_rows += '<tr><td>Tool subscriptions (annual)</td><td style="text-align:right;font-weight:700">${:,.0f}/yr</td></tr>'.format(ongoing)
    if hidden: cost_rows += '<tr><td>Likely hidden costs (annual upsells)</td><td style="text-align:right;font-weight:700;color:#EA580C">${:,.0f}/yr</td></tr>'.format(hidden)
    if setup: cost_rows += '<tr><td>Setup &amp; configuration</td><td style="text-align:right;font-weight:700">${:,.0f}</td></tr>'.format(setup)
    if consultant: cost_rows += '<tr><td>Consultant / implementation fees</td><td style="text-align:right;font-weight:700">${:,.0f}</td></tr>'.format(consultant)
    if integration: cost_rows += '<tr><td>Integration &amp; automation build</td><td style="text-align:right;font-weight:700">${:,.0f}</td></tr>'.format(integration)
    if training: cost_rows += '<tr><td>Training</td><td style="text-align:right;font-weight:700">${:,.0f}</td></tr>'.format(training)

    cost_summary_html = """
    <div style="max-width:900px;margin:40px auto;padding:0 24px">
      <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:28px;box-shadow:0 1px 8px rgba(15,24,37,0.06)">
        <div style="font-size:20px;font-weight:800;color:#0f1825;margin-bottom:4px">SaaS Toolkit — Cost Breakdown</div>
        <div style="font-size:12px;color:#64748b;margin-bottom:20px">What it costs to implement and run this toolkit</div>
        <table style="width:100%;border-collapse:collapse;font-size:13px">
          <tbody>
            {rows}
            <tr style="border-top:2px solid #0f1825"><td style="padding-top:12px;font-weight:800;font-size:15px">First-year total</td><td style="text-align:right;padding-top:12px;font-weight:800;font-size:15px">${fy:,.0f}</td></tr>
            <tr><td style="color:#64748b">Ongoing (year 2+)</td><td style="text-align:right;color:#64748b;font-weight:600">${og:,.0f}/yr</td></tr>
          </tbody>
        </table>
        <div style="display:flex;gap:24px;margin-top:20px;padding-top:16px;border-top:1px solid #e2e8f0;flex-wrap:wrap">
          <div style="text-align:center;flex:1"><div style="font-size:22px;font-weight:800;color:#0f1825">{wk}</div><div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:#64748b">Weeks to implement</div></div>
          <div style="text-align:center;flex:1"><div style="font-size:22px;font-weight:800;color:#0f1825">{ah}</div><div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:#64748b">Admin hrs/month</div></div>
          <div style="text-align:center;flex:1"><div style="font-size:22px;font-weight:800;color:#0f1825">{nt}</div><div style="font-size:10px;text-transform:uppercase;letter-spacing:0.06em;color:#64748b">Separate tools</div></div>
        </div>
        {scaled_note}
      </div>

      <div style="background:#f0fdf4;border:2px solid #86efac;border-radius:14px;padding:28px;margin-top:20px;text-align:center">
        <div style="font-size:18px;font-weight:800;color:#0f1825;margin-bottom:6px">Alternative: Custom Software</div>
        <div style="font-size:13px;color:#374151;line-height:1.6;max-width:600px;margin:0 auto 16px">Instead of stitching together multiple SaaS tools, a unified custom platform eliminates data silos, per-user fees, and integration complexity. One login, one database, built for your business.</div>
        <div style="font-size:12px;color:#166534;font-weight:600;margin-bottom:16px">Hosting: $6,000/yr flat &mdash; no per-user fees at any scale</div>
        {proto_cta}
      </div>
    </div>""".format(
        rows=cost_rows, fy=first_year, og=ongoing + hidden, wk=impl_weeks, ah=admin_hrs, proto_cta=proto_cta,
        nt=len(set(ts.get("selected_tool", "") for ts in tool_sel_by_change.values())),
        scaled_note='<div style="font-size:11px;color:#64748b;margin-top:12px;text-align:center">At 2&times; staff: ${:,.0f}/yr (per-user tools scale)</div>'.format(scaled) if scaled and scaled != ongoing else ""
    )

    # Load CSS template
    css = _sa_pipe_css()
    js = _sa_pipe_js(n_total)

    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>{company} \u2014 Recommended Toolkit</title>\n'
        '{favicon}\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n'
        '<style>\n{css}\n</style>\n'
        '</head>\n<body>\n'
        '<div class="pipe-header">\n'
        '<div class="pipe-header-top">\n'
        '<img src="{logo}" alt="{YOUR_COMPANY}" style="height:36px;border-radius:8px">\n'
        '<div><div class="logo">{company}</div><div class="sub">Recommended Toolkit &mdash; {date}</div></div>\n'
        '<div class="sel-summary">'
        '<div><span class="sel-val">${ongoing:,.0f}</span>/yr ongoing</div>'
        '<div><span class="sel-val">${fy:,.0f}</span> first year</div>'
        '</div></div>\n'
        '<div class="pipe-area"><div class="pipe"><div class="pipe-segs">{segs}</div></div>\n'
        '<div class="flow-labels">'
        '<div class="flow-lbl"><span class="flow-arrow">&rarr;</span> Leads in</div>'
        '<div class="flow-lbl">Happy families <span class="flow-arrow">&rarr;</span></div>'
        '</div>{cross_bar}</div></div>\n'
        '<div class="detail-area">{panels}</div>\n'
        '{cost_section}\n'
        '<script>\n{js}\n</script>\n'
        '</body>\n</html>'
    ).format(company=company, favicon=BRAND_FAVICON, css=css, logo=COMPANY_LOGO_URL,
             date=generated, ongoing=ongoing + hidden, fy=first_year,
             segs=pipe_segments_html,
             cross_bar=cross_bar_html, panels=detail_panels_html,
             cost_section=cost_summary_html, js=js)


def _sa_hours_per_week(change: dict, blended_rate: float) -> float:
    """Extract or estimate weekly hours saved from a proposed change."""
    import re
    formula = change.get("value", {}).get("formula_summary", "")
    m = re.search(r'(\d+\.?\d*)\s*hrs?/w', formula)
    if m:
        return float(m.group(1))
    annual = change.get("value", {}).get("combined_annual_value_aud", 0)
    return round(annual / max(blended_rate, 1) / 52, 1) if annual > 0 else 0


def generate_strategic_approaches_landing(ssad: dict, sections: dict = None) -> str:
    """Generate strategic-approaches.html — 3-tier engagement page: Quick Wins / SaaS Toolkit / Custom Platform."""
    import math
    company = escape(ssad.get("company_name", "Client"))
    generated = datetime.now().strftime("%d %b %Y")
    changes = ssad.get("proposed_changes", [])
    n_changes = len(changes)
    roi_items = ssad.get("roi_items", [])
    blended_rate = ssad.get("blended_hourly_rate_aud", 40)

    # ── Map changes to tiers — use quick_win_plan if available, fall back to suggested_tier ──
    roi_tier_map = {r.get("linked_change_id", ""): r.get("suggested_tier", "standard") for r in roi_items}
    qw_changes = [c for c in changes if c.get("quick_win_plan", {}).get("qualified") is True]
    # Fallback: if no quick_win_plan data exists yet, use suggested_tier == "micro"
    if not qw_changes and not any(c.get("quick_win_plan") for c in changes):
        qw_changes = [c for c in changes if roi_tier_map.get(c.get("change_id")) == "micro"]
    qw_change_ids = {c.get("change_id") for c in qw_changes}
    saas_changes = [c for c in changes if c.get("change_id") not in qw_change_ids and roi_tier_map.get(c.get("change_id")) in ("micro", "standard", "complex")]
    custom_changes = [c for c in changes if roi_tier_map.get(c.get("change_id")) == "sprint"]

    # Hours saved per tier
    qw_hrs = sum(_sa_hours_per_week(c, blended_rate) for c in qw_changes)
    saas_hrs = sum(_sa_hours_per_week(c, blended_rate) for c in saas_changes)
    all_hrs = sum(_sa_hours_per_week(c, blended_rate) for c in changes)

    qw_items = [r for r in roi_items if r.get("suggested_tier") == "micro"]
    n_qw = len(qw_items)

    # ── SaaS data ──
    sa = ssad.get("strategic_approaches", {})
    strategies = sa.get("strategies", [])
    saas_strat = None
    for s in strategies:
        if s.get("strategy_id") in ("recommended-saas-toolkit", "smart-saas-mix"):
            saas_strat = s
            break
    if not saas_strat and strategies:
        saas_strat = strategies[0]

    tool_selections = saas_strat.get("tool_selections", []) if saas_strat else []
    has_saas = saas_strat is not None

    # Build SaaS feature list — deduplicate by tool name
    saas_features_seen = {}
    for ts in tool_selections:
        tool_name = ts.get("selected_tool", "").split("(")[0].strip()
        title = ts.get("title", "")
        if tool_name and tool_name not in saas_features_seen:
            saas_features_seen[tool_name] = title
    saas_feature_items = "".join(
        f'<li><strong>{escape(name)}</strong> &mdash; {escape(desc)}</li>'
        for name, desc in list(saas_features_seen.items())[:10]
    )

    # ── Custom build data ──
    arch = ssad.get("architecture_doc", {})
    arch_meta = ssad.get("architect_metadata", {})
    modules = arch.get("module_inventory", [])
    n_modules = len(modules)
    has_custom = n_modules > 0

    # Build custom feature list from module inventory
    custom_feature_items = "".join(
        f'<li><strong>{escape(m.get("module_name", "Module"))}</strong> &mdash; {escape(m.get("description", ""))}</li>'
        for m in modules[:10]
    )

    # Quick wins feature list with hours saved and approach
    qw_feature_items = ""
    for c in qw_changes[:8]:
        qwp = c.get("quick_win_plan", {})
        hrs = qwp.get("dev_hours") or _sa_hours_per_week(c, blended_rate)
        title = escape(c.get("title", ""))
        approach = escape(qwp.get("approach", "")) if qwp.get("approach") else ""
        if approach:
            qw_feature_items += f'<li><strong>{title}</strong><br><span style="color:#64748b;font-size:11px">{approach}</span></li>'
        else:
            hrs_label = f' <span style="color:#059669;font-weight:600">saves ~{hrs:.0f} hrs/wk</span>' if hrs >= 1 else ""
            qw_feature_items += f'<li>{title}{hrs_label}</li>'

    # Compliance note
    compliance_keywords = ["xero", "ndis", "compliance", "accounting", "health", "claiming"]
    has_compliance_tools = any(
        any(kw in ts.get("selected_tool", "").lower() or kw in ts.get("title", "").lower()
            for kw in compliance_keywords)
        for ts in tool_selections
    )
    compliance_note = ""
    if has_compliance_tools and has_custom:
        compliance_note = (
            '<div class="sa-note">'
            '<strong>Note:</strong> Specialist SaaS is retained for compliance-critical functions '
            '(e.g., accounting, industry-specific claiming) where certified platforms are required. '
            'The custom platform integrates with these rather than replacing them.'
            '</div>'
        )

    # Prototype URL
    proto_url = ""
    if sections and sections.get("prototype_url"):
        proto_url = sections["prototype_url"]

    # Total annual value
    total_value = sa.get("total_annual_value_aud", 0)

    # ── CSS ──
    css = """
    html { scroll-behavior: smooth; }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #1e293b; min-height: 100vh; }

    .sa-header { background: #fff; border-bottom: 1px solid #e2e8f0; padding: 16px 24px; display: flex; align-items: center; gap: 12px; position: sticky; top: 0; z-index: 10; }
    .sa-header img { height: 32px; width: 32px; border-radius: 6px; }
    .sa-header-title { font-size: 15px; font-weight: 600; color: #1e293b; }
    .sa-header-sub { font-size: 12px; color: #64748b; }

    .sa-container { max-width: 1200px; margin: 0 auto; padding: 40px 24px 60px; }

    .sa-hero { text-align: center; margin-bottom: 40px; }
    .sa-hero h1 { font-size: 28px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
    .sa-hero p { font-size: 15px; color: #64748b; max-width: 640px; margin: 0 auto; line-height: 1.6; }

    .sa-stats { display: flex; justify-content: center; gap: 32px; margin-bottom: 48px; flex-wrap: wrap; }
    .sa-stat { text-align: center; }
    .sa-stat-val { font-size: 24px; font-weight: 700; color: #0f172a; }
    .sa-stat-val.green { color: #16a34a; }
    .sa-stat-label { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }

    .sa-cards { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 48px; }
    @media (max-width: 900px) { .sa-cards { grid-template-columns: 1fr; } }

    .sa-card { background: #fff; border-radius: 16px; border: 2px solid #e2e8f0; padding: 28px; display: flex; flex-direction: column; transition: border-color 0.2s; }
    .sa-card:hover { border-color: #cbd5e1; }
    .sa-card-qw { border-color: #fdba74; }
    .sa-card-qw:hover { border-color: #fb923c; }
    .sa-card-saas { border-color: #93c5fd; }
    .sa-card-saas:hover { border-color: #60a5fa; }
    .sa-card-custom { border-color: #86efac; }
    .sa-card-custom:hover { border-color: #4ade80; }

    .sa-card-icon { font-size: 28px; margin-bottom: 10px; }
    .sa-card-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
    .sa-card-label.qw { color: #ea580c; }
    .sa-card-label.saas { color: #2563eb; }
    .sa-card-label.custom { color: #16a34a; }
    .sa-card-title { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
    .sa-card-desc { font-size: 12px; color: #64748b; line-height: 1.5; margin-bottom: 16px; }

    .sa-card-metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
    .sa-metric { background: #f8fafc; border-radius: 8px; padding: 10px; }
    .sa-metric-val { font-size: 16px; font-weight: 700; color: #0f172a; }
    .sa-metric-label { font-size: 10px; color: #94a3b8; margin-top: 2px; }

    .sa-features { margin-bottom: 16px; }
    .sa-features-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 6px; }
    .sa-features ul { list-style: none; padding: 0; }
    .sa-features li { font-size: 11px; color: #475569; padding: 3px 0; line-height: 1.4; }
    .sa-features li strong { color: #1e293b; }

    .sa-card-pros-cons { margin-bottom: 20px; flex: 1; }
    .sa-pc-section { margin-bottom: 10px; }
    .sa-pc-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 5px; }
    .sa-pc-label.pro { color: #16a34a; }
    .sa-pc-label.con { color: #dc2626; }
    .sa-pc-list { list-style: none; padding: 0; }
    .sa-pc-list li { font-size: 11px; color: #475569; padding: 2px 0 2px 14px; position: relative; line-height: 1.4; }
    .sa-pc-list li::before { content: ''; position: absolute; left: 0; top: 8px; width: 5px; height: 5px; border-radius: 50%; }
    .sa-pc-list.pro li::before { background: #86efac; }
    .sa-pc-list.con li::before { background: #fca5a5; }

    .sa-card-cta { margin-top: auto; }
    .sa-btn { display: inline-flex; align-items: center; gap: 8px; padding: 11px 20px; border-radius: 10px; font-size: 13px; font-weight: 600; text-decoration: none; transition: all 0.2s; border: none; cursor: pointer; }
    .sa-btn-qw { background: #ea580c; color: #fff; }
    .sa-btn-qw:hover { background: #c2410c; }
    .sa-btn-saas { background: #2563eb; color: #fff; }
    .sa-btn-saas:hover { background: #1d4ed8; }
    .sa-btn-custom { background: #16a34a; color: #fff; }
    .sa-btn-custom:hover { background: #15803d; }
    .sa-btn-disabled { background: #e2e8f0; color: #94a3b8; cursor: default; }
    .sa-btn-arrow { font-size: 14px; }

    .sa-note { background: #fffbeb; border: 1px solid #fcd34d; border-radius: 10px; padding: 12px 16px; font-size: 11px; color: #92400e; line-height: 1.5; margin-bottom: 16px; }

    .sa-compare { background: #fff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; }
    .sa-compare-title { padding: 20px 24px; font-size: 16px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #e2e8f0; }
    .sa-compare table { width: 100%; border-collapse: collapse; }
    .sa-compare th, .sa-compare td { padding: 12px 16px; text-align: left; font-size: 12px; border-bottom: 1px solid #f1f5f9; }
    .sa-compare th { color: #64748b; font-weight: 500; width: 25%; }
    .sa-compare td { font-weight: 600; color: #0f172a; width: 25%; }
    .sa-compare td.qw-col { color: #ea580c; }
    .sa-compare td.saas-col { color: #2563eb; }
    .sa-compare td.custom-col { color: #16a34a; }
    .sa-compare tr:last-child th, .sa-compare tr:last-child td { border-bottom: none; }
    .sa-compare thead th { font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; background: #f8fafc; }
    """

    # ── Quick Wins card ──
    qw_card = (
        '<div class="sa-card sa-card-qw">'
        '<div class="sa-card-icon">&#9889;</div>'
        '<div class="sa-card-label qw">QUICK WINS</div>'
        '<div class="sa-card-title">Optimise What You Have</div>'
        '<div class="sa-card-desc">Automations, configurations, and training that deliver value in days, not weeks. We work with your existing tools to unlock immediate improvements.</div>'
        '<div class="sa-card-metrics">'
        f'<div class="sa-metric"><div class="sa-metric-val">{n_qw}</div><div class="sa-metric-label">Quick wins identified</div></div>'
        f'<div class="sa-metric"><div class="sa-metric-val">~{qw_hrs:.0f} hrs/wk</div><div class="sa-metric-label">Time saved</div></div>'
        '</div>'
        f'<div class="sa-features"><div class="sa-features-title">Includes</div><ul>{qw_feature_items}</ul></div>'
        '<div class="sa-card-pros-cons">'
        '<div class="sa-pc-section"><div class="sa-pc-label pro">Strengths</div><ul class="sa-pc-list pro">'
        '<li>Lowest cost, fastest to implement</li>'
        '<li>No new tools &mdash; uses what you already have</li>'
        '<li>Immediate, measurable impact</li>'
        '<li>No ongoing subscription costs</li>'
        '</ul></div>'
        '<div class="sa-pc-section"><div class="sa-pc-label con">Trade-offs</div><ul class="sa-pc-list con">'
        '<li>Limited to what existing tools can do</li>'
        '<li>Data stays fragmented across systems</li>'
        '</ul></div>'
        '</div>'
        '<div class="sa-card-cta">'
        '<a href="priority-matrix.html" target="_blank" class="sa-btn sa-btn-qw">View Priority Matrix <span class="sa-btn-arrow">&rarr;</span></a>'
        '</div>'
        '</div>'
    )

    # ── SaaS Toolkit card ──
    saas_card = ""
    if has_saas:
        n_unique_tools = len(saas_features_seen)
        saas_card = (
            '<div class="sa-card sa-card-saas">'
            '<div class="sa-card-icon">&#127919;</div>'
            '<div class="sa-card-label saas">SAAS TOOLKIT</div>'
            '<div class="sa-card-title">Best-Fit Tools</div>'
            '<div class="sa-card-desc">The right tool for each business function, configured and connected with automation workflows to keep everything in sync.</div>'
            '<div class="sa-card-metrics">'
            f'<div class="sa-metric"><div class="sa-metric-val">{n_unique_tools}</div><div class="sa-metric-label">Tools configured</div></div>'
            f'<div class="sa-metric"><div class="sa-metric-val">~{saas_hrs:.0f} hrs/wk</div><div class="sa-metric-label">Time saved</div></div>'
            '</div>'
            f'<div class="sa-features"><div class="sa-features-title">Tools</div><ul>{saas_feature_items}</ul></div>'
            '<div class="sa-card-pros-cons">'
            '<div class="sa-pc-section"><div class="sa-pc-label pro">Strengths</div><ul class="sa-pc-list pro">'
            '<li>Proven products with vendor support</li>'
            '<li>Moderate upfront investment</li>'
            '<li>Automation workflows connect tools together</li>'
            '<li>Each tool is best-in-class for its function</li>'
            '</ul></div>'
            '<div class="sa-pc-section"><div class="sa-pc-label con">Trade-offs</div><ul class="sa-pc-list con">'
            '<li>Multiple logins and systems to manage</li>'
            '<li>Data spread across vendors</li>'
            '<li>Per-user pricing scales with headcount</li>'
            '</ul></div>'
            '</div>'
            '<div class="sa-card-cta">'
            '<a href="strategic-approaches-saas.html" target="_blank" class="sa-btn sa-btn-saas">View Toolkit Plan <span class="sa-btn-arrow">&rarr;</span></a>'
            '</div>'
            '</div>'
        )
    else:
        saas_card = (
            '<div class="sa-card">'
            '<div class="sa-card-icon">&#127919;</div>'
            '<div class="sa-card-label saas">SAAS TOOLKIT</div>'
            '<div class="sa-card-title">Best-Fit Tools</div>'
            '<div class="sa-card-desc">We\'re researching the best tools for each of your business functions. This option will appear here once ready.</div>'
            '<div class="sa-card-cta" style="margin-top:auto">'
            '<span class="sa-btn sa-btn-disabled">Coming Soon</span>'
            '</div>'
            '</div>'
        )

    # ── Custom Platform card ──
    custom_card = ""
    if has_custom:
        proto_btn = ""
        if proto_url:
            proto_btn = f'<a href="{escape(proto_url)}" target="_blank" class="sa-btn sa-btn-custom">Explore Prototype <span class="sa-btn-arrow">&rarr;</span></a>'
        else:
            proto_btn = '<span class="sa-btn sa-btn-disabled">Prototype in Progress</span>'

        custom_card = (
            '<div class="sa-card sa-card-custom">'
            '<div class="sa-card-icon">&#128187;</div>'
            '<div class="sa-card-label custom">CUSTOM PLATFORM</div>'
            '<div class="sa-card-title">Your Central Hub</div>'
            '<div class="sa-card-desc">A central system that connects to the tools that make sense &mdash; one place to manage contacts, scheduling, payroll, and more. '
            f'Instead of {n_unique_tools} separate logins, your team learns one simple system. Automations and AI features are built around it.</div>'
            '<div class="sa-card-metrics">'
            f'<div class="sa-metric"><div class="sa-metric-val">{n_modules}</div><div class="sa-metric-label">Modules</div></div>'
            f'<div class="sa-metric"><div class="sa-metric-val">~{all_hrs:.0f} hrs/wk</div><div class="sa-metric-label">Time saved</div></div>'
            '</div>'
            f'<div class="sa-features"><div class="sa-features-title">Modules</div><ul>{custom_feature_items}</ul></div>'
            '<div class="sa-card-pros-cons">'
            '<div class="sa-pc-section"><div class="sa-pc-label pro">Strengths</div><ul class="sa-pc-list pro">'
            f'<li>1 login instead of {n_unique_tools} &mdash; easier to train staff</li>'
            '<li>No per-user SaaS fees at scale</li>'
            '<li>No restrictions on automations or integrations</li>'
            '<li>Can be built in stages &mdash; start small, add over time</li>'
            '<li>Still connects to specialist tools where they make sense</li>'
            '</ul></div>'
            '<div class="sa-pc-section"><div class="sa-pc-label con">Trade-offs</div><ul class="sa-pc-list con">'
            '<li>Higher upfront investment</li>'
            '<li>Build timeline measured in sprints</li>'
            '</ul></div>'
            '</div>'
            f'{compliance_note}'
            '<div class="sa-card-cta">'
            f'{proto_btn}'
            '</div>'
            '</div>'
        )
    else:
        custom_card = (
            '<div class="sa-card">'
            '<div class="sa-card-icon">&#128187;</div>'
            '<div class="sa-card-label custom">CUSTOM PLATFORM</div>'
            '<div class="sa-card-title">Your Central Hub</div>'
            '<div class="sa-card-desc">We\'re designing a central platform tailored to your business. Architecture and prototype will appear here once ready.</div>'
            '<div class="sa-card-cta" style="margin-top:auto">'
            '<span class="sa-btn sa-btn-disabled">Coming Soon</span>'
            '</div>'
            '</div>'
        )

    # ── Comparison table (no prices) ──
    compare_html = (
        '<div class="sa-compare">'
        '<div class="sa-compare-title">How They Compare</div>'
        '<table>'
        '<thead><tr><th></th><th class="qw-col">Quick Wins</th><th class="saas-col">SaaS Toolkit</th><th class="custom-col">Custom Platform</th></tr></thead>'
        '<tbody>'
        f'<tr><th>Time saved</th><td class="qw-col">~{qw_hrs:.0f} hrs/wk</td><td class="saas-col">~{saas_hrs:.0f} hrs/wk</td><td class="custom-col">~{all_hrs:.0f} hrs/wk</td></tr>'
        '<tr><th>Timeline</th><td class="qw-col">Days</td><td class="saas-col">Weeks</td><td class="custom-col">Sprints (2-week cycles)</td></tr>'
        f'<tr><th>Systems to learn</th><td class="qw-col">Your existing tools</td><td class="saas-col">{n_unique_tools} separate logins</td><td class="custom-col">1 central system + specialist tools</td></tr>'
        f'<tr><th>Record keeping</th><td class="qw-col">No change</td><td class="saas-col">Update {n_unique_tools} separate systems</td><td class="custom-col">Enter data once</td></tr>'
        '<tr><th>Automations</th><td class="qw-col">Basic</td><td class="saas-col">Limited by vendor APIs</td><td class="custom-col">No restrictions</td></tr>'
        '<tr><th>Scaling</th><td class="qw-col">No change</td><td class="saas-col">Per-user fees grow</td><td class="custom-col">Fixed hosting cost</td></tr>'
        '<tr><th>Best for</th><td class="qw-col">Quick ROI from what you have</td><td class="saas-col">Right tool for each job</td><td class="custom-col">Simple central hub that connects everything</td></tr>'
        '</tbody></table>'
        '</div>'
    )

    return (
        '<!DOCTYPE html>\n<html lang="en"><head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<title>{company} &mdash; Your Options</title>\n'
        f'{BRAND_FAVICON}\n'
        f'<style>{css}</style>\n'
        '</head><body>\n'
        f'<div class="sa-header"><img src="{COMPANY_LOGO_URL}" alt="{YOUR_COMPANY}">'
        f'<div><div class="sa-header-title">{company} &mdash; Your Options</div>'
        f'<div class="sa-header-sub">Generated {generated}</div></div></div>\n'
        '<div class="sa-container">\n'
        '<div class="sa-hero">'
        '<h1>Three Ways Forward</h1>'
        '<p>Based on everything we discussed, here are three approaches to improve your operations &mdash; '
        'from quick automation wins to a fully unified platform. Each approach can work on its own or as a stepping stone to the next.</p>'
        '</div>\n'
        f'<div class="sa-cards">{qw_card}{saas_card}{custom_card}</div>\n'
        f'{compare_html}\n'
        '</div>\n'
        '</body></html>'
    )


def _sa_pipe_css():
    """Return CSS for the strategic approaches pipe page."""
    return """
  html { scroll-behavior: smooth; }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --pain-bg: #fef2f2; --pain-border: #fca5a5; --pain-text: #dc2626;
    --opp-bg: #f0fdf4; --opp-border: #86efac; --opp-text: #16a34a;
    --decision-bg: #fffbeb; --decision-border: #fcd34d; --decision-text: #92400e;
    --auto-bg: #eff6ff; --auto-border: #93c5fd; --auto-text: #1d4ed8;
  }
  body { background: #f7f9fc; font-family: 'Inter', -apple-system, sans-serif; color: #0f1825; min-height: 100vh; }
  .pipe-header { position: sticky; top: 0; z-index: 100; background: #0f1825; padding: 20px 24px 0; border-bottom: 3px solid #7DFF00; box-shadow: 0 4px 24px rgba(0,0,0,0.4); overflow: visible; }
  .pipe-header-top { display: flex; align-items: center; gap: 16px; padding-bottom: 16px; }
  .pipe-header-top .logo { font-size: 20px; font-weight: 800; color: #fff; }
  .pipe-header-top .sub { font-size: 13px; color: #9CA3AF; margin-top: 2px; }
  .sel-summary { margin-left: auto; font-size: 11px; color: #94a3b8; display: flex; gap: 16px; align-items: center; }
  .sel-val { color: #7DFF00; font-weight: 700; }
  .pipe-area { padding: 12px 24px 16px; position: relative; }
  .pipe { position: relative; height: 64px; border-radius: 32px; background: linear-gradient(to bottom, #2a4a6b 0%, #1e3a5f 15%, #15294a 50%, #1e3a5f 85%, #2a4a6b 100%); box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 2px 4px rgba(255,255,255,0.08), inset 0 -2px 4px rgba(0,0,0,0.3); display: flex; align-items: center; overflow: visible; }
  .pipe::before { content: ''; position: absolute; top: 4px; left: 32px; right: 32px; height: 10px; border-radius: 5px; background: linear-gradient(to bottom, rgba(125,255,0,0.1) 0%, transparent 100%); pointer-events: none; }
  .pipe::after { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 2px; transform: translateY(-50%); background: repeating-linear-gradient(90deg, transparent 0px, transparent 20px, rgba(125,255,0,0.12) 20px, rgba(125,255,0,0.12) 24px); animation: pipeflow 2s linear infinite; pointer-events: none; }
  @keyframes pipeflow { 0% { transform: translateY(-50%) translateX(0); } 100% { transform: translateY(-50%) translateX(24px); } }
  .pipe-segs { display: flex; width: 100%; height: 100%; position: relative; z-index: 2; }
  .pipe-seg { flex: 1; height: 100%; display: flex; align-items: center; justify-content: center; position: relative; cursor: pointer; transition: all 0.2s; border-right: 1px solid rgba(255,255,255,0.06); }
  .pipe-seg:last-child { border-right: none; }
  .pipe-seg:first-child { border-radius: 32px 0 0 32px; }
  .pipe-seg:last-child { border-radius: 0 32px 32px 0; }
  .pipe-seg:hover { background: rgba(125,255,0,0.1); }
  .pipe-seg.active { background: rgba(125,255,0,0.18); }
  .seg-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #94a3b8; text-align: center; line-height: 1.3; padding: 0 4px; pointer-events: none; transition: color 0.2s; }
  .pipe-seg:hover .seg-label, .pipe-seg.active .seg-label { color: #7DFF00; }
  .seg-badge { position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%); background: #7DFF00; color: #0f1825; font-size: 9px; font-weight: 800; padding: 2px 8px; border-radius: 10px; opacity: 0; transition: opacity 0.2s, transform 0.2s; white-space: nowrap; pointer-events: none; }
  .pipe-seg:hover .seg-badge { opacity: 1; transform: translateX(-50%) translateY(4px); }
  .seg-tt { position: absolute; top: calc(100% + 20px); left: 50%; transform: translateX(-50%) scale(0.95); background: #1a2332; border: 1px solid #2d3f52; border-radius: 12px; padding: 14px 18px; min-width: 220px; max-width: 280px; opacity: 0; pointer-events: none; transition: opacity 0.2s, transform 0.2s; box-shadow: 0 12px 40px rgba(0,0,0,0.5); z-index: 50; }
  .seg-tt::after { content: ''; position: absolute; top: -7px; left: 50%; transform: translateX(-50%) rotate(45deg); width: 12px; height: 12px; background: #1a2332; border-left: 1px solid #2d3f52; border-top: 1px solid #2d3f52; }
  .pipe-seg:hover .seg-tt { opacity: 1; transform: translateX(-50%) scale(1); pointer-events: auto; }
  .tt-title { font-size: 14px; font-weight: 800; color: #fff; margin-bottom: 3px; }
  .tt-sub { font-size: 11px; color: #64748b; margin-bottom: 10px; }
  .tt-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .tt-stat { text-align: center; padding: 6px; background: rgba(125,255,0,0.05); border-radius: 6px; border: 1px solid rgba(125,255,0,0.1); }
  .tt-stat-val { font-size: 16px; font-weight: 800; color: #7DFF00; }
  .tt-stat-lbl { font-size: 9px; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; }
  .tt-changes { margin-top: 8px; border-top: 1px solid #2d3f52; padding-top: 6px; }
  .tt-change { font-size: 10px; color: #94a3b8; padding: 2px 0; display: flex; align-items: center; gap: 5px; }
  .tt-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
  .tt-cta { margin-top: 6px; font-size: 10px; color: #7DFF00; font-weight: 600; text-align: center; opacity: 0.7; }
  .flow-labels { display: flex; justify-content: space-between; padding: 8px 0 0; }
  .flow-lbl { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #475569; display: flex; align-items: center; gap: 4px; }
  .flow-arrow { color: #7DFF00; font-size: 13px; }
  .cross-wrap { padding: 8px 0 0; }
  .cross-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #475569; margin-bottom: 6px; }
  .cross-bar { height: 36px; border-radius: 18px; background: linear-gradient(to bottom, rgba(139,92,246,0.22) 0%, rgba(139,92,246,0.12) 50%, rgba(139,92,246,0.22) 100%); border: 1px solid rgba(139,92,246,0.3); display: flex; align-items: center; justify-content: center; gap: 12px; cursor: pointer; transition: all 0.2s; }
  .cross-bar:hover { background: linear-gradient(to bottom, rgba(139,92,246,0.32) 0%, rgba(139,92,246,0.18) 50%, rgba(139,92,246,0.32) 100%); }
  .cross-bar.active { background: linear-gradient(to bottom, rgba(139,92,246,0.38) 0%, rgba(139,92,246,0.22) 50%, rgba(139,92,246,0.38) 100%); }
  .cross-text { font-size: 10px; font-weight: 700; color: #A78BFA; text-transform: uppercase; letter-spacing: 0.04em; }
  .cross-count { font-size: 9px; background: rgba(139,92,246,0.3); color: #C4B5FD; padding: 2px 8px; border-radius: 10px; font-weight: 700; }
  .detail-area { padding: 24px; }
  .stage-panel { animation: panelIn 0.3s ease; }
  @keyframes panelIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  .panel-close { background: none; border: 1px solid #e2e8f0; color: #64748b; border-radius: 6px; padding: 4px 12px; cursor: pointer; font-size: 16px; transition: all 0.15s; }
  .panel-close:hover { border-color: #7DFF00; color: #7DFF00; }
  .bp-zone { background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px 22px 24px; margin-bottom: 20px; box-shadow: 0 1px 8px rgba(15,24,37,0.06); }
  .bp-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .bp-col { min-width: 0; }
  .bp-col-header { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; }
  @media (max-width: 768px) { .bp-columns { grid-template-columns: 1fr; } }
  .stat-box { background: #fff; border: 1px solid #E5E7EB; border-radius: 10px; padding: 20px 16px; text-align: center; }
  .stat-val { font-size: 28px; font-weight: 800; color: #0f1825; letter-spacing: -0.03em; margin-bottom: 4px; }
  .stat-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; }
  .box { border-radius: 10px; padding: 12px 14px; font-size: 12px; line-height: 1.55; position: relative; box-shadow: 0 1px 4px rgba(0,0,0,0.06); transition: box-shadow 0.15s; }
  .box:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.10); }
  .box-title { font-weight: 600; font-size: 13px; margin-bottom: 4px; color: #0f1825; }
  .box-body { font-size: 12px; color: #374151; line-height: 1.6; }
  .step { background: #f7f9fc; border: 1px solid #e2e8f0; }
  .step-z1,.step-z2,.step-z3,.step-z4,.step-z5,.step-z6,.step-z7,.step-z8,.step-z9 { background:#f7f9fc; border:1px solid #e2e8f0; }
  .decision-box { background: var(--decision-bg); border: 2px dashed var(--decision-border); border-radius: 50px; text-align: center; }
  .decision-box .box-title { color: var(--decision-text); }
  .auto-box { background: var(--auto-bg); border: 1.5px solid var(--auto-border); }
  .auto-box .box-title { color: var(--auto-text); }
  .pain-box { background: var(--pain-bg); border: 1.5px solid var(--pain-border); }
  .pain-box .box-title { color: var(--pain-text); }
  .opp-box { background: var(--opp-bg); border: 1.5px solid var(--opp-border); }
  .opp-box .box-title { color: var(--opp-text); }
  .v-arrow { display:flex; flex-direction:column; align-items:center; margin: 3px 0; }
  .v-line { width:2px; background:#94a3b8; }
  .v-tip { width:0; height:0; border-left:5px solid transparent; border-right:5px solid transparent; border-top:7px solid #94a3b8; }
  .two-col { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
  .col { display:flex; flex-direction:column; align-items:center; }
  .col .box { width:100%; }
  .fork-label { font-size:10px; font-weight:700; color:white; border-radius:10px; padding:3px 10px; display:inline-block; margin-bottom:4px; }
  .fork-label.yes { background:#16a34a; }
  .fork-label.no { background:#dc2626; }
  .branch-yes-box { background:#f0fdf4; border:1.5px solid #86efac; }
  .branch-no-box { background:#fef2f2; border:1.5px solid #fca5a5; }
  .branch-yes-box .box-title { color:#15803d; }
  .branch-no-box .box-title { color:#dc2626; }
  .decision-gate { position: relative; margin: 4px 0; }
  .gate-merge-spacer { height: 16px; }
  .gate-condition { background: #fffbeb; border: 2px dashed #fcd34d; border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600; color: #92400e; text-align: center; }
  .person-tag { background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 11px; padding: 3px 10px; display: inline-block; margin-top: 2px; }
  .step-tools { margin-top:4px; display:flex; flex-wrap:wrap; gap:3px; }
  .step-tool-tag { display:inline-block; font-size:11px; font-weight:600; background:#f0fdf4; color:#166534; border:1px solid #bbf7d0; padding:1px 7px; border-radius:10px; }
  .step-meta { margin-top:5px; display:flex; flex-wrap:wrap; gap:4px; }
  .meta-chip { font-size:10px; font-weight:600; color:#64748b; background:#f1f5f9; border:1px solid #e2e8f0; padding:1px 7px; border-radius:8px; }
  .pg-label { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#9CA3AF; text-align:center; margin-bottom:6px; }
  .pg-container { border:1px dashed #cbd5e1; border-radius:10px; padding:12px; margin-bottom:6px; background:rgba(241,245,249,0.5); }
  .pg-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; margin: 4px 0; }
  .pg-chip { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 12px; font-size: 11px; font-weight: 600; color: #0f1825; text-align: center; min-width: 60px; flex: 1 1 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
  .pg-chip .chip-tool { display: block; font-size: 9px; font-weight: 600; color: #166634; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 1px 6px; margin-top: 3px; }
  .pg-chip .chip-owner { display: block; font-size: 9px; margin-top: 3px; }
  .pg-chip .chip-dropdown { display: block; margin-top: 4px; }
  .pg-chip .chip-dropdown > summary { display: inline-flex; align-items: center; gap: 3px; font-size: 9px; color: #5B4FCF; cursor: pointer; list-style: none; opacity: 0.7; }
  .pg-chip .chip-dropdown > summary::-webkit-details-marker { display: none; }
  .pg-chip:hover .chip-dropdown > summary { opacity: 1; }
  .pg-chip .chip-panel { margin-top: 4px; background: rgba(91,79,207,0.06); border: 1px solid rgba(91,79,207,0.2); border-radius: 6px; padding: 5px 8px; display: flex; flex-direction: column; gap: 5px; text-align: left; }
  .pg-chip .chip-excerpt { font-size: 9px; font-style: italic; color: #5B4FCF; border-left: 2px solid rgba(91,79,207,0.3); padding-left: 5px; margin: 0; line-height: 1.4; }
  .pg-chip .chip-open-btn { align-self: flex-start; font-size: 9px; font-weight: 700; color: #5B4FCF; text-decoration: none; background: rgba(91,79,207,0.1); border: 1px solid rgba(91,79,207,0.25); border-radius: 4px; padding: 1px 6px; }
  .pg-merge { display: flex; flex-direction: column; align-items: center; }
  .pg-legs { display: flex; justify-content: center; width: 100%; }
  .pg-leg { flex: 1; display: flex; justify-content: center; }
  .pg-leg .v-line { height: 10px; width: 2px; background: #94a3b8; }
  .pg-crossbar { height: 2px; background: #94a3b8; }
  .pg-drop { display: flex; flex-direction: column; align-items: center; }
  .pg-drop .v-line { height: 10px; width: 2px; background: #94a3b8; }
  .pg-drop .v-tip { width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 7px solid #94a3b8; }
  .process-step { position: relative; margin-bottom: 6px; }
  .labeled-arrow { margin: 2px 0; }
  .flow-label { font-size: 9px; font-weight: 700; padding: 2px 8px; border-radius: 10px; border: 1.5px solid; background: #fff; white-space: nowrap; }
  .email-link { display: inline-block; font-size: 9px; font-weight: 600; color: #1a7f5a; text-decoration: none; background: rgba(26,127,90,0.08); border: 1px solid rgba(26,127,90,0.2); border-radius: 4px; padding: 2px 6px; white-space: nowrap; }
  .email-link:hover { background: rgba(26,127,90,0.15); text-decoration: underline; }
  .sa-change-card { border: 2px solid #e2e8f0; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px; font-size: 12px; position: relative; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
  .sa-change-badge { position: absolute; top: 10px; right: 10px; color: #fff; font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 3px; letter-spacing: 0.02em; }
  .sa-change-title { font-weight: 700; font-size: 14px; color: #0f1825; padding-right: 90px; margin-bottom: 6px; }
  .sa-change-steps { margin-bottom: 4px; }
  .sa-tool-options { margin-top: 10px; }
  .sa-tool-options-header { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 6px; }
  .sa-tool-option { border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin-bottom: 6px; cursor: pointer; transition: all 0.15s; background: #fff; }
  .sa-tool-option:hover { border-color: #94a3b8; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  .sa-tool-option.selected { border-color: #7DFF00; background: rgba(125,255,0,0.04); box-shadow: 0 0 0 1px #7DFF00; }
  .sa-tool-header { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .sa-tool-name { font-weight: 700; font-size: 13px; color: #0f1825; }
  .sa-tool-cost { font-size: 12px; font-weight: 700; color: #166534; background: #D1FAE5; padding: 1px 8px; border-radius: 4px; margin-left: auto; }
  .sa-rec-badge { font-size: 9px; font-weight: 700; color: #166534; background: rgba(125,255,0,0.2); border: 1px solid rgba(125,255,0,0.4); padding: 1px 6px; border-radius: 3px; text-transform: uppercase; letter-spacing: 0.04em; }
  .sa-tool-rating { font-size: 10px; color: #64748b; }
  .sa-tool-pricing { font-size: 11px; color: #64748b; margin-top: 3px; }
  .sa-tool-caveat { font-size: 10px; color: #B45309; margin-top: 3px; background: #FFFBEB; padding: 3px 6px; border-radius: 4px; }
  .sa-tool-expand { margin-top: 4px; }
  .sa-tool-expand summary { font-size: 10px; color: #3B82F6; cursor: pointer; font-weight: 600; }
  .sa-tool-expand-body { font-size: 11px; color: #475569; margin-top: 4px; padding: 8px; background: #f7f9fc; border-radius: 6px; }
  .sa-det-sec { margin-bottom: 6px; }
  .sa-det-sec strong { font-size: 10px; text-transform: uppercase; color: #64748b; letter-spacing: 0.04em; }
  .sa-det-sec ul { margin: 2px 0 0 14px; font-size: 11px; }
  .sa-det-sec li { margin-bottom: 2px; }
"""


def _sa_pipe_js(n_total):
    """Return JavaScript for the strategic approaches pipe page."""
    return """
var activeStage = null;

function toggleStage(stage) {
  var panels = document.querySelectorAll('.stage-panel');
  var segs = document.querySelectorAll('.pipe-seg');
  var crossBar = document.querySelector('.cross-bar');
  if (activeStage === stage) { closeDetail(); return; }
  panels.forEach(function(p) { p.style.display = 'none'; });
  segs.forEach(function(s) { s.classList.remove('active'); });
  if (crossBar) crossBar.classList.remove('active');
  var panel = document.getElementById('panel-' + stage);
  if (panel) {
    panel.style.display = 'block';
    activeStage = stage;
    var seg = document.querySelector('[data-stage="' + stage + '"]');
    if (seg) seg.classList.add('active');
    if (stage === 'cross-process' && crossBar) crossBar.classList.add('active');
    setTimeout(function() { panel.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 100);
  }
}

function closeDetail() {
  document.querySelectorAll('.stage-panel').forEach(function(p) { p.style.display = 'none'; });
  document.querySelectorAll('.pipe-seg').forEach(function(s) { s.classList.remove('active'); });
  var cb = document.querySelector('.cross-bar');
  if (cb) cb.classList.remove('active');
  activeStage = null;
}

// Tooltip clipping fix
document.querySelectorAll('.pipe-seg').forEach(function(seg) {
  seg.addEventListener('mouseenter', function() {
    var tt = seg.querySelector('.seg-tt');
    if (!tt) return;
    tt.style.left = '50%'; tt.style.right = ''; tt.style.transform = 'translateX(-50%) scale(1)';
    var rect = tt.getBoundingClientRect();
    if (rect.left < 8) { tt.style.left = '0'; tt.style.transform = 'translateX(0) scale(1)'; tt.querySelector(':after') && (tt.style.setProperty('--arrow-left', (seg.getBoundingClientRect().left - rect.left + seg.offsetWidth/2) + 'px')); }
    else if (rect.right > window.innerWidth - 8) { tt.style.left = 'auto'; tt.style.right = '0'; tt.style.transform = 'translateX(0) scale(1)'; }
  });
  seg.addEventListener('mouseleave', function() {
    var tt = seg.querySelector('.seg-tt');
    if (!tt) return;
    tt.style.left = '50%'; tt.style.right = ''; tt.style.transform = 'translateX(-50%) scale(0.95)';
  });
});
"""


def main():
    parser = argparse.ArgumentParser(description="HTML deliverable generator")
    parser.add_argument("--client-slug", required=True, help="Client slug (matches clients/ folder name)")
    parser.add_argument("--output", required=True,
                        choices=["process-map", "priority-matrix", "transformation-blueprint", "audit-report", "audit-report-print", "client-website", "findings", "waste", "solutions-overview", "strategic-approaches", "strategic-approaches-saas", "all"],
                        help="Which output to generate")
    args = parser.parse_args()

    ssad = load_audit_data(args.client_slug)
    out_dir = ensure_deliverables_dir(args.client_slug)
    sections = load_client_sections(args.client_slug)
    generated = []

    targets = (
        ["process-map", "findings", "waste", "client-website"]
        if args.output == "all" else [args.output]
    )

    generators = {
        "process-map": (generate_process_map, "process-map.html"),
        "priority-matrix": (generate_priority_matrix, "priority-matrix.html"),
        "transformation-blueprint": (generate_transformation_blueprint, "transformation-blueprint.html"),
        "audit-report": (generate_audit_report, "audit-report.html"),
        "audit-report-print": (generate_audit_report_print, "audit-report-print.html"),
        "client-website": (lambda s: generate_client_website(s, sections), "client-website.html"),
        "findings": (generate_findings_partial, "findings.html"),
        "waste": (generate_waste_partial, "waste.html"),
        "solutions-overview": (generate_solutions_overview, "solutions-overview.html"),
        "strategic-approaches": (generate_options_pricing, "strategic-approaches.html"),
        "strategic-approaches-saas": (generate_strategic_approaches, "strategic-approaches-saas.html"),
    }

    for target in targets:
        fn, filename = generators[target]
        html = fn(ssad)
        path = out_dir / filename
        path.write_text(html, encoding="utf-8")
        generated.append(str(path))
        print(f"Generated: {path}")

    result = {
        "status": "ok",
        "client_slug": args.client_slug,
        "generated": generated,
        "company_name": ssad.get("company_name", ""),
        "audit_status": ssad.get("audit_status", ""),
        "sessions_completed": ssad.get("sessions_completed", 0),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
