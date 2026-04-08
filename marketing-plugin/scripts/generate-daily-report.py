#!/usr/bin/env python3
"""generate-daily-report.py — Build daily Meta ad performance report.

Supports multiple campaigns, dynamic winner/loser thresholds (percentile-based),
ROAS calculation from action values, and actionable recommendations.
"""
import argparse, json, math, sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent
DATA_PATH = PLUGIN_ROOT / "data" / "marketing-data.json"
TEMPLATE_PATH = PLUGIN_ROOT / "templates" / "daily-report.html"


def load_data():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found", file=sys.stderr); sys.exit(1)
    with open(DATA_PATH) as f:
        return json.load(f)


def aggregate(insights, start, end, level):
    by_id = defaultdict(lambda: {"spend":0.0,"impressions":0,"clicks":0,"reach":0,
                                  "conversions":0,"frequency_sum":0.0,"freq_count":0,
                                  "action_values":0.0})
    for i in insights:
        if i.get("entity_type") != level: continue
        d = i.get("date","")
        if not (start <= d <= end): continue
        eid = i.get("entity_id")
        r = by_id[eid]
        r["spend"] += float(i.get("spend",0))
        r["impressions"] += int(i.get("impressions",0))
        r["clicks"] += int(i.get("clicks",0))
        r["reach"] += int(i.get("reach",0))
        r["conversions"] += int(i.get("conversions",0))
        f = float(i.get("frequency",0))
        if f > 0:
            r["frequency_sum"] += f
            r["freq_count"] += 1
        # Sum action values for ROAS (purchase, lead values)
        for action in (i.get("actions") or []):
            if action.get("action_type") in ("purchase", "offsite_conversion.fb_pixel_purchase"):
                r["action_values"] += float(action.get("value", 0))
    for r in by_id.values():
        r["ctr"] = (r["clicks"]/r["impressions"]*100) if r["impressions"] else 0
        r["cpc"] = (r["spend"]/r["clicks"]) if r["clicks"] else 0
        r["cpm"] = (r["spend"]/r["impressions"]*1000) if r["impressions"] else 0
        r["cpa"] = (r["spend"]/r["conversions"]) if r["conversions"] else 0
        r["frequency_avg"] = (r["frequency_sum"]/r["freq_count"]) if r["freq_count"] else 0
        r["roas"] = (r["action_values"]/r["spend"]) if r["spend"] > 0 and r["action_values"] > 0 else 0
    return by_id


def totals(insights, start, end, level="campaign"):
    t = {"spend":0.0,"impressions":0,"clicks":0,"reach":0,"conversions":0,"action_values":0.0}
    for i in insights:
        if i.get("entity_type") != level: continue
        d = i.get("date","")
        if not (start <= d <= end): continue
        t["spend"] += float(i.get("spend",0))
        t["impressions"] += int(i.get("impressions",0))
        t["clicks"] += int(i.get("clicks",0))
        t["reach"] += int(i.get("reach",0))
        t["conversions"] += int(i.get("conversions",0))
        for action in (i.get("actions") or []):
            if action.get("action_type") in ("purchase", "offsite_conversion.fb_pixel_purchase"):
                t["action_values"] += float(action.get("value", 0))
    t["ctr"] = (t["clicks"]/t["impressions"]*100) if t["impressions"] else 0
    t["cpc"] = (t["spend"]/t["clicks"]) if t["clicks"] else 0
    t["cpm"] = (t["spend"]/t["impressions"]*1000) if t["impressions"] else 0
    t["cpa"] = (t["spend"]/t["conversions"]) if t["conversions"] else 0
    t["roas"] = (t["action_values"]/t["spend"]) if t["spend"] > 0 and t["action_values"] > 0 else 0
    return t


def daily_series(insights, start, end, level="campaign"):
    daily = defaultdict(lambda: {"spend":0.0,"impressions":0,"clicks":0,"reach":0,"conversions":0})
    for i in insights:
        if i.get("entity_type") != level: continue
        d = i.get("date","")
        if not (start <= d <= end): continue
        daily[d]["spend"] += float(i.get("spend",0))
        daily[d]["impressions"] += int(i.get("impressions",0))
        daily[d]["clicks"] += int(i.get("clicks",0))
        daily[d]["reach"] += int(i.get("reach",0))
        daily[d]["conversions"] += int(i.get("conversions",0))
    for r in daily.values():
        r["ctr"] = (r["clicks"]/r["impressions"]*100) if r["impressions"] else 0
        r["cpc"] = (r["spend"]/r["clicks"]) if r["clicks"] else 0
        r["cpm"] = (r["spend"]/r["impressions"]*1000) if r["impressions"] else 0
    return dict(sorted(daily.items()))


def pct_change(c, p):
    if p == 0: return 0 if c == 0 else 100
    return (c-p)/p*100


def percentile(values, pct):
    """Calculate the pct-th percentile from a sorted list of values."""
    if not values:
        return 0
    s = sorted(values)
    k = (len(s) - 1) * (pct / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] * (c - k) + s[c] * (k - f)


def compute_thresholds(ads_data):
    """Compute dynamic winner/loser thresholds from account performance data.

    Returns dict with CTR and CPC thresholds based on 25th/75th percentiles.
    Ads with <$5 spend are excluded from threshold calculation.
    """
    ctrs = [v["ctr"] for v in ads_data.values() if v["spend"] >= 5]
    cpcs = [v["cpc"] for v in ads_data.values() if v["spend"] >= 5 and v["clicks"] > 0]

    if not ctrs or not cpcs:
        # Fallback to reasonable defaults if not enough data
        return {"ctr_winner": 2.0, "ctr_loser": 1.0, "cpc_winner": 2.50, "cpc_loser": 4.00}

    return {
        "ctr_winner": percentile(ctrs, 75),   # Top 25% CTR = winner
        "ctr_loser": percentile(ctrs, 25),     # Bottom 25% CTR = loser
        "cpc_winner": percentile(cpcs, 25),    # Bottom 25% CPC = winner (lower is better)
        "cpc_loser": percentile(cpcs, 75),     # Top 25% CPC = loser (higher is worse)
    }


def classify(r, thresholds):
    flags = []
    if r["frequency_avg"] > 3.0: flags.append("fatigued")
    if r["spend"] < 5: return "low-spend", flags
    if r["ctr"] >= thresholds["ctr_winner"] and r["cpc"] <= thresholds["cpc_winner"]:
        return "winner", flags
    if r["ctr"] < thresholds["ctr_loser"] or r["cpc"] > thresholds["cpc_loser"]:
        return "loser", flags
    return "okay", flags


def generate_recommendations(ad_rows, thresholds):
    """Generate actionable recommendations based on ad performance."""
    recs = []

    winners = [r for r in ad_rows if r["status_class"] == "winner"]
    losers = [r for r in ad_rows if r["status_class"] == "loser" and r["spend"] >= 10]
    fatigued = [r for r in ad_rows if "fatigued" in r.get("flags", [])]

    if losers:
        loser_names = [r["name"] for r in sorted(losers, key=lambda x: x["spend"], reverse=True)[:5]]
        total_loser_spend = sum(r["spend"] for r in losers)
        recs.append({
            "type": "pause",
            "priority": "high",
            "message": f"Consider pausing {len(losers)} underperforming ads (${total_loser_spend:.2f} wasted this week)",
            "ads": loser_names
        })

    if winners:
        winner_names = [r["name"] for r in sorted(winners, key=lambda x: x["ctr"], reverse=True)[:5]]
        recs.append({
            "type": "scale",
            "priority": "medium",
            "message": f"{len(winners)} ads performing well — consider increasing budget",
            "ads": winner_names
        })

    if fatigued:
        fatigued_names = [r["name"] for r in fatigued[:5]]
        recs.append({
            "type": "refresh",
            "priority": "medium",
            "message": f"{len(fatigued)} ads showing fatigue (frequency > 3.0) — refresh creative or narrow audience",
            "ads": fatigued_names
        })

    no_conversions = [r for r in ad_rows if r["spend"] >= 20 and r["conversions"] == 0]
    if no_conversions:
        recs.append({
            "type": "investigate",
            "priority": "high",
            "message": f"{len(no_conversions)} ads with $20+ spend and zero conversions — check landing page or tracking",
            "ads": [r["name"] for r in no_conversions[:5]]
        })

    return recs


def build_payload(data):
    meta = data["meta"]
    ads = {a["ad_id"]: a for a in meta["ads"]}
    insights = meta["insights"]
    campaigns = meta["campaigns"]

    # Build campaign name map
    campaign_names = {c["campaign_id"]: c["name"] for c in campaigns}

    ad_dates = [i["date"] for i in insights if i.get("entity_type") == "ad"]
    camp_dates = [i["date"] for i in insights if i.get("entity_type") == "campaign"]
    latest = max(ad_dates) if ad_dates else (max(camp_dates) if camp_dates else None)
    if not latest:
        print("Error: no insights", file=sys.stderr); sys.exit(1)

    dt = datetime.strptime(latest, "%Y-%m-%d")
    week_start = (dt - timedelta(days=6)).strftime("%Y-%m-%d")
    pw_start = (dt - timedelta(days=13)).strftime("%Y-%m-%d")
    pw_end = (dt - timedelta(days=7)).strftime("%Y-%m-%d")
    m_start = (dt - timedelta(days=29)).strftime("%Y-%m-%d")

    y = totals(insights, latest, latest)
    w = totals(insights, week_start, latest)
    pw = totals(insights, pw_start, pw_end)

    # Per-campaign breakdowns
    campaign_breakdowns = {}
    for campaign in campaigns:
        cid = campaign["campaign_id"]
        campaign_breakdowns[cid] = {
            "name": campaign["name"],
            "week": totals(
                [i for i in insights if i.get("entity_id") == cid or
                 (i.get("entity_type") == "campaign" and i.get("entity_id") == cid)],
                week_start, latest, "campaign"
            ),
        }

    has_ad = any(i.get("entity_type") == "ad" for i in insights)
    msg = ""
    if has_ad:
        ads_w = aggregate(insights, week_start, latest, "ad")
        ads_pw = aggregate(insights, pw_start, pw_end, "ad")
        # Compute dynamic thresholds from this week's data
        thresholds = compute_thresholds(ads_w)
    else:
        ads_w, ads_pw = {}, {}
        thresholds = {"ctr_winner": 2.0, "ctr_loser": 1.0, "cpc_winner": 2.50, "cpc_loser": 4.00}
        msg = "Ad-level insights not yet synced. Run fetch-meta-campaigns.py --level ad."

    rows = []
    for ad_id, m in ads_w.items():
        ad = ads.get(ad_id, {})
        status_class, flags = classify(m, thresholds)
        prev = ads_pw.get(ad_id, {})
        ctr_ch = pct_change(m["ctr"], prev.get("ctr", 0)) if prev.get("ctr") else None
        rows.append({"ad_id":ad_id, "name":ad.get("name",f"Ad {ad_id}"),
                     "status":ad.get("status","UNKNOWN"), "creative_id":ad.get("creative_id"),
                     "status_class":status_class, "flags":flags, "ctr_change":ctr_ch, **m})
    rows.sort(key=lambda r: r["spend"], reverse=True)

    # Generate recommendations
    recommendations = generate_recommendations(rows, thresholds)

    return {"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "data_through": latest, "yesterday": y, "week": w, "prev_week": pw,
            "ad_rows": rows,
            "daily_30": [{"date":d, **v} for d, v in daily_series(insights, m_start, latest).items()],
            "ad_level_msg": msg,
            "campaigns": campaign_breakdowns,
            "campaign_count": len(campaigns),
            "thresholds": thresholds,
            "recommendations": recommendations}


def render_html(payload):
    tmpl = TEMPLATE_PATH.read_text()
    return tmpl.replace("__DATA__", json.dumps(payload, default=str))


def print_summary(p):
    w, y = p["week"], p["yesterday"]
    print("─"*60)
    print(f"Meta Daily Report · {p['data_through']}")
    if p["campaign_count"] > 1:
        print(f"Campaigns: {p['campaign_count']}")
    print("─"*60)
    print(f"Yesterday: ${y['spend']:.2f} | {y['impressions']:,} impr | {y['clicks']} clicks | "
          f"CTR {y['ctr']:.2f}% | CPC ${y['cpc']:.2f} | {y['conversions']} conv"
          + (f" | ROAS {y['roas']:.2f}x" if y.get('roas', 0) > 0 else ""))
    print(f"7-day:     ${w['spend']:.2f} | {w['impressions']:,} impr | {w['clicks']} clicks | "
          f"CTR {w['ctr']:.2f}% | CPC ${w['cpc']:.2f} | {w['conversions']} conv"
          + (f" | ROAS {w['roas']:.2f}x" if w.get('roas', 0) > 0 else ""))

    # Per-campaign breakdown (if multiple)
    if p["campaign_count"] > 1:
        print("\nPer-campaign (7-day):")
        for cid, cd in p["campaigns"].items():
            cw = cd["week"]
            print(f"  {cd['name']}: ${cw['spend']:.2f} | CTR {cw['ctr']:.2f}% | CPC ${cw['cpc']:.2f}")

    if p["ad_rows"]:
        winners = sum(1 for r in p["ad_rows"] if r["status_class"] == "winner")
        losers = sum(1 for r in p["ad_rows"] if r["status_class"] == "loser")
        fatigued = sum(1 for r in p["ad_rows"] if "fatigued" in r.get("flags", []))
        t = p["thresholds"]
        print(f"\nAds: {len(p['ad_rows'])} | {winners} winners | {losers} losers | {fatigued} fatigued")
        print(f"Thresholds: Winner CTR >= {t['ctr_winner']:.2f}% & CPC <= ${t['cpc_winner']:.2f} | "
              f"Loser CTR < {t['ctr_loser']:.2f}% or CPC > ${t['cpc_loser']:.2f}")

    if p.get("recommendations"):
        print("\nRecommendations:")
        for rec in p["recommendations"]:
            priority_icon = "!" if rec["priority"] == "high" else "-"
            print(f"  {priority_icon} [{rec['type'].upper()}] {rec['message']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args()

    out_dir = Path(args.output_dir) if args.output_dir else PLUGIN_ROOT / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = out_dir / f"meta-daily-report-{today}.html"
    latest_path = out_dir / "meta-daily-report-latest.html"

    data = load_data()
    payload = build_payload(data)
    html = render_html(payload)
    out_path.write_text(html)
    latest_path.write_text(html)
    print_summary(payload)
    print(f"\nReport:    {out_path}")
    print(f"Latest:    {latest_path}")


if __name__ == "__main__":
    main()
