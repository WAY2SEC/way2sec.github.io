/* Way2Sec website: shared script for article pages (built into web/site.js by tools/build_previews.py) */
(function(){
/*ART*/
const $=id=>document.getElementById(id);
const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const sid=s=>{let h=5381;const t=(s.url||'')+'|'+(s.h||'');for(let i=0;i<t.length;i++)h=((h<<5)+h+t.charCodeAt(i))|0;return (h>>>0).toString(36)};
const tsOf=s=>{const m=/^(\d\d)\.(\d\d)\.(\d{4})$/.exec(s.d||''),t=/^(\d\d):(\d\d)$/.exec(s.t||'');return m?Date.parse(`${m[3]}-${m[2]}-${m[1]}T${t?t[1]:'12'}:${t?t[2]:'00'}:00+05:30`):0};
const store={get(k,d){try{const v=localStorage.getItem('w2s.'+k);return v?JSON.parse(v):d}catch(e){return d}},set(k,v){try{localStorage.setItem('w2s.'+k,JSON.stringify(v))}catch(e){}}};
const te=v=>/[ఀ-౿]/.test(v||'');
const here=location.pathname.replace(/\.html$/,'').split('/').pop();

/* theme */
function applyTheme(t){const r=document.documentElement; if(!t||t==='auto') r.removeAttribute('data-theme'); else r.setAttribute('data-theme',t);}
applyTheme((store.get('prefs',{})||{}).theme);
const tb=$('theme'); if(tb) tb.onclick=()=>{const r=document.documentElement,cur=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'),nx=cur==='dark'?'light':'dark';applyTheme(nx);const p=store.get('prefs',{})||{};p.theme=nx;store.set('prefs',p);};

/* story drawing in the article header */
document.querySelectorAll('svg[data-art]').forEach(s=>{ s.innerHTML=ART[s.dataset.art]||ART.unity; });

/* listen in Telugu */
const lb=$('listen'); if(lb) lb.onclick=()=>{ const sy=window.speechSynthesis; if(!sy) return; if(sy.speaking){ sy.cancel(); return; }
  const t=[...document.querySelectorAll('.ar h1,.ar .alead,.ar .pts li,.ar .why')].map(n=>n.textContent).join('. ');
  const u=new SpeechSynthesisUtterance(t); u.lang='te-IN'; u.rate=.95; const v=sy.getVoices().find(v=>/^te/i.test(v.lang)); if(v) u.voice=v; sy.speak(u); };

function card(s){ const col=s.col||'--c-gov';
  return `<a class="card" href="/s/${sid(s)}" style="--hl:var(${col});--hlink:var(${col})"><div class="pnl"><svg class="art" viewBox="0 0 200 200" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ART[s.art]||ART.unity}</svg>${s.brk?'<span class="chip brk">🔴 BREAKING</span>':`<span class="chip">${esc(s.cat||'వార్త')}</span>`}<div class="stat${te(s.stat)?' te':''}">${esc(s.stat||'')}</div></div><div class="bd"><h3>${esc(s.h)}</h3><div class="m">${esc(s.src||'')} · ${esc(s.d||'')}${s.t?' · '+esc(s.t):''}</div></div></a>`; }
function daysLeft(j){const m=/^(\d\d)\.(\d\d)\.(\d{4})$/.exec(j.last||'');if(!m)return null;return Math.floor((new Date(+m[3],+m[2]-1,+m[1],23,59,59)-Date.now())/864e5)}
async function getJSON(u){ try{ const r=await fetch(u+'?t='+Date.now(),{cache:'no-store'}); return r.ok?await r.json():null; }catch(e){ return null; } }

(async()=>{
  const [news,jobs]=await Promise.all([getJSON('/news.json'),getJSON('/jobs.json')]);
  const all=((news&&news.stories)||[]).slice().sort((a,b)=>tsOf(b)-tsOf(a)).filter(s=>sid(s)!==here);
  const tk=$('tick'); if(tk) tk.innerHTML=(t=>t+t)(all.slice(0,10).map(s=>`<a href="/s/${sid(s)}"><b>${s.brk?'🔴 BREAKING':esc(s.t||'')}</b>${esc(s.h)}</a>`).join(''));
  const lt=$('latest'); if(lt) lt.innerHTML=all.slice(0,6).map(s=>`<a class="it" href="/s/${sid(s)}"><span class="tm">${esc(s.t||'')}</span><span class="hd">${esc(s.h)}</span></a>`).join('');
  const mo=$('more'); if(mo){ const rel=new Set([...document.querySelectorAll('.sec .card')].map(a=>a.getAttribute('href').split('/').pop()));
    mo.innerHTML=all.filter(s=>!rel.has(sid(s))).slice(6,14).map(card).join(''); }
  const J=((jobs&&jobs.jobs)||[]).map(j=>[j,daysLeft(j)]).filter(x=>x[1]!==null&&x[1]>=0).sort((a,b)=>a[1]-b[1]).slice(0,5);
  if(J.length && $('railJobs')){ $('railJobs').hidden=false;
    $('railJobsList').innerHTML=J.map(([j,d])=>`<a class="rj" href="/s/${sid({url:j.url||j.apply||'',h:j.h})}">${esc(j.h)}<small>${d===0?'ఈరోజే చివరి రోజు':d+' రోజులు మిగిలాయి'} · ${esc(j.org||'')}</small></a>`).join(''); }
})();
})();
