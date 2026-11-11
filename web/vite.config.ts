import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const files = (d: string): string[] => readdirSync(d).sort().flatMap((f) => { const p = join(d, f); return statSync(p).isDirectory() ? files(p) : [p]; });
const h = createHash('sha256');
for (const f of [...files('src'), ...files('public'), 'index.html', 'sw-template.js', '../data/seed.json']) h.update(f).update(readFileSync(f));
const ID = h.digest('hex').slice(0, 12);

export default defineConfig({
  base: './',
  plugins: [react(), { name: 'build-id', transformIndexHtml: (html: string) => html.replace('<head>', `<head>\n    <meta name="build-id" content="${ID}">`) },
    // 오프라인용 서비스 워커: 빌드할 때마다 캐시 이름에 build-id를 넣어 새 버전이 나오면 옛 캐시를 버린다
    { name: 'sw', apply: 'build', generateBundle(_o: unknown, bundle: Record<string, unknown>) {
      const assets = Object.keys(bundle).filter((f) => !f.endsWith('.map'));
      const src = readFileSync('sw-template.js', 'utf8').replace('__ID__', ID).replace('__ASSETS__', JSON.stringify(['./', './manifest.webmanifest', './favicon.svg', './icon-192.png', ...assets.map((a) => './' + a)]));
      (this as unknown as { emitFile: (f: object) => void }).emitFile({ type: 'asset', fileName: 'sw.js', source: src });
    } }],
  define: { __BUILD_ID__: JSON.stringify(ID) },
  server: { fs: { allow: ['..'] } },
});
