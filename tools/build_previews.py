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

SITE_SECS = [('telangana','తెలంగాణ'),('ap','ఆంధ్రప్రదేశ్'),('india','దేశం'),('world','ప్రపంచం'),('ai','AI & టెక్'),('jobs','ఉద్యోగ వార్తలు'),('business','బిజినెస్'),('education','విద్య'),('agri','వ్యవసాయం'),('weather','వాతావరణం'),('sports','క్రీడలు')]
ARTICLE_CSS = """
.agrid{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:28px;margin-top:28px;align-items:start}
@media (max-width:1020px){.agrid{grid-template-columns:1fr}}
.ar{border-radius:24px;background:var(--paper);box-shadow:var(--shadow);overflow:hidden}
.ar .pnl{position:relative;padding:28px 32px;color:#fff;min-height:220px;display:flex;flex-direction:column;justify-content:space-between;background:radial-gradient(130% 120% at 85% 0%,color-mix(in srgb,var(--hl) 70%,#fff) 0,var(--hl) 45%,color-mix(in srgb,var(--hl) 70%,#000) 100%)}
.ar .pnl .art2{position:absolute;right:-10px;bottom:-24px;width:270px;height:270px;opacity:.2}
.ar .chips{display:flex;flex-wrap:wrap;gap:8px}
.ar .stat{font:400 clamp(40px,5.5vw,68px)/1 var(--display);margin-top:16px}
.ar .stat.te{font:800 clamp(34px,4.6vw,54px)/1.25 var(--body)}
.ar .statl{font-weight:800;font-size:18px;max-width:34ch}
.ar .in{padding:26px 32px 30px}
@media (max-width:640px){.ar .pnl,.ar .in{padding-left:20px;padding-right:20px}}
.ar h1{margin:0 0 12px;font-size:clamp(26px,3.4vw,40px);line-height:1.35;color:var(--hlink)}
.ar .alead{font-size:19px;line-height:1.85;margin:16px 0 18px}
.ar .pts{margin:0 0 18px;padding:16px 20px 16px 40px;border-radius:16px;background:var(--soft);border:1px solid var(--line)}
.ar .pts li{margin:6px 0;font-weight:700}
.ar .why{margin:0 0 20px;padding:16px 20px;border-radius:16px;border-left:5px solid var(--hl);background:var(--soft);font-weight:700}
.ar .why small{display:block;color:var(--hlink);font-size:13px;font-weight:800}
.ar .src{margin:0 0 22px;font-size:15px;color:var(--muted);font-weight:700}.ar .src a{color:var(--brand);text-decoration:underline}
table.jd{width:100%;border-collapse:collapse;margin:16px 0 20px;border-radius:16px;overflow:hidden;border:1px solid var(--line)}
table.jd th,table.jd td{text-align:left;padding:11px 16px;border-top:1px solid var(--line);font-size:15.5px;vertical-align:top}
table.jd tr:first-child th,table.jd tr:first-child td{border-top:0}
table.jd th{width:34%;color:var(--muted);font-weight:800;background:var(--soft)}
.warnj{margin:0 0 20px;padding:12px 16px;border-radius:12px;background:#FCE9EC;color:#8A0B20;font-weight:800;font-size:14.5px}
:root[data-theme="dark"] .warnj{background:#3A1219;color:#FFB3BF}
.acts{display:flex;flex-wrap:wrap;gap:10px}
.acts .cta.ghost{background:var(--soft);color:var(--ink);border:1px solid var(--line)}
.aside{display:flex;flex-direction:column;gap:18px;position:sticky;top:70px}
@media (max-width:1020px){.aside{position:static}}
.aside .latest{flex:none}
.brk{background:#C8102E!important;border-color:#C8102E!important;color:#fff!important;animation:brk 1.6s ease-in-out infinite}
@keyframes brk{50%{box-shadow:0 0 0 6px rgba(200,16,46,.25)}}
"""
COLS = {'--c-election':'#B3400F','--c-gov':'#1F6B3A','--c-money':'#16406E','--c-water':'#0B5CAD','--c-power':'#5B3A8C','--c-city':'#7A4A12','--c-job':'#0F6E5C'}
PLACES = {'hyderabad':'హైదరాబాద్','rangareddy':'రంగారెడ్డి','medchal':'మేడ్చల్','adilabad':'ఆదిలాబాద్','bhadradri':'భద్రాద్రి','hanumakonda':'హనుమకొండ','jagtial':'జగిత్యాల','jangaon':'జనగామ','bhupalpally':'భూపాలపల్లి','gadwal':'గద్వాల','kamareddy':'కామారెడ్డి','karimnagar':'కరీంనగర్','khammam':'ఖమ్మం','asifabad':'ఆసిఫాబాద్','mahabubabad':'మహబూబాబాద్','mahabubnagar':'మహబూబ్‌నగర్','mancherial':'మంచిర్యాల','medak':'మెదక్','mulugu':'ములుగు','nagarkurnool':'నాగర్‌కర్నూల్','nalgonda':'నల్గొండ','narayanpet':'నారాయణపేట','nirmal':'నిర్మల్','nizamabad':'నిజామాబాద్','peddapalli':'పెద్దపల్లి','sircilla':'సిరిసిల్ల','sangareddy':'సంగారెడ్డి','siddipet':'సిద్దిపేట','suryapet':'సూర్యాపేట','vikarabad':'వికారాబాద్','wanaparthy':'వనపర్తి','warangal':'వరంగల్','yadadri':'యాదాద్రి','AP':'ఆంధ్రప్రదేశ్'}

def iso_time(s):
    d = dmy(s.get("d", ""))
    if not d: return None
    t = s.get("t") or "12:00"
    return f"{d.isoformat()}T{t}:00+05:30"

SHELL = {}
def shell():
    """Reuse the website's look (styles, top bar, ticker, side rails, footer) from tools/web_template.html."""
    if SHELL: return SHELL
    t = open(os.path.join(ROOT, "tools", "web_template.html"), encoding="utf-8").read()
    SHELL["css"] = t[t.index("<style>") + 7:t.index("</style>")]
    hd = t[t.index('<header class="top">'):t.index('<aside class="rail l"')]
    nav = "".join(f'<a href="/?sec={k}">{n}</a>' for k, n in SITE_SECS) + '<a href="/?jobs=1">💼 జాబ్స్</a>'
    hd = hd.replace('<nav class="secs" id="secs" aria-label="విభాగాలు"></nav>', f'<nav class="secs" aria-label="విభాగాలు"><a href="/">హోమ్</a>{nav}</nav>')
    hd = hd.replace('<label class="search">', '<form class="search" action="/" method="get" role="search"><label style="display:contents">').replace('<kbd>/</kbd></label>', '<kbd>↵</kbd></label></form>')
    hd = hd.replace('<input id="q" type="search"', '<input id="q" name="q" type="search"')
    SHELL["header"] = hd
    SHELL["footer"] = t[t.index("<footer>"):t.index("</footer>") + 9]
    ad = t.index('<a class="ad tall adslot"'); SHELL["ad"] = t[ad:t.index("</a>", ad) + 4].replace("ad tall adslot", "ad adslot").replace('data-ad="rail"', 'data-ad="article" style="min-height:300px"')
    return SHELL

ART_JS = {}
def page(sid, s, kind, img, has_card, target, desc, related):
    e = lambda t: html.escape(str(t or ""), quote=True)
    sh = shell()
    colvar = s.get("col") or ("--c-job" if kind == "job" else "--c-gov")
    title = s.get("h", "Way2Sec")
    place = PLACES.get(s.get("place") or "", "")
    brk = '<span class="chip brk">🔴 BREAKING</span>' if s.get("brk") else ""
    chips = brk + f'<span class="chip">{e(s.get("cat") or "వార్త")}</span>' + (f'<span class="chip">📍 {e(place)}</span>' if place else "")
    stat = str(s.get("stat") or "")
    te = any("ఀ" <= c <= "౿" for c in stat)
    if kind == "job":
        meta = [x for x in [s.get("org"), s.get("d") and f"ప్రచురణ {s['d']}"] if x]
        rows = [("posts", "పోస్టులు", s.get("posts")), ("qual", "అర్హత", s.get("qual")), ("exp", "అనుభవం", s.get("exp")), ("loc", "ఎక్కడ", s.get("loc")), ("age", "వయసు", s.get("age")),
                ("pay", "జీతం", s.get("pay")), ("last", "చివరి తేదీ", s.get("last")), ("walk", "వాక్-ఇన్", s.get("walk")), ("how", "ఎలా దరఖాస్తు", s.get("how"))]
        body = (f'<p class="alead">{e(s.get("sum") or s.get("p"))}</p>' +
                '<table class="jd">' + "".join(f'<tr data-k="{rk}"><th>{k}</th><td>{e(v)}</td></tr>' for rk, k, v in rows if v) + "</table>" +
                '<p class="warnj">⚠️ ఉద్యోగం కోసం ఎవరికీ డబ్బులు ఇవ్వకండి. అధికారిక వెబ్‌సైట్‌లోనే దరఖాస్తు చేయండి.</p>')
        apply = s.get("apply") or s.get("url")
        src = f'<p class="src">మూలం: {e(s.get("src"))}' + (f' · <a href="{e(apply)}" target="_blank" rel="noopener nofollow">అధికారిక వెబ్‌సైట్‌లో దరఖాస్తు →</a>' if apply else "") + "</p>"
    else:
        meta = [x for x in [s.get("d"), s.get("t"), s.get("src") and f"Source: {s['src']}"] if x]
        pts = s.get("pts") or []
        body = (f'<p class="alead">{e(s.get("p"))}</p>' +
                ('<ul class="pts">' + "".join(f"<li>{e(x)}</li>" for x in pts) + "</ul>" if pts else "") +
                (f'<p class="why"><small>ఇది ఎందుకు ముఖ్యం?</small>{e(s.get("why"))}</p>' if s.get("why") else ""))
        src = f'<p class="src">మూలం: {e(s.get("src"))}' + (f' · <a href="{e(s.get("url"))}" target="_blank" rel="noopener nofollow">పూర్తి వార్త చదవండి →</a>' if s.get("url") else "") + "</p>"
    share_text = f"{title}\n{SITE}/s/{sid}"
    trs = {l: {k: s[l][k] for k in ("h", "p", "pts", "why", "cat", "statl", "posts", "qual", "exp", "loc", "age", "how", "walk") if isinstance(s.get(l), dict) and s[l].get(k)} for l in ("en", "hi") if isinstance(s.get(l), dict)}
    trs = {l: v for l, v in trs.items() if v.get("h")}
    tr_json = ('<script type="application/json" id="w2sTr">' + json.dumps(trs, ensure_ascii=False).replace("</", "<\\/") + "</script>") if trs else ""
    import urllib.parse as up
    rel_cards = "".join(
        f'<a class="card" href="/s/{rid}" style="--hl:var({r.get("col") or "--c-gov"});--hlink:var({r.get("col") or "--c-gov"})"><div class="pnl">{r.get("_scene","")}{'<span class="chip brk">🔴 BREAKING</span>' if r.get("brk") else f'<span class="chip">{e(r.get("cat") or "వార్త")}</span>'}<div class="stat">{e(r.get("stat"))}</div></div><div class="bd"><h3>{e(r.get("h"))}</h3><div class="m">{e(r.get("src"))} · {e(r.get("d"))}</div></div></a>'
        for rid, r in related)
    published = iso_time(s)
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": title[:110], "image": [img],
          "datePublished": published, "dateModified": published, "inLanguage": "te",
          "author": {"@type": "Organization", "name": "Way2Sec", "url": SITE},
          "publisher": {"@type": "Organization", "name": "Way2Sec", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}},
          "mainEntityOfPage": f"{SITE}/s/{sid}", "isBasedOn": (s.get("url") if kind == "news" else s.get("apply")) or None}
    ld = {k: v for k, v in ld.items() if v}
    return f"""<!doctype html><html lang="te"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)} | Way2Sec</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Way2Sec News">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/s/{sid}">
<meta property="og:image" content="{e(img)}"><meta property="og:image:secure_url" content="{e(img)}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{e(img)}">
<meta name="theme-color" content="#12284A"><link rel="icon" href="/favicon-48.png"><link rel="manifest" href="/manifest.webmanifest">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>{tr_json}
<style>{sh["css"]}{ARTICLE_CSS}</style>
</head><body>
{sh["header"]}
<main class="wrap">
<div class="agrid">
<article class="ar" style="--hl:var({colvar});--hlink:var({colvar})">
  <div class="pnl">{s.get("_scene","")}
    <div class="chips">{chips}</div>
    <div><div class="stat{' te' if te else ''}">{e(stat)}</div><div class="statl">{e(s.get("statl"))}</div></div></div>
  <div class="in">
    <h1>{e(title)}</h1>
    <div class="meta">{'<span class="dot"></span>'.join(f"<span>{e(x)}</span>" for x in meta)}</div>
    {body}
    {src}
    <div class="acts">
      <a class="cta wa" href="https://wa.me/?text={e(up.quote(share_text))}" target="_blank" rel="noopener">WhatsAppలో షేర్ చేయండి</a>
      <button class="cta ghost" type="button" id="listen">🔊 తెలుగులో వినండి</button>
      <a class="cta ghost" href="{e(target)}">📱 కార్డుల్లో చూడండి</a>
    </div>
  </div>
</article>
<aside class="aside">
  <div class="latest"><h3>⚡ తాజా వార్తలు</h3><div id="latest"></div></div>
  {sh["ad"]}
  <div class="rbox" id="railJobs" hidden><h4>⏰ చివరి తేదీ దగ్గర</h4><div id="railJobsList"></div></div>
  <div class="rbox rqr"><h4>📲 Way2Sec ఛానెల్</h4><img src="/qr.png" alt="Way2Sec WhatsApp ఛానెల్ QR"><p>స్కాన్ చేసి ప్రతి 30 నిమిషాలకు వార్తలు పొందండి</p></div>
</aside>
</div>
{('<section class="sec"><div class="sh"><h2>ఇవి కూడా చదవండి</h2></div><div class="grid">' + rel_cards + '</div></section>') if rel_cards else ''}
<section class="sec"><div class="sh"><h2>మరిన్ని తాజా వార్తలు</h2><a href="/">హోమ్ →</a></div><div class="grid" id="more"></div></section>
</main>
{sh["footer"]}
<script src="/scenes.js" defer></script><script src="/web/site.js" defer></script>
</body></html>
"""


STATIC_PAGES = {
 "about.html": ("మా గురించి | About Way2Sec – మీ సమయానికి విలువ. మీ ఊరి వార్తకు వేదిక.", "WAY2SEC — మీ సమయానికి విలువ. మీ ఊరి వార్తకు వేదిక. ముఖ్యమైన వార్తలను సులభమైన తెలుగులో, క్లుప్తంగా, వేగంగా అందించడమే మా లక్ష్యం.", """
<div class="ab-hero">
  <span class="ab-k">మా గురించి · ABOUT WAY2SEC</span>
  <h1><span class="ab-b">WAY2SEC</span><span class="ab-l1"><span class="ab-pray" aria-hidden="true">🙏</span> మీ సమయానికి విలువ.</span><span class="ab-l2">మీ ఊరి వార్తకు వేదిక.</span></h1>
  <p>ముఖ్యమైన వార్తలను సులభమైన తెలుగులో, క్లుప్తంగా, వేగంగా.</p>
</div>
<div class="ab-body">
  <h2>ఈ ఆలోచన ఎలా పుట్టింది</h2>
  <p class="alead">ఈ రోజుల్లో సమాచారం ఎక్కువగా ఉంది. కానీ <b>ఏం జరిగింది, ఎందుకు జరిగింది, మనకు ఎందుకు ముఖ్యమో</b> తెలుసుకోవడానికి ఎన్నో పేజీలు చదవాల్సి వస్తోంది.</p>
  <p class="alead">ఆ అవసరం నుంచే WAY2SEC ఆలోచన పుట్టింది. ముఖ్యమైన వార్తలను <b>సులభమైన తెలుగులో, క్లుప్తంగా, వేగంగా</b> అందించాలనేది మా లక్ష్యం.</p>

  <h2>మా దృష్టిలో వార్త అంటే</h2>
  <p class="alead">మా దృష్టిలో వార్త అంటే పెద్ద నగరాల్లో జరిగేది మాత్రమే కాదు.</p>
  <div class="ab-grid3">
    <div class="ab-c"><b>🏘️</b><span>ఒక గ్రామంలో పరిష్కారం కోసం ఎదురుచూస్తున్న సమస్య</span></div>
    <div class="ab-c"><b>🎓</b><span>ఒక విద్యార్థి సాధించిన విజయం</span></div>
    <div class="ab-c"><b>🌾</b><span>ఒక రైతు అనుభవం</span></div>
  </div>
  <p class="alead">ఇవి కూడా ప్రజలకు తెలియాల్సిన వార్తలే.</p>

  <h2>AI తో, ఖచ్చితత్వంతో</h2>
  <p class="alead">AI సాంకేతికతను ఉపయోగించి సమాచారాన్ని సులభంగా అందిస్తూ, ప్రతి వార్తలో <b>ఖచ్చితత్వానికి, సందర్భానికి</b> ప్రాధాన్యం ఇవ్వాలనేది మా సంకల్పం.</p>

  <h2>WAY2SEC అనే పేరు</h2>
  <p class="alead">WAY2SEC అనే పేరు <b>వేగానికి ప్రతీక</b>. ప్రతి వార్తను రెండు సెకన్లలో చదవాలనే అర్థం కాదు — కొద్దిసమయంలో ముఖ్యమైన విషయం అర్థమయ్యేలా అందించాలనే ఆలోచన.</p>
</div>

<blockquote class="ab-q">
  <small>మా పెద్ద ఆలోచన ఒక్కటే</small>
  <p>ప్రపంచ వార్త మీ చేతిలోకి రావాలి.</p>
  <p>మీ ఊరి వార్త ప్రపంచానికి చేరాలి.</p>
</blockquote>

<div class="ab-body">
  <h2>మా విలువలు</h2>
  <div class="ab-grid">
    <div class="ab-v"><b>⚡ వేగం</b><span>ప్రతి 30 నిమిషాలకు తాజా వార్తలు – ముఖ్యమైన విషయం కొద్ది సమయంలో.</span></div>
    <div class="ab-v"><b>✍️ సులభమైన తెలుగు</b><span>మా సొంత మాటల్లో, అందరికీ అర్థమయ్యేలా క్లుప్తంగా.</span></div>
    <div class="ab-v"><b>✅ ఖచ్చితత్వం</b><span>నమ్మకమైన వార్తా సంస్థలు, అధికారిక ప్రకటనల నుంచే. ప్రతి వార్తకు అసలు మూలం పేరు, లింక్.</span></div>
    <div class="ab-v"><b>🧭 సందర్భం</b><span>"ఇది ఎందుకు ముఖ్యం?" – ప్రతి వార్తలో మీకు ఏం అర్థం అనేది కూడా.</span></div>
    <div class="ab-v"><b>⚖️ తటస్థత</b><span>రాజకీయ వార్తల్లో వాస్తవాలకే పరిమితం. ఊహాగానాలు, అభిప్రాయాలు ఉండవు.</span></div>
    <div class="ab-v"><b>📍 మీ ఊరు</b><span>గ్రామం, మండలం, జిల్లా నుంచి దేశం, ప్రపంచం వరకు – మీ ప్రాంత వార్తలు ముందుగా.</span></div>
  </div>

  <h2>మీరూ భాగస్వాములు కండి</h2>
  <p class="alead">మీ ఊరిలో జరిగిన ముఖ్యమైన విషయం, పరిష్కారం కావాల్సిన సమస్య, ఎవరైనా సాధించిన విజయం – మాకు పంపండి. పరిశీలించి ప్రపంచానికి చేరుస్తాం.</p>
  <div class="acts"><a class="cta" href="/?tip=1&amp;cards=1" style="background:var(--brand)">📝 మీ ఊరి వార్త పంపండి</a><a class="cta wa" href="https://whatsapp.com/channel/0029Vb9nNd8CBtxIYFryH138" target="_blank" rel="noopener">WhatsApp ఛానెల్‌లో చేరండి</a><a class="cta" href="/contact.html">సంప్రదించండి</a></div>

  <h2>In English</h2>
  <p><b>WAY2SEC — your time matters; a platform for your village's news.</b> Information is everywhere today, yet understanding what happened, why it happened and why it matters to us still means reading page after page. WAY2SEC was born from that need: to deliver the important news in simple Telugu – short, clear and fast. For us, news is not only what happens in big cities; a village problem waiting for a solution, a student's achievement or a farmer's experience is news people deserve to know. We use AI to make information easy to read, while putting accuracy and context first in every story – each one names its original source. The name WAY2SEC stands for speed: not reading every story in two seconds, but understanding what matters in very little time. Our one big idea: <b>the world's news should reach your hands, and your village's news should reach the world.</b></p>
  <p class="why"><small>తప్పు కనిపించిందా? · Spotted an error?</small>ఏదైనా వార్తలో తప్పు ఉంటే <a href="/contact.html" style="color:var(--brand)">మాకు తెలియజేయండి</a> – వెంటనే సరిచేస్తాం.</p>
</div>
"""),
 "contact.html": ("సంప్రదించండి | Contact Way2Sec", "Way2Sec ను సంప్రదించండి – వార్తలు, సవరణలు, ప్రకటనలు.", """
<h1>సంప్రదించండి · Contact us</h1>
<p class="alead">వార్తల సమాచారం, తప్పుల సవరణ, ప్రకటనలు లేదా ఏ ప్రశ్నకైనా మమ్మల్ని సంప్రదించండి.</p>
<table class="jd">
<tr><th>📧 ఈమెయిల్ · Email</th><td><a href="mailto:way2sec.news@gmail.com" style="color:var(--brand);font-weight:800">way2sec.news@gmail.com</a></td></tr>
<tr><th>📝 మీ ఊరి వార్త పంపండి</th><td><a href="/?tip=1&amp;cards=1" style="color:var(--brand);font-weight:800">వార్త పంపే ఫారం →</a></td></tr>
<tr><th>📢 ప్రకటనలు · Advertising</th><td><a href="https://wa.me/917032656422?text=Way2Sec%20advertising" target="_blank" rel="noopener" style="color:var(--brand);font-weight:800">WhatsAppలో సంప్రదించండి →</a></td></tr>
<tr><th>📲 WhatsApp ఛానెల్</th><td><a href="https://whatsapp.com/channel/0029Vb9nNd8CBtxIYFryH138" target="_blank" rel="noopener" style="color:var(--brand);font-weight:800">Way2Sec ఛానెల్‌లో చేరండి →</a></td></tr>
<tr><th>🔒 గోప్యత · Privacy</th><td><a href="/privacy.html" style="color:var(--brand);font-weight:800">Privacy Policy →</a></td></tr>
</table>
<p class="why"><small>సవరణలు · Corrections</small>ఏదైనా వార్తలో తప్పు కనిపిస్తే, ఆ వార్త లింక్‌తో ఈమెయిల్ చేయండి. పరిశీలించి సరిచేస్తాం.</p>
"""),
}

def static_page(title, desc, body):
    sh = shell(); e = lambda t: html.escape(t or "", quote=True)
    return f"""<!doctype html><html lang="te"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#12284A"><link rel="icon" href="/favicon-48.png"><link rel="manifest" href="/manifest.webmanifest">
<meta property="og:title" content="{e(title)}"><meta property="og:image" content="{IMG}/og-image.jpg">
<style>{sh["css"]}{ARTICLE_CSS}.ar .in h2{{font-size:22px;margin:26px 0 10px}}.ar .in p{{line-height:1.85}}
.ab-hero{{margin:-26px -32px 24px;padding:44px 32px 40px;color:#fff;background:radial-gradient(120% 140% at 100% 0%,#3B2A7A 0,#1A2C55 45%,#0B1A33 100%);position:relative;overflow:hidden}}
.ab-hero:after{{content:"";position:absolute;right:-60px;top:-60px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(200,16,46,.55),transparent 65%)}}
.ab-k{{font:400 12px/1 var(--display);letter-spacing:.14em;color:var(--gold)}}
.ab-hero h1{{margin:14px 0 12px;line-height:1.3;color:#fff;position:relative;z-index:1}}
.ab-b{{display:block;font:400 clamp(30px,4.6vw,48px)/1.1 var(--display);letter-spacing:.02em;margin-bottom:10px}}
.ab-l1{{display:block;white-space:nowrap;color:var(--gold);font-size:clamp(22px,3.5vw,38px)}}
.ab-l2{{display:block;font-size:clamp(22px,3.5vw,38px)}}
.ab-pray{{display:inline-block;margin-right:4px;animation:pray 2.4s ease-in-out infinite;transform-origin:50% 80%}}
@keyframes pray{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-8deg) scale(1.08)}}}}
@media (prefers-reduced-motion:reduce){{.ab-pray{{animation:none}}}}
.ab-hero p{{margin:0;font-size:18px;color:#D6DEEA;font-weight:700;position:relative;z-index:1}}
.ab-grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:6px 0 14px}}@media (max-width:640px){{.ab-grid3{{grid-template-columns:1fr}}}}
.ab-c{{padding:18px;border-radius:16px;background:var(--soft);border:1px solid var(--line);font-weight:800;line-height:1.5}}.ab-c b{{display:block;font-size:30px;margin-bottom:6px}}
.ab-q{{margin:28px -32px;padding:34px 32px;background:linear-gradient(135deg,#C8102E,#8A0B20);color:#fff;text-align:center}}
.ab-q small{{display:block;font-weight:800;color:#FFD54A;letter-spacing:.04em;margin-bottom:10px}}.ab-q p{{margin:4px 0;font-size:clamp(22px,3.4vw,34px);font-weight:800;line-height:1.45}}
.ab-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}@media (max-width:640px){{.ab-grid{{grid-template-columns:1fr}}}}
.ab-v{{padding:16px 18px;border-radius:16px;border:1px solid var(--line);background:var(--paper);border-left:5px solid var(--brand)}}.ab-v b{{display:block;font-size:17px;margin-bottom:4px}}.ab-v span{{color:var(--muted);font-weight:600;font-size:15px;line-height:1.6}}
@media (max-width:640px){{.ab-hero,.ab-q{{margin-left:-20px;margin-right:-20px;padding-left:20px;padding-right:20px}}}}
</style>
</head><body>
{sh["header"]}
<main class="wrap"><div class="agrid"><article class="ar" style="--hl:var(--c-money);--hlink:var(--c-money)"><div class="in">{body}</div></article>
<aside class="aside"><div class="latest"><h3>⚡ తాజా వార్తలు</h3><div id="latest"></div></div><div class="rbox rqr"><h4>📲 Way2Sec ఛానెల్</h4><img src="/qr.png" alt="Way2Sec WhatsApp ఛానెల్ QR"><p>స్కాన్ చేసి ప్రతి 30 నిమిషాలకు వార్తలు పొందండి</p></div></aside></div></main>
{sh["footer"]}
<script src="/scenes.js" defer></script><script src="/web/site.js" defer></script>
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
        normed = pg.evaluate("(arr)=>arr.map(a=>{const s=a[0]==='job'?normJob(a[1]):a[1]; s._scene=sceneSVG(s,'scene'); return [a[0], s, sid(s)];})", raw)
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
        # shared script for article pages (ticker, latest, jobs, more news, theme, listen)
        app0 = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        b0 = app0.index("const ART = {"); b1 = app0.index("\n};", b0) + 3
        site_js = open(os.path.join(ROOT, "tools", "site_js.js"), encoding="utf-8").read().replace("/*ART*/", app0[b0:b1])
        os.makedirs(os.path.join(ROOT, "web"), exist_ok=True)
        sj = os.path.join(ROOT, "web", "site.js")
        if not os.path.exists(sj) or open(sj, encoding="utf-8").read() != site_js:
            with open(sj, "w", encoding="utf-8") as f: f.write(site_js)
        for name, (t, dsc, body) in STATIC_PAGES.items():
            out = static_page(t, dsc, body); fp = os.path.join(ROOT, name)
            if not os.path.exists(fp) or open(fp, encoding="utf-8").read() != out:
                with open(fp, "w", encoding="utf-8") as f: f.write(out)
        # sitemap for Google (home, sections, static pages, every article) + robots.txt
        urls = [(SITE + "/", None), (SITE + "/about.html", None), (SITE + "/contact.html", None), (SITE + "/privacy.html", None)]
        urls += [(f"{SITE}/?sec={k}", None) for k, _ in SITE_SECS]
        for kind, s, sid in uniq:
            urls.append((f"{SITE}/s/{sid}", iso_time(s)))
        sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u, lm in urls:
            sm.append(f"<url><loc>{html.escape(u)}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>")
        sm.append("</urlset>")
        with open(os.path.join(ROOT, "web", "sitemap.xml"), "w", encoding="utf-8") as f: f.write("\n".join(sm) + "\n")
        rb = f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/web/sitemap.xml\n"
        with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f: f.write(rb)
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
