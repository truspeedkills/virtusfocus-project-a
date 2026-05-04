"""
Build Selected_App_Mockup_Printouts.pdf for the GTM artifact packet.

4 pages, one per screen, each with: page header, screen title, phone-frame
rendering of the screen, and a two-part annotation block (what you're looking
at + breakout question). Letter portrait, 0.5" margins.

Approach:
1. Read the walkthrough gallery's CSS (phone-frame + status-bar styles) and
   JavaScript (helper functions + the 4 needed render functions).
2. Strip the JS pieces specific to the gallery's runtime (sidebar, scaling,
   selectScreen) since the print page renders 4 phones statically.
3. Build a self-contained print HTML with a 4-page layout.
4. Convert HTML -> PDF via Chrome headless --print-to-pdf.

Run from project root:
    python scripts/build_mockup_printouts.py
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GALLERY = REPO_ROOT / "Focus Group Materials" / "Mockup Walkthrough" / "Mockup_Walkthrough_Gallery.html"
OUT_HTML = REPO_ROOT / "Focus Group Materials" / "Artifact Packets" / "Selected_App_Mockup_Printouts.html"
OUT_PDF = REPO_ROOT / "Focus Group Materials" / "Artifact Packets" / "Selected_App_Mockup_Printouts.pdf"

CHROME_CANDIDATES = [
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
]

# 4 screens for the GTM packet (per Mockup Walkthrough Handoff decision g).
SCREENS = [
    {
        "render": "renderHomeMorningActive",
        "title": "Home (Morning)",
        "subtitle": "8:12 AM, daily entry point",
        "what": (
            "The athlete's daily entry point. The Focus Word ('STALWART') is "
            "pre-generated coaching content the athlete reads, not creates. "
            "The Mindset Tune-Up CTA is the one required ritual for the day. "
            "Bullseye and Coaching Feedback are secondary cards, always "
            "present, always glanceable. The Coaching Feedback preview shows "
            "the most recent message from Coach Arron in the athlete's Inbox."
        ),
        "ask": (
            "Is '30 seconds in the morning, anchored to a single word' "
            "something an athlete actually opens, or another notification "
            "they'd bury? What positioning makes this feel essential rather "
            "than optional?"
        ),
    },
    {
        "render": "renderTuneUpActive",
        "title": "Mindset Tune-Up (Active)",
        "subtitle": "Active first interaction of the day",
        "what": (
            "The Morning Mindset Tune-Up frames the day. Focus Word, "
            "performance prompt, mindset challenge to accept or decline, "
            "and an intention. Total time: roughly 30 seconds. This is the "
            "only daily input the athlete is asked to complete, and the "
            "anchor that everything else builds from."
        ),
        "ask": (
            "At what price point does a 30-second daily ritual feel "
            "high-value to your athletes or coaching staff? What kills "
            "compliance: too long, too short, too generic, or wrong moment "
            "of the day?"
        ),
    },
    {
        "render": "renderRecapActive",
        "title": "Weekly Recap (Active)",
        "subtitle": "Sunday evening, closes the week",
        "what": (
            "The five-question recap that closes the week. Stats at the top "
            "show how the week went. Quick ratings and the Forward Anchor "
            "are the gate. Submitting fires the AI pipeline that produces "
            "the Weekly Coaching Message and Deep Dive that arrive in the "
            "athlete's Inbox shortly after."
        ),
        "ask": (
            "Is Sunday evening the right ask? What would have to be true "
            "about the institutional environment, or the athlete's own "
            "incentive structure, for this to get done weekly without "
            "becoming a chore?"
        ),
    },
    {
        "render": "renderInboxFeed",
        "title": "Inbox (Feed)",
        "subtitle": "Where coaching lands",
        "what": (
            "Two coaching streams in one feed. Daily snippets at the top "
            "(yesterday-to-today bridge, roughly thirty words, Coach Arron "
            "voice). The Weekly Coaching Message (amber-bordered card) is "
            "the substantive output, and the message in the athlete's packet "
            "is exactly this card. The Deep Dive preview leads to long-form "
            "analysis. Same coach voice across both cadences."
        ),
        "ask": (
            "Is this the right artifact set for an athlete? Would your "
            "coaching staff want their own institutional view of the same "
            "data? Is the daily cadence 'right' or noise?"
        ),
    },
]


def find_chrome() -> Path:
    for c in CHROME_CANDIDATES:
        if c.exists():
            return c
    raise RuntimeError("Chrome not found; install or update CHROME_CANDIDATES.")


def extract_gallery_assets(gallery_text: str) -> tuple[str, str]:
    """Return (css, js) extracted from the gallery, with runtime-only JS stripped."""
    css_match = re.search(r"<style>(.*?)</style>", gallery_text, re.DOTALL)
    if not css_match:
        raise RuntimeError("Could not find <style> block in gallery")
    css = css_match.group(1)

    # Grab the script that begins with the SCREEN REGISTRY comment.
    js_match = re.search(
        r"<script>\s*(// ─+\s*//\s*SCREEN REGISTRY.*?)</script>",
        gallery_text,
        re.DOTALL,
    )
    if not js_match:
        raise RuntimeError("Could not find main <script> block in gallery")
    js = js_match.group(1)

    # Strip runtime-only pieces. Print page doesn't need a sidebar, scaling,
    # or screen selection logic. Each replacement uses a re.sub for one block
    # whose end is the next "  }\n" line at column 2.
    def strip_function(name: str, src: str) -> str:
        pattern = re.compile(
            r"  function " + re.escape(name) + r"\([^)]*\) \{.*?\n  \}\n",
            re.DOTALL,
        )
        new_src, count = pattern.subn("", src)
        if count != 1:
            raise RuntimeError(f"Expected to strip 1 {name}, stripped {count}")
        return new_src

    for fname in ("buildSidebar", "selectScreen", "scalePhoneFrame"):
        js = strip_function(fname, js)

    # Strip init block and event listeners after scalePhoneFrame removal.
    js = re.sub(r"  window\.addEventListener.*?\n", "", js)
    js = re.sub(r"  // Re-scale.*?\n", "", js)
    js = re.sub(r"  requestAnimationFrame\(scalePhoneFrame\);\n", "", js)
    js = re.sub(r"  // Init.*?\n", "", js)
    js = re.sub(r"  buildSidebar\(\);\n", "", js)
    js = re.sub(r"  selectScreen\(0\);\n", "", js)
    js = re.sub(r"  scalePhoneFrame\(\);\n", "", js)

    # Remove the statusConfig block, only used by buildSidebar's status sub-pill,
    # and not needed by render functions. Safe to leave but cleaner to drop.
    # (Actually leave it. Harmless, and removal would require careful matching.)

    return css, js


def build_print_html(css: str, js: str) -> str:
    pages = []
    for i, s in enumerate(SCREENS):
        pages.append(
            f"""
  <section class="page">
    <header class="page-header">
      <span class="brand"><span class="brand-virtus">Virtus</span><span class="brand-focus">Focus</span></span>
      <span class="brand-meta">App Mockup &middot; Page {i + 1} of {len(SCREENS)}</span>
    </header>
    <div class="screen-title">
      <div class="screen-title-main">{s['title']}</div>
      <div class="screen-title-sub">{s['subtitle']}</div>
    </div>
    <div class="phone-area">
      <div class="phone-wrapper">
        <div class="phone-frame">
          <div class="screen-content" id="screen-{i + 1}"></div>
        </div>
      </div>
    </div>
    <div class="annotation">
      <div class="anno-block">
        <div class="anno-label">What you're looking at</div>
        <div class="anno-body">{s['what']}</div>
      </div>
      <div class="anno-block">
        <div class="anno-label">For the breakout</div>
        <div class="anno-body">{s['ask']}</div>
      </div>
    </div>
    <footer class="page-footer">VirtusFocus Focus Group &middot; May 9, 2026 &middot; Confidential under NDA</footer>
  </section>"""
        )

    populate_calls = "\n      ".join(
        f"document.getElementById('screen-{i + 1}').innerHTML = {s['render']}();"
        for i, s in enumerate(SCREENS)
    )

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <title>VirtusFocus: Selected App Mockup Printouts</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{ extend: {{ colors: {{ zinc: {{ 950: '#09090b' }} }} }} }}
    }}
  </script>
  <style>
{css}

    /* Print page setup */
    @page {{ size: letter; margin: 0.5in; }}
    html, body {{ background: white; color: #111827; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}

    .page {{
      page-break-after: always;
      height: 10in;
      display: grid;
      grid-template-rows: auto auto 1fr auto auto;
      gap: 0.12in;
    }}
    .page:last-child {{ page-break-after: auto; }}

    .page-header {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      padding-bottom: 0.06in;
      border-bottom: 1px solid #e5e7eb;
    }}
    .brand {{ font-size: 14px; font-weight: 800; letter-spacing: -0.3px; }}
    .brand-virtus {{ color: #111827; }}
    .brand-focus {{ color: #f59e0b; }}
    .brand-meta {{
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: #6b7280;
      text-transform: uppercase;
    }}

    .screen-title-main {{
      font-size: 20px;
      font-weight: 800;
      color: #111827;
      letter-spacing: -0.01em;
    }}
    .screen-title-sub {{
      font-size: 12px;
      color: #6b7280;
      margin-top: 2px;
    }}

    .phone-area {{
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    /* Scale the native 375x812 phone-frame to fit the print page. */
    .phone-wrapper {{
      width: 244px;   /* 375 * 0.65 */
      height: 528px;  /* 812 * 0.65 */
      position: relative;
    }}
    .phone-area .phone-frame {{
      transform: scale(0.65);
      transform-origin: top left;
      box-shadow: 0 0 0 1px #3f3f46, 0 8px 16px rgba(0,0,0,0.18), inset 0 0 0 1px rgba(255,255,255,0.04);
    }}

    .annotation {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.25in;
      padding-top: 0.05in;
      border-top: 1px solid #e5e7eb;
    }}
    .anno-label {{
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: #6b7280;
      text-transform: uppercase;
      margin-bottom: 0.05in;
    }}
    .anno-body {{
      font-size: 11.5px;
      color: #1f2937;
      line-height: 1.55;
    }}

    .page-footer {{
      font-size: 9px;
      color: #9ca3af;
      text-align: center;
      letter-spacing: 0.04em;
      padding-top: 0.05in;
      border-top: 1px solid #f3f4f6;
    }}

    /* Inside the phone-frame we keep the dark zinc-950 background and white
       text from the gallery's CSS. Tailwind dark mode comes via class on
       <html>, so the screen content renders identically to the gallery. */
  </style>
</head>
<body>
{''.join(pages)}

  <script>
{js}

      // Populate phone screens
      {populate_calls}
  </script>
</body>
</html>
"""


def main() -> None:
    chrome = find_chrome()
    gallery_text = GALLERY.read_text(encoding="utf-8")
    css, js = extract_gallery_assets(gallery_text)
    html = build_print_html(css, js)

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")

    # Convert to PDF via Chrome headless. Use --virtual-time-budget to give
    # tailwind CDN a chance to load and DOM to settle.
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=10000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={OUT_PDF}",
        "--no-pdf-header-footer",
        OUT_HTML.as_uri(),
    ]
    print("Running Chrome:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Chrome stderr:", result.stderr, file=sys.stderr)
        raise RuntimeError(f"Chrome failed (exit {result.returncode})")
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
