#!/usr/bin/env python3
"""Full-page screenshots of every real page of the site at 1280 px and 390 px.

Usage: python3 screens.py OUT_DIR [--site SITE_DIR] [--widths 1280,390]

Needs the Playwright Python package (pip install playwright). It serves the site from a
temporary local web server and drives Chromium. Browser lookup order: Playwright's own
Chromium, the CHROME_PATH environment variable, the Playwright browser caches, then Google
Chrome on a Mac. Install Playwright's browser with `python3 -m playwright install chromium`
when none of those exists.

Files are named by page path and width: principles/index.html at 390 px becomes
principles-index-390.png.
Exit code 1 when a page fails to load or scrolls sideways.
"""
import argparse
import functools
import glob
import http.server
import os
import re
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent

BROWSER_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/opt/pw-browsers/chromium",
    "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
    os.path.expanduser("~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"),
    os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def real_pages(site: Path):
    pages = []
    for root, dirs, files in os.walk(site):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in ("tools", "node_modules"))
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            path = Path(root, name)
            pages.append(path.relative_to(site).as_posix())
    return pages


def find_browsers():
    found = []
    for pattern in BROWSER_CANDIDATES:
        if not pattern:
            continue
        for hit in sorted(glob.glob(pattern)):
            if os.path.isfile(hit) and os.access(hit, os.X_OK):
                found.append(hit)
    return found


def launch(p):
    errors = []
    try:
        return p.chromium.launch()
    except Exception as e:  # Playwright's own browser is not installed
        errors.append(f"playwright chromium: {str(e).splitlines()[0]}")
    for exe in find_browsers():
        try:
            return p.chromium.launch(executable_path=exe)
        except Exception as e:
            errors.append(f"{exe}: {str(e).splitlines()[0]}")
    raise SystemExit("screens: no usable Chromium found.\n  " + "\n  ".join(errors))


def main() -> int:
    ap = argparse.ArgumentParser(description="Full-page screenshots of every real page.")
    ap.add_argument("out_dir", help="folder for the PNG files (created if missing)")
    ap.add_argument("--site", default=str(HERE.parent), help="site folder (default: the folder above this script)")
    ap.add_argument("--widths", default="1280,390", help="comma-separated viewport widths (default: 1280,390)")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("screens: Playwright is missing. Run: pip install playwright")

    site = Path(args.site).resolve()
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    pages = real_pages(site)
    if not pages:
        raise SystemExit(f"screens: no pages found in {site}")

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass

    handler = functools.partial(QuietHandler, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}/"

    failed = False
    try:
        with sync_playwright() as p:
            browser = launch(p)
            for page_path in pages:
                stem = re.sub(r"\.html$", "", page_path).replace("/", "-")
                for width in widths:
                    ctx = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1)
                    page = ctx.new_page()
                    problems = []
                    page.on("pageerror", lambda e: problems.append(f"script error: {e}"))
                    page.on("requestfailed", lambda r: problems.append(f"request failed: {r.url}"))
                    try:
                        resp = page.goto(base + page_path, wait_until="networkidle")
                        if resp is None or resp.status >= 400:
                            problems.append(f"HTTP {resp.status if resp else 'none'}")
                        page.wait_for_timeout(250)
                        scroll_w = page.evaluate("document.documentElement.scrollWidth")
                        if scroll_w > width:
                            problems.append(f"scrolls sideways: {scroll_w} px wide")
                        target = out / f"{stem}-{width}.png"
                        page.screenshot(path=str(target), full_page=True)
                        height = page.evaluate("document.documentElement.scrollHeight")
                        print(f"{target.name:44} {height:6d} px high" + ("   " + "; ".join(problems) if problems else ""))
                    except Exception as e:
                        problems.append(str(e).splitlines()[0])
                        print(f"{stem}-{width}: FAILED {problems[-1]}")
                    if problems and any(not x.startswith(("script error", "request failed")) for x in problems):
                        failed = True
                    ctx.close()
            browser.close()
    finally:
        server.shutdown()
    print(f"{len(pages)} pages, {len(widths)} widths, written to {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
