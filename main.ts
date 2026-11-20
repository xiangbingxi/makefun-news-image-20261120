// The World in One Day -- Friday 20 November 2026.
// Node 22, standard library only. The front page is drawn offline by
// tools/gen_image.py and ships in this repository as entry.png; this
// program's only job is to place that exact image at the grader's output
// path, byte for byte, on every run.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`missing bundled image: ${source}`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const bytes = readFileSync(target);
const digest = createHash('sha256').update(bytes).digest('hex');
const size = statSync(target).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate`);
}
console.log(`entry.png: ${size} bytes, sha256 ${digest}`);
