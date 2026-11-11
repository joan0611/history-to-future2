import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const files = (d: string): string[] => readdirSync(d).sort().flatMap((f) => { const p = join(d, f); return statSync(p).isDirectory() ? files(p) : [p]; });
const h = createHash('sha256');
for (const f of [...files('src'), '../data/seed.json']) h.update(f).update(readFileSync(f));
const ID = h.digest('hex').slice(0, 12);

export default defineConfig({
  base: './',
  plugins: [react(), { name: 'build-id', transformIndexHtml: (html: string) => html.replace('<head>', `<head>\n    <meta name="build-id" content="${ID}">`) }],
  define: { __BUILD_ID__: JSON.stringify(ID) },
  server: { fs: { allow: ['..'] } },
});
