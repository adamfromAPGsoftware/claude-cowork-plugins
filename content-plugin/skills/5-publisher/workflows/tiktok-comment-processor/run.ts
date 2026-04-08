/**
 * Playwright testing harness for TikTok Comment Processor userscript.
 *
 * Usage:
 *   npx tsx run.ts [--url <tiktok-url>] [--cookie <sessionid>] [--sid <sid_tt>] [--csrf <tt_csrf_token>] [--headless]
 *
 * Supports two modes:
 *   1. Video mode:   --url "https://www.tiktok.com/@user/video/123"  (process single video)
 *   2. Profile mode: --url "https://www.tiktok.com/@user"            (auto-iterate all videos)
 *
 * Opens a Chromium browser with a persistent session (so TikTok
 * stays logged in across runs). The userscript is injected into every page
 * via context.addInitScript.
 *
 * Pass --cookie with your sessionid token to skip manual login.
 * Pass --headless to run without a visible browser window.
 *
 * On Ctrl+C the harness exports a debug snapshot (DOM + screenshot + URL)
 * for every open tab into debug/{ISO-timestamp}/.
 */

import { chromium } from "playwright";
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { parseArgs } from "node:util";

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

const { values } = parseArgs({
  options: {
    url: { type: "string", default: "https://www.tiktok.com/" },
    cookie: { type: "string" },
    sid: { type: "string" },
    csrf: { type: "string" },
    headless: { type: "boolean", default: false },
  },
});

const TARGET_URL = values.url!;
const SESSION_ID = values.cookie;
const SID_TT = values.sid;
const TT_CSRF = values.csrf;
const HEADLESS = values.headless!;
const SCRIPT_DIR = decodeURIComponent(dirname(new URL(import.meta.url).pathname));
const USERSCRIPT_PATH = join(SCRIPT_DIR, "userscript.js");
const BROWSER_DATA_DIR = join(SCRIPT_DIR, ".browser-data");
const DEBUG_DIR = join(SCRIPT_DIR, "debug");

// ---------------------------------------------------------------------------
// Userscript wrapper — runs at document-start but waits for DOM ready
// ---------------------------------------------------------------------------

const rawScript = readFileSync(USERSCRIPT_PATH, "utf-8");

const wrappedScript = `
(function() {
  function runUserscript() { ${rawScript} }
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    runUserscript();
  } else {
    document.addEventListener('DOMContentLoaded', runUserscript);
  }
})();
`;

// ---------------------------------------------------------------------------
// Debug export
// ---------------------------------------------------------------------------

async function exportDebugSnapshot(
  pages: Awaited<ReturnType<typeof chromium.launchPersistentContext>>["pages"]
) {
  const ts = new Date().toISOString().replace(/[:.]/g, "-");
  const snapshotDir = join(DEBUG_DIR, ts);
  mkdirSync(snapshotDir, { recursive: true });

  const openPages = pages();
  console.log(`\nExporting debug snapshot for ${openPages.length} tab(s)...`);

  for (let i = 0; i < openPages.length; i++) {
    const page = openPages[i];
    const prefix = `tab-${i}`;

    try {
      // URL
      writeFileSync(join(snapshotDir, `${prefix}.url.txt`), page.url());

      // DOM
      const html = await page.content();
      writeFileSync(join(snapshotDir, `${prefix}.html`), html);

      // Screenshot
      await page.screenshot({
        path: join(snapshotDir, `${prefix}.png`),
        fullPage: false,
      });

      console.log(`  ${prefix}: ${page.url()}`);
    } catch (err) {
      console.error(`  ${prefix}: export failed — ${err}`);
    }
  }

  console.log(`Snapshot saved to: ${snapshotDir}`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

(async () => {
  console.log("Launching Chromium (persistent session)...");
  console.log(`  Browser data: ${BROWSER_DATA_DIR}`);
  console.log(`  Target URL:   ${TARGET_URL}`);

  const context = await chromium.launchPersistentContext(BROWSER_DATA_DIR, {
    headless: HEADLESS,
    args: [
      "--disable-blink-features=AutomationControlled",
      "--disable-features=IsolateOrigins",
      "--no-first-run",
      "--no-default-browser-check",
    ],
    viewport: { width: 1280, height: 900 },
    ignoreDefaultArgs: ["--enable-automation"],
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
  });

  // Inject TikTok session cookies if provided
  const cookies: Array<{
    name: string;
    value: string;
    domain: string;
    path: string;
    httpOnly: boolean;
    secure: boolean;
    sameSite: "None" | "Lax" | "Strict";
  }> = [];

  if (SESSION_ID) {
    cookies.push({
      name: "sessionid",
      value: SESSION_ID,
      domain: ".tiktok.com",
      path: "/",
      httpOnly: true,
      secure: true,
      sameSite: "None",
    });
    console.log("  Session cookie injected (sessionid).");
  }

  if (SID_TT) {
    cookies.push({
      name: "sid_tt",
      value: SID_TT,
      domain: ".tiktok.com",
      path: "/",
      httpOnly: true,
      secure: true,
      sameSite: "None",
    });
    console.log("  Session cookie injected (sid_tt).");
  }

  if (TT_CSRF) {
    cookies.push({
      name: "tt_csrf_token",
      value: TT_CSRF,
      domain: ".tiktok.com",
      path: "/",
      httpOnly: false,
      secure: true,
      sameSite: "None",
    });
    console.log("  CSRF token injected (tt_csrf_token).");
  }

  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }

  // Inject userscript into every page (including new tabs opened by the script)
  await context.addInitScript(wrappedScript);

  // Track new tabs (the DM flow opens profile pages in new tabs)
  context.on("page", (page) => {
    console.log(`  [tab opened] ${page.url()}`);
    page.on("close", () => console.log(`  [tab closed]`));
  });

  // Navigate the first page
  const page = context.pages()[0] || (await context.newPage());
  await page.goto(TARGET_URL, { waitUntil: "domcontentloaded", timeout: 60000 });

  // Login detection
  const currentUrl = page.url();
  if (
    currentUrl.includes("/login") ||
    currentUrl.includes("login_redirect")
  ) {
    if (SESSION_ID) {
      console.log("\n--- Cookie rejected — TikTok still requires login ---");
      console.log("The sessionid cookie may be expired. Get a fresh one from your browser.");
      console.log("Or log in manually in this window — session will be saved.\n");
    } else {
      console.log("\n--- TikTok login required ---");
      console.log("Log in manually in the browser window.");
      console.log("Your session will be saved for future runs.");
      console.log("Tip: use --cookie <sessionid> next time to skip login.\n");
    }
  } else {
    console.log("\nBrowser ready. The userscript will activate on video pages.");
    console.log("Navigate to a TikTok video to see the Comment Processor UI.\n");
  }

  console.log("Press Ctrl+C (or click Stop & Export in the browser) to stop and export a debug snapshot.\n");

  // Graceful shutdown on SIGINT
  let isExiting = false;

  // Poll for Stop & Export button signal from the userscript
  const stopPollInterval = setInterval(async () => {
    try {
      const pages = context.pages();
      for (const p of pages) {
        const stopRequested = await p.evaluate(() => (window as any).__STOP_EXPORT_REQUESTED === true).catch(() => false);
        if (stopRequested) {
          console.log("\nStop & Export requested from browser UI.");
          clearInterval(stopPollInterval);
          await shutdown();
          return;
        }
      }
    } catch {
      // Page may have closed, ignore
    }
  }, 1000);

  const shutdown = async () => {
    if (isExiting) return;
    isExiting = true;

    console.log("\nShutting down...");

    try {
      await exportDebugSnapshot(() => context.pages());
    } catch (err) {
      console.error("Debug export failed:", err);
    }

    try {
      await context.close();
    } catch {
      // Browser may already be closed
    }

    process.exit(0);
  };

  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);

  // Also handle browser being closed manually
  context.on("close", () => {
    if (!isExiting) {
      console.log("\nBrowser closed by user.");
      process.exit(0);
    }
  });

  // Keep alive
  await new Promise(() => {});
})();
