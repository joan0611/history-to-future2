// 지금 코드·데이터의 빌드 지문. 배포된 사이트의 <meta name="build-id">와 같으면 같은 코드다.
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
const files = (d) => readdirSync(d).sort().flatMap((f) => { const p = join(d, f); return statSync(p).isDirectory() ? files(p) : [p]; });
const h = createHash('sha256');
for (const f of [...files('src'), '../data/seed.json']) h.update(f).update(readFileSync(f));
console.log(h.digest('hex').slice(0, 12));
