/**
 * Way2Sec newsroom inbox (Google Apps Script, bound to the "Way2Sec Reporters" Google Sheet).
 * Reporters send news from https://way2sec.news/reporter/ ; the editor approves at https://way2sec.news/editor/ ;
 * the Way2Sec publishing task collects approved stories and puts them live.
 *
 * SETUP: Extensions → Apps Script → paste this file → set the two keys below → Run "setup" once → Deploy → New deployment
 *        → type "Web app" → Execute as: Me → Who has access: Anyone → Deploy → copy the Web app URL.
 * Keep EDITOR_KEY and BOT_KEY secret (do not put them on the website).
 */
const EDITOR_KEY = 'PUT-EDITOR-KEY-HERE';   // typed once on the editor page
const BOT_KEY    = 'PUT-BOT-KEY-HERE';      // used only by the Way2Sec publishing task
const FOLDER     = 'Way2Sec reporter photos';
const COLS = ['id','time','pin','reporter','district','place','lat','lng','headline','text','photo','status','note','link'];

function setup() {
  const ss = SpreadsheetApp.getActive();
  let r = ss.getSheetByName('Reporters');
  if (!r) { r = ss.insertSheet('Reporters'); r.appendRow(['pin','name','phone','district','place','active']); r.appendRow(['1001','Sample Reporter','','yadadri','ఆలేరు','yes']); }
  let s = ss.getSheetByName('Submissions');
  if (!s) { s = ss.insertSheet('Submissions'); s.appendRow(COLS); s.setFrozenRows(1); }
  folder_();
}

function folder_() {
  const it = DriveApp.getFoldersByName(FOLDER);
  return it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER);
}
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function sheet_(n) { return SpreadsheetApp.getActive().getSheetByName(n); }
function rows_() {
  const s = sheet_('Submissions'), v = s.getDataRange().getValues(), h = v[0];
  return v.slice(1).map((r, i) => { const o = { _row: i + 2 }; h.forEach((k, j) => o[k] = r[j]); return o; });
}
function reporter_(pin) {
  const v = sheet_('Reporters').getDataRange().getValues();
  for (let i = 1; i < v.length; i++) if (String(v[i][0]).trim() === String(pin).trim() && String(v[i][5]).toLowerCase() !== 'no') return { name: v[i][1], district: v[i][3], place: v[i][4] };
  return null;
}
function clean_(t, n) { return String(t || '').replace(/[<>]/g, '').slice(0, n); }

function doPost(e) {
  let b = {}; try { b = JSON.parse(e.postData.contents); } catch (x) { return out_({ ok: false, error: 'bad request' }); }
  const lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    if (b.action === 'submit') {
      const rep = reporter_(b.pin); if (!rep) return out_({ ok: false, error: 'pin' });
      const text = clean_(b.text, 3000); if (text.length < 30) return out_({ ok: false, error: 'short' });
      const id = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyMMddHHmmss') + '-' + Math.floor(Math.random() * 900 + 100);
      let photo = '';
      if (b.photo && /^data:image\/jpeg;base64,/.test(b.photo) && b.photo.length < 2800000) {
        const blob = Utilities.newBlob(Utilities.base64Decode(b.photo.split(',')[1]), 'image/jpeg', id + '.jpg');
        photo = folder_().createFile(blob).getId();
      }
      sheet_('Submissions').appendRow([id, Utilities.formatDate(new Date(), 'Asia/Kolkata', 'dd.MM.yyyy HH:mm'), String(b.pin), rep.name,
        clean_(b.district, 40) || rep.district, clean_(b.place, 80) || rep.place, Number(b.lat) || '', Number(b.lng) || '',
        clean_(b.headline, 160), text, photo, 'pending', '', '']);
      return out_({ ok: true, id: id, name: rep.name });
    }
    if (b.action === 'list' && b.key === EDITOR_KEY) {
      return out_({ ok: true, items: rows_().slice(-60).reverse() });  // newest first; photos load one by one with "photo"
    }
    if (b.action === 'photo' && b.key === EDITOR_KEY) {
      const r = rows_().find(x => x.id === b.id); if (!r || !r.photo) return out_({ ok: false });
      return out_({ ok: true, data: 'data:image/jpeg;base64,' + Utilities.base64Encode(DriveApp.getFileById(r.photo).getBlob().getBytes()) });
    }
    if (b.action === 'decide' && b.key === EDITOR_KEY) {
      const r = rows_().find(x => x.id === b.id); if (!r) return out_({ ok: false, error: 'missing' });
      const st = b.decision === 'approve' ? 'approved' : 'rejected';
      const s = sheet_('Submissions'); s.getRange(r._row, COLS.indexOf('status') + 1).setValue(st); s.getRange(r._row, COLS.indexOf('note') + 1).setValue(clean_(b.note, 300));
      return out_({ ok: true, status: st });
    }
    if (b.action === 'approved' && b.key === BOT_KEY) {
      const items = rows_().filter(r => r.status === 'approved').map(r => Object.assign({}, r,
        { photo_data: r.photo ? Utilities.base64Encode(DriveApp.getFileById(r.photo).getBlob().getBytes()) : '' }));
      return out_({ ok: true, items: items });
    }
    if (b.action === 'published' && b.key === BOT_KEY) {
      const r = rows_().find(x => x.id === b.id); if (!r) return out_({ ok: false });
      const s = sheet_('Submissions'); s.getRange(r._row, COLS.indexOf('status') + 1).setValue('published'); s.getRange(r._row, COLS.indexOf('link') + 1).setValue(clean_(b.link, 200));
      return out_({ ok: true });
    }
    return out_({ ok: false, error: 'not allowed' });
  } finally { lock.releaseLock(); }
}

function doGet() { return out_({ ok: true, service: 'Way2Sec newsroom' }); }
