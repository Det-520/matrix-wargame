"""Render a map SVG to PNG in Chromium.

usage: render_png.py <map.svg> <out.png> [scale]
The viewport is the SVG's own size (width and height, or else its viewBox).
"""
import os, re, sys
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1])
root = re.search(r"<svg\b[^>]*>", open(src).read()).group(0)
w, h = re.search(r'\bwidth="([\d.]+)', root), re.search(r'\bheight="([\d.]+)', root)
if w and h:
    W, H = float(w.group(1)), float(h.group(1))
else:
    W, H = map(float, re.search(r'viewBox="[\d.-]+[ ,]+[\d.-]+[ ,]+([\d.]+)[ ,]+([\d.]+)"', root).groups())
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
    pg = b.new_page(viewport={"width": round(W), "height": round(H)}, device_scale_factor=float(sys.argv[3]) if len(sys.argv) > 3 else 1)
    pg.goto("file://" + src); pg.wait_for_timeout(600)
    pg.screenshot(path=sys.argv[2]); b.close()
