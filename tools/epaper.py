#!/usr/bin/env python3
"""Way2Sec e-paper: turns one day's stories (archive/YYYY-MM-DD.json) and open jobs into a newspaper PDF.

usage:  python3 tools/epaper.py [YYYY-MM-DD]      (default: today in India)
output: epaper/YYYY-MM-DD.pdf  (+ epaper/index.json listing all issues)

The PDF is locked against copying text and editing (it can be read and printed),
and every page carries the Way2Sec name, date and a faint watermark."""
import json, os, sys, html, datetime, secrets, threading, http.server, functools, socketserver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
LAUNCH = datetime.date(2026, 10, 31)  # first Way2Sec issue
WEEK = ['సోమవారం', 'మంగళవారం', 'బుధవారం', 'గురువారం', 'శుక్రవారం', 'శనివారం', 'ఆదివారం']
MON = ['జనవరి', 'ఫిబ్రవరి', 'మార్చి', 'ఏప్రిల్', 'మే', 'జూన్', 'జులై', 'ఆగస్టు', 'సెప్టెంబర్', 'అక్టోబర్', 'నవంబర్', 'డిసెంబర్']
COLS = {'--c-election': '#B3400F', '--c-gov': '#1F6B3A', '--c-money': '#16406E', '--c-water': '#0B5CAD',
        '--c-power': '#5B3A8C', '--c-city': '#7A4A12', '--c-job': '#0F6E5C'}
e = lambda s: html.escape(str(s or ''))


def secs(s):
    v = s.get('sec')
    return v if isinstance(v, list) else ([v] if v else ['telangana'])


def group(stories):
    """front page + section pages, each story used once"""
    order = sorted(stories, key=lambda s: (not s.get('brk'), s.get('t') or ''), reverse=False)
    order = sorted(stories, key=lambda s: (0 if s.get('brk') else 1, -(int((s.get('t') or '0:0').replace(':', '')))))
    used = set()
    take = lambda l, n: [x for x in l if id(x) not in used][:n]
    def mark(l):
        for x in l: used.add(id(x))
        return l
    front = mark(take(order, 4))
    state = mark(take([s for s in order if (s.get('st') in (None, 'TG', 'AP') and 'telangana' in secs(s))], 12))
    india = mark(take([s for s in order if 'india' in secs(s)], 10))
    world = mark(take([s for s in order if 'world' in secs(s)], 10))
    rest = mark(take(order, 20))
    return front, state, india, world, rest


def story(s, size='', lead=False):
    col = COLS.get(s.get('col'), '#12284A')
    pts = ''.join(f'<li>{e(p)}</li>' for p in (s.get('pts') or []))
    art = f'<div class="scene" data-sid="{e(s["_k"])}" style="background:{col}"><span class="kick">{e(s.get("cat"))}</span><b class="big{' te' if any('ఀ' <= ch <= '౿' for ch in str(s.get('stat') or '')) else ''}">{e(s.get("stat"))}</b><i>{e(s.get("statl"))}</i></div>' if lead or size == 'mid' else ''
    brk = '<span class="brk">BREAKING</span>' if s.get('brk') else ''
    return f'''<article class="st {size}" style="--c:{col}">{art}
  {'' if (lead or size == 'mid') else f'<div class="kick2">{e(s.get("cat"))}</div>'}
  <h2>{brk}{e(s.get('h'))}</h2>
  <p class="p">{e(s.get('p'))}</p>
  {f'<ul class="pts">{pts}</ul>' if pts and size not in ('small', 'mid') else ''}
  {f'<p class="why"><b>ఎందుకు ముఖ్యం?</b> {e(s.get("why"))}</p>' if s.get('why') and size not in ('small', 'mid') else ''}
  <p class="src">మూలం: {e(s.get('src'))}{(' · ' + e(s.get('t')) + ' గం.') if s.get('t') else ''}</p>
</article>'''


def page_head(title, color, date_te, pno):
    return f'<header class="ph"><span class="pt" style="--c:{color}">{title}</span><span class="pm"><b>way2sec</b> · {date_te} · పేజీ {pno}</span></header>'


def build_html(iso, day, jobs):
    d = datetime.date.fromisoformat(iso)
    date_te = f'{d.day} {MON[d.month - 1]} {d.year}'
    wk = WEEK[d.weekday()]
    issue = (d - LAUNCH).days + 1
    stories = [dict(s, _k=str(i)) for i, s in enumerate(day.get('stories') or [])]
    front, state, india, world, rest = group(stories)
    nums = [s for s in stories if s.get('stat')][:5]
    lead, sub = (front[0] if front else None), front[1:4]
    def jobrow(j):
        return f'<tr><td><b>{e(j.get("h"))}</b><small>{e(j.get("org"))}{(" · " + e(j.get("qual"))) if j.get("qual") else ""}</small></td><td class="n">{e(j.get("posts"))}</td><td class="n">{e(j.get("last") or j.get("loc") or "")}</td></tr>'
    jobs = sorted(jobs, key=lambda j: (j.get('last') or '99.99.9999')[6:] + (j.get('last') or '99.99')[3:5] + (j.get('last') or '99')[:2])
    pages = []
    # ---------- front page ----------
    pages.append(f'''<section class="page front">
 <div class="mast">
   <div class="mtop"><span>{wk}, {date_te}</span><span>సంపుటి 1 · సంచిక {issue}</span><span>హైదరాబాద్ · AI ఈ-పేపర్ · ఉచితం</span></div>
   <div class="mname"><img src="/logo.png" alt="Way2Sec"><div class="mtag"><b>వార్తలు క్షణాల్లో!</b><span>Fastest AI News in Telugu · తెలుగులో వేగంగా, క్లుప్తంగా వార్తలు</span></div></div>
   <div class="mbar"><span>📍 తెలంగాణ</span><span>ఆంధ్రప్రదేశ్</span><span>దేశం</span><span>ప్రపంచం</span><span>ఉద్యోగాలు</span><span class="r">way2sec.news</span></div>
 </div>
 <div class="fgrid">
   <div class="flead">{story(lead, 'lead', True) if lead else ''}</div>
   <aside class="fside">
     <div class="box nums"><h3>ఈరోజు సంఖ్యల్లో</h3>{''.join(f'<div class="num"><b class="{'te' if any('ఀ' <= ch <= '౿' for ch in str(s.get('stat') or '')) else ''}" style="color:{COLS.get(s.get("col"), "#12284A")}">{e(s.get("stat"))}</b><span>{e(s.get("statl"))}</span></div>' for s in nums)}</div>
     <div class="box idx"><h3>ఈ సంచికలో</h3>
       <div><span>రాష్ట్రం – తెలంగాణ, ఏపీ</span><b data-p="state">2</b></div><div><span>దేశం</span><b data-p="india">3</b></div><div><span>ప్రపంచం</span><b data-p="world">4</b></div><div><span>ఉద్యోగాలు</span><b data-p="jobs">5</b></div><div><span>మరిన్ని వార్తలు</span><b data-p="rest">6</b></div>
       <p>మొత్తం {len(stories)} వార్తలు · {len(jobs)} ఉద్యోగ ప్రకటనలు</p></div>
   </aside>
 </div>
 <div class="fsub">{''.join(story(s, 'mid') for s in sub)}</div>
</section>''')
    # ---------- section pages ----------
    def sec_page(title, color, items, pno, key):
        if not items: return ''
        first, more = items[0], items[1:]
        return f'''<section class="page" data-p="{key}">{page_head(title, color, date_te, pno)}
  <div class="secopen">{story(first, 'lead', True)}</div>
  <div class="cols">{''.join(story(s) for s in more)}</div></section>'''
    pno = 2
    for title, color, items, key in [('రాష్ట్రం · తెలంగాణ & ఆంధ్రప్రదేశ్', '#1F6B3A', state, 'state'), ('దేశం', '#B3400F', india, 'india'), ('ప్రపంచం', '#5B3A8C', world, 'world')]:
        h = sec_page(title, color, items, pno, key)
        if h: pages.append(h); pno += 1
    # ---------- jobs ----------
    pages.append(f'''<section class="page" data-p="jobs">{page_head('ఉద్యోగాలు · Jobs', '#0F6E5C', date_te, pno)}
  <p class="jintro">ఈరోజు దరఖాస్తు చేయగలిగే ప్రభుత్వ, ప్రైవేట్ ఉద్యోగాలు. పూర్తి వివరాలు, అధికారిక లింకులు: <b>way2sec.news/?jobs=1</b></p>
  <table class="jobs"><thead><tr><th>ఉద్యోగం</th><th class="n">పోస్టులు</th><th class="n">చివరి తేదీ</th></tr></thead><tbody>{''.join(jobrow(j) for j in jobs[:28])}</tbody></table>
  <p class="warn">⚠️ ఉద్యోగం కోసం ఎవరికీ డబ్బులు ఇవ్వకండి. అధికారిక వెబ్‌సైట్‌లోనే దరఖాస్తు చేయండి.</p></section>''')
    pno += 1
    # ---------- more news + back cover ----------
    pages.append(f'''<section class="page" data-p="rest">{page_head('మరిన్ని వార్తలు', '#16406E', date_te, pno)}
  <div class="cols" data-rest="1">{''.join(story(s, 'small') for s in rest)}</div>
  <div class="back">
    <img src="/qr.png" alt="">
    <div><h3>ప్రతి 30 నిమిషాలకు తాజా వార్తలు – మీ ఫోన్‌లోనే</h3>
      <p>Way2Sec WhatsApp ఛానెల్‌లో చేరండి · యాప్: <b>way2sec.news</b></p>
      <p>📝 మీ ఊరి వార్త పంపండి – పరిశీలించి ప్రపంచానికి చేరుస్తాం.</p>
      <p class="fine">ఈ ఈ-పేపర్‌లోని వార్తలు AI సహాయంతో మా మాటల్లో రాసినవి; ప్రతి వార్తకు మూలం పేర్కొన్నాం. © {d.year} Way2Sec. అనుమతి లేకుండా పునఃప్రచురణ, కాపీ నిషిద్ధం.</p></div>
  </div></section>''')
    return f'''<!doctype html><html lang="te"><head><meta charset="utf-8"><title>Way2Sec ఈ-పేపర్ – {date_te}</title>
<style>
@font-face{{font-family:W2Rama;src:url(/tools/fonts/Ramabhadra-Regular.ttf)}}
@font-face{{font-family:W2Serif;src:url(/tools/fonts/NotoSerifTelugu.ttf);font-weight:100 900}}
@font-face{{font-family:W2Sans;src:url(/tools/fonts/NotoSansTelugu.ttf);font-weight:100 900}}
@font-face{{font-family:W2Disp;src:url(/tools/fonts/ArchivoBlack-Regular.ttf)}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:#fff;color:#1A1410;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;padding:11mm 11mm 14mm;position:relative;overflow:hidden;break-after:page;background:#FFFFFF}}
.page::after{{content:"WAY2SEC · {date_te} · way2sec.news";position:absolute;left:11mm;right:11mm;bottom:6mm;font:600 7pt/1 W2Sans;color:#8A7E70;
  border-top:.6pt solid #CFC4B2;padding-top:2.2mm;letter-spacing:.3pt}}
.page::before{{content:"WAY2SEC";position:absolute;left:50%;top:52%;transform:translate(-50%,-50%) rotate(-30deg);font:400 120pt/1 W2Disp;color:rgba(18,40,74,.028);pointer-events:none;white-space:nowrap}}
/* masthead */
.mast{{border-bottom:2.4pt solid #12284A;margin-bottom:4mm}}
.mtop{{display:flex;justify-content:space-between;font:700 7.6pt/1 W2Sans;color:#5E5246;border-bottom:.6pt solid #CFC4B2;padding-bottom:2mm}}
.mname{{display:flex;align-items:center;justify-content:center;gap:6mm;padding:3.5mm 0 2.5mm}}
.mname img{{height:19mm}}
.mtag{{border-left:.8pt solid #CFC4B2;padding-left:5mm;display:grid;gap:1mm}}
.mtag b{{font:400 21pt/1.1 W2Rama;color:#C8102E}} .mtag span{{font:600 8pt/1.3 W2Sans;color:#3B332B}}
.mbar{{display:flex;gap:5mm;background:#12284A;color:#fff;font:700 8pt/1 W2Sans;padding:2.2mm 4mm;margin-bottom:.8mm}} .mbar .r{{margin-left:auto;color:#FFD54A}}
/* stories */
.st{{break-inside:avoid;margin:0 0 4mm}}
.st h2{{font:400 13pt/1.32 W2Rama;margin:1mm 0 1.5mm;color:#14100C;text-wrap:balance}}
.st .p{{font:400 8.6pt/1.62 W2Serif;margin:0 0 1.5mm;text-align:justify}}
.kick2{{font:800 6.8pt/1 W2Sans;color:var(--c);letter-spacing:.2pt;text-transform:uppercase;border-top:2pt solid var(--c);padding-top:1.5mm;display:inline-block}}
.pts{{margin:0 0 1.5mm;padding-left:4mm;font:600 8pt/1.5 W2Sans}} .pts li::marker{{color:var(--c)}}
.why{{font:500 7.8pt/1.5 W2Sans;margin:0 0 1.5mm;background:#F2F4F7;border-left:2pt solid var(--c);padding:1.5mm 2.5mm}} .why b{{color:var(--c)}}
.src{{font:600 6.8pt/1 W2Sans;color:#7A6E60;margin:0}}
.brk{{display:inline-block;background:#C8102E;color:#fff;font:800 7pt/1 W2Sans;padding:1mm 2mm;border-radius:1mm;margin-right:2mm;vertical-align:middle}}
.scene{{position:relative;height:46mm;border-radius:2mm;overflow:hidden;color:#fff;padding:4mm 5mm;display:flex;flex-direction:column;justify-content:flex-end;margin-bottom:2.5mm}}
.scene svg{{position:absolute;inset:0;width:100%;height:100%;opacity:.3}}
.scene>*{{position:relative}}
.scene .kick{{position:absolute;top:3.5mm;left:5mm;border:.8pt solid rgba(255,255,255,.85);border-radius:10mm;padding:.8mm 3mm;font:800 7pt/1.4 W2Sans}}
.scene .big{{font:400 30pt/1 W2Disp}} .scene .big.te{{font:400 26pt/1.15 W2Rama}} .scene i{{font:700 9pt/1.3 W2Sans;font-style:normal;opacity:.95;margin-top:1mm}}
.st.lead h2{{font-size:21pt;line-height:1.28}} .st.lead .p{{font-size:9.6pt;line-height:1.7}}
.st.mid .scene{{height:30mm}} .st.mid .scene .big{{font-size:20pt}} .st.mid h2{{font-size:12pt}}
.st.small h2{{font-size:11pt}} .st.small .p{{font-size:8.2pt}} .st.small .pts,.st.small .why{{display:none}}
/* front grid */
.fgrid{{display:grid;grid-template-columns:1fr 52mm;gap:5mm;border-bottom:.8pt solid #CFC4B2;margin-bottom:4mm}}
.fside{{display:grid;gap:4mm;align-content:start}}
.box{{border:.8pt solid #CFC4B2;border-top:2.4pt solid #12284A;padding:3mm;background:#fff}}
.box h3{{margin:0 0 2.5mm;font:400 11pt/1 W2Rama;color:#12284A}}
.num{{display:grid;border-top:.6pt dashed #DDD3C4;padding:1.8mm 0}} .num b{{font:400 15pt/1.1 W2Disp}} .num b.te{{font:400 14pt/1.2 W2Rama}} .num span{{font:600 7.2pt/1.35 W2Sans;color:#3B332B}}
.idx div{{display:flex;justify-content:space-between;font:700 8pt/1 W2Sans;border-top:.6pt dashed #DDD3C4;padding:2mm 0}} .idx b{{color:#C8102E}} .idx p{{font:600 7pt/1.4 W2Sans;color:#7A6E60;margin:2mm 0 0}}
.fsub{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}}
/* inner pages */
.ph{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2.4pt solid #12284A;padding-bottom:2mm;margin-bottom:4mm}}
.pt{{font:400 19pt/1 W2Rama;color:var(--c)}} .pm{{font:600 7.4pt/1 W2Sans;color:#5E5246}} .pm b{{font:400 9pt/1 W2Disp;color:#12284A}}
.secopen .scene{{height:52mm}}
.secopen{{border-bottom:.8pt solid #CFC4B2;margin-bottom:4mm}}
.cols{{column-count:3;column-gap:5mm;column-rule:.6pt solid #E0D6C6;column-fill:auto}}
.cols .st{{break-inside:auto}} .st h2,.kick2{{break-after:avoid}} .why,.pts li,.src{{break-inside:avoid}} .cols .st .p{{orphans:3;widows:3}}
.jintro{{font:600 9pt/1.5 W2Sans;margin:0 0 3mm}}
table.jobs{{width:100%;border-collapse:collapse;font:600 8pt/1.4 W2Sans}}
table.jobs th{{background:#0F6E5C;color:#fff;text-align:left;padding:2mm 2.5mm;font-weight:800}}
table.jobs td{{border-bottom:.6pt solid #DDD3C4;padding:1.8mm 2.5mm;vertical-align:top}}
table.jobs tr:nth-child(even) td{{background:#F3F5F8}}
table.jobs td small{{display:block;color:#6B5F52;font-weight:600;font-size:7pt}}
table.jobs .n{{text-align:right;white-space:nowrap;width:24mm}}
.warn{{font:800 8.6pt/1.5 W2Sans;color:#B3400F;margin:3mm 0 0}}
.back{{position:absolute;left:11mm;right:11mm;bottom:16mm;display:flex;gap:6mm;align-items:center;background:#12284A;color:#fff;border-radius:3mm;padding:5mm}}
.back img{{width:30mm;height:30mm;background:#fff;padding:1.5mm;border-radius:1.5mm}}
.back h3{{margin:0 0 2mm;font:400 14pt/1.3 W2Rama;color:#FFD54A}} .back p{{margin:0 0 1.5mm;font:600 8.4pt/1.5 W2Sans}} .back .fine{{font-size:6.8pt;color:#B9C4D6;margin:2mm 0 0}}
</style></head><body>{''.join(pages)}
<script src="/scenes.js"></script>
<script>const S={json.dumps(stories, ensure_ascii=False)};
document.querySelectorAll('.scene[data-sid]').forEach(el=>{{ const s=S.find(x=>x._k===el.dataset.sid); if(s) el.insertAdjacentHTML('afterbegin', sceneSVG(s,'ep')); }});
{FIT_JS}</script></body></html>'''


FIT_JS = r'''/* fit every page: stories that do not fit move to a continuation page, nothing is cut */
const MM=96/25.4;
async function fit(){ await document.fonts.ready; let changed=true, guard=0;
  while(changed && guard++<30){ changed=false;
    for(const pg of [...document.querySelectorAll('.page')]){ const c=pg.querySelector('.cols'); if(!c||c.dataset.fit) continue;
      const back=pg.querySelector('.back'); const pr=pg.getBoundingClientRect();
      const limit=(back?back.getBoundingClientRect().top-4*MM:pr.bottom-16*MM);
      c.style.height=Math.max(40,limit-c.getBoundingClientRect().top)+'px'; c.dataset.fit=1;
      const moved=[]; while(c.scrollWidth>c.clientWidth+2 && c.children.length>1){ moved.unshift(c.lastElementChild); c.lastElementChild.remove(); }
      const rest=document.querySelector('.cols[data-rest]');
      if(moved.length && rest && c!==rest && !c.closest('.page.cont')){ moved.reverse().forEach(m=>{ m.classList.add('small'); rest.insertBefore(m,rest.firstChild); }); delete rest.dataset.fit; rest.style.height=''; changed=true; break; }
      if(moved.length){ const np=document.createElement('section'); np.className='page cont'; const ph=pg.querySelector('.ph');
        np.innerHTML=(ph?ph.outerHTML:'')+'<div class="cols"></div>'; const t=np.querySelector('.pt'); if(t&&!/కొనసాగింపు/.test(t.textContent)) t.textContent+=' (కొనసాగింపు)';
        moved.forEach(m=>np.querySelector('.cols').appendChild(m)); (back?pg:pg).after(np); changed=true; break; } } }
  const pgs=[...document.querySelectorAll('.page')], last=pgs[pgs.length-1], back=document.querySelector('.back');
  if(back && last && !last.contains(back)){ const cs=[...last.querySelectorAll('.cols > *')], bot=cs.length?Math.max(...cs.map(x=>x.getBoundingClientRect().bottom)):last.getBoundingClientRect().top+40*MM;
    const room=last.getBoundingClientRect().bottom-16*MM-bot; if(room>back.offsetHeight+8*MM){ last.appendChild(back); const c=last.querySelector('.cols'); if(c) c.style.height=''; } }
  document.querySelectorAll('.idx b[data-p]').forEach(b=>{ const i=pgs.findIndex(p=>p.dataset.p===b.dataset.p); if(i>=0) b.textContent=i+1; else b.parentNode.remove(); });
  document.querySelectorAll('.page').forEach((pg,i)=>{ const pm=pg.querySelector('.pm'); if(pm) pm.innerHTML=pm.innerHTML.replace(/పేజీ \d+/,'పేజీ '+(i+1)); });
  document.body.dataset.ready='1'; }
fit();'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def serve():
    h = functools.partial(Quiet, directory=ROOT)
    srv = socketserver.TCPServer(('127.0.0.1', 0), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    iso = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now(IST).date().isoformat()
    day = json.load(open(os.path.join(ROOT, 'archive', iso + '.json'), encoding='utf-8'))
    try: jobs = json.load(open(os.path.join(ROOT, 'jobs.json'), encoding='utf-8')).get('jobs', [])
    except Exception: jobs = []
    out_dir = os.path.join(ROOT, 'epaper'); os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(ROOT, 'epaper', '_build.html')
    open(tmp, 'w', encoding='utf-8').write(build_html(iso, day, jobs))
    srv = serve()
    from playwright.sync_api import sync_playwright
    raw = os.path.join(out_dir, '_raw.pdf')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/epaper/_build.html'); pg.wait_for_selector('body[data-ready="1"]')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        pg.pdf(path=raw, format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
    srv.shutdown()
    # lock: readers can open and print, but not copy text or edit
    from pypdf import PdfReader, PdfWriter
    from pypdf.constants import UserAccessPermissions as P
    r = PdfReader(raw); w = PdfWriter()
    for pgx in r.pages: w.add_page(pgx)
    w.add_metadata({'/Title': f'Way2Sec ఈ-పేపర్ {iso}', '/Author': 'Way2Sec', '/Subject': 'Fastest AI News in Telugu', '/Creator': 'way2sec.news'})
    w.encrypt(user_password='', owner_password=secrets.token_hex(16), permissions_flag=P.PRINT | P.PRINT_TO_REPRESENTATION, algorithm='AES-256')
    out = os.path.join(out_dir, iso + '.pdf')
    with open(out, 'wb') as f: w.write(f)
    os.remove(raw); os.remove(tmp)
    idx_p = os.path.join(out_dir, 'index.json')
    try: idx = json.load(open(idx_p, encoding='utf-8'))
    except Exception: idx = {'issues': []}
    idx['issues'] = [x for x in idx['issues'] if x.get('iso') != iso] + [{'iso': iso, 'date': day.get('date'), 'pages': len(r.pages), 'stories': len(day.get('stories') or [])}]
    idx['issues'].sort(key=lambda x: x['iso'], reverse=True)
    json.dump(idx, open(idx_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'epaper: {out} · {len(r.pages)} pages · {os.path.getsize(out)//1024} KB')


if __name__ == '__main__':
    main()
