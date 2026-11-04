#!/usr/bin/env python3
"""Way2Sec: make a WhatsApp link-preview page + picture for every story and job.

  s/<id>.html   tiny page with the story's title/picture tags, then it opens the story in the app
  cards/<id>.jpg 1200x630 preview picture (same look as the app cards)

Run from anywhere:  python3 tools/build_previews.py
Only new stories get pictures (existing ones are kept). Pictures of news older than KEEP_DAYS
are removed again to keep the site small; their pages then show the general Way2Sec picture.
Needs Playwright + Chromium (pre-installed in the cloud sessions).
"""
import json, os, glob, base64, html, threading, functools, datetime, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://way2sec.news"
# pictures are served from GitHub directly: always-valid HTTPS and live the moment they are pushed
IMG = "https://raw.githubusercontent.com/WAY2SEC/way2sec.github.io/main"
KEEP_DAYS = 21

def load(p, d):
    try:
        with open(os.path.join(ROOT, p), encoding="utf-8") as f: return json.load(f)
    except Exception: return d

def dmy(d):
    try: return datetime.datetime.strptime(d, "%d.%m.%Y").date()
    except Exception: return None

def page(sid, title, desc, img, target):
    e = lambda t: html.escape(t or "", quote=True)
    return f"""<!doctype html><html lang="te"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Way2Sec</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Way2Sec News">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/s/{sid}">
<meta property="og:image" content="{e(img)}"><meta property="og:image:secure_url" content="{e(img)}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{e(img)}">
<script>location.replace({json.dumps(target)})</script>
<style>body{{margin:0;font:16px system-ui;background:#12284A;color:#fff;display:grid;place-items:center;min-height:100vh}}a{{color:#FFD54A}}</style>
</head><body><a href="{e(target)}">Way2Sec లో చదవండి →</a></body></html>
"""

def main():
    news = load("news.json", {}).get("stories", [])
    days = []
    for p in sorted(glob.glob(os.path.join(ROOT, "archive", "20*.json"))):
        days += load(os.path.relpath(p, ROOT), {}).get("stories", [])
    jobs = load("jobs.json", {}).get("jobs", [])
    os.makedirs(os.path.join(ROOT, "cards"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "s"), exist_ok=True)

    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    handler = functools.partial(Quiet, directory=ROOT)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"

    from playwright.sync_api import sync_playwright
    today = datetime.date.today()
    made = pages = removed = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.route("**/*", lambda r: r.abort() if not r.request.url.startswith(base) and not r.request.url.startswith("data:") else r.continue_())
        pg.goto(base + "/index.html?build=1")
        pg.add_style_tag(content="""
@font-face{font-family:'Noto Sans Telugu';src:url(/tools/fonts/NotoSansTelugu.ttf);font-weight:100 900}
@font-face{font-family:'Archivo Black';src:url(/tools/fonts/ArchivoBlack-Regular.ttf)}""")
        pg.add_script_tag(path=os.path.join(ROOT, "tools", "og.js"))
        pg.evaluate("Promise.all([document.fonts.load(\"800 40px 'Noto Sans Telugu'\"),document.fonts.load(\"600 40px 'Noto Sans Telugu'\"),document.fonts.load(\"40px 'Archivo Black'\")])")

        items, seen = [], set()
        for s in news + days:
            items.append(("news", s))
        for j in jobs:
            items.append(("job", j))
        for kind, raw in items:
            s = pg.evaluate("(a)=>a[0]==='job'?normJob(a[1]):a[1]", [kind, raw])
            sid = pg.evaluate("(s)=>sid(s)", s)
            if sid in seen: continue
            seen.add(sid)
            d = dmy(s.get("d", ""))
            old = kind == "news" and d and (today - d).days > KEEP_DAYS
            img_path = os.path.join(ROOT, "cards", sid + ".jpg")
            if old:
                if os.path.exists(img_path): os.remove(img_path); removed += 1
                img = IMG + "/og-image.jpg"
            else:
                if not os.path.exists(img_path):
                    url = pg.evaluate("(s)=>ogImage(s)", s)
                    with open(img_path, "wb") as f: f.write(base64.b64decode(url.split(",", 1)[1]))
                    made += 1
                img = f"{IMG}/cards/{sid}.jpg"
            if kind == "job":
                target = f"/?jobs=1&s={sid}"
                desc = " · ".join(x for x in [s.get("posts") and f"{s['posts']} పోస్టులు", s.get("last") and f"చివరి తేదీ {s['last']}", s.get("org")] if x)
            else:
                iso = d.isoformat() if d else ""
                target = f"/?d={iso}&s={sid}" if iso else f"/?s={sid}"
                desc = (s.get("p") or "")[:160]
            out = page(sid, s.get("h", "Way2Sec"), desc, img, target)
            sp = os.path.join(ROOT, "s", sid + ".html")
            prev = open(sp, encoding="utf-8").read() if os.path.exists(sp) else None
            if prev != out:
                with open(sp, "w", encoding="utf-8") as f: f.write(out)
                pages += 1
        b.close()
    srv.shutdown()
    print(f"previews: {made} new pictures, {pages} pages written, {removed} old pictures removed")

if __name__ == "__main__":
    sys.exit(main())
