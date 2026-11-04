#!/usr/bin/env python3
"""Way2Sec: make a WhatsApp link-preview page + picture for every story and job.

  s/<id>.html   full article page (also gives WhatsApp the story picture) + web/index.html (website home)
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

ARTICLE_CSS = """
:root{--bg:#F4F1EA;--paper:#fff;--ink:#14110D;--muted:#655A4E;--line:#E6DED1;--soft:#FAF6EF;--navy:#12284A;--brand:#C8102E;
--body:'Noto Sans Telugu','Nirmala UI','Gautami',system-ui,sans-serif;--display:'W2S Display','Archivo Black','Arial Black',sans-serif;color-scheme:light}
@font-face{font-family:'W2S Display';src:url(/tools/fonts/ArchivoBlack-Regular.ttf);font-display:swap}
@media (prefers-color-scheme:dark){:root{--bg:#0B111C;--paper:#121A28;--ink:#EEF1F6;--muted:#9AA6B8;--line:#223047;--soft:#162133;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.75 var(--body)}a{color:inherit;text-decoration:none}
.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 80%,transparent);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.bar{max-width:1080px;margin:0 auto;padding:0 20px;height:62px;display:flex;align-items:center;gap:12px}
.bar img{height:30px;display:block}.bar .sp{flex:1}
.btn{display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 15px;border-radius:12px;border:0;background:var(--navy);color:#fff;font:800 13.5px/1 var(--body);cursor:pointer;white-space:nowrap}
.btn.wa{background:linear-gradient(145deg,#2FE47A,#1DA851)}.btn.ghost{background:var(--soft);color:var(--ink);border:1px solid var(--line)}
main{max-width:780px;margin:0 auto;padding:28px 20px 10px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.chip{font-size:13px;font-weight:800;padding:4px 12px;border-radius:999px;background:var(--hl);color:#fff}
.chip.pl{background:var(--soft);color:var(--ink);border:1px solid var(--line)}
h1{margin:0 0 12px;font-size:clamp(26px,4.2vw,38px);line-height:1.35;color:var(--hl)}
@media (prefers-color-scheme:dark){h1{color:color-mix(in srgb,var(--hl) 45%,#fff)}}
.meta{font-size:14px;color:var(--muted);font-weight:700;display:flex;flex-wrap:wrap;gap:4px 14px}
.hero{margin:20px 0;border-radius:20px;overflow:hidden;box-shadow:0 10px 30px -14px rgba(18,40,74,.4)}.hero img{display:block;width:100%;height:auto}
.statbox{margin:20px 0;border-radius:20px;padding:22px 24px;color:#fff;background:linear-gradient(150deg,color-mix(in srgb,var(--hl) 75%,#fff),var(--hl) 55%,color-mix(in srgb,var(--hl) 70%,#000))}
.statbox b{display:block;font:400 48px/1.1 var(--display)}.statbox span{font-weight:800}
.lead{font-size:19px;line-height:1.85;margin:0 0 18px}
.pts{margin:0 0 18px;padding:18px 20px 18px 40px;border-radius:16px;background:var(--paper);border:1px solid var(--line)}
.pts li{margin:6px 0;font-weight:600}
.why{margin:0 0 20px;padding:16px 20px;border-radius:16px;border-left:5px solid var(--hl);background:var(--soft);font-weight:700}
.why small{display:block;color:var(--muted);font-size:13px;font-weight:800}
.src{margin:0 0 22px;font-size:15px;color:var(--muted);font-weight:700}.src a{color:var(--brand);text-decoration:underline}
table.jd{width:100%;border-collapse:collapse;margin:0 0 20px;background:var(--paper);border-radius:16px;overflow:hidden;border:1px solid var(--line)}
table.jd th,table.jd td{text-align:left;padding:11px 16px;border-top:1px solid var(--line);font-size:15.5px;vertical-align:top}table.jd tr:first-child th,table.jd tr:first-child td{border-top:0}
table.jd th{width:34%;color:var(--muted);font-weight:800;background:var(--soft)}
.warn{margin:0 0 20px;padding:12px 16px;border-radius:12px;background:#FCE9EC;color:#8A0B20;font-weight:800;font-size:14.5px}
@media (prefers-color-scheme:dark){.warn{background:#3A1219;color:#FFB3BF}}
.acts{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 30px}
.rel h2{font-size:21px;margin:34px 0 14px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}@media (max-width:560px){.grid{grid-template-columns:1fr}}
.rc{display:block;padding:14px 16px;border-radius:16px;background:var(--paper);border:1px solid var(--line);border-top:4px solid var(--c);font-weight:800;font-size:15.5px;line-height:1.5}
.rc small{display:block;margin-top:6px;color:var(--muted);font-size:12.5px;font-weight:700}.rc:hover{border-color:var(--c)}
footer{max-width:780px;margin:30px auto 0;padding:24px 20px 40px;border-top:1px solid var(--line);color:var(--muted);font-size:13.5px}
footer a{color:var(--brand);font-weight:800}
"""
COLS = {'--c-election':'#B3400F','--c-gov':'#1F6B3A','--c-money':'#16406E','--c-water':'#0B5CAD','--c-power':'#5B3A8C','--c-city':'#7A4A12','--c-job':'#0F6E5C'}
PLACES = {'hyderabad':'హైదరాబాద్','rangareddy':'రంగారెడ్డి','medchal':'మేడ్చల్','adilabad':'ఆదిలాబాద్','bhadradri':'భద్రాద్రి','hanumakonda':'హనుమకొండ','jagtial':'జగిత్యాల','jangaon':'జనగామ','bhupalpally':'భూపాలపల్లి','gadwal':'గద్వాల','kamareddy':'కామారెడ్డి','karimnagar':'కరీంనగర్','khammam':'ఖమ్మం','asifabad':'ఆసిఫాబాద్','mahabubabad':'మహబూబాబాద్','mahabubnagar':'మహబూబ్‌నగర్','mancherial':'మంచిర్యాల','medak':'మెదక్','mulugu':'ములుగు','nagarkurnool':'నాగర్‌కర్నూల్','nalgonda':'నల్గొండ','narayanpet':'నారాయణపేట','nirmal':'నిర్మల్','nizamabad':'నిజామాబాద్','peddapalli':'పెద్దపల్లి','sircilla':'సిరిసిల్ల','sangareddy':'సంగారెడ్డి','siddipet':'సిద్దిపేట','suryapet':'సూర్యాపేట','vikarabad':'వికారాబాద్','wanaparthy':'వనపర్తి','warangal':'వరంగల్','yadadri':'యాదాద్రి','AP':'ఆంధ్రప్రదేశ్'}

def iso_time(s):
    d = dmy(s.get("d", ""))
    if not d: return None
    t = s.get("t") or "12:00"
    return f"{d.isoformat()}T{t}:00+05:30"

def page(sid, s, kind, img, has_card, target, desc, related):
    e = lambda t: html.escape(str(t or ""), quote=True)
    col = COLS.get(s.get("col") or ("--c-job" if kind == "job" else "--c-gov"), "#1F6B3A")
    title = s.get("h", "Way2Sec")
    place = PLACES.get(s.get("place") or "", "")
    chips = f'<span class="chip">{e(s.get("cat") or "వార్త")}</span>' + (f'<span class="chip pl">📍 {e(place)}</span>' if place else "")
    if kind == "job":
        meta = [x for x in [s.get("org"), s.get("d") and f"ప్రచురణ {s['d']}"] if x]
        rows = [("పోస్టులు", s.get("posts")), ("అర్హత", s.get("qual")), ("అనుభవం", s.get("exp")), ("ఎక్కడ", s.get("loc")), ("వయసు", s.get("age")),
                ("జీతం", s.get("pay")), ("చివరి తేదీ", s.get("last")), ("వాక్-ఇన్", s.get("walk")), ("ఎలా దరఖాస్తు", s.get("how"))]
        body = (f'<p class="lead">{e(s.get("sum") or s.get("p"))}</p>' +
                '<table class="jd">' + "".join(f"<tr><th>{k}</th><td>{e(v)}</td></tr>" for k, v in rows if v) + "</table>" +
                '<p class="warn">⚠️ ఉద్యోగం కోసం ఎవరికీ డబ్బులు ఇవ్వకండి. అధికారిక వెబ్‌సైట్‌లోనే దరఖాస్తు చేయండి.</p>')
        apply = s.get("apply") or s.get("url")
        src = f'<p class="src">మూలం: {e(s.get("src"))}' + (f' · <a href="{e(apply)}" target="_blank" rel="noopener nofollow">అధికారిక వెబ్‌సైట్ →</a>' if apply else "") + "</p>"
    else:
        meta = [x for x in [s.get("d"), s.get("t"), s.get("src") and f"Source: {s['src']}"] if x]
        pts = s.get("pts") or []
        body = (f'<p class="lead">{e(s.get("p"))}</p>' +
                ('<ul class="pts">' + "".join(f"<li>{e(x)}</li>" for x in pts) + "</ul>" if pts else "") +
                (f'<p class="why"><small>ఇది ఎందుకు ముఖ్యం?</small>{e(s.get("why"))}</p>' if s.get("why") else ""))
        src = f'<p class="src">మూలం: {e(s.get("src"))}' + (f' · <a href="{e(s.get("url"))}" target="_blank" rel="noopener nofollow">పూర్తి వార్త చదవండి →</a>' if s.get("url") else "") + "</p>"
    visual = f'<div class="statbox"><b>{e(s.get("stat"))}</b><span>{e(s.get("statl"))}</span></div>' if s.get("stat") else ''
    share_text = f"{title}\n{SITE}/s/{sid}"
    rel = "".join(f'<a class="rc" style="--c:{COLS.get(r.get("col") or "--c-gov","#1F6B3A")}" href="/s/{rid}">{e(r.get("h"))}<small>{e(r.get("src"))} · {e(r.get("d"))}</small></a>' for rid, r in related)
    published = iso_time(s)
    if kind == "job":
        ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": title[:110], "image": [img],
              "datePublished": published, "author": {"@type": "Organization", "name": "Way2Sec"},
              "publisher": {"@type": "Organization", "name": "Way2Sec", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}},
              "mainEntityOfPage": f"{SITE}/s/{sid}"}
    else:
        ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": title[:110], "image": [img],
              "datePublished": published, "dateModified": published, "inLanguage": "te",
              "author": {"@type": "Organization", "name": "Way2Sec"},
              "publisher": {"@type": "Organization", "name": "Way2Sec", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}},
              "mainEntityOfPage": f"{SITE}/s/{sid}", "isBasedOn": s.get("url") or None}
    ld = {k: v for k, v in ld.items() if v}
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
<meta name="theme-color" content="#12284A"><link rel="icon" href="/favicon-48.png"><link rel="manifest" href="/manifest.webmanifest">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{ARTICLE_CSS}</style>
</head><body style="--hl:{col}">
<header class="top"><div class="bar"><a href="/web/" aria-label="Way2Sec హోమ్"><img src="/logo.png" alt="Way2Sec"></a><span class="sp"></span>
<a class="btn ghost" href="/web/">🖥️ హోమ్</a><a class="btn" href="{e(target)}">📱 కార్డుల్లో చదవండి</a></div></header>
<main><article>
<div class="chips">{chips}</div>
<h1>{e(title)}</h1>
<div class="meta">{"".join(f"<span>{e(x)}</span>" for x in meta)}</div>
{visual}
{body}
{src}
<div class="acts">
<a class="btn wa" href="https://wa.me/?text={html.escape(__import__('urllib.parse').parse.quote(share_text), quote=True)}" target="_blank" rel="noopener">WhatsAppలో షేర్ చేయండి</a>
<button class="btn ghost" type="button" id="listen">🔊 తెలుగులో వినండి</button>
<a class="btn ghost" href="https://whatsapp.com/channel/0029Vb9nNd8CBtxIYFryH138" target="_blank" rel="noopener">Way2Sec ఛానెల్‌లో చేరండి</a>
</div>
</article>
{('<section class="rel"><h2>ఇవి కూడా చదవండి</h2><div class="grid">' + rel + '</div></section>') if rel else ''}
</main>
<footer>Way2Sec – Fastest AI News in Telugu · సారాంశాలు మా సొంత మాటల్లో; అసలు మూలం పైన పేర్కొన్నాం. · <a href="/web/">హోమ్</a> · <a href="/privacy.html">Privacy</a></footer>
<script>
document.getElementById('listen').onclick=function(){{var sy=window.speechSynthesis;if(!sy)return;if(sy.speaking){{sy.cancel();return;}}
var t=Array.prototype.map.call(document.querySelectorAll('h1,.lead,.pts li,.why'),function(n){{return n.textContent}}).join('. ');
var u=new SpeechSynthesisUtterance(t);u.lang='te-IN';u.rate=.95;var v=sy.getVoices().filter(function(v){{return /^te/i.test(v.lang)}})[0];if(v)u.voice=v;sy.speak(u);}};
</script>
</body></html>
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

        raw = [("news", s) for s in news + days] + [("job", j) for j in jobs]
        normed = pg.evaluate("(arr)=>arr.map(a=>{const s=a[0]==='job'?normJob(a[1]):a[1]; return [a[0], s, sid(s)];})", raw)
        uniq, seen = [], set()
        for kind, s, sid in normed:
            if sid in seen: continue
            seen.add(sid); uniq.append((kind, s, sid))
        secs = lambda s: s.get("sec") if isinstance(s.get("sec"), list) else ([s.get("sec")] if s.get("sec") else [])
        for kind, s, sid in uniq:
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
                related = [(rid, r) for k2, r, rid in uniq if k2 == "job" and rid != sid][:4]
            else:
                iso = d.isoformat() if d else ""
                target = f"/?d={iso}&s={sid}" if iso else f"/?s={sid}"
                desc = (s.get("p") or "")[:160]
                mine = set(secs(s))
                related = [(rid, r) for k2, r, rid in uniq if k2 == "news" and rid != sid and mine & set(secs(r))][:4]
            out = page(sid, s, kind, img, os.path.exists(img_path), target, desc, related)
            sp = os.path.join(ROOT, "s", sid + ".html")
            prev = open(sp, encoding="utf-8").read() if os.path.exists(sp) else None
            if prev != out:
                with open(sp, "w", encoding="utf-8") as f: f.write(out)
                pages += 1
        # website home page (template + the app's card drawings)
        app = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        a0 = app.index("const ART = {"); a1 = app.index("\n};", a0) + 3
        tpl = open(os.path.join(ROOT, "tools", "web_template.html"), encoding="utf-8").read()
        os.makedirs(os.path.join(ROOT, "web"), exist_ok=True)
        web = tpl.replace("/*ART*/", app[a0:a1])
        wp = os.path.join(ROOT, "web", "index.html")
        if not os.path.exists(wp) or open(wp, encoding="utf-8").read() != web:
            with open(wp, "w", encoding="utf-8") as f: f.write(web)
        b.close()
    srv.shutdown()
    print(f"previews: {made} new pictures, {pages} pages written, {removed} old pictures removed")

if __name__ == "__main__":
    sys.exit(main())
