#!/usr/bin/env node
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const W = '/root/.openclaw/workspace/jomoo';
const OUT = '/root/.openclaw/workspace/jomoo/videos';
const W2 = 1080, H2 = 1920, FPS = 30;
const FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';

function getProduct(dir, m) {
  const vi = path.join(dir, 'PRODUCT_VI.md');
  const id = path.join(dir, 'images');
  if (!fs.existsSync(vi)) return null;
  const c = fs.readFileSync(vi, 'utf-8');
  const imgs = fs.readdirSync(id).filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f)).sort().slice(0, 10).map(f => path.join(id, f));
  if (!imgs.length) return null;
  const nm = (c.match(/^#\s*(.+)/m) || [])[1] || m;
  const pr = (c.match(/Giá.*?¥([\d,.]+)/) || [])[1] || '';
  const h = (c.match(/###\s*\d+\.\s*(.+)/g) || []).map(l => l.replace(/###\s*\d+\.\s*/, '').substring(0, 50));
  const f = h.length ? h : (c.match(/- \*\*[^*]+\*\*:.+/g) || []).slice(0, 6).map(l => l.replace(/- \*\*([^*]+)\*\*:.*/, '$1').substring(0, 50));
  return { m, nm, pr, f, imgs };
}

function renderScene(img, dur, title, sub, outFile) {
  const vf = [
    `scale=${W2}:${H2}:force_original_aspect_ratio=decrease`,
    `pad=${W2}:${H2}:(ow-iw)/2:(oh-ih)/2:color=black`,
    `setsar=1,format=yuv420p`,
    `drawbox=x=0:y=ih*0.68:w=iw:h=ih*0.32:color=black@0.65:t=fill`,
    `drawtext=fontfile='${FONT}':text='${title}':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=h*0.72:shadowcolor=black@0.8:shadowx=3:shadowy=3`,
    `drawtext=fontfile='${FONT}':text='${sub}':fontcolor=white@0.9:fontsize=32:x=(w-text_w)/2:y=h*0.79:shadowcolor=black@0.8:shadowx=2:shadowy=2`,
    `drawtext=fontfile='${FONT}':text='JOMOO':fontcolor=white@0.25:fontsize=24:x=w-tw-20:y=30`,
    `fade=t=in:st=0:d=0.5,fade=t=out:st=${dur - 0.5}:d=0.5`
  ].join(',');
  
  execFileSync('ffmpeg', [
    '-y', '-loop', '1', '-t', String(dur), '-i', img,
    '-vf', vf,
    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '26',
    '-pix_fmt', 'yuv420p', '-r', String(FPS),
    outFile
  ], { stdio: 'pipe', timeout: 60000 });
}

function main() {
  const target = process.argv[2];
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
  const pDir = path.join(W, 'products');
  const models = fs.readdirSync(pDir).filter(d => {
    const p = path.join(pDir, d);
    return fs.statSync(p).isDirectory() && d !== 'phu-kien' && fs.existsSync(path.join(p, 'PRODUCT_VI.md'));
  });
  const targets = target ? [target] : models;
  console.log(`\n🎬 JOMOO Video v5 | ${targets.length} sản phẩm\n`);
  let ok = 0, fail = 0;

  for (const m of targets) {
    console.log(`📹 ${m}`);
    const prod = getProduct(path.join(pDir, m), m);
    if (!prod) { console.log(`  ⏭️  skip`); fail++; continue; }
    console.log(`  📝 ${prod.nm.substring(0, 50)}`);

    const oDir = path.join(OUT, m, 'scenes');
    fs.mkdirSync(oDir, { recursive: true });

    const scenes = [
      { i: 0, d: 4, t: `JOMOO ${m}`, s: prod.nm.substring(0, 40) },
      { i: 1, d: 5, t: 'Thiet Ke Sang Trong', s: 'Tinh te - Hien dai - Cao cap' },
      { i: 2, d: 5, t: prod.f[0] || 'Cong Nghe Vuot Troi', s: 'Cong nghe hang dau' },
      { i: 3, d: 5, t: prod.f[1] || 'Tien Ich Thong Minh', s: 'Dieu khien thong minh' },
      { i: 4, d: 5, t: prod.f[2] || 'An Toan Tuyet Doi', s: 'Bao ve suc khoe' },
      { i: 5, d: 4, t: prod.f[3] || 'Tiet Kiem Nang Luong', s: 'Hieu suat nang luong cap 1' },
      { i: 6, d: 4, t: 'Nang Tam Phong Tam', s: prod.pr ? `Gia tham khao ${prod.pr}` : 'Phong cach song dang cap' },
      { i: 7, d: 4, t: `JOMOO ${m}`, s: 'Dat hang ngay hom nay!' },
    ];

    const files = [];
    let sok = true;
    for (let idx = 0; idx < scenes.length; idx++) {
      const sc = scenes[idx];
      const img = prod.imgs[Math.min(sc.i, prod.imgs.length - 1)];
      const f = path.join(oDir, `s${idx}.mp4`);
      process.stdout.write(`  🎞️  ${idx + 1}/${scenes.length} ${sc.t.substring(0, 25)}...`);
      try {
        renderScene(img, sc.d, sc.t, sc.s, f);
        files.push(f);
        console.log(' ✓');
      } catch (e) {
        console.log(` ✗ ${(e.stderr || e.message || '').toString().substring(0, 100)}`);
        sok = false; break;
      }
    }
    if (!sok || !files.length) { fail++; continue; }

    const catF = path.join(oDir, 'cat.txt');
    fs.writeFileSync(catF, files.map(f => `file '${f}'`).join('\n'));
    const finalF = path.join(OUT, m, `${m}_promo.mp4`);
    try {
      execFileSync('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', catF, '-c', 'copy', finalF], { stdio: 'pipe', timeout: 60000 });
      const mb = (fs.statSync(finalF).size / 1024 / 1024).toFixed(1);
      console.log(`  ✅ ${m}_promo.mp4 (${mb} MB)`);
      ok++;
    } catch (e) {
      console.error(`  ❌ concat: ${(e.stderr || e.message).toString().substring(0, 80)}`);
      fail++;
    }
  }
  console.log(`\n✅ ${ok}/${targets.length} thành công | ❌ ${fail} thất bại\n📁 ${OUT}/`);
}
main();
