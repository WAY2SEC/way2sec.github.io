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
/* more drawings: coast, palaces, monuments, rivers, hills */
Object.assign(SCENES, {
  beach: `
    <circle cx="300" cy="110" r="34" opacity=".55"/>
    <g opacity=".35"><path d="M0 150h400v50H0z"/></g>
    <g>
      <path d="M0 160q25-8 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v8q-25-8-50 0t-50 0-50 0-50 0-50 0-50 0-50 0-50 0z"/>
      <path d="M0 182q25-8 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v18H0z"/>
      <path d="M70 160c-2-30 2-62 10-84" stroke="#fff" stroke-width="6" fill="none"/>
      <path d="M80 76c-22-2-38 8-44 20 14-8 30-10 44-8-20 6-32 16-36 28 14-12 28-18 38-18-2 12-10 22-18 30 14-8 22-18 24-30 6 12 18 20 34 24-8-10-16-20-18-30 14 2 30 10 38 20-4-14-18-24-36-28 12-2 26 2 38 10-8-14-26-20-44-18z"/>
      <path d="M330 160v-70h14v70z"/><path d="M326 90h22l-4-10h-14z"/><path d="M332 80h10v-8h-10z"/>
      <path d="M200 150l30-10 6 10z" opacity=".7"/>
    </g>`,
  palace: `
    <g opacity=".35"><path d="M0 200v-30h400v30z"/></g>
    <g>
      <rect x="60" y="130" width="280" height="70"/>
      ${[80,120,160,224,264,304].map(x=>`<path d="M${x} 200v-30c0-8 6-14 13-14s13 6 13 14v30z" fill="var(--hl,#000)" opacity=".35"/>`).join('')}
      <rect x="170" y="92" width="60" height="38"/>
      <path d="M176 92c0-22 11-36 24-36s24 14 24 36z"/><rect x="198" y="40" width="4" height="16"/>
      ${[60,326].map(x=>`<rect x="${x}" y="104" width="14" height="26"/><path d="M${x-2} 104c0-10 4-16 9-16s9 6 9 16z"/>`).join('')}
      ${[130,256].map(x=>`<rect x="${x}" y="110" width="14" height="20"/><path d="M${x-2} 110c0-8 4-13 9-13s9 5 9 13z"/>`).join('')}
    </g>`,
  gateway: `
    <g opacity=".35"><path d="M0 178q25-8 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v22H0z"/></g>
    <g>
      <path d="M130 186V96h140v90h-40v-44c0-17-13-30-30-30s-30 13-30 30v44z"/>
      <rect x="124" y="86" width="152" height="10"/>
      ${[130,170,214,254].map(x=>`<rect x="${x}" y="58" width="16" height="28"/><path d="M${x-2} 58c0-10 5-16 10-16s10 6 10 16z"/>`).join('')}
      <path d="M180 78h40v8h-40z"/>
    </g>`,
  redfort: `
    <g opacity=".35"><path d="M0 200v-20h400v20z"/></g>
    <g>
      <path d="M20 200v-60${[...Array(18)].map((_,i)=>`h10v-8h10v8`).join('')}h0v60z"/>
      <path d="M150 200v-90h100v90h-26v-36c0-14-10-24-24-24s-24 10-24 24v36z"/>
      <rect x="144" y="100" width="112" height="10"/>
      ${[150,226].map(x=>`<rect x="${x}" y="78" width="24" height="22"/><path d="M${x-4} 78c0-12 8-20 16-20s16 8 16 20z"/>`).join('')}
      <path d="M186 100c0-14 6-24 14-24s14 10 14 24z"/>
      ${[30,350].map(x=>`<rect x="${x}" y="110" width="20" height="30"/><path d="M${x-3} 110c0-10 6-16 13-16s13 6 13 16z"/>`).join('')}
    </g>`,
  bridge: `
    <g opacity=".35"><path d="M0 176q25-8 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v24H0z"/></g>
    <g>
      <rect x="0" y="150" width="400" height="10"/>
      ${[110,290].map(x=>`<path d="M${x-14} 160V40h28v120z"/><rect x="${x-20}" y="36" width="40" height="8"/>`).join('')}
      <path d="M0 150L96 60M124 60L200 120L276 60M304 60L400 150" stroke="#fff" stroke-width="7" fill="none"/>
      <path d="M40 150L96 100M150 150L124 100M250 150L276 100M360 150L304 100M200 120v30" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>
    </g>`,
  taj: `
    <g opacity=".35"><path d="M0 200v-18h400v18z"/></g>
    <g>
      <rect x="120" y="170" width="160" height="12"/>
      <rect x="150" y="110" width="100" height="60"/>
      <path d="M200 112h-40c0-30 18-50 40-62 22 12 40 32 40 62z"/><rect x="198" y="34" width="4" height="18"/>
      <path d="M186 170v-30c0-8 6-14 14-14s14 6 14 14v30z" fill="var(--hl,#000)" opacity=".35"/>
      ${[160,226].map(x=>`<rect x="${x}" y="98" width="14" height="12"/><path d="M${x-2} 98c0-8 4-13 9-13s9 5 9 13z"/>`).join('')}
      ${[110,282].map(x=>`<rect x="${x}" y="66" width="8" height="104"/><path d="M${x-2} 66c0-8 3-12 6-12s6 4 6 12z"/><rect x="${x-2}" y="96" width="12" height="3"/><rect x="${x-2}" y="130" width="12" height="3"/>`).join('')}
    </g>`,
  boat: `
    <g opacity=".35"><path d="M0 150h400v50H0z"/></g>
    <g>
      <path d="M0 170q25-8 50 0t50 0 50 0 50 0 50 0 50 0 50 0 50 0v30H0z" opacity=".6"/>
      <path d="M120 160h170c-10 14-30 20-50 20h-80c-20 0-34-8-40-20z"/>
      <path d="M150 160c0-24 20-40 52-40s52 16 52 40z"/>
      <path d="M296 150c-2-30 2-60 10-80" stroke="#fff" stroke-width="5" fill="none"/>
      <path d="M306 70c-20-2-34 8-40 18 12-6 26-8 40-6-18 6-28 14-32 24 12-10 24-14 34-14-2 10-8 20-16 26 12-6 20-16 22-26 6 10 16 18 30 22-6-8-14-18-16-26 12 2 26 8 34 18-4-12-16-22-32-26 10-2 22 2 34 8-8-12-24-18-40-16z"/>
      <path d="M40 150c-2-24 0-46 6-64" stroke="#fff" stroke-width="4" fill="none" opacity=".8"/>
    </g>`,
  hills: `
    <g opacity=".35"><path d="M0 200L70 90l50 60 60-100 70 90 50-50 100 110z"/></g>
    <g>
      <path d="M0 200l60-70 40 40 70-90 60 80 50-40 120 80z"/>
      <path d="M170 80l-14 18 14-6 14 8z" fill="var(--hl,#000)" opacity=".4"/>
      ${[40,320,360].map(x=>`<path d="M${x} 150l14 24h-8l12 20h-36l12-20h-8z"/>`).join('')}
    </g>`,
  dam: `
    <g opacity=".35"><path d="M0 110h400v20H0z"/></g>
    <g>
      <path d="M0 120h400l-30 80H30z"/>
      ${[...Array(9)].map((_,i)=>`<rect x="${52+i*34}" y="132" width="18" height="40" rx="2" fill="var(--hl,#000)" opacity=".35"/>`).join('')}
      <rect x="0" y="112" width="400" height="8"/>
      <path d="M40 200q20-10 40 0t40 0 40 0 40 0 40 0 40 0 40 0 40 0" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>
    </g>`
});

/* Places: India → state → district (Telangana + Andhra Pradesh now; other states state-level) → town/village (story "loc") */
const STATES = [
  ['TG','తెలంగాణ','Telangana'],['AP','ఆంధ్రప్రదేశ్','Andhra Pradesh'],['KA','కర్ణాటక','Karnataka'],['TN','తమిళనాడు','Tamil Nadu'],
  ['MH','మహారాష్ట్ర','Maharashtra'],['KL','కేరళ','Kerala'],['DL','ఢిల్లీ','Delhi'],['OD','ఒడిశా','Odisha'],['CG','ఛత్తీస్‌గఢ్','Chhattisgarh'],
  ['GJ','గుజరాత్','Gujarat'],['RJ','రాజస్థాన్','Rajasthan'],['UP','ఉత్తరప్రదేశ్','Uttar Pradesh'],['MP','మధ్యప్రదేశ్','Madhya Pradesh'],
  ['WB','పశ్చిమ బెంగాల్','West Bengal'],['BR','బిహార్','Bihar'],['JH','జార్ఖండ్','Jharkhand'],['PB','పంజాబ్','Punjab'],['HR','హరియాణా','Haryana'],
  ['HP','హిమాచల్ ప్రదేశ్','Himachal Pradesh'],['UK','ఉత్తరాఖండ్','Uttarakhand'],['JK','జమ్మూ కశ్మీర్','Jammu & Kashmir'],['LA','లద్దాఖ్','Ladakh'],
  ['GA','గోవా','Goa'],['AS','అస్సాం','Assam'],['NE','ఈశాన్య రాష్ట్రాలు','North-East states'],['PY','పుదుచ్చేరి','Puducherry'],['AN','అండమాన్ నికోబార్','Andaman & Nicobar']
];
const AP_DISTRICTS = [
  ['ap-srikakulam','శ్రీకాకుళం','Srikakulam'],['ap-manyam','పార్వతీపురం మన్యం','Parvathipuram Manyam'],['ap-vizianagaram','విజయనగరం','Vizianagaram'],
  ['ap-visakhapatnam','విశాఖపట్నం','Visakhapatnam'],['ap-asr','అల్లూరి సీతారామరాజు','Alluri Sitharama Raju'],['ap-anakapalli','అనకాపల్లి','Anakapalli'],
  ['ap-kakinada','కాకినాడ','Kakinada'],['ap-eastgodavari','తూర్పు గోదావరి','East Godavari'],['ap-konaseema','కోనసీమ','Konaseema'],['ap-eluru','ఏలూరు','Eluru'],
  ['ap-westgodavari','పశ్చిమ గోదావరి','West Godavari'],['ap-ntr','ఎన్టీఆర్ (విజయవాడ)','NTR (Vijayawada)'],['ap-krishna','కృష్ణా','Krishna'],['ap-palnadu','పల్నాడు','Palnadu'],
  ['ap-guntur','గుంటూరు','Guntur'],['ap-bapatla','బాపట్ల','Bapatla'],['ap-prakasam','ప్రకాశం','Prakasam'],['ap-nellore','నెల్లూరు','SPS Nellore'],
  ['ap-kurnool','కర్నూలు','Kurnool'],['ap-nandyal','నంద్యాల','Nandyal'],['ap-anantapur','అనంతపురం','Anantapur'],['ap-sathyasai','శ్రీ సత్యసాయి','Sri Sathya Sai'],
  ['ap-kadapa','వైఎస్ఆర్ కడప','YSR Kadapa'],['ap-annamayya','అన్నమయ్య','Annamayya'],['ap-tirupati','తిరుపతి','Tirupati'],['ap-chittoor','చిత్తూరు','Chittoor']
];
const PLACE_SCENE = {hyderabad:'hyderabad', rangareddy:'city', medchal:'city', sangareddy:'city',
  warangal:'warangal', hanumakonda:'warangal', jangaon:'warangal',
  bhadradri:'temple', yadadri:'temple', sircilla:'temple', jagtial:'temple', mulugu:'temple',
  khammam:'fort', medak:'fort', nizamabad:'fort', suryapet:'village', siddipet:'village', kamareddy:'village',
  peddapalli:'mine', mancherial:'mine', bhupalpally:'mine', karimnagar:'river',
  adilabad:'forest', asifabad:'forest', nirmal:'forest', nalgonda:'dam',
  mahabubnagar:'river', gadwal:'river', wanaparthy:'river', nagarkurnool:'river', narayanpet:'village', vikarabad:'forest', mahabubabad:'village',
  'ap-srikakulam':'beach','ap-manyam':'hills','ap-vizianagaram':'fort','ap-visakhapatnam':'beach','ap-asr':'hills','ap-anakapalli':'village',
  'ap-kakinada':'beach','ap-eastgodavari':'boat','ap-konaseema':'boat','ap-eluru':'boat','ap-westgodavari':'boat','ap-ntr':'dam','ap-krishna':'river',
  'ap-palnadu':'dam','ap-guntur':'city','ap-bapatla':'beach','ap-prakasam':'beach','ap-nellore':'beach','ap-kurnool':'fort','ap-nandyal':'temple',
  'ap-anantapur':'fort','ap-sathyasai':'temple','ap-kadapa':'fort','ap-annamayya':'hills','ap-tirupati':'temple','ap-chittoor':'temple', AP:'river'};
const STATE_SCENE = {TG:'village',AP:'river',KA:'palace',TN:'temple',MH:'gateway',KL:'boat',DL:'redfort',OD:'temple',CG:'forest',GJ:'city',RJ:'fort',
  UP:'taj',MP:'forest',WB:'bridge',BR:'village',JH:'forest',PB:'village',HR:'city',HP:'hills',UK:'hills',JK:'hills',LA:'hills',GA:'beach',AS:'hills',NE:'hills',PY:'beach',AN:'beach'};

/* district lists for other states (key = state code + "-" + short English name) */
const STATE_DISTRICTS = {
 KA: [['ka-bagalkot','బాగల్‌కోట్','Bagalkot'],['ka-ballari','బళ్లారి','Ballari'],['ka-belagavi','బెళగావి','Belagavi'],['ka-bengalururural','బెంగళూరు గ్రామీణ','Bengaluru Rural'],
  ['ka-bengaluru','బెంగళూరు అర్బన్','Bengaluru Urban'],['ka-bengalurusouth','బెంగళూరు సౌత్ (రామనగర)','Bengaluru South (Ramanagara)'],['ka-bidar','బీదర్','Bidar'],['ka-chamarajanagar','చామరాజనగర్','Chamarajanagar'],
  ['ka-chikkaballapur','చిక్కబళ్లాపూర్','Chikkaballapur'],['ka-chikkamagaluru','చిక్కమగళూరు','Chikkamagaluru'],['ka-chitradurga','చిత్రదుర్గ','Chitradurga'],['ka-dakshinakannada','దక్షిణ కన్నడ (మంగళూరు)','Dakshina Kannada'],
  ['ka-davanagere','దావణగెరె','Davanagere'],['ka-dharwad','ధార్వాడ్ (హుబ్లీ)','Dharwad'],['ka-gadag','గదగ్','Gadag'],['ka-hassan','హాసన్','Hassan'],['ka-haveri','హావేరి','Haveri'],
  ['ka-kalaburagi','కలబురగి','Kalaburagi'],['ka-kodagu','కొడగు','Kodagu'],['ka-kolar','కోలార్','Kolar'],['ka-koppal','కొప్పళ','Koppal'],['ka-mandya','మండ్య','Mandya'],['ka-mysuru','మైసూరు','Mysuru'],
  ['ka-raichur','రాయచూరు','Raichur'],['ka-shivamogga','శివమొగ్గ','Shivamogga'],['ka-tumakuru','తుమకూరు','Tumakuru'],['ka-udupi','ఉడుపి','Udupi'],['ka-uttarakannada','ఉత్తర కన్నడ','Uttara Kannada'],
  ['ka-vijayapura','విజయపుర','Vijayapura'],['ka-vijayanagara','విజయనగర (హంపి)','Vijayanagara'],['ka-yadgir','యాదగిరి','Yadgir']],
 TN: [['tn-ariyalur','అరియలూరు','Ariyalur'],['tn-chengalpattu','చెంగల్పట్టు','Chengalpattu'],['tn-chennai','చెన్నై','Chennai'],['tn-coimbatore','కోయంబత్తూరు','Coimbatore'],['tn-cuddalore','కడలూరు','Cuddalore'],
  ['tn-dharmapuri','ధర్మపురి','Dharmapuri'],['tn-dindigul','దిండిగల్','Dindigul'],['tn-erode','ఈరోడ్','Erode'],['tn-kallakurichi','కళ్లకురిచ్చి','Kallakurichi'],['tn-kanchipuram','కాంచీపురం','Kanchipuram'],
  ['tn-kanyakumari','కన్యాకుమారి','Kanyakumari'],['tn-karur','కరూర్','Karur'],['tn-krishnagiri','కృష్ణగిరి','Krishnagiri'],['tn-madurai','మదురై','Madurai'],['tn-mayiladuthurai','మయిలాడుతురై','Mayiladuthurai'],
  ['tn-nagapattinam','నాగపట్నం','Nagapattinam'],['tn-namakkal','నామక్కల్','Namakkal'],['tn-nilgiris','నీలగిరి (ఊటీ)','Nilgiris'],['tn-perambalur','పెరంబలూరు','Perambalur'],['tn-pudukkottai','పుదుక్కోట్టై','Pudukkottai'],
  ['tn-ramanathapuram','రామనాథపురం','Ramanathapuram'],['tn-ranipet','రాణిపేట్','Ranipet'],['tn-salem','సేలం','Salem'],['tn-sivaganga','శివగంగ','Sivaganga'],['tn-tenkasi','తెన్‌కాశి','Tenkasi'],
  ['tn-thanjavur','తంజావూరు','Thanjavur'],['tn-theni','తేని','Theni'],['tn-thoothukudi','తూత్తుకుడి','Thoothukudi'],['tn-tiruchirappalli','తిరుచిరాపల్లి','Tiruchirappalli'],['tn-tirunelveli','తిరునెల్వేలి','Tirunelveli'],
  ['tn-tirupathur','తిరుపత్తూరు','Tirupathur'],['tn-tiruppur','తిరుప్పూర్','Tiruppur'],['tn-tiruvallur','తిరువళ్లూరు','Tiruvallur'],['tn-tiruvannamalai','తిరువణ్ణామలై','Tiruvannamalai'],
  ['tn-tiruvarur','తిరువారూర్','Tiruvarur'],['tn-vellore','వేలూరు','Vellore'],['tn-viluppuram','విల్లుపురం','Viluppuram'],['tn-virudhunagar','విరుదునగర్','Virudhunagar']],
 MH: [['mh-ahilyanagar','అహిల్యానగర్ (అహ్మద్‌నగర్)','Ahilyanagar (Ahmednagar)'],['mh-akola','అకోలా','Akola'],['mh-amravati','అమరావతి (మహారాష్ట్ర)','Amravati'],['mh-sambhajinagar','ఛత్రపతి శంభాజీనగర్ (ఔరంగాబాద్)','Chhatrapati Sambhajinagar'],
  ['mh-beed','బీడ్','Beed'],['mh-bhandara','భండారా','Bhandara'],['mh-buldhana','బుల్ధానా','Buldhana'],['mh-chandrapur','చంద్రపూర్','Chandrapur'],['mh-dharashiv','ధారాశివ్ (ఉస్మానాబాద్)','Dharashiv (Osmanabad)'],
  ['mh-dhule','ధులే','Dhule'],['mh-gadchiroli','గడ్చిరోలి','Gadchiroli'],['mh-gondia','గోండియా','Gondia'],['mh-hingoli','హింగోలి','Hingoli'],['mh-jalgaon','జల్గావ్','Jalgaon'],['mh-jalna','జాల్నా','Jalna'],
  ['mh-kolhapur','కొల్హాపూర్','Kolhapur'],['mh-latur','లాతూర్','Latur'],['mh-mumbai','ముంబై సిటీ','Mumbai City'],['mh-mumbaisuburban','ముంబై సబర్బన్','Mumbai Suburban'],['mh-nagpur','నాగ్‌పూర్','Nagpur'],
  ['mh-nanded','నాందేడ్','Nanded'],['mh-nandurbar','నందుర్బార్','Nandurbar'],['mh-nashik','నాశిక్','Nashik'],['mh-palghar','పాల్ఘర్','Palghar'],['mh-parbhani','పర్భణి','Parbhani'],['mh-pune','పుణె','Pune'],
  ['mh-raigad','రాయగఢ్','Raigad'],['mh-ratnagiri','రత్నగిరి','Ratnagiri'],['mh-sangli','సాంగ్లీ','Sangli'],['mh-satara','సతారా','Satara'],['mh-sindhudurg','సింధుదుర్గ్','Sindhudurg'],['mh-solapur','షోలాపూర్','Solapur'],
  ['mh-thane','ఠాణె','Thane'],['mh-wardha','వార్ధా','Wardha'],['mh-washim','వాశిమ్','Washim'],['mh-yavatmal','యవత్మాల్','Yavatmal']]
};
/* other names the news may use for the same district */
const PLACE_ALIAS = {'mh-ahmednagar':'mh-ahilyanagar','mh-aurangabad':'mh-sambhajinagar','mh-chhatrapatisambhajinagar':'mh-sambhajinagar','mh-osmanabad':'mh-dharashiv',
  'mh-mumbaicity':'mh-mumbai','ka-ramanagara':'ka-bengalurusouth','ka-bengaluruurban':'ka-bengaluru','ka-bangalore':'ka-bengaluru','ka-mysore':'ka-mysuru','ka-mangaluru':'ka-dakshinakannada',
  'ka-hubballi':'ka-dharwad','tn-trichy':'tn-tiruchirappalli','tn-ooty':'tn-nilgiris','tn-thenilgiris':'tn-nilgiris','tn-tuticorin':'tn-thoothukudi','ka-gulbarga':'ka-kalaburagi','ka-belgaum':'ka-belagavi'};
const normPlace = k => PLACE_ALIAS[k] || k;
Object.assign(PLACE_SCENE, {'ka-bengaluru':'city','ka-bengalururural':'city','ka-bengalurusouth':'city','ka-mysuru':'palace','ka-kodagu':'hills','ka-chikkamagaluru':'hills','ka-udupi':'beach',
  'ka-dakshinakannada':'beach','ka-uttarakannada':'beach','ka-vijayanagara':'fort','ka-vijayapura':'fort','ka-bidar':'fort','ka-chitradurga':'fort','ka-mandya':'dam',
  'tn-chennai':'beach','tn-kanyakumari':'beach','tn-thoothukudi':'beach','tn-nagapattinam':'beach','tn-ramanathapuram':'beach','tn-cuddalore':'beach','tn-madurai':'temple','tn-thanjavur':'temple',
  'tn-kanchipuram':'temple','tn-tiruvannamalai':'temple','tn-nilgiris':'hills','tn-theni':'hills','tn-coimbatore':'city','tn-tiruppur':'city','tn-salem':'city',
  'mh-mumbai':'gateway','mh-mumbaisuburban':'city','mh-thane':'city','mh-pune':'city','mh-nagpur':'city','mh-ratnagiri':'beach','mh-sindhudurg':'beach','mh-raigad':'fort','mh-satara':'hills',
  'mh-gadchiroli':'forest','mh-chandrapur':'forest','mh-kolhapur':'temple','mh-nashik':'temple','mh-sambhajinagar':'fort'});
function stateOf(s){ if(s.st && s.st!=='IN' && s.st!=='WORLD') return s.st; const p=s.place||''; if(p.startsWith('ap-')||p==='AP') return 'AP'; const m=/^(ka|tn|mh)-/.exec(p); if(m) return m[1].toUpperCase(); if(s.st) return ''; if(p&&p!=='TS'&&p!=='IN') return 'TG'; return ''; }
function sceneFor(s){
  if(s.kind==='job') return 'city';
  const pk=normPlace(s.place||''); if(pk && PLACE_SCENE[pk]) return PLACE_SCENE[pk];
  const sec = Array.isArray(s.sec)?s.sec:(s.sec?[s.sec]:[]);
  const cat = s.cat||'';
  const st = stateOf(s);
  if(st && st!=='TG' && STATE_SCENE[st]) return STATE_SCENE[st];
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
/* name of a place key for chips: Telangana/AP district or "st-XX" state */
function placeLabel(key){
  if(!key) return '';
  if(key.startsWith('st-')){ const s=STATES.find(x=>x[0]===key.slice(3)); return s?s[1]:''; }
  key=normPlace(key); const a=AP_DISTRICTS.find(x=>x[0]===key); if(a) return a[1];
  for(const st in STATE_DISTRICTS){ const d=STATE_DISTRICTS[st].find(x=>x[0]===key); if(d) return d[1]; }
  return '';
}
function sceneSVG(s, cls){
  const k=sceneFor(s); const body=SCENES[k]||SCENES.city;
  const hole = k==='hyderabad' ? `<mask id="m${cls}"><rect width="400" height="200" fill="#fff"/><g fill="#000">${SCENES.hyderabadHole}</g></mask>` : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" class="${cls||'scene'}" viewBox="0 0 400 200" preserveAspectRatio="xMidYMax meet" fill="#fff" aria-hidden="true">${hole?`<defs>${hole}</defs><g mask="url(#m${cls})">${body}</g>`:body}</svg>`;
}
