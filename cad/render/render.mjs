// usage: node render.mjs job.json   (job: {w,h,parts:[{stl,color,...}],views:[{name,dir,up}],out_prefix})
import { chromium } from 'playwright-core';
import fs from 'fs'; import http from 'http'; import path from 'path';
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const root = '/';
const srv = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  const f = p.startsWith('/@/') ? p.slice(2) : path.join(process.cwd(), p);
  fs.readFile(f, (e, b) => { if (e) { res.writeHead(404); res.end(); return; }
    const t = f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/octet-stream';
    res.writeHead(200, {'Content-Type': t}); res.end(b); });
}).listen(0);
const port = srv.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: job.w, height: job.h } });
page.on('console', m => { if (m.type() === 'error') console.error('page:', m.text()); });
await page.goto(`http://127.0.0.1:${port}/page.html`);
await page.waitForFunction(() => window.ready === true);
job.parts.forEach(p => p.stl = '/@' + path.resolve(p.stl));
const imgs = await page.evaluate(j => window.renderJob(j), job);
imgs.forEach((u, i) => fs.writeFileSync(job.views[i].out, Buffer.from(u.split(',')[1], 'base64')));
await browser.close(); srv.close();
console.log('rendered', imgs.length);
