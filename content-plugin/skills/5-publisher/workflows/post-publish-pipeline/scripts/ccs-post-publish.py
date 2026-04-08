#!/usr/bin/env python3
"""
CCS Post-Publish Pipeline Orchestrator

After filming and publishing a long-form YouTube video, this script auto-generates
all derivative content in parallel: 5 short-form scripts, blog post, ConvertKit
email, LinkedIn lead magnet, and Instagram carousel.

4 parallel lanes via ThreadPoolExecutor:
  1. Shorts: short-form-scripts workflow (auto mode)
  2. Blog+Email: blog → Supabase publish → email → ConvertKit
  3. LinkedIn: content generation → schedule via schedule-linkedin-post.py
  4. Instagram: carousel generation → schedule via schedule-instagram-post.py

Usage:
    python content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py <youtube-url>
    python content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py <youtube-url> --slug my-project
    python content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py <youtube-url> --schedule-at 2026-03-13T07:00:00+11:00
    python content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py <youtube-url> --skip shorts linkedin
    python content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py <youtube-url> --resume
    python content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py <youtube-url> --dry-run
"""

import argparse
import os
import queue as queue_module
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Environment config loader
# ---------------------------------------------------------------------------

def load_env_config():
    """Load key=value pairs from ccs-post-publish.env (same dir as this script) if it exists."""
    env_file = Path(__file__).resolve().parent / "ccs-post-publish.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                k, _, v = stripped.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


load_env_config()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[6]
CONTENT_PROJECTS = PROJECT_ROOT / "_bmad-output" / "content" / "projects"
ACTIVE_PROJECT_PATH = PROJECT_ROOT / "_bmad" / "ccs" / "active-project.yaml"
LOG_DIR = PROJECT_ROOT / os.environ.get("LOG_DIR", "_bmad-output/post-publish-logs")

STEP_TIMEOUT = int(os.environ.get("STEP_TIMEOUT", "1800"))
HEARTBEAT_INTERVAL = int(os.environ.get("HEARTBEAT_INTERVAL", "30"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "1"))
DEFAULT_SCHEDULE_HOUR = int(os.environ.get("DEFAULT_SCHEDULE_HOUR", "7"))
ALLOWED_TOOLS = os.environ.get("ALLOWED_TOOLS", "Read,Edit,Write,Bash,Glob,Grep")

# Workflow paths (relative to PROJECT_ROOT)
WORKFLOWS = {
    "short-form-scripts": "content-plugin/skills/2-copywriter/workflows/short-form-scripts/workflow.md",
    "short-form-thumbnail": "content-plugin/skills/3-creative-director/workflows/short-form-thumbnail/workflow.md",
    "blog-email-copy": "content-plugin/skills/2-copywriter/workflows/blog-email-copy/workflow.md",
    "linkedin-content": "content-plugin/skills/2-copywriter/workflows/linkedin-content/workflow.md",
    "visual-asset-creation": "content-plugin/skills/3-creative-director/workflows/visual-asset-creation/workflow.md",
}

# All task names
ALL_TASKS = [
    "short-form-scripts",
    "short-form-thumbnails",
    "blog-publish",
    "email-draft",
    "linkedin-video-clip",
    "linkedin-lead-magnet",
    "linkedin-schedule",
    "instagram-carousel",
    "instagram-schedule",
]


# ---------------------------------------------------------------------------
# Live run log
# ---------------------------------------------------------------------------

RUN_LOG: Optional[Path] = None
_log_lock = threading.Lock()


def ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def init_run_log():
    """Create a timestamped run log and print the tail -f command."""
    global RUN_LOG
    ensure_log_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    RUN_LOG = LOG_DIR / f"{ts}_run.log"
    log_event("=" * 56)
    log_event("CCS Post-Publish Pipeline started")
    log_event("=" * 56)
    print(f"\n  Live log: {RUN_LOG}")
    print(f"  Monitor:  tail -f {RUN_LOG}\n")


def log_event(msg: str):
    """Append a timestamped event line to the live run log."""
    if RUN_LOG is None:
        return
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        with _log_lock:
            with open(RUN_LOG, "a") as f:
                f.write(line)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Console output helpers
# ---------------------------------------------------------------------------

def step_header(task_name: str, detail: str = ""):
    """Print a visible header for a task starting."""
    ts = datetime.now().strftime("%H:%M:%S")
    detail_str = f" — {detail}" if detail else ""
    print(f"\n{'='*60}", flush=True)
    print(f"  [{ts}] TASK: {task_name}{detail_str}", flush=True)
    print(f"{'='*60}", flush=True)


def step_footer(task_name: str, duration: float, success: bool):
    """Print a visible footer when a task finishes."""
    ts = datetime.now().strftime("%H:%M:%S")
    status = "PASS" if success else "FAIL"
    print(f"\n  [{ts}] {task_name}: {status} ({duration:.0f}s)", flush=True)
    print(f"{'─'*60}", flush=True)


# ---------------------------------------------------------------------------
# Status YAML management (thread-safe)
# ---------------------------------------------------------------------------

_status_lock = threading.Lock()


def _status_path(slug: str) -> Path:
    return CONTENT_PROJECTS / slug / "post-publish-status.yaml"


def init_status(slug: str, youtube_url: str, schedule_linkedin: str,
                schedule_instagram: str, linkedin_media_type: str,
                skip_tasks: list) -> dict:
    """Create initial status dict and write to YAML."""
    status = {
        "youtube_url": youtube_url,
        "project_slug": slug,
        "started_at": datetime.now().astimezone().isoformat(),
        "schedule_linkedin": schedule_linkedin,
        "schedule_instagram": schedule_instagram,
        "linkedin_media_type": linkedin_media_type,
        "tasks": {},
    }
    for task in ALL_TASKS:
        if task in skip_tasks:
            status["tasks"][task] = {
                "status": "skipped",
                "started_at": None,
                "completed_at": None,
                "error": None,
            }
        else:
            status["tasks"][task] = {
                "status": "pending",
                "started_at": None,
                "completed_at": None,
                "error": None,
            }
    _write_status(slug, status)
    return status


def load_status(slug: str) -> Optional[dict]:
    """Load existing status YAML if it exists."""
    path = _status_path(slug)
    if not path.exists():
        return None
    try:
        import yaml
        return yaml.safe_load(path.read_text())
    except Exception:
        # Fallback: parse manually
        return _parse_status_yaml(path)


def update_task_status(status: dict, slug: str, task: str,
                       new_status: str, error: str = None):
    """Thread-safe update of a single task's status."""
    with _status_lock:
        now = datetime.now().astimezone().isoformat()
        task_data = status["tasks"][task]
        task_data["status"] = new_status
        if new_status == "running" and task_data["started_at"] is None:
            task_data["started_at"] = now
        if new_status in ("done", "failed"):
            task_data["completed_at"] = now
        if error:
            task_data["error"] = error
        _write_status(slug, status)


def _write_status(slug: str, status: dict):
    """Write status dict as YAML."""
    path = _status_path(slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append(f'youtube_url: "{status["youtube_url"]}"')
    lines.append(f'project_slug: "{status["project_slug"]}"')
    lines.append(f'started_at: "{status["started_at"]}"')
    lines.append(f'schedule_linkedin: "{status["schedule_linkedin"]}"')
    lines.append(f'schedule_instagram: "{status["schedule_instagram"]}"')
    lines.append(f'linkedin_media_type: "{status.get("linkedin_media_type", "image")}"')
    lines.append("")
    lines.append("tasks:")
    for task_name, task_data in status["tasks"].items():
        lines.append(f"  {task_name}:")
        for k, v in task_data.items():
            if v is None:
                lines.append(f"    {k}: null")
            else:
                lines.append(f'    {k}: "{v}"')
    path.write_text("\n".join(lines) + "\n")


def _parse_status_yaml(path: Path) -> Optional[dict]:
    """Minimal YAML parser for status file (no pyyaml dependency)."""
    text = path.read_text()
    status = {"tasks": {}}
    current_task = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "tasks:":
            continue
        # Top-level key
        if not line.startswith(" ") and ":" in stripped:
            k, _, v = stripped.partition(":")
            v = v.strip().strip('"')
            if v == "null":
                v = None
            status[k.strip()] = v
        # Task name (2-space indent, ends with :)
        elif line.startswith("  ") and not line.startswith("    ") and stripped.endswith(":"):
            current_task = stripped[:-1].strip()
            status["tasks"][current_task] = {}
        # Task field (4-space indent)
        elif line.startswith("    ") and current_task and ":" in stripped:
            k, _, v = stripped.partition(":")
            v = v.strip().strip('"')
            if v == "null":
                v = None
            status["tasks"][current_task][k.strip()] = v
    return status


# ---------------------------------------------------------------------------
# Streaming subprocess (ported from bmad-orchestrator.py)
# ---------------------------------------------------------------------------

def stream_subprocess(
    cmd: list,
    cwd: Path,
    env: dict = None,
    timeout: int = None,
    log_file: Path = None,
    label: str = "",
) -> tuple:
    """Run a subprocess and stream its output line-by-line.

    - Prints every output line to terminal in real time
    - Writes full output to log_file (if provided)
    - Emits a heartbeat every HEARTBEAT_INTERVAL seconds when silent
    - Kills the process if timeout is exceeded

    Returns:
        (exit_code, full_output_str)
        exit_code is None on timeout or launch failure.
    """
    if timeout is None:
        timeout = STEP_TIMEOUT
    if env is None:
        env = os.environ.copy()

    log_event(f"START: {label} — {' '.join(cmd[:3])}...")
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{ts}] >>> {label}", flush=True)

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=str(cwd),
            env=env,
            text=True,
            bufsize=1,
        )
    except FileNotFoundError:
        msg = f"ERROR: command not found: {cmd[0]}"
        print(f"  {msg}", flush=True)
        log_event(f"ERROR: {label} — {msg}")
        return None, msg

    q = queue_module.Queue()
    output_lines = []

    def _reader():
        try:
            for line in proc.stdout:
                q.put(line)
        finally:
            q.put(None)  # sentinel: stdout closed

    thread = threading.Thread(target=_reader, daemon=True)
    thread.start()

    start = time.time()
    last_output_time = time.time()
    log_fh = open(log_file, "w") if log_file else None

    try:
        while True:
            elapsed = time.time() - start

            if elapsed > timeout:
                proc.kill()
                msg = f"TIMEOUT: {label} exceeded {timeout}s — process killed"
                print(f"\n  {msg}", flush=True)
                log_event(msg)
                if log_fh:
                    log_fh.write(f"\n{msg}\n")
                return None, "\n".join(output_lines)

            try:
                line = q.get(timeout=2.0)
            except queue_module.Empty:
                silence = time.time() - last_output_time
                if silence >= HEARTBEAT_INTERVAL:
                    ts = datetime.now().strftime("%H:%M:%S")
                    hb = f"  [{ts}] ... {label} still running ({elapsed:.0f}s elapsed)"
                    print(hb, flush=True)
                    log_event(f"{label}: heartbeat ({elapsed:.0f}s elapsed)")
                    if log_fh:
                        log_fh.write(f"{hb}\n")
                    last_output_time = time.time()
                continue

            if line is None:  # stdout closed — process finished
                break

            last_output_time = time.time()
            line_stripped = line.rstrip("\n")
            print(line_stripped, flush=True)
            output_lines.append(line_stripped)
            if log_fh:
                log_fh.write(line)
                log_fh.flush()

        proc.wait()
        duration = time.time() - start
        result_status = "PASS" if proc.returncode == 0 else f"FAIL (exit {proc.returncode})"
        log_event(f"END: {label} — {result_status} ({duration:.0f}s)")
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] <<< {label}: {result_status} ({duration:.0f}s)", flush=True)
        return proc.returncode, "\n".join(output_lines)

    finally:
        if log_fh:
            log_fh.close()
        thread.join(timeout=5)


# ---------------------------------------------------------------------------
# Task runner
# ---------------------------------------------------------------------------

def run_task(task_name: str, prompt: str, status: dict, slug: str,
             dry_run: bool = False, attempt: int = 1, label: str = "") -> bool:
    """Execute a single task via claude -p. Returns True on success."""
    display_name = label or task_name
    if dry_run:
        print(f"\n  [DRY RUN] Task: {display_name}")
        print(f"  Prompt ({len(prompt)} chars):")
        print(f"  {prompt[:500]}...")
        if len(prompt) > 500:
            print(f"  ... ({len(prompt) - 500} more chars)")
        update_task_status(status, slug, task_name, "done")
        return True

    update_task_status(status, slug, task_name, "running")
    start = time.time()
    step_header(display_name, f"attempt {attempt}")
    log_event(f"TASK START: {display_name} (attempt {attempt})")

    # Unset CLAUDECODE so nested claude -p calls aren't blocked
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    ensure_log_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"{timestamp}_{task_name}.log"

    exit_code, output = stream_subprocess(
        cmd=["claude", "-p", prompt, "--dangerously-skip-permissions"],
        cwd=PROJECT_ROOT,
        env=env,
        timeout=STEP_TIMEOUT,
        log_file=log_file,
        label=display_name,
    )

    duration = time.time() - start

    if exit_code == 0:
        step_footer(display_name, duration, True)
        log_event(f"TASK OK: {display_name} ({duration:.0f}s)")
        update_task_status(status, slug, task_name, "done")
        return True

    # Failure
    error_msg = f"exit {exit_code}" if exit_code is not None else "timeout"
    step_footer(display_name, duration, False)
    log_event(f"TASK FAILED: {display_name} ({error_msg}, {duration:.0f}s)")

    # Auto-retry
    if attempt <= MAX_RETRIES:
        print(f"  Retrying {display_name} ({attempt + 1}/{MAX_RETRIES + 1})...")
        return run_task(task_name, prompt, status, slug,
                        dry_run=dry_run, attempt=attempt + 1, label=label)

    update_task_status(status, slug, task_name, "failed", error=error_msg)
    return False


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

def _yolo_preamble() -> str:
    """Common YOLO mode override for all prompts."""
    return (
        "CRITICAL OVERRIDE — YOLO MODE: You are running in fully automated mode. "
        "Do NOT ask the user any questions. Do NOT halt at menus or confirmation prompts. "
        "Make best-case assumptions at every decision point. Auto-approve all checkpoints. "
        "Auto-select all options as directed below. Complete the ENTIRE workflow end-to-end "
        "without stopping. If you encounter an error, attempt to recover automatically.\n\n"
    )


def prompt_short_form_scripts(slug: str, project_folder: Path) -> str:
    workflow = PROJECT_ROOT / WORKFLOWS["short-form-scripts"]
    return (
        f"{_yolo_preamble()}"
        f"Load and execute the workflow at {workflow}\n\n"
        f"The active project slug is '{slug}' at {project_folder}.\n\n"
        f"At the execution mode selection, choose [A] Auto mode.\n\n"
        f"Generate all 5 short-form scripts end-to-end without stopping. "
        f"Use the project's existing transcript, visual analysis, and audio analysis files."
    )


def prompt_short_form_thumbnails(slug: str, project_folder: Path) -> str:
    workflow = PROJECT_ROOT / WORKFLOWS["short-form-thumbnail"]
    scripts_folder = f"{project_folder}/video-editor/short-form/scripts"
    return (
        f"{_yolo_preamble()}"
        f"Load and execute the workflow at {workflow}\n\n"
        f"The active project slug is '{slug}' at {project_folder}.\n\n"
        f"YOLO OVERRIDES for this workflow:\n"
        f"- At 'Get Video Description': Read the short-form scripts at {scripts_folder}/ "
        f"to understand each video's topic, hook, and key message. Generate thumbnails "
        f"for ALL 5 short-form videos (sf-01 through sf-05).\n"
        f"- At 'Get Video Title Slug': Use the project slug '{slug}'.\n"
        f"- At concept approval: auto-approve the top 1 concept per video [A].\n"
        f"- At completion: select [D] Done.\n\n"
        f"Generate 1 thumbnail per video for 5 short-form videos (5 total). "
        f"Sequential generation only. Save to the project's video-editor/short-form/thumbnails/ folder "
        f"as sf-{{NN}}-thumbnail.png."
    )


def prompt_blog_publish(slug: str, project_folder: Path, youtube_url: str) -> str:
    workflow = PROJECT_ROOT / WORKFLOWS["blog-email-copy"]
    return (
        f"{_yolo_preamble()}"
        f"Load and execute the workflow at {workflow}\n\n"
        f"The active project slug is '{slug}' at {project_folder}.\n"
        f"The YouTube video URL is: {youtube_url}\n\n"
        f"At step-01-init: auto-select [P] Project mode. Use project slug '{slug}'.\n"
        f"At step-02-format: auto-select Blog format.\n"
        f"For SEO metadata at step-03: auto-select option [A] for the recommended SEO metadata.\n"
        f"At step-04-publish: auto-confirm publishing to Supabase.\n\n"
        f"Complete the entire blog creation and publishing workflow. "
        f"The blog must be fully published to Supabase before this task is complete."
    )


def prompt_email_draft(slug: str, project_folder: Path, youtube_url: str) -> str:
    workflow = PROJECT_ROOT / WORKFLOWS["blog-email-copy"]
    return (
        f"{_yolo_preamble()}"
        f"Load and execute the workflow at {workflow}\n\n"
        f"The active project slug is '{slug}' at {project_folder}.\n"
        f"The YouTube video URL is: {youtube_url}\n\n"
        f"At step-01-init: auto-select [P] Project mode. Use project slug '{slug}'.\n"
        f"At step-02-format: auto-select Email format.\n\n"
        f"IMPORTANT: A blog post for this project has already been published to Supabase. "
        f"Reference the blog's Supabase image URLs in the email content where appropriate.\n\n"
        f"Look for blog output files at: {project_folder}/copywriter/blog-email/blog-*.md\n\n"
        f"At step-04-polish: auto-confirm pushing the email draft to ConvertKit.\n\n"
        f"Complete the entire email creation and ConvertKit push workflow."
    )


def prompt_linkedin_video_clip(slug: str, project_folder: Path) -> str:
    video_src = f"{project_folder}/video-editor/clips/body-clipped.mp4"
    transcript_src = f"{project_folder}/video-editor/clips/body-clipped-transcript.json"
    output_path = f"{project_folder}/copywriter/linkedin/linkedin-teaser-20x.mp4"
    return (
        f"{_yolo_preamble()}"
        f"You need to create a 20x sped-up teaser clip from the project's body video for LinkedIn.\n\n"
        f"Steps:\n"
        f"1. Read the word-level transcript at:\n"
        f"   {transcript_src}\n\n"
        f"2. Analyze the transcript and pick the most visually interesting ~300 second (240-360s) "
        f"contiguous section of the video. Prefer demo/building/coding sections where something "
        f"is being shown or built on screen. Avoid intro recap, talking head sections, and outro.\n\n"
        f"3. Run FFmpeg to cut that section and speed it up 20x at proxy quality:\n"
        f"   ffmpeg -y -ss {{start_seconds}} -t {{duration_seconds}} -i {video_src} "
        f"-filter_complex \"[0:v]setpts=PTS/20[v]\" -map \"[v]\" -an "
        f"-c:v libx264 -preset fast -crf 28 -s 1280:720 {output_path}\n\n"
        f"4. Verify the output file exists and is non-zero size.\n\n"
        f"The source video is body-clipped.mp4 (~30MB proxy), NOT the full 4.8GB render.\n"
        f"Output should be ~2-5MB at {output_path}"
    )


def prompt_linkedin_lead_magnet(slug: str, project_folder: Path,
                                 youtube_url: str) -> str:
    workflow = PROJECT_ROOT / WORKFLOWS["linkedin-content"]
    video_file = f"{project_folder}/copywriter/linkedin/linkedin-teaser-20x.mp4"
    return (
        f"{_yolo_preamble()}"
        f"Load and execute the workflow at {workflow}\n\n"
        f"The active project slug is '{slug}' at {project_folder}.\n"
        f"The YouTube video URL is: {youtube_url}\n\n"
        f"COLLAB-ONLY OVERRIDE: This workflow is normally COLLAB-only (halts at every menu). "
        f"You MUST override this and run in full auto mode — make best-case decisions at every "
        f"menu and checkpoint without stopping.\n\n"
        f"At step-01-init: auto-select [P] Project-based source mode.\n"
        f"At format selection: auto-select [V] Video post format.\n\n"
        f"IMPORTANT: The video file already exists at:\n"
        f"  {video_file}\n"
        f"Do NOT create, generate, or modify the video. It is a 20x sped-up clip from the "
        f"actual YouTube video and is ready to use as-is.\n\n"
        f"At step-03 (media planning): reference the existing video file above.\n"
        f"At step-05b (media production): skip video creation — the file already exists.\n\n"
        f"Content category: Lead Magnet — create a post that offers value and drives engagement "
        f"through a lead magnet CTA. Select a keyword from the centralised library at "
        f"_bmad/ccs/data/lead-magnet-keywords.yaml that best matches this video's topic. "
        f"Use the LinkedIn CTA template from the library.\n\n"
        f"Complete the entire LinkedIn content generation workflow end-to-end."
    )


def prompt_linkedin_schedule(slug: str, project_folder: Path,
                              schedule_at: str) -> str:
    video_file = f"{project_folder}/copywriter/linkedin/linkedin-teaser-20x.mp4"
    return (
        f"{_yolo_preamble()}"
        f"Find the most recently created LinkedIn post output file in:\n"
        f"  {project_folder}/copywriter/linkedin/\n\n"
        f"Look for the latest .md file. Read it to get the post content.\n\n"
        f"Then run the LinkedIn scheduling script:\n"
        f"  python3 {PROJECT_ROOT}/scripts/schedule-linkedin-post.py "
        f"--file <path-to-linkedin-post.md> "
        f"--media \"{video_file}\" "
        f"--scheduled-at \"{schedule_at}\"\n\n"
        f"Confirm the scheduling was successful by checking the script output."
    )


def prompt_instagram_carousel(slug: str, project_folder: Path,
                               youtube_url: str) -> str:
    workflow = PROJECT_ROOT / WORKFLOWS["visual-asset-creation"]
    return (
        f"{_yolo_preamble()}"
        f"Load and execute the workflow at {workflow}\n\n"
        f"The active project slug is '{slug}' at {project_folder}.\n"
        f"The YouTube video URL is: {youtube_url}\n\n"
        f"At step-02-select (asset type selection): auto-select [IC] Instagram Carousel.\n\n"
        f"At brand selection: select [P] Personal — generate for @{YOUR_HANDLE_PERSONAL} only (dark mode, no logo).\n\n"
        f"Generate the full Instagram carousel (up to 10 slides, 1080x1350). "
        f"Use the project's content concepts, scripts, and visual assets as source material.\n\n"
        f"Also generate an Instagram caption with relevant hashtags. "
        f"Save the caption to the project's creative-director output folder.\n\n"
        f"Complete the entire Instagram carousel creation workflow end-to-end."
    )


def prompt_instagram_schedule(slug: str, project_folder: Path,
                               schedule_at: str, account: str = "adam") -> str:
    account_folder = f"{project_folder}/creative-director/carousels/instagram/{account}/"
    return (
        f"{_yolo_preamble()}"
        f"Find the Instagram carousel output in:\n"
        f"  {account_folder}\n\n"
        f"Look for the Instagram carousel slides (numbered PNGs like slide-01.png).\n"
        f"Also find the caption file: {account_folder}instagram-caption.md\n\n"
        f"Then run the Instagram scheduling script:\n"
        f"  python3 {PROJECT_ROOT}/scripts/schedule-instagram-post.py "
        f"--media-dir {account_folder} "
        f"--file {account_folder}instagram-caption.md "
        f"--account {account} "
        f"--scheduled-at \"{schedule_at}\"\n\n"
        f"Confirm the scheduling was successful by checking the script output."
    )


# ---------------------------------------------------------------------------
# Lane functions (run within ThreadPoolExecutor)
# ---------------------------------------------------------------------------

def lane_short_form(ctx: dict) -> str:
    """Lane 1: Short-form scripts → thumbnails (sequential)."""
    results = []

    # Scripts
    task = "short-form-scripts"
    if not _should_skip(ctx, task):
        prompt = prompt_short_form_scripts(ctx["slug"], ctx["project_folder"])
        ok = run_task(task, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task}: {'done' if ok else 'failed'}")
        if not ok:
            task_thumb = "short-form-thumbnails"
            if not _should_skip(ctx, task_thumb):
                update_task_status(ctx["status"], ctx["slug"], task_thumb,
                                   "failed", error="dependency short-form-scripts failed")
                results.append(f"{task_thumb}: failed (dependency)")
            return " | ".join(results)
    else:
        results.append(f"{task}: skipped")

    # Thumbnails (depends on scripts existing)
    task_thumb = "short-form-thumbnails"
    if not _should_skip(ctx, task_thumb):
        prompt = prompt_short_form_thumbnails(ctx["slug"], ctx["project_folder"])
        ok = run_task(task_thumb, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_thumb}: {'done' if ok else 'failed'}")
    else:
        results.append(f"{task_thumb}: skipped")

    return " | ".join(results)


def lane_blog_email(ctx: dict) -> str:
    """Lane 2: Blog publish → Email draft (sequential)."""
    results = []

    # Blog
    task_blog = "blog-publish"
    if not _should_skip(ctx, task_blog):
        prompt = prompt_blog_publish(ctx["slug"], ctx["project_folder"],
                                     ctx["youtube_url"])
        ok = run_task(task_blog, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_blog}: {'done' if ok else 'failed'}")
        if not ok:
            # Blog failed — skip email since it depends on blog being published
            task_email = "email-draft"
            if not _should_skip(ctx, task_email):
                update_task_status(ctx["status"], ctx["slug"], task_email,
                                   "failed", error="dependency blog-publish failed")
                results.append(f"{task_email}: failed (dependency)")
            return " | ".join(results)
    else:
        results.append(f"{task_blog}: skipped")

    # Email (depends on blog)
    task_email = "email-draft"
    if not _should_skip(ctx, task_email):
        prompt = prompt_email_draft(ctx["slug"], ctx["project_folder"],
                                    ctx["youtube_url"])
        ok = run_task(task_email, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_email}: {'done' if ok else 'failed'}")
    else:
        results.append(f"{task_email}: skipped")

    return " | ".join(results)


def lane_linkedin(ctx: dict) -> str:
    """Lane 3: LinkedIn video clip → content → schedule (sequential)."""
    results = []
    downstream_tasks = ["linkedin-lead-magnet", "linkedin-schedule"]

    # Video clip (first step — cut 20x sped-up teaser from body video)
    task_clip = "linkedin-video-clip"
    if not _should_skip(ctx, task_clip):
        prompt = prompt_linkedin_video_clip(ctx["slug"], ctx["project_folder"])
        ok = run_task(task_clip, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_clip}: {'done' if ok else 'failed'}")
        if not ok:
            for dep_task in downstream_tasks:
                if not _should_skip(ctx, dep_task):
                    update_task_status(ctx["status"], ctx["slug"], dep_task,
                                       "failed", error="dependency linkedin-video-clip failed")
                    results.append(f"{dep_task}: failed (dependency)")
            return " | ".join(results)
    else:
        results.append(f"{task_clip}: skipped")

    # Lead magnet content
    task_content = "linkedin-lead-magnet"
    if not _should_skip(ctx, task_content):
        prompt = prompt_linkedin_lead_magnet(
            ctx["slug"], ctx["project_folder"], ctx["youtube_url"])
        ok = run_task(task_content, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_content}: {'done' if ok else 'failed'}")
        if not ok:
            task_sched = "linkedin-schedule"
            if not _should_skip(ctx, task_sched):
                update_task_status(ctx["status"], ctx["slug"], task_sched,
                                   "failed", error="dependency linkedin-lead-magnet failed")
                results.append(f"{task_sched}: failed (dependency)")
            return " | ".join(results)
    else:
        results.append(f"{task_content}: skipped")

    # Schedule
    task_sched = "linkedin-schedule"
    if not _should_skip(ctx, task_sched):
        prompt = prompt_linkedin_schedule(
            ctx["slug"], ctx["project_folder"], ctx["schedule_linkedin"])
        ok = run_task(task_sched, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_sched}: {'done' if ok else 'failed'}")
    else:
        results.append(f"{task_sched}: skipped")

    return " | ".join(results)


def lane_instagram(ctx: dict) -> str:
    """Lane 4: Instagram carousel → schedule (sequential)."""
    results = []

    # Carousel creation
    task_carousel = "instagram-carousel"
    if not _should_skip(ctx, task_carousel):
        prompt = prompt_instagram_carousel(
            ctx["slug"], ctx["project_folder"], ctx["youtube_url"])
        ok = run_task(task_carousel, prompt, ctx["status"], ctx["slug"], ctx["dry_run"])
        results.append(f"{task_carousel}: {'done' if ok else 'failed'}")
        if not ok:
            task_sched = "instagram-schedule"
            if not _should_skip(ctx, task_sched):
                update_task_status(ctx["status"], ctx["slug"], task_sched,
                                   "failed", error="dependency instagram-carousel failed")
                results.append(f"{task_sched}: failed (dependency)")
            return " | ".join(results)
    else:
        results.append(f"{task_carousel}: skipped")

    # Schedule — Adam's personal account only (is handled standalone)
    task_sched = "instagram-schedule"
    if not _should_skip(ctx, task_sched):
        prompt = prompt_instagram_schedule(
            ctx["slug"], ctx["project_folder"], ctx["schedule_instagram"], "adam")
        ok = run_task(task_sched, prompt, ctx["status"], ctx["slug"], ctx["dry_run"],
                      label="instagram-schedule")
        results.append(f"{task_sched}: {'done' if ok else 'failed'}")
    else:
        results.append(f"{task_sched}: skipped")

    return " | ".join(results)


def _should_skip(ctx: dict, task: str) -> bool:
    """Check if a task should be skipped (explicit skip or already done on resume)."""
    task_status = ctx["status"]["tasks"].get(task, {}).get("status")
    if task_status == "skipped":
        return True
    if task_status == "done" and ctx.get("resume"):
        print(f"  [{task}] already done — skipping (resume mode)")
        return True
    return False


# ---------------------------------------------------------------------------
# Slug detection
# ---------------------------------------------------------------------------

def detect_slug() -> Optional[str]:
    """Auto-detect project slug from active-project.yaml."""
    if not ACTIVE_PROJECT_PATH.exists():
        return None
    for line in ACTIVE_PROJECT_PATH.read_text().splitlines():
        if line.startswith("slug:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


# ---------------------------------------------------------------------------
# Schedule time helpers
# ---------------------------------------------------------------------------

def default_schedule_time() -> str:
    """Tomorrow at DEFAULT_SCHEDULE_HOUR local time, ISO format."""
    now = datetime.now().astimezone()
    tomorrow = now + timedelta(days=1)
    scheduled = tomorrow.replace(
        hour=DEFAULT_SCHEDULE_HOUR, minute=0, second=0, microsecond=0
    )
    return scheduled.isoformat()


# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------

def print_summary(status: dict):
    """Print a final summary table of all task statuses."""
    print(f"\n{'='*60}")
    print("  POST-PUBLISH PIPELINE — FINAL SUMMARY")
    print(f"{'='*60}\n")

    # Calculate durations
    for task_name, task_data in status["tasks"].items():
        duration = ""
        if task_data.get("started_at") and task_data.get("completed_at"):
            try:
                start = datetime.fromisoformat(task_data["started_at"])
                end = datetime.fromisoformat(task_data["completed_at"])
                secs = (end - start).total_seconds()
                if secs >= 60:
                    duration = f"{secs / 60:.1f}m"
                else:
                    duration = f"{secs:.0f}s"
            except (ValueError, TypeError):
                duration = "-"
        else:
            duration = "-"

        s = task_data.get("status", "unknown")
        icon = {"done": "+", "failed": "X", "skipped": "-", "pending": "?", "running": ">"}.get(s, "?")
        error_str = f" — {task_data.get('error', '')}" if task_data.get("error") else ""
        print(f"  [{icon}] {task_name:25s} {s:10s} {duration:>8s}{error_str}")

    # Overall result
    all_tasks = status["tasks"]
    done_count = sum(1 for t in all_tasks.values() if t.get("status") == "done")
    failed_count = sum(1 for t in all_tasks.values() if t.get("status") == "failed")
    skipped_count = sum(1 for t in all_tasks.values() if t.get("status") == "skipped")
    total = len(all_tasks)

    print(f"\n  Done: {done_count}/{total}  Failed: {failed_count}  Skipped: {skipped_count}")

    if failed_count > 0:
        print(f"\n  Some tasks failed. Re-run with --resume to retry failed tasks.")
    elif done_count + skipped_count == total:
        print(f"\n  All tasks completed successfully!")

    print(f"\n  Status file: {_status_path(status['project_slug'])}")
    if RUN_LOG:
        print(f"  Run log: {RUN_LOG}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global STEP_TIMEOUT

    parser = argparse.ArgumentParser(
        description="CCS Post-Publish Pipeline — generate all derivative content from a YouTube video"
    )
    parser.add_argument("youtube_url", help="YouTube video URL")
    parser.add_argument("--slug", help="Project slug (auto-detect from active-project.yaml if omitted)")
    parser.add_argument("--schedule-at", dest="schedule_at",
                        help="ISO datetime for LinkedIn + Instagram (default: tomorrow 7am)")
    parser.add_argument("--linkedin-at", dest="linkedin_at",
                        help="Override LinkedIn schedule time")
    parser.add_argument("--instagram-at", dest="instagram_at",
                        help="Override Instagram schedule time")
    parser.add_argument("--skip", nargs="+", default=[],
                        help="Skip tasks: shorts, thumbnails, blog, email, linkedin, instagram")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from existing status YAML (skip completed tasks)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompts without executing")
    parser.add_argument("--timeout", type=int, default=None,
                        help=f"Per-task timeout in seconds (default: {STEP_TIMEOUT})")

    args = parser.parse_args()

    # Override timeout if provided
    if args.timeout is not None:
        STEP_TIMEOUT = args.timeout

    # Resolve slug
    slug = args.slug or detect_slug()
    if not slug:
        print("ERROR: No project slug provided and couldn't auto-detect from active-project.yaml")
        sys.exit(1)

    project_folder = CONTENT_PROJECTS / slug
    if not project_folder.exists():
        print(f"ERROR: Project folder does not exist: {project_folder}")
        sys.exit(1)

    # Resolve schedule times
    schedule_at = args.schedule_at or default_schedule_time()
    schedule_linkedin = args.linkedin_at or schedule_at
    schedule_instagram = args.instagram_at or schedule_at

    # LinkedIn always uses video (20x sped-up clip from body video)
    linkedin_media_type = "video"

    # Expand skip shorthand to full task names
    skip_map = {
        "shorts": ["short-form-scripts", "short-form-thumbnails"],
        "thumbnails": ["short-form-thumbnails"],
        "blog": ["blog-publish"],
        "email": ["email-draft"],
        "linkedin": ["linkedin-video-clip", "linkedin-lead-magnet", "linkedin-schedule"],
        "instagram": ["instagram-carousel", "instagram-schedule"],
    }
    skip_tasks = []
    for s in args.skip:
        if s in skip_map:
            skip_tasks.extend(skip_map[s])
        elif s in ALL_TASKS:
            skip_tasks.append(s)
        else:
            print(f"WARNING: Unknown skip target '{s}' — ignoring")

    # Initialize or resume status
    if args.resume:
        status = load_status(slug)
        if status is None:
            print(f"ERROR: No existing status file to resume from at {_status_path(slug)}")
            sys.exit(1)
        print(f"  Resuming from existing status file...")
        # Preserve linkedin_media_type from existing status
        linkedin_media_type = status.get("linkedin_media_type", linkedin_media_type)
        # Reset failed tasks to pending for retry
        for task_name, task_data in status["tasks"].items():
            if task_data.get("status") == "failed":
                task_data["status"] = "pending"
                task_data["started_at"] = None
                task_data["completed_at"] = None
                task_data["error"] = None
        _write_status(slug, status)
    else:
        status = init_status(slug, args.youtube_url, schedule_linkedin,
                             schedule_instagram, linkedin_media_type, skip_tasks)

    # Init logging
    init_run_log()

    # Print run config
    print(f"\n  CCS Post-Publish Pipeline")
    print(f"  {'─'*40}")
    print(f"  YouTube:    {args.youtube_url}")
    print(f"  Project:    {slug}")
    print(f"  LinkedIn:   {schedule_linkedin} ({linkedin_media_type} format)")
    print(f"  Instagram:  {schedule_instagram}")
    print(f"  Timeout:    {STEP_TIMEOUT}s per task")
    if skip_tasks:
        print(f"  Skipping:   {', '.join(skip_tasks)}")
    if args.resume:
        print(f"  Mode:       RESUME")
    if args.dry_run:
        print(f"  Mode:       DRY RUN")
    print()

    # Build shared context for lanes
    ctx = {
        "slug": slug,
        "project_folder": project_folder,
        "youtube_url": args.youtube_url,
        "schedule_linkedin": schedule_linkedin,
        "schedule_instagram": schedule_instagram,
        "status": status,
        "dry_run": args.dry_run,
        "resume": args.resume,
    }

    # Launch 4 parallel lanes
    log_event("Launching 4 parallel lanes...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(lane_short_form, ctx): "shorts",
            pool.submit(lane_blog_email, ctx): "blog+email",
            pool.submit(lane_linkedin, ctx): "linkedin",
            pool.submit(lane_instagram, ctx): "instagram",
        }
        for future in as_completed(futures):
            lane_name = futures[future]
            try:
                result = future.result()
                log_event(f"LANE DONE: {lane_name} — {result}")
                print(f"\n  Lane complete: {lane_name} — {result}")
            except Exception as e:
                log_event(f"LANE ERROR: {lane_name} — {e}")
                print(f"\n  Lane error: {lane_name} — {e}")

    total_duration = time.time() - start_time
    log_event(f"All lanes complete ({total_duration:.0f}s total)")

    # Reload status from disk (lanes may have updated it)
    status = load_status(slug) or status

    # Print final summary
    print_summary(status)

    # Exit code: non-zero if any task failed
    any_failed = any(
        t.get("status") == "failed"
        for t in status["tasks"].values()
    )
    sys.exit(1 if any_failed else 0)


if __name__ == "__main__":
    main()
