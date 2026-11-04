/* Way2Sec place & topic illustrations (drawn by hand as vector art, 400x200, white silhouettes).
   Used behind the big number on every card. Layers: far (faint), mid, near. */
const SCENES = {
  hyderabad: `
    <g opacity=".35"><path d="M0 200V150h18v-22h14v22h10v-40h16v40h12v-28h20v28h8v-52h18v52h10v-18h14v18H0z"/><path d="M290 200v-58h16v-20h14v20h10v-34h18v34h12v-24h16v24h24v58z"/></g>
    <g>
      <rect x="150" y="128" width="100" height="72"/>
      <path d="M150 128h100v-8H150z"/>
      <path d="M200 74c-10 0-18 9-18 18h36c0-9-8-18-18-18zM198 60h4v14h-4z"/>
      <rect x="184" y="92" width="32" height="28"/>
      ${[148,238].map(x=>`<rect x="${x}" y="44" width="14" height="156"/><rect x="${x-3}" y="78" width="20" height="5"/><rect x="${x-3}" y="104" width="20" height="5"/><path d="M${x} 44c0-9 3-16 7-20 4 4 7 11 7 20z"/><rect x="${x+6}" y="12" width="2" height="12"/>`).join('')}
    </g>
    <path fill="#000" fill-opacity=".001" d="M0 0"/>
    <g fill="var(--hole,#000)" opacity="0"></g>`,
  hyderabadHole: `<path d="M178 200v-38c0-14 10-24 22-24s22 10 22 24v38z"/><path d="M160 200v-26c0-7 4-11 8-11s8 4 8 11v26zM224 200v-26c0-7 4-11 8-11s8 4 8 11v26z"/>`,
  warangal: `
    <g opacity=".35"><path d="M0 200c40-30 80-36 120-30s60 24 80 30H0z"/><path d="M220 200c30-24 80-38 180-26v26z"/></g>
    <g>
      <path d="M120 74c10-16 26-18 34-10l-6 10c-6-4-14-2-20 6z"/><path d="M280 74c-10-16-26-18-34-10l6 10c6-4 14-2 20 6z"/>
      <rect x="128" y="74" width="144" height="14" rx="3"/>
      <rect x="140" y="62" width="120" height="8" rx="2"/>
      <path d="M150 88h100v10H150z"/>
      <rect x="150" y="98" width="18" height="102"/><rect x="232" y="98" width="18" height="102"/>
      <rect x="144" y="188" width="30" height="12"/><rect x="226" y="188" width="30" height="12"/>
      <path d="M168 98h64c0 22-14 36-32 40-18-4-32-18-32-40z" opacity=".55"/>
      <circle cx="200" cy="81" r="4" opacity=".6"/>
    </g>`,
  temple: `
    <g opacity=".35"><path d="M0 200c30-40 70-60 110-60s70 30 90 60z"/><path d="M250 200c20-30 60-44 100-40s50 20 50 40z"/></g>
    <g>
      <path d="M150 200h100l-6-30H156z"/>
      <path d="M156 170h88l-8-26H164z"/>
      <path d="M164 144h72l-8-24H172z"/>
      <path d="M172 120h56l-8-22H180z"/>
      <path d="M180 98h40l-7-18h-26z"/>
      <path d="M187 80h26c0-9-6-14-13-14s-13 5-13 14z"/>
      <rect x="198" y="48" width="4" height="18"/><circle cx="200" cy="46" r="5"/>
      <path d="M190 200v-22c0-6 4-10 10-10s10 4 10 10v22z" opacity=".5"/>
      <rect x="60" y="176" width="10" height="24"/><path d="M52 176h26l-13-14z"/>
      <rect x="330" y="176" width="10" height="24"/><path d="M322 176h26l-13-14z"/>
    </g>`,
  fort: `
    <g opacity=".35"><path d="M0 200c50-70 120-96 200-96s150 26 200 96z"/></g>
    <g>
      <path d="M60 200v-62h10v-8h10v8h10v-8h10v8h10v-8h10v8h10v62z"/>
      <path d="M210 200v-62h10v-8h10v8h10v-8h10v8h10v-8h10v8h10v62z"/>
      <path d="M130 200v-48h80v48z"/>
      <path d="M124 152h92v-8h-8v-8h-8v8h-10v-8h-8v8h-10v-8h-8v8h-10v-8h-8v8h-8v-8h-8v8h-6z"/>
      <circle cx="96" cy="128" r="12"/><circle cx="244" cy="128" r="12"/>
      <path d="M156 200v-26c0-8 6-14 14-14s14 6 14 14v26z" opacity=".5"/>
      <path d="M300 200v-34h10v-6h8v6h8v-6h8v6h10v34z" opacity=".7"/>
    </g>`,
  mine: `
    <g opacity=".35"><path d="M0 200v-26l60-20 70 14 60-24 80 18 70-20 60 16v42z"/></g>
    <g>
      <path d="M130 200l40-130h10l40 130h-12l-33-110-33 110z"/>
      <path d="M146 150h68v6h-68zM158 112h44v6h-44z"/>
      <circle cx="175" cy="64" r="18" fill="none" stroke="#fff" stroke-width="6"/><circle cx="175" cy="64" r="4"/>
      <path d="M175 64l70 136h-8l-66-128z" opacity=".7"/>
      <rect x="250" y="150" width="90" height="50"/><rect x="262" y="120" width="12" height="30"/><rect x="290" y="128" width="10" height="22"/>
      <path d="M40 200v-20h60v20z"/><circle cx="54" cy="200" r="6"/><circle cx="86" cy="200" r="6"/>
    </g>`,
  forest: `
    <g opacity=".35"><path d="M0 200c40-50 90-70 140-70s80 30 110 30 90-40 150-30v70z"/></g>
    <g>
      ${[[40,1],[90,.8],[140,1.15],[200,.9],[250,1.25],[310,.85],[360,1.05]].map(([x,s])=>`<path d="M${x} ${200-120*s}l${22*s} ${40*s}h-${10*s}l${20*s} ${34*s}h-${12*s}l${22*s} ${38*s}h-${104*s}l${22*s}-${38*s}h-${12*s}l${20*s}-${34*s}h-${10*s}z" transform="translate(${-0*s} 0)"/><rect x="${x-3}" y="${200-8*s}" width="6" height="${8*s}"/>`).join('')}
    </g>`,
  river: `
    <g opacity=".35"><path d="M0 120c60-20 120-24 200-10s140 10 200-6v96H0z"/></g>
    <g>
      <path d="M0 148h400v10H0z"/>
      ${[0,1,2,3,4].map(i=>`<path d="M${20+i*76} 200v-30c0-18 14-30 30-30s30 12 30 30v30h-10v-28c0-12-9-20-20-20s-20 8-20 20v28z"/>`).join('')}
      <path d="M0 178q25-10 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v6q-25-10-50 0t-50 0-50 0-50 0-50 0-50 0-50 0-50 0z" opacity=".6"/>
      <path d="M0 192q25-10 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v8H0z" opacity=".45"/>
    </g>`,
  village: `
    <g opacity=".35"><path d="M0 170c80-20 160-24 240-14s120 10 160 4v40H0z"/></g>
    <g>
      <path d="M70 200v-36h52v36z"/><path d="M62 166l34-30 34 30z"/>
      <path d="M150 200v-28h40v28z"/><path d="M144 174l26-24 26 24z"/>
      <path d="M86 200v-16h14v16z" opacity=".5"/>
      ${[[250,1],[300,.8],[30,.75]].map(([x,s])=>`<path d="M${x} 200c-2-40 0-80 6-${110*s}" stroke="#fff" stroke-width="${5*s}" fill="none"/><path d="M${x+6} ${200-110*s}c-20 0-34 10-40 22 14-8 28-12 40-10-18 4-30 14-34 26 12-12 24-18 34-18 0 12-6 24-14 32 12-8 18-20 20-30 6 10 18 18 32 22-8-8-14-18-16-28 12 2 26 8 34 18-4-12-16-22-32-26 10-2 24 0 36 8-6-12-22-18-40-18z"/>`).join('')}
      <path d="M200 200l40-24 40 24M240 200v-24" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>
      <path d="M330 200h70v-6h-70zM320 188h80v-4h-80zM340 178h60v-3h-60z" opacity=".55"/>
    </g>`,
  city: `
    <g opacity=".35"><path d="M0 200v-60h24v-20h20v80zM50 200v-90h26v90zM300 200v-70h20v-24h22v94zM350 200v-50h50v50z"/></g>
    <g>
      <path d="M86 200V96h34v104z"/><path d="M126 200V64l20-14 20 14v136z"/><rect x="172" y="110" width="30" height="90"/>
      <path d="M208 200V80h40v120z"/><path d="M254 200v-88l18-18 18 18v88z"/>
      <rect x="226" y="58" width="4" height="22"/><rect x="144" y="28" width="4" height="22"/>
      ${[100,112].map(y=>`<rect x="92" y="${y}" width="22" height="4" opacity=".5"/>`).join('')}
      ${[90,104,118,132,146,160].map(y=>`<rect x="214" y="${y}" width="28" height="4" opacity=".5"/>`).join('')}
    </g>`,
  india: `
    <g opacity=".35"><path d="M0 200c60-24 140-30 200-24s140 10 200-4v28z"/></g>
    <g>
      <path d="M140 200V96h120v104h-30v-56c0-16-14-28-30-28s-30 12-30 28v56z"/>
      <rect x="132" y="84" width="136" height="12"/><rect x="146" y="72" width="108" height="12"/>
      <rect x="176" y="58" width="48" height="14"/><path d="M186 58c0-8 6-14 14-14s14 6 14 14z"/>
      <rect x="50" y="168" width="60" height="32" opacity=".7"/><rect x="290" y="168" width="60" height="32" opacity=".7"/>
    </g>`,
  world: `
    <g>
      <circle cx="200" cy="200" r="150" fill="none" stroke="#fff" stroke-width="6"/>
      <ellipse cx="200" cy="200" rx="60" ry="150" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/>
      <ellipse cx="200" cy="200" rx="110" ry="150" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>
      <path d="M50 160h300M66 110h268M100 70h200" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>
      <path d="M120 120c20-10 40 0 50 14s30 10 40 0 30-4 34 10-10 26-30 26-34 14-54 10-44-30-40-60z" opacity=".55"/>
      <path d="M250 90c16-8 40-4 52 10s4 24-12 24-30-8-40-18z" opacity=".55"/>
    </g>`,
  tech: `
    <g opacity=".5" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round">
      <path d="M0 160h80l20-20h60M0 120h50l20 20M400 150h-80l-20-20h-50M400 110h-40l-20 20M200 0v40M160 0v30l10 10M240 0v30l-10 10"/>
      <circle cx="80" cy="160" r="5"/><circle cx="320" cy="150" r="5"/><circle cx="50" cy="120" r="4"/><circle cx="360" cy="110" r="4"/>
    </g>
    <g>
      <rect x="150" y="60" width="100" height="100" rx="12"/>
      ${[0,1,2,3].map(i=>`<rect x="${162+i*22}" y="44" width="8" height="16" rx="2"/><rect x="${162+i*22}" y="160" width="8" height="16" rx="2"/><rect x="134" y="${72+i*22}" width="16" height="8" rx="2"/><rect x="250" y="${72+i*22}" width="16" height="8" rx="2"/>`).join('')}
      <path d="M175 140l20-60h10l20 60h-12l-4-14h-18l-4 14zM192 116h12l-6-20z" fill="var(--hl,#16406E)"/>
    </g>
    <g opacity=".35"><path d="M0 200h400v-14H0z"/></g>`,
  sports: `
    <g opacity=".35"><path d="M0 200c60-40 140-56 200-56s140 16 200 56z"/></g>
    <g>
      <path d="M60 200c10-50 70-80 140-80s130 30 140 80h-20c-10-38-60-60-120-60s-110 22-120 60z"/>
      ${[80,120,160,200,240,280,320].map(x=>`<rect x="${x}" y="90" width="4" height="${30+Math.abs(200-x)/6}" opacity=".6"/>`).join('')}
      <circle cx="200" cy="174" r="12"/><path d="M190 168q10 6 20 0M190 180q10-6 20 0" stroke="var(--hl,#1F6B3A)" stroke-width="2" fill="none"/>
      <rect x="150" y="150" width="5" height="50"/><rect x="160" y="150" width="5" height="50"/><rect x="170" y="150" width="5" height="50"/><rect x="148" y="146" width="29" height="4"/>
    </g>`
};
const PLACE_SCENE = {hyderabad:'hyderabad', rangareddy:'city', medchal:'city', sangareddy:'city',
  warangal:'warangal', hanumakonda:'warangal', jangaon:'warangal',
  bhadradri:'temple', yadadri:'temple', sircilla:'temple', jagtial:'temple', mulugu:'forest',
  khammam:'fort', medak:'fort', nizamabad:'fort', suryapet:'village', siddipet:'village', kamareddy:'village',
  peddapalli:'mine', mancherial:'mine', bhupalpally:'mine', karimnagar:'river',
  adilabad:'forest', asifabad:'forest', nirmal:'forest',
  nalgonda:'river', mahabubnagar:'river', gadwal:'river', wanaparthy:'river', nagarkurnool:'river', narayanpet:'village',
  vikarabad:'forest', mahabubabad:'village'};
function sceneFor(s){
  if(s.kind==='job') return 'city';
  if(s.place && PLACE_SCENE[s.place]) return PLACE_SCENE[s.place];
  const sec = Array.isArray(s.sec)?s.sec:(s.sec?[s.sec]:[]);
  const cat = s.cat||'';
  if(sec.includes('world')||/ప్రపంచం/.test(cat)) return 'world';
  if(sec.includes('ai')||sec.includes('innovation')||/టెక్|AI/.test(cat)) return 'tech';
  if(sec.includes('sports')||/క్రీడ|క్రికెట్/.test(cat)) return 'sports';
  if(sec.includes('agri')||s.art==='farm') return 'village';
  if(/హైదరాబాద్/.test(cat)) return 'hyderabad';
  if(/ఏపీ|ఆంధ్ర/.test(cat)) return 'river';
  if(sec.includes('india')||/భారత్|దేశ/.test(cat)) return 'india';
  if(sec.includes('telangana')) return 'village';
  return 'city';
}
function sceneSVG(s, cls){
  const k=sceneFor(s); const body=SCENES[k]||SCENES.city;
  const hole = k==='hyderabad' ? `<mask id="m${cls}"><rect width="400" height="200" fill="#fff"/><g fill="#000">${SCENES.hyderabadHole}</g></mask>` : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" class="${cls||'scene'}" viewBox="0 0 400 200" preserveAspectRatio="xMidYMax meet" fill="#fff" aria-hidden="true">${hole?`<defs>${hole}</defs><g mask="url(#m${cls})">${body}</g>`:body}</svg>`;
}
