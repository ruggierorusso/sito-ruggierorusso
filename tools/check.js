const { chromium, devices } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = process.argv[2], OUT = process.argv[3];
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff': 'font/woff', '.ttf': 'font/ttf' };
const srv = http.createServer((q, r) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end('nf'); }
  r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
}).listen(8765);
(async () => {
  const b = await chromium.launch();
  const bad = [];
  // crawl all html for broken links
  const pages = [];
  (function walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) walk(p); else if (p.endsWith('.html')) pages.push(p); } })(ROOT);
  for (const p of pages) {
    const html = fs.readFileSync(p, 'utf8');
    for (const m of html.matchAll(/(?:href|src)="([^"#:?]+)(?:#[^"]*)?"/g)) {
      const u = m[1]; if (u.startsWith('/')) { if (!fs.existsSync(path.join(ROOT, u))) bad.push(p + ' -> ' + u); continue; }
      const t = path.resolve(path.dirname(p), u); if (!fs.existsSync(t)) bad.push(path.relative(ROOT, p) + ' -> ' + u);
    }
  }
  console.log('pagine', pages.length, 'link rotti', bad.length, bad.slice(0, 10));
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const pg = await ctx.newPage(); const errs = [];
  pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8765/index.html', { waitUntil: 'networkidle' });
  await pg.screenshot({ path: OUT + '/d-home.png', fullPage: true });
  await pg.click('.chips button[data-f="STILL-LIFE"]');
  console.log('still-life visibili', await pg.$$eval('.list li:not([hidden])', l => l.length), await pg.textContent('.count'));
  await pg.goto('http://localhost:8765/lavori/dalila.html', { waitUntil: 'networkidle' });
  await pg.screenshot({ path: OUT + '/d-proj.png', fullPage: true });
  await pg.click('.gallery a >> nth=2'); await pg.waitForTimeout(400);
  console.log('lightbox', await pg.isVisible('.lb'), await pg.textContent('.lb-c'));
  await pg.keyboard.press('ArrowRight'); console.log('dopo freccia', await pg.textContent('.lb-c'));
  await pg.screenshot({ path: OUT + '/d-lb.png' });
  await pg.keyboard.press('Escape');
  const fontOk = await pg.evaluate(() => document.fonts.check('16px "RR Stencil"'));
  console.log('font', fontOk);
  const m = await b.newContext({ ...devices['iPhone 13'] }); const mp = await m.newPage();
  await mp.goto('http://localhost:8765/en/index.html', { waitUntil: 'networkidle' });
  const ov = await mp.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  console.log('overflow mobile', ov);
  await mp.screenshot({ path: OUT + '/m-home.png', fullPage: true });
  await mp.goto('http://localhost:8765/en/works/scisci.html', { waitUntil: 'networkidle' });
  console.log('overflow mobile proj', await mp.evaluate(() => document.documentElement.scrollWidth - innerWidth));
  await mp.screenshot({ path: OUT + '/m-proj.png', fullPage: true });
  console.log('errori console', errs);
  await b.close(); srv.close();
})();
