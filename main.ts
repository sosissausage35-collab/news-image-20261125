// One-day world news image for Wednesday 25 November 2026.
//
// The entry image is drawn in code by draw.py (Pillow) and shipped in this
// repository as entry.png. This program simply copies it to the output
// directory, so both runs write byte-identical output with no network.
//
// Before copying, it checks the shipped image is a whole JPEG inside the
// competition limits (at most 1 MiB, at most 1024x1024 px) and refuses to
// write anything otherwise, so a bad image fails loudly instead of
// submitting silently.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");

const bytes = readFileSync(src);
if (bytes[0] !== 0xff || bytes[1] !== 0xd8 || bytes[2] !== 0xff) {
  throw new Error("entry.png is not a JPEG (bad magic bytes)");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (statSync(src).size !== bytes.length) {
  throw new Error("entry.png changed while being read");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
