#!/usr/bin/env python3
"""Render the profile cards as Material 3 SVGs (light + dark).

usage: python3 render.py [--data data.json] [--out assets]
"""
import argparse, json, os, re, sys
from tokens import LIGHT, DARK, SANS, MONO, TYPE, RADIUS, GUTTER, PAD

W = 880


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _is_wide(c):
    """CJK / fullwidth only — em dashes and typographic punctuation are narrow."""
    o = ord(c)
    return (0x2E80 <= o <= 0x9FFF) or (0xAC00 <= o <= 0xD7AF) or (0x3040 <= o <= 0x30FF) \
        or (0xFF00 <= o <= 0xFF60) or (0x3000 <= o <= 0x303F)


_NARROW = set("iljtfrI.,:;'!|()[]{} ")
_MEDIUM = set("abcdeghknopqsuvxyz0123456789-$_/=+<>?")
_WIDE = set("ABCDEFGHKNOPQRSUVXYZ&@%#*")


def _char_em(c, weight):
    o = ord(c)
    if (0x2E80 <= o <= 0x9FFF) or (0xAC00 <= o <= 0xD7AF) or (0x3040 <= o <= 0x30FF) \
            or (0xFF00 <= o <= 0xFF60) or (0x3000 <= o <= 0x303F):
        return 1.0
    bump = 0.03 if weight >= 500 else 0.0
    if c in _NARROW:
        return 0.30 + bump
    if c in _WIDE:
        return 0.70 + bump
    if c in _MEDIUM:
        return 0.56 + bump
    return 0.62 + bump


def tw(text, size, weight=400, ls=0.0):
    """Advance width estimate: per-character classes, tighter than a flat average."""
    if not text:
        return 0.0
    return sum(_char_em(c, weight) for c in text) * size + ls * (len(text) - 1)


def fit(text, maxw, size, weight=400, ls=0.0):
    """Truncate with an ellipsis so text never runs into a trailing chip."""
    if tw(text, size, weight, ls) <= maxw:
        return text
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if tw(text[:mid] + "…", size, weight, ls) <= maxw:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo].rstrip(" ,;—-") + "…"


def t(x, y, s, size, weight=400, fill="#000", ls=0.0, font=SANS, anchor="start", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def tt(style, s, x, y, fill, **kw):
    size, lh, weight, ls = TYPE[style]
    return t(x, y, s, size, weight, fill, ls, **kw)


def svg(body, w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">\n'
            f'<defs>\n'
            f'  <filter id="e1" x="-6%" y="-12%" width="112%" height="130%">'
            f'<feDropShadow dx="0" dy="1" stdDeviation="1.8" flood-color="#000000" flood-opacity="0.14"/></filter>\n'
            f'  <filter id="e2" x="-6%" y="-12%" width="112%" height="130%">'
            f'<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.18"/></filter>\n'
            f'</defs>\n{body}\n</svg>\n')


def card(x, y, w, h, r, fill, stroke, elev=1, extra=""):
    f = ' filter="url(#e1)"' if elev == 1 else (' filter="url(#e2)"' if elev == 2 else "")
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1"{f}{extra}/>')


def chip_row(x, y, labels, th, dk, gap=8, h=32, r=8):
    out, cx = [], x
    for lab in labels:
        w = tw(lab, 13, 500, 0.1) + 26
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{r}" fill="none" '
                   f'stroke="{th["outline_variant"]}" stroke-width="1"/>')
        out.append(t(cx + 13, y + h / 2 + 4.6, lab, 13, 500, th["on_surface_variant"], 0.1))
        cx += w + gap
    return out, cx


# ---------------------------------------------------------------- components
def hero(d, th, dk):
    h = 240
    o = [card(0.5, 0.5, W - 1, h - 1, RADIUS["full"], th["surface_container_low"], th["outline_variant"], 1)]
    o.append(t(PAD + 16, 54, "PROFILE / 01", 11, 500, th["primary"], 1.6, MONO))
    o.append(t(PAD + 16, 110, d["name"], 40, 500, th["on_surface"], -0.5))
    o.append(t(PAD + 16, 144, d["tagline"], 16, 400, th["on_surface_variant"], 0.15))
    chips, _ = chip_row(PAD + 16, 172, d.get("chips", []), th, dk)
    o += chips
    # state pill
    lab, detail = d.get("state", "ACTIVE"), d.get("state_detail", "")
    pw = max(112.0, tw(lab, 12, 500, 1.0) * 1.08 + 52)   # 8% slack: fallback fonts run wider than Roboto
    px = W - PAD - 16 - pw
    o.append(f'<rect x="{px:.1f}" y="38" width="{pw:.1f}" height="30" rx="15" fill="{th["primary_container"]}"/>')
    o.append(f'<circle cx="{px + 19:.1f}" cy="53" r="4" fill="{th["primary"]}">'
             f'<animate attributeName="opacity" values="1;0.3;1" dur="2.6s" repeatCount="indefinite"/></circle>')
    o.append(t(px + 31, 57.5, lab, 12, 500, th["on_primary_container"], 1.0))
    if detail:
        o.append(t(W - PAD - 16, 90, detail, 11, 400, th["outline"], 0.4, MONO, anchor="end"))
    return svg("\n".join(o), W, h, f'{d["name"]} — {d["tagline"]}')


def metrics(d, th, dk):
    h, gap = 116, GUTTER
    items = d.get("metrics", [])[:3]
    w = (W - gap * (len(items) - 1)) / max(1, len(items))
    o = []
    for i, m in enumerate(items):
        x = i * (w + gap)
        o.append(card(x + 0.5, 0.5, w - 1, h - 1, RADIUS["xl"], th["surface_container"], th["outline_variant"], 0))
        o.append(t(x + PAD, 56, m["value"], 34, 500, th["on_surface"], -0.25))
        o.append(t(x + PAD, 84, m["label"], 11, 500, th["on_surface_variant"], 0.8).replace(
            ">", ' text-transform="uppercase">', 1) if False else
            t(x + PAD, 84, m["label"].upper(), 11, 500, th["on_surface_variant"], 0.8))
    return svg("\n".join(o), W, h, "metrics")


def activity(d, th, dk):
    h = 196
    a = d.get("activity", {})
    days = a.get("days") or [0]
    n = len(days)
    x0, x1 = PAD, W - PAD
    base, top = 156, 78
    mx = (max(days) or 1) * 1.15   # headroom so the peak never touches the top rule
    o = [card(0.5, 0.5, W - 1, h - 1, RADIUS["full"], th["surface_container_low"], th["outline_variant"], 1)]
    o.append(t(PAD, 46, "ACTIVITY", 11, 500, th["on_surface_variant"], 1.6, MONO))
    o.append(t(PAD, 68, a.get("caption", "public commits, rolling window"), 12, 400, th["outline"], 0.3))
    o.append(t(W - PAD, 68, str(a.get("total", 0)), 13, 500, th["primary"], 0.6, MONO, anchor="end"))
    o.append(t(W - PAD, 46, a.get("total_label", "TOTAL"), 11, 500, th["on_surface_variant"], 1.2, MONO, anchor="end"))
    for gy in (top, (top + base) / 2, base):
        o.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{th["outline_variant"]}" '
                 f'stroke-width="1" stroke-dasharray="2 6" opacity="0.7"/>')
    if a.get("total", 0) == 0:
        o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{th["outline"]}" '
                 f'stroke-width="2" stroke-linecap="round" opacity="0.5"/>')
        o.append(t((x0 + x1) / 2, base - 14, a.get("empty", "no public activity in this window"), 12, 400,
                   th["outline"], 0.3, anchor="middle"))
    else:
        step = (x1 - x0) / max(1, n - 1)
        pts = []
        for i, v in enumerate(days):
            x = x0 + i * step
            y = base - (v / mx) * (base - top)
            pts.append((x, y))
        # smooth-ish path: quadratic midpoint smoothing
        p = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for i in range(1, len(pts)):
            px, py = pts[i - 1]
            cx, cy = pts[i]
            mxp, myp = (px + cx) / 2, (py + cy) / 2
            p += f" Q{px:.1f} {py:.1f} {mxp:.1f} {myp:.1f}"
        p += f" L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"
        o.append(f'<linearGradient id="g1" x1="0" y1="{top}" x2="0" y2="{base}" gradientUnits="userSpaceOnUse">'
                 f'<stop offset="0" stop-color="{th["primary"]}" stop-opacity="0.22"/>'
                 f'<stop offset="1" stop-color="{th["primary"]}" stop-opacity="0"/></linearGradient>')
        o.append(f'<path d="{p} L{x1} {base} L{x0} {base} Z" fill="url(#g1)"/>')
        o.append(f'<path d="{p}" fill="none" stroke="{th["primary"]}" stroke-width="2" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="3.2" fill="{th["primary"]}"/>')
    o.append(t(x0, base + 22, a.get("left_label", "90d ago"), 10, 400, th["outline"], 0.3, MONO))
    o.append(t(x1, base + 22, a.get("right_label", "today"), 10, 400, th["outline"], 0.3, MONO, anchor="end"))
    return svg("\n".join(o), W, h, "activity")


def projects(d, th, dk):
    rows = d.get("projects", [])
    rh, gap = 84, 12
    h = max(1, len(rows)) * rh + max(0, len(rows) - 1) * gap
    o = []
    for i, p in enumerate(rows):
        y = i * (rh + gap)
        o.append(card(0.5, y + 0.5, W - 1, rh - 1, RADIUS["xl"], th["surface_container"], th["outline_variant"], 0))
        o.append(f'<circle cx="52" cy="{y + rh / 2:.1f}" r="22" fill="{th["primary_container"]}"/>')
        ini = p.get("initials") or "".join(w[0] for w in re.split(r"[-_ ]+", p["name"]) if w)[:2].upper() or p["name"][:2].upper()
        o.append(t(52, y + rh / 2 + 4.6, ini, 13, 500, th["on_primary_container"], 0.6, MONO, anchor="middle"))
        o.append(t(88, y + 36, p["name"], 16, 500, th["on_surface"], 0.15, MONO))
        tag0 = p.get("tag", "PUBLIC")
        avail = W - PAD - (tw(tag0, 11, 500, 0.8) + 22) - 24 - 88
        o.append(t(88, y + 58, fit(p["desc"], avail, 12.5, 400, 0.2), 12.5, 400, th["on_surface_variant"], 0.2))
        tag = p.get("tag", "PUBLIC")
        cw = tw(tag, 11, 500, 0.8) + 22
        o.append(f'<rect x="{W - PAD - cw:.1f}" y="{y + rh / 2 - 13:.1f}" width="{cw:.1f}" height="26" rx="8" '
                 f'fill="none" stroke="{th["outline_variant"]}" stroke-width="1"/>')
        o.append(t(W - PAD - cw + 11, y + rh / 2 + 4, tag, 11, 500, th["on_surface_variant"], 0.8))
    return svg("\n".join(o), W, h, "projects")


def stack(d, th, dk):
    labels = d.get("stack", [])
    rows, cur, cx, maxx = [], [], PAD, W - PAD
    y = 30
    for lab in labels:
        w = tw(lab, 13, 500, 0.1) + 26
        if cx + w > maxx:
            rows.append((cur, y)); cur, cx, y = [], 0, y + 40
        cur.append((lab, cx, w)); cx += w + 8
    rows.append((cur, y))
    h = y + 32
    o = [t(PAD, 12, "TOOLBOX", 11, 500, th["on_surface_variant"], 0.9)]
    for row, ry in rows:
        for lab, x, w in row:
            o.append(f'<rect x="{x:.1f}" y="{ry}" width="{w:.1f}" height="32" rx="8" fill="none" '
                     f'stroke="{th["outline_variant"]}" stroke-width="1"/>')
            o.append(t(x + 13, ry + 20.6, lab, 13, 500, th["on_surface_variant"], 0.1))
    return svg("\n".join(o), W, h, "stack")


CARDS = dict(hero=hero, metrics=metrics, activity=activity, projects=projects, stack=stack)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data.json")
    ap.add_argument("--out", default="assets")
    a = ap.parse_args()
    data = json.load(open(a.data, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    for name, fn in CARDS.items():
        for scheme, th, dk in (("light", LIGHT, False), ("dark", DARK, True)):
            p = os.path.join(a.out, f"{name}-{scheme}.svg")
            open(p, "w", encoding="utf-8").write(fn(data, th, dk))
            print(f"  {p}  {os.path.getsize(p)}B")


if __name__ == "__main__":
    main()
