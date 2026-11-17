#!/usr/bin/env python3
"""Builds the static README section SVGs in the same visual language as banner/boot/profile-card.
Run from repo root: python3 scripts/gen_static.py"""
import math, os, textwrap

OUT = "assets"
FONT = "font-family=\"'Courier New',Courier,monospace\""
C = dict(bg="#050505", panel="#0b0b0b", line="#1f1f1f", edge="#3a3a3a", card="#2a2a2a", txt="#cfcfcf",
         dim="#6e6e6e", faint="#444", hi="#f2f2f2", acc="#d4d4d4")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def chamfer(x, y, w, h, c=10):
    return f"M{x+c} {y}H{x+w-c}L{x+w} {y+c}V{y+h-c}L{x+w-c} {y+h}H{x+c}L{x} {y+h-c}V{y+c}Z"


def frame(w, h, body, extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>'
            '<pattern id="gr" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#111"/></pattern>'
            '<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="vs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<clipPath id="rc"><rect x="28" y="60" width="844" height="10"/></clipPath><pattern id="hz" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V8" stroke="#171717" stroke-width="3"/></pattern>'
            f'{extra_defs}</defs><g {FONT}><rect width="{w}" height="{h}" fill="{C["bg"]}"/><rect width="{w}" height="{h}" fill="url(#gr)"/>'
            f'<rect y="-60" width="{w}" height="60" fill="url(#vs)"><animate attributeName="y" values="-60;{h}" dur="7s" repeatCount="indefinite"/></rect>'
            f'<path d="{chamfer(2, 2, w-4, h-4, 16)}" fill="none" stroke="{C["edge"]}" stroke-width="2"/>{body}</g></svg>')


def header(title, sub):
    return (f'<rect x="28" y="24" width="8" height="30" fill="{C["acc"]}"/>'
            f'<text x="50" y="48" font-size="24" font-weight="700" fill="{C["hi"]}" letter-spacing="3">{esc(title)}</text>'
            f'<text x="872" y="46" font-size="12" fill="#555" text-anchor="end" letter-spacing="3">{esc(sub)}</text>'
            f'<path d="M28 66H872" stroke="{C["line"]}"/><g clip-path="url(#rc)"><rect y="65" width="160" height="2" fill="url(#sw)"><animate attributeName="x" values="-160;900" dur="3.6s" repeatCount="indefinite"/></rect></g>'
            f'<g fill="{C["acc"]}"><rect x="868" y="62" width="6" height="6" transform="rotate(45 871 65)"/><rect x="25" y="62" width="6" height="6" transform="rotate(45 28 65)"/></g>')


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name, len(svg))


# ---------------------------------------------------------------- WHO
def who():
    b = [header("WHO THE FUCK AM I?", "// you might ask")]
    L = [  # (y, [(text, fill, bold)...])
        (104, [("I'm ", C["txt"], 0), ("V", "#fff", 1), (". I do ", C["txt"], 0), ("offensive security", "#fff", 1), (" and ", C["txt"], 0), ("vulnerability research", "#fff", 1), (",", C["txt"], 0)]),
        (128, [("with ", C["txt"], 0), ("exploit development", "#fff", 1), (" and ", C["txt"], 0), ("malware analysis & development", "#fff", 1), (" next to it", C["txt"], 0)]),
        (152, [("(Holy fuck I do a lot of things).", C["dim"], 0)]),
        (196, [("I'm a ", C["txt"], 0), ("perfectionist", "#fff", 1), (".", C["txt"], 0)]),
        (240, [("I'll probably import all of my projects from my other acc later.", "#8a8a8a", 0)]),
    ]
    b.append(f'<path d="M58 84V258" stroke="{C["line"]}"/>')
    for i, (y, runs) in enumerate(L):
        b.append(f'<text x="28" y="{y}" font-size="11" fill="#3a3a3a">{i+1:02d}</text>')
        t = "".join(f'<tspan fill="{f}"{" font-weight=\"700\"" if bd else ""}>{esc(s)}</tspan>' for s, f, bd in runs)
        b.append(f'<text x="76" y="{y}" font-size="16" xml:space="preserve">{t}</text>')
    b.append(f'<rect x="694" y="228" width="10" height="16" fill="{C["acc"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    b.append(f'<text x="872" y="262" font-size="10" fill="#2e2e2e" text-anchor="end" letter-spacing="2">56 20 // 0xV</text>')
    b.append(f'<g stroke="{C["acc"]}" stroke-width="2" fill="none"><path d="M28 280V268"/><path d="M28 280H40"/><path d="M872 280V268"/><path d="M872 280H860"/></g>')
    write("who.svg", frame(900, 300, "".join(b)))


# ---------------------------------------------------------------- WHAT I DO
ICONS = {
    "cross": '<path d="M0 -21L-19 -14V3Q-19 14 -1 22L1 12L-3 6L2 -3L-4 -10Z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M4 -20L19 -14V3Q19 14 5 21L4 11L0 6L5 -3L-1 -10Z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
    "hex": '<path d="M10 -10A14 14 0 1 0 14 2" fill="none" stroke="{c}" stroke-width="3"/><path d="M10 -10L21 -8L12 -20Z" fill="{c}"/><path d="M-5 -3L-9 1L-5 5M5 -3L1 1L5 5" fill="none" stroke="{c}" stroke-width="2"/>',
    "scan": '<circle cx="-3" cy="-3" r="13" fill="none" stroke="{c}" stroke-width="2"/><path d="M7 7L20 20" stroke="{c}" stroke-width="3"/><path d="M-9 -3H3M-3 -9V3" stroke="{c}" stroke-width="2"/>',
    "break": '<path d="M-16 -16H-2L2 -6L-4 2L4 10L0 16H-16Z" fill="none" stroke="{c}" stroke-width="2"/><path d="M8 -16H18V16H6L10 8L4 0L10 -8Z" fill="none" stroke="{c}" stroke-width="2"/>',
}
WHAT = [
    ("01", "OFFENSIVE SECURITY", "vulnerability research, exploit development, attack-surface analysis.", "cross"),
    ("02", "REVERSE ENGINEERING", "disassembly, debugging, static and dynamic analysis.", "hex"),
    ("03", "MALWARE ANALYSIS", "behavior and structure analysis of binaries.", "scan"),
    ("04", "HOW I LEARN", "I break things to understand and learn so uhm sorry bro (Not sorry.)", "break"),
]


def what():
    b = [header("WHAT I DO", "// includes ?")]
    for i, (n, t, d, ic) in enumerate(WHAT):
        x = 28 + (i % 2) * 432
        y = 90 + (i // 2) * 136
        w, h = 412, 120
        b.append(f'<path d="{chamfer(x, y, w, h, 10)}" fill="{C["panel"]}" stroke="{C["card"]}"/>')
        b.append(f'<text x="{x+18}" y="{y+26}" font-size="11" fill="{C["faint"]}" letter-spacing="3">[{n}]</text>')
        b.append(f'<text x="{x+18}" y="{y+50}" font-size="17" font-weight="700" fill="{C["hi"]}" letter-spacing="2">{t}</text>')
        for k, line in enumerate(textwrap.wrap(d, 40)):
            b.append(f'<text x="{x+18}" y="{y+76+k*18}" font-size="13" fill="#9a9a9a">{esc(line)}</text>')
        b.append(f'<g transform="translate({x+w-52} {y+44})">{ICONS[ic].format(c=C["acc"])}</g>')
        b.append(f'<path d="M{x+18} {y+h-8}H{x+w-18}" stroke="#171717"/><rect x="{x+18}" y="{y+h-9}" width="70" height="2" fill="url(#sw)"><animate attributeName="x" values="{x+18};{x+w-88}" dur="{3+i*.7:.1f}s" repeatCount="indefinite"/></rect>')
    b.append(f'<text x="872" y="372" font-size="10" fill="#2e2e2e" text-anchor="end" letter-spacing="2">4 / 4 MODULES LOADED</text>')
    write("what-i-do.svg", frame(900, 384, "".join(b)))


# ---------------------------------------------------------------- PROJECTS
def lock(x, y, c):
    return (f'<g transform="translate({x} {y})"><path d="M-9 -2V-9A9 9 0 0 1 9 -9V-2" fill="none" stroke="{c}" stroke-width="3"/>'
            f'<rect x="-14" y="-2" width="28" height="22" fill="none" stroke="{c}" stroke-width="2"/><rect x="-3" y="5" width="6" height="8" fill="{c}"/></g>')


def projects():
    b = [header("PROJECTS", "// 4 slots · 0 shipped")]
    b.append(f'<rect x="28" y="86" width="3" height="40" fill="{C["acc"]}"/>')
    b.append(f'<text x="46" y="104" font-size="15" fill="{C["txt"]}">slots are empty <tspan fill="#fff" font-weight="700">on purpose</tspan>.</text>')
    b.append(f'<text x="46" y="124" font-size="15" fill="#8a8a8a">stuff goes here when it\'s perfect for use.</text>')
    for i in range(4):
        x = 28 + (i % 2) * 432
        y = 148 + (i // 2) * 112
        w, h = 412, 96
        b.append(f'<path d="{chamfer(x, y, w, h, 10)}" fill="url(#hz)" stroke="{C["card"]}"/><path d="{chamfer(x+3, y+3, w-6, h-6, 8)}" fill="{C["panel"]}" fill-opacity=".86"/>')
        b.append(lock(x + 46, y + 34, "#8a8a8a"))
        b.append(f'<text x="{x+90}" y="{y+34}" font-size="12" fill="{C["dim"]}" letter-spacing="3">slot_{i+1:02d}</text>')
        b.append(f'<text x="{x+90}" y="{y+60}" font-size="20" font-weight="700" fill="{C["hi"]}" letter-spacing="2">'
                 f'<tspan fill="#555">[</tspan> LOCKED <tspan fill="#555">]</tspan></text>')
        for k, wd in enumerate((150, 96)):
            b.append(f'<rect x="{x+90}" y="{y+72+k*8}" width="{wd}" height="4" fill="#1c1c1c"><animate attributeName="opacity" values="1;.35;1" dur="{2.4+i*.4+k*.3:.1f}s" repeatCount="indefinite"/></rect>')
        b.append(f'<text x="{x+w-16}" y="{y+22}" font-size="10" fill="#333" text-anchor="end" letter-spacing="2">NULL</text>')
    write("projects.svg", frame(900, 376, "".join(b)))


# ---------------------------------------------------------------- TYPING
def typing():
    lines = ["17. Offensive Security and Vulnerability Research.", "Exploit Development. Malware Analysis.",
             "Perfectionist. that's why half my stuff get pushed late.", "I love breaking things."]
    cw, size, slot, type_t = 9.6, 16, 5.0, 1.9
    T = slot * len(lines)
    o = []
    for i, ln in enumerate(lines):
        n = len(ln)
        x0 = (900 - n * cw) / 2
        s0, s1 = i * slot / T, (i * slot + type_t) / T
        e0 = ((i + 1) * slot - .25) / T
        vals, keys = ["0"], ["0"]
        if s0 > 0:
            vals.append("0"); keys.append(f"{s0:.4f}")
        for k in range(1, n + 1):
            vals.append(f"{k*cw:.1f}"); keys.append(f"{s0 + (s1 - s0) * k / n:.4f}")
        vals.append(f"{n*cw:.1f}"); keys.append(f"{e0:.4f}")
        vals.append("0"); keys.append(f"{e0 + .0001:.4f}")
        if keys[-1] != "1":
            vals.append("0"); keys.append("1")
        ck = ([0, e0, 1], [1, 0, 0]) if s0 == 0 else ([0, s0, e0, 1], [0, 1, 0, 0])
        cur = (f'<rect y="14" width="9" height="20" fill="{C["acc"]}" opacity="0"><animate attributeName="opacity" calcMode="discrete" values="{";".join(map(str, ck[1]))}" keyTimes="{";".join(f"{k:.4f}" if k not in (0, 1) else str(k) for k in ck[0])}" dur="{T}s" repeatCount="indefinite"/>'
               f'<animate attributeName="x" calcMode="discrete" values="{";".join(f"{x0+float(v):.1f}" for v in vals)}" keyTimes="{";".join(keys)}" dur="{T}s" repeatCount="indefinite"/></rect>')
        o.append(f'<clipPath id="c{i}"><rect x="{x0:.1f}" y="0" width="0" height="48"><animate attributeName="width" calcMode="discrete" values="{";".join(vals)}" keyTimes="{";".join(keys)}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
                 f'<text x="{x0:.1f}" y="31" font-size="{size}" font-weight="700" fill="#c8c8c8" clip-path="url(#c{i})" xml:space="preserve">{esc(ln)}</text>{cur}')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 48" width="900" height="48"><rect width="900" height="48" fill="#050505"/><g {FONT}>'
           f'<path d="M28 4H872M28 44H872" stroke="{C["line"]}"/>{"".join(o)}</g></svg>')
    write("typing.svg", svg)


# ---------------------------------------------------------------- BADGES
def badges():
    tags = ["OFFENSIVE_SECURITY", "VULN_RESEARCH", "EXPLOIT_DEV", "MALWARE_ANALYSIS", "REVERSE_ENGINEERING", "SELF-HOSTING"]
    cw, gap, pad = 6.8, 8, 12
    widths = [len(t) * cw + 36 for t in tags]
    x = (900 - (sum(widths) + gap * (len(tags) - 1))) / 2
    o = []
    for t, w in zip(tags, widths):
        o.append(f'<path d="{chamfer(x, 6, w, 28, 5)}" fill="#0a0a0a" stroke="#2a2a2a"/><rect x="{x+10}" y="17" width="6" height="6" fill="{C["acc"]}"/>'
                 f'<text x="{x+24}" y="25" font-size="10" font-weight="700" fill="{C["txt"]}" letter-spacing=".8" xml:space="preserve">{t}</text>')
        x += w + gap
    write("badges.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 40" width="900" height="40"><rect width="900" height="40" fill="#050505"/><g {FONT}>{"".join(o)}</g></svg>')


# ---------------------------------------------------------------- CONTACT
def contact():
    b = [header("CONTACT", "// find me")]
    for i, (k, v) in enumerate([("GITHUB", "github.com/03xe"), ("DISCORD", "@03xe")]):
        x = 28 + i * 432
        y = 90
        b.append(f'<path d="{chamfer(x, y, 412, 64, 10)}" fill="{C["panel"]}" stroke="{C["card"]}"/><rect x="{x+18}" y="{y+22}" width="6" height="6" fill="{C["acc"]}"/>'
                 f'<text x="{x+34}" y="{y+28}" font-size="12" fill="{C["dim"]}" letter-spacing="4">{k}</text>'
                 f'<text x="{x+34}" y="{y+50}" font-size="17" font-weight="700" fill="{C["hi"]}">{v}</text>'
                 f'<text x="{x+394}" y="{y+40}" font-size="22" fill="#444" text-anchor="end">&gt;</text>')
    write("contact.svg", frame(900, 176, "".join(b)))


# ---------------------------------------------------------------- FOOTER
def footer():
    paths = []
    for k, (amp, ph, col, dur) in enumerate([(14, 0, "#0c0c0c", 9), (10, 1.3, "#111", 7), (7, 2.6, "#171717", 5)]):
        pts = " ".join(f"{'M' if j == 0 else 'L'}{j*10 - 100} {58 + amp*math.sin(j/6.0 + ph):.1f}" for j in range(0, 130))
        paths.append(f'<path d="{pts}V120H-100Z" fill="{col}"><animateTransform attributeName="transform" type="translate" values="0 0;-{math.pi*6*10:.0f} 0" dur="{dur*2}s" repeatCount="indefinite"/></path>')
    t = (f'<text x="450" y="92" font-size="13" font-weight="700" fill="#cfcfcf" text-anchor="middle" letter-spacing="6">0xVel // 03xe</text>'
         f'<text x="450" y="112" font-size="12" fill="#8a8a8a" text-anchor="middle" letter-spacing="6">I\'m God</text>')
    write("footer.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 120" width="900" height="120"><defs><clipPath id="f"><rect width="900" height="120"/></clipPath></defs><g {FONT}><rect width="900" height="120" fill="{C["bg"]}"/><g clip-path="url(#f)">{"".join(paths)}</g><rect y="0" width="900" height="120" fill="none"/>{t}</g></svg>')


# ---------------------------------------------------------------- SNAKE (placeholder; snk overwrites)
def snake_placeholder():
    cells = "".join(f'<rect x="{28+i*16}" y="{48+j*16}" width="12" height="12" fill="#{"1a1a1a" if (i*j) % 5 else "2a2a2a"}"/>' for i in range(52) for j in range(7))
    t = f'<text x="450" y="34" font-size="11" fill="#555" text-anchor="middle" letter-spacing="4">SNAKE WARMING UP // RUNS AFTER FIRST WORKFLOW</text>'
    write("snake.svg", frame(900, 176, t + cells))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    who(); what(); projects(); typing(); badges(); contact(); footer(); snake_placeholder()
