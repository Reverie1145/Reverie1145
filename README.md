<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg?v=20261031">
  <img src="assets/hero-light.svg?v=20261031" alt="Reverie1337 — I build small sharp tools: watch apps, bytecode, infrastructure." width="880">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics-dark.svg?v=20261031">
  <img src="assets/metrics-light.svg?v=20261031" alt="Public repos, commits in the last 30 and 90 days" width="880">
</picture>

</div>

### Now

Most of my time goes into **watch-side software**: quick apps that survive a 480×480 screen,
a ~100 MB heap and no browser. When the tooling I need does not exist, I take the bytecode apart
and write the tool — that is where [`veladec`](https://github.com/Reverie1145/veladec) came from.

Right now: QuickJS bytecode analysis for Vela `.rpk` bundles, and the infrastructure that keeps
those side projects building and shipping.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg?v=20261031">
  <img src="assets/activity-light.svg?v=20261031" alt="Public commit activity over the last 90 days" width="880">
</picture>
</div>

### Selected work

**[veladec](https://github.com/Reverie1145/veladec)** — a self-contained decompiler for QuickJS
bytecode as found in Vela / Xiaomi watch `.rpk` quick apps. Single file, zero dependencies,
6 embedded opcode tables, structure recovery, HTML reports. Verified structurally: 2 208 functions
and 129 442 instructions decoded exactly, zero out-of-range references.

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects-dark.svg?v=20261031">
  <img src="assets/projects-light.svg?v=20261031" alt="Recently updated public repositories" width="880">
</picture>
</div>

### Toolbox

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg?v=20261031">
  <img src="assets/stack-light.svg?v=20261031" alt="Python, JavaScript, Java, Kotlin, Linux, Docker" width="880">
</picture>
</div>

<div align="center">
<sub>

These cards are Material&nbsp;3 SVGs rendered from the GitHub API — no third-party badge
services, no tracking pixels, no external requests at view time.
Refresh runs daily at 03:00 Asia/Shanghai; the generator lives in [`scripts/`](scripts) and
[`data.json`](data.json) holds the exact numbers on the cards.

</sub>
</div>
