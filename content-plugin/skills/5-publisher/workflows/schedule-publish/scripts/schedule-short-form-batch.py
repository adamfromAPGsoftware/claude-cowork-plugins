#!/usr/bin/env python3
"""
One-off batch scheduler for short-form videos across TikTok/Instagram/YouTube via Late.dev.
Reads video captions from script markdown files, uploads videos via presigned URL,
and creates scheduled posts with lead magnet first-comments.

Usage: edit CONFIG block, then run. Dry-run by default.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ---- CONFIG ----------------------------------------------------------------

DRY_RUN = False  # set True to print payloads without calling API
API_BASE = "https://getlate.dev/api/v1"
LATE_API_KEY = os.environ["LATE_API_KEY"]

PROJECT_ROOT = Path("{PROJECT_ROOT}")
RENDERS_DIR = PROJECT_ROOT / "content/projects/2026-04-02-apg-ai-business-system/video-editor/short-form/renders"
SCRIPTS_DIR = PROJECT_ROOT / "content/projects/2026-04-02-apg-ai-business-system/video-editor/short-form/scripts"

ACCOUNTS = {
    "tiktok":    "6962db684207e06f4ca84bdb",  # {YOUR_HANDLE_DOT}
    "instagram": "695966304207e06f4ca83ae2",  # {YOUR_HANDLE_DOT} (personal)
    "youtube":   "{LATE_YOUTUBE_CHANNEL_ID}",  # example-account
}

# AEST = UTC+10. ISO times in UTC.
VIDEOS = [
    # (id, date AEST,       keyword,  tiktok_hm, insta_hm, yt_hm)
    ("sf-01", "2026-04-06", "RESULTS",  "18:00", "13:00", "15:00"),
    ("sf-02", "2026-04-08", "CLAUDE",   "07:00", "13:00", "10:00"),
    ("sf-03", "2026-04-10", "AGENT",    "07:00", "13:00", "10:00"),
    ("sf-04", "2026-04-13", "AUTOMATE", "07:00", "13:00", "10:00"),
    ("sf-05", "2026-04-15", "BUILD",    "07:00", "13:00", "10:00"),
]

# ---- HELPERS ---------------------------------------------------------------

def aest_to_utc_iso(date_str, hm):
    """2026-04-06, 07:00 AEST -> 2026-04-05T21:00:00.000Z"""
    from datetime import datetime, timedelta, timezone
    h, m = map(int, hm.split(":"))
    y, mo, d = map(int, date_str.split("-"))
    local = datetime(y, mo, d, h, m, tzinfo=timezone(timedelta(hours=10)))
    utc = local.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def http(method, url, headers=None, body=None, raw_body=None):
    headers = headers or {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif raw_body is not None:
        data = raw_body
    else:
        data = None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")

def auth_headers():
    return {"Authorization": f"Bearer {LATE_API_KEY}"}

def parse_script(sf_id):
    """Parse script markdown for Instagram caption, TikTok caption, YouTube title+description."""
    path = SCRIPTS_DIR / f"{sf_id}-script.md"
    text = path.read_text()

    def extract_section(header):
        idx = text.find(f"### {header}")
        if idx == -1:
            return None
        nxt = text.find("\n### ", idx + 1)
        end = text.find("\n---", idx + 1)
        stop = min(x for x in [nxt, end, len(text)] if x != -1)
        return text[idx:stop]

    ig_sec = extract_section("Instagram Reel") or ""
    tt_sec = extract_section("TikTok") or ""
    yt_sec = extract_section("YouTube Shorts") or ""

    def after_label(section, label):
        """Grab text after '**Label:**' until the next '**X:**' or end."""
        i = section.find(f"**{label}:**")
        if i == -1:
            return ""
        i += len(f"**{label}:**")
        # find next **word:** block
        import re
        m = re.search(r"\n\*\*[A-Z][a-zA-Z ]+:\*\*", section[i:])
        end = i + m.start() if m else len(section)
        return section[i:end].strip()

    ig_caption = after_label(ig_sec, "Caption")
    if not ig_caption:
        # caption is everything after "### Instagram Reel\n\n**Caption:**"
        parts = ig_sec.split("**Caption:**", 1)
        ig_caption = parts[1].strip() if len(parts) > 1 else ""
    # strip trailing hashtag line kept — it's part of IG caption
    tt_body = tt_sec.split("\n", 1)[1].strip() if "\n" in tt_sec else tt_sec
    # remove "### TikTok" header
    tt_body = tt_body.lstrip()

    yt_title = after_label(yt_sec, "Title").strip('"')
    yt_desc = after_label(yt_sec, "Description")

    return {
        "ig_caption": ig_caption.strip(),
        "tt_caption": tt_body.strip(),
        "yt_title": yt_title.strip(),
        "yt_description": yt_desc.strip(),
    }

def upload_video(sf_id):
    path = RENDERS_DIR / f"{sf_id}.mp4"
    size = path.stat().st_size
    print(f"  [upload] {sf_id}.mp4 ({size/1024/1024:.1f} MB)...", flush=True)
    # 1) presign
    status, body = http("POST", f"{API_BASE}/media/presign",
                        headers=auth_headers(),
                        body={"filename": f"{sf_id}.mp4", "contentType": "video/mp4", "size": size})
    if status >= 300:
        print(f"  ERROR presign: {status} {body}")
        sys.exit(1)
    pre = json.loads(body)
    # 2) PUT file to R2 via curl (handles large uploads reliably)
    print(f"  [upload] PUT to R2 via curl...", flush=True)
    import subprocess
    result = subprocess.run(
        ["curl", "-s", "-w", "%{http_code}", "-o", "/dev/null",
         "-X", "PUT", pre["uploadUrl"],
         "--data-binary", f"@{path}"],
        capture_output=True, text=True, timeout=600
    )
    code = result.stdout.strip()
    if not code.startswith("2"):
        print(f"  ERROR R2 PUT: HTTP {code}\n{result.stderr}")
        sys.exit(1)
    print(f"  [upload] done → {pre['publicUrl']}", flush=True)
    return pre["publicUrl"]

def lead_magnet_comment(keyword):
    return (f"Comment {keyword} below and I'll DM you the resource. "
            f"(Or DM me directly if comments don't notify me — happens often.)")

def build_posts(sf_id, video_url, date_str, keyword, tt_hm, ig_hm, yt_hm, copy):
    posts = []

    # TikTok
    posts.append({
        "platform": "tiktok",
        "scheduledFor": aest_to_utc_iso(date_str, tt_hm),
        "title": f"{sf_id.upper()} — TikTok ({keyword})",
        "payload": {
            "content": copy["tt_caption"],
            "platforms": [{
                "platform": "tiktok",
                "accountId": ACCOUNTS["tiktok"],
                "platformSpecificData": {
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "content_preview_confirmed": True,
                    "express_consent_given": True,
                    "video_cover_timestamp_ms": 0,
                },
            }],
            "mediaItems": [{"type": "video", "url": video_url}],
            "scheduledFor": aest_to_utc_iso(date_str, tt_hm),
            "title": f"{sf_id.upper()} — TikTok ({keyword})",
        },
    })

    # Instagram Reel
    posts.append({
        "platform": "instagram",
        "scheduledFor": aest_to_utc_iso(date_str, ig_hm),
        "title": f"{sf_id.upper()} — Instagram Reel ({keyword})",
        "payload": {
            "content": copy["ig_caption"],
            "platforms": [{
                "platform": "instagram",
                "accountId": ACCOUNTS["instagram"],
                "platformSpecificData": {
                    "contentType": "reels",
                    "firstComment": lead_magnet_comment(keyword),
                },
            }],
            "mediaItems": [{"type": "video", "url": video_url}],
            "scheduledFor": aest_to_utc_iso(date_str, ig_hm),
            "title": f"{sf_id.upper()} — Instagram Reel ({keyword})",
        },
    })

    # YouTube Shorts
    yt_desc = copy["yt_description"]
    posts.append({
        "platform": "youtube",
        "scheduledFor": aest_to_utc_iso(date_str, yt_hm),
        "title": f"{sf_id.upper()} — YouTube Short ({keyword})",
        "payload": {
            "content": yt_desc,
            "platforms": [{
                "platform": "youtube",
                "accountId": ACCOUNTS["youtube"],
                "platformSpecificData": {
                    "title": copy["yt_title"],
                    "privacyStatus": "public",
                    "madeForKids": False,
                    "firstComment": lead_magnet_comment(keyword),
                },
            }],
            "mediaItems": [{"type": "video", "url": video_url}],
            "scheduledFor": aest_to_utc_iso(date_str, yt_hm),
            "title": f"{sf_id.upper()} — YouTube Short ({keyword})",
        },
    })

    return posts

def schedule_post(post):
    status, body = http("POST", f"{API_BASE}/posts",
                        headers=auth_headers(), body=post["payload"])
    if status >= 300:
        print(f"  [FAIL] {post['title']} — {status}: {body[:400]}")
        return None
    resp = json.loads(body)
    post_id = resp.get("post", {}).get("_id") or resp.get("_id") or "?"
    print(f"  [OK] {post['title']} → {post_id}")
    return resp

# ---- MAIN ------------------------------------------------------------------

def main():
    results = []
    for (sf_id, date_str, keyword, tt_hm, ig_hm, yt_hm) in VIDEOS:
        print(f"\n=== {sf_id.upper()} ({keyword}) — {date_str} ===")
        copy = parse_script(sf_id)
        print(f"  IG cap: {copy['ig_caption'][:80]}...")
        print(f"  YT title: {copy['yt_title']}")
        if DRY_RUN:
            print("  [DRY] Skipping upload + scheduling")
            continue
        video_url = upload_video(sf_id)
        posts = build_posts(sf_id, video_url, date_str, keyword, tt_hm, ig_hm, yt_hm, copy)
        for p in posts:
            r = schedule_post(p)
            results.append({"sf": sf_id, "platform": p["platform"],
                            "scheduledFor": p["scheduledFor"],
                            "title": p["title"], "response": r})
            time.sleep(0.5)

    # write results log
    out = PROJECT_ROOT / "content/projects/2026-04-02-apg-ai-business-system/video-editor/short-form/schedule-log.json"
    out.write_text(json.dumps(results, indent=2, default=str))
    print(f"\nWrote log: {out}")

if __name__ == "__main__":
    main()
