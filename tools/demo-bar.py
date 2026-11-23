#!/usr/bin/env python3
"""Put the site's top bar on a demo page: the brand on the left, a "Back to" button on the right, frozen at the top.

    python3 tools/demo-bar.py <demo index.html> <back link> <back label>

Run it again after a demo is rebuilt; it replaces its own earlier bar. The bar goes right after <body>,
or before the page's first element when the file has no <body> tag.
"""
import html
import re
import sys
from pathlib import Path

START, END = "<!-- demo-bar -->", "<!-- /demo-bar -->"

BAR = START + """<style>
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:700;font-display:swap;src:url("../../assets/fonts/source-serif-4-latin-700-normal.woff2") format("woff2")}
html{scroll-padding-top:72px}
.site-bar{position:sticky;top:0;z-index:35;background:#F7F4EE;border-bottom:1px solid #E2DDD2;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.site-bar .in{box-sizing:border-box;max-width:1120px;min-height:68px;margin:0 auto;padding:10px 24px;display:flex;align-items:center;gap:16px}
.site-bar .brand{font:700 1.2rem "Source Serif 4",Georgia,"Times New Roman",serif;color:#1F2A2E;text-decoration:none;display:flex;align-items:center;gap:10px;min-height:44px;margin-right:auto}
.site-bar .dot{display:inline-grid;grid-template-columns:repeat(3,7px);gap:2px}
.site-bar .dot i{width:7px;height:7px;border-radius:50%;display:block}
.site-bar .back{display:inline-flex;align-items:center;gap:0;min-height:44px;padding:0 20px;border-radius:99px;background:#1F2A2E;color:#fff;font-size:.95rem;font-weight:600;text-decoration:none;white-space:nowrap}
.site-bar .back:hover{background:#0F6E6E}
.site-bar a:focus-visible{outline:3px solid #0F6E6E;outline-offset:2px}
@media (max-width:520px){.site-bar .in{min-height:60px;padding:8px 16px;gap:10px}.site-bar .brand{font-size:1.05rem;gap:8px}.site-bar .back{padding:0 16px}.site-bar .long{display:none}}
</style>
<div class="site-bar"><div class="in"><a class="brand" href="../../index.html"><span aria-hidden="true" class="dot"><i style="background:#0F6E6E"></i><i style="background:#2A5A8C"></i><i style="background:#7A3E6B"></i><i style="background:#4A6B23"></i><i style="background:#A4452C"></i><i style="background:#8A5A00"></i></span>Daniel Cohen</a><a class="back" href="__HREF__" aria-label="Back to __LABEL__"><span aria-hidden="true">&larr;&nbsp;</span>Back<span class="long">&nbsp;to __LABEL__</span></a></div></div>
""" + END


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    path, href, label = Path(sys.argv[1]), sys.argv[2], html.escape(sys.argv[3])
    page = path.read_text()
    page = re.sub(re.escape(START) + ".*?" + re.escape(END) + "\n?", "", page, flags=re.S)
    bar = BAR.replace("__HREF__", html.escape(href)).replace("__LABEL__", label) + "\n"
    m = re.search(r"<body[^>]*>\n?", page)
    if m:
        page = page[:m.end()] + bar + page[m.end():]
    else:
        m = re.search(r"</head>\s*|<div ", page)
        if not m:
            sys.exit(f"{path}: no place for the bar")
        page = page[:m.end()] + bar + page[m.end():] if m.group(0).startswith("</head>") else page[:m.start()] + bar + page[m.start():]
    path.write_text(page)
    print(f"bar added to {path}")


if __name__ == "__main__":
    main()
